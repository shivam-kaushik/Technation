# 🚀 Enhanced AI Skills Recognition Engine# Skill Recognition Engine - AI-based Prior Learning Evaluator



A comprehensive Streamlit application designed to help **women**, **underrepresented minorities**, and **career changers** transition into AI roles through intelligent skill recognition, personalized career matching, and equity-focused support.A professional AI-powered application that helps individuals (especially women and non-degree professionals) recognize their skills, match to AI-adjacent roles, identify skill gaps, and receive personalized learning recommendations.



## ✨ Key Features## 🎯 Features



### 🏠 **Women Leaders in AI**- **CV/LinkedIn Profile Analysis**: Upload PDF/DOCX or paste text

- Showcase of 8 inspiring female AI leaders with filtering by country, ethnicity, and specialization- **AI Skill Extraction**: Automatically extract hard and soft skills using NLP

- Direct links to keynotes and professional profiles- **Role Matching**: Match users to 8+ AI-adjacent roles using Sentence-BERT embeddings

- **Gap Analysis**: Identify missing skills for target roles

### 👩‍💼 **Women's Hub**- **Bridge Courses**: Recommend micro-credentials to close skill gaps

- **Scholarships**: $25,000+ in opportunities with deadline tracking- **Skill Passport**: Generate downloadable JSON + PDF credentials

- **Mentorship Programs**: 5 free programs with detailed information- **Beautiful UI**: Modern, responsive Streamlit interface with navigation

- **Communities**: Access to 225,000+ members across major tech communities

## 🚀 Quick Start

### 🤝 **Mentorship Matching**

- 8 diverse mentors with personal journey stories (200-400 words each)### Prerequisites

- Smart matching algorithm based on industry, ethnicity, and interests

- Mentors from various backgrounds: Healthcare, Finance, E-commerce, Automotive, and more- Python 3.8 or higher

- pip package manager

### 🏢 **Industry Customization**

- 8 complete industry pathways: Healthcare, Finance, Retail, Manufacturing, Marketing, Automotive, Energy, Telecommunications### Installation

- Skill translation engine: Converts generic skills to industry-specific applications

- 80+ skill translations, 40+ AI applications, and company recommendations1. **Clone or navigate to the project directory**:

```bash

### 🔍 **CV Analysis & Skill Recognition**cd "c:\Users\Public\Documents\My_Projects\Technation"

- Upload PDF/TXT files, paste text, or take a quick skill quiz```

- Extracts technical and soft skills automatically

- Industry-specific skill translation2. **Install required packages**:

```bash

### 🧠 **AI Role Matching**pip install -r requirements.txt

- Top 10 AI role matches with similarity scores```

- Salary range information with equity adjustments

- Shows skill coverage and gaps3. **Download spaCy language model** (optional, for enhanced NER):

```bash

### 📈 **Skill Gap Analysis**python -m spacy download en_core_web_sm

- Identifies missing skills for target roles```

- Recommends specific learning resources with duration, cost, and provider

- Personalized learning paths### Running the Application



### 🌍 **Equity & Support**1. **Start the Streamlit app**:

- Anonymous analysis mode for privacy```bash

- Representation gap analysis (e.g., "Black: 7% in tech vs 13% in population")streamlit run app.py

- Salary equity alerts with negotiation tips (8-15% gender+ethnicity gaps)```

- Company DEI insights: 8 major tech companies scored (3.9-4.7/5)

2. **Open your browser** to the URL shown (typically `http://localhost:8501`)

### 🪪 **Skill Passport**

- Generate comprehensive JSON and PDF passports3. **Start using the app**:

- Includes demographic profile, verified skills, role matches, and learning recommendations   - Upload your CV or paste LinkedIn profile text

- Professional PDF with color-coded sections and achievement badges   - View recognized skills

- Downloadable and shareable with employers   - Explore AI role matches

   - Review skill gaps and recommended courses

### 💬 **Community Forums**   - Generate and download your Skill Passport

- 17 discussion forums across 4 categories:

  - Women in AI (4 forums)## 📁 Project Structure

  - Identity-Based Groups (5 forums)

  - Industry Groups (4 forums)```

  - Skill Level Groups (4 forums)Technation/

├── app.py                          # Main Streamlit application

## 🛠️ Installation├── utils.py                        # Backend logic and NLP functions

├── requirements.txt                # Python dependencies

### Prerequisites├── README.md                       # This file

- Python 3.8 or higher├── data/

- pip package manager│   ├── skill_ontology.json        # Skill taxonomy (20 hard + 10 soft skills)

│   ├── ai_role_clusters.json      # 8 AI-adjacent job roles

### Setup│   └── microcredentials.json      # 12 bridge courses

└── output/                         # Generated passports (auto-created)

1. **Clone the repository**    ├── skill_passport.json

```bash    └── skill_passport.pdf

git clone https://github.com/shivam-kaushik/Technation.git```

cd Technation

```## 🧩 Core Components



2. **Create a virtual environment**### 1. Skill Extraction (`utils.py`)

```bash- **`ingest_and_clean()`**: Extract text from PDF/DOCX, remove PII

python -m venv .venv- **`extract_skills()`**: Pattern-based skill recognition using ontology

```- Uses regex and keyword matching against predefined skill taxonomy



3. **Activate the virtual environment**### 2. Embedding & Matching

- Windows (PowerShell):- **`compute_user_vector()`**: Create Sentence-BERT embeddings for user skills

  ```powershell- **`match_roles()`**: Cosine similarity + skill coverage scoring

  .\.venv\Scripts\Activate.ps1- Returns top 5 matching AI roles with gap analysis

  ```

- Windows (Command Prompt):### 3. Bridge Recommendations

  ```cmd- **`recommend_bridges()`**: Suggest micro-credentials to fill gaps

  .venv\Scripts\activate.bat- Considers prerequisites, duration, and efficiency

  ```- Prioritizes courses based on user's current skills

- macOS/Linux:

  ```bash### 4. Passport Generation

  source .venv/bin/activate- **`generate_skill_passport()`**: Create JSON summary

  ```- **`create_pdf_passport()`**: Generate downloadable PDF certificate



4. **Install dependencies**## 🎨 UI/UX Features

```bash

pip install -r requirements.txt### Navigation Sections:

```1. **🔍 Upload or Paste CV**: File upload, text input, or skill quiz

2. **📋 Recognized Skills**: Colored skill tags (blue=hard, green=soft)

5. **Download spaCy language model**3. **🧠 AI Role Matches**: Top 5 roles with scores and salary ranges

```bash4. **📈 Skill Gap & Bridge Plan**: Missing skills and course recommendations

python -m spacy download en_core_web_sm5. **🏅 Skill Passport & Download**: Generate credentials and download

```

### Design Elements:

6. **Run the application**- **Responsive layout**: Wide mode with sidebar navigation

```bash- **Color-coded tags**: Visual distinction between skill types

streamlit run app.py- **Role cards**: Hover effects and top match highlighting

```- **Progress bars**: Visual representation of match scores

- **Custom CSS**: Professional gradients and shadows

7. **Open in browser**

Navigate to `http://localhost:8501`## 📊 Data Files



## 📊 Data Files### `skill_ontology.json`

- 20 hard skills (Python, SQL, Excel, ML, etc.)

The application uses structured JSON data files located in the `data/` directory:- 10 soft skills (Communication, Leadership, etc.)

- Keywords for pattern matching

- `skill_ontology.json` - Hard and soft skills definitions

- `ai_role_clusters.json` - AI role descriptions and requirements### `ai_role_clusters.json`

- `microcredentials.json` - Learning resources and courses- 8 AI-adjacent roles:

- `equity_profiles.json` - Demographic and equity data  - Data Analyst

- `women_in_ai.json` - Women leaders, scholarships, mentorship programs, and mentors  - AI Marketing Assistant

- `industry_customization.json` - Industry pathways and company DEI insights  - Business Intelligence Trainee

  - Junior Data Scientist

## 🎯 Usage Flow  - AI Operations Coordinator

  - Customer Insights Analyst

1. **Explore Women Leaders** - Get inspired by successful women in AI  - Digital Transformation Assistant

2. **Browse Women's Hub** - Check scholarships and mentorship opportunities  - Junior ML Engineer

3. **Find Your Mentor** - Match with mentors based on your profile

4. **Choose Your Industry** - Select from 8 industry pathways### `microcredentials.json`

5. **Upload Your CV** - Analyze your skills automatically- 12 free/low-cost courses

6. **Fill Demographic Profile** (Optional) - Get personalized equity insights- Duration: 6-30 hours

7. **View Recognized Skills** - See your technical and soft skills- Providers: Coursera, FreeCodeCamp, Microsoft Learn, etc.

8. **Check Role Matches** - Find your best-fit AI roles

9. **Analyze Skill Gaps** - Get learning recommendations## 🔧 Customization

10. **Generate Passport** - Create downloadable skill passport (JSON + PDF)

11. **Join Communities** - Connect with relevant forums### Adding New Skills

Edit `data/skill_ontology.json`:

## 🎨 Features by User Group```json

{

### For Women  "id": "new_skill",

- 8 role models from diverse backgrounds  "name": "New Skill Name",

- $25,000+ in scholarships with deadline tracking  "category": "Category",

- +30% skill confidence boost (inferred skills)  "keywords": ["keyword1", "keyword2"],

- 8-15% salary gap alerts with negotiation tips  "level": "technical"

- Women-focused communities and mentors}

```

### For Diverse Ethnic Groups

- 8 mentors from Black, Hispanic, South Asian, and East Asian backgrounds### Adding New Roles

- Representation gap analysisEdit `data/ai_role_clusters.json`:

- 5% ethnicity salary adjustment calculations```json

- Targeted communities (Black in AI, Latinx in AI, etc.){

- Cultural awareness and bias insights  "role_id": "new_role",

  "role_name": "New Role Name",

### For Career Changers  "description": "Description",

- 8 industry-specific pathways  "icon": "🎯",

- Skill translation (e.g., "Medical knowledge" → "Clinical decision support")  "required_skills": ["skill1", "skill2"],

- Success rates for STEM (75%) and Non-STEM (60%) backgrounds  "soft_skills": ["communication"],

- Domain expertise valued alongside technical skills  "pay_range": "$50,000 - $75,000",

- Self-taught and bootcamp graduate support  "demand": "high"

}

## 🔒 Privacy Features```



- **Anonymous Mode**: Toggle to disable demographic data collection### Adding New Courses

- **Optional Profile**: All demographic information is voluntaryEdit `data/microcredentials.json`:

- **Data Privacy**: No external data sharing```json

- **Local Processing**: All analysis happens on your machine{

  "course_id": "new_course",

## 📈 Technology Stack  "course_name": "Course Name",

  "description": "Description",

- **Frontend**: Streamlit  "duration_hours": 20,

- **ML/NLP**: sentence-transformers, spaCy  "cost": 0,

- **Data Processing**: pandas, numpy, scikit-learn  "provider": "Provider Name",

- **PDF Generation**: reportlab  "bridges_from": ["prerequisite_skill"],

- **Document Parsing**: PyPDF2, python-docx  "bridges_to": ["target_skill"],

  "url": "https://example.com"

## 📁 Project Structure}

```

```

Technation/## 🤝 Use Cases

├── app.py                      # Main Streamlit application

├── utils.py                    # Helper functions and utilities### For Job Seekers:

├── requirements.txt            # Python dependencies- Discover transferable skills from previous experience

├── ARCHITECTURE.md             # System architecture documentation- Identify AI roles matching current capabilities

├── README.md                   # This file- Get personalized upskilling roadmap

├── .streamlit/

│   └── config.toml            # Streamlit configuration### For Career Counselors:

├── data/- Assess client skills objectively

│   ├── skill_ontology.json- Match clients to in-demand roles

│   ├── ai_role_clusters.json- Recommend targeted training

│   ├── microcredentials.json

│   ├── equity_profiles.json### For Employers:

│   ├── women_in_ai.json- Evaluate candidate skill portfolios

│   └── industry_customization.json- Identify internal reskilling opportunities

└── output/- Support diversity hiring initiatives

    └── skill_passport.json     # Generated passports

```## 🔐 Privacy & Security



## 🤝 Contributing- **Local processing**: All data processed on your machine

- **PII removal**: Emails and phone numbers automatically redacted

This project is designed to support underrepresented groups in AI. Contributions are welcome, especially:- **No cloud storage**: CVs not uploaded to external servers

- Additional mentor profiles and success stories- **Session-based**: Data cleared when browser closed

- More industry pathways

- Updated scholarship and community information## 🛠️ Troubleshooting

- Enhanced DEI company data

- Bug fixes and performance improvements### Issue: Model download fails

**Solution**: Manually download Sentence-BERT model:

## 📄 License```python

from sentence_transformers import SentenceTransformer

MIT License - See LICENSE file for detailsmodel = SentenceTransformer('all-MiniLM-L6-v2')

```

## 🙏 Acknowledgments

### Issue: PDF extraction fails

- Built for women, underrepresented minorities, and career changers entering AI**Solution**: Ensure PyPDF2 is installed:

- Inspired by the need for equitable access to AI careers```bash

- Data sources: Public company reports, community aggregations, and curated resourcespip install PyPDF2 --upgrade

```

## 📞 Support

### Issue: DOCX extraction fails

For issues, questions, or suggestions:**Solution**: Install python-docx:

- Open an issue on GitHub```bash

- Contact: shivam-kaushik (GitHub)pip install python-docx

```

---

## 📈 Future Enhancements

**Made with ❤️ for diversity and inclusion in AI**

- [ ] Support for more file formats (TXT, RTF)

© 2025 TechNation | Empowering underrepresented talent in AI- [ ] Integration with LinkedIn API

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
