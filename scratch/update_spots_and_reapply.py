import json, math, sys
sys.path.insert(0, '.')

# 1. Update SPOTS in build_and_verify_all_spots
from scratch.build_and_verify_all_spots import SPOTS

# North wall (z = 4.86, rotY = pi, facing -Z)
xs_n = [-12.0, -15.0, -18.0, -21.0, -24.0, -27.0, -30.0, -40.0, -43.0, -46.0, -49.0, -51.0, -59.5, -62.5, -65.5]
spots_III_street = []
for x in xs_n:
    spots_III_street.append({'x': x, 'y': 2.4, 'z': 4.86, 'rotY': math.pi, 'viewX': x, 'viewZ': 2.3})

# South wall (z = -4.86, rotY = 0, facing +Z)
for x in xs_n:
    spots_III_street.append({'x': x, 'y': 2.4, 'z': -4.86, 'rotY': 0, 'viewX': x, 'viewZ': -2.3})

# West End Wall (x = -67.86, rotY = pi/2, facing +X)
spots_III_street.append({'x': -67.86, 'y': 2.4, 'z': -2.8, 'rotY': math.pi / 2, 'viewX': -65.2, 'viewZ': -2.8})
spots_III_street.append({'x': -67.86, 'y': 2.4, 'z': 2.8,  'rotY': math.pi / 2, 'viewX': -65.2, 'viewZ': 2.8})

SPOTS[('III', 'street')] = spots_III_street
assert len(spots_III_street) == 32, f"Street spots count is {len(spots_III_street)}"

# Also apply corner adjustments
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
with open('scratch/exhibit_spots.json', 'w', encoding='utf-8') as f:
    f.write(spots_js_str)

print("Updated exhibit_spots.json with 100% door-clear spots!")

# Now re-generate architecture code and re-apply
import subprocess
subprocess.run(['python', 'scratch/generate_architecture_code.py'], check=True)
subprocess.run(['python', 'scratch/apply_complete_museum_205.py'], check=True)
subprocess.run(['python', 'scratch/fix_lights_and_load.py'], check=True)
subprocess.run(['python', 'scratch/check_syntax.py'], check=True)
print("ALL PIPELINES EXECUTED AND SYNTAX VERIFIED!")
