import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ---------------------------------------------------------------------------
# 1. Darken Floor Textures (checkeredMarble & herringbone) by 0.38x
#    and add ProcTex.blackLouverCeiling and ProcTex.galleryWallWithDado
# ---------------------------------------------------------------------------
proc_tex_start = html.find("const ProcTex = {")
proc_tex_end = html.find("/* --------------------------------------------------------------------------\n   4.3  Procedural paintings")
if proc_tex_end == -1:
    proc_tex_end = html.find("function painterlyPass(")

assert proc_tex_start != -1 and proc_tex_end != -1, "ProcTex bounds not found"

new_proc_tex = '''const ProcTex = {
  /** Neoclassical checkered marble — darkened by 0.38x for moody, sleek gallery floors. */
  checkeredMarble(S = 512) {
    const [c, ctx] = makeCanvas(S, S);
    const img = ctx.createImageData(S, S), d = img.data;
    const { fbm } = makeNoise(1337);
    const tiles = 4, ts = S / tiles;
    const cream = [225, 220, 212], terra = [95, 68, 54];
    const tileRnd = [];
    const tr = rng(77);
    for (let i = 0; i < tiles * tiles; i++) tileRnd.push([tr(), tr(), tr()]);
    for (let y = 0; y < S; y++) {
      for (let x = 0; x < S; x++) {
        const tx = (x / ts) | 0, ty = (y / ts) | 0, odd = (tx + ty) & 1;
        const base = odd ? terra : cream, tRand = tileRnd[ty * tiles + tx];
        const u = x / S, v = y / S;
        const t = fbm(u * 8, v * 8, 4, 8);
        const ang = tRand[0] * Math.PI;
        const m = Math.abs(Math.sin((u * Math.cos(ang) + v * Math.sin(ang)) * 14 + t * 9 + tRand[1] * 10));
        const vein = Math.pow(1 - m, 9) * 0.9 + Math.pow(1 - Math.abs(Math.sin(u * 40 + t * 22)), 30) * 0.25;
        const cloud = 0.9 + fbm(u * 16 + tRand[2] * 3, v * 16, 3, 16) * 0.2;
        let r, g, b;
        if (odd) { r = base[0] * cloud + vein * 45; g = base[1] * cloud + vein * 38; b = base[2] * cloud + vein * 30; }
        else { const k = 1 - vein * 0.38; r = base[0] * cloud * k; g = base[1] * cloud * k; b = base[2] * cloud * k; }
        const ex = Math.min(x % ts, ts - 1 - (x % ts)), ey = Math.min(y % ts, ts - 1 - (y % ts));
        const edge = Math.min(ex, ey);
        if (edge < 1.2) { r = 18; g = 18; b = 18; }
        else if (edge < 3) { r *= 1.04; g *= 1.04; b *= 1.04; }
        // Multiply base RGB by 0.38 for dark, sleek reflective gallery floor
        r *= 0.38; g *= 0.38; b *= 0.38;
        const i = (y * S + x) * 4;
        d[i] = clamp(r, 0, 255); d[i + 1] = clamp(g, 0, 255); d[i + 2] = clamp(b, 0, 255); d[i + 3] = 255;
      }
    }
    ctx.putImageData(img, 0, 0);
    return c;
  },

  /** Dark polished herringbone parquet — RGB multiplied by 0.38 so floor is dark and understated. */
  herringbone(S = 512) {
    const [c, ctx] = makeCanvas(S, S);
    const W = 32, n = 4, L = W * n, P = S / W;
    ctx.fillStyle = '#0b0a09'; ctx.fillRect(0, 0, S, S);
    const rawPalette = [[150, 92, 54], [134, 80, 46], [168, 104, 62], [122, 72, 42], [158, 96, 56], [142, 86, 50]];
    const palette = rawPalette.map(([r, g, b]) => [r * 0.38, g * 0.38, b * 0.38]);
    const plank = (px, py, horizontal) => {
      const kx = ((px % P) + P) % P, ky = ((py % P) + P) % P;
      const r = rng(hashString(`${kx}:${ky}:${horizontal}`));
      const x = px * W, y = py * W, w = horizontal ? L : W, h = horizontal ? W : L;
      if (x > S || y > S || x + w < 0 || y + h < 0) return;
      const col = palette[(r() * palette.length) | 0], k = 0.88 + r() * 0.2;
      ctx.save();
      ctx.beginPath(); ctx.rect(x + 0.8, y + 0.8, w - 1.6, h - 1.6); ctx.clip();
      const g = horizontal ? ctx.createLinearGradient(x, y, x + w, y) : ctx.createLinearGradient(x, y, x, y + h);
      g.addColorStop(0, rgba(col[0] * k * 0.92, col[1] * k * 0.92, col[2] * k * 0.92));
      g.addColorStop(0.5, rgba(col[0] * k * 1.06, col[1] * k * 1.06, col[2] * k * 1.06));
      g.addColorStop(1, rgba(col[0] * k * 0.95, col[1] * k * 0.95, col[2] * k * 0.95));
      ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
      for (let i = 0; i < 12; i++) {
        const off = r() * (horizontal ? h : w), amp = 0.6 + r() * 1.6, freq = 0.02 + r() * 0.05, ph = r() * TAU;
        ctx.strokeStyle = r() > 0.5 ? 'rgba(0,0,0,0.32)' : 'rgba(120,95,65,0.12)';
        ctx.lineWidth = 0.6 + r() * 1.0;
        ctx.beginPath();
        for (let s = 0; s <= (horizontal ? w : h); s += 4) {
          const o = off + Math.sin(s * freq + ph) * amp;
          if (horizontal) (s === 0 ? ctx.moveTo(x + s, y + o) : ctx.lineTo(x + s, y + o));
          else (s === 0 ? ctx.moveTo(x + o, y + s) : ctx.lineTo(x + o, y + s));
        }
        ctx.stroke();
      }
      ctx.restore();
    };
    for (let j = -8; j <= 8; j++) {
      for (let i = -24; i <= 40; i++) {
        const px = i + n * j, py = i - n * j;
        if (px < -n - 1 || px > P + 1 || py < -n - 1 || py > P + 1) continue;
        plank(px, py, true);
        plank(px, py + 1, false);
      }
    }
    return c;
  },

  /** Matte Black Industrial Louvered/Slatted Ceiling (base #0a0b0c with #16181a fine parallel slats). */
  blackLouverCeiling(S = 512) {
    const [c, ctx] = makeCanvas(S, S);
    ctx.fillStyle = '#0a0b0c';
    ctx.fillRect(0, 0, S, S);
    // Fine parallel louver blades
    const step = 8;
    for (let y = 0; y < S; y += step) {
      ctx.fillStyle = '#16181a';
      ctx.fillRect(0, y, S, 3);
      ctx.fillStyle = '#1f2226';
      ctx.fillRect(0, y, S, 1);
    }
    // Cross-grid structural channels every 64px
    for (let x = 0; x < S; x += 64) {
      ctx.fillStyle = '#060708';
      ctx.fillRect(x, 0, 5, S);
      ctx.fillStyle = '#1b1d20';
      ctx.fillRect(x + 1, 0, 2, S);
    }
    return c;
  },

  /**
   * Moody Gallery Wall with Lower Wainscot Dado Rail & Recessed Panels along bottom 0.95m (22.6% of 4.2m wall).
   * Base color in shadow: #383633 (neutral taupe/slate) or #3a1816 (Wing I).
   */
  galleryWallWithDado(S = 512, baseRGB = [56, 54, 51]) {
    const [c, ctx] = makeCanvas(S, S);
    const img = ctx.createImageData(S, S), d = img.data;
    const { fbm } = makeNoise(42);
    const dadoY = Math.round(S * (1.0 - 0.95 / 4.2)); // y = 396 (0.95m from floor)
    const skirtY = Math.round(S * (1.0 - 0.14 / 4.2)); // y = 495 (baseboard)

    for (let y = 0; y < S; y++) {
      const isDadoZone = y >= dadoY;
      for (let x = 0; x < S; x++) {
        const grain = 0.95 + fbm((x / S) * 10, (y / S) * 10, 4, 10) * 0.10;
        // Lower wainscot zone is slightly deeper in tone
        const zoneMul = y >= skirtY ? 0.58 : (isDadoZone ? 0.88 : 1.0);
        const i = (y * S + x) * 4;
        d[i]     = clamp(baseRGB[0] * grain * zoneMul, 0, 255);
        d[i + 1] = clamp(baseRGB[1] * grain * zoneMul, 0, 255);
        d[i + 2] = clamp(baseRGB[2] * grain * zoneMul, 0, 255);
        d[i + 3] = 255;
      }
    }
    ctx.putImageData(img, 0, 0);

    // Subtle vertical architectural wall panel seams above the dado rail (like reference photo)
    for (let x = 0; x < S; x += 128) {
      ctx.fillStyle = 'rgba(0,0,0,0.32)';
      ctx.fillRect(x, 0, 1.5, dadoY);
      ctx.fillStyle = 'rgba(255,248,235,0.05)';
      ctx.fillRect(x + 1.5, 0, 1, dadoY);
    }
    // Horizontal upper picture-rail seam near ceiling
    ctx.fillStyle = 'rgba(0,0,0,0.35)';
    ctx.fillRect(0, 16, S, 2);
    ctx.fillStyle = 'rgba(255,248,235,0.07)';
    ctx.fillRect(0, 18, S, 1.5);

    // Wainscot Dado Rail (horizontal chair-rail molding at 0.95m height)
    ctx.fillStyle = rgba(baseRGB[0] * 1.48, baseRGB[1] * 1.46, baseRGB[2] * 1.42, 0.95);
    ctx.fillRect(0, dadoY - 4, S, 4); // bright top bevel of dado rail catch-light
    ctx.fillStyle = rgba(baseRGB[0] * 1.22, baseRGB[1] * 1.20, baseRGB[2] * 1.18, 0.95);
    ctx.fillRect(0, dadoY, S, 6);     // dado rail face
    ctx.fillStyle = 'rgba(0,0,0,0.55)';
    ctx.fillRect(0, dadoY + 6, S, 4); // crisp underside shadow below dado rail

    // Recessed rectangular architectural panels inside the lower wainscot zone
    const panelTop = dadoY + 18, panelH = skirtY - panelTop - 12;
    const panels = [[22, 234], [278, 490]];
    panels.forEach(([x0, x1]) => {
      const pw = x1 - x0;
      // Slightly darker recessed interior
      ctx.fillStyle = 'rgba(0,0,0,0.16)';
      ctx.fillRect(x0, panelTop, pw, panelH);
      // Fine vertical radiator/louver grooves inside recessed panel
      ctx.fillStyle = 'rgba(0,0,0,0.12)';
      for (let gx = x0 + 8; gx < x1 - 6; gx += 6) {
        ctx.fillRect(gx, panelTop + 5, 2, panelH - 10);
      }
      // Crisp light trim border around recessed panel (matching reference photo)
      ctx.strokeStyle = rgba(baseRGB[0] * 1.42, baseRGB[1] * 1.40, baseRGB[2] * 1.36, 0.85);
      ctx.lineWidth = 2.2;
      ctx.strokeRect(x0 + 1, panelTop + 1, pw - 2, panelH - 2);
      // Inner shadow line
      ctx.strokeStyle = 'rgba(0,0,0,0.45)';
      ctx.lineWidth = 1.2;
      ctx.strokeRect(x0 + 3, panelTop + 3, pw - 6, panelH - 6);
    });

    // Top bevel on baseboard skirting
    ctx.fillStyle = rgba(baseRGB[0] * 1.15, baseRGB[1] * 1.15, baseRGB[2] * 1.12, 0.7);
    ctx.fillRect(0, skirtY, S, 2);
    return c;
  },

  /** Soft plaster (grayscale, multiplied by each wing's wall colour). */
  plaster(S = 256) {
    const [c, ctx] = makeCanvas(S, S);
    const img = ctx.createImageData(S, S), d = img.data, { fbm } = makeNoise(42);
    for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) {
      const v = 0.86 + fbm(x / S * 8, y / S * 8, 4, 8) * 0.14;
      const i = (y * S + x) * 4; d[i] = d[i + 1] = d[i + 2] = v * 255; d[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
    return c;
  },

  /** Subtle damask wall-silk for the Classical Wing. */
  damask(S = 512) {
    return ProcTex.galleryWallWithDado(S, [58, 24, 22]);
  },

  /** Polished white statuary marble (sculptures, pedestals). */
  whiteMarble(S = 512, tint = [251, 255, 254], veinColor = [190, 155, 100]) {
    const [c, ctx] = makeCanvas(S, S);
    const img = ctx.createImageData(S, S), d = img.data, { fbm } = makeNoise(9001);
    for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) {
      const u = x / S, v = y / S;
      const t = fbm(u * 6, v * 6, 5, 6);
      const m = Math.abs(Math.sin((u * 3 + v * 2) * TAU + t * 10));
      const vein = Math.pow(1 - m, 14);
      const cloud = 0.93 + fbm(u * 12, v * 12, 3, 12) * 0.1;
      const i = (y * S + x) * 4;
      for (let k = 0; k < 3; k++) d[i + k] = clamp(lerp(tint[k] * cloud, veinColor[k], vein * 0.7), 0, 255);
      d[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
    return c;
  },

  /** Coffered ceiling panel (recessed square with rosette). */
  coffer(S = 512, base = [251, 255, 254], rosette = '#e6af2e') {
    return ProcTex.blackLouverCeiling(S);
  }
};

'''

html = html[:proc_tex_start] + new_proc_tex + html[proc_tex_end:]

# ---------------------------------------------------------------------------
# 2. Set renderer.toneMappingExposure = 0.75 & moody scene fog/background
# ---------------------------------------------------------------------------
html = re.sub(
    r'renderer\.toneMappingExposure\s*=\s*[0-9.]+;',
    'renderer.toneMappingExposure = 0.75;',
    html
)
html = re.sub(
    r'scene\.environmentIntensity\s*=\s*[0-9.]+;',
    'scene.environmentIntensity = 0.05;',
    html
)

# ---------------------------------------------------------------------------
# 3. Update Materials (Mat) for blackLouverCeiling, galleryWallWithDado, and dark floors
# ---------------------------------------------------------------------------
mat_start = html.find("const M_CHECKER =")
mat_end = html.find("/* --------------------------------------------------------------------------\n   4.7  Collider system")
assert mat_start != -1 and mat_end != -1, "Mat section not found"

new_mat_section = '''const M_CHECKER = managedTexture(ProcTex.checkeredMarble(512), EUNOIA_CONFIG.textures?.floorMarble, { repeat: true });
M_CHECKER.repeat.set(7, 7);

const M_HERRING = managedTexture(ProcTex.herringbone(512), EUNOIA_CONFIG.textures?.floorWood, { repeat: true });
M_HERRING.repeat.set(6, 6);

const T_PLASTER = new THREE.CanvasTexture(ProcTex.galleryWallWithDado(512, [56, 54, 51]));
T_PLASTER.colorSpace = THREE.SRGBColorSpace;
T_PLASTER.wrapS = THREE.RepeatWrapping;
T_PLASTER.wrapT = THREE.ClampToEdgeWrapping;
T_PLASTER.repeat.set(1, 1);
T_PLASTER.anisotropy = MAX_ANISO;

const T_DAMASK = new THREE.CanvasTexture(ProcTex.galleryWallWithDado(512, [58, 24, 22]));
T_DAMASK.colorSpace = THREE.SRGBColorSpace;
T_DAMASK.wrapS = THREE.RepeatWrapping;
T_DAMASK.wrapT = THREE.ClampToEdgeWrapping;
T_DAMASK.repeat.set(1, 1);
T_DAMASK.anisotropy = MAX_ANISO;

const T_WHITE_MARBLE = new THREE.CanvasTexture(ProcTex.whiteMarble(512, [150, 146, 140], [95, 85, 70]));
T_WHITE_MARBLE.colorSpace = THREE.SRGBColorSpace;
T_WHITE_MARBLE.wrapS = T_WHITE_MARBLE.wrapT = THREE.RepeatWrapping;
T_WHITE_MARBLE.repeat.set(2, 2);
T_WHITE_MARBLE.anisotropy = MAX_ANISO;

const T_LOUVER_CEIL = new THREE.CanvasTexture(ProcTex.blackLouverCeiling(512));
T_LOUVER_CEIL.colorSpace = THREE.SRGBColorSpace;
T_LOUVER_CEIL.wrapS = T_LOUVER_CEIL.wrapT = THREE.RepeatWrapping;
T_LOUVER_CEIL.repeat.set(10, 10);
T_LOUVER_CEIL.anisotropy = MAX_ANISO;

const T_COFFER_ROT = T_LOUVER_CEIL;

const Mat = {
  floorRotunda: new THREE.MeshStandardMaterial({ map: M_CHECKER, roughness: 0.20, metalness: 0.08 }),
  floorWingI:   new THREE.MeshStandardMaterial({ map: M_HERRING, roughness: 0.20, metalness: 0.08 }),
  floorWingII:  new THREE.MeshStandardMaterial({ map: M_CHECKER, roughness: 0.20, metalness: 0.08 }),
  floorWingIII: new THREE.MeshStandardMaterial({ map: M_HERRING, roughness: 0.20, metalness: 0.08 }),

  wallRotunda:  new THREE.MeshStandardMaterial({ color: 0x383633, map: T_PLASTER, emissive: 0xffffff, emissiveMap: T_PLASTER, emissiveIntensity: 0.85, roughness: 0.85 }),
  ceilingRot:   new THREE.MeshStandardMaterial({ color: 0xffffff, map: T_LOUVER_CEIL, emissive: 0xffffff, emissiveMap: T_LOUVER_CEIL, emissiveIntensity: 0.85, roughness: 0.92 }),
  archTrim:     new THREE.MeshStandardMaterial({ color: 0x282725, emissive: 0x1e1d1b, roughness: 0.55 }),

  wallWingI:    new THREE.MeshStandardMaterial({ color: 0x3a1816, map: T_DAMASK, emissive: 0xffffff, emissiveMap: T_DAMASK, emissiveIntensity: 0.88, roughness: 0.78 }),
  trimWingI:    new THREE.MeshStandardMaterial({ color: 0x240e0c, roughness: 0.5 }),
  ceilingWingI: new THREE.MeshStandardMaterial({ color: 0xffffff, map: T_LOUVER_CEIL, emissive: 0xffffff, emissiveMap: T_LOUVER_CEIL, emissiveIntensity: 0.90, roughness: 0.92 }),

  wallWingII:   new THREE.MeshStandardMaterial({ color: 0x383633, map: T_PLASTER, emissive: 0xffffff, emissiveMap: T_PLASTER, emissiveIntensity: 0.88, roughness: 0.88 }),
  trimWingII:   new THREE.MeshStandardMaterial({ color: 0x181716, roughness: 0.45 }),
  ceilingWingII:new THREE.MeshStandardMaterial({ color: 0xffffff, map: T_LOUVER_CEIL, emissive: 0xffffff, emissiveMap: T_LOUVER_CEIL, emissiveIntensity: 0.90, roughness: 0.92 }),

  wallWingIII:  new THREE.MeshStandardMaterial({ color: 0x383633, map: T_PLASTER, emissive: 0xffffff, emissiveMap: T_PLASTER, emissiveIntensity: 0.82, roughness: 0.92 }),
  trimWingIII:  new THREE.MeshStandardMaterial({ color: 0x141413, roughness: 0.5 }),
  ceilingWingIII:new THREE.MeshStandardMaterial({ color: 0xffffff, map: T_LOUVER_CEIL, emissive: 0xffffff, emissiveMap: T_LOUVER_CEIL, emissiveIntensity: 0.90, roughness: 0.92 }),

  flutedColumn: new THREE.MeshStandardMaterial({ color: 0x45423e, map: T_WHITE_MARBLE, emissive: 0x282623, roughness: 0.35, metalness: 0.05 }),
  pedestal:     new THREE.MeshStandardMaterial({ color: 0x181715, emissive: 0x100f0e, roughness: 0.32, metalness: 0.15 }),
  goldLeaf:     new THREE.MeshStandardMaterial({ color: 0x6e521b, emissive: 0x38280b, roughness: 0.32, metalness: 0.65 }),
  darkWood:     new THREE.MeshStandardMaterial({ color: 0x382214, emissive: 0x1f120a, roughness: 0.45, metalness: 0.08 }),
  bronze:       new THREE.MeshStandardMaterial({ color: 0x4a381c, emissive: 0x241b0c, roughness: 0.35, metalness: 0.65 }),
  blackVelvet:  new THREE.MeshStandardMaterial({ color: 0x121212, roughness: 0.88 }),
  crimsonVelvet:new THREE.MeshStandardMaterial({ color: 0x3a1010, roughness: 0.85 }),
  alabaster:    new THREE.MeshStandardMaterial({ color: 0x4d4942, emissive: 0x2a2723, roughness: 0.40, metalness: 0.05 })
};

'''

html = html[:mat_start] + new_mat_section + html[mat_end:]

# ---------------------------------------------------------------------------
# 4. Update addSolidWall so wall UVs map 1:1 vertically [0, H_WING] (keeping 0.95m dado rail exact)
#    and uniformly every 4.2m horizontally
# ---------------------------------------------------------------------------
solid_wall_old = '''    const geo = new THREE.BoxGeometry(0.24, h, len);
    const mesh = new THREE.Mesh(geo, mat);'''

solid_wall_new = '''    const geo = new THREE.BoxGeometry(0.24, h, len);
    const uvAttr = geo.attributes.uv;
    const posAttr = geo.attributes.position;
    const normAttr = geo.attributes.normal;
    const tileW = 4.2;
    for (let vi = 0; vi < uvAttr.count; vi++) {
      const wy = posAttr.getY(vi) + midY;
      const v = clamp(wy / H_WING, 0, 1);
      const u = Math.abs(normAttr.getX(vi)) > 0.5
        ? (posAttr.getZ(vi) + len / 2) / tileW
        : (posAttr.getX(vi) + 0.12) / tileW;
      uvAttr.setXY(vi, u, v);
    }
    const mesh = new THREE.Mesh(geo, mat);'''

assert solid_wall_old in html, "addSolidWall snippet not found"
html = html.replace(solid_wall_old, solid_wall_new, 1)

# ---------------------------------------------------------------------------
# 5. Update FrameGeoCache & buildPictureFrame:
#    - True IES Parabolic Hyperbola Texture (512x768) + PlaneGeometry(artW * 2.35, artH * 2.45) at z = 0.005
#    - Offset Frame Drop-Shadow (PlaneGeometry(artW + 0.44, artH + 0.44)) at (0.07, -0.09, 0.01)
#    - Stop "Neon TV Screen" Art Glow (0.52 brightness + top-down spotlight vignette)
#    - Remove brass picture-frame lamp meshes completely
# ---------------------------------------------------------------------------
fgc_start = html.find("const FrameGeoCache = {")
fgc_end = html.find("const activeHogwartsVideos = [];")
assert fgc_start != -1 and fgc_end != -1, "FrameGeoCache bounds not found"

new_fgc_section = '''/* 1. Shared Procedural IES Parabolic Hyperbola Texture (512x768 CanvasTexture) */
const IES_CONE_TEX = (() => {
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
})();

const IES_CONE_MAT = new THREE.MeshBasicMaterial({
  map: IES_CONE_TEX,
  transparent: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false
});
IES_CONE_MAT.toneMapped = false;

/* 2. Shared Radial-Box Frame Drop-Shadow Texture (rgba(0, 0, 0, 0.78)) */
const DROP_SHADOW_TEX = (() => {
  const S = 256;
  const [c, ctx] = makeCanvas(S, S);
  const img = ctx.createImageData(S, S);
  const d = img.data;
  for (let y = 0; y < S; y++) {
    const ny = Math.abs(y / (S - 1) * 2.0 - 1.0);
    for (let x = 0; x < S; x++) {
      const nx = Math.abs(x / (S - 1) * 2.0 - 1.0);
      const dx = Math.max(0.0, nx - 0.76) / 0.24;
      const dy = Math.max(0.0, ny - 0.76) / 0.24;
      const dist = Math.hypot(dx, dy);
      if (dist < 1.0) {
        const a = 0.78 * Math.pow(0.5 + 0.5 * Math.cos(dist * Math.PI), 1.35);
        const idx = (y * S + x) * 4;
        d[idx] = 0; d[idx + 1] = 0; d[idx + 2] = 0;
        d[idx + 3] = Math.min(255, Math.round(a * 255));
      }
    }
  }
  ctx.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
})();

const DROP_SHADOW_MAT = new THREE.MeshBasicMaterial({
  map: DROP_SHADOW_TEX,
  transparent: true,
  depthWrite: false
});

const FrameGeoCache = {
  backLandscape: new RoundedBoxGeometry(2.6 + 0.32, 1.95 + 0.32, 0.12, 2, 0.02),
  backPortrait:  new RoundedBoxGeometry(1.95 + 0.32, 2.6 + 0.32, 0.12, 2, 0.02),
  linerLandscape: new RoundedBoxGeometry(2.6 + 0.08, 1.95 + 0.08, 0.13, 2, 0.01),
  linerPortrait:  new RoundedBoxGeometry(1.95 + 0.08, 2.6 + 0.08, 0.13, 2, 0.01),
  canvasLandscape: new THREE.PlaneGeometry(2.6, 1.95),
  canvasPortrait:  new THREE.PlaneGeometry(1.95, 2.6),
  plaque: new THREE.PlaneGeometry(0.7, 0.28),
  iesConeTex: IES_CONE_TEX,
  iesConeLandscape: new THREE.PlaneGeometry(2.6 * 2.35, 1.95 * 2.45),
  iesConePortrait:  new THREE.PlaneGeometry(1.95 * 2.35, 2.6 * 2.45),
  shadowLandscape: new THREE.PlaneGeometry(2.6 + 0.44, 1.95 + 0.44),
  shadowPortrait:  new THREE.PlaneGeometry(1.95 + 0.44, 2.6 + 0.44)
};

/* Gallery Hanging Wires: sleek vertical wires extending from frame top up towards ceiling track */
function buildHangingWires(artW, artH) {
  const parts = [];
  const wireH = Math.max(0.4, H_WING - 2.15 - artH / 2);
  const wireGeo = new THREE.CylinderGeometry(0.0025, 0.0025, wireH, 4);
  const wireY = artH / 2 + wireH / 2;
  const sx = artW * 0.42;
  [-sx, sx].forEach((x) => {
    const w = wireGeo.clone();
    w.translate(x, wireY, 0.008);
    parts.push(w);
  });
  const flatParts = parts.map((p) => (p.index ? p.toNonIndexed() : p));
  const merged = mergeGeometries(flatParts, false);
  parts.forEach((p) => p.dispose()); flatParts.forEach((p) => p.dispose());
  return merged;
}
FrameGeoCache.wiresLandscape = buildHangingWires(2.6, 1.95);
FrameGeoCache.wiresPortrait = buildHangingWires(1.95, 2.6);
const WIRE_MAT = new THREE.MeshBasicMaterial({ color: 0x8a8680 });

/* Two shared procedural fallbacks for ALL frames (instead of 180 painterly canvases). */
function makeSharedFallback(orientation, w, h, seed) {
  const src = paintArtwork('gallery', orientation, seed);
  const [c, ctx] = makeCanvas(w, h);
  ctx.drawImage(src, 0, 0, w, h);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.generateMipmaps = false;
  t.minFilter = THREE.LinearFilter;
  t.magFilter = THREE.LinearFilter;
  return t;
}
const SHARED_FALLBACK_LANDSCAPE = makeSharedFallback('landscape', 512, 384, 1337);
const SHARED_FALLBACK_PORTRAIT = makeSharedFallback('portrait', 384, 512, 7331);
// Reduced base canvas brightness (0.52) so paintings look physically illuminated rather than glowing like monitors
const ART_TINT = new THREE.Color(0.52, 0.50, 0.46);

/* Top-down spotlight vignette baked onto the canvas: brightest in upper-center under the overhead beam,
   with natural falloff toward the lower corners. */
const ART_SPOT_LIGHTMAP = (() => {
  const S = 256;
  const [c, ctx] = makeCanvas(S, S);
  const img = ctx.createImageData(S, S);
  for (let y = 0; y < S; y++) {
    const v = y / (S - 1); // 0 = top, 1 = bottom
    for (let x = 0; x < S; x++) {
      const u = (x / (S - 1)) * 2.0 - 1.0; // -1 to 1
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
})();
const ART_SPOT_INTENSITY = Math.PI * 1.35;

'''

html = html[:fgc_start] + new_fgc_section + html[fgc_end:]

# Update buildPictureFrame
bpf_start = html.find("function buildPictureFrame(exhibit, width, height) {")
bpf_end = html.find("/* --------------------------------------------------------------------------\n   4.10  EXHIBIT SPOTS")
assert bpf_start != -1 and bpf_end != -1, "buildPictureFrame bounds not found"

new_bpf = '''function buildPictureFrame(exhibit, width, height) {
  const group = new THREE.Group();

  const isLandscape = exhibit.orientation === 'landscape';
  const artW = width || (isLandscape ? 2.6 : 1.95);
  const artH = height || (isLandscape ? 1.95 : 2.6);
  const frameDepth = 0.12;

  let frameMat = Mat.goldLeaf;
  if (exhibit.wing === 'II') frameMat = Mat.darkWood;
  if (exhibit.wing === 'III') frameMat = Mat.pedestal;
  if (exhibit.wing === 'IV') frameMat = Mat.bronze;

  const flat = (m) => { m.castShadow = false; m.receiveShadow = false; m.matrixAutoUpdate = false; m.updateMatrix(); return m; };

  // 1. True IES Parabolic Wall-Wash Light Cone (z = 0.005, flush against wall behind frame)
  const iesGeo = (artW === 2.6 && artH === 1.95) ? FrameGeoCache.iesConeLandscape
               : (artW === 1.95 && artH === 2.6) ? FrameGeoCache.iesConePortrait
               : new THREE.PlaneGeometry(artW * 2.35, artH * 2.45);
  const iesConeMesh = new THREE.Mesh(iesGeo, IES_CONE_MAT);
  // Positioned at x = 0, shifted slightly up (y = artH * 0.18, clamped so top stays below ceiling)
  const coneH = artH * 2.45;
  const maxConeY = (H_WING - 2.15 - 0.02) - (coneH * 0.42);
  iesConeMesh.position.set(0, Math.min(artH * 0.18, maxConeY), 0.005);
  iesConeMesh.renderOrder = 1;
  group.add(flat(iesConeMesh));

  // 2. Physical Offset Frame Drop-Shadow (x = 0.07, y = -0.09, z = 0.01)
  const shadowGeo = (artW === 2.6 && artH === 1.95) ? FrameGeoCache.shadowLandscape
                  : (artW === 1.95 && artH === 2.6) ? FrameGeoCache.shadowPortrait
                  : new THREE.PlaneGeometry(artW + 0.44, artH + 0.44);
  const shadowMesh = new THREE.Mesh(shadowGeo, DROP_SHADOW_MAT);
  shadowMesh.position.set(0.07, -0.09, 0.01);
  shadowMesh.renderOrder = 2;
  group.add(flat(shadowMesh));

  // 3. Frame Molding & Inner Liner (front face at z = +0.06 occludes cone & shadow behind frame)
  const frameBack = flat(new THREE.Mesh(isLandscape ? FrameGeoCache.backLandscape : FrameGeoCache.backPortrait, frameMat));
  group.add(frameBack);

  const linerMat = exhibit.wing === 'II' ? Mat.goldLeaf : Mat.alabaster;
  const liner = flat(new THREE.Mesh(isLandscape ? FrameGeoCache.linerLandscape : FrameGeoCache.linerPortrait, linerMat));
  group.add(liner);

  // 4. Artwork Canvas with 0.52 baseline & top-down spotlight vignette (no neon glow)
  const fallbackTex = isLandscape ? SHARED_FALLBACK_LANDSCAPE : SHARED_FALLBACK_PORTRAIT;
  const artMat = new THREE.MeshBasicMaterial({
    map: fallbackTex,
    color: ART_TINT,
    lightMap: ART_SPOT_LIGHTMAP,
    lightMapIntensity: ART_SPOT_INTENSITY
  });

  if (exhibit.mediaType === 'video') {
    const video = document.createElement('video');
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
    video.preload = 'none';

    activeHogwartsVideos.push({
      video, videoTex: null, group, artMat, fallbackTex,
      srcPath: exhibit.imagePath, srcSet: false, dSq: Infinity,
      wing: exhibit.wing, room: exhibit.room
    });
  } else if (exhibit.imagePath) {
    loadTracker.total++;
    TextureLoadQueue.enqueue({ url: exhibit.imagePath, artMat, group, wing: exhibit.wing });
  }

  const canvasGeo = isLandscape ? FrameGeoCache.canvasLandscape : FrameGeoCache.canvasPortrait;
  const artCanvasMesh = new THREE.Mesh(canvasGeo, artMat);
  artCanvasMesh.position.z = frameDepth / 2 + 0.015;
  artCanvasMesh.castShadow = false;
  artCanvasMesh.receiveShadow = false;
  group.add(artCanvasMesh);

  artCanvasMesh.userData = { exhibit, group };
  exhibitMeshes.push(artCanvasMesh);
  exhibitDataMap.set(artCanvasMesh.uuid, exhibit);

  // Museum wall plaque: 256x96 canvas
  const plaqueTex = textTexture(256, 96, (ctx, cw, ch) => {
    ctx.save();
    ctx.scale(cw / 512, ch / 192);
    const w = 512, h = 192;
    ctx.fillStyle = '#0d0e0e';
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#9e7824';
    ctx.lineWidth = 4;
    ctx.strokeRect(6, 6, w - 12, h - 12);
    ctx.fillStyle = '#c49735';
    ctx.font = `600 22px ${SANS}`;
    ctx.textAlign = 'center';
    ctx.fillText(`${(exhibit.category || '').toUpperCase()} · ${exhibit.year || ''}`, w / 2, 42);
    if (exhibit.title) {
      ctx.fillStyle = '#e0dcd3';
      ctx.font = `600 32px ${SERIF}`;
      wrapText(ctx, exhibit.title, w / 2, 88, w - 40, 36);
      ctx.fillStyle = '#9a968e';
      ctx.font = `italic 20px ${SERIF}`;
      ctx.fillText(exhibit.subtitle || '', w / 2, 154);
    } else {
      ctx.fillStyle = '#e0dcd3';
      ctx.font = `italic 24px ${SERIF}`;
      ctx.fillText(exhibit.category || '', w / 2, 108);
    }
    ctx.restore();
  });
  plaqueTex.generateMipmaps = false;
  plaqueTex.minFilter = THREE.LinearFilter;
  plaqueTex.anisotropy = 1;

  const plaqueMesh = new THREE.Mesh(FrameGeoCache.plaque, new THREE.MeshBasicMaterial({ map: plaqueTex, color: 0x99948a }));
  plaqueMesh.position.set(0, -artH / 2 - 0.30, frameDepth / 2);
  group.add(flat(plaqueMesh));

  // Sleek gallery hanging wires extending from top of frame to ceiling rail (no brass frame lamp!)
  const wiresGeo = artH === 1.95 ? FrameGeoCache.wiresLandscape
                 : artH === 2.6 ? FrameGeoCache.wiresPortrait
                 : buildHangingWires(artW, artH);
  const wiresMesh = flat(new THREE.Mesh(wiresGeo, WIRE_MAT));
  group.add(wiresMesh);

  return { group, artCanvasMesh, artW, artH };
}

'''

html = html[:bpf_start] + new_bpf + html[bpf_end:]

# ---------------------------------------------------------------------------
# 6. Update buildTrackLight / buildLightPools and layoutExhibits + buildLighting
# ---------------------------------------------------------------------------
blp_start = html.find("function buildLightPools(poolSpots) {")
bl_end = html.find("/* --------------------------------------------------------------------------\n   4.12  PROCEDURAL WEB AUDIO")
assert blp_start != -1 and bl_end != -1, "buildLightPools..buildLighting bounds not found"

new_lighting_pipeline = '''function buildTrackLight(poolSpots) {
  // White rectangular track rails (#d8d6d0) at 1.6m from each wall (y = H_WING - 0.15),
  // with angled white cylindrical spotlight cans (CylinderGeometry(0.055, 0.055, 0.22, 12))
  // aimed at each painting and a bright warm emissive lens (0xfff2cc) on the front of each can.
  const trackMat = new THREE.MeshBasicMaterial({ color: 0xd8d6d0 });
  const clampMat = new THREE.MeshBasicMaterial({ color: 0x222324 });
  const lensMat = new THREE.MeshBasicMaterial({ color: 0xfff2cc });
  lensMat.toneMapped = false;

  // Soft warm floor bounce reflection under each lit painting
  const [fc, fctx] = makeCanvas(256, 128);
  const fg = fctx.createRadialGradient(128, 64, 0, 128, 64, 120);
  fg.addColorStop(0.00, 'rgba(255,232,190,0.45)');
  fg.addColorStop(0.45, 'rgba(255,215,160,0.18)');
  fg.addColorStop(1.00, 'rgba(255,200,130,0)');
  fctx.fillStyle = fg; fctx.fillRect(0, 0, 256, 128);
  const floorPoolTex = new THREE.CanvasTexture(fc);
  floorPoolTex.colorSpace = THREE.SRGBColorSpace;
  const floorPoolMat = new THREE.MeshBasicMaterial({
    map: floorPoolTex, transparent: true, opacity: 0.28,
    blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide
  });
  floorPoolMat.toneMapped = false;

  const wingGroups = { I: wingI_group, II: wingII_group, III: wingIII_group, IV: wingIV_group };

  Object.keys(poolSpots).forEach((wing) => {
    const trackGeos = [];
    const clampGeos = [];
    const lensGeos = [];
    const floorGeos = [];

    poolSpots[wing].forEach((s) => {
      const isLand = s.land;
      const artW = isLand ? 2.6 : 1.95;

      // Track rail parallel to wall at 1.6m distance, y = H_WING - 0.15
      const trackDist = 1.6;
      const railY = (H_WING - 0.15) - s.y;
      const railW = artW + 2.4; // connects into continuous architectural track runs

      const gRail = new THREE.BoxGeometry(railW, 0.042, 0.055);
      gRail.translate(0, railY, trackDist);
      gRail.rotateY(s.rotY);
      gRail.translate(s.x, s.y, s.z);
      trackGeos.push(gRail);

      // Vertical suspension stems up to the slatted black ceiling
      [-artW * 0.45, artW * 0.45].forEach((rx) => {
        const gStem = new THREE.CylinderGeometry(0.006, 0.006, 0.15, 6);
        gStem.translate(rx, railY + 0.075, trackDist);
        gStem.rotateY(s.rotY);
        gStem.translate(s.x, s.y, s.z);
        clampGeos.push(gStem);
      });

      // Angled white cylindrical spotlight cans (CylinderGeometry(0.055, 0.055, 0.22, 12))
      const headOffsets = isLand ? [-0.42, 0.42] : [0.0];
      const canY = railY - 0.12;
      const spotAngle = Math.atan2(trackDist, canY - 0.15);

      headOffsets.forEach((hx) => {
        // Track adapter box
        const gBox = new THREE.BoxGeometry(0.048, 0.036, 0.075);
        gBox.translate(hx, railY - 0.032, trackDist);
        gBox.rotateY(s.rotY);
        gBox.translate(s.x, s.y, s.z);
        trackGeos.push(gBox);

        // White cylindrical spotlight can aimed at painting
        const gCan = new THREE.CylinderGeometry(0.055, 0.055, 0.22, 12);
        gCan.rotateX(Math.PI / 2);
        gCan.rotateX(-spotAngle);
        gCan.translate(hx, canY, trackDist);
        gCan.rotateY(s.rotY);
        gCan.translate(s.x, s.y, s.z);
        trackGeos.push(gCan);

        // Bright warm emissive lens (0xfff2cc) on the front of each can
        const gLens = new THREE.CircleGeometry(0.052, 12);
        gLens.rotateX(Math.PI);
        gLens.rotateX(-spotAngle);
        const lensOffZ = trackDist - Math.sin(spotAngle) * 0.112;
        const lensOffY = canY - Math.cos(spotAngle) * 0.112;
        gLens.translate(hx, lensOffY, lensOffZ);
        gLens.rotateY(s.rotY);
        gLens.translate(s.x, s.y, s.z);
        lensGeos.push(gLens);
      });

      // Subtle floor reflection pool
      const gFloor = new THREE.PlaneGeometry(artW + 1.2, 1.8);
      gFloor.rotateX(-Math.PI / 2);
      gFloor.translate(0, 0.015, 1.15);
      gFloor.rotateY(s.rotY);
      gFloor.translate(s.x, 0, s.z);
      floorGeos.push(gFloor);
    });

    const mergeAndEmit = (list, mat, order) => {
      if (!list.length) return;
      const flat = list.map((p) => (p.index ? p.toNonIndexed() : p));
      const merged = mergeGeometries(flat, false);
      list.forEach((g) => g.dispose()); flat.forEach((p) => p.dispose());
      const mesh = new THREE.Mesh(merged, mat);
      mesh.renderOrder = order;
      mesh.frustumCulled = false;
      mesh.matrixAutoUpdate = false;
      wingGroups[wing].add(mesh);
    };

    mergeAndEmit(trackGeos, trackMat, 1);
    mergeAndEmit(clampGeos, clampMat, 1);
    mergeAndEmit(lensGeos, lensMat, 1);
    mergeAndEmit(floorGeos, floorPoolMat, 1);
  });
}

function buildLightPools(poolSpots) {
  buildTrackLight(poolSpots);
}

function buildMuseumAtmosphere() {
  // Keep wings moody and free of ceiling rings; only place subtle floor glow in Grand Rotunda
  const [c, ctx] = makeCanvas(256, 256);
  const g = ctx.createRadialGradient(128, 128, 0, 128, 128, 128);
  g.addColorStop(0.00, 'rgba(255,230,185,0.45)');
  g.addColorStop(0.50, 'rgba(255,210,150,0.14)');
  g.addColorStop(1.00, 'rgba(255,190,120,0)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, 256, 256);
  const poolTex = new THREE.CanvasTexture(c);
  poolTex.colorSpace = THREE.SRGBColorSpace;
  const poolMat = new THREE.MeshBasicMaterial({
    map: poolTex, transparent: true, opacity: 0.35,
    blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide
  });
  poolMat.toneMapped = false;
  const ringPool = new THREE.Mesh(new THREE.PlaneGeometry(7.5, 7.5), poolMat);
  ringPool.rotation.x = -Math.PI / 2;
  ringPool.position.y = 0.016;
  rotunda_group.add(ringPool);
}

function layoutExhibits() {
  const poolSpots = {};
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

      // Hang frames just above the 0.95m wainscot dado rail so the parabolic IES cone
      // has ~0.85m of upper gallery wall to arch above each frame (matching reference photo)
      const hangY = ex.orientation === 'landscape' ? 2.15 : 2.12;

      const { group } = buildPictureFrame(ex);
      group.position.set(spot.x, hangY, spot.z);
      group.rotation.y = spot.rotY;
      group.updateMatrix();

      if (ex.wing === 'I') wingI_group.add(group);
      else if (ex.wing === 'II') wingII_group.add(group);
      else if (ex.wing === 'III') wingIII_group.add(group);
      else if (ex.wing === 'IV') wingIV_group.add(group);
      else scene.add(group);

      ex.teleportPos = new THREE.Vector3(spot.viewX, EYE_HEIGHT, spot.viewZ);
      ex.lookTarget = new THREE.Vector3(spot.x, hangY, spot.z);
      (poolSpots[ex.wing] = poolSpots[ex.wing] || []).push({
        x: spot.x, y: hangY, z: spot.z, rotY: spot.rotY,
        land: ex.orientation === 'landscape'
      });
      hungCount++;
    });
  }
  buildTrackLight(poolSpots);
  console.log(`Successfully hung ${hungCount} exhibits in 3D museum!`);
}

/* --------------------------------------------------------------------------
   4.11  LIGHTING PIPELINE
   -------------------------------------------------------------------------- */
function buildLighting() {
  // 4.1 Dark Ambient Baseline: HemisphereLight 0.14, AmbientLight 0.10, toneMappingExposure 0.75
  const hemi = new THREE.HemisphereLight(0xf4e6d4, 0x100c08, 0.14);
  scene.add(hemi);

  const amb = new THREE.AmbientLight(0xfff3e2, 0.10);
  scene.add(amb);

  // Subtle visitor lantern so camera never washes out the moody walls
  const visitorLantern = new THREE.PointLight(0xffeed4, 0.28, 9.0, 1.6);
  camera.add(visitorLantern);
  scene.add(camera);

  // Rotunda skylight: global, NO shadow map
  const rotundaSun = new THREE.SpotLight(0xffeaad, 18, 22, Math.PI / 3.2, 0.65, 1.2);
  rotundaSun.position.set(0, H_ROT + 1.2, 0);
  rotundaSun.target.position.set(0, 0, 0);
  rotundaSun.castShadow = false;
  scene.add(rotundaSun, rotundaSun.target);

  // Baked soft contact shadow under the central sculpture
  const [sc, sctx] = makeCanvas(256, 256);
  const grad = sctx.createRadialGradient(128, 128, 20, 128, 128, 128);
  grad.addColorStop(0, 'rgba(0,0,0,0.65)');
  grad.addColorStop(1, 'rgba(0,0,0,0)');
  sctx.fillStyle = grad; sctx.fillRect(0, 0, 256, 256);
  const shadowTex = new THREE.CanvasTexture(sc);
  const bakedShadow = new THREE.Mesh(
    new THREE.PlaneGeometry(4.6, 4.6),
    new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false })
  );
  bakedShadow.rotation.x = -Math.PI / 2;
  bakedShadow.position.y = 0.012;
  rotunda_group.add(bakedShadow);
}

'''

html = html[:blp_start] + new_lighting_pipeline + html[bl_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully applied all 5 visual upgrades to index.html!")

