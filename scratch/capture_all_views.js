const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9255', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_views_' + Date.now()
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9255/json', (res) => {
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

        const views = [
          { name: 'refined_wing1_hall', pos: [12, 1.7, 2.0], rot: [0.05, -Math.PI / 2 - 0.35, 0] },
          { name: 'refined_close_art', pos: [13.2, 1.7, 0.2], rot: [0.02, -Math.PI / 2 + 0.1, 0] },
          { name: 'refined_wing2_roomB', pos: [17.5, 1.7, 14.0], rot: [-0.02, -1.25, 0] },
          { name: 'refined_wing2_char3d', pos: [0, 1.7, 20.0], rot: [0.0, 0.0, 0] },
          { name: 'refined_wing4_cinema', pos: [0, 1.7, 54.0], rot: [0.04, 0.0, 0] }
        ];

        for (const v of views) {
          await send('Runtime.evaluate', {
            expression: `camera.position.set(${v.pos[0]}, ${v.pos[1]}, ${v.pos[2]}); camera.rotation.set(${v.rot[0]}, ${v.rot[1]}, ${v.rot[2]}, 'YXZ');`
          });
          await sleep(1500);
          const s = await send('Page.captureScreenshot', { format: 'png' });
          fs.writeFileSync('scratch/' + v.name + '.png', Buffer.from(s.data, 'base64'));
          console.log('Captured:', v.name);
        }

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

