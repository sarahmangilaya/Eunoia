import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('exhibits: [')
end = html.find(']\n};', start)
exhibits = json.loads(html[start + len('exhibits: '):end + 1])

for e in exhibits:
    if '3D Works/Character Design' in e['imagePath']:
        print(f"[{e['id']}] mediaType={e['mediaType']} isHung={e['isHung']} path={e['imagePath']}")

