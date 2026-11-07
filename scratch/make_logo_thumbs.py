from PIL import Image
import os

for f in ['aev logo.png', 'asg logo.png', 'asthyles.png']:
    im = Image.open(f'assets/Projects/Logos/{f}')
    im.thumbnail((400, 400))
    im.convert('RGB').save(f'scratch/thumb_logo_{f}.jpg')

