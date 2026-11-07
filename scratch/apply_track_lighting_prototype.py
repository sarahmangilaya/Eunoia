import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update ART_SPOT_LIGHTMAP
art_lightmap_code = """const ART_SPOT_LIGHTMAP = (() => {
  const S = 256;
  const [c, ctx] = makeCanvas(S, S);
  const img = ctx.createImageData(S, S);
  // Ceiling track spotlight hitting the canvas at ~38 degree downward angle:
  // Brightest core across the upper-third of the painting, smoothly washing down across the canvas.
  for (let y = 0; y < S; y++) {
    const ny = y / (S - 1); // 0 = top of painting, 1 = bottom
    for (let x = 0; x < S; x++) {
      const nx = x / (S - 1) - 0.5; // -0.5 to 0.5 across width
      const dy = ny + 0.18;
      const dist = Math.hypot(nx * 1.05, dy * 0.82);
      // Soft elliptical cone spreading downward
      const cone = Math.pow(Math.max(0, 1.0 - (Math.abs(nx) / (0.38 + dy * 0.45))), 1.25);
      const fall = Math.pow(Math.max(0, 1.0 - (dist / 1.50)), 1.35);
      const spot = cone * fall;
      // Multiplier: 0.85 baseline ambient up to 1.32 peak spotlight core
      const t = 0.85 + 0.47 * spot;
      const i = (y * S + x) * 4;
      img.data[i]     = Math.min(255, 255 * t) | 0;
      img.data[i + 1] = Math.min(255, 247 * t) | 0; // warm gallery halogen tint
      img.data[i + 2] = Math.min(255, 228 * t) | 0;
      img.data[i + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
})();
const ART_SPOT_INTENSITY = Math.PI; // Exact 1.0x factor"""

html = re.sub(
    r'const ART_SPOT_LIGHTMAP = \(\(\) => \{.*?\}\)\(\);\s*const ART_SPOT_INTENSITY = [^;]+;',
    art_lightmap_code,
    html,
    flags=re.DOTALL
)
print("Updated ART_SPOT_LIGHTMAP!")

# 2. Update FrameGeoCache: replace clunky clamped brass lamp with sleek gallery hanging wires
wire_cache_code = """/* Gallery Hanging Wires: sleek vertical wires extending from frame top up towards ceiling track */
function buildHangingWires(artW, artH) {
  const parts = [];
  const wireH = Math.max(0.4, H_WING - 2.4 - artH / 2);
  const wireGeo = new THREE.CylinderGeometry(0.002, 0.002, wireH, 4);
  const wireY = artH / 2 + wireH / 2;
  const sx = artW * 0.32;
  [-sx, sx].forEach((x) => {
    const w = wireGeo.clone();
    w.translate(x, wireY, -0.01);
    parts.push(w);
  });
  const flatParts = parts.map((p) => (p.index ? p.toNonIndexed() : p));
  const merged = mergeGeometries(flatParts, false);
  parts.forEach((p) => p.dispose()); flatParts.forEach((p) => p.dispose());
  return merged;
}
FrameGeoCache.wiresLandscape = buildHangingWires(2.6, 1.95);
FrameGeoCache.wiresPortrait = buildHangingWires(1.95, 2.6);
const WIRE_MAT = new THREE.MeshBasicMaterial({ color: 0x777777 });"""

html = re.sub(
    r'function buildMergedFixture\(artH\) \{.*?const LAMP_BULB_MAT = [^;]+;',
    wire_cache_code,
    html,
    flags=re.DOTALL
)
print("Updated FrameGeoCache hanging wires!")

# 3. Update buildPictureFrame to use hanging wires instead of clamped lamps
frame_fixture_old = re.compile(
    r'// Brass lamp: 4 parts merged into 1 geometry \+ 1 shared glowing bulb.*?'
    r'group\.add\(fixture, lampBulb\);',
    re.DOTALL
)
frame_fixture_new = """// Modern gallery hanging wires extending from top of frame to ceiling rail
  const wiresGeo = artH === 1.95 ? FrameGeoCache.wiresLandscape
                 : artH === 2.6 ? FrameGeoCache.wiresPortrait
                 : buildHangingWires(artW, artH);
  const wiresMesh = flat(new THREE.Mesh(wiresGeo, WIRE_MAT));
  group.add(wiresMesh);"""

html, n_wire = frame_fixture_old.subn(frame_fixture_new, html)
print(f"Replaced picture frame fixtures with hanging wires: {n_wire}")

# 4. Update buildLightPools: generate scalloped wall wash + ceiling track rail and canister spots!
build_light_pools_code = """function buildLightPools(poolSpots) {
  // Scalloped Gallery Track Light Wall Wash (hyperbolic arc matching reference photo)
  const W = 512, H = 1024;
  const [pc, pctx] = makeCanvas(W, H);
  const imgData = pctx.createImageData(W, H);
  const data = imgData.data;
  const apex_y = 110.0; // rounded arch apex on upper wall

  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      const nx = (x - W / 2.0) / (W / 2.0); // -1.0 to 1.0 across width
      const dy = y - apex_y;

      let intensity = 0.0;
      if (dy > 0.0) {
        // Conical / hyperbolic spread expanding downward
        const spread = 0.22 + 0.026 * Math.sqrt(dy * 12.0) + 0.00065 * dy;
        const norm_x = Math.abs(nx) / spread;

        if (norm_x < 1.0) {
          const radial = Math.pow(Math.cos(norm_x * Math.PI * 0.5), 1.35);
          // Rises below apex, covers artwork zone, tapers gently to floor
          const vert = dy < 130.0
            ? Math.pow(dy / 130.0, 0.75)
            : Math.pow(Math.max(0.0, 1.0 - (dy - 130.0) / (H - apex_y - 130.0)), 1.25);

          const coreDist = Math.hypot(nx * 1.4, (y - 390.0) / 290.0);
          const coreGlow = Math.pow(Math.max(0.0, 1.0 - coreDist / 1.15), 1.8) * 0.48;

          intensity = Math.min(1.0, radial * vert * 0.85 + coreGlow);
        }
      } else {
        // Very subtle soft feather just above apex
        const distAbove = -dy;
        if (distAbove < 35.0) {
          intensity = 0.05 * (1.0 - distAbove / 35.0) * Math.max(0.0, 1.0 - Math.abs(nx) * 3.0);
        }
      }

      if (intensity > 0.002) {
        const idx = (y * W + x) * 4;
        data[idx]     = Math.min(255, 255 * intensity * 1.08) | 0;
        data[idx + 1] = Math.min(255, 238 * (intensity * 0.96 + 0.04)) | 0;
        data[idx + 2] = Math.min(255, 185 * (intensity * 0.65 + 0.05)) | 0;
        data[idx + 3] = Math.min(255, 255 * Math.pow(intensity, 1.1)) | 0;
      }
    }
  }
  pctx.putImageData(imgData, 0, 0);

  const poolTex = new THREE.CanvasTexture(pc);
  poolTex.colorSpace = THREE.SRGBColorSpace;
  poolTex.generateMipmaps = true;
  poolTex.minFilter = THREE.LinearMipmapLinearFilter;
  poolTex.magFilter = THREE.LinearFilter;

  // Scalloped wall wash material: prominent, warm gallery wash
  const poolMat = new THREE.MeshBasicMaterial({
    map: poolTex, transparent: true, opacity: 0.68,
    blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide
  });
  poolMat.toneMapped = false;

  // Track hardware materials
  const trackMat = new THREE.MeshBasicMaterial({ color: 0x4a4a4a }); // sleek dark architectural track
  const lensMat = new THREE.MeshBasicMaterial({ color: 0xfffae0 });  // glowing warm spotlight lens
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
    map: beamTex, transparent: true, opacity: 0.05, blending: THREE.AdditiveBlending,
    depthWrite: false, side: THREE.DoubleSide, fog: false
  });
  beamMat.toneMapped = false;

  const wingGroups = { I: wingI_group, II: wingII_group, III: wingIII_group, IV: wingIV_group };

  Object.keys(poolSpots).forEach((wing) => {
    const wallGeos = [];
    const trackGeos = [];
    const lensGeos = [];
    const beamGeos = [];

    poolSpots[wing].forEach((s) => {
      const isLand = s.land;
      const artW = isLand ? 2.6 : 1.95, artH = isLand ? 1.95 : 2.6;

      // 1. Scalloped Wall Wash Plane:
      // Spans from near ceiling (Y=3.9m) down past frame to lower wall (Y=0.5m)
      const wallW = artW + 2.0;
      const wallH = 3.4;
      const yShiftWall = 0.0; // centered at frame center (Y=2.4), spanning 0.7m to 4.1m
      const gWall = new THREE.PlaneGeometry(wallW, wallH);
      gWall.translate(0, yShiftWall, -0.015);
      gWall.rotateY(s.rotY);
      gWall.translate(s.x, s.y, s.z);
      wallGeos.push(gWall);

      // 2. Suspended Ceiling Track System:
      // Track is located ~1.85m out from wall, just below ceiling
      const ceilY = H_WING - s.y; // relative to frame center (e.g. 4.2 - 2.4 = 1.8m)
      const trackDist = 1.85;

      // Track rail segment running along ceiling parallel to the wall
      const railW = artW + 1.2;
      const gRail = new THREE.BoxGeometry(railW, 0.035, 0.05);
      gRail.translate(0, ceilY - 0.02, trackDist);
      gRail.rotateY(s.rotY);
      gRail.translate(s.x, s.y, s.z);
      trackGeos.push(gRail);

      // Track spotlight canister angled down toward painting
      const spotAngle = Math.atan2(trackDist, ceilY - 0.15); // ~46 degrees down-tilt
      const gCanister = new THREE.CylinderGeometry(0.055, 0.055, 0.18, 12);
      gCanister.rotateX(Math.PI / 2); // align along Z
      gCanister.rotateX(-spotAngle); // tilt down toward wall
      gCanister.translate(0, ceilY - 0.15, trackDist);
      gCanister.rotateY(s.rotY);
      gCanister.translate(s.x, s.y, s.z);
      trackGeos.push(gCanister);

      // Glowing lens disc at the front face of the canister
      const gLens = new THREE.CircleGeometry(0.052, 12);
      gLens.rotateX(Math.PI);
      gLens.rotateX(-spotAngle);
      // Offset along the angled beam axis
      const lensOffZ = trackDist - Math.sin(spotAngle) * 0.095;
      const lensOffY = (ceilY - 0.15) - Math.cos(spotAngle) * 0.095;
      gLens.translate(0, lensOffY, lensOffZ);
      gLens.rotateY(s.rotY);
      gLens.translate(s.x, s.y, s.z);
      lensGeos.push(gLens);

      // 3. Volumetric Air Beam connecting track head to painting
      const gBeam = new THREE.BufferGeometry();
      const topHalf = 0.08, botHalf = artW * 0.55;
      gBeam.setAttribute('position', new THREE.Float32BufferAttribute([
        -topHalf, lensOffY, lensOffZ,   topHalf, lensOffY, lensOffZ,
        -botHalf, -artH * 0.45, 0.10,   botHalf, -artH * 0.45, 0.10
      ], 3));
      gBeam.setAttribute('uv', new THREE.Float32BufferAttribute([0, 1, 1, 1, 0, 0, 1, 0], 2));
      gBeam.setAttribute('normal', new THREE.Float32BufferAttribute([0,0,1, 0,0,1, 0,0,1, 0,0,1], 3));
      gBeam.setIndex([0, 2, 1, 1, 2, 3]);
      gBeam.rotateY(s.rotY);
      gBeam.translate(s.x, s.y, s.z);
      beamGeos.push(gBeam);
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
    mergeAndEmit(trackGeos, trackMat, 1);
    mergeAndEmit(lensGeos, lensMat, 1);
    mergeAndEmit(beamGeos, beamMat, 2);
  });
}"""

html = re.sub(
    r'function buildLightPools\(poolSpots\) \{.*?\}\n\nfunction buildMuseumAtmosphere',
    build_light_pools_code + "\n\nfunction buildMuseumAtmosphere",
    html,
    flags=re.DOTALL
)
print("Updated buildLightPools!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated index.html with gallery track lighting!")

