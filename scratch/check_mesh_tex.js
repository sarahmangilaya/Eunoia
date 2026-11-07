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
      const ws = new WebSocket(JSON.parse(data)[0].webSocketDebuggerUrl);
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

        // Get the data URL of the canvas/image on ex36
        const imgData = await send('Runtime.evaluate', {
          expression: `(() => {
            const ex36 = window.exhibitMeshes.find(m => m.userData.exhibit.id.includes('project-36'));
            const tex = ex36.material.map;
            const img = tex.image;
            if (img instanceof HTMLCanvasElement) {
              return { type: 'canvas', data: img.toDataURL('image/png') };
            } else if (img instanceof HTMLImageElement) {
              const c = document.createElement('canvas');
              c.width = 400; c.height = Math.round(400 * (img.naturalHeight / img.naturalWidth));
              const ctx = c.getContext('2d');
              ctx.drawImage(img, 0, 0, c.width, c.height);
              return { type: 'img', src: img.src, data: c.toDataURL('image/png') };
            }
            return { type: 'unknown' };
          })()`,
          returnByValue: true
        });

        console.log('EX36 IMG TYPE:', imgData.result.value.type, imgData.result.value.src);
        const b64 = imgData.result.value.data.split(',')[1];
        fs.writeFileSync('scratch/ex36_texture_content.png', Buffer.from(b64, 'base64'));
        console.log('Saved scratch/ex36_texture_content.png');

        chrome.kill();
        process.exit(0);
      };
    });
  });
}
run();

