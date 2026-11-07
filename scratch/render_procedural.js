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
    '--allow-file-access-from-files'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  http.get('http://127.0.0.1:9222/json', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', async () => {
      const targets = JSON.parse(data);
      const wsUrl = targets[0].webSocketDebuggerUrl;
      const ws = new WebSocket(wsUrl);

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

        const fileUrl = 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html';
        await send('Page.navigate', { url: fileUrl });
        await new Promise(r => setTimeout(r, 3000));

        const res = await send('Runtime.evaluate', {
          expression: `(() => {
            const canvas = paintArtwork('gallery', 'portrait', hashString('project-36-drawing-2-plate-8-character-png'));
            return canvas.toDataURL('image/png');
          })()`,
          returnByValue: true
        });

        const base64 = res.result.value.split(',')[1];
        fs.writeFileSync('scratch/paintArtwork_gallery.png', Buffer.from(base64, 'base64'));
        console.log('Saved scratch/paintArtwork_gallery.png');

        chrome.kill();
        process.exit(0);
      };
    });
  });
}

run().catch(console.error);

