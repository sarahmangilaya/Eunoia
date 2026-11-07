const { spawn } = require('child_process');
const http = require('http');

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
        await new Promise(r => setTimeout(r, 4000));

        const info = await send('Runtime.evaluate', {
          expression: `(() => {
            try {
              const ex36 = window.exhibitMeshes.find(m => m.userData.exhibit.id.includes('project-36'));
              if (!ex36) return { err: 'not found' };
              ex36.updateWorldMatrix(true, false);
              const m = ex36.matrixWorld.elements;
              return {
                worldPos: { x: m[12], y: m[13], z: m[14] },
                teleportPos: ex36.userData.exhibit.teleportPos,
                lookTarget: ex36.userData.exhibit.lookTarget
              };
            } catch(e) {
              return { err: e.message, stack: e.stack };
            }
          })()`,
          returnByValue: true
        });
        console.log('EX36 POS:', JSON.stringify(info.result.value, null, 2));

        chrome.kill();
        process.exit(0);
      };
    });
  });
}
run();
