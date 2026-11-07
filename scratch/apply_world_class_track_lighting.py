import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update buildLightPools
start_marker = "function buildLightPools(poolSpots) {"
end_marker = "function buildMuseumAtmosphere() {"

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Error: buildLightPools markers not found")
    exit(1)

new_build_light_pools = '''function buildLightPools(poolSpots) {
  // Scalloped Gallery Track Light Wall Wash (hyperbolic arc matching reference photo)
  const W = 512, H = 1024;
  const [pc, pctx] = makeCanvas(W, H);
  const imgData = pctx.createImageData(W, H);
  const data = imgData.data;
  // Apex sits at y = 55 (approx 5.4% from top of plane)
  const apex_y = 55.0;

  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      const nx = (x - W / 2.0) / (W / 2.0); // -1.0 to 1.0 across width
      const dy = y - apex_y;

      let intensity = 0.0;
      if (dy > 0.0) {
        // Hyperbolic cone spread expanding downward from spotlight angle
        const spread = 0.20 + 0.024 * Math.sqrt(dy * 10.0) + 0.00060 * dy;
        const norm_x = Math.abs(nx) / spread;

        if (norm_x < 1.0) {
          const radial = Math.pow(Math.cos(norm_x * Math.PI * 0.5), 1.40);
          // Rises below apex, washes across artwork zone, gently tapers to floor
          const vert = dy < 160.0
            ? Math.pow(dy / 160.0, 0.65)
            : Math.pow(Math.max(0.0, 1.0 - (dy - 160.0) / (H - apex_y - 160.0)), 1.30);

          // Warm core highlight right behind and over painting
          const coreDist = Math.hypot(nx * 1.30, (y - 420.0) / 320.0);
          const coreGlow = Math.pow(Math.max(0.0, 1.0 - coreDist / 1.15), 1.8) * 0.55;

          intensity = Math.min(1.0, radial * vert * 0.88 + coreGlow);
        }
      } else {
        // Soft feather just above apex towards ceiling rail
        const distAbove = -dy;
        if (distAbove < 45.0) {
          intensity = 0.08 * (1.0 - distAbove / 45.0) * Math.max(0.0, 1.0 - Math.abs(nx) * 3.0);
        }
      }

      // Smooth horizontal edge fade: guarantee exact zero at left and right borders of plane (no hard edges)
      const edgeFadeX = Math.pow(Math.cos(nx * Math.PI * 0.5), 0.70);
      intensity *= edgeFadeX;

      if (intensity > 0.002) {
        const idx = (y * W + x) * 4;
        data[idx]     = Math.min(255, 255 * intensity * 1.15) | 0;
        data[idx + 1] = Math.min(255, 238 * (intensity * 0.96 + 0.04)) | 0; // warm gallery halogen tint
        data[idx + 2] = Math.min(255, 188 * (intensity * 0.68 + 0.06)) | 0;
        data[idx + 3] = Math.min(255, 255 * Math.pow(intensity, 1.05)) | 0;
      }
    }
  }
  pctx.putImageData(imgData, 0, 0);

  const poolTex = new THREE.CanvasTexture(pc);
  poolTex.colorSpace = THREE.SRGBColorSpace;
  poolTex.generateMipmaps = true;
  poolTex.minFilter = THREE.LinearMipmapLinearFilter;
  poolTex.magFilter = THREE.LinearFilter;

  // Scalloped wall wash material: prominent, warm gallery wash sitting right on wall
  const poolMat = new THREE.MeshBasicMaterial({
    map: poolTex, transparent: true, opacity: 0.92,
    blending: THREE.AdditiveBlending, depthWrite: false, depthTest: true, side: THREE.DoubleSide
  });
  poolMat.toneMapped = false;

  // Floor wash texture: soft warm oval of light bouncing on floor in front of painting
  const [fc, fctx] = makeCanvas(256, 128);
  const fg = fctx.createRadialGradient(128, 64, 0, 128, 64, 120);
  fg.addColorStop(0.00, 'rgba(255,232,185,0.75)');
  fg.addColorStop(0.35, 'rgba(255,210,150,0.35)');
  fg.addColorStop(0.70, 'rgba(255,190,120,0.10)');
  fg.addColorStop(1.00, 'rgba(255,180,100,0)');
  fctx.fillStyle = fg; fctx.fillRect(0, 0, 256, 128);
  const floorPoolTex = new THREE.CanvasTexture(fc);
  floorPoolTex.colorSpace = THREE.SRGBColorSpace;
  const floorPoolMat = new THREE.MeshBasicMaterial({
    map: floorPoolTex, transparent: true, opacity: 0.38,
    blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide
  });
  floorPoolMat.toneMapped = false;

  // Track hardware materials: clean architectural satin white/aluminum matching reference photo
  const trackMat = new THREE.MeshBasicMaterial({ color: 0xe8e8e8 });
  const trackDarkMat = new THREE.MeshBasicMaterial({ color: 0x2b2b2b }); // dark adapter clamp
  const lensMat = new THREE.MeshBasicMaterial({ color: 0xfffae2 });     // glowing warm spotlight lens
  lensMat.toneMapped = false;

  // Subtle volumetric light cone from track head to painting
  const [bc, bctx] = makeCanvas(64, 256);
  const bg = bctx.createLinearGradient(0, 0, 0, 256);
  bg.addColorStop(0.00, 'rgba(255,245,210,0.85)');
  bg.addColorStop(0.30, 'rgba(255,225,170,0.25)');
  bg.addColorStop(1.00, 'rgba(255,210,150,0)');
  bctx.fillStyle = bg; bctx.fillRect(0, 0, 64, 256);
  const sg = bctx.createLinearGradient(0, 0, 64, 0);
  sg.addColorStop(0, 'rgba(0,0,0,1)'); sg.addColorStop(0.35, 'rgba(0,0,0,0)');
  sg.addColorStop(0.65, 'rgba(0,0,0,0)'); sg.addColorStop(1, 'rgba(0,0,0,1)');
  bctx.globalCompositeOperation = 'destination-out';
  bctx.fillStyle = sg; bctx.fillRect(0, 0, 64, 256);
  const beamTex = new THREE.CanvasTexture(bc);
  beamTex.colorSpace = THREE.SRGBColorSpace;

  const beamMat = new THREE.MeshBasicMaterial({
    map: beamTex, transparent: true, opacity: 0.055, blending: THREE.AdditiveBlending,
    depthWrite: false, side: THREE.DoubleSide, fog: false
  });
  beamMat.toneMapped = false;

  const wingGroups = { I: wingI_group, II: wingII_group, III: wingIII_group, IV: wingIV_group };

  Object.keys(poolSpots).forEach((wing) => {
    const wallGeos = [];
    const floorGeos = [];
    const trackGeos = [];
    const trackDarkGeos = [];
    const lensGeos = [];
    const beamGeos = [];

    poolSpots[wing].forEach((s) => {
      const isLand = s.land;
      const artW = isLand ? 2.6 : 1.95, artH = isLand ? 1.95 : 2.6;

      // 1. Scalloped Wall Wash Plane:
      // Height 3.65m. Top touches Y = 4.15m (just 5cm below H_WING = 4.2m).
      // Apex at y=55/1024 is at Y = 3.95m — well above both portrait and landscape frame tops!
      const wallW = artW + 2.2;
      const wallH = 3.65;
      const wallTop = H_WING - 0.05;
      const wallCenterY = wallTop - wallH / 2.0; // e.g. 4.15 - 1.825 = 2.325m
      const yShiftWall = wallCenterY - s.y;      // relative to frame center s.y

      const gWall = new THREE.PlaneGeometry(wallW, wallH);
      // Sits at z = +0.008 (flush on wall, behind the frame front & canvas)
      gWall.translate(0, yShiftWall, 0.008);
      gWall.rotateY(s.rotY);
      gWall.translate(s.x, s.y, s.z);
      wallGeos.push(gWall);

      // 2. Soft floor bounce light pool:
      // In front of the painting on the floor, laid flat
      const gFloor = new THREE.PlaneGeometry(artW + 1.2, 1.8);
      gFloor.rotateX(-Math.PI / 2);
      gFloor.translate(0, 0.015, 0.95); // 0.95m out from wall towards room
      gFloor.rotateY(s.rotY);
      gFloor.translate(s.x, 0, s.z);
      floorGeos.push(gFloor);

      // 3. Suspended Ceiling Track System:
      // Track rail is located ~1.85m out from wall, suspended ~0.24m below ceiling
      const ceilY = H_WING - s.y; // relative to frame center (e.g. 4.2 - 2.4 = 1.8m)
      const trackDist = 1.85;
      const trackRailY = ceilY - 0.24;

      // Continuous rail segment parallel to wall
      const railW = artW + 1.5;
      const gRail = new THREE.BoxGeometry(railW, 0.038, 0.048);
      gRail.translate(0, trackRailY, trackDist);
      gRail.rotateY(s.rotY);
      gRail.translate(s.x, s.y, s.z);
      trackGeos.push(gRail);

      // Suspension drop rods connecting track rail up to ceiling
      [-artW * 0.42, artW * 0.42].forEach((rx) => {
        const gRod = new THREE.CylinderGeometry(0.004, 0.004, 0.24, 6);
        gRod.translate(rx, ceilY - 0.12, trackDist);
        gRod.rotateY(s.rotY);
        gRod.translate(s.x, s.y, s.z);
        trackGeos.push(gRod);
      });

      // Track spotlight heads:
      // 2 heads for landscape (spaced -0.45, +0.45), 1 head for portrait (centered 0)
      const headOffsets = isLand ? [-0.45, 0.45] : [0.0];
      const spotAngle = Math.atan2(trackDist, trackRailY - 0.12); // angle down toward painting

      headOffsets.forEach((hx) => {
        // Track adapter clamp
        const gClamp = new THREE.BoxGeometry(0.045, 0.03, 0.065);
        gClamp.translate(hx, trackRailY - 0.025, trackDist);
        gClamp.rotateY(s.rotY);
        gClamp.translate(s.x, s.y, s.z);
        trackDarkGeos.push(gClamp);

        // Sleek cylindrical track canister
        const headY = trackRailY - 0.12;
        const gCanister = new THREE.CylinderGeometry(0.058, 0.058, 0.19, 14);
        gCanister.rotateX(Math.PI / 2); // align along Z
        gCanister.rotateX(-spotAngle);  // tilt down toward wall
        gCanister.translate(hx, headY, trackDist);
        gCanister.rotateY(s.rotY);
        gCanister.translate(s.x, s.y, s.z);
        trackGeos.push(gCanister);

        // Glowing lens disc at front of canister
        const gLens = new THREE.CircleGeometry(0.055, 12);
        gLens.rotateX(Math.PI);
        gLens.rotateX(-spotAngle);
        const lensOffZ = trackDist - Math.sin(spotAngle) * 0.10;
        const lensOffY = headY - Math.cos(spotAngle) * 0.10;
        gLens.translate(hx, lensOffY, lensOffZ);
        gLens.rotateY(s.rotY);
        gLens.translate(s.x, s.y, s.z);
        lensGeos.push(gLens);

        // Volumetric Air Beam connecting track head to painting
        const gBeam = new THREE.BufferGeometry();
        const topHalf = 0.08, botHalf = (artW / headOffsets.length) * 0.58;
        gBeam.setAttribute('position', new THREE.Float32BufferAttribute([
          hx - topHalf, lensOffY, lensOffZ,   hx + topHalf, lensOffY, lensOffZ,
          hx - botHalf, -artH * 0.45, 0.10,   hx + botHalf, -artH * 0.45, 0.10
        ], 3));
        gBeam.setAttribute('uv', new THREE.Float32BufferAttribute([0, 1, 1, 1, 0, 0, 1, 0], 2));
        gBeam.setAttribute('normal', new THREE.Float32BufferAttribute([0,0,1, 0,0,1, 0,0,1, 0,0,1], 3));
        gBeam.setIndex([0, 2, 1, 1, 2, 3]);
        gBeam.rotateY(s.rotY);
        gBeam.translate(s.x, s.y, s.z);
        beamGeos.push(gBeam);
      });
    });

    const mergeAndEmit = (list, mat, order) => {
      if (!list.length) return;
      const flat = list.map((p) => (p.index ? p.toNonIndexed() : p));
      const merged = mergeGeometries(flat, false);
      list.forEach((g) => g.dispose()); flat.forEach((p) => p.dispose());
      const mesh = new THREE.Mesh(merged, mat);
      mesh.renderOrder = order;
      mesh.frustumCulled = false;
      mesh.matrixAutoUpdate = false;
      wingGroups[wing].add(mesh);
    };

    mergeAndEmit(wallGeos, poolMat, 2);
    mergeAndEmit(floorGeos, floorPoolMat, 1);
    mergeAndEmit(trackGeos, trackMat, 1);
    mergeAndEmit(trackDarkGeos, trackDarkMat, 1);
    mergeAndEmit(lensGeos, lensMat, 1);
    mergeAndEmit(beamGeos, beamMat, 2);
  });
}

'''

# 2. Update buildMuseumAtmosphere so it only adds atmosphere in Grand Rotunda, leaving wings clean for track lighting
atmosphere_start = "function buildMuseumAtmosphere() {"
atmosphere_end = "function layoutExhibits() {"

atmo_start_idx = html.find(atmosphere_start)
atmo_end_idx = html.find(atmosphere_end)

if atmo_start_idx == -1 or atmo_end_idx == -1:
    print("Error: buildMuseumAtmosphere markers not found")
    exit(1)

new_build_atmosphere = '''function buildMuseumAtmosphere() {
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

  // Grand Rotunda recessed lighting ring
  const poolTex = mkTex(256, radial([
    [0.00, 'rgba(255,226,170,1)'], [0.30, 'rgba(255,205,140,0.55)'],
    [0.65, 'rgba(255,180,110,0.16)'], [1.00, 'rgba(255,170,100,0)']
  ]));
  const haloTex = mkTex(128, radial([
    [0.00, 'rgba(255,250,232,1)'], [0.12, 'rgba(255,240,205,0.95)'],
    [0.30, 'rgba(255,214,150,0.35)'], [1.00, 'rgba(255,200,130,0)']
  ]));
  const shaftTex = mkTex(128, (ctx, s) => {
    const g = ctx.createLinearGradient(0, 0, 0, s);
    g.addColorStop(0.00, 'rgba(255,232,185,0.95)');
    g.addColorStop(0.35, 'rgba(255,215,160,0.35)');
    g.addColorStop(1.00, 'rgba(255,200,140,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, s, s);
  });

  const poolMat = addMat(poolTex, 0.42);
  const haloMat = addMat(haloTex, 0.95);
  const shaftMat = addMat(shaftTex, 0.045);
  const discMat = new THREE.MeshBasicMaterial({ color: 0xfff4dc, fog: false });
  discMat.toneMapped = false;
  const trimMat = new THREE.MeshBasicMaterial({ color: 0x8a6a2e });

  const rb = { pool: [], halo: [], shaft: [], disc: [], trim: [] };

  function addRotundaDownlight(x, z, ceilY) {
    const pool = new THREE.PlaneGeometry(3.4, 3.4);
    pool.rotateX(-Math.PI / 2); pool.translate(x, 0.018, z); rb.pool.push(pool);

    const halo = new THREE.PlaneGeometry(1.5, 1.5);
    halo.rotateX(Math.PI / 2); halo.translate(x, ceilY - 0.012, z); rb.halo.push(halo);

    const disc = new THREE.CircleGeometry(0.13, 20);
    disc.rotateX(Math.PI / 2); disc.translate(x, ceilY - 0.018, z); rb.disc.push(disc);

    const trim = new THREE.RingGeometry(0.13, 0.17, 20);
    trim.rotateX(Math.PI / 2); trim.translate(x, ceilY - 0.016, z); rb.trim.push(trim);

    const h = ceilY - 0.05;
    const shaft = new THREE.CylinderGeometry(0.16, 1.15, h, 18, 1, true);
    shaft.translate(x, h / 2, z); rb.shaft.push(shaft);
  }

  // Grand Rotunda: 8 recessed architectural lights surrounding the central sculpture
  for (let i = 0; i < 8; i++) {
    const a = (i / 8) * TAU + TAU / 16;
    addRotundaDownlight(Math.cos(a) * 5.4, Math.sin(a) * 5.4, H_ROT);
  }

  const emit = (list, mat, order) => {
    if (!list.length) return;
    const flat = list.map((g) => (g.index ? g.toNonIndexed() : g));
    const merged = mergeGeometries(flat, false);
    list.forEach((g) => g.dispose()); flat.forEach((g) => g.dispose());
    const mesh = new THREE.Mesh(merged, mat);
    mesh.renderOrder = order;
    mesh.frustumCulled = false;
    mesh.matrixAutoUpdate = false;
    rotunda_group.add(mesh);
  };
  emit(rb.trim, trimMat, 0);
  emit(rb.disc, discMat, 0);
  emit(rb.halo, haloMat, 3);
  emit(rb.pool, poolMat, 3);
  emit(rb.shaft, shaftMat, 4);
}

'''

new_html = html[:start_idx] + new_build_light_pools + new_build_atmosphere + html[atmo_end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Successfully updated track lighting and cleaned atmosphere in index.html!")

