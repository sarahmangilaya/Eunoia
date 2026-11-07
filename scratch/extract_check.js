const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const match = html.match(/<script type="module">([\s\S]*?)<\/script>/);
if (match) {
  fs.writeFileSync('scratch/extracted_module.js', match[1]);
  console.log('Wrote scratch/extracted_module.js, length:', match[1].length);
} else {
  console.log('No module script found!');
}

