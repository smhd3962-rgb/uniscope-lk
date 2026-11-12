import subprocess
import os
import tempfile
import time

PAGES = [
    ('home', 'http://localhost:3000/'),
    ('degrees', 'http://localhost:3000/degrees/all/'),
    ('detail', 'http://localhost:3000/degrees/detail/008/'),
    ('compare', 'http://localhost:3000/dashboard/compare/'),
    ('gpa', 'http://localhost:3000/gpa-calculator/'),
    ('cutoff', 'http://localhost:3000/degrees/cutoff-tool/'),
    ('subcombo', 'http://localhost:3000/subject-combination/?sub1=129&sub2=124&sub3=125'),
    ('login', 'http://localhost:3000/accounts/login/'),
]

SIZES = [
    ('desktop_1440', 1440, 900),
    ('mobile_390', 390, 844),
]

out_dir = os.path.abspath('audit_screenshots')
os.makedirs(out_dir, exist_ok=True)
edge_exe = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

print(f"Capturing screenshots into {out_dir}...")
tmp = tempfile.mkdtemp()

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
        subprocess.run(cmd, capture_output=True, timeout=15)
        if os.path.exists(out_file):
            print(f"Captured {page_name}_{size_name}.png ({os.path.getsize(out_file)} bytes)")
        else:
            print(f"FAILED {page_name}_{size_name}")

print("Done capturing baseline screenshots.")
