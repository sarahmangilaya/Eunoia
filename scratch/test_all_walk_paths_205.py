import re, math

# Parse colliders directly from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

wall_segments = []
for m in re.finditer(r'addWallSegment\(\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*\)', html):
    x1, z1, x2, z2 = map(float, m.groups())
    wall_segments.append(((x1, z1), (x2, z2)))

box_colliders = []
for m in re.finditer(r'addRotatedBoxCollider\(\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*\)', html):
    cx, cz, hx, hz, rot = map(float, m.groups())
    box_colliders.append((cx, cz, hx, hz, rot))

print(f"Extracted {len(wall_segments)} wall segments and {len(box_colliders)} box colliders from index.html.")

PLAYER_RADIUS = 0.45

def resolve_collision(px, pz):
    for (x1, z1), (x2, z2) in wall_segments:
        dx = x2 - x1
        dz = z2 - z1
        seg_len_sq = dx * dx + dz * dz
        if seg_len_sq < 1e-6:
            continue
        t = max(0.0, min(1.0, ((px - x1) * dx + (pz - z1) * dz) / seg_len_sq))
        cx = x1 + t * dx
        cz = z1 + t * dz
        dist_x = px - cx
        dist_z = pz - cz
        dist = math.sqrt(dist_x * dist_x + dist_z * dist_z)
        if dist < PLAYER_RADIUS:
            if dist < 1e-6:
                nx, nz = 0.0, 1.0
            else:
                nx = dist_x / dist
                nz = dist_z / dist
            penetration = PLAYER_RADIUS - dist
            px += nx * penetration
            pz += nz * penetration

    for (cx, cz, hx, hz, rot) in box_colliders:
        cos_r = math.cos(-rot)
        sin_r = math.sin(-rot)
        dx = px - cx
        dz = pz - cz
        lx = cos_r * dx - sin_r * dz
        lz = sin_r * dx + cos_r * dz
        hw = hx + PLAYER_RADIUS
        hd = hz + PLAYER_RADIUS
        if abs(lx) < hw and abs(lz) < hd:
            overlap_x = hw - abs(lx)
            overlap_z = hd - abs(lz)
            if overlap_x < overlap_z:
                sign_x = 1 if lx > 0 else -1
                lx = sign_x * hw
            else:
                sign_z = 1 if lz > 0 else -1
                lz = sign_z * hd
            cos_b = math.cos(rot)
            sin_b = math.sin(rot)
            px = cx + (cos_b * lx - sin_b * lz)
            pz = cz + (sin_b * lx + cos_b * lz)
    return px, pz

def test_walk(p_start, p_end, steps=80):
    px, pz = p_start
    tx, tz = p_end
    for i in range(steps):
        step_frac = 1.0 / (steps - i)
        step_x = (tx - px) * step_frac
        step_z = (tz - pz) * step_frac
        px += step_x
        pz += step_z
        px, pz = resolve_collision(px, pz)
    final_dist = math.sqrt((px - tx) ** 2 + (pz - tz) ** 2)
    return px, pz, final_dist

paths = [
    # 1. Rotunda to Wings
    ("Rotunda Center to Wing I Entrance", (0, 0), (8.5, 0)),
    ("Rotunda Center to Wing II Entrance", (0, 0), (0, 8.5)),
    ("Rotunda Center to Wing III Entrance", (0, 0), (-8.5, 0)),

    # 2. Wing I Suite
    ("Wing I Entrance into Promenade", (8.5, 0), (25.0, 0)),
    ("Wing I Promenade to Vestibule", (25.0, 0), (51.0, 0)),
    ("Vestibule North into Traditional Salon", (51.0, 0), (51.0, 13.5)),
    ("Traditional Salon back to Vestibule", (51.0, 13.5), (51.0, 0)),
    ("Vestibule South into 2D Character Studio", (51.0, 0), (51.0, -13.5)),
    ("2D Character Studio back to Vestibule", (51.0, -13.5), (51.0, 0)),
    ("Wing I Vestibule back to Rotunda", (51.0, 0), (0, 0)),

    # 3. Wing II Suite
    ("Wing II Entrance into Promenade", (0, 8.5), (0, 17.5)),
    ("Promenade West into Room A (3D Environment)", (0, 17.5), (-13.0, 17.5)),
    ("Room A back to Promenade", (-13.0, 17.5), (0, 17.5)),
    ("Promenade East into Room B (3D Interior)", (0, 17.5), (13.0, 17.5)),
    ("Room B back to Promenade", (13.0, 17.5), (0, 17.5)),
    ("Promenade North to z=41.0", (0, 17.5), (0, 41.0)),
    ("Promenade West into Room C (3D VFX Cinema)", (0, 41.0), (-13.0, 41.0)),
    ("Room C back to Promenade", (-13.0, 41.0), (0, 41.0)),
    ("Promenade East into Room D (3D Still Life)", (0, 41.0), (13.0, 41.0)),
    ("Room D back to Promenade", (13.0, 41.0), (0, 41.0)),

    # 4. Wing IV Suite (From Wing II)
    ("Promenade North through Wing IV Portal into Cinema Atrium", (0, 41.0), (0, 60.0)),
    ("Cinema Atrium East into Graphic Design & Logos Gallery", (0, 60.0), (18.0, 60.0)),
    ("Graphic Design Gallery back to Cinema Atrium", (18.0, 60.0), (0, 60.0)),
    ("Cinema Atrium West into Production Design Gallery", (0, 60.0), (-18.0, 60.0)),
    ("Production Design Gallery back to Cinema Atrium", (-18.0, 60.0), (0, 60.0)),
    ("Cinema Atrium North into Master Storyboard Grand Hall", (0, 60.0), (0, 80.0)),
    ("Storyboard Grand Hall back through Cinema Atrium into Wing II", (0, 80.0), (0, 41.0)),
    ("Wing II back to Rotunda", (0, 41.0), (0, 0)),

    # 5. Wing III Suite
    ("Rotunda into Wing III Central Boulevard", (0, 0), (-25.0, 0)),
    ("Boulevard North into Lunar Astrophotography Observatory", (-35.0, 0), (-35.0, 14.0)),
    ("Lunar Observatory back to Boulevard", (-35.0, 14.0), (-35.0, 0)),
    ("Boulevard South into Wildlife Sanctuary", (-35.0, 0), (-35.0, -14.0)),
    ("Wildlife Sanctuary back to Boulevard", (-35.0, -14.0), (-35.0, 0)),
    ("Boulevard West to x=-55.0", (-35.0, 0), (-55.0, 0)),
    ("Boulevard North into Editorial Portrait Salon", (-55.0, 0), (-55.0, 14.0)),
    ("Editorial Portrait Salon back to Boulevard", (-55.0, 14.0), (-55.0, 0)),
    ("Boulevard South into Materiality Gallery", (-55.0, 0), (-55.0, -14.0)),
    ("Materiality Gallery back to Boulevard", (-55.0, -14.0), (-55.0, 0)),
    ("Boulevard to Far West End Feature", (-55.0, 0), (-65.0, 0)),
    ("Boulevard West End all the way back to Rotunda", (-65.0, 0), (0, 0)),
]

print(f"\n=== SIMULATING {len(paths)} VISITOR WALKING PATHS ACROSS ENTIRE MUSEUM ===")
all_passed = True
for name, p_start, p_end in paths:
    rx, rz, dist = test_walk(p_start, p_end, steps=90)
    passed = dist < 0.15
    if not passed:
        all_passed = False
    status = "PASS" if passed else f"BLOCKED (dist={dist:.2f}m)"
    print(f"[{status:<5}] {name}")

print(f"\nFinal Result: {'100% PASS - ALL 4 WINGS AND ROOMS FULLY ACCESSIBLE WITH ZERO INVISIBLE WALLS!' if all_passed else 'FAIL - SOME PATHS BLOCKED'}")

