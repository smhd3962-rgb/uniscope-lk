import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')

campus_files = [
    ('UOC', 'File:Department of Mathematics UoC.jpg', 'commons'),
    ('UOP', 'File:Campus lion UoP.jpg', 'commons'),
    ('USJ', 'File:University of Sri Jayewardenepura Science Faculty.JPG', 'commons'),
    ('UOK', 'File:University of Kelaniya.jpg', 'commons'),
    ('UOJ', 'File:University of Jaffna.jpg', 'commons'),
    ('UOR', 'File:Ruhuna University air view.jpg', 'commons'),
    ('EUSL', 'File:Faculty of Health-Care Sciences, Eastern University, Batticaloa..JPG', 'commons'),
    ('SEUSL', 'File:South Eastern University Sri Lanka 2.jpg', 'commons'),
    ('RUSL', 'File:Library, Rajarata Unviersity of Sri Lanka.jpg', 'commons'),
    ('SUSL', 'File:UG-LK Photowalk - 2018-03-25 - Sabaragamuwa University (1).jpg', 'commons'),
    ('WUSL', 'File:WUSL010.jpg', 'commons'),
    ('UWU', 'File:Uva Wellassa university.jpg', 'commons'),
    ('OUSL', 'File:Open University of Sri Lanka.jpg', 'commons'),
    ('OCUSL', 'File:Entrance of Ocean University.jpg', 'commons'),
    ('SP-UOC', 'File:Sri Palee Campus - Layan House.jpg', 'commons'),
    ('VAV', 'File:Vavuniya campus.jpg', 'commons')
]

for code, title, wiki in campus_files:
    endpoint = 'commons.wikimedia.org' if wiki == 'commons' else 'en.wikipedia.org'
    url = f'https://{endpoint}/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url|size|mime|extmetadata&format=json'
    req = urllib.request.Request(url, headers={'User-Agent': 'UniScopeLK-AssetBot/1.0 (educational; farhan@eng.jfn.ac.lk)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for pid, pdata in pages.items():
                if int(pid) < 0:
                    print(f'{code} NOT FOUND: {title}')
                else:
                    info = pdata.get('imageinfo', [{}])[0]
                    meta = info.get('extmetadata', {})
                    artist = meta.get('Artist', {}).get('value', 'Unknown')
                    license_short = meta.get('LicenseShortName', {}).get('value', 'Unknown')
                    print(f'{code}: {info.get("url")} | {artist} | {license_short}')
    except Exception as e:
        print(f'{code} Error: {e}')
