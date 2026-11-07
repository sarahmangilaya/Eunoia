import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('exhibits: [')
end = html.find(']\n};', start)
exhibits = json.loads(html[start + len('exhibits: '):end + 1])

for e in exhibits:
    if 'Finals_Mangilaya.mp4' in e['imagePath']:
        print(json.dumps(e, indent=2))

