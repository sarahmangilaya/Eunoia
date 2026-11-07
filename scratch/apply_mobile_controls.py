import re

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text_norm = text.replace('\r\n', '\n')

# -----------------------------------------------------------------------------
# 1. Update Viewport Meta tag
# -----------------------------------------------------------------------------
old_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">'
new_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">'

if old_meta in text_norm:
    text_norm = text_norm.replace(old_meta, new_meta, 1)
    print("1. Updated viewport meta tag.")
else:
    print("ERROR: old_meta not found")

# -----------------------------------------------------------------------------
# 2. Add Mobile & Virtual Joystick CSS
# -----------------------------------------------------------------------------
old_media_query = '''    @media (max-width: 720px) {
      .legend { grid-template-columns: repeat(3, 1fr); }
      .hud-hint, .hud-fps { display: none; }
      .plaque-scroll { padding: 22px 22px 18px; }
      .plaque-footer { padding: 14px 22px 20px; }
      .catalog-head, .filters, .catalog-grid { padding-left: 18px; padding-right: 18px; }
      .hud-btn .label { display: none; }
    }'''

new_mobile_css = '''    /* ---------- VIRTUAL JOYSTICK (Mobile First-Person Movement) ---------- */
    .virtual-joystick {
      position: fixed; left: max(22px, env(safe-area-inset-left) + 12px);
      bottom: max(24px, env(safe-area-inset-bottom) + 16px);
      z-index: 45; opacity: 0; pointer-events: none;
      transition: opacity .35s var(--ease), transform .35s var(--ease);
      transform: scale(.88);
      touch-action: none; user-select: none; -webkit-user-select: none;
    }
    .virtual-joystick.visible {
      opacity: 1; pointer-events: auto; transform: scale(1);
    }
    .joystick-base {
      width: 124px; height: 124px; border-radius: 50%; position: relative;
      background: radial-gradient(circle, rgba(230, 175, 46, .14) 0%, rgba(0, 21, 20, .68) 75%);
      border: 2px solid rgba(230, 175, 46, .45);
      box-shadow: 0 8px 30px rgba(0, 0, 0, .75), inset 0 0 18px rgba(230, 175, 46, .18);
      backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
      touch-action: none;
    }
    .joystick-knob {
      width: 50px; height: 50px; border-radius: 50%;
      position: absolute; left: 50%; top: 50%; margin: -25px 0 0 -25px;
      background: radial-gradient(circle at 35% 35%, #fff2cc 0%, #e6af2e 55%, #8c6314 100%);
      border: 2px solid rgba(251, 255, 254, .8);
      box-shadow: 0 4px 18px rgba(0, 0, 0, .8), 0 0 15px rgba(230, 175, 46, .6);
      pointer-events: none; will-change: transform;
      transition: transform .08s ease-out;
    }
    .joy-dir {
      position: absolute; font-size: 11px; color: rgba(230, 175, 46, .45); pointer-events: none;
      user-select: none; line-height: 1;
    }
    .joy-up    { top: 7px; left: 50%; transform: translateX(-50%); }
    .joy-down  { bottom: 7px; left: 50%; transform: translateX(-50%); }
    .joy-left  { left: 7px; top: 50%; transform: translateY(-50%); }
    .joy-right { right: 7px; top: 50%; transform: translateY(-50%); }

    /* Crosshair Tap Target & Pulsing on Target */
    #reticle.active {
      cursor: pointer; pointer-events: auto; transform: scale(1.18);
    }
    #reticle.active::after {
      content: ""; position: absolute; inset: -14px; border-radius: 50%;
      border: 1.5px solid rgba(230, 175, 46, .75);
      animation: reticlePulse 1.7s ease-out infinite; pointer-events: none;
    }
    @keyframes reticlePulse {
      0%   { transform: scale(.75); opacity: 1; }
      100% { transform: scale(1.45); opacity: 0; }
    }
    #prompt { cursor: pointer; pointer-events: auto; }

    /* Mobile Controls Info Banner in Lobby */
    .mobile-controls-banner {
      display: none; padding: 14px 18px; border-radius: 12px;
      background: rgba(230, 175, 46, .10); border: 1px solid rgba(230, 175, 46, .35);
      margin: 18px 0 6px; text-align: left;
    }
    .mobile-controls-banner .mob-title {
      font-size: .68rem; letter-spacing: .18em; text-transform: uppercase; color: var(--gold-bright); font-weight: 700;
      margin-bottom: 6px; display: flex; align-items: center; gap: 6px;
    }
    .mobile-controls-banner .mob-list {
      font-size: .75rem; color: #dbe4e2; line-height: 1.5; margin: 0;
    }

    /* ---------- COMPREHENSIVE RESPONSIVE STYLES (PORTRAIT & LANDSCAPE) ---------- */
    @media (max-width: 768px), (pointer: coarse) {
      .legend { display: none !important; }
      .mobile-controls-banner { display: block; }
      .hud-hint, .hud-fps { display: none; }
      #resume { display: none !important; }
      #stage { touch-action: none; }
    }

    /* Portrait Phone Adaptation */
    @media (max-width: 768px) and (orientation: portrait) {
      .hud-top { padding: 12px 14px; }
      .hud-brand .name { font-size: 1.15rem; }
      .hud-brand .loc { font-size: .68rem; }
      .hud-btn { padding: 7px 11px; font-size: .74rem; }
      .hud-btn .label { display: inline-block; font-size: .70rem; }
      .hud-btn .kbd { display: none; }

      .lobby-card {
        width: min(92vw, 440px); max-height: 90vh; padding: 28px 20px 22px;
      }
      .wordmark { font-size: clamp(2.5rem, 10vw, 3.6rem); margin: 6px 0; }
      .tagline { font-size: 1.05rem; }
      .lobby-sub { font-size: .84rem; line-height: 1.45; }
      .lobby-actions { flex-direction: column; width: 100%; gap: 10px; }
      .lobby-actions .btn { width: 100%; }

      /* Curator Plaque as Native Bottom Sheet */
      #plaque {
        width: 100vw; max-width: 100vw; height: 86vh; top: auto; bottom: 0; left: 0; right: 0;
        border-radius: 22px 22px 0 0; border: 1px solid rgba(230, 175, 46, .4);
        transform: translateY(105%); box-shadow: 0 -15px 50px rgba(0, 0, 0, .9);
      }
      #plaque.open { transform: translateY(0); }
      .plaque-scroll { padding: 22px 20px 18px; }
      .plaque-footer { padding: 14px 20px max(18px, env(safe-area-inset-bottom) + 12px); }

      /* Catalog Single-Column Stack */
      .catalog-panel { width: 100vw; }
      .catalog-head { padding: 20px 18px 14px; }
      .catalog-head h2 { font-size: 1.8rem; }
      .filters { padding: 10px 18px 0; overflow-x: auto; flex-wrap: nowrap; -webkit-overflow-scrolling: touch; }
      .filters::-webkit-scrollbar { display: none; }
      .chip { flex-shrink: 0; font-size: .68rem; padding: .55em .95em; }
      .catalog-grid {
        grid-template-columns: 1fr; padding: 16px 18px max(32px, env(safe-area-inset-bottom) + 20px); gap: 18px;
      }

      /* Concierge Modals */
      .concierge-card-wrap { width: min(94vw, 520px); padding: 24px 18px; max-height: 90vh; }
      .dossier-card-container { height: 260px; }
      .dossier-3d-card { width: min(88vw, 420px); height: 250px; }
      .dossier-back-content { padding: 24px 32px 30px; }
      .dossier-quote { font-size: .76rem; }
      .dossier-bio { font-size: .64rem; }
    }

    /* Landscape Phone Adaptation (short screen height) */
    @media (orientation: landscape) and (max-height: 600px) {
      .hud-top { padding: 8px 18px; }
      .hud-btn .kbd { display: none; }
      .virtual-joystick {
        bottom: 14px; left: 16px; transform: scale(.84);
      }
      .virtual-joystick.visible { transform: scale(.92); }

      .lobby-card {
        width: min(92vw, 680px); max-height: 94vh; padding: 18px 28px 16px;
      }
      .wordmark { font-size: 2.2rem; margin: 2px 0; }
      .tagline { font-size: .95rem; margin-bottom: 4px; }
      .lobby-sub { font-size: .78rem; line-height: 1.35; margin-bottom: 12px; }
      .mobile-controls-banner { margin: 8px 0 10px; padding: 8px 14px; }
      .lobby-actions { flex-direction: row; gap: 12px; }

      #plaque {
        width: min(460px, 85vw); height: 100vh; top: 0; bottom: 0; right: 0;
        transform: translateX(105%);
      }
      #plaque.open { transform: translateX(0); }
      .plaque-scroll { padding: 16px 20px 14px; }
      .plaque-footer { padding: 10px 20px 12px; }

      .catalog-panel { width: 100vw; }
      .catalog-head { padding: 14px 22px 10px; }
      .catalog-head h2 { font-size: 1.6rem; }
      .filters { padding: 8px 22px 0; overflow-x: auto; flex-wrap: nowrap; }
      .catalog-grid {
        grid-template-columns: repeat(2, 1fr); padding: 14px 22px 30px; gap: 16px;
      }

      .concierge-card-wrap { max-height: 94vh; padding: 16px 22px; }
      .dossier-card-container { height: 215px; margin: 6px 0; }
      .dossier-3d-card { width: min(80vw, 360px); height: 210px; }
      .dossier-back-content { padding: 18px 24px 24px; }
      .dossier-back-name { font-size: 1.25rem; }
      .dossier-quote { font-size: .72rem; }
      .dossier-bio { font-size: .60rem; line-height: 1.35; }
    }'''

if old_media_query in text_norm:
    text_norm = text_norm.replace(old_media_query, new_mobile_css, 1)
    print("2. Added Virtual Joystick and mobile responsive CSS.")
else:
    print("ERROR: old_media_query not found")

# -----------------------------------------------------------------------------
# 3. Add Virtual Joystick HTML and Menu Button to HUD
# -----------------------------------------------------------------------------
old_hud_actions = '''      <div class="hud-actions">
        <button class="hud-btn glass" id="btnIndex" title="Exhibition Index [TAB]">'''

new_hud_actions = '''      <div class="hud-actions">
        <button class="hud-btn glass" id="btnMenu" title="Menu / Lobby">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="6" x2="20" y2="6"/><line x1="4" y1="18" x2="20" y2="18"/></svg>
          <span class="label">Menu</span>
        </button>
        <button class="hud-btn glass" id="btnIndex" title="Exhibition Index [TAB]">'''

if old_hud_actions in text_norm:
    text_norm = text_norm.replace(old_hud_actions, new_hud_actions, 1)
    print("3. Added btnMenu to HUD actions.")
else:
    print("ERROR: old_hud_actions not found")

# Add Virtual Joystick element before </body>
joystick_html = '''  <!-- ---------------- VIRTUAL TOUCH JOYSTICK FOR MOBILE ---------------- -->
  <div id="virtualJoystick" class="virtual-joystick" aria-hidden="true">
    <div class="joystick-base" id="joystickBase">
      <div class="joystick-knob" id="joystickKnob"></div>
      <span class="joy-dir joy-up">▲</span>
      <span class="joy-dir joy-down">▼</span>
      <span class="joy-dir joy-left">◀</span>
      <span class="joy-dir joy-right">▶</span>
    </div>
  </div>'''

old_lobby_end = '''      <div class="touch-note hidden" id="touchNote">The 3D walk needs a mouse &amp; keyboard. On this device, the 2D catalog offers the full collection.</div>'''
new_lobby_mobile = '''      <div class="mobile-controls-banner" id="mobControlsBanner">
        <div class="mob-title">✦ Dual-Touch Mobile Navigation</div>
        <div class="mob-list">
          <div>• <b>Left Virtual Joystick:</b> Walk forward, back &amp; strafe</div>
          <div>• <b>Drag Screen:</b> Look around smoothly</div>
          <div>• <b>Tap Crosshair:</b> Inspect any targeted work</div>
        </div>
      </div>'''

if old_lobby_end in text_norm:
    text_norm = text_norm.replace(old_lobby_end, new_lobby_mobile, 1)
    print("4. Replaced touch note with mobile controls banner.")
else:
    print("ERROR: old_lobby_end not found")

body_close_anchor = '</body>'
if body_close_anchor in text_norm:
    text_norm = text_norm.replace(body_close_anchor, joystick_html + '\n' + body_close_anchor, 1)
    print("5. Added Virtual Joystick HTML before body close.")
else:
    print("ERROR: body_close_anchor not found")

# -----------------------------------------------------------------------------
# 6. Add JavaScript for Touch Detection, Joystick & Screen Drag Look Around
# -----------------------------------------------------------------------------
mobile_js_code = '''
/* --------------------------------------------------------------------------
   4.13.5  MOBILE DUAL-TOUCH ENGINE: VIRTUAL JOYSTICK & TOUCH LOOK
   -------------------------------------------------------------------------- */
const isTouchDevice = ('ontouchstart' in window || navigator.maxTouchPoints > 0 || window.matchMedia('(pointer: coarse)').matches);
let isMobileActive = false;

// Joystick state
const joystickMove = { x: 0, y: 0 };
let joystickTouchId = null;
let joystickCenter = { x: 0, y: 0 };
const JOYSTICK_MAX_R = 46;

// Look around touch state
let lookTouchId = null;
let lastLookX = 0, lastLookY = 0;

function updateMobileUIState() {
  const joy = $('virtualJoystick');
  if (!joy) return;
  const shouldShow = isTouchDevice && !isLobbyActive && !isInspecting && !isCatalogOpen && !isPhoneModalOpen && !isCardModalOpen;
  joy.classList.toggle('visible', shouldShow);
  joy.setAttribute('aria-hidden', (!shouldShow).toString());
}

// 1. Virtual Joystick Listeners (Bottom-Left)
const joystickBase = $('joystickBase');
const joystickKnob = $('joystickKnob');

function updateJoystickKnob(clientX, clientY) {
  let dx = clientX - joystickCenter.x;
  let dy = clientY - joystickCenter.y;
  const dist = Math.hypot(dx, dy);
  if (dist > JOYSTICK_MAX_R) {
    dx = (dx / dist) * JOYSTICK_MAX_R;
    dy = (dy / dist) * JOYSTICK_MAX_R;
  }
  if (joystickKnob) {
    joystickKnob.style.transform = `translate(${dx}px, ${dy}px)`;
  }
  const normDist = dist / JOYSTICK_MAX_R;
  if (normDist < 0.12) {
    joystickMove.x = 0;
    joystickMove.y = 0;
  } else {
    joystickMove.x = dx / JOYSTICK_MAX_R;
    joystickMove.y = dy / JOYSTICK_MAX_R;
  }
}

if (joystickBase) {
  window.addEventListener('touchstart', (e) => {
    if (!isTouchDevice || isLobbyActive || isInspecting || isCatalogOpen || isPhoneModalOpen || isCardModalOpen) return;
    for (let i = 0; i < e.changedTouches.length; i++) {
      const t = e.changedTouches[i];
      const rect = joystickBase.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dist = Math.hypot(t.clientX - cx, t.clientY - cy);
      // If touch starts within or near joystick base
      if (dist <= rect.width * 0.78 && joystickTouchId === null) {
        joystickTouchId = t.identifier;
        joystickCenter = { x: cx, y: cy };
        updateJoystickKnob(t.clientX, t.clientY);
        break;
      }
    }
  }, { passive: false });

  window.addEventListener('touchmove', (e) => {
    if (joystickTouchId === null) return;
    for (let i = 0; i < e.changedTouches.length; i++) {
      const t = e.changedTouches[i];
      if (t.identifier === joystickTouchId) {
        updateJoystickKnob(t.clientX, t.clientY);
        break;
      }
    }
  }, { passive: false });

  function releaseJoystick(e) {
    if (joystickTouchId === null) return;
    for (let i = 0; i < e.changedTouches.length; i++) {
      const t = e.changedTouches[i];
      if (t.identifier === joystickTouchId) {
        joystickTouchId = null;
        joystickMove.x = 0;
        joystickMove.y = 0;
        if (joystickKnob) {
          joystickKnob.style.transform = 'translate(0, 0)';
        }
        break;
      }
    }
  }
  window.addEventListener('touchend', releaseJoystick, { passive: true });
  window.addEventListener('touchcancel', releaseJoystick, { passive: true });
}

// 2. Touch Drag to Look Around (Outside Joystick)
window.addEventListener('touchstart', (e) => {
  if (isLobbyActive || isInspecting || isCatalogOpen || isPhoneModalOpen || isCardModalOpen) return;
  for (let i = 0; i < e.changedTouches.length; i++) {
    const t = e.changedTouches[i];
    if (t.identifier === joystickTouchId) continue;
    const target = t.target;
    if (target && target.closest && (target.closest('button') || target.closest('a') || target.closest('#reticle') || target.closest('#prompt') || target.closest('#virtualJoystick'))) {
      continue;
    }
    if (lookTouchId === null) {
      lookTouchId = t.identifier;
      lastLookX = t.clientX;
      lastLookY = t.clientY;
    }
  }
}, { passive: true });

window.addEventListener('touchmove', (e) => {
  if (isLobbyActive || isInspecting || isCatalogOpen || isPhoneModalOpen || isCardModalOpen) return;
  if (lookTouchId === null) return;
  for (let i = 0; i < e.changedTouches.length; i++) {
    const t = e.changedTouches[i];
    if (t.identifier === lookTouchId) {
      const dx = t.clientX - lastLookX;
      const dy = t.clientY - lastLookY;
      lastLookX = t.clientX;
      lastLookY = t.clientY;

      const lookSens = 0.0034;
      camera.rotation.order = 'YXZ';
      camera.rotation.y -= dx * lookSens;
      camera.rotation.x -= dy * lookSens;
      camera.rotation.x = Math.max(-1.42, Math.min(1.42, camera.rotation.x));
      break;
    }
  }
}, { passive: true });

function releaseLook(e) {
  if (lookTouchId === null) return;
  for (let i = 0; i < e.changedTouches.length; i++) {
    if (e.changedTouches[i].identifier === lookTouchId) {
      lookTouchId = null;
      break;
    }
  }
}
window.addEventListener('touchend', releaseLook, { passive: true });
window.addEventListener('touchcancel', releaseLook, { passive: true });

// 3. Tap Crosshair Reticle / Prompt to Inspect Targeted Project
function triggerInspectCurrentTarget() {
  if (!hoveredExhibitMesh || isInspecting) return;
  if (hoveredExhibitMesh.userData.isPhone) {
    openPhoneModal();
  } else if (hoveredExhibitMesh.userData.isCard) {
    openCardModal();
  } else if (hoveredExhibitMesh.userData.exhibit) {
    inspectExhibit(hoveredExhibitMesh.userData.exhibit, hoveredExhibitMesh);
  }
}

$('reticle')?.addEventListener('click', (e) => {
  e.stopPropagation();
  triggerInspectCurrentTarget();
});
$('reticle')?.addEventListener('touchend', (e) => {
  e.stopPropagation();
  e.preventDefault();
  triggerInspectCurrentTarget();
});

$('prompt')?.addEventListener('click', (e) => {
  e.stopPropagation();
  triggerInspectCurrentTarget();
});
$('prompt')?.addEventListener('touchend', (e) => {
  e.stopPropagation();
  e.preventDefault();
  triggerInspectCurrentTarget();
});

$('btnMenu')?.addEventListener('click', () => {
  openLobby();
});
'''

# -----------------------------------------------------------------------------
# 7. Update Physics Movement Loop in animate() to incorporate Joystick
# -----------------------------------------------------------------------------
old_physics_loop = '''  // 3. First-Person Physics & Movement
  if (isControlsLocked) {
    const moveSpeed = moveState.sprint ? 5.8 : 3.4;
    const damping = 9.0;

    velocity.x -= velocity.x * damping * delta;
    velocity.z -= velocity.z * damping * delta;

    direction.z = Number(moveState.forward) - Number(moveState.backward);
    direction.x = Number(moveState.right) - Number(moveState.left);
    direction.normalize();

    if (moveState.forward || moveState.backward) {
      velocity.z -= direction.z * moveSpeed * 8.0 * delta;
    }
    if (moveState.left || moveState.right) {
      velocity.x += direction.x * moveSpeed * 8.0 * delta;
    }

    controls.moveRight(velocity.x * delta);
    controls.moveForward(-velocity.z * delta);'''

new_physics_loop = '''  // 3. First-Person Physics & Movement (Desktop Keyboard + Mobile Virtual Joystick)
  if (isControlsLocked || (isTouchDevice && isMobileActive)) {
    const isJoyActive = Math.hypot(joystickMove.x, joystickMove.y) > 0.1;
    const moveSpeed = (moveState.sprint || Math.hypot(joystickMove.x, joystickMove.y) > 0.85) ? 5.8 : 3.4;
    const damping = 9.0;

    velocity.x -= velocity.x * damping * delta;
    velocity.z -= velocity.z * damping * delta;

    // Combine keyboard inputs with virtual joystick analog displacement
    const kForward = (moveState.forward ? 1 : 0) - (moveState.backward ? 1 : 0);
    const kRight = (moveState.right ? 1 : 0) - (moveState.left ? 1 : 0);

    const joyForward = -joystickMove.y; // Up on joystick is forward
    const joyRight = joystickMove.x;

    direction.z = kForward + joyForward;
    direction.x = kRight + joyRight;

    const inputLen = direction.length();
    if (inputLen > 1.0) direction.normalize();

    if (Math.abs(direction.z) > 0.05) {
      velocity.z -= direction.z * moveSpeed * 8.0 * delta;
    }
    if (Math.abs(direction.x) > 0.05) {
      velocity.x += direction.x * moveSpeed * 8.0 * delta;
    }

    controls.moveRight(velocity.x * delta);
    controls.moveForward(-velocity.z * delta);'''

if old_physics_loop in text_norm:
    text_norm = text_norm.replace(old_physics_loop, new_physics_loop, 1)
    print("7. Updated physics movement loop to support virtual joystick.")
else:
    print("ERROR: old_physics_loop not found")

# -----------------------------------------------------------------------------
# 8. Update updateRaycast guard to allow mobile active state
# -----------------------------------------------------------------------------
old_rc_guard = 'if (!isControlsLocked || isInspecting || isCatalogOpen || isPhoneModalOpen || isCardModalOpen) {'
new_rc_guard = 'if ((!isControlsLocked && !isMobileActive) || isInspecting || isCatalogOpen || isPhoneModalOpen || isCardModalOpen) {'

if old_rc_guard in text_norm:
    text_norm = text_norm.replace(old_rc_guard, new_rc_guard, 1)
    print("8. Updated updateRaycast guard for mobileActive.")
else:
    print("ERROR: old_rc_guard not found")

# -----------------------------------------------------------------------------
# 9. Update enterExhibition and openLobby to manage isMobileActive & updateMobileUIState
# -----------------------------------------------------------------------------
old_enter_fn = '''function enterExhibition() {
  initAudio();
  if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();

  isLobbyActive = false;
  $('lobby').classList.add('out');
  document.body.classList.add('in-gallery');

  wakeAllHogwartsVideos();

  // Spawn player in Grand Rotunda facing the central sculpture and north arch
  camera.position.set(0, EYE_HEIGHT, -4.5);
  camera.lookAt(0, EYE_HEIGHT, 4.0);
  camera.rotation.setFromQuaternion(camera.quaternion, 'YXZ');
  if (controls.object) controls.object.position.set(0, EYE_HEIGHT, -4.5);
  velocity.set(0, 0, 0);

  try { controls.lock(); } catch (e) {}
}

function openLobby() {
  isLobbyActive = true;
  document.body.classList.remove('in-gallery');
  $('lobby').classList.remove('out');
  controls.unlock();
}'''

new_enter_fn = '''function enterExhibition() {
  initAudio();
  if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();

  isLobbyActive = false;
  $('lobby').classList.add('out');
  document.body.classList.add('in-gallery');

  wakeAllHogwartsVideos();

  // Spawn player in Grand Rotunda facing the central sculpture and north arch
  camera.position.set(0, EYE_HEIGHT, -4.5);
  camera.lookAt(0, EYE_HEIGHT, 4.0);
  camera.rotation.setFromQuaternion(camera.quaternion, 'YXZ');
  if (controls.object) controls.object.position.set(0, EYE_HEIGHT, -4.5);
  velocity.set(0, 0, 0);

  if (isTouchDevice) {
    isMobileActive = true;
    updateMobileUIState();
  } else {
    try { controls.lock(); } catch (e) {}
  }
}

function openLobby() {
  isLobbyActive = true;
  document.body.classList.remove('in-gallery');
  $('lobby').classList.remove('out');
  if (isTouchDevice) {
    isMobileActive = false;
    updateMobileUIState();
  } else {
    controls.unlock();
  }
}'''

if old_enter_fn in text_norm:
    text_norm = text_norm.replace(old_enter_fn, new_enter_fn, 1)
    print("9. Updated enterExhibition and openLobby for mobile.")
else:
    print("ERROR: old_enter_fn not found")

# -----------------------------------------------------------------------------
# 10. Hook updateMobileUIState in inspection, catalog, and modals
# -----------------------------------------------------------------------------
# Hook in inspectExhibit
old_inspect_open = "$('plaque').classList.add('open');"
new_inspect_open = "$('plaque').classList.add('open');\n  updateMobileUIState();"
text_norm = text_norm.replace(old_inspect_open, new_inspect_open, 1)

# Hook in exitInspection
old_exit_inspect = "$('plaque').classList.remove('open');"
new_exit_inspect = "$('plaque').classList.remove('open');\n  updateMobileUIState();"
text_norm = text_norm.replace(old_exit_inspect, new_exit_inspect, 1)

# Hook in toggleCatalog
old_toggle_cat = "$('catalog').classList.toggle('open', isCatalogOpen);"
new_toggle_cat = "$('catalog').classList.toggle('open', isCatalogOpen);\n  updateMobileUIState();"
text_norm = text_norm.replace(old_toggle_cat, new_toggle_cat, 1)

# Hook in openPhoneModal / closePhoneModal / openCardModal / closeCardModal
text_norm = text_norm.replace("isPhoneModalOpen = true;", "isPhoneModalOpen = true;\n  updateMobileUIState();", 1)
text_norm = text_norm.replace("isPhoneModalOpen = false;", "isPhoneModalOpen = false;\n  updateMobileUIState();", 1)
text_norm = text_norm.replace("isCardModalOpen = true;", "isCardModalOpen = true;\n  updateMobileUIState();", 1)
text_norm = text_norm.replace("isCardModalOpen = false;", "isCardModalOpen = false;\n  updateMobileUIState();", 1)

# Insert mobile_js_code before animate() or before physics loop
animate_anchor = 'function animate() {'
if animate_anchor in text_norm:
    text_norm = text_norm.replace(animate_anchor, mobile_js_code + '\n' + animate_anchor, 1)
    print("10. Inserted mobile dual-touch engine script.")
else:
    print("ERROR: animate_anchor not found")

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text_norm)

print("Mobile compatibility update successfully applied to index.html!")

