from PIL import Image
import os

folder = 'assets/Projects/Character Designs'
for f in os.listdir(folder):
    im = Image.open(f'{folder}/{f}')
    im.thumbnail((400, 400))
    im.convert('RGB').save(f'scratch/thumb_cd_{f}.jpg')
    print(f"Thumbnail saved for {f}")

