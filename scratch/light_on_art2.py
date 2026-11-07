p = 'index.html'
h = open(p, encoding='utf-8').read()
def rep(old, new):
    global h
    assert old in h, old[:70]
    h = h.replace(old, new, 1)

# Stronger, clearly visible hot spot on the artwork with deeper fall-off
rep("const v = Math.min(1, cone * fall * 1.55);\n      const t = 0.42 + 0.58 * v;",
    "const v = Math.min(1, Math.pow(cone * fall * 1.5, 1.6));\n      const t = 0.30 + 0.70 * v;")
rep("const ART_SPOT_INTENSITY = Math.PI * 1.32;", "const ART_SPOT_INTENSITY = Math.PI * 1.55;")
# More visible beam from the lamp onto the art
rep("opacity: 0.16, blending: THREE.AdditiveBlending,\n    depthWrite: false, side: THREE.DoubleSide, fog: false\n  });\n  artLightMat.toneMapped = false;",
    "opacity: 0.30, blending: THREE.AdditiveBlending,\n    depthWrite: false, side: THREE.DoubleSide, fog: false\n  });\n  artLightMat.toneMapped = false;")
# Tone down the wall halo behind the frame so the light reads as landing ON the art
rep("map: poolTex, transparent: true, opacity: 0.95,\n    blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide\n  });",
    "map: poolTex, transparent: true, opacity: 0.45,\n    blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide\n  });")
open(p, 'w', encoding='utf-8').write(h)
print('ok')

