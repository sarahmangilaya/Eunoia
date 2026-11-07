const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');

(async () => {
  const port = 9290;
  const tmpDir = path.join(os.tmpdir(), 'eu_cat_click_' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--no-sandbox',
    '--disable-web-security',
    '--allow-file-access-from-files',
    `--user-data-dir=${tmpDir}`,
    '--window-size=1600,1000'
  ]);

  await new Promise(r => setTimeout(r, 2200));

  http.get(`http://127.0.0.1:${port}/json`, (res) => {
    let d = ''; res.on('data', x => d += x);
    res.on('end', async () => {
      const tabs = JSON.parse(d).filter(x => x.type === 'page');
      const ws = new WebSocket(tabs[0].webSocketDebuggerUrl);
      let id = 1;
      const send = (method, params = {}) => new Promise(r => {
        const i = id++;
        const h = e => {
          const m = JSON.parse(e.data);
          if (m.id === i) {
            ws.removeEventListener('message', h);
            r(m.result);
          }
        };
        ws.addEventListener('message', h);
        ws.send(JSON.stringify({ id: i, method, params }));
      });

      ws.onopen = async () => {
        await send('Page.enable');
        await send('Runtime.enable');
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 3500));

        await send('Runtime.evaluate', { expression: "document.getElementById('btnEnter')?.click()" });
        await new Promise(r => setTimeout(r, 1000));

        // Click Index Button
        await send('Runtime.evaluate', { expression: "document.getElementById('btnIndex')?.click()" });
        await new Promise(r => setTimeout(r, 1000));

        const snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/catalog_view_actual.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved catalog_view_actual.png');

        const info = await send('Runtime.evaluate', {
          expression: `(() => {
            const grid = document.getElementById('catGrid');
            const cards = grid.querySelectorAll('.card');
            const c0 = cards[0];
            return {
              count: cards.length,
              card0HTML: c0 ? c0.outerHTML : 'none',
              card0Rect: c0 ? c0.getBoundingClientRect() : null,
              card0Computed: c0 ? {
                height: getComputedStyle(c0).height,
                display: getComputedStyle(c0).display,
                overflow: getComputedStyle(c0).overflow
              } : null
            };
          })()`,
          returnByValue: true
        });

        console.log('Catalog Info:', JSON.stringify(info.result.value, null, 2));

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

