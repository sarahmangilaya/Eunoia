import json

with open('scratch/full_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

for item in cat:
    if item['wing'] == 'IV':
        print(f"{item['id']:<45} | {item['title'][:35]:<35} | {item['category']:<35} | {item.get('mediaType')}")

