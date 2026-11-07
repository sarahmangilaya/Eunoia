const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9230', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_tex_check'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9230/json', (res) => {
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
            let poolTex = null;
            wingII_group.traverse(c => {
              if (c.material && c.material.blending === THREE.AdditiveBlending) {
                poolTex = c.material.map;
              }
            });
            if (!poolTex || !poolTex.image) return null;
            return poolTex.image.toDataURL();
          })()`,
          returnByValue: true
        });
        if (evalRes.result && evalRes.result.value) {
          const b64 = evalRes.result.value.replace(/^data:image\/png;base64,/, '');
          fs.writeFileSync('scratch/pool_texture.png', Buffer.from(b64, 'base64'));
          console.log('Saved scratch/pool_texture.png');
        } else {
          console.log('No texture found:', evalRes);
        }
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

