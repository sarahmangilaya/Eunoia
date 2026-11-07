import json

with open('scratch/exhibit_spots.json', 'r') as f:
    spots = json.load(f)

print("Spots in II_char3d:", len(spots.get('II_char3d', [])))
for i, s in enumerate(spots.get('II_char3d', [])):
    print(f"  spot {i}: x={s['x']}, y={s['y']}, z={s['z']}, rotY={s['rotY']}")

