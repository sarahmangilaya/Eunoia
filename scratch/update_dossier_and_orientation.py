import re

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text_norm = text.replace('\r\n', '\n')

# 1. Update stand rotation to -2.25 (directly facing Rotunda entrance spawn)
old_rot = '  // Orient table so local +Z faces visitor arriving from entrance at (0, -4.5)\n  standG.rotation.y = Math.PI - 0.42;'
new_rot = '  // Orient table so local +Z faces visitor arriving from entrance at (0, -4.5)\n  standG.rotation.y = -2.25;'

if old_rot in text_norm:
    text_norm = text_norm.replace(old_rot, new_rot, 1)
    print("1. Updated stand rotation to -2.25.")
else:
    print("ERROR: old_rot not found")

# 2. Position phone & easel slightly forward (z = 0.04) and plaques
old_phone_pos = 'phoneG.position.set(-0.20, 0.975, -0.02);'
new_phone_pos = 'phoneG.position.set(-0.20, 0.975, 0.04);'
if old_phone_pos in text_norm:
    text_norm = text_norm.replace(old_phone_pos, new_phone_pos, 1)
    print("2. Updated phone position.")

old_easel_pos = 'easelG.position.set(0.19, 0.975, -0.02);'
new_easel_pos = 'easelG.position.set(0.19, 0.975, 0.04);'
if old_easel_pos in text_norm:
    text_norm = text_norm.replace(old_easel_pos, new_easel_pos, 1)
    print("3. Updated easel position.")

# 3. Add rich typography to dossierFaceBack inside cardModal
old_card_back = '<div class="dossier-face back" id="dossierFaceBack"></div>'
new_card_back = '''<div class="dossier-face back" id="dossierFaceBack">
            <div style="padding: 24px 28px; color: #fbfffe; height: 100%; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; position: relative; z-index: 2; text-shadow: 0 1px 4px rgba(0,0,0,0.9);">
              <div>
                <div style="font-size: .66rem; letter-spacing: .25em; color: var(--gold); text-transform: uppercase;">Curatorial Dossier · No. 01</div>
                <h3 style="font-family: var(--serif); font-size: 1.45rem; color: #fbfffe; margin: 4px 0 2px;">Mangilaya</h3>
                <div style="font-size: .74rem; color: #dbe4e2; font-style: italic;">2D Animator · 3D Generalist · Visual Development Artist</div>
              </div>
              <div style="font-size: .72rem; line-height: 1.45; color: #c4d1ce; margin: 8px 0;">
                <p style="margin: 0 0 6px; font-size: .70rem; color: #9ab0ac;">Specializing in expressive 2D keyframe animation, atmospheric 3D environments, Blender VFX simulations, and observational photography.</p>
                <div style="display:flex; flex-wrap:wrap; gap:4px 8px; font-size:.66rem; color:var(--gold-bright);">
                  <span>• 2D Keyframe Animation</span>
                  <span>• 3D ArchViz &amp; Worlds</span>
                  <span>• Blender VFX</span>
                  <span>• Character Design</span>
                  <span>• Observational Photography</span>
                </div>
              </div>
              <div style="display: flex; justify-content: space-between; align-items: flex-end; font-size: .68rem; border-top: 1px solid rgba(230,175,46,0.3); padding-top: 8px;">
                <span style="color: var(--gold);">Available for Studio Roles &amp; Collaborations</span>
                <span style="color: #fbfffe; font-family: monospace;">hello@eunoia.studio</span>
              </div>
            </div>
          </div>'''

if old_card_back in text_norm:
    text_norm = text_norm.replace(old_card_back, new_card_back, 1)
    print("4. Added formatted typography overlay to card back face.")
else:
    print("ERROR: old_card_back not found")

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text_norm)

print("Saved updates to index.html")

