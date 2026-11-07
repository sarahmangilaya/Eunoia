import os
from PIL import Image

def compare_images(dirpath):
    print(f"\n================ Comparing {dirpath} ================")
    files = sorted([f for f in os.listdir(dirpath) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    imgs = {}
    for f in files:
        im = Image.open(os.path.join(dirpath, f)).convert('RGB').resize((64, 48))
        imgs[f] = list(im.getdata())

    for i in range(len(files)):
        f1 = files[i]
        p1 = imgs[f1]
        for j in range(i + 1, len(files)):
            f2 = files[j]
            p2 = imgs[f2]
            diff = sum(abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2]) for a, b in zip(p1, p2)) / (len(p1) * 3)
            if diff < 20.0:
                print(f"  NEAR DUPLICATE (diff={diff:.2f}): {f1} <==> {f2}")

compare_images("./assets/Projects/Photography/Animal Photography")
compare_images("./assets/Projects/Photography/Lunar Photography")
