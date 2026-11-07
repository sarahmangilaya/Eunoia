import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('exhibits: [')
end = html.find(']\n};', start)
exhibits = json.loads(html[start + len('exhibits: '):end + 1])

char3d_exs = [e for e in exhibits if e.get('room') == 'char3d']
print(f"Total char3d exhibits: {len(char3d_exs)}")
for e in char3d_exs:
    print(f"  {e['id']} | {e['imagePath']}")

