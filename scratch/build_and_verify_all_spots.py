import json, math

with open('scratch/full_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

print(f"Total catalog exhibits: {len(cat)}")

# Group exhibits by (wing, room)
groups = {}
for ex in cat:
    key = (ex['wing'], ex['room'])
    groups.setdefault(key, []).append(ex)

for k, items in sorted(groups.items()):
    print(f"Group {k}: {len(items)} exhibits")

# Now let's define the exact spots for each room!
SPOTS = {}

# -------------------------------------------------------------
# WING I: 29 items
# -------------------------------------------------------------
# 1. finearts_promenade (16 items)
# North Wall (z = 4.86, rotY = PI, facing -Z)
# South Wall (z = -4.86, rotY = 0, facing +Z)
spots_I_prom = []
# 8 on North wall: x = 11.5, 15.5, 19.5, 23.5, 27.5, 31.5, 35.5, 39.5
for x in [11.5, 15.5, 19.5, 23.5, 27.5, 31.5, 35.5, 39.5]:
    spots_I_prom.append({'x': x, 'y': 2.4, 'z': 4.86, 'rotY': math.pi, 'viewX': x, 'viewZ': 2.3})
# 8 on South wall: x = 11.5, 15.5, 19.5, 23.5, 27.5, 31.5, 35.5, 39.5
for x in [11.5, 15.5, 19.5, 23.5, 27.5, 31.5, 35.5, 39.5]:
    spots_I_prom.append({'x': x, 'y': 2.4, 'z': -4.86, 'rotY': 0, 'viewX': x, 'viewZ': -2.3})
SPOTS[('I', 'finearts_promenade')] = spots_I_prom

# 2. finearts_traditional (6 items) in North Salon (x in [44, 60], z in [5, 22])
spots_I_trad = [
    # West wall (x = 44.14, rotY = PI/2)
    {'x': 44.14, 'y': 2.4, 'z': 10.0, 'rotY': math.pi / 2, 'viewX': 46.8, 'viewZ': 10.0},
    {'x': 44.14, 'y': 2.4, 'z': 16.5, 'rotY': math.pi / 2, 'viewX': 46.8, 'viewZ': 16.5},
    # North wall (z = 21.86, rotY = PI)
    {'x': 48.5, 'y': 2.4, 'z': 21.86, 'rotY': math.pi, 'viewX': 48.5, 'viewZ': 19.2},
    {'x': 55.5, 'y': 2.4, 'z': 21.86, 'rotY': math.pi, 'viewX': 55.5, 'viewZ': 19.2},
    # East wall (x = 59.86, rotY = -PI/2)
    {'x': 59.86, 'y': 2.4, 'z': 16.5, 'rotY': -math.pi / 2, 'viewX': 57.2, 'viewZ': 16.5},
    {'x': 59.86, 'y': 2.4, 'z': 10.0, 'rotY': -math.pi / 2, 'viewX': 57.2, 'viewZ': 10.0},
]
SPOTS[('I', 'finearts_traditional')] = spots_I_trad

# 3. finearts_character (7 items) in South Studio (x in [44, 60], z in [-22, -5])
spots_I_char = [
    # West wall (x = 44.14, rotY = PI/2)
    {'x': 44.14, 'y': 2.4, 'z': -10.0, 'rotY': math.pi / 2, 'viewX': 46.8, 'viewZ': -10.0},
    {'x': 44.14, 'y': 2.4, 'z': -16.5, 'rotY': math.pi / 2, 'viewX': 46.8, 'viewZ': -16.5},
    # South wall (z = -21.86, rotY = 0)
    {'x': 47.5, 'y': 2.4, 'z': -21.86, 'rotY': 0, 'viewX': 47.5, 'viewZ': -19.2},
    {'x': 52.0, 'y': 2.4, 'z': -21.86, 'rotY': 0, 'viewX': 52.0, 'viewZ': -19.2},
    {'x': 56.5, 'y': 2.4, 'z': -21.86, 'rotY': 0, 'viewX': 56.5, 'viewZ': -19.2},
    # East wall (x = 59.86, rotY = -PI/2)
    {'x': 59.86, 'y': 2.4, 'z': -16.5, 'rotY': -math.pi / 2, 'viewX': 57.2, 'viewZ': -16.5},
    {'x': 59.86, 'y': 2.4, 'z': -10.0, 'rotY': -math.pi / 2, 'viewX': 57.2, 'viewZ': -10.0},
]
SPOTS[('I', 'finearts_character')] = spots_I_char

# -------------------------------------------------------------
# WING II: 38 items
# -------------------------------------------------------------
# 1. env (9 items) in Room A (x in [-22, -4], z in [9.5, 25.5])
spots_II_env = [
    # North wall (z = 25.36, rotY = PI)
    {'x': -17.5, 'y': 2.4, 'z': 25.36, 'rotY': math.pi, 'viewX': -17.5, 'viewZ': 22.8},
    {'x': -13.0, 'y': 2.4, 'z': 25.36, 'rotY': math.pi, 'viewX': -13.0, 'viewZ': 22.8},
    {'x': -8.5,  'y': 2.4, 'z': 25.36, 'rotY': math.pi, 'viewX': -8.5,  'viewZ': 22.8},
    # West wall (x = -21.86, rotY = PI/2)
    {'x': -21.86, 'y': 2.4, 'z': 21.5, 'rotY': math.pi / 2, 'viewX': -19.2, 'viewZ': 21.5},
    {'x': -21.86, 'y': 2.4, 'z': 17.5, 'rotY': math.pi / 2, 'viewX': -19.2, 'viewZ': 17.5},
    {'x': -21.86, 'y': 2.4, 'z': 13.5, 'rotY': math.pi / 2, 'viewX': -19.2, 'viewZ': 13.5},
    # South wall (z = 9.64, rotY = 0)
    {'x': -17.5, 'y': 2.4, 'z': 9.64, 'rotY': 0, 'viewX': -17.5, 'viewZ': 12.2},
    {'x': -13.0, 'y': 2.4, 'z': 9.64, 'rotY': 0, 'viewX': -13.0, 'viewZ': 12.2},
    {'x': -8.5,  'y': 2.4, 'z': 9.64, 'rotY': 0, 'viewX': -8.5,  'viewZ': 12.2},
]
SPOTS[('II', 'env')] = spots_II_env

# 2. interior (10 items) in Room B (x in [4, 22], z in [9.5, 25.5])
spots_II_int = [
    # South wall (z = 9.64, rotY = 0)
    {'x': 8.5,  'y': 2.4, 'z': 9.64, 'rotY': 0, 'viewX': 8.5,  'viewZ': 12.2},
    {'x': 13.0, 'y': 2.4, 'z': 9.64, 'rotY': 0, 'viewX': 13.0, 'viewZ': 12.2},
    {'x': 17.5, 'y': 2.4, 'z': 9.64, 'rotY': 0, 'viewX': 17.5, 'viewZ': 12.2},
    # East wall (x = 21.86, rotY = -PI/2)
    {'x': 21.86, 'y': 2.4, 'z': 12.0, 'rotY': -math.pi / 2, 'viewX': 19.2, 'viewZ': 12.0},
    {'x': 21.86, 'y': 2.4, 'z': 15.5, 'rotY': -math.pi / 2, 'viewX': 19.2, 'viewZ': 15.5},
    {'x': 21.86, 'y': 2.4, 'z': 19.0, 'rotY': -math.pi / 2, 'viewX': 19.2, 'viewZ': 19.0},
    {'x': 21.86, 'y': 2.4, 'z': 22.5, 'rotY': -math.pi / 2, 'viewX': 19.2, 'viewZ': 22.5},
    # North wall (z = 25.36, rotY = PI)
    {'x': 17.5, 'y': 2.4, 'z': 25.36, 'rotY': math.pi, 'viewX': 17.5, 'viewZ': 22.8},
    {'x': 13.0, 'y': 2.4, 'z': 25.36, 'rotY': math.pi, 'viewX': 13.0, 'viewZ': 22.8},
    {'x': 8.5,  'y': 2.4, 'z': 25.36, 'rotY': math.pi, 'viewX': 8.5,  'viewZ': 22.8},
]
SPOTS[('II', 'interior')] = spots_II_int

# 3. vfx (8 items) in Room C (x in [-22, -4], z in [33, 49])
spots_II_vfx = [
    # South wall (z = 33.14, rotY = 0)
    {'x': -17.5, 'y': 2.5, 'z': 33.14, 'rotY': 0, 'viewX': -17.5, 'viewZ': 35.8},
    {'x': -13.0, 'y': 2.5, 'z': 33.14, 'rotY': 0, 'viewX': -13.0, 'viewZ': 35.8},
    {'x': -8.5,  'y': 2.5, 'z': 33.14, 'rotY': 0, 'viewX': -8.5,  'viewZ': 35.8},
    # West wall (x = -21.86, rotY = PI/2)
    {'x': -21.86, 'y': 2.5, 'z': 38.5, 'rotY': math.pi / 2, 'viewX': -19.2, 'viewZ': 38.5},
    {'x': -21.86, 'y': 2.5, 'z': 43.5, 'rotY': math.pi / 2, 'viewX': -19.2, 'viewZ': 43.5},
    # North wall (z = 48.86, rotY = PI)
    {'x': -17.5, 'y': 2.5, 'z': 48.86, 'rotY': math.pi, 'viewX': -17.5, 'viewZ': 46.2},
    {'x': -13.0, 'y': 2.5, 'z': 48.86, 'rotY': math.pi, 'viewX': -13.0, 'viewZ': 46.2},
    {'x': -8.5,  'y': 2.5, 'z': 48.86, 'rotY': math.pi, 'viewX': -8.5,  'viewZ': 46.2},
]
SPOTS[('II', 'vfx')] = spots_II_vfx

# 4. stilllife (4 items) in Room D (x in [4, 22], z in [33, 49])
spots_II_still = [
    # South wall (z = 33.14, rotY = 0)
    {'x': 13.0, 'y': 2.4, 'z': 33.14, 'rotY': 0, 'viewX': 13.0, 'viewZ': 35.8},
    # East wall (x = 21.86, rotY = -PI/2)
    {'x': 21.86, 'y': 2.4, 'z': 38.5, 'rotY': -math.pi / 2, 'viewX': 19.2, 'viewZ': 38.5},
    {'x': 21.86, 'y': 2.4, 'z': 43.5, 'rotY': -math.pi / 2, 'viewX': 19.2, 'viewZ': 43.5},
    # North wall (z = 48.86, rotY = PI)
    {'x': 13.0, 'y': 2.4, 'z': 48.86, 'rotY': math.pi, 'viewX': 13.0, 'viewZ': 46.2},
]
SPOTS[('II', 'stilllife')] = spots_II_still

# 5. char3d (7 items) in Promenade & Center Kiosk
spots_II_char = [
    # West Piers (x = -3.86, rotY = PI/2)
    {'x': -3.86, 'y': 2.4, 'z': 11.0, 'rotY': math.pi / 2, 'viewX': -1.6, 'viewZ': 11.0},
    {'x': -3.86, 'y': 2.4, 'z': 24.0, 'rotY': math.pi / 2, 'viewX': -1.6, 'viewZ': 24.0},
    {'x': -3.86, 'y': 2.4, 'z': 35.0, 'rotY': math.pi / 2, 'viewX': -1.6, 'viewZ': 35.0},
    # East Piers (x = 3.86, rotY = -PI/2)
    {'x': 3.86, 'y': 2.4, 'z': 11.0, 'rotY': -math.pi / 2, 'viewX': 1.6, 'viewZ': 11.0},
    {'x': 3.86, 'y': 2.4, 'z': 24.0, 'rotY': -math.pi / 2, 'viewX': 1.6, 'viewZ': 24.0},
    {'x': 3.86, 'y': 2.4, 'z': 35.0, 'rotY': -math.pi / 2, 'viewX': 1.6, 'viewZ': 35.0},
    # Center Kiosk at z = 28.0 (rotY = 0)
    {'x': 0.0, 'y': 2.1, 'z': 28.0, 'rotY': 0, 'viewX': 0.0, 'viewZ': 25.5},
]
SPOTS[('II', 'char3d')] = spots_II_char

# -------------------------------------------------------------
# WING III: 86 items
# -------------------------------------------------------------
# 1. street (32 items) in Central Boulevard (x in [-68, -8.3], z in [-5, 5])
spots_III_street = []
# 16 on North wall (z = 4.86, rotY = PI, facing -Z)
# Spaced along x = -11.5 down to -65.5 (every 3.6m)
xs_street = [-11.5 - i * 3.6 for i in range(16)]
for x in xs_street:
    spots_III_street.append({'x': x, 'y': 2.4, 'z': 4.86, 'rotY': math.pi, 'viewX': x, 'viewZ': 2.3})
# 16 on South wall (z = -4.86, rotY = 0, facing +Z)
for x in xs_street:
    spots_III_street.append({'x': x, 'y': 2.4, 'z': -4.86, 'rotY': 0, 'viewX': x, 'viewZ': -2.3})
SPOTS[('III', 'street')] = spots_III_street

# 2. lunar (19 items) in North Chamber 1 (x in [-46, -28], z in [5, 23])
spots_III_lunar = [
    # East wall (x = -28.14, rotY = -PI/2) : 6 items at z = 7.5, 10.5, 13.5, 16.5, 19.5, 21.5
    {'x': -28.14, 'y': 2.4, 'z': 7.5,  'rotY': -math.pi / 2, 'viewX': -30.6, 'viewZ': 7.5},
    {'x': -28.14, 'y': 2.4, 'z': 10.5, 'rotY': -math.pi / 2, 'viewX': -30.6, 'viewZ': 10.5},
    {'x': -28.14, 'y': 2.4, 'z': 13.5, 'rotY': -math.pi / 2, 'viewX': -30.6, 'viewZ': 13.5},
    {'x': -28.14, 'y': 2.4, 'z': 16.5, 'rotY': -math.pi / 2, 'viewX': -30.6, 'viewZ': 16.5},
    {'x': -28.14, 'y': 2.4, 'z': 19.5, 'rotY': -math.pi / 2, 'viewX': -30.6, 'viewZ': 19.5},
    {'x': -28.14, 'y': 2.4, 'z': 21.5, 'rotY': -math.pi / 2, 'viewX': -30.6, 'viewZ': 21.5},
    # North wall (z = 22.86, rotY = PI) : 7 items at x = -30.0, -32.5, -35.0, -37.5, -40.0, -42.5, -44.5
    {'x': -30.0, 'y': 2.4, 'z': 22.86, 'rotY': math.pi, 'viewX': -30.0, 'viewZ': 20.3},
    {'x': -32.5, 'y': 2.4, 'z': 22.86, 'rotY': math.pi, 'viewX': -32.5, 'viewZ': 20.3},
    {'x': -35.0, 'y': 2.4, 'z': 22.86, 'rotY': math.pi, 'viewX': -35.0, 'viewZ': 20.3},
    {'x': -37.5, 'y': 2.4, 'z': 22.86, 'rotY': math.pi, 'viewX': -37.5, 'viewZ': 20.3},
    {'x': -40.0, 'y': 2.4, 'z': 22.86, 'rotY': math.pi, 'viewX': -40.0, 'viewZ': 20.3},
    {'x': -42.5, 'y': 2.4, 'z': 22.86, 'rotY': math.pi, 'viewX': -42.5, 'viewZ': 20.3},
    {'x': -44.5, 'y': 2.4, 'z': 22.86, 'rotY': math.pi, 'viewX': -44.5, 'viewZ': 20.3},
    # West wall (x = -45.86, rotY = PI/2) : 6 items at z = 21.5, 19.5, 16.5, 13.5, 10.5, 7.5
    {'x': -45.86, 'y': 2.4, 'z': 21.5, 'rotY': math.pi / 2, 'viewX': -43.4, 'viewZ': 21.5},
    {'x': -45.86, 'y': 2.4, 'z': 19.5, 'rotY': math.pi / 2, 'viewX': -43.4, 'viewZ': 19.5},
    {'x': -45.86, 'y': 2.4, 'z': 16.5, 'rotY': math.pi / 2, 'viewX': -43.4, 'viewZ': 16.5},
    {'x': -45.86, 'y': 2.4, 'z': 13.5, 'rotY': math.pi / 2, 'viewX': -43.4, 'viewZ': 13.5},
    {'x': -45.86, 'y': 2.4, 'z': 10.5, 'rotY': math.pi / 2, 'viewX': -43.4, 'viewZ': 10.5},
    {'x': -45.86, 'y': 2.4, 'z': 7.5,  'rotY': math.pi / 2, 'viewX': -43.4, 'viewZ': 7.5},
]
SPOTS[('III', 'lunar')] = spots_III_lunar

# 3. wildlife (13 items) in South Chamber 1 (x in [-46, -28], z in [-23, -5])
spots_III_wildlife = [
    # East wall (x = -28.14, rotY = -PI/2) : 4 items at z = -8.5, -12.5, -16.5, -20.5
    {'x': -28.14, 'y': 2.4, 'z': -8.5,  'rotY': -math.pi / 2, 'viewX': -30.6, 'viewZ': -8.5},
    {'x': -28.14, 'y': 2.4, 'z': -12.5, 'rotY': -math.pi / 2, 'viewX': -30.6, 'viewZ': -12.5},
    {'x': -28.14, 'y': 2.4, 'z': -16.5, 'rotY': -math.pi / 2, 'viewX': -30.6, 'viewZ': -16.5},
    {'x': -28.14, 'y': 2.4, 'z': -20.5, 'rotY': -math.pi / 2, 'viewX': -30.6, 'viewZ': -20.5},
    # South wall (z = -22.86, rotY = 0) : 5 items at x = -30.5, -34.0, -37.5, -41.0, -44.0
    {'x': -30.5, 'y': 2.4, 'z': -22.86, 'rotY': 0, 'viewX': -30.5, 'viewZ': -20.3},
    {'x': -34.0, 'y': 2.4, 'z': -22.86, 'rotY': 0, 'viewX': -34.0, 'viewZ': -20.3},
    {'x': -37.5, 'y': 2.4, 'z': -22.86, 'rotY': 0, 'viewX': -37.5, 'viewZ': -20.3},
    {'x': -41.0, 'y': 2.4, 'z': -22.86, 'rotY': 0, 'viewX': -41.0, 'viewZ': -20.3},
    {'x': -44.0, 'y': 2.4, 'z': -22.86, 'rotY': 0, 'viewX': -44.0, 'viewZ': -20.3},
    # West wall (x = -45.86, rotY = PI/2) : 4 items at z = -20.5, -16.5, -12.5, -8.5
    {'x': -45.86, 'y': 2.4, 'z': -20.5, 'rotY': math.pi / 2, 'viewX': -43.4, 'viewZ': -20.5},
    {'x': -45.86, 'y': 2.4, 'z': -16.5, 'rotY': math.pi / 2, 'viewX': -43.4, 'viewZ': -16.5},
    {'x': -45.86, 'y': 2.4, 'z': -12.5, 'rotY': math.pi / 2, 'viewX': -43.4, 'viewZ': -12.5},
    {'x': -45.86, 'y': 2.4, 'z': -8.5,  'rotY': math.pi / 2, 'viewX': -43.4, 'viewZ': -8.5},
]
SPOTS[('III', 'wildlife')] = spots_III_wildlife

# 4. portrait (8 items) in North Chamber 2 (x in [-66, -48], z in [5, 23])
spots_III_portrait = [
    # East wall (x = -48.14, rotY = -PI/2) : 2 items
    {'x': -48.14, 'y': 2.4, 'z': 10.0, 'rotY': -math.pi / 2, 'viewX': -50.6, 'viewZ': 10.0},
    {'x': -48.14, 'y': 2.4, 'z': 18.0, 'rotY': -math.pi / 2, 'viewX': -50.6, 'viewZ': 18.0},
    # North wall (z = 22.86, rotY = PI) : 4 items
    {'x': -51.5, 'y': 2.4, 'z': 22.86, 'rotY': math.pi, 'viewX': -51.5, 'viewZ': 20.3},
    {'x': -55.0, 'y': 2.4, 'z': 22.86, 'rotY': math.pi, 'viewX': -55.0, 'viewZ': 20.3},
    {'x': -58.5, 'y': 2.4, 'z': 22.86, 'rotY': math.pi, 'viewX': -58.5, 'viewZ': 20.3},
    {'x': -62.0, 'y': 2.4, 'z': 22.86, 'rotY': math.pi, 'viewX': -62.0, 'viewZ': 20.3},
    # West wall (x = -65.86, rotY = PI/2) : 2 items
    {'x': -65.86, 'y': 2.4, 'z': 18.0, 'rotY': math.pi / 2, 'viewX': -63.4, 'viewZ': 18.0},
    {'x': -65.86, 'y': 2.4, 'z': 10.0, 'rotY': math.pi / 2, 'viewX': -63.4, 'viewZ': 10.0},
]
SPOTS[('III', 'portrait')] = spots_III_portrait

# 5. stilllife_object (14 items) in South Chamber 2 (x in [-66, -48], z in [-23, -5])
spots_III_still = [
    # East wall (x = -48.14, rotY = -PI/2) : 4 items
    {'x': -48.14, 'y': 2.4, 'z': -8.5,  'rotY': -math.pi / 2, 'viewX': -50.6, 'viewZ': -8.5},
    {'x': -48.14, 'y': 2.4, 'z': -12.5, 'rotY': -math.pi / 2, 'viewX': -50.6, 'viewZ': -12.5},
    {'x': -48.14, 'y': 2.4, 'z': -16.5, 'rotY': -math.pi / 2, 'viewX': -50.6, 'viewZ': -16.5},
    {'x': -48.14, 'y': 2.4, 'z': -20.5, 'rotY': -math.pi / 2, 'viewX': -50.6, 'viewZ': -20.5},
    # South wall (z = -22.86, rotY = 0) : 6 items
    {'x': -51.0, 'y': 2.4, 'z': -22.86, 'rotY': 0, 'viewX': -51.0, 'viewZ': -20.3},
    {'x': -53.8, 'y': 2.4, 'z': -22.86, 'rotY': 0, 'viewX': -53.8, 'viewZ': -20.3},
    {'x': -56.6, 'y': 2.4, 'z': -22.86, 'rotY': 0, 'viewX': -56.6, 'viewZ': -20.3},
    {'x': -59.4, 'y': 2.4, 'z': -22.86, 'rotY': 0, 'viewX': -59.4, 'viewZ': -20.3},
    {'x': -62.2, 'y': 2.4, 'z': -22.86, 'rotY': 0, 'viewX': -62.2, 'viewZ': -20.3},
    {'x': -64.5, 'y': 2.4, 'z': -22.86, 'rotY': 0, 'viewX': -64.5, 'viewZ': -20.3},
    # West wall (x = -65.86, rotY = PI/2) : 4 items
    {'x': -65.86, 'y': 2.4, 'z': -20.5, 'rotY': math.pi / 2, 'viewX': -63.4, 'viewZ': -20.5},
    {'x': -65.86, 'y': 2.4, 'z': -16.5, 'rotY': math.pi / 2, 'viewX': -63.4, 'viewZ': -16.5},
    {'x': -65.86, 'y': 2.4, 'z': -12.5, 'rotY': math.pi / 2, 'viewX': -63.4, 'viewZ': -12.5},
    {'x': -65.86, 'y': 2.4, 'z': -8.5,  'rotY': math.pi / 2, 'viewX': -63.4, 'viewZ': -8.5},
]
SPOTS[('III', 'stilllife_object')] = spots_III_still

# -------------------------------------------------------------
# WING IV: 52 items
# -------------------------------------------------------------
# 1. applied_graphic (13 items) in East Chamber (x in [8, 28], z in [52, 68])
spots_IV_applied = [
    # South Wall (z = 52.14, rotY = 0) : 4 Graphic Design Posters
    {'x': 11.5, 'y': 2.4, 'z': 52.14, 'rotY': 0, 'viewX': 11.5, 'viewZ': 54.8},
    {'x': 15.5, 'y': 2.4, 'z': 52.14, 'rotY': 0, 'viewX': 15.5, 'viewZ': 54.8},
    {'x': 19.5, 'y': 2.4, 'z': 52.14, 'rotY': 0, 'viewX': 19.5, 'viewZ': 54.8},
    {'x': 23.5, 'y': 2.4, 'z': 52.14, 'rotY': 0, 'viewX': 23.5, 'viewZ': 54.8},
    # East Wall (x = 27.86, rotY = -PI/2) : 3 Brand Logos
    {'x': 27.86, 'y': 2.4, 'z': 56.0, 'rotY': -math.pi / 2, 'viewX': 25.2, 'viewZ': 56.0},
    {'x': 27.86, 'y': 2.4, 'z': 60.0, 'rotY': -math.pi / 2, 'viewX': 25.2, 'viewZ': 60.0},
    {'x': 27.86, 'y': 2.4, 'z': 64.0, 'rotY': -math.pi / 2, 'viewX': 25.2, 'viewZ': 64.0},
    # North Wall (z = 67.86, rotY = PI) : 6 Atelier Lanyards
    {'x': 11.0, 'y': 2.4, 'z': 67.86, 'rotY': math.pi, 'viewX': 11.0, 'viewZ': 65.2},
    {'x': 13.8, 'y': 2.4, 'z': 67.86, 'rotY': math.pi, 'viewX': 13.8, 'viewZ': 65.2},
    {'x': 16.6, 'y': 2.4, 'z': 67.86, 'rotY': math.pi, 'viewX': 16.6, 'viewZ': 65.2},
    {'x': 19.4, 'y': 2.4, 'z': 67.86, 'rotY': math.pi, 'viewX': 19.4, 'viewZ': 65.2},
    {'x': 22.2, 'y': 2.4, 'z': 67.86, 'rotY': math.pi, 'viewX': 22.2, 'viewZ': 65.2},
    {'x': 25.0, 'y': 2.4, 'z': 67.86, 'rotY': math.pi, 'viewX': 25.0, 'viewZ': 65.2},
]
SPOTS[('IV', 'applied_graphic')] = spots_IV_applied

# 2. cinema (6 items) in Central Cinema Atrium (x in [-8, 8], z in [52, 68])
spots_IV_cinema = [
    # North Wall flanking portal (z = 67.86, rotY = PI)
    {'x': -5.2, 'y': 2.6, 'z': 67.86, 'rotY': math.pi, 'viewX': -5.2, 'viewZ': 64.5},
    {'x':  5.2, 'y': 2.6, 'z': 67.86, 'rotY': math.pi, 'viewX':  5.2, 'viewZ': 64.5},
    # West Wall (x = -7.86, rotY = PI/2)
    {'x': -7.86, 'y': 2.6, 'z': 55.5, 'rotY': math.pi / 2, 'viewX': -5.2, 'viewZ': 55.5},
    {'x': -7.86, 'y': 2.6, 'z': 64.5, 'rotY': math.pi / 2, 'viewX': -5.2, 'viewZ': 64.5},
    # East Wall (x = 7.86, rotY = -PI/2)
    {'x':  7.86, 'y': 2.6, 'z': 55.5, 'rotY': -math.pi / 2, 'viewX':  5.2, 'viewZ': 55.5},
    {'x':  7.86, 'y': 2.6, 'z': 64.5, 'rotY': -math.pi / 2, 'viewX':  5.2, 'viewZ': 64.5},
]
SPOTS[('IV', 'cinema')] = spots_IV_cinema

# 3. production_design (14 items) in West Chamber (x in [-28, -8], z in [52, 68])
spots_IV_prod = [
    # South Wall (z = 52.14, rotY = 0) : 4 items
    {'x': -24.5, 'y': 2.4, 'z': 52.14, 'rotY': 0, 'viewX': -24.5, 'viewZ': 54.8},
    {'x': -20.5, 'y': 2.4, 'z': 52.14, 'rotY': 0, 'viewX': -20.5, 'viewZ': 54.8},
    {'x': -16.5, 'y': 2.4, 'z': 52.14, 'rotY': 0, 'viewX': -16.5, 'viewZ': 54.8},
    {'x': -11.5, 'y': 2.4, 'z': 52.14, 'rotY': 0, 'viewX': -11.5, 'viewZ': 54.8},
    # West Wall (x = -27.86, rotY = PI/2) : 6 items
    {'x': -27.86, 'y': 2.4, 'z': 54.5, 'rotY': math.pi / 2, 'viewX': -25.2, 'viewZ': 54.5},
    {'x': -27.86, 'y': 2.4, 'z': 57.0, 'rotY': math.pi / 2, 'viewX': -25.2, 'viewZ': 57.0},
    {'x': -27.86, 'y': 2.4, 'z': 59.5, 'rotY': math.pi / 2, 'viewX': -25.2, 'viewZ': 59.5},
    {'x': -27.86, 'y': 2.4, 'z': 62.0, 'rotY': math.pi / 2, 'viewX': -25.2, 'viewZ': 62.0},
    {'x': -27.86, 'y': 2.4, 'z': 64.5, 'rotY': math.pi / 2, 'viewX': -25.2, 'viewZ': 64.5},
    {'x': -27.86, 'y': 2.4, 'z': 66.5, 'rotY': math.pi / 2, 'viewX': -25.2, 'viewZ': 66.5},
    # North Wall (z = 67.86, rotY = PI) : 4 items
    {'x': -24.5, 'y': 2.4, 'z': 67.86, 'rotY': math.pi, 'viewX': -24.5, 'viewZ': 65.2},
    {'x': -21.0, 'y': 2.4, 'z': 67.86, 'rotY': math.pi, 'viewX': -21.0, 'viewZ': 65.2},
    {'x': -15.5, 'y': 2.4, 'z': 67.86, 'rotY': math.pi, 'viewX': -15.5, 'viewZ': 65.2},
    {'x': -11.5, 'y': 2.4, 'z': 67.86, 'rotY': math.pi, 'viewX': -11.5, 'viewZ': 65.2},
]
SPOTS[('IV', 'production_design')] = spots_IV_prod

# 4. storyboard (19 items) in North Grand Hall (x in [-28, 28], z in [68, 92])
spots_IV_story = [
    # Grand North Wall (z = 91.86, rotY = PI) : 7 The Wind Rises plates
    {'x': -21.0, 'y': 2.5, 'z': 91.86, 'rotY': math.pi, 'viewX': -21.0, 'viewZ': 88.5},
    {'x': -14.0, 'y': 2.5, 'z': 91.86, 'rotY': math.pi, 'viewX': -14.0, 'viewZ': 88.5},
    {'x':  -7.0, 'y': 2.5, 'z': 91.86, 'rotY': math.pi, 'viewX':  -7.0, 'viewZ': 88.5},
    {'x':   0.0, 'y': 2.5, 'z': 91.86, 'rotY': math.pi, 'viewX':   0.0, 'viewZ': 88.5},
    {'x':   7.0, 'y': 2.5, 'z': 91.86, 'rotY': math.pi, 'viewX':   7.0, 'viewZ': 88.5},
    {'x':  14.0, 'y': 2.5, 'z': 91.86, 'rotY': math.pi, 'viewX':  14.0, 'viewZ': 88.5},
    {'x':  21.0, 'y': 2.5, 'z': 91.86, 'rotY': math.pi, 'viewX':  21.0, 'viewZ': 88.5},
    # West Wall (x = -27.86, rotY = PI/2) : 4 Cinematography plates
    {'x': -27.86, 'y': 2.4, 'z': 72.5, 'rotY': math.pi / 2, 'viewX': -25.2, 'viewZ': 72.5},
    {'x': -27.86, 'y': 2.4, 'z': 77.5, 'rotY': math.pi / 2, 'viewX': -25.2, 'viewZ': 77.5},
    {'x': -27.86, 'y': 2.4, 'z': 82.5, 'rotY': math.pi / 2, 'viewX': -25.2, 'viewZ': 82.5},
    {'x': -27.86, 'y': 2.4, 'z': 87.5, 'rotY': math.pi / 2, 'viewX': -25.2, 'viewZ': 87.5},
    # East Wall (x = 27.86, rotY = -PI/2) : 4 Continuity plates
    {'x': 27.86, 'y': 2.4, 'z': 72.5, 'rotY': -math.pi / 2, 'viewX': 25.2, 'viewZ': 72.5},
    {'x': 27.86, 'y': 2.4, 'z': 77.5, 'rotY': -math.pi / 2, 'viewX': 25.2, 'viewZ': 77.5},
    {'x': 27.86, 'y': 2.4, 'z': 82.5, 'rotY': -math.pi / 2, 'viewX': 25.2, 'viewZ': 82.5},
    {'x': 27.86, 'y': 2.4, 'z': 87.5, 'rotY': -math.pi / 2, 'viewX': 25.2, 'viewZ': 87.5},
    # South Wall returns (z = 68.14, rotY = 0) : 4 Paneling & Composition plates
    {'x': -22.0, 'y': 2.4, 'z': 68.14, 'rotY': 0, 'viewX': -22.0, 'viewZ': 70.8},
    {'x': -12.0, 'y': 2.4, 'z': 68.14, 'rotY': 0, 'viewX': -12.0, 'viewZ': 70.8},
    {'x':  12.0, 'y': 2.4, 'z': 68.14, 'rotY': 0, 'viewX':  12.0, 'viewZ': 70.8},
    {'x':  22.0, 'y': 2.4, 'z': 68.14, 'rotY': 0, 'viewX':  22.0, 'viewZ': 70.8},
]
SPOTS[('IV', 'storyboard')] = spots_IV_story

# Verify spot counts match exhibit counts exactly!
total_spots = sum(len(s) for s in SPOTS.values())
print(f"Total defined spots: {total_spots} / Exhibits: {len(cat)}")

all_matched = True
for k, items in sorted(groups.items()):
    s_len = len(SPOTS.get(k, []))
    if len(items) != s_len:
        print(f"MISMATCH in group {k}: items={len(items)}, spots={s_len}")
        all_matched = False
    else:
        print(f"Group {k} PERFECT: {len(items)} items == {s_len} spots")

assert all_matched, "Spots count mismatch!"
print("\nALL 205 SPOTS MATCH EXHIBIT COUNTS 100%!")

