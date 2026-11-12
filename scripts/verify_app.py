import urllib.request
import urllib.parse
import urllib.error
import json

tests = [
    ('/', 200, 'UniScope'),
    ('/degrees/detail/008/', 200, 'Faculty of Engineering'),
    ('/subject-combination/?sub1=129&sub2=124&sub3=125', 200, 'Physical Science Stream'),
    ('/api/course/008/', 200, 'Engineering'),
    ('/degrees/all/', 200, 'Explore All Sri Lankan University Degrees'),
    ('/degrees/cutoff-tool/?stream=Physical+Science&district=Colombo', 200, 'Cut-Off Records'),
    ('/zscore-calculator/?stream=Physical+Science&district=Colombo&zscore=1.85', 200, 'High Probability'),
    ('/district-tool/', 200, 'UGC District Determination'),
    ('/gpa-calculator/', 200, 'GPA'),
    ('/degree-finder/', 200, 'Smart Degree Finder'),
    ('/ai-risk/', 200, 'AI Displacement Risk Checker'),
    ('/universities/', 200, 'University of Jaffna'),
    ('/career-paths/', 200, 'Electrical'),
    ('/about-us/', 200, 'Empowering Sri Lankan Higher Education'),
    ('/faq/', 200, 'Frequently Asked Questions'),
    ('/contact-us/', 200, 'Direct Channels'),
    ('/dashboard/compare/', 200, 'Comparison Facet (17-Sections)'),
    ('/accounts/login/', 200, 'Welcome Back'),
    ('/accounts/register/', 200, 'Create Free Account'),
    ('/student-services/', 200, 'Student Services &amp; Official Resources'),
    ('/api/student-services', 200, '"services":'),
    ('/student-tools/application-checklist/', 200, 'University Application Checklist'),
    ('/student-tools/cost-planner/', 200, 'University Cost-of-Living Planner'),
    ('/student-tools/degree-recognition/', 200, 'Degree Recognition &amp; Accreditation Guide'),
    ('/api/degree-recognition', 200, '"records":')
]

passed = 0
for path, code, expect in tests:
    url = f'http://localhost:3000{path}'
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            content = resp.read().decode('utf-8')
            if resp.status == code and expect in content:
                print(f'PASS: {path}')
                passed += 1
            else:
                print(f'FAIL content: {path} (expected "{expect}")')
    except Exception as e:
        print(f'FAIL exception: {path} -> {e}')

# 404 Route Test
try:
    urllib.request.urlopen('http://localhost:3000/non-existent-route-audit-test', timeout=5)
    print('FAIL: Expected 404 for unknown route')
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8')
    if e.code == 404 and 'Degree or Page Not Found' in body and 'UniScope LK' in body:
        print('PASS: Dedicated 404 Catch-All Page & Attribution')
        passed += 1
    else:
        print(f'FAIL: 404 page content check (code={e.code})')

# 404 Invalid Degree Code Test
try:
    urllib.request.urlopen('http://localhost:3000/degrees/detail/INVALID999/', timeout=5)
    print('FAIL: Expected 404 for non-existent degree code')
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8')
    if e.code == 404 and 'Degree or Page Not Found' in body:
        print('PASS: Dedicated 404 on Invalid Degree Lookup')
        passed += 1
    else:
        print(f'FAIL: Invalid degree 404 (code={e.code})')

# Empty Login Validation Test
try:
    data = urllib.parse.urlencode({'email': '', 'password': ''}).encode('utf-8')
    req = urllib.request.Request('http://localhost:3000/accounts/login/', data=data, method='POST')
    urllib.request.urlopen(req, timeout=5)
    print('FAIL: Expected 400 for empty login')
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8')
    if e.code == 400 and 'Please provide both email and password' in body:
        print('PASS: Login Input Validation (400 Bad Request)')
        passed += 1
    else:
        print(f'FAIL: Login validation (code={e.code})')

# Empty Register Validation Test
try:
    data = urllib.parse.urlencode({'name': '', 'email': '', 'password': ''}).encode('utf-8')
    req = urllib.request.Request('http://localhost:3000/accounts/register/', data=data, method='POST')
    urllib.request.urlopen(req, timeout=5)
    print('FAIL: Expected 400 for empty register')
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8')
    if e.code == 400 and 'Name, email, and password are required' in body:
        print('PASS: Register Input Validation (400 Bad Request)')
        passed += 1
    else:
        print(f'FAIL: Register validation (code={e.code})')

total_tests = len(tests) + 4
print(f'\nFULL TEST SUITE RESULTS: {passed}/{total_tests} passed successfully!')
