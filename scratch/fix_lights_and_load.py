with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix updateLoadStatus
old_load = """function updateLoadStatus() {
  const el = $('loadStatus'), txt = $('loadText');"""

new_load = """function updateLoadStatus() {
  const el = $('loadStatus'), txt = $('loadText');
  if (!el || !txt) return;"""

if old_load in text:
    text = text.replace(old_load, new_load, 1)
    print("Fixed updateLoadStatus!")
else:
    print("WARNING: old_load not found directly, checking normalized...")
    # Normalize \r\n
    text_norm = text.replace('\r\n', '\n')
    if old_load.replace('\r\n', '\n') in text_norm:
        text = text_norm.replace(old_load.replace('\r\n', '\n'), new_load.replace('\r\n', '\n'), 1)
        print("Fixed updateLoadStatus normalized!")

# 2. Fix buildPictureFrame spotlight overflow
old_spot = """  // Dedicated warm spotlight pointing at artwork
  const spot = new THREE.SpotLight(0xffe4a0, 55, 9, Math.PI / 5, 0.55, 1.2);
  spot.position.set(0, artH / 2 + 1.2, 2.2);
  spot.target = artCanvasMesh;
  spot.castShadow = false;
  group.add(spot);
  group.add(spot.target);

  // Small brass light fixture geometry above frame
  const fixtureBar = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.6, 8), Mat.bronze);
  fixtureBar.rotation.z = Math.PI / 2;
  fixtureBar.position.set(0, artH / 2 + 0.32, 0.35);
  const fixtureHood = new THREE.Mesh(new RoundedBoxGeometry(0.7, 0.06, 0.12, 3, 0.01), Mat.bronze);
  fixtureHood.position.set(0, artH / 2 + 0.35, 0.35);
  const stemL = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.35, 8), Mat.bronze);
  stemL.rotation.x = Math.PI / 3; stemL.position.set(-0.25, artH / 2 + 0.18, 0.18);
  const stemR = stemL.clone(); stemR.position.x = 0.25;
  group.add(fixtureBar, fixtureHood, stemL, stemR);"""

new_spot = """  // Small brass light fixture geometry above frame with warm glowing filament
  const fixtureBar = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.6, 8), Mat.bronze);
  fixtureBar.rotation.z = Math.PI / 2;
  fixtureBar.position.set(0, artH / 2 + 0.32, 0.35);
  const fixtureHood = new THREE.Mesh(new RoundedBoxGeometry(0.7, 0.06, 0.12, 3, 0.01), Mat.bronze);
  fixtureHood.position.set(0, artH / 2 + 0.35, 0.35);
  const stemL = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.35, 8), Mat.bronze);
  stemL.rotation.x = Math.PI / 3; stemL.position.set(-0.25, artH / 2 + 0.18, 0.18);
  const stemR = stemL.clone(); stemR.position.x = 0.25;
  const lampBulb = new THREE.Mesh(
    new THREE.CylinderGeometry(0.012, 0.012, 0.52, 8),
    new THREE.MeshBasicMaterial({ color: 0xfff0c8 })
  );
  lampBulb.rotation.z = Math.PI / 2;
  lampBulb.position.set(0, artH / 2 + 0.32, 0.33);
  group.add(fixtureBar, fixtureHood, stemL, stemR, lampBulb);"""

if old_spot in text:
    text = text.replace(old_spot, new_spot, 1)
    print("Fixed spotlight overflow!")
else:
    text_norm = text.replace('\r\n', '\n')
    if old_spot.replace('\r\n', '\n') in text_norm:
        text = text_norm.replace(old_spot.replace('\r\n', '\n'), new_spot.replace('\r\n', '\n'), 1)
        print("Fixed spotlight overflow normalized!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved updated index.html!")

