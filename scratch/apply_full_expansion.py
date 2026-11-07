import json, re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Load full 205 exhibits catalog
with open('scratch/full_catalog.json', 'r', encoding='utf-8') as f:
    full_catalog = json.load(f)

print(f"Loaded {len(full_catalog)} exhibits from catalog")

# Replace exhibits array
start_needle = '  exhibits: ['
start_idx = content.find(start_needle)
if start_idx == -1:
    raise ValueError("start needle not found")

end_needle = ']\n};\n\n/* ==========================================================================\n   §4  ENGINE'
end_idx = content.find(end_needle)
if end_idx == -1:
    raise ValueError("end needle not found")

catalog_json_str = json.dumps(full_catalog, indent=4)
new_exhibits_block = f"  exhibits: {catalog_json_str}\n}};"
content = content[:start_idx] + new_exhibits_block + content[end_idx + len(']\n};'):]
print("Replaced exhibits array!")

# 2. Update rotunda board directory text in buildArchitecture
old_rot_board = """      ctx.fillStyle = '#e6af2e'; ctx.fillText('← Wing III · The Nocturne & Astrophotography (32 Works)', w / 2, 290);
      ctx.fillStyle = '#fbfffe'; ctx.fillText('↑ Wing II · 3D Virtual Worlds & CGI (27 Works)', w / 2, 335);
      ctx.fillStyle = '#e6af2e'; ctx.fillText('Wing I · The Classical & Fine Arts Wing (12 Works) →', w / 2, 380);
      ctx.fillStyle = '#ffc94d'; ctx.fillText('★ Wing IV · The Kinematic Pavilion (25 Works) [North Portal]', w / 2, 425);"""

new_rot_board = """      ctx.fillStyle = '#e6af2e'; ctx.fillText('← Wing III · The Nocturne & Astrophotography (86 Works)', w / 2, 290);
      ctx.fillStyle = '#fbfffe'; ctx.fillText('↑ Wing II · 3D Virtual Worlds: 5 Specialized Chambers (38 Works)', w / 2, 335);
      ctx.fillStyle = '#e6af2e'; ctx.fillText('Wing I · The Classical & Fine Arts Wing (29 Works) →', w / 2, 380);
      ctx.fillStyle = '#ffc94d'; ctx.fillText('★ Wing IV · The Kinematic Pavilion (52 Works) [North Portal]', w / 2, 425);"""

if old_rot_board in content:
    content = content.replace(old_rot_board, new_rot_board)
    print("Updated rotunda directory board!")
else:
    print("Warning: old_rot_board needle not matched directly")

# 3. Replace the Wing II call in buildArchitecture with dedicated buildWingII()
old_wing_calls = """  // Wing I (East, along +X axis)
  buildWing({
    key: 'I',
    label: EUNOIA_CONFIG.wings.I.name,
    subtitle: EUNOIA_CONFIG.wings.I.blurb,
    floorMat: Mat.floorWingI, wallMat: Mat.wallWingI, trimMat: Mat.trimWingI, ceilMat: Mat.ceilingWingI,
    length: WING_L, rotY: Math.PI / 2, ox: R_ROT - 0.2, oz: 0
  });

  // Wing II (North, along +Z axis)
  buildWing({
    key: 'II',
    label: EUNOIA_CONFIG.wings.II.name,
    subtitle: EUNOIA_CONFIG.wings.II.blurb,
    floorMat: Mat.floorWingII, wallMat: Mat.wallWingII, trimMat: Mat.trimWingII, ceilMat: Mat.ceilingWingII,
    length: WING_L, rotY: 0, ox: 0, oz: R_ROT - 0.2
  });

  // Wing III (West, along -X axis)
  buildWing({
    key: 'III',
    label: EUNOIA_CONFIG.wings.III.name,
    subtitle: EUNOIA_CONFIG.wings.III.blurb,
    floorMat: Mat.floorWingIII, wallMat: Mat.wallWingIII, trimMat: Mat.trimWingIII, ceilMat: Mat.ceilingWingIII,
    length: WING_L, rotY: -Math.PI / 2, ox: -(R_ROT - 0.2), oz: 0
  });"""

new_wing_calls = """  // Wing I (East, along +X axis)
  buildWing({
    key: 'I',
    label: EUNOIA_CONFIG.wings.I.name,
    subtitle: EUNOIA_CONFIG.wings.I.blurb,
    floorMat: Mat.floorWingI, wallMat: Mat.wallWingI, trimMat: Mat.trimWingI, ceilMat: Mat.ceilingWingI,
    length: WING_L, rotY: Math.PI / 2, ox: R_ROT - 0.2, oz: 0
  });

  // Wing II (North, along +Z axis) - Expanded Multi-Chamber 3D Pavilion
  buildWingII();

  // Wing III (West, along -X axis)
  buildWing({
    key: 'III',
    label: EUNOIA_CONFIG.wings.III.name,
    subtitle: EUNOIA_CONFIG.wings.III.blurb,
    floorMat: Mat.floorWingIII, wallMat: Mat.wallWingIII, trimMat: Mat.trimWingIII, ceilMat: Mat.ceilingWingIII,
    length: WING_L, rotY: -Math.PI / 2, ox: -(R_ROT - 0.2), oz: 0
  });"""

if old_wing_calls in content:
    content = content.replace(old_wing_calls, new_wing_calls)
    print("Replaced Wing II call with buildWingII()!")
else:
    raise ValueError("Could not find old_wing_calls needle")

# 4. Insert buildWingII function right before buildWingIV()
wing2_func_code = """
  /* --- 2.1 Wing II: The 3D Virtual Worlds Pavilion (Expanded Multi-Chamber Complex) --- */
  function buildWingII() {
    const wing = new THREE.Group();
    const ox = 0, oz = R_ROT - 0.2; // oz = 8.3
    const length = WING_L; // 26.0m: corridor runs from z = 8.3 to z = 34.3
    const hw = WING_W / 2; // 3.5m

    // --- A. Central Promenade Floor & Ceiling ---
    const floorStart = 0.35;
    const floorLen = length - floorStart;
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(WING_W, floorLen), Mat.floorWingII);
    floor.rotation.x = -Math.PI / 2;
    floor.position.set(0, 0, oz + floorStart + floorLen / 2);
    floor.receiveShadow = true;

    const ceil = new THREE.Mesh(new THREE.PlaneGeometry(WING_W, floorLen), Mat.ceilingWingII);
    ceil.rotation.x = Math.PI / 2;
    ceil.position.set(0, H_WING, oz + floorStart + floorLen / 2);

    const threshold = new THREE.Mesh(new RoundedBoxGeometry(WING_W + 0.1, 0.024, 0.72, 3, 0.01), Mat.archTrim);
    threshold.position.set(0, 0.012, oz);
    wing.add(floor, ceil, threshold);

    // Entrance portal arch from Rotunda into Wing II Promenade
    const portal = buildWallPortal('II', EUNOIA_CONFIG.wings.II.name, EUNOIA_CONFIG.wings.II.blurb, Mat.wallWingII);
    portal.position.set(0, 0, oz);
    wing.add(portal);

    // Entrance portal return wall colliders
    addWallSegment(-hw, oz, -1.50, oz);
    addWallSegment(1.50, oz, hw, oz);

    // Track lighting along Central Promenade
    const promTrack = buildTrackLight(length - 3);
    promTrack.position.set(0, 0, oz + length / 2);
    wing.add(promTrack);

    // Helper: Build Doorway Archway between Promenade and a Side Chamber
    function buildChamberPortal({ x, zCenter, width, label, sub, pointToChamber }) {
      const g = new THREE.Group();
      g.position.set(x, 0, zCenter);

      // Lintel beam above opening
      const lintelH = H_WING - 3.8;
      const lintel = new THREE.Mesh(new THREE.BoxGeometry(0.35, lintelH, width), Mat.archTrim);
      lintel.position.set(0, 3.8 + lintelH / 2, 0);

      // Fluted pilaster columns flanking doorway
      const colL = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 3.8, 16), Mat.flutedColumn);
      colL.position.set(0, 1.9, -width / 2 + 0.22);
      const colR = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 3.8, 16), Mat.flutedColumn);
      colR.position.set(0, 1.9, width / 2 - 0.22);

      // Sign facing Promenade
      const signTexProm = textTexture(1024, 256, (ctx, w, h) => {
        ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
        ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 5; ctx.strokeRect(10, 10, w - 20, h - 20);
        ctx.fillStyle = '#e6af2e'; ctx.font = `600 22px ${SANS}`;
        spacedText(ctx, 'WING II · 3D VIRTUAL WORLDS', w / 2, 54, 4);
        ctx.fillStyle = '#fbfffe'; ctx.font = `600 38px ${SERIF}`;
        spacedText(ctx, label, w / 2, 114, 5);
        ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 20px ${SERIF}`; ctx.textAlign = 'center';
        ctx.fillText(sub, w / 2, 172);
        ctx.fillStyle = '#e6af2e'; ctx.font = `500 15px ${SANS}`;
        ctx.fillText(pointToChamber ? 'ENTER GALLERY →' : '← ENTER GALLERY', w / 2, 218);
      });
      const signProm = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 0.8), new THREE.MeshStandardMaterial({ map: signTexProm, roughness: 0.35 }));
      signProm.position.set(x < 0 ? 0.18 : -0.18, 4.0, 0);
      signProm.rotation.y = x < 0 ? Math.PI / 2 : -Math.PI / 2;

      // Sign facing inside chamber looking back to promenade
      const signTexBack = textTexture(1024, 256, (ctx, w, h) => {
        ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
        ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 5; ctx.strokeRect(10, 10, w - 20, h - 20);
        ctx.fillStyle = '#e6af2e'; ctx.font = `600 22px ${SANS}`;
        spacedText(ctx, 'THE 3D VIRTUAL WORLDS WING', w / 2, 54, 4);
        ctx.fillStyle = '#fbfffe'; ctx.font = `600 36px ${SERIF}`;
        spacedText(ctx, 'PROMENADE & CHARACTER STUDIO', w / 2, 114, 4);
        ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 20px ${SERIF}`; ctx.textAlign = 'center';
        ctx.fillText('Central Colonnade · Wing IV Access · Grand Rotunda', w / 2, 172);
        ctx.fillStyle = '#e6af2e'; ctx.font = `500 15px ${SANS}`;
        ctx.fillText('← RETURN TO PROMENADE', w / 2, 218);
      });
      const signBack = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 0.8), new THREE.MeshStandardMaterial({ map: signTexBack, roughness: 0.35 }));
      signBack.position.set(x < 0 ? -0.18 : 0.18, 4.0, 0);
      signBack.rotation.y = x < 0 ? -Math.PI / 2 : Math.PI / 2;

      const signLight = new THREE.PointLight(0xffe4a0, 1.8, 5, 1.3);
      signLight.position.set(x < 0 ? 1.0 : -1.0, 4.2, 0);

      g.add(lintel, colL, colR, signProm, signBack, signLight);
      return g;
    }

    // Promenade Pier Walls
    // Left side (West: x = -hw = -3.5):
    const wallL1 = new THREE.Mesh(new THREE.PlaneGeometry(4.7, H_WING), Mat.wallWingII);
    wallL1.rotation.y = Math.PI / 2; wallL1.position.set(-hw, H_WING / 2, 8.3 + 2.35);
    const wallL2 = new THREE.Mesh(new THREE.PlaneGeometry(7.5, H_WING), Mat.wallWingII);
    wallL2.rotation.y = Math.PI / 2; wallL2.position.set(-hw, H_WING / 2, 18.5 + 3.75);
    const wallL3 = new THREE.Mesh(new THREE.PlaneGeometry(2.8, H_WING), Mat.wallWingII);
    wallL3.rotation.y = Math.PI / 2; wallL3.position.set(-hw, H_WING / 2, 31.5 + 1.4);

    // Right side (East: x = +hw = +3.5):
    const wallR1 = new THREE.Mesh(new THREE.PlaneGeometry(4.7, H_WING), Mat.wallWingII);
    wallR1.rotation.y = -Math.PI / 2; wallR1.position.set(hw, H_WING / 2, 8.3 + 2.35);
    const wallR2 = new THREE.Mesh(new THREE.PlaneGeometry(7.5, H_WING), Mat.wallWingII);
    wallR2.rotation.y = -Math.PI / 2; wallR2.position.set(hw, H_WING / 2, 18.5 + 3.75);
    const wallR3 = new THREE.Mesh(new THREE.PlaneGeometry(2.8, H_WING), Mat.wallWingII);
    wallR3.rotation.y = -Math.PI / 2; wallR3.position.set(hw, H_WING / 2, 31.5 + 1.4);

    wing.add(wallL1, wallL2, wallL3, wallR1, wallR2, wallR3);

    // Add Promenade Archway Portals
    const portalA = buildChamberPortal({ x: -hw, zCenter: 15.75, width: 5.5, label: '3D ENVIRONMENT GALLERY', sub: 'Exterior Worlds · Architecture · PBR Illumination', pointToChamber: false });
    const portalB = buildChamberPortal({ x: hw, zCenter: 15.75, width: 5.5, label: '3D INTERIOR ARCHITECTURE', sub: 'Spatial Layouts · Materiality & Raytracing', pointToChamber: true });
    const portalC = buildChamberPortal({ x: -hw, zCenter: 28.75, width: 5.5, label: '3D VFX THEATRE', sub: 'Dynamic Simulations · Fluids & Particles', pointToChamber: false });
    const portalD = buildChamberPortal({ x: hw, zCenter: 28.75, width: 5.5, label: '3D STILL LIFE & PROP RENDER', sub: 'Studio Lighting · Microfacet Shading', pointToChamber: true });
    wing.add(portalA, portalB, portalC, portalD);

    // North Portal to Wing IV at z = 34.3
    const pW = (WING_W - 3.6) / 2;
    const retEndL = new THREE.Mesh(new THREE.BoxGeometry(pW, H_WING, 0.4), Mat.wallWingII);
    retEndL.position.set(-hw + pW / 2, H_WING / 2, oz + length);
    const retEndR = new THREE.Mesh(new THREE.BoxGeometry(pW, H_WING, 0.4), Mat.wallWingII);
    retEndR.position.set(hw - pW / 2, H_WING / 2, oz + length);
    const atticEnd = new THREE.Mesh(new THREE.BoxGeometry(3.6, H_WING - 3.6, 0.4), Mat.wallWingII);
    atticEnd.position.set(0, 3.6 + (H_WING - 3.6) / 2, oz + length);

    const toWingIVTex = textTexture(1024, 256, (ctx, w, h) => {
      ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
      ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 5; ctx.strokeRect(10, 10, w - 20, h - 20);
      ctx.fillStyle = '#e6af2e'; ctx.font = `600 22px ${SANS}`;
      spacedText(ctx, 'WING IV · THE KINEMATIC PAVILION', w / 2, 56, 5);
      ctx.fillStyle = '#fbfffe'; ctx.font = `600 44px ${SERIF}`;
      spacedText(ctx, '2D ANIMATION & STORYBOARDS', w / 2, 118, 6);
      ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 22px ${SERIF}`; ctx.textAlign = 'center';
      ctx.fillText('Kinematic Momentum · The Wind Rises · Applied Design', w / 2, 180);
      ctx.fillStyle = '#e6af2e'; ctx.font = `500 15px ${SANS}`;
      ctx.fillText('ENTER PAVILION →', w / 2, 222);
    });
    const toWingIVSign = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 0.75), new THREE.MeshStandardMaterial({ map: toWingIVTex, roughness: 0.35 }));
    toWingIVSign.position.set(0, 3.85, oz + length - 0.22);
    toWingIVSign.rotation.y = Math.PI;
    wing.add(retEndL, retEndR, atticEnd, toWingIVSign);

    // Promenade Colliders
    addWallSegment(-hw, 8.3, -hw, 13.0);
    addWallSegment(-hw, 18.5, -hw, 26.0);
    addWallSegment(-hw, 31.5, -hw, 34.3);

    addWallSegment(hw, 8.3, hw, 13.0);
    addWallSegment(hw, 18.5, hw, 26.0);
    addWallSegment(hw, 31.5, hw, 34.3);

    addWallSegment(-hw, 34.3, -1.8, 34.3);
    addWallSegment(1.8, 34.3, hw, 34.3);

    // --- B. Build Side Chambers Function ---
    function buildChamber({ minX, maxX, minZ, maxZ, floorMat, wallMat, ceilMat, isDark=false }) {
      const cW = maxX - minX;
      const cD = maxZ - minZ;
      const cx = (minX + maxX) / 2;
      const cz = (minZ + maxZ) / 2;

      const chFloor = new THREE.Mesh(new THREE.PlaneGeometry(cW, cD), floorMat);
      chFloor.rotation.x = -Math.PI / 2; chFloor.position.set(cx, 0, cz); chFloor.receiveShadow = true;
      const chCeil = new THREE.Mesh(new THREE.PlaneGeometry(cW, cD), ceilMat);
      chCeil.rotation.x = Math.PI / 2; chCeil.position.set(cx, H_WING, cz);

      const isLeft = cx < 0;
      const backX = isLeft ? minX : maxX;
      const chBack = new THREE.Mesh(new THREE.PlaneGeometry(cD, H_WING), wallMat);
      chBack.rotation.y = isLeft ? Math.PI / 2 : -Math.PI / 2;
      chBack.position.set(backX, H_WING / 2, cz); chBack.castShadow = true; chBack.receiveShadow = true;

      const chSouth = new THREE.Mesh(new THREE.PlaneGeometry(cW, H_WING), wallMat);
      chSouth.position.set(cx, H_WING / 2, minZ); chSouth.castShadow = true; chSouth.receiveShadow = true;

      const chNorth = new THREE.Mesh(new THREE.PlaneGeometry(cW, H_WING), wallMat);
      chNorth.rotation.y = Math.PI; chNorth.position.set(cx, H_WING / 2, maxZ); chNorth.castShadow = true; chNorth.receiveShadow = true;

      const frontX = isLeft ? maxX : minX;
      const retZ1 = 2.5;
      const ret1 = new THREE.Mesh(new THREE.PlaneGeometry(retZ1, H_WING), wallMat);
      ret1.rotation.y = isLeft ? -Math.PI / 2 : Math.PI / 2;
      ret1.position.set(frontX, H_WING / 2, minZ + retZ1 / 2);

      const retZ2 = 2.5;
      const ret2 = new THREE.Mesh(new THREE.PlaneGeometry(retZ2, H_WING), wallMat);
      ret2.rotation.y = isLeft ? -Math.PI / 2 : Math.PI / 2;
      ret2.position.set(frontX, H_WING / 2, maxZ - retZ2 / 2);

      wing.add(chFloor, chCeil, chBack, chSouth, chNorth, ret1, ret2);

      if (isDark) {
        const darkLight = new THREE.PointLight(0x3a88ff, 2.2, 14, 1.2);
        darkLight.position.set(cx, 4.8, cz);
        wing.add(darkLight);
      } else {
        const warmLight = new THREE.PointLight(0xffecd0, 2.0, 15, 1.2);
        warmLight.position.set(cx, 4.9, cz);
        wing.add(warmLight);
      }

      addWallSegment(isLeft ? minX : maxX, minZ, isLeft ? minX : maxX, maxZ);
      addWallSegment(minX, minZ, maxX, minZ);
      addWallSegment(minX, maxZ, maxX, maxZ);
    }

    // Chamber A: 3D Environment Gallery
    buildChamber({ minX: -13.5, maxX: -3.5, minZ: 10.5, maxZ: 21.0, floorMat: Mat.floorWingII, wallMat: Mat.wallWingII, ceilMat: Mat.ceilingWingII });
    const benchA = buildMuseumBench(Mat.pedestal, Mat.blackVelvet);
    benchA.position.set(-8.5, 0, 15.75); wing.add(benchA);
    addRotatedBoxCollider(-8.5, 15.75, 0.45, 1.6, 0);

    // Chamber B: 3D Interior Architecture Hall
    buildChamber({ minX: 3.5, maxX: 13.5, minZ: 10.5, maxZ: 21.0, floorMat: Mat.floorWingII, wallMat: Mat.wallWingII, ceilMat: Mat.ceilingWingII });
    const benchB = buildMuseumBench(Mat.pedestal, Mat.blackVelvet);
    benchB.position.set(8.5, 0, 15.75); wing.add(benchB);
    addRotatedBoxCollider(8.5, 15.75, 0.45, 1.6, 0);

    // Chamber C: 3D VFX & Dynamic Simulations Theatre (Darkened Cinema Setting)
    const darkSlate = new THREE.MeshStandardMaterial({ color: 0x050a0f, roughness: 0.85, metalness: 0.1 });
    const darkWall = new THREE.MeshStandardMaterial({ color: 0x001514, roughness: 0.9, metalness: 0.05 });
    buildChamber({ minX: -13.5, maxX: -3.5, minZ: 23.5, maxZ: 34.0, floorMat: darkSlate, wallMat: darkWall, ceilMat: darkWall, isDark: true });
    const benchC = buildMuseumBench(Mat.pedestal, Mat.blackVelvet);
    benchC.position.set(-8.5, 0, 28.75); wing.add(benchC);
    addRotatedBoxCollider(-8.5, 28.75, 0.45, 1.6, 0);

    // Chamber D: 3D Still Life & Studio Renders
    buildChamber({ minX: 3.5, maxX: 13.5, minZ: 23.5, maxZ: 34.0, floorMat: Mat.floorWingII, wallMat: Mat.wallWingII, ceilMat: Mat.ceilingWingII });
    const stillPed = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.6, 1.05, 24), Mat.pedestal);
    stillPed.position.set(8.5, 0.525, 28.75);
    const stillSculpt = new THREE.Mesh(new THREE.TorusKnotGeometry(0.28, 0.08, 64, 16), Mat.goldLeaf);
    stillSculpt.position.set(8.5, 1.45, 28.75);
    wing.add(stillPed, stillSculpt);
    addRotatedBoxCollider(8.5, 28.75, 0.65, 0.65, 0);

    // Central Promenade Kiosk: Finals_Mangilaya.mp4 Pedestal
    const charKioskPed = new THREE.Mesh(new RoundedBoxGeometry(1.8, 1.1, 0.7, 3, 0.03), Mat.pedestal);
    charKioskPed.position.set(0, 0.55, 22.25); charKioskPed.castShadow = true;
    wing.add(charKioskPed);
    addRotatedBoxCollider(0, 22.25, 0.9, 0.45, 0);

    root.add(wing);
    return wing;
  }
"""

pivot = '  /* --- 3. Wing IV: The Kinematic Pavilion (Grand Transverse Hall) --- */'
if pivot in content:
    content = content.replace(pivot, wing2_func_code + '\n' + pivot)
    print("Inserted buildWingII() function definition!")
else:
    raise ValueError("Could not find buildWingIV pivot")

# 5. Replace layoutExhibits()
old_layout_needle = """  // Layout Wings I, II, III (Linear galleries)
  ['I', 'II', 'III'].forEach((wingKey) => {
    const cfg = wingConfigs[wingKey];
    const list = wingExhibits[wingKey] || [];

    list.forEach((ex, idx) => {
      const { group, artCanvasMesh } = buildPictureFrame(ex);
      const side = idx % 2 === 0 ? -1 : 1; // -1: left wall, 1: right wall
      const wallOffset = (WING_W / 2) - 0.14;
      const xLocal = side * wallOffset;
      const zLocal = 4.2 + Math.floor(idx / 2) * 5.6; // Spaced 5.6m apart along 26m hall
      const yLocal = 2.4;

      group.position.set(xLocal, yLocal, zLocal);
      group.rotation.y = side === -1 ? Math.PI / 2 : -Math.PI / 2;

      const worldGroup = new THREE.Group();
      worldGroup.position.set(cfg.ox, 0, cfg.oz);
      worldGroup.rotation.y = cfg.rotY;
      worldGroup.add(group);
      scene.add(worldGroup);

      const localViewPos = new THREE.Vector3(side * (wallOffset - 2.6), EYE_HEIGHT, zLocal);
      const worldViewPos = localViewPos.clone().applyAxisAngle(V3(0, 1, 0), cfg.rotY).add(V3(cfg.ox, 0, cfg.oz));
      const localArtPos = new THREE.Vector3(xLocal, yLocal, zLocal);
      const worldArtPos = localArtPos.clone().applyAxisAngle(V3(0, 1, 0), cfg.rotY).add(V3(cfg.ox, 0, cfg.oz));

      ex.teleportPos = worldViewPos;
      ex.lookTarget = worldArtPos;
    });
  });"""

new_layout_code = """  // Layout Wings I and III (Linear galleries)
  ['I', 'III'].forEach((wingKey) => {
    const cfg = wingConfigs[wingKey];
    const list = wingExhibits[wingKey] || [];

    list.forEach((ex, idx) => {
      const { group } = buildPictureFrame(ex);
      const side = idx % 2 === 0 ? -1 : 1;
      const wallOffset = (WING_W / 2) - 0.14;
      const xLocal = side * wallOffset;
      const zLocal = 4.2 + Math.floor(idx / 2) * 5.6;
      const yLocal = 2.4;

      group.position.set(xLocal, yLocal, zLocal);
      group.rotation.y = side === -1 ? Math.PI / 2 : -Math.PI / 2;

      const worldGroup = new THREE.Group();
      worldGroup.position.set(cfg.ox, 0, cfg.oz);
      worldGroup.rotation.y = cfg.rotY;
      worldGroup.add(group);
      scene.add(worldGroup);

      const localViewPos = new THREE.Vector3(side * (wallOffset - 2.6), EYE_HEIGHT, zLocal);
      const worldViewPos = localViewPos.clone().applyAxisAngle(V3(0, 1, 0), cfg.rotY).add(V3(cfg.ox, 0, cfg.oz));
      const localArtPos = new THREE.Vector3(xLocal, yLocal, zLocal);
      const worldArtPos = localArtPos.clone().applyAxisAngle(V3(0, 1, 0), cfg.rotY).add(V3(cfg.ox, 0, cfg.oz));

      ex.teleportPos = worldViewPos;
      ex.lookTarget = worldArtPos;
    });
  });

  // Layout Wing II (The 3D Virtual Worlds Pavilion - Multi-Room Layout: 34 Exhibits)
  const listII = wingExhibits.II || [];
  const roomsII = { env: [], interior: [], vfx: [], stilllife: [], char3d: [] };
  listII.forEach((ex) => {
    if (roomsII[ex.room]) roomsII[ex.room].push(ex);
    else roomsII.char3d.push(ex);
  });

  // Room A: 3D Environment Gallery (9 exhibits)
  const envWallSpots = [
    { x: -11.0, y: 2.4, z: 10.65, rotY: 0, viewX: -11.0, viewZ: 13.0 },
    { x: -8.5,  y: 2.4, z: 10.65, rotY: 0, viewX: -8.5,  viewZ: 13.0 },
    { x: -6.0,  y: 2.4, z: 10.65, rotY: 0, viewX: -6.0,  viewZ: 13.0 },
    { x: -13.35, y: 2.4, z: 13.0, rotY: Math.PI / 2, viewX: -11.0, viewZ: 13.0 },
    { x: -13.35, y: 2.4, z: 15.75, rotY: Math.PI / 2, viewX: -11.0, viewZ: 15.75 },
    { x: -13.35, y: 2.4, z: 18.5, rotY: Math.PI / 2, viewX: -11.0, viewZ: 18.5 },
    { x: -11.0, y: 2.4, z: 20.85, rotY: Math.PI, viewX: -11.0, viewZ: 18.5 },
    { x: -8.5,  y: 2.4, z: 20.85, rotY: Math.PI, viewX: -8.5,  viewZ: 18.5 },
    { x: -6.0,  y: 2.4, z: 20.85, rotY: Math.PI, viewX: -6.0,  viewZ: 18.5 }
  ];
  roomsII.env.forEach((ex, idx) => {
    if (idx >= envWallSpots.length) return;
    const spot = envWallSpots[idx];
    const { group } = buildPictureFrame(ex);
    group.position.set(spot.x, spot.y, spot.z);
    group.rotation.y = spot.rotY;
    scene.add(group);
    ex.teleportPos = new THREE.Vector3(spot.viewX, EYE_HEIGHT, spot.viewZ);
    ex.lookTarget = new THREE.Vector3(spot.x, spot.y, spot.z);
  });

  // Room B: 3D Interior Architecture Hall (10 exhibits)
  const intWallSpots = [
    { x: 6.0,  y: 2.4, z: 10.65, rotY: 0, viewX: 6.0,  viewZ: 13.0 },
    { x: 8.5,  y: 2.4, z: 10.65, rotY: 0, viewX: 8.5,  viewZ: 13.0 },
    { x: 11.0, y: 2.4, z: 10.65, rotY: 0, viewX: 11.0, viewZ: 13.0 },
    { x: 13.35, y: 2.4, z: 12.0, rotY: -Math.PI / 2, viewX: 11.0, viewZ: 12.0 },
    { x: 13.35, y: 2.4, z: 14.5, rotY: -Math.PI / 2, viewX: 11.0, viewZ: 14.5 },
    { x: 13.35, y: 2.4, z: 17.0, rotY: -Math.PI / 2, viewX: 11.0, viewZ: 17.0 },
    { x: 13.35, y: 2.4, z: 19.5, rotY: -Math.PI / 2, viewX: 11.0, viewZ: 19.5 },
    { x: 6.0,  y: 2.4, z: 20.85, rotY: Math.PI, viewX: 6.0,  viewZ: 18.5 },
    { x: 8.5,  y: 2.4, z: 20.85, rotY: Math.PI, viewX: 8.5,  viewZ: 18.5 },
    { x: 11.0, y: 2.4, z: 20.85, rotY: Math.PI, viewX: 11.0, viewZ: 18.5 }
  ];
  roomsII.interior.forEach((ex, idx) => {
    if (idx >= intWallSpots.length) return;
    const spot = intWallSpots[idx];
    const { group } = buildPictureFrame(ex);
    group.position.set(spot.x, spot.y, spot.z);
    group.rotation.y = spot.rotY;
    scene.add(group);
    ex.teleportPos = new THREE.Vector3(spot.viewX, EYE_HEIGHT, spot.viewZ);
    ex.lookTarget = new THREE.Vector3(spot.x, spot.y, spot.z);
  });

  // Room C: 3D VFX Dynamic Simulations Theatre (4 video projection screens)
  const vfxSpots = [
    { x: -13.35, y: 2.5, z: 26.5, rotY: Math.PI / 2,  viewX: -10.5, viewZ: 26.5 },
    { x: -13.35, y: 2.5, z: 31.0, rotY: Math.PI / 2,  viewX: -10.5, viewZ: 31.0 },
    { x: -8.5,   y: 2.5, z: 33.85, rotY: Math.PI,     viewX: -8.5,  viewZ: 31.0 },
    { x: -8.5,   y: 2.5, z: 23.65, rotY: 0,           viewX: -8.5,  viewZ: 26.5 }
  ];
  roomsII.vfx.forEach((ex, idx) => {
    if (idx >= vfxSpots.length) return;
    const spot = vfxSpots[idx];
    const { group } = buildPictureFrame(ex);
    group.position.set(spot.x, spot.y, spot.z);
    group.rotation.y = spot.rotY;
    scene.add(group);
    ex.teleportPos = new THREE.Vector3(spot.viewX, EYE_HEIGHT, spot.viewZ);
    ex.lookTarget = new THREE.Vector3(spot.x, spot.y, spot.z);
  });

  // Room D: 3D Still Life & Studio Renders (4 exhibits)
  const stillSpots = [
    { x: 8.5,   y: 2.4, z: 23.65, rotY: 0,           viewX: 8.5,  viewZ: 26.2 },
    { x: 13.35, y: 2.4, z: 26.5,  rotY: -Math.PI / 2, viewX: 10.8, viewZ: 26.5 },
    { x: 13.35, y: 2.4, z: 31.0,  rotY: -Math.PI / 2, viewX: 10.8, viewZ: 31.0 },
    { x: 8.5,   y: 2.4, z: 33.85, rotY: Math.PI,     viewX: 8.5,  viewZ: 31.2 }
  ];
  roomsII.stilllife.forEach((ex, idx) => {
    if (idx >= stillSpots.length) return;
    const spot = stillSpots[idx];
    const { group } = buildPictureFrame(ex);
    group.position.set(spot.x, spot.y, spot.z);
    group.rotation.y = spot.rotY;
    scene.add(group);
    ex.teleportPos = new THREE.Vector3(spot.viewX, EYE_HEIGHT, spot.viewZ);
    ex.lookTarget = new THREE.Vector3(spot.x, spot.y, spot.z);
  });

  // Promenade & Character Studio (Room E: 7 exhibits)
  const charSpots = [
    { x: -3.35, y: 2.4, z: 10.5, rotY: Math.PI / 2,  viewX: -1.2, viewZ: 10.5 },
    { x: -3.35, y: 2.4, z: 20.5, rotY: Math.PI / 2,  viewX: -1.2, viewZ: 20.5 },
    { x: -3.35, y: 2.4, z: 24.0, rotY: Math.PI / 2,  viewX: -1.2, viewZ: 24.0 },
    { x: 3.35,  y: 2.4, z: 10.5, rotY: -Math.PI / 2, viewX: 1.2,  viewZ: 10.5 },
    { x: 3.35,  y: 2.4, z: 20.5, rotY: -Math.PI / 2, viewX: 1.2,  viewZ: 20.5 },
    { x: 3.35,  y: 2.4, z: 24.0, rotY: -Math.PI / 2, viewX: 1.2,  viewZ: 24.0 },
    { x: 0,      y: 2.1, z: 22.25, rotY: 0,           viewX: 0,    viewZ: 19.8 }
  ];
  roomsII.char3d.forEach((ex, idx) => {
    if (idx >= charSpots.length) return;
    const spot = charSpots[idx];
    const { group } = buildPictureFrame(ex);
    group.position.set(spot.x, spot.y, spot.z);
    group.rotation.y = spot.rotY;
    scene.add(group);
    ex.teleportPos = new THREE.Vector3(spot.viewX, EYE_HEIGHT, spot.viewZ);
    ex.lookTarget = new THREE.Vector3(spot.x, spot.y, spot.z);
  });"""

if old_layout_needle in content:
    content = content.replace(old_layout_needle, new_layout_code)
    print("Updated layoutExhibits() for multi-room layout!")
else:
    raise ValueError("Could not find old_layout_needle")

# 6. Update updateCurrentWingCaption
old_caption_func = """function updateCurrentWingCaption(pos) {
  const locEl = $('hudLoc');
  const cap = $('roomCaption');
  const capNum = $('capNum');
  const capTitle = $('capTitle');

  let wingName = 'Grand Rotunda';
  let wingNum = 'Entrance';

  if (pos.x > 7.5) {
    wingName = EUNOIA_CONFIG.wings.I.name;
    wingNum = 'Wing I';
  } else if (pos.x < -7.5) {
    wingName = EUNOIA_CONFIG.wings.III.name;
    wingNum = 'Wing III';
  } else if (pos.z > 33.5) {
    wingName = EUNOIA_CONFIG.wings.IV.name;
    wingNum = 'Wing IV';
  } else if (pos.z > 7.5) {
    wingName = EUNOIA_CONFIG.wings.II.name;
    wingNum = 'Wing II';
  }

  locEl.textContent = wingName;
  if (capTitle.textContent !== wingName) {
    capTitle.textContent = wingName;
    capNum.textContent = wingNum;
    cap.classList.add('show');
    clearTimeout(cap._timer);
    cap._timer = setTimeout(() => cap.classList.remove('show'), 3200);
  }
}"""

new_caption_func = """function updateCurrentWingCaption(pos) {
  const locEl = $('hudLoc');
  const cap = $('roomCaption');
  const capNum = $('capNum');
  const capTitle = $('capTitle');

  let wingName = 'Grand Rotunda';
  let wingNum = 'Entrance';

  if (pos.x > 7.5 && Math.abs(pos.z) < 6.0) {
    wingName = EUNOIA_CONFIG.wings.I.name;
    wingNum = 'Wing I';
  } else if (pos.x < -7.5 && Math.abs(pos.z) < 6.0) {
    wingName = EUNOIA_CONFIG.wings.III.name;
    wingNum = 'Wing III';
  } else if (pos.z > 34.0) {
    wingName = EUNOIA_CONFIG.wings.IV.name;
    wingNum = 'Wing IV';
  } else if (pos.z > 8.0) {
    // Inside Wing II Multi-Chamber Complex
    if (pos.x < -4.0) {
      if (pos.z < 22.0) {
        wingName = 'Wing II · 3D Environment Gallery';
        wingNum = 'Room A';
      } else {
        wingName = 'Wing II · 3D VFX Theatre';
        wingNum = 'Room C';
      }
    } else if (pos.x > 4.0) {
      if (pos.z < 22.0) {
        wingName = 'Wing II · 3D Interior Architecture';
        wingNum = 'Room B';
      } else {
        wingName = 'Wing II · 3D Still Life Studio';
        wingNum = 'Room D';
      }
    } else {
      wingName = 'Wing II · 3D Virtual Worlds Promenade';
      wingNum = 'Colonnade';
    }
  }

  locEl.textContent = wingName;
  if (capTitle.textContent !== wingName) {
    capTitle.textContent = wingName;
    capNum.textContent = wingNum;
    cap.classList.add('show');
    clearTimeout(cap._timer);
    cap._timer = setTimeout(() => cap.classList.remove('show'), 3200);
  }
}"""

if old_caption_func in content:
    content = content.replace(old_caption_func, new_caption_func)
    print("Updated updateCurrentWingCaption()!")
else:
    raise ValueError("Could not find old_caption_func")

# 7. Update initCatalog filters
old_catalog_wings = """  const wings = [
    { id: 'ALL', name: 'All Works (96)' },
    { id: 'I',   name: 'Wing I · Fine Arts (12)' },
    { id: 'II',  name: 'Wing II · 3D CGI (27)' },
    { id: 'III', name: 'Wing III · Nocturne (32)' },
    { id: 'IV',  name: 'Wing IV · Kinematic (25)' }
  ];"""

new_catalog_wings = """  const countAll = EUNOIA_CONFIG.exhibits.length;
  const countI = EUNOIA_CONFIG.exhibits.filter(e => e.wing === 'I').length;
  const countII = EUNOIA_CONFIG.exhibits.filter(e => e.wing === 'II').length;
  const countIII = EUNOIA_CONFIG.exhibits.filter(e => e.wing === 'III').length;
  const countIV = EUNOIA_CONFIG.exhibits.filter(e => e.wing === 'IV').length;

  const wings = [
    { id: 'ALL', name: `All Works (${countAll})` },
    { id: 'I',   name: `Wing I · Fine Arts (${countI})` },
    { id: 'II',  name: `Wing II · 3D CGI (${countII})` },
    { id: 'III', name: `Wing III · Nocturne (${countIII})` },
    { id: 'IV',  name: `Wing IV · Kinematic (${countIV})` }
  ];"""

if old_catalog_wings in content:
    content = content.replace(old_catalog_wings, new_catalog_wings)
    print("Updated initCatalog dynamic counts!")
else:
    raise ValueError("Could not find old_catalog_wings")

# Save to index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully wrote updated index.html!")

