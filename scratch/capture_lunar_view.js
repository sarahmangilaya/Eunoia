const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9278', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_lunar_' + Date.now()
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9278/json', (res) => {
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

        // Look at Lunar Observatory North Wall
        await send('Runtime.evaluate', {
          expression: `
            camera.position.set(-37.0, 1.8, 9.5);
            camera.rotation.set(0.04, -Math.PI, 0, 'YXZ');
          `
        });
        await new Promise(r => setTimeout(r, 1000));
        let snap1 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/lunar_final_north.png', Buffer.from(snap1.data, 'base64'));

        // Look at Wing IV Cinema Atrium
        await send('Runtime.evaluate', {
          expression: `
            camera.position.set(0.0, 1.8, 59.0);
            camera.rotation.set(0.04, -0.65, 0, 'YXZ');
          `
        });
        await new Promise(r => setTimeout(r, 1000));
        let snap2 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/wing4_final_atrium.png', Buffer.from(snap2.data, 'base64'));

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

