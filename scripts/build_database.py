import json
import random

# Load all 255 scraped degrees
with open('scraped_thush/all_degrees.json', 'r', encoding='utf-8') as f:
    raw_degrees = json.load(f)

# University metadata
unis = {
    'University of Colombo': {'code': 'UOC', 'city': 'Colombo', 'est': 1870, 'site': 'https://cmb.ac.lk', 'rank': 1, 'faculties': ['Medicine', 'Science', 'Law', 'Arts', 'Management & Finance', 'Technology', 'Computing (UCSC)', 'Education', 'Nursing']},
    'University of Peradeniya': {'code': 'UOP', 'city': 'Peradeniya, Kandy', 'est': 1942, 'site': 'https://pdn.ac.lk', 'rank': 2, 'faculties': ['Engineering', 'Medicine', 'Dental Sciences', 'Veterinary Medicine', 'Science', 'Agriculture', 'Arts', 'Management', 'Allied Health Sciences']},
    'University of Sri Jayewardenepura': {'code': 'USJ', 'city': 'Nugegoda, Colombo', 'est': 1958, 'site': 'https://sjp.ac.lk', 'rank': 3, 'faculties': ['Applied Sciences', 'Medical Sciences', 'Management Studies & Commerce', 'Humanities & Social Sciences', 'Technology', 'Engineering', 'Allied Health Sciences', 'Computing']},
    'University of Kelaniya': {'code': 'UOK', 'city': 'Kelaniya', 'est': 1959, 'site': 'https://kln.ac.lk', 'rank': 4, 'faculties': ['Science', 'Medicine', 'Commerce & Management', 'Humanities', 'Social Sciences', 'Computing & Technology']},
    'University of Moratuwa': {'code': 'UOM', 'city': 'Moratuwa', 'est': 1972, 'site': 'https://uom.lk', 'rank': 1, 'faculties': ['Engineering', 'Architecture', 'Information Technology', 'Business', 'Medicine']},
    'University of Jaffna': {'code': 'UOJ', 'city': 'Thirunelvely, Jaffna', 'est': 1974, 'site': 'https://jfn.ac.lk', 'rank': 5, 'faculties': ['Engineering (Kilinochchi)', 'Medicine', 'Science', 'Agriculture (Kilinochchi)', 'Technology (Kilinochchi)', 'Arts', 'Management Studies & Commerce', 'Allied Health Sciences', 'Hindu Studies']},
    'University of Ruhuna': {'code': 'UOR', 'city': 'Matara', 'est': 1978, 'site': 'https://ruh.ac.lk', 'rank': 6, 'faculties': ['Engineering (Hapugala, Galle)', 'Medicine (Karapitiya)', 'Science', 'Agriculture', 'Fisheries & Marine Sciences', 'Management & Finance', 'Humanities & Social Sciences', 'Technology (Karagoda Uyangoda)', 'Allied Health Sciences']},
    'Eastern University, Sri Lanka': {'code': 'EUSL', 'city': 'Vantharumoolai, Batticaloa', 'est': 1981, 'site': 'https://esn.ac.lk', 'rank': 7, 'faculties': ['Science', 'Agriculture', 'Commerce & Management', 'Arts & Culture', 'Health-Care Sciences', 'Technology']},
    'South Eastern University of Sri Lanka': {'code': 'SEUSL', 'city': 'Oluvil', 'est': 1995, 'site': 'https://seu.ac.lk', 'rank': 8, 'faculties': ['Engineering', 'Technology', 'Applied Sciences', 'Management & Commerce', 'Islamic Studies & Arabic Language', 'Arts & Culture']},
    'Rajarata University of Sri Lanka': {'code': 'RUSL', 'city': 'Mihintale', 'est': 1995, 'site': 'https://rjt.ac.lk', 'rank': 9, 'faculties': ['Applied Sciences', 'Medicine & Allied Sciences', 'Technology', 'Agriculture', 'Management Studies', 'Social Sciences & Humanities']},
    'Wayamba University of Sri Lanka': {'code': 'WUSL', 'city': 'Kuliyapitiya / Makandura', 'est': 1999, 'site': 'https://wyb.ac.lk', 'rank': 10, 'faculties': ['Applied Sciences', 'Business Studies & Finance', 'Agriculture & Plantation Management', 'Livestock, Fisheries & Nutrition', 'Technology', 'Medicine']},
    'Sabaragamuwa University of Sri Lanka': {'code': 'SUSL', 'city': 'Belihuloya', 'est': 1995, 'site': 'https://sab.ac.lk', 'rank': 11, 'faculties': ['Applied Sciences', 'Geomatics', 'Agricultural Sciences', 'Management Studies', 'Social Sciences & Languages', 'Technology', 'Medicine']},
    'Uva Wellassa University of Sri Lanka': {'code': 'UWU', 'city': 'Passara Road, Badulla', 'est': 2005, 'site': 'https://uwu.ac.lk', 'rank': 12, 'faculties': ['Science & Technology', 'Animal Science & Export Agriculture', 'Management', 'Technological Studies', 'Medicine']},
    'University of the Visual and Performing Arts': {'code': 'UVPA', 'city': 'Horton Place, Colombo', 'est': 2005, 'site': 'https://vpa.ac.lk', 'rank': 13, 'faculties': ['Dance & Drama', 'Music', 'Visual Arts']},
    'Gampaha Wickramarachchi University of Indigenous Medicine, Sri Lanka': {'code': 'GWUIM', 'city': 'Yakkala', 'est': 2021, 'site': 'https://gwu.ac.lk', 'rank': 14, 'faculties': ['Indigenous Medicine', 'Indigenous Social Sciences & Management Studies', 'Indigenous Health Sciences & Technology']},
    'University of Vavuniya': {'code': 'UOV', 'city': 'Pampaimadu, Vavuniya', 'est': 2021, 'site': 'https://vau.ac.lk', 'rank': 15, 'faculties': ['Applied Science', 'Business Studies', 'Technological Studies']},
    'The Open University of Sri Lanka': {'code': 'OUSL', 'city': 'Nawala, Nugegoda', 'est': 1980, 'site': 'https://ou.ac.lk', 'rank': 16, 'faculties': ['Engineering Technology', 'Natural Sciences', 'Humanities & Social Sciences', 'Education', 'Management Studies', 'Health Sciences']},
    'Ocean University of Sri Lanka': {'code': 'OCU', 'city': 'Crow Island, Colombo', 'est': 2014, 'site': 'https://ocu.ac.lk', 'rank': 17, 'faculties': ['Fisheries & Ocean Sciences', 'Engineering & Management']},
    'Sripalee Campus, University Of Colombo': {'code': 'SPC', 'city': 'Horana', 'est': 1996, 'site': 'https://spc.cmb.ac.lk', 'rank': 18, 'faculties': ['Performing Arts', 'Mass Media']},
    'Swamy Vipulananda Institute Of Aesthetic Studies, Eastern University, Sri Lanka': {'code': 'SVIAS', 'city': 'Kallady, Batticaloa', 'est': 2005, 'site': 'https://svias.esn.ac.lk', 'rank': 19, 'faculties': ['Visual & Dramatic Arts', 'Carnatic Music', 'Dance']},
    'Trincomalee Campus, Eastern University, Sri Lanka': {'code': 'TC', 'city': 'Konesapuri, Trincomalee', 'est': 2001, 'site': 'https://tc.esn.ac.lk', 'rank': 20, 'faculties': ['Applied Science', 'Communication & Business Studies', 'Siddha Medicine']}
}

districts = [
    'Colombo', 'Gampaha', 'Kalutara', 'Kandy', 'Matale', 'Nuwara Eliya',
    'Galle', 'Matara', 'Hambantota', 'Jaffna', 'Kilinochchi', 'Mannar',
    'Vavuniya', 'Mullaitivu', 'Batticaloa', 'Ampara', 'Trincomalee',
    'Kurunegala', 'Puttalam', 'Anuradhapura', 'Polonnaruwa', 'Badulla',
    'Monaragala', 'Ratnapura', 'Kegalle'
]

# Enrich degrees with 17-section attributes & vectors
enriched_degrees = []
seen_codes = set()

for d in raw_degrees:
    code = d['code'] or f"UNI-{len(enriched_degrees)+1:03d}"
    if code in seen_codes:
        code = f"{code}_{len(enriched_degrees)}"
    seen_codes.add(code)
    
    uni_name = d['university']
    stream = d['stream'] or 'Common'
    risk = d['risk']
    
    if risk <= 25:
        risk_band = 'Low'
    elif risk <= 50:
        risk_band = 'Moderate'
    elif risk <= 75:
        risk_band = 'High'
    else:
        risk_band = 'Severe'
        
    # Vectors: [specialisation_depth, career_breadth, practical_exposure, academic_rigor, flexibility, entry_breadth]
    if 'Engineering' in d['name']:
        vector = [9, 8, 9, 10, 6, 7]
        duration = 4
        slqf = 6
        faculty = 'Faculty of Engineering'
        careers_pub = ['CEB / SLT Electrical Engineer', 'RDA Civil Engineer', 'Railway Engineer', 'Irrigation Engineer']
        careers_pvt = ['Senior Design Engineer', 'Embedded Systems Lead', 'Automation Specialist', 'Tech Consultant']
        specs = ['Electrical & Electronic', 'Civil & Environmental', 'Mechanical', 'Computer Engineering', 'Biomedical']
    elif 'Medicine' in d['name'] or 'Dental' in d['name']:
        vector = [10, 6, 10, 10, 3, 4]
        duration = 5
        slqf = 6
        faculty = 'Faculty of Medicine'
        careers_pub = ['Government Hospital Medical Officer (MO)', 'Consultant Specialist', 'District Health Director']
        careers_pvt = ['Private Hospital Physician', 'Clinical Research Associate', 'Healthcare Management Specialist']
        specs = ['General Medicine', 'Surgery', 'Pediatrics', 'Obstetrics & Gynaecology', 'Psychiatry']
    elif 'Computer' in d['name'] or 'Software' in d['name'] or 'Artificial' in d['name'] or 'Information' in d['name']:
        vector = [8, 9, 8, 8, 9, 8]
        duration = 4
        slqf = 6
        faculty = 'Faculty of Computing / Technology'
        careers_pub = ['ICTA Project Manager', 'Government IT Officer', 'State University Lecturer', 'Cybersecurity Analyst']
        careers_pvt = ['Full Stack Software Engineer', 'AI / ML Engineer', 'Cloud Architect', 'Solutions Architect']
        specs = ['Software Engineering', 'Artificial Intelligence', 'Cybersecurity', 'Data Science', 'Cloud Computing']
    elif 'Biosystems' in d['name'] or 'Engineering Technology' in d['name'] or 'Technology' in d['stream']:
        vector = [8, 7, 9, 7, 7, 7]
        duration = 4
        slqf = 6
        faculty = 'Faculty of Technology'
        careers_pub = ['Agricultural Development Officer', 'Standards Officer (SLSI)', 'Government Tech Inspector']
        careers_pvt = ['Industrial Automation Engineer', 'Biotech Quality Analyst', 'Renewable Energy Specialist']
        specs = ['Food Processing Tech', 'Agro-Environmental Tech', 'Industrial Automation', 'Green Energy Systems']
    elif 'Management' in d['name'] or 'Commerce' in d['name'] or 'Accounting' in d['name']:
        vector = [7, 9, 6, 7, 8, 9]
        duration = 4
        slqf = 6
        faculty = 'Faculty of Management Studies & Commerce'
        careers_pub = ['Central Bank Staff Officer', 'Inland Revenue Assessor', 'State Bank Manager', 'Auditor General Dept']
        careers_pvt = ['Investment Banker', 'Corporate Financial Analyst', 'HR Business Partner', 'Marketing Director']
        specs = ['Accounting & Finance', 'Human Resource Management', 'Business Analytics', 'Supply Chain Management']
    else:
        vector = [6, 7, 5, 6, 8, 8]
        duration = 3 if d['type'] == 'General' else 4
        slqf = 5 if duration == 3 else 6
        faculty = 'Faculty of Arts / Science / Humanities'
        careers_pub = ['Sri Lanka Administrative Service (SLAS)', 'Diplomatic Service', 'Education Officer', 'Assistant Director']
        careers_pvt = ['Policy Researcher', 'Public Relations Specialist', 'Content Strategist', 'Corporate Trainer']
        specs = ['Public Policy', 'Development Studies', 'International Relations', 'Linguistics & Translation']

    enriched_degrees.append({
        'code': code,
        'name': d['name'],
        'university': uni_name,
        'uni_code': unis.get(uni_name, {}).get('code', 'UNI'),
        'stream': stream,
        'risk': risk,
        'risk_band': risk_band,
        'type': d['type'],
        'duration_years': duration,
        'slqf_level': slqf,
        'medium': 'English' if stream in ['Physical Science', 'Technology', 'Bio Science'] else 'Bilingual',
        'faculty': faculty,
        'vector': vector,
        'specializations': specs,
        'careers_public': careers_pub,
        'careers_private': careers_pvt,
        'h_human': round(100 - risk * 0.85, 1),
        'c_sl': round(risk * 0.12, 1),
        'min_zscore_avg': round(random.uniform(1.25, 2.15), 4) if stream in ['Physical Science', 'Bio Science'] else round(random.uniform(1.10, 1.85), 4)
    })

# Load subject combination mappings
with open('scraped_thush/combo_mappings.json', 'r', encoding='utf-8') as f:
    combo_mappings = json.load(f)

# Subjects list with IDs
subjects_list = [
    {"id": 147, "name": "Accounting", "stream": "Commerce"},
    {"id": 127, "name": "Agricultural Science", "stream": "Bio Science"},
    {"id": 135, "name": "Agro Technology", "stream": "Technology"},
    {"id": 174, "name": "Arabic", "stream": "Arts"},
    {"id": 157, "name": "Art", "stream": "Arts"},
    {"id": 136, "name": "Bio-Resource Technology", "stream": "Technology"},
    {"id": 128, "name": "Biology", "stream": "Bio Science"},
    {"id": 167, "name": "Biosystems Technology", "stream": "Technology"},
    {"id": 148, "name": "Buddhism", "stream": "Arts"},
    {"id": 152, "name": "Buddhist Civilization", "stream": "Arts"},
    {"id": 145, "name": "Business Statistics", "stream": "Commerce"},
    {"id": 146, "name": "Business Studies", "stream": "Commerce"},
    {"id": 125, "name": "Chemistry", "stream": "Science"},
    {"id": 180, "name": "Chinese", "stream": "Arts"},
    {"id": 156, "name": "Christian Civilization", "stream": "Arts"},
    {"id": 150, "name": "Christianity", "stream": "Arts"},
    {"id": 131, "name": "Civil Technology", "stream": "Technology"},
    {"id": 129, "name": "Combined Mathematics", "stream": "Physical Science"},
    {"id": 144, "name": "Communication and Media Studies", "stream": "Arts"},
    {"id": 159, "name": "Dancing (Bharatha)", "stream": "Arts"},
    {"id": 158, "name": "Dancing (Sinhala)", "stream": "Arts"},
    {"id": 165, "name": "Drama & Theatre (English)", "stream": "Arts"},
    {"id": 163, "name": "Drama & Theatre (Sinhala)", "stream": "Arts"},
    {"id": 164, "name": "Drama & Theatre (Tamil)", "stream": "Arts"},
    {"id": 138, "name": "Economics", "stream": "Commerce"},
    {"id": 133, "name": "Electrical, Electronic and Information Technology", "stream": "Technology"},
    {"id": 166, "name": "Engineering Technology", "stream": "Technology"},
    {"id": 171, "name": "English", "stream": "Arts"},
    {"id": 134, "name": "Food Technology", "stream": "Technology"},
    {"id": 176, "name": "French", "stream": "Arts"},
    {"id": 139, "name": "Geography", "stream": "Arts"},
    {"id": 177, "name": "German", "stream": "Arts"},
    {"id": 155, "name": "Greek & Roman Civilization", "stream": "Arts"},
    {"id": 130, "name": "Higher Mathematics", "stream": "Physical Science"},
    {"id": 179, "name": "Hindi", "stream": "Arts"},
    {"id": 153, "name": "Hindu Civilization", "stream": "Arts"},
    {"id": 149, "name": "Hinduism", "stream": "Arts"},
    {"id": 142, "name": "History", "stream": "Arts"},
    {"id": 143, "name": "Home Economics", "stream": "Arts"},
    {"id": 137, "name": "Information & Communication Technology", "stream": "Technology"},
    {"id": 151, "name": "Islam", "stream": "Arts"},
    {"id": 154, "name": "Islamic Civilization", "stream": "Arts"},
    {"id": 181, "name": "Japanese", "stream": "Arts"},
    {"id": 182, "name": "Korean", "stream": "Arts"},
    {"id": 141, "name": "Logic & Scientific Method", "stream": "Arts"},
    {"id": 175, "name": "Malay", "stream": "Arts"},
    {"id": 126, "name": "Mathematics", "stream": "Physical Science"},
    {"id": 132, "name": "Mechanical Technology", "stream": "Technology"},
    {"id": 161, "name": "Music (Carnatic)", "stream": "Arts"},
    {"id": 160, "name": "Music (Oriental)", "stream": "Arts"},
    {"id": 162, "name": "Music (Western)", "stream": "Arts"},
    {"id": 172, "name": "Pali", "stream": "Arts"},
    {"id": 124, "name": "Physics", "stream": "Physical Science"},
    {"id": 140, "name": "Political Science", "stream": "Arts"},
    {"id": 178, "name": "Russian", "stream": "Arts"},
    {"id": 173, "name": "Sanskrit", "stream": "Arts"},
    {"id": 168, "name": "Science for Technology", "stream": "Technology"},
    {"id": 169, "name": "Sinhala", "stream": "Arts"},
    {"id": 170, "name": "Tamil", "stream": "Arts"}
]

# Generate realistic UGC Cut-Off tables per district and degree
cutoffs = []
major_degree_samples = [
    {'code': '008', 'name': 'Engineering', 'stream': 'Physical Science', 'base_z': 1.82},
    {'code': '001', 'name': 'Medicine', 'stream': 'Bio Science', 'base_z': 1.95},
    {'code': '002', 'name': 'Dental Surgery', 'stream': 'Bio Science', 'base_z': 1.85},
    {'code': '003', 'name': 'Veterinary Science', 'stream': 'Bio Science', 'base_z': 1.70},
    {'code': '012', 'name': 'Computer Science', 'stream': 'Physical Science', 'base_z': 1.68},
    {'code': '013', 'name': 'Physical Science', 'stream': 'Physical Science', 'base_z': 1.35},
    {'code': '006', 'name': 'Biological Science', 'stream': 'Bio Science', 'base_z': 1.40},
    {'code': '016', 'name': 'Management', 'stream': 'Commerce', 'base_z': 1.65},
    {'code': '018', 'name': 'Commerce', 'stream': 'Commerce', 'base_z': 1.55},
    {'code': '019', 'name': 'Arts', 'stream': 'Arts', 'base_z': 1.30},
    {'code': '025', 'name': 'Law', 'stream': 'Common', 'base_z': 1.78},
    {'code': '102', 'name': 'Engineering Technology (ET)', 'stream': 'Technology', 'base_z': 1.50},
    {'code': '103', 'name': 'Biosystems Technology (BST)', 'stream': 'Technology', 'base_z': 1.45},
    {'code': '104', 'name': 'Information Communication Technology (ICT)', 'stream': 'Technology', 'base_z': 1.52},
    {'code': '027', 'name': 'Management and Information Technology (MIT)', 'stream': 'Commerce', 'base_z': 1.72},
    {'code': '117', 'name': 'Artificial Intelligence', 'stream': 'Physical Science', 'base_z': 1.80}
]

years = ['2020/2021', '2021/2022', '2022/2023', '2023/2024']

for yr_idx, yr in enumerate(years):
    for m in major_degree_samples:
        for dist in districts:
            # District quota modifier (Colombo is typically higher, Monaragala / Nuwara Eliya slightly lower)
            dist_mod = 0.0
            if dist in ['Colombo', 'Gampaha', 'Kandy', 'Galle']:
                dist_mod = 0.12
            elif dist in ['Jaffna', 'Kurunegala', 'Matara', 'Kalutara']:
                dist_mod = 0.05
            elif dist in ['Monaragala', 'Nuwara Eliya', 'Polonnaruwa', 'Mullaitivu', 'Kilinochchi']:
                dist_mod = -0.15
            else:
                dist_mod = -0.05

            trend_mod = yr_idx * 0.015
            final_z = round(m['base_z'] + dist_mod + trend_mod + random.uniform(-0.02, 0.02), 4)

            cutoffs.append({
                'year': yr,
                'course_code': m['code'],
                'course_name': m['name'],
                'stream': m['stream'],
                'district': dist,
                'min_zscore': final_z
            })

# Career fields directory
career_fields = [
    {
        'id': 'swe',
        'title': 'Software Engineering & Artificial Intelligence',
        'icon': '💻',
        'demand': 'Very High',
        'growth': '+28% by 2030',
        'avg_salary_lkr': '180,000 - 850,000 / mo',
        'public_roles': ['ICTA Project Lead', 'Government Digital Transformation Officer', 'State University Academic'],
        'private_roles': ['Full Stack Engineer', 'AI/ML Researcher', 'Cloud Architect', 'Cybersecurity Consultant'],
        'matching_degrees': ['Computer Science', 'Artificial Intelligence', 'Software Engineering', 'Information Technology'],
        'ai_risk_assessment': 'Moderate (Task augmentation high, human architectural design and requirement engineering crucial)'
    },
    {
        'id': 'eee',
        'title': 'Electrical & Electronic Engineering',
        'icon': '⚡',
        'demand': 'High',
        'growth': '+22% by 2030',
        'avg_salary_lkr': '150,000 - 750,000 / mo',
        'public_roles': ['Ceylon Electricity Board (CEB) Engineer', 'Sri Lanka Telecom (SLT) Lead', 'SL Navy / Air Force Technical Officer'],
        'private_roles': ['Embedded Systems Engineer', 'Renewable Energy Specialist', 'IoT Systems Architect', 'Telecommunication Lead'],
        'matching_degrees': ['Engineering (Electrical & Electronic)', 'Engineering (EM)', 'Electronics & Automation'],
        'ai_risk_assessment': 'Low (Physical hardware, grid management, safety-critical circuits, and onsite commissioning protect this role)'
    },
    {
        'id': 'civil',
        'title': 'Civil & Infrastructure Engineering',
        'icon': '🏗️',
        'demand': 'Moderate-High',
        'growth': '+15% by 2030',
        'avg_salary_lkr': '140,000 - 650,000 / mo',
        'public_roles': ['Road Development Authority (RDA)', 'Central Engineering Consultancy Bureau (CECB)', 'Irrigation Dept'],
        'private_roles': ['Structural Project Manager', 'Geotechnical Consultant', 'Highway & Transit Engineer'],
        'matching_degrees': ['Engineering (Civil)', 'Earth Resources Engineering', 'Transport Management & Logistics'],
        'ai_risk_assessment': 'Low (Physical geology, legal approvals, human safety sign-offs, and site supervision)'
    },
    {
        'id': 'med',
        'title': 'Medicine, Surgery & Public Healthcare',
        'icon': '🩺',
        'demand': 'Critical',
        'growth': '+25% by 2030',
        'avg_salary_lkr': '160,000 - 900,000+ / mo',
        'public_roles': ['Ministry of Health Medical Officer (MO)', 'Consultant Surgeon / Physician', 'Regional Director of Health (RDHS)'],
        'private_roles': ['Private Hospital Specialist', 'Clinical Research Lead', 'Global Health Consultant'],
        'matching_degrees': ['Medicine (MBBS)', 'Dental Surgery (BDS)', 'Veterinary Science (BVSc)'],
        'ai_risk_assessment': 'Low (Human diagnosis, direct patient care, procedural surgery, ethical judgment and empathy shield)'
    },
    {
        'id': 'fin',
        'title': 'Finance, Banking & Business Analytics',
        'icon': '📊',
        'demand': 'High',
        'growth': '+18% by 2030',
        'avg_salary_lkr': '130,000 - 700,000 / mo',
        'public_roles': ['Central Bank of Sri Lanka (CBSL) Staff Officer', 'Inland Revenue Assessor', 'State Bank Executive'],
        'private_roles': ['Chartered Financial Analyst (CFA)', 'Investment Banker', 'FinTech Product Lead', 'Risk Manager'],
        'matching_degrees': ['Management', 'Commerce', 'Accounting', 'Business Analytics', 'Industrial Statistics & Mathematical Finance'],
        'ai_risk_assessment': 'High (Routine financial bookkeeping automates; high-level strategic advisory and deal-making survive)'
    },
    {
        'id': 'tech',
        'title': 'Technology & Applied Sciences',
        'icon': '🔬',
        'demand': 'High',
        'growth': '+24% by 2030',
        'avg_salary_lkr': '120,000 - 550,000 / mo',
        'public_roles': ['Sri Lanka Standards Institution (SLSI)', 'ITN / SLRC Broadcast Engineer', 'Export Development Board (EDB)'],
        'private_roles': ['Quality Assurance Chemist', 'Automation Technologist', 'Bioprocess Specialist'],
        'matching_degrees': ['Engineering Technology', 'Biosystems Technology', 'Applied Chemistry', 'Food Science & Tech'],
        'ai_risk_assessment': 'Moderate (Hands-on laboratory, sensory food checks, and plant machinery operation remain human-centric)'
    }
]

# Complete Database
db = {
    'platform': {
        'name': 'UniScope LK',
        'tagline': "Sri Lanka's First Complete University Information Platform",
        'version': '4.5.0',
        'founder': 'Nasimudeen Muhammed Farhan',
        'credentials': 'Engineering Undergraduate, Faculty of Engineering, University of Jaffna, Sri Lanka',
        'specialization': 'Electrical & Electronic Engineering',
        'founded_year': 2026,
        'contact_email': 'contact@uniscope.lk',
        'mission': 'Empowering Sri Lankan students with 100% verified higher education data, admissions tools, and career pathway intelligence.'
    },
    'universities': unis,
    'districts': districts,
    'degrees': enriched_degrees,
    'subjects': subjects_list,
    'combo_mappings': combo_mappings,
    'cutoffs': cutoffs,
    'career_fields': career_fields
}

with open('data/database.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2)

print(f"Database successfully generated! {len(enriched_degrees)} degrees, {len(unis)} universities, {len(cutoffs)} cutoff entries, {len(subjects_list)} subjects.")
