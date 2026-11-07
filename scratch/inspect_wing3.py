import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all exhibits in Wing III
pos = text.find('EUNOIA_CONFIG = {')
pos_end = text.find('window.EUNOIA_CONFIG', pos)
config_text = text[pos:pos_end]

# Extract exhibit blocks
exhibit_matches = re.findall(r'\{\s*id:\s*[\'"][^\'"]+[\'"].*?wing:\s*[\'"]III[\'"].*?\}', config_text, re.DOTALL)
print(f'Total Wing III exhibits found: {len(exhibit_matches)}')

by_room = {}
for em in exhibit_matches:
    rm_match = re.search(r"room:\s*['\"]([^'\"]+)['\"]", em)
    id_match = re.search(r"id:\s*['\"]([^'\"]+)['\"]", em)
    title_match = re.search(r"title:\s*['\"]([^'\"]+)['\"]", em)
    img_match = re.search(r"imagePath:\s*['\"]([^'\"]+)['\"]", em)
    rm = rm_match.group(1) if rm_match else 'unknown'
    ex_id = id_match.group(1) if id_match else 'unknown'
    title = title_match.group(1) if title_match else ''
    img = img_match.group(1) if img_match else ''
    by_room.setdefault(rm, []).append((ex_id, title, img))

for rm, items in by_room.items():
    print(f"\n--- ROOM: {rm} (Count: {len(items)}) ---")
    for ex_id, title, img in items:
        print(f"  {ex_id}: '{title}' -> {img}")

