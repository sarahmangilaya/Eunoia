const { spawn } = require('child_process');
const http = require('http');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9275', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_test2f_' + Date.now()
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9275/json', (res) => {
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
            try {
              const walls = [];
              wingII_group.traverse(m => {
                if (m.isMesh && m.geometry && m.geometry.type === 'BoxGeometry' && m.geometry.parameters.height > 3.0) {
                  walls.push({
                    pos: [+m.position.x.toFixed(2), +m.position.y.toFixed(2), +m.position.z.toFixed(2)],
                    rotY: +m.rotation.y.toFixed(3),
                    w: +m.geometry.parameters.width.toFixed(2),
                    d: +m.geometry.parameters.depth.toFixed(2)
                  });
                }
              });
              return JSON.stringify(walls);
            } catch(e) {
              return 'ERR: ' + e.message;
            }
          })()`
        });
        console.log('Wing II walls:', res.result ? res.result.value : res);

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();
