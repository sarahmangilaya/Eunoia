import re

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text_norm = text.replace('\r\n', '\n')

# -----------------------------------------------------------------------------
# 1. Update CSS for 3D Dossier Card & Back Face Typography
# -----------------------------------------------------------------------------
old_dossier_css = '''    /* 3D Dossier Card Viewport in Modal */
    .dossier-card-container {
      perspective: 1200px; width: 100%; height: 280px; display: flex; align-items: center; justify-content: center;
      margin: 18px 0 22px; cursor: grab; user-select: none;
    }
    .dossier-card-container:active { cursor: grabbing; }
    .dossier-3d-card {
      width: min(88vw, 460px); height: 260px; position: relative;
      transform-style: preserve-3d; transition: transform .2s cubic-bezier(.2, .8, .2, 1);
    }
    .dossier-face {
      position: absolute; inset: 0; width: 100%; height: 100%; border-radius: 12px;
      backface-visibility: hidden; -webkit-backface-visibility: hidden;
      box-shadow: 0 18px 45px rgba(0, 0, 0, .8), 0 0 20px rgba(230, 175, 46, .2);
      overflow: hidden; border: 1px solid rgba(230, 175, 46, .45); background-size: cover; background-position: center;
    }
    .dossier-face.front { background-color: #001514; }
    .dossier-face.back { background-color: #001514; transform: rotateY(180deg); }
    .dossier-flip-hint {
      text-align: center; font-size: .76rem; letter-spacing: .12em; color: var(--gold);
      text-transform: uppercase; margin-bottom: 12px; display: flex; align-items: center; justify-content: center; gap: 8px;
    }
    .dossier-flip-btn {
      display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 999px;
      background: rgba(230, 175, 46, .15); border: 1px solid rgba(230, 175, 46, .4); color: var(--gold-bright);
      font-size: .72rem; cursor: pointer; transition: background .2s;
    }
    .dossier-flip-btn:hover { background: rgba(230, 175, 46, .3); }'''

new_dossier_css = '''    /* 3D Dossier Card Viewport in Modal - Click to Flip */
    .dossier-card-container {
      perspective: 1200px; width: 100%; height: 310px; display: flex; align-items: center; justify-content: center;
      margin: 14px 0 18px; cursor: pointer; user-select: none;
    }
    .dossier-3d-card {
      width: min(90vw, 480px); height: 285px; position: relative;
      transform-style: preserve-3d;
      transition: transform .65s cubic-bezier(.22, 1, .36, 1);
    }
    .dossier-3d-card:hover {
      box-shadow: 0 24px 55px rgba(0, 0, 0, .9), 0 0 35px rgba(230, 175, 46, .25);
    }
    .dossier-3d-card.is-flipped {
      transform: rotateY(180deg);
    }
    .dossier-face {
      position: absolute; inset: 0; width: 100%; height: 100%; border-radius: 14px;
      backface-visibility: hidden; -webkit-backface-visibility: hidden;
      box-shadow: 0 18px 45px rgba(0, 0, 0, .8), 0 0 20px rgba(230, 175, 46, .2);
      overflow: hidden; border: 1px solid rgba(230, 175, 46, .45); background-size: cover; background-position: center;
    }
    .dossier-face.front { background-color: #001514; }
    .dossier-face.back { background-color: #001514; transform: rotateY(180deg); }

    /* Centered curatorial back layout safely cleared from corner filigree borders */
    .dossier-back-content {
      padding: 30px 48px 24px; color: #fbfffe; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; justify-content: space-between; align-items: center; text-align: center;
      position: relative; z-index: 2; text-shadow: 0 1px 4px rgba(0,0,0,.9);
    }
    .dossier-back-sub {
      font-size: .62rem; letter-spacing: .24em; color: var(--gold); text-transform: uppercase; margin-bottom: 2px;
    }
    .dossier-back-name {
      font-family: var(--serif); font-size: 1.45rem; color: #fbfffe; margin: 2px 0 3px; letter-spacing: .04em;
    }
    .dossier-back-title {
      font-size: .70rem; color: #dbe4e2; font-style: italic; letter-spacing: .02em;
    }
    .dossier-back-statement {
      max-width: 340px; margin: 4px auto;
    }
    .dossier-quote {
      font-family: var(--serif); font-size: .84rem; color: var(--gold-bright); font-style: italic;
      line-height: 1.35; margin: 0 0 4px;
    }
    .dossier-bio {
      font-size: .68rem; line-height: 1.42; color: #b8c8c5; margin: 0;
    }
    .dossier-back-disciplines {
      font-size: .62rem; letter-spacing: .05em; color: var(--gold);
      display: flex; flex-wrap: wrap; justify-content: center; gap: 4px 6px;
      max-width: 340px; margin: 2px auto;
    }
    .dossier-back-disciplines span { color: #dbe4e2; }
    .dossier-back-bottom {
      width: 100%; max-width: 350px; display: flex; justify-content: space-between; align-items: center;
      font-size: .66rem; border-top: 1px solid rgba(230,175,46,.3); padding-top: 6px;
    }
    .dossier-status { color: var(--gold); font-size: .64rem; }
    .dossier-email { color: #fbfffe; font-family: monospace; font-size: .66rem; }

    .dossier-flip-hint {
      text-align: center; font-size: .76rem; letter-spacing: .12em; color: var(--gold);
      text-transform: uppercase; margin-bottom: 12px; display: flex; align-items: center; justify-content: center; gap: 8px;
    }
    .dossier-flip-btn {
      display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 999px;
      background: rgba(230, 175, 46, .15); border: 1px solid rgba(230, 175, 46, .4); color: var(--gold-bright);
      font-size: .72rem; cursor: pointer; transition: background .2s;
    }
    .dossier-flip-btn:hover { background: rgba(230, 175, 46, .3); }'''

if old_dossier_css in text_norm:
    text_norm = text_norm.replace(old_dossier_css, new_dossier_css, 1)
    print("1. Updated CSS for click-to-flip and border-cleared card typography.")
else:
    print("ERROR: old_dossier_css not found")

# -----------------------------------------------------------------------------
# 2. Update HTML for cardModal: poetic copy and border-safe layout
# -----------------------------------------------------------------------------
card_modal_pattern = re.compile(r'<!-- -+ CONCIERGE: 3D DOSSIER CARD MODAL -+ -->.*?<!-- -+ QUICK EXHIBITION INDEX -+ -->', re.DOTALL)

new_card_modal_html = '''<!-- ---------------- CONCIERGE: 3D DOSSIER CARD MODAL ---------------- -->
  <div id="cardModal" class="concierge-overlay" aria-hidden="true" role="dialog" aria-labelledby="cardModalTitle">
    <div class="concierge-card-wrap" style="width:min(94vw, 580px)">
      <button class="concierge-close" id="btnCloseCard" aria-label="Close Dossier Modal">&times;</button>
      <div style="text-align:center; margin-bottom: 8px;">
        <div class="overline" style="color:var(--gold); font-size:.70rem; letter-spacing:.3em;">CURATORIAL DOSSIER · EUNOIA ARCHIVE</div>
        <h2 id="cardModalTitle" class="phone-modal-title" style="font-size:1.8rem; margin:4px 0 0;">Sarah Mae Mangilaya</h2>
        <div style="font-size:.82rem; color:var(--muted); margin-top:4px;">Click card to flip · Exploring the intersection of animation, virtual worlds &amp; classical art</div>
      </div>

      <div class="dossier-flip-hint">
        <span>Click Card to Flip</span>
        <button type="button" class="dossier-flip-btn" id="btnFlipCardManual" aria-label="Flip Card">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v-3a9 9 0 0 1 15-5.3L22 6"/><path d="M20 12v3a9 9 0 0 1-15 5.3L2 18"/><polyline points="16 6 22 6 22 12"/><polyline points="8 18 2 18 2 12"/></svg>
          Flip Card
        </button>
      </div>

      <div class="dossier-card-container" id="dossierCardContainer" title="Click card to flip">
        <div class="dossier-3d-card" id="dossier3dCard">
          <div class="dossier-face front" id="dossierFaceFront"></div>
          <div class="dossier-face back" id="dossierFaceBack">
            <div class="dossier-back-content">
              <div>
                <div class="dossier-back-sub">CURATORIAL DOSSIER · NO. 01</div>
                <h3 class="dossier-back-name">Sarah Mae Mangilaya</h3>
                <div class="dossier-back-title">Visual Development Artist · 2D Animator · 3D Generalist</div>
              </div>
              
              <div class="dossier-back-statement">
                <p class="dossier-quote">“Beautiful thinking, made visible through movement, light, and architectural form.”</p>
                <p class="dossier-bio">Bridging expressive 2D keyframe animation with atmospheric 3D environments, Blender VFX simulations, and observational studies across 205 curated museum exhibits.</p>
              </div>

              <div class="dossier-back-disciplines">
                <span>2D Keyframe Animation</span> · <span>3D ArchViz &amp; Worlds</span> · <span>Blender VFX</span> · <span>Observational Studies</span>
              </div>

              <div class="dossier-back-bottom">
                <span class="dossier-status">Open for Studio Roles &amp; Collaborations</span>
                <span class="dossier-email">hello@eunoia.studio</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div style="display:flex; justify-content:center; gap:12px; margin-top:10px;">
        <a href="mailto:hello@eunoia.studio" class="btn btn-ghost btn-small">Email Curator</a>
        <button type="button" class="btn btn-gold btn-small" id="btnDossierCall">Ring Rotary Phone</button>
      </div>
    </div>
  </div>

  <!-- ---------------- QUICK EXHIBITION INDEX ---------------- -->'''

if card_modal_pattern.search(text_norm):
    text_norm = card_modal_pattern.sub(new_card_modal_html, text_norm, 1)
    print("2. Replaced cardModal HTML with border-cleared layout and museum-grade copy.")
else:
    print("ERROR: card_modal_pattern not found")

# -----------------------------------------------------------------------------
# 3. Update HUD Reticle Prompts & Table Plaque text
# -----------------------------------------------------------------------------
old_reticle_prompts = '''    if (hit.userData.isPhone) {
      $('promptTitle').textContent = "Curator's Rotary Phone [Ring Line]";
    } else if (hit.userData.isCard) {
      $('promptTitle').textContent = "Curator's Dossier [Inspect & Flip]";
    } else {'''

new_reticle_prompts = '''    if (hit.userData.isPhone) {
      $('promptTitle').textContent = "Curator's Direct Line [Call Studio]";
    } else if (hit.userData.isCard) {
      $('promptTitle').textContent = "Curator's Dossier · Mangilaya [Examine]";
    } else {'''

if old_reticle_prompts in text_norm:
    text_norm = text_norm.replace(old_reticle_prompts, new_reticle_prompts, 1)
    print("3. Updated HUD reticle prompts.")
else:
    print("ERROR: old_reticle_prompts not found")

# -----------------------------------------------------------------------------
# 4. Update Table Brass Plaque text
# -----------------------------------------------------------------------------
old_card_plaque = '''    ctx.fillStyle = '#fbfffe'; ctx.font = `italic 20px ${SERIF}`; ctx.textAlign = 'center';
    ctx.fillText('Click to Inspect & Flip 3D Card', w / 2, 85);'''

new_card_plaque = '''    ctx.fillStyle = '#fbfffe'; ctx.font = `italic 20px ${SERIF}`; ctx.textAlign = 'center';
    ctx.fillText('Click to Examine & Flip Dossier', w / 2, 85);'''

if old_card_plaque in text_norm:
    text_norm = text_norm.replace(old_card_plaque, new_card_plaque, 1)
    print("4. Updated table 3D brass plaque text.")
else:
    print("ERROR: old_card_plaque not found")

# -----------------------------------------------------------------------------
# 5. Remove drag-to-flip interaction, replace with pure click-to-flip
# -----------------------------------------------------------------------------
old_drag_interaction = '''// 3D Card Gyroscopic Drag & Flip Interaction
let cardRotX = 0, cardRotY = 0;
let isCardFlipped = false;
let isDraggingCard = false;
let startCardX = 0, startCardY = 0;
let baseCardRotX = 0, baseCardRotY = 0;

function updateCardTransform() {
  const card = $('dossier3dCard');
  if (!card) return;
  const targetY = cardRotY + (isCardFlipped ? 180 : 0);
  card.style.transform = `rotateX(${cardRotX}deg) rotateY(${targetY}deg)`;
}

const cardContainer = $('dossierCardContainer');
if (cardContainer) {
  cardContainer.addEventListener('mousedown', (e) => {
    isDraggingCard = true;
    startCardX = e.clientX;
    startCardY = e.clientY;
    baseCardRotX = cardRotX;
    baseCardRotY = cardRotY;
  });
  window.addEventListener('mousemove', (e) => {
    if (!isDraggingCard) return;
    const dx = e.clientX - startCardX;
    const dy = e.clientY - startCardY;
    cardRotY = baseCardRotY + dx * 0.45;
    cardRotX = Math.max(-45, Math.min(45, baseCardRotX - dy * 0.35));
    updateCardTransform();
  });
  window.addEventListener('mouseup', () => {
    if (isDraggingCard) {
      isDraggingCard = false;
      cardRotX *= 0.4;
      updateCardTransform();
    }
  });

  // Touch support for mobile / tablets
  cardContainer.addEventListener('touchstart', (e) => {
    if (e.touches.length > 0) {
      isDraggingCard = true;
      startCardX = e.touches[0].clientX;
      startCardY = e.touches[0].clientY;
      baseCardRotX = cardRotX;
      baseCardRotY = cardRotY;
    }
  }, { passive: true });
  window.addEventListener('touchmove', (e) => {
    if (!isDraggingCard || !e.touches.length) return;
    const dx = e.touches[0].clientX - startCardX;
    const dy = e.touches[0].clientY - startCardY;
    cardRotY = baseCardRotY + dx * 0.45;
    cardRotX = Math.max(-45, Math.min(45, baseCardRotX - dy * 0.35));
    updateCardTransform();
  }, { passive: true });
  window.addEventListener('touchend', () => {
    isDraggingCard = false;
  });

  // Manual Flip Button
  $('btnFlipCardManual')?.addEventListener('click', () => {
    isCardFlipped = !isCardFlipped;
    updateCardTransform();
  });

  // Ring Rotary Phone from inside Card Modal
  $('btnDossierCall')?.addEventListener('click', () => {
    closeCardModal();
    setTimeout(openPhoneModal, 150);
  });

  $('btnCloseCard')?.addEventListener('click', closeCardModal);
  $('cardModal')?.addEventListener('click', (e) => {
    if (e.target === $('cardModal')) closeCardModal();
  });
}'''

new_click_flip_interaction = '''// 3D Dossier Card Click-to-Flip Interaction (Pure Click, No Dragging)
let isCardFlipped = false;

function setCardFlipped(flipped) {
  isCardFlipped = flipped;
  const card = $('dossier3dCard');
  if (card) {
    if (isCardFlipped) {
      card.classList.add('is-flipped');
    } else {
      card.classList.remove('is-flipped');
    }
  }
}

function toggleCardFlip() {
  setCardFlipped(!isCardFlipped);
}

const cardContainer = $('dossierCardContainer');
if (cardContainer) {
  // Click anywhere on the card or container to flip
  cardContainer.addEventListener('click', () => {
    toggleCardFlip();
  });

  // Manual Flip Button
  $('btnFlipCardManual')?.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleCardFlip();
  });

  // Ring Rotary Phone from inside Card Modal
  $('btnDossierCall')?.addEventListener('click', () => {
    closeCardModal();
    setTimeout(openPhoneModal, 150);
  });

  $('btnCloseCard')?.addEventListener('click', closeCardModal);
  $('cardModal')?.addEventListener('click', (e) => {
    if (e.target === $('cardModal')) closeCardModal();
  });
}'''

if old_drag_interaction in text_norm:
    text_norm = text_norm.replace(old_drag_interaction, new_click_flip_interaction, 1)
    print("5. Replaced drag-to-flip interaction with pure click-to-flip.")
else:
    print("ERROR: old_drag_interaction not found")

# Also update openCardModal to reset is-flipped class
old_open_card = '''  cardRotX = 0; cardRotY = 0; isCardFlipped = false;
  updateCardTransform();'''
new_open_card = '''  setCardFlipped(false);'''

if old_open_card in text_norm:
    text_norm = text_norm.replace(old_open_card, new_open_card, 1)
    print("6. Updated openCardModal to reset card flip state.")
else:
    print("ERROR: old_open_card not found")

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text_norm)

print("Card adjustments successfully applied!")

