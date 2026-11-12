"""
UniScope LK — Production ZIP Archive Builder
Packages the modernized project into UniScope_LK_Modernized_Production.zip,
excluding node_modules and temporary/backup files.
"""
import os
import zipfile
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUTPUT_ZIP = os.path.join(ROOT_DIR, 'UniScope_LK_Modernized_Production.zip')

EXCLUDE_DIRS = {'node_modules', '.git', '__pycache__'}
EXCLUDE_EXTS = {'.backup.json', '.backup.js', '.tmp'}

def should_include(rel_path):
    parts = rel_path.replace('\\', '/').split('/')
    for p in parts:
        if p in EXCLUDE_DIRS:
            return False
    if rel_path.endswith('.zip'):
        return False
    for ext in EXCLUDE_EXTS:
        if rel_path.endswith(ext):
            return False
    return True

print(f"Creating production archive: {OUTPUT_ZIP}")
file_count = 0
total_size = 0

with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, ROOT_DIR)
            if should_include(rel_path):
                zf.write(full_path, rel_path)
                file_count += 1
                total_size += os.path.getsize(full_path)

zip_size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
print(f"Archive successfully created: {OUTPUT_ZIP}")
print(f"Files included: {file_count}")
print(f"Uncompressed size: {total_size / (1024 * 1024):.2f} MB")
print(f"Compressed archive size: {zip_size_mb:.2f} MB")
