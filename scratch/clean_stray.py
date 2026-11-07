with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find("'''")
print('pos:', pos)
if pos != -1:
    pos_func = text.find('function layoutExhibits', pos)
    print('pos_func:', pos_func)
    text = text[:pos] + text[pos_func:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Successfully removed stray tokens!')

