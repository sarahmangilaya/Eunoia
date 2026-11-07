const { spawn } = require('child_process');
const http = require('http');
const os = require('os');
const path = require('path');

(async () => {
  const port = 9292;
  const tmpDir = path.join(os.tmpdir(), 'eu_test_fix_' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--no-sandbox',
    '--disable-web-security',
    '--allow-file-access-from-files',
    `--user-data-dir=${tmpDir}`,
    '--window-size=1600,1000'
  ]);

  await new Promise(r => setTimeout(r, 2200));

  http.get(`http://127.0.0.1:${port}/json`, (res) => {
    let d = ''; res.on('data', x => d += x);
    res.on('end', async () => {
      const tabs = JSON.parse(d).filter(x => x.type === 'page');
      const ws = new WebSocket(tabs[0].webSocketDebuggerUrl);
      let id = 1;
      const send = (method, params = {}) => new Promise(r => {
        const i = id++;
        const h = e => {
          const m = JSON.parse(e.data);
          if (m.id === i) {
            ws.removeEventListener('message', h);
            r(m.result);
          }
        };
        ws.addEventListener('message', h);
        ws.send(JSON.stringify({ id: i, method, params }));
      });

      ws.onopen = async () => {
        await send('Page.enable');
        await send('Runtime.enable');
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 3500));

        await send('Runtime.evaluate', { expression: "document.getElementById('btnEnter')?.click()" });
        await new Promise(r => setTimeout(r, 500));
        await send('Runtime.evaluate', { expression: "document.getElementById('btnIndex')?.click()" });
        await new Promise(r => setTimeout(r, 500));

        // Inject fix into page to test
        const testRes = await send('Runtime.evaluate', {
          expression: `(() => {
            const style = document.createElement('style');
            style.textContent = \`
              .catalog-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)) !important;
                gap: 20px !important;
                align-content: start !important;
              }
              .card {
                display: flex !important;
                flex-direction: column !important;
                min-height: 380px !important;
                height: 100% !important;
              }
              .card-thumb {
                width: 100% !important;
                aspect-ratio: 4 / 3 !important;
                flex-shrink: 0 !important;
              }
              .card-body {
                flex: 1 1 auto !important;
                display: flex !important;
                flex-direction: column !important;
              }
            \`;
            document.head.appendChild(style);

            const c = document.querySelector('.card');
            const thumb = c.querySelector('.card-thumb');
            const body = c.querySelector('.card-body');
            return {
              cardHeight: getComputedStyle(c).height,
              thumbHeight: getComputedStyle(thumb).height,
              bodyHeight: getComputedStyle(body).height
            };
          })()`,
          returnByValue: true
        });

        console.log('Tested fix:', testRes.result.value);

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

