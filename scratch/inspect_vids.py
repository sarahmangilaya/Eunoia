import json

with open('scratch/full_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

vids = [x for x in cat if x['mediaType'] == 'video']
print(f"Total video exhibits: {len(vids)}")
for v in vids:
    print(f"  {v['id']}: wing={v['wing']}, room={v['room']}, isHung={v['isHung']}, title={v['title']}")

