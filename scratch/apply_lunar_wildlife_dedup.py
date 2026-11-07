import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Identify IDs to remove
remove_ids = {
    # Lunar duplicates (11 removed, 8 kept)
    'project-91-20260302-205457',
    'project-92-20260302-205511',
    'project-95-20260302-205643',
    'project-96-20260302-205707',
    'project-98-20260302-205757',
    'project-99-20260302-205804',
    'project-101-20260403-200426',
    'project-104-20261004-005111',
    'project-105-20261004-005117',
    'project-106-20261004-005119',
    'project-108-20261004-005149',
    # Wildlife duplicates (6 removed, 7 kept)
    'project-80-20250917-125310-100kb',
    'project-82-20250917-125348-100kb',
    'project-85-20251219-182545',
    'project-86-20251219-182547',
    'project-88-20251219-182558',
    'project-89-20251219-182559'
}

print(f"Total IDs to remove: {len(remove_ids)}")

# Extract exhibits JSON array
pos = text.find('exhibits: [')
bracket_start = text.find('[', pos)
depth = 0
bracket_end = bracket_start
for i in range(bracket_start, len(text)):
    if text[i] == '[': depth += 1
    elif text[i] == ']':
        depth -= 1
        if depth == 0:
            bracket_end = i + 1
            break

exhibits = json.loads(text[bracket_start:bracket_end])
print(f"Original exhibit count: {len(exhibits)}")

filtered_exhibits = [e for e in exhibits if e['id'] not in remove_ids]
print(f"Filtered exhibit count: {len(filtered_exhibits)} (Removed: {len(exhibits) - len(filtered_exhibits)})")

# Check remaining counts
lunar_remaining = [e for e in filtered_exhibits if e.get('wing') == 'III' and e.get('room') == 'lunar']
wildlife_remaining = [e for e in filtered_exhibits if e.get('wing') == 'III' and e.get('room') == 'wildlife']
print(f"Remaining in III_lunar: {len(lunar_remaining)}")
print(f"Remaining in III_wildlife: {len(wildlife_remaining)}")

# Format new exhibits JSON
new_exhibits_json = json.dumps(filtered_exhibits, indent=2)

# Replace exhibits array in text
text = text[:bracket_start] + new_exhibits_json + text[bracket_end:]

# 2. Define new perfectly spaced EXHIBIT_SPOTS for III_lunar (8 spots) and III_wildlife (7 spots)
new_lunar_spots = [
  # West Wall (3 exhibits - Zoom progression from wide to telephoto)
  { "x": -45.86, "y": 2.4, "z": 9.0,  "rotY": 1.5707963267948966, "viewX": -43.4, "viewZ": 9.0 },
  { "x": -45.86, "y": 2.4, "z": 14.0, "rotY": 1.5707963267948966, "viewX": -43.4, "viewZ": 14.0 },
  { "x": -45.86, "y": 2.4, "z": 19.0, "rotY": 1.5707963267948966, "viewX": -43.4, "viewZ": 19.0 },
  # North Wall (2 feature exhibits - Macro Craters & Transit Line across Moon)
  { "x": -40.0,  "y": 2.4, "z": 22.86, "rotY": 3.141592653589793,  "viewX": -40.0, "viewZ": 20.3 },
  { "x": -34.0,  "y": 2.4, "z": 22.86, "rotY": 3.141592653589793,  "viewX": -34.0, "viewZ": 20.3 },
  # East Wall (3 exhibits - Phase progression from waxing to crescent)
  { "x": -28.14, "y": 2.4, "z": 19.0, "rotY": -1.5707963267948966, "viewX": -30.6, "viewZ": 19.0 },
  { "x": -28.14, "y": 2.4, "z": 14.0, "rotY": -1.5707963267948966, "viewX": -30.6, "viewZ": 14.0 },
  { "x": -28.14, "y": 2.4, "z": 9.0,  "rotY": -1.5707963267948966, "viewX": -30.6, "viewZ": 9.0 }
]

new_wildlife_spots = [
  # East Wall (2 White Cat portraits)
  { "x": -28.14, "y": 2.4, "z": -11.0, "rotY": -1.5707963267948966, "viewX": -30.6, "viewZ": -11.0 },
  { "x": -28.14, "y": 2.4, "z": -17.0, "rotY": -1.5707963267948966, "viewX": -30.6, "viewZ": -17.0 },
  # South Wall (3 Calico Cat portraits - crouching, sleeping, alert)
  { "x": -32.0,  "y": 2.4, "z": -22.86, "rotY": 0.0, "viewX": -32.0, "viewZ": -20.3 },
  { "x": -37.0,  "y": 2.4, "z": -22.86, "rotY": 0.0, "viewX": -37.0, "viewZ": -20.3 },
  { "x": -42.0,  "y": 2.4, "z": -22.86, "rotY": 0.0, "viewX": -42.0, "viewZ": -20.3 },
  # West Wall (2 Sleeping Dog landscapes)
  { "x": -45.86, "y": 2.4, "z": -17.0, "rotY": 1.5707963267948966, "viewX": -43.4, "viewZ": -17.0 },
  { "x": -45.86, "y": 2.4, "z": -11.0, "rotY": 1.5707963267948966, "viewX": -43.4, "viewZ": -11.0 }
]

# Replace EXHIBIT_SPOTS['III_lunar'] in text
pos_lunar_spot = text.find('III_lunar:')
if pos_lunar_spot == -1: pos_lunar_spot = text.find('"III_lunar":')
lunar_bracket_start = text.find('[', pos_lunar_spot)
depth = 0
lunar_bracket_end = lunar_bracket_start
for i in range(lunar_bracket_start, len(text)):
    if text[i] == '[': depth += 1
    elif text[i] == ']':
        depth -= 1
        if depth == 0:
            lunar_bracket_end = i + 1
            break

text = text[:lunar_bracket_start] + json.dumps(new_lunar_spots, indent=4) + text[lunar_bracket_end:]
print("Updated EXHIBIT_SPOTS['III_lunar']!")

# Replace EXHIBIT_SPOTS['III_wildlife'] in text
pos_wild_spot = text.find('III_wildlife:')
if pos_wild_spot == -1: pos_wild_spot = text.find('"III_wildlife":')
wild_bracket_start = text.find('[', pos_wild_spot)
depth = 0
wild_bracket_end = wild_bracket_start
for i in range(wild_bracket_start, len(text)):
    if text[i] == '[': depth += 1
    elif text[i] == ']':
        depth -= 1
        if depth == 0:
            wild_bracket_end = i + 1
            break

text = text[:wild_bracket_start] + json.dumps(new_wildlife_spots, indent=4) + text[wild_bracket_end:]
print("Updated EXHIBIT_SPOTS['III_wildlife']!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved updated index.html successfully!")

