const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

async function run() {
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const chrome = spawn(chromePath, [
    '--headless=new',
    '--remote-debugging-port=9222',
    '--disable-gpu-sandbox',
    '--no-sandbox',
    '--disable-web-security',
    '--allow-file-access-from-files',
    '--autoplay-policy=no-user-gesture-required'
  ]);

  await new Promise(r => setTimeout(r, 2000));

  http.get('http://127.0.0.1:9222/json', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', async () => {
      const targets = JSON.parse(data);
      const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
      let id = 1;

      function send(method, params = {}) {
        return new Promise((resolve) => {
          const reqId = id++;
          const handler = (evt) => {
            const msg = JSON.parse(evt.data);
            if (msg.id === reqId) {
              ws.removeEventListener('message', handler);
              resolve(msg.result);
            }
          };
          ws.addEventListener('message', handler);
          ws.send(JSON.stringify({ id: reqId, method, params }));
        });
      }

      ws.onopen = async () => {
        await send('Page.enable');
        await send('Runtime.enable');
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 4500));

        // Call inspectExhibit directly
        const modalInfo = await send('Runtime.evaluate', {
          expression: `(() => {
            const ex = window.EUNOIA_CONFIG.exhibits.find(e => e.title === 'What the Heart Invents');
            if (!ex) return { error: 'Not found' };
            window.inspectExhibit(ex);
            return {
              title: document.getElementById('plqTitle')?.textContent,
              sub: document.getElementById('plqSubtitle')?.textContent,
              desc: document.getElementById('plqDesc')?.textContent,
              isOpen: document.getElementById('plaque')?.classList.contains('open')
            };
          })()`,
          returnByValue: true
        });

        console.log('Modal direct inspection result:', modalInfo.result.value);

        await new Promise(r => setTimeout(r, 600));

        const snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/direct_inspect_heart.png', Buffer.from(snap.data, 'base64'));
        console.log('Captured scratch/direct_inspect_heart.png');

        chrome.kill();
        process.exit(0);
      };
    });
  });
}

run();

