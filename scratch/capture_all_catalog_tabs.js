const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');

(async () => {
  const port = 9293;
  const tmpDir = path.join(os.tmpdir(), 'eu_cat_tabs_' + Date.now());
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
        await new Promise(r => setTimeout(r, 800));

        // Open Catalog
        await send('Runtime.evaluate', { expression: "document.getElementById('btnIndex')?.click()" });
        await new Promise(r => setTimeout(r, 1200));

        // 1. All Works Tab
        let snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/catalog_tab_all.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved catalog_tab_all.png');

        // 2. Wing I Tab
        await send('Runtime.evaluate', {
          expression: `(() => {
            const chips = document.querySelectorAll('.chip');
            if (chips[1]) chips[1].click();
          })()`
        });
        await new Promise(r => setTimeout(r, 800));
        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/catalog_tab_wing1.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved catalog_tab_wing1.png');

        // 3. Wing II Tab
        await send('Runtime.evaluate', {
          expression: `(() => {
            const chips = document.querySelectorAll('.chip');
            if (chips[2]) chips[2].click();
          })()`
        });
        await new Promise(r => setTimeout(r, 800));
        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/catalog_tab_wing2.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved catalog_tab_wing2.png');

        // 4. Wing III Tab
        await send('Runtime.evaluate', {
          expression: `(() => {
            const chips = document.querySelectorAll('.chip');
            if (chips[3]) chips[3].click();
          })()`
        });
        await new Promise(r => setTimeout(r, 800));
        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/catalog_tab_wing3.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved catalog_tab_wing3.png');

        // 5. Wing IV Tab
        await send('Runtime.evaluate', {
          expression: `(() => {
            const chips = document.querySelectorAll('.chip');
            if (chips[4]) chips[4].click();
          })()`
        });
        await new Promise(r => setTimeout(r, 800));
        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/catalog_tab_wing4.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved catalog_tab_wing4.png');

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

