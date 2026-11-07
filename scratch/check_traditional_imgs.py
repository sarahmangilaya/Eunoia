import os
from PIL import Image

folder = 'assets/Projects/Traditional Illustrations'
for f in sorted(os.listdir(folder)):
    path = os.path.join(folder, f)
    img = Image.open(path)
    print(f"{f}: size={img.size}")

