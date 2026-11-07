import math

# Collision simulation
wall_segments = []
box_colliders = []

def add_wall(x1, z1, x2, z2):
    wall_segments.append(((x1, z1), (x2, z2)))

def add_box(cx, cz, hx, hz, rotY=0):
    box_colliders.append((cx, cz, hx, hz, rotY))

PLAYER_RADIUS = 0.40

# Setup Wing II expansion colliders
# Promenade West
add_wall(-3.5, 8.3, -3.5, 13.0)
add_wall(-3.5, 18.5, -3.5, 26.0)
add_wall(-3.5, 31.5, -3.5, 34.3)

# Promenade East
add_wall(3.5, 8.3, 3.5, 13.0)
add_wall(3.5, 18.5, 3.5, 26.0)
add_wall(3.5, 31.5, 3.5, 34.3)

# Promenade North Portal to Wing IV
add_wall(-3.5, 34.3, -1.8, 34.3)
add_wall(1.8, 34.3, 3.5, 34.3)

# Room A (3D Environment)
add_wall(-13.5, 10.5, -13.5, 21.0)
add_wall(-13.5, 10.5, -3.5, 10.5)
add_wall(-13.5, 21.0, -3.5, 21.0)
add_wall(-3.5, 10.5, -3.5, 13.0)
add_wall(-3.5, 18.5, -3.5, 21.0)

# Room B (3D Interior)
add_wall(13.5, 10.5, 13.5, 21.0)
add_wall(3.5, 10.5, 13.5, 10.5)
add_wall(3.5, 21.0, 13.5, 21.0)
add_wall(3.5, 10.5, 3.5, 13.0)
add_wall(3.5, 18.5, 3.5, 21.0)

# Room C (3D VFX)
add_wall(-13.5, 23.5, -13.5, 34.0)
add_wall(-13.5, 23.5, -3.5, 23.5)
add_wall(-13.5, 34.0, -3.5, 34.0)
add_wall(-3.5, 23.5, -3.5, 26.0)
add_wall(-3.5, 31.5, -3.5, 34.0)

# Room D (3D Still Life)
add_wall(13.5, 23.5, 13.5, 34.0)
add_wall(3.5, 23.5, 13.5, 23.5)
add_wall(3.5, 34.0, 13.5, 34.0)
add_wall(3.5, 23.5, 3.5, 26.0)
add_wall(3.5, 31.5, 3.5, 34.0)

# Benches and kiosk
add_box(-8.5, 15.75, 0.45, 1.6, 0)
add_box(8.5, 15.75, 0.45, 1.6, 0)
add_box(-8.5, 28.75, 0.45, 1.6, 0)
add_box(8.5, 28.75, 0.65, 0.65, 0)
add_box(0, 22.25, 0.9, 0.45, 0)

def resolve_collision(px, pz):
    for ((x1, z1), (x2, z2)) in wall_segments:
        dx = x2 - x1
        dz = z2 - z1
        seg_len_sq = dx * dx + dz * dz
        if seg_len_sq == 0:
            continue
        t = max(0.0, min(1.0, ((px - x1) * dx + (pz - z1) * dz) / seg_len_sq))
        cx = x1 + t * dx
        cz = z1 + t * dz
        to_px = px - cx
        to_pz = pz - cz
        dist = math.sqrt(to_px * to_px + to_pz * to_pz)
        if dist < PLAYER_RADIUS:
            if dist < 0.0001:
                to_px = -dz
                to_pz = dx
                dist = math.sqrt(to_px * to_px + to_pz * to_pz)
            norm_x = to_px / dist
            norm_z = to_pz / dist
            overlap = PLAYER_RADIUS - dist
            px += norm_x * overlap
            pz += norm_z * overlap
            
    for (cx, cz, hx, hz, rotY) in box_colliders:
        cosR = math.cos(-rotY)
        sinR = math.sin(-rotY)
        dx = px - cx
        dz = pz - cz
        lx = cosR * dx - sinR * dz
        lz = sinR * dx + cosR * dz
        clamped_x = max(-hx, min(hx, lx))
        clamped_z = max(-hz, min(hz, lz))
        diff_x = lx - clamped_x
        diff_z = lz - clamped_z
        d_sq = diff_x * diff_x + diff_z * diff_z
        if d_sq < PLAYER_RADIUS * PLAYER_RADIUS:
            dist = math.sqrt(d_sq)
            if dist < 0.0001:
                diff_x = 0
                diff_z = 1
                dist = 1
            push = (PLAYER_RADIUS - dist)
            push_lx = (diff_x / dist) * push
            push_lz = (diff_z / dist) * push
            cosBack = math.cos(rotY)
            sinBack = math.sin(rotY)
            px += cosBack * push_lx - sinBack * push_lz
            pz += sinBack * push_lx + cosBack * push_lz
            
    return px, pz

def test_walk(p_start, p_end, steps=100):
    px, pz = p_start
    target_x, target_z = p_end
    for i in range(steps):
        t = (i + 1) / steps
        next_x = p_start[0] + (target_x - p_start[0]) * t
        next_z = p_start[1] + (target_z - p_start[1]) * t
        px, pz = resolve_collision(next_x, next_z)
    final_dist = math.sqrt((px - target_x)**2 + (pz - target_z)**2)
    return px, pz, final_dist

tests = [
    ("Promenade North", (0, 8.5), (0, 20.0)),
    ("Enter Room A (Environment)", (0, 15.75), (-8.5, 15.75)),
    ("Walk inside Room A to South wall", (-8.5, 15.75), (-8.5, 11.5)),
    ("Exit Room A to Promenade", (-8.5, 15.75), (0, 15.75)),
    ("Enter Room B (Interior)", (0, 15.75), (8.5, 15.75)),
    ("Walk inside Room B to East wall", (8.5, 15.75), (12.5, 15.75)),
    ("Exit Room B to Promenade", (8.5, 15.75), (0, 15.75)),
    ("Walk around Central Kiosk to North Promenade", (0, 20.0), (1.8, 22.25)),
    ("Continue past Kiosk to z=28.75", (1.8, 22.25), (0, 28.75)),
    ("Enter Room C (3D VFX)", (0, 28.75), (-8.5, 28.75)),
    ("Walk inside Room C to West wall", (-8.5, 28.75), (-12.5, 28.75)),
    ("Exit Room C to Promenade", (-8.5, 28.75), (0, 28.75)),
    ("Enter Room D (Still Life)", (0, 28.75), (8.5, 28.75)),
    ("Walk inside Room D to East wall", (8.5, 28.75), (12.5, 28.75)),
    ("Exit Room D to Promenade", (8.5, 28.75), (0, 28.75)),
    ("Walk North through Wing IV Portal", (0, 32.0), (0, 36.0)),
]

print("Running Collision Path Simulation:")
all_passed = True
for name, p_start, p_end in tests:
    rx, rz, dist = test_walk(p_start, p_end)
    passed = dist < 0.1
    if not passed:
        all_passed = False
    status = "OK" if passed else f"BLOCKED (dist={dist:.2f}m, pos=({rx:.2f}, {rz:.2f}))"
    print(f"  [{status}] {name}")

print(f"\nOverall Result: {'ALL PATHS CLEAR - ZERO INVISIBLE WALLS' if all_passed else 'SOME PATHS BLOCKED'}")

