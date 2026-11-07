import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('EXHIBIT_SPOTS = {')
pos_end = text.find('window.EXHIBIT_SPOTS', pos)
spots_chunk = text[pos:pos_end]

keys = re.findall(r"['\"]([A-Za-z0-9_]+)['\"]:\s*\[", spots_chunk)
print("All EXHIBIT_SPOTS keys:", keys)

