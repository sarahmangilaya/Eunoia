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
        ws.addEventListener('message', (evt) => {
          const msg = JSON.parse(evt.data);
          if (msg.method === 'Runtime.exceptionThrown') {
            console.error('BROWSER EXCEPTION:', JSON.stringify(msg.params.exceptionDetails));
          }
          if (msg.method === 'Runtime.consoleAPICalled') {
            console.log('CONSOLE:', msg.params.type, msg.params.args.map(a => a.value || a.description));
          }
        });

        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 4000));

        // Click enter and remove lobby overlay
        await send('Runtime.evaluate', {
          expression: `(() => {
            const btn = document.getElementById('btnEnter');
            if (btn) btn.click();
            const lobby = document.getElementById('lobby');
            if (lobby) lobby.remove();
            const overlay = document.getElementById('fade');
            if (overlay) overlay.remove();
          })()`
        });

        await new Promise(r => setTimeout(r, 1200));

        // 1. Teleport to Wing IV Cinema Atrium, looking West towards Production Design (user's exact viewpoint!)
        await send('Runtime.evaluate', {
          expression: `(() => {
            camera.position.set(0, 1.7, 60.0);
            camera.rotation.set(0, Math.PI / 2, 0);
            if (controls) {
              controls.pitch = 0;
              controls.yaw = Math.PI / 2;
            }
            updateDynamicWingCulling();
          })()`
        });

        await new Promise(r => setTimeout(r, 800));
        let snap1 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/verified_wingIV_cinema_west.png', Buffer.from(snap1.data, 'base64'));

        // 2. Teleport to Wing IV looking North towards Storyboards
        await send('Runtime.evaluate', {
          expression: `(() => {
            camera.position.set(0, 1.7, 60.0);
            camera.rotation.set(0, 0, 0);
            if (controls) {
              controls.pitch = 0;
              controls.yaw = 0;
            }
            updateDynamicWingCulling();
          })()`
        });

        await new Promise(r => setTimeout(r, 800));
        let snap2 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/verified_wingIV_cinema_north.png', Buffer.from(snap2.data, 'base64'));

        // 3. Teleport to Wing III Boulevard looking down the hallway
        await send('Runtime.evaluate', {
          expression: `(() => {
            camera.position.set(-20.0, 1.7, 0);
            camera.rotation.set(0, Math.PI / 2, 0);
            if (controls) {
              controls.pitch = 0;
              controls.yaw = Math.PI / 2;
            }
            updateDynamicWingCulling();
          })()`
        });

        await new Promise(r => setTimeout(r, 800));
        let snap3 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/verified_wingIII_boulevard.png', Buffer.from(snap3.data, 'base64'));

        // 4. Measure performance
        const perf = await send('Runtime.evaluate', {
          expression: `(() => {
            return {
              activeVideos: activeHogwartsVideos.filter(v => !v.video.paused).length,
              totalVideos: activeHogwartsVideos.length,
              calls: renderer.info.render.calls,
              triangles: renderer.info.render.triangles,
              hudFps: document.getElementById('hudFps')?.textContent
            };
          })()`,
          returnByValue: true
        });

        console.log('PERF RAW:', JSON.stringify(perf));

        chrome.kill();
        process.exit(0);
      };
    });
  });
}

run();
