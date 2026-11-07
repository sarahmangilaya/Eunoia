const { spawn } = require('child_process');
const http = require('http');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9265', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_inspect_' + Date.now()
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9265/json', (res) => {
    let d = ''; res.on('data', x => d += x);
    res.on('end', async () => {
      const t = JSON.parse(d).filter(x => x.type === 'page')[0];
      const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 1;
      const send = (method, params = {}) => new Promise(r => { const i = id++; const h = e => { const m = JSON.parse(e.data); if (m.id === i) { ws.removeEventListener('message', h); r(m.result); } }; ws.addEventListener('message', h); ws.send(JSON.stringify({ id: i, method, params })); });

      ws.onopen = async () => {
        await send('Page.enable'); await send('Runtime.enable');
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 3500));
        await send('Runtime.evaluate', { expression: "document.getElementById('btnEnter')?.click()" });
        await new Promise(r => setTimeout(r, 2000));

        const res = await send('Runtime.evaluate', {
          expression: `(() => {
            const pools = [];
            const wings = { I: wingI_group, II: wingII_group, III: wingIII_group, IV: wingIV_group };
            for (const [k, w] of Object.entries(wings)) {
              w.traverse(m => {
                if (m.isMesh && m.material && m.material.blending === THREE.AdditiveBlending) {
                  pools.push({
                    wing: k,
                    renderOrder: m.renderOrder,
                    depthWrite: m.material.depthWrite,
                    depthTest: m.material.depthTest,
                    opacity: m.material.opacity,
                    geoVertCount: m.geometry.attributes.position ? m.geometry.attributes.position.count : 0
                  });
                }
              });
            }
            return JSON.stringify(pools, null, 2);
          })()`
        });
        console.log('Pool meshes in scene:', res.result.value);
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

