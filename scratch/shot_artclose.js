const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9251', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_artclose'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9251/json', (res) => {
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
        await sleep(6000);
        const chk = await send('Runtime.evaluate', { expression: "(()=>{const m=exhibitMeshes[0].material;return [!!m.lightMap,m.lightMapIntensity]})()", returnByValue: true });
        console.log('lightmap on art:', JSON.stringify(chk.result.value));
        const views = [
          ['close_wing1', 14.5, 2.2, -0.25 - Math.PI / 2 + Math.PI, 0.02],
          ['close_roomB', 17.5, 14.0, -1.25, -0.02],
          ['close_wing1_hall', 12, 2.0, -Math.PI / 2 - 0.35, 0.05]
        ];
        for (const [n, x, z, yaw, pitch] of views) {
          await send('Runtime.evaluate', { expression: `camera.position.set(${x},1.7,${z}); camera.rotation.set(${pitch},${yaw},0,'YXZ');` });
          await sleep(1500);
          const s = await send('Page.captureScreenshot', { format: 'png' });
          fs.writeFileSync('scratch/' + n + '.png', Buffer.from(s.data, 'base64'));
        }
        chrome.kill(); process.exit(0);
      };
    });
  });
})();

