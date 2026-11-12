import subprocess
import os
import tempfile
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

out_dir = os.path.abspath('audit_screenshots/campus_background')
os.makedirs(out_dir, exist_ok=True)
edge_exe = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

# In headless Edge, --screenshot with --window-size can capture different pages or full scroll height if we set height
HEIGHTS = [
    ('homepage_desktop_hero', 1440, 900),
    ('homepage_desktop_middle', 1440, 1800),
    ('homepage_desktop_fullflow', 1440, 3200)
]

tmp = tempfile.mkdtemp()
for name, w, h in HEIGHTS:
    out_file = os.path.join(out_dir, f"{name}.png")
    cmd = [
        edge_exe,
        '--headless=new',
        f'--user-data-dir={tmp}',
        f'--window-size={w},{h}',
        '--hide-scrollbars',
        f'--screenshot={out_file}',
        'http://localhost:3000/'
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=25)
        if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
            print(f"  [OK] Captured {name}.png ({os.path.getsize(out_file):,} bytes)")
    except Exception as e:
        print(f"  [ERR] {name}: {e}")

print("Scroll captures complete.")
