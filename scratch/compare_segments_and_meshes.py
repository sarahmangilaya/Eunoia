with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

wings = ['buildWingI', 'buildWingII', 'buildWingIII', 'buildWingIV']
for w in wings:
    start = text.find(f'function {w}()')
    end = text.find('function buildWing', start + 20)
    if end == -1: end = text.find('rotunda_group.add', start)
    code = text[start:end]
    
    print(f"\n==================== {w} ====================")
    segments = re.findall(r'addWallSegment\(([^)]+)\)', code)
    print(f"Total addWallSegment: {len(segments)}")
    for s in segments:
        print("  segment:", s.strip())
        
    meshes = re.findall(r'new THREE\.Mesh\(new THREE\.PlaneGeometry\(([^)]+)\)', code)
    print(f"Total PlaneGeometry meshes: {len(meshes)}")
    for m in meshes:
        print("  mesh plane:", m.strip())

