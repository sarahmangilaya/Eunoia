import math, json

# Extract wall segments and box colliders from index.html or simulate them
from test_wing2_sim import resolve_collision, test_walk

paths = [
    ("Rotunda to Wing II Entrance", (0, 0), (0, 8.5)),
    ("Wing II Entrance into Promenade", (0, 8.5), (0, 13.0)),
    ("Walk into Room A (3D Environment)", (0, 15.75), (-6.5, 15.75)),
    ("Walk inside Room A along West Artworks", (-6.5, 15.75), (-11.0, 18.5)),
    ("Walk inside Room A along North Artworks", (-11.0, 18.5), (-6.0, 18.5)),
    ("Exit Room A back to Promenade", (-6.0, 15.75), (0, 15.75)),
    ("Walk into Room B (3D Interior)", (0, 15.75), (6.5, 15.75)),
    ("Walk inside Room B along East Artworks", (6.5, 15.75), (11.0, 17.0)),
    ("Exit Room B back to Promenade", (6.5, 15.75), (0, 15.75)),
    ("Walk North past Character Kiosk (West Side)", (0, 15.75), (-1.8, 22.25)),
    ("Walk North past Character Kiosk to z=26.0", (-1.8, 22.25), (0, 26.0)),
    ("Walk into Room C (3D VFX Theatre)", (0, 28.75), (-6.5, 28.75)),
    ("Walk inside Room C to view Bonfire", (-6.5, 28.75), (-10.5, 26.5)),
    ("Exit Room C back to Promenade", (-6.5, 28.75), (0, 28.75)),
    ("Walk into Room D (Still Life Studio)", (0, 28.75), (6.5, 28.75)),
    ("Walk inside Room D to view still life render", (6.5, 28.75), (10.5, 26.5)),
    ("Exit Room D back to Promenade", (6.5, 28.75), (0, 28.75)),
    ("Walk North to Wing IV Portal", (0, 28.75), (0, 34.0)),
    ("Walk into Wing IV (The Kinematic Pavilion)", (0, 34.0), (0, 37.0)),
    ("Walk South from Wing IV back into Wing II", (0, 37.0), (0, 32.0)),
    ("Walk South down Wing II Promenade into Rotunda", (0, 32.0), (0, 0)),
]

print("=== 21 PATH COMPREHENSIVE WALKABILITY AUDIT ===")
all_passed = True
for name, p_start, p_end in paths:
    rx, rz, dist = test_walk(p_start, p_end, steps=80)
    passed = dist < 0.1
    if not passed:
        all_passed = False
    status = "PASS" if passed else f"BLOCKED (dist={dist:.2f}m)"
    print(f"[{status}] {name}")

print(f"\nFinal Result: {'100% PASS - COMPLETE FREEDOM OF MOVEMENT' if all_passed else 'FAIL'}")

