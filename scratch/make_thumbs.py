import os
from PIL import Image

folder = 'assets/Projects/Traditional Illustrations'
for f in sorted(os.listdir(folder)):
    path = os.path.join(folder, f)
    im = Image.open(path)
    im.thumbnail((400, 400))
    im.convert('RGB').save(f"scratch/thumb_trad_{f}.jpg")
    print(f"Saved scratch/thumb_trad_{f}.jpg")
