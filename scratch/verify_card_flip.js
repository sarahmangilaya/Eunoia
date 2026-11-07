const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');

(async () => {
  const port = 9288;
  const tmpDir = path.join(os.tmpdir(), 'eu_test_flip_' + Date.now());
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

        // Open Card Modal
        await send('Runtime.evaluate', { expression: "window.openCardModal()" });
        await new Promise(r => setTimeout(r, 500));

        // Front Face Capture
        let snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/verify_adjusted_front.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved verify_adjusted_front.png');

        // Click on the card container to flip it
        await send('Runtime.evaluate', {
          expression: "document.getElementById('dossierCardContainer')?.click()"
        });
        // Wait for CSS flip animation to complete (0.65s)
        await new Promise(r => setTimeout(r, 800));

        // Back Face Capture
        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/verify_adjusted_back.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved verify_adjusted_back.png');

        // Verify click again flips it back
        await send('Runtime.evaluate', {
          expression: "document.getElementById('dossierCardContainer')?.click()"
        });
        await new Promise(r => setTimeout(r, 800));
        const flippedState = await send('Runtime.evaluate', {
          expression: "document.getElementById('dossier3dCard')?.classList.contains('is-flipped')"
        });
        console.log('Card returned to front (is-flipped === false):', flippedState.result.value === false);

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

