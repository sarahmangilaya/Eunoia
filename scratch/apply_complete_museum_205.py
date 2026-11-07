import json, os, re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update EUNOIA_CONFIG.exhibits
with open('scratch/full_catalog.json', 'r', encoding='utf-8') as f:
    full_catalog = json.load(f)

print(f"Catalog has {len(full_catalog)} items.")
start_ex = content.find('  exhibits: [')
if start_ex == -1:
    raise ValueError("exhibits: [ not found")

end_ex = content.find(']\n};\n\n/* ==========================================================================\n   §4  ENGINE')
if end_ex == -1:
    raise ValueError("end of exhibits not found")

new_catalog_str = "  exhibits: " + json.dumps(full_catalog, indent=4, ensure_ascii=False) + "\n};"
content = content[:start_ex] + new_catalog_str + content[end_ex + len(']\n};'):]
print("Updated EUNOIA_CONFIG.exhibits in content!")

# 2. Update Architecture section
# From: '  /* --- 2. Build the three connected wings --- */'
# To: '/* --------------------------------------------------------------------------\n   4.10  FRAMES, EXHIBIT HANGING'
start_arch = content.find('/* --- 2. Build the three connected wings --- */')
if start_arch == -1:
    start_arch = content.find('/* ==========================================================================\n     §4.9 MUSEUM ARCHITECTURE')
if start_arch == -1:
    start_arch = content.find('§4.9 MUSEUM ARCHITECTURE')
if start_arch == -1:
    raise ValueError("start_arch not found")

end_arch = content.find('/* --------------------------------------------------------------------------\n   4.10  FRAMES, EXHIBIT HANGING')
if end_arch == -1:
    raise ValueError("end_arch not found")

# Let's read generated_arch.js up to '/* --------------------------------------------------------------------------\n   4.10  EXHIBIT SPOTS'
with open('scratch/generated_arch.js', 'r', encoding='utf-8') as f:
    gen_js = f.read()

split_token = '/* --------------------------------------------------------------------------\n   4.10  EXHIBIT SPOTS'
arch_part, spots_and_layout_part = gen_js.split(split_token)

content = content[:start_arch] + arch_part.strip() + "\n\n" + content[end_arch:]
print("Updated Architecture section in content!")

# 3. Update layoutExhibits section
# From: 'function layoutExhibits() {'
# To: '/* --------------------------------------------------------------------------\n   4.11  LIGHTING PIPELINE'
start_layout = content.find('const EXHIBIT_SPOTS =')
if start_layout == -1:
    start_layout = content.find('function layoutExhibits() {')
if start_layout == -1:
    raise ValueError("start_layout not found")

end_layout = content.find('/* --------------------------------------------------------------------------\n   4.11  LIGHTING PIPELINE')
if end_layout == -1:
    raise ValueError("end_layout not found")

new_layout_code = "/* --------------------------------------------------------------------------\n   4.10  EXHIBIT SPOTS" + spots_and_layout_part.strip() + "\n\n"
content = content[:start_layout] + new_layout_code + content[end_layout:]
print("Updated layoutExhibits and EXHIBIT_SPOTS in content!")

# 4. Update updateCurrentWingCaption(pos)
start_cap = content.find('function updateCurrentWingCaption(pos) {')
if start_cap == -1:
    raise ValueError("start_cap not found")

end_cap = content.find('\nfunction animate() {')
if end_cap == -1:
    raise ValueError("end_cap not found")

new_caption_fn = """function updateCurrentWingCaption(pos) {
  const locEl = $('hudLoc');
  const cap = $('roomCaption');
  const capNum = $('capNum');
  const capTitle = $('capTitle');

  let wingName = 'Grand Rotunda';
  let wingNum = 'Entrance';

  if (pos.z > 51.5) {
    // Wing IV: The Kinematic Pavilion
    wingNum = 'Wing IV';
    if (pos.z > 68.0) {
      wingName = 'Wing IV · Master Storyboard & Pre-Visualization';
    } else if (pos.x > 8.0) {
      wingName = 'Wing IV · Applied Graphic Design & Brand Identity';
    } else if (pos.x < -8.0) {
      wingName = 'Wing IV · Production Design & Art Direction';
    } else {
      wingName = 'Wing IV · 2D Animation & Cinema Atrium';
    }
  } else if (pos.z > 8.0 && Math.abs(pos.x) <= 24.0) {
    // Wing II: 3D Virtual Worlds
    wingNum = 'Wing II';
    if (pos.x < -4.0) {
      if (pos.z < 30.0) {
        wingName = 'Wing II · 3D Environment Gallery';
      } else {
        wingName = 'Wing II · 3D VFX Dynamic Simulations';
      }
    } else if (pos.x > 4.0) {
      if (pos.z < 30.0) {
        wingName = 'Wing II · 3D Interior Architecture';
      } else {
        wingName = 'Wing II · 3D Still Life Studio';
      }
    } else {
      wingName = 'Wing II · 3D Character Topology Studio';
    }
  } else if (pos.x > 7.5) {
    // Wing I: The Classical & Fine Arts Wing
    wingNum = 'Wing I';
    if (pos.x > 44.0) {
      if (pos.z > 5.0) {
        wingName = 'Wing I · Traditional Fine Art & Life Study';
      } else if (pos.z < -5.0) {
        wingName = 'Wing I · 2D Character Anatomy Studio';
      } else {
        wingName = 'Wing I · Classical Foyer & Vestibule';
      }
    } else {
      wingName = 'Wing I · Digital Concept Art & Painting';
    }
  } else if (pos.x < -7.5) {
    // Wing III: The Nocturne Gallery
    wingNum = 'Wing III';
    if (pos.z > 5.0) {
      if (pos.x < -47.0) {
        wingName = 'Wing III · Editorial & Model Portraiture';
      } else {
        wingName = 'Wing III · Lunar Astrophotography Observatory';
      }
    } else if (pos.z < -5.0) {
      if (pos.x < -47.0) {
        wingName = 'Wing III · Still Life & Observational Objects';
      } else {
        wingName = 'Wing III · Wildlife & Animal Photography';
      }
    } else {
      wingName = 'Wing III · Observational Street Photography';
    }
  }

  locEl.textContent = wingName;
  if (capTitle.textContent !== wingName) {
    capTitle.textContent = wingName;
    capNum.textContent = wingNum;
    cap.classList.add('show');
    clearTimeout(cap._timer);
    cap._timer = setTimeout(() => cap.classList.remove('show'), 3200);
  }
}"""

content = content[:start_cap] + new_caption_fn + content[end_cap:]
print("Updated updateCurrentWingCaption in content!")

# Write updated file to index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: index.html has been fully updated!")

