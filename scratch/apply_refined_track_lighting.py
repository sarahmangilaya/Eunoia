import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect buildLightPools in index.html
start_marker = "function buildLightPools(poolSpots) {"
end_marker = "function buildMuseumAtmosphere() {"

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Error: markers not found")
    exit(1)

new_build_light_pools = '''function buildLightPools(poolSpots) {
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
          const vert = dy < 140.0
            ? Math.pow(dy / 140.0, 0.70)
            : Math.pow(Math.max(0.0, 1.0 - (dy - 140.0) / (H - apex_y - 140.0)), 1.25);

          const coreDist = Math.hypot(nx * 1.35, (y - 380.0) / 280.0);
          const coreGlow = Math.pow(Math.max(0.0, 1.0 - coreDist / 1.15), 1.8) * 0.52;

          intensity = Math.min(1.0, radial * vert * 0.88 + coreGlow);
        }
      } else {
        // Very subtle soft feather just above apex
        const distAbove = -dy;
        if (distAbove < 40.0) {
          intensity = 0.08 * (1.0 - distAbove / 40.0) * Math.max(0.0, 1.0 - Math.abs(nx) * 2.8);
        }
      }

      if (intensity > 0.002) {
        const idx = (y * W + x) * 4;
        data[idx]     = Math.min(255, 255 * intensity * 1.12) | 0;
        data[idx + 1] = Math.min(255, 240 * (intensity * 0.96 + 0.04)) | 0;
        data[idx + 2] = Math.min(255, 192 * (intensity * 0.68 + 0.06)) | 0;
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
    map: poolTex, transparent: true, opacity: 0.88,
    blending: THREE.AdditiveBlending, depthWrite: false, depthTest: true, side: THREE.DoubleSide
  });
  poolMat.toneMapped = false;

  // Track hardware materials: clean architectural satin white/aluminum matching reference photo
  const trackMat = new THREE.MeshBasicMaterial({ color: 0xe6e6e6 });
  const trackDarkMat = new THREE.MeshBasicMaterial({ color: 0x333333 }); // dark adapter clamp
  const lensMat = new THREE.MeshBasicMaterial({ color: 0xfffae0 });     // glowing warm spotlight lens
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
    const trackDarkGeos = [];
    const lensGeos = [];
    const beamGeos = [];

    poolSpots[wing].forEach((s) => {
      const isLand = s.land;
      const artW = isLand ? 2.6 : 1.95, artH = isLand ? 1.95 : 2.6;

      // 1. Scalloped Wall Wash Plane:
      // Sits at z = +0.008 (8mm in front of frame origin, flush on wall, behind the frame front & canvas)
      const wallW = artW + 2.2;
      const wallH = 3.4;
      const gWall = new THREE.PlaneGeometry(wallW, wallH);
      gWall.translate(0, 0, 0.008);
      gWall.rotateY(s.rotY);
      gWall.translate(s.x, s.y, s.z);
      wallGeos.push(gWall);

      // 2. Suspended Ceiling Track System:
      // Track rail is located ~1.85m out from wall, suspended ~0.22m below ceiling
      const ceilY = H_WING - s.y; // relative to frame center (e.g. 4.2 - 2.4 = 1.8m)
      const trackDist = 1.85;
      const trackRailY = ceilY - 0.22;

      // Continuous rail segment parallel to wall
      const railW = artW + 1.4;
      const gRail = new THREE.BoxGeometry(railW, 0.038, 0.048);
      gRail.translate(0, trackRailY, trackDist);
      gRail.rotateY(s.rotY);
      gRail.translate(s.x, s.y, s.z);
      trackGeos.push(gRail);

      // Suspension drop rods connecting track rail up to ceiling
      [-artW * 0.42, artW * 0.42].forEach((rx) => {
        const gRod = new THREE.CylinderGeometry(0.004, 0.004, 0.22, 6);
        gRod.translate(rx, ceilY - 0.11, trackDist);
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

        // 3. Volumetric Air Beam connecting track head to painting
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
    mergeAndEmit(trackGeos, trackMat, 1);
    mergeAndEmit(trackDarkGeos, trackDarkMat, 1);
    mergeAndEmit(lensGeos, lensMat, 1);
    mergeAndEmit(beamGeos, beamMat, 2);
  });
}

'''

new_html = html[:start_idx] + new_build_light_pools + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Successfully replaced buildLightPools in index.html!")

