# 🧪 Testing Guide - All New Features

## Quick Test Scenarios for Each Feature

---

## 🏠 Test 1: Women Leaders in AI

### Steps:
1. Navigate to **"🏠 Home & Women Leaders"**
2. View all 8 leader profiles by default
3. **Filter Test 1**: Select Country = "USA"
   - Expected: 6 leaders shown (Fei-Fei Li, Timnit Gebru, Joy Buolamwini, Cynthia Breazeal, Ayanna Howard, Kate Crawford)
4. **Filter Test 2**: Select Ethnicity = "Black"
   - Expected: 4 leaders shown (Timnit Gebru, Joy Buolamwini, Ayanna Howard, Rediet Abebe)
5. **Filter Test 3**: Select Specialization = "AI Ethics"
   - Expected: 1 leader shown (Timnit Gebru)
6. **Click Links**: Click "Watch Keynote" and "LinkedIn" buttons
   - Expected: Opens placeholder URLs in new tab

### What to Check:
- ✅ Purple gradient cards display correctly
- ✅ Photos show (placeholder images)
- ✅ Achievements list properly formatted
- ✅ Filters work independently and together
- ✅ "Showing X leader(s)" count updates

---

## 👩‍💼 Test 2: Women's Hub

### Tab 1: Scholarships

#### Steps:
1. Navigate to **"👩‍💼 Women's Hub"**
2. Click **"💰 Scholarships"** tab
3. Check all 5 scholarship cards
4. Verify deadline color coding:
   - Women Techmakers (Dec 15, 2025) - Should be orange/red
   - AnitaB.org (Nov 30, 2025) - Should be orange/red
   - Break Through Tech (Oct 31, 2025) - Should be red (likely passed)
5. **Test Email Alert**: Enter email, click "Subscribe to Alerts"
   - Expected: Success message appears

#### What to Check:
- ✅ Days remaining calculated correctly
- ✅ Color coding matches urgency
- ✅ "Apply Now" buttons link correctly
- ✅ Amount and provider clearly visible

### Tab 2: Mentorship Programs

#### Steps:
1. Click **"🤝 Mentorship Programs"** tab
2. Review all 5 programs
3. Check duration, cost, target audience
4. Click "Apply Now" links

#### What to Check:
- ✅ Purple gradient cards
- ✅ All programs show "Free" cost
- ✅ Application links functional

### Tab 3: Communities

#### Steps:
1. Click **"🌐 Communities"** tab
2. View all 5 communities
3. Check member counts
4. Click "Join Community" links

#### What to Check:
- ✅ Pink gradient design
- ✅ 2-column layout responsive
- ✅ Member counts visible

---

## 🤝 Test 3: Mentorship Matching

### Scenario 1: Healthcare Match

#### Steps:
1. Navigate to **"🤝 Mentorship Matching"**
2. Select:
   - **Industry**: Healthcare
   - **Ethnicity**: South Asian
   - **Career Stage**: Mid Career
   - **Help With**: Career transition, Technical skills
3. Click **"🔍 Find Matching Mentors"**

#### Expected Result:
- **Maya Patel** should be top match (South Asian, Healthcare, 15 years experience)
- Full story displayed with pink border
- Shows: Photo, experience, industry, specializations, languages, story, "I can help with" section

### Scenario 2: Career Break Match

#### Steps:
1. Select:
   - **Industry**: Technology
   - **Career Stage**: Career Changer
   - **Help With**: Work-life balance, Career transition
2. Click **"🔍 Find Matching Mentors"**

#### Expected Result:
- **Sarah Thompson** should rank high (career break expert)

### Scenario 3: Black in Finance Match

#### Steps:
1. Select:
   - **Industry**: Finance
   - **Ethnicity**: Black
   - **Help With**: Overcoming bias, Salary negotiation
2. Click **"🔍 Find Matching Mentors"**

#### Expected Result:
- **Keisha Williams** should be top match (Black, Goldman Sachs)

#### What to Check:
- ✅ Matching algorithm prioritizes correct mentors
- ✅ Mentor cards have 200x200px photos
- ✅ Full personal stories display (200-400 words)
- ✅ "I can help with" lists shown
- ✅ Languages and timezone visible

---

## 🏢 Test 4: Industry Customization

### Test Healthcare Industry

#### Steps:
1. Navigate to **"🏢 Industry Customization"**
2. Select **"🏥 Healthcare & Life Sciences"**
3. Review:
   - AI applications (7 listed)
   - Key skills (technical + domain)
   - Target roles (5 roles)
   - Learning pathway visualization
   - Top companies (7 companies)

#### What to Check:
- ✅ Blue gradient header with 🏥 icon
- ✅ 3-column layout for AI applications
- ✅ 2-column layout for skills
- ✅ 3-stage pathway: Learn → Build → Launch
- ✅ Top 3 certifications displayed
- ✅ 4-column grid for companies

### Test Finance Industry

#### Steps:
1. Select **"💰 Finance & Banking"**
2. Compare skill translations:
   - ML should translate to "Credit scoring, fraud pattern detection"
   - NLP should translate to "News sentiment analysis"
3. Check companies: Should include Goldman Sachs, Two Sigma, Citadel

### Test All 8 Industries

Quick check that all load:
- ✅ Healthcare 🏥
- ✅ Finance 💰
- ✅ Retail 🛒
- ✅ Manufacturing 🏭
- ✅ Marketing 📢
- ✅ Automotive 🚗
- ✅ Energy ⚡
- ✅ Telecommunications 📡

---

## 🔒 Test 5: Anonymous Analysis Mode

### Scenario: Compare Biased vs. Unbiased

#### Part A: With Demographics (Biased)
1. **Turn OFF** anonymous mode (uncheck sidebar)
2. Navigate to **"👤 Demographic Profile"**
3. Enter:
   - Gender: Woman
   - Ethnicity: Black or African American
   - Background: Non-STEM
4. Click **"💾 Save Demographic Profile"**
5. Upload CV (or paste text)
6. Go to **"✨ Recognized Skills"**
   - Expected: See "⭐ Skills You Likely Have" section
7. Go to **"🧠 AI Role Matches"**
   - Expected: See salary equity alerts (8-15% gap warnings)

#### Part B: With Anonymous Mode (Unbiased)
1. **Turn ON** anonymous mode (check sidebar)
2. Verify sidebar shows: "🔒 Anonymous mode active"
3. Navigate to **"👤 Demographic Profile"**
   - Expected: Warning shown, data not collected
4. Go to **"✨ Recognized Skills"**
   - Expected: NO inferred skills section
5. Go to **"🧠 AI Role Matches"**
   - Expected: NO equity alerts

#### What to Check:
- ✅ Anonymous mode persists across pages
- ✅ Demographics blocked when active
- ✅ Inferred skills disappear
- ✅ Salary alerts disappear
- ✅ Sidebar info banner shows

---

## 🏢 Test 6: Company DEI Insights

### Steps:
1. Navigate to **"🌍 Equity & Support"**
2. Fill demographic profile first (if not done)
3. Scroll to **"🏢 Detailed Company DEI Insights"**
4. Check all 8 companies displayed

### Expected Results:

#### Salesforce (Top Score)
- DEI Score: 4.7/5 - **GREEN** indicator
- Women in Tech: 33%
- URM: 13.5%
- Parental Leave: 26 weeks (highest)

#### Amazon (Lower Score)
- DEI Score: 3.9/5 - **ORANGE** indicator
- Women in Tech: 26%
- URM: 11.1%

### What to Check:
- ✅ Score color coding: Green (≥4.5), Orange (≥4.0)
- ✅ Large score badge (top right)
- ✅ Initiative tags display as blue pills
- ✅ Benefits section has green background
- ✅ 5 companies shown by default

---

## 💬 Test 7: Community Forums

### Steps:
1. Navigate to **"💬 Community Forums"**
2. Expand each category:
   - 👩‍💼 Women in AI (4 forums)
   - 🌍 Identity-Based Groups (5 forums)
   - 🏢 Industry Groups (4 forums)
   - 🎓 Skill Level (4 forums)
3. Click **"Join [Forum Name]"** for any forum
   - Expected: Success message "✅ Joined [Forum]! Welcome to the community."

### What to Check:
- ✅ Total 17 forums across 4 categories
- ✅ Each forum shows member count, discussion count
- ✅ Blue "Active" and yellow "Moderated" badges
- ✅ Join buttons functional
- ✅ Community Guidelines displayed at bottom

---

## 🎯 Test 8: Complete User Journey

### Scenario: Latina Woman, Non-STEM, Transitioning to Retail AI

#### Step-by-Step Journey:

1. **🏠 Home & Women Leaders**
   - Filter Ethnicity: "Hispanic or Latino"
   - View: Dr. Sofia Rodriguez (Director at Amazon)
   - Click her LinkedIn

2. **👩‍💼 Women's Hub → Scholarships**
   - Apply for "Women in AI Awards" ($5,000)
   - Subscribe to alerts with email

3. **🤝 Mentorship Matching**
   - Industry: Retail
   - Ethnicity: Hispanic/Latino
   - Help With: Career switching, First-gen support
   - Get matched with: **Maria Gonzalez** (Latina, Target, career switcher)

4. **🏢 Industry Customization**
   - Select: "🛒 Retail & E-commerce"
   - Review skill translations:
     - ML → Product recommendations, demand forecasting
   - Note companies: Amazon, Walmart Labs, Target

5. **👤 Demographic Profile**
   - Gender: Woman
   - Ethnicity: Hispanic or Latino
   - Background: Non-STEM
   - Save profile

6. **🔍 Upload CV & Analyze**
   - Paste sample text:
     ```
     Marketing Manager with 8 years experience in campaign management, 
     customer analytics, Excel, and SQL. Led teams of 5-10 people. 
     Bilingual (English/Spanish). Business degree from state university.
     ```
   - Click "🔍 Analyze Skills"

7. **✨ Recognized Skills**
   - Check for inferred skills (should add ML-related skills)
   - See bilingual advantage highlighted

8. **🧠 AI Role Matches**
   - Top matches should include: Customer Analytics Lead, E-commerce ML Engineer
   - Check salary equity alerts (8% gender gap + ethnicity adjustment)
   - See "Negotiate for fair market range" tip

9. **🌍 Equity & Support**
   - View representation gap: "8% in tech vs 18% in population"
   - See communities: Latinos in Tech, SHPE, Techqueria
   - Scroll to Company DEI Insights
   - Identify Target, Amazon as good matches

10. **💬 Community Forums**
    - Join: "Latinx in AI"
    - Join: "Retail & E-commerce AI"
    - Join: "Career Changers (Non-STEM to AI)"

11. **🪪 Skill Passport**
    - Generate passport
    - Download JSON

#### Expected Outcome:
- ✅ Complete personalized journey
- ✅ Found role model (Sofia Rodriguez)
- ✅ Applied for scholarship
- ✅ Matched with mentor (Maria Gonzalez)
- ✅ Industry pathway clear (Retail AI)
- ✅ Skills translated to industry context
- ✅ Equity gaps identified (15-16% combined)
- ✅ Support resources found (3+ communities)
- ✅ DEI companies identified (Target, Amazon)
- ✅ Joined 3 forums
- ✅ Skill passport generated

---

## 🔍 Test 9: Skill Translation Feature

### Steps:
1. Select Industry: **"🏥 Healthcare & Life Sciences"**
2. Upload CV with text:
   ```
   Data Analyst with Python, SQL, Machine Learning, and NLP experience.
   Built predictive models for customer churn. Worked with Excel and Tableau.
   ```
3. Go to **"✨ Recognized Skills"**
4. Scroll to **"🏢 Your Skills in Healthcare & Life Sciences"** section

### Expected Translation:
- **Machine Learning** → "Patient outcome prediction, readmission risk modeling"
- **NLP** → "Clinical note extraction, medical literature analysis, symptom parsing"
- **Data Analysis** → "Electronic health record mining, clinical trial data analysis"

### What to Check:
- ✅ Green-bordered translation boxes
- ✅ Format: "Original Skill → Industry Application"
- ✅ Only translated skills shown (not generic ones)

---

## 📊 Test 10: Equity Salary Adjustments

### Scenario: Black Woman in Healthcare AI

#### Steps:
1. **Demographic Profile**:
   - Gender: Woman (92% adjustment)
   - Ethnicity: Black or African American (95% adjustment)
   - Background: Non-AI STEM (75% success rate)

2. **Upload CV** with healthcare experience

3. **Go to Role Matches**

4. **Select Role** with salary: "$100,000 - $150,000"

### Expected Calculations:
- **Market Range**: $100,000 - $150,000 (unchanged)
- **Typical Offer Range**: $87,000 - $130,500 (0.92 × 0.95 = 0.874 adjustment)
- **Target Fair Range**: $100,000 - $150,000 (no adjustment)
- **Negotiation Tip**: "⚠️ You may be offered 13% less due to combined gender and ethnicity pay gaps. Negotiate firmly for the market range. Use sites like Glassdoor, Levels.fyi, and Blind to research fair compensation."

### What to Check:
- ✅ Three salary ranges displayed
- ✅ Combined adjustment calculated correctly (8% + 5% = ~13%)
- ✅ Negotiation tip appears with warning icon
- ✅ Tip mentions specific resources (Glassdoor, Levels.fyi, Blind)

---

## 🐛 Common Issues to Check

### Issue 1: Data Files Not Found
**Symptom**: Error loading women_in_ai.json or industry_customization.json  
**Fix**: Ensure files exist in `data/` directory  
**Test**: Check file paths are correct

### Issue 2: Anonymous Mode Not Persisting
**Symptom**: Mode resets when changing pages  
**Fix**: Verify `st.session_state.anonymous_mode` used correctly  
**Test**: Toggle on, navigate to 3 different pages, check sidebar

### Issue 3: Mentor Matching Returns Empty
**Symptom**: "No matches found"  
**Fix**: Check matching algorithm logic, ensure at least partial matches  
**Test**: Try different combinations of filters

### Issue 4: Skill Translation Not Showing
**Symptom**: Translation section missing  
**Fix**: Ensure industry selected before uploading CV  
**Test**: Select industry FIRST, then upload CV

### Issue 5: DEI Cards Not Displaying
**Symptom**: Company cards not showing  
**Fix**: Verify `load_industry_data()` returns correct structure  
**Test**: Check JSON structure matches code expectations

---

## ✅ Final Checklist

Before considering testing complete, verify:

- [ ] All 12 navigation items work
- [ ] All 8 women leaders display with filters
- [ ] All 5 scholarships show correct deadlines
- [ ] All 5 mentorship programs load
- [ ] All 8 mentors have complete stories
- [ ] Mentorship matching returns relevant results
- [ ] All 8 industries load with correct icons
- [ ] Skill translation works for at least 3 skills
- [ ] Anonymous mode toggles correctly
- [ ] Demographic profile saves and persists
- [ ] Inferred skills appear when demographics provided
- [ ] Salary equity alerts show with correct percentages
- [ ] All 8 company DEI cards display
- [ ] All 17 forum categories present
- [ ] Forum join buttons work
- [ ] Skill passport generates successfully

---

## 🎉 Success Criteria

**All features tested successfully when**:
1. ✅ No error messages in console
2. ✅ All pages load within 2 seconds
3. ✅ Filters produce expected results
4. ✅ Matching algorithm returns relevant mentors
5. ✅ Translations are accurate and contextual
6. ✅ Anonymous mode properly blocks demographic features
7. ✅ Salary calculations mathematically correct
8. ✅ All external links open in new tabs
9. ✅ UI is responsive on different screen sizes
10. ✅ No broken images or missing data

**MVP is production-ready!** 🚀
