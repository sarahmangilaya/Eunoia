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

        // Enter exhibition properly
        await send('Runtime.evaluate', {
          expression: `(() => {
            if (window.setLobbyActive) window.setLobbyActive(false);
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
          })()`
        });

        await new Promise(r => setTimeout(r, 1200));

        // Audit video playback and scene state
        const audit = await send('Runtime.evaluate', {
          expression: `(() => {
            let totalVideos = 0;
            let playingVideos = 0;
            const videoDetails = [];

            const vids = document.querySelectorAll('video');
            vids.forEach(v => {
              totalVideos++;
              if (!v.paused) playingVideos++;
              videoDetails.push({
                src: v.src.split('/').slice(-2).join('/'),
                paused: v.paused,
                muted: v.muted,
                currentTime: v.currentTime
              });
            });

            return {
              totalVideos,
              playingVideos,
              videoDetails,
              hungMeshes: window.exhibitMeshes ? window.exhibitMeshes.length : 0
            };
          })()`,
          returnByValue: true
        });

        console.log('=== HOGWARTS VIDEO PLAYBACK AUDIT ===');
        console.log(JSON.stringify(audit.result.value, null, 2));

        async function captureView(name, posX, posY, posZ, lookX, lookY, lookZ) {
          await send('Runtime.evaluate', {
            expression: `(() => {
              window.camera.position.set(${posX}, ${posY}, ${posZ});
              window.camera.lookAt(${lookX}, ${lookY}, ${lookZ});
              window.camera.rotation.setFromQuaternion(window.camera.quaternion, 'YXZ');
              if (window.controls && window.controls.object) {
                window.controls.object.position.set(${posX}, ${posY}, ${posZ});
              }
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

          console.log(`View ${name}: HUD =`, hudInfo.result.value);

          const shot = await send('Page.captureScreenshot', { format: 'png' });
          fs.writeFileSync(`scratch/${name}.png`, Buffer.from(shot.data, 'base64'));
          console.log(`Saved screenshot scratch/${name}.png`);
        }

        // 1. Room B (Interior Architecture) - Matching the exact user screenshot view!
        // Looking from Southwest towards East and North walls
        await captureView('expanded_roomB_interior_corner', 7.5, 1.7, 13.5, 18.0, 2.4, 21.0);

        // 2. Room B looking directly at East Wall paintings (showing clear spacing)
        await captureView('expanded_roomB_interior_east', 13.0, 1.7, 17.5, 21.85, 2.4, 17.5);

        // 3. Room A (Environment Gallery) looking at West wall and South wall
        await captureView('expanded_roomA_environment_wide', -8.0, 1.7, 13.5, -18.0, 2.4, 19.0);

        // 4. Room C (3D VFX Cinema) showing glowing moving video canvases
        await captureView('expanded_roomC_vfx_cinema', -8.0, 1.7, 36.5, -17.0, 2.5, 44.0);

        // 5. Promenade looking at character turnaround kiosk
        await captureView('expanded_promenade_kiosk', 0, 1.7, 21.0, 0, 2.1, 27.0);

        // 6. Wing IV (Kinematic Pavilion) showing 2D Animation videos playing
        await captureView('expanded_wingIV_kinematic', 0, 1.7, 56.0, 0, 2.6, 67.85);

        console.log('ALL EXPANDED ROOMS CAPTURED & AUDITED!');
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
