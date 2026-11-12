import subprocess
import os
import tempfile
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PAGES = [
    ('home', 'http://localhost:3000/'),
    ('degrees', 'http://localhost:3000/degrees/all/'),
    ('detail', 'http://localhost:3000/degrees/detail/008/'),
    ('compare', 'http://localhost:3000/dashboard/compare/?d1=006A&d2=052C'),
    ('gpa', 'http://localhost:3000/gpa-calculator/'),
    ('cutoff', 'http://localhost:3000/degrees/cutoff-tool/?stream=Physical+Science&district=Colombo'),
    ('zscore', 'http://localhost:3000/zscore-calculator/?stream=Physical+Science&district=Colombo&zscore=1.85'),
    ('finder', 'http://localhost:3000/degree-finder/'),
    ('airisk', 'http://localhost:3000/ai-risk/'),
    ('district', 'http://localhost:3000/district-tool/'),
    ('login', 'http://localhost:3000/accounts/login/'),
    ('register', 'http://localhost:3000/accounts/register/'),
    ('page404', 'http://localhost:3000/non-existent-audit-route'),
    ('about', 'http://localhost:3000/about-us/')
]

SIZES = [
    ('desktop_1440', 1440, 900),
    ('tablet_1024', 1024, 768),
    ('mobile_390', 390, 844)
]

out_dir = os.path.abspath('audit_screenshots/post_audit')
os.makedirs(out_dir, exist_ok=True)
edge_exe = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

print(f"Capturing post-audit verification screenshots into {out_dir}...")
tmp = tempfile.mkdtemp()

success_count = 0
for page_name, url in PAGES:
    for size_name, w, h in SIZES:
        out_file = os.path.join(out_dir, f"{page_name}_{size_name}.png")
        cmd = [
            edge_exe,
            '--headless',
            f'--user-data-dir={tmp}',
            f'--window-size={w},{h}',
            f'--screenshot={out_file}',
            url
        ]
        try:
            subprocess.run(cmd, capture_output=True, timeout=15)
            if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
                print(f"  [OK] Captured {page_name}_{size_name}.png ({os.path.getsize(out_file):,} bytes)")
                success_count += 1
            else:
                print(f"  [FAIL] Empty or missing: {page_name}_{size_name}")
        except Exception as e:
            print(f"  [ERROR] on {page_name}_{size_name}: {e}")

total = len(PAGES) * len(SIZES)
print(f"\nVerification screenshot capture complete: {success_count}/{total} captured successfully!")
