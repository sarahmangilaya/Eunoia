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
    '--allow-file-access-from-files',
    '--autoplay-policy=no-user-gesture-required'
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
        await new Promise(r => setTimeout(r, 4500));

        // Enter exhibition & wake videos
        await send('Runtime.evaluate', {
          expression: `(() => {
            if (window.setLobbyActive) window.setLobbyActive(false);
            if (window.wakeAllHogwartsVideos) window.wakeAllHogwartsVideos();
          })()`
        });

        await new Promise(r => setTimeout(r, 2000));

        const res = await send('Runtime.evaluate', {
          expression: `(() => {
            const vids = document.querySelectorAll('video');
            let playing = 0;
            const details = [];
            vids.forEach(v => {
              if (!v.paused) playing++;
              details.push({
                src: v.src.split('/').pop(),
                paused: v.paused,
                currentTime: v.currentTime,
                readyState: v.readyState
              });
            });
            return { total: vids.length, playing, details };
          })()`,
          returnByValue: true
        });

        console.log('AUTOPLAY TEST RESULT:');
        console.log(JSON.stringify(res.result.value, null, 2));

        chrome.kill();
        process.exit(0);
      };
    });
  });
}

run().catch(e => {
  console.error(e);
  process.exit(1);
});

