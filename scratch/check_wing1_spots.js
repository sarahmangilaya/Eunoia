const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const match = html.match(/"I_finearts_promenade":\s*(\[[^;]*?\])\s*,\s*"I_/);
if (match) {
  const list = JSON.parse(match[1]);
  list.forEach((s, i) => console.log(i, 'x:', s.x, 'z:', s.z, 'rotY:', s.rotY));
}

