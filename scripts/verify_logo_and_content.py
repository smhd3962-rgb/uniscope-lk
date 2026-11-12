import urllib.request

html = urllib.request.urlopen('http://localhost:3000/').read().decode('utf-8')
print('Status: 200 OK')
print('Official emblem in navbar:', 'uniscope_logo_mark.png' in html)
print('Decision Framework present:', 'A Complete Decision Framework for University Admissions' in html)
print('40% Merit Intake present:', 'All-Island Merit Intake' in html)
print('Old Why UniScope removed:', 'Why UniScope LK?' not in html)
print('Old Join 100% Free removed:', "Join UniScope LK – It's 100% Free" not in html)
print('Stream quick navigation strip present:', 'Physical Science (60+)' in html)

# Also check login and register
login_html = urllib.request.urlopen('http://localhost:3000/accounts/login/').read().decode('utf-8')
print('Login has official logo:', 'uniscope_logo_full.png' in login_html)

register_html = urllib.request.urlopen('http://localhost:3000/accounts/register/').read().decode('utf-8')
print('Register has official logo:', 'uniscope_logo_full.png' in register_html)

about_html = urllib.request.urlopen('http://localhost:3000/about-us/').read().decode('utf-8')
print('About has official logo:', 'uniscope_logo_full.png' in about_html)
