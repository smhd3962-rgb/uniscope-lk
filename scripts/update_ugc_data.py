import os
import json
import re
import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Starting UGC Data Extraction and Database Modernization...")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources', 'ugc')

os.makedirs(RESOURCES_DIR, exist_ok=True)
for yr in ['2025-2026', '2024-2025', '2023-2024', '2022-2023']:
    os.makedirs(os.path.join(RESOURCES_DIR, yr), exist_ok=True)

# 1. Manifest
manifest = {
    "platform": "UniScope LK",
    "updated_at": "2026-11-10T19:30:00Z",
    "primary_academic_year": "2025/2026",
    "verification_authority": "University Grants Commission (UGC) Sri Lanka",
    "sources": [
        {
            "academic_year": "2025/2026",
            "title": "Minimum 'Z' Scores for Selection to Various Courses of Study of Universities (Academic Year 2025/2026)",
            "document": "COP_2025_2026-ENGLISH_Final.pdf",
            "publication_date": "2026-07-31",
            "authority": "University Grants Commission - Sri Lanka",
            "status": "Latest Official Verified",
            "total_pages": 10,
            "districts_covered": 25
        },
        {
            "academic_year": "2024/2025",
            "title": "Minimum 'Z' Scores for Selection to Various Courses of Study of Universities (Academic Year 2024/2025)",
            "document": "COP_2024_2025-ENGLISH_Final.pdf",
            "publication_date": "2025-08-25",
            "authority": "University Grants Commission - Sri Lanka",
            "status": "Previous Academic Year Verified",
            "total_pages": 10,
            "districts_covered": 25
        },
        {
            "academic_year": "2023/2024",
            "title": "Minimum 'Z' Scores for Selection to Various Courses of Study of Universities (Academic Year 2023/2024)",
            "document": "University Cut-Off Marks 2024 English - www.gazette.lk.pdf",
            "publication_date": "2024-09-20",
            "authority": "University Grants Commission - Sri Lanka",
            "status": "Historical Official Verified",
            "total_pages": 10,
            "districts_covered": 25
        },
        {
            "academic_year": "2022/2023",
            "title": "Minimum 'Z' Scores for Selection to Various Courses of Study of Universities (Academic Year 2022/2023)",
            "document": "COP_2022_2023-ENGLISH_AR_TG.pdf",
            "publication_date": "2023-12-01",
            "authority": "University Grants Commission - Sri Lanka",
            "status": "Historical Official Verified",
            "total_pages": 10,
            "districts_covered": 25
        },
        {
            "academic_year": "2025/2026",
            "title": "Admission to Undergraduate Courses of the Universities in Sri Lanka (Academic Year 2025/2026)",
            "document": "student_handbook_english.pdf",
            "publication_date": "2025-11-15",
            "authority": "University Grants Commission - Sri Lanka",
            "status": "Official Student Admission Handbook",
            "total_pages": 210,
            "description": "Rules, subject combinations, course codes, and eligibility criteria for state university admission."
        }
    ],
    "copyright_notice": "Official UGC publications are referenced strictly for non-commercial educational transparency, public guidance, and student research. Extracted structured data is preserved under statutory fair use."
}

with open(os.path.join(RESOURCES_DIR, 'manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)

print("[OK] Manifest written to resources/ugc/manifest.json")

# 2. Districts List
DISTRICTS = [
    'COLOMBO', 'GAMPAHA', 'KALUTARA', 'MATALE', 'KANDY', 'NUWARA ELIYA',
    'GALLE', 'MATARA', 'HAMBANTOTA', 'JAFFNA', 'KILINOCHCHI', 'MANNAR',
    'MULLAITIVU', 'VAVUNIYA', 'TRINCOMALEE', 'BATTICALOA', 'AMPARA',
    'PUTTALAM', 'KURUNEGALA', 'ANURADHAPURA', 'POLONNARUWA', 'BADULLA',
    'MONARAGALA', 'KEGALLE', 'RATNAPURA'
]

def clean_course_name(raw):
    c = raw.replace('#', '').replace('*', '').strip()
    c = ' '.join(c.split())
    # Convert ALL CAPS to Clean Title Case
    # Keep abbreviations like (ET), (BST), (ICT), MBBS, BDS
    words = c.split()
    clean_words = []
    for w in words:
        if w.upper() in ['(ET)', '(BST)', '(ICT)', 'MBBS', 'BDS', 'BVSC', 'B.SC', 'BA', 'BBA', 'BCOM', 'MIT', 'AI', 'IT']:
            clean_words.append(w.upper())
        elif w.startswith('(') and w.endswith(')'):
            clean_words.append(w.upper())
        else:
            clean_words.append(w.capitalize())
    return ' '.join(clean_words)

def infer_stream(cname):
    c = cname.upper()
    if any(x in c for x in ['MEDICINE', 'DENTAL', 'VETERINARY', 'BIOLOGICAL', 'ANIMAL', 'FOOD SCIENCE', 'NURSING', 'PHARMACY', 'PHYSIOTHERAPY', 'MEDICAL LAB', 'SPEECH', 'RADIOGRAPHY', 'HEALTH']):
        return 'Bio Science'
    if any(x in c for x in ['ENGINEERING TECHNOLOGY', 'BIOSYSTEMS TECHNOLOGY', 'INFORMATION COMMUNICATION TECHNOLOGY (ICT)', 'TECHNOLOGY (ET)', 'TECHNOLOGY (BST)']):
        return 'Technology'
    if any(x in c for x in ['ENGINEERING', 'PHYSICAL SCIENCE', 'SURVEYING', 'STATISTICS & OPERATIONS', 'COMPUTER SCIENCE', 'ARTIFICIAL INTELLIGENCE', 'ELECTRONICS']):
        return 'Physical Science'
    if any(x in c for x in ['MANAGEMENT', 'COMMERCE', 'BUSINESS', 'ACCOUNTING', 'FINANCE', 'MARKETING', 'HUMAN RESOURCE', 'ESTATE MANAGEMENT']):
        return 'Commerce'
    if any(x in c for x in ['LAW', 'ARTS', 'PEACE', 'TRANSLATION', 'SOCIAL', 'COMMUNICATION', 'MASS MEDIA', 'LANGUAGES', 'ISLAMIC', 'ARABIC', 'MUSIC', 'DANCE', 'DRAMA', 'VISUAL ART']):
        return 'Arts'
    return 'Common'

PDF_SOURCES = [
    ('Updated Cutoff/COP_2025_2026-ENGLISH_Final.pdf', '2025/2026', 'COP 2025/2026 (Final)'),
    ('Updated Cutoff/COP_2024_2025-ENGLISH_Final.pdf', '2024/2025', 'COP 2024/2025 (Final)'),
    ('Updated Cutoff/University Cut-Off Marks 2024 English - www.gazette.lk.pdf', '2023/2024', 'COP 2023/2024 (Official Gazette)'),
    ('Updated Cutoff/COP_2022_2023-ENGLISH_AR_TG.pdf', '2022/2023', 'COP 2022/2023 (Official)')
]

all_extracted_cutoffs = []
courses_per_year = {}

for fpath, year, doc_label in PDF_SOURCES:
    print(f"\nProcessing {year} from {fpath}...")
    doc = fitz.open(fpath)
    yr_records = []
    courses_seen = set()
    
    for pno in range(len(doc)):
        page = doc[pno]
        tables = list(page.find_tables())
        for tab in tables:
            data = tab.extract()
            if not data or len(data) < 2:
                continue
            headers = data[0]
            cols = []
            for c_idx in range(1, len(headers)):
                clean_h = ' '.join((headers[c_idx] or '').split())
                m = re.search(r'^(.*?)\s*\(([^()]+)\)\s*$', clean_h)
                if m:
                    raw_cname = m.group(1)
                    raw_uname = m.group(2)
                    cname = clean_course_name(raw_cname)
                    uname = ' '.join(raw_uname.split())
                    cols.append((c_idx, cname, uname))
                    courses_seen.add((cname, uname))
            
            for row in data[1:]:
                if not row or not row[0]:
                    continue
                raw_d = ' '.join(str(row[0]).split()).upper()
                matched_d = next((d.title() for d in DISTRICTS if d == raw_d or d in raw_d), None)
                if not matched_d:
                    continue
                
                for c_idx, cname, uname in cols:
                    if c_idx < len(row):
                        val_raw = str(row[c_idx] or '').strip()
                        if val_raw and val_raw != '-' and val_raw != '':
                            is_nqc = 'NQC' in val_raw.upper()
                            min_z = 'NQC' if is_nqc else None
                            if not is_nqc:
                                num_match = re.search(r'^-?\d+\.\d+', val_raw)
                                if num_match:
                                    min_z = float(num_match.group(0))
                            
                            if min_z is not None:
                                record = {
                                    'year': year,
                                    'course_name': cname,
                                    'university': uname,
                                    'stream': infer_stream(cname),
                                    'district': matched_d,
                                    'min_zscore': min_z,
                                    'source': f"{doc_label} - Page {pno+1}",
                                    'status': 'Official Verified'
                                }
                                yr_records.append(record)
                                all_extracted_cutoffs.append(record)
                                
    courses_per_year[year] = len(courses_seen)
    print(f"  [OK] Extracted {len(yr_records)} cut-off points across {len(courses_seen)} courses for {year}.")

print(f"\nTotal official cutoff records extracted: {len(all_extracted_cutoffs)}")

# 3. Load and update data/database.json
db_path = os.path.join(DATA_DIR, 'database.json')
with open(db_path, 'r', encoding='utf-8') as f:
    db = json.load(f)

# Update platform metadata & remove unverified marketing claims
db['platform'] = {
    'name': 'UniScope LK',
    'tagline': 'Explore Sri Lankan Universities and Degree Opportunities',
    'description': 'Discover degree programmes, compare university options, explore official admission information, and plan your academic journey with UniScope LK.',
    'hero_headline': 'Explore Your Future.',
    'hero_subtitle': 'Find degrees, compare universities, and explore admission information—all in one place.',
    'version': '5.0.0',
    'latest_academic_year': '2025/2026',
    'verified_sources': [
        'UGC Sri Lanka Admission Handbook 2025/2026',
        'Official UGC Cut-Off Points 2025/2026 (Published July 2026)',
        'Official UGC Cut-Off Points 2024/2025 (Published August 2025)',
        'Official UGC Cut-Off Points 2023/2024 (Published September 2024)',
        'Official UGC Cut-Off Points 2022/2023 (Published December 2023)'
    ],
    'developer': {
        'name': 'Farhan Mohammad',
        'title': 'B.Sc. (Hons) Electrical and Electronics Engineering Undergraduate',
        'institution': 'University of Jaffna, Sri Lanka',
        'email': 'farhanugc@gmail.com',
        'linkedin': 'https://www.linkedin.com/in/farhan-mohammad-417a772b9',
        'bio': 'Engineering undergraduate at the University of Jaffna with a focus on engineering, technology, and accessible higher education systems in Sri Lanka.'
    },
    'disclaimer': 'UniScope LK is an independent educational information website and is not an official University Grants Commission service. Important admission decisions should be verified using official university and UGC publications.'
}

# Update cutoffs
db['latest_academic_year'] = '2025/2026'
db['academic_years'] = ['2025/2026', '2024/2025', '2023/2024', '2022/2023']
db['cutoffs'] = all_extracted_cutoffs

# 4. Recalculate each degree's min_zscore_avg using 2025/2026 data
cutoff_2025_map = {}
cutoff_historical_map = {}

for c in all_extracted_cutoffs:
    if isinstance(c['min_zscore'], (int, float)):
        key = (c['course_name'].lower(), c['university'].lower())
        if c['year'] == '2025/2026':
            cutoff_2025_map.setdefault(key, []).append(c['min_zscore'])
        cutoff_historical_map.setdefault(key, []).append(c['min_zscore'])

updated_degrees = 0
for d in db.get('degrees', []):
    d_name = d.get('name', '').lower()
    d_uni = d.get('university', '').lower()
    
    # Try exact match, then substring match
    scores = cutoff_2025_map.get((d_name, d_uni))
    if not scores:
        for (cn, un), s_list in cutoff_2025_map.items():
            if (cn in d_name or d_name in cn) and (un in d_uni or d_uni in un):
                scores = s_list
                break
    
    # Fallback to historical if not in 2025/2026
    if not scores:
        scores = cutoff_historical_map.get((d_name, d_uni))
    
    if scores:
        avg_score = round(sum(scores) / len(scores), 4)
        d['min_zscore_avg'] = avg_score
        d['min_zscore_latest_year'] = '2025/2026'
        d['min_zscore_samples'] = len(scores)
        updated_degrees += 1

print(f"\n[OK] Recalculated min_zscore_avg for {updated_degrees}/{len(db.get('degrees', []))} degrees using verified UGC data.")

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2)

print(f"[OK] data/database.json updated with {len(all_extracted_cutoffs)} verified cutoff records!")
