import json, math, os, sys

# Load catalog
with open('scratch/full_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for item in catalog:
    item['isHung'] = True

print(f"Catalog contains {len(catalog)} items, all marked isHung = True.")

# Write updated full_catalog.json back to scratch
with open('scratch/full_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)

# Let's import SPOTS
sys.path.insert(0, '.')
from scratch.build_and_verify_all_spots import SPOTS

# Apply fine-tuned corner clearance adjustments
SPOTS[('III', 'lunar')][5]['z'] = 20.8
SPOTS[('III', 'lunar')][5]['viewZ'] = 20.8

SPOTS[('III', 'lunar')][12]['x'] = -43.8
SPOTS[('III', 'lunar')][12]['viewX'] = -43.8

SPOTS[('III', 'lunar')][13]['z'] = 20.8
SPOTS[('III', 'lunar')][13]['viewZ'] = 20.8

SPOTS[('III', 'stilllife_object')][9]['x'] = -64.0
SPOTS[('III', 'stilllife_object')][9]['viewX'] = -64.0

SPOTS[('IV', 'production_design')][9]['z'] = 66.0
SPOTS[('IV', 'production_design')][9]['viewZ'] = 66.0

# Format EXHIBIT_SPOTS as JavaScript
spots_js_dict = {}
for (w, r), spot_list in SPOTS.items():
    key = f"{w}_{r}"
    spots_js_dict[key] = spot_list

spots_js_str = json.dumps(spots_js_dict, indent=2)

print(f"Serialized EXHIBIT_SPOTS for {len(spots_js_dict)} groups ({sum(len(v) for v in spots_js_dict.values())} total spots).")

# Save spots to scratch/exhibit_spots.json for reference
with open('scratch/exhibit_spots.json', 'w', encoding='utf-8') as f:
    f.write(spots_js_str)

print("Saved exhibit_spots.json successfully.")

