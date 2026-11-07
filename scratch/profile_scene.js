const { spawn } = require('child_process');
const http = require('http');

async function run() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
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
          if (msg.method === 'Runtime.consoleAPICalled') {
            console.log('[BROWSER CONSOLE]', msg.params.type, msg.params.args.map(a => a.value || a.description).join(' '));
          }
          if (msg.method === 'Runtime.exceptionThrown') {
            console.error('[BROWSER EXCEPTION]', msg.params.exceptionDetails.text, msg.params.exceptionDetails.exception?.description);
          }
        });

        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 4500));

        // Enter gallery
        await send('Runtime.evaluate', {
          expression: `(() => {
            if (window.enterExhibition) window.enterExhibition();
            if (window.setLobbyActive) window.setLobbyActive(false);
          })()`
        });

        await new Promise(r => setTimeout(r, 2000));

        const info = await send('Runtime.evaluate', {
          expression: `(() => {
            if (!window.renderer) return { error: 'renderer not on window' };
            return {
              render: {
                calls: window.renderer.info.render.calls,
                triangles: window.renderer.info.render.triangles,
                lines: window.renderer.info.render.lines,
                frame: window.renderer.info.render.frame
              },
              memory: {
                geometries: window.renderer.info.memory.geometries,
                textures: window.renderer.info.memory.textures
              },
              programs: window.renderer.info.programs ? window.renderer.info.programs.length : 0,
              pixelRatio: window.renderer.getPixelRatio(),
              canvasWidth: window.renderer.domElement.width,
              canvasHeight: window.renderer.domElement.height,
              hogwartsVideos: window.activeHogwartsVideos ? window.activeHogwartsVideos.length : 0
            };
          })()`,
          returnByValue: true
        });

        console.log('=== RENDERER PROFILE INFO ===');
        console.log(JSON.stringify(info.result ? info.result.value : info, null, 2));

        chrome.kill();
        process.exit(0);
      };
    });
  });
}

run();

