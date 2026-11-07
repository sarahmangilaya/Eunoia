const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9263', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_track_' + Date.now()
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9263/json', (res) => {
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
          // 1. Oblique wall view matching the user's reference photo angle:
          // In Wing I along the wall looking obliquely at the paintings, track lights, and scallops
          { name: 'track_ref_angle_wing1', pos: [11.8, 1.7, 2.8], rot: [0.08, -Math.PI / 2 - 0.40, 0] },
          // 2. Wing II white wall gallery (closest wall material to the reference photo)
          { name: 'track_ref_angle_wing2', pos: [14.0, 1.7, 13.0], rot: [0.06, -1.35, 0] },
          // 3. Wing III Boulevard long wall of street photography
          { name: 'track_ref_angle_wing3', pos: [-18.0, 1.7, 1.5], rot: [0.06, -2.6, 0] },
          // 4. Wildlife room with new deduped even spacing
          { name: 'track_wildlife_room', pos: [-37.0, 1.7, -9.5], rot: [-0.02, 0, 0] }
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

