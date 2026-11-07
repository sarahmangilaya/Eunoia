import re

html = open('index.html', encoding='utf-8').read()

start = html.find('function buildLightPools(poolSpots) {')
end = html.find('wingGroups[wing].add(mesh);\n  });\n}', start)
assert start != -1 and end != -1, 'buildLightPools not found'

NEW_CODE = r'''function buildLightPools(poolSpots) {
  // Generate downward gallery spotlight texture matching museum track lighting
  const [pc, pctx] = makeCanvas(512, 512);
  const imgData = pctx.createImageData(512, 512);
  const data = imgData.data;
  const lx = 256.0, ly = 30.0; // spotlight apex high on wall above frame

  for (let y = 0; y < 512; y++) {
    const dy = y - ly; // positive dy points DOWNWARDS onto the artwork
    for (let x = 0; x < 512; x++) {
      const dx = x - lx;

      let intensity = 0.0;
      if (dy > -5.0) {
        // Conical spotlight beam spreading downward (~48 degree half-angle)
        const spread = 30.0 + dy * 0.72;
        const xNorm = Math.abs(dx) / spread;

        if (xNorm < 1.0) {
          const fan = Math.pow(Math.cos(xNorm * Math.PI * 0.5), 1.3);
          const distTaper = Math.pow(Math.max(0, 1.0 - (dy / 490.0)), 1.15);
          const topEase = Math.min(1.0, (dy + 5.0) / 35.0);
          intensity = fan * distTaper * topEase;
        }
      }

      // Warm radiant illumination centered directly over the artwork
      const dArt = Math.hypot(dx * 0.9, (dy - 220.0) * 0.8);
      const artGlow = Math.pow(Math.max(0, 1.0 - dArt / 240.0), 1.6) * 0.55;

      const total = Math.min(1.0, intensity * 0.75 + artGlow);
      if (total > 0.005) {
        const idx = (y * 512 + x) * 4;
        data[idx]     = Math.min(255, 255 * total * 1.15) | 0;
        data[idx + 1] = Math.min(255, 235 * (total * 0.98 + 0.04)) | 0;
        data[idx + 2] = Math.min(255, 170 * (total * 0.62 + 0.04)) | 0;
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
    map: poolTex, transparent: true, opacity: 0.95,
    blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide
  });
  poolMat.toneMapped = false;

  const wingGroups = { I: wingI_group, II: wingII_group, III: wingIII_group, IV: wingIV_group };
  Object.keys(poolSpots).forEach((wing) => {
    const geos = [];
    poolSpots[wing].forEach((s) => {
      const isLand = s.land;
      const artW = isLand ? 2.6 : 1.95, artH = isLand ? 1.95 : 2.6;

      // 1. Wall Wash: sits flush on wall surface (-0.015m local z)
      // Spans from above frame down past the bottom, washing downward
      const pw = artW + 1.4, ph = artH + 1.6;
      const yShiftWall = 0.1; // wall plane center is slightly above frame center
      const gWall = new THREE.PlaneGeometry(pw, ph);
      gWall.translate(0, yShiftWall, -0.015);
      gWall.rotateY(s.rotY);
      gWall.translate(s.x, s.y, s.z);
      geos.push(gWall);

      // 2. Artwork Illumination: sits flush on canvas (+0.076m local z)
      // Bathes the project image in warm downward spotlight
      const gArt = new THREE.PlaneGeometry(artW, artH);
      // Remap UVs so gArt samples the exact corresponding spotlight region
      const uMin = 0.5 - (artW / (2.0 * pw));
      const uMax = 0.5 + (artW / (2.0 * pw));
      const vMin = 0.5 + (-yShiftWall - artH / 2.0) / ph;
      const vMax = 0.5 + (-yShiftWall + artH / 2.0) / ph;

      const uvAttr = gArt.attributes.uv;
      // PlaneGeometry UVs: (0,1) top-left, (1,1) top-right, (0,0) bottom-left, (1,0) bottom-right
      uvAttr.setXY(0, uMin, vMax);
      uvAttr.setXY(1, uMax, vMax);
      uvAttr.setXY(2, uMin, vMin);
      uvAttr.setXY(3, uMax, vMin);
      uvAttr.needsUpdate = true;

      gArt.translate(0, 0, 0.076);
      gArt.rotateY(s.rotY);
      gArt.translate(s.x, s.y, s.z);
      geos.push(gArt);
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

html = html[:start] + NEW_CODE + html[end + len('wingGroups[wing].add(mesh);\n  });\n}'):]

open('index.html', 'w', encoding='utf-8').write(html)
print('Successfully applied downward spotlights to index.html')

