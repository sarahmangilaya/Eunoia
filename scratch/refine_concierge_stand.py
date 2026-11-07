import re

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text_norm = text.replace('\r\n', '\n')

# 1. Replace buildConciergeStand with refined geometry and correct orientation
pattern_stand = re.compile(r'/\* -+ \s*4\.9\.5 CURATOR\'S CONCIERGE STAND.*?\n}\n', re.DOTALL)

refined_stand = '''/* --------------------------------------------------------------------------
   4.9.5  CURATOR'S CONCIERGE STAND (WALNUT PEDESTAL, ROTARY PHONE & 3D CARD)
   -------------------------------------------------------------------------- */
function makeWalnutCanvas() {
  const [c, ctx] = makeCanvas(512, 512);
  ctx.fillStyle = '#26160e'; ctx.fillRect(0, 0, 512, 512);
  for (let y = 0; y < 512; y++) {
    const v = Math.sin(y * 0.07) * 16 + Math.sin(y * 0.24) * 8;
    ctx.fillStyle = `rgba(58, 34, 20, ${0.18 + (Math.sin(y * 0.4) * 0.5 + 0.5) * 0.22})`;
    ctx.fillRect(0, y, 512, 1);
  }
  for (let i = 0; i < 45; i++) {
    const gy = Math.random() * 512;
    ctx.strokeStyle = 'rgba(15, 8, 4, 0.28)'; ctx.lineWidth = 1 + Math.random() * 2;
    ctx.beginPath(); ctx.moveTo(0, gy);
    ctx.bezierCurveTo(170, gy + (Math.random() - 0.5) * 18, 340, gy + (Math.random() - 0.5) * 18, 512, gy);
    ctx.stroke();
  }
  return c;
}

function makeRotaryDialCanvas() {
  const [c, ctx] = makeCanvas(512, 512);
  ctx.fillStyle = '#141412'; ctx.fillRect(0, 0, 512, 512);
  ctx.beginPath(); ctx.arc(256, 256, 238, 0, Math.PI * 2);
  ctx.fillStyle = '#f8f4e6'; ctx.fill();
  ctx.lineWidth = 16; ctx.strokeStyle = '#c49735'; ctx.stroke();
  ctx.fillStyle = '#111'; ctx.font = `bold 42px ${SANS}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  const nums = ['1','2','3','4','5','6','7','8','9','0'];
  for (let i = 0; i < 10; i++) {
    const angle = 0.60 + (i * 0.42);
    const r = 164;
    const x = 256 + Math.cos(angle) * r;
    const y = 256 + Math.sin(angle) * r;
    ctx.beginPath(); ctx.arc(x, y, 28, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(255,255,255,0.85)'; ctx.fill();
    ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(0,0,0,0.25)'; ctx.stroke();
    ctx.fillStyle = '#151515'; ctx.fillText(nums[i], x, y);
  }
  ctx.beginPath(); ctx.arc(256, 256, 70, 0, Math.PI * 2);
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
  // Orient table so local +Z faces visitor arriving from entrance at (0, -4.5)
  standG.rotation.y = Math.PI - 0.42;

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
  grad.addColorStop(0, 'rgba(255, 238, 205, 0.70)');
  grad.addColorStop(0.5, 'rgba(255, 220, 170, 0.32)');
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
  // 2. Vintage Glossy Red Rotary Telephone (Table Left: x = -0.20, z = -0.02)
  // --------------------------------------------------------------------------
  const phoneG = new THREE.Group();
  phoneG.position.set(-0.20, 0.975, -0.02);

  const matRedPhone = new THREE.MeshStandardMaterial({
    color: 0xcc1414,
    roughness: 0.14,
    metalness: 0.04
  });
  const matBlackPlastic = new THREE.MeshStandardMaterial({
    color: 0x151515,
    roughness: 0.28,
    metalness: 0.1
  });
  const matChrome = new THREE.MeshStandardMaterial({
    color: 0xeeeeee,
    roughness: 0.15,
    metalness: 0.95
  });

  // Base housing: classic trapezoidal pyramidal rounded shape
  const phoneBase = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.04, 0.18), matRedPhone);
  phoneBase.position.y = 0.02;
  const phoneBodyMid = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.035, 0.16), matRedPhone);
  phoneBodyMid.position.set(0, 0.055, -0.005);
  const phoneBodyUpper = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.04, 0.13), matRedPhone);
  phoneBodyUpper.position.set(0, 0.08, -0.012);
  phoneBodyUpper.rotation.x = -0.16;

  // Front slanted face dial mount
  const dialMount = new THREE.Mesh(new THREE.CylinderGeometry(0.062, 0.065, 0.015, 24), matRedPhone);
  dialMount.position.set(0, 0.076, 0.034);
  dialMount.rotation.x = Math.PI / 3.8;

  // Rotary Dial Face with loaded texture
  const dialFaceMat = new THREE.MeshBasicMaterial({ map: T_ROTARY });
  const dialFace = new THREE.Mesh(new THREE.CircleGeometry(0.058, 24), dialFaceMat);
  dialFace.position.set(0, 0.084, 0.042);
  dialFace.rotation.x = -Math.PI / 3.8;

  // Acrylic finger wheel & Gold central hub
  const fingerWheel = new THREE.Mesh(
    new THREE.CylinderGeometry(0.058, 0.058, 0.004, 24),
    new THREE.MeshStandardMaterial({ color: 0xffffff, transparent: true, opacity: 0.4, roughness: 0.1 })
  );
  fingerWheel.position.set(0, 0.086, 0.044);
  fingerWheel.rotation.x = -Math.PI / 3.8;

  const dialHub = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.016, 0.008, 16), Mat.goldLeaf);
  dialHub.position.set(0, 0.089, 0.047);
  dialHub.rotation.x = -Math.PI / 3.8;

  const fingerStop = new THREE.Mesh(new THREE.BoxGeometry(0.006, 0.016, 0.004), matChrome);
  fingerStop.position.set(0.038, 0.058, 0.068);
  fingerStop.rotation.z = -0.6;

  // Handset cradle horns / prongs
  const cradleL = new THREE.Mesh(new THREE.BoxGeometry(0.024, 0.026, 0.028), matChrome);
  cradleL.position.set(-0.055, 0.115, -0.035);
  const cradleR = new THREE.Mesh(new THREE.BoxGeometry(0.024, 0.026, 0.028), matChrome);
  cradleR.position.set(0.055, 0.115, -0.035);

  // Red Handset resting horizontally across the cradle
  const handsetG = new THREE.Group();
  handsetG.position.set(0, 0.13, -0.035);
  const grip = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.15, 12), matRedPhone);
  grip.rotation.z = Math.PI / 2;
  const earCup = new THREE.Mesh(new THREE.CylinderGeometry(0.034, 0.026, 0.035, 16), matRedPhone);
  earCup.position.set(-0.09, -0.006, 0); earCup.rotation.z = 0.22;
  const mouthCup = new THREE.Mesh(new THREE.CylinderGeometry(0.034, 0.026, 0.035, 16), matRedPhone);
  mouthCup.position.set(0.09, -0.006, 0); mouthCup.rotation.z = -0.22;
  const earCap = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.008, 16), matBlackPlastic);
  earCap.position.set(-0.104, -0.018, 0); earCap.rotation.z = 0.22;
  const mouthCap = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.008, 16), matBlackPlastic);
  mouthCap.position.set(0.104, -0.018, 0); mouthCap.rotation.z = -0.22;
  handsetG.add(grip, earCup, mouthCup, earCap, mouthCap);
  handsetG.rotation.y = 0.06;

  // Coiled black telephone cord
  const cordG = new THREE.Group();
  for (let c = 0; c < 12; c++) {
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.011, 0.0032, 8, 12), matBlackPlastic);
    ring.position.set(-0.075 - c * 0.006, 0.07 - c * 0.0045, -0.04 - Math.sin(c * 0.55) * 0.015);
    ring.rotation.x = Math.PI / 2 + c * 0.22;
    cordG.add(ring);
  }

  // Brass Plaque in front of phone
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
  phonePlaque.rotation.x = -Math.PI / 3.5;
  phonePlaque.position.set(0, 0.015, 0.12);

  phoneG.add(phoneBase, phoneBodyMid, phoneBodyUpper, dialMount, dialFace, fingerWheel, dialHub, fingerStop, cradleL, cradleR, handsetG, cordG, phonePlaque);
  phoneG.rotation.y = 0.18; // angled slightly toward visitor
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
  // 3. Brass Display Easel & 3D Dossier Card (Table Right: x = +0.19, z = -0.02)
  // --------------------------------------------------------------------------
  const easelG = new THREE.Group();
  easelG.position.set(0.19, 0.975, -0.02);

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
  cardPlaque.rotation.x = -Math.PI / 3.5;
  cardPlaque.position.set(0, 0.015, 0.12);

  easelG.add(cardG, cardPlaque);
  easelG.rotation.y = -0.18; // angled slightly toward visitor
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

# Replace in text_norm
# We'll use start and end markers
start_marker = "/* --------------------------------------------------------------------------\n   4.9.5  CURATOR'S CONCIERGE STAND"
end_marker = "function buildArchitecture() {"

if start_marker in text_norm and end_marker in text_norm:
    idx1 = text_norm.index(start_marker)
    idx2 = text_norm.index(end_marker)
    text_norm = text_norm[:idx1] + refined_stand + '\n' + text_norm[idx2:]
    print("Replaced buildConciergeStand with refined version.")
else:
    print("ERROR: markers not found")

# Expose openPhoneModal, closePhoneModal, openCardModal, closeCardModal, interactivePropMeshes on window
expose_anchor = 'window.updateCurrentWingCaption = updateCurrentWingCaption;'
expose_code = '''window.openPhoneModal = openPhoneModal;
window.closePhoneModal = closePhoneModal;
window.openCardModal = openCardModal;
window.closeCardModal = closeCardModal;
window.interactivePropMeshes = interactivePropMeshes;
window.updateCurrentWingCaption = updateCurrentWingCaption;'''

if expose_anchor in text_norm:
    text_norm = text_norm.replace(expose_anchor, expose_code, 1)
    print("Exposed concierge methods to window.")

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text_norm)

print("Saved updated index.html")

