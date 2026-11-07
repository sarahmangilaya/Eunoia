import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ----------------------------------------------------------------------------
# 1. TextureLoadQueue definition before buildPictureFrame
# ----------------------------------------------------------------------------
queue_code = """
const TextureLoadQueue = {
  queue: [],
  activeCount: 0,
  maxConcurrent: 6,
  enqueue(url, onLoad, onError) {
    this.queue.push({ url, onLoad, onError });
    this.process();
  },
  process() {
    while (this.activeCount < this.maxConcurrent && this.queue.length > 0) {
      const item = this.queue.shift();
      this.activeCount++;
      texLoader.load(
        item.url,
        (tex) => {
          this.activeCount--;
          item.onLoad(tex);
          this.process();
        },
        undefined,
        (err) => {
          this.activeCount--;
          if (item.onError) item.onError(err);
          this.process();
        }
      );
    }
  }
};
"""

# ----------------------------------------------------------------------------
# 2. Complete buildArchitecture implementation with addSolidWall
# ----------------------------------------------------------------------------
new_build_arch = """function buildArchitecture() {
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
    const isWingI = (i === 0 || i === segments - 1);
    const isWingII = (i === 4 || i === 3);
    const isWingIII = (i === 8 || i === 7);
    if (isWingI || isWingII || isWingIII) {
      continue;
    }
    const chord = 2 * R_ROT * Math.sin(dTheta / 2);
    const wallSeg = new THREE.Mesh(new THREE.BoxGeometry(chord * 1.02, H_ROT, 0.4), Mat.wallRotunda);
    wallSeg.position.set(Math.cos(mid) * R_ROT, H_ROT / 2, Math.sin(mid) * R_ROT);
    wallSeg.rotation.y = -mid + Math.PI / 2;
    wallSeg.castShadow = true; wallSeg.receiveShadow = true; root.add(wallSeg);

    const p1x = Math.cos(a0) * (R_ROT - 0.25), p1z = Math.sin(a0) * (R_ROT - 0.25);
    const p2x = Math.cos(a1) * (R_ROT - 0.25), p2z = Math.sin(a1) * (R_ROT - 0.25);
    addWallSegment(p1x, p1z, p2x, p2z);
  }

  // Skylight ring & classical columns
  const skylight = new THREE.Mesh(new THREE.CylinderGeometry(3.6, 3.6, 0.4, 32, 1, true), Mat.goldLeaf);
  skylight.position.y = H_ROT - 0.2; root.add(skylight);

  const colR = 0.45, numCols = 8;
  const colCircRadius = R_ROT - 2.8;
  for (let i = 0; i < numCols; i++) {
    const angle = (i / numCols) * TAU + Math.PI / numCols;
    const cx = Math.cos(angle) * colCircRadius, cz = Math.sin(angle) * colCircRadius;
    const colMesh = buildClassicalColumn(colR, H_ROT - 0.6, Mat.flutedColumn, Mat.archTrim);
    colMesh.position.set(cx, 0, cz); root.add(colMesh);
    addCylCollider(cx, cz, colR + 0.15);
  }

  // Rotunda center feature: Circular pedestal & classical bronze sphere
  const ped = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.8, 0.9, 32), Mat.pedestal);
  ped.position.set(0, 0.45, 0); ped.receiveShadow = true; ped.castShadow = true;
  const statue = new THREE.Mesh(new THREE.DodecahedronGeometry(0.85, 1), Mat.bronze);
  statue.position.set(0, 1.8, 0); statue.castShadow = true;
  root.add(ped, statue);
  addCylCollider(0, 0, 1.95);

  // Peripheral benches
  for (let i = 0; i < 4; i++) {
    const a = (i / 4) * TAU + Math.PI / 4;
    const bx = Math.cos(a) * (R_ROT - 1.8), bz = Math.sin(a) * (R_ROT - 1.8);
    const bench = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    bench.position.set(bx, 0, bz);
    bench.rotation.y = -a + Math.PI / 2;
    root.add(bench);
    addRotatedBoxCollider(bx, bz, 1.75, 0.55, -a + Math.PI / 2);
  }

  // Donor plaque
  const donorTex = textTexture(1024, 512, (ctx, w, h) => {
    ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 6; ctx.strokeRect(12, 12, w - 24, h - 24);
    ctx.fillStyle = '#e6af2e'; ctx.font = `600 24px ${SANS}`; ctx.textAlign = 'center';
    spacedText(ctx, 'A MUSEUM OF ANIMATION & VISUAL ART', w / 2, 70, 4);
    ctx.fillStyle = '#fbfffe'; ctx.font = `700 68px ${SERIF}`;
    spacedText(ctx, 'E U N O I A', w / 2, 150, 8);
    ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 22px ${SERIF}`;
    ctx.fillText('Selected Works of Sarah Mae · Animation, 3D, VFX & Visual Arts', w / 2, 210);
    ctx.fillStyle = '#e6af2e'; ctx.font = `500 16px ${SANS}`;
    ctx.fillText('• Wing I · Classical and Fine Arts (Traditional, Academic & 2D Model)', w / 2, 280);
    ctx.fillText('• Wing II · 3D Virtual Worlds (VFX Cinema, Environments, Character)', w / 2, 320);
    ctx.fillText('• Wing III · Observational Nocturne (Photography)', w / 2, 360);
    ctx.fillText('• Wing IV · The Kinematic Pavilion (2D Animation, Cinema & Graphic Design)', w / 2, 400);
    ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 16px ${SERIF}`;
    ctx.fillText('Curated in 2026 · Move with WASD/Arrows · Click artworks to inspect', w / 2, 460);
  });
  const donor = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 1.8), new THREE.MeshStandardMaterial({ map: donorTex, roughness: 0.35 }));
  donor.position.set(0, 3.2, -(R_ROT - 0.4)); root.add(donor);

  /* --- 2.1 Wing I: The Classical & Fine Arts Wing (29 Works) --- */
  function buildWingI() {
    const wing = wingI_group;
    const ox = R_ROT - 0.2; // ox = 8.3

    // Central Promenade Floor & Ceiling (x in [8.3, 44.3], z in [-5.0, 5.0])
    const promLen = 36.0, promW = 10.0;
    const floorP = new THREE.Mesh(new THREE.PlaneGeometry(promLen, promW), Mat.floorWingI);
    floorP.rotation.x = -Math.PI / 2; floorP.position.set(ox + promLen / 2, 0, 0); floorP.receiveShadow = true;
    const ceilP = new THREE.Mesh(new THREE.PlaneGeometry(promLen, promW), Mat.ceilingWingI);
    ceilP.rotation.x = Math.PI / 2; ceilP.position.set(ox + promLen / 2, H_WING, 0);
    const threshold = new THREE.Mesh(new RoundedBoxGeometry(0.72, 0.024, promW + 0.1, 3, 0.01), Mat.archTrim);
    threshold.position.set(ox, 0.012, 0);
    wing.add(floorP, ceilP, threshold);

    // Entrance Portal from Rotunda
    const portal = buildWallPortal('I', EUNOIA_CONFIG.wings.I.name, EUNOIA_CONFIG.wings.I.blurb, Mat.wallWingI);
    portal.position.set(ox, 0, 0); portal.rotation.y = Math.PI / 2; wing.add(portal);

    // Portal flanking returns & header
    addSolidWall(ox, -5.0, ox, -1.50, Mat.wallWingI, wing);
    addSolidWall(ox, -1.50, ox, 1.50, Mat.wallWingI, wing, 3.8, H_WING);
    addSolidWall(ox, 1.50, ox, 5.0, Mat.wallWingI, wing);

    // Promenade Continuous Side Walls
    addSolidWall(ox, 5.0, ox + promLen, 5.0, Mat.wallWingI, wing);
    addSolidWall(ox, -5.0, ox + promLen, -5.0, Mat.wallWingI, wing);

    // Viewing benches along Promenade
    const benchP1 = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchP1.position.set(20.0, 0, 0); wing.add(benchP1); addRotatedBoxCollider(20.0, 0, 1.75, 0.55, 0);
    const benchP2 = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchP2.position.set(34.0, 0, 0); wing.add(benchP2); addRotatedBoxCollider(34.0, 0, 1.75, 0.55, 0);

    // Vestibule Floor & Ceiling (x in [44.3, 58.0], z in [-5.0, 5.0])
    const vestLen = 13.7;
    const floorV = new THREE.Mesh(new THREE.PlaneGeometry(vestLen, promW), Mat.floorWingI);
    floorV.rotation.x = -Math.PI / 2; floorV.position.set(44.3 + vestLen / 2, 0, 0); floorV.receiveShadow = true;
    const ceilV = new THREE.Mesh(new THREE.PlaneGeometry(vestLen, promW), Mat.ceilingWingI);
    ceilV.rotation.x = Math.PI / 2; ceilV.position.set(44.3 + vestLen / 2, H_WING, 0);
    wing.add(floorV, ceilV);

    // East End Wall at x = 58.0
    addSolidWall(58.0, -5.0, 58.0, 5.0, Mat.wallWingI, wing);

    // Console table & urn
    const consoleTable = new THREE.Mesh(new RoundedBoxGeometry(2.4, 0.9, 0.6, 3, 0.03), Mat.darkWood);
    consoleTable.position.set(57.5, 0.45, 0); consoleTable.rotation.y = -Math.PI / 2; consoleTable.castShadow = true;
    const urn = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.18, 0.7, 16), Mat.goldLeaf);
    urn.position.set(57.5, 1.25, 0); urn.castShadow = true;
    wing.add(consoleTable, urn);
    addRotatedBoxCollider(57.5, 0, 1.35, 0.45, Math.PI / 2);

    // North Portal to Traditional Salon
    const portTrad = buildGalleryPortal({ x: 51.0, z: 5.0, rotY: 0, width: 6.0, label: 'TRADITIONAL FINE ART SALON', sub: 'Life Studies · Academic Plates · Anatomical Mastery' });
    wing.add(portTrad);
    addSolidWall(44.3, 5.0, 48.0, 5.0, Mat.wallWingI, wing);
    addSolidWall(48.0, 5.0, 54.0, 5.0, Mat.wallWingI, wing, 3.8, H_WING); // Portal header
    addSolidWall(54.0, 5.0, 58.0, 5.0, Mat.wallWingI, wing);

    // South Portal to Character Studio
    const portChar = buildGalleryPortal({ x: 51.0, z: -5.0, rotY: Math.PI, width: 6.0, label: '2D CHARACTER ANATOMY STUDIO', sub: 'Figure Proportions · Model Sheets & Design Plates' });
    wing.add(portChar);
    addSolidWall(44.3, -5.0, 48.0, -5.0, Mat.wallWingI, wing);
    addSolidWall(48.0, -5.0, 54.0, -5.0, Mat.wallWingI, wing, 3.8, H_WING); // Portal header
    addSolidWall(54.0, -5.0, 58.0, -5.0, Mat.wallWingI, wing);

    // North Salon Floor, Ceiling & Walls (x in [44.0, 60.0], z in [5.0, 22.0])
    const salLen = 16.0, salD = 17.0;
    const floorSal = new THREE.Mesh(new THREE.PlaneGeometry(salLen, salD), Mat.floorWingI);
    floorSal.rotation.x = -Math.PI / 2; floorSal.position.set(52.0, 0, 13.5); floorSal.receiveShadow = true;
    const ceilSal = new THREE.Mesh(new THREE.PlaneGeometry(salLen, salD), Mat.ceilingWingI);
    ceilSal.rotation.x = Math.PI / 2; ceilSal.position.set(52.0, H_WING, 13.5);
    wing.add(floorSal, ceilSal);

    addSolidWall(44.0, 5.0, 44.0, 22.0, Mat.wallWingI, wing);  // West wall
    addSolidWall(44.0, 22.0, 60.0, 22.0, Mat.wallWingI, wing); // North wall
    addSolidWall(60.0, 5.0, 60.0, 22.0, Mat.wallWingI, wing);  // East wall

    const benchSal = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchSal.position.set(52.0, 0, 13.5); wing.add(benchSal); addRotatedBoxCollider(52.0, 13.5, 1.75, 0.55, 0);

    // South Studio Floor, Ceiling & Walls (x in [44.0, 60.0], z in [-22.0, -5.0])
    const floorChar = new THREE.Mesh(new THREE.PlaneGeometry(salLen, salD), Mat.floorWingI);
    floorChar.rotation.x = -Math.PI / 2; floorChar.position.set(52.0, 0, -13.5); floorChar.receiveShadow = true;
    const ceilChar = new THREE.Mesh(new THREE.PlaneGeometry(salLen, salD), Mat.ceilingWingI);
    ceilChar.rotation.x = Math.PI / 2; ceilChar.position.set(52.0, H_WING, -13.5);
    wing.add(floorChar, ceilChar);

    addSolidWall(44.0, -22.0, 44.0, -5.0, Mat.wallWingI, wing);  // West wall
    addSolidWall(44.0, -22.0, 60.0, -22.0, Mat.wallWingI, wing); // South wall
    addSolidWall(60.0, -22.0, 60.0, -5.0, Mat.wallWingI, wing);  // East wall

    const benchChar = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchChar.position.set(52.0, 0, -13.5); wing.add(benchChar); addRotatedBoxCollider(52.0, -13.5, 1.75, 0.55, 0);
  }

  /* --- 2.2 Wing II: The 3D Virtual Worlds Pavilion (38 Works) --- */
  function buildWingII() {
    const wing = wingII_group;
    const oz = R_ROT - 0.2; // oz = 8.3
    const length = 43.7; // Spans z = 8.3 to 52.0
    const hw = 4.0;

    const floorStart = 0.35;
    const floorLen = length - floorStart;
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(hw * 2, floorLen), Mat.floorWingII);
    floor.rotation.x = -Math.PI / 2; floor.position.set(0, 0, oz + floorStart + floorLen / 2); floor.receiveShadow = true;
    const ceil = new THREE.Mesh(new THREE.PlaneGeometry(hw * 2, floorLen), Mat.ceilingWingII);
    ceil.rotation.x = Math.PI / 2; ceil.position.set(0, H_WING, oz + floorStart + floorLen / 2);
    const threshold = new THREE.Mesh(new RoundedBoxGeometry(hw * 2 + 0.1, 0.024, 0.72, 3, 0.01), Mat.archTrim);
    threshold.position.set(0, 0.012, oz);
    wing.add(floor, ceil, threshold);

    // Entrance portal arch from Rotunda into Wing II
    const portal = buildWallPortal('II', EUNOIA_CONFIG.wings.II.name, EUNOIA_CONFIG.wings.II.blurb, Mat.wallWingII);
    portal.position.set(0, 0, oz); wing.add(portal);

    addSolidWall(-hw, oz, -1.50, oz, Mat.wallWingII, wing);
    addSolidWall(-1.50, oz, 1.50, oz, Mat.wallWingII, wing, 3.8, H_WING);
    addSolidWall(1.50, oz, hw, oz, Mat.wallWingII, wing);

    // Promenade West Walls (x = -4.0)
    addSolidWall(-hw, 8.3, -hw, 14.5, Mat.wallWingII, wing);
    addSolidWall(-hw, 14.5, -hw, 20.5, Mat.wallWingII, wing, 3.8, H_WING); // Room A header
    addSolidWall(-hw, 20.5, -hw, 38.0, Mat.wallWingII, wing);
    addSolidWall(-hw, 38.0, -hw, 44.0, Mat.wallWingII, wing, 3.8, H_WING); // Room C header
    addSolidWall(-hw, 44.0, -hw, 52.0, Mat.wallWingII, wing);

    // Promenade East Walls (x = 4.0)
    addSolidWall(hw, 8.3, hw, 14.5, Mat.wallWingII, wing);
    addSolidWall(hw, 14.5, hw, 20.5, Mat.wallWingII, wing, 3.8, H_WING); // Room B header
    addSolidWall(hw, 20.5, hw, 38.0, Mat.wallWingII, wing);
    addSolidWall(hw, 38.0, hw, 44.0, Mat.wallWingII, wing, 3.8, H_WING); // Room D header
    addSolidWall(hw, 44.0, hw, 52.0, Mat.wallWingII, wing);

    // Chamber Doorway Portals
    const portalA = buildGalleryPortal({ x: -hw, z: 17.5, rotY: Math.PI / 2, width: 6.0, label: '3D ENVIRONMENT GALLERY', sub: 'Exterior Worlds · Architecture · PBR Illumination' });
    const portalB = buildGalleryPortal({ x: hw, z: 17.5, rotY: -Math.PI / 2, width: 6.0, label: '3D INTERIOR ARCHITECTURE', sub: 'Spatial Layouts · Materiality & Raytracing' });
    const portalC = buildGalleryPortal({ x: -hw, z: 41.0, rotY: Math.PI / 2, width: 6.0, label: '3D VFX THEATRE', sub: 'Dynamic Simulations · Fluids & Particles' });
    const portalD = buildGalleryPortal({ x: hw, z: 41.0, rotY: -Math.PI / 2, width: 6.0, label: '3D STILL LIFE & PROP RENDER', sub: 'Studio Lighting · Microfacet Shading' });
    wing.add(portalA, portalB, portalC, portalD);

    // North Portal to Wing IV at z = 52.0
    const portToIV = buildGalleryPortal({ x: 0, z: 52.0, rotY: 0, width: 4.0, label: 'WING IV · THE KINEMATIC PAVILION', sub: 'Animation, Storyboards & Applied Graphic Design' });
    wing.add(portToIV);
    addSolidWall(-hw, 52.0, -2.0, 52.0, Mat.wallWingII, wing);
    addSolidWall(-2.0, 52.0, 2.0, 52.0, Mat.wallWingII, wing, 3.8, H_WING);
    addSolidWall(2.0, 52.0, hw, 52.0, Mat.wallWingII, wing);

    // Helper: Build Room
    function buildRoom({ xMin, xMax, zMin, zMax, openSide, benchMat, floorMat = Mat.floorWingII, wallMat = Mat.wallWingII }) {
      const rw = xMax - xMin, rd = zMax - zMin;
      const cx = (xMin + xMax) / 2, cz = (zMin + zMax) / 2;

      const f = new THREE.Mesh(new THREE.PlaneGeometry(rw, rd), floorMat);
      f.rotation.x = -Math.PI / 2; f.position.set(cx, 0, cz); f.receiveShadow = true;
      const c = new THREE.Mesh(new THREE.PlaneGeometry(rw, rd), Mat.ceilingWingII);
      c.rotation.x = Math.PI / 2; c.position.set(cx, H_WING, cz);
      wing.add(f, c);

      addSolidWall(xMin, zMax, xMax, zMax, wallMat, wing); // North wall
      addSolidWall(xMin, zMin, xMax, zMin, wallMat, wing); // South wall

      if (openSide === 'east') {
        addSolidWall(xMin, zMin, xMin, zMax, wallMat, wing); // West outer wall
      } else {
        addSolidWall(xMax, zMin, xMax, zMax, wallMat, wing); // East outer wall
      }

      const bench = buildMuseumBench(Mat.darkWood, benchMat || Mat.blackVelvet);
      bench.position.set(cx, 0, cz); wing.add(bench);
      addRotatedBoxCollider(cx, cz, 1.75, 0.55, 0);
    }

    buildRoom({ xMin: -22.0, xMax: -4.0, zMin: 9.5, zMax: 25.5, openSide: 'east', benchMat: Mat.darkWood });
    buildRoom({ xMin: 4.0, xMax: 22.0, zMin: 9.5, zMax: 25.5, openSide: 'west', benchMat: Mat.crimsonVelvet });
    buildRoom({ xMin: -22.0, xMax: -4.0, zMin: 33.0, zMax: 49.0, openSide: 'east', benchMat: Mat.blackVelvet });
    buildRoom({ xMin: 4.0, xMax: 22.0, zMin: 33.0, zMax: 49.0, openSide: 'west', benchMat: Mat.darkWood });
  }

  /* --- 2.3 Wing III: The Nocturne & Observational Photography Gallery (86 Works) --- */
  function buildWingIII() {
    const wing = wingIII_group;
    const ox = -(R_ROT - 0.2); // ox = -8.3
    const blvdLen = 59.7, blvdW = 10.0;

    const floorB = new THREE.Mesh(new THREE.PlaneGeometry(blvdLen, blvdW), Mat.floorWingIII);
    floorB.rotation.x = -Math.PI / 2; floorB.position.set(-8.3 - blvdLen / 2, 0, 0); floorB.receiveShadow = true;
    const ceilB = new THREE.Mesh(new THREE.PlaneGeometry(blvdLen, blvdW), Mat.ceilingWingIII);
    ceilB.rotation.x = Math.PI / 2; ceilB.position.set(-8.3 - blvdLen / 2, H_WING, 0);
    const threshold = new THREE.Mesh(new RoundedBoxGeometry(0.72, 0.024, blvdW + 0.1, 3, 0.01), Mat.archTrim);
    threshold.position.set(ox, 0.012, 0);
    wing.add(floorB, ceilB, threshold);

    // Entrance Portal from Rotunda
    const portal = buildWallPortal('III', EUNOIA_CONFIG.wings.III.name, EUNOIA_CONFIG.wings.III.blurb, Mat.wallWingIII);
    portal.position.set(ox, 0, 0); portal.rotation.y = -Math.PI / 2; wing.add(portal);

    // Portal flanking return walls
    addSolidWall(ox, -5.0, ox, -1.50, Mat.wallWingIII, wing);
    addSolidWall(ox, -1.50, ox, 1.50, Mat.wallWingIII, wing, 3.8, H_WING);
    addSolidWall(ox, 1.50, ox, 5.0, Mat.wallWingIII, wing);

    // West End Wall at x = -68.0
    addSolidWall(-68.0, -5.0, -68.0, 5.0, Mat.wallWingIII, wing);

    // Pedestal & Golden Lunar Sphere
    const noctPed = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.45, 1.0, 24), Mat.pedestal);
    noctPed.position.set(-66.8, 0.5, 0);
    const orb = new THREE.Mesh(new THREE.SphereGeometry(0.28, 24, 24), Mat.goldLeaf);
    orb.position.set(-66.8, 1.28, 0);
    wing.add(noctPed, orb);
    addCylCollider(-66.8, 0, 0.6);

    // North & South Portals
    const portLunar = buildGalleryPortal({ x: -35.0, z: 5.0, rotY: Math.PI, width: 6.0, label: 'LUNAR ASTROPHOTOGRAPHY OBSERVATORY', sub: 'Selenography · Deep Celestial Horizons · Moonlit Tonalities' });
    const portWild = buildGalleryPortal({ x: -35.0, z: -5.0, rotY: 0, width: 6.0, label: 'WILDLIFE & ANIMAL SANCTUARY', sub: 'Fauna Portraiture · Kinetic Instinct · Living Light' });
    const portPort = buildGalleryPortal({ x: -55.0, z: 5.0, rotY: Math.PI, width: 6.0, label: 'EDITORIAL & MODEL PORTRAITURE SALON', sub: 'Dramatic Key Lighting · Human Expressiveness' });
    const portStill = buildGalleryPortal({ x: -55.0, z: -5.0, rotY: 0, width: 6.0, label: 'STILL LIFE & OBSERVATIONAL OBJECTS', sub: 'Form, Shadow & Everyday Materiality' });
    wing.add(portLunar, portWild, portPort, portStill);

    // Boulevard North Walls (z = 5.0) - Street Photography hangs here!
    addSolidWall(-8.3, 5.0, -32.0, 5.0, Mat.wallWingIII, wing);
    addSolidWall(-32.0, 5.0, -38.0, 5.0, Mat.wallWingIII, wing, 3.8, H_WING); // Lunar header
    addSolidWall(-38.0, 5.0, -52.0, 5.0, Mat.wallWingIII, wing);
    addSolidWall(-52.0, 5.0, -58.0, 5.0, Mat.wallWingIII, wing, 3.8, H_WING); // Portrait header
    addSolidWall(-58.0, 5.0, -68.0, 5.0, Mat.wallWingIII, wing);

    // Boulevard South Walls (z = -5.0) - Street Photography hangs here!
    addSolidWall(-8.3, -5.0, -32.0, -5.0, Mat.wallWingIII, wing);
    addSolidWall(-32.0, -5.0, -38.0, -5.0, Mat.wallWingIII, wing, 3.8, H_WING); // Wildlife header
    addSolidWall(-38.0, -5.0, -52.0, -5.0, Mat.wallWingIII, wing);
    addSolidWall(-52.0, -5.0, -58.0, -5.0, Mat.wallWingIII, wing, 3.8, H_WING); // Still life header
    addSolidWall(-58.0, -5.0, -68.0, -5.0, Mat.wallWingIII, wing);

    const bB1 = buildMuseumBench(Mat.pedestal, Mat.blackVelvet);
    bB1.position.set(-20.0, 0, 0); wing.add(bB1); addRotatedBoxCollider(-20.0, 0, 1.75, 0.55, 0);
    const bB2 = buildMuseumBench(Mat.pedestal, Mat.blackVelvet);
    bB2.position.set(-45.0, 0, 0); wing.add(bB2); addRotatedBoxCollider(-45.0, 0, 1.75, 0.55, 0);

    function buildPhotoChamber({ xMin, xMax, zMin, zMax, openZ }) {
      const cw = xMax - xMin, cd = zMax - zMin;
      const cx = (xMin + xMax) / 2, cz = (zMin + zMax) / 2;

      const f = new THREE.Mesh(new THREE.PlaneGeometry(cw, cd), Mat.floorWingIII);
      f.rotation.x = -Math.PI / 2; f.position.set(cx, 0, cz); f.receiveShadow = true;
      const c = new THREE.Mesh(new THREE.PlaneGeometry(cw, cd), Mat.ceilingWingIII);
      c.rotation.x = Math.PI / 2; c.position.set(cx, H_WING, cz);
      wing.add(f, c);

      addSolidWall(xMax, zMin, xMax, zMax, Mat.wallWingIII, wing);
      addSolidWall(xMin, zMin, xMin, zMax, Mat.wallWingIII, wing);

      if (openZ < 0) {
        addSolidWall(xMin, zMin, xMax, zMin, Mat.wallWingIII, wing);
      } else {
        addSolidWall(xMin, zMax, xMax, zMax, Mat.wallWingIII, wing);
      }

      const bench = buildMuseumBench(Mat.pedestal, Mat.blackVelvet);
      bench.position.set(cx, 0, cz); wing.add(bench);
      addRotatedBoxCollider(cx, cz, 1.75, 0.55, 0);
    }

    buildPhotoChamber({ xMin: -46.0, xMax: -28.0, zMin: 5.0, zMax: 23.0, openZ: 5.0 });
    buildPhotoChamber({ xMin: -46.0, xMax: -28.0, zMin: -23.0, zMax: -5.0, openZ: -5.0 });
    buildPhotoChamber({ xMin: -66.0, xMax: -48.0, zMin: 5.0, zMax: 23.0, openZ: 5.0 });
    buildPhotoChamber({ xMin: -66.0, xMax: -48.0, zMin: -23.0, zMax: -5.0, openZ: -5.0 });
  }

  /* --- 2.4 Wing IV: The Kinematic & Applied Design Pavilion (52 Works) --- */
  function buildWingIV() {
    const wing = wingIV_group;

    // A. Central Cinema Atrium (x in [-8.0, 8.0], z in [52.0, 68.0], 16m x 16m)
    const floorC = new THREE.Mesh(new THREE.PlaneGeometry(16.0, 16.0), Mat.floorWingI);
    floorC.rotation.x = -Math.PI / 2; floorC.position.set(0, 0, 60.0); floorC.receiveShadow = true;
    const ceilC = new THREE.Mesh(new THREE.PlaneGeometry(16.0, 16.0), Mat.ceilingWingI);
    ceilC.rotation.x = Math.PI / 2; ceilC.position.set(0, H_WING, 60.0);
    wing.add(floorC, ceilC);

    const toWingIITex = textTexture(1024, 256, (ctx, w, h) => {
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
    wing.add(toWingIISign);

    // Portals
    const portGraphic = buildGalleryPortal({ x: 8.0, z: 60.0, rotY: -Math.PI / 2, width: 4.0, label: 'APPLIED GRAPHIC DESIGN & BRAND IDENTITY', sub: 'Poster Typography · Brand Monograms · Atelier Jacquard Lanyards' });
    const portProd = buildGalleryPortal({ x: -8.0, z: 60.0, rotY: Math.PI / 2, width: 4.0, label: 'PRODUCTION DESIGN & ART DIRECTION', sub: 'Set Photography · Cinematic Scenography & Atmosphere' });
    const portStory = buildGalleryPortal({ x: 0, z: 68.0, rotY: 0, width: 6.0, label: 'MASTER STORYBOARD & PRE-VISUALIZATION', sub: 'The Wind Rises Adaptation · Dynamic Continuity & Cinematography' });
    wing.add(portGraphic, portProd, portStory);

    // 1. South Wall of Wing IV (z = 52.0)
    addSolidWall(-28.0, 52.0, -8.0, 52.0, Mat.wallWingII, wing); // West Chamber south
    addSolidWall(-8.0, 52.0, -2.0, 52.0, Mat.wallWingII, wing);  // Cinema left return
    addSolidWall(-2.0, 52.0, 2.0, 52.0, Mat.wallWingII, wing, 3.8, H_WING); // Entrance portal header
    addSolidWall(2.0, 52.0, 8.0, 52.0, Mat.wallWingII, wing);   // Cinema right return
    addSolidWall(8.0, 52.0, 28.0, 52.0, Mat.wallWingII, wing);  // East Chamber south

    // 2. West Dividing Wall between Cinema and Production Design (x = -8.0)
    addSolidWall(-8.0, 52.0, -8.0, 58.0, Mat.wallWingII, wing); // Spot 3 hangs here!
    addSolidWall(-8.0, 58.0, -8.0, 62.0, Mat.wallWingII, wing, 3.8, H_WING); // Portal header
    addSolidWall(-8.0, 62.0, -8.0, 68.0, Mat.wallWingII, wing); // Spot 4 hangs here!

    // 3. East Dividing Wall between Cinema and Applied Graphic (x = 8.0)
    addSolidWall(8.0, 52.0, 8.0, 58.0, Mat.wallWingII, wing);  // Spot 5 hangs here!
    addSolidWall(8.0, 58.0, 8.0, 62.0, Mat.wallWingII, wing, 3.8, H_WING); // Portal header
    addSolidWall(8.0, 62.0, 8.0, 68.0, Mat.wallWingII, wing);  // Spot 6 hangs here!

    // 4. North Dividing Wall at z = 68.0 (between South Chambers and Grand Storyboard Hall)
    addSolidWall(-28.0, 68.0, -8.0, 68.0, Mat.wallWingII, wing); // West Chamber north
    addSolidWall(-8.0, 68.0, -3.0, 68.0, Mat.wallWingII, wing);  // Cinema left return (Spot 1 hangs here!)
    addSolidWall(-3.0, 68.0, 3.0, 68.0, Mat.wallWingII, wing, 3.8, H_WING); // Grand Portal header
    addSolidWall(3.0, 68.0, 8.0, 68.0, Mat.wallWingII, wing);   // Cinema right return (Spot 2 hangs here!)
    addSolidWall(8.0, 68.0, 28.0, 68.0, Mat.wallWingII, wing);  // East Chamber north

    // 5. Outer Perimeter Walls
    addSolidWall(-28.0, 52.0, -28.0, 68.0, Mat.wallWingII, wing); // West Chamber outer
    addSolidWall(28.0, 52.0, 28.0, 68.0, Mat.wallWingII, wing);  // East Chamber outer
    addSolidWall(-28.0, 68.0, -28.0, 92.0, Mat.wallWingII, wing); // Storyboard Hall west outer
    addSolidWall(28.0, 68.0, 28.0, 92.0, Mat.wallWingII, wing);  // Storyboard Hall east outer
    addSolidWall(-28.0, 92.0, 28.0, 92.0, Mat.wallWingII, wing); // Grand north wall

    const cinemaBench = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    cinemaBench.position.set(0, 0, 60.0); wing.add(cinemaBench);
    addRotatedBoxCollider(0, 60.0, 1.75, 0.55, 0);

    // B. East Chamber Floor & Ceiling
    const floorG = new THREE.Mesh(new THREE.PlaneGeometry(20.0, 16.0), Mat.floorWingI);
    floorG.rotation.x = -Math.PI / 2; floorG.position.set(18.0, 0, 60.0); floorG.receiveShadow = true;
    const ceilG = new THREE.Mesh(new THREE.PlaneGeometry(20.0, 16.0), Mat.ceilingWingI);
    ceilG.rotation.x = Math.PI / 2; ceilG.position.set(18.0, H_WING, 60.0);
    wing.add(floorG, ceilG);
    const benchG = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchG.position.set(18.0, 0, 60.0); wing.add(benchG);
    addRotatedBoxCollider(18.0, 60.0, 1.75, 0.55, 0);

    // C. West Chamber Floor & Ceiling
    const floorP = new THREE.Mesh(new THREE.PlaneGeometry(20.0, 16.0), Mat.floorWingI);
    floorP.rotation.x = -Math.PI / 2; floorP.position.set(-18.0, 0, 60.0); floorP.receiveShadow = true;
    const ceilP = new THREE.Mesh(new THREE.PlaneGeometry(20.0, 16.0), Mat.ceilingWingI);
    ceilP.rotation.x = Math.PI / 2; ceilP.position.set(-18.0, H_WING, 60.0);
    wing.add(floorP, ceilP);
    const benchP = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchP.position.set(-18.0, 0, 60.0); wing.add(benchP);
    addRotatedBoxCollider(-18.0, 60.0, 1.75, 0.55, 0);

    // D. North Grand Hall: Master Storyboard Floor & Ceiling
    const floorS = new THREE.Mesh(new THREE.PlaneGeometry(56.0, 24.0), Mat.floorWingI);
    floorS.rotation.x = -Math.PI / 2; floorS.position.set(0, 0, 80.0); floorS.receiveShadow = true;
    const ceilS = new THREE.Mesh(new THREE.PlaneGeometry(56.0, 24.0), Mat.ceilingWingI);
    ceilS.rotation.x = Math.PI / 2; ceilS.position.set(0, H_WING, 80.0);
    wing.add(floorS, ceilS);
    const benchS1 = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchS1.position.set(0, 0, 80.0); wing.add(benchS1); addRotatedBoxCollider(0, 80.0, 1.75, 0.55, 0);
    const benchS2 = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchS2.position.set(-14.0, 0, 80.0); wing.add(benchS2); addRotatedBoxCollider(-14.0, 80.0, 1.75, 0.55, 0);
    const benchS3 = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchS3.position.set(14.0, 0, 80.0); wing.add(benchS3); addRotatedBoxCollider(14.0, 80.0, 1.75, 0.55, 0);
  }

  buildWingI();
  buildWingII();
  buildWingIII();
  buildWingIV();

  rotunda_group.add(root);
  scene.add(rotunda_group, wingI_group, wingII_group, wingIII_group, wingIV_group);
}"""

# ----------------------------------------------------------------------------
# 3. New buildPictureFrame with matrix updates & warm luminous canvas
# ----------------------------------------------------------------------------
new_build_pic_frame = """function buildPictureFrame(exhibit, width, height) {
  const group = new THREE.Group();

  const isLandscape = exhibit.orientation === 'landscape';
  const artW = width || (isLandscape ? 2.6 : 1.95);
  const artH = height || (isLandscape ? 1.95 : 2.6);
  const frameDepth = 0.12;

  let frameMat = Mat.goldLeaf;
  if (exhibit.wing === 'II') frameMat = Mat.darkWood;
  if (exhibit.wing === 'III') frameMat = Mat.pedestal;
  if (exhibit.wing === 'IV') frameMat = Mat.bronze;

  // Frame back
  const backGeo = isLandscape ? FrameGeoCache.backLandscape : FrameGeoCache.backPortrait;
  const frameBack = new THREE.Mesh(backGeo, frameMat);
  frameBack.matrixAutoUpdate = false;
  frameBack.updateMatrix();
  group.add(frameBack);

  // Inner beveled liner
  const linerMat = exhibit.wing === 'II' ? Mat.goldLeaf : Mat.alabaster;
  const linerGeo = isLandscape ? FrameGeoCache.linerLandscape : FrameGeoCache.linerPortrait;
  const liner = new THREE.Mesh(linerGeo, linerMat);
  liner.matrixAutoUpdate = false;
  liner.updateMatrix();
  group.add(liner);

  // Canvas surface
  let artMat;
  if (exhibit.mediaType === 'video') {
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
    video.preload = 'metadata';

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

    // Self-illuminated warm canvas so the artwork is never dark or muddy
    artMat = new THREE.MeshStandardMaterial({
      map: fallbackTex,
      roughness: 0.35,
      metalness: 0.02,
      emissiveMap: fallbackTex,
      emissive: new THREE.Color(0x484848),
      emissiveIntensity: 0.90
    });

    if (exhibit.imagePath) {
      loadTracker.total++;
      TextureLoadQueue.enqueue(
        exhibit.imagePath,
        (loadedTex) => {
          loadedTex.colorSpace = THREE.SRGBColorSpace;
          loadedTex.generateMipmaps = false;
          loadedTex.minFilter = THREE.LinearFilter;
          loadedTex.magFilter = THREE.LinearFilter;
          loadedTex.anisotropy = Math.min(4, MAX_ANISO);
          artMat.map = loadedTex;
          artMat.emissiveMap = loadedTex;
          artMat.emissive = new THREE.Color(0x484848);
          artMat.emissiveIntensity = 0.90;
          artMat.needsUpdate = true;
          fallbackTex.dispose();
          loadTracker.done++;
          loadTracker.ok++;
          updateLoadStatus();
        },
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
  });
  plaqueTex.generateMipmaps = false;
  plaqueTex.minFilter = THREE.LinearFilter;

  const plaqueMesh = new THREE.Mesh(
    FrameGeoCache.plaque,
    new THREE.MeshStandardMaterial({ map: plaqueTex, roughness: 0.35 })
  );
  plaqueMesh.position.set(0, -artH / 2 - 0.34, frameDepth / 2);
  plaqueMesh.matrixAutoUpdate = false;
  plaqueMesh.updateMatrix();
  group.add(plaqueMesh);

  // Small brass light fixture geometry above frame with warm glowing filament
  const fixtureBar = new THREE.Mesh(FrameGeoCache.fixtureBar, Mat.bronze);
  fixtureBar.position.set(0, artH / 2 + 0.32, 0.35);
  fixtureBar.matrixAutoUpdate = false;
  fixtureBar.updateMatrix();

  const fixtureHood = new THREE.Mesh(FrameGeoCache.fixtureHood, Mat.bronze);
  fixtureHood.position.set(0, artH / 2 + 0.35, 0.35);
  fixtureHood.matrixAutoUpdate = false;
  fixtureHood.updateMatrix();

  const stemL = new THREE.Mesh(FrameGeoCache.stem, Mat.bronze);
  stemL.rotation.x = Math.PI / 3; stemL.position.set(-0.25, artH / 2 + 0.18, 0.18);
  stemL.matrixAutoUpdate = false;
  stemL.updateMatrix();

  const stemR = new THREE.Mesh(FrameGeoCache.stem, Mat.bronze);
  stemR.rotation.x = Math.PI / 3; stemR.position.set(0.25, artH / 2 + 0.18, 0.18);
  stemR.matrixAutoUpdate = false;
  stemR.updateMatrix();

  const lampBulb = new THREE.Mesh(FrameGeoCache.lampBulb, new THREE.MeshBasicMaterial({ color: 0xfff6d0 }));
  lampBulb.position.set(0, artH / 2 + 0.32, 0.33);
  lampBulb.matrixAutoUpdate = false;
  lampBulb.updateMatrix();

  group.add(fixtureBar, fixtureHood, stemL, stemR, lampBulb);

  return { group, artCanvasMesh, artW, artH };
}"""

# ----------------------------------------------------------------------------
# 4. New buildLighting with visitor lantern on camera
# ----------------------------------------------------------------------------
new_build_lighting = """function buildLighting() {
  // Balanced ambient baseline - moody and gloomy gallery atmosphere as requested
  const hemi = new THREE.HemisphereLight(0xdcd0bc, 0x000808, 0.30);
  scene.add(hemi);

  const amb = new THREE.AmbientLight(0xfbf2e4, 0.24);
  scene.add(amb);

  // Dedicated warm visitor lantern attached to player - smoothly illuminates whichever artwork or wall the player approaches
  const visitorLantern = new THREE.PointLight(0xffeed4, 1.25, 9.0, 1.4);
  camera.add(visitorLantern);
  scene.add(camera);

  // Grand Rotunda central skylight chandelier illumination
  const rotundaSun = new THREE.SpotLight(0xffeaad, 36, 22, Math.PI / 3.2, 0.65, 1.2);
  rotundaSun.position.set(0, H_ROT + 1.2, 0);
  rotundaSun.target.position.set(0, 0, 0);
  rotundaSun.castShadow = true;
  rotundaSun.shadow.mapSize.width = 1024;
  rotundaSun.shadow.mapSize.height = 1024;
  rotundaSun.shadow.bias = -0.0004;
  rotunda_group.add(rotundaSun, rotundaSun.target);

  // Rotunda subtle perimeter accent lights
  for (let i = 0; i < 4; i++) {
    const a = (i / 4) * TAU + Math.PI / 4;
    const pl = new THREE.PointLight(0xffd599, 2.4, 8, 1.4);
    pl.position.set(Math.cos(a) * 5.2, 4.2, Math.sin(a) * 5.2);
    rotunda_group.add(pl);
  }

  // --- Wing I Dedicated Chamber Lights ---
  [
    { x: 26.0, y: 4.5, z: 0, color: 0xffd8b0, int: 2.8, dist: 22 }, // Promenade
    { x: 52.0, y: 4.5, z: 13.5, color: 0xffd8b0, int: 2.5, dist: 18 }, // North Salon
    { x: 52.0, y: 4.5, z: -13.5, color: 0xffd8b0, int: 2.5, dist: 18 } // South Studio
  ].forEach(p => {
    const l = new THREE.PointLight(p.color, p.int, p.dist, 1.4);
    l.position.set(p.x, p.y, p.z);
    wingI_group.add(l);
  });

  // --- Wing II Dedicated Chamber Lights ---
  [
    { x: 0, y: 4.5, z: 26.0, color: 0xf5f0e6, int: 2.8, dist: 24 }, // Promenade
    { x: 12.0, y: 4.5, z: 20.0, color: 0xf5f0e6, int: 2.4, dist: 16 }, // Room A (Env)
    { x: -12.0, y: 4.5, z: 20.0, color: 0xf5f0e6, int: 2.4, dist: 16 }, // Room B (Interior)
    { x: 12.0, y: 4.5, z: 38.0, color: 0xf5f0e6, int: 2.4, dist: 16 }, // Room C (VFX Cinema)
    { x: -12.0, y: 4.5, z: 38.0, color: 0xf5f0e6, int: 2.4, dist: 16 }  // Room D (Still Life)
  ].forEach(p => {
    const l = new THREE.PointLight(p.color, p.int, p.dist, 1.4);
    l.position.set(p.x, p.y, p.z);
    wingII_group.add(l);
  });

  // --- Wing III Dedicated Chamber Lights ---
  [
    { x: -26.0, y: 4.5, z: 0, color: 0x90a8d4, int: 2.2, dist: 22 }, // Boulevard East
    { x: -52.0, y: 4.5, z: 0, color: 0x90a8d4, int: 2.2, dist: 22 }, // Boulevard West
    { x: -35.0, y: 4.5, z: 13.5, color: 0xb0c8f5, int: 2.4, dist: 18 }, // Lunar Observatory
    { x: -35.0, y: 4.5, z: -13.5, color: 0xffdfb8, int: 2.4, dist: 18 }, // Wildlife Sanctuary
    { x: -55.0, y: 4.5, z: 13.5, color: 0xffecd2, int: 2.4, dist: 18 }, // Editorial Portraiture
    { x: -55.0, y: 4.5, z: -13.5, color: 0xffd5b0, int: 2.4, dist: 18 }  // Materiality Studies
  ].forEach(p => {
    const l = new THREE.PointLight(p.color, p.int, p.dist, 1.4);
    l.position.set(p.x, p.y, p.z);
    wingIII_group.add(l);
  });

  // --- Wing IV Dedicated Chamber Lights ---
  [
    { x: 0, y: 4.5, z: 60.0, color: 0xffe4a0, int: 2.8, dist: 20 }, // Cinema Atrium
    { x: 18.0, y: 4.5, z: 60.0, color: 0xffeedd, int: 2.6, dist: 18 }, // East Chamber (Graphics)
    { x: -18.0, y: 4.5, z: 60.0, color: 0xffeedd, int: 2.6, dist: 18 }, // West Chamber (Production)
    { x: 0, y: 4.5, z: 80.0, color: 0xffd8b0, int: 3.0, dist: 24 }  // North Hall (Storyboards)
  ].forEach(p => {
    const l = new THREE.PointLight(p.color, p.int, p.dist, 1.4);
    l.position.set(p.x, p.y, p.z);
    wingIV_group.add(l);
  });
}"""

# ----------------------------------------------------------------------------
# 5. New Video Streaming in animate (throttled, max 2 active videos)
# ----------------------------------------------------------------------------
old_vid_marker = "// Hogwarts video proximity streaming (play only within 26m)"
idx_vid_start = html.find(old_vid_marker)
assert idx_vid_start != -1, "Could not find video streaming block in animate"

idx_vid_end = html.find("// 5. Render Scene", idx_vid_start)
assert idx_vid_end != -1, "Could not find // 5. Render Scene"

new_vid_loop = """// Hogwarts video proximity streaming (throttled, max 2 closest concurrent videos within 10m)
  const nowMs = performance.now();
  if (nowMs - lastVideoCheckTime > 250) {
    lastVideoCheckTime = nowMs;
    const candidates = [];
    for (let vi = 0; vi < activeHogwartsVideos.length; vi++) {
      const hv = activeHogwartsVideos[vi];
      const dSq = hv.group.position.distanceToSquared(camera.position);
      if (dSq < 100.0) { // within 10 meters
        candidates.push({ hv, dSq });
      } else {
        if (!hv.video.paused) hv.video.pause();
      }
    }
    candidates.sort((a, b) => a.dSq - b.dSq);
    for (let ci = 0; ci < candidates.length; ci++) {
      const { hv } = candidates[ci];
      if (ci < 2) {
        if (hv.video.paused) {
          hv.video.muted = true;
          hv.video.volume = 0;
          hv.video.play().catch(() => {});
        }
      } else {
        if (!hv.video.paused) hv.video.pause();
      }
    }
  }

  """

# Apply animate video loop replacement
html = html[:idx_vid_start] + new_vid_loop + html[idx_vid_end:]
print("1. Replaced video streaming loop in animate!")

# Define let lastVideoCheckTime = 0; if not present
if "let lastVideoCheckTime = 0;" not in html:
    html = html.replace("const activeHogwartsVideos = [];", "const activeHogwartsVideos = [];\nlet lastVideoCheckTime = 0;")
    print("2. Added lastVideoCheckTime definition!")

# Replace buildLighting
start_light = html.find('function buildLighting() {')
end_light = html.find('\n}\n\n/* --------------------------------------------------------------------------\n   4.12', start_light)
assert start_light != -1 and end_light != -1, "Could not find buildLighting"
html = html[:start_light] + new_build_lighting + html[end_light + 2:]
print("3. Replaced buildLighting with visitor lantern!")

# Replace buildPictureFrame and add TextureLoadQueue before it
start_pic = html.find('function buildPictureFrame(exhibit, width, height) {')
ret_pic = html.find('return { group, artCanvasMesh, artW, artH };\n}', start_pic)
assert start_pic != -1 and ret_pic != -1, "Could not find buildPictureFrame"
end_pic = ret_pic + len('return { group, artCanvasMesh, artW, artH };\n}')

html = html[:start_pic] + queue_code + "\n" + new_build_pic_frame + html[end_pic:]
print("4. Replaced buildPictureFrame and added TextureLoadQueue!")

# Replace buildArchitecture
start_arch = html.find('function buildArchitecture() {')
close_wingIV = html.find('buildWingIV();', start_arch)
end_arch = html.find('\n}\n\n/* -------------', close_wingIV)
assert start_arch != -1 and end_arch != -1, "Could not find buildArchitecture"

html = html[:start_arch] + new_build_arch + html[end_arch + 2:]
print("5. Replaced buildArchitecture with solid drywall partitions across all wings!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html updated successfully with complete walls, lighting, and performance upgrades!")

