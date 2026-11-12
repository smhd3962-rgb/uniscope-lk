import subprocess
import os
import tempfile
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

out_dir = os.path.abspath('audit_screenshots/visual_assets')
os.makedirs(out_dir, exist_ok=True)
edge_exe = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

TESTS = [
    ('universities_grid_top', 'http://localhost:3000/universities/', 1440, 1100),
    ('universities_grid_full', 'http://localhost:3000/universities/', 1440, 2400),
    ('homepage_unis_showcase', 'http://localhost:3000/', 1440, 1400)
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
        subprocess.run(cmd, capture_output=True, timeout=25)
        if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
            print(f"  [OK] Captured {name}.png ({os.path.getsize(out_file):,} bytes)")
    except Exception as e:
        print(f"  [ERR] {name}: {e}")

print("Visual verification screenshots captured.")
