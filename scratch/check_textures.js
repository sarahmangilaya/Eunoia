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

        await new Promise(r => setTimeout(r, 4000));

        // Click enter exhibition
        await send('Runtime.evaluate', {
          expression: `(() => {
            window.enterExhibition();
            const ex36 = window.exhibitMeshes.find(m => m.userData.exhibit.id.includes('project-36'));
            if (window.teleportToExhibit) {
              window.teleportToExhibit(ex36.userData.exhibit.id);
            }
          })()`
        });

        await new Promise(r => setTimeout(r, 1500));

        const snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/snap_ex36.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved scratch/snap_ex36.png');

        const evalAll = await send('Runtime.evaluate', {
          expression: `(() => {
            return {
              totalMeshes: window.exhibitMeshes.length,
              totalConfig: window.EUNOIA_CONFIG.exhibits.length,
              exhibits: window.exhibitMeshes.map(m => ({
                id: m.userData.exhibit.id,
                title: m.userData.exhibit.title,
                wing: m.userData.exhibit.wing,
                imagePath: m.userData.exhibit.imagePath,
                isImg: m.material.map && m.material.map.image instanceof HTMLImageElement,
                naturalW: m.material.map && m.material.map.image ? (m.material.map.image.naturalWidth || m.material.map.image.width) : null
              }))
            };
          })()`,
          returnByValue: true
        });

        console.log('Total exhibits hung:', evalAll.result.value.totalMeshes, 'out of config:', evalAll.result.value.totalConfig);
        fs.writeFileSync('scratch/exhibits_status.json', JSON.stringify(evalAll.result.value, null, 2));

        chrome.kill();
        process.exit(0);
      };
    });
  });
}

run().catch(console.error);
