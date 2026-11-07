from PIL import Image

for name in ['eunoia_card_front.png', 'eunoia_card_back.png']:
    im = Image.open('assets/concierge/' + name)
    print(name, im.size, im.mode)

