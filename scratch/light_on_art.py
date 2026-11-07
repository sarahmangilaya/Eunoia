p = 'index.html'
h = open(p, encoding='utf-8').read()

def rep(old, new):
    global h
    assert old in h, old[:70]
    h = h.replace(old, new, 1)

# 1. Baked picture-lamp lightmap applied DIRECTLY to every artwork canvas material
rep("const ART_TINT = 0xe8e4dc;", r"""const ART_TINT = 0xf2eee6;

/* Picture-lamp spotlight baked straight into the artwork: the lamp sits above the
   top-centre of the frame, so the canvas is brightest just under it and falls off
   softly towards the lower corners (multiplies the artwork, so colours stay true). */
const ART_SPOT_LIGHTMAP = (() => {
  const S = 256;
  const [c, ctx] = makeCanvas(S, S);
  const img = ctx.createImageData(S, S);
  for (let y = 0; y < S; y++) {
    const ny = y / (S - 1);               // 0 = top of the artwork
    for (let x = 0; x < S; x++) {
      const nx = x / (S - 1) - 0.5;
      const dy = ny + 0.32;               // lamp is ~0.32 canvas-heights above the top edge
      const ang = Math.atan2(Math.abs(nx), dy);          // angle from the beam axis
      const cone = Math.pow(Math.max(0, Math.cos(Math.min(1, ang / 1.05) * Math.PI * 0.5)), 0.9);
      const fall = 1 / (1 + Math.pow(Math.hypot(nx, dy) * 1.05, 2));
      const v = Math.min(1, cone * fall * 1.55);
      const t = 0.42 + 0.58 * v;          // never fully dark: ambient floor
      const i = (y * S + x) * 4;
      img.data[i]     = Math.min(255, 255 * t) | 0;
      img.data[i + 1] = Math.min(255, 244 * t) | 0;     // warm tungsten tint
      img.data[i + 2] = Math.min(255, 222 * t) | 0;
      img.data[i + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
})();
const ART_SPOT_INTENSITY = Math.PI * 1.32; // peak ~1.3x under the lamp, ~0.55x at the far corners""")

rep("const artMat = new THREE.MeshBasicMaterial({ map: fallbackTex, color: ART_TINT });",
    "const artMat = new THREE.MeshBasicMaterial({ map: fallbackTex, color: ART_TINT, lightMap: ART_SPOT_LIGHTMAP, lightMapIntensity: ART_SPOT_INTENSITY });")

# 2. Replace the flat additive overlay on the canvas with a visible light beam
#    falling from each brass lamp onto the face of the artwork.
rep("""  const artLightMat = poolMat.clone();
  artLightMat.opacity = 0.32;""", """  const [bc, bctx] = makeCanvas(64, 256);
  const bg = bctx.createLinearGradient(0, 0, 0, 256);
  bg.addColorStop(0.00, 'rgba(255,236,190,1)');
  bg.addColorStop(0.40, 'rgba(255,220,165,0.45)');
  bg.addColorStop(1.00, 'rgba(255,205,145,0)');
  bctx.fillStyle = bg; bctx.fillRect(0, 0, 64, 256);
  const sg = bctx.createLinearGradient(0, 0, 64, 0);   // soft side edges
  sg.addColorStop(0, 'rgba(0,0,0,1)'); sg.addColorStop(0.3, 'rgba(0,0,0,0)');
  sg.addColorStop(0.7, 'rgba(0,0,0,0)'); sg.addColorStop(1, 'rgba(0,0,0,1)');
  bctx.globalCompositeOperation = 'destination-out';
  bctx.fillStyle = sg; bctx.fillRect(0, 0, 64, 256);
  const beamTex = new THREE.CanvasTexture(bc);
  beamTex.colorSpace = THREE.SRGBColorSpace;
  const artLightMat = new THREE.MeshBasicMaterial({
    map: beamTex, transparent: true, opacity: 0.16, blending: THREE.AdditiveBlending,
    depthWrite: false, side: THREE.DoubleSide, fog: false
  });
  artLightMat.toneMapped = false;""")

# Build the beam geometry instead of the canvas overlay
start = h.find("      // 2. Artwork Illumination: sits flush on canvas (+0.076m local z)")
end = h.find("      artGeos.push(gArt);", start)
assert start != -1 and end != -1
BEAM = """      // 2. Light beam: a soft fan from the brass lamp down onto the face of the artwork
      const lampY = artH / 2 + 0.30, lampZ = 0.34;
      const hitY = artH / 2 - artH * 0.62, hitZ = 0.085;
      const topHalf = 0.30, botHalf = artW * 0.55;
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
"""
h = h[:start] + BEAM + h[end:]

open(p, 'w', encoding='utf-8').write(h)
print('art lighting applied')

