const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');

(async () => {
  const port = 9287;
  const tmpDir = path.join(os.tmpdir(), 'eu_concierge_final_' + Date.now());
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
      if (!tabs.length) {
        chrome.kill();
        process.exit(1);
      }
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
        await new Promise(r => setTimeout(r, 1200));

        // 1. Direct Front Closeup of the Pedestal Tabletop: Phone & Card
        await send('Runtime.evaluate', {
          expression: `(() => {
            camera.position.set(1.30, 1.35, -3.48);
            camera.lookAt(2.4, 1.05, -2.6);
            if (window.controls) {
              window.controls.getObject().position.copy(camera.position);
            }
          })()`
        });
        await new Promise(r => setTimeout(r, 600));
        let snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/concierge_table_closeup.png', Buffer.from(snap.data, 'base64'));

        // 2. Open Card Modal (Front Face)
        await send('Runtime.evaluate', {
          expression: `(() => {
            if (window.openCardModal) openCardModal();
          })()`
        });
        await new Promise(r => setTimeout(r, 600));
        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/concierge_card_modal.png', Buffer.from(snap.data, 'base64'));

        // 3. Flip Card Modal (Back Face)
        await send('Runtime.evaluate', {
          expression: `(() => {
            document.getElementById('btnFlipCardManual')?.click();
          })()`
        });
        await new Promise(r => setTimeout(r, 600));
        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/concierge_card_back_modal.png', Buffer.from(snap.data, 'base64'));

        console.log('Successfully captured all concierge screenshots directly into brain artifacts.');

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();
