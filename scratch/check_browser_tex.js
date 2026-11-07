const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9269', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_test_tex'
  ]);
  await new Promise(r => setTimeout(r, 1500));
  http.get('http://127.0.0.1:9269/json', (res) => {
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
            let poolMesh = null;
            wingI_group.traverse(o => { if (o.isMesh && o.material && o.material.opacity === 0.68) poolMesh = o; });
            if (!poolMesh || !poolMesh.material.map) return "no pool mesh";
            const canvas = poolMesh.material.map.image;
            return canvas.toDataURL('image/png');
          })()`,
          returnByValue: true
        });
        const dataUrl = res.result.value;
        if (dataUrl && dataUrl.startsWith('data:image/png;base64,')) {
          const b64 = dataUrl.replace('data:image/png;base64,', '');
          fs.writeFileSync('scratch/browser_pool_tex.png', Buffer.from(b64, 'base64'));
          console.log('Saved browser_pool_tex.png!');
        } else {
          console.log('Result:', dataUrl);
        }
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

