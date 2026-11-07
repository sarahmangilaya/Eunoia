import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('exhibits: [')
end = html.find(']\n};', start)
exhibits = json.loads(html[start + len('exhibits: '):end + 1])

print(f"Total exhibits in index.html: {len(exhibits)}")

# 1. Traditional Illustrations (6)
trad = [e for e in exhibits if 'Traditional Illustrations' in e['imagePath']]
print(f"\n--- 1. Traditional Illustrations ({len(trad)}) ---")
for t in trad:
    print(f"  [{t['title']}] ({t['subtitle']})")
    print(f"     \"{t['description'][:70]}...\"")

# 2. Logos (3)
logos = [e for e in exhibits if 'Logos' in e['imagePath']]
print(f"\n--- 2. Logos ({len(logos)}) ---")
for l in logos:
    print(f"  [{l['title']}] ({l['subtitle']})")
    print(f"     \"{l['description'][:70]}...\"")

# 3. Graphic Design (4)
gd = [e for e in exhibits if 'Graphic Design' in e['imagePath']]
print(f"\n--- 3. Graphic Design ({len(gd)}) ---")
for g in gd:
    print(f"  [{g['title']}] ({g['subtitle']})")
    print(f"     \"{g['description'][:70]}...\"")

# 4. Character Designs (7)
cd = [e for e in exhibits if 'Character Designs/' in e['imagePath']]
print(f"\n--- 4. Character Designs ({len(cd)}) ---")
for c in cd:
    print(f"  [{c['title']}] ({c['subtitle']}) | desc empty: {c['description'] == ''}")

# 5. Atelier Lanyard Designs (6)
lanyards = [e for e in exhibits if 'Atelier Lanyard Designs' in e['imagePath']]
print(f"\n--- 5. Atelier Lanyard Designs ({len(lanyards)}) ---")
for lan in lanyards:
    print(f"  [{lan['title']}] ({lan['subtitle']}) | desc empty: {lan['description'] == ''}")

# 6. 3D Works
vfx3d = [e for e in exhibits if '3D VFX' in e['imagePath']]
char3d = [e for e in exhibits if '3D Works/Character Design' in e['imagePath']]
other3d = [e for e in exhibits if ('3D Works' in e['imagePath'] and '3D VFX' not in e['imagePath'] and 'Character Design' not in e['imagePath'])]
print(f"\n--- 6. 3D Works ---")
print(f"  3D VFX ({len(vfx3d)}): {[v['title'] for v in vfx3d]}")
print(f"  3D Character Design ({len(char3d)}): {[v['imagePath'].split('/')[-1] for v in char3d]} (only video: {all(v['mediaType'] == 'video' for v in char3d)})")
print(f"  Other 3D Works ({len(other3d)}): all titles empty: {all(o['title'] == '' for o in other3d)}, all desc empty: {all(o['description'] == '' for o in other3d)}")

# 7. 2D Animation (2)
anim2d = [e for e in exhibits if '2D Animation' in e['imagePath']]
print(f"\n--- 7. 2D Animation ({len(anim2d)}) ---")
for a in anim2d:
    print(f"  [{a['title']}] ({a['subtitle']}) | desc empty: {a['description'] == ''}")

# 8. Digital Art & Illustrations (16)
digi = [e for e in exhibits if 'Digital Illustrations' in e['imagePath']]
print(f"\n--- 8. Digital Art & Illustrations ({len(digi)}) ---")
for d in digi:
    if d['description']:
        print(f"  [{d['title']}] ({d['subtitle']}) -> desc: \"{d['description'][:60]}...\"")
    else:
        print(f"  [{d['title']}] ({d['subtitle']}) -> (no desc)")

# 9. Audio Editing (1)
foley = [e for e in exhibits if 'Foley' in e['imagePath']]
print(f"\n--- 9. Audio Editing ({len(foley)}) ---")
for f in foley:
    print(f"  title empty: {f['title'] == ''} | desc empty: {f['description'] == ''}")

# 10. Storyboarding (20)
sb = [e for e in exhibits if 'Storyboarding' in e['imagePath']]
print(f"\n--- 10. Storyboarding ({len(sb)}) ---")
from collections import Counter
print(f"  Folders: {Counter(s['title'] for s in sb)}")
print(f"  All desc empty: {all(s['description'] == '' for s in sb)}")

# 11. Production Design (14)
pd = [e for e in exhibits if 'Production Design' in e['imagePath']]
print(f"\n--- 11. Production Design ({len(pd)}) ---")
for p in pd[:2]:
    print(f"  [{p['title']}] ({p['subtitle']}) -> \"{p['description'][:70]}...\"")

# 12. Photography (86)
photo = [e for e in exhibits if 'Photography' in e['imagePath']]
print(f"\n--- 12. Photography ({len(photo)}) ---")
for p in photo[:6]:
    print(f"  title: '{p['title']}' | sub: '{p['subtitle']}' | desc: '{p['description']}'")
print(f"  Titles count: {Counter(p['title'] for p in photo)}")
print(f"  All desc empty: {all(p['description'] == '' for p in photo)}")
