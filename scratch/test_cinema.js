const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9233', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_cinema_test'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9233/json', (res) => {
    let d = ''; res.on('data', x => d += x);
    res.on('end', async () => {
      const t = JSON.parse(d).filter(x => x.type === 'page')[0];
      const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 1;
      const send = (method, params = {}) => new Promise(r => {
        const i = id++;
        const h = e => { const m = JSON.parse(e.data); if (m.id === i) { ws.removeEventListener('message', h); r(m.result); } };
        ws.addEventListener('message', h);
        ws.send(JSON.stringify({ id: i, method, params }));
      });
      const sleep = ms => new Promise(r => setTimeout(r, ms));
      ws.onopen = async () => {
        await send('Page.enable'); await send('Runtime.enable');
        await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await sleep(3000);
        await send('Runtime.evaluate', {
          expression: `(() => {
            document.getElementById('btnEnter')?.click();
            document.getElementById('lobby')?.remove();
            // In Cinema Atrium (x=0, z=60), look West towards portProd (-8, 60) and slightly north
            camera.position.set(3.5, 1.7, 57.0);
            camera.rotation.set(-0.02, 1.15, 0, 'YXZ');
          })()`
        });
        await sleep(1500);
        const s = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/cinema_view_test.png', Buffer.from(s.data, 'base64'));
        console.log('Saved scratch/cinema_view_test.png');
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

