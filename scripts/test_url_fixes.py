import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

gazette_variants = [
    "http://www.documents.gov.lk/",
    "http://documents.gov.lk/",
    "http://www.documents.gov.lk/en/gazette.php",
    "http://documents.gov.lk/gazette.php",
    "https://www.documents.gov.lk/",
    "http://www.gazette.lk/"
]

print("Testing Gazette variants:")
for u in gazette_variants:
    try:
        req = urllib.request.Request(u, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5, context=ctx) as r:
            print(f"  [OK {r.status}] {u} -> {r.geturl()}")
    except Exception as e:
        print(f"  [ERR] {u} : {e}")

edupub_variants = [
    "http://www.edupub.gov.lk/",
    "http://edupub.gov.lk/",
    "http://www.edupub.gov.lk/BooksDownload.php",
    "http://www.edupub.gov.lk/Administrator/English/1.html"
]

print("\nTesting EduPub variants:")
for u in edupub_variants:
    try:
        req = urllib.request.Request(u, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5, context=ctx) as r:
            print(f"  [OK {r.status}] {u} -> {r.geturl()}")
    except Exception as e:
        print(f"  [ERR] {u} : {e}")
