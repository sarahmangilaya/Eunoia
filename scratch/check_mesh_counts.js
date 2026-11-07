const { spawn } = require('child_process');
const http = require('http');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9267', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_test_mesh3'
  ]);
  await new Promise(r => setTimeout(r, 1500));
  http.get('http://127.0.0.1:9267/json', (res) => {
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
            const counts = {};
            [wingI_group, wingII_group, wingIII_group, wingIV_group].forEach((wg, idx) => {
              let c = 0;
              wg.traverse(o => {
                if (o.isMesh && o.material && o.material.opacity === 0.68) {
                  c += o.geometry.attributes.position.count / 6;
                }
              });
              counts['wing_' + (idx + 1)] = c;
            });
            return counts;
          })()`,
          returnByValue: true
        });
        console.log('wall mesh planes per wing:', JSON.stringify(res.result.value, null, 2));
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

