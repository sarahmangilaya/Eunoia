const { spawn } = require('child_process');
const http = require('http');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9236', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_overlap_check3'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9236/json', (res) => {
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
            const signs = [];
            scene.traverse(c => {
              if (c.isMesh && c.geometry && c.geometry.type === 'PlaneGeometry' && c.material?.map?.image) {
                if (!c.geometry.boundingBox) c.geometry.computeBoundingBox();
                c.updateWorldMatrix(true, false);
                const b = c.geometry.boundingBox.clone().applyMatrix4(c.matrixWorld);
                signs.push({
                  pos: { x: c.position.x, y: c.position.y, z: c.position.z },
                  box: b,
                  center: b.getCenter(new THREE.Vector3()),
                  size: b.getSize(new THREE.Vector3()),
                  w: c.geometry.parameters?.width,
                  h: c.geometry.parameters?.height
                });
              }
            });

            // Find signs that are very close to each other (distance < 0.3)
            const closeSigns = [];
            for (let i = 0; i < signs.length; i++) {
              for (let j = i + 1; j < signs.length; j++) {
                const s1 = signs[i], s2 = signs[j];
                const dist = s1.center.distanceTo(s2.center);
                if (dist < 0.5) {
                  closeSigns.push({
                    dist: dist.toFixed(3),
                    s1: { center: s1.center, size: s1.size },
                    s2: { center: s2.center, size: s2.size }
                  });
                }
              }
            }
            return { signCount: signs.length, closeSigns };
          })()`,
          returnByValue: true
        });
        console.log('CLOSE SIGNS EVAL:', JSON.stringify(evalRes, null, 2));
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();
