import json

with open('data/database.json', encoding='utf-8') as f:
    db = json.load(f)

for k, v in db.get('universities', {}).items():
    print(f"{v.get('code'):8} : {k}")
