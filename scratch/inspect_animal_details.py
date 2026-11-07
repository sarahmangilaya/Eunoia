import os
from PIL import Image

def inspect_animal():
    folder = "./assets/Projects/Photography/Animal Photography"
    print(f"\n--- {folder} ---")
    for f in sorted(os.listdir(folder)):
        if not f.lower().endswith('.jpg'): continue
        im = Image.open(os.path.join(folder, f))
        print(f"{f}: size={im.size}, aspect={im.size[0]/im.size[1]:.2f}")

inspect_animal()

