import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract exhibits JSON
pos = text.find('"exhibits": [')
if pos == -1:
    pos = text.find('exhibits: [')
    pos = text.find('[', pos)

# Find matching closing bracket
depth = 0
end = pos
for i in range(pos, len(text)):
    if text[i] == '[':
        depth += 1
    elif text[i] == ']':
        depth -= 1
        if depth == 0:
            end = i + 1
            break

exhibits = json.loads(text[pos:end])
print(f"Total exhibits loaded: {len(exhibits)}")

wing3 = [e for e in exhibits if e.get('wing') == 'III']
print(f"Total Wing III exhibits: {len(wing3)}")

by_room = {}
for e in wing3:
    rm = e.get('room', 'unknown')
    by_room.setdefault(rm, []).append(e)

for rm, items in by_room.items():
    print(f"\n================ ROOM: {rm} (Count: {len(items)}) ================")
    for idx, e in enumerate(items):
        print(f"[{idx}] {e.get('id')}: '{e.get('title')}' | orient: {e.get('orientation')} | img: {e.get('imagePath')}")

