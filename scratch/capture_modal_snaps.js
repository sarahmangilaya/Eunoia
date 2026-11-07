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

        // Click Enter Exhibition
        await send('Runtime.evaluate', {
          expression: `(() => {
            const btn = document.getElementById('btnEnter');
            if (btn) btn.click();
            const lobby = document.getElementById('lobby');
            if (lobby) lobby.style.display = 'none';
          })()`
        });

        await new Promise(r => setTimeout(r, 1000));

        // Open inspection modal for "What the Heart Invents"
        const modalInfo = await send('Runtime.evaluate', {
          expression: `(() => {
            const ex = window.EUNOIA_CONFIG.exhibits.find(e => e.title === 'What the Heart Invents');
            if (!ex) return { error: 'Not found' };
            window.inspectExhibit(ex);
            return {
              title: document.getElementById('plqTitle')?.textContent,
              sub: document.getElementById('plqSubtitle')?.textContent,
              desc: document.getElementById('plqDesc')?.textContent,
              category: document.getElementById('plqCategory')?.textContent,
              isOpen: document.getElementById('plaque')?.classList.contains('open')
            };
          })()`,
          returnByValue: true
        });

        console.log('Inspection Modal Info:', modalInfo.result.value);

        await new Promise(r => setTimeout(r, 500));

        const snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/inspect_modal_heart.png', Buffer.from(snap.data, 'base64'));

        // Also test "Where the Moon Embraces the Sun"
        await send('Runtime.evaluate', {
          expression: `(() => {
            const ex = window.EUNOIA_CONFIG.exhibits.find(e => e.title === 'Where the Moon Embraces the Sun');
            window.inspectExhibit(ex);
          })()`
        });

        await new Promise(r => setTimeout(r, 500));

        const snap2 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/inspect_modal_sun_moon.png', Buffer.from(snap2.data, 'base64'));

        // Also test "High and Mighty" in Graphic Design
        await send('Runtime.evaluate', {
          expression: `(() => {
            const ex = window.EUNOIA_CONFIG.exhibits.find(e => e.title === 'High and Mighty' && e.wing === 'IV');
            window.inspectExhibit(ex);
          })()`
        });

        await new Promise(r => setTimeout(r, 500));

        const snap3 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/inspect_modal_high_mighty_graphic.png', Buffer.from(snap3.data, 'base64'));

        console.log('ALL MODALS CAPTURED SUCCESSFULLY!');
        chrome.kill();
        process.exit(0);
      };
    });
  });
}

run();

