import os
from PIL import Image

def summarize_images(d):
    print(f"\n================ Summary for {d} ================")
    for f in sorted(os.listdir(d)):
        if not f.lower().endswith(('.jpg', '.jpeg', '.png')): continue
        fp = os.path.join(d, f)
        im = Image.open(fp)
        # get average RGB and thumbnail info
        stat = im.resize((1, 1)).getpixel((0, 0))
        print(f"{f}: size={im.size}, aspect={im.size[0]/im.size[1]:.2f}, avgRGB={stat[:3]}")

summarize_images("./assets/Projects/Photography/Animal Photography")
summarize_images("./assets/Projects/Photography/Lunar Photography")

