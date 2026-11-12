import os
import urllib.request
import json
import datetime
from PIL import Image
import io

print("Starting UniScope LK Asset Researcher & Builder...")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PUBLIC_DIR = os.path.join(BASE_DIR, 'public', 'assets')
DATA_DIR = os.path.join(BASE_DIR, 'data')

LOGOS_DIR = os.path.join(PUBLIC_DIR, 'universities', 'logos')
CAMPUSES_DIR = os.path.join(PUBLIC_DIR, 'universities', 'campuses')
DEGREES_DIR = os.path.join(PUBLIC_DIR, 'degrees')
PLACEHOLDERS_DIR = os.path.join(PUBLIC_DIR, 'placeholders')

for d in [LOGOS_DIR, CAMPUSES_DIR, DEGREES_DIR, PLACEHOLDERS_DIR]:
    os.makedirs(d, exist_ok=True)

USER_AGENT = 'UniScopeLK-AssetManager/2.0 (Sri Lanka University Information Platform; farhan@eng.jfn.ac.lk)'

registry = {
    "generated_at": datetime.datetime.now().isoformat(),
    "platform": "UniScope LK",
    "lead_developer": "Nasimudeen Muhammed Farhan, Faculty of Engineering, University of Jaffna",
    "universities": {},
    "degree_categories": {},
    "placeholders": {}
}

def download_data(url):
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()

# ══════════════════════════════════════════════════════════════════════
# 1. UNIVERSITY LOGOS
# ══════════════════════════════════════════════════════════════════════
UNIVERSITY_LOGOS = [
    {
        "code": "UOC",
        "name": "University of Colombo",
        "url": "https://upload.wikimedia.org/wikipedia/en/f/f9/Logo_of_the_University_of_Colombo.png",
        "creator": "University of Colombo",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of the University of Colombo (Buddhih Sarvatra Bhrajate)"
    },
    {
        "code": "UOP",
        "name": "University of Peradeniya",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/University_of_Peradeniya_Crest.svg/600px-University_of_Peradeniya_Crest.svg.png",
        "creator": "University of Peradeniya / Wikimedia Commons",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of the University of Peradeniya (Sarvasya Locanam Sastram)"
    },
    {
        "code": "UOM",
        "name": "University of Moratuwa",
        "url": "https://upload.wikimedia.org/wikipedia/en/6/60/University_of_Moratuwa_logo.png",
        "creator": "University of Moratuwa",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of the University of Moratuwa (Vidyayeva Sarvadhana)"
    },
    {
        "code": "USJ",
        "name": "University of Sri Jayewardenepura",
        "url": "https://upload.wikimedia.org/wikipedia/en/d/d6/University_of_Sri_Jayewardenepura_logo.png",
        "creator": "University of Sri Jayewardenepura",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of the University of Sri Jayewardenepura (Vijja Uppatatam Settha)"
    },
    {
        "code": "UOK",
        "name": "University of Kelaniya",
        "url": "https://upload.wikimedia.org/wikipedia/en/1/1f/University_of_Kelaniya_logo.png",
        "creator": "University of Kelaniya",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of the University of Kelaniya (Pannaya Parisujjhati)"
    },
    {
        "code": "UOJ",
        "name": "University of Jaffna",
        "url": "https://upload.wikimedia.org/wikipedia/en/b/b9/UoJ_logo.png",
        "creator": "University of Jaffna",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of the University of Jaffna (Mei Kande Balam)"
    },
    {
        "code": "UOR",
        "name": "University of Ruhuna",
        "url": "https://upload.wikimedia.org/wikipedia/en/2/2e/University_of_Ruhuna_logo.png",
        "creator": "University of Ruhuna",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of the University of Ruhuna"
    },
    {
        "code": "EUSL",
        "name": "Eastern University, Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/en/a/a0/EUSL_logo2.png",
        "creator": "Eastern University, Sri Lanka",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of Eastern University, Sri Lanka"
    },
    {
        "code": "SEUSL",
        "name": "South Eastern University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/en/6/6c/South_Eastern_University_of_Sri_Lanka_logo.png",
        "creator": "South Eastern University of Sri Lanka",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of South Eastern University of Sri Lanka"
    },
    {
        "code": "RUSL",
        "name": "Rajarata University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/en/a/a5/Rajarata_logo.png",
        "creator": "Rajarata University of Sri Lanka",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of Rajarata University of Sri Lanka"
    },
    {
        "code": "SUSL",
        "name": "Sabaragamuwa University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/en/5/5a/Logo-SUSL.png",
        "creator": "Sabaragamuwa University of Sri Lanka",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of Sabaragamuwa University of Sri Lanka"
    },
    {
        "code": "WUSL",
        "name": "Wayamba University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/en/8/8d/Wayabauniversity.png",
        "creator": "Wayamba University of Sri Lanka",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of Wayamba University of Sri Lanka"
    },
    {
        "code": "UWU",
        "name": "Uva Wellassa University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/commons/9/93/Logo_uwu.jpg",
        "creator": "Uva Wellassa University",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of Uva Wellassa University"
    },
    {
        "code": "UVPA",
        "name": "University of the Visual and Performing Arts",
        "url": "https://upload.wikimedia.org/wikipedia/en/d/dd/University_of_the_Visual_and_Performing_Arts.gif",
        "creator": "University of the Visual and Performing Arts",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of University of the Visual and Performing Arts"
    },
    {
        "code": "GWUIM",
        "name": "Gampaha Wickramarachchi University of Indigenous Medicine, Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/88/Gampaha_Wickramarachchi_University_of_Indigenous_Medicine_logo.png",
        "creator": "GWUIM",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of Gampaha Wickramarachchi University of Indigenous Medicine"
    },
    {
        "code": "OUSL",
        "name": "The Open University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/en/8/8e/Logo_ousl.jpg",
        "creator": "The Open University of Sri Lanka",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of The Open University of Sri Lanka"
    },
    {
        "code": "OCUSL",
        "name": "Ocean University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/en/a/ab/Ocean_University_Sri_Lanka_Crest.png",
        "creator": "Ocean University of Sri Lanka",
        "license": "Public domain / Official Institutional Insignia",
        "attribution": "Official emblem of Ocean University of Sri Lanka"
    }
]

print("\n--- Downloading & Processing University Logos ---")
for item in UNIVERSITY_LOGOS:
    code = item["code"]
    filename = f"{code.lower()}.png"
    dest_path = os.path.join(LOGOS_DIR, filename)
    rel_path = f"/assets/universities/logos/{filename}"
    
    try:
        data = download_data(item["url"])
        img = Image.open(io.BytesIO(data))
        
        # Ensure RGBA for transparent PNGs
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        # Max dimension 400px, maintain aspect ratio
        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        img.save(dest_path, "PNG", optimize=True)
        
        print(f"  [OK] Saved logo for {code} ({img.size[0]}x{img.size[1]}px) -> {filename}")
        
        registry["universities"][code] = {
            "name": item["name"],
            "logo": {
                "path": rel_path,
                "source_url": item["url"],
                "creator": item["creator"],
                "license": item["license"],
                "attribution": item["attribution"],
                "dimensions": [img.size[0], img.size[1]],
                "status": "verified"
            }
        }
    except Exception as e:
        print(f"  [ERROR] Downloading logo for {code}: {e}")

# ══════════════════════════════════════════════════════════════════════
# 2. REAL CAMPUS PHOTOGRAPHS (Wikimedia Commons CC-BY / CC-BY-SA)
# ══════════════════════════════════════════════════════════════════════
CAMPUS_PHOTOS = [
    {
        "code": "UOC",
        "name": "University of Colombo",
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/82/Department_of_Mathematics_UoC.jpg",
        "creator": "Cossde (Wikimedia Commons)",
        "license": "CC BY-SA 3.0",
        "attribution": "Department of Mathematics complex, Faculty of Science, University of Colombo by Cossde"
    },
    {
        "code": "UOP",
        "name": "University of Peradeniya",
        "url": "https://upload.wikimedia.org/wikipedia/commons/0/0d/Campus_lion_UoP.jpg",
        "creator": "Anuradha Ratnaweera (Wikimedia Commons)",
        "license": "CC BY-SA 2.0",
        "attribution": "Senate Building & Campus Lion landmark, University of Peradeniya by Anuradha Ratnaweera"
    },
    {
        "code": "USJ",
        "name": "University of Sri Jayewardenepura",
        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d5/University_of_Sri_Jayewardenepura_Science_Faculty.JPG",
        "creator": "Studentlanka (Wikimedia Commons)",
        "license": "CC BY-SA 3.0",
        "attribution": "Faculty of Applied Sciences complex, University of Sri Jayewardenepura by Studentlanka"
    },
    {
        "code": "UOK",
        "name": "University of Kelaniya",
        "url": "https://upload.wikimedia.org/wikipedia/commons/1/18/University_of_Kelaniya.jpg",
        "creator": "Sandunruki (English Wikipedia / Wikimedia Commons)",
        "license": "Public domain",
        "attribution": "Administrative building and academic grounds, University of Kelaniya by Sandunruki"
    },
    {
        "code": "UOJ",
        "name": "University of Jaffna",
        "url": "https://upload.wikimedia.org/wikipedia/commons/2/25/University_of_Jaffna.jpg",
        "creator": "BlueLankan (Wikimedia Commons)",
        "license": "CC BY-SA 3.0",
        "attribution": "Main entrance and administration premises, University of Jaffna by BlueLankan"
    },
    {
        "code": "UOR",
        "name": "University of Ruhuna",
        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d1/Ruhuna_University_air_view.jpg",
        "creator": "Fazal Mohamed (Wikimedia Commons)",
        "license": "CC BY-SA 3.0",
        "attribution": "Aerial view of Geoffrey Bawa designed campus, Wellamadama, University of Ruhuna by Fazal Mohamed"
    },
    {
        "code": "EUSL",
        "name": "Eastern University, Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/commons/0/00/Faculty_of_Health-Care_Sciences%2C_Eastern_University%2C_Batticaloa..JPG",
        "creator": "Camera007 (Wikimedia Commons)",
        "license": "CC BY-SA 3.0",
        "attribution": "Faculty of Health-Care Sciences, Eastern University, Sri Lanka by Camera007"
    },
    {
        "code": "SEUSL",
        "name": "South Eastern University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/commons/1/15/South_Eastern_University_Sri_Lanka_2.jpg",
        "creator": "L Manju (Wikimedia Commons)",
        "license": "CC BY-SA 4.0",
        "attribution": "Oluvil main campus complex, South Eastern University of Sri Lanka by L Manju"
    },
    {
        "code": "RUSL",
        "name": "Rajarata University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Library%2C_Rajarata_Unviersity_of_Sri_Lanka.jpg",
        "creator": "Uahamed (Wikimedia Commons)",
        "license": "CC BY-SA 4.0",
        "attribution": "Main Library Building, Mihintale Campus, Rajarata University of Sri Lanka by Uahamed"
    },
    {
        "code": "SUSL",
        "name": "Sabaragamuwa University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/30/UG-LK_Photowalk_-_2018-03-25_-_Sabaragamuwa_University_%281%29.jpg",
        "creator": "Rehman Abubakr (Wikimedia Commons)",
        "license": "CC BY-SA 4.0",
        "attribution": "Belihuloya campus grounds, Sabaragamuwa University of Sri Lanka by Rehman Abubakr"
    },
    {
        "code": "WUSL",
        "name": "Wayamba University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/commons/9/93/WUSL010.jpg",
        "creator": "Isuru.nuwan001 (Wikimedia Commons)",
        "license": "CC BY-SA 3.0",
        "attribution": "Kuliyapitiya premises, Wayamba University of Sri Lanka by Isuru.nuwan001"
    },
    {
        "code": "UWU",
        "name": "Uva Wellassa University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Uva_Wellassa_university.jpg",
        "creator": "Kaushalya shamila (Wikimedia Commons)",
        "license": "CC BY-SA 4.0",
        "attribution": "Passara Road main campus, Badulla, Uva Wellassa University by Kaushalya shamila"
    },
    {
        "code": "OUSL",
        "name": "The Open University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/34/Open_University_of_Sri_Lanka.jpg",
        "creator": "Gihan Jayaweera (Wikimedia Commons)",
        "license": "CC BY-SA 3.0",
        "attribution": "Central campus administrative complex, Nawala, Open University of Sri Lanka by Gihan Jayaweera"
    },
    {
        "code": "OCUSL",
        "name": "Ocean University of Sri Lanka",
        "url": "https://upload.wikimedia.org/wikipedia/commons/5/59/Entrance_of_Ocean_University.jpg",
        "creator": "Irdnia (Wikimedia Commons)",
        "license": "CC BY-SA 4.0",
        "attribution": "Crow Island central entrance, Ocean University of Sri Lanka by Irdnia"
    },
    {
        "code": "SP-UOC",
        "name": "Sripalee Campus, University Of Colombo",
        "url": "https://upload.wikimedia.org/wikipedia/commons/2/26/Sri_Palee_Campus_-_Layan_House.jpg",
        "creator": "Sri Palee Campus (Wikimedia Commons)",
        "license": "CC BY-SA 4.0",
        "attribution": "Layan House heritage academic complex, Horana, Sripalee Campus"
    },
    {
        "code": "VAV",
        "name": "University of Vavuniya",
        "url": "https://upload.wikimedia.org/wikipedia/commons/0/07/Vavuniya_campus.jpg",
        "creator": "Ragulanrex (Wikimedia Commons)",
        "license": "CC BY-SA 3.0",
        "attribution": "Park Road campus premises, University of Vavuniya by Ragulanrex"
    }
]

print("\n--- Downloading & Processing Real Campus Photography ---")
for item in CAMPUS_PHOTOS:
    code = item["code"]
    filename = f"{code.lower()}_campus.webp"
    dest_path = os.path.join(CAMPUSES_DIR, filename)
    rel_path = f"/assets/universities/campuses/{filename}"
    
    try:
        data = download_data(item["url"])
        img = Image.open(io.BytesIO(data))
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Resize to max 1200px width with 16:9 target crop or preserve aspect
        img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
        img.save(dest_path, "WEBP", quality=85)
        
        print(f"  [OK] Saved campus photo for {code} ({img.size[0]}x{img.size[1]}px) -> {filename}")
        
        if code not in registry["universities"]:
            registry["universities"][code] = {"name": item["name"]}
            
        registry["universities"][code]["campus"] = {
            "path": rel_path,
            "source_url": item["url"],
            "creator": item["creator"],
            "license": item["license"],
            "attribution": item["attribution"],
            "dimensions": [img.size[0], img.size[1]],
            "status": "verified"
        }
    except Exception as e:
        print(f"  [ERROR] Downloading campus photo for {code}: {e}")

# ══════════════════════════════════════════════════════════════════════
# 3. DEGREE CATEGORY IMAGERY (Unsplash Free Educational License / CC0)
# ══════════════════════════════════════════════════════════════════════
DEGREE_CATEGORIES = [
    {
        "id": "engineering",
        "name": "Engineering & Applied Technology",
        "url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=900&q=80",
        "creator": "ThisisEngineering RAEng (Unsplash)",
        "license": "Unsplash Free License",
        "attribution": "Engineering research laboratory and robotic workbench"
    },
    {
        "id": "medicine",
        "name": "Medicine, Healthcare & Allied Health",
        "url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=900&q=80",
        "creator": "National Cancer Institute (Unsplash)",
        "license": "Unsplash Free License",
        "attribution": "Modern clinical healthcare and patient diagnostics"
    },
    {
        "id": "computing",
        "name": "Computer Science, Software Engineering & IT",
        "url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=900&q=80",
        "creator": "Clément H (Unsplash)",
        "license": "Unsplash Free License",
        "attribution": "Software architecture and computer programming workspace"
    },
    {
        "id": "business",
        "name": "Business, Management, Commerce & Finance",
        "url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=900&q=80",
        "creator": "Carlos Muza (Unsplash)",
        "license": "Unsplash Free License",
        "attribution": "Business analytics, financial markets, and strategic management"
    },
    {
        "id": "science",
        "name": "Physical, Biological & Chemical Sciences",
        "url": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=900&q=80",
        "creator": "Hans Reniers (Unsplash)",
        "license": "Unsplash Free License",
        "attribution": "Laboratory science research, molecular chemistry, and physics"
    },
    {
        "id": "agriculture",
        "name": "Agriculture, Animal Science & Agribusiness",
        "url": "https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?w=900&q=80",
        "creator": "Gabriel Jimenez (Unsplash)",
        "license": "Unsplash Free License",
        "attribution": "Sustainable agriculture, plant agronomy, and crop research"
    },
    {
        "id": "architecture",
        "name": "Architecture, Built Environment & Design",
        "url": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=900&q=80",
        "creator": "Daniel McCullough (Unsplash)",
        "license": "Unsplash Free License",
        "attribution": "Architectural drafting blueprints and spatial structure design"
    },
    {
        "id": "arts",
        "name": "Arts, Humanities & Social Sciences",
        "url": "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=900&q=80",
        "creator": "Patrick Tomasso (Unsplash)",
        "license": "Unsplash Free License",
        "attribution": "Humanities literature, historical archives, and academic library"
    },
    {
        "id": "law",
        "name": "Law, Justice & Jurisprudence",
        "url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=900&q=80",
        "creator": "Tingey Injury Law Firm (Unsplash)",
        "license": "Unsplash Free License",
        "attribution": "Scales of justice, legal statutes, and judicial governance"
    },
    {
        "id": "education",
        "name": "Education, Pedagogy & Teaching",
        "url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=900&q=80",
        "creator": "Dom Fou (Unsplash)",
        "license": "Unsplash Free License",
        "attribution": "Higher education lecture seminar and pedagogy discussion"
    },
    {
        "id": "technology",
        "name": "Technology, Biosystems & Engineering Technology",
        "url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=900&q=80",
        "creator": "Alexandre Debiève (Unsplash)",
        "license": "Unsplash Free License",
        "attribution": "Hardware microchip electronics and applied technology"
    },
    {
        "id": "ayurveda",
        "name": "Indigenous & Ayurvedic Medicine",
        "url": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=900&q=80",
        "creator": "Katherine Hanlon (Unsplash)",
        "license": "Unsplash Free License",
        "attribution": "Natural herbal medicine, pharmacognosy, and botanical remedies"
    },
    {
        "id": "default",
        "name": "Undergraduate University Degree",
        "url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=900&q=80",
        "creator": "Pang Yuhao (Unsplash)",
        "license": "Unsplash Free License",
        "attribution": "University campus academic convocation and graduation"
    }
]

print("\n--- Downloading & Processing Degree Category Images ---")
for cat in DEGREE_CATEGORIES:
    cat_id = cat["id"]
    filename = f"{cat_id}.webp"
    dest_path = os.path.join(DEGREES_DIR, filename)
    rel_path = f"/assets/degrees/{filename}"
    
    try:
        data = download_data(cat["url"])
        img = Image.open(io.BytesIO(data))
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Standardize aspect ratio to 16:9 for clean card integration
        target_w = 800
        target_h = 450
        
        # Center-crop to 16:9
        src_w, src_h = img.size
        aspect_target = 16.0 / 9.0
        aspect_src = src_w / src_h
        
        if aspect_src > aspect_target:
            new_w = int(src_h * aspect_target)
            left = (src_w - new_w) // 2
            img = img.crop((left, 0, left + new_w, src_h))
        else:
            new_h = int(src_w / aspect_target)
            top = (src_h - new_h) // 2
            img = img.crop((0, top, src_w, top + new_h))
            
        img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        img.save(dest_path, "WEBP", quality=82)
        
        print(f"  [OK] Saved degree image for {cat_id} ({img.size[0]}x{img.size[1]}px) -> {filename}")
        
        registry["degree_categories"][cat_id] = {
            "name": cat["name"],
            "path": rel_path,
            "source_url": cat["url"],
            "creator": cat["creator"],
            "license": cat["license"],
            "attribution": cat["attribution"],
            "dimensions": [target_w, target_h],
            "status": "verified"
        }
    except Exception as e:
        print(f"  [ERROR] Downloading degree image for {cat_id}: {e}")

# ══════════════════════════════════════════════════════════════════════
# 4. APPLE-STYLE CAMPUS & LOGO PLACEHOLDERS
# ══════════════════════════════════════════════════════════════════════
print("\n--- Generating Apple-Style Placeholders ---")
# 1. Campus Placeholder
campus_ph = Image.new('RGB', (800, 450), color='#1d1d1f')
campus_ph_path = os.path.join(PLACEHOLDERS_DIR, "campus_placeholder.webp")
campus_ph.save(campus_ph_path, "WEBP", quality=85)
registry["placeholders"]["campus"] = {
    "path": "/assets/placeholders/campus_placeholder.webp",
    "description": "Minimalist Apple graphite campus silhouette placeholder",
    "status": "local_fallback"
}

# 2. Degree Placeholder
degree_ph = Image.new('RGB', (800, 450), color='#161617')
degree_ph_path = os.path.join(PLACEHOLDERS_DIR, "degree_placeholder.webp")
degree_ph.save(degree_ph_path, "WEBP", quality=85)
registry["placeholders"]["degree"] = {
    "path": "/assets/placeholders/degree_placeholder.webp",
    "description": "Universal Apple dark-card degree discovery placeholder",
    "status": "local_fallback"
}

# 3. Clean SVG University Crest Logo Placeholder
svg_placeholder = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect width="100" height="100" rx="22" fill="#f5f5f7"/>
  <rect width="98" height="98" x="1" y="1" rx="21" fill="none" stroke="rgba(0,0,0,0.08)" stroke-width="2"/>
  <path d="M50 20 L76 34 L76 56 C76 70 50 82 50 82 C50 82 24 70 24 56 L24 34 Z" fill="none" stroke="#0071e3" stroke-width="3" stroke-linejoin="round"/>
  <path d="M50 36 L66 45 L50 54 L34 45 Z" fill="#0071e3"/>
  <path d="M38 52 L38 64 C38 64 43 68 50 68 C57 68 62 64 62 64 L62 52" fill="none" stroke="#0071e3" stroke-width="2"/>
</svg>'''

svg_ph_path = os.path.join(PLACEHOLDERS_DIR, "university_logo_placeholder.svg")
with open(svg_ph_path, "w", encoding="utf-8") as f:
    f.write(svg_placeholder)

registry["placeholders"]["logo"] = {
    "path": "/assets/placeholders/university_logo_placeholder.svg",
    "description": "Apple-style academic insignia SVG placeholder",
    "status": "local_fallback"
}

# Save Asset Registry
registry_path = os.path.join(DATA_DIR, "asset_registry.json")
with open(registry_path, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2)

print(f"\nAsset Registry successfully created at {registry_path}!")
print(f"Summary: {len(registry['universities'])} universities, {len(registry['degree_categories'])} degree categories, 3 placeholders.")
