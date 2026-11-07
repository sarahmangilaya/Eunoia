const { spawn } = require('child_process');
const http = require('http');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9279', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_final_' + Date.now()
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9279/json', (res) => {
    let d = ''; res.on('data', x => d += x);
    res.on('end', async () => {
      const t = JSON.parse(d).filter(x => x.type === 'page')[0];
      const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 1;
      const send = (method, params = {}) => new Promise(r => { const i = id++; const h = e => { const m = JSON.parse(e.data); if (m.id === i) { ws.removeEventListener('message', h); r(m.result); } }; ws.addEventListener('message', h); ws.send(JSON.stringify({ id: i, method, params })); });

      const errors = [];
      ws.addEventListener('message', e => {
        const m = JSON.parse(e.data);
        if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') {
          errors.push(m.params.args.map(a => a.value || a.description).join(' '));
        }
        if (m.method === 'Runtime.exceptionThrown') {
          errors.push(m.params.exceptionDetails.text + ': ' + (m.params.exceptionDetails.exception?.description || ''));
        }
      });

      ws.onopen = async () => {
        await send('Page.enable'); await send('Runtime.enable');
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 3500));
        await send('Runtime.evaluate', { expression: "document.getElementById('btnEnter')?.click()" });
        await new Promise(r => setTimeout(r, 2000));

        const res = await send('Runtime.evaluate', {
          expression: `(() => {
            return {
              totalExhibits: EUNOIA_CONFIG.exhibits.length,
              exhibitMeshes: exhibitMeshes.length,
              lunarExhibits: EUNOIA_CONFIG.exhibits.filter(e => e.room === 'lunar').length,
              wildlifeExhibits: EUNOIA_CONFIG.exhibits.filter(e => e.room === 'wildlife').length,
              activeVideos: activeHogwartsVideos.length
            };
          })()`,
          returnByValue: true
        });

        console.log('Final Museum State:', JSON.stringify(res.result.value, null, 2));
        console.log('Errors encountered:', errors.length ? errors : 'None! (0 errors)');

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

