const { spawn } = require('child_process');
const http = require('http');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9227', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_inspect_pools'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9227/json', (res) => {
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
        ws.addEventListener('message', (e) => {
          const m = JSON.parse(e.data);
          if (m.method === 'Runtime.exceptionThrown') {
            console.error('EXCEPTION:', JSON.stringify(m.params.exceptionDetails));
          }
          if (m.method === 'Runtime.consoleAPICalled') {
            console.log('LOG:', m.params.args.map(a => a.value || a.description).join(' '));
          }
        });
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await sleep(3500);
        const evalRes = await send('Runtime.evaluate', {
          expression: `(() => {
            const pools = [];
            [wingI_group, wingII_group, wingIII_group, wingIV_group].forEach((wg, idx) => {
              wg.traverse((c) => {
                if (c.material && c.material.blending === THREE.AdditiveBlending) {
                  pools.push({ wing: idx+1, visible: c.visible, geomVerts: c.geometry.attributes.position.count, matColor: c.material.color.getHexString(), opacity: c.material.opacity });
                }
              });
            });
            return pools;
          })()`,
          returnByValue: true
        });
        console.log('POOLS EVAL:', JSON.stringify(evalRes));
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

