const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9267', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_dbg_' + Date.now()
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9267/json', (res) => {
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

        // 1. Export poolTex canvas image
        const texData = await send('Runtime.evaluate', {
          expression: `(() => {
            let poolMat = null;
            wingI_group.traverse(m => {
              if (m.isMesh && m.material && m.material.opacity === 0.68) poolMat = m.material;
            });
            if (!poolMat || !poolMat.map || !poolMat.map.image) return null;
            return poolMat.map.image.toDataURL('image/png');
          })()`
        });

        if (texData.result.value) {
          const b64 = texData.result.value.replace(/^data:image\/png;base64,/, '');
          fs.writeFileSync('scratch/exported_poolTex.png', Buffer.from(b64, 'base64'));
          console.log('Saved scratch/exported_poolTex.png');
        } else {
          console.log('Could not export poolTex image!');
        }

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

