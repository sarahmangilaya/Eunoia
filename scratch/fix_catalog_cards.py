with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text_norm = text.replace('\r\n', '\n')

old_card_css = '''    .catalog-grid {
      flex: 1; overflow-y: auto; padding: 20px 34px 40px;
      display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 18px; align-content: start;
      scrollbar-width: thin; scrollbar-color: var(--gold-deep) transparent;
    }
    .card {
      border-radius: 16px; overflow: hidden; border: 1px solid rgba(251, 255, 254, .08); background: rgba(251, 255, 254, .025);
      display: flex; flex-direction: column; transition: transform .3s var(--ease), border-color .3s;
      animation: rise .6s var(--ease) both;
    }
    .card:hover { transform: translateY(-4px); border-color: rgba(230, 175, 46, .6); box-shadow: 0 12px 30px -10px rgba(230, 175, 46, .35); }
    .card-thumb { position: relative; aspect-ratio: 4 / 3; background: #001514; overflow: hidden; cursor: pointer; }
    .card-thumb img { width: 100%; height: 100%; object-fit: cover; transition: transform .8s var(--ease); }
    .card:hover .card-thumb img { transform: scale(1.05); }
    .card-thumb .no { position: absolute; left: 12px; top: 10px; font-family: var(--serif); font-size: .95rem; letter-spacing: .16em; color: #fff; text-shadow: 0 2px 8px #000; }
    .card-body { padding: 16px 18px 18px; display: flex; flex-direction: column; gap: 6px; flex: 1; }
    .card-wing { font-size: .62rem; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); }
    .card-title { font-family: var(--serif); font-size: 1.45rem; font-weight: 500; line-height: 1.1; margin: 0; }
    .card-meta { font-size: .76rem; color: var(--muted); }
    .card-actions { display: flex; gap: 8px; margin-top: auto; padding-top: 12px; }
    .card-actions .btn { flex: 1; }'''

new_card_css = '''    .catalog-grid {
      flex: 1; overflow-y: auto; padding: 24px 34px 48px;
      display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 22px; align-content: start;
      scrollbar-width: thin; scrollbar-color: var(--gold-deep) transparent;
    }
    .card {
      border-radius: 16px; overflow: hidden; border: 1px solid rgba(251, 255, 254, .10);
      background: linear-gradient(180deg, rgba(251, 255, 254, .04) 0%, rgba(0, 21, 20, .6) 100%), #001413;
      display: flex; flex-direction: column; min-height: 390px;
      transition: transform .3s var(--ease), border-color .3s, box-shadow .3s;
      animation: rise .5s var(--ease) both;
    }
    .card:hover { transform: translateY(-4px); border-color: rgba(230, 175, 46, .65); box-shadow: 0 16px 36px -10px rgba(0, 0, 0, .85), 0 0 22px rgba(230, 175, 46, .22); }
    .card-thumb { position: relative; width: 100%; aspect-ratio: 4 / 3; background: #001514; overflow: hidden; cursor: pointer; flex-shrink: 0; }
    .card-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform .8s var(--ease); }
    .card:hover .card-thumb img { transform: scale(1.05); }
    .card-thumb .no { position: absolute; left: 12px; top: 10px; font-family: var(--serif); font-size: .84rem; letter-spacing: .12em; color: #fff; text-shadow: 0 2px 8px #000; padding: 3px 8px; border-radius: 4px; background: rgba(0, 21, 20, .75); backdrop-filter: blur(4px); }
    .card-body { padding: 18px 20px 20px; display: flex; flex-direction: column; gap: 8px; flex: 1 1 auto; }
    .card-wing { font-size: .64rem; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); }
    .card-title { font-family: var(--serif); font-size: 1.45rem; font-weight: 500; line-height: 1.2; margin: 0; color: var(--ivory); }
    .card-meta { font-size: .78rem; color: var(--muted); }
    .card-actions { display: flex; gap: 8px; margin-top: auto; padding-top: 14px; }
    .card-actions .btn { flex: 1; padding: 10px 14px; text-align: center; }'''

if old_card_css in text_norm:
    text_norm = text_norm.replace(old_card_css, new_card_css, 1)
    print("Replaced catalog card CSS with full height, robust flex layout.")
else:
    print("ERROR: old_card_css not found")

with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text_norm)

print("Saved updated index.html")

