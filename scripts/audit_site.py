import glob
import re
import os

views = glob.glob('views/**/*.ejs', recursive=True)
print(f'Total views found: {len(views)}')

for v in sorted(views):
    with open(v, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    issues = []
    # Check for hardcoded fixed pixel widths >= 500px that aren't max-width
    for m in re.finditer(r'(?<!max-)(?<!min-)width\s*:\s*([5-9]\d{2}|[1-9]\d{3,})px', content):
        issues.append(f'Fixed width: {m.group(0)}')

    # Check for tables
    if '<table' in content:
        has_wrap = any(w in content for w in ['overflow', 'table-wrap', 'table-container', 'responsive', 'scroll'])
        if not has_wrap:
            issues.append('Table without visible scroll/responsive wrapper')

    # Check for empty links
    if 'href="#"' in content:
        issues.append('Contains empty href="#" links')

    # Check for missing alt tags on images
    for img in re.finditer(r'<img\s+[^>]*>', content):
        if 'alt=' not in img.group(0):
            issues.append(f'Image missing alt attribute: {img.group(0)[:50]}')

    # Check for inline dark-mode unfriendly styles (e.g. background:#fff, color:#000 without data-theme override)
    hardcoded_white_bg = len(re.findall(r'background:\s*#fff\b|background:\s*white\b', content))
    hardcoded_dark_text = len(re.findall(r'color:\s*#000000\b|color:\s*#000\b|color:\s*#0f172a\b|color:\s*#1e293b\b|color:\s*#111827\b|color:\s*#1a1a2e\b', content))

    if issues:
        print(f"\n[{v}] ({len(issues)} issues)")
        for iss in issues:
            print(f"  - {iss}")
    if hardcoded_white_bg > 3 or hardcoded_dark_text > 3:
        print(f"  * Warning: {v} has {hardcoded_white_bg} inline white backgrounds and {hardcoded_dark_text} inline dark text colors (risk in dark mode)")
