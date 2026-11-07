import { spawn } from 'child_process';
import http from 'http';
import fs from 'fs';
import path from 'path';

const server = http.createServer((req, res) => {
  let urlPath = decodeURIComponent(req.url.split('?')[0]);
  let filePath = path.join(process.cwd(), urlPath === '/' ? 'index.html' : urlPath);
  try {
    if (!fs.existsSync(filePath)) { res.writeHead(404); res.end('404'); return; }
    const ext = path.extname(filePath).toLowerCase();
    const mime = ext === '.png' ? 'image/png' : ext === '.jpg' || ext === '.jpeg' ? 'image/jpeg' : ext === '.mp4' ? 'video/mp4' : 'text/html';
    res.writeHead(200, { 'Access-Control-Allow-Origin': '*', 'Content-Type': mime });
    fs.createReadStream(filePath).pipe(res);
  } catch(e) { res.writeHead(500); res.end(e.message); }
});

server.listen(8100, '127.0.0.1', async () => {
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const chrome = spawn(chromePath, ['--headless=new', '--remote-debugging-port=9242', '--window-size=1280,720', 'about:blank']);
  await new Promise(r => setTimeout(r, 1200));

  const listRes = await fetch('http://127.0.0.1:9242/json/list');
  const tabs = await listRes.json();
  const ws = new WebSocket(tabs[0].webSocketDebuggerUrl);
  let msgId = 1; const pending = new Map();
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  };
  await new Promise(resolve => ws.onopen = resolve);
  const send = (method, params = {}) => new Promise((resolve) => {
    const id = msgId++; pending.set(id, (res) => resolve(res.result));
    ws.send(JSON.stringify({ id, method, params }));
  });
  await send('Runtime.enable');
  await send('Page.enable');
  await send('Page.navigate', { url: 'http://127.0.0.1:8100/index.html' });
  await new Promise(r => setTimeout(r, 4500));

  await send('Runtime.evaluate', { expression: 'window.enterExhibition();' });
  await new Promise(r => setTimeout(r, 800));

  const exhibitsToTest = [
    'project-35-character-design-draft-png',
    'project-8-modern-house-design-png',
    'project-59-20260302-205738-jpg',
    'project-89-the-wind-rises-story-boarding-3-png'
  ];

  for (const exId of exhibitsToTest) {
    console.log('Testing', exId);
    await send('Runtime.evaluate', {
      expression: `window.teleportToExhibit('${exId}');`
    });
    await new Promise(r => setTimeout(r, 1500));

    const check = await send('Runtime.evaluate', {
      expression: `(() => {
        const mesh = window.exhibitMeshes.find(m => m.userData.exhibit.id === '${exId}');
        const map = mesh ? mesh.material.map : null;
        return {
          id: '${exId}',
          isTexture: map && map.isTexture && !map.isCanvasTexture,
          width: map && map.image ? (map.image.naturalWidth || map.image.width) : null,
          height: map && map.image ? (map.image.naturalHeight || map.image.height) : null,
          src: map && map.image ? map.image.src : null
        };
      })()`,
      returnByValue: true
    });
    console.log('Result for', exId, ':', check.result.value);

    const shot = await send('Page.captureScreenshot');
    fs.writeFileSync(`scratch/test_${exId.slice(0, 15)}.png`, Buffer.from(shot.data, 'base64'));
  }

  // Also verify all hung exhibits status
  const allStatus = await send('Runtime.evaluate', {
    expression: `(() => {
      const results = [];
      for (const m of window.exhibitMeshes) {
        const ex = m.userData.exhibit;
        const map = m.material.map;
        results.push({
          id: ex.id,
          mediaType: ex.mediaType,
          isRealTexture: map && map.isTexture && !map.isCanvasTexture,
          isCanvas: map && map.isCanvasTexture,
          imgW: map && map.image ? (map.image.naturalWidth || map.image.width) : null,
          imgH: map && map.image ? (map.image.naturalHeight || map.image.height) : null
        });
      }
      return {
        total: results.length,
        realTextures: results.filter(r => r.isRealTexture || r.mediaType === 'video').length,
        canvasFallbacks: results.filter(r => r.isCanvas).length
      };
    })()`,
    returnByValue: true
  });

  console.log('ALL EXHIBITS SUMMARY:', JSON.stringify(allStatus.result.value, null, 2));

  ws.close(); chrome.kill(); server.close(); process.exit(0);
});

