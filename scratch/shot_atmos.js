const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9250', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_atmos'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9250/json', (res) => {
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
          const dd = m.params.exceptionDetails;
          const txt = dd.exception?.description || dd.text;
          if (!/pointer lock/i.test(txt)) errors.push(txt);
        }
      });
      ws.onopen = async () => {
        await send('Page.enable'); await send('Runtime.enable');
        await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await sleep(3500);
        await send('Runtime.evaluate', { expression: "document.getElementById('btnEnter')?.click(); setTimeout(()=>document.getElementById('lobby')?.remove(),300)" });
        await sleep(5000);
        const views = [
          ['atm_wing1_hall', 12, 2.0, -Math.PI / 2 - 0.35, 0.05],
          ['atm_wing2_hall', 0, 12, Math.PI + 0.0, 0.08],
          ['atm_roomB', 9, 17.5, -Math.PI / 2, 0.04],
          ['atm_rotunda', 0, -5, Math.PI, 0.1],
          ['atm_wing4', 0, 74, Math.PI, 0.06],
          ['atm_wing3', -12, 0, Math.PI / 2, 0.05]
        ];
        for (const [n, x, z, yaw, pitch] of views) {
          await send('Runtime.evaluate', { expression: `camera.position.set(${x},1.7,${z}); camera.rotation.set(${pitch},${yaw},0,'YXZ'); if (window.updateWingCulling) updateWingCulling();` });
          await sleep(1500);
          const s = await send('Page.captureScreenshot', { format: 'png' });
          fs.writeFileSync('scratch/' + n + '.png', Buffer.from(s.data, 'base64'));
        }
        const info = await send('Runtime.evaluate', { expression: "JSON.stringify(renderer.info.render)", returnByValue: true });
        console.log('render info', info.result.value, 'errors', errors);
        chrome.kill(); process.exit(0);
      };
    });
  });
})();

