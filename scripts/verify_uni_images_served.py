import urllib.request

IMAGES = [
    '/assets/universities/campuses/uom_campus.webp',
    '/assets/universities/campuses/gwuim_campus.webp',
    '/assets/universities/campuses/uvpa_campus.webp',
    '/assets/universities/campuses/svias_campus.webp',
    '/assets/universities/campuses/eusl_campus.webp',
    '/assets/universities/campuses/usj_campus.webp',
    '/assets/universities/campuses/rusl_campus.webp',
    '/assets/universities/campuses/seusl_campus.webp',
    '/assets/universities/campuses/uoj_campus.webp'
]

print("Checking HTTP serving for all 9 updated university campus photos:")
all_ok = True
for img_path in IMAGES:
    url = f"http://localhost:3000{img_path}"
    try:
        with urllib.request.urlopen(url) as resp:
            content = resp.read()
            print(f"  [HTTP {resp.status}] {img_path} ({len(content):,} bytes)")
    except Exception as e:
        print(f"  [ERROR] {img_path}: {e}")
        all_ok = False

if all_ok:
    print("\nAll 9 updated campus photos successfully serve over HTTP 200!")
else:
    print("\nSome images failed to serve.")
