import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('exhibits: [')
end = text.find(']\n};', start)
exhibits = json.loads(text[start + len('exhibits: '):end + 1])

print(f"Total exhibits: {len(exhibits)}")

# Group exhibits by wing and room
wings = {}
for e in exhibits:
    w = e.get('wing', 'Unknown')
    r = e.get('room', 'Unknown')
    wings.setdefault(w, {}).setdefault(r, []).append(e)

for w, rooms in sorted(wings.items()):
    print(f"\n=== WING {w} ===")
    for r, exs in sorted(rooms.items()):
        print(f"  Room '{r}': {len(exs)} exhibits")
        # Print bounding box of exhibits in this room
        xs = [e['x'] for e in exs]
        zs = [e['z'] for e in exs]
        print(f"    X range: [{min(xs):.1f}, {max(xs):.1f}], Z range: [{min(zs):.1f}, {max(zs):.1f}]")
        # Group by orientation/plane
        planes = {}
        for e in exs:
            key = f"x={e['x']:.1f}" if abs(e['rotY'] - 1.57) < 0.2 or abs(e['rotY'] + 1.57) < 0.2 else f"z={e['z']:.1f}"
            planes.setdefault(key, []).append(e)
        for p, p_exs in planes.items():
            print(f"      Wall {p}: {len(p_exs)} artworks (rotY: {p_exs[0]['rotY']:.2f})")

