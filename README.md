# Skill Recognition Engine - AI-based Prior Learning Evaluator

A professional AI-powered application that helps individuals (especially women and non-degree professionals) recognize their skills, match to AI-adjacent roles, identify skill gaps, and receive personalized learning recommendations.

## 🎯 Features

- **CV/LinkedIn Profile Analysis**: Upload PDF/DOCX or paste text
- **AI Skill Extraction**: Automatically extract hard and soft skills using NLP
- **Role Matching**: Match users to 8+ AI-adjacent roles using Sentence-BERT embeddings
- **Gap Analysis**: Identify missing skills for target roles
- **Bridge Courses**: Recommend micro-credentials to close skill gaps
- **Skill Passport**: Generate downloadable JSON + PDF credentials
- **Beautiful UI**: Modern, responsive Streamlit interface with navigation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory**:
```bash
cd "c:\Users\Public\Documents\My_Projects\Technation"
```

2. **Install required packages**:
```bash
pip install -r requirements.txt
```

3. **Download spaCy language model** (optional, for enhanced NER):
```bash
python -m spacy download en_core_web_sm
```

### Running the Application

1. **Start the Streamlit app**:
```bash
streamlit run app.py
```

2. **Open your browser** to the URL shown (typically `http://localhost:8501`)

3. **Start using the app**:
   - Upload your CV or paste LinkedIn profile text
   - View recognized skills
   - Explore AI role matches
   - Review skill gaps and recommended courses
   - Generate and download your Skill Passport

## 📁 Project Structure

```
Technation/
├── app.py                          # Main Streamlit application
├── utils.py                        # Backend logic and NLP functions
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data/
│   ├── skill_ontology.json        # Skill taxonomy (20 hard + 10 soft skills)
│   ├── ai_role_clusters.json      # 8 AI-adjacent job roles
│   └── microcredentials.json      # 12 bridge courses
└── output/                         # Generated passports (auto-created)
    ├── skill_passport.json
    └── skill_passport.pdf
```

## 🧩 Core Components

### 1. Skill Extraction (`utils.py`)
- **`ingest_and_clean()`**: Extract text from PDF/DOCX, remove PII
- **`extract_skills()`**: Pattern-based skill recognition using ontology
- Uses regex and keyword matching against predefined skill taxonomy

### 2. Embedding & Matching
- **`compute_user_vector()`**: Create Sentence-BERT embeddings for user skills
- **`match_roles()`**: Cosine similarity + skill coverage scoring
- Returns top 5 matching AI roles with gap analysis

### 3. Bridge Recommendations
- **`recommend_bridges()`**: Suggest micro-credentials to fill gaps
- Considers prerequisites, duration, and efficiency
- Prioritizes courses based on user's current skills

### 4. Passport Generation
- **`generate_skill_passport()`**: Create JSON summary
- **`create_pdf_passport()`**: Generate downloadable PDF certificate

## 🎨 UI/UX Features

### Navigation Sections:
1. **🔍 Upload or Paste CV**: File upload, text input, or skill quiz
2. **📋 Recognized Skills**: Colored skill tags (blue=hard, green=soft)
3. **🧠 AI Role Matches**: Top 5 roles with scores and salary ranges
4. **📈 Skill Gap & Bridge Plan**: Missing skills and course recommendations
5. **🏅 Skill Passport & Download**: Generate credentials and download

### Design Elements:
- **Responsive layout**: Wide mode with sidebar navigation
- **Color-coded tags**: Visual distinction between skill types
- **Role cards**: Hover effects and top match highlighting
- **Progress bars**: Visual representation of match scores
- **Custom CSS**: Professional gradients and shadows

## 📊 Data Files

### `skill_ontology.json`
- 20 hard skills (Python, SQL, Excel, ML, etc.)
- 10 soft skills (Communication, Leadership, etc.)
- Keywords for pattern matching

### `ai_role_clusters.json`
- 8 AI-adjacent roles:
  - Data Analyst
  - AI Marketing Assistant
  - Business Intelligence Trainee
  - Junior Data Scientist
  - AI Operations Coordinator
  - Customer Insights Analyst
  - Digital Transformation Assistant
  - Junior ML Engineer

### `microcredentials.json`
- 12 free/low-cost courses
- Duration: 6-30 hours
- Providers: Coursera, FreeCodeCamp, Microsoft Learn, etc.

## 🔧 Customization

### Adding New Skills
Edit `data/skill_ontology.json`:
```json
{
  "id": "new_skill",
  "name": "New Skill Name",
  "category": "Category",
  "keywords": ["keyword1", "keyword2"],
  "level": "technical"
}
```

### Adding New Roles
Edit `data/ai_role_clusters.json`:
```json
{
  "role_id": "new_role",
  "role_name": "New Role Name",
  "description": "Description",
  "icon": "🎯",
  "required_skills": ["skill1", "skill2"],
  "soft_skills": ["communication"],
  "pay_range": "$50,000 - $75,000",
  "demand": "high"
}
```

### Adding New Courses
Edit `data/microcredentials.json`:
```json
{
  "course_id": "new_course",
  "course_name": "Course Name",
  "description": "Description",
  "duration_hours": 20,
  "cost": 0,
  "provider": "Provider Name",
  "bridges_from": ["prerequisite_skill"],
  "bridges_to": ["target_skill"],
  "url": "https://example.com"
}
```

## 🤝 Use Cases

### For Job Seekers:
- Discover transferable skills from previous experience
- Identify AI roles matching current capabilities
- Get personalized upskilling roadmap

### For Career Counselors:
- Assess client skills objectively
- Match clients to in-demand roles
- Recommend targeted training

### For Employers:
- Evaluate candidate skill portfolios
- Identify internal reskilling opportunities
- Support diversity hiring initiatives

## 🔐 Privacy & Security

- **Local processing**: All data processed on your machine
- **PII removal**: Emails and phone numbers automatically redacted
- **No cloud storage**: CVs not uploaded to external servers
- **Session-based**: Data cleared when browser closed

## 🛠️ Troubleshooting

### Issue: Model download fails
**Solution**: Manually download Sentence-BERT model:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
```

### Issue: PDF extraction fails
**Solution**: Ensure PyPDF2 is installed:
```bash
pip install PyPDF2 --upgrade
```

### Issue: DOCX extraction fails
**Solution**: Install python-docx:
```bash
pip install python-docx
```

## 📈 Future Enhancements

- [ ] Support for more file formats (TXT, RTF)
- [ ] Integration with LinkedIn API
- [ ] Real-time job market data
- [ ] Multi-language support
- [ ] Advanced NER with spaCy models
- [ ] Interactive skill visualization graphs
- [ ] Email delivery of Skill Passport
- [ ] Certification blockchain integration

## 📝 License

This project is developed as a prototype for equitable career recognition. Free to use for educational and non-commercial purposes.

## 👥 Credits

**Developed by**: EquiForce AI Team  
**Powered by**: EquiForce AI Dataset  
**Purpose**: Empowering women and non-degree professionals to discover their AI potential

---

**Contact**: For questions or feedback, please reach out to your project supervisor or technical lead.

**Version**: 1.0.0 (October 2025)
