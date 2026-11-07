const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9261', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_test_rooms2_' + Date.now()
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9261/json', (res) => {
    let d = ''; res.on('data', x => d += x);
    res.on('end', async () => {
      const t = JSON.parse(d).filter(x => x.type === 'page')[0];
      const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 1;
      const send = (method, params = {}) => new Promise(r => { const i = id++; const h = e => { const m = JSON.parse(e.data); if (m.id === i) { ws.removeEventListener('message', h); r(m.result); } }; ws.addEventListener('message', h); ws.send(JSON.stringify({ id: i, method, params })); });
      const sleep = ms => new Promise(r => setTimeout(r, ms));

      ws.onopen = async () => {
        await send('Page.enable'); await send('Runtime.enable');
        await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await sleep(3500);
        await send('Runtime.evaluate', { expression: "document.getElementById('btnEnter')?.click(); setTimeout(()=>document.getElementById('lobby')?.remove(),300)" });
        await sleep(6500);

        // 1. Room: Lunar (Attachment 1 angle - looking North into the room at back wall)
        await send('Runtime.evaluate', {
          expression: `camera.position.set(-37.0, 1.7, 9.5); camera.rotation.set(-0.04, Math.PI, 0, 'YXZ');`
        });
        await sleep(2000);
        let s = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/fixed_room_lunar_wide.png', Buffer.from(s.data, 'base64'));
        console.log('Captured fixed_room_lunar_wide.png');

        // 2. Room: Wildlife (Attachment 2 angle - looking South into the room at back wall)
        await send('Runtime.evaluate', {
          expression: `camera.position.set(-37.0, 1.7, -9.5); camera.rotation.set(-0.04, 0, 0, 'YXZ');`
        });
        await sleep(2000);
        s = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/fixed_room_wildlife_wide.png', Buffer.from(s.data, 'base64'));
        console.log('Captured fixed_room_wildlife_wide.png');

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();
