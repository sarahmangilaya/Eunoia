import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update ART_SPOT_LIGHTMAP and ART_SPOT_INTENSITY
old_art_lightmap_regex = re.compile(
    r'const ART_SPOT_LIGHTMAP = \(\(\) => \{.*?\}\)\(\);\s*const ART_SPOT_INTENSITY = [^;]+;',
    re.DOTALL
)

new_art_lightmap = """const ART_SPOT_LIGHTMAP = (() => {
  const S = 256;
  const [c, ctx] = makeCanvas(S, S);
  const img = ctx.createImageData(S, S);
  // Elegant gallery spotlight: focused beam at the top-center of the painting,
  // softly washing down across the artwork surface (multiplies texture, keeps contrast crisp).
  for (let y = 0; y < S; y++) {
    const ny = y / (S - 1); // 0 = top of painting, 1 = bottom
    for (let x = 0; x < S; x++) {
      const nx = x / (S - 1) - 0.5; // -0.5 to 0.5 across width
      const dy = ny + 0.22;
      const dist = Math.hypot(nx * 1.1, dy * 0.85);
      // Soft elliptical cone spreading downward
      const cone = Math.pow(Math.max(0, 1.0 - (Math.abs(nx) / (0.35 + dy * 0.42))), 1.3);
      const fall = Math.pow(Math.max(0, 1.0 - (dist / 1.45)), 1.4);
      const spot = cone * fall;
      // Multiplier: 0.82 baseline ambient up to 1.32 peak spotlight core
      const t = 0.82 + 0.50 * spot;
      const i = (y * S + x) * 4;
      img.data[i]     = Math.min(255, 255 * t) | 0;
      img.data[i + 1] = Math.min(255, 246 * t) | 0; // warm gallery halogen tint
      img.data[i + 2] = Math.min(255, 226 * t) | 0;
      img.data[i + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
})();
const ART_SPOT_INTENSITY = Math.PI; // Three.js multiplies lightMapTexel * (lightMapIntensity / PI) = exact 1.0x factor"""

html, n1 = old_art_lightmap_regex.subn(new_art_lightmap, html)
print('Replaced ART_SPOT_LIGHTMAP:', n1)

# 2. Update buildLightPools to position gWall strictly from lamp downwards and refine artLightMat
old_build_light_pools_regex = re.compile(
    r'function buildLightPools\(poolSpots\) \{.*?function layoutExhibits',
    re.DOTALL
)

new_build_light_pools = """function buildLightPools(poolSpots) {
  // Generate downward gallery spotlight texture matching museum track lighting
  const [pc, pctx] = makeCanvas(512, 512);
  const imgData = pctx.createImageData(512, 512);
  const data = imgData.data;
  const lx = 256.0, ly = 16.0; // spotlight apex begins at lamp level

  for (let y = 0; y < 512; y++) {
    const dy = y - ly; // positive dy points DOWNWARDS onto the artwork & wall
    for (let x = 0; x < 512; x++) {
      const dx = x - lx;

      let intensity = 0.0;
      if (dy > 0.0) {
        // Conical spotlight beam spreading downward (~46 degree spread)
        const spread = 28.0 + dy * 0.68;
        const xNorm = Math.abs(dx) / spread;

        if (xNorm < 1.0) {
          const fan = Math.pow(Math.cos(xNorm * Math.PI * 0.5), 1.25);
          const distTaper = Math.pow(Math.max(0, 1.0 - (dy / 500.0)), 1.2);
          const topEase = Math.min(1.0, dy / 25.0);
          intensity = fan * distTaper * topEase;
        }
      }

      // Warm radiant illumination centered over the artwork zone
      const dArt = Math.hypot(dx * 0.85, (dy - 190.0) * 0.75);
      const artGlow = Math.pow(Math.max(0, 1.0 - dArt / 220.0), 1.5) * 0.50;

      const total = Math.min(1.0, intensity * 0.80 + artGlow);
      if (total > 0.005) {
        const idx = (y * 512 + x) * 4;
        data[idx]     = Math.min(255, 255 * total * 1.15) | 0;
        data[idx + 1] = Math.min(255, 236 * (total * 0.98 + 0.03)) | 0;
        data[idx + 2] = Math.min(255, 175 * (total * 0.62 + 0.03)) | 0;
        data[idx + 3] = Math.min(255, 255 * Math.pow(total, 1.05)) | 0;
      }
    }
  }
  pctx.putImageData(imgData, 0, 0);

  const poolTex = new THREE.CanvasTexture(pc);
  poolTex.colorSpace = THREE.SRGBColorSpace;
  poolTex.generateMipmaps = true;
  poolTex.minFilter = THREE.LinearMipmapLinearFilter;
  poolTex.magFilter = THREE.LinearFilter;

  const poolMat = new THREE.MeshBasicMaterial({
    map: poolTex, transparent: true, opacity: 0.42,
    blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide
  });
  poolMat.toneMapped = false;

  const wingGroups = { I: wingI_group, II: wingII_group, III: wingIII_group, IV: wingIV_group };
  const [bc, bctx] = makeCanvas(64, 256);
  const bg = bctx.createLinearGradient(0, 0, 0, 256);
  bg.addColorStop(0.00, 'rgba(255,236,190,0.85)');
  bg.addColorStop(0.35, 'rgba(255,220,165,0.35)');
  bg.addColorStop(1.00, 'rgba(255,205,145,0)');
  bctx.fillStyle = bg; bctx.fillRect(0, 0, 64, 256);
  const sg = bctx.createLinearGradient(0, 0, 64, 0);
  sg.addColorStop(0, 'rgba(0,0,0,1)'); sg.addColorStop(0.35, 'rgba(0,0,0,0)');
  sg.addColorStop(0.65, 'rgba(0,0,0,0)'); sg.addColorStop(1, 'rgba(0,0,0,1)');
  bctx.globalCompositeOperation = 'destination-out';
  bctx.fillStyle = sg; bctx.fillRect(0, 0, 64, 256);
  const beamTex = new THREE.CanvasTexture(bc);
  beamTex.colorSpace = THREE.SRGBColorSpace;

  // Soft subtle volumetric air beam: 0.10 opacity (ethereal dust/glow, zero fogging on artwork)
  const artLightMat = new THREE.MeshBasicMaterial({
    map: beamTex, transparent: true, opacity: 0.10, blending: THREE.AdditiveBlending,
    depthWrite: false, side: THREE.DoubleSide, fog: false
  });
  artLightMat.toneMapped = false;

  Object.keys(poolSpots).forEach((wing) => {
    const geos = [];
    const artGeos = [];
    poolSpots[wing].forEach((s) => {
      const isLand = s.land;
      const artW = isLand ? 2.6 : 1.95, artH = isLand ? 1.95 : 2.6;

      // 1. Wall Wash: strictly spans from lamp hood DOWNWARDS past bottom of frame.
      // Top edge aligns with lamp (+0.35m), bottom extends -0.70m below frame center.
      // This guarantees ZERO light points upwards at the ceiling!
      const wallH = artH + 1.05;
      const wallW = artW + 1.30;
      const yCenterWall = -0.175; // (0.35 + (-artH/2 - 0.70) + artH/2) / 2 = -0.175
      const gWall = new THREE.PlaneGeometry(wallW, wallH);
      gWall.translate(0, yCenterWall, -0.015);
      gWall.rotateY(s.rotY);
      gWall.translate(s.x, s.y, s.z);
      geos.push(gWall);

      // 2. 3D Light Cone: subtle volumetric beam fanning from lamp hood down across the painting
      const lampY = artH / 2 + 0.32, lampZ = 0.35;
      const hitY = -artH / 2 - 0.05, hitZ = 0.082;
      const topHalf = 0.28, botHalf = artW * 0.52;
      const gArt = new THREE.BufferGeometry();
      gArt.setAttribute('position', new THREE.Float32BufferAttribute([
        -topHalf, lampY, lampZ,   topHalf, lampY, lampZ,
        -botHalf, hitY, hitZ,     botHalf, hitY, hitZ
      ], 3));
      gArt.setAttribute('uv', new THREE.Float32BufferAttribute([0, 1, 1, 1, 0, 0, 1, 0], 2));
      gArt.setAttribute('normal', new THREE.Float32BufferAttribute([0,0,1, 0,0,1, 0,0,1, 0,0,1], 3));
      gArt.setIndex([0, 2, 1, 1, 2, 3]);
      gArt.rotateY(s.rotY);
      gArt.translate(s.x, s.y, s.z);
      artGeos.push(gArt);
    });
    if (artGeos.length) {
      const flatArt = artGeos.map((p) => (p.index ? p.toNonIndexed() : p));
      const mergedArt = mergeGeometries(flatArt, false);
      artGeos.forEach((g) => g.dispose()); flatArt.forEach((g) => g.dispose());
      const artMesh = new THREE.Mesh(mergedArt, artLightMat);
      artMesh.renderOrder = 2;
      artMesh.frustumCulled = false;
      wingGroups[wing].add(artMesh);
    }
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
}

function layoutExhibits"""

html, n2 = old_build_light_pools_regex.subn(new_build_light_pools, html)
print('Replaced buildLightPools:', n2)

# 3. Update buildLighting ambient and tone mapping
html = re.sub(
    r'const hemi = new THREE\.HemisphereLight\(0x[0-9a-fA-F]+,\s*0x[0-9a-fA-F]+,\s*[0-9.]+\);',
    'const hemi = new THREE.HemisphereLight(0xf4e6d4, 0x181008, 0.52);',
    html
)
html = re.sub(
    r'const amb = new THREE\.AmbientLight\(0x[0-9a-fA-F]+,\s*[0-9.]+\);',
    'const amb = new THREE.AmbientLight(0xfff3e2, 0.42);',
    html
)
html = re.sub(
    r'const visitorLantern = new THREE\.PointLight\(0x[0-9a-fA-F]+,\s*[0-9.]+,\s*[0-9.]+,\s*[0-9.]+\);',
    'const visitorLantern = new THREE.PointLight(0xffeed4, 1.4, 15.0, 1.3);',
    html
)
html = re.sub(
    r'renderer\.toneMappingExposure = [0-9.]+;',
    'renderer.toneMappingExposure = 1.18;',
    html
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated index.html successfully!')

