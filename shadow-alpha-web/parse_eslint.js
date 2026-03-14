const fs = require('fs');
const report = JSON.parse(fs.readFileSync('eslint-output.json', 'utf8'));

for (const file of report) {
  const errors = file.messages.filter(m => m.severity === 2);
  if (errors.length > 0) {
    console.log(`\nFILE: ${file.filePath}`);
    for (const err of errors) {
      console.log(`  Line ${err.line}: [${err.ruleId || 'ERROR'}] ${err.message}`);
    }
  }
}
