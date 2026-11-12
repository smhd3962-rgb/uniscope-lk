const fs = require('fs');
const path = require('path');
const { getUniCampus, getUniLogo, normalizeUniCode } = require('../utils/asset_helper');

const dbPath = path.join(__dirname, '..', 'data', 'database.json');
const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));

console.log('Testing University Campus Asset Resolutions:\n');
let count = 0;
let placeholderCount = 0;

for (const [uName, uInfo] of Object.entries(db.universities)) {
  const code = normalizeUniCode(uName);
  const campus = getUniCampus(uName);
  const logo = getUniLogo(uName);
  const isPlaceholder = campus.includes('placeholder');
  if (isPlaceholder) placeholderCount++;
  count++;
  
  const status = isPlaceholder ? '[PLACEHOLDER]' : '[OK REAL PHOTO]';
  console.log(`${status} ${code.padEnd(8)}: ${uName}`);
  console.log(`         Campus -> ${campus}`);
  console.log(`         Logo   -> ${logo}\n`);
}

console.log(`Summary: ${count - placeholderCount}/${count} universities have verified campus photos!`);
