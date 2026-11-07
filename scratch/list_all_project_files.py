import os

projects_root = 'assets/Projects'
for root, dirs, files in os.walk(projects_root):
    if files:
        rel = os.path.relpath(root, projects_root)
        print(f"\nFolder: {rel} ({len(files)} files)")
        for f in sorted(files)[:15]:
            print(f"  {f}")

