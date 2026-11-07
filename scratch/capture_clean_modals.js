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
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 4500));

        // Dismiss lobby
        await send('Runtime.evaluate', {
          expression: `(() => {
            if (window.enterExhibition) {
              try { window.enterExhibition(); } catch (e) {}
            }
            if (window.setLobbyActive) window.setLobbyActive(false);
            const lobby = document.getElementById('lobby');
            if (lobby) lobby.remove();
            const fade = document.getElementById('fade');
            if (fade) fade.remove();
          })()`
        });

        await new Promise(r => setTimeout(r, 1000));

        // Inspect "What the Heart Invents"
        await send('Runtime.evaluate', {
          expression: `(() => {
            const ex = window.EUNOIA_CONFIG.exhibits.find(e => e.title === 'What the Heart Invents');
            window.teleportToExhibit(ex);
          })()`
        });

        await new Promise(r => setTimeout(r, 1500));

        const snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/modal_what_the_heart_invents_clean.png', Buffer.from(snap.data, 'base64'));

        // Inspect "Where the Moon Embraces the Sun"
        await send('Runtime.evaluate', {
          expression: `(() => {
            const ex = window.EUNOIA_CONFIG.exhibits.find(e => e.title === 'Where the Moon Embraces the Sun');
            window.teleportToExhibit(ex);
          })()`
        });

        await new Promise(r => setTimeout(r, 1500));

        const snap2 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/modal_sun_moon_clean.png', Buffer.from(snap2.data, 'base64'));

        console.log('CAPTURED CLEAN SCREENSHOTS!');
        chrome.kill();
        process.exit(0);
      };
    });
  });
}

run();

