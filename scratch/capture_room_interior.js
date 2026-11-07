const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9277', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_room_int_' + Date.now()
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9277/json', (res) => {
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
        await new Promise(r => setTimeout(r, 2000));

        // Look at II_interior south wall
        await send('Runtime.evaluate', {
          expression: `
            camera.position.set(13.0, 1.8, 14.5);
            camera.rotation.set(0.06, 0, 0, 'YXZ');
          `
        });
        await new Promise(r => setTimeout(r, 1000));
        let snap1 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/snap_room_interior_south.png', Buffer.from(snap1.data, 'base64'));

        // Look at Wing III lunar observatory
        await send('Runtime.evaluate', {
          expression: `
            camera.position.set(-37.0, 1.8, 12.0);
            camera.rotation.set(0.04, 0, 0, 'YXZ');
          `
        });
        await new Promise(r => setTimeout(r, 1000));
        let snap2 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/snap_lunar_obs.png', Buffer.from(snap2.data, 'base64'));

        // Look at Wing I fine arts promenade looking down the wall
        await send('Runtime.evaluate', {
          expression: `
            camera.position.set(13.5, 1.8, 2.5);
            camera.rotation.set(0.06, 0.40, 0, 'YXZ');
          `
        });
        await new Promise(r => setTimeout(r, 1000));
        let snap3 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/snap_wing1_promenade.png', Buffer.from(snap3.data, 'base64'));

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

