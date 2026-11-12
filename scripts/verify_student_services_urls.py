import urllib.request
import ssl
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

CANDIDATE_URLS = [
    # Category A: Exams & Results
    ("Official examination results", "https://www.results.exams.gov.lk/home.htm"),
    ("Department of Examinations", "https://www.doenets.lk/"),
    ("Examination results portal", "https://www.doenets.lk/examresults"),
    ("Examination notices and resources", "https://www.exams.gov.lk/"),
    ("Official examination certificates", "https://certificate.doenets.lk/"),
    ("Grade 6 school selection", "https://g6application.moe.gov.lk/"),
    
    # Category B: University Admission & Z-Scores
    ("University Grants Commission", "https://www.ugc.ac.lk/"),
    ("UGC application portal", "https://eugc.ugc.ac.lk/"),
    ("UGC admission handbook", "https://eugc.ugc.ac.lk/ugc_handbook/"),
    ("University selection 2025/2026", "https://www.ugc.ac.lk/selection_26/"),
    ("University selection 2024/2025", "https://ugc.ac.lk/selection_25/"),
    ("Official admission handbook PDF", "https://www.ugc.ac.lk/downloads/admissions/Handbook_2025_26/student_handbook_english.pdf"),

    # Category C: Scholarships & Financial Support
    ("Mahapola Scholarship", "https://www.mahapola.lk/"),
    ("Interest-Free Student Loan Scheme", "https://studentloans.mohe.gov.lk/"),
    ("Foreign scholarship portal", "https://foreignscholarships.mohe.gov.lk/"),
    ("Ministry of Higher Education", "https://www.mohe.gov.lk/"),

    # Category D: Government Documents & Certificates
    ("Birth certificate requests", "https://online.ebmd.rgd.gov.lk/"),
    ("Registrar General's Department", "https://www.rgd.gov.lk/"),
    ("NIC services (DRP)", "https://drp.gov.lk/"),
    ("NIC online services", "https://eservices.drp.gov.lk/nic-portal/"),
    ("Passport services", "https://immigration.gov.lk/"),
    ("Passport appointments", "https://eservices.immigration.gov.lk/MakeAppointments/"),
    ("Sri Lanka Government Portal", "https://www.gov.lk/"),
    ("Government Information Centre (1919)", "https://gic.gov.lk/"),
    ("Government Gazette", "https://documents.gov.lk/en/gazette.php"),

    # Category E: Learning Resources & School Education
    ("e-Thaksalawa Learning Portal", "https://e-thaksalawa.moe.gov.lk/"),
    ("Ministry of Education", "https://moe.gov.lk/"),
    ("National Institute of Education", "https://www.nie.ac.lk/"),
    ("Educational Publications Department", "https://www.edupub.gov.lk/"),
    ("National Library of Sri Lanka", "https://www.natlib.lk/"),

    # Category F: HND, Technical & Vocational Education
    ("SLIATE Main Portal", "https://www.sliate.ac.lk/"),
    ("SLIATE Application Portal", "https://apply.sliate.ac.lk/"),
    ("Department of Technical Education and Training", "https://dtet.gov.lk/en/"),
    ("NAITA", "https://www.naita.gov.lk/"),
    ("TVEC NVQ Portal", "https://www.tvec.gov.lk/"),
    ("Vocational Training Authority (VTA)", "https://www.vtasl.gov.lk/"),
    ("University of Vocational Technology (UNIVOTEC)", "https://www.uovt.ac.lk/"),
    ("The Open University of Sri Lanka", "https://ou.ac.lk/"),

    # Category G: Careers & Employment
    ("Sri Lanka Government Gazette Vacancies", "https://documents.gov.lk/en/gazette.php"),
    ("NAITA Apprenticeship Opportunities", "https://www.naita.gov.lk/"),
    ("Department of Manpower and Employment", "https://www.dome.gov.lk/"),
    ("TopJobs Sri Lanka Government Section", "https://www.topjobs.lk/")
]

print("Verifying candidate government and educational URLs...")
for name, url in CANDIDATE_URLS:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
            status = resp.status
            final_url = resp.geturl()
            print(f"[OK {status}] {name:40} -> {url} (final: {final_url})")
    except urllib.error.HTTPError as e:
        print(f"[HTTP {e.code}] {name:40} -> {url}")
    except urllib.error.URLError as e:
        print(f"[URL ERROR] {name:40} -> {url} : {e.reason}")
    except Exception as e:
        print(f"[ERR] {name:40} -> {url} : {e}")
