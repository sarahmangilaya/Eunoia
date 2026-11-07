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

        const consoleErrors = [];
        ws.addEventListener('message', (evt) => {
          const msg = JSON.parse(evt.data);
          if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
            consoleErrors.push(msg.params.args.map(a => a.value || a.description).join(' '));
          }
          if (msg.method === 'Runtime.exceptionThrown') {
            consoleErrors.push(msg.params.exceptionDetails.text + ' ' + (msg.params.exceptionDetails.exception?.description || ''));
          }
        });

        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 5000));

        // Enter exhibition
        await send('Runtime.evaluate', {
          expression: `(() => {
            if (window.enterExhibition) {
              try { window.enterExhibition(); } catch (e) {}
            }
            if (window.setLobbyActive) window.setLobbyActive(false);
            const lobby = document.getElementById('lobby');
            if (lobby) lobby.remove();
            const resume = document.getElementById('resume');
            if (resume) resume.remove();
            const fade = document.getElementById('fade');
            if (fade) fade.remove();
            if (window.wakeAllHogwartsVideos) window.wakeAllHogwartsVideos();
          })()`
        });

        await new Promise(r => setTimeout(r, 2000));

        // Audit exhibit mesh count and video states
        const stats = await send('Runtime.evaluate', {
          expression: `(() => {
            const totalMeshes = window.exhibitMeshes ? window.exhibitMeshes.length : 0;
            const catalogTotal = window.EUNOIA_CONFIG ? window.EUNOIA_CONFIG.exhibits.length : 0;
            const hungInCatalog = window.EUNOIA_CONFIG ? window.EUNOIA_CONFIG.exhibits.filter(e => e.isHung).length : 0;
            const vids = document.querySelectorAll('video');
            let playingVids = 0;
            vids.forEach(v => {
              if (!v.paused) playingVids++;
            });

            // Check graphic design exhibits specifically
            const graphicExhibits = window.EUNOIA_CONFIG.exhibits.filter(e => 
              e.category.includes('Graphic') || e.category.includes('Logo') || e.category.includes('Jacquard')
            );
            const graphicHung = graphicExhibits.filter(e => e.isHung).length;

            return {
              totalMeshes,
              catalogTotal,
              hungInCatalog,
              totalHtmlVideos: vids.length,
              playingHtmlVideos: playingVids,
              graphicExhibitsCount: graphicExhibits.length,
              graphicExhibitsHung: graphicHung
            };
          })()`,
          returnByValue: true
        });

        console.log('=== AUDIT RESULTS ===');
        console.log(JSON.stringify(stats.result.value, null, 2));

        if (consoleErrors.length > 0) {
          console.log('Console errors:', consoleErrors);
        } else {
          console.log('Console errors: 0 (Clean log!)');
        }

        async function captureView(name, posX, posY, posZ, lookX, lookY, lookZ) {
          await send('Runtime.evaluate', {
            expression: `(() => {
              window.camera.position.set(${posX}, ${posY}, ${posZ});
              window.camera.lookAt(${lookX}, ${lookY}, ${lookZ});
              window.camera.rotation.setFromQuaternion(window.camera.quaternion, 'YXZ');
              if (window.controls && window.controls.object) {
                window.controls.object.position.set(${posX}, ${posY}, ${posZ});
              }
              if (window.updateWingCulling) window.updateWingCulling();
              window.updateCurrentWingCaption(window.camera.position);
              window.renderer.render(window.scene, window.camera);
            })()`
          });

          await new Promise(r => setTimeout(r, 600));

          const hudInfo = await send('Runtime.evaluate', {
            expression: `(() => {
              return {
                hudLoc: document.getElementById('hudLoc')?.textContent,
                capTitle: document.getElementById('capTitle')?.textContent,
                capNum: document.getElementById('capNum')?.textContent
              };
            })()`,
            returnByValue: true
          });

          const snap = await send('Page.captureScreenshot', { format: 'png' });
          const buf = Buffer.from(snap.data, 'base64');
          fs.writeFileSync(`scratch/${name}.png`, buf);
          console.log(`Captured scratch/${name}.png -> HUD: [${hudInfo.result.value.capNum}] ${hudInfo.result.value.hudLoc}`);
        }

        // 1. Wing IV East Chamber: Applied Graphic Design & Logos
        await captureView('wing4_applied_graphic_view', 18.0, 1.7, 56.5, 18.0, 2.4, 52.14);
        // 2. Wing IV East Chamber looking North at Atelier Lanyards
        await captureView('wing4_lanyards_view', 18.0, 1.7, 63.0, 18.0, 2.4, 67.86);
        // 3. Wing IV Cinema Atrium
        await captureView('wing4_cinema_atrium', 0.0, 1.7, 56.0, 0.0, 2.4, 67.86);
        // 4. Wing IV North Grand Hall: The Wind Rises Storyboards
        await captureView('wing4_storyboards', 0.0, 1.7, 78.0, 0.0, 2.5, 91.86);
        // 5. Wing I Traditional Fine Art Salon
        await captureView('wing1_traditional_salon', 52.0, 1.7, 14.0, 48.5, 2.4, 21.86);
        // 6. Wing III Observational Street Photography Boulevard
        await captureView('wing3_street_boulevard', -25.0, 1.7, 0.0, -45.0, 1.7, 0.0);
        // 7. Wing III Lunar Observatory
        await captureView('wing3_lunar_observatory', -35.0, 1.7, 14.0, -35.0, 2.4, 21.86);

        console.log('ALL VIEWS CAPTURED SUCCESSFULLY!');
        chrome.kill();
        process.exit(0);
      };
    });
  });
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});

