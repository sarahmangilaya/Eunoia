p = 'index.html'
h = open(p, encoding='utf-8').read()

def rep(old, new, count=1):
    global h
    assert old in h, old[:60]
    h = h.replace(old, new, count)

# 1. Softer light shafts, sparser grid in big rooms
rep("const shaftMat = addMat(shaftTex, 0.07);", "const shaftMat = addMat(shaftTex, 0.045);")
rep("const spacing = 4.6, inset = 1.6;", "const spacing = (w >= 11 && d >= 11) ? 6.0 : 4.6, inset = 1.6;")

# 2. Split the art-canvas overlay into its own, gentler material so artwork colours are not washed out
rep("""  Object.keys(poolSpots).forEach((wing) => {
    const geos = [];
    poolSpots[wing].forEach((s) => {
      const isLand = s.land;""", """  const artLightMat = poolMat.clone();
  artLightMat.opacity = 0.32;
  Object.keys(poolSpots).forEach((wing) => {
    const geos = [];
    const artGeos = [];
    poolSpots[wing].forEach((s) => {
      const isLand = s.land;""")
rep("""      gArt.translate(s.x, s.y, s.z);
      geos.push(gArt);
    });""", """      gArt.translate(s.x, s.y, s.z);
      artGeos.push(gArt);
    });
    if (artGeos.length) {
      const flatArt = artGeos.map((p) => (p.index ? p.toNonIndexed() : p));
      const mergedArt = mergeGeometries(flatArt, false);
      artGeos.forEach((g) => g.dispose()); flatArt.forEach((g) => g.dispose());
      const artMesh = new THREE.Mesh(mergedArt, artLightMat);
      artMesh.renderOrder = 2;
      artMesh.frustumCulled = false;
      wingGroups[wing].add(artMesh);
    }""")
open(p, 'w', encoding='utf-8').write(h)
print('tuned')

