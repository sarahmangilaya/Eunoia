import re

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text_norm = text.replace('\r\n', '\n')

# 1. Add interactivePropMeshes declaration near exhibitMeshes
old_geo_cache = 'const exhibitMeshes = [];      // For raycasting'
new_geo_cache = '''const exhibitMeshes = [];      // For raycasting
const interactivePropMeshes = []; // For raycasting interactive props (telephone, dossier card)'''

if old_geo_cache in text_norm:
    text_norm = text_norm.replace(old_geo_cache, new_geo_cache, 1)
    print("1. Added interactivePropMeshes declaration.")
else:
    print("ERROR: old_geo_cache not found")

# 2. Add buildConciergeStand implementation
# We will define buildConciergeStand right before buildArchitecture or inside it.
concierge_stand_code = '''
/* --------------------------------------------------------------------------
   4.9.5  CURATOR'S CONCIERGE STAND (WALNUT PEDESTAL, ROTARY PHONE & 3D CARD)
   -------------------------------------------------------------------------- */
function makeWalnutCanvas() {
  const [c, ctx] = makeCanvas(512, 512);
  ctx.fillStyle = '#2b1a11'; ctx.fillRect(0, 0, 512, 512);
  for (let y = 0; y < 512; y++) {
    const v = Math.sin(y * 0.08) * 15 + Math.sin(y * 0.22) * 8;
    ctx.fillStyle = `rgba(60, 36, 20, ${0.15 + (Math.sin(y * 0.45) * 0.5 + 0.5) * 0.2})`;
    ctx.fillRect(0, y, 512, 1);
  }
  // Wood grain veins
  for (let i = 0; i < 40; i++) {
    const gy = Math.random() * 512;
    ctx.strokeStyle = 'rgba(18, 10, 6, 0.25)'; ctx.lineWidth = 1 + Math.random() * 2;
    ctx.beginPath(); ctx.moveTo(0, gy);
    ctx.bezierCurveTo(170, gy + (Math.random() - 0.5) * 20, 340, gy + (Math.random() - 0.5) * 20, 512, gy);
    ctx.stroke();
  }
  return c;
}

function makeRotaryDialCanvas() {
  const [c, ctx] = makeCanvas(512, 512);
  ctx.fillStyle = '#181714'; ctx.fillRect(0, 0, 512, 512);
  ctx.beginPath(); ctx.arc(256, 256, 238, 0, Math.PI * 2);
  ctx.fillStyle = '#f6f1e2'; ctx.fill();
  ctx.lineWidth = 16; ctx.strokeStyle = '#c49735'; ctx.stroke();
  ctx.fillStyle = '#111'; ctx.font = `bold 40px ${SANS}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  const nums = ['1','2','3','4','5','6','7','8','9','0'];
  for (let i = 0; i < 10; i++) {
    const angle = 0.62 + (i * 0.42);
    const r = 162;
    const x = 256 + Math.cos(angle) * r;
    const y = 256 + Math.sin(angle) * r;
    ctx.beginPath(); ctx.arc(x, y, 27, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(255,255,255,0.78)'; ctx.fill();
    ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(0,0,0,0.25)'; ctx.stroke();
    ctx.fillStyle = '#151515'; ctx.fillText(nums[i], x, y);
  }
  ctx.beginPath(); ctx.arc(256, 256, 68, 0, Math.PI * 2);
  ctx.fillStyle = '#c49735'; ctx.fill();
  ctx.lineWidth = 6; ctx.strokeStyle = '#e6af2e'; ctx.stroke();
  return c;
}

function makeCardFrontCanvas() {
  const [c, ctx] = makeCanvas(768, 480);
  ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, 768, 480);
  ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 6; ctx.strokeRect(16, 16, 736, 448);
  ctx.lineWidth = 2; ctx.strokeRect(26, 26, 716, 428);
  ctx.fillStyle = '#e6af2e'; ctx.font = `600 24px ${SANS}`;
  spacedText(ctx, 'CURATORIAL DOSSIER · NO. 01', 384, 90, 5);
  ctx.fillStyle = '#fbfffe'; ctx.font = `600 72px ${SERIF}`;
  spacedText(ctx, 'EUNOIA', 384, 185, 12);
  ctx.fillStyle = '#e6af2e'; ctx.font = `italic 24px ${SERIF}`; ctx.textAlign = 'center';
  ctx.fillText('A Museum of Animation & Visual Art', 384, 235);
  ctx.fillStyle = '#dbe4e2'; ctx.font = `500 20px ${SANS}`;
  ctx.fillText('Mangilaya · 2D Animator & 3D Generalist', 384, 340);
  ctx.fillStyle = '#8b9c9a'; ctx.font = `400 16px ${SANS}`;
  ctx.fillText('hello@eunoia.studio', 384, 385);
  return c;
}

function makeCardBackCanvas() {
  const [c, ctx] = makeCanvas(768, 480);
  ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, 768, 480);
  ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 4; ctx.strokeRect(16, 16, 736, 448);
  ctx.fillStyle = '#e6af2e'; ctx.font = `600 20px ${SANS}`;
  spacedText(ctx, 'MANGILAYA · ATELIER', 384, 70, 4);
  ctx.fillStyle = '#dbe4e2'; ctx.font = `400 17px ${SANS}`; ctx.textAlign = 'center';
  ctx.fillText('• 2D Keyframe Animation & Character Design', 384, 140);
  ctx.fillText('• 3D Environment Design & ArchViz (Blender)', 384, 180);
  ctx.fillText('• VFX Simulation & Cinematic Direction', 384, 220);
  ctx.fillText('• Observational Street & Lunar Photography', 384, 260);
  ctx.fillStyle = '#fbfffe'; ctx.font = `italic 18px ${SERIF}`;
  ctx.fillText('"Beautiful thinking, made visible."', 384, 340);
  ctx.fillStyle = '#e6af2e'; ctx.font = `600 16px ${SANS}`;
  ctx.fillText('Available for Creative Collaborations & Roles', 384, 395);
  return c;
}

function buildConciergeStand(root) {
  const standG = new THREE.Group();
  standG.position.set(2.4, 0, -2.6);
  standG.rotation.y = -Math.PI * 0.28; // Angled gracefully toward rotunda entrance

  // Textures with graceful procedural fallbacks
  const assets = EUNOIA_CONFIG.site.conciergeAssets || {};
  const T_WALNUT = managedTexture(makeWalnutCanvas(), assets.walnutWood, { repeat: true });
  T_WALNUT.repeat.set(2, 2);
  const T_ROTARY = managedTexture(makeRotaryDialCanvas(), assets.rotaryDial);
  const T_CARD_FRONT = managedTexture(makeCardFrontCanvas(), assets.cardFront);
  const T_CARD_BACK = managedTexture(makeCardBackCanvas(), assets.cardBack);

  const matWalnut = new THREE.MeshStandardMaterial({
    map: T_WALNUT,
    roughness: 0.32,
    metalness: 0.04
  });

  // 1. Walnut Pedestal Table (Square top, fluted/chamfered post, stepped plinth, console bracket feet)
  const plinthBottom = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.05, 0.72), matWalnut);
  plinthBottom.position.y = 0.025;
  const plinthStep = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.04, 0.62), matWalnut);
  plinthStep.position.y = 0.07;
  const plinthTop = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.03, 0.52), matWalnut);
  plinthTop.position.y = 0.105;
  standG.add(plinthBottom, plinthStep, plinthTop);

  // 4 Decorative console bracket feet at corners
  for (let i = 0; i < 4; i++) {
    const ang = (i * Math.PI) / 2 + Math.PI / 4;
    const foot = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.14, 0.22), matWalnut);
    foot.position.set(Math.cos(ang) * 0.28, 0.08, Math.sin(ang) * 0.28);
    foot.rotation.y = -ang;
    standG.add(foot);
  }

  // Central square shaft / post
  const postH = 0.74;
  const post = new THREE.Mesh(new THREE.BoxGeometry(0.16, postH, 0.16), matWalnut);
  post.position.y = 0.12 + postH / 2;
  standG.add(post);

  // 4 corner fluting / accent beading on post
  for (let i = 0; i < 4; i++) {
    const ang = (i * Math.PI) / 2 + Math.PI / 4;
    const bead = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.016, postH - 0.04, 8), matWalnut);
    bead.position.set(Math.cos(ang) * 0.10, 0.49, Math.sin(ang) * 0.10);
    standG.add(bead);
  }

  // Capital collar below tabletop
  const collar = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.04, 0.32), matWalnut);
  collar.position.y = 0.12 + postH + 0.02;
  const subTop = new THREE.Mesh(new THREE.BoxGeometry(0.76, 0.03, 0.76), matWalnut);
  subTop.position.y = 0.915;
  const topMesh = new THREE.Mesh(new THREE.BoxGeometry(0.86, 0.045, 0.86), matWalnut);
  topMesh.position.y = 0.9525;
  standG.add(collar, subTop, topMesh);

  // Floor contact shadow under table
  const shadowPlane = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 1.2), DROP_SHADOW_MAT);
  shadowPlane.rotation.x = -Math.PI / 2;
  shadowPlane.position.set(0.02, 0.005, 0.02);
  standG.add(shadowPlane);

  // Tabletop warm pin-spotlight pool
  const [glowC, glowCtx] = makeCanvas(256, 256);
  const grad = glowCtx.createRadialGradient(128, 128, 10, 128, 128, 120);
  grad.addColorStop(0, 'rgba(255, 238, 205, 0.65)');
  grad.addColorStop(0.5, 'rgba(255, 220, 170, 0.30)');
  grad.addColorStop(1, 'rgba(255, 200, 140, 0)');
  glowCtx.fillStyle = grad; glowCtx.fillRect(0, 0, 256, 256);
  const tableGlowTex = new THREE.CanvasTexture(glowC);
  const tableLightPool = new THREE.Mesh(
    new THREE.PlaneGeometry(0.80, 0.80),
    new THREE.MeshBasicMaterial({ map: tableGlowTex, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false })
  );
  tableLightPool.rotation.x = -Math.PI / 2;
  tableLightPool.position.set(0, 0.976, 0);
  standG.add(tableLightPool);

  // Floor warm spot pool
  const floorLightPool = new THREE.Mesh(
    new THREE.PlaneGeometry(1.8, 1.8),
    new THREE.MeshBasicMaterial({ map: tableGlowTex, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false })
  );
  floorLightPool.rotation.x = -Math.PI / 2;
  floorLightPool.position.set(0, 0.006, 0);
  standG.add(floorLightPool);

  // Overhead track light rail & spotlight can above the stand
  const canRail = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.04, 0.08), Mat.trackRail);
  canRail.position.set(0, H_ROT - 0.10, 0);
  const canCyl = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.065, 0.24, 12), Mat.trackCylinder);
  canCyl.position.set(0, H_ROT - 0.22, 0);
  canCyl.rotation.x = 0.18;
  const canLens = new THREE.Mesh(new THREE.CircleGeometry(0.055, 12), Mat.trackLens);
  canLens.position.set(0, H_ROT - 0.34, 0.02);
  canLens.rotation.x = Math.PI / 2 + 0.18;
  standG.add(canRail, canCyl, canLens);

  // Add physical collider for stand
  addBoxCollider(2.4, -2.6, 0.44, 0.44);

  // --------------------------------------------------------------------------
  // 2. Vintage Glossy Red Rotary Telephone (Table Left: x = -0.19, z = 0.02)
  // --------------------------------------------------------------------------
  const phoneG = new THREE.Group();
  phoneG.position.set(-0.19, 0.975, 0.02);

  const matRedPhone = new THREE.MeshStandardMaterial({
    color: 0xba1212,
    roughness: 0.18,
    metalness: 0.08
  });
  const matBlackPlastic = new THREE.MeshStandardMaterial({
    color: 0x151515,
    roughness: 0.3,
    metalness: 0.1
  });
  const matChrome = new THREE.MeshStandardMaterial({
    color: 0xe0e0e0,
    roughness: 0.15,
    metalness: 0.92
  });

  const phoneBase = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.06, 0.18), matRedPhone);
  phoneBase.position.y = 0.03;
  const phoneBodyUpper = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.045, 0.14), matRedPhone);
  phoneBodyUpper.position.set(0, 0.075, -0.01);
  phoneBodyUpper.rotation.x = -0.12;

  const dialMount = new THREE.Mesh(new THREE.CylinderGeometry(0.062, 0.065, 0.015, 24), matRedPhone);
  dialMount.position.set(0, 0.072, 0.032);
  dialMount.rotation.x = Math.PI / 4;

  const dialFaceMat = new THREE.MeshBasicMaterial({ map: T_ROTARY });
  const dialFace = new THREE.Mesh(new THREE.CircleGeometry(0.058, 24), dialFaceMat);
  dialFace.position.set(0, 0.08, 0.04);
  dialFace.rotation.x = -Math.PI / 4;

  const dialHub = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.016, 0.008, 16), Mat.goldLeaf);
  dialHub.position.set(0, 0.082, 0.042);
  dialHub.rotation.x = -Math.PI / 4;

  const fingerStop = new THREE.Mesh(new THREE.BoxGeometry(0.008, 0.014, 0.004), matChrome);
  fingerStop.position.set(0.036, 0.056, 0.066);
  fingerStop.rotation.z = -0.6;

  const cradleL = new THREE.Mesh(new THREE.BoxGeometry(0.024, 0.022, 0.03), matChrome);
  cradleL.position.set(-0.055, 0.11, -0.03);
  const cradleR = new THREE.Mesh(new THREE.BoxGeometry(0.024, 0.022, 0.03), matChrome);
  cradleR.position.set(0.055, 0.11, -0.03);

  const handsetG = new THREE.Group();
  handsetG.position.set(0, 0.125, -0.03);
  const grip = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.15, 12), matRedPhone);
  grip.rotation.z = Math.PI / 2;
  const earCup = new THREE.Mesh(new THREE.CylinderGeometry(0.034, 0.028, 0.035, 16), matRedPhone);
  earCup.position.set(-0.09, -0.006, 0); earCup.rotation.z = 0.2;
  const mouthCup = new THREE.Mesh(new THREE.CylinderGeometry(0.034, 0.028, 0.035, 16), matRedPhone);
  mouthCup.position.set(0.09, -0.006, 0); mouthCup.rotation.z = -0.2;
  const earCap = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.008, 16), matBlackPlastic);
  earCap.position.set(-0.104, -0.018, 0); earCap.rotation.z = 0.2;
  const mouthCap = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.008, 16), matBlackPlastic);
  mouthCap.position.set(0.104, -0.018, 0); mouthCap.rotation.z = -0.2;
  handsetG.add(grip, earCup, mouthCup, earCap, mouthCap);
  handsetG.rotation.y = 0.08;

  const cordG = new THREE.Group();
  for (let c = 0; c < 10; c++) {
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.012, 0.0035, 8, 12), matBlackPlastic);
    ring.position.set(-0.08 - c * 0.006, 0.07 - c * 0.005, -0.04 - Math.sin(c * 0.6) * 0.015);
    ring.rotation.x = Math.PI / 2 + c * 0.2;
    cordG.add(ring);
  }

  const phonePlqTex = textTexture(512, 128, (ctx, w, h) => {
    ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 3; ctx.strokeRect(4, 4, w - 8, h - 8);
    ctx.fillStyle = '#e6af2e'; ctx.font = `600 18px ${SANS}`;
    spacedText(ctx, "CURATOR'S DIRECT LINE", w / 2, 42, 3);
    ctx.fillStyle = '#fbfffe'; ctx.font = `italic 20px ${SERIF}`; ctx.textAlign = 'center';
    ctx.fillText('Click to Ring / Transmit Dispatch', w / 2, 85);
  });
  const phonePlaque = new THREE.Mesh(
    new THREE.PlaneGeometry(0.18, 0.05),
    new THREE.MeshBasicMaterial({ map: phonePlqTex })
  );
  phonePlaque.rotation.x = -Math.PI / 3;
  phonePlaque.position.set(0, 0.015, 0.12);

  phoneG.add(phoneBase, phoneBodyUpper, dialMount, dialFace, dialHub, fingerStop, cradleL, cradleR, handsetG, cordG, phonePlaque);
  phoneG.rotation.y = 0.22;
  standG.add(phoneG);

  // Invisible proxy box for raycasting on the phone
  const phoneHitProxy = new THREE.Mesh(
    new THREE.BoxGeometry(0.28, 0.26, 0.28),
    new THREE.MeshBasicMaterial({ visible: false })
  );
  phoneHitProxy.position.set(0, 0.12, 0);
  phoneHitProxy.userData = { isPhone: true, group: standG };
  phoneG.add(phoneHitProxy);
  interactivePropMeshes.push(phoneHitProxy);

  // --------------------------------------------------------------------------
  // 3. Brass Display Easel & 3D Dossier Card (Table Right: x = +0.19, z = 0.0)
  // --------------------------------------------------------------------------
  const easelG = new THREE.Group();
  easelG.position.set(0.19, 0.975, 0.0);

  const matBrassEasel = new THREE.MeshStandardMaterial({
    color: 0xe6af2e,
    roughness: 0.22,
    metalness: 0.88
  });

  const legGeo = new THREE.CylinderGeometry(0.005, 0.005, 0.28, 8);
  const legL = new THREE.Mesh(legGeo, matBrassEasel);
  legL.position.set(-0.08, 0.13, -0.02); legL.rotation.z = -0.16;
  const legR = new THREE.Mesh(legGeo, matBrassEasel);
  legR.position.set(0.08, 0.13, -0.02); legR.rotation.z = 0.16;
  const legBack = new THREE.Mesh(legGeo, matBrassEasel);
  legBack.position.set(0, 0.13, -0.09); legBack.rotation.x = -0.38;

  const restBar = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.008, 0.015), matBrassEasel);
  restBar.position.set(0, 0.06, 0.01);
  const restLip = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.014, 0.005), matBrassEasel);
  restLip.position.set(0, 0.068, 0.016);

  easelG.add(legL, legR, legBack, restBar, restLip);

  const cardG = new THREE.Group();
  cardG.position.set(0, 0.135, 0.01);
  cardG.rotation.x = -0.22;

  const cardFrontMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(0.24, 0.15),
    new THREE.MeshStandardMaterial({ map: T_CARD_FRONT, roughness: 0.35, metalness: 0.08 })
  );
  cardFrontMesh.position.z = 0.0012;

  const cardBackMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(0.24, 0.15),
    new THREE.MeshStandardMaterial({ map: T_CARD_BACK, roughness: 0.35, metalness: 0.08 })
  );
  cardBackMesh.rotation.y = Math.PI;
  cardBackMesh.position.z = -0.0012;

  const cardRim = new THREE.Mesh(
    new THREE.BoxGeometry(0.241, 0.151, 0.002),
    Mat.goldLeaf
  );

  cardG.add(cardFrontMesh, cardBackMesh, cardRim);

  const cardPlqTex = textTexture(512, 128, (ctx, w, h) => {
    ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 3; ctx.strokeRect(4, 4, w - 8, h - 8);
    ctx.fillStyle = '#e6af2e'; ctx.font = `600 18px ${SANS}`;
    spacedText(ctx, "CURATOR'S DOSSIER", w / 2, 42, 3);
    ctx.fillStyle = '#fbfffe'; ctx.font = `italic 20px ${SERIF}`; ctx.textAlign = 'center';
    ctx.fillText('Click to Inspect & Flip 3D Card', w / 2, 85);
  });
  const cardPlaque = new THREE.Mesh(
    new THREE.PlaneGeometry(0.18, 0.05),
    new THREE.MeshBasicMaterial({ map: cardPlqTex })
  );
  cardPlaque.rotation.x = -Math.PI / 3;
  cardPlaque.position.set(0, 0.015, 0.12);

  easelG.add(cardG, cardPlaque);
  easelG.rotation.y = -0.22;
  standG.add(easelG);

  // Invisible proxy box for card clicking
  const cardHitProxy = new THREE.Mesh(
    new THREE.BoxGeometry(0.26, 0.24, 0.22),
    new THREE.MeshBasicMaterial({ visible: false })
  );
  cardHitProxy.position.set(0, 0.13, 0);
  cardHitProxy.userData = { isCard: true, group: standG };
  easelG.add(cardHitProxy);
  interactivePropMeshes.push(cardHitProxy);

  root.add(standG);
}
'''

# We place buildConciergeStand right above function buildArchitecture
arch_anchor = 'function buildArchitecture() {'
if arch_anchor in text_norm:
    text_norm = text_norm.replace(arch_anchor, concierge_stand_code + '\n' + arch_anchor, 1)
    print("2. Added buildConciergeStand function.")
else:
    print("ERROR: arch_anchor not found")

# 3. Call buildConciergeStand(root) inside buildArchitecture
dir_anchor = '  root.add(dirShadow, dirCone);'
new_dir_call = '''  root.add(dirShadow, dirCone);

  // Curator's Concierge Stand (Pedestal table, Rotary Phone, 3D Dossier Card)
  buildConciergeStand(root);'''

if dir_anchor in text_norm:
    text_norm = text_norm.replace(dir_anchor, new_dir_call, 1)
    print("3. Called buildConciergeStand(root).")
else:
    print("ERROR: dir_anchor not found")

# 4. Update updateRaycast and mousedown
old_raycast_block = '''  // Spatial filter: visible wing + within 7 m  (185 meshes -> ~2-4)
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

// Click to inspect
window.addEventListener('mousedown', (e) => {
  if (e.button === 0 && isControlsLocked && hoveredExhibitMesh && !isInspecting) {
    inspectExhibit(hoveredExhibitMesh.userData.exhibit, hoveredExhibitMesh);
  }
});'''

new_raycast_block = '''  // Spatial filter: visible wing + within 7 m  (185 meshes -> ~2-4)
  _rayCandidates.length = 0;
  const cp = camera.position;
  for (let i = 0; i < exhibitMeshes.length; i++) {
    const m = exhibitMeshes[i];
    const g = m.userData.group;
    if (!g.visible || !g.parent || !g.parent.visible) continue;
    if (g.position.distanceToSquared(cp) < 49.0) _rayCandidates.push(m);
  }
  for (let i = 0; i < interactivePropMeshes.length; i++) {
    const pm = interactivePropMeshes[i];
    const pg = pm.userData.group;
    if (pg && (!pg.visible || !pg.parent || !pg.parent.visible)) continue;
    if (pm.getWorldPosition(_tmpVec).distanceToSquared(cp) < 49.0) {
      _rayCandidates.push(pm);
    }
  }

  raycaster.setFromCamera(screenCenter, camera);
  raycaster.far = 6.5;
  const intersects = raycaster.intersectObjects(_rayCandidates, false);

  if (intersects.length > 0) {
    const hit = intersects[0].object;
    hoveredExhibitMesh = hit;
    $('reticle').classList.add('active');
    $('prompt').classList.add('show');
    if (hit.userData.isPhone) {
      $('promptTitle').textContent = "Curator's Rotary Phone [Ring Line]";
    } else if (hit.userData.isCard) {
      $('promptTitle').textContent = "Curator's Dossier [Inspect & Flip]";
    } else {
      const exhibit = hit.userData.exhibit;
      $('promptTitle').textContent = exhibit ? (exhibit.title || exhibit.category || '') : '';
    }
  } else {
    $('reticle').classList.remove('active');
    $('prompt').classList.remove('show');
    hoveredExhibitMesh = null;
  }
}

// Click to inspect exhibit or interact with concierge props
window.addEventListener('mousedown', (e) => {
  if (e.button === 0 && isControlsLocked && hoveredExhibitMesh && !isInspecting) {
    if (hoveredExhibitMesh.userData.isPhone) {
      openPhoneModal();
    } else if (hoveredExhibitMesh.userData.isCard) {
      openCardModal();
    } else if (hoveredExhibitMesh.userData.exhibit) {
      inspectExhibit(hoveredExhibitMesh.userData.exhibit, hoveredExhibitMesh);
    }
  }
});'''

if old_raycast_block in text_norm:
    text_norm = text_norm.replace(old_raycast_block, new_raycast_block, 1)
    print("4. Updated raycasting and mousedown interaction.")
else:
    print("ERROR: old_raycast_block not found")

# 5. Add vector helper for _tmpVec if not present
if 'const _tmpVec = new THREE.Vector3();' not in text_norm:
    old_ray_time = 'let lastRaycastTime = 0;'
    new_ray_time = 'const _tmpVec = new THREE.Vector3();\nlet lastRaycastTime = 0;'
    text_norm = text_norm.replace(old_ray_time, new_ray_time, 1)
    print("5. Added _tmpVec helper.")

# 6. Add modal states to updateRaycast guard
old_guard = 'if (!isControlsLocked || isInspecting || isCatalogOpen) {'
new_guard = 'if (!isControlsLocked || isInspecting || isCatalogOpen || isPhoneModalOpen || isCardModalOpen) {'
if old_guard in text_norm:
    text_norm = text_norm.replace(old_guard, new_guard, 1)
    print("6. Updated updateRaycast modal guard.")
else:
    print("ERROR: old_guard not found")

# 7. Update Escape key handler
old_esc = '''  if (e.code === 'Escape') {
    if (isCatalogOpen) {
      toggleCatalog(false);
    } else if (isInspecting) {
      exitInspection();
    } else if (!isLobbyActive) {
      openLobby();
    }
  }'''

new_esc = '''  if (e.code === 'Escape') {
    if (isPhoneModalOpen) {
      closePhoneModal();
    } else if (isCardModalOpen) {
      closeCardModal();
    } else if (isCatalogOpen) {
      toggleCatalog(false);
    } else if (isInspecting) {
      exitInspection();
    } else if (!isLobbyActive) {
      openLobby();
    }
  }'''

if old_esc in text_norm:
    text_norm = text_norm.replace(old_esc, new_esc, 1)
    print("7. Updated Escape key handler.")
else:
    print("ERROR: old_esc not found")

# 8. Add modal logic handlers (Formspree dispatch and 3D card drag-to-flip)
modal_logic_code = '''
/* --------------------------------------------------------------------------
   4.16  CONCIERGE MODALS: ROTARY PHONE DISPATCH & 3D GYROSCOPIC CARD
   -------------------------------------------------------------------------- */
let isPhoneModalOpen = false;
let isCardModalOpen = false;

function openPhoneModal() {
  if (isControlsLocked) controls.unlock();
  isPhoneModalOpen = true;
  const m = $('phoneModal');
  if (m) {
    m.classList.add('open');
    m.setAttribute('aria-hidden', 'false');
    const input = $('phoneInputName');
    if (input) setTimeout(() => input.focus(), 120);
  }
}

function closePhoneModal() {
  isPhoneModalOpen = false;
  const m = $('phoneModal');
  if (m) {
    m.classList.remove('open');
    m.setAttribute('aria-hidden', 'true');
  }
}

function openCardModal() {
  if (isControlsLocked) controls.unlock();
  isCardModalOpen = true;
  const m = $('cardModal');
  if (m) {
    m.classList.add('open');
    m.setAttribute('aria-hidden', 'false');
  }
  const assets = EUNOIA_CONFIG.site.conciergeAssets || {};
  const frontEl = $('dossierFaceFront');
  const backEl = $('dossierFaceBack');
  if (frontEl && assets.cardFront) frontEl.style.backgroundImage = `url("${assets.cardFront}")`;
  if (backEl && assets.cardBack) backEl.style.backgroundImage = `url("${assets.cardBack}")`;
  cardRotX = 0; cardRotY = 0; isCardFlipped = false;
  updateCardTransform();
}

function closeCardModal() {
  isCardModalOpen = false;
  const m = $('cardModal');
  if (m) {
    m.classList.remove('open');
    m.setAttribute('aria-hidden', 'true');
  }
}

// 3D Card Gyroscopic Drag & Flip Interaction
let cardRotX = 0, cardRotY = 0;
let isCardFlipped = false;
let isDraggingCard = false;
let startCardX = 0, startCardY = 0;
let baseCardRotX = 0, baseCardRotY = 0;

function updateCardTransform() {
  const card = $('dossier3dCard');
  if (!card) return;
  const targetY = cardRotY + (isCardFlipped ? 180 : 0);
  card.style.transform = `rotateX(${cardRotX}deg) rotateY(${targetY}deg)`;
}

const cardContainer = $('dossierCardContainer');
if (cardContainer) {
  cardContainer.addEventListener('mousedown', (e) => {
    isDraggingCard = true;
    startCardX = e.clientX;
    startCardY = e.clientY;
    baseCardRotX = cardRotX;
    baseCardRotY = cardRotY;
  });
  window.addEventListener('mousemove', (e) => {
    if (!isDraggingCard) return;
    const dx = e.clientX - startCardX;
    const dy = e.clientY - startCardY;
    cardRotY = baseCardRotY + dx * 0.45;
    cardRotX = Math.max(-45, Math.min(45, baseCardRotX - dy * 0.35));
    updateCardTransform();
  });
  window.addEventListener('mouseup', () => {
    if (isDraggingCard) {
      isDraggingCard = false;
      cardRotX *= 0.4;
      updateCardTransform();
    }
  });

  // Touch support for mobile / tablets
  cardContainer.addEventListener('touchstart', (e) => {
    if (e.touches.length > 0) {
      isDraggingCard = true;
      startCardX = e.touches[0].clientX;
      startCardY = e.touches[0].clientY;
      baseCardRotX = cardRotX;
      baseCardRotY = cardRotY;
    }
  }, { passive: true });
  window.addEventListener('touchmove', (e) => {
    if (!isDraggingCard || !e.touches.length) return;
    const dx = e.touches[0].clientX - startCardX;
    const dy = e.touches[0].clientY - startCardY;
    cardRotY = baseCardRotY + dx * 0.45;
    cardRotX = Math.max(-45, Math.min(45, baseCardRotX - dy * 0.35));
    updateCardTransform();
  }, { passive: true });
  window.addEventListener('touchend', () => {
    isDraggingCard = false;
  });

  // Manual Flip Button
  $('btnFlipCardManual')?.addEventListener('click', () => {
    isCardFlipped = !isCardFlipped;
    updateCardTransform();
  });

  // Ring Rotary Phone from inside Card Modal
  $('btnDossierCall')?.addEventListener('click', () => {
    closeCardModal();
    setTimeout(openPhoneModal, 150);
  });

  $('btnCloseCard')?.addEventListener('click', closeCardModal);
  $('cardModal')?.addEventListener('click', (e) => {
    if (e.target === $('cardModal')) closeCardModal();
  });
}

// Live Formspree API Integration for Rotary Telephone
const phoneForm = $('phoneContactForm');
if (phoneForm) {
  phoneForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = $('phoneSubmitBtn');
    const statusMsg = $('phoneStatusMsg');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Transmitting via Rotary Line…';
    }
    if (statusMsg) {
      statusMsg.className = 'phone-status-msg';
      statusMsg.textContent = '';
    }

    const endpoint = EUNOIA_CONFIG.site.formspreeEndpoint || 'https://formspree.io/f/mrpeqnle';
    const payload = {
      name: $('phoneInputName')?.value || '',
      _replyto: $('phoneInputEmail')?.value || '',
      subject: $('phoneInputSubject')?.value || '',
      message: $('phoneInputMessage')?.value || ''
    };

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        if (statusMsg) {
          statusMsg.classList.add('success');
          statusMsg.textContent = '✓ Transmitted! Curator Mangilaya alerted. Expect a response soon.';
        }
        phoneForm.reset();
        if (submitBtn) submitBtn.textContent = 'Dispatched Successfully';
        setTimeout(() => {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Transmit via Rotary Dispatch';
          }
        }, 4000);
      } else {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || 'Server rejected transmission.');
      }
    } catch (err) {
      if (statusMsg) {
        statusMsg.classList.add('error');
        statusMsg.textContent = '⚠ Dispatch Failed: ' + (err.message || 'Network error') + '. Please try again or email hello@eunoia.studio';
      }
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Retry Rotary Dispatch';
      }
    }
  });
}

$('btnClosePhone')?.addEventListener('click', closePhoneModal);
$('phoneModal')?.addEventListener('click', (e) => {
  if (e.target === $('phoneModal')) closePhoneModal();
});
'''

# Place modal logic before window.updateCurrentWingCaption or at the end of the script
script_end_anchor = 'window.updateCurrentWingCaption = updateCurrentWingCaption;'
if script_end_anchor in text_norm:
    text_norm = text_norm.replace(script_end_anchor, modal_logic_code + '\n' + script_end_anchor, 1)
    print("8. Added modal logic handlers.")
else:
    print("ERROR: script_end_anchor not found")

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text_norm)

print("Concierge stand implementation completed successfully!")

