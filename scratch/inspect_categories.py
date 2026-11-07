import json
import re
from collections import Counter

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('exhibits: [')
end_idx = html.find(']\n};', start_idx)

if start_idx == -1 or end_idx == -1:
    print("Could not find exhibits slice")
    exit(1)

exhibits_json = html[start_idx + len('exhibits: '): end_idx + 1]
exhibits = json.loads(exhibits_json)
print("Total exhibits:", len(exhibits))

by_cat = Counter(e['category'] for e in exhibits)
for cat, c in by_cat.most_common():
    print(f"  {cat}: {c}")

# Let's inspect the file paths and IDs of works in each category to correlate with user's list
print("\n--- SAMPLE EXHIBITS BY CATEGORY ---")
for cat in by_cat:
    items = [e for e in exhibits if e['category'] == cat]
    print(f"\nCategory: {cat} (Total {len(items)})")
    for it in items[:10]:
        print(f"  [{it['id']}] title: '{it['title']}' | path: '{it['imagePath']}'")
