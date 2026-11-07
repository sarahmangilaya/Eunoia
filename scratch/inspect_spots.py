import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find EXHIBIT_SPOTS['III_lunar'] and EXHIBIT_SPOTS['III_wildlife']
pos_spots = text.find('EXHIBIT_SPOTS = {')
pos_spots_end = text.find('window.EXHIBIT_SPOTS', pos_spots)
spots_chunk = text[pos_spots:pos_spots_end]

for rm in ['III_lunar', 'III_wildlife']:
    m = re.search(r"['\"]?" + rm + r"['\"]?:\s*\[(.*?)\](?=,\s*['\"]?[A-Za-z0-9_]+['\"]?:|(?=\s*\}))", spots_chunk, re.DOTALL)
    if m:
        # count entries
        entries = re.findall(r'\{[^\}]+\}', m.group(1))
        print(f"--- EXHIBIT_SPOTS for {rm} (Count: {len(entries)}) ---")
        for idx, entry in enumerate(entries):
            print(f"  [{idx}] {entry.strip()}")
    else:
        print(f"Could not find EXHIBIT_SPOTS for {rm}")

