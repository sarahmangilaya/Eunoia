import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find("'II_interior':")
if pos == -1: pos = text.find('"II_interior":')
print(text[pos:pos+1200])

