const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9243', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_downward_test'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9243/json', (res) => {
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
      const errors = [];
      ws.addEventListener('message', (e) => {
        const m = JSON.parse(e.data);
        if (m.method === 'Runtime.exceptionThrown') {
          const d = m.params.exceptionDetails;
          const txt = d.exception?.description || d.text;
          if (!/pointer lock|Pointer Lock/i.test(txt)) errors.push(txt);
        }
      });

      ws.onopen = async () => {
        await send('Page.enable'); await send('Runtime.enable');
        await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await sleep(3500);
        await send('Runtime.evaluate', {
          expression: "document.getElementById('btnEnter')?.click(); setTimeout(()=>document.getElementById('lobby')?.remove(),300)"
        });
        await sleep(4000);

        // Position camera inside Room B looking East at the 4 paintings
        await send('Runtime.evaluate', {
          expression: "camera.position.set(9.0, 1.7, 17.5); camera.rotation.set(0.04, -Math.PI / 2, 0, 'YXZ');"
        });
        await sleep(2000);
        const s1 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/roomB_downward_spotlights.png', Buffer.from(s1.data, 'base64'));
        console.log('Saved scratch/roomB_downward_spotlights.png');

        // Also take a closer, angled view of one of the paintings (e.g. bed painting)
        await send('Runtime.evaluate', {
          expression: "camera.position.set(18.0, 1.9, 13.5); camera.rotation.set(-0.05, -1.2, 0, 'YXZ');"
        });
        await sleep(1500);
        const s2 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/roomB_angled_art_spotlight.png', Buffer.from(s2.data, 'base64'));
        console.log('Saved scratch/roomB_angled_art_spotlight.png');

        console.log('ERRORS:', errors);
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

