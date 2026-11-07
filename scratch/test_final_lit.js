const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9244', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_final_check'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9244/json', (res) => {
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
        await sleep(3500);
        await send('Runtime.evaluate', {
          expression: "document.getElementById('btnEnter')?.click(); setTimeout(()=>document.getElementById('lobby')?.remove(),300)"
        });
        await sleep(4000);

        // 1. Wing I Traditional Salon
        await send('Runtime.evaluate', {
          expression: "camera.position.set(52.0, 1.8, 12.0); camera.rotation.set(-0.02, 0.0, 0, 'YXZ');"
        });
        await sleep(1500);
        const s1 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/final_wing1_traditional_lit.png', Buffer.from(s1.data, 'base64'));

        // 2. Wing IV Cinema Atrium
        await send('Runtime.evaluate', {
          expression: "camera.position.set(3.5, 1.7, 57.0); camera.rotation.set(-0.02, 1.15, 0, 'YXZ');"
        });
        await sleep(1500);
        const s2 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/final_wing4_cinema_lit.png', Buffer.from(s2.data, 'base64'));

        console.log('Final screenshots saved');
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

