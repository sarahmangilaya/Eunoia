import math

wall_segments = []
box_colliders = []

def add_wall(x1, z1, x2, z2):
    wall_segments.append(((x1, z1), (x2, z2)))

def add_box(cx, cz, hx, hz, rotY=0):
    box_colliders.append((cx, cz, hx, hz, rotY))

PLAYER_RADIUS = 0.45

# Promenade West
add_wall(-4.0, 8.3, -4.0, 14.5)
add_wall(-4.0, 20.5, -4.0, 34.0)
add_wall(-4.0, 40.0, -4.0, 52.0)

# Promenade East
add_wall(4.0, 8.3, 4.0, 14.5)
add_wall(4.0, 20.5, 4.0, 34.0)
add_wall(4.0, 40.0, 4.0, 52.0)

# Promenade North Portal to Wing IV
add_wall(-4.0, 52.0, -2.0, 52.0)
add_wall(2.0, 52.0, 4.0, 52.0)

# Room A (3D Environment: x in [-22.0, -4.0], z in [9.5, 25.5])
add_wall(-22.0, 9.5, -22.0, 25.5)
add_wall(-22.0, 9.5, -4.0, 9.5)
add_wall(-22.0, 25.5, -4.0, 25.5)
add_wall(-4.0, 9.5, -4.0, 14.5)
add_wall(-4.0, 20.5, -4.0, 25.5)

# Room B (3D Interior: x in [4.0, 22.0], z in [9.5, 25.5])
add_wall(22.0, 9.5, 22.0, 25.5)
add_wall(4.0, 9.5, 22.0, 9.5)
add_wall(4.0, 25.5, 22.0, 25.5)
add_wall(4.0, 9.5, 4.0, 14.5)
add_wall(4.0, 20.5, 4.0, 25.5)

# Room C (3D VFX: x in [-22.0, -4.0], z in [33.0, 49.0])
add_wall(-22.0, 33.0, -22.0, 49.0)
add_wall(-22.0, 33.0, -4.0, 33.0)
add_wall(-22.0, 49.0, -4.0, 49.0)
add_wall(-4.0, 33.0, -4.0, 34.0)
add_wall(-4.0, 40.0, -4.0, 49.0)

# Room D (3D Still Life: x in [4.0, 22.0], z in [33.0, 49.0])
add_wall(22.0, 33.0, 22.0, 49.0)
add_wall(4.0, 33.0, 22.0, 33.0)
add_wall(4.0, 49.0, 22.0, 49.0)
add_wall(4.0, 33.0, 4.0, 34.0)
add_wall(4.0, 40.0, 4.0, 49.0)

# Wing IV (x in [-13.0, 13.0], z in [52.0, 68.0])
add_wall(-13.0, 68.0, 13.0, 68.0)
add_wall(-13.0, 52.0, -13.0, 68.0)
add_wall(13.0, 52.0, 13.0, 68.0)
add_wall(-13.0, 52.0, -2.0, 52.0)
add_wall(2.0, 52.0, 13.0, 52.0)

# Furniture Colliders
add_box(-13.0, 17.5, 0.55, 1.8, 0) # Room A bench
add_box(13.0, 17.5, 0.55, 1.8, 0)  # Room B bench
add_box(-13.0, 41.0, 0.55, 1.8, 0) # Room C bench
add_box(13.0, 41.0, 0.65, 0.65, 0) # Room D pedestal
add_box(0, 27.0, 0.9, 0.45, 0)     # Promenade kiosk
add_box(0, 59.0, 1.75, 0.55, 0)    # Wing IV bench

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

paths = [
    ("Rotunda to Promenade North", (0, 8.5), (0, 17.5)),
    ("Enter Room A (3D Environment)", (0, 17.5), (-10.0, 17.5)),
    ("Walk around Room A along West Wall", (-10.0, 17.5), (-19.0, 21.5)),
    ("Walk to North Wall of Room A", (-19.0, 21.5), (-13.0, 23.0)),
    ("Exit Room A to Promenade", (-13.0, 23.0), (0, 17.5)),
    ("Enter Room B (3D Interior)", (0, 17.5), (10.0, 17.5)),
    ("Walk around Room B along East Wall", (10.0, 17.5), (19.0, 15.5)),
    ("Exit Room B to Promenade", (19.0, 15.5), (0, 17.5)),
    ("Walk past Promenade Kiosk on West side", (0, 17.5), (-2.0, 27.0)),
    ("Continue to z=37.0", (-2.0, 27.0), (0, 37.0)),
    ("Enter Room C (3D VFX)", (0, 37.0), (-10.0, 37.0)),
    ("Walk inside Room C to view Bonfire", (-10.0, 37.0), (-18.0, 41.0)),
    ("Exit Room C to Promenade", (-18.0, 41.0), (0, 37.0)),
    ("Enter Room D (Still Life)", (0, 37.0), (10.0, 37.0)),
    ("Exit Room D to Promenade", (10.0, 37.0), (0, 37.0)),
    ("Walk North to Wing IV Portal", (0, 37.0), (0, 52.0)),
    ("Enter Wing IV (Kinematic Pavilion)", (0, 52.0), (0, 60.0)),
    ("Walk South from Wing IV all the way to Rotunda", (0, 60.0), (0, 0))
]

print("Running Collision Path Simulation on Expanded Pavilion:")
all_passed = True
for name, p_start, p_end in paths:
    rx, rz, dist = test_walk(p_start, p_end)
    passed = dist < 0.1
    if not passed:
        all_passed = False
    status = "PASS" if passed else f"BLOCKED (dist={dist:.2f}m)"
    print(f"  [{status}] {name}")

print(f"\nOverall Result: {'100% PASS - ALL PATHS CLEAR' if all_passed else 'SOME PATHS BLOCKED'}")

