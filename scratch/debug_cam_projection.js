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

server.listen(8099, '127.0.0.1', async () => {
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const chrome = spawn(chromePath, ['--headless=new', '--remote-debugging-port=9241', '--window-size=1280,720', 'about:blank']);
  await new Promise(r => setTimeout(r, 1200));

  const listRes = await fetch('http://127.0.0.1:9241/json/list');
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
  await send('Page.navigate', { url: 'http://127.0.0.1:8099/index.html' });
  await new Promise(r => setTimeout(r, 3500));

  await send('Runtime.evaluate', { expression: 'window.enterExhibition();' });
  await new Promise(r => setTimeout(r, 800));

  await send('Runtime.evaluate', {
    expression: `window.teleportToExhibit('project-36-drawing-2-plate-8-character-png');`
  });
  await new Promise(r => setTimeout(r, 2000));

  const debugInfo = await send('Runtime.evaluate', {
    expression: `(() => {
      const ex36 = window.exhibitMeshes.find(m => m.userData.exhibit.id === 'project-36-drawing-2-plate-8-character-png');
      const cam = window.camera;
      
      // Project ex36 world position into screen coords
      ex36.updateWorldMatrix(true, false);
      const wp = new THREE.Vector3();
      ex36.getWorldPosition(wp);
      
      const screenPos = wp.clone().project(cam);
      // Normalized Device Coordinates to pixel coords
      const pixelX = (screenPos.x * 0.5 + 0.5) * window.innerWidth;
      const pixelY = (-(screenPos.y * 0.5) + 0.5) * window.innerHeight;

      // Group world position
      const groupWp = new THREE.Vector3();
      ex36.userData.group.getWorldPosition(groupWp);

      // Frustum check
      const frustum = new THREE.Frustum();
      const projScreenMatrix = new THREE.Matrix4();
      projScreenMatrix.multiplyMatrices(cam.projectionMatrix, cam.matrixWorldInverse);
      frustum.setFromProjectionMatrix(projScreenMatrix);
      const inFrustum = frustum.containsPoint(wp);

      return {
        camPos: { x: cam.position.x, y: cam.position.y, z: cam.position.z },
        camRot: { x: cam.rotation.x, y: cam.rotation.y, z: cam.rotation.z },
        ex36WorldPos: { x: wp.x, y: wp.y, z: wp.z },
        groupWorldPos: { x: groupWp.x, y: groupWp.y, z: groupWp.z },
        screenPos: { x: screenPos.x, y: screenPos.y, z: screenPos.z },
        pixelX, pixelY,
        inFrustum,
        windowSize: { w: window.innerWidth, h: window.innerHeight }
      };
    })()`,
    returnByValue: true
  });

  console.log('DEBUG INFO:', JSON.stringify(debugInfo.result.value, null, 2));

  ws.close(); chrome.kill(); server.close(); process.exit(0);
});

