import json

with open('scratch/full_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

for item in cat:
    item['isHung'] = True
    w = item['wing']
    c = item['category']
    media = item.get('mediaType', 'image')
    
    if w == 'I':
        if 'Traditional' in c:
            item['room'] = 'finearts_traditional'
        elif 'Character' in c:
            item['room'] = 'finearts_character'
        else:
            item['room'] = 'finearts_promenade'
    elif w == 'II':
        if 'Environment' in c:
            item['room'] = 'env'
        elif 'Interior' in c:
            item['room'] = 'interior'
        elif 'VFX' in c:
            item['room'] = 'vfx'
        elif 'Still Life' in c:
            item['room'] = 'stilllife'
        else:
            item['room'] = 'char3d'
    elif w == 'III':
        if 'Lunar' in c:
            item['room'] = 'lunar'
        elif 'Street' in c:
            item['room'] = 'street'
        elif 'Animal' in c or 'Wildlife' in c:
            item['room'] = 'wildlife'
        elif 'Model' in c or 'Portrait' in c:
            item['room'] = 'portrait'
        else:
            item['room'] = 'stilllife_object'
    elif w == 'IV':
        if 'Graphic' in c or 'Brand' in c or 'Logo' in c or 'Jacquard' in c or 'Textile' in c:
            item['room'] = 'applied_graphic'
        elif 'Production Design' in c:
            item['room'] = 'production_design'
        elif media == 'video' or 'Animation' in c or 'Foley' in c or 'Kinetic' in c or 'Storytelling' in c or 'Patterns' in item['title']:
            item['room'] = 'cinema'
        else:
            item['room'] = 'storyboard'

with open('scratch/full_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(cat, f, indent=4, ensure_ascii=False)

print("Saved scratch/full_catalog.json with all 205 items hung and categorized!")

