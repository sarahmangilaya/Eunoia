const { spawn } = require('child_process');
const http = require('http');

async function run() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9223', '--disable-gpu-sandbox', '--no-sandbox',
    '--disable-web-security', '--allow-file-access-from-files', '--autoplay-policy=no-user-gesture-required',
    '--user-data-dir=' + require('os').tmpdir() + '\\eunoia_perf_profile'
  ]);
  await new Promise(r => setTimeout(r, 2500));

  http.get('http://127.0.0.1:9223/json', (res) => {
    let data = '';
    res.on('data', c => data += c);
    res.on('end', async () => {
      const targets = JSON.parse(data).filter(t => t.type === 'page');
      const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
      let id = 1;
      const send = (method, params = {}) => new Promise((resolve) => {
        const reqId = id++;
        const h = (evt) => { const m = JSON.parse(evt.data); if (m.id === reqId) { ws.removeEventListener('message', h); resolve(m.result); } };
        ws.addEventListener('message', h);
        ws.send(JSON.stringify({ id: reqId, method, params }));
      });
      const ev = async (expression) => {
        const r = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
        if (r.exceptionDetails) return { __error: r.exceptionDetails.exception?.description || r.exceptionDetails.text };
        return r.result.value;
      };
      const sleep = (ms) => new Promise(r => setTimeout(r, ms));

      const errors = [];
      ws.addEventListener('message', (e) => {
        const m = JSON.parse(e.data);
        if (m.method === 'Runtime.exceptionThrown') {
          const d = m.params.exceptionDetails;
          const txt = d.exception?.description || d.text;
          if (!/pointer lock|Pointer Lock/i.test(txt)) errors.push(txt);
        }
      });

      ws.onopen = async () => {
        await send('Page.enable'); await send('Runtime.enable');
        const t0 = Date.now();
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await sleep(3500);

        console.log('--- STARTUP ---');
        console.log('exhibits in config:', await ev('window.EUNOIA_CONFIG.exhibits.length'));
        console.log('catalog cards mounted at startup:', await ev("document.querySelectorAll('#catGrid .card').length"));
        console.log('videos with src at startup:', await ev('activeHogwartsVideos.filter(v => v.srcSet).length') + ' / ' + await ev('activeHogwartsVideos.length'));
        console.log('scene lights:', await ev("(() => { let n=0; scene.traverse(o => { if (o.isLight) n++; }); return n; })()"));
        console.log('shadowMap enabled:', await ev('renderer.shadowMap.enabled'));

        await ev("document.getElementById('btnEnter').click()");
        await sleep(500);
        await ev("document.getElementById('lobby')?.remove()");

        // let the throttled queue stream in textures (1 upload / frame)
        await sleep(15000);
        console.log('--- TEXTURE STREAMING (after ~18s) ---');
        console.log('loadTracker:', JSON.stringify(await ev('window.loadTracker')));
        console.log('queue left / uploads pending:', await ev('TextureLoadQueue.queue.length + " / " + TextureLoadQueue.uploads.length'));
        console.log('max GPU texture dim among art:', await ev(`(() => { let mx=0; window.exhibitMeshes.forEach(m => { const s = m.material.userData.texSize; if (s) mx = Math.max(mx, s[0], s[1]); }); return mx; })()`));
        console.log('art materials type:', await ev("window.exhibitMeshes[0].material.type"));

        const places = [
          ['Rotunda facing N', 0, 0, 0],
          ['Wing I', 22, 0, -Math.PI / 2],
          ['Wing II', 0, 25, 0],
          ['Wing III', -22, 0, Math.PI / 2],
          ['Wing IV cinema', 0, 60, 0]
        ];
        console.log('--- PER-WING (2s rAF sample) ---');
        const rows = [];
        for (const [name, x, z, yaw] of places) {
          await ev(`camera.position.set(${x}, 1.7, ${z}); camera.rotation.set(0, ${yaw}, 0, 'YXZ');`);
          await sleep(1200);
          const stats = await ev(`new Promise(res => { let f = 0, worst = 0, last = performance.now(); const t0 = last;
            function tick(){ const n = performance.now(); worst = Math.max(worst, n - last); last = n; f++; if (n - t0 < 2000) requestAnimationFrame(tick); else res({ fps: Math.round(f * 1000 / (n - t0)), worstFrameMs: Math.round(worst), calls: renderer.info.render.calls, tris: renderer.info.render.triangles, geoms: renderer.info.memory.geometries, tex: renderer.info.memory.textures, playing: activeHogwartsVideos.filter(v => !v.video.paused).length, withSrc: activeHogwartsVideos.filter(v => v.srcSet).length }); }
            requestAnimationFrame(tick); })`);
          rows.push({ name, ...stats });
        }
        console.table(rows);

        // Input must NOT wake videos any more
        await ev("camera.position.set(0,1.7,-4.5)");
        await sleep(800);
        await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'w', code: 'KeyW' });
        await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'w', code: 'KeyW' });
        await sleep(300);
        console.log('videos with src after WASD in Rotunda:', await ev('activeHogwartsVideos.filter(v => v.srcSet).length'));

        // Catalog lazy mount / unmount + render pause
        await ev("document.getElementById('btnIndex').click()");
        await sleep(400);
        console.log('catalog cards after open:', await ev("document.querySelectorAll('#catGrid .card').length"));
        console.log('<video> inside catalog:', await ev("document.querySelectorAll('#catGrid video').length"));
        await ev("document.getElementById('catClose').click()");
        await sleep(200);
        console.log('catalog cards after close:', await ev("document.querySelectorAll('#catGrid .card').length"));

        console.log('--- JS ERRORS ---', errors.length ? errors : 'none');
        console.log('total wall time', ((Date.now() - t0) / 1000).toFixed(1) + 's');
        chrome.kill(); process.exit(0);
      };
    });
  });
}
run();

