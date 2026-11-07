import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('exhibits: [')
end = html.find(']\n};', start)
exhibits = json.loads(html[start + len('exhibits: '):end + 1])

for e in exhibits:
    p = e['imagePath']
    if 'Photography' in p:
        if 'Animal' in p:
            e['title'] = 'Animal Photography'
        elif 'Lunar' in p:
            e['title'] = 'Lunar Photography'
        elif 'Model' in p:
            e['title'] = 'Model Photography'
        elif 'Object' in p:
            e['title'] = 'Object Photography'
        elif 'Still Life' in p:
            e['title'] = 'Still Life Photography'
        elif 'Street' in p:
            e['title'] = 'Street Photography'
        e['subtitle'] = 'Photography'
        e['description'] = ''

new_json = json.dumps(exhibits, indent=2)
new_html = html[:start + len('exhibits: ')] + new_json + html[end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Photography titles fixed!")

