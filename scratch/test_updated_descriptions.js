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

        // Audit exhibits in window.EUNOIA_CONFIG
        const audit = await send('Runtime.evaluate', {
          expression: `(() => {
            const exs = window.EUNOIA_CONFIG.exhibits;
            
            function findByTitle(title) {
              return exs.find(e => e.title === title);
            }

            return {
              totalExhibits: exs.length,
              sampleChecks: {
                highAndMightyTrad: findByTitle('High and Mighty'),
                faceInFragments: findByTitle('A Face in Fragments'),
                thornedDevotion: findByTitle('Thorned Devotion'),
                theWatchful: findByTitle('The Watchful'),
                sunMoon: findByTitle('Where the Moon Embraces the Sun'),
                unusualGentleman: findByTitle('The Unusual Gentleman'),
                aev: findByTitle('AEV'),
                monogram: findByTitle('Aesthylegia: The Monogram'),
                wordmark: findByTitle('Aesthylegia: The Wordmark'),
                chessQue: findByTitle('Chess Que'),
                feastOfPower: findByTitle('Feast of Power'),
                inBetween: findByTitle('In Between'),
                matilda: findByTitle('Matilda'),
                littleMoreOfMe: findByTitle('A Little More of Me'),
                meInMotion: findByTitle('Me in Motion'),
                studyOfMyself: findByTitle('A Study of Myself'),
                michael: findByTitle('Michael'),
                phoenix: findByTitle('Rise of the Phoenix'),
                rickAndMorty: findByTitle('Me, in Another Dimension'),
                whatTheHeartInvents: findByTitle('What the Heart Invents'),
                stillHere: findByTitle('Still Here'),
                parkJihyo: findByTitle('Park Jihyo'),
                masquerade: findByTitle('Masquerade of Smiles'),
                productionDesign: findByTitle('Oi Marichin Marukoy! – Fancy Kitchen')
              }
            };
          })()`,
          returnByValue: true
        });

        console.log('=== AUDIT VERIFICATION ===');
        console.log('Total exhibits:', audit.result.value.totalExhibits);
        for (const [k, v] of Object.entries(audit.result.value.sampleChecks)) {
          if (v) {
            console.log(`PASS [${k}]: title="${v.title}" | sub="${v.subtitle}" | descLen=${v.description.length}`);
          } else {
            console.error(`FAIL [${k}]: not found!`);
          }
        }

        // Test inspect modal opening for "High and Mighty"
        await send('Runtime.evaluate', {
          expression: `(() => {
            const ex = window.EUNOIA_CONFIG.exhibits.find(e => e.title === 'High and Mighty' && e.room === 'finearts_traditional');
            window.teleportToExhibit(ex);
          })()`
        });

        await new Promise(r => setTimeout(r, 1200));

        const snap1 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/modal_high_and_mighty.png', Buffer.from(snap1.data, 'base64'));
        console.log('Saved scratch/modal_high_and_mighty.png');

        // Test inspect modal for "What the Heart Invents"
        await send('Runtime.evaluate', {
          expression: `(() => {
            const ex = window.EUNOIA_CONFIG.exhibits.find(e => e.title === 'What the Heart Invents');
            window.teleportToExhibit(ex);
          })()`
        });

        await new Promise(r => setTimeout(r, 1200));

        const snap2 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('scratch/modal_what_the_heart_invents.png', Buffer.from(snap2.data, 'base64'));
        console.log('Saved scratch/modal_what_the_heart_invents.png');

        chrome.kill();
        process.exit(0);
      };
    });
  });
}

run();

