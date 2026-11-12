import json
import os

with open('data/asset_registry.json', 'r', encoding='utf-8') as f:
    reg = json.load(f)

unis = reg.get('universities', {})
print(f"Asset Registry has {len(unis)} universities:")
for code, u in sorted(unis.items()):
    has_logo = 'logo' in u
    has_campus = 'campus' in u
    print(f"  {code:8} : {u.get('name')} [Logo: {has_logo}, Campus: {has_campus}]")
