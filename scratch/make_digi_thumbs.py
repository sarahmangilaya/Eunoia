from PIL import Image
import os

folder = 'assets/Projects/Digital Illustrations'
for f in os.listdir(folder):
    im = Image.open(f'{folder}/{f}')
    im.thumbnail((400, 400))
    im.convert('RGB').save(f'scratch/thumb_digi_{f}.jpg')
    print(f"Thumb saved for {f}")

