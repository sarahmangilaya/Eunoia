const { spawn } = require('child_process');
const http = require('http');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9268', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_test_depth'
  ]);
  await new Promise(r => setTimeout(r, 1500));
  http.get('http://127.0.0.1:9268/json', (res) => {
    let d = ''; res.on('data', x => d += x);
    res.on('end', async () => {
      const t = JSON.parse(d).filter(x => x.type === 'page')[0];
      const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 1;
      const send = (method, params = {}) => new Promise(r => { const i = id++; const h = e => { const m = JSON.parse(e.data); if (m.id === i) { ws.removeEventListener('message', h); r(m.result); } }; ws.addEventListener('message', h); ws.send(JSON.stringify({ id: i, method, params })); });
      ws.onopen = async () => {
        await send('Page.enable'); await send('Runtime.enable');
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await new Promise(r => setTimeout(r, 3000));
        const res = await send('Runtime.evaluate', {
          expression: `(() => {
            // Check Room B East wall exhibit spot: spot is at x = 21.86, z = 17.5, rotY = -PI/2
            // Let's find the solid wall and the pool mesh vertices around there
            let poolMesh = null;
            wingII_group.traverse(o => { if (o.isMesh && o.material && o.material.opacity === 0.68) poolMesh = o; });
            let solidWalls = [];
            wingII_group.traverse(o => { if (o.isMesh && o.material === Mat.wallWingII && o.geometry.type === 'BoxGeometry') solidWalls.push(o); });
            
            // Find solid wall near x = 22.0
            let eastWall = solidWalls.find(w => Math.abs(w.position.x - 22.0) < 0.5);
            return {
              solidEastWallPos: eastWall ? [eastWall.position.x, eastWall.position.y, eastWall.position.z] : null,
              solidEastWallBox: eastWall ? eastWall.geometry.parameters : null
            };
          })()`,
          returnByValue: true
        });
        console.log('Room B Wall info:', JSON.stringify(res.result.value, null, 2));
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

