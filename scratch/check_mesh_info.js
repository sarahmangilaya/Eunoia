const { spawn } = require('child_process');
const http = require('http');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9265', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_test_mesh2'
  ]);
  await new Promise(r => setTimeout(r, 1500));
  http.get('http://127.0.0.1:9265/json', (res) => {
    let d = ''; res.on('data', x => d += x);
    res.on('end', async () => {
      const t = JSON.parse(d).filter(x => x.type === 'page')[0];
      const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 1;
      const send = (method, params = {}) => new Promise(r => { const i = id++; const h = e => { const m = JSON.parse(e.data); if (m.id === i) { ws.removeEventListener('message', h); r(m.result); } }; ws.addEventListener('message', h); ws.send(JSON.stringify({ id: i, method, params })); });
      ws.onopen = async () => {
        await send('Page.enable'); await send('Runtime.enable');
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 3000));
        const res = await send('Runtime.evaluate', {
          expression: `(() => {
            let m = null;
            wingI_group.traverse(obj => { if (obj.isMesh && obj.material && obj.material.opacity === 0.68) m = obj; });
            if (!m) return "not found";
            m.geometry.computeBoundingBox();
            const box = m.geometry.boundingBox;
            const posAttr = m.geometry.attributes.position;
            const p0 = [posAttr.getX(0), posAttr.getY(0), posAttr.getZ(0)];
            const p1 = [posAttr.getX(1), posAttr.getY(1), posAttr.getZ(1)];
            const p2 = [posAttr.getX(2), posAttr.getY(2), posAttr.getZ(2)];
            return {
              boxMin: [box.min.x, box.min.y, box.min.z],
              boxMax: [box.max.x, box.max.y, box.max.z],
              p0, p1, p2,
              depthTest: m.material.depthTest,
              depthWrite: m.material.depthWrite,
              blending: m.material.blending,
              transparent: m.material.transparent,
              side: m.material.side,
              hasTex: !!m.material.map,
              texWidth: m.material.map ? m.material.map.image.width : null,
              texHeight: m.material.map ? m.material.map.image.height : null
            };
          })()`,
          returnByValue: true
        });
        console.log('mesh info:', JSON.stringify(res.result.value, null, 2));
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

