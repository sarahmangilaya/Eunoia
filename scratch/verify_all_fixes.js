const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

(async () => {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9238', '--no-sandbox', '--disable-web-security',
    '--allow-file-access-from-files', '--window-size=1280,720',
    '--user-data-dir=' + require('os').tmpdir() + '\\eu_verify_fixes'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  http.get('http://127.0.0.1:9238/json', (res) => {
    let d = ''; res.on('data', x => d += x);
    res.on('end', async () => {
      const t = JSON.parse(d).filter(x => x.type === 'page')[0];
      const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 1;
      const send = (method, params = {}) => new Promise(r => {
        const i = id++;
        const h = e => { const m = JSON.parse(e.data); if (m.id === i) { ws.removeEventListener('message', h); r(m.result); } };
        ws.addEventListener('message', h);
        ws.send(JSON.stringify({ id: i, method, params }));
      });
      const sleep = ms => new Promise(r => setTimeout(r, ms));

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
        await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });
        await sleep(3500);

        // Enter museum
        await send('Runtime.evaluate', {
          expression: "document.getElementById('btnEnter')?.click(); setTimeout(()=>document.getElementById('lobby')?.remove(),300)"
        });
        await sleep(4000);

        // Check close signs (z-fighting check)
        const signOverlapCheck = await send('Runtime.evaluate', {
          expression: `(() => {
            const signs = [];
            scene.traverse(c => {
              if (c.isMesh && c.geometry && c.geometry.type === 'PlaneGeometry' && c.material?.map?.image) {
                if (!c.geometry.boundingBox) c.geometry.computeBoundingBox();
                c.updateWorldMatrix(true, false);
                const b = c.geometry.boundingBox.clone().applyMatrix4(c.matrixWorld);
                signs.push({ box: b, center: b.getCenter(new THREE.Vector3()), size: b.getSize(new THREE.Vector3()) });
              }
            });
            const close = [];
            for (let i = 0; i < signs.length; i++) {
              for (let j = i + 1; j < signs.length; j++) {
                const dist = signs[i].center.distanceTo(signs[j].center);
                if (dist < 0.15) close.push({ dist: dist.toFixed(3), c1: signs[i].center, c2: signs[j].center });
              }
            }
            return { totalSigns: signs.length, closeSigns: close };
          })()`,
          returnByValue: true
        });
        console.log('SIGN OVERLAP CHECK:', JSON.stringify(signOverlapCheck.result.value));

        // Locations to capture
        const views = [
          { name: 'wing2_roomB_interior', x: 13.0, z: 17.5, yaw: Math.PI / 2, pitch: 0.05, desc: 'Wing II Room B (Interior Architecture)' },
          { name: 'wing2_char3d_studio', x: 0.0, z: 18.0, yaw: 0.0, pitch: 0.05, desc: 'Wing II Character Topology Promenade' },
          { name: 'wing4_cinema_view', x: 3.5, z: 57.0, yaw: 1.15, pitch: -0.02, desc: 'Wing IV Cinema Atrium Looking West' },
          { name: 'rotunda_wing1_entrance', x: 0.0, z: 0.0, yaw: Math.PI / 2, pitch: 0.0, desc: 'Rotunda facing Wing I Portal' },
          { name: 'wing2_to_wing4_portal', x: 0.0, z: 46.0, yaw: 0.0, pitch: 0.05, desc: 'Wing II facing Wing IV Portal at z=52' }
        ];

        for (const v of views) {
          await send('Runtime.evaluate', {
            expression: `camera.position.set(${v.x}, 1.7, ${v.z}); camera.rotation.set(${v.pitch}, ${v.yaw}, 0, 'YXZ');`
          });
          await sleep(1500);
          const s = await send('Page.captureScreenshot', { format: 'png' });
          fs.writeFileSync(`scratch/verified_${v.name}.png`, Buffer.from(s.data, 'base64'));
          console.log(`Saved scratch/verified_${v.name}.png (${v.desc})`);
        }

        console.log('ERRORS:', errors);
        chrome.kill();
        process.exit(0);
      };
    });
  });
})();

