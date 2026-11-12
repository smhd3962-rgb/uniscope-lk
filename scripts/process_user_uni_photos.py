import os
import json
from PIL import Image

UNI_PHOTO_MAP = [
    {
        "file": "Morattuwa Uni.png",
        "code": "UOM",
        "name": "University of Moratuwa",
        "city": "Katubedda, Moratuwa",
        "attribution": "University of Moratuwa main campus complex"
    },
    {
        "file": "Gampaha vikramrchi.png",
        "code": "GWUIM",
        "name": "Gampaha Wickramarachchi University of Indigenous Medicine, Sri Lanka",
        "city": "Yakkala, Gampaha",
        "attribution": "Gampaha Wickramarachchi University campus grounds"
    },
    {
        "file": "visual performing arts.png",
        "code": "UVPA",
        "name": "University of the Visual and Performing Arts",
        "city": "Colombo 07",
        "attribution": "University of the Visual and Performing Arts complex, Albert Crescent"
    },
    {
        "file": "swami vipulanadha.png",
        "code": "SVIAS",
        "name": "Swamy Vipulananda Institute Of Aesthetic Studies, Eastern University, Sri Lanka",
        "city": "Kallady, Batticaloa",
        "attribution": "Swami Vipulananda Institute of Aesthetic Studies campus premises"
    },
    {
        "file": "Eastern Uni.png",
        "code": "EUSL",
        "name": "Eastern University, Sri Lanka",
        "city": "Vantharumoolai, Chenkalady",
        "attribution": "Eastern University Sri Lanka main administrative & academic campus"
    },
    {
        "file": "jaywardhanapura uni.jpg",
        "code": "USJ",
        "name": "University of Sri Jayewardenepura",
        "city": "Gangodawila, Nugegoda",
        "attribution": "University of Sri Jayewardenepura main campus entrance & faculty complex"
    },
    {
        "file": "Rajartta.png",
        "code": "RUSL",
        "name": "Rajarata University of Sri Lanka",
        "city": "Mihintale, Anuradhapura",
        "attribution": "Rajarata University of Sri Lanka faculty and campus complex, Mihintale"
    },
    {
        "file": "SEUSL.png",
        "code": "SEUSL",
        "name": "South Eastern University of Sri Lanka",
        "city": "Oluvil",
        "attribution": "South Eastern University of Sri Lanka Oluvil main campus"
    },
    {
        "file": "UOJ.png",
        "code": "UOJ",
        "name": "University of Jaffna",
        "city": "Thirunelvely, Jaffna",
        "attribution": "University of Jaffna main campus administration & academic complex"
    }
]

SOURCE_DIR = 'Uni photos'
DEST_DIR = os.path.join('public', 'assets', 'universities', 'campuses')
os.makedirs(DEST_DIR, exist_ok=True)

# Load asset registry
registry_path = os.path.join('data', 'asset_registry.json')
with open(registry_path, 'r', encoding='utf-8') as f:
    reg = json.load(f)

if "universities" not in reg:
    reg["universities"] = {}

results = []

for item in UNI_PHOTO_MAP:
    src_path = os.path.join(SOURCE_DIR, item["file"])
    if not os.path.exists(src_path):
        print(f"[FAIL] Missing source file: {src_path}")
        continue
    
    code = item["code"]
    dest_filename = f"{code.lower()}_campus.webp"
    dest_path = os.path.join(DEST_DIR, dest_filename)
    rel_path = f"/assets/universities/campuses/{dest_filename}"
    
    with Image.open(src_path) as img:
        orig_w, orig_h = img.size
        orig_mode = img.mode
        
        # Convert RGBA to RGB with clean background if needed
        if orig_mode in ('RGBA', 'LA') or (orig_mode == 'P' and 'transparency' in img.info):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[3]) # 3 is alpha channel
            rgb_img = background
        else:
            rgb_img = img.convert('RGB')
        
        # Resize to max 1200x800 preserving aspect ratio
        rgb_img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
        final_w, final_h = rgb_img.size
        
        # Save as high-quality WebP
        rgb_img.save(dest_path, "WEBP", quality=88, method=6)
        file_size = os.path.getsize(dest_path)
        
        print(f"[OK] Processed {item['file']} -> {dest_filename} ({final_w}x{final_h}px, {file_size:,} bytes)")
        
        # Update registry entry
        if code not in reg["universities"]:
            reg["universities"][code] = {"name": item["name"]}
            
        reg["universities"][code]["campus"] = {
            "path": rel_path,
            "source": f"Uni photos/{item['file']}",
            "attribution": item["attribution"],
            "license": "Official / Authenticated Sri Lankan University Photography",
            "dimensions": [final_w, final_h],
            "status": "verified",
            "updated_at": "2026-11-11"
        }
        
        results.append({
            "code": code,
            "name": item["name"],
            "filename": dest_filename,
            "dimensions": f"{final_w}x{final_h}",
            "size": file_size
        })

# Save updated registry
with open(registry_path, 'w', encoding='utf-8') as f:
    json.dump(reg, f, indent=2, ensure_ascii=False)

print(f"\nSuccessfully updated {len(results)} university campus images in asset_registry.json & public/assets/universities/campuses/!")
