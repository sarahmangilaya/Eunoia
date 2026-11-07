with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update IES_CONE_TEX generation: wider cone expansion, smoother falloff, brighter alpha peak
old_ies_block = """const IES_CONE_TEX = (() => {
  const W = 512, H = 768;
  const [c, ctx] = makeCanvas(W, H);
  const img = ctx.createImageData(W, H);
  const d = img.data;
  for (let py = 0; py < H; py++) {
    const v = py / (H - 1); // [0, 1] top to bottom
    for (let px = 0; px < W; px++) {
      const u = (px / (W - 1)) * 2.0 - 1.0; // [-1, 1] horizontally
      let intensity = 0.0;
      if (v > 0.03) {
        const vNorm = Math.max(0.0001, (v - 0.08) / 0.92);
        const coneWidth = 0.12 + Math.pow(vNorm, 0.78) * 0.85;
        const hFalloff = Math.exp(-Math.pow(u / coneWidth, 2) * 2.8);
        let vFalloff = 0.0;
        if (v >= 0.08) {
          vFalloff = Math.sin(Math.pow(vNorm, 0.55) * Math.PI) * (1.0 - 0.35 * v);
        } else {
          // Soft 0.05 feather at the apex (v in [0.03, 0.08])
          const ft = (v - 0.03) / 0.05;
          vFalloff = ft * ft * (3.0 - 2.0 * ft) * 0.16;
        }
        // Feather horizontal boundary |u| > 0.88 to 0 so plane edges are 100% seamless
        const edgeFade = Math.abs(u) > 0.88 ? Math.max(0.0, 1.0 - (Math.abs(u) - 0.88) / 0.12) : 1.0;
        intensity = clamp(hFalloff * vFalloff * edgeFade, 0.0, 1.0);
      }
      if (intensity > 0.001) {
        const idx = (py * W + px) * 4;
        d[idx]     = 255;
        d[idx + 1] = 238;
        d[idx + 2] = 205;
        d[idx + 3] = Math.min(255, Math.round(intensity * 0.72 * 255));
      }
    }
  }
  ctx.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
})();"""

new_ies_block = """const IES_CONE_TEX = (() => {
  const W = 512, H = 768;
  const [c, ctx] = makeCanvas(W, H);
  const img = ctx.createImageData(W, H);
  const d = img.data;
  for (let py = 0; py < H; py++) {
    const v = py / (H - 1); // [0, 1] top to bottom
    for (let px = 0; px < W; px++) {
      const u = (px / (W - 1)) * 2.0 - 1.0; // [-1, 1] horizontally
      let intensity = 0.0;
      if (v > 0.02) {
        const vNorm = Math.max(0.0001, (v - 0.065) / 0.935);
        // Wider spotlight beam cone expansion (0.22 base + 1.25 span)
        const coneWidth = 0.22 + Math.pow(vNorm, 0.70) * 1.25;
        // Smoother, broader horizontal falloff
        const hFalloff = Math.exp(-Math.pow(u / coneWidth, 2) * 2.1);
        let vFalloff = 0.0;
        if (v >= 0.065) {
          vFalloff = Math.sin(Math.pow(vNorm, 0.48) * Math.PI) * (1.0 - 0.25 * v);
        } else {
          // Soft feather at apex
          const ft = (v - 0.02) / 0.045;
          vFalloff = ft * ft * (3.0 - 2.0 * ft) * 0.22;
        }
        // Seamless outer horizontal feather
        const edgeFade = Math.abs(u) > 0.88 ? Math.max(0.0, 1.0 - (Math.abs(u) - 0.88) / 0.12) : 1.0;
        intensity = clamp(hFalloff * vFalloff * edgeFade, 0.0, 1.0);
      }
      if (intensity > 0.001) {
        const idx = (py * W + px) * 4;
        d[idx]     = 255;
        d[idx + 1] = 240;
        d[idx + 2] = 212;
        // Increased brightness: 0.95 peak alpha (was 0.72)
        d[idx + 3] = Math.min(255, Math.round(intensity * 0.95 * 255));
      }
    }
  }
  ctx.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
})();"""

# Normalize CRLF for replacement
content_norm = content.replace('\r\n', '\n')
if old_ies_block in content_norm:
    content_norm = content_norm.replace(old_ies_block, new_ies_block)
    print("Replaced IES_CONE_TEX successfully.")
else:
    print("ERROR: old_ies_block not found!")

# 2. Update ART_SPOT_LIGHTMAP to be wider and brighter across canvas
old_lightmap = """const ART_SPOT_LIGHTMAP = (() => {
  const S = 256;
  const [c, ctx] = makeCanvas(S, S);
  const img = ctx.createImageData(S, S);
  for (let y = 0; y < S; y++) {
    const v = y / (S - 1);
    for (let x = 0; x < S; x++) {
      const u = (x / (S - 1)) * 2.0 - 1.0;
      const coneW = 0.55 + v * 0.65;
      const hSpot = Math.exp(-Math.pow(u / coneW, 2) * 1.45);
      const vSpot = Math.sin(Math.pow(clamp(v * 0.85 + 0.12, 0, 1), 0.65) * Math.PI) * (1.0 - 0.25 * v);
      const vignette = 1.0 - 0.22 * Math.pow(Math.hypot(u, v - 0.45), 1.5);
      const mult = clamp((0.55 + 0.68 * hSpot * vSpot) * vignette, 0.35, 1.15);
      const i = (y * S + x) * 4;
      img.data[i]     = Math.min(255, Math.round(255 * mult));
      img.data[i + 1] = Math.min(255, Math.round(244 * mult));
      img.data[i + 2] = Math.min(255, Math.round(220 * mult));
      img.data[i + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
})();"""

new_lightmap = """const ART_SPOT_LIGHTMAP = (() => {
  const S = 256;
  const [c, ctx] = makeCanvas(S, S);
  const img = ctx.createImageData(S, S);
  for (let y = 0; y < S; y++) {
    const v = y / (S - 1);
    for (let x = 0; x < S; x++) {
      const u = (x / (S - 1)) * 2.0 - 1.0;
      // Wider illumination on canvas (0.75 base + 0.85 expand)
      const coneW = 0.75 + v * 0.85;
      const hSpot = Math.exp(-Math.pow(u / coneW, 2) * 1.15);
      const vSpot = Math.sin(Math.pow(clamp(v * 0.80 + 0.15, 0, 1), 0.60) * Math.PI) * (1.0 - 0.18 * v);
      const vignette = 1.0 - 0.15 * Math.pow(Math.hypot(u, v - 0.45), 1.5);
      // Increased multiplier range: 0.65 to 1.35 (brighter spotlight beam)
      const mult = clamp((0.65 + 0.82 * hSpot * vSpot) * vignette, 0.45, 1.38);
      const i = (y * S + x) * 4;
      img.data[i]     = Math.min(255, Math.round(255 * mult));
      img.data[i + 1] = Math.min(255, Math.round(246 * mult));
      img.data[i + 2] = Math.min(255, Math.round(226 * mult));
      img.data[i + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
})();"""

if old_lightmap in content_norm:
    content_norm = content_norm.replace(old_lightmap, new_lightmap)
    print("Replaced ART_SPOT_LIGHTMAP successfully.")
else:
    print("ERROR: old_lightmap not found!")

# 3. Update ART_TINT and ART_SPOT_INTENSITY
old_art_tint = "const ART_TINT = new THREE.Color(0.52, 0.50, 0.46);"
new_art_tint = "const ART_TINT = new THREE.Color(0.66, 0.64, 0.60);"
if old_art_tint in content_norm:
    content_norm = content_norm.replace(old_art_tint, new_art_tint)
    print("Replaced ART_TINT successfully.")
else:
    print("ERROR: old_art_tint not found!")

old_intensity = "const ART_SPOT_INTENSITY = Math.PI * 1.35;"
new_intensity = "const ART_SPOT_INTENSITY = Math.PI * 1.65;"
if old_intensity in content_norm:
    content_norm = content_norm.replace(old_intensity, new_intensity)
    print("Replaced ART_SPOT_INTENSITY successfully.")
else:
    print("ERROR: old_intensity not found!")

# 4. Make the IES Cone Geometry wider (2.85x artW instead of 2.35x artW)
old_cache = """  iesConeLandscape: new THREE.PlaneGeometry(2.6 * 2.35, 1.95 * 2.45),
  iesConePortrait:  new THREE.PlaneGeometry(1.95 * 2.35, 2.6 * 2.45),"""

new_cache = """  iesConeLandscape: new THREE.PlaneGeometry(2.6 * 2.95, 1.95 * 2.55),
  iesConePortrait:  new THREE.PlaneGeometry(1.95 * 2.95, 2.6 * 2.55),"""

if old_cache in content_norm:
    content_norm = content_norm.replace(old_cache, new_cache)
    print("Replaced FrameGeoCache geometry dimensions successfully.")
else:
    print("ERROR: old_cache not found!")

# 5. Also in buildPictureFrame where fallback PlaneGeometry is created if dynamic size
old_frame_cone = "new THREE.PlaneGeometry(artW * 2.35, artH * 2.45)"
new_frame_cone = "new THREE.PlaneGeometry(artW * 2.95, artH * 2.55)"
if old_frame_cone in content_norm:
    content_norm = content_norm.replace(old_frame_cone, new_frame_cone)
    print("Replaced fallback PlaneGeometry successfully.")
else:
    print("ERROR: old_frame_cone not found!")

# Convert back to CRLF
with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(content_norm)

print("Saved index.html successfully.")

