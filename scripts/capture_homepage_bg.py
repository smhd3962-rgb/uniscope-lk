import subprocess
import os
import tempfile
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

out_dir = os.path.abspath('audit_screenshots/campus_background')
os.makedirs(out_dir, exist_ok=True)
edge_exe = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

TESTS = [
    ('homepage_desktop_1920', 'http://localhost:3000/', 1920, 1080),
    ('homepage_laptop_1440', 'http://localhost:3000/', 1440, 900),
    ('homepage_tablet_768', 'http://localhost:3000/', 768, 1024),
    ('homepage_mobile_390', 'http://localhost:3000/', 390, 844)
]

tmp = tempfile.mkdtemp()
print(f"Capturing homepage campus background audit screenshots...")

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
        else:
            print(f"  [FAIL] {name}.png missing or empty")
    except Exception as e:
        print(f"  [ERR] {name}: {e}")

print("Done.")
