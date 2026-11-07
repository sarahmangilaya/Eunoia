import json, math

# Check Room B exhibit coordinates
with open('scratch/full_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

# Room B exhibits
int_exhibits = [x for x in cat if x.get('room') == 'interior' and x.get('isHung')]
print(f"Room B hung exhibits: {len(int_exhibits)}")

# From layoutExhibits in index.html:
intWallSpots = [
    # South Wall (z = 9.65, rotY = 0)
    { 'x': 8.5,  'y': 2.4, 'z': 9.65, 'wall': 'South' },
    { 'x': 13.0, 'y': 2.4, 'z': 9.65, 'wall': 'South' },
    { 'x': 17.5, 'y': 2.4, 'z': 9.65, 'wall': 'South' },
    # East Wall (x = 21.85, rotY = -Math.PI / 2)
    { 'x': 21.85, 'y': 2.4, 'z': 12.0, 'wall': 'East' },
    { 'x': 21.85, 'y': 2.4, 'z': 15.5, 'wall': 'East' },
    { 'x': 21.85, 'y': 2.4, 'z': 19.5, 'wall': 'East' },
    { 'x': 21.85, 'y': 2.4, 'z': 23.0, 'wall': 'East' },
    # North Wall (z = 25.35, rotY = Math.PI)
    { 'x': 8.5,  'y': 2.4, 'z': 25.35, 'wall': 'North' },
    { 'x': 13.0, 'y': 2.4, 'z': 25.35, 'wall': 'North' },
    { 'x': 17.5, 'y': 2.4, 'z': 25.35, 'wall': 'North' }
]

frame_outer_w = 2.92 # artW (2.6) + 2*frameBorder (0.16)

# Check pairwise distances on same wall
for i in range(len(intWallSpots)):
    for j in range(i + 1, len(intWallSpots)):
        s1 = intWallSpots[i]
        s2 = intWallSpots[j]
        if s1['wall'] == s2['wall']:
            dist = math.sqrt((s1['x'] - s2['x'])**2 + (s1['z'] - s2['z'])**2)
            gap = dist - frame_outer_w
            print(f"Wall {s1['wall']}: spot {i} to {j} -> dist={dist:.2f}m, clear gap={gap:.2f}m (OVERLAP: {gap < 0})")

# Check corner distances
# South-East corner is at (22.0, 9.5)
se_south_frame = intWallSpots[2] # x=17.5, z=9.65
se_east_frame = intWallSpots[3]  # x=21.85, z=12.0
south_frame_max_x = se_south_frame['x'] + frame_outer_w / 2
east_frame_min_z = se_east_frame['z'] - frame_outer_w / 2
print(f"\nSouth-East Corner Check:")
print(f"  South frame right edge: x={south_frame_max_x:.2f}m (East wall is at x=22.0m, distance to East wall={22.0 - south_frame_max_x:.2f}m)")
print(f"  East frame bottom edge: z={east_frame_min_z:.2f}m (South wall is at z=9.5m, distance to South wall={east_frame_min_z - 9.5:.2f}m)")

# North-East corner is at (22.0, 25.5)
ne_north_frame = intWallSpots[9] # x=17.5, z=25.35
ne_east_frame = intWallSpots[6]  # x=21.85, z=23.0
north_frame_max_x = ne_north_frame['x'] + frame_outer_w / 2
east_frame_max_z = ne_east_frame['z'] + frame_outer_w / 2
print(f"\nNorth-East Corner Check:")
print(f"  North frame right edge: x={north_frame_max_x:.2f}m (East wall is at x=22.0m, distance to East wall={22.0 - north_frame_max_x:.2f}m)")
print(f"  East frame top edge: z={east_frame_max_z:.2f}m (North wall is at z=25.5m, distance to North wall={25.5 - east_frame_max_z:.2f}m)")
