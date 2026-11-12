import subprocess
import os
import tempfile
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

out_dir = os.path.abspath('audit_screenshots/logo_and_framework')
os.makedirs(out_dir, exist_ok=True)
edge_exe = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

TESTS = [
    ('homepage_hero_logo', 'http://localhost:3000/', 1440, 800),
    ('homepage_framework_section', 'http://localhost:3000/', 1440, 1800),
    ('login_page_logo', 'http://localhost:3000/accounts/login/', 1200, 800),
    ('about_page_logo', 'http://localhost:3000/about-us/', 1200, 900)
]

tmp = tempfile.mkdtemp()
for name, url, w, h in TESTS:
    out_file = os.path.join(out_dir, f"{name}.png")
    cmd = [
        edge_exe,
        '--headless=new',
        f'--user-data-dir={tmp}',
        f'--window-size={w},{h}',
        '--hide-scrollbars',
        f'--screenshot={out_file}',
        url
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=20)
        if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
            print(f"  [OK] Captured {name}.png ({os.path.getsize(out_file):,} bytes)")
    except Exception as e:
        print(f"  [ERR] {name}: {e}")

print("Visual verification captures complete.")
