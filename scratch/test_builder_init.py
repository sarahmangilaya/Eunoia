import json, re

print("Building complete 205-exhibit museum architecture and layout...")

# 1. Load full catalog
with open('scratch/full_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Ensure all 205 items are hung
for item in catalog:
    item['isHung'] = True

print(f"Loaded {len(catalog)} items, all set to isHung = True.")

# 2. Load spots from build_and_verify_all_spots
from scratch.build_and_verify_all_spots import SPOTS

# Let's verify that SPOTS has exact matches for all groups
groups = {}
for ex in catalog:
    key = (ex['wing'], ex['room'])
    groups.setdefault(key, []).append(ex)

for k, items in sorted(groups.items()):
    assert len(items) == len(SPOTS[k]), f"Mismatch in {k}"

print("SPOTS verification passed!")

