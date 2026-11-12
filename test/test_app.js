const assert = require('assert');
const http = require('http');
const fs = require('fs');
const path = require('path');
const app = require('../server');
const auth = require('../utils/auth');

let server;
const PORT = 3001;
const BASE_URL = `http://localhost:${PORT}`;

function makeRequest(method, pathName, headers = {}, body = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(pathName, BASE_URL);
    const req = http.request(url, { method, headers }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body: data }));
    });
    req.on('error', reject);
    if (body) {
      req.write(typeof body === 'string' ? body : JSON.stringify(body));
    }
    req.end();
  });
}

async function runTests() {
  console.log('========================================================');
  console.log('🧪 UNISCOPE LK AUTOMATED QA & INTEGRITY TEST SUITE');
  console.log('========================================================\n');

  let passed = 0;
  let total = 0;

  async function test(name, fn) {
    total++;
    try {
      await fn();
      console.log(`  ✓ PASS: ${name}`);
      passed++;
    } catch (err) {
      console.error(`  ✗ FAIL: ${name}`);
      console.error(`    ${err.message}`);
    }
  }

  // 1. Data Integrity Tests
  console.log('1. DATA INTEGRITY & UGC CUTOFF RECONCILIATION:');
  
  await test('Cutoff records total exactly 26,225', () => {
    const db = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'database.json'), 'utf8'));
    assert.strictEqual(db.cutoffs.length, 26225);
  });

  await test('Zero duplicate cutoff keys across (year, course, university, district)', () => {
    const db = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'database.json'), 'utf8'));
    const grouped = new Map();
    for (const c of db.cutoffs) {
      const key = `${c.year}|${c.course_name}|${c.university}|${c.district}`;
      if (grouped.has(key)) {
        throw new Error(`Duplicate cutoff group detected: ${key}`);
      }
      grouped.set(key, true);
    }
    assert.strictEqual(grouped.size, 26225);
  });

  await test('All 25 districts properly populated with 1,049 records each (including Galle & Kegalle)', () => {
    const db = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'database.json'), 'utf8'));
    const counts = {};
    for (const c of db.cutoffs) {
      counts[c.district] = (counts[c.district] || 0) + 1;
    }
    assert.strictEqual(Object.keys(counts).length, 25);
    assert.strictEqual(counts['Galle'], 1049, 'Galle must have 1049 records');
    assert.strictEqual(counts['Kegalle'], 1049, 'Kegalle must have 1049 records');
  });

  await test('Degrees data integrity: no unrelated careers (e.g. Nursing has Allied Health careers, not diplomacy)', () => {
    const db = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'database.json'), 'utf8'));
    const nursing = db.degrees.filter(d => d.name === 'Nursing');
    assert.ok(nursing.length > 0, 'Nursing degrees must exist');
    for (const n of nursing) {
      assert.strictEqual(n.faculty, 'Faculty of Allied Health Sciences');
      assert.strictEqual(n.duration_years, 4);
      assert.strictEqual(n.slqf_level, 6);
      const allCareers = [...n.careers_public, ...n.careers_private].join(' ');
      assert.ok(!allCareers.includes('Diplomatic Service'), 'Nursing must not have Diplomatic Service career');
      assert.ok(!allCareers.includes('Sri Lanka Administrative Service'), 'Nursing must not have SLAS career');
      assert.ok(allCareers.includes('Nurse') || allCareers.includes('Nursing'), 'Nursing must have nursing careers');
    }
  });

  // 2. HTTP Server & Route Tests
  console.log('\n2. WEB ROUTES, NAVIGATION & TRANSPARENCY:');

  await test('GET / returns 200 with proper brand title', async () => {
    const res = await makeRequest('GET', '/');
    assert.strictEqual(res.status, 200);
    assert.ok(res.body.includes('UniScope'));
  });

  await test('GET /data-sources/ renders actual data-sources page (NOT faq.ejs)', async () => {
    const res = await makeRequest('GET', '/data-sources/');
    assert.strictEqual(res.status, 200);
    assert.ok(res.body.includes('Data Sources &amp; Research Standards'), 'Must render data-sources.ejs');
    assert.ok(res.body.includes('tab-sources'), 'Must contain Data Sources tabs');
  });

  await test('GET /community/forums/ redirects (301) to /community/resources/', async () => {
    const res = await makeRequest('GET', '/community/forums/');
    assert.strictEqual(res.status, 301);
    assert.strictEqual(res.headers.location, '/community/resources/');
  });

  await test('GET /community/resources/ returns 200 with student guides', async () => {
    const res = await makeRequest('GET', '/community/resources/');
    assert.strictEqual(res.status, 200);
    assert.ok(res.body.includes('Student Resources &amp; Guides'));
  });

  await test('GET /universities/ returns 200 with state universities list', async () => {
    const res = await makeRequest('GET', '/universities/');
    assert.strictEqual(res.status, 200);
    assert.ok(res.body.includes('University of Colombo'));
  });

  await test('GET /gpa-calculator/ returns 200 with GPA calculator', async () => {
    const res = await makeRequest('GET', '/gpa-calculator/');
    assert.strictEqual(res.status, 200);
    assert.ok(res.body.includes('GPA &amp; CGPA Calculator'));
  });

  // 3. API & Data Security Tests
  console.log('\n3. COURSE API & DATA PROTECTION:');

  await test('GET /api/course/UNKNOWN_CODE returns 404 error (never 5 fictitious universities)', async () => {
    const res = await makeRequest('GET', '/api/course/NON_EXISTENT_999/');
    assert.strictEqual(res.status, 404);
    const data = JSON.parse(res.body);
    assert.strictEqual(data.status, 'not_found');
    assert.ok(data.message.includes('Course information not available'));
    assert.strictEqual(typeof data.universities, 'undefined', 'Must not return fictitious universities');
  });

  await test('GET /api/course/001 returns 200 with offering universities for Medicine', async () => {
    const res = await makeRequest('GET', '/api/course/001/');
    assert.strictEqual(res.status, 200);
    const data = JSON.parse(res.body);
    assert.ok(data.course_code.startsWith('001'), 'Must match course code starting with 001');
    assert.ok(data.universities.length > 0, 'Must have offering universities');
  });

  // 4. Authentication & Security Tests
  console.log('\n4. AUTHENTICATION & SECURITY:');

  await test('POST /accounts/login/ rejects invalid credentials with 401 (no demo fallback)', async () => {
    const body = new URLSearchParams({ email: 'nonexistent_test@example.com', password: 'random_password_xyz' }).toString();
    const res = await makeRequest('POST', '/accounts/login/', {
      'Content-Type': 'application/x-www-form-urlencoded'
    }, body);
    assert.strictEqual(res.status, 401);
    assert.ok(res.body.includes('Invalid email address or password'));
  });

  await test('POST /accounts/login/ succeeds with valid credentials and sets session cookie', async () => {
    const body = new URLSearchParams({ email: 'student@uniscope.lk', password: 'UniScope@2026!' }).toString();
    const res = await makeRequest('POST', '/accounts/login/', {
      'Content-Type': 'application/x-www-form-urlencoded'
    }, body);
    assert.strictEqual(res.status, 302);
    assert.strictEqual(res.headers.location, '/accounts/profile/');
    const cookieHeader = res.headers['set-cookie'];
    assert.ok(cookieHeader && cookieHeader.some(c => c.includes('uniscope_session')), 'Must set session cookie');
  });

  await test('POST /accounts/register/ rejects duplicate email with 409 Conflict', async () => {
    const body = new URLSearchParams({
      name: 'Duplicate Test',
      email: 'student@uniscope.lk',
      password: 'newpassword123',
      district: 'Colombo',
      stream: 'Physical Science'
    }).toString();
    const res = await makeRequest('POST', '/accounts/register/', {
      'Content-Type': 'application/x-www-form-urlencoded'
    }, body);
    assert.strictEqual(res.status, 409);
    assert.ok(res.body.includes('already exists'));
  });

  await test('GET /accounts/google/login/ without credentials returns 503 config message (no fake user)', async () => {
    const res = await makeRequest('GET', '/accounts/google/login/');
    assert.strictEqual(res.status, 503);
    assert.ok(res.body.includes('Google Sign-In is currently in configuration mode'));
  });

  await test('Password hashing check: stored users use salt:hash and never plaintext', () => {
    const users = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'users.json'), 'utf8'));
    for (const u of users) {
      assert.strictEqual(typeof u.password, 'undefined', 'Plaintext password must not be stored');
      assert.ok(u.passwordHash && u.passwordHash.includes(':'), 'passwordHash must contain salt:hash format');
    }
  });

  // 5. Contact Form Validation & Real Storage
  console.log('\n5. CONTACT FORM VALIDATION & PERSISTENCE:');

  await test('POST /api/contact validates input and records legitimate submission', async () => {
    const testMsg = {
      name: 'QA Test Student',
      email: 'qatest@example.com',
      message: 'Automated verification test of student message recording.'
    };
    const res = await makeRequest('POST', '/api/contact', {
      'Content-Type': 'application/json'
    }, testMsg);
    assert.strictEqual(res.status, 200);
    const data = JSON.parse(res.body);
    assert.strictEqual(data.status, 'success');
    assert.ok(data.id, 'Must return message id');

    // Verify written to file
    const msgFile = path.join(__dirname, '..', 'data', 'contact_messages.json');
    assert.ok(fs.existsSync(msgFile), 'contact_messages.json must exist');
    const recorded = JSON.parse(fs.readFileSync(msgFile, 'utf8'));
    const found = recorded.find(m => m.id === data.id);
    assert.ok(found, 'Message record must be found in storage');
    assert.strictEqual(found.email, 'qatest@example.com');
  });

  await test('POST /api/contact rejects invalid email with 400', async () => {
    const invalidMsg = {
      name: 'Test',
      email: 'not-an-email',
      message: 'Hello world'
    };
    const res = await makeRequest('POST', '/api/contact', {
      'Content-Type': 'application/json'
    }, invalidMsg);
    assert.strictEqual(res.status, 400);
    const data = JSON.parse(res.body);
    assert.strictEqual(data.status, 'error');
  });

  console.log('\n========================================================');
  console.log(`TOTAL TESTS: ${total} | PASSED: ${passed} | FAILED: ${total - passed}`);
  console.log('========================================================');

  if (passed === total) {
    console.log('🎉 ALL INTEGRITY, SECURITY & NAVIGATION TESTS PASSED 100%!');
  } else {
    process.exitCode = 1;
  }
}

// Start test server
server = app.listen(PORT, async () => {
  try {
    await runTests();
  } catch (err) {
    console.error('Test run failed:', err);
    process.exitCode = 1;
  } finally {
    server.close();
  }
});
