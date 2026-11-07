import os
from PIL import Image

def inspect_details(folder):
    print(f"\n--- {folder} ---")
    for f in sorted(os.listdir(folder)):
        if not f.lower().endswith('.jpg'): continue
        im = Image.open(os.path.join(folder, f))
        # downsample and look at bounding box of non-dark pixels for moon
        im_gray = im.convert('L')
        # find min/max
        extrema = im_gray.getextrema()
        # find center of brightness
        w, h = im.size
        small = im_gray.resize((100, 75))
        pixels = list(small.getdata())
        bright = [i for i, p in enumerate(pixels) if p > 30]
        count_bright = len(bright)
        avg_bright = sum(pixels) / len(pixels)
        print(f"{f}: maxVal={extrema[1]}, brightPixels%={count_bright/len(pixels)*100:.1f}%, avgVal={avg_bright:.1f}")

inspect_details("./assets/Projects/Photography/Lunar Photography")

