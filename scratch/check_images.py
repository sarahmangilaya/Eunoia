import os
from PIL import Image

def analyze_dir(d):
    print(f"\nAnalyzing: {d}")
    files = sorted(os.listdir(d))
    for f in files:
        if not f.lower().endswith(('.jpg', '.jpeg', '.png')): continue
        fp = os.path.join(d, f)
        sz = os.path.getsize(fp)
        try:
            im = Image.open(fp)
            print(f"  {f}: {im.size[0]}x{im.size[1]} | {sz} bytes")
        except Exception as e:
            print(f"  {f}: {sz} bytes (error: {e})")

analyze_dir("./assets/Projects/Photography/Animal Photography")
analyze_dir("./assets/Projects/Photography/Lunar Photography")

