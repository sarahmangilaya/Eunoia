const { spawn } = require('child_process');
const http = require('http');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9229', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_depth_check2'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9229/json', (res) => {
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
      ws.onopen = async () => {
        await send('Page.enable'); await send('Runtime.enable');
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await sleep(3000);
        const evalRes = await send('Runtime.evaluate', {
          expression: `(() => {
            const walls = [];
            wingII_group.traverse(c => {
              if (c.geometry && c.geometry.type === 'BoxGeometry') {
                c.geometry.computeBoundingBox();
                const b = c.geometry.boundingBox.clone().applyMatrix4(c.matrixWorld);
                if (b.max.y > 4.0 && (b.max.x - b.min.x > 3.0 || b.max.z - b.min.z > 3.0)) {
                  walls.push({
                    pos: { x: c.position.x.toFixed(2), y: c.position.y.toFixed(2), z: c.position.z.toFixed(2) },
                    min: { x: b.min.x.toFixed(2), z: b.min.z.toFixed(2) },
                    max: { x: b.max.x.toFixed(2), z: b.max.z.toFixed(2) }
                  });
                }
              }
            });
            let poolMesh = null;
            wingII_group.traverse(c => {
              if (c.material && c.material.blending === THREE.AdditiveBlending) poolMesh = c;
            });
            const poolVerts = [];
            if (poolMesh) {
              const pos = poolMesh.geometry.attributes.position;
              for (let i = 0; i < Math.min(pos.count, 16); i++) {
                poolVerts.push({ x: pos.getX(i).toFixed(3), y: pos.getY(i).toFixed(3), z: pos.getZ(i).toFixed(3) });
              }
            }
            return { wallCount: walls.length, walls: walls.slice(0, 10), poolVerts };
          })()`,
          returnByValue: true
        });
        console.log('DEPTH EVAL:', JSON.stringify(evalRes, null, 2));
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();
