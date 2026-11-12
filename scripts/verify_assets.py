import json
import os
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Starting UniScope LK Asset Verification Suite...")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')

# 1. Load Registry
reg_path = os.path.join(DATA_DIR, 'asset_registry.json')
if not os.path.exists(reg_path):
    print("FAIL: asset_registry.json not found!")
    sys.exit(1)

with open(reg_path, 'r', encoding='utf-8') as f:
    reg = json.load(f)

print(f"[OK] asset_registry.json loaded (Generated: {reg.get('generated_at')})")

# 2. Check Database Universities
db_path = os.path.join(DATA_DIR, 'database.json')
with open(db_path, 'r', encoding='utf-8') as f:
    db = json.load(f)

passed = 0
failed = 0

print("\n--- Verifying University Logo Assets ---")
for code, udata in reg.get('universities', {}).items():
    if 'logo' in udata:
        logo_rel = udata['logo']['path'].lstrip('/')
        disk_path = os.path.join(PUBLIC_DIR, logo_rel)
        if os.path.exists(disk_path) and os.path.getsize(disk_path) > 500:
            passed += 1
        else:
            print(f"FAIL: Missing or empty logo file: {disk_path}")
            failed += 1

print(f"[OK] Verified {passed} university logo files on disk.")

print("\n--- Verifying Real Campus Photography ---")
campus_count = 0
for code, udata in reg.get('universities', {}).items():
    if 'campus' in udata:
        campus_rel = udata['campus']['path'].lstrip('/')
        disk_path = os.path.join(PUBLIC_DIR, campus_rel)
        if os.path.exists(disk_path) and os.path.getsize(disk_path) > 1000:
            campus_count += 1
        else:
            print(f"FAIL: Missing or empty campus photo: {disk_path}")
            failed += 1

print(f"[OK] Verified {campus_count} real campus photography files on disk.")

print("\n--- Verifying Degree Category Visuals ---")
cat_count = 0
for cat_id, cat_data in reg.get('degree_categories', {}).items():
    cat_rel = cat_data['path'].lstrip('/')
    disk_path = os.path.join(PUBLIC_DIR, cat_rel)
    if os.path.exists(disk_path) and os.path.getsize(disk_path) > 1000:
        cat_count += 1
    else:
        print(f"FAIL: Missing or empty category image: {disk_path}")
        failed += 1

print(f"[OK] Verified {cat_count} degree category photographic assets on disk.")

print("\n--- Verifying Apple-Style Placeholders ---")
ph_count = 0
for ph_id, ph_data in reg.get('placeholders', {}).items():
    ph_rel = ph_data['path'].lstrip('/')
    disk_path = os.path.join(PUBLIC_DIR, ph_rel)
    if os.path.exists(disk_path) and os.path.getsize(disk_path) > 100:
        ph_count += 1
    else:
        print(f"FAIL: Missing placeholder: {disk_path}")
        failed += 1

print(f"[OK] Verified {ph_count} placeholder assets on disk.")

print("\n--- Testing HTTP Endpoints on Live Server (http://localhost:3000) ---")
test_urls = [
    '/assets/universities/logos/uoc.png',
    '/assets/universities/logos/uop.png',
    '/assets/universities/logos/uom.png',
    '/assets/universities/logos/usj.png',
    '/assets/universities/logos/uok.png',
    '/assets/universities/logos/uoj.png',
    '/assets/universities/campuses/uoc_campus.webp',
    '/assets/universities/campuses/uop_campus.webp',
    '/assets/universities/campuses/uoj_campus.webp',
    '/assets/universities/campuses/usj_campus.webp',
    '/assets/degrees/engineering.webp',
    '/assets/degrees/medicine.webp',
    '/assets/degrees/computing.webp',
    '/assets/degrees/business.webp',
    '/assets/degrees/science.webp',
    '/assets/degrees/agriculture.webp',
    '/assets/placeholders/university_logo_placeholder.svg',
    '/assets/placeholders/campus_placeholder.webp'
]

http_ok = 0
for path in test_urls:
    url = f"http://localhost:3000{path}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            if resp.status == 200:
                http_ok += 1
            else:
                print(f"FAIL: {path} returned status {resp.status}")
                failed += 1
    except Exception as e:
        print(f"FAIL: {path} -> {e}")
        failed += 1

print(f"[OK] {http_ok}/{len(test_urls)} asset endpoints verified 200 OK.")

if failed == 0:
    print("\n🎉 ALL VISUAL ASSETS VERIFIED WITH 100% SUCCESS!")
else:
    print(f"\nAsset verification finished with {failed} failures.")
    sys.exit(1)
