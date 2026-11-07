const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');

(async () => {
  const port = 9295;
  const tmpDir = path.join(os.tmpdir(), 'eu_mobile_test_' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--no-sandbox',
    '--disable-web-security',
    '--allow-file-access-from-files',
    `--user-data-dir=${tmpDir}`,
    '--window-size=414,896' // Mobile iPhone size
  ]);

  await new Promise(r => setTimeout(r, 2200));

  http.get(`http://127.0.0.1:${port}/json`, (res) => {
    let d = ''; res.on('data', x => d += x);
    res.on('end', async () => {
      const tabs = JSON.parse(d).filter(x => x.type === 'page');
      if (!tabs.length) {
        chrome.kill();
        process.exit(1);
      }
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

      const errors = [];
      ws.addEventListener('message', e => {
        const m = JSON.parse(e.data);
        if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') {
          errors.push(m.params.args.map(a => a.value || a.description).join(' '));
        }
        if (m.method === 'Runtime.exceptionThrown') {
          errors.push('EXCEPTION: ' + JSON.stringify(m.params.exceptionDetails));
        }
      });

      ws.onopen = async () => {
        await send('Page.enable');
        await send('Runtime.enable');

        // 1. Emulate Mobile Device (iPhone 14 Pro: 393 x 852, mobile=true, touch=true)
        await send('Emulation.setDeviceMetricsOverride', {
          width: 393,
          height: 852,
          deviceScaleFactor: 2,
          mobile: true
        });
        await send('Emulation.setTouchEmulationEnabled', {
          enabled: true,
          maxTouchPoints: 5
        });
        await send('Network.setUserAgentOverride', {
          userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1'
        });

        await send('Page.navigate', { url: 'file:///C:/Users/JM/Documents/Websites/Eunoia/index.html' });

        // Wait until application is ready
        console.log('Waiting for museum app to initialize...');
        for (let i = 0; i < 60; i++) {
          const ready = await send('Runtime.evaluate', { expression: "typeof window.enterExhibition === 'function'" });
          if (ready && ready.result && ready.result.value === true) {
            console.log('Museum app initialized successfully!');
            break;
          }
          await new Promise(r => setTimeout(r, 300));
        }

        // Portrait Lobby Screenshot
        let snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/mobile_portrait_lobby.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved mobile_portrait_lobby.png');

        // Tap Enter Exhibition via window.enterExhibition()
        await send('Runtime.evaluate', { expression: "window.enterExhibition()" });
        await new Promise(r => setTimeout(r, 1200));

        // Check mobile status
        const mobStatus = await send('Runtime.evaluate', {
          expression: `(() => {
            const jBase = document.getElementById('joystickBase');
            const r = jBase ? jBase.getBoundingClientRect() : null;
            return {
              lobbyOut: document.getElementById('lobby')?.classList.contains('out'),
              joystickVisible: document.getElementById('virtualJoystick')?.classList.contains('visible'),
              joystickRect: r ? { left: r.left, top: r.top, width: r.width, height: r.height } : null,
              cameraPos: camera ? { x: camera.position.x, y: camera.position.y, z: camera.position.z } : null
            };
          })()`,
          returnByValue: true
        });
        console.log('Mobile Gallery Status:', JSON.stringify(mobStatus?.result?.value));

        // Portrait Gallery View with Virtual Joystick
        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/mobile_portrait_gallery.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved mobile_portrait_gallery.png');

        // Test Virtual Joystick Movement Forward (simulating touch on joystick)
        await send('Runtime.evaluate', {
          expression: `(() => {
            if (window.joystickMove) {
              window.joystickMove.x = 0;
              window.joystickMove.y = -0.9;
            }
          })()`
        });
        // Let physics run for 800ms
        await new Promise(r => setTimeout(r, 800));

        // Release joystick
        await send('Runtime.evaluate', {
          expression: `(() => {
            if (window.joystickMove) {
              window.joystickMove.x = 0;
              window.joystickMove.y = 0;
            }
          })()`
        });

        const movedPos = await send('Runtime.evaluate', {
          expression: `({ x: camera.position.x, y: camera.position.y, z: camera.position.z })`,
          returnByValue: true
        });
        console.log('Player moved forward to:', movedPos.result.value);

        // Position player in front of Exhibit in Wing I
        const targetExhibitInfo = await send('Runtime.evaluate', {
          expression: `(() => {
            const ex = EUNOIA_CONFIG.exhibits.find(e => e.wing === 'I') || EUNOIA_CONFIG.exhibits[0];
            const mesh = exhibitMeshes.find(m => m.userData?.exhibit?.id === ex.id);
            if (!mesh) return { error: 'No mesh found' };
            const g = mesh.userData.group;
            // Position camera 2.2 meters in front of painting
            const worldPos = new THREE.Vector3();
            mesh.getWorldPosition(worldPos);
            // Move camera back along the normal
            const normal = new THREE.Vector3(0, 0, 1).applyQuaternion(mesh.getWorldQuaternion(new THREE.Quaternion()));
            camera.position.copy(worldPos).addScaledVector(normal, 2.2);
            camera.position.y = 1.7;
            camera.lookAt(worldPos.x, 1.7, worldPos.z);
            camera.rotation.order = 'YXZ';
            camera.rotation.setFromQuaternion(camera.quaternion, 'YXZ');
            updateRaycast();
            return {
              title: ex.title,
              id: ex.id,
              hasHover: !!hoveredExhibitMesh,
              reticleActive: document.getElementById('reticle')?.classList.contains('active'),
              promptShown: document.getElementById('prompt')?.classList.contains('show'),
              promptText: document.getElementById('promptText')?.textContent
            };
          })()`,
          returnByValue: true
        });
        console.log('Target Exhibit Hover Status:', JSON.stringify(targetExhibitInfo?.result?.value));
        await new Promise(r => setTimeout(r, 600));

        // Portrait view looking directly at Exhibit with active reticle
        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/mobile_portrait_target.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved mobile_portrait_target.png');

        // Tap Crosshair to inspect the targeted exhibit!
        console.log('Tapping crosshair reticle on mobile touch screen...');
        await send('Runtime.evaluate', {
          expression: `(() => {
            document.getElementById('reticle')?.click();
          })()`
        });
        await new Promise(r => setTimeout(r, 1000));

        // Portrait Curatorial Plaque open bottom sheet
        const plaqueState = await send('Runtime.evaluate', {
          expression: `(() => {
            const p = document.getElementById('plaque');
            return {
              isOpen: p?.classList.contains('open'),
              title: document.getElementById('plqTitle')?.textContent,
              joystickVisible: document.getElementById('virtualJoystick')?.classList.contains('visible')
            };
          })()`,
          returnByValue: true
        });
        console.log('Plaque State after Reticle Tap:', JSON.stringify(plaqueState?.result?.value));

        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/mobile_portrait_plaque.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved mobile_portrait_plaque.png');

        // Close plaque
        await send('Runtime.evaluate', {
          expression: `(() => {
            window.exitInspection();
          })()`
        });
        await new Promise(r => setTimeout(r, 600));

        // Portrait Card Modal opened by pressing crosshair
        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/mobile_portrait_card_modal.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved mobile_portrait_card_modal.png');

        // Close modal and test Portrait Catalog
        await send('Runtime.evaluate', {
          expression: `(() => {
            if (window.closeCardModal) closeCardModal();
            document.getElementById('btnIndex')?.click();
          })()`
        });
        await new Promise(r => setTimeout(r, 800));

        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/mobile_portrait_catalog.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved mobile_portrait_catalog.png');

        // 2. NOW TEST LANDSCAPE MODE (852 x 393)
        await send('Emulation.setDeviceMetricsOverride', {
          width: 852,
          height: 393,
          deviceScaleFactor: 2,
          mobile: true
        });
        await new Promise(r => setTimeout(r, 500));

        // Landscape Catalog
        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/mobile_landscape_catalog.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved mobile_landscape_catalog.png');

        // Close catalog in landscape -> Gallery view with joystick
        await send('Runtime.evaluate', {
          expression: `document.getElementById('catClose')?.click()`
        });
        await new Promise(r => setTimeout(r, 600));

        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/mobile_landscape_gallery.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved mobile_landscape_gallery.png');

        // Open Dossier Card in Landscape
        await send('Runtime.evaluate', {
          expression: `if (window.openCardModal) openCardModal()`
        });
        await new Promise(r => setTimeout(r, 600));

        snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/mobile_landscape_card_modal.png', Buffer.from(snap.data, 'base64'));
        console.log('Saved mobile_landscape_card_modal.png');

        console.log('Console Errors:', errors.filter(e => !e.includes('WrongDocumentError')));

        chrome.kill();
        process.exit(0);
      };
    });
  });
})();
