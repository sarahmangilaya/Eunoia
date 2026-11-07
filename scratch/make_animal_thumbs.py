import os
from PIL import Image

folder = "./assets/Projects/Photography/Animal Photography"
out_dir = "./scratch/animal_thumbs"
os.makedirs(out_dir, exist_ok=True)

for f in sorted(os.listdir(folder)):
    if not f.lower().endswith('.jpg'): continue
    im = Image.open(os.path.join(folder, f))
    im.thumbnail((300, 300))
    im.save(os.path.join(out_dir, f))
    print(f"Saved thumb for {f}")

