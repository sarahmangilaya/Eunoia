const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9266', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_wash_' + Date.now()
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9266/json', (res) => {
    let d = ''; res.on('data', x => d += x);
    res.on('end', async () => {
      const t = JSON.parse(d).filter(x => x.type === 'page')[0];
      const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 1;
      const send = (method, params = {}) => new Promise(r => { const i = id++; const h = e => { const m = JSON.parse(e.data); if (m.id === i) { ws.removeEventListener('message', h); r(m.result); } }; ws.addEventListener('message', h); ws.send(JSON.stringify({ id: i, method, params })); });

      ws.onopen = async () => {
        await send('Page.enable'); await send('Runtime.enable');
        await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 3500));
        await send('Runtime.evaluate', { expression: "document.getElementById('btnEnter')?.click()" });
        await new Promise(r => setTimeout(r, 3000));

        // Position camera in Wing I looking at the wall with exhibits
        // Viewpoint looking directly at a painting on the wall
        await send('Runtime.evaluate', {
          expression: `
            camera.position.set(11.5, 1.9, 1.8);
            camera.rotation.set(0.08, 0, 0, 'YXZ');
          `
        });
        await new Promise(r => setTimeout(r, 1000));

        let snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/test_wash_default.png', Buffer.from(snap.data, 'base64'));

        // Check the wall wash mesh in wing I
        const info = await send('Runtime.evaluate', {
          expression: `(() => {
            let washMesh = null;
            wingI_group.traverse(m => {
              if (m.isMesh && m.material && m.material.opacity === 0.68) washMesh = m;
            });
            if (!washMesh) return 'not found';
            return {
              visible: washMesh.visible,
              pos: washMesh.position,
              vertCount: washMesh.geometry.attributes.position.count,
              box: (() => {
                washMesh.geometry.computeBoundingBox();
                return washMesh.geometry.boundingBox;
              })()
            };
          })()`
        });
        console.log('Wash mesh info:', info.result.value);

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

