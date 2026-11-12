# UniScope LK (Sri Lanka's First Complete University Information Platform)

> **UniScope LK** is an independent, full-stack higher education platform built from scratch to provide Sri Lankan students, undergraduates, and career planners with 100% verified academic intelligence, admissions calculators, degree comparisons, and career roadmap predictions.

---

### DEVELOPER & PLATFORM CREDITS
- **Platform Name:** UniScope LK (Sri Lanka's First Complete University Information Platform)
- **Founder & Lead Systems Engineer:** Nasimudeen Muhammed Farhan
- **Role / Credentials:** Engineering Undergraduate, Faculty of Engineering, University of Jaffna, Sri Lanka
- **Specialization:** Electrical & Electronic Engineering

---

## 🏛️ Architecture Overview

The system is engineered as an enterprise-grade, full-stack Node.js + Express application with server-rendered EJS views, high-fidelity responsive styling matching original design tokens (`Outfit`, `DM Serif Display`), dark theme support with anti-flash script, and complete RESTful APIs.

```
c:\Users\Dell\Desktop\REA V2.0\
├── server.js                        # Express 5 application, API routes, middleware, session auth
├── package.json                     # Dependencies: express, ejs, cookie-parser, cors
├── data/
│   └── database.json                # Complete verified relational database:
│                                    # - 255 University Degrees with 17-section attributes & 6D vectors
│                                    # - 21 National Universities & Campuses with rankings and faculties
│                                    # - 1,600 District-wise UGC Z-score Cutoff records (2020 - 2024)
│                                    # - 59 A/L Subjects with statutory stream allocations
│                                    # - 6 Core Career Industry Fields & Salary benchmarks
├── public/
│   ├── static/
│   │   ├── home/
│   │   │   ├── css/styles.css       # Complete layout, card grids, typography, animations
│   │   │   ├── js/script.js         # Mobile drawer, accordions, dropdowns
│   │   │   └── images/              # SVG logo emblem, banners, icons
│   │   └── accounts/
│   │       └── css/auth.css         # Auth styling & password toggle
│   ├── favicon.ico
│   └── manifest.json
├── views/
│   ├── index.ejs                    # Homepage (Hero, Live Counter Bar, Why, Tools, CTA)
│   ├── subject-combination.ejs      # 3-Subject selector, stream results, university modal
│   ├── degrees.ejs                  # Searchable 255+ degree catalog & visual gallery
│   ├── degree-detail.ejs            # Full 17-section deep dive for individual degree
│   ├── compare.ejs                  # 17-Section side-by-side like-for-like comparison matrix
│   ├── cutoff-tool.ejs              # Multi-district (25 districts) UGC cut-off tracker
│   ├── zscore-calculator.ejs        # Probability qualification calculator
│   ├── district-tool.ejs            # UGC District Quota determination wizard
│   ├── degree-finder.ejs            # 10-Step AI quiz with Cosine Similarity vector matching
│   ├── ai-risk.ejs                  # 7-Framework AI Displacement Risk model & calculator
│   ├── universities.ejs             # Directory of 17+ State Universities
│   ├── career-paths.ejs             # Public vs Private sector career pathways
│   ├── announcements.ejs            # UGC admission notices & aptitude test dates
│   ├── forums.ejs                   # Student study resources & discussion threads
│   ├── about-us.ejs                 # Founder spotlight (Nasimudeen Muhammed Farhan, Jaffna Engineering)
│   ├── data-sources.ejs             # 6-Tab research transparency record
│   ├── contact-us.ejs               # Working contact form & inquiry routing
│   ├── disclaimer.ejs               # Legal & UGC data disclaimer
│   ├── donate.ejs                   # Non-profit funding philosophy
│   ├── login.ejs                    # Authentication & session creation
│   ├── register.ejs                 # Student account registration
│   ├── profile.ejs                  # Student dashboard & Degree Cart management
│   └── partials/
│       ├── head.ejs                 # Metadata, anti-flash dark theme, CSS imports
│       ├── navbar.ejs               # Fixed header, dropdowns, cart indicator, notifications
│       ├── footer.ejs               # 4-Column footer with Nasimudeen Muhammed Farhan credits
│       └── scripts.ejs              # Toast alerts, cart management, scroll animations
└── scripts/
    ├── build_database.py            # Automated relational dataset generator
    └── verify_app.py                # Comprehensive test suite (17/17 passed)
```

---

## 🚀 Key Modules & Logic Pipelines

### 1. Subject Combination to Degree Search (`/subject-combination/`)
- Dynamic 3-subject selector with select2 duplicate option prevention.
- Instant grouping across all A/L streams: Biological Science, Physical Science, Commerce, Arts, Technology.
- Click any course row to trigger `/api/course/:code/` modal popup showing the number and names of universities offering the degree.

### 2. UGC Cut-Off Marks Comparison Tool (`/degrees/cutoff-tool/`)
- Covers all **25 administrative districts** of Sri Lanka.
- Multi-year trend analysis (2020/21 through 2023/24).
- Interactive Z-score gap estimator: Enter your score and see if you have qualified or have a shortfall ($\Delta z$).

### 3. Smart Degree Comparison (`/dashboard/compare/`)
- Side-by-side like-for-like matrix across **17 distinct academic & career facets**:
  1. Degree Code & Title
  2. University & Faculty Campus
  3. Stream Eligibility & Prerequisites
  4. Duration (Years) & SLQF Level
  5. Medium of Instruction
  6. Average Historical Z-Score Cutoff
  7. AI Displacement Risk Score & Risk Band
  8. Available Specializations & Majoring Tracks
  9. Public Sector Government Careers
  10. Private Corporate Careers
  11. Practical & Lab Exposure Index (1-10)
  12. Academic Rigor Index (1-10)
  13. Human Empathy Protection Factor ($H_{human}$)
  14. Industrial Training & Internships
  15. Professional Body Accreditation
  16. Career Breadth Score
  17. Degree Profile Direct Link

### 4. AI Displacement Risk Engine (`/ai-risk/`)
- Computes degree-level automation risk using the composite formula:
  $$R_{degree} = \sum_{i=1}^7 (w_i \cdot F_i \cdot T_i) + \alpha \cdot C_{SL} - \beta \cdot H_{human}$$
- 7 Frameworks:
  - Framework 01: Task-probability Computerisation Model (Frey & Osborne)
  - Framework 02: Task-based Substitution Mechanics (Acemoglu & Restrepo)
  - Framework 03: Global Workforce & Job Creation Outlook (WEF Future of Jobs)
  - Framework 04: Skill-Demand Velocity Shift Index
  - Framework 05: Cognitive vs Routine Axis Decomposition
  - Framework 06: LLM Direct Exposure Index (OpenAI & Eloundou)
  - Framework 07: Sri Lankan Labour-Market Model & Public Sector Absorption ($C_{SL}$)
- 4 Color-Coded Risk Bands:
  - 🟢 **Low Risk (0 - 25):** Clinical medicine, onsite civil engineering, electrical commissioning.
  - 🟡 **Moderate Risk (26 - 50):** Software engineering, technology, applied chemistry.
  - 🟠 **High Risk (51 - 75):** Routine bookkeeping, data administration.
  - 🔴 **Severe Risk (76 - 100):** High task substitutability; requires prompt engineering & leadership specialization.

### 5. Smart Degree Finder (`/degree-finder/`)
- 10-Step questionnaire mapping personality, theory vs practical preference, and career goals.
- Calculates Cosine Similarity against the 6-dimensional vector space:
  $$\text{Similarity}(u, v) = \frac{u \cdot v}{\|u\| \|v\|}$$
- Displays top matched degrees with match percentage (e.g. 96% Match) and one-click add to cart.

### 6. Degree Cart & Real-Time Toast System
- Client-side persistence via `localStorage` with server synchronization (`/api/cart/toggle`).
- Animated feedback toast at the bottom of the screen with smooth slide transitions.
- Global navigation counter badge dynamically reflecting shortlist count.

### 7. Complete Transparency & Story (`/about-us/` & `/data-sources/`)
- Credits Founder **Nasimudeen Muhammed Farhan**, Engineering Undergraduate at Faculty of Engineering, University of Jaffna, Specializing in Electrical & Electronic Engineering.
- 6-Tab transparency record detailing the Six Pillars of Verified Truth, 7-Stage Research Pipeline, and Public Integrity Covenant.

### 8. Sri Lankan University GPA & CGPA Calculator (`/gpa-calculator/`)
- Integrated from the Android Application (*GPA Calculator: Sri Lanka Uni* - `com.gpa.calc.gpa_calculation_app`).
- **Target Audience:** Exclusively tailored for Sri Lankan university undergraduates across all state faculties (University of Jaffna, Moratuwa, Peradeniya, Colombo, Sri Jayewardenepura, Kelaniya, Ruhuna, SLIIT, etc.).
- **Authentic Sri Lankan University Grading Scales:**
  - Standard UGC / SLQF 4.00 Scale
  - University of Moratuwa (UOM 4.20 Scale with A+ = 4.20)
  - University of Peradeniya (UOP 4.00 Scale)
  - University of Jaffna (UOJ Engineering & Science Scale)
  - University of Colombo / UCSC (4.00 Scale with C- = 1.70)
  - University of Sri Jayewardenepura (USJ)
  - Custom grading scale editor
- **Academic Governance & Bylaw Rules:**
  - **Repeat Module Exam Capping:** Automated cap at 'C' grade (GPV 2.00) in accordance with Sri Lankan university examination bylaws.
  - **Non-GPA (NGPA) Course Flag:** Tracks credits towards degree completion without affecting academic GPA denominator.
- **Honours Class Predictor:** Instant evaluation against Sri Lankan honours benchmarks:
  - 🏆 First Class Honours: $\text{CGPA} \ge 3.70$
  - 🎖️ Second Class Upper (2:1): $3.30 \le \text{CGPA} < 3.70$
  - 🥈 Second Class Lower (2:2): $3.00 \le \text{CGPA} < 3.30$
  - 🎓 General / Pass: $2.00 \le \text{CGPA} < 3.00$
- **Target GPA / What-If Forecast Engine:** Calculates the precise average GPA needed across remaining credits to graduate with a desired degree classification.
- **Transcript Generation & Offline Support:** Browser `localStorage` auto-save, JSON backup/restore, and 1-click printable official academic transcript preview.

---

## ⚡ Quick Start & Run Instructions

```bash
# 1. Install dependencies (already installed)
npm install

# 2. Run verification test suite
python scripts/verify_app.py

# 3. Start the server
node server.js
```
The application runs on `http://localhost:3000`.
