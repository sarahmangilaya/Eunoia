import re, shutil
shutil.copy('index.html', 'scratch/index.html.prefix_doors.bak')
html = open('index.html', encoding='utf-8').read()

# 1. Remove every header box that duplicates a portal lintel / frieze / attic
html, n = re.subn(r"[ \t]*addSolidWall\([^\n]*3\.8, H_WING\);[^\n]*\n", "", html)
print('header boxes removed:', n)
assert n >= 15

def split_flank(src, old, new, label):
    assert old in src, label
    return src.replace(old, new, 1)

# 2. Rotunda wall-portals: portal already builds returns (|x| 1.85..3.5). Mesh only beyond 3.3.
html = split_flank(html,
 "addSolidWall(ox, -5.0, ox, -1.50, Mat.wallWingI, wing);",
 "addSolidWall(ox, -5.0, ox, -3.3, Mat.wallWingI, wing); addWallSegment(ox, -3.3, ox, -1.50);", 'wingI neg')
html = split_flank(html,
 "addSolidWall(ox, 1.50, ox, 5.0, Mat.wallWingI, wing);",
 "addSolidWall(ox, 3.3, ox, 5.0, Mat.wallWingI, wing); addWallSegment(ox, 1.50, ox, 3.3);", 'wingI pos')
html = split_flank(html,
 "addSolidWall(ox, -5.0, ox, -1.50, Mat.wallWingIII, wing);",
 "addSolidWall(ox, -5.0, ox, -3.3, Mat.wallWingIII, wing); addWallSegment(ox, -3.3, ox, -1.50);", 'wingIII neg')
html = split_flank(html,
 "addSolidWall(ox, 1.50, ox, 5.0, Mat.wallWingIII, wing);",
 "addSolidWall(ox, 3.3, ox, 5.0, Mat.wallWingIII, wing); addWallSegment(ox, 1.50, ox, 3.3);", 'wingIII pos')
html = split_flank(html,
 "addSolidWall(-hw, oz, -1.50, oz, Mat.wallWingII, wing);",
 "addSolidWall(-hw, oz, -3.3, oz, Mat.wallWingII, wing); addWallSegment(-3.3, oz, -1.50, oz);", 'wingII neg')
html = split_flank(html,
 "addSolidWall(1.50, oz, hw, oz, Mat.wallWingII, wing);",
 "addSolidWall(3.3, oz, hw, oz, Mat.wallWingII, wing); addWallSegment(1.50, oz, 3.3, oz);", 'wingII pos')

# 3. Wing II's z=52 end walls are fully duplicated by Wing IV's south wall -> collider only
html = split_flank(html,
 "addSolidWall(-hw, 52.0, -2.0, 52.0, Mat.wallWingII, wing);",
 "addWallSegment(-hw, 52.0, -2.0, 52.0); // visual wall provided by Wing IV south wall", 'w2 52 L')
html = split_flank(html,
 "addSolidWall(2.0, 52.0, hw, 52.0, Mat.wallWingII, wing);",
 "addWallSegment(2.0, 52.0, hw, 52.0);", 'w2 52 R')

# 4. Wing I vestibule: fill the missing wall pieces between x=58 and the salon east walls (x=60)
html = split_flank(html,
 "addSolidWall(54.0, 5.0, 58.0, 5.0, Mat.wallWingI, wing);",
 "addSolidWall(54.0, 5.0, 60.0, 5.0, Mat.wallWingI, wing);", 'wing1 N')
html = split_flank(html,
 "addSolidWall(54.0, -5.0, 58.0, -5.0, Mat.wallWingI, wing);",
 "addSolidWall(54.0, -5.0, 60.0, -5.0, Mat.wallWingI, wing);", 'wing1 S')

open('index.html', 'w', encoding='utf-8').write(html)
print('door overlaps fixed')

