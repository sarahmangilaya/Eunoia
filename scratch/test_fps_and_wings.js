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
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 4500));

        // Enter exhibition
        await send('Runtime.evaluate', {
          expression: `(() => {
            if (window.enterExhibition) window.enterExhibition();
            if (window.setLobbyActive) window.setLobbyActive(false);
          })()`
        });
        await new Promise(r => setTimeout(r, 1500));

        const testPositions = [
          { name: 'Rotunda', x: 0, y: 1.7, z: 0 },
          { name: 'Wing I (Classical Art)', x: 22, y: 1.7, z: 0 },
          { name: 'Wing II (3D Worlds)', x: 0, y: 1.7, z: 25 },
          { name: 'Wing III (Photography)', x: -22, y: 1.7, z: 0 },
          { name: 'Wing IV (Kinematic/Graphic)', x: 0, y: 1.7, z: 60 }
        ];

        const results = [];

        for (const pos of testPositions) {
          await send('Runtime.evaluate', {
            expression: `window.camera.position.set(${pos.x}, ${pos.y}, ${pos.z});`
          });
          await new Promise(r => setTimeout(r, 400));

          // Measure FPS over 30 frames
          const fpsRes = await send('Runtime.evaluate', {
            expression: `new Promise((resolve) => {
              let frames = 0;
              const start = performance.now();
              function loop() {
                frames++;
                if (frames >= 30) {
                  const elapsed = performance.now() - start;
                  resolve(Math.round((frames / elapsed) * 1000));
                } else {
                  requestAnimationFrame(loop);
                }
              }
              requestAnimationFrame(loop);
            })`,
            awaitPromise: true,
            returnByValue: true
          });

          const res = await send('Runtime.evaluate', {
            expression: `(() => {
              const activePlayingVids = window.activeHogwartsVideos ? 
                window.activeHogwartsVideos.filter(h => !h.video.paused).length : 0;
              return {
                name: "${pos.name}",
                measuredFPS: ${fpsRes.result.value},
                calls: window.renderer.info.render.calls,
                triangles: window.renderer.info.render.triangles,
                geometries: window.renderer.info.memory.geometries,
                textures: window.renderer.info.memory.textures,
                activePlayingVideos: activePlayingVids,
                rotunda_vis: window.rotunda_group ? window.rotunda_group.visible : 'N/A',
                wingI_vis: window.wingI_group ? window.wingI_group.visible : 'N/A',
                wingII_vis: window.wingII_group ? window.wingII_group.visible : 'N/A',
                wingIII_vis: window.wingIII_group ? window.wingIII_group.visible : 'N/A',
                wingIV_vis: window.wingIV_group ? window.wingIV_group.visible : 'N/A'
              };
            })()`,
            returnByValue: true
          });
          results.push(res.result.value);
        }

        console.log('=== MULTI-WING PERFORMANCE BENCHMARK ===');
        console.table(results);

        chrome.kill();
        process.exit(0);
      };
    });
  });
}

run();
