import json, math

with open('scratch/full_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

print(f"Total catalog items: {len(cat)}")

# Group by wing and folder
grouped = {}
for item in cat:
    wing = item['wing']
    room = item.get('room', 'default')
    cat_name = item['category']
    grouped.setdefault((wing, room, cat_name), []).append(item)

print(f"Total categories/subgroups: {len(grouped)}")
for (w, r, c), items in sorted(grouped.items()):
    print(f"  Wing {w} [{r}] {c}: {len(items)} items")

