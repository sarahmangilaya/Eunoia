const { spawn } = require('child_process');
const http = require('http');
const os = require('os');
const path = require('path');

(async () => {
  const port = 9289;
  const tmpDir = path.join(os.tmpdir(), 'eu_cat_inspect_' + Date.now());
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
        await new Promise(r => setTimeout(r, 1000));

        // Open Catalog
        await send('Runtime.evaluate', { expression: "toggleCatalog(true)" });
        await new Promise(r => setTimeout(r, 1000));

        const info = await send('Runtime.evaluate', {
          expression: `(() => {
            const grid = document.getElementById('catGrid');
            const cards = grid.querySelectorAll('.card');
            if (!cards.length) return { count: 0 };
            const c0 = cards[0];
            const thumb = c0.querySelector('.card-thumb');
            const img = c0.querySelector('img');
            const body = c0.querySelector('.card-body');
            return {
              count: cards.length,
              gridStyle: {
                display: getComputedStyle(grid).display,
                gridTemplateColumns: getComputedStyle(grid).gridTemplateColumns,
                gap: getComputedStyle(grid).gap,
                height: getComputedStyle(grid).height
              },
              card0: {
                outerHTML: c0.outerHTML.slice(0, 300),
                rect: c0.getBoundingClientRect(),
                cardHeight: getComputedStyle(c0).height,
                cardMaxHeight: getComputedStyle(c0).maxHeight,
                overflow: getComputedStyle(c0).overflow,
                thumbRect: thumb ? thumb.getBoundingClientRect() : null,
                thumbDisplay: thumb ? getComputedStyle(thumb).display : null,
                imgSrc: img ? img.src : null,
                imgNaturalWidth: img ? img.naturalWidth : null,
                bodyRect: body ? body.getBoundingClientRect() : null,
                bodyHeight: body ? getComputedStyle(body).height : null
              }
            };
          })()`,
          returnByValue: true
        });

        console.log('Catalog Info:', JSON.stringify(info.result.value, null, 2));

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

