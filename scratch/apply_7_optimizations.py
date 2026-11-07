import re, shutil

shutil.copy('index.html', 'scratch/index.html.pre7.bak')
html = open('index.html', encoding='utf-8').read()

def must_replace(src, old, new, label, count=1):
    assert old in src, f"[{label}] anchor not found"
    return src.replace(old, new, count)

# ---------------------------------------------------------------------------
# 0. Import mergeGeometries + disable shadow maps (zero dynamic shadow passes)
# ---------------------------------------------------------------------------
m = re.search(r"import \{ RoundedBoxGeometry \}[^\n]*\n", html)
assert m, "RoundedBoxGeometry import not found"
html = html[:m.end()] + "import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';\n" + html[m.end():]

html = must_replace(html, "renderer.shadowMap.enabled = true;", "renderer.shadowMap.enabled = false; // perf: zero dynamic shadow maps", "shadowMap")

# ---------------------------------------------------------------------------
# 1+2+3+5. FrameGeoCache / video manager / texture queue / buildPictureFrame
# ---------------------------------------------------------------------------
start = html.find('const FrameGeoCache = {')
assert start != -1
ret = html.find('return { group, artCanvasMesh, artW, artH };\n}', start)
assert ret != -1
end = ret + len('return { group, artCanvasMesh, artW, artH };\n}')

NEW_BLOCK = r'''const FrameGeoCache = {
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

/* Merge bar + hood + both stems into ONE static brass geometry (1 mesh instead of 4). */
function buildMergedFixture(artH) {
  const parts = [];
  const bar = FrameGeoCache.fixtureBar.clone(); bar.translate(0, artH / 2 + 0.32, 0.35); parts.push(bar);
  const hood = FrameGeoCache.fixtureHood.clone(); hood.translate(0, artH / 2 + 0.35, 0.35); parts.push(hood);
  [-0.25, 0.25].forEach((sx) => {
    const st = FrameGeoCache.stem.clone();
    st.rotateX(Math.PI / 3); st.translate(sx, artH / 2 + 0.18, 0.18);
    parts.push(st);
  });
  const merged = mergeGeometries(parts, false);
  parts.forEach((p) => p.dispose());
  return merged;
}
FrameGeoCache.fixtureMergedLandscape = buildMergedFixture(1.95);
FrameGeoCache.fixtureMergedPortrait = buildMergedFixture(2.6);
FrameGeoCache.lampBulbLandscape = FrameGeoCache.lampBulb; // shared
const LAMP_BULB_MAT = new THREE.MeshBasicMaterial({ color: 0xfff6d0 });

/* Two shared procedural fallbacks for ALL frames (instead of 180 painterly canvases). */
function makeSharedFallback(orientation, w, h, seed) {
  const src = paintArtwork('gallery', orientation, seed);
  const [c, ctx] = makeCanvas(w, h);
  ctx.drawImage(src, 0, 0, w, h);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.generateMipmaps = false;
  t.minFilter = THREE.LinearFilter;
  t.magFilter = THREE.LinearFilter;
  return t;
}
const SHARED_FALLBACK_LANDSCAPE = makeSharedFallback('landscape', 512, 384, 1337);
const SHARED_FALLBACK_PORTRAIT = makeSharedFallback('portrait', 384, 512, 7331);
const ART_TINT = 0xe8e4dc;

/* ---------------------------------------------------------------------------
   Hogwarts living portraits - lazy, proximity-driven, never input-driven
   --------------------------------------------------------------------------- */
const activeHogwartsVideos = [];
window.activeHogwartsVideos = activeHogwartsVideos;
let lastVideoCheckTime = 0;

/* Kept for API compatibility: just requests an immediate proximity re-check.
   It is NO LONGER bound to keydown / click / pointerdown / touchstart. */
function wakeAllHogwartsVideos() { lastVideoCheckTime = 0; }

function activateHogwartsVideo(hv) {
  const v = hv.video;
  if (!hv.videoTex) {
    hv.videoTex = new THREE.VideoTexture(v);
    hv.videoTex.colorSpace = THREE.SRGBColorSpace;
    hv.videoTex.minFilter = THREE.LinearFilter;
    hv.videoTex.magFilter = THREE.LinearFilter;
    hv.videoTex.generateMipmaps = false;
  }
  if (!hv.srcSet) {
    hv.srcSet = true;
    v.preload = 'auto';
    v.addEventListener('loadeddata', () => {
      hv.artMat.map = hv.videoTex;
      hv.artMat.needsUpdate = true;
    }, { once: true });
    v.src = hv.srcPath;
  }
  if (v.paused) {
    v.muted = true; v.volume = 0;
    v.play().catch(() => {});
  }
}

function releaseHogwartsVideo(hv) {
  if (!hv.srcSet) return;
  const v = hv.video;
  v.pause();
  v.removeAttribute('src');
  v.load();
  hv.srcSet = false;
  hv.artMat.map = hv.fallbackTex;
  hv.artMat.needsUpdate = true;
}

function updateHogwartsVideos() {
  const cp = camera.position;
  const near = [];
  for (let i = 0; i < activeHogwartsVideos.length; i++) {
    const hv = activeHogwartsVideos[i];
    hv.dSq = hv.group.position.distanceToSquared(cp);
    if (hv.dSq < 144.0) near.push(hv); // within 12 m
  }
  near.sort((a, b) => a.dSq - b.dSq);
  const play = new Set(near.slice(0, 2));
  let playing = play.size;
  for (let i = 0; i < activeHogwartsVideos.length; i++) {
    const hv = activeHogwartsVideos[i];
    if (play.has(hv)) { activateHogwartsVideo(hv); continue; }
    if (hv.srcSet && !hv.video.paused) {
      // hysteresis band 12-16 m: keep playing only if we are under the 2-video cap
      if (hv.dSq > 256.0 || playing >= 2) hv.video.pause();
      else playing++;
    }
    if (hv.srcSet && hv.dSq > 900.0) releaseHogwartsVideo(hv); // >30 m: free buffers
  }
}

/* ---------------------------------------------------------------------------
   Texture streaming: fetch -> createImageBitmap (max 1024px) -> 1 GPU upload / frame
   Full-res imagePath is kept ONLY for the 2D #plqImg inspection modal.
   --------------------------------------------------------------------------- */
const TEX_MAX_DIM = 1024;
const TextureLoadQueue = {
  queue: [],
  uploads: [],
  activeCount: 0,
  maxConcurrent: 2,
  paused: true,
  enqueue(item) {
    this.queue.push(item);
    if (!this.paused) this.process();
  },
  resume() { this.paused = false; this.process(); },
  pickNext() {
    let best = 0, bestScore = Infinity;
    const cp = camera.position;
    for (let i = 0; i < this.queue.length; i++) {
      const it = this.queue[i];
      const score = (it.wing === currentWingKey ? 0 : 1e6) + it.group.position.distanceToSquared(cp);
      if (score < bestScore) { bestScore = score; best = i; }
    }
    return best;
  },
  process() {
    while (this.activeCount < this.maxConcurrent && this.queue.length > 0) {
      const item = this.queue.splice(this.pickNext(), 1)[0];
      this.activeCount++;
      this.decode(item.url).then(
        (bmp) => { this.uploads.push({ item, bmp }); },
        () => { loadTracker.done++; updateLoadStatus(); }
      ).finally(() => {
        this.activeCount--;
        // 16 ms yield between decodes so the main thread is never saturated
        setTimeout(() => this.process(), 16);
      });
    }
  },
  async downscale(source, w, h) {
    const s = Math.min(1, TEX_MAX_DIM / Math.max(w, h));
    return createImageBitmap(source, {
      resizeWidth: Math.max(1, Math.round(w * s)),
      resizeHeight: Math.max(1, Math.round(h * s)),
      resizeQuality: 'medium',
      imageOrientation: 'flipY'
    });
  },
  async decode(url) {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const blob = await res.blob();
      const full = await createImageBitmap(blob);
      const small = await this.downscale(full, full.width, full.height);
      full.close();
      return small;
    } catch (e) {
      // Fallback (e.g. file:// where fetch is blocked): <img> -> bitmap
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.crossOrigin = 'anonymous';
        img.onload = () => this.downscale(img, img.naturalWidth, img.naturalHeight).then(resolve, reject);
        img.onerror = reject;
        img.src = url;
      });
    }
  },
  /* Called once per animation frame: at most ONE texture reaches the GPU per frame. */
  pump() {
    if (this.uploads.length === 0) return;
    const { item, bmp } = this.uploads.shift();
    const tex = new THREE.Texture(bmp);
    tex.flipY = false; // bitmap already flipped at creation
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.generateMipmaps = false;
    tex.minFilter = THREE.LinearFilter;
    tex.magFilter = THREE.LinearFilter;
    tex.onUpdate = (t) => { if (t.image && t.image.close) t.image.close(); t.onUpdate = null; };
    tex.needsUpdate = true;
    renderer.initTexture(tex); // deterministic single upload now
    item.artMat.map = tex;
    loadTracker.done++;
    loadTracker.ok++;
    updateLoadStatus();
  }
};
window.TextureLoadQueue = TextureLoadQueue;

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

  const flat = (m) => { m.castShadow = false; m.receiveShadow = false; m.matrixAutoUpdate = false; m.updateMatrix(); return m; };

  const frameBack = flat(new THREE.Mesh(isLandscape ? FrameGeoCache.backLandscape : FrameGeoCache.backPortrait, frameMat));
  group.add(frameBack);

  const linerMat = exhibit.wing === 'II' ? Mat.goldLeaf : Mat.alabaster;
  const liner = flat(new THREE.Mesh(isLandscape ? FrameGeoCache.linerLandscape : FrameGeoCache.linerPortrait, linerMat));
  group.add(liner);

  // Canvas: unlit MeshBasicMaterial (no per-pixel PBR lighting), shared fallback texture first
  const fallbackTex = isLandscape ? SHARED_FALLBACK_LANDSCAPE : SHARED_FALLBACK_PORTRAIT;
  const artMat = new THREE.MeshBasicMaterial({ map: fallbackTex, color: ART_TINT });

  if (exhibit.mediaType === 'video') {
    // No src, no preload at startup: the proximity manager assigns it lazily.
    const video = document.createElement('video');
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
    video.preload = 'none';

    activeHogwartsVideos.push({
      video, videoTex: null, group, artMat, fallbackTex,
      srcPath: exhibit.imagePath, srcSet: false, dSq: Infinity,
      wing: exhibit.wing, room: exhibit.room
    });
  } else if (exhibit.imagePath) {
    loadTracker.total++;
    TextureLoadQueue.enqueue({ url: exhibit.imagePath, artMat, group, wing: exhibit.wing });
  }

  const canvasGeo = isLandscape ? FrameGeoCache.canvasLandscape : FrameGeoCache.canvasPortrait;
  const artCanvasMesh = new THREE.Mesh(canvasGeo, artMat);
  artCanvasMesh.position.z = frameDepth / 2 + 0.015;
  artCanvasMesh.castShadow = false;
  artCanvasMesh.receiveShadow = false;
  group.add(artCanvasMesh);

  artCanvasMesh.userData = { exhibit, group };
  exhibitMeshes.push(artCanvasMesh);
  exhibitDataMap.set(artCanvasMesh.uuid, exhibit);

  // Museum wall plaque: 256x96 canvas (drawn in a 512x192 logical space)
  const plaqueTex = textTexture(256, 96, (ctx, cw, ch) => {
    ctx.save();
    ctx.scale(cw / 512, ch / 192);
    const w = 512, h = 192;
    ctx.fillStyle = '#001514';
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#e6af2e';
    ctx.lineWidth = 4;
    ctx.strokeRect(6, 6, w - 12, h - 12);
    ctx.fillStyle = '#e6af2e';
    ctx.font = `600 22px ${SANS}`;
    ctx.textAlign = 'center';
    ctx.fillText(`${(exhibit.category || '').toUpperCase()} · ${exhibit.year || ''}`, w / 2, 42);
    if (exhibit.title) {
      ctx.fillStyle = '#fbfffe';
      ctx.font = `600 32px ${SERIF}`;
      wrapText(ctx, exhibit.title, w / 2, 88, w - 40, 36);
      ctx.fillStyle = '#dbe4e2';
      ctx.font = `italic 20px ${SERIF}`;
      ctx.fillText(exhibit.subtitle || '', w / 2, 154);
    } else {
      ctx.fillStyle = '#fbfffe';
      ctx.font = `italic 24px ${SERIF}`;
      ctx.fillText(exhibit.category || '', w / 2, 108);
    }
    ctx.restore();
  });
  plaqueTex.generateMipmaps = false;
  plaqueTex.minFilter = THREE.LinearFilter;
  plaqueTex.anisotropy = 1;

  const plaqueMesh = new THREE.Mesh(FrameGeoCache.plaque, new THREE.MeshBasicMaterial({ map: plaqueTex, color: 0xe0e0e0 }));
  plaqueMesh.position.set(0, -artH / 2 - 0.34, frameDepth / 2);
  group.add(flat(plaqueMesh));

  // Brass lamp: 4 parts merged into 1 geometry + 1 shared glowing bulb
  const fixtureGeo = artH === 1.95 ? FrameGeoCache.fixtureMergedLandscape
                   : artH === 2.6 ? FrameGeoCache.fixtureMergedPortrait
                   : buildMergedFixture(artH);
  const fixture = flat(new THREE.Mesh(fixtureGeo, Mat.bronze));
  const lampBulb = new THREE.Mesh(FrameGeoCache.lampBulb, LAMP_BULB_MAT);
  lampBulb.position.set(0, artH / 2 + 0.32, 0.33);
  flat(lampBulb);
  group.add(fixture, lampBulb);

  return { group, artCanvasMesh, artW, artH };
}'''
html = html[:start] + NEW_BLOCK + html[end:]

# ---------------------------------------------------------------------------
# 4a. Remove portal PointLights
# ---------------------------------------------------------------------------
html = must_replace(html,
"""  // Subtle warm gallery accent lights for both entrance and exit signs
  const entrySignLight = new THREE.PointLight(0xffe4a0, 2.5, 5, 1.3);
  entrySignLight.position.set(0, 4.3, -1.2);
  const exitSignLight = new THREE.PointLight(0xffe4a0, 2.5, 5, 1.3);
  exitSignLight.position.set(0, 4.3, 1.2);

  g.add(lintel, frieze, cornice, jL, jR, retL, retR, attic, signIn, signOut, entrySignLight, exitSignLight);""",
"""  g.add(lintel, frieze, cornice, jL, jR, retL, retR, attic, signIn, signOut);""", "wallPortalLights")

html = must_replace(html,
"""    const signLight = new THREE.PointLight(0xffe4a0, 1.8, 6, 1.3);
    signLight.position.set(0, 4.2, 1.0);

    g.add(lintel, colL, colR, signMesh, signLight);""",
"""    g.add(lintel, colL, colR, signMesh);""", "galleryPortalLight")

# ---------------------------------------------------------------------------
# 4b. buildLighting: constant light count, no shadows, no chamber point lights
# ---------------------------------------------------------------------------
ls = html.find('function buildLighting() {')
le = html.find('\n}\n\n/* --------------------------------------------------------------------------\n   4.12', ls)
assert ls != -1 and le != -1
NEW_LIGHTING = r'''function buildLighting() {
  // Constant light count (4 total) => no shader recompiles when wings toggle visibility.
  const hemi = new THREE.HemisphereLight(0xdcd0bc, 0x000808, 0.65);
  scene.add(hemi);

  const amb = new THREE.AmbientLight(0xfbf2e4, 0.45);
  scene.add(amb);

  // Warm visitor lantern follows the camera and lights whatever you approach
  const visitorLantern = new THREE.PointLight(0xffeed4, 1.8, 14.0, 1.4);
  camera.add(visitorLantern);
  scene.add(camera);

  // Rotunda skylight: global (not inside a toggled group), NO shadow map
  const rotundaSun = new THREE.SpotLight(0xffeaad, 36, 22, Math.PI / 3.2, 0.65, 1.2);
  rotundaSun.position.set(0, H_ROT + 1.2, 0);
  rotundaSun.target.position.set(0, 0, 0);
  rotundaSun.castShadow = false;
  scene.add(rotundaSun, rotundaSun.target);

  // Baked soft contact shadow under the central sculpture
  const [sc, sctx] = makeCanvas(256, 256);
  const grad = sctx.createRadialGradient(128, 128, 20, 128, 128, 128);
  grad.addColorStop(0, 'rgba(0,0,0,0.55)');
  grad.addColorStop(1, 'rgba(0,0,0,0)');
  sctx.fillStyle = grad; sctx.fillRect(0, 0, 256, 256);
  const shadowTex = new THREE.CanvasTexture(sc);
  const bakedShadow = new THREE.Mesh(
    new THREE.PlaneGeometry(4.6, 4.6),
    new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false })
  );
  bakedShadow.rotation.x = -Math.PI / 2;
  bakedShadow.position.y = 0.012;
  rotunda_group.add(bakedShadow);
}'''
html = html[:ls] + NEW_LIGHTING + html[le + 2:]

# ---------------------------------------------------------------------------
# 4c. Wing culling (facing-aware Rotunda + depth culling of deep sub-chambers)
# ---------------------------------------------------------------------------
cs = html.find('function updateWingCulling() {')
ce = html.find('\nfunction animate() {', cs)
assert cs != -1 and ce != -1
NEW_CULL = r'''let currentWingKey = 'R';
const WING_PORTALS = {
  I: new THREE.Vector3(8.3, 0, 0),
  II: new THREE.Vector3(0, 0, 8.3),
  III: new THREE.Vector3(-8.3, 0, 0)
};
const _cullFwd = new THREE.Vector3();
const _cullTmp = new THREE.Vector3();

/* From inside the Rotunda, hide deep sub-chambers (> 28 m from the wing threshold). */
function setWingDepthCull(key, active) {
  const group = { I: wingI_group, II: wingII_group, III: wingIII_group }[key];
  if (!group || group.userData.depthCulled === active) return;
  if (active && !group.userData.cullCache) {
    group.updateMatrixWorld(true);
    group.userData.cullCache = group.children.map((c) => ({ c, box: new THREE.Box3().setFromObject(c) }));
  }
  const cache = group.userData.cullCache;
  if (cache) {
    const portal = WING_PORTALS[key];
    for (let i = 0; i < cache.length; i++) {
      const e = cache[i];
      e.c.visible = active ? (e.box.isEmpty() || e.box.distanceToPoint(portal) < 28.0) : true;
    }
  }
  group.userData.depthCulled = active;
}

function updateWingCulling() {
  const camX = camera.position.x;
  const camZ = camera.position.z;

  const inWingIV  = (camZ >= 50.0);
  const inWingI   = (camX >= 42.0 && Math.abs(camZ) <= 24.0) || (camX >= 7.5 && Math.abs(camZ) <= 5.5);
  const inWingIII = (camX <= -22.0 && Math.abs(camZ) <= 24.0) || (camX <= -7.5 && Math.abs(camZ) <= 5.5);
  const inWingII  = (camZ >= 7.5 && camZ < 50.0 && Math.abs(camX) < 22.0);

  const inRotunda = !inWingIV && !inWingII && !inWingI && !inWingIII;
  if (!inRotunda) { setWingDepthCull('I', false); setWingDepthCull('II', false); setWingDepthCull('III', false); }

  if (inWingIV) {
    currentWingKey = 'IV';
    rotunda_group.visible = false;
    wingIV_group.visible = true;
    wingII_group.visible = (camZ < 68.0);
    wingI_group.visible = false;
    wingIII_group.visible = false;
  } else if (inWingII) {
    currentWingKey = 'II';
    rotunda_group.visible = (camZ < 16.0);
    wingII_group.visible = true;
    wingIV_group.visible = (camZ > 36.0);
    wingI_group.visible = false;
    wingIII_group.visible = false;
  } else if (inWingI) {
    currentWingKey = 'I';
    rotunda_group.visible = (camX < 18.0);
    wingI_group.visible = true;
    wingII_group.visible = false;
    wingIII_group.visible = false;
    wingIV_group.visible = false;
  } else if (inWingIII) {
    currentWingKey = 'III';
    rotunda_group.visible = (camX > -18.0);
    wingIII_group.visible = true;
    wingI_group.visible = false;
    wingII_group.visible = false;
    wingIV_group.visible = false;
  } else {
    currentWingKey = 'R';
    rotunda_group.visible = true;
    wingIV_group.visible = false;
    const rotunda = Math.hypot(camX, camZ) < 8.5;
    camera.getWorldDirection(_cullFwd);
    const groups = { I: wingI_group, II: wingII_group, III: wingIII_group };
    for (const key of ['I', 'II', 'III']) {
      let vis = true;
      if (rotunda) {
        _cullTmp.subVectors(WING_PORTALS[key], camera.position);
        const dist = _cullTmp.length();
        _cullTmp.y = 0; _cullTmp.normalize();
        const facing = _cullFwd.x * _cullTmp.x + _cullFwd.z * _cullTmp.z;
        vis = dist < 12.0 || facing > 0.25;
      }
      groups[key].visible = vis;
      setWingDepthCull(key, rotunda);
    }
  }
}
'''
html = html[:cs] + NEW_CULL + html[ce:]

# ---------------------------------------------------------------------------
# 6. Throttled + spatially filtered raycast
# ---------------------------------------------------------------------------
rs = html.find('function updateRaycast() {')
re_ = html.find('// Click to inspect', rs)
assert rs != -1 and re_ != -1
NEW_RAY = r'''let lastRaycastTime = 0;
const _rayCandidates = [];

function updateRaycast() {
  const nowR = performance.now();
  if (nowR - lastRaycastTime < 80) return; // ~12 Hz
  lastRaycastTime = nowR;

  if (!isControlsLocked || isInspecting || isCatalogOpen) {
    $('reticle').classList.remove('active');
    $('prompt').classList.remove('show');
    hoveredExhibitMesh = null;
    return;
  }

  // Spatial filter: visible wing + within 7 m  (185 meshes -> ~2-4)
  _rayCandidates.length = 0;
  const cp = camera.position;
  for (let i = 0; i < exhibitMeshes.length; i++) {
    const m = exhibitMeshes[i];
    const g = m.userData.group;
    if (!g.visible || !g.parent || !g.parent.visible) continue;
    if (g.position.distanceToSquared(cp) < 49.0) _rayCandidates.push(m);
  }

  raycaster.setFromCamera(screenCenter, camera);
  raycaster.far = 6.5;
  const intersects = raycaster.intersectObjects(_rayCandidates, false);

  if (intersects.length > 0) {
    const hit = intersects[0].object;
    hoveredExhibitMesh = hit;
    const exhibit = hit.userData.exhibit;
    $('reticle').classList.add('active');
    $('prompt').classList.add('show');
    $('promptTitle').textContent = exhibit.title || exhibit.category || '';
  } else {
    $('reticle').classList.remove('active');
    $('prompt').classList.remove('show');
    hoveredExhibitMesh = null;
  }
}

'''
html = html[:rs] + NEW_RAY + html[re_:]

# ---------------------------------------------------------------------------
# 7. Lazy catalog + pause WebGL while open
# ---------------------------------------------------------------------------
html = must_replace(html,
"""function toggleCatalog(force) {
  isCatalogOpen = force !== undefined ? force : !isCatalogOpen;
  $('catalog').classList.toggle('open', isCatalogOpen);
  $('catalog').setAttribute('aria-hidden', (!isCatalogOpen).toString());
""",
"""let renderCatalogGrid = null;
let catalogBuilt = false;
function toggleCatalog(force) {
  isCatalogOpen = force !== undefined ? force : !isCatalogOpen;
  $('catalog').classList.toggle('open', isCatalogOpen);
  $('catalog').setAttribute('aria-hidden', (!isCatalogOpen).toString());

  if (isCatalogOpen) {
    // Lazy-mount DOM cards only when the catalog is actually opened
    if (!catalogBuilt && renderCatalogGrid) { renderCatalogGrid(); catalogBuilt = true; }
  } else {
    // Unmount cards (frees decoded thumbnails) when closed
    const g = $('catGrid');
    if (g) g.querySelectorAll('video').forEach((v) => { v.pause(); v.removeAttribute('src'); v.load(); });
    if (g) g.innerHTML = '';
    catalogBuilt = false;
  }
""", "toggleCatalog")

# video card -> static poster (no <video autoplay>)
vs = html.find("        const vid = document.createElement('video');")
ve = html.find("        thumb.appendChild(vid);", vs)
assert vs != -1 and ve != -1
ve_end = ve + len("        thumb.appendChild(vid);")
POSTER = r'''        thumb.style.background = 'radial-gradient(circle at 50% 45%, #0b2e2c 0%, #001514 75%)';
        thumb.style.display = 'flex';
        thumb.style.alignItems = 'center';
        thumb.style.justifyContent = 'center';
        const play = document.createElement('div');
        play.textContent = '▶';
        play.style.cssText = 'font-size:42px;color:#e6af2e;opacity:.85;text-shadow:0 0 18px rgba(230,175,46,.45)';
        thumb.appendChild(play);'''
html = html[:vs] + POSTER + html[ve_end:]

html = must_replace(html, "        img.loading = 'lazy';\n", "        img.loading = 'lazy';\n        img.decoding = 'async';\n", "imgDecoding")

html = must_replace(html,
"    filtersNav.appendChild(btn);\n  });\n\n  renderGrid();\n}",
"    filtersNav.appendChild(btn);\n  });\n\n  renderCatalogGrid = renderGrid; // mounted lazily on first toggleCatalog(true)\n}",
"initCatalogTail")

# ---------------------------------------------------------------------------
# animate(): upload pump, video check, skip render while catalog open
# ---------------------------------------------------------------------------
html = must_replace(html,
"function animate() {\n  requestAnimationFrame(animate);\n\n  const delta = Math.min(clock.getDelta(), 0.1);\n",
"function animate() {\n  requestAnimationFrame(animate);\n\n  const delta = Math.min(clock.getDelta(), 0.1);\n\n  // At most ONE texture upload to the GPU per frame\n  TextureLoadQueue.pump();\n",
"animateHead")

vs2 = html.find('  // Hogwarts video proximity streaming (throttled')
ve2 = html.find('  // 5. Render Scene', vs2)
assert vs2 != -1 and ve2 != -1
html = html[:vs2] + """  // Hogwarts video proximity manager (every 300 ms)
  const nowMs = performance.now();
  if (nowMs - lastVideoCheckTime > 300) {
    lastVideoCheckTime = nowMs;
    updateHogwartsVideos();
  }

""" + html[ve2:]

html = must_replace(html,
"  // 5. Render Scene\n  renderer.render(scene, camera);\n",
"  // 5. Render Scene (skipped while the 2D catalog owns the screen)\n  if (!isCatalogOpen) renderer.render(scene, camera);\n",
"renderGate")

# ---------------------------------------------------------------------------
# 5. Time-sliced font redraw
# ---------------------------------------------------------------------------
html = must_replace(html,
"""  document.fonts.ready.then(() => {
    textTextures.forEach(({ ctx, w, h, draw, t }) => {
      ctx.clearRect(0, 0, w, h);
      draw(ctx, w, h);
      t.needsUpdate = true;
    });
  });""",
"""  document.fonts.ready.then(() => {
    let fi = 0;
    const CHUNK = 6; // textures redrawn per frame
    (function redrawChunk() {
      const stop = Math.min(fi + CHUNK, textTextures.length);
      for (; fi < stop; fi++) {
        const { ctx, w, h, draw, t } = textTextures[fi];
        ctx.clearRect(0, 0, w, h);
        draw(ctx, w, h);
        t.needsUpdate = true;
      }
      if (fi < textTextures.length) requestAnimationFrame(redrawChunk);
    })();
  });""", "fonts")

# ---------------------------------------------------------------------------
# Bootstrap: start streaming only after frames are hung
# ---------------------------------------------------------------------------
html = must_replace(html, "layoutExhibits();\nbuildLighting();\ninitCatalog();", "layoutExhibits();\nbuildLighting();\ninitCatalog();\nTextureLoadQueue.resume();", "bootstrap")

open('index.html', 'w', encoding='utf-8').write(html)
print("All 7 optimizations applied.")

