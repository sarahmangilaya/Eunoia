const { spawn } = require('child_process');
const http = require('http');
const os = require('os');
const path = require('path');

(async () => {
  const port = 9291;
  const tmpDir = path.join(os.tmpdir(), 'eu_css_inspect_' + Date.now());
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

        const res = await send('Runtime.evaluate', {
          expression: `(() => {
            const c = document.querySelector('.card');
            const thumb = c ? c.querySelector('.card-thumb') : null;
            const body = c ? c.querySelector('.card-body') : null;
            const title = c ? c.querySelector('.card-title') : null;
            return {
              cardClientHeight: c ? c.clientHeight : null,
              cardOffsetHeight: c ? c.offsetHeight : null,
              cardBounding: c ? c.getBoundingClientRect() : null,
              thumbClientHeight: thumb ? thumb.clientHeight : null,
              thumbBounding: thumb ? thumb.getBoundingClientRect() : null,
              thumbComputed: thumb ? {
                display: getComputedStyle(thumb).display,
                height: getComputedStyle(thumb).height,
                aspectRatio: getComputedStyle(thumb).aspectRatio
              } : null,
              bodyClientHeight: body ? body.clientHeight : null,
              bodyBounding: body ? body.getBoundingClientRect() : null,
              bodyComputed: body ? {
                display: getComputedStyle(body).display,
                height: getComputedStyle(body).height,
                overflow: getComputedStyle(body).overflow
              } : null,
              titleClientHeight: title ? title.clientHeight : null,
              gridBounding: document.getElementById('catGrid').getBoundingClientRect(),
              panelBounding: document.querySelector('.catalog-panel').getBoundingClientRect()
            };
          })()`,
          returnByValue: true
        });

        console.log(JSON.stringify(res.result.value, null, 2));

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

