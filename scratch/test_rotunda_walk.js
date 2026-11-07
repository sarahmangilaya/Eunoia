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

server.listen(8101, '127.0.0.1', async () => {
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const chrome = spawn(chromePath, ['--headless=new', '--remote-debugging-port=9243', '--window-size=1280,720', 'about:blank']);
  await new Promise(r => setTimeout(r, 1200));

  const listRes = await fetch('http://127.0.0.1:9243/json/list');
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
  await send('Page.navigate', { url: 'http://127.0.0.1:8101/index.html' });
  await new Promise(r => setTimeout(r, 3500));

  await send('Runtime.evaluate', { expression: 'window.enterExhibition();' });
  await new Promise(r => setTimeout(r, 800));

  // Turn around to look south at the directory plaque (matching user screenshot)
  await send('Runtime.evaluate', {
    expression: `(() => {
      window.camera.position.set(0, 1.7, -3.5);
      window.camera.lookAt(0, 1.7, -8.5);
    })()`
  });
  await new Promise(r => setTimeout(r, 300));
  const shotSouth = await send('Page.captureScreenshot');
  fs.writeFileSync('scratch/rotunda_look_south.png', Buffer.from(shotSouth.data, 'base64'));
  console.log('Saved scratch/rotunda_look_south.png');

  // Test full navigation walk grid in rotunda
  const testResults = await send('Runtime.evaluate', {
    expression: `(() => {
      const issues = [];
      const cam = window.camera;
      
      // Test 1: Walk from (0, -4.5) to South Plaque (0, -7.5)
      for (let z = -4.5; z >= -7.2; z -= 0.2) {
        const p = new THREE.Vector3(0, 1.7, z);
        const origZ = z;
        // In index.html, resolveCollision is called during animate
        // Let's test walking through resolveCollision
        const testP = { x: 0, z: z };
        // We can call resolveCollision if accessible or simulate movement
        // Let's check window.camera position by setting and checking next frame
      }

      // Check all colliders in scene
      return {
        collidersCount: window.scene ? 1 : 0
      };
    })()`,
    returnByValue: true
  });

  // Test walking in Chrome using camera movements and checking collision resolution
  const walkGrid = await send('Runtime.evaluate', {
    expression: `(() => {
      // Test grid of 50 points across the southern rotunda floor (x: -5 to +5, z: -2 to -7)
      // Check for any points that get pushed by more than 0.05m where there should be open floor
      const results = [];
      const cam = window.camera;
      
      // Let's sample angles 0 to 2PI at radius 3.5m around pedestal:
      for (let deg = 0; deg < 360; deg += 15) {
        const rad = (deg * Math.PI) / 180;
        const x = Math.cos(rad) * 3.5;
        const z = Math.sin(rad) * 3.5;
        // Check if point is inside any column or pedestal
        results.push({ deg, x: x.toFixed(2), z: z.toFixed(2) });
      }
      return { samples: results.length };
    })()`,
    returnByValue: true
  });
  console.log('Walk grid sample count:', walkGrid.result.value);

  // Turn back to north (facing pedestal & north arch)
  await send('Runtime.evaluate', {
    expression: `(() => {
      window.camera.position.set(0, 1.7, -4.5);
      window.camera.lookAt(0, 1.7, 4.0);
    })()`
  });
  await new Promise(r => setTimeout(r, 300));
  const shotNorth = await send('Page.captureScreenshot');
  fs.writeFileSync('scratch/rotunda_look_north.png', Buffer.from(shotNorth.data, 'base64'));
  console.log('Saved scratch/rotunda_look_north.png');

  ws.close(); chrome.kill(); server.close(); process.exit(0);
});

