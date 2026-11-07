import os
import shutil

folder = 'assets/Projects/Traditional Illustrations'
for f in sorted(os.listdir(folder)):
    src = os.path.join(folder, f)
    dst = f"scratch/trad_{f}"
    shutil.copyfile(src, dst)
    print(f"Copied {f} to {dst}")

