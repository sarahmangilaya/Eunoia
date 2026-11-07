import re

with open('index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Camera Far and PixelRatio
old_cam = "const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.15, 120);"
new_cam = "const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.15, 65.0);"
assert old_cam in code, "old_cam not found"
code = code.replace(old_cam, new_cam, 1)

old_pr = "renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75));"
new_pr = "renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.25));"
code = code.replace(old_pr, new_pr)

print("1. Updated camera.far (65.0) and pixelRatio (1.25)!")

# 2. Add FrameGeoCache and optimized buildPictureFrame
old_build_pic_start = code.find('function buildPictureFrame(exhibit, width, height) {')
assert old_build_pic_start != -1, "buildPictureFrame not found"

old_build_pic_end = code.find('/* --------------------------------------------------------------------------\n   4.10  EXHIBIT SPOTS')
assert old_build_pic_end != -1, "EXHIBIT SPOTS start not found"

# Let's inspect what is currently between old_build_pic_start and old_build_pic_end
# We will define FrameGeoCache right before buildPictureFrame
new_pic_frame_block = """// ============================================================================
// PERFORMANCE OPTIMIZATION: GEOMETRY CACHE & STREAMING VIDEO TEXTURES
// ============================================================================
const FrameGeoCache = {
  backLandscape: new RoundedBoxGeometry(2.6 + 0.32, 1.95 + 0.32, 0.12, 2, 0.02),
  backPortrait:  new RoundedBoxGeometry(1.95 + 0.32, 2.6 + 0.32, 0.12, 2, 0.02),
  linerLandscape: new RoundedBoxGeometry(2.6 + 0.08, 1.95 + 0.08, 0.13, 2, 0.01),
  linerPortrait:  new RoundedBoxGeometry(1.95 + 0.08, 2.6 + 0.08, 0.13, 2, 0.01),
  canvasLandscape: new THREE.PlaneGeometry(2.6, 1.95),
  canvasPortrait:  new THREE.PlaneGeometry(1.95, 2.6),
  plaque: new THREE.PlaneGeometry(0.7, 0.28),
  fixtureBar: new THREE.CylinderGeometry(0.015, 0.015, 0.6, 6),
  fixtureHood: new RoundedBoxGeometry(0.7, 0.06, 0.12, 2, 0.01),
  stem: new THREE.CylinderGeometry(0.01, 0.01, 0.35, 6),
  lampBulb: new THREE.CylinderGeometry(0.012, 0.012, 0.52, 6)
};
FrameGeoCache.fixtureBar.rotateZ(Math.PI / 2);
FrameGeoCache.lampBulb.rotateZ(Math.PI / 2);

const activeHogwartsVideos = [];

function wakeAllHogwartsVideos() {
  activeHogwartsVideos.forEach((item) => {
    const v = item.video || item;
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

  const isLandscape = exhibit.orientation === 'landscape';
  const artW = width || (isLandscape ? 2.6 : 1.95);
  const artH = height || (isLandscape ? 1.95 : 2.6);
  const frameDepth = 0.12;

  let frameMat = Mat.goldLeaf;
  if (exhibit.wing === 'II') frameMat = Mat.darkWood;
  if (exhibit.wing === 'III') frameMat = Mat.pedestal;
  if (exhibit.wing === 'IV') frameMat = Mat.bronze;

  // Use cached shared geometry for frame back
  const backGeo = isLandscape ? FrameGeoCache.backLandscape : FrameGeoCache.backPortrait;
  const frameBack = new THREE.Mesh(backGeo, frameMat);
  frameBack.matrixAutoUpdate = false;
  group.add(frameBack);

  // Inner beveled liner / slip
  const linerMat = exhibit.wing === 'II' ? Mat.goldLeaf : Mat.alabaster;
  const linerGeo = isLandscape ? FrameGeoCache.linerLandscape : FrameGeoCache.linerPortrait;
  const liner = new THREE.Mesh(linerGeo, linerMat);
  liner.matrixAutoUpdate = false;
  group.add(liner);

  // Artwork Canvas texture & fallback
  let artMat;
  if (exhibit.mediaType === 'video') {
    // Hogwarts living portrait: continuous silent moving picture with distance management
    const video = document.createElement('video');
    video.src = exhibit.imagePath;
    video.crossOrigin = 'anonymous';
    video.loop = true;
    video.muted = true;
    video.defaultMuted = true;
    video.volume = 0;
    video.playsInline = true;
    video.setAttribute('playsinline', '');
    video.setAttribute('webkit-playsinline', '');
    video.setAttribute('muted', '');
    video.setAttribute('loop', '');
    video.preload = 'metadata'; // Low memory footprint

    const videoTex = new THREE.VideoTexture(video);
    videoTex.colorSpace = THREE.SRGBColorSpace;
    videoTex.minFilter = THREE.LinearFilter;
    videoTex.magFilter = THREE.LinearFilter;
    videoTex.generateMipmaps = false;

    artMat = new THREE.MeshBasicMaterial({ map: videoTex });

    activeHogwartsVideos.push({
      video,
      videoTex,
      group,
      wing: exhibit.wing,
      room: exhibit.room
    });
  } else {
    const fallbackCanvas = paintArtwork('gallery', exhibit.orientation, hashString(exhibit.id));
    const fallbackTex = new THREE.CanvasTexture(fallbackCanvas);
    fallbackTex.colorSpace = THREE.SRGBColorSpace;
    fallbackTex.generateMipmaps = false;
    fallbackTex.minFilter = THREE.LinearFilter;
    fallbackTex.magFilter = THREE.LinearFilter;
    artMat = new THREE.MeshStandardMaterial({
      map: fallbackTex,
      roughness: 0.38,
      metalness: 0.05
    });

    if (exhibit.imagePath) {
      loadTracker.total++;
      texLoader.load(
        exhibit.imagePath,
        (loadedTex) => {
          loadedTex.colorSpace = THREE.SRGBColorSpace;
          loadedTex.generateMipmaps = false; // Fast instant GPU upload without CPU freezing
          loadedTex.minFilter = THREE.LinearFilter;
          loadedTex.magFilter = THREE.LinearFilter;
          loadedTex.anisotropy = Math.min(4, MAX_ANISO);
          artMat.map = loadedTex;
          artMat.needsUpdate = true;
          fallbackTex.dispose();
          loadTracker.done++;
          loadTracker.ok++;
          updateLoadStatus();
        },
        undefined,
        (err) => {
          loadTracker.done++;
          updateLoadStatus();
        }
      );
    }
  }

  const canvasGeo = isLandscape ? FrameGeoCache.canvasLandscape : FrameGeoCache.canvasPortrait;
  const artCanvasMesh = new THREE.Mesh(canvasGeo, artMat);
  artCanvasMesh.position.z = frameDepth / 2 + 0.015;
  artCanvasMesh.receiveShadow = false;
  group.add(artCanvasMesh);

  // Attach data to interactive mesh
  artCanvasMesh.userData = { exhibit, group };
  exhibitMeshes.push(artCanvasMesh);
  exhibitDataMap.set(artCanvasMesh.uuid, exhibit);

  // Museum Wall Plaque beneath painting
  const plaqueTex = textTexture(512, 192, (ctx, w, h) => {
    ctx.fillStyle = '#001514';
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#e6af2e';
    ctx.lineWidth = 4;
    ctx.strokeRect(6, 6, w - 12, h - 12);
    ctx.fillStyle = '#e6af2e';
    ctx.font = `600 22px ${SANS}`;
    ctx.textAlign = 'center';
    ctx.fillText(`${exhibit.category.toUpperCase()} · ${exhibit.year}`, w / 2, 42);
    ctx.fillStyle = '#fbfffe';
    ctx.font = `600 32px ${SERIF}`;
    wrapText(ctx, exhibit.title, w / 2, 88, w - 40, 36);
    ctx.fillStyle = '#dbe4e2';
    ctx.font = `italic 20px ${SERIF}`;
    ctx.fillText(exhibit.subtitle || '', w / 2, 154);
  });
  plaqueTex.generateMipmaps = false;
  plaqueTex.minFilter = THREE.LinearFilter;

  const plaqueMesh = new THREE.Mesh(
    FrameGeoCache.plaque,
    new THREE.MeshStandardMaterial({ map: plaqueTex, roughness: 0.35 })
  );
  plaqueMesh.position.set(0, -artH / 2 - 0.34, frameDepth / 2);
  plaqueMesh.matrixAutoUpdate = false;
  group.add(plaqueMesh);

  // Small brass light fixture geometry above frame with warm glowing filament
  const fixtureBar = new THREE.Mesh(FrameGeoCache.fixtureBar, Mat.bronze);
  fixtureBar.position.set(0, artH / 2 + 0.32, 0.35);
  fixtureBar.matrixAutoUpdate = false;

  const fixtureHood = new THREE.Mesh(FrameGeoCache.fixtureHood, Mat.bronze);
  fixtureHood.position.set(0, artH / 2 + 0.35, 0.35);
  fixtureHood.matrixAutoUpdate = false;

  const stemL = new THREE.Mesh(FrameGeoCache.stem, Mat.bronze);
  stemL.rotation.x = Math.PI / 3; stemL.position.set(-0.25, artH / 2 + 0.18, 0.18);
  stemL.matrixAutoUpdate = false;

  const stemR = new THREE.Mesh(FrameGeoCache.stem, Mat.bronze);
  stemR.rotation.x = Math.PI / 3; stemR.position.set(0.25, artH / 2 + 0.18, 0.18);
  stemR.matrixAutoUpdate = false;

  const lampBulb = new THREE.Mesh(FrameGeoCache.lampBulb, new THREE.MeshBasicMaterial({ color: 0xfff0c8 }));
  lampBulb.position.set(0, artH / 2 + 0.32, 0.33);
  lampBulb.matrixAutoUpdate = false;

  group.add(fixtureBar, fixtureHood, stemL, stemR, lampBulb);

  return { group, artCanvasMesh, artW, artH };
}
"""

code = code[:old_build_pic_start] + new_pic_frame_block.strip() + "\n\n" + code[old_build_pic_end:]
print("2. Injected FrameGeoCache and optimized buildPictureFrame!")

# 3. Update Wing Groups in buildArchitecture and layoutExhibits
# Let's inspect where buildWingI, buildWingII etc. are declared
# We can create top-level wing groups:
# const rotunda_group = new THREE.Group();
# const wingI_group = new THREE.Group();
# const wingII_group = new THREE.Group();
# const wingIII_group = new THREE.Group();
# const wingIV_group = new THREE.Group();

wing_groups_decl = """// Grand Wing Groups for Hierarchical Occlusion Culling
const rotunda_group = new THREE.Group();
const wingI_group = new THREE.Group();
const wingII_group = new THREE.Group();
const wingIII_group = new THREE.Group();
const wingIV_group = new THREE.Group();
"""

arch_header_needle = "/* ==========================================================================\n     §4.9 MUSEUM ARCHITECTURE (4 GRAND WINGS & SPECIALIZED CHAMBERS)\n     ========================================================================== */"
assert arch_header_needle in code, "arch_header_needle not found"

code = code.replace(arch_header_needle, arch_header_needle + "\n\n  " + wing_groups_decl.strip(), 1)
print("3. Injected wing groups declaration!")

# In buildArchitecture:
# Replace root.add(wing) in buildWingI with wingI_group.add(wing); scene.add(wingI_group);
# Replace root.add(wing) in buildWingII with wingII_group.add(wing); scene.add(wingII_group);
# Replace root.add(wing) in buildWingIII with wingIII_group.add(wing); scene.add(wingIII_group);
# Replace root.add(wing) in buildWingIV with wingIV_group.add(wing); scene.add(wingIV_group);
# And in buildArchitecture bottom:
# rotunda_group.add(root); scene.add(rotunda_group);

code = code.replace("/* --- 2.1 Wing I: The Classical & Fine Arts Wing (29 Works) --- */\n  function buildWingI() {\n    const wing = new THREE.Group();",
                    "/* --- 2.1 Wing I: The Classical & Fine Arts Wing (29 Works) --- */\n  function buildWingI() {\n    const wing = wingI_group;", 1)

code = code.replace("/* --- 2.2 Wing II: The 3D Virtual Worlds Pavilion (38 Works) --- */\n  function buildWingII() {\n    const wing = new THREE.Group();",
                    "/* --- 2.2 Wing II: The 3D Virtual Worlds Pavilion (38 Works) --- */\n  function buildWingII() {\n    const wing = wingII_group;", 1)

code = code.replace("/* --- 2.3 Wing III: The Nocturne & Observational Photography Gallery (86 Works) --- */\n  function buildWingIII() {\n    const wing = new THREE.Group();",
                    "/* --- 2.3 Wing III: The Nocturne & Observational Photography Gallery (86 Works) --- */\n  function buildWingIII() {\n    const wing = wingIII_group;", 1)

code = code.replace("/* --- 2.4 Wing IV: The Kinematic & Applied Design Pavilion (52 Works) --- */\n  function buildWingIV() {\n    const wing = new THREE.Group();",
                    "/* --- 2.4 Wing IV: The Kinematic & Applied Design Pavilion (52 Works) --- */\n  function buildWingIV() {\n    const wing = wingIV_group;", 1)

# In each wing function, remove the `root.add(wing);` at the end
code = code.replace("    root.add(wing);\n  }\n\n  /* --- 2.2 Wing II:", "  }\n\n  /* --- 2.2 Wing II:", 1)
code = code.replace("    root.add(wing);\n  }\n\n  /* --- 2.3 Wing III:", "  }\n\n  /* --- 2.3 Wing III:", 1)
code = code.replace("    root.add(wing);\n  }\n\n  /* --- 2.4 Wing IV:", "  }\n\n  /* --- 2.4 Wing IV:", 1)
code = code.replace("    root.add(wing);\n  }\n\n  // Build all 4 expanded wings", "  }\n\n  // Build all 4 expanded wings", 1)

# At the bottom of buildArchitecture:
old_bottom = """  // Build all 4 expanded wings
  buildWingI();
  buildWingII();
  buildWingIII();
  buildWingIV();

  scene.add(root);
}"""

new_bottom = """  // Build all 4 expanded wings
  buildWingI();
  buildWingII();
  buildWingIII();
  buildWingIV();

  rotunda_group.add(root);
  scene.add(rotunda_group, wingI_group, wingII_group, wingIII_group, wingIV_group);
}"""

assert old_bottom in code, "old_bottom not found"
code = code.replace(old_bottom, new_bottom, 1)
print("4. Wired wing groups to scene hierarchy!")

# 4. In layoutExhibits: add exhibit frames to their wing groups instead of scene directly!
old_layout_add = """      const { group } = buildPictureFrame(ex);
      group.position.set(spot.x, spot.y, spot.z);
      group.rotation.y = spot.rotY;
      scene.add(group);"""

new_layout_add = """      const { group } = buildPictureFrame(ex);
      group.position.set(spot.x, spot.y, spot.z);
      group.rotation.y = spot.rotY;
      group.updateMatrix();

      if (ex.wing === 'I') wingI_group.add(group);
      else if (ex.wing === 'II') wingII_group.add(group);
      else if (ex.wing === 'III') wingIII_group.add(group);
      else if (ex.wing === 'IV') wingIV_group.add(group);
      else scene.add(group);"""

assert old_layout_add in code, "old_layout_add not found"
code = code.replace(old_layout_add, new_layout_add, 1)
print("5. Connected exhibits to their respective wing groups in layoutExhibits!")

# 5. In animate(): add Dynamic Wing Culling and Video Proximity Update
old_render_call = """  // 5. Render Scene
  renderer.render(scene, camera);"""

new_render_call = """  // 4.5 Performance: Dynamic Wing Culling & Hogwarts Video Proximity Streaming
  const camX = camera.position.x;
  const camZ = camera.position.z;

  const inRotunda = Math.abs(camX) < 9.5 && Math.abs(camZ) < 9.5;
  const inWingI   = camX > 7.5;
  const inWingIII = camX < -7.5;
  const inWingII  = camZ > 7.5 && camZ <= 52.0 && Math.abs(camX) < 25.0;
  const inWingIV  = camZ > 50.0;

  if (inRotunda) {
    rotunda_group.visible = true;
    wingI_group.visible = true;
    wingII_group.visible = true;
    wingIII_group.visible = true;
    wingIV_group.visible = false;
  } else if (inWingI) {
    rotunda_group.visible = (camX < 18.0);
    wingI_group.visible = true;
    wingII_group.visible = false;
    wingIII_group.visible = false;
    wingIV_group.visible = false;
  } else if (inWingIII) {
    rotunda_group.visible = (camX > -18.0);
    wingIII_group.visible = true;
    wingI_group.visible = false;
    wingII_group.visible = false;
    wingIV_group.visible = false;
  } else if (inWingII) {
    rotunda_group.visible = (camZ < 16.0);
    wingII_group.visible = true;
    wingIV_group.visible = (camZ > 36.0);
    wingI_group.visible = false;
    wingIII_group.visible = false;
  } else if (inWingIV) {
    rotunda_group.visible = false;
    wingIV_group.visible = true;
    wingII_group.visible = (camZ < 68.0);
    wingI_group.visible = false;
    wingIII_group.visible = false;
  }

  // Hogwarts video proximity streaming (play only within 26m)
  for (let vi = 0; vi < activeHogwartsVideos.length; vi++) {
    const hv = activeHogwartsVideos[vi];
    const dSq = hv.group.position.distanceToSquared(camera.position);
    if (dSq < 676.0) { // 26m squared
      if (hv.video.paused) {
        hv.video.muted = true;
        hv.video.volume = 0;
        hv.video.play().catch(() => {});
      }
    } else {
      if (!hv.video.paused) {
        hv.video.pause();
      }
    }
  }

  // 5. Render Scene
  renderer.render(scene, camera);"""

assert old_render_call in code, "old_render_call not found"
code = code.replace(old_render_call, new_render_call, 1)
print("6. Injected Dynamic Wing Culling and Video Proximity Streaming in animate()!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("ALL PERFORMANCE OPTIMIZATIONS SUCCESSFULLY APPLIED TO index.html!")

