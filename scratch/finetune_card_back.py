import re

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text_norm = text.replace('\r\n', '\n')

# 1. Update CSS for .dossier-back-content and .dossier-back-bottom
old_css_part = '''.dossier-back-content {
      padding: 30px 48px 24px; color: #fbfffe; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; justify-content: space-between; align-items: center; text-align: center;
      position: relative; z-index: 2; text-shadow: 0 1px 4px rgba(0,0,0,.9);
    }'''

new_css_part = '''.dossier-back-content {
      padding: 32px 52px 38px; color: #fbfffe; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; justify-content: space-between; align-items: center; text-align: center;
      position: relative; z-index: 2; text-shadow: 0 1px 4px rgba(0,0,0,.9);
    }'''

if old_css_part in text_norm:
    text_norm = text_norm.replace(old_css_part, new_css_part, 1)
    print("1. Updated padding-bottom on dossier-back-content.")

old_bottom_css = '''.dossier-back-bottom {
      width: 100%; max-width: 350px; display: flex; justify-content: space-between; align-items: center;
      font-size: .66rem; border-top: 1px solid rgba(230,175,46,.3); padding-top: 6px;
    }'''

new_bottom_css = '''.dossier-back-bottom {
      width: 100%; max-width: 280px; display: flex; flex-direction: column; gap: 3px; align-items: center; text-align: center;
      font-size: .66rem; border-top: 1px solid rgba(230,175,46,.35); padding-top: 7px; margin: 0 auto;
    }'''

if old_bottom_css in text_norm:
    text_norm = text_norm.replace(old_bottom_css, new_bottom_css, 1)
    print("2. Updated dossier-back-bottom to centered column.")

# 2. Update the HTML for the bottom area in cardModal
old_bottom_html = '''              <div class="dossier-back-bottom">
                <span class="dossier-status">Open for Studio Roles &amp; Collaborations</span>
                <span class="dossier-email">hello@eunoia.studio</span>
              </div>'''

new_bottom_html = '''              <div class="dossier-back-bottom">
                <span class="dossier-status">Open for Studio Roles, Commissions &amp; Collaborations</span>
                <span class="dossier-email">hello@eunoia.studio</span>
              </div>'''

if old_bottom_html in text_norm:
    text_norm = text_norm.replace(old_bottom_html, new_bottom_html, 1)
    print("3. Updated bottom html in cardModal.")

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text_norm)

print("Saved fine-tuned card back layout.")

