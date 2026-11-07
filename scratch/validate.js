const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const scriptMatches = html.match(/<script type="module">([\s\S]*?)<\/script>/);
if (!scriptMatches) {
  console.error('Could not find module script!');
  process.exit(1);
}
console.log('Script length:', scriptMatches[1].length);
fs.writeFileSync('scratch/validate_script.js', scriptMatches[1].replace(/import .* from .*/g, '// $&'));
console.log('Written scratch/validate_script.js');

