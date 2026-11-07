const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9242', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_final_sweep'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9242/json', (res) => {
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

        const views = [
          { name: 'final_wing1_promenade', x: 20.0, z: 0.0, yaw: Math.PI / 2, pitch: 0.04 },
          { name: 'final_wing3_boulevard', x: -25.0, z: 0.0, yaw: -Math.PI / 2, pitch: 0.04 },
          { name: 'final_wing4_storyboards', x: 0.0, z: 76.0, yaw: Math.PI, pitch: 0.04 }
        ];

        for (const v of views) {
          await send('Runtime.evaluate', {
            expression: `camera.position.set(${v.x}, 1.7, ${v.z}); camera.rotation.set(${v.pitch}, ${v.yaw}, 0, 'YXZ');`
          });
          await sleep(1500);
          const s = await send('Page.captureScreenshot', { format: 'png' });
          fs.writeFileSync(`scratch/${v.name}.png`, Buffer.from(s.data, 'base64'));
          console.log(`Saved scratch/${v.name}.png`);
        }

        console.log('FINAL ERRORS:', errors);
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

