with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('scratch/add_atmosphere.py', 'r', encoding='utf-8') as f:
    atm_code = f.read()

pos1 = atm_code.find('function buildMuseumAtmosphere')
pos2 = atm_code.find('function layoutExhibits', pos1)
atm_func = atm_code[pos1:pos2].strip()

# In atm_func, remove shaftTex.flipY = false
atm_func = atm_func.replace('  shaftTex.flipY = false; // v=0 (top of cylinder after flip) => bright end\n', '')
# And set shaftMat opacity to 0.045
atm_func = atm_func.replace('const shaftMat = addMat(shaftTex, 0.07);', 'const shaftMat = addMat(shaftTex, 0.045);')

# Insert right before function layoutExhibits
pos_target = html.find('function layoutExhibits() {')
if pos_target == -1:
    print('Error: function layoutExhibits not found')
    exit(1)

html = html[:pos_target] + atm_func + '\n\n' + html[pos_target:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Restored buildMuseumAtmosphere into index.html!')

