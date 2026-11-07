// Simulation of rotunda navigation with old vs new collision code

function createOldCollision() {
  const colliders = [];
  function addRotatedBoxCollider(cx, cz, hx, hz, rotY) {
    colliders.push({ type: 'obb', cx, cz, hx, hz, rotY, cos: Math.cos(-rotY), sin: Math.sin(-rotY) });
  }
  function addCylCollider(cx, cz, r) { colliders.push({ type: 'cyl', cx, cz, r }); }

  // Pedestal
  addCylCollider(0, 0, 1.28);

  // 8 columns
  const R_COLS = 5.8;
  const colAngles = [
    Math.PI / 6, 2 * Math.PI / 6,
    4 * Math.PI / 6, 5 * Math.PI / 6,
    7 * Math.PI / 6, 8 * Math.PI / 6,
    10 * Math.PI / 6, 11 * Math.PI / 6
  ];
  colAngles.forEach(a => addCylCollider(Math.cos(a) * R_COLS, Math.sin(a) * R_COLS, 0.55));

  // Rotunda benches
  addRotatedBoxCollider(4.2, -4.2, 1.70, 0.50, -Math.PI / 4);
  addRotatedBoxCollider(-4.2, -4.2, 1.70, 0.50, Math.PI / 4);

  const PLAYER_R = 0.45;
  function resolve(pos) {
    for (let iter = 0; iter < 4; iter++) {
      for (const c of colliders) {
        if (c.type === 'obb') {
          const dx = pos.x - c.cx, dz = pos.z - c.cz;
          const lx = dx * c.cos - dz * c.sin;
          const lz = dx * c.sin + dz * c.cos;
          const clx = Math.max(-c.hx, Math.min(c.hx, lx));
          const clz = Math.max(-c.hz, Math.min(c.hz, lz));
          const diffX = lx - clx, diffZ = lz - clz;
          const d2 = diffX * diffX + diffZ * diffZ;
          if (d2 < PLAYER_R * PLAYER_R) {
            const d = Math.sqrt(d2);
            let pushLX, pushLZ;
            if (d > 0.0001) {
              pushLX = clx + (diffX / d) * PLAYER_R;
              pushLZ = clz + (diffZ / d) * PLAYER_R;
            } else {
              pushLX = lx; pushLZ = lz + c.hz + PLAYER_R;
            }
            const cosRev = Math.cos(c.rotY), sinRev = Math.sin(c.rotY);
            pos.x = c.cx + pushLX * cosRev - pushLZ * sinRev;
            pos.z = c.cz + pushLX * sinRev + pushLZ * cosRev;
          }
        } else if (c.type === 'cyl') {
          const dx = pos.x - c.cx, dz = pos.z - c.cz, d2 = dx * dx + dz * dz;
          const minD = c.r + PLAYER_R;
          if (d2 < minD * minD) {
            const d = Math.max(0.0001, Math.sqrt(d2));
            pos.x = c.cx + (dx / d) * minD;
            pos.z = c.cz + (dz / d) * minD;
          }
        }
      }
    }
  }
  return { colliders, resolve };
}

function createNewCollision() {
  const colliders = [];
  function addRotatedBoxCollider(cx, cz, hx, hz, rotY) {
    colliders.push({ type: 'obb', cx, cz, hx, hz, rotY, cos: Math.cos(rotY), sin: Math.sin(rotY) });
  }
  function addCylCollider(cx, cz, r) { colliders.push({ type: 'cyl', cx, cz, r }); }

  addCylCollider(0, 0, 1.28);
  const R_COLS = 5.8;
  const colAngles = [
    Math.PI / 6, 2 * Math.PI / 6,
    4 * Math.PI / 6, 5 * Math.PI / 6,
    7 * Math.PI / 6, 8 * Math.PI / 6,
    10 * Math.PI / 6, 11 * Math.PI / 6
  ];
  colAngles.forEach(a => addCylCollider(Math.cos(a) * R_COLS, Math.sin(a) * R_COLS, 0.55));

  addRotatedBoxCollider(4.2, -4.2, 1.70, 0.50, -Math.PI / 4);
  addRotatedBoxCollider(-4.2, -4.2, 1.70, 0.50, Math.PI / 4);

  const PLAYER_R = 0.45;
  function resolve(pos) {
    for (let iter = 0; iter < 4; iter++) {
      for (const c of colliders) {
        if (c.type === 'obb') {
          const dx = pos.x - c.cx, dz = pos.z - c.cz;
          const lx = dx * c.cos - dz * c.sin;
          const lz = dx * c.sin + dz * c.cos;
          const clx = Math.max(-c.hx, Math.min(c.hx, lx));
          const clz = Math.max(-c.hz, Math.min(c.hz, lz));
          const diffX = lx - clx, diffZ = lz - clz;
          const d2 = diffX * diffX + diffZ * diffZ;
          if (d2 < PLAYER_R * PLAYER_R) {
            const d = Math.sqrt(d2);
            let pushLX, pushLZ;
            if (d > 0.0001) {
              pushLX = clx + (diffX / d) * PLAYER_R;
              pushLZ = clz + (diffZ / d) * PLAYER_R;
            } else {
              const dLeft = Math.abs(lx - (-c.hx)), dRight = Math.abs(lx - c.hx);
              const dTop = Math.abs(lz - (-c.hz)), dBot = Math.abs(lz - c.hz);
              const m = Math.min(dLeft, dRight, dTop, dBot);
              pushLX = lx; pushLZ = lz;
              if (m === dLeft) pushLX = -c.hx - PLAYER_R;
              else if (m === dRight) pushLX = c.hx + PLAYER_R;
              else if (m === dTop) pushLZ = -c.hz - PLAYER_R;
              else pushLZ = c.hz + PLAYER_R;
            }
            pos.x = c.cx + pushLX * c.cos + pushLZ * c.sin;
            pos.z = c.cz - pushLX * c.sin + pushLZ * c.cos;
          }
        } else if (c.type === 'cyl') {
          const dx = pos.x - c.cx, dz = pos.z - c.cz, d2 = dx * dx + dz * dz;
          const minD = c.r + PLAYER_R;
          if (d2 < minD * minD) {
            const d = Math.max(0.0001, Math.sqrt(d2));
            pos.x = c.cx + (dx / d) * minD;
            pos.z = c.cz + (dz / d) * minD;
          }
        }
      }
    }
  }
  return { colliders, resolve };
}

// Compare what points in the walkway are blocked:
const oldC = createOldCollision();
const newC = createNewCollision();

// Let's test walking along x = 3.0, z from -2.0 to -6.0:
console.log('Testing path along x=3.0, z from -2 to -6:');
for (let z = -2.0; z >= -6.0; z -= 0.5) {
  const pOld = { x: 3.0, z: z };
  oldC.resolve(pOld);
  const pNew = { x: 3.0, z: z };
  newC.resolve(pNew);
  console.log(`z=${z.toFixed(1)}: Old pushed to (${pOld.x.toFixed(2)}, ${pOld.z.toFixed(2)}) [diff=${Math.hypot(pOld.x-3.0, pOld.z-z).toFixed(2)}] | New pushed to (${pNew.x.toFixed(2)}, ${pNew.z.toFixed(2)}) [diff=${Math.hypot(pNew.x-3.0, pNew.z-z).toFixed(2)}]`);
}

