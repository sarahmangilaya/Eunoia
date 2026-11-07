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
    res.writeHead(200, {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': mime
    });
    fs.createReadStream(filePath).pipe(res);
  } catch(e) { res.writeHead(500); res.end(e.message); }
});

server.listen(8098, '127.0.0.1', async () => {
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const chrome = spawn(chromePath, ['--headless=new', '--remote-debugging-port=9240', '--window-size=1280,720', 'about:blank']);
  await new Promise(r => setTimeout(r, 1200));

  const listRes = await fetch('http://127.0.0.1:9240/json/list');
  const tabs = await listRes.json();
  const ws = new WebSocket(tabs[0].webSocketDebuggerUrl);
  let msgId = 1; const pending = new Map();
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
    if (msg.method === 'Runtime.consoleAPICalled') {
      console.log('CONSOLE:', msg.params.args.map(a => a.value || a.description || JSON.stringify(a)).join(' '));
    }
  };
  await new Promise(resolve => ws.onopen = resolve);
  const send = (method, params = {}) => new Promise((resolve) => {
    const id = msgId++; pending.set(id, (res) => resolve(res.result));
    ws.send(JSON.stringify({ id, method, params }));
  });
  await send('Runtime.enable');
  await send('Page.enable');
  await send('Page.navigate', { url: 'http://127.0.0.1:8098/index.html' });
  await new Promise(r => setTimeout(r, 3500));

  await send('Runtime.evaluate', { expression: 'window.enterExhibition();' });
  await new Promise(r => setTimeout(r, 800));

  console.log('Teleporting to project-36...');
  await send('Runtime.evaluate', {
    expression: `window.teleportToExhibit('project-36-drawing-2-plate-8-character-png');`
  });

  await new Promise(r => setTimeout(r, 2000));

  const checkInfo = await send('Runtime.evaluate', {
    expression: `(() => {
      const mesh = window.exhibitMeshes.find(m => m.userData.exhibit.id === 'project-36-drawing-2-plate-8-character-png');
      const map = mesh ? mesh.material.map : null;
      return {
        id: mesh.userData.exhibit.id,
        mapIsCanvasTexture: map ? map.isCanvasTexture : null,
        mapIsTexture: map ? map.isTexture : null,
        imgSrc: map && map.image ? map.image.src : null,
        imgWidth: map && map.image ? map.image.width : null,
        imgHeight: map && map.image ? map.image.height : null,
        version: map ? map.version : null
      };
    })()`,
    returnByValue: true
  });

  console.log('Check info:', JSON.stringify(checkInfo.result.value, null, 2));

  const shot = await send('Page.captureScreenshot');
  fs.writeFileSync('scratch/verified_real_art_36.png', Buffer.from(shot.data, 'base64'));
  console.log('Saved scratch/verified_real_art_36.png');

  ws.close(); chrome.kill(); server.close(); process.exit(0);
});

