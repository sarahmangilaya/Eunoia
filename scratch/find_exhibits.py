with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('exhibits:')
print('exhibits: at', pos)
print(text[pos:pos+2500])

