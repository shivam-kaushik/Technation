# 🏗️ System Architecture

## Overview
```
┌─────────────────────────────────────────────────────────────┐
│                     SKILL RECOGNITION ENGINE                 │
│                AI-based Prior Learning Evaluator             │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         STREAMLIT UI (app.py)                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  Upload CV  │  │  Recognize  │  │ AI Role     │            │
│  │             │→ │  Skills     │→ │ Matching    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐                              │
│  │ Gap Analysis│→ │  Passport   │                              │
│  │  & Courses  │  │  Generator  │                              │
│  └─────────────┘  └─────────────┘                              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│                    BACKEND LOGIC (utils.py)                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐    ┌──────────────────┐                  │
│  │ Document Parser  │    │  Skill Extractor │                  │
│  │ • PDF Reader     │    │ • Pattern Match  │                  │
│  │ • DOCX Reader    │    │ • Keyword Search │                  │
│  │ • PII Remover    │    │ • Ontology Lookup│                  │
│  └──────────────────┘    └──────────────────┘                  │
│                                                                  │
│  ┌──────────────────┐    ┌──────────────────┐                  │
│  │  NLP Engine      │    │  Role Matcher    │                  │
│  │ • Sentence-BERT  │    │ • Cosine Sim     │                  │
│  │ • Embeddings     │    │ • Coverage Score │                  │
│  │ • Vector Compute │    │ • Gap Analysis   │                  │
│  └──────────────────┘    └──────────────────┘                  │
│                                                                  │
│  ┌──────────────────┐    ┌──────────────────┐                  │
│  │ Course Recomm.   │    │ Passport Gen.    │                  │
│  │ • Efficiency Calc│    │ • JSON Export    │                  │
│  │ • Prerequisites  │    │ • PDF Creation   │                  │
│  │ • Path Planning  │    │ • Badge System   │                  │
│  └──────────────────┘    └──────────────────┘                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │ skill_ontology   │  │ ai_role_clusters │  │ microcreds   │ │
│  │                  │  │                  │  │              │ │
│  │ • 20 Hard Skills │  │ • 8 AI Roles     │  │ • 12 Courses │ │
│  │ • 10 Soft Skills │  │ • Salary Ranges  │  │ • Providers  │ │
│  │ • Keywords       │  │ • Requirements   │  │ • Duration   │ │
│  │ • Categories     │  │ • Demand Levels  │  │ • Costs      │ │
│  │                  │  │                  │  │              │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌─────────────┐
│   User      │
│  Uploads    │
│   CV/Text   │
└──────┬──────┘
       │
       ↓
┌──────────────────┐
│ ingest_and_clean │
│ • Extract text   │
│ • Remove PII     │
│ • Normalize      │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ extract_skills   │
│ • Pattern match  │
│ • Ontology look  │
│ • Categorize     │
└──────┬───────────┘
       │
       ↓
┌──────────────────────┐
│ compute_user_vector  │
│ • Embed skills       │
│ • Mean pooling       │
│ • Create vector      │
└──────┬───────────────┘
       │
       ↓
┌──────────────────┐
│  match_roles     │
│ • Cosine sim     │
│ • Coverage calc  │
│ • Gap identify   │
└──────┬───────────┘
       │
       ↓
┌──────────────────────┐
│ recommend_bridges    │
│ • Find courses       │
│ • Check prereqs      │
│ • Rank efficiency    │
└──────┬───────────────┘
       │
       ↓
┌──────────────────────────┐
│ generate_skill_passport  │
│ • Compile data           │
│ • Create JSON            │
│ • Generate PDF           │
└──────┬───────────────────┘
       │
       ↓
┌──────────────┐
│  Download    │
│  Passport    │
└──────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────┐
│           Frontend Layer            │
├─────────────────────────────────────┤
│ • Streamlit 1.31.0                  │
│ • Custom CSS                        │
│ • Responsive Layout                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│          NLP/ML Layer               │
├─────────────────────────────────────┤
│ • Sentence-Transformers 2.3.1       │
│ • Scikit-learn 1.4.0                │
│ • NumPy 1.26.3                      │
│ • Model: all-MiniLM-L6-v2           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│       Document Processing           │
├─────────────────────────────────────┤
│ • PyPDF2 3.0.1                      │
│ • python-docx 1.1.0                 │
│ • Regular Expressions               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│        Data Management              │
├─────────────────────────────────────┤
│ • Pandas 2.2.0                      │
│ • JSON (stdlib)                     │
│ • Session State                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│       Output Generation             │
├─────────────────────────────────────┤
│ • FPDF 1.7.2                        │
│ • ReportLab 4.0.9                   │
│ • Pillow 10.2.0                     │
└─────────────────────────────────────┘
```

## Algorithm Details

### Skill Extraction
```
Input: CV Text
  ↓
1. Load Skill Ontology
2. Normalize text (lowercase, clean)
3. For each skill in ontology:
     For each keyword:
       If keyword in text:
         Add skill to found_skills
4. Categorize as hard/soft
  ↓
Output: {hard_skills: [...], soft_skills: [...]}
```

### Role Matching
```
Input: User Vector, User Skills
  ↓
1. For each role in clusters:
     a. Get required skills
     b. Compute role vector (embed + mean pool)
     c. Calculate cosine similarity
     d. Calculate coverage (matched/required)
     e. Combined score = 0.7*similarity + 0.3*coverage
     f. Identify gaps (required - possessed)
2. Sort by combined score
3. Return top 5
  ↓
Output: [
  {role, score, gaps, matches, pay, demand},
  ...
]
```

### Bridge Recommendations
```
Input: Gap Skills, User Skills
  ↓
1. For each course in catalog:
     a. Check if course.bridges_to ∩ gaps ≠ ∅
     b. Check if course.bridges_from ∩ user_skills ≠ ∅
     c. Calculate efficiency = gaps_filled / (hours + 1)
     d. Assign priority (High/Medium)
2. Sort by (has_prereqs, efficiency)
3. Return ranked list
  ↓
Output: [
  {course, provider, duration, cost, fills_gaps, priority},
  ...
]
```

## File Structure

```
Technation/
│
├── app.py                    # Main Streamlit UI (700+ lines)
├── utils.py                  # Backend functions (400+ lines)
├── requirements.txt          # Dependencies
├── setup.ps1                 # Installation script
├── sample_cv.txt             # Test data
│
├── .streamlit/
│   └── config.toml           # Theme config
│
├── data/
│   ├── skill_ontology.json   # Skills database
│   ├── ai_role_clusters.json # Roles database
│   └── microcredentials.json # Courses database
│
├── output/                   # Generated passports
│   ├── skill_passport.json
│   └── skill_passport.pdf
│
└── docs/
    ├── README.md             # Full documentation
    ├── QUICKSTART.md         # Quick start guide
    ├── PROJECT_SUMMARY.md    # Project overview
    ├── FEATURES.md           # Feature checklist
    └── ARCHITECTURE.md       # This file
```

## Performance Characteristics

### Time Complexity
- **Skill Extraction**: O(n*m) where n=text length, m=keyword count
- **Vector Computation**: O(k*384) where k=number of skills
- **Role Matching**: O(r*s) where r=roles, s=skills per role
- **Bridge Recommendations**: O(c*g) where c=courses, g=gaps

### Space Complexity
- **User Vector**: 384 floats (~1.5KB)
- **Model Cache**: ~80MB (one-time load)
- **Session State**: ~10-50KB per user
- **Data Files**: ~50KB total

### Response Times (Estimated)
- **Document Upload**: 1-3 seconds
- **Skill Extraction**: 0.5-1 second
- **Vector Computation**: 1-2 seconds (first run), 0.1s (cached)
- **Role Matching**: 0.5-1 second
- **Passport Generation**: 0.5-1 second

## Security & Privacy

```
┌──────────────────────────────────┐
│       Privacy Features           │
├──────────────────────────────────┤
│ ✓ PII Removal (email, phone)    │
│ ✓ Local Processing              │
│ ✓ No Cloud Storage              │
│ ✓ Session-based Data            │
│ ✓ No Permanent Logs             │
└──────────────────────────────────┘
```

## Scalability Considerations

### Current MVP (Single User)
- ✓ Streamlit local server
- ✓ In-memory processing
- ✓ File-based data storage

### Future Scaling (Multi-User)
- → Deploy to Streamlit Cloud / AWS
- → Add database (PostgreSQL / MongoDB)
- → Implement caching (Redis)
- → Add API layer (FastAPI)
- → Queue system for batch processing

---

## 🎯 Architecture Benefits

1. **Modular**: Clear separation of concerns
2. **Maintainable**: Easy to update data files
3. **Extensible**: Add new skills/roles/courses easily
4. **Performant**: Lazy loading and caching
5. **User-Friendly**: Intuitive UI flow
6. **Privacy-First**: Local processing, no data retention
7. **Customizable**: JSON-based configuration
8. **Scalable**: Ready for cloud deployment

---

**Architecture Status**: ✅ Production-Ready
