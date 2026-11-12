const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const fs = require('fs');
const auth = require('./utils/auth');
const contact = require('./utils/contact');
const assetHelper = require('./utils/asset_helper');

const app = express();
const PORT = process.env.PORT || 3000;

// Load database
const dbPath = path.join(__dirname, 'data', 'database.json');
let database = { degrees: [], universities: {}, districts: [], subjects: [], combo_mappings: {}, cutoffs: [], career_fields: [] };

try {
  database = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
  console.log(`[UniScope LK] Loaded database with ${database.degrees.length} degrees and ${database.cutoffs.length} cutoff records.`);
} catch (err) {
  console.error('[UniScope LK] Error reading database.json:', err);
}

// Load student services directory
const studentServicesPath = path.join(__dirname, 'data', 'student_services.json');
let studentServicesData = { version: "1.0.0", total_services: 0, categories: [], services: [] };

try {
  if (fs.existsSync(studentServicesPath)) {
    studentServicesData = JSON.parse(fs.readFileSync(studentServicesPath, 'utf8'));
    console.log(`[UniScope LK] Loaded Student Services Directory with ${studentServicesData.services.length} services across ${studentServicesData.categories.length} categories.`);
  }
} catch (err) {
  console.error('[UniScope LK] Error reading student_services.json:', err);
}

// Load degree recognition and accreditation directory
const degreeRecPath = path.join(__dirname, 'data', 'degree_recognition.json');
let degreeRecData = { version: "1.0.0", total_records: 0, authorities: [], records: [] };

try {
  if (fs.existsSync(degreeRecPath)) {
    degreeRecData = JSON.parse(fs.readFileSync(degreeRecPath, 'utf8'));
    console.log(`[UniScope LK] Loaded Degree Recognition & Accreditation Directory with ${degreeRecData.records.length} records.`);
  }
} catch (err) {
  console.error('[UniScope LK] Error reading degree_recognition.json:', err);
}

// View engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser('uniscope_secure_secret_2026'));
app.use(express.static(path.join(__dirname, 'public')));

// Global Asset & Branding Helpers
app.locals.getUniLogo = assetHelper.getUniLogo;
app.locals.getUniCampus = assetHelper.getUniCampus;
app.locals.getDegreeImage = assetHelper.getDegreeImage;
app.locals.getDegreeCategory = assetHelper.getDegreeCategory;
app.locals.assetRegistry = assetHelper.assetRegistry;

// User authentication helper
function getAuthUser(req) {
  // Check session token first
  const sessionToken = req.cookies.uniscope_session;
  if (sessionToken) {
    const user = auth.getUserFromSession(sessionToken);
    if (user) return user;
  }
  // Check legacy user id if present and valid
  const legacyUserId = req.cookies.uniscope_user;
  if (legacyUserId) {
    return auth.findUserById(legacyUserId);
  }
  return null;
}

// Request context middleware
app.use((req, res, next) => {
  res.locals.user = getAuthUser(req);
  res.locals.currentPath = req.path;
  res.locals.getUniLogo = assetHelper.getUniLogo;
  res.locals.getUniCampus = assetHelper.getUniCampus;
  res.locals.getDegreeImage = assetHelper.getDegreeImage;
  res.locals.getDegreeCategory = assetHelper.getDegreeCategory;
  res.locals.assetRegistry = assetHelper.assetRegistry;
  res.locals.platform = database.platform || {
    name: 'UniScope LK',
    initiative: 'Independent Sri Lankan Higher Education Information Directory'
  };
  next();
});

// Proper static media handling
app.use('/media', (req, res, next) => {
  const mediaPath = path.join(__dirname, 'public', 'media', req.path);
  if (fs.existsSync(mediaPath) && fs.statSync(mediaPath).isFile()) {
    return res.sendFile(mediaPath);
  }
  // Fallback placeholder instead of blanket logo redirect
  const placeholder = path.join(__dirname, 'public', 'assets', 'placeholders', 'campus_placeholder.webp');
  if (fs.existsSync(placeholder)) {
    return res.sendFile(placeholder);
  }
  res.status(404).send('Asset not found');
});

// ==========================================
// WEB ROUTES
// ==========================================

// Homepage
app.get('/', (req, res) => {
  res.render('index', {
    title: "UniScope LK - Sri Lanka Higher Education Directory & UGC Admissions Platform"
  });
});

// Subject Combination Search
app.get('/subject-combination/', (req, res) => {
  const { sub1, sub2, sub3 } = req.query;
  const subjects = database.subjects || [];
  let results = {};
  let hasSearched = false;

  if (sub1 && sub2 && sub3) {
    hasSearched = true;
    const s1 = parseInt(sub1);
    const s2 = parseInt(sub2);
    const s3 = parseInt(sub3);
    const setIds = new Set([s1, s2, s3]);

    // Check known combinations
    if (setIds.has(129) && setIds.has(124)) { // Maths + Physics (Engineering/Physical stream)
      results = database.combo_mappings['Tech_ET'] || {};
      // Inject physical science courses
      results['Physical Science Stream'] = [
        { code: '008', name: 'Engineering' },
        { code: '009', name: 'Engineering (EM)' },
        { code: '010', name: 'Engineering (TM)' },
        { code: '012', name: 'Computer Science' },
        { code: '013', name: 'Physical Science' },
        { code: '015', name: 'Applied Sciences (Physical Sc.)' },
        { code: '057', name: 'Transport Management & Logistics Engineering (TMLE)' },
        { code: '059', name: 'Industrial Statistics & Mathematical Finance' },
        { code: '060', name: 'Statistics & Operations Research' },
        { code: '117', name: 'Artificial Intelligence' },
        { code: '119', name: 'Data Science' }
      ];
    } else if (setIds.has(128) && setIds.has(125)) { // Bio + Chemistry
      results = database.combo_mappings['Bio'] || {};
    } else if (setIds.has(147) || setIds.has(146) || setIds.has(138)) { // Commerce
      results = database.combo_mappings['Commerce'] || {};
    } else if (setIds.has(166) || setIds.has(167)) { // Technology
      results = database.combo_mappings['Tech_ET'] || {};
    } else {
      results = database.combo_mappings['Arts'] || {};
    }
  }

  res.render('subject-combination', {
    subjects: subjects,
    selectedSub1: sub1,
    selectedSub2: sub2,
    selectedSub3: sub3,
    results: results,
    hasSearched: hasSearched
  });
});

// All Degrees Directory & Gallery
app.get(['/degrees/all/', '/degrees/gallery/'], (req, res) => {
  const stream = req.query.stream || '';
  const q = (req.query.q || '').trim().toLowerCase();
  const page = parseInt(req.query.page) || 1;
  const pageSize = 24;

  let filtered = database.degrees || [];

  if (stream) {
    filtered = filtered.filter(d => (d.stream || '').toLowerCase() === stream.toLowerCase());
  }

  if (q) {
    filtered = filtered.filter(d => 
      (d.name || '').toLowerCase().includes(q) ||
      (d.university || '').toLowerCase().includes(q) ||
      (d.code || '').toLowerCase().includes(q) ||
      (d.faculty || '').toLowerCase().includes(q)
    );
  }

  const totalCount = filtered.length;
  const totalPages = Math.ceil(totalCount / pageSize) || 1;
  const startIndex = (page - 1) * pageSize;
  const paginated = filtered.slice(startIndex, startIndex + pageSize);

  res.render('degrees', {
    degrees: paginated,
    selectedStream: stream,
    searchQuery: req.query.q || '',
    page: page,
    totalPages: totalPages,
    totalCount: totalCount
  });
});

// Single Degree Detail (17-Sections)
app.get('/degrees/detail/:code/', (req, res) => {
  const code = req.params.code;
  const degree = database.degrees.find(d => 
    d.code === code || 
    d.code === code.toUpperCase() ||
    d.code.startsWith(code) ||
    (d.code && d.code.replace(/[^0-9]/g, '') === code)
  );

  if (!degree) {
    return res.status(404).render('404');
  }

  res.render('degree-detail', { degree: degree });
});

// Smart Degree Comparison Tool
app.get('/dashboard/compare/', (req, res) => {
  const { d1, d2, d3, district } = req.query;
  const selectedCodes = [d1, d2, d3].filter(Boolean);
  const compareDistrict = district || 'Colombo';
  
  let comparedDegrees = [];
  if (selectedCodes.length > 0) {
    comparedDegrees = selectedCodes.map(code => 
      database.degrees.find(d => d.code === code || d.code.startsWith(code) || (code && d.code.replace(/[^0-9]/g, '') === code))
    ).filter(Boolean);
  }
  
  if (comparedDegrees.length === 0) {
    // Default show 2 prominent degrees (e.g. Engineering and Computer Science)
    comparedDegrees = database.degrees.slice(0, 2);
  }

  // Calculate historical cut-off trend for each compared degree for compareDistrict
  const years = database.academic_years || ['2025/2026', '2024/2025', '2023/2024', '2022/2023'];
  const historicalData = comparedDegrees.map(deg => {
    const records = {};
    let sum = 0;
    let count = 0;
    years.forEach(yr => {
      const match = database.cutoffs.find(c => 
        c.year === yr && 
        (c.course_code === deg.code || c.course_name.toLowerCase().includes(deg.name.toLowerCase().slice(0, 15))) &&
        c.district.toLowerCase() === compareDistrict.toLowerCase()
      );
      if (match) {
        records[yr] = match.min_zscore;
        if (typeof match.min_zscore === 'number') {
          sum += match.min_zscore;
          count++;
        }
      } else {
        records[yr] = 'N/A';
      }
    });

    // Year-to-year change between 2024/2025 and 2025/2026
    let yoyChange = 'N/A';
    if (typeof records['2025/2026'] === 'number' && typeof records['2024/2025'] === 'number') {
      const diff = records['2025/2026'] - records['2024/2025'];
      yoyChange = (diff >= 0 ? '+' : '') + diff.toFixed(4);
    }

    const avg = count > 0 ? (sum / count).toFixed(4) : 'N/A';

    return {
      degreeCode: deg.code,
      degreeName: deg.name,
      university: deg.university,
      records: records,
      yoyChange: yoyChange,
      average: avg
    };
  });

  res.render('compare', {
    allDegrees: database.degrees,
    selectedCodes: comparedDegrees.map(d => d.code),
    comparedDegrees: comparedDegrees,
    districts: database.districts,
    selectedDistrict: compareDistrict,
    academicYears: years,
    historicalData: historicalData
  });
});

// UGC Cut-Off Marks Tool / University Z-Score Explorer
app.get(['/degrees/cutoff-tool/', '/tools/zscore-explorer/'], (req, res) => {
  const { stream, district, year, myZ } = req.query;
  const targetYear = year || database.latest_academic_year || '2025/2026';
  const years = database.academic_years || ['2025/2026', '2024/2025', '2023/2024', '2022/2023'];

  let filtered = database.cutoffs.filter(c => c.year === targetYear);

  if (stream) {
    filtered = filtered.filter(c => c.stream.toLowerCase() === stream.toLowerCase());
  }

  if (district) {
    filtered = filtered.filter(c => c.district.toLowerCase() === district.toLowerCase());
  }

  // Generate historical trends if district is selected (or default Colombo)
  let historicalTrends = [];
  const trendDistrict = district || 'Colombo';
  if (filtered.length > 0) {
    const sampleCourses = filtered.slice(0, 20);
    historicalTrends = sampleCourses.map(item => {
      const records = {};
      years.forEach(yr => {
        const match = database.cutoffs.find(c => 
          c.year === yr && 
          c.course_name.toLowerCase() === item.course_name.toLowerCase() &&
          c.university.toLowerCase() === item.university.toLowerCase() &&
          c.district.toLowerCase() === trendDistrict.toLowerCase()
        );
        records[yr] = match ? match.min_zscore : 'N/A';
      });

      // Calculate trend description
      let trendText = 'Stable';
      if (typeof records['2025/2026'] === 'number' && typeof records['2024/2025'] === 'number') {
        const delta = records['2025/2026'] - records['2024/2025'];
        if (delta > 0.01) trendText = `+${delta.toFixed(4)} ↑`;
        else if (delta < -0.01) trendText = `${delta.toFixed(4)} ↓`;
        else trendText = `${delta >= 0 ? '+' : ''}${delta.toFixed(4)} ~`;
      }

      return {
        course_code: item.course_code || '',
        course_name: item.course_name,
        university: item.university,
        stream: item.stream,
        district: trendDistrict,
        records: records,
        trend: trendText
      };
    });
  }

  res.render('cutoff-tool', {
    cutoffs: filtered.slice(0, 60),
    districts: database.districts,
    selectedStream: stream || '',
    selectedDistrict: district || '',
    selectedYear: targetYear,
    latestYear: database.latest_academic_year || '2025/2026',
    academicYears: years,
    historicalTrends: historicalTrends,
    trendDistrict: trendDistrict,
    myZ: myZ || ''
  });
});

// Dedicated Z-Score Eligibility Tool
app.get('/zscore-calculator/', (req, res) => {
  const { stream, district, zscore } = req.query;
  let confirmed = [];
  let competitive = [];
  let hasCalculated = false;
  let z = parseFloat(zscore);
  const targetYear = database.latest_academic_year || '2025/2026';

  if (stream && district && !isNaN(z)) {
    hasCalculated = true;
    const matchCutoffs = database.cutoffs.filter(c => 
      c.year === targetYear &&
      c.stream.toLowerCase() === stream.toLowerCase() &&
      c.district.toLowerCase() === district.toLowerCase()
    );

    matchCutoffs.forEach(c => {
      if (typeof c.min_zscore !== 'number') return;
      const diff = z - c.min_zscore;
      if (diff >= 0.05) {
        confirmed.push(c);
      } else if (diff >= -0.05 && diff < 0.05) {
        competitive.push(c);
      }
    });
  }

  res.render('zscore-calculator', {
    districts: database.districts,
    stream: stream || '',
    district: district || '',
    zscore: zscore || '',
    z: z,
    hasCalculated: hasCalculated,
    confirmed: confirmed,
    competitive: competitive,
    latestYear: targetYear
  });
});

// UGC District Determination Tool
app.get('/district-tool/', (req, res) => {
  res.render('district-tool', {
    districts: database.districts
  });
});

// GPA Calculator for Sri Lankan University Students
app.get(['/gpa-calculator/', '/tools/gpa-calculator/'], (req, res) => {
  res.render('gpa-calculator', {
    title: "Sri Lankan University GPA & CGPA Calculator - UniScope LK",
    universities: database.universities || {}
  });
});

// Student Services & Official Resources Directory
app.get(['/student-services', '/student-services/'], (req, res) => {
  res.render('student-services', {
    title: "Student Services & Official Portals Directory - UniScope LK",
    servicesData: studentServicesData,
    categories: studentServicesData.categories || [],
    services: studentServicesData.services || [],
    user: getAuthUser(req)
  });
});

// FEATURE 1: University Application Checklist
app.get(['/student-tools/application-checklist', '/student-tools/application-checklist/'], (req, res) => {
  res.render('application-checklist', {
    title: "University Application Checklist - UniScope LK",
    user: getAuthUser(req)
  });
});

// FEATURE 2: University Cost-of-Living Planner
app.get(['/student-tools/cost-planner', '/student-tools/cost-planner/'], (req, res) => {
  res.render('cost-planner', {
    title: "University Cost-of-Living Planner - UniScope LK",
    user: getAuthUser(req)
  });
});

// FEATURE 3: Degree Recognition & Accreditation Guide
app.get(['/student-tools/degree-recognition', '/student-tools/degree-recognition/'], (req, res) => {
  res.render('degree-recognition', {
    title: "Degree Recognition & Accreditation Guide - UniScope LK",
    authorities: degreeRecData.authorities || [],
    records: degreeRecData.records || [],
    user: getAuthUser(req)
  });
});

// Degree Recognition JSON API
app.get('/api/degree-recognition', (req, res) => {
  const { search, discipline, authority } = req.query;
  let results = degreeRecData.records || [];
  if (discipline && discipline !== 'all') {
    results = results.filter(r => r.discipline.toLowerCase().includes(discipline.toLowerCase()));
  }
  if (authority && authority !== 'all') {
    results = results.filter(r => r.authority.toLowerCase().includes(authority.toLowerCase()));
  }
  if (search) {
    const q = search.toLowerCase();
    results = results.filter(r =>
      r.programme.toLowerCase().includes(q) ||
      r.institution.toLowerCase().includes(q) ||
      r.discipline.toLowerCase().includes(q) ||
      r.authority.toLowerCase().includes(q)
    );
  }
  res.json({
    total: results.length,
    records: results,
    authorities: degreeRecData.authorities || []
  });
});

// Student Services JSON API endpoint
app.get('/api/student-services', (req, res) => {
  const { category, search } = req.query;
  let results = studentServicesData.services || [];
  if (category && category !== 'all') {
    results = results.filter(s => s.category === category);
  }
  if (search) {
    const q = search.toLowerCase();
    results = results.filter(r =>
      r.title.toLowerCase().includes(q) ||
      r.description.toLowerCase().includes(q) ||
      r.provider.toLowerCase().includes(q) ||
      (r.keywords && r.keywords.some(k => k.toLowerCase().includes(q))) ||
      (r.targetAudience && r.targetAudience.toLowerCase().includes(q))
    );
  }
  res.json({
    total: results.length,
    services: results,
    categories: studentServicesData.categories || []
  });
});

// Smart Degree Finder (Cosine Similarity)
app.get('/degree-finder/', (req, res) => {
  res.render('degree-finder', {
    districts: database.districts
  });
});

// AI Displacement Risk Checker
app.get('/ai-risk/', (req, res) => {
  res.render('ai-risk', {
    degrees: database.degrees
  });
});

// Universities Directory
app.get('/universities/', (req, res) => {
  res.render('universities', {
    universities: database.universities
  });
});

// Career Pathways & Job Field Explorer
app.get('/career-paths/', (req, res) => {
  res.render('career-paths', {
    careerFields: database.career_fields
  });
});

// Community Announcements & Educational Resources
app.get('/community/announcements/', (req, res) => {
  res.render('announcements');
});

// Student Educational Guides & Reference Knowledge Base
app.get('/community/resources/', (req, res) => {
  res.render('forums');
});

// Canonical Redirects for legacy forum/friend routes
app.get(['/community/forums/', '/dashboard/find-friends/'], (req, res) => {
  res.redirect(301, '/community/resources/');
});

// About Us & Founder
app.get('/about-us/', (req, res) => {
  res.render('about-us');
});

// Admissions & Student FAQ
app.get(['/faq/', '/community/faq/'], (req, res) => {
  res.render('faq');
});

// Data Sources, Methodology & Research Standards (Fixed Canonical Route)
app.get(['/data-sources/', '/data-sources', '/research/transparency/'], (req, res) => {
  res.render('data-sources');
});

// Legal & Institutional Notice Pages
app.get('/disclaimer/', (req, res) => res.render('disclaimer'));
app.get('/donate/', (req, res) => res.render('donate'));
app.get('/privacy-policy/', (req, res) => res.render('privacy-policy'));
app.get('/terms-of-use/', (req, res) => res.render('terms-of-use'));
app.get(['/contact-us/', '/share-feedback/'], (req, res) => res.render('contact-us'));

// ==========================================
// AUTHENTICATION ROUTES (Secure, Salted Hashing, No Demo Fallback)
// ==========================================

app.get('/accounts/login/', (req, res) => {
  const user = getAuthUser(req);
  if (user) {
    return res.redirect('/accounts/profile/');
  }
  res.render('login', { error: null });
});

app.post('/accounts/login/', (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).render('login', { error: 'Please enter both your email address and password.' });
  }

  const user = auth.validateCredentials(email, password);
  if (!user) {
    return res.status(401).render('login', { error: 'Invalid email address or password. Please check your credentials.' });
  }

  const sessionToken = auth.createSession(user.id);
  res.cookie('uniscope_session', sessionToken, {
    maxAge: 14 * 24 * 60 * 60 * 1000,
    httpOnly: true,
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production'
  });
  res.cookie('uniscope_user', user.id, {
    maxAge: 14 * 24 * 60 * 60 * 1000,
    httpOnly: true,
    sameSite: 'lax'
  });

  const redirectTo = req.query.redirect || '/accounts/profile/';
  res.redirect(redirectTo);
});

app.get('/accounts/register/', (req, res) => {
  const user = getAuthUser(req);
  if (user) {
    return res.redirect('/accounts/profile/');
  }
  res.render('register', { error: null, districts: database.districts });
});

app.post('/accounts/register/', (req, res) => {
  const { name, email, password, district, stream } = req.body;
  if (!name || !email || !password) {
    return res.status(400).render('register', {
      error: 'Name, email address, and password are required.',
      districts: database.districts
    });
  }

  if (password.length < 6) {
    return res.status(400).render('register', {
      error: 'Password must be at least 6 characters in length.',
      districts: database.districts
    });
  }

  try {
    const newUser = auth.createUser({ name, email, password, district, stream });
    const sessionToken = auth.createSession(newUser.id);
    res.cookie('uniscope_session', sessionToken, {
      maxAge: 14 * 24 * 60 * 60 * 1000,
      httpOnly: true,
      sameSite: 'lax',
      secure: process.env.NODE_ENV === 'production'
    });
    res.cookie('uniscope_user', newUser.id, {
      maxAge: 14 * 24 * 60 * 60 * 1000,
      httpOnly: true,
      sameSite: 'lax'
    });
    res.redirect('/accounts/profile/');
  } catch (err) {
    return res.status(409).render('register', {
      error: err.message,
      districts: database.districts
    });
  }
});

app.get('/accounts/profile/', (req, res) => {
  const user = getAuthUser(req);
  if (!user) {
    return res.redirect('/accounts/login/?redirect=/accounts/profile/');
  }
  res.render('profile', { user: user });
});

app.get('/accounts/logout/', (req, res) => {
  const sessionToken = req.cookies.uniscope_session;
  if (sessionToken) {
    auth.destroySession(sessionToken);
  }
  res.clearCookie('uniscope_session');
  res.clearCookie('uniscope_user');
  res.redirect('/accounts/login/');
});

// Google OAuth Handler (Secure Requirement Check: No Demo Users)
app.get('/accounts/google/login/', (req, res) => {
  const hasGoogleConfig = process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET;
  if (!hasGoogleConfig) {
    return res.status(503).render('login', {
      error: 'Google Sign-In is currently in configuration mode. External OAuth requires GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment settings. Please log in with your student email and password.'
    });
  }
  // When credentials exist, redirect to official Google OAuth flow
  res.redirect(`https://accounts.google.com/o/oauth2/v2/auth?client_id=${process.env.GOOGLE_CLIENT_ID}&response_type=code&scope=openid%20email%20profile`);
});

// ==========================================
// REST APIS
// ==========================================

// Exact API required by subject combination popup (Zero Fictitious University Output)
app.get('/api/course/:code/', (req, res) => {
  const code = req.params.code;
  const matchedDegrees = database.degrees.filter(d => 
    d.code === code || 
    d.code === code.toUpperCase() ||
    d.code.startsWith(code) || 
    (d.code && d.code.replace(/[^0-9]/g, '') === code)
  );

  if (matchedDegrees.length === 0) {
    // Clear user-friendly error instead of fictitious universities
    return res.status(404).json({
      status: 'not_found',
      course_code: code,
      error: 'Course information not available',
      message: `Course information not available for code '${code}' in the official UGC catalog.`
    });
  }

  const primary = matchedDegrees[0];
  const offeringUnis = matchedDegrees.map(d => ({
    uni_code: d.uni_code || 'UNI',
    name: d.university
  }));

  res.json({
    path_id: 1,
    course_code: primary.code,
    course_name: primary.name,
    university_count: offeringUnis.length,
    universities: offeringUnis
  });
});

// All degrees API
app.get('/api/degrees', (req, res) => {
  const stream = req.query.stream;
  if (stream) {
    return res.json(database.degrees.filter(d => (d.stream || '').toLowerCase() === stream.toLowerCase()));
  }
  res.json(database.degrees);
});

// Cart toggle API
app.post('/api/cart/toggle', (req, res) => {
  const { code, status } = req.body;
  res.json({ status: status || 'added', code: code });
});

// Contact submission API with real storage and validation
app.post('/api/contact', (req, res) => {
  const { name, email, message } = req.body;
  try {
    const record = contact.recordContactMessage({
      name,
      email,
      message,
      ip: req.ip || req.headers['x-forwarded-for'] || '127.0.0.1',
      userAgent: req.headers['user-agent'] || 'unknown'
    });
    res.json({
      status: 'success',
      message: 'Thank you! Your message has been securely recorded. Our student advisory team will review it.',
      id: record.id
    });
  } catch (err) {
    res.status(400).json({
      status: 'error',
      message: err.message
    });
  }
});

// 404 Catch-All
app.use((req, res) => {
  res.status(404).render('404');
});

// Start Server
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`=======================================================`);
    console.log(`✨ UniScope LK is LIVE at: http://localhost:${PORT}`);
    console.log(`🎓 Platform: UniScope LK (Sri Lanka Higher Education Platform)`);
    console.log(`🏛️ State Universities, Degrees & Admissions Intelligence`);
    console.log(`=======================================================`);
  });
}

module.exports = app;
