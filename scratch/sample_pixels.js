const fs = require('fs');
// Let's decode PNG or sample using Chrome!
const { spawn } = require('child_process');
const http = require('http');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9276', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_test2g_' + Date.now()
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9276/json', (res) => {
    let d = ''; res.on('data', x => d += x);
    res.on('end', async () => {
      const t = JSON.parse(d).filter(x => x.type === 'page')[0];
      const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 1;
      const send = (method, params = {}) => new Promise(r => { const i = id++; const h = e => { const m = JSON.parse(e.data); if (m.id === i) { ws.removeEventListener('message', h); r(m.result); } }; ws.addEventListener('message', h); ws.send(JSON.stringify({ id: i, method, params })); });

      ws.onopen = async () => {
        await send('Page.enable'); await send('Runtime.enable');
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 3500));
        await send('Runtime.evaluate', { expression: "document.getElementById('btnEnter')?.click()" });
        await new Promise(r => setTimeout(r, 2000));

        // Sample pixel colors from the WebGL canvas directly!
        const res = await send('Runtime.evaluate', {
          expression: `(() => {
            // Position camera looking directly at the painting in II_interior
            camera.position.set(13.0, 2.0, 13.0);
            camera.rotation.set(0, 0, 0, 'YXZ');
            renderer.render(scene, camera);

            const gl = renderer.getContext();
            const w = gl.drawingBufferWidth, h = gl.drawingBufferHeight;
            const pixels = new Uint8Array(w * h * 4);
            gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, pixels);

            // Sample vertical column at center of screen (x = w / 2) from y = h/2 (painting) to top of wall
            const col = [];
            const cx = Math.floor(w / 2);
            for (let y = Math.floor(h * 0.4); y < Math.floor(h * 0.9); y += Math.floor(h * 0.05)) {
              const idx = (y * w + cx) * 4;
              col.push({
                screenY: y,
                r: pixels[idx], g: pixels[idx+1], b: pixels[idx+2]
              });
            }
            return JSON.stringify(col);
          })()`
        });
        console.log('Vertical sample above painting:', res.result ? res.result.value : res);

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

