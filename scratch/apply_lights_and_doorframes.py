import re
import shutil

shutil.copy('index.html', 'scratch/index.html.before_lights_doors.bak')
html = open('index.html', encoding='utf-8').read()

# ---------------------------------------------------------------------------
# 1. FIX buildWallPortal: remove retL and retR duplicate boxes
# ---------------------------------------------------------------------------
old_ret = """  // Solid return walls flanking the portal from corridor wall (-3.5) to casing edge (-1.85)
  const retW = (WING_W / 2) - casingHalfW; // 3.50 - 1.85 = 1.65m
  const retGeom = new THREE.BoxGeometry(retW, H_WING, 0.36); // depth 0.36
  const retL = new THREE.Mesh(retGeom, wallMat || Mat.wallRotunda);
  retL.position.set(-WING_W / 2 + retW / 2, H_WING / 2, 0); // center -2.675
  retL.castShadow = true; retL.receiveShadow = true;

  const retR = new THREE.Mesh(retGeom, wallMat || Mat.wallRotunda);
  retR.position.set(WING_W / 2 - retW / 2, H_WING / 2, 0); // center +2.675
  retR.castShadow = true; retR.receiveShadow = true;"""

new_ret = """  // (Return walls are provided cleanly with zero overlap by addSolidWall at each entrance)"""

assert old_ret in html, "old_ret not found in buildWallPortal"
html = html.replace(old_ret, new_ret, 1)

# And remove retL, retR from g.add
old_g_add = "g.add(lintel, frieze, cornice, jL, jR, retL, retR, attic, signIn, signOut);"
new_g_add = "g.add(lintel, frieze, cornice, jL, jR, attic, signIn, signOut);"
assert old_g_add in html, "old_g_add not found in buildWallPortal"
html = html.replace(old_g_add, new_g_add, 1)

# Ensure wall flanks for rotunda portals cleanly span up to jamb casing (|x|=1.85)
flank_replacements = [
    ("addSolidWall(ox, -5.0, ox, -3.3, Mat.wallWingI, wing); addWallSegment(ox, -3.3, ox, -1.50);",
     "addSolidWall(ox, -5.0, ox, -1.85, Mat.wallWingI, wing); addWallSegment(ox, -1.85, ox, -1.50);"),
    ("addSolidWall(ox, 3.3, ox, 5.0, Mat.wallWingI, wing); addWallSegment(ox, 1.50, ox, 3.3);",
     "addSolidWall(ox, 1.85, ox, 5.0, Mat.wallWingI, wing); addWallSegment(ox, 1.50, ox, 1.85);"),

    ("addSolidWall(-hw, oz, -3.3, oz, Mat.wallWingII, wing); addWallSegment(-3.3, oz, -1.50, oz);",
     "addSolidWall(-hw, oz, -1.85, oz, Mat.wallWingII, wing); addWallSegment(-1.85, oz, -1.50, oz);"),
    ("addSolidWall(3.3, oz, hw, oz, Mat.wallWingII, wing); addWallSegment(1.50, oz, 3.3, oz);",
     "addSolidWall(1.85, oz, hw, oz, Mat.wallWingII, wing); addWallSegment(1.50, oz, 1.85, oz);"),

    ("addSolidWall(ox, -5.0, ox, -3.3, Mat.wallWingIII, wing); addWallSegment(ox, -3.3, ox, -1.50);",
     "addSolidWall(ox, -5.0, ox, -1.85, Mat.wallWingIII, wing); addWallSegment(ox, -1.85, ox, -1.50);"),
    ("addSolidWall(ox, 3.3, ox, 5.0, Mat.wallWingIII, wing); addWallSegment(ox, 1.50, ox, 3.3);",
     "addSolidWall(ox, 1.85, ox, 5.0, Mat.wallWingIII, wing); addWallSegment(ox, 1.50, ox, 1.85);"),
]

for old_flank, new_flank in flank_replacements:
    assert old_flank in html, f"Missing flank: {old_flank}"
    html = html.replace(old_flank, new_flank, 1)

# ---------------------------------------------------------------------------
# 2. FIX buildGalleryPortal: two-sided signs (Front & Back) + remove duplicate toWingIISign
# ---------------------------------------------------------------------------
old_gal = """  function buildGalleryPortal({ x, z, rotY = 0, width = 6.0, label, sub }) {
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

    g.add(lintel, colL, colR, signMesh);
    return g;
  }"""

new_gal = """  function buildGalleryPortal({ x, z, rotY = 0, width = 6.0, label, sub, returnLabel = 'RETURN TO PROMENADE' }) {
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

    // Front Sign (Facing entrance approach, +Z in local coordinates)
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

    // Reverse Sign (Facing gallery interior, -Z in local coordinates)
    const revTex = textTexture(512, 128, (ctx, w, h) => {
      ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
      ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 3; ctx.strokeRect(6, 6, w - 12, h - 12);
      ctx.fillStyle = '#e6af2e'; ctx.font = `600 16px ${SANS}`;
      spacedText(ctx, 'GALLERY EXIT', w / 2, 38, 4);
      ctx.fillStyle = '#fbfffe'; ctx.font = `italic 18px ${SERIF}`; ctx.textAlign = 'center';
      ctx.fillText(`← ${returnLabel} →`, w / 2, 82);
    });
    const revMesh = new THREE.Mesh(new THREE.PlaneGeometry(Math.min(width - 0.6, 3.2), 0.6), new THREE.MeshStandardMaterial({ map: revTex, roughness: 0.35 }));
    revMesh.position.set(0, 4.0, -0.22);
    revMesh.rotation.y = Math.PI;

    g.add(lintel, colL, colR, signMesh, revMesh);
    return g;
  }"""

assert old_gal in html, "old_gal not found"
html = html.replace(old_gal, new_gal, 1)

# Remove the duplicate toWingIISign block from Wing IV
old_wing2_sign = """    const toWingIITex = textTexture(1024, 256, (ctx, w, h) => {
      ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
      ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 5; ctx.strokeRect(10, 10, w - 20, h - 20);
      ctx.fillStyle = '#e6af2e'; ctx.font = `600 22px ${SANS}`;
      spacedText(ctx, 'TO WING II · 3D VIRTUAL WORLDS & GRAND ROTUNDA', w / 2, 54, 4);
      ctx.fillStyle = '#fbfffe'; ctx.font = `600 38px ${SERIF}`;
      spacedText(ctx, 'THE 3D VIRTUAL WORLDS PAVILION', w / 2, 114, 5);
      ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 20px ${SERIF}`; ctx.textAlign = 'center';
      ctx.fillText('Environment · Interior · VFX Cinema · Still Life · Character Topology', w / 2, 172);
      ctx.fillStyle = '#e6af2e'; ctx.font = `500 15px ${SANS}`;
      ctx.fillText('← RETURN TO WING II PROMENADE', w / 2, 218);
    });
    const toWingIISign = new THREE.Mesh(new THREE.PlaneGeometry(3.8, 0.8), new THREE.MeshStandardMaterial({ map: toWingIITex, roughness: 0.35 }));
    toWingIISign.position.set(0, 4.0, 52.22);
    wing.add(toWingIISign);"""

assert old_wing2_sign in html, "old_wing2_sign not found"
html = html.replace(old_wing2_sign, "    // (Two-sided portal sign provided cleanly by portToIV at z = 52.0)", 1)

# Update portToIV, portStory, portTrad, portChar orientations and return labels
old_portToIV = "const portToIV = buildGalleryPortal({ x: 0, z: 52.0, rotY: 0, width: 4.0, label: 'WING IV · THE KINEMATIC PAVILION', sub: 'Animation, Storyboards & Applied Graphic Design' });"
new_portToIV = "const portToIV = buildGalleryPortal({ x: 0, z: 52.0, rotY: Math.PI, width: 4.0, label: 'WING IV · THE KINEMATIC PAVILION', sub: 'Animation, Storyboards & Applied Graphic Design', returnLabel: 'RETURN TO WING II PROMENADE' });"
assert old_portToIV in html, "old_portToIV not found"
html = html.replace(old_portToIV, new_portToIV, 1)

old_portStory = "const portStory = buildGalleryPortal({ x: 0, z: 68.0, rotY: 0, width: 6.0, label: 'MASTER STORYBOARD & PRE-VISUALIZATION', sub: 'The Wind Rises Adaptation · Dynamic Continuity & Cinematography' });"
new_portStory = "const portStory = buildGalleryPortal({ x: 0, z: 68.0, rotY: Math.PI, width: 6.0, label: 'MASTER STORYBOARD & PRE-VISUALIZATION', sub: 'The Wind Rises Adaptation · Dynamic Continuity & Cinematography', returnLabel: 'RETURN TO CINEMA ATRIUM' });"
assert old_portStory in html, "old_portStory not found"
html = html.replace(old_portStory, new_portStory, 1)

old_portTrad = "const portTrad = buildGalleryPortal({ x: 51.0, z: 5.0, rotY: 0, width: 6.0, label: 'TRADITIONAL FINE ART SALON', sub: 'Life Studies · Academic Plates · Anatomical Mastery' });"
new_portTrad = "const portTrad = buildGalleryPortal({ x: 51.0, z: 5.0, rotY: Math.PI, width: 6.0, label: 'TRADITIONAL FINE ART SALON', sub: 'Life Studies · Academic Plates · Anatomical Mastery', returnLabel: 'RETURN TO PROMENADE' });"
assert old_portTrad in html, "old_portTrad not found"
html = html.replace(old_portTrad, new_portTrad, 1)

old_portChar = "const portChar = buildGalleryPortal({ x: 51.0, z: -5.0, rotY: Math.PI, width: 6.0, label: '2D CHARACTER ANATOMY STUDIO', sub: 'Figure Proportions · Model Sheets & Design Plates' });"
new_portChar = "const portChar = buildGalleryPortal({ x: 51.0, z: -5.0, rotY: 0, width: 6.0, label: '2D CHARACTER ANATOMY STUDIO', sub: 'Figure Proportions · Model Sheets & Design Plates', returnLabel: 'RETURN TO PROMENADE' });"
assert old_portChar in html, "old_portChar not found"
html = html.replace(old_portChar, new_portChar, 1)

# ---------------------------------------------------------------------------
# 3. UPGRADE buildLightPools: authentic scalloped museum wash & precise wall alignment
# ---------------------------------------------------------------------------
old_pools_start = "function buildLightPools(poolSpots) {"
old_pools_end = "wingGroups[wing].add(mesh);\n  });\n}"
ps = html.find(old_pools_start)
pe = html.find(old_pools_end, ps)
assert ps != -1 and pe != -1, "buildLightPools block not found"

NEW_POOLS = r'''function buildLightPools(poolSpots) {
  const [pc, pctx] = makeCanvas(256, 256);
  const imgData = pctx.createImageData(256, 256);
  const data = imgData.data;
  const lx = 128.0, ly = 45.0; // hot spot at picture lamp fixture

  for (let y = 0; y < 256; y++) {
    const dy = y - ly;
    for (let x = 0; x < 256; x++) {
      const dx = x - lx;

      // 1. Hot filament core right at lamp hood
      const dHot = Math.hypot(dx * 1.0, dy * 1.8);
      const hot = Math.pow(Math.max(0, 1.0 - dHot / 32.0), 1.8);

      // 2. Scalloped downward fan (55-degree half-angle with cosine falloff)
      let wash = 0;
      if (dy > -6.0) {
        const angDeg = Math.abs(Math.atan2(dx, dy) * 180 / Math.PI);
        if (angDeg < 55.0) {
          const fan = Math.pow(Math.cos(angDeg / 55.0 * Math.PI * 0.5), 1.2);
          const dist = Math.hypot(dx, dy);
          const distTaper = Math.pow(Math.max(0, 1.0 - dist / 195.0), 1.2);
          wash = fan * distTaper * 0.95;
        }
      }

      // 3. Upward spill on wall above fixture
      const dUp = Math.hypot(dx * 1.2, dy * 2.0);
      const spill = Math.pow(Math.max(0, 1.0 - dUp / 35.0), 2.0) * 0.40;

      const intensity = Math.min(1.0, hot * 1.0 + wash + spill);
      if (intensity > 0.005) {
        const idx = (y * 256 + x) * 4;
        data[idx]     = Math.min(255, 255 * intensity * 1.1) | 0;
        data[idx + 1] = Math.min(255, 230 * (intensity * 0.95 + 0.05)) | 0;
        data[idx + 2] = Math.min(255, 170 * (intensity * 0.65 + 0.05)) | 0;
        data[idx + 3] = Math.min(255, 255 * Math.pow(intensity, 1.1)) | 0;
      }
    }
  }
  pctx.putImageData(imgData, 0, 0);

  const poolTex = new THREE.CanvasTexture(pc);
  poolTex.colorSpace = THREE.SRGBColorSpace;
  poolTex.generateMipmaps = false;
  poolTex.minFilter = THREE.LinearFilter;
  poolTex.magFilter = THREE.LinearFilter;

  const poolMat = new THREE.MeshBasicMaterial({
    map: poolTex, transparent: true, opacity: 0.95,
    blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide
  });
  poolMat.toneMapped = false;

  const wingGroups = { I: wingI_group, II: wingII_group, III: wingIII_group, IV: wingIV_group };
  Object.keys(poolSpots).forEach((wing) => {
    const geos = [];
    poolSpots[wing].forEach((s) => {
      const artW = s.land ? 2.6 : 1.95, artH = s.land ? 1.95 : 2.6;
      const pw = artW + 1.6, ph = artH + 1.8;
      const g = new THREE.PlaneGeometry(pw, ph);
      // Align hot spot (ly/256 = 0.1757 from top) with brass hood (artH/2 + 0.35)
      const yShift = (artH / 2 + 0.35) - 0.3243 * ph;
      // Position plane directly on wall surface behind frame (-0.055 in local z)
      g.translate(0, yShift, -0.055);
      g.rotateY(s.rotY);
      g.translate(s.x, s.y, s.z);
      geos.push(g);
    });
    if (!geos.length) return;
    const flatParts = geos.map((p) => (p.index ? p.toNonIndexed() : p));
    const merged = mergeGeometries(flatParts, false);
    geos.forEach((g) => g.dispose());
    flatParts.forEach((p) => p.dispose());
    const mesh = new THREE.Mesh(merged, poolMat);
    mesh.renderOrder = 2;
    mesh.frustumCulled = false;
    wingGroups[wing].add(mesh);
  });
}'''

html = html[:ps] + NEW_POOLS + html[pe + len(old_pools_end):]

# ---------------------------------------------------------------------------
# 4. ADJUST buildLighting: gallery-appropriate ambient so warm lights stand out
# ---------------------------------------------------------------------------
old_lighting = """function buildLighting() {
  // Constant light count (4 total) => no shader recompiles when wings toggle visibility.
  const hemi = new THREE.HemisphereLight(0xdcd0bc, 0x000808, 0.65);
  scene.add(hemi);

  const amb = new THREE.AmbientLight(0xfbf2e4, 0.45);
  scene.add(amb);"""

new_lighting = """function buildLighting() {
  // Constant light count (4 total) => no shader recompiles when wings toggle visibility.
  // Tuned ambient so baked picture lamps & visitor lantern create dramatic, warm gallery highlights.
  const hemi = new THREE.HemisphereLight(0xdcd0bc, 0x000808, 0.40);
  scene.add(hemi);

  const amb = new THREE.AmbientLight(0xfbf2e4, 0.28);
  scene.add(amb);"""

assert old_lighting in html, "old_lighting not found"
html = html.replace(old_lighting, new_lighting, 1)

open('index.html', 'w', encoding='utf-8').write(html)
print("Successfully applied lights and doorframe glitch fixes!")

