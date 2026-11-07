html = open('index.html', encoding='utf-8').read()

old = """      ex.teleportPos = new THREE.Vector3(spot.viewX, EYE_HEIGHT, spot.viewZ);
      ex.lookTarget = new THREE.Vector3(spot.x, spot.y, spot.z);
      hungCount++;
    });
  }
"""
assert old in html, 'layout anchor missing'

new = """      ex.teleportPos = new THREE.Vector3(spot.viewX, EYE_HEIGHT, spot.viewZ);
      ex.lookTarget = new THREE.Vector3(spot.x, spot.y, spot.z);
      (poolSpots[ex.wing] = poolSpots[ex.wing] || []).push({
        x: spot.x, y: spot.y, z: spot.z, rotY: spot.rotY,
        land: ex.orientation === 'landscape'
      });
      hungCount++;
    });
  }
  buildLightPools(poolSpots);
"""
html = html.replace(old, new, 1)

# declare poolSpots at top of layoutExhibits
old_head = "function layoutExhibits() {\n  const groups = {};"
assert old_head in html
html = html.replace(old_head, "function layoutExhibits() {\n  const poolSpots = {};\n  const groups = {};", 1)

POOLS = r'''/* ---------------------------------------------------------------------------
   Baked picture-light pools: one additive wall glow per frame, merged into a
   single mesh per wing (4 draw calls total, zero real-time lights).
   --------------------------------------------------------------------------- */
function buildLightPools(poolSpots) {
  const [pc, pctx] = makeCanvas(256, 256);
  pctx.clearRect(0, 0, 256, 256);
  // broad scalloped wash falling down the wall from the lamp
  pctx.save();
  pctx.translate(128, 70);
  pctx.scale(1, 1.25);
  const wash = pctx.createRadialGradient(0, 0, 4, 0, 0, 122);
  wash.addColorStop(0.00, 'rgba(255,236,190,1.00)');
  wash.addColorStop(0.35, 'rgba(255,214,150,0.62)');
  wash.addColorStop(0.70, 'rgba(255,190,110,0.24)');
  wash.addColorStop(1.00, 'rgba(255,170,90,0)');
  pctx.fillStyle = wash;
  pctx.fillRect(-128, -70, 256, 256);
  pctx.restore();
  // hot spot right under the fixture
  const hot = pctx.createRadialGradient(128, 22, 1, 128, 22, 58);
  hot.addColorStop(0, 'rgba(255,248,220,0.95)');
  hot.addColorStop(1, 'rgba(255,230,170,0)');
  pctx.fillStyle = hot;
  pctx.fillRect(0, 0, 256, 256);

  const poolTex = new THREE.CanvasTexture(pc);
  poolTex.colorSpace = THREE.SRGBColorSpace;
  poolTex.generateMipmaps = false;
  poolTex.minFilter = THREE.LinearFilter;
  poolTex.magFilter = THREE.LinearFilter;
  const poolMat = new THREE.MeshBasicMaterial({
    map: poolTex, color: 0xffe2b0, transparent: true, opacity: 0.8,
    blending: THREE.AdditiveBlending, depthWrite: false, fog: false
  });
  poolMat.toneMapped = false;

  const wingGroups = { I: wingI_group, II: wingII_group, III: wingIII_group, IV: wingIV_group };
  Object.keys(poolSpots).forEach((wing) => {
    const geos = [];
    poolSpots[wing].forEach((s) => {
      const artW = s.land ? 2.6 : 1.95, artH = s.land ? 1.95 : 2.6;
      const pw = artW + 3.4, ph = artH + 3.0;
      const g = new THREE.PlaneGeometry(pw, ph);
      // texture hot spot sits near the top: shift plane so the lamp is ~ at the fixture height
      g.translate(0, artH / 2 + 0.55 - ph * 0.30, -0.008);
      g.rotateY(s.rotY);
      g.translate(s.x, s.y, s.z);
      geos.push(g);
    });
    if (!geos.length) return;
    const merged = mergeGeometries(geos, false);
    geos.forEach((g) => g.dispose());
    const mesh = new THREE.Mesh(merged, poolMat);
    mesh.renderOrder = 2;
    mesh.frustumCulled = false;
    wingGroups[wing].add(mesh);
  });
}

'''
anchor = "function layoutExhibits() {"
html = html.replace(anchor, POOLS + anchor, 1)
open('index.html', 'w', encoding='utf-8').write(html)
print('light pools added')

