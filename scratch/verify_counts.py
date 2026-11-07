import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

ex_start = text.find('exhibits: [')
ex_end = text.find(']\n};', ex_start)
hungs = re.findall(r'"isHung":\s*true', text[ex_start:ex_end])
print(f"isHung: true count in index.html: {len(hungs)}")

spots_count = len(re.findall(r'"rotY":', text[text.find('const EXHIBIT_SPOTS'):text.find('function layoutExhibits()')]))
print(f"Total spots in EXHIBIT_SPOTS: {spots_count}")

