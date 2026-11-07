html = open('index.html', encoding='utf-8').read()

ATMOS = r'''/* ---------------------------------------------------------------------------
   Museum atmosphere: recessed ceiling downlights, soft light shafts, warm floor
   pools and ceiling cove glow in every hallway & room. Fully baked: a handful of
   merged additive meshes per wing, ZERO extra real-time lights.
   --------------------------------------------------------------------------- */
function buildMuseumAtmosphere() {
  const mkTex = (size, painter) => {
    const [c, ctx] = makeCanvas(size, size);
    painter(ctx, size);
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    return t;
  };
  const radial = (stops) => (ctx, s) => {
    const g = ctx.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2);
    stops.forEach(([o, col]) => g.addColorStop(o, col));
    ctx.fillStyle = g; ctx.fillRect(0, 0, s, s);
  };
  const addMat = (map, opacity) => {
    const m = new THREE.MeshBasicMaterial({
      map, transparent: true, opacity, blending: THREE.AdditiveBlending,
      depthWrite: false, side: THREE.DoubleSide, fog: false
    });
    m.toneMapped = false;
    return m;
  };

  // Floor pool: warm, soft-edged ellipse of light under each downlight
  const poolTex = mkTex(256, radial([
    [0.00, 'rgba(255,226,170,1)'], [0.30, 'rgba(255,205,140,0.55)'],
    [0.65, 'rgba(255,180,110,0.16)'], [1.00, 'rgba(255,170,100,0)']
  ]));
  // Ceiling halo around each recessed fixture
  const haloTex = mkTex(128, radial([
    [0.00, 'rgba(255,250,232,1)'], [0.12, 'rgba(255,240,205,0.95)'],
    [0.30, 'rgba(255,214,150,0.35)'], [1.00, 'rgba(255,200,130,0)']
  ]));
  // Light shaft: bright at the fixture, fading out towards the floor
  const shaftTex = mkTex(128, (ctx, s) => {
    const g = ctx.createLinearGradient(0, 0, 0, s);
    g.addColorStop(0.00, 'rgba(255,232,185,0.95)');
    g.addColorStop(0.35, 'rgba(255,215,160,0.35)');
    g.addColorStop(1.00, 'rgba(255,200,140,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, s, s);
  });
  shaftTex.flipY = false; // v=0 (top of cylinder after flip) => bright end
  // Cove glow: strip fading from the wall edge into the ceiling
  const coveTex = mkTex(128, (ctx, s) => {
    const g = ctx.createLinearGradient(0, 0, 0, s);
    g.addColorStop(0.00, 'rgba(255,214,150,0.9)');
    g.addColorStop(0.45, 'rgba(255,200,135,0.25)');
    g.addColorStop(1.00, 'rgba(255,190,120,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, s, s);
  });

  const poolMat = addMat(poolTex, 0.42);
  const haloMat = addMat(haloTex, 0.95);
  const shaftMat = addMat(shaftTex, 0.07);
  const coveMat = addMat(coveTex, 0.55);
  const discMat = new THREE.MeshBasicMaterial({ color: 0xfff4dc, fog: false });
  discMat.toneMapped = false;
  const trimMat = new THREE.MeshBasicMaterial({ color: 0x8a6a2e });

  const floorMats = new Set([Mat.floorWingI, Mat.floorWingII, Mat.floorWingIII]);

  const buckets = new Map(); // group -> { pool:[], halo:[], shaft:[], disc:[], trim:[], cove:[] }
  const bucket = (g) => {
    if (!buckets.has(g)) buckets.set(g, { pool: [], halo: [], shaft: [], disc: [], trim: [], cove: [] });
    return buckets.get(g);
  };

  function addDownlight(b, x, z, ceilY) {
    const pool = new THREE.PlaneGeometry(3.4, 3.4);
    pool.rotateX(-Math.PI / 2); pool.translate(x, 0.018, z); b.pool.push(pool);

    const halo = new THREE.PlaneGeometry(1.5, 1.5);
    halo.rotateX(Math.PI / 2); halo.translate(x, ceilY - 0.012, z); b.halo.push(halo);

    const disc = new THREE.CircleGeometry(0.13, 20);
    disc.rotateX(Math.PI / 2); disc.translate(x, ceilY - 0.018, z); b.disc.push(disc);

    const trim = new THREE.RingGeometry(0.13, 0.17, 20);
    trim.rotateX(Math.PI / 2); trim.translate(x, ceilY - 0.016, z); b.trim.push(trim);

    const h = ceilY - 0.05;
    const shaft = new THREE.CylinderGeometry(0.16, 1.15, h, 18, 1, true);
    shaft.translate(x, h / 2, z); b.shaft.push(shaft);
  }

  function addCove(b, cx, cz, w, d, ceilY) {
    const band = 0.9, y = ceilY - 0.02;
    const strip = (len, px, pz, rotY) => {
      const g = new THREE.PlaneGeometry(len, band);
      g.translate(0, -band / 2, 0);       // top edge (bright) at the wall line
      g.rotateX(Math.PI / 2);              // lay flat on the ceiling, facing down
      g.rotateY(rotY);
      g.translate(px, y, pz);
      b.cove.push(g);
    };
    strip(w, cx, cz - d / 2, 0);
    strip(w, cx, cz + d / 2, Math.PI);
    strip(d, cx - w / 2, cz, -Math.PI / 2);
    strip(d, cx + w / 2, cz, Math.PI / 2);
  }

  // 1. Every wing floor plane gets a grid of downlights + a ceiling cove
  [wingI_group, wingII_group, wingIII_group, wingIV_group].forEach((wg) => {
    wg.updateMatrixWorld(true);
    const b = bucket(wg);
    wg.traverse((m) => {
      if (!m.isMesh || !floorMats.has(m.material) || m.geometry.type !== 'PlaneGeometry') return;
      const { width: w, height: d } = m.geometry.parameters;
      const cx = m.position.x, cz = m.position.z;
      const spacing = 4.6, inset = 1.6;
      const nx = Math.max(1, Math.round((w - inset * 2) / spacing) + 1);
      const nz = Math.max(1, Math.round((d - inset * 2) / spacing) + 1);
      // Narrow hallways: single centre line of lights
      const cols = w < 11 ? 1 : nx, rows = d < 11 ? 1 : nz;
      for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
          const x = cols === 1 ? cx : cx - w / 2 + inset + (i * (w - inset * 2)) / (cols - 1);
          const z = rows === 1 ? cz : cz - d / 2 + inset + (j * (d - inset * 2)) / (rows - 1);
          addDownlight(b, x, z, H_WING);
        }
      }
      // Long hallways also get lights along their length
      if (cols === 1 && rows === 1) {
        const long = Math.max(w, d), n = Math.max(1, Math.round((long - inset * 2) / spacing) + 1);
        for (let k = 0; k < n; k++) {
          const t = n === 1 ? 0 : -long / 2 + inset + (k * (long - inset * 2)) / (n - 1);
          if (Math.abs(t) < 0.01 && n % 2 === 1) continue; // centre one already placed
          addDownlight(b, w >= d ? cx + t : cx, w >= d ? cz : cz + t, H_WING);
        }
      }
      addCove(b, cx, cz, w, d, H_WING);
    });
  });

  // 2. Grand Rotunda: ring of recessed lights around the sculpture
  const rb = bucket(rotunda_group);
  for (let i = 0; i < 8; i++) {
    const a = (i / 8) * TAU + TAU / 16;
    addDownlight(rb, Math.cos(a) * 5.4, Math.sin(a) * 5.4, H_ROT);
  }

  // 3. Merge everything: <= 6 draw calls per wing
  buckets.forEach((b, group) => {
    const emit = (list, mat, order) => {
      if (!list.length) return;
      const flat = list.map((g) => (g.index ? g.toNonIndexed() : g));
      const merged = mergeGeometries(flat, false);
      list.forEach((g) => g.dispose()); flat.forEach((g) => g.dispose());
      const mesh = new THREE.Mesh(merged, mat);
      mesh.renderOrder = order;
      mesh.frustumCulled = false;
      mesh.matrixAutoUpdate = false;
      group.add(mesh);
    };
    emit(b.trim, trimMat, 0);
    emit(b.disc, discMat, 0);
    emit(b.cove, coveMat, 3);
    emit(b.halo, haloMat, 3);
    emit(b.pool, poolMat, 3);
    emit(b.shaft, shaftMat, 4);
  });
}

'''

anchor = "function layoutExhibits() {"
assert anchor in html
html = html.replace(anchor, ATMOS + anchor, 1)

old_call = "layoutExhibits();\r\nbuildLighting();"
if old_call not in html:
    old_call = "layoutExhibits();\nbuildLighting();"
assert old_call in html
html = html.replace(old_call, old_call.replace("buildLighting();", "buildLighting();\nbuildMuseumAtmosphere();"), 1)

# Brighter, warmer overall exposure and less oppressive fog in long halls
html = html.replace("renderer.toneMappingExposure = 0.88;", "renderer.toneMappingExposure = 1.0;", 1)
html = html.replace("scene.fog = new THREE.Fog(0x001514, 16, 52);", "scene.fog = new THREE.Fog(0x120d08, 28, 85);", 1)

open('index.html', 'w', encoding='utf-8').write(html)
print('atmosphere added')

