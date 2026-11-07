import re

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# -----------------------------------------------------------------------------
# 1. Update EUNOIA_CONFIG.site with formspreeEndpoint, conciergeAssets, and card data
# -----------------------------------------------------------------------------
old_site_block = '''    contactEmail: "hello@eunoia.studio",
    copyright: "© 2024–2026 Mangilaya · Eunoia Museum. All rights reserved."
  },'''

new_site_block = '''    contactEmail: "hello@eunoia.studio",
    copyright: "© 2024–2026 Mangilaya · Eunoia Museum. All rights reserved.",
    formspreeEndpoint: "https://formspree.io/f/mrpeqnle",
    conciergeAssets: {
      walnutWood: "./assets/concierge/walnut_wood.png",
      rotaryDial: "./assets/concierge/rotary_dial_face.png",
      phoneHero:  "./assets/concierge/red_telephone_hero.png",
      cardFront:  "./assets/concierge/eunoia_card_front.png",
      cardBack:   "./assets/concierge/eunoia_card_back.png"
    },
    card: {
      front: {
        title: "EUNOIA",
        monogram: "E",
        curator: "Mangilaya",
        role: "2D Animator · 3D Generalist · Visual Development Artist",
        tagline: "Beautiful thinking, made visible.",
        stamp: "Curatorial Dossier · No. 01"
      },
      back: {
        bio: "A multidisciplinary animator, 3D generalist, and visual development artist specializing in expressive 2D keyframe animation, atmospheric 3D environments, dynamic VFX simulations, and observational photography.",
        specialties: [
          "2D Hand-Drawn Animation",
          "3D ArchViz & Environments",
          "Blender VFX & Simulations",
          "Character Design & Storyboarding",
          "Editorial & Lunar Photography"
        ],
        education: "B.S. in Entertainment & Multimedia Computing / Fine Arts & Animation",
        status: "Available for Studio Roles, Commissions & Creative Collaborations",
        email: "hello@eunoia.studio"
      }
    }
  },'''

text_norm = text.replace('\r\n', '\n')
if old_site_block in text_norm:
    text_norm = text_norm.replace(old_site_block, new_site_block)
    print("Updated EUNOIA_CONFIG.site")
else:
    print("ERROR: old_site_block not found")

# -----------------------------------------------------------------------------
# 2. Add CSS for Rotary Phone Modal & 3D Dossier Card Modal
# -----------------------------------------------------------------------------
old_css_anchor = '    @media (max-width: 720px) {'

concierge_css = '''    /* ---------- Concierge Telephone & 3D Flip Card Modals ---------- */
    .concierge-overlay {
      position: fixed; inset: 0; z-index: 120; display: flex; align-items: center; justify-content: center;
      background: rgba(0, 8, 8, .78); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
      opacity: 0; pointer-events: none; transition: opacity .4s var(--ease);
    }
    .concierge-overlay.open { opacity: 1; pointer-events: auto; }
    
    .concierge-card-wrap {
      width: min(92vw, 560px); padding: 36px 36px 32px; border-radius: 18px; border: 1px solid rgba(230, 175, 46, .35);
      background: radial-gradient(circle at 50% 0%, rgba(230, 175, 46, .08), transparent 70%), #050b0a;
      box-shadow: 0 24px 60px rgba(0, 0, 0, .85), 0 0 35px rgba(230, 175, 46, .15);
      position: relative; max-height: 90vh; overflow-y: auto;
    }
    .concierge-close {
      position: absolute; top: 16px; right: 18px; background: transparent; border: none;
      color: var(--muted); font-size: 1.5rem; cursor: pointer; padding: 4px 8px; line-height: 1;
      transition: color .2s, transform .2s;
    }
    .concierge-close:hover { color: var(--gold-bright); transform: scale(1.15); }
    
    .phone-modal-head { display: flex; align-items: center; gap: 18px; margin-bottom: 22px; }
    .phone-modal-icon {
      width: 64px; height: 64px; border-radius: 12px; border: 1px solid rgba(230, 175, 46, .3);
      overflow: hidden; flex-shrink: 0; background: #1a0505;
    }
    .phone-modal-icon img { width: 100%; height: 100%; object-fit: cover; }
    .phone-modal-title { font-family: var(--serif); font-size: 1.6rem; color: var(--ivory); margin: 0; line-height: 1.2; }
    .phone-modal-sub { font-size: .80rem; color: var(--gold); letter-spacing: .08em; text-transform: uppercase; margin-top: 4px; }
    
    .phone-form-group { margin-bottom: 16px; }
    .phone-form-label { display: block; font-size: .75rem; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }
    .phone-form-input, .phone-form-textarea {
      width: 100%; padding: 12px 14px; border-radius: 8px; border: 1px solid rgba(251, 255, 254, .12);
      background: rgba(0, 21, 20, .6); color: var(--ivory); font-family: var(--sans); font-size: .88rem;
      outline: none; transition: border-color .25s, box-shadow .25s; box-sizing: border-box;
    }
    .phone-form-input:focus, .phone-form-textarea:focus {
      border-color: var(--gold); box-shadow: 0 0 12px rgba(230, 175, 46, .25);
    }
    .phone-form-textarea { resize: vertical; min-height: 100px; }
    .phone-submit-btn {
      width: 100%; padding: 14px; border-radius: 8px; border: 1px solid var(--gold);
      background: linear-gradient(135deg, #c49735, #e6af2e); color: #001514;
      font-family: var(--sans); font-weight: 700; font-size: .86rem; letter-spacing: .14em;
      text-transform: uppercase; cursor: pointer; transition: transform .2s, box-shadow .2s, filter .2s;
    }
    .phone-submit-btn:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(230, 175, 46, .4); filter: brightness(1.08); }
    .phone-status-msg { margin-top: 14px; font-size: .84rem; text-align: center; display: none; }
    .phone-status-msg.success { color: #52c41a; display: block; }
    .phone-status-msg.error { color: #f5222d; display: block; }

    /* 3D Dossier Card Viewport in Modal */
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
    .dossier-flip-btn:hover { background: rgba(230, 175, 46, .3); }

'''

if old_css_anchor in text_norm:
    text_norm = text_norm.replace(old_css_anchor, concierge_css + old_css_anchor)
    print("Added Concierge CSS styles")
else:
    print("ERROR: old_css_anchor not found")

# -----------------------------------------------------------------------------
# 3. Add HTML Overlays for Telephone Contact Modal & 3D Dossier Card Modal
# -----------------------------------------------------------------------------
old_html_anchor = '  <!-- ---------------- QUICK EXHIBITION INDEX ---------------- -->'

concierge_html = '''  <!-- ---------------- CONCIERGE: ROTARY PHONE CONTACT MODAL ---------------- -->
  <div id="phoneModal" class="concierge-overlay" aria-hidden="true" role="dialog" aria-labelledby="phoneTitle">
    <div class="concierge-card-wrap">
      <button class="concierge-close" id="btnClosePhone" aria-label="Close Telephone Modal">&times;</button>
      <div class="phone-modal-head">
        <div class="phone-modal-icon">
          <img src="./assets/concierge/red_telephone_hero.png" alt="Curator's Rotary Telephone" onerror="this.style.display='none'">
        </div>
        <div>
          <h2 class="phone-modal-title" id="phoneTitle">Curator's Direct Line</h2>
          <div class="phone-modal-sub">Dispatch a Message to Mangilaya</div>
        </div>
      </div>
      <form id="phoneContactForm">
        <div class="phone-form-group">
          <label class="phone-form-label" for="phoneInputName">Your Name / Studio</label>
          <input type="text" id="phoneInputName" name="name" class="phone-form-input" required placeholder="e.g. Hayao Miyazaki · Studio Ghibli">
        </div>
        <div class="phone-form-group">
          <label class="phone-form-label" for="phoneInputEmail">Your Return Line (Email)</label>
          <input type="email" id="phoneInputEmail" name="_replyto" class="phone-form-input" required placeholder="director@studio.com">
        </div>
        <div class="phone-form-group">
          <label class="phone-form-label" for="phoneInputSubject">Subject / Inquiry Type</label>
          <input type="text" id="phoneInputSubject" name="subject" class="phone-form-input" required placeholder="Studio Role / Commission / Art Collaboration">
        </div>
        <div class="phone-form-group">
          <label class="phone-form-label" for="phoneInputMessage">Message Dispatch</label>
          <textarea id="phoneInputMessage" name="message" class="phone-form-textarea" required placeholder="Transmit your inquiry, project scope, or curatorial invitation…"></textarea>
        </div>
        <button type="submit" id="phoneSubmitBtn" class="phone-submit-btn">Transmit via Rotary Dispatch</button>
        <div id="phoneStatusMsg" class="phone-status-msg"></div>
      </form>
    </div>
  </div>

  <!-- ---------------- CONCIERGE: 3D DOSSIER CARD MODAL ---------------- -->
  <div id="cardModal" class="concierge-overlay" aria-hidden="true" role="dialog" aria-labelledby="cardModalTitle">
    <div class="concierge-card-wrap" style="width:min(94vw, 580px)">
      <button class="concierge-close" id="btnCloseCard" aria-label="Close Dossier Modal">&times;</button>
      <div style="text-align:center; margin-bottom: 8px;">
        <div class="overline" style="color:var(--gold); font-size:.70rem; letter-spacing:.3em;">CURATORIAL DOSSIER · NO. 01</div>
        <h2 id="cardModalTitle" class="phone-modal-title" style="font-size:1.8rem; margin:4px 0 0;">Eunoia Atelier</h2>
        <div style="font-size:.82rem; color:var(--muted); margin-top:4px;">Drag to inspect &amp; flip card · 360° Gyroscopic Dossier</div>
      </div>

      <div class="dossier-flip-hint">
        <span>Click or Drag to Flip</span>
        <button type="button" class="dossier-flip-btn" id="btnFlipCardManual">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v-3a9 9 0 0 1 15-5.3L22 6"/><path d="M20 12v3a9 9 0 0 1-15 5.3L2 18"/><polyline points="16 6 22 6 22 12"/><polyline points="8 18 2 18 2 12"/></svg>
          Flip Card
        </button>
      </div>

      <div class="dossier-card-container" id="dossierCardContainer">
        <div class="dossier-3d-card" id="dossier3dCard">
          <div class="dossier-face front" id="dossierFaceFront"></div>
          <div class="dossier-face back" id="dossierFaceBack"></div>
        </div>
      </div>

      <div style="display:flex; justify-content:center; gap:12px; margin-top:10px;">
        <a href="mailto:hello@eunoia.studio" class="btn btn-ghost btn-small">Email Curator</a>
        <button type="button" class="btn btn-gold btn-small" id="btnDossierCall">Ring Rotary Phone</button>
      </div>
    </div>
  </div>

'''

if old_html_anchor in text_norm:
    text_norm = text_norm.replace(old_html_anchor, concierge_html + old_html_anchor)
    print("Added Concierge HTML modals")
else:
    print("ERROR: old_html_anchor not found")

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text_norm)

print("Step 1 & 2 applied.")

