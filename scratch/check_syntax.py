import re, subprocess

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'<script type="module">(.*?)</script>', html, re.DOTALL)
if not m:
    print('Module script not found!')
else:
    js = m.group(1)
    with open('scratch/module_syntax_check.mjs', 'w', encoding='utf-8') as f_out:
        f_out.write(js)
    res = subprocess.run(['node', '--check', 'scratch/module_syntax_check.mjs'], capture_output=True, text=True)
    if res.returncode == 0:
        print('Node --check PASSED: JavaScript syntax is 100% valid!')
    else:
        print('Syntax error:\n', res.stderr)

