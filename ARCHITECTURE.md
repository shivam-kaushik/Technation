# 🏗️ System Architecture# 🏗️ System Architecture



## Overview## Overview

```

The Enhanced AI Skills Recognition Engine is a Streamlit-based web application that provides comprehensive career guidance for underrepresented groups entering AI. The system combines NLP-powered skill extraction, ML-based role matching, and equity-focused analytics.┌─────────────────────────────────────────────────────────────┐

│                     SKILL RECOGNITION ENGINE                 │

## Architecture Diagram│                AI-based Prior Learning Evaluator             │

└─────────────────────────────────────────────────────────────┘

``````

┌─────────────────────────────────────────────────────────────────┐

│                     STREAMLIT WEB APPLICATION                   │## Component Architecture

│                                                                 │

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │```

│  │ Women Leaders│  │  Women's Hub │  │  Mentorship  │        │┌──────────────────────────────────────────────────────────────────┐

│  │   Showcase   │  │ (Scholarships│  │   Matching   │        ││                         STREAMLIT UI (app.py)                    │

│  └──────────────┘  │  Mentorship) │  └──────────────┘        │├──────────────────────────────────────────────────────────────────┤

│                    └──────────────┘                            ││                                                                  │

│                                                                 ││  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        ││  │  Upload CV  │  │  Recognize  │  │ AI Role     │            │

│  │   Industry   │  │ CV Upload &  │  │ Demographic  │        ││  │             │→ │  Skills     │→ │ Matching    │            │

│  │Customization │  │Skill Extract │  │   Profile    │        ││  └─────────────┘  └─────────────┘  └─────────────┘            │

│  └──────────────┘  └──────────────┘  └──────────────┘        ││                                                                  │

│                                                                 ││  ┌─────────────┐  ┌─────────────┐                              │

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        ││  │ Gap Analysis│→ │  Passport   │                              │

│  │  Recognized  │  │  Role Match  │  │  Skill Gap   │        ││  │  & Courses  │  │  Generator  │                              │

│  │    Skills    │  │   Analysis   │  │   Analysis   │        ││  └─────────────┘  └─────────────┘                              │

│  └──────────────┘  └──────────────┘  └──────────────┘        ││                                                                  │

│                                                                 │└──────────────────────────────────────────────────────────────────┘

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │                              ↓

│  │   Equity &   │  │    Skill     │  │  Community   │        │┌──────────────────────────────────────────────────────────────────┐

│  │   Support    │  │   Passport   │  │    Forums    │        ││                    BACKEND LOGIC (utils.py)                      │

│  └──────────────┘  └──────────────┘  └──────────────┘        │├──────────────────────────────────────────────────────────────────┤

└─────────────────────────────────────────────────────────────────┘│                                                                  │

                            ││  ┌──────────────────┐    ┌──────────────────┐                  │

                            ▼│  │ Document Parser  │    │  Skill Extractor │                  │

┌─────────────────────────────────────────────────────────────────┐│  │ • PDF Reader     │    │ • Pattern Match  │                  │

│                     CORE PROCESSING LAYER                       ││  │ • DOCX Reader    │    │ • Keyword Search │                  │

│                        (utils.py)                               ││  │ • PII Remover    │    │ • Ontology Lookup│                  │

│                                                                 ││  └──────────────────┘    └──────────────────┘                  │

│  ┌──────────────────┐    ┌──────────────────┐                ││                                                                  │

│  │ Skill Extraction │    │   Role Matching  │                ││  ┌──────────────────┐    ┌──────────────────┐                  │

│  │   (NLP/spaCy)    │    │  (Cosine Sim)    │                ││  │  NLP Engine      │    │  Role Matcher    │                  │

│  └──────────────────┘    └──────────────────┘                ││  │ • Sentence-BERT  │    │ • Cosine Sim     │                  │

│                                                                 ││  │ • Embeddings     │    │ • Coverage Score │                  │

│  ┌──────────────────┐    ┌──────────────────┐                ││  │ • Vector Compute │    │ • Gap Analysis   │                  │

│  │  Skill Inference │    │ Learning Bridge  │                ││  └──────────────────┘    └──────────────────┘                  │

│  │  (ML Boosting)   │    │ Recommendation   │                ││                                                                  │

│  └──────────────────┘    └──────────────────┘                ││  ┌──────────────────┐    ┌──────────────────┐                  │

│                                                                 ││  │ Course Recomm.   │    │ Passport Gen.    │                  │

│  ┌──────────────────┐    ┌──────────────────┐                ││  │ • Efficiency Calc│    │ • JSON Export    │                  │

│  │ Equity Analysis  │    │ PDF Generation   │                ││  │ • Prerequisites  │    │ • PDF Creation   │                  │

│  │ (Demographics)   │    │  (ReportLab)     │                ││  │ • Path Planning  │    │ • Badge System   │                  │

│  └──────────────────┘    └──────────────────┘                ││  └──────────────────┘    └──────────────────┘                  │

└─────────────────────────────────────────────────────────────────┘│                                                                  │

                            │└──────────────────────────────────────────────────────────────────┘

                            ▼                              ↓

┌─────────────────────────────────────────────────────────────────┐┌──────────────────────────────────────────────────────────────────┐

│                        DATA LAYER                               ││                        DATA LAYER                                │

│                       (JSON Files)                              │├──────────────────────────────────────────────────────────────────┤

│                                                                 ││                                                                  │

│  • skill_ontology.json      - 200+ skills definitions          ││  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │

│  • ai_role_clusters.json    - 20+ AI roles                     ││  │ skill_ontology   │  │ ai_role_clusters │  │ microcreds   │ │

│  • microcredentials.json    - Learning resources               ││  │                  │  │                  │  │              │ │

│  • equity_profiles.json     - Demographic analytics            ││  │ • 20 Hard Skills │  │ • 8 AI Roles     │  │ • 12 Courses │ │

│  • women_in_ai.json         - Leaders, mentors, scholarships   ││  │ • 10 Soft Skills │  │ • Salary Ranges  │  │ • Providers  │ │

│  • industry_customization   - Industry pathways & DEI data     ││  │ • Keywords       │  │ • Requirements   │  │ • Duration   │ │

└─────────────────────────────────────────────────────────────────┘│  │ • Categories     │  │ • Demand Levels  │  │ • Costs      │ │

```│  │                  │  │                  │  │              │ │

│  └──────────────────┘  └──────────────────┘  └──────────────┘ │

## Core Components│                                                                  │

└──────────────────────────────────────────────────────────────────┘

### 1. Frontend Layer (app.py)```



**Navigation System**: 12 main sections accessed via sidebar## Data Flow

- Session state management for user data persistence

- Real-time data visualization with charts and metrics```

- Responsive UI with custom CSS styling┌─────────────┐

│   User      │

**Key Pages**:│  Uploads    │

- **Home & Women Leaders**: Dynamic filtering, leader cards│   CV/Text   │

- **Women's Hub**: Tabbed interface (scholarships, mentorship, communities)└──────┬──────┘

- **Mentorship Matching**: Smart algorithm with weighted scoring       │

- **Industry Customization**: Industry selection and skill translation       ↓

- **CV Upload**: Multiple input methods (file, text, quiz)┌──────────────────┐

- **Demographic Profile**: Optional data collection│ ingest_and_clean │

- **Recognized Skills**: Categorized display with translation│ • Extract text   │

- **Role Matches**: Top 10 roles with equity adjustments│ • Remove PII     │

- **Skill Gap Analysis**: Learning recommendations│ • Normalize      │

- **Equity & Support**: Representation analysis, DEI insights└──────┬───────────┘

- **Skill Passport**: JSON + PDF generation       │

- **Community Forums**: 17 forums with filtering       ↓

┌──────────────────┐

### 2. Processing Layer (utils.py)│ extract_skills   │

│ • Pattern match  │

#### A. Document Processing│ • Ontology look  │

```python│ • Categorize     │

def ingest_and_clean(file) -> str└──────┬───────────┘

```       │

- Extracts text from PDF and DOCX files       ↓

- Handles encoding issues┌──────────────────────┐

- Cleans and normalizes text│ compute_user_vector  │

│ • Embed skills       │

#### B. Skill Extraction│ • Mean pooling       │

```python│ • Create vector      │

def extract_skills(text, ontology_path) -> Dict[str, List[str]]└──────┬───────────────┘

```       │

- Keyword-based matching using skill ontology       ↓

- Returns `{'hard_skills': [...], 'soft_skills': [...]}`┌──────────────────┐

- Matches 200+ predefined skills│  match_roles     │

│ • Cosine sim     │

#### C. Skill Inference (Equity Feature)│ • Coverage calc  │

```python│ • Gap identify   │

def infer_skills_from_background(skills, gender, ethnicity, background) -> List[str]└──────┬───────────┘

```       │

- Adds +30% confidence boost for underrepresented groups       ↓

- Infers transferable skills from non-traditional backgrounds┌──────────────────────┐

- Reduces imposter syndrome by highlighting hidden strengths│ recommend_bridges    │

│ • Find courses       │

#### D. Embedding & Matching│ • Check prereqs      │

```python│ • Rank efficiency    │

def compute_user_vector(skills) -> np.ndarray└──────┬───────────────┘

def match_roles(user_vector, user_skills, role_clusters_path) -> List[Dict]       │

```       ↓

- Uses `sentence-transformers/all-MiniLM-L6-v2` for embeddings┌──────────────────────────┐

- Computes cosine similarity between user and role vectors│ generate_skill_passport  │

- Combined score: 70% similarity + 30% skill coverage│ • Compile data           │

- Returns top 5 roles with gaps and matched skills│ • Create JSON            │

│ • Generate PDF           │

#### E. Learning Recommendations└──────┬───────────────────┘

```python       │

def recommend_bridges(gaps, user_skills, microcreds_path) -> List[Dict]       ↓

```┌──────────────┐

- Matches skill gaps to available courses│  Download    │

- Calculates efficiency score: `gaps_filled / duration_hours`│  Passport    │

- Checks prerequisites and prioritizes high-impact courses└──────────────┘

```

#### F. Equity Analytics

```python## Technology Stack

def calculate_equity_adjusted_salary(salary_range, gender, ethnicity) -> Dict

def get_representation_gap(ethnicity) -> Dict```

```┌─────────────────────────────────────┐

- Gender salary gap: 8-15% (varies by role)│           Frontend Layer            │

- Ethnicity salary gap: 3-5%├─────────────────────────────────────┤

- Shows market range vs. fair target range│ • Streamlit 1.31.0                  │

- Provides negotiation tips│ • Custom CSS                        │

│ • Responsive Layout                 │

#### G. PDF Generation└─────────────────────────────────────┘

```python

def create_pdf_passport(passport, demographic_info, output_path) -> str┌─────────────────────────────────────┐

```│          NLP/ML Layer               │

- Uses ReportLab for professional PDF creation├─────────────────────────────────────┤

- Color-coded sections (Blue, Green, Yellow)│ • Sentence-Transformers 2.3.1       │

- Includes all profile data, skills, roles, gaps, courses│ • Scikit-learn 1.4.0                │

- Achievement badges and verification│ • NumPy 1.26.3                      │

│ • Model: all-MiniLM-L6-v2           │

### 3. Data Layer└─────────────────────────────────────┘



#### skill_ontology.json┌─────────────────────────────────────┐

```json│       Document Processing           │

{├─────────────────────────────────────┤

  "hard_skills": [│ • PyPDF2 3.0.1                      │

    {│ • python-docx 1.1.0                 │

      "id": "python",│ • Regular Expressions               │

      "name": "Python",└─────────────────────────────────────┘

      "category": "programming",

      "keywords": ["python", "py", "pandas", "numpy"]┌─────────────────────────────────────┐

    }│        Data Management              │

  ],├─────────────────────────────────────┤

  "soft_skills": [...]│ • Pandas 2.2.0                      │

}│ • JSON (stdlib)                     │

```│ • Session State                     │

└─────────────────────────────────────┘

#### ai_role_clusters.json

```json┌─────────────────────────────────────┐

{│       Output Generation             │

  "role_id": "ml_engineer",├─────────────────────────────────────┤

  "role_name": "Machine Learning Engineer",│ • FPDF 1.7.2                        │

  "description": "...",│ • ReportLab 4.0.9                   │

  "required_skills": ["python", "tensorflow", "ml", ...],│ • Pillow 10.2.0                     │

  "soft_skills": ["problem_solving", "communication"],└─────────────────────────────────────┘

  "pay_range": "$120,000 - $180,000",```

  "demand": "high"

}## Algorithm Details

```

### Skill Extraction

#### women_in_ai.json```

```jsonInput: CV Text

{  ↓

  "women_leaders": [1. Load Skill Ontology

    {2. Normalize text (lowercase, clean)

      "name": "Dr. Fei-Fei Li",3. For each skill in ontology:

      "title": "Professor of Computer Science",     For each keyword:

      "country": "USA",       If keyword in text:

      "ethnicity": "East Asian",         Add skill to found_skills

      "specialization": "Computer Vision",4. Categorize as hard/soft

      "bio": "...",  ↓

      "achievements": [...],Output: {hard_skills: [...], soft_skills: [...]}

      "keynote_link": "...",```

      "linkedin": "..."

    }### Role Matching

  ],```

  "women_hub": {Input: User Vector, User Skills

    "scholarships": [...],  ↓

    "mentorship_programs": [...],1. For each role in clusters:

    "communities": [...]     a. Get required skills

  },     b. Compute role vector (embed + mean pool)

  "mentors": [     c. Calculate cosine similarity

    {     d. Calculate coverage (matched/required)

      "id": "maya_patel",     e. Combined score = 0.7*similarity + 0.3*coverage

      "name": "Maya Patel",     f. Identify gaps (required - possessed)

      "ethnicity": "South Asian",2. Sort by combined score

      "industry": "Healthcare AI",3. Return top 5

      "story": "200-400 word personal journey...",  ↓

      "available_for": ["Career transition", "Technical mentorship"],Output: [

      "languages": ["English", "Hindi", "Gujarati"]  {role, score, gaps, matches, pay, demand},

    }  ...

  ]]

}```

```

### Bridge Recommendations

#### industry_customization.json```

```jsonInput: Gap Skills, User Skills

{  ↓

  "industries": [1. For each course in catalog:

    {     a. Check if course.bridges_to ∩ gaps ≠ ∅

      "id": "healthcare",     b. Check if course.bridges_from ∩ user_skills ≠ ∅

      "name": "Healthcare & Life Sciences",     c. Calculate efficiency = gaps_filled / (hours + 1)

      "icon": "🏥",     d. Assign priority (High/Medium)

      "ai_applications": ["Medical imaging", "Drug discovery", ...],2. Sort by (has_prereqs, efficiency)

      "key_skills": {3. Return ranked list

        "technical": ["Python", "TensorFlow", "NLP"],  ↓

        "domain": ["Medical terminology", "HIPAA compliance"]Output: [

      },  {course, provider, duration, cost, fills_gaps, priority},

      "skill_translations": {  ...

        "NLP": "Clinical note extraction, medical literature analysis",]

        "Computer Vision": "X-ray/MRI analysis, pathology detection"```

      },

      "roles": ["Clinical AI Scientist", "Healthcare ML Engineer"],## File Structure

      "certifications": ["AI for Medicine (Coursera)", "Healthcare Analytics"],

      "companies": ["Mayo Clinic", "Google Health", ...]```

    }Technation/

  ],│

  "company_dei_insights": [├── app.py                    # Main Streamlit UI (700+ lines)

    {├── utils.py                  # Backend functions (400+ lines)

      "company": "Salesforce",├── requirements.txt          # Dependencies

      "dei_score": 4.7,├── setup.ps1                 # Installation script

      "women_in_tech": 33,├── sample_cv.txt             # Test data

      "underrepresented_minorities": 13.5,│

      "initiatives": ["Equal pay assessments", "BOLDforce ERG", ...],├── .streamlit/

      "parental_leave": "26 weeks",│   └── config.toml           # Theme config

      "flexible_work": "Work from anywhere",│

      "accessibility": "Comprehensive accommodations"├── data/

    }│   ├── skill_ontology.json   # Skills database

  ]│   ├── ai_role_clusters.json # Roles database

}│   └── microcredentials.json # Courses database

```│

├── output/                   # Generated passports

## Data Flow│   ├── skill_passport.json

│   └── skill_passport.pdf

### 1. CV Upload → Skill Recognition│

```└── docs/

User uploads CV    ├── README.md             # Full documentation

    ↓    ├── QUICKSTART.md         # Quick start guide

ingest_and_clean() → Extract text    ├── PROJECT_SUMMARY.md    # Project overview

    ↓    ├── FEATURES.md           # Feature checklist

extract_skills() → Match keywords to ontology    └── ARCHITECTURE.md       # This file

    ↓```

get_skill_names() → Convert IDs to readable names

    ↓## Performance Characteristics

Display categorized skills (hard/soft)

```### Time Complexity

- **Skill Extraction**: O(n*m) where n=text length, m=keyword count

### 2. Role Matching- **Vector Computation**: O(k*384) where k=number of skills

```- **Role Matching**: O(r*s) where r=roles, s=skills per role

Recognized skills- **Bridge Recommendations**: O(c*g) where c=courses, g=gaps

    ↓

compute_user_vector() → Create embeddings (384-dim)### Space Complexity

    ↓- **User Vector**: 384 floats (~1.5KB)

match_roles() → Compare with all role vectors- **Model Cache**: ~80MB (one-time load)

    ↓- **Session State**: ~10-50KB per user

Calculate: similarity (70%) + coverage (30%)- **Data Files**: ~50KB total

    ↓

Return top 5 roles with gaps### Response Times (Estimated)

```- **Document Upload**: 1-3 seconds

- **Skill Extraction**: 0.5-1 second

### 3. Equity Adjustments- **Vector Computation**: 1-2 seconds (first run), 0.1s (cached)

```- **Role Matching**: 0.5-1 second

Demographic info (gender, ethnicity)- **Passport Generation**: 0.5-1 second

    ↓

calculate_equity_adjusted_salary()## Security & Privacy

    ↓

Apply gender gap (8-15%) + ethnicity gap (3-5%)```

    ↓┌──────────────────────────────────┐

Show: typical offer vs. fair target│       Privacy Features           │

```├──────────────────────────────────┤

│ ✓ PII Removal (email, phone)    │

### 4. Skill Gap → Learning Path│ ✓ Local Processing              │

```│ ✓ No Cloud Storage              │

Target role gaps│ ✓ Session-based Data            │

    ↓│ ✓ No Permanent Logs             │

recommend_bridges() → Match gaps to courses└──────────────────────────────────┘

    ↓```

Calculate efficiency = gaps_filled / hours

    ↓## Scalability Considerations

Check prerequisites

    ↓### Current MVP (Single User)

Return top 5 courses with provider, cost, duration- ✓ Streamlit local server

```- ✓ In-memory processing

- ✓ File-based data storage

### 5. Passport Generation

```### Future Scaling (Multi-User)

Collect all data:- → Deploy to Streamlit Cloud / AWS

  - Demographic profile- → Add database (PostgreSQL / MongoDB)

  - Verified skills- → Implement caching (Redis)

  - Role matches- → Add API layer (FastAPI)

  - Skill gaps- → Queue system for batch processing

  - Recommended courses

    ↓---

generate_skill_passport() → Create JSON

    ↓## 🎯 Architecture Benefits

create_pdf_passport() → Generate PDF with ReportLab

    ↓1. **Modular**: Clear separation of concerns

Downloadable files (JSON + PDF)2. **Maintainable**: Easy to update data files

```3. **Extensible**: Add new skills/roles/courses easily

4. **Performant**: Lazy loading and caching

## Key Algorithms5. **User-Friendly**: Intuitive UI flow

6. **Privacy-First**: Local processing, no data retention

### Mentorship Matching Algorithm7. **Customizable**: JSON-based configuration

```python8. **Scalable**: Ready for cloud deployment

score = 0

if user_industry == mentor_industry:---

    score += 3  # Industry match

if user_ethnicity == mentor_ethnicity:**Architecture Status**: ✅ Production-Ready

    score += 2  # Ethnicity match
for interest in user_interests:
    if interest in mentor_specializations:
        score += 1  # Interest overlap
```

### Skill Translation Engine
```python
if industry_selected:
    for skill in user_skills:
        if skill in industry_data['skill_translations']:
            translated = industry_data['skill_translations'][skill]
            # Display: "NLP" → "Clinical note extraction"
```

### Anonymous Mode
```python
if anonymous_mode:
    - Skip demographic data collection
    - Disable inferred skills boost
    - Hide salary equity alerts
    - Hide representation gap analysis
    - Keep skill recognition and role matching
```

## Technology Stack

### Core Libraries
- **Streamlit 1.31.0**: Web framework
- **sentence-transformers 2.3.1**: Skill embeddings
- **spaCy 3.7.2**: NLP processing
- **scikit-learn 1.4.0**: Cosine similarity
- **numpy 1.26.3**: Numerical operations
- **pandas 2.2.0**: Data manipulation

### Document Processing
- **PyPDF2 3.0.1**: PDF parsing
- **python-docx 1.1.0**: DOCX parsing

### PDF Generation
- **reportlab 4.0.9**: Professional PDF creation
- **Pillow 10.2.0**: Image handling

## Performance Considerations

- **Caching**: `@st.cache_data` for JSON loading (women_in_ai, industry_data)
- **Model Loading**: Lazy loading of sentence-transformers model
- **Embeddings**: Pre-computed for role descriptions (not user skills)
- **Session State**: Persistent data across page navigation

## Security & Privacy

- **Local Processing**: No external API calls
- **No Data Storage**: No database, files stored locally
- **Optional Profile**: All demographic data is voluntary
- **Anonymous Mode**: Complete privacy option
- **File Upload**: Max 200MB, CORS disabled for local dev

## Scalability

### Current Limitations
- Single-user local deployment
- In-memory processing
- No database persistence

### Future Enhancements
- Multi-user support with authentication
- PostgreSQL database for persistence
- Cloud deployment (AWS/Azure)
- Real-time mentor booking
- Live forum discussions
- Blockchain credentials

## Error Handling

- Try-catch blocks for file parsing
- Graceful degradation for missing data
- User-friendly error messages
- Debug logging for PDF generation
- Fallback to JSON if PDF fails

## Configuration

### .streamlit/config.toml
```toml
[theme]
primaryColor = "#3B82F6"        # Blue
backgroundColor = "#FFFFFF"      # White
secondaryBackgroundColor = "#F3F4F6"  # Gray
textColor = "#1F2937"           # Dark gray
font = "sans serif"

[server]
headless = false
port = 8501
maxUploadSize = 200             # MB
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

## Deployment

### Local Development
```bash
streamlit run app.py
```

### Production (Example: Streamlit Cloud)
1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy with requirements.txt
4. Add secrets for any API keys (currently none)

---

**Architecture Version**: 2.0  
**Last Updated**: October 29, 2025  
**Maintained by**: TechNation Team
