with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace the entire Rotunda section in buildArchitecture with the original working Rotunda code + addSolidWall
start_arch = html.find('function buildArchitecture() {')
start_wing1 = html.find('/* --- 2.1 Wing I: The Classical & Fine Arts Wing', start_arch)
assert start_arch != -1 and start_wing1 != -1

new_rotunda_and_helpers = """function buildArchitecture() {
  const root = new THREE.Group();

  function addSolidWall(x1, z1, x2, z2, mat, targetGroup, yMin = 0, yMax = H_WING) {
    const dx = x2 - x1;
    const dz = z2 - z1;
    const len = Math.hypot(dx, dz);
    if (len < 0.001) return;
    const h = yMax - yMin;
    const midX = (x1 + x2) / 2;
    const midZ = (z1 + z2) / 2;
    const midY = (yMin + yMax) / 2;
    const angle = Math.atan2(dx, dz);

    const geo = new THREE.BoxGeometry(0.24, h, len);
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(midX, midY, midZ);
    mesh.rotation.y = angle;
    mesh.receiveShadow = true;
    mesh.castShadow = false;
    targetGroup.add(mesh);

    if (yMin < 1.0) {
      addWallSegment(x1, z1, x2, z2);
    }
    return mesh;
  }

  /* --- 1. Grand Rotunda --- */
  const rotFloor = new THREE.Mesh(new THREE.CylinderGeometry(R_ROT, R_ROT, 0.4, 48), Mat.floorRotunda);
  rotFloor.position.y = -0.2; rotFloor.receiveShadow = true; root.add(rotFloor);

  const rotCeil = new THREE.Mesh(new THREE.CylinderGeometry(R_ROT, R_ROT, 0.3, 48), Mat.ceilingRot);
  rotCeil.position.y = H_ROT + 0.15; root.add(rotCeil);

  // Rotunda walls: 16-sided polygon with openings into the 3 wings & entrance niche
  const segments = 16, dTheta = TAU / segments;
  for (let i = 0; i < segments; i++) {
    const a0 = i * dTheta, a1 = (i + 1) * dTheta, mid = (a0 + a1) / 2;
    // Wing openings: i=0 (East +X, Wing I), i=4 (North +Z, Wing II), i=8 (West -X, Wing III)
    const isWingI = (i === 0 || i === segments - 1);
    const isWingII = (i === 4 || i === 3);
    const isWingIII = (i === 8 || i === 7);
    if (isWingI || isWingII || isWingIII) {
      // Clear doorway opening into wings (portal archway provided cleanly by buildWallPortal)
      continue;
    }
    const chord = 2 * R_ROT * Math.sin(dTheta / 2);
    const wallSeg = new THREE.Mesh(new THREE.BoxGeometry(chord * 1.02, H_ROT, 0.4), Mat.wallRotunda);
    wallSeg.position.set(Math.cos(mid) * R_ROT, H_ROT / 2, Math.sin(mid) * R_ROT);
    wallSeg.rotation.y = -mid + Math.PI / 2;
    wallSeg.castShadow = true; wallSeg.receiveShadow = true; root.add(wallSeg);

    // Continuous line-segment collider for each solid rotunda wall
    const p1x = Math.cos(a0) * (R_ROT - 0.2), p1z = Math.sin(a0) * (R_ROT - 0.2);
    const p2x = Math.cos(a1) * (R_ROT - 0.2), p2z = Math.sin(a1) * (R_ROT - 0.2);
    addWallSegment(p1x, p1z, p2x, p2z);
  }

  // 8 peristyle fluted columns flanking portals and foyer
  const R_COLS = 5.8;
  const colAngles = [
    Math.PI / 6, 2 * Math.PI / 6,
    4 * Math.PI / 6, 5 * Math.PI / 6,
    7 * Math.PI / 6, 8 * Math.PI / 6,
    10 * Math.PI / 6, 11 * Math.PI / 6
  ];
  colAngles.forEach((a) => {
    const col = buildFlutedColumn(H_ROT, 0.38);
    const cx = Math.cos(a) * R_COLS, cz = Math.sin(a) * R_COLS;
    col.position.set(cx, 0, cz); root.add(col);
    addCylCollider(cx, cz, 0.55);
  });

  // Central sculpture pedestal + abstract classical sculpture
  const ped = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.3, 1.1, 32), Mat.pedestal);
  ped.position.set(0, 0.55, 0); ped.castShadow = true; ped.receiveShadow = true; root.add(ped);
  addCylCollider(0, 0, 1.28);

  const plinthTop = new THREE.Mesh(new THREE.CylinderGeometry(1.26, 1.26, 0.08, 32), Mat.goldLeaf);
  plinthTop.position.set(0, 1.14, 0); root.add(plinthTop);

  // Modernist alabaster / bronze torsion sculpture atop the pedestal
  const sculpG = new THREE.Group();
  sculpG.position.set(0, 1.18, 0);
  const ring1 = new THREE.Mesh(new THREE.TorusGeometry(0.7, 0.08, 16, 64), Mat.goldLeaf);
  ring1.position.y = 1.0; ring1.rotation.set(0.6, 0.4, 0); ring1.castShadow = true;
  const ring2 = new THREE.Mesh(new THREE.TorusGeometry(0.55, 0.07, 16, 64), Mat.alabaster);
  ring2.position.y = 1.0; ring2.rotation.set(-0.5, 0.9, 0.3); ring2.castShadow = true;
  const coreOrb = new THREE.Mesh(new THREE.SphereGeometry(0.32, 32, 32), Mat.flutedColumn);
  coreOrb.position.y = 1.0; coreOrb.castShadow = true;
  const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.18, 0.7, 16), Mat.pedestal);
  stem.position.y = 0.35; stem.castShadow = true;
  sculpG.add(ring1, ring2, coreOrb, stem); root.add(sculpG);

  // Welcome directory plaque on the south wall (-Z)
  const dirTex = textTexture(1024, 512, (ctx, w, h) => {
    ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 6; ctx.strokeRect(10, 10, w - 20, h - 20);
    ctx.fillStyle = '#e6af2e'; ctx.font = `600 24px ${SANS}`;
    spacedText(ctx, EUNOIA_CONFIG.site.overline.toUpperCase(), w / 2, 54, 4);
    ctx.fillStyle = '#fbfffe'; ctx.font = `600 70px ${SERIF}`;
    spacedText(ctx, EUNOIA_CONFIG.site.title, w / 2, 128, 12);
    ctx.strokeStyle = 'rgba(230,175,46,0.55)'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(w * 0.18, 154); ctx.lineTo(w * 0.82, 154); ctx.stroke();
    ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 26px ${SERIF}`; ctx.textAlign = 'center';
    ctx.fillText(EUNOIA_CONFIG.site.tagline, w / 2, 196);

    ctx.font = `500 18px ${SANS}`;
    ctx.fillStyle = '#e6af2e'; ctx.fillText('← Wing III · The Nocturne & Light Gallery (86 Works)', w / 2, 260);
    ctx.fillStyle = '#fbfffe'; ctx.fillText('↑ Wing II · 3D Virtual Worlds: 5 Specialized Chambers (38 Works) → leads to Wing IV', w / 2, 305);
    ctx.fillStyle = '#e6af2e'; ctx.fillText('Wing I · The Classical & Fine Arts Wing (29 Works) →', w / 2, 350);
    ctx.fillStyle = '#ffc94d'; ctx.fillText('★ Wing IV · The Kinematic Pavilion (Animation, Storyboards & Applied Design · 52 Works)', w / 2, 395);

    ctx.fillStyle = '#8b9c9a'; ctx.font = `400 16px ${SANS}`;
    ctx.fillText('[WASD] Walk  ·  [LMB] Inspect Art & Watch Video  ·  [TAB] Full 205-Piece Exhibition Index', w / 2, 460);
  });
  const dirPlaque = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 1.8), new THREE.MeshStandardMaterial({ map: dirTex, roughness: 0.3 }));
  dirPlaque.position.set(0, 2.2, -R_ROT + 0.3);
  root.add(dirPlaque);

  // Helper: Build Grand Doorway Archway between Galleries
  function buildGalleryPortal({ x, z, rotY = 0, width = 6.0, label, sub }) {
    const g = new THREE.Group();
    g.position.set(x, 0, z);
    g.rotation.y = rotY;

    const lintelH = H_WING - 3.8;
    const lintel = new THREE.Mesh(new THREE.BoxGeometry(width, lintelH, 0.4), Mat.archTrim);
    lintel.position.set(0, 3.8 + lintelH / 2, 0);

    const colL = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 3.8, 16), Mat.flutedColumn);
    colL.position.set(-width / 2 + 0.24, 1.9, 0);
    const colR = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 3.8, 16), Mat.flutedColumn);
    colR.position.set(width / 2 - 0.24, 1.9, 0);

    const signTex = textTexture(1024, 256, (ctx, w, h) => {
      ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
      ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 5; ctx.strokeRect(10, 10, w - 20, h - 20);
      ctx.fillStyle = '#e6af2e'; ctx.font = `600 22px ${SANS}`;
      spacedText(ctx, 'EUNOIA GALLERIES · DEDICATED SALON', w / 2, 54, 4);
      ctx.fillStyle = '#fbfffe'; ctx.font = `600 38px ${SERIF}`;
      spacedText(ctx, label, w / 2, 114, 5);
      ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 20px ${SERIF}`; ctx.textAlign = 'center';
      ctx.fillText(sub, w / 2, 172);
      ctx.fillStyle = '#e6af2e'; ctx.font = `500 15px ${SANS}`;
      ctx.fillText('ENTER GALLERY →', w / 2, 218);
    });
    const signMesh = new THREE.Mesh(new THREE.PlaneGeometry(Math.min(width - 0.6, 4.2), 0.8), new THREE.MeshStandardMaterial({ map: signTex, roughness: 0.35 }));
    signMesh.position.set(0, 4.0, 0.22);

    const signLight = new THREE.PointLight(0xffe4a0, 1.8, 6, 1.3);
    signLight.position.set(0, 4.2, 1.0);

    g.add(lintel, colL, colR, signMesh, signLight);
    return g;
  }

  """

html = html[:start_arch] + new_rotunda_and_helpers + html[start_wing1:]

# Make sure activeHogwartsVideos is exposed immediately
html = html.replace("const activeHogwartsVideos = [];", "const activeHogwartsVideos = [];\nwindow.activeHogwartsVideos = activeHogwartsVideos;")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html fixed with valid Rotunda columns and portal builder!")

