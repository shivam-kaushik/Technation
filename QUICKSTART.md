# 🚀 Quick Start Guide

## Run the App in 3 Steps

### Step 1: Open Terminal
Open PowerShell in VS Code or Windows Terminal

### Step 2: Navigate to Project
```powershell
cd "c:\Users\Public\Documents\My_Projects\Technation"
```

### Step 3: Run the App
```powershell
# Option A: Using the virtual environment (fastest)
.\.venv-1\Scripts\python.exe -m streamlit run app.py

# Option B: Using system Python
python -m streamlit run app.py
```

### Step 4: Open Browser
The app will automatically open at: **http://localhost:8501**

If it doesn't open automatically, manually navigate to that URL.

---

## 📝 Test the App

### Test with Sample CV
1. Click "Upload or Paste CV" in the sidebar
2. Scroll down and paste the contents of `sample_cv.txt`
3. Click "🚀 Extract Skills"
4. Navigate through sections to see results

### Test with File Upload
1. Have a PDF or DOCX resume ready
2. Click "Choose a PDF or DOCX file"
3. Upload your file
4. Click "🚀 Extract Skills"

### Test with Skill Quiz
1. Check "❓ No CV? Take Quick Skill Quiz"
2. Select skills from the dropdown
3. Choose comfort level
4. Click "🚀 Extract Skills"

---

## 🎯 What to Expect

### Section 1: Upload
- Upload interface with file uploader and text box
- Quick skill quiz option
- Extract Skills button

### Section 2: Recognized Skills
- Blue tags for technical skills
- Green tags for soft skills
- Edit functionality
- Statistics

### Section 3: AI Role Matches
- Top 5 matching roles
- Match scores with progress bars
- Salary ranges
- Best match highlighted in gold

### Section 4: Skill Gap & Bridge Plan
- Missing skills list
- Recommended courses
- Duration and cost info
- Learning path progress

### Section 5: Skill Passport
- Summary metrics
- Generate button
- Download JSON and PDF
- Badges earned

---

## ⚠️ Troubleshooting

### Issue: App won't start
**Solution**: Make sure all packages are installed:
```powershell
pip install -r requirements.txt
```

### Issue: Import errors
**Solution**: Use the virtual environment:
```powershell
.\.venv-1\Scripts\python.exe -m streamlit run app.py
```

### Issue: Port already in use
**Solution**: Kill existing Streamlit processes or use a different port:
```powershell
streamlit run app.py --server.port 8502
```

### Issue: Model download fails
**Solution**: First run will download Sentence-BERT model (~100MB). This may take a few minutes. Be patient!

---

## 🎨 Customization

### Change Colors
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#3B82F6"  # Change this
backgroundColor = "#FFFFFF"
```

### Add Skills
Edit `data/skill_ontology.json`:
```json
{
  "id": "new_skill",
  "name": "New Skill",
  "keywords": ["keyword1", "keyword2"]
}
```

### Add Roles
Edit `data/ai_role_clusters.json`

### Add Courses
Edit `data/microcredentials.json`

---

## 📊 Sample Workflow

1. **Start App** → Open http://localhost:8501
2. **Upload CV** → Use sample_cv.txt or your own
3. **View Skills** → Check extracted skills (should see ~10-15)
4. **See Matches** → View top AI roles (Data Analyst likely #1)
5. **Check Gaps** → See missing skills for target role
6. **Review Courses** → Get bridge course recommendations
7. **Generate Passport** → Download your credentials

---

## 🎉 You're All Set!

The Skill Recognition Engine is fully functional and ready to use.

Enjoy exploring AI career opportunities! 🚀
