const { spawn } = require('child_process');
const http = require('http');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9241', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_debug_pools'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9241/json', (res) => {
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
        await sleep(3500);

        const res = await send('Runtime.evaluate', {
          expression: `(() => {
            let poolMesh = null;
            wingII_group.traverse(c => {
              if (c.material && c.material.blending === THREE.AdditiveBlending) poolMesh = c;
            });
            if (!poolMesh) return { error: 'No pool mesh found in wingII_group' };
            
            // Check position attribute of poolMesh
            const pos = poolMesh.geometry.attributes.position;
            const norm = poolMesh.geometry.attributes.normal;
            const uvs = poolMesh.geometry.attributes.uv;
            
            // Find vertices near x=22 (the east wall of Room B)
            const eastWallVerts = [];
            for (let i = 0; i < pos.count; i++) {
              const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i);
              if (Math.abs(x - 22.0) < 1.0) {
                eastWallVerts.push({
                  idx: i,
                  x: x.toFixed(3), y: y.toFixed(3), z: z.toFixed(3),
                  nx: norm ? norm.getX(i).toFixed(3) : 'none',
                  ny: norm ? norm.getY(i).toFixed(3) : 'none',
                  nz: norm ? norm.getZ(i).toFixed(3) : 'none',
                  u: uvs ? uvs.getX(i).toFixed(3) : 'none',
                  v: uvs ? uvs.getY(i).toFixed(3) : 'none'
                });
              }
            }
            return {
              totalVerts: pos.count,
              eastWallVertCount: eastWallVerts.length,
              sampleEastVerts: eastWallVerts.slice(0, 16),
              poolMeshVisible: poolMesh.visible,
              poolMeshParent: poolMesh.parent === wingII_group ? 'wingII_group' : 'other',
              mat: {
                transparent: poolMesh.material.transparent,
                opacity: poolMesh.material.opacity,
                blending: poolMesh.material.blending,
                depthWrite: poolMesh.material.depthWrite,
                side: poolMesh.material.side,
                hasMap: !!poolMesh.material.map,
                mapSize: poolMesh.material.map ? [poolMesh.material.map.image.width, poolMesh.material.map.image.height] : null
              }
            };
          })()`,
          returnByValue: true
        });
        console.log('DEBUG POOLS:', JSON.stringify(res.result.value, null, 2));
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

