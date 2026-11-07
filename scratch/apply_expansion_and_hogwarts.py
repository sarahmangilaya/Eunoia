import json, re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update exhibits array in index.html with the updated full_catalog.json (with new hung videos)
with open('scratch/full_catalog.json', 'r', encoding='utf-8') as f:
    full_catalog = json.load(f)

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
print("Replaced exhibits catalog!")

# 2. Update buildPictureFrame for Hogwarts video autoplay & frame sizing
old_pic_frame_code = """function buildPictureFrame(exhibit, width, height) {
  const group = new THREE.Group();

  // Aspect ratio based dimensions
  const isLandscape = exhibit.orientation === 'landscape';
  const artW = isLandscape ? 3.0 : 2.2;
  const artH = isLandscape ? 2.25 : 2.93;
  const frameBorder = 0.22;
  const frameDepth = 0.14;

  // Frame outer border
  const outerW = artW + frameBorder * 2;
  const outerH = artH + frameBorder * 2;

  let frameMat = Mat.goldLeaf;
  if (exhibit.wing === 'II') frameMat = Mat.darkWood;
  if (exhibit.wing === 'III') frameMat = Mat.pedestal;

  const frameBack = new THREE.Mesh(
    new RoundedBoxGeometry(outerW, outerH, frameDepth, 4, 0.03),
    frameMat
  );
  frameBack.castShadow = true;
  frameBack.receiveShadow = true;
  group.add(frameBack);

  // Inner beveled liner / slip
  const linerMat = exhibit.wing === 'II' ? Mat.goldLeaf : Mat.alabaster;
  const liner = new THREE.Mesh(
    new RoundedBoxGeometry(artW + 0.08, artH + 0.08, frameDepth + 0.02, 3, 0.01),
    linerMat
  );
  group.add(liner);

  // Artwork Canvas texture & fallback
  let artMat;
  if (exhibit.mediaType === 'video') {
    const video = document.createElement('video');
    video.src = exhibit.imagePath;
    video.crossOrigin = 'anonymous';
    video.loop = true;
    video.muted = true;
    video.playsInline = true;
    video.autoplay = true;
    video.setAttribute('webkit-playsinline', 'true');
    video.play().catch(() => {});

    const videoTex = new THREE.VideoTexture(video);
    videoTex.colorSpace = THREE.SRGBColorSpace;
    videoTex.minFilter = THREE.LinearFilter;
    videoTex.magFilter = THREE.LinearFilter;

    // Glowing video canvas surface
    artMat = new THREE.MeshBasicMaterial({ map: videoTex });
  } else {"""

new_pic_frame_code = """const activeHogwartsVideos = [];

function wakeAllHogwartsVideos() {
  activeHogwartsVideos.forEach((v) => {
    if (v.paused) {
      v.muted = true;
      v.volume = 0;
      v.play().catch(() => {});
    }
  });
}
window.addEventListener('click', wakeAllHogwartsVideos, { passive: true });
window.addEventListener('keydown', wakeAllHogwartsVideos, { passive: true });
window.addEventListener('pointerdown', wakeAllHogwartsVideos, { passive: true });
window.addEventListener('touchstart', wakeAllHogwartsVideos, { passive: true });

function buildPictureFrame(exhibit, width, height) {
  const group = new THREE.Group();

  // Aspect ratio based dimensions - proportioned for museum breathing room
  const isLandscape = exhibit.orientation === 'landscape';
  const artW = width || (isLandscape ? 2.6 : 1.95);
  const artH = height || (isLandscape ? 1.95 : 2.6);
  const frameBorder = 0.16;
  const frameDepth = 0.12;

  // Frame outer border
  const outerW = artW + frameBorder * 2;
  const outerH = artH + frameBorder * 2;

  let frameMat = Mat.goldLeaf;
  if (exhibit.wing === 'II') frameMat = Mat.darkWood;
  if (exhibit.wing === 'III') frameMat = Mat.pedestal;

  const frameBack = new THREE.Mesh(
    new RoundedBoxGeometry(outerW, outerH, frameDepth, 4, 0.03),
    frameMat
  );
  frameBack.castShadow = true;
  frameBack.receiveShadow = true;
  group.add(frameBack);

  // Inner beveled liner / slip
  const linerMat = exhibit.wing === 'II' ? Mat.goldLeaf : Mat.alabaster;
  const liner = new THREE.Mesh(
    new RoundedBoxGeometry(artW + 0.08, artH + 0.08, frameDepth + 0.02, 3, 0.01),
    linerMat
  );
  group.add(liner);

  // Artwork Canvas texture & fallback
  let artMat;
  if (exhibit.mediaType === 'video') {
    // Hogwarts living portrait: continuous silent moving picture
    const video = document.createElement('video');
    video.src = exhibit.imagePath;
    video.crossOrigin = 'anonymous';
    video.loop = true;
    video.muted = true;
    video.defaultMuted = true;
    video.volume = 0;
    video.playsInline = true;
    video.autoplay = true;
    video.setAttribute('playsinline', '');
    video.setAttribute('webkit-playsinline', '');
    video.setAttribute('muted', '');
    video.setAttribute('autoplay', '');
    video.setAttribute('loop', '');
    video.preload = 'auto';

    video.play().catch(() => {});
    activeHogwartsVideos.push(video);

    const videoTex = new THREE.VideoTexture(video);
    videoTex.colorSpace = THREE.SRGBColorSpace;
    videoTex.minFilter = THREE.LinearFilter;
    videoTex.magFilter = THREE.LinearFilter;
    videoTex.generateMipmaps = false;

    // Glowing video canvas surface
    artMat = new THREE.MeshBasicMaterial({ map: videoTex });
  } else {"""

if old_pic_frame_code in content:
    content = content.replace(old_pic_frame_code, new_pic_frame_code)
    print("Updated buildPictureFrame with Hogwarts video autoplay!")
else:
    raise ValueError("Could not find old_pic_frame_code")

# 3. Update buildWingII() with expanded spacious pavilion dimensions
# Locate buildWingII definition
old_wing2_regex = r'  /\* --- 2\.1 Wing II: The 3D Virtual Worlds Pavilion \(Expanded Multi-Chamber Complex\) --- \*/\s*function buildWingII\(\) \{[\s\S]*?return wing;\s*\}'

new_wing2_code = """  /* --- 2.1 Wing II: The 3D Virtual Worlds Pavilion (Expanded Multi-Chamber Complex) --- */
  function buildWingII() {
    const wing = new THREE.Group();
    const ox = 0, oz = R_ROT - 0.2; // oz = 8.3
    const length = 43.7; // Grand Promenade spans z = 8.3 to z = 52.0 (total 43.7m)
    const hw = 4.0; // Promenade width 8.0m (-4.0 to +4.0)

    // --- A. Central Promenade Floor & Ceiling ---
    const floorStart = 0.35;
    const floorLen = length - floorStart;
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(hw * 2, floorLen), Mat.floorWingII);
    floor.rotation.x = -Math.PI / 2;
    floor.position.set(0, 0, oz + floorStart + floorLen / 2);
    floor.receiveShadow = true;

    const ceil = new THREE.Mesh(new THREE.PlaneGeometry(hw * 2, floorLen), Mat.ceilingWingII);
    ceil.rotation.x = Math.PI / 2;
    ceil.position.set(0, H_WING, oz + floorStart + floorLen / 2);

    const threshold = new THREE.Mesh(new RoundedBoxGeometry(hw * 2 + 0.1, 0.024, 0.72, 3, 0.01), Mat.archTrim);
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
    const promTrack1 = buildTrackLight(18);
    promTrack1.position.set(0, 0, 18.0);
    const promTrack2 = buildTrackLight(18);
    promTrack2.position.set(0, 0, 42.0);
    wing.add(promTrack1, promTrack2);

    // Helper: Build Grand Doorway Archway between Promenade and a Side Chamber
    function buildChamberPortal({ x, zCenter, width, label, sub, pointToChamber }) {
      const g = new THREE.Group();
      g.position.set(x, 0, zCenter);

      // Lintel beam above opening
      const lintelH = H_WING - 3.8;
      const lintel = new THREE.Mesh(new THREE.BoxGeometry(0.35, lintelH, width), Mat.archTrim);
      lintel.position.set(0, 3.8 + lintelH / 2, 0);

      // Fluted pilaster columns flanking doorway
      const colL = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 3.8, 16), Mat.flutedColumn);
      colL.position.set(0, 1.9, -width / 2 + 0.24);
      const colR = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 3.8, 16), Mat.flutedColumn);
      colR.position.set(0, 1.9, width / 2 - 0.24);

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
      const signProm = new THREE.Mesh(new THREE.PlaneGeometry(3.8, 0.8), new THREE.MeshStandardMaterial({ map: signTexProm, roughness: 0.35 }));
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
      const signBack = new THREE.Mesh(new THREE.PlaneGeometry(3.8, 0.8), new THREE.MeshStandardMaterial({ map: signTexBack, roughness: 0.35 }));
      signBack.position.set(x < 0 ? -0.18 : 0.18, 4.0, 0);
      signBack.rotation.y = x < 0 ? -Math.PI / 2 : Math.PI / 2;

      const signLight = new THREE.PointLight(0xffe4a0, 1.8, 6, 1.3);
      signLight.position.set(x < 0 ? 1.0 : -1.0, 4.2, 0);

      g.add(lintel, colL, colR, signProm, signBack, signLight);
      return g;
    }

    // Promenade Pier Walls:
    // Left side (West: x = -hw = -4.0):
    // Pier 1: z in [8.3, 14.5] (length 6.2)
    const wallL1 = new THREE.Mesh(new THREE.PlaneGeometry(6.2, H_WING), Mat.wallWingII);
    wallL1.rotation.y = Math.PI / 2; wallL1.position.set(-hw, H_WING / 2, 8.3 + 3.1);
    // Pier 2: z in [20.5, 38.0] (length 17.5)
    const wallL2 = new THREE.Mesh(new THREE.PlaneGeometry(17.5, H_WING), Mat.wallWingII);
    wallL2.rotation.y = Math.PI / 2; wallL2.position.set(-hw, H_WING / 2, 20.5 + 8.75);
    // Pier 3: z in [44.0, 52.0] (length 8.0)
    const wallL3 = new THREE.Mesh(new THREE.PlaneGeometry(8.0, H_WING), Mat.wallWingII);
    wallL3.rotation.y = Math.PI / 2; wallL3.position.set(-hw, H_WING / 2, 44.0 + 4.0);

    // Right side (East: x = +hw = +4.0):
    const wallR1 = new THREE.Mesh(new THREE.PlaneGeometry(6.2, H_WING), Mat.wallWingII);
    wallR1.rotation.y = -Math.PI / 2; wallR1.position.set(hw, H_WING / 2, 8.3 + 3.1);
    const wallR2 = new THREE.Mesh(new THREE.PlaneGeometry(17.5, H_WING), Mat.wallWingII);
    wallR2.rotation.y = -Math.PI / 2; wallR2.position.set(hw, H_WING / 2, 20.5 + 8.75);
    const wallR3 = new THREE.Mesh(new THREE.PlaneGeometry(8.0, H_WING), Mat.wallWingII);
    wallR3.rotation.y = -Math.PI / 2; wallR3.position.set(hw, H_WING / 2, 44.0 + 4.0);

    wing.add(wallL1, wallL2, wallL3, wallR1, wallR2, wallR3);

    // Doorway archway portals (Width 6.0m each!)
    const portalA = buildChamberPortal({ x: -hw, zCenter: 17.5, width: 6.0, label: '3D ENVIRONMENT GALLERY', sub: 'Exterior Worlds · Architecture · PBR Illumination', pointToChamber: false });
    const portalB = buildChamberPortal({ x: hw, zCenter: 17.5, width: 6.0, label: '3D INTERIOR ARCHITECTURE', sub: 'Spatial Layouts · Materiality & Raytracing', pointToChamber: true });
    const portalC = buildChamberPortal({ x: -hw, zCenter: 41.0, width: 6.0, label: '3D VFX THEATRE', sub: 'Dynamic Simulations · Fluids & Particles', pointToChamber: false });
    const portalD = buildChamberPortal({ x: hw, zCenter: 41.0, width: 6.0, label: '3D STILL LIFE & PROP RENDER', sub: 'Studio Lighting · Microfacet Shading', pointToChamber: true });
    wing.add(portalA, portalB, portalC, portalD);

    // North Portal to Wing IV at z = 52.0
    const pW = (hw * 2 - 4.0) / 2; // 2.0m on each side
    const retEndL = new THREE.Mesh(new THREE.BoxGeometry(pW, H_WING, 0.4), Mat.wallWingII);
    retEndL.position.set(-hw + pW / 2, H_WING / 2, 52.0);
    const retEndR = new THREE.Mesh(new THREE.BoxGeometry(pW, H_WING, 0.4), Mat.wallWingII);
    retEndR.position.set(hw - pW / 2, H_WING / 2, 52.0);
    const atticEnd = new THREE.Mesh(new THREE.BoxGeometry(4.0, H_WING - 3.8, 0.4), Mat.wallWingII);
    atticEnd.position.set(0, 3.8 + (H_WING - 3.8) / 2, 52.0);

    const toWingIVTex = textTexture(1024, 256, (ctx, w, h) => {
      ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
      ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 5; ctx.strokeRect(10, 10, w - 20, h - 20);
      ctx.fillStyle = '#e6af2e'; ctx.font = `600 22px ${SANS}`;
      spacedText(ctx, 'WING IV · THE KINEMATIC PAVILION', w / 2, 56, 5);
      ctx.fillStyle = '#fbfffe'; ctx.font = `600 44px ${SERIF}`;
      spacedText(ctx, '2D ANIMATION & CINEMATIC MEDIA', w / 2, 118, 6);
      ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 22px ${SERIF}`; ctx.textAlign = 'center';
      ctx.fillText('Living Kinematic Moving Portraits · Master Storyboards · Applied Design', w / 2, 180);
      ctx.fillStyle = '#e6af2e'; ctx.font = `500 15px ${SANS}`;
      ctx.fillText('ENTER PAVILION →', w / 2, 222);
    });
    const toWingIVSign = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 0.8), new THREE.MeshStandardMaterial({ map: toWingIVTex, roughness: 0.35 }));
    toWingIVSign.position.set(0, 4.0, 52.0 - 0.22);
    toWingIVSign.rotation.y = Math.PI;
    wing.add(retEndL, retEndR, atticEnd, toWingIVSign);

    // Promenade Colliders
    addWallSegment(-hw, 8.3, -hw, 14.5);
    addWallSegment(-hw, 20.5, -hw, 38.0);
    addWallSegment(-hw, 44.0, -hw, 52.0);

    addWallSegment(hw, 8.3, hw, 14.5);
    addWallSegment(hw, 20.5, hw, 38.0);
    addWallSegment(hw, 44.0, hw, 52.0);

    addWallSegment(-hw, 52.0, -2.0, 52.0);
    addWallSegment(2.0, 52.0, hw, 52.0);

    // --- B. Build Spacious Expanded Side Chambers ---
    function buildChamber({ minX, maxX, minZ, maxZ, floorMat, wallMat, ceilMat, isDark=false, doorZ1, doorZ2 }) {
      const cW = maxX - minX; // 18.0m wide!
      const cD = maxZ - minZ; // 16.0m deep!
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

      // Front returns flanking doorway
      const frontX = isLeft ? maxX : minX;
      const retLen1 = doorZ1 - minZ; // e.g. 14.5 - 9.5 = 5.0m
      const ret1 = new THREE.Mesh(new THREE.PlaneGeometry(retLen1, H_WING), wallMat);
      ret1.rotation.y = isLeft ? -Math.PI / 2 : Math.PI / 2;
      ret1.position.set(frontX, H_WING / 2, minZ + retLen1 / 2);

      const retLen2 = maxZ - doorZ2; // e.g. 25.5 - 20.5 = 5.0m
      const ret2 = new THREE.Mesh(new THREE.PlaneGeometry(retLen2, H_WING), wallMat);
      ret2.rotation.y = isLeft ? -Math.PI / 2 : Math.PI / 2;
      ret2.position.set(frontX, H_WING / 2, maxZ - retLen2 / 2);

      wing.add(chFloor, chCeil, chBack, chSouth, chNorth, ret1, ret2);

      if (isDark) {
        const darkLight1 = new THREE.PointLight(0x3a88ff, 2.0, 16, 1.2);
        darkLight1.position.set(cx - 3, 4.8, cz);
        const darkLight2 = new THREE.PointLight(0x3a88ff, 2.0, 16, 1.2);
        darkLight2.position.set(cx + 3, 4.8, cz);
        wing.add(darkLight1, darkLight2);
      } else {
        const warmLight1 = new THREE.PointLight(0xffecd0, 2.2, 16, 1.2);
        warmLight1.position.set(cx - 4, 4.9, cz);
        const warmLight2 = new THREE.PointLight(0xffecd0, 2.2, 16, 1.2);
        warmLight2.position.set(cx + 4, 4.9, cz);
        wing.add(warmLight1, warmLight2);
      }

      addWallSegment(isLeft ? minX : maxX, minZ, isLeft ? minX : maxX, maxZ);
      addWallSegment(minX, minZ, maxX, minZ);
      addWallSegment(minX, maxZ, maxX, maxZ);
    }

    // Chamber A: 3D Environment Gallery (Spacious 18m x 16m Hall)
    buildChamber({ minX: -22.0, maxX: -4.0, minZ: 9.5, maxZ: 25.5, floorMat: Mat.floorWingII, wallMat: Mat.wallWingII, ceilMat: Mat.ceilingWingII, doorZ1: 14.5, doorZ2: 20.5 });
    const benchA = buildMuseumBench(Mat.pedestal, Mat.blackVelvet);
    benchA.position.set(-13.0, 0, 17.5); wing.add(benchA);
    addRotatedBoxCollider(-13.0, 17.5, 0.55, 1.8, 0);

    // Chamber B: 3D Interior Architecture Hall (Spacious 18m x 16m Hall)
    buildChamber({ minX: 4.0, maxX: 22.0, minZ: 9.5, maxZ: 25.5, floorMat: Mat.floorWingII, wallMat: Mat.wallWingII, ceilMat: Mat.ceilingWingII, doorZ1: 14.5, doorZ2: 20.5 });
    const benchB = buildMuseumBench(Mat.pedestal, Mat.blackVelvet);
    benchB.position.set(13.0, 0, 17.5); wing.add(benchB);
    addRotatedBoxCollider(13.0, 17.5, 0.55, 1.8, 0);

    // Chamber C: 3D VFX Dynamic Simulations Theatre (Spacious 18m x 16m Cinema)
    const darkSlate = new THREE.MeshStandardMaterial({ color: 0x050a0f, roughness: 0.85, metalness: 0.1 });
    const darkWall = new THREE.MeshStandardMaterial({ color: 0x001514, roughness: 0.9, metalness: 0.05 });
    buildChamber({ minX: -22.0, maxX: -4.0, minZ: 33.0, maxZ: 49.0, floorMat: darkSlate, wallMat: darkWall, ceilMat: darkWall, isDark: true, doorZ1: 38.0, doorZ2: 44.0 });
    const benchC = buildMuseumBench(Mat.pedestal, Mat.blackVelvet);
    benchC.position.set(-13.0, 0, 41.0); wing.add(benchC);
    addRotatedBoxCollider(-13.0, 41.0, 0.55, 1.8, 0);

    // Chamber D: 3D Still Life & Studio Renders (Spacious 18m x 16m Hall)
    buildChamber({ minX: 4.0, maxX: 22.0, minZ: 33.0, maxZ: 49.0, floorMat: Mat.floorWingII, wallMat: Mat.wallWingII, ceilMat: Mat.ceilingWingII, doorZ1: 38.0, doorZ2: 44.0 });
    const stillPed = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.72, 1.05, 24), Mat.pedestal);
    stillPed.position.set(13.0, 0.525, 41.0);
    const stillSculpt = new THREE.Mesh(new THREE.TorusKnotGeometry(0.35, 0.1, 64, 16), Mat.goldLeaf);
    stillSculpt.position.set(13.0, 1.5, 41.0);
    wing.add(stillPed, stillSculpt);
    addRotatedBoxCollider(13.0, 41.0, 0.75, 0.75, 0);

    // Central Promenade Kiosk: Finals_Mangilaya.mp4 Pedestal at z = 27.0
    const charKioskPed = new THREE.Mesh(new RoundedBoxGeometry(1.8, 1.1, 0.7, 3, 0.03), Mat.pedestal);
    charKioskPed.position.set(0, 0.55, 27.0); charKioskPed.castShadow = true;
    wing.add(charKioskPed);
    addRotatedBoxCollider(0, 27.0, 0.9, 0.45, 0);

    root.add(wing);
    return wing;
  }"""

content = re.sub(old_wing2_regex, new_wing2_code, content)
print("Updated buildWingII() with spacious 18m x 16m chambers!")

# 4. Update buildWingIV to be located at z = 52.0 to 68.0
old_wing4_regex = r'  /\* --- 3\. Wing IV: The Kinematic Pavilion \(Grand Transverse Hall\) --- \*/\s*function buildWingIV\(\) \{[\s\S]*?buildWingIV\(\);'

new_wing4_code = """  /* --- 3. Wing IV: The Kinematic Pavilion (Grand Transverse Hall) --- */
  function buildWingIV() {
    const pavW = 26.0, pavD = 16.0, pavH = 5.4;
    const startZ = 52.0;
    const g = new THREE.Group();

    // Floor & Ceiling
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(pavW, pavD), Mat.floorWingI);
    floor.rotation.x = -Math.PI / 2; floor.position.set(0, 0, startZ + pavD / 2); floor.receiveShadow = true;

    const ceil = new THREE.Mesh(new THREE.PlaneGeometry(pavW, pavD), Mat.ceilingWingI);
    ceil.rotation.x = Math.PI / 2; ceil.position.set(0, pavH, startZ + pavD / 2);

    // North Wall (Back wall facing visitor entering from Wing II)
    const wallN = new THREE.Mesh(new THREE.PlaneGeometry(pavW, pavH), Mat.wallWingII);
    wallN.rotation.y = Math.PI; wallN.position.set(0, pavH / 2, startZ + pavD); wallN.castShadow = true; wallN.receiveShadow = true;

    // West & East Walls
    const wallW = new THREE.Mesh(new THREE.PlaneGeometry(pavD, pavH), Mat.wallWingII);
    wallW.rotation.y = Math.PI / 2; wallW.position.set(-pavW / 2, pavH / 2, startZ + pavD / 2);
    wallW.castShadow = true; wallW.receiveShadow = true;

    const wallE = new THREE.Mesh(new THREE.PlaneGeometry(pavD, pavH), Mat.wallWingII);
    wallE.rotation.y = -Math.PI / 2; wallE.position.set(pavW / 2, pavH / 2, startZ + pavD / 2);
    wallE.castShadow = true; wallE.receiveShadow = true;

    // South Wall (Flanking the entrance portal from Wing II: opening 4.0m)
    const southSectW = (pavW - 4.0) / 2; // 11.0m
    const wallSL = new THREE.Mesh(new THREE.PlaneGeometry(southSectW, pavH), Mat.wallWingII);
    wallSL.position.set(-pavW / 2 + southSectW / 2, pavH / 2, startZ);
    const wallSR = new THREE.Mesh(new THREE.PlaneGeometry(southSectW, pavH), Mat.wallWingII);
    wallSR.position.set(pavW / 2 - southSectW / 2, pavH / 2, startZ);
    const wallSTop = new THREE.Mesh(new THREE.PlaneGeometry(4.0, pavH - 3.8), Mat.wallWingII);
    wallSTop.position.set(0, 3.8 + (pavH - 3.8) / 2, startZ);

    // Return Sign facing inside Wing IV looking back towards Wing II & Rotunda
    const toWingIITex = textTexture(1024, 256, (ctx, w, h) => {
      ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
      ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 5; ctx.strokeRect(10, 10, w - 20, h - 20);
      ctx.fillStyle = '#e6af2e'; ctx.font = `600 22px ${SANS}`;
      spacedText(ctx, 'TO WING II · 3D VIRTUAL WORLDS & GRAND ROTUNDA', w / 2, 54, 4);
      ctx.fillStyle = '#fbfffe'; ctx.font = `600 40px ${SERIF}`;
      spacedText(ctx, 'THE 3D VIRTUAL WORLDS PAVILION', w / 2, 114, 5);
      ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 20px ${SERIF}`; ctx.textAlign = 'center';
      ctx.fillText('Environment · Interior · VFX Cinema · Still Life · Character Topology', w / 2, 172);
      ctx.fillStyle = '#e6af2e'; ctx.font = `500 15px ${SANS}`;
      ctx.fillText('← RETURN TO WING II PROMENADE', w / 2, 218);
    });
    const toWingIISign = new THREE.Mesh(new THREE.PlaneGeometry(3.8, 0.8), new THREE.MeshStandardMaterial({ map: toWingIITex, roughness: 0.35 }));
    toWingIISign.position.set(0, 4.0, startZ + 0.22);
    toWingIISign.rotation.y = 0;

    g.add(floor, ceil, wallN, wallW, wallE, wallSL, wallSR, wallSTop, toWingIISign);

    // Warm ceiling downlights
    const pavLight1 = new THREE.PointLight(0xffecd0, 2.2, 18, 1.2);
    pavLight1.position.set(-6, 4.9, startZ + pavD / 2);
    const pavLight2 = new THREE.PointLight(0xffecd0, 2.2, 18, 1.2);
    pavLight2.position.set(6, 4.9, startZ + pavD / 2);
    g.add(pavLight1, pavLight2);

    // Central Viewing Bench facing the 2D Animation Video Canvas
    const bench = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    bench.position.set(0, 0, startZ + 7.5);
    g.add(bench);
    addRotatedBoxCollider(0, startZ + 7.5, 1.75, 0.55, 0);

    root.add(g);

    // Perimeter colliders for Wing IV
    addWallSegment(-pavW / 2, startZ + pavD, pavW / 2, startZ + pavD); // North wall
    addWallSegment(-pavW / 2, startZ, -pavW / 2, startZ + pavD);        // West wall
    addWallSegment(pavW / 2, startZ, pavW / 2, startZ + pavD);         // East wall
    addWallSegment(-pavW / 2, startZ, -2.0, startZ);                   // South wall left
    addWallSegment(2.0, startZ, pavW / 2, startZ);                    // South wall right
  }

  buildWingIV();"""

content = re.sub(old_wing4_regex, new_wing4_code, content)
print("Updated buildWingIV() with new coordinates at z=52.0 to 68.0!")

# 5. Update layoutExhibits() with zero-overlap coordinates and all Hogwarts videos
old_layout_regex = r'  // Layout Wing II \(The 3D Virtual Worlds Pavilion - Multi-Room Layout: 34 Exhibits\)[\s\S]*?// Layout Wing IV: The Kinematic Pavilion \(Grand Transverse Hall\)[\s\S]*?buildPictureFrame\(ex\);[\s\S]*?scene\.add\(worldGroup\);\s*\}\);'

new_layout_code = """  // Layout Wing II (The 3D Virtual Worlds Pavilion - Multi-Room Layout: 36 Exhibits)
  const listII = wingExhibits.II || [];
  const roomsII = { env: [], interior: [], vfx: [], stilllife: [], char3d: [] };
  listII.forEach((ex) => {
    if (roomsII[ex.room]) roomsII[ex.room].push(ex);
    else roomsII.char3d.push(ex);
  });

  // Room A: 3D Environment Gallery (9 exhibits - 18m x 16m Hall, 4.5m spacing, ZERO overlap)
  const envWallSpots = [
    // South Wall (z = 9.65, rotY = 0)
    { x: -17.5, y: 2.4, z: 9.65, rotY: 0, viewX: -17.5, viewZ: 12.5 },
    { x: -13.0, y: 2.4, z: 9.65, rotY: 0, viewX: -13.0, viewZ: 12.5 },
    { x: -8.5,  y: 2.4, z: 9.65, rotY: 0, viewX: -8.5,  viewZ: 12.5 },
    // West Wall (x = -21.85, rotY = Math.PI / 2)
    { x: -21.85, y: 2.4, z: 13.5, rotY: Math.PI / 2, viewX: -18.5, viewZ: 13.5 },
    { x: -21.85, y: 2.4, z: 17.5, rotY: Math.PI / 2, viewX: -18.5, viewZ: 17.5 }, // Cantilever Villa Centerpiece
    { x: -21.85, y: 2.4, z: 21.5, rotY: Math.PI / 2, viewX: -18.5, viewZ: 21.5 },
    // North Wall (z = 25.35, rotY = Math.PI)
    { x: -17.5, y: 2.4, z: 25.35, rotY: Math.PI, viewX: -17.5, viewZ: 22.5 },
    { x: -13.0, y: 2.4, z: 25.35, rotY: Math.PI, viewX: -13.0, viewZ: 22.5 },
    { x: -8.5,  y: 2.4, z: 25.35, rotY: Math.PI, viewX: -8.5,  viewZ: 22.5 }
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

  // Room B: 3D Interior Architecture Hall (10 exhibits - 18m x 16m Hall, 4.0m spacing, ZERO overlap)
  const intWallSpots = [
    // South Wall (z = 9.65, rotY = 0)
    { x: 8.5,  y: 2.4, z: 9.65, rotY: 0, viewX: 8.5,  viewZ: 12.5 },
    { x: 13.0, y: 2.4, z: 9.65, rotY: 0, viewX: 13.0, viewZ: 12.5 },
    { x: 17.5, y: 2.4, z: 9.65, rotY: 0, viewX: 17.5, viewZ: 12.5 },
    // East Wall (x = 21.85, rotY = -Math.PI / 2)
    { x: 21.85, y: 2.4, z: 12.0, rotY: -Math.PI / 2, viewX: 18.5, viewZ: 12.0 },
    { x: 21.85, y: 2.4, z: 15.5, rotY: -Math.PI / 2, viewX: 18.5, viewZ: 15.5 },
    { x: 21.85, y: 2.4, z: 19.5, rotY: -Math.PI / 2, viewX: 18.5, viewZ: 19.5 },
    { x: 21.85, y: 2.4, z: 23.0, rotY: -Math.PI / 2, viewX: 18.5, viewZ: 23.0 },
    // North Wall (z = 25.35, rotY = Math.PI)
    { x: 8.5,  y: 2.4, z: 25.35, rotY: Math.PI, viewX: 8.5,  viewZ: 22.5 },
    { x: 13.0, y: 2.4, z: 25.35, rotY: Math.PI, viewX: 13.0, viewZ: 22.5 },
    { x: 17.5, y: 2.4, z: 25.35, rotY: Math.PI, viewX: 17.5, viewZ: 22.5 }
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

  // Room C: 3D VFX Dynamic Simulations Theatre (6 glowing silent video canvases on walls)
  const vfxSpots = [
    { x: -13.0,  y: 2.5, z: 33.15, rotY: 0,           viewX: -13.0, viewZ: 36.5 }, // South Wall: Ice Cream Bar
    { x: -21.85, y: 2.5, z: 37.5,  rotY: Math.PI / 2, viewX: -18.5, viewZ: 37.5 }, // West Wall: Bonfire
    { x: -21.85, y: 2.5, z: 44.5,  rotY: Math.PI / 2, viewX: -18.5, viewZ: 44.5 }, // West Wall: Will O Wisp
    { x: -13.0,  y: 2.5, z: 48.85, rotY: Math.PI,     viewX: -13.0, viewZ: 45.5 }, // North Wall: Magical Night (Centerpiece)
    { x: -4.15,  y: 2.5, z: 35.5,  rotY: -Math.PI / 2, viewX: -7.5, viewZ: 35.5 }, // East Return: Energy Ball
    { x: -4.15,  y: 2.5, z: 46.5,  rotY: -Math.PI / 2, viewX: -7.5, viewZ: 46.5 }  // East Return: VFX Finals 2.0
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

  // Room D: 3D Still Life & Studio Renders (4 exhibits - 18m x 16m Hall)
  const stillSpots = [
    { x: 13.0,  y: 2.4, z: 33.15, rotY: 0,           viewX: 13.0, viewZ: 36.5 },
    { x: 21.85, y: 2.4, z: 37.5,  rotY: -Math.PI / 2, viewX: 18.5, viewZ: 37.5 },
    { x: 21.85, y: 2.4, z: 44.5,  rotY: -Math.PI / 2, viewX: 18.5, viewZ: 44.5 },
    { x: 13.0,  y: 2.4, z: 48.85, rotY: Math.PI,     viewX: 13.0, viewZ: 45.5 }
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
    { x: -3.85, y: 2.4, z: 23.5, rotY: Math.PI / 2,  viewX: -1.5, viewZ: 23.5 },
    { x: -3.85, y: 2.4, z: 27.0, rotY: Math.PI / 2,  viewX: -1.5, viewZ: 27.0 },
    { x: -3.85, y: 2.4, z: 30.5, rotY: Math.PI / 2,  viewX: -1.5, viewZ: 30.5 },
    { x: 3.85,  y: 2.4, z: 23.5, rotY: -Math.PI / 2, viewX: 1.5,  viewZ: 23.5 },
    { x: 3.85,  y: 2.4, z: 27.0, rotY: -Math.PI / 2, viewX: 1.5,  viewZ: 27.0 },
    { x: 3.85,  y: 2.4, z: 30.5, rotY: -Math.PI / 2, viewX: 1.5,  viewZ: 30.5 },
    // Centerpiece: Finals_Mangilaya.mp4 on the pedestal at (0, 27.0)
    { x: 0,     y: 2.1, z: 27.0, rotY: 0,           viewX: 0,    viewZ: 24.5 }
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
  });

  // Layout Wing IV: The Kinematic Pavilion (Grand Transverse Hall at z = 52.0 to 68.0)
  const listIV = wingExhibits.IV || [];
  const pavStart = 52.0, pavDepth = 16.0;

  // Spots in Kinematic Pavilion with multiple moving video canvases
  const ivSpots = [
    // 0: CENTERPIECE Video on North Wall: Jump Animation.mp4
    { x: 0,     y: 2.8, z: pavStart + pavDepth - 0.16, rotY: Math.PI, viewX: 0, viewZ: pavStart + pavDepth - 4.5 },
    // 1: Center-Left Video on North Wall: The Shadows of a Secret.mp4
    { x: -6.5,  y: 2.6, z: pavStart + pavDepth - 0.16, rotY: Math.PI, viewX: -6.5, viewZ: pavStart + pavDepth - 3.8 },
    // 2: Center-Right Video on North Wall: Weekend at Ernies Short Film Teaser.mp4
    { x: 6.5,   y: 2.6, z: pavStart + pavDepth - 0.16, rotY: Math.PI, viewX: 6.5, viewZ: pavStart + pavDepth - 3.8 },
    // 3: West Wall Video: Case File No. 27 Motion Graphics.mp4
    { x: -12.85, y: 2.4, z: pavStart + 5.5, rotY: Math.PI / 2, viewX: -9.8, viewZ: pavStart + 5.5 },
    // 4: West Wall: The Wind Rises Storyboard Sheet 3
    { x: -12.85, y: 2.4, z: pavStart + 11.5, rotY: Math.PI / 2, viewX: -9.8, viewZ: pavStart + 11.5 },
    // 5: East Wall Video: Patterns Motion Animatic.mov
    { x: 12.85,  y: 2.4, z: pavStart + 5.5, rotY: -Math.PI / 2, viewX: 9.8, viewZ: pavStart + 5.5 },
    // 6: East Wall Video: Foley Cedilla Plate 2.mp4
    { x: 12.85,  y: 2.4, z: pavStart + 11.5, rotY: -Math.PI / 2, viewX: 9.8, viewZ: pavStart + 11.5 },
    // 7: South Wall Left of Portal: The Wind Rises Storyboard Sheet 4
    { x: -7.5,   y: 2.4, z: pavStart + 0.16, rotY: 0, viewX: -7.5, viewZ: pavStart + 3.2 },
    // 8: South Wall Right of Portal: Oi Marichin Marukoy Fancy Kitchen Set
    { x: 7.5,    y: 2.4, z: pavStart + 0.16, rotY: 0, viewX: 7.5, viewZ: pavStart + 3.2 }
  ];

  listIV.forEach((ex, idx) => {
    if (idx >= ivSpots.length) return;
    const spot = ivSpots[idx];
    const { group } = buildPictureFrame(ex);
    group.position.set(spot.x, spot.y, spot.z);
    group.rotation.y = spot.rotY;
    scene.add(group);
    ex.teleportPos = new THREE.Vector3(spot.viewX, EYE_HEIGHT, spot.viewZ);
    ex.lookTarget = new THREE.Vector3(spot.x, spot.y, spot.z);
  });"""

content = re.sub(old_layout_regex, new_layout_code, content)
print("Updated layoutExhibits() with spacious coordinates and Hogwarts videos!")

# 6. Update updateCurrentWingCaption coordinates for the new layout
old_caption_regex = r'function updateCurrentWingCaption\(pos\) \{[\s\S]*?clearTimeout\(cap\._timer\);[\s\S]*?cap\._timer = setTimeout\(\(\) => cap\.classList\.remove\(\'show\'\), 3200\);\s*\}\s*\}'

new_caption_code = """function updateCurrentWingCaption(pos) {
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
  } else if (pos.z > 51.5) {
    wingName = EUNOIA_CONFIG.wings.IV.name;
    wingNum = 'Wing IV';
  } else if (pos.z > 8.0) {
    // Inside Wing II Multi-Chamber Complex
    if (pos.x < -4.0) {
      if (pos.z < 30.0) {
        wingName = 'Wing II · 3D Environment Gallery';
        wingNum = 'Room A';
      } else {
        wingName = 'Wing II · 3D VFX Theatre';
        wingNum = 'Room C';
      }
    } else if (pos.x > 4.0) {
      if (pos.z < 30.0) {
        wingName = 'Wing II · 3D Interior Architecture';
        wingNum = 'Room B';
      } else {
        wingName = 'Wing II · 3D Still Life Studio';
        wingNum = 'Room D';
      }
    } else {
      if (pos.z >= 20.5 && pos.z <= 34.0) {
        wingName = 'Wing II · 3D Character Studio';
        wingNum = 'Colonnade';
      } else {
        wingName = 'Wing II · 3D Virtual Worlds Promenade';
        wingNum = 'Colonnade';
      }
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

content = re.sub(old_caption_regex, new_caption_code, content)
print("Updated updateCurrentWingCaption() coordinates!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated index.html!")

