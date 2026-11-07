from PIL import Image
import os

folder = 'assets/Projects/Atelier Lanyard Designs'
for f in sorted(os.listdir(folder)):
    im = Image.open(f'{folder}/{f}')
    im.thumbnail((400, 400))
    im.convert('RGB').save(f'scratch/thumb_lanyard_{f}.jpg')
    print(f"Lanyard thumb saved for {f}")

