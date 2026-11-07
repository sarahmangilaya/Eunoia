import json

with open('scratch/full_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

hung_vids = [
    'project-3-mangilaya-energyball',
    'project-4-mangilaya-finals-2-0',
    'project-163-cedilla-mangilaya-plate2',
    'project-164-case-file-no-27',
    'project-165-weekend-at-ernies-nori-productions-teasers',
    'project-191-patterns'
]

for item in cat:
    if item['id'] in hung_vids:
        item['isHung'] = True
        print(f"Set isHung=True for {item['id']}")

with open('scratch/full_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(cat, f, indent=4)

print("Updated full_catalog.json with new hung videos!")

