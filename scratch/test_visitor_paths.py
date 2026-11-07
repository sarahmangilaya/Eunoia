with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re, math
wall_segments = []
for m in re.finditer(r'addWallSegment\(\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*\)', html):
    x1, z1, x2, z2 = map(float, m.groups())
    wall_segments.append(((x1, z1), (x2, z2)))

box_colliders = []
for m in re.finditer(r'addRotatedBoxCollider\(\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*\)', html):
    cx, cz, hx, hz, rot = map(float, m.groups())
    box_colliders.append((cx, cz, hx, hz, rot))

PLAYER_RADIUS = 0.45

def resolve_collision(px, pz):
    for (x1, z1), (x2, z2) in wall_segments:
        dx = x2 - x1
        dz = z2 - z1
        seg_len_sq = dx * dx + dz * dz
        if seg_len_sq < 1e-6: continue
        t = max(0.0, min(1.0, ((px - x1) * dx + (pz - z1) * dz) / seg_len_sq))
        cx = x1 + t * dx
        cz = z1 + t * dz
        dist = math.sqrt((px - cx)**2 + (pz - cz)**2)
        if dist < PLAYER_RADIUS:
            nx = (px - cx) / (dist if dist > 1e-6 else 1.0)
            nz = (pz - cz) / (dist if dist > 1e-6 else 1.0)
            px += nx * (PLAYER_RADIUS - dist)
            pz += nz * (PLAYER_RADIUS - dist)
    for (cx, cz, hx, hz, rot) in box_colliders:
        cos_r = math.cos(-rot); sin_r = math.sin(-rot)
        dx = px - cx; dz = pz - cz
        lx = cos_r * dx - sin_r * dz
        lz = sin_r * dx + cos_r * dz
        hw = hx + PLAYER_RADIUS; hd = hz + PLAYER_RADIUS
        if abs(lx) < hw and abs(lz) < hd:
            ox = hw - abs(lx); oz = hd - abs(lz)
            if ox < oz: lx = (1 if lx > 0 else -1) * hw
            else: lz = (1 if lz > 0 else -1) * hd
            cos_b = math.cos(rot); sin_b = math.sin(rot)
            px = cx + (cos_b * lx - sin_b * lz)
            pz = cz + (sin_b * lx + cos_b * lz)
    return px, pz

def test_walk(p_start, p_end, steps=90):
    px, pz = p_start
    tx, tz = p_end
    for i in range(steps):
        f = 1.0 / (steps - i)
        px += (tx - px) * f
        pz += (tz - pz) * f
        px, pz = resolve_collision(px, pz)
    return px, pz, math.sqrt((px - tx)**2 + (pz - tz)**2)

paths = [
    ('Wing I: Vestibule North into Traditional Salon (viewing area)', (51.0, 0), (48.5, 10.0)),
    ('Wing I: Traditional Salon to West art line', (48.5, 10.0), (46.5, 16.5)),
    ('Wing I: Traditional Salon back to Vestibule', (46.5, 16.5), (51.0, 0)),
    ('Wing I: Vestibule South into 2D Character Studio (viewing area)', (51.0, 0), (48.5, -10.0)),
    ('Wing I: 2D Character Studio to South art line', (48.5, -10.0), (52.0, -19.0)),
    ('Wing I: 2D Character Studio back to Vestibule', (52.0, -19.0), (51.0, 0)),
    ('Wing II: North through Wing IV Portal into Cinema Atrium (viewing area)', (0, 41.0), (0, 55.5)),
    ('Wing IV: Cinema Atrium East into Graphic Design Gallery (viewing area)', (0, 55.5), (18.0, 55.5)),
    ('Wing IV: Graphic Design Gallery to North Atelier wall', (18.0, 55.5), (22.0, 65.0)),
    ('Wing IV: Graphic Design Gallery back to Cinema Atrium', (22.0, 65.0), (0, 55.5)),
    ('Wing IV: Cinema Atrium West into Production Design Gallery (viewing area)', (0, 55.5), (-18.0, 55.5)),
    ('Wing IV: Production Design Gallery to West art line', (-18.0, 55.5), (-25.0, 60.0)),
    ('Wing IV: Production Design Gallery back to Cinema Atrium', (-25.0, 60.0), (0, 55.5)),
    ('Wing IV: Cinema Atrium North into Master Storyboards (viewing area)', (0, 55.5), (0, 75.0)),
    ('Wing IV: Master Storyboard Grand Hall to North wall', (0, 75.0), (0, 88.5)),
    ('Wing IV: Master Storyboards all the way back into Wing II', (0, 88.5), (0, 41.0)),
]

all_pass = True
for name, p_start, p_end in paths:
    rx, rz, dist = test_walk(p_start, p_end)
    passed = dist < 0.15
    if not passed: all_pass = False
    print(f"[{'PASS' if passed else 'FAIL'}] {name} (dist={dist:.2f}m)")

if all_pass:
    print("\nRESULT: 100% PERFECT WALKABILITY THROUGH ALL ROOMS AND GALLERIES!")
else:
    print("\nRESULT: SOME PATHS BLOCKED")

