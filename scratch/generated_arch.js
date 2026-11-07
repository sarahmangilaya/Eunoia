  /* ==========================================================================
     §4.9 MUSEUM ARCHITECTURE (4 GRAND WINGS & SPECIALIZED CHAMBERS)
     ========================================================================== */

  // Helper: Build Grand Doorway Archway between Galleries
  function buildGalleryPortal({ x, z, rotY = 0, width = 6.0, label, sub }) {
    const g = new THREE.Group();
    g.position.set(x, 0, z);
    g.rotation.y = rotY;

    // Lintel beam above opening
    const lintelH = H_WING - 3.8;
    const lintel = new THREE.Mesh(new THREE.BoxGeometry(width, lintelH, 0.4), Mat.archTrim);
    lintel.position.set(0, 3.8 + lintelH / 2, 0);

    // Fluted pilaster columns flanking doorway
    const colL = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 3.8, 16), Mat.flutedColumn);
    colL.position.set(-width / 2 + 0.24, 1.9, 0);
    const colR = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 3.8, 16), Mat.flutedColumn);
    colR.position.set(width / 2 - 0.24, 1.9, 0);

    // Front Sign
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

  /* --- 2.1 Wing I: The Classical & Fine Arts Wing (29 Works) --- */
  function buildWingI() {
    const wing = new THREE.Group();
    const ox = R_ROT - 0.2, oz = 0; // ox = 8.3

    // A. Central Promenade (x in [8.3, 44.3], z in [-5.0, 5.0])
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

    // Portal flanking return colliders
    addWallSegment(ox, -5.0, ox, -1.50);
    addWallSegment(ox, 1.50, ox, 5.0);

    // Promenade Continuous Side Walls (z = 5.0 and z = -5.0)
    const wallNorthP = new THREE.Mesh(new THREE.PlaneGeometry(promLen, H_WING), Mat.wallWingI);
    wallNorthP.rotation.y = Math.PI; wallNorthP.position.set(ox + promLen / 2, H_WING / 2, 5.0);
    const wallSouthP = new THREE.Mesh(new THREE.PlaneGeometry(promLen, H_WING), Mat.wallWingI);
    wallSouthP.position.set(ox + promLen / 2, H_WING / 2, -5.0);
    wing.add(wallNorthP, wallSouthP);

    addWallSegment(ox, 5.0, ox + promLen, 5.0);
    addWallSegment(ox, -5.0, ox + promLen, -5.0);

    // Viewing benches along Promenade
    const benchP1 = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchP1.position.set(20.0, 0, 0); wing.add(benchP1);
    addRotatedBoxCollider(20.0, 0, 1.75, 0.55, 0);
    const benchP2 = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchP2.position.set(34.0, 0, 0); wing.add(benchP2);
    addRotatedBoxCollider(34.0, 0, 1.75, 0.55, 0);

    // B. Vestibule & T-Junction (x in [44.3, 58.0], z in [-5.0, 5.0])
    const vestLen = 13.7;
    const floorV = new THREE.Mesh(new THREE.PlaneGeometry(vestLen, promW), Mat.floorWingI);
    floorV.rotation.x = -Math.PI / 2; floorV.position.set(44.3 + vestLen / 2, 0, 0); floorV.receiveShadow = true;
    const ceilV = new THREE.Mesh(new THREE.PlaneGeometry(vestLen, promW), Mat.ceilingWingI);
    ceilV.rotation.x = Math.PI / 2; ceilV.position.set(44.3 + vestLen / 2, H_WING, 0);
    wing.add(floorV, ceilV);

    // East End Wall at x = 58.0
    const wallEastV = new THREE.Mesh(new THREE.PlaneGeometry(promW, H_WING), Mat.wallWingI);
    wallEastV.rotation.y = -Math.PI / 2; wallEastV.position.set(58.0, H_WING / 2, 0); wing.add(wallEastV);
    addWallSegment(58.0, -5.0, 58.0, 5.0);

    // East End Wall Console Table & classical urn
    const consoleTable = new THREE.Mesh(new RoundedBoxGeometry(2.4, 0.9, 0.6, 3, 0.03), Mat.darkWood);
    consoleTable.position.set(57.5, 0.45, 0); consoleTable.rotation.y = -Math.PI / 2; consoleTable.castShadow = true;
    const urn = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.18, 0.7, 16), Mat.goldLeaf);
    urn.position.set(57.5, 1.25, 0); urn.castShadow = true;
    wing.add(consoleTable, urn);
    addRotatedBoxCollider(57.5, 0, 1.35, 0.45, Math.PI / 2);

    // North Portal to Traditional Salon (Opening x in [48.0, 54.0] at z = 5.0)
    const portTrad = buildGalleryPortal({ x: 51.0, z: 5.0, rotY: 0, width: 6.0, label: 'TRADITIONAL FINE ART SALON', sub: 'Life Studies · Academic Plates · Anatomical Mastery' });
    wing.add(portTrad);
    addWallSegment(44.3, 5.0, 48.0, 5.0);
    addWallSegment(54.0, 5.0, 58.0, 5.0);

    // South Portal to Character Studio (Opening x in [48.0, 54.0] at z = -5.0)
    const portChar = buildGalleryPortal({ x: 51.0, z: -5.0, rotY: Math.PI, width: 6.0, label: '2D CHARACTER ANATOMY STUDIO', sub: 'Figure Proportions · Model Sheets & Design Plates' });
    wing.add(portChar);
    addWallSegment(44.3, -5.0, 48.0, -5.0);
    addWallSegment(54.0, -5.0, 58.0, -5.0);

    // C. North Salon: Traditional Fine Art (x in [44.0, 60.0], z in [5.0, 22.0], 16m x 17m)
    const salLen = 16.0, salD = 17.0;
    const floorSal = new THREE.Mesh(new THREE.PlaneGeometry(salLen, salD), Mat.floorWingI);
    floorSal.rotation.x = -Math.PI / 2; floorSal.position.set(52.0, 0, 13.5); floorSal.receiveShadow = true;
    const ceilSal = new THREE.Mesh(new THREE.PlaneGeometry(salLen, salD), Mat.ceilingWingI);
    ceilSal.rotation.x = Math.PI / 2; ceilSal.position.set(52.0, H_WING, 13.5);
    wing.add(floorSal, ceilSal);

    const wallSalW = new THREE.Mesh(new THREE.PlaneGeometry(salD, H_WING), Mat.wallWingI);
    wallSalW.rotation.y = Math.PI / 2; wallSalW.position.set(44.0, H_WING / 2, 13.5);
    const wallSalN = new THREE.Mesh(new THREE.PlaneGeometry(salLen, H_WING), Mat.wallWingI);
    wallSalN.rotation.y = Math.PI; wallSalN.position.set(52.0, H_WING / 2, 22.0);
    const wallSalE = new THREE.Mesh(new THREE.PlaneGeometry(salD, H_WING), Mat.wallWingI);
    wallSalE.rotation.y = -Math.PI / 2; wallSalE.position.set(60.0, H_WING / 2, 13.5);
    wing.add(wallSalW, wallSalN, wallSalE);

    addWallSegment(44.0, 5.0, 44.0, 22.0);  // West wall
    addWallSegment(44.0, 22.0, 60.0, 22.0); // North wall
    addWallSegment(60.0, 22.0, 60.0, 5.0);  // East wall
    addWallSegment(44.0, 5.0, 48.0, 5.0);   // South return L
    addWallSegment(54.0, 5.0, 60.0, 5.0);   // South return R

    const benchSal = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchSal.position.set(52.0, 0, 13.5); wing.add(benchSal);
    addRotatedBoxCollider(52.0, 13.5, 1.75, 0.55, 0);

    // D. South Studio: 2D Character Anatomy (x in [44.0, 60.0], z in [-22.0, -5.0], 16m x 17m)
    const floorChar = new THREE.Mesh(new THREE.PlaneGeometry(salLen, salD), Mat.floorWingI);
    floorChar.rotation.x = -Math.PI / 2; floorChar.position.set(52.0, 0, -13.5); floorChar.receiveShadow = true;
    const ceilChar = new THREE.Mesh(new THREE.PlaneGeometry(salLen, salD), Mat.ceilingWingI);
    ceilChar.rotation.x = Math.PI / 2; ceilChar.position.set(52.0, H_WING, -13.5);
    wing.add(floorChar, ceilChar);

    const wallCharW = new THREE.Mesh(new THREE.PlaneGeometry(salD, H_WING), Mat.wallWingI);
    wallCharW.rotation.y = Math.PI / 2; wallCharW.position.set(44.0, H_WING / 2, -13.5);
    const wallCharS = new THREE.Mesh(new THREE.PlaneGeometry(salLen, H_WING), Mat.wallWingI);
    wallCharS.position.set(52.0, H_WING / 2, -22.0);
    const wallCharE = new THREE.Mesh(new THREE.PlaneGeometry(salD, H_WING), Mat.wallWingI);
    wallCharE.rotation.y = -Math.PI / 2; wallCharE.position.set(60.0, H_WING / 2, -13.5);
    wing.add(wallCharW, wallCharS, wallCharE);

    addWallSegment(44.0, -5.0, 44.0, -22.0);  // West wall
    addWallSegment(44.0, -22.0, 60.0, -22.0); // South wall
    addWallSegment(60.0, -22.0, 60.0, -5.0);  // East wall
    addWallSegment(44.0, -5.0, 48.0, -5.0);   // North return L
    addWallSegment(54.0, -5.0, 60.0, -5.0);   // North return R

    const benchChar = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchChar.position.set(52.0, 0, -13.5); wing.add(benchChar);
    addRotatedBoxCollider(52.0, -13.5, 1.75, 0.55, 0);

    root.add(wing);
  }

  /* --- 2.2 Wing II: The 3D Virtual Worlds Pavilion (38 Works) --- */
  function buildWingII() {
    const wing = new THREE.Group();
    const ox = 0, oz = R_ROT - 0.2; // oz = 8.3
    const length = 43.7; // Spans z = 8.3 to 52.0
    const hw = 4.0;

    // Central Promenade Floor & Ceiling
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

    addWallSegment(-hw, oz, -1.50, oz);
    addWallSegment(1.50, oz, hw, oz);

    // Promenade Pier Walls
    const wallL1 = new THREE.Mesh(new THREE.PlaneGeometry(6.2, H_WING), Mat.wallWingII);
    wallL1.rotation.y = Math.PI / 2; wallL1.position.set(-hw, H_WING / 2, 8.3 + 3.1);
    const wallL2 = new THREE.Mesh(new THREE.PlaneGeometry(17.5, H_WING), Mat.wallWingII);
    wallL2.rotation.y = Math.PI / 2; wallL2.position.set(-hw, H_WING / 2, 20.5 + 8.75);
    const wallL3 = new THREE.Mesh(new THREE.PlaneGeometry(8.0, H_WING), Mat.wallWingII);
    wallL3.rotation.y = Math.PI / 2; wallL3.position.set(-hw, H_WING / 2, 44.0 + 4.0);

    const wallR1 = new THREE.Mesh(new THREE.PlaneGeometry(6.2, H_WING), Mat.wallWingII);
    wallR1.rotation.y = -Math.PI / 2; wallR1.position.set(hw, H_WING / 2, 8.3 + 3.1);
    const wallR2 = new THREE.Mesh(new THREE.PlaneGeometry(17.5, H_WING), Mat.wallWingII);
    wallR2.rotation.y = -Math.PI / 2; wallR2.position.set(hw, H_WING / 2, 20.5 + 8.75);
    const wallR3 = new THREE.Mesh(new THREE.PlaneGeometry(8.0, H_WING), Mat.wallWingII);
    wallR3.rotation.y = -Math.PI / 2; wallR3.position.set(hw, H_WING / 2, 44.0 + 4.0);
    wing.add(wallL1, wallL2, wallL3, wallR1, wallR2, wallR3);

    // Chamber Doorway Portals (6m wide openings)
    const portalA = buildGalleryPortal({ x: -hw, z: 17.5, rotY: Math.PI / 2, width: 6.0, label: '3D ENVIRONMENT GALLERY', sub: 'Exterior Worlds · Architecture · PBR Illumination' });
    const portalB = buildGalleryPortal({ x: hw, z: 17.5, rotY: -Math.PI / 2, width: 6.0, label: '3D INTERIOR ARCHITECTURE', sub: 'Spatial Layouts · Materiality & Raytracing' });
    const portalC = buildGalleryPortal({ x: -hw, z: 41.0, rotY: Math.PI / 2, width: 6.0, label: '3D VFX THEATRE', sub: 'Dynamic Simulations · Fluids & Particles' });
    const portalD = buildGalleryPortal({ x: hw, z: 41.0, rotY: -Math.PI / 2, width: 6.0, label: '3D STILL LIFE & PROP RENDER', sub: 'Studio Lighting · Microfacet Shading' });
    wing.add(portalA, portalB, portalC, portalD);

    // Portal to Wing IV at z = 52.0
    const portToIV = buildGalleryPortal({ x: 0, z: 52.0, rotY: 0, width: 4.0, label: 'WING IV · THE KINEMATIC PAVILION', sub: 'Animation, Storyboards & Applied Graphic Design' });
    wing.add(portToIV);
    addWallSegment(-hw, 52.0, -2.0, 52.0);
    addWallSegment(2.0, 52.0, hw, 52.0);

    // Pier Colliders along Promenade
    addWallSegment(-hw, 8.3, -hw, 14.5);
    addWallSegment(-hw, 20.5, -hw, 38.0);
    addWallSegment(-hw, 44.0, -hw, 52.0);

    addWallSegment(hw, 8.3, hw, 14.5);
    addWallSegment(hw, 20.5, hw, 38.0);
    addWallSegment(hw, 44.0, hw, 52.0);

    // Helper: Build Spacious 18m x 16m Chamber
    function buildRoom({ xMin, xMax, zMin, zMax, openSide, openZ1, openZ2, benchMat, floorMat = Mat.floorWingII, wallMat = Mat.wallWingII }) {
      const rw = xMax - xMin, rd = zMax - zMin;
      const cx = (xMin + xMax) / 2, cz = (zMin + zMax) / 2;

      const f = new THREE.Mesh(new THREE.PlaneGeometry(rw, rd), floorMat);
      f.rotation.x = -Math.PI / 2; f.position.set(cx, 0, cz); f.receiveShadow = true;
      const c = new THREE.Mesh(new THREE.PlaneGeometry(rw, rd), Mat.ceilingWingII);
      c.rotation.x = Math.PI / 2; c.position.set(cx, H_WING, cz);
      wing.add(f, c);

      // North wall (z = zMax)
      const wN = new THREE.Mesh(new THREE.PlaneGeometry(rw, H_WING), wallMat);
      wN.rotation.y = Math.PI; wN.position.set(cx, H_WING / 2, zMax);
      // South wall (z = zMin)
      const wS = new THREE.Mesh(new THREE.PlaneGeometry(rw, H_WING), wallMat);
      wS.position.set(cx, H_WING / 2, zMin);
      wing.add(wN, wS);
      addWallSegment(xMin, zMax, xMax, zMax);
      addWallSegment(xMin, zMin, xMax, zMin);

      // Outer side wall (opposite to opening)
      if (openSide === 'east') {
        const wW = new THREE.Mesh(new THREE.PlaneGeometry(rd, H_WING), wallMat);
        wW.rotation.y = Math.PI / 2; wW.position.set(xMin, H_WING / 2, cz);
        wing.add(wW);
        addWallSegment(xMin, zMin, xMin, zMax);
        // East side has opening
        addWallSegment(xMax, zMin, xMax, openZ1);
        addWallSegment(xMax, openZ2, xMax, zMax);
      } else {
        const wE = new THREE.Mesh(new THREE.PlaneGeometry(rd, H_WING), wallMat);
        wE.rotation.y = -Math.PI / 2; wE.position.set(xMax, H_WING / 2, cz);
        wing.add(wE);
        addWallSegment(xMax, zMin, xMax, zMax);
        // West side has opening
        addWallSegment(xMin, zMin, xMin, openZ1);
        addWallSegment(xMin, openZ2, xMin, zMax);
      }

      const bench = buildMuseumBench(Mat.darkWood, benchMat || Mat.blackVelvet);
      bench.position.set(cx, 0, cz); wing.add(bench);
      addRotatedBoxCollider(cx, cz, 1.75, 0.55, 0);
    }

    // Room A (Environment): x in [-22, -4], z in [9.5, 25.5]
    buildRoom({ xMin: -22.0, xMax: -4.0, zMin: 9.5, zMax: 25.5, openSide: 'east', openZ1: 14.5, openZ2: 20.5, benchMat: Mat.darkWood });
    // Room B (Interior): x in [4, 22], z in [9.5, 25.5]
    buildRoom({ xMin: 4.0, xMax: 22.0, zMin: 9.5, zMax: 25.5, openSide: 'west', openZ1: 14.5, openZ2: 20.5, benchMat: Mat.crimsonVelvet });
    // Room C (VFX): x in [-22, -4], z in [33, 49]
    buildRoom({ xMin: -22.0, xMax: -4.0, zMin: 33.0, zMax: 49.0, openSide: 'east', openZ1: 38.0, openZ2: 44.0, benchMat: Mat.blackVelvet });
    // Room D (Still Life): x in [4, 22], z in [33, 49]
    buildRoom({ xMin: 4.0, xMax: 22.0, zMin: 33.0, zMax: 49.0, openSide: 'west', openZ1: 38.0, openZ2: 44.0, benchMat: Mat.darkWood });

    root.add(wing);
  }

  /* --- 2.3 Wing III: The Nocturne & Observational Photography Gallery (86 Works) --- */
  function buildWingIII() {
    const wing = new THREE.Group();
    const ox = -(R_ROT - 0.2), oz = 0; // ox = -8.3
    const blvdLen = 59.7, blvdW = 10.0; // Spans x in [-68.0, -8.3]

    // Central Boulevard Floor & Ceiling
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

    addWallSegment(ox, -5.0, ox, -1.50);
    addWallSegment(ox, 1.50, ox, 5.0);

    // West End Wall at x = -68.0
    const wallWest = new THREE.Mesh(new THREE.PlaneGeometry(blvdW, H_WING), Mat.wallWingIII);
    wallWest.rotation.y = Math.PI / 2; wallWest.position.set(-68.0, H_WING / 2, 0); wing.add(wallWest);
    addWallSegment(-68.0, -5.0, -68.0, 5.0);

    // End-of-hall feature: Pedestal & Golden Lunar Sphere
    const noctPed = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.45, 1.0, 24), Mat.pedestal);
    noctPed.position.set(-66.8, 0.5, 0);
    const orb = new THREE.Mesh(new THREE.SphereGeometry(0.28, 24, 24), Mat.goldLeaf);
    orb.position.set(-66.8, 1.28, 0);
    wing.add(noctPed, orb);
    addCylCollider(-66.8, 0, 0.6);

    // North & South Portals (6m wide openings)
    const portLunar = buildGalleryPortal({ x: -35.0, z: 5.0, rotY: Math.PI, width: 6.0, label: 'LUNAR ASTROPHOTOGRAPHY OBSERVATORY', sub: 'Selenography · Deep Celestial Horizons · Moonlit Tonalities' });
    const portWild = buildGalleryPortal({ x: -35.0, z: -5.0, rotY: 0, width: 6.0, label: 'WILDLIFE & ANIMAL SANCTUARY', sub: 'Fauna Portraiture · Kinetic Instinct · Living Light' });
    const portPort = buildGalleryPortal({ x: -55.0, z: 5.0, rotY: Math.PI, width: 6.0, label: 'EDITORIAL & MODEL PORTRAITURE SALON', sub: 'Dramatic Key Lighting · Human Expressiveness' });
    const portStill = buildGalleryPortal({ x: -55.0, z: -5.0, rotY: 0, width: 6.0, label: 'STILL LIFE & OBSERVATIONAL OBJECTS', sub: 'Form, Shadow & Everyday Materiality' });
    wing.add(portLunar, portWild, portPort, portStill);

    // Boulevard North & South Wall Colliders
    addWallSegment(-8.3, 5.0, -32.0, 5.0);
    addWallSegment(-38.0, 5.0, -52.0, 5.0);
    addWallSegment(-58.0, 5.0, -68.0, 5.0);

    addWallSegment(-8.3, -5.0, -32.0, -5.0);
    addWallSegment(-38.0, -5.0, -52.0, -5.0);
    addWallSegment(-58.0, -5.0, -68.0, -5.0);

    // Boulevard Benches
    const bB1 = buildMuseumBench(Mat.pedestal, Mat.blackVelvet);
    bB1.position.set(-20.0, 0, 0); wing.add(bB1); addRotatedBoxCollider(-20.0, 0, 1.75, 0.55, 0);
    const bB2 = buildMuseumBench(Mat.pedestal, Mat.blackVelvet);
    bB2.position.set(-45.0, 0, 0); wing.add(bB2); addRotatedBoxCollider(-45.0, 0, 1.75, 0.55, 0);

    // Helper: Build Photography Chamber (18m x 18m)
    function buildPhotoChamber({ xMin, xMax, zMin, zMax, openZ, openX1, openX2 }) {
      const cw = xMax - xMin, cd = zMax - zMin;
      const cx = (xMin + xMax) / 2, cz = (zMin + zMax) / 2;

      const f = new THREE.Mesh(new THREE.PlaneGeometry(cw, cd), Mat.floorWingIII);
      f.rotation.x = -Math.PI / 2; f.position.set(cx, 0, cz); f.receiveShadow = true;
      const c = new THREE.Mesh(new THREE.PlaneGeometry(cw, cd), Mat.ceilingWingIII);
      c.rotation.x = Math.PI / 2; c.position.set(cx, H_WING, cz);
      wing.add(f, c);

      const wE = new THREE.Mesh(new THREE.PlaneGeometry(cd, H_WING), Mat.wallWingIII);
      wE.rotation.y = -Math.PI / 2; wE.position.set(xMax, H_WING / 2, cz);
      const wW = new THREE.Mesh(new THREE.PlaneGeometry(cd, H_WING), Mat.wallWingIII);
      wW.rotation.y = Math.PI / 2; wW.position.set(xMin, H_WING / 2, cz);
      wing.add(wE, wW);

      addWallSegment(xMax, zMin, xMax, zMax);
      addWallSegment(xMin, zMin, xMin, zMax);

      if (openZ < 0) {
        // Opens North, far wall is South (zMin)
        const wFar = new THREE.Mesh(new THREE.PlaneGeometry(cw, H_WING), Mat.wallWingIII);
        wFar.position.set(cx, H_WING / 2, zMin); wing.add(wFar);
        addWallSegment(xMin, zMin, xMax, zMin);
        addWallSegment(xMin, zMax, openX1, zMax);
        addWallSegment(openX2, zMax, xMax, zMax);
      } else {
        // Opens South, far wall is North (zMax)
        const wFar = new THREE.Mesh(new THREE.PlaneGeometry(cw, H_WING), Mat.wallWingIII);
        wFar.rotation.y = Math.PI; wFar.position.set(cx, H_WING / 2, zMax); wing.add(wFar);
        addWallSegment(xMin, zMax, xMax, zMax);
        addWallSegment(xMin, zMin, openX1, zMin);
        addWallSegment(openX2, zMin, xMax, zMin);
      }

      const bench = buildMuseumBench(Mat.pedestal, Mat.blackVelvet);
      bench.position.set(cx, 0, cz); wing.add(bench);
      addRotatedBoxCollider(cx, cz, 1.75, 0.55, 0);
    }

    // North Chamber 1: Lunar (x in [-46, -28], z in [5, 23])
    buildPhotoChamber({ xMin: -46.0, xMax: -28.0, zMin: 5.0, zMax: 23.0, openZ: 5.0, openX1: -38.0, openX2: -32.0 });
    // South Chamber 1: Wildlife (x in [-46, -28], z in [-23, -5])
    buildPhotoChamber({ xMin: -46.0, xMax: -28.0, zMin: -23.0, zMax: -5.0, openZ: -5.0, openX1: -38.0, openX2: -32.0 });
    // North Chamber 2: Portrait (x in [-66, -48], z in [5, 23])
    buildPhotoChamber({ xMin: -66.0, xMax: -48.0, zMin: 5.0, zMax: 23.0, openZ: 5.0, openX1: -58.0, openX2: -52.0 });
    // South Chamber 2: Materiality (x in [-66, -48], z in [-23, -5])
    buildPhotoChamber({ xMin: -66.0, xMax: -48.0, zMin: -23.0, zMax: -5.0, openZ: -5.0, openX1: -58.0, openX2: -52.0 });

    root.add(wing);
  }

  /* --- 2.4 Wing IV: The Kinematic & Applied Design Pavilion (52 Works) --- */
  function buildWingIV() {
    const wing = new THREE.Group();

    // A. Central Cinema Atrium (x in [-8.0, 8.0], z in [52.0, 68.0], 16m x 16m)
    const floorC = new THREE.Mesh(new THREE.PlaneGeometry(16.0, 16.0), Mat.floorWingI);
    floorC.rotation.x = -Math.PI / 2; floorC.position.set(0, 0, 60.0); floorC.receiveShadow = true;
    const ceilC = new THREE.Mesh(new THREE.PlaneGeometry(16.0, 16.0), Mat.ceilingWingI);
    ceilC.rotation.x = Math.PI / 2; ceilC.position.set(0, H_WING, 60.0);
    wing.add(floorC, ceilC);

    // Return Sign facing inside Cinema Atrium looking back towards Wing II
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

    // South wall returns flanking entrance portal from Wing II (z = 52.0)
    addWallSegment(-8.0, 52.0, -2.0, 52.0);
    addWallSegment(2.0, 52.0, 8.0, 52.0);

    // Doorways connecting to other Wing IV chambers
    const portGraphic = buildGalleryPortal({ x: 8.0, z: 60.0, rotY: -Math.PI / 2, width: 4.0, label: 'APPLIED GRAPHIC DESIGN & BRAND IDENTITY', sub: 'Poster Typography · Brand Monograms · Atelier Jacquard Lanyards' });
    const portProd = buildGalleryPortal({ x: -8.0, z: 60.0, rotY: Math.PI / 2, width: 4.0, label: 'PRODUCTION DESIGN & ART DIRECTION', sub: 'Set Photography · Cinematic Scenography & Atmosphere' });
    const portStory = buildGalleryPortal({ x: 0, z: 68.0, rotY: 0, width: 6.0, label: 'MASTER STORYBOARD & PRE-VISUALIZATION', sub: 'The Wind Rises Adaptation · Dynamic Continuity & Cinematography' });
    wing.add(portGraphic, portProd, portStory);

    // Cinema Atrium Wall Colliders
    addWallSegment(8.0, 52.0, 8.0, 58.0);
    addWallSegment(8.0, 62.0, 8.0, 68.0);
    addWallSegment(-8.0, 52.0, -8.0, 58.0);
    addWallSegment(-8.0, 62.0, -8.0, 68.0);
    addWallSegment(-8.0, 68.0, -3.0, 68.0);
    addWallSegment(3.0, 68.0, 8.0, 68.0);

    // Cinema Viewing Bench
    const cinemaBench = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    cinemaBench.position.set(0, 0, 60.0); wing.add(cinemaBench);
    addRotatedBoxCollider(0, 60.0, 1.75, 0.55, 0);

    // B. East Chamber: Applied Graphic Design, Logos & Atelier Gallery (x in [8.0, 28.0], z in [52.0, 68.0], 20m x 16m)
    const floorG = new THREE.Mesh(new THREE.PlaneGeometry(20.0, 16.0), Mat.floorWingI);
    floorG.rotation.x = -Math.PI / 2; floorG.position.set(18.0, 0, 60.0); floorG.receiveShadow = true;
    const ceilG = new THREE.Mesh(new THREE.PlaneGeometry(20.0, 16.0), Mat.ceilingWingI);
    ceilG.rotation.x = Math.PI / 2; ceilG.position.set(18.0, H_WING, 60.0);
    wing.add(floorG, ceilG);

    const wallGSouth = new THREE.Mesh(new THREE.PlaneGeometry(20.0, H_WING), Mat.wallWingII);
    wallGSouth.position.set(18.0, H_WING / 2, 52.0);
    const wallGEast = new THREE.Mesh(new THREE.PlaneGeometry(16.0, H_WING), Mat.wallWingII);
    wallGEast.rotation.y = -Math.PI / 2; wallGEast.position.set(28.0, H_WING / 2, 60.0);
    const wallGNorth = new THREE.Mesh(new THREE.PlaneGeometry(20.0, H_WING), Mat.wallWingII);
    wallGNorth.rotation.y = Math.PI; wallGNorth.position.set(18.0, H_WING / 2, 68.0);
    wing.add(wallGSouth, wallGEast, wallGNorth);

    addWallSegment(8.0, 52.0, 28.0, 52.0); // South wall
    addWallSegment(28.0, 52.0, 28.0, 68.0); // East wall
    addWallSegment(8.0, 68.0, 28.0, 68.0);  // North wall

    const benchG = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchG.position.set(18.0, 0, 60.0); wing.add(benchG);
    addRotatedBoxCollider(18.0, 60.0, 1.75, 0.55, 0);

    // C. West Chamber: Production Design & Art Direction Gallery (x in [-28.0, -8.0], z in [52.0, 68.0], 20m x 16m)
    const floorP = new THREE.Mesh(new THREE.PlaneGeometry(20.0, 16.0), Mat.floorWingI);
    floorP.rotation.x = -Math.PI / 2; floorP.position.set(-18.0, 0, 60.0); floorP.receiveShadow = true;
    const ceilP = new THREE.Mesh(new THREE.PlaneGeometry(20.0, 16.0), Mat.ceilingWingI);
    ceilP.rotation.x = Math.PI / 2; ceilP.position.set(-18.0, H_WING, 60.0);
    wing.add(floorP, ceilP);

    const wallPSouth = new THREE.Mesh(new THREE.PlaneGeometry(20.0, H_WING), Mat.wallWingII);
    wallPSouth.position.set(-18.0, H_WING / 2, 52.0);
    const wallPWest = new THREE.Mesh(new THREE.PlaneGeometry(16.0, H_WING), Mat.wallWingII);
    wallPWest.rotation.y = Math.PI / 2; wallPWest.position.set(-28.0, H_WING / 2, 60.0);
    const wallPNorth = new THREE.Mesh(new THREE.PlaneGeometry(20.0, H_WING), Mat.wallWingII);
    wallPNorth.rotation.y = Math.PI; wallPNorth.position.set(-18.0, H_WING / 2, 68.0);
    wing.add(wallPSouth, wallPWest, wallPNorth);

    addWallSegment(-28.0, 52.0, -8.0, 52.0); // South wall
    addWallSegment(-28.0, 52.0, -28.0, 68.0); // West wall
    addWallSegment(-28.0, 68.0, -8.0, 68.0);  // North wall

    const benchP = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchP.position.set(-18.0, 0, 60.0); wing.add(benchP);
    addRotatedBoxCollider(-18.0, 60.0, 1.75, 0.55, 0);

    // D. North Grand Hall: Master Storyboard & Sequence Pavilion (x in [-28.0, 28.0], z in [68.0, 92.0], 56m x 24m)
    const floorS = new THREE.Mesh(new THREE.PlaneGeometry(56.0, 24.0), Mat.floorWingI);
    floorS.rotation.x = -Math.PI / 2; floorS.position.set(0, 0, 80.0); floorS.receiveShadow = true;
    const ceilS = new THREE.Mesh(new THREE.PlaneGeometry(56.0, 24.0), Mat.ceilingWingI);
    ceilS.rotation.x = Math.PI / 2; ceilS.position.set(0, H_WING, 80.0);
    wing.add(floorS, ceilS);

    const wallSNorth = new THREE.Mesh(new THREE.PlaneGeometry(56.0, H_WING), Mat.wallWingII);
    wallSNorth.rotation.y = Math.PI; wallSNorth.position.set(0, H_WING / 2, 92.0);
    const wallSWest = new THREE.Mesh(new THREE.PlaneGeometry(24.0, H_WING), Mat.wallWingII);
    wallSWest.rotation.y = Math.PI / 2; wallSWest.position.set(-28.0, H_WING / 2, 80.0);
    const wallSEast = new THREE.Mesh(new THREE.PlaneGeometry(24.0, H_WING), Mat.wallWingII);
    wallSEast.rotation.y = -Math.PI / 2; wallSEast.position.set(28.0, H_WING / 2, 80.0);
    wing.add(wallSNorth, wallSWest, wallSEast);

    addWallSegment(-28.0, 92.0, 28.0, 92.0); // Grand North wall
    addWallSegment(-28.0, 68.0, -28.0, 92.0); // West wall
    addWallSegment(28.0, 68.0, 28.0, 92.0);  // East wall
    addWallSegment(-28.0, 68.0, -3.0, 68.0);  // South return L
    addWallSegment(3.0, 68.0, 28.0, 68.0);   // South return R

    const benchS1 = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchS1.position.set(0, 0, 80.0); wing.add(benchS1); addRotatedBoxCollider(0, 80.0, 1.75, 0.55, 0);
    const benchS2 = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchS2.position.set(-14.0, 0, 80.0); wing.add(benchS2); addRotatedBoxCollider(-14.0, 80.0, 1.75, 0.55, 0);
    const benchS3 = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchS3.position.set(14.0, 0, 80.0); wing.add(benchS3); addRotatedBoxCollider(14.0, 80.0, 1.75, 0.55, 0);

    root.add(wing);
  }

  // Build all 4 expanded wings
  buildWingI();
  buildWingII();
  buildWingIII();
  buildWingIV();

  scene.add(root);
}

/* --------------------------------------------------------------------------
   4.10  EXHIBIT SPOTS & COMPLETE 205-PIECE LAYOUT ENGINE
   -------------------------------------------------------------------------- */
const EXHIBIT_SPOTS = {
  "I_finearts_promenade": [
    {
      "x": 11.5,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": 11.5,
      "viewZ": 2.3
    },
    {
      "x": 15.5,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": 15.5,
      "viewZ": 2.3
    },
    {
      "x": 19.5,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": 19.5,
      "viewZ": 2.3
    },
    {
      "x": 23.5,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": 23.5,
      "viewZ": 2.3
    },
    {
      "x": 27.5,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": 27.5,
      "viewZ": 2.3
    },
    {
      "x": 31.5,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": 31.5,
      "viewZ": 2.3
    },
    {
      "x": 35.5,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": 35.5,
      "viewZ": 2.3
    },
    {
      "x": 39.5,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": 39.5,
      "viewZ": 2.3
    },
    {
      "x": 11.5,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": 11.5,
      "viewZ": -2.3
    },
    {
      "x": 15.5,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": 15.5,
      "viewZ": -2.3
    },
    {
      "x": 19.5,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": 19.5,
      "viewZ": -2.3
    },
    {
      "x": 23.5,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": 23.5,
      "viewZ": -2.3
    },
    {
      "x": 27.5,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": 27.5,
      "viewZ": -2.3
    },
    {
      "x": 31.5,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": 31.5,
      "viewZ": -2.3
    },
    {
      "x": 35.5,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": 35.5,
      "viewZ": -2.3
    },
    {
      "x": 39.5,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": 39.5,
      "viewZ": -2.3
    }
  ],
  "I_finearts_traditional": [
    {
      "x": 44.14,
      "y": 2.4,
      "z": 10.0,
      "rotY": 1.5707963267948966,
      "viewX": 46.8,
      "viewZ": 10.0
    },
    {
      "x": 44.14,
      "y": 2.4,
      "z": 16.5,
      "rotY": 1.5707963267948966,
      "viewX": 46.8,
      "viewZ": 16.5
    },
    {
      "x": 48.5,
      "y": 2.4,
      "z": 21.86,
      "rotY": 3.141592653589793,
      "viewX": 48.5,
      "viewZ": 19.2
    },
    {
      "x": 55.5,
      "y": 2.4,
      "z": 21.86,
      "rotY": 3.141592653589793,
      "viewX": 55.5,
      "viewZ": 19.2
    },
    {
      "x": 59.86,
      "y": 2.4,
      "z": 16.5,
      "rotY": -1.5707963267948966,
      "viewX": 57.2,
      "viewZ": 16.5
    },
    {
      "x": 59.86,
      "y": 2.4,
      "z": 10.0,
      "rotY": -1.5707963267948966,
      "viewX": 57.2,
      "viewZ": 10.0
    }
  ],
  "I_finearts_character": [
    {
      "x": 44.14,
      "y": 2.4,
      "z": -10.0,
      "rotY": 1.5707963267948966,
      "viewX": 46.8,
      "viewZ": -10.0
    },
    {
      "x": 44.14,
      "y": 2.4,
      "z": -16.5,
      "rotY": 1.5707963267948966,
      "viewX": 46.8,
      "viewZ": -16.5
    },
    {
      "x": 47.5,
      "y": 2.4,
      "z": -21.86,
      "rotY": 0,
      "viewX": 47.5,
      "viewZ": -19.2
    },
    {
      "x": 52.0,
      "y": 2.4,
      "z": -21.86,
      "rotY": 0,
      "viewX": 52.0,
      "viewZ": -19.2
    },
    {
      "x": 56.5,
      "y": 2.4,
      "z": -21.86,
      "rotY": 0,
      "viewX": 56.5,
      "viewZ": -19.2
    },
    {
      "x": 59.86,
      "y": 2.4,
      "z": -16.5,
      "rotY": -1.5707963267948966,
      "viewX": 57.2,
      "viewZ": -16.5
    },
    {
      "x": 59.86,
      "y": 2.4,
      "z": -10.0,
      "rotY": -1.5707963267948966,
      "viewX": 57.2,
      "viewZ": -10.0
    }
  ],
  "II_env": [
    {
      "x": -17.5,
      "y": 2.4,
      "z": 25.36,
      "rotY": 3.141592653589793,
      "viewX": -17.5,
      "viewZ": 22.8
    },
    {
      "x": -13.0,
      "y": 2.4,
      "z": 25.36,
      "rotY": 3.141592653589793,
      "viewX": -13.0,
      "viewZ": 22.8
    },
    {
      "x": -8.5,
      "y": 2.4,
      "z": 25.36,
      "rotY": 3.141592653589793,
      "viewX": -8.5,
      "viewZ": 22.8
    },
    {
      "x": -21.86,
      "y": 2.4,
      "z": 21.5,
      "rotY": 1.5707963267948966,
      "viewX": -19.2,
      "viewZ": 21.5
    },
    {
      "x": -21.86,
      "y": 2.4,
      "z": 17.5,
      "rotY": 1.5707963267948966,
      "viewX": -19.2,
      "viewZ": 17.5
    },
    {
      "x": -21.86,
      "y": 2.4,
      "z": 13.5,
      "rotY": 1.5707963267948966,
      "viewX": -19.2,
      "viewZ": 13.5
    },
    {
      "x": -17.5,
      "y": 2.4,
      "z": 9.64,
      "rotY": 0,
      "viewX": -17.5,
      "viewZ": 12.2
    },
    {
      "x": -13.0,
      "y": 2.4,
      "z": 9.64,
      "rotY": 0,
      "viewX": -13.0,
      "viewZ": 12.2
    },
    {
      "x": -8.5,
      "y": 2.4,
      "z": 9.64,
      "rotY": 0,
      "viewX": -8.5,
      "viewZ": 12.2
    }
  ],
  "II_interior": [
    {
      "x": 8.5,
      "y": 2.4,
      "z": 9.64,
      "rotY": 0,
      "viewX": 8.5,
      "viewZ": 12.2
    },
    {
      "x": 13.0,
      "y": 2.4,
      "z": 9.64,
      "rotY": 0,
      "viewX": 13.0,
      "viewZ": 12.2
    },
    {
      "x": 17.5,
      "y": 2.4,
      "z": 9.64,
      "rotY": 0,
      "viewX": 17.5,
      "viewZ": 12.2
    },
    {
      "x": 21.86,
      "y": 2.4,
      "z": 12.0,
      "rotY": -1.5707963267948966,
      "viewX": 19.2,
      "viewZ": 12.0
    },
    {
      "x": 21.86,
      "y": 2.4,
      "z": 15.5,
      "rotY": -1.5707963267948966,
      "viewX": 19.2,
      "viewZ": 15.5
    },
    {
      "x": 21.86,
      "y": 2.4,
      "z": 19.0,
      "rotY": -1.5707963267948966,
      "viewX": 19.2,
      "viewZ": 19.0
    },
    {
      "x": 21.86,
      "y": 2.4,
      "z": 22.5,
      "rotY": -1.5707963267948966,
      "viewX": 19.2,
      "viewZ": 22.5
    },
    {
      "x": 17.5,
      "y": 2.4,
      "z": 25.36,
      "rotY": 3.141592653589793,
      "viewX": 17.5,
      "viewZ": 22.8
    },
    {
      "x": 13.0,
      "y": 2.4,
      "z": 25.36,
      "rotY": 3.141592653589793,
      "viewX": 13.0,
      "viewZ": 22.8
    },
    {
      "x": 8.5,
      "y": 2.4,
      "z": 25.36,
      "rotY": 3.141592653589793,
      "viewX": 8.5,
      "viewZ": 22.8
    }
  ],
  "II_vfx": [
    {
      "x": -17.5,
      "y": 2.5,
      "z": 33.14,
      "rotY": 0,
      "viewX": -17.5,
      "viewZ": 35.8
    },
    {
      "x": -13.0,
      "y": 2.5,
      "z": 33.14,
      "rotY": 0,
      "viewX": -13.0,
      "viewZ": 35.8
    },
    {
      "x": -8.5,
      "y": 2.5,
      "z": 33.14,
      "rotY": 0,
      "viewX": -8.5,
      "viewZ": 35.8
    },
    {
      "x": -21.86,
      "y": 2.5,
      "z": 38.5,
      "rotY": 1.5707963267948966,
      "viewX": -19.2,
      "viewZ": 38.5
    },
    {
      "x": -21.86,
      "y": 2.5,
      "z": 43.5,
      "rotY": 1.5707963267948966,
      "viewX": -19.2,
      "viewZ": 43.5
    },
    {
      "x": -17.5,
      "y": 2.5,
      "z": 48.86,
      "rotY": 3.141592653589793,
      "viewX": -17.5,
      "viewZ": 46.2
    },
    {
      "x": -13.0,
      "y": 2.5,
      "z": 48.86,
      "rotY": 3.141592653589793,
      "viewX": -13.0,
      "viewZ": 46.2
    },
    {
      "x": -8.5,
      "y": 2.5,
      "z": 48.86,
      "rotY": 3.141592653589793,
      "viewX": -8.5,
      "viewZ": 46.2
    }
  ],
  "II_stilllife": [
    {
      "x": 13.0,
      "y": 2.4,
      "z": 33.14,
      "rotY": 0,
      "viewX": 13.0,
      "viewZ": 35.8
    },
    {
      "x": 21.86,
      "y": 2.4,
      "z": 38.5,
      "rotY": -1.5707963267948966,
      "viewX": 19.2,
      "viewZ": 38.5
    },
    {
      "x": 21.86,
      "y": 2.4,
      "z": 43.5,
      "rotY": -1.5707963267948966,
      "viewX": 19.2,
      "viewZ": 43.5
    },
    {
      "x": 13.0,
      "y": 2.4,
      "z": 48.86,
      "rotY": 3.141592653589793,
      "viewX": 13.0,
      "viewZ": 46.2
    }
  ],
  "II_char3d": [
    {
      "x": -3.86,
      "y": 2.4,
      "z": 11.0,
      "rotY": 1.5707963267948966,
      "viewX": -1.6,
      "viewZ": 11.0
    },
    {
      "x": -3.86,
      "y": 2.4,
      "z": 24.0,
      "rotY": 1.5707963267948966,
      "viewX": -1.6,
      "viewZ": 24.0
    },
    {
      "x": -3.86,
      "y": 2.4,
      "z": 35.0,
      "rotY": 1.5707963267948966,
      "viewX": -1.6,
      "viewZ": 35.0
    },
    {
      "x": 3.86,
      "y": 2.4,
      "z": 11.0,
      "rotY": -1.5707963267948966,
      "viewX": 1.6,
      "viewZ": 11.0
    },
    {
      "x": 3.86,
      "y": 2.4,
      "z": 24.0,
      "rotY": -1.5707963267948966,
      "viewX": 1.6,
      "viewZ": 24.0
    },
    {
      "x": 3.86,
      "y": 2.4,
      "z": 35.0,
      "rotY": -1.5707963267948966,
      "viewX": 1.6,
      "viewZ": 35.0
    },
    {
      "x": 0.0,
      "y": 2.1,
      "z": 28.0,
      "rotY": 0,
      "viewX": 0.0,
      "viewZ": 25.5
    }
  ],
  "III_street": [
    {
      "x": -12.0,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -12.0,
      "viewZ": 2.3
    },
    {
      "x": -15.0,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -15.0,
      "viewZ": 2.3
    },
    {
      "x": -18.0,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -18.0,
      "viewZ": 2.3
    },
    {
      "x": -21.0,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -21.0,
      "viewZ": 2.3
    },
    {
      "x": -24.0,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -24.0,
      "viewZ": 2.3
    },
    {
      "x": -27.0,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -27.0,
      "viewZ": 2.3
    },
    {
      "x": -30.0,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -30.0,
      "viewZ": 2.3
    },
    {
      "x": -40.0,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -40.0,
      "viewZ": 2.3
    },
    {
      "x": -43.0,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -43.0,
      "viewZ": 2.3
    },
    {
      "x": -46.0,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -46.0,
      "viewZ": 2.3
    },
    {
      "x": -49.0,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -49.0,
      "viewZ": 2.3
    },
    {
      "x": -51.0,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -51.0,
      "viewZ": 2.3
    },
    {
      "x": -59.5,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -59.5,
      "viewZ": 2.3
    },
    {
      "x": -62.5,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -62.5,
      "viewZ": 2.3
    },
    {
      "x": -65.5,
      "y": 2.4,
      "z": 4.86,
      "rotY": 3.141592653589793,
      "viewX": -65.5,
      "viewZ": 2.3
    },
    {
      "x": -12.0,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -12.0,
      "viewZ": -2.3
    },
    {
      "x": -15.0,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -15.0,
      "viewZ": -2.3
    },
    {
      "x": -18.0,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -18.0,
      "viewZ": -2.3
    },
    {
      "x": -21.0,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -21.0,
      "viewZ": -2.3
    },
    {
      "x": -24.0,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -24.0,
      "viewZ": -2.3
    },
    {
      "x": -27.0,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -27.0,
      "viewZ": -2.3
    },
    {
      "x": -30.0,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -30.0,
      "viewZ": -2.3
    },
    {
      "x": -40.0,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -40.0,
      "viewZ": -2.3
    },
    {
      "x": -43.0,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -43.0,
      "viewZ": -2.3
    },
    {
      "x": -46.0,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -46.0,
      "viewZ": -2.3
    },
    {
      "x": -49.0,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -49.0,
      "viewZ": -2.3
    },
    {
      "x": -51.0,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -51.0,
      "viewZ": -2.3
    },
    {
      "x": -59.5,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -59.5,
      "viewZ": -2.3
    },
    {
      "x": -62.5,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -62.5,
      "viewZ": -2.3
    },
    {
      "x": -65.5,
      "y": 2.4,
      "z": -4.86,
      "rotY": 0,
      "viewX": -65.5,
      "viewZ": -2.3
    },
    {
      "x": -67.86,
      "y": 2.4,
      "z": -2.8,
      "rotY": 1.5707963267948966,
      "viewX": -65.2,
      "viewZ": -2.8
    },
    {
      "x": -67.86,
      "y": 2.4,
      "z": 2.8,
      "rotY": 1.5707963267948966,
      "viewX": -65.2,
      "viewZ": 2.8
    }
  ],
  "III_lunar": [
    {
      "x": -28.14,
      "y": 2.4,
      "z": 7.5,
      "rotY": -1.5707963267948966,
      "viewX": -30.6,
      "viewZ": 7.5
    },
    {
      "x": -28.14,
      "y": 2.4,
      "z": 10.5,
      "rotY": -1.5707963267948966,
      "viewX": -30.6,
      "viewZ": 10.5
    },
    {
      "x": -28.14,
      "y": 2.4,
      "z": 13.5,
      "rotY": -1.5707963267948966,
      "viewX": -30.6,
      "viewZ": 13.5
    },
    {
      "x": -28.14,
      "y": 2.4,
      "z": 16.5,
      "rotY": -1.5707963267948966,
      "viewX": -30.6,
      "viewZ": 16.5
    },
    {
      "x": -28.14,
      "y": 2.4,
      "z": 19.5,
      "rotY": -1.5707963267948966,
      "viewX": -30.6,
      "viewZ": 19.5
    },
    {
      "x": -28.14,
      "y": 2.4,
      "z": 20.8,
      "rotY": -1.5707963267948966,
      "viewX": -30.6,
      "viewZ": 20.8
    },
    {
      "x": -30.0,
      "y": 2.4,
      "z": 22.86,
      "rotY": 3.141592653589793,
      "viewX": -30.0,
      "viewZ": 20.3
    },
    {
      "x": -32.5,
      "y": 2.4,
      "z": 22.86,
      "rotY": 3.141592653589793,
      "viewX": -32.5,
      "viewZ": 20.3
    },
    {
      "x": -35.0,
      "y": 2.4,
      "z": 22.86,
      "rotY": 3.141592653589793,
      "viewX": -35.0,
      "viewZ": 20.3
    },
    {
      "x": -37.5,
      "y": 2.4,
      "z": 22.86,
      "rotY": 3.141592653589793,
      "viewX": -37.5,
      "viewZ": 20.3
    },
    {
      "x": -40.0,
      "y": 2.4,
      "z": 22.86,
      "rotY": 3.141592653589793,
      "viewX": -40.0,
      "viewZ": 20.3
    },
    {
      "x": -42.5,
      "y": 2.4,
      "z": 22.86,
      "rotY": 3.141592653589793,
      "viewX": -42.5,
      "viewZ": 20.3
    },
    {
      "x": -43.8,
      "y": 2.4,
      "z": 22.86,
      "rotY": 3.141592653589793,
      "viewX": -43.8,
      "viewZ": 20.3
    },
    {
      "x": -45.86,
      "y": 2.4,
      "z": 20.8,
      "rotY": 1.5707963267948966,
      "viewX": -43.4,
      "viewZ": 20.8
    },
    {
      "x": -45.86,
      "y": 2.4,
      "z": 19.5,
      "rotY": 1.5707963267948966,
      "viewX": -43.4,
      "viewZ": 19.5
    },
    {
      "x": -45.86,
      "y": 2.4,
      "z": 16.5,
      "rotY": 1.5707963267948966,
      "viewX": -43.4,
      "viewZ": 16.5
    },
    {
      "x": -45.86,
      "y": 2.4,
      "z": 13.5,
      "rotY": 1.5707963267948966,
      "viewX": -43.4,
      "viewZ": 13.5
    },
    {
      "x": -45.86,
      "y": 2.4,
      "z": 10.5,
      "rotY": 1.5707963267948966,
      "viewX": -43.4,
      "viewZ": 10.5
    },
    {
      "x": -45.86,
      "y": 2.4,
      "z": 7.5,
      "rotY": 1.5707963267948966,
      "viewX": -43.4,
      "viewZ": 7.5
    }
  ],
  "III_wildlife": [
    {
      "x": -28.14,
      "y": 2.4,
      "z": -8.5,
      "rotY": -1.5707963267948966,
      "viewX": -30.6,
      "viewZ": -8.5
    },
    {
      "x": -28.14,
      "y": 2.4,
      "z": -12.5,
      "rotY": -1.5707963267948966,
      "viewX": -30.6,
      "viewZ": -12.5
    },
    {
      "x": -28.14,
      "y": 2.4,
      "z": -16.5,
      "rotY": -1.5707963267948966,
      "viewX": -30.6,
      "viewZ": -16.5
    },
    {
      "x": -28.14,
      "y": 2.4,
      "z": -20.5,
      "rotY": -1.5707963267948966,
      "viewX": -30.6,
      "viewZ": -20.5
    },
    {
      "x": -30.5,
      "y": 2.4,
      "z": -22.86,
      "rotY": 0,
      "viewX": -30.5,
      "viewZ": -20.3
    },
    {
      "x": -34.0,
      "y": 2.4,
      "z": -22.86,
      "rotY": 0,
      "viewX": -34.0,
      "viewZ": -20.3
    },
    {
      "x": -37.5,
      "y": 2.4,
      "z": -22.86,
      "rotY": 0,
      "viewX": -37.5,
      "viewZ": -20.3
    },
    {
      "x": -41.0,
      "y": 2.4,
      "z": -22.86,
      "rotY": 0,
      "viewX": -41.0,
      "viewZ": -20.3
    },
    {
      "x": -44.0,
      "y": 2.4,
      "z": -22.86,
      "rotY": 0,
      "viewX": -44.0,
      "viewZ": -20.3
    },
    {
      "x": -45.86,
      "y": 2.4,
      "z": -20.5,
      "rotY": 1.5707963267948966,
      "viewX": -43.4,
      "viewZ": -20.5
    },
    {
      "x": -45.86,
      "y": 2.4,
      "z": -16.5,
      "rotY": 1.5707963267948966,
      "viewX": -43.4,
      "viewZ": -16.5
    },
    {
      "x": -45.86,
      "y": 2.4,
      "z": -12.5,
      "rotY": 1.5707963267948966,
      "viewX": -43.4,
      "viewZ": -12.5
    },
    {
      "x": -45.86,
      "y": 2.4,
      "z": -8.5,
      "rotY": 1.5707963267948966,
      "viewX": -43.4,
      "viewZ": -8.5
    }
  ],
  "III_portrait": [
    {
      "x": -48.14,
      "y": 2.4,
      "z": 10.0,
      "rotY": -1.5707963267948966,
      "viewX": -50.6,
      "viewZ": 10.0
    },
    {
      "x": -48.14,
      "y": 2.4,
      "z": 18.0,
      "rotY": -1.5707963267948966,
      "viewX": -50.6,
      "viewZ": 18.0
    },
    {
      "x": -51.5,
      "y": 2.4,
      "z": 22.86,
      "rotY": 3.141592653589793,
      "viewX": -51.5,
      "viewZ": 20.3
    },
    {
      "x": -55.0,
      "y": 2.4,
      "z": 22.86,
      "rotY": 3.141592653589793,
      "viewX": -55.0,
      "viewZ": 20.3
    },
    {
      "x": -58.5,
      "y": 2.4,
      "z": 22.86,
      "rotY": 3.141592653589793,
      "viewX": -58.5,
      "viewZ": 20.3
    },
    {
      "x": -62.0,
      "y": 2.4,
      "z": 22.86,
      "rotY": 3.141592653589793,
      "viewX": -62.0,
      "viewZ": 20.3
    },
    {
      "x": -65.86,
      "y": 2.4,
      "z": 18.0,
      "rotY": 1.5707963267948966,
      "viewX": -63.4,
      "viewZ": 18.0
    },
    {
      "x": -65.86,
      "y": 2.4,
      "z": 10.0,
      "rotY": 1.5707963267948966,
      "viewX": -63.4,
      "viewZ": 10.0
    }
  ],
  "III_stilllife_object": [
    {
      "x": -48.14,
      "y": 2.4,
      "z": -8.5,
      "rotY": -1.5707963267948966,
      "viewX": -50.6,
      "viewZ": -8.5
    },
    {
      "x": -48.14,
      "y": 2.4,
      "z": -12.5,
      "rotY": -1.5707963267948966,
      "viewX": -50.6,
      "viewZ": -12.5
    },
    {
      "x": -48.14,
      "y": 2.4,
      "z": -16.5,
      "rotY": -1.5707963267948966,
      "viewX": -50.6,
      "viewZ": -16.5
    },
    {
      "x": -48.14,
      "y": 2.4,
      "z": -20.5,
      "rotY": -1.5707963267948966,
      "viewX": -50.6,
      "viewZ": -20.5
    },
    {
      "x": -51.0,
      "y": 2.4,
      "z": -22.86,
      "rotY": 0,
      "viewX": -51.0,
      "viewZ": -20.3
    },
    {
      "x": -53.8,
      "y": 2.4,
      "z": -22.86,
      "rotY": 0,
      "viewX": -53.8,
      "viewZ": -20.3
    },
    {
      "x": -56.6,
      "y": 2.4,
      "z": -22.86,
      "rotY": 0,
      "viewX": -56.6,
      "viewZ": -20.3
    },
    {
      "x": -59.4,
      "y": 2.4,
      "z": -22.86,
      "rotY": 0,
      "viewX": -59.4,
      "viewZ": -20.3
    },
    {
      "x": -62.2,
      "y": 2.4,
      "z": -22.86,
      "rotY": 0,
      "viewX": -62.2,
      "viewZ": -20.3
    },
    {
      "x": -64.0,
      "y": 2.4,
      "z": -22.86,
      "rotY": 0,
      "viewX": -64.0,
      "viewZ": -20.3
    },
    {
      "x": -65.86,
      "y": 2.4,
      "z": -20.5,
      "rotY": 1.5707963267948966,
      "viewX": -63.4,
      "viewZ": -20.5
    },
    {
      "x": -65.86,
      "y": 2.4,
      "z": -16.5,
      "rotY": 1.5707963267948966,
      "viewX": -63.4,
      "viewZ": -16.5
    },
    {
      "x": -65.86,
      "y": 2.4,
      "z": -12.5,
      "rotY": 1.5707963267948966,
      "viewX": -63.4,
      "viewZ": -12.5
    },
    {
      "x": -65.86,
      "y": 2.4,
      "z": -8.5,
      "rotY": 1.5707963267948966,
      "viewX": -63.4,
      "viewZ": -8.5
    }
  ],
  "IV_applied_graphic": [
    {
      "x": 11.5,
      "y": 2.4,
      "z": 52.14,
      "rotY": 0,
      "viewX": 11.5,
      "viewZ": 54.8
    },
    {
      "x": 15.5,
      "y": 2.4,
      "z": 52.14,
      "rotY": 0,
      "viewX": 15.5,
      "viewZ": 54.8
    },
    {
      "x": 19.5,
      "y": 2.4,
      "z": 52.14,
      "rotY": 0,
      "viewX": 19.5,
      "viewZ": 54.8
    },
    {
      "x": 23.5,
      "y": 2.4,
      "z": 52.14,
      "rotY": 0,
      "viewX": 23.5,
      "viewZ": 54.8
    },
    {
      "x": 27.86,
      "y": 2.4,
      "z": 56.0,
      "rotY": -1.5707963267948966,
      "viewX": 25.2,
      "viewZ": 56.0
    },
    {
      "x": 27.86,
      "y": 2.4,
      "z": 60.0,
      "rotY": -1.5707963267948966,
      "viewX": 25.2,
      "viewZ": 60.0
    },
    {
      "x": 27.86,
      "y": 2.4,
      "z": 64.0,
      "rotY": -1.5707963267948966,
      "viewX": 25.2,
      "viewZ": 64.0
    },
    {
      "x": 11.0,
      "y": 2.4,
      "z": 67.86,
      "rotY": 3.141592653589793,
      "viewX": 11.0,
      "viewZ": 65.2
    },
    {
      "x": 13.8,
      "y": 2.4,
      "z": 67.86,
      "rotY": 3.141592653589793,
      "viewX": 13.8,
      "viewZ": 65.2
    },
    {
      "x": 16.6,
      "y": 2.4,
      "z": 67.86,
      "rotY": 3.141592653589793,
      "viewX": 16.6,
      "viewZ": 65.2
    },
    {
      "x": 19.4,
      "y": 2.4,
      "z": 67.86,
      "rotY": 3.141592653589793,
      "viewX": 19.4,
      "viewZ": 65.2
    },
    {
      "x": 22.2,
      "y": 2.4,
      "z": 67.86,
      "rotY": 3.141592653589793,
      "viewX": 22.2,
      "viewZ": 65.2
    },
    {
      "x": 25.0,
      "y": 2.4,
      "z": 67.86,
      "rotY": 3.141592653589793,
      "viewX": 25.0,
      "viewZ": 65.2
    }
  ],
  "IV_cinema": [
    {
      "x": -5.2,
      "y": 2.6,
      "z": 67.86,
      "rotY": 3.141592653589793,
      "viewX": -5.2,
      "viewZ": 64.5
    },
    {
      "x": 5.2,
      "y": 2.6,
      "z": 67.86,
      "rotY": 3.141592653589793,
      "viewX": 5.2,
      "viewZ": 64.5
    },
    {
      "x": -7.86,
      "y": 2.6,
      "z": 55.5,
      "rotY": 1.5707963267948966,
      "viewX": -5.2,
      "viewZ": 55.5
    },
    {
      "x": -7.86,
      "y": 2.6,
      "z": 64.5,
      "rotY": 1.5707963267948966,
      "viewX": -5.2,
      "viewZ": 64.5
    },
    {
      "x": 7.86,
      "y": 2.6,
      "z": 55.5,
      "rotY": -1.5707963267948966,
      "viewX": 5.2,
      "viewZ": 55.5
    },
    {
      "x": 7.86,
      "y": 2.6,
      "z": 64.5,
      "rotY": -1.5707963267948966,
      "viewX": 5.2,
      "viewZ": 64.5
    }
  ],
  "IV_production_design": [
    {
      "x": -24.5,
      "y": 2.4,
      "z": 52.14,
      "rotY": 0,
      "viewX": -24.5,
      "viewZ": 54.8
    },
    {
      "x": -20.5,
      "y": 2.4,
      "z": 52.14,
      "rotY": 0,
      "viewX": -20.5,
      "viewZ": 54.8
    },
    {
      "x": -16.5,
      "y": 2.4,
      "z": 52.14,
      "rotY": 0,
      "viewX": -16.5,
      "viewZ": 54.8
    },
    {
      "x": -11.5,
      "y": 2.4,
      "z": 52.14,
      "rotY": 0,
      "viewX": -11.5,
      "viewZ": 54.8
    },
    {
      "x": -27.86,
      "y": 2.4,
      "z": 54.5,
      "rotY": 1.5707963267948966,
      "viewX": -25.2,
      "viewZ": 54.5
    },
    {
      "x": -27.86,
      "y": 2.4,
      "z": 57.0,
      "rotY": 1.5707963267948966,
      "viewX": -25.2,
      "viewZ": 57.0
    },
    {
      "x": -27.86,
      "y": 2.4,
      "z": 59.5,
      "rotY": 1.5707963267948966,
      "viewX": -25.2,
      "viewZ": 59.5
    },
    {
      "x": -27.86,
      "y": 2.4,
      "z": 62.0,
      "rotY": 1.5707963267948966,
      "viewX": -25.2,
      "viewZ": 62.0
    },
    {
      "x": -27.86,
      "y": 2.4,
      "z": 64.5,
      "rotY": 1.5707963267948966,
      "viewX": -25.2,
      "viewZ": 64.5
    },
    {
      "x": -27.86,
      "y": 2.4,
      "z": 66.0,
      "rotY": 1.5707963267948966,
      "viewX": -25.2,
      "viewZ": 66.0
    },
    {
      "x": -24.5,
      "y": 2.4,
      "z": 67.86,
      "rotY": 3.141592653589793,
      "viewX": -24.5,
      "viewZ": 65.2
    },
    {
      "x": -21.0,
      "y": 2.4,
      "z": 67.86,
      "rotY": 3.141592653589793,
      "viewX": -21.0,
      "viewZ": 65.2
    },
    {
      "x": -15.5,
      "y": 2.4,
      "z": 67.86,
      "rotY": 3.141592653589793,
      "viewX": -15.5,
      "viewZ": 65.2
    },
    {
      "x": -11.5,
      "y": 2.4,
      "z": 67.86,
      "rotY": 3.141592653589793,
      "viewX": -11.5,
      "viewZ": 65.2
    }
  ],
  "IV_storyboard": [
    {
      "x": -21.0,
      "y": 2.5,
      "z": 91.86,
      "rotY": 3.141592653589793,
      "viewX": -21.0,
      "viewZ": 88.5
    },
    {
      "x": -14.0,
      "y": 2.5,
      "z": 91.86,
      "rotY": 3.141592653589793,
      "viewX": -14.0,
      "viewZ": 88.5
    },
    {
      "x": -7.0,
      "y": 2.5,
      "z": 91.86,
      "rotY": 3.141592653589793,
      "viewX": -7.0,
      "viewZ": 88.5
    },
    {
      "x": 0.0,
      "y": 2.5,
      "z": 91.86,
      "rotY": 3.141592653589793,
      "viewX": 0.0,
      "viewZ": 88.5
    },
    {
      "x": 7.0,
      "y": 2.5,
      "z": 91.86,
      "rotY": 3.141592653589793,
      "viewX": 7.0,
      "viewZ": 88.5
    },
    {
      "x": 14.0,
      "y": 2.5,
      "z": 91.86,
      "rotY": 3.141592653589793,
      "viewX": 14.0,
      "viewZ": 88.5
    },
    {
      "x": 21.0,
      "y": 2.5,
      "z": 91.86,
      "rotY": 3.141592653589793,
      "viewX": 21.0,
      "viewZ": 88.5
    },
    {
      "x": -27.86,
      "y": 2.4,
      "z": 72.5,
      "rotY": 1.5707963267948966,
      "viewX": -25.2,
      "viewZ": 72.5
    },
    {
      "x": -27.86,
      "y": 2.4,
      "z": 77.5,
      "rotY": 1.5707963267948966,
      "viewX": -25.2,
      "viewZ": 77.5
    },
    {
      "x": -27.86,
      "y": 2.4,
      "z": 82.5,
      "rotY": 1.5707963267948966,
      "viewX": -25.2,
      "viewZ": 82.5
    },
    {
      "x": -27.86,
      "y": 2.4,
      "z": 87.5,
      "rotY": 1.5707963267948966,
      "viewX": -25.2,
      "viewZ": 87.5
    },
    {
      "x": 27.86,
      "y": 2.4,
      "z": 72.5,
      "rotY": -1.5707963267948966,
      "viewX": 25.2,
      "viewZ": 72.5
    },
    {
      "x": 27.86,
      "y": 2.4,
      "z": 77.5,
      "rotY": -1.5707963267948966,
      "viewX": 25.2,
      "viewZ": 77.5
    },
    {
      "x": 27.86,
      "y": 2.4,
      "z": 82.5,
      "rotY": -1.5707963267948966,
      "viewX": 25.2,
      "viewZ": 82.5
    },
    {
      "x": 27.86,
      "y": 2.4,
      "z": 87.5,
      "rotY": -1.5707963267948966,
      "viewX": 25.2,
      "viewZ": 87.5
    },
    {
      "x": -22.0,
      "y": 2.4,
      "z": 68.14,
      "rotY": 0,
      "viewX": -22.0,
      "viewZ": 70.8
    },
    {
      "x": -12.0,
      "y": 2.4,
      "z": 68.14,
      "rotY": 0,
      "viewX": -12.0,
      "viewZ": 70.8
    },
    {
      "x": 12.0,
      "y": 2.4,
      "z": 68.14,
      "rotY": 0,
      "viewX": 12.0,
      "viewZ": 70.8
    },
    {
      "x": 22.0,
      "y": 2.4,
      "z": 68.14,
      "rotY": 0,
      "viewX": 22.0,
      "viewZ": 70.8
    }
  ]
};

function layoutExhibits() {
  const groups = {};
  EUNOIA_CONFIG.exhibits.forEach((ex) => {
    const key = `${ex.wing}_${ex.room}`;
    if (!groups[key]) groups[key] = [];
    groups[key].push(ex);
  });

  let hungCount = 0;
  for (const [key, list] of Object.entries(groups)) {
    const spots = EXHIBIT_SPOTS[key] || [];
    list.forEach((ex, idx) => {
      const spot = spots[idx];
      if (!spot) {
        console.warn(`No spot for exhibit ${ex.id} in group ${key} index ${idx}`);
        return;
      }

      const { group } = buildPictureFrame(ex);
      group.position.set(spot.x, spot.y, spot.z);
      group.rotation.y = spot.rotY;
      scene.add(group);

      ex.teleportPos = new THREE.Vector3(spot.viewX, EYE_HEIGHT, spot.viewZ);
      ex.lookTarget = new THREE.Vector3(spot.x, spot.y, spot.z);
      hungCount++;
    });
  }
  console.log(`Successfully hung ${hungCount} exhibits in 3D museum!`);
}
