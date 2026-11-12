const fs = require('fs');
const path = require('path');

let assetRegistry = {};
try {
  const regPath = path.join(__dirname, '..', 'data', 'asset_registry.json');
  if (fs.existsSync(regPath)) {
    assetRegistry = JSON.parse(fs.readFileSync(regPath, 'utf8'));
  }
} catch (e) {
  console.error('[AssetHelper] Error loading asset registry:', e.message);
}

// Canonical University Code Normalization Map
const UNI_CODE_MAP = {
  'university of colombo': 'UOC',
  'university of peradeniya': 'UOP',
  'university of moratuwa': 'UOM',
  'university of sri jayewardenepura': 'USJ',
  'university of kelaniya': 'UOK',
  'university of jaffna': 'UOJ',
  'university of ruhuna': 'UOR',
  'eastern university, sri lanka': 'EUSL',
  'south eastern university of sri lanka': 'SEUSL',
  'rajarata university of sri lanka': 'RUSL',
  'sabaragamuwa university of sri lanka': 'SUSL',
  'wayamba university of sri lanka': 'WUSL',
  'uva wellassa university of sri lanka': 'UWU',
  'uva wellassa university': 'UWU',
  'university of the visual and performing arts': 'UVPA',
  'university of the visual & performing arts': 'UVPA',
  'gampaha wickramarachchi university of indigenous medicine, sri lanka': 'GWUIM',
  'the open university of sri lanka': 'OUSL',
  'ocean university of sri lanka': 'OCUSL',
  'sripalee campus, university of colombo': 'SP-UOC',
  'university of vavuniya': 'VAV',
  'university of vavuniya, sri lanka': 'VAV',
  'university of colombo school of computing': 'UCSC',
  'trincomalee campus, eastern university, sri lanka': 'TC-EUSL',
  'swamy vipulananda institute of aesthetic studies, eastern university, sri lanka': 'SVIAS'
};

function normalizeUniCode(input) {
  if (!input) return 'DEFAULT';
  const raw = String(input).trim();
  const upper = raw.toUpperCase();
  if (assetRegistry.universities && assetRegistry.universities[upper]) {
    return upper;
  }
  const lower = raw.toLowerCase();
  if (UNI_CODE_MAP[lower]) {
    return UNI_CODE_MAP[lower];
  }
  // Substring search in UNI_CODE_MAP
  for (const [key, code] of Object.entries(UNI_CODE_MAP)) {
    if (lower.includes(key) || key.includes(lower)) {
      return code;
    }
  }
  return upper;
}

function getUniLogo(uniNameOrCode) {
  const code = normalizeUniCode(uniNameOrCode);
  const codeLower = code.toLowerCase();
  
  // Direct file check in registry
  if (assetRegistry.universities && assetRegistry.universities[code] && assetRegistry.universities[code].logo) {
    return assetRegistry.universities[code].logo.path;
  }

  // Known campus affiliates
  if (code === 'SP-UOC' || code === 'UCSC') {
    return '/assets/universities/logos/uoc.png';
  }
  if (code === 'TC-EUSL' || code === 'SVIAS') {
    return '/assets/universities/logos/eusl.png';
  }

  // Check if logo file exists on disk
  const localLogo = path.join(__dirname, '..', 'public', 'assets', 'universities', 'logos', `${codeLower}.png`);
  if (fs.existsSync(localLogo)) {
    return `/assets/universities/logos/${codeLower}.png`;
  }

  // Graceful SVG Crest Placeholder
  return '/assets/placeholders/university_logo_placeholder.svg';
}

function getUniCampus(uniNameOrCode) {
  const code = normalizeUniCode(uniNameOrCode);
  const codeLower = code.toLowerCase();

  if (assetRegistry.universities && assetRegistry.universities[code] && assetRegistry.universities[code].campus) {
    return assetRegistry.universities[code].campus.path;
  }

  const localCampus = path.join(__dirname, '..', 'public', 'assets', 'universities', 'campuses', `${codeLower}_campus.webp`);
  if (fs.existsSync(localCampus)) {
    return `/assets/universities/campuses/${codeLower}_campus.webp`;
  }

  // Affiliates
  if (code === 'UCSC') {
    return '/assets/universities/campuses/uoc_campus.webp';
  }

  return '/assets/placeholders/campus_placeholder.webp';
}

function getDegreeCategory(degree) {
  if (!degree) return 'default';
  const text = ((degree.name || '') + ' ' + (degree.stream || '') + ' ' + (degree.faculty || '')).toLowerCase();
  if (/ayurved|indigenous|siddha|unani/.test(text)) return 'ayurveda';
  if (/architecture|design|landscape|interior|built|town|urban/.test(text)) return 'architecture';
  if (/law|legal|llb/.test(text)) return 'law';
  if (/medic|mbbs|dental|surgery|pharm|nurs|physiotherapy|health|radiography/.test(text)) return 'medicine';
  if (/comput|software|information system|data science|artificial intelligence|cyber|ict|it\b/.test(text)) return 'computing';
  if (/engineer|robot|mechatron|aeronaut|electrical|mechanical|civil|chemical/.test(text)) return 'engineering';
  if (/agricul|food science|animal science|aquatic|fisher|forestry|plantation/.test(text)) return 'agriculture';
  if (/manage|commerc|business|account|financ|market|human resource|banking|econom/.test(text)) return 'business';
  if (/educat|teaching|tesl|pedagog/.test(text)) return 'education';
  if (/technolog|bet\b|bict|biosystem/.test(text)) return 'technology';
  if (/arts|humanit|linguist|languag|translat|music|drama|performing|visual art|history|philosophy|sociol/.test(text)) return 'arts';
  if (/physic|chemist|math|statistic|geolog|bio|science/.test(text)) return 'science';
  return 'default';
}

function getDegreeImage(degree) {
  const cat = getDegreeCategory(degree);
  return `/assets/degrees/${cat}.webp`;
}

module.exports = {
  assetRegistry,
  normalizeUniCode,
  getUniLogo,
  getUniCampus,
  getDegreeCategory,
  getDegreeImage
};
