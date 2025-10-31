"""
Skill Recognition Engine - Enhanced with Women in AI, Industry Customization, and Inclusivity Features
A comprehensive Streamlit application for skill recognition and career matching with DEI focus
"""

# Disable TensorFlow to avoid compatibility issues
import os
os.environ['USE_TF'] = 'NO'
os.environ['TRANSFORMERS_NO_TF'] = '1'

import streamlit as st
import json
import os
from datetime import datetime, timedelta
from utils import (
    ingest_and_clean,
    extract_skills,
    compute_user_vector,
    match_roles,
    recommend_bridges,
    generate_skill_passport,
    create_pdf_passport,
    get_skill_names,
    get_demographic_profile,
    calculate_equity_adjusted_salary,
    enhance_skills_with_confidence,
    get_targeted_role_recommendations,
    get_support_resources,
    generate_confidence_message,
    analyze_representation_gap
)

# ============================================================================
# HELPER FUNCTIONS FOR NEW FEATURES
# ============================================================================

@st.cache_data
def load_women_in_ai_data():
    """Load women leaders, mentors, and hub data"""
    with open('data/women_in_ai.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def load_industry_data():
    """Load industry customization and DEI insights"""
    with open('data/industry_customization.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def filter_women_leaders(leaders, country=None, ethnicity=None, specialization=None):
    """Filter women leaders based on criteria"""
    filtered = leaders
    if country and country != "All":
        filtered = [l for l in filtered if country.lower() in l['country'].lower()]
    if ethnicity and ethnicity != "All":
        filtered = [l for l in filtered if ethnicity == l['ethnicity']]
    if specialization and specialization != "All":
        filtered = [l for l in filtered if specialization in l['specialization']]
    return filtered

def display_leader_card(leader):
    """Display a women leader profile card"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; padding: 1.5rem; margin: 1rem 0; color: white;">
        <div style="display: flex; align-items: start; gap: 1rem;">
            <div style="flex-shrink: 0;">
                <img src="{leader['photo_url']}" style="width: 100px; height: 100px; 
                     border-radius: 50%; border: 3px solid white; object-fit: cover;" />
            </div>
            <div style="flex-grow: 1;">
                <h3 style="margin: 0; color: white;">{leader['name']}</h3>
                <p style="margin: 0.3rem 0; font-size: 1.1rem; opacity: 0.9;">
                    {leader['title']}
                </p>
                <p style="margin: 0.5rem 0; font-size: 0.9rem;">
                    🌍 {leader['country']} | 🎯 {leader['specialization']}
                </p>
                <p style="margin: 0.3rem 0; font-size: 0.85rem; opacity: 0.95;">
                    ✉️ {leader.get('email', 'Not available')}
                </p>
            </div>
        </div>
        <p style="margin: 1rem 0; line-height: 1.6;">{leader['bio']}</p>
        <div style="margin-top: 1rem;">
            <strong>Key Achievements:</strong>
            <ul style="margin: 0.5rem 0;">
                {''.join([f"<li>{achievement}</li>" for achievement in leader['achievements']])}
            </ul>
        </div>
        <div style="margin-top: 1rem; display: flex; gap: 1rem;">
            <a href="{leader['keynote_link']}" target="_blank" 
               style="background: white; color: #667eea; padding: 0.5rem 1rem; 
                      border-radius: 8px; text-decoration: none; font-weight: 500;">
                🎥 Watch Keynote
            </a>
            <a href="{leader['linkedin']}" target="_blank"
               style="background: white; color: #667eea; padding: 0.5rem 1rem; 
                      border-radius: 8px; text-decoration: none; font-weight: 500;">
                💼 LinkedIn
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_mentor_card(mentor):
    """Display a mentor profile card with their story"""
    st.markdown(f"""
    <div style="background: white; border: 3px solid #f472b6; 
                border-radius: 15px; padding: 2rem; margin: 1rem 0;">
        <div style="display: flex; align-items: start; gap: 1.5rem;">
            <div style="flex-shrink: 0;">
                <img src="{mentor['photo_url']}" style="width: 150px; height: 150px; 
                     border-radius: 15px; border: 3px solid #f472b6; object-fit: cover;" />
            </div>
            <div style="flex-grow: 1;">
                <h2 style="margin: 0; color: #be185d;">{mentor['name']}</h2>
                <p style="margin: 0.5rem 0; font-size: 1.2rem; color: #831843; font-weight: 600;">
                    {mentor['current_role']} at {mentor['company']}
                </p>
                <p style="margin: 0.5rem 0; color: #666;">
                    🌍 {mentor['industry']} | 💼 {mentor['experience_years']} years experience
                </p>
                <p style="margin: 0.3rem 0; font-size: 0.9rem; color: #666;">
                    ✉️ {mentor.get('email', 'Contact via platform')}
                </p>
                <div style="margin: 0.5rem 0;">
                    <strong>Specializations:</strong> {', '.join(mentor['specializations'])}
                </div>
                <div style="margin: 0.5rem 0;">
                    <strong>Languages:</strong> {', '.join(mentor['languages'])} | 
                    <strong>Timezone:</strong> {mentor['timezone']}
                </div>
            </div>
        </div>
        <div style="background: #fce7f3; border-left: 4px solid #f472b6; 
                    padding: 1.5rem; margin: 1.5rem 0; border-radius: 8px;">
            <h4 style="margin: 0 0 1rem 0; color: #be185d;">📖 My Story</h4>
            <p style="line-height: 1.8; color: #333; font-size: 1.05rem;">{mentor['story']}</p>
        </div>
        <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <strong style="color: #166534;">I can help with:</strong>
            <ul style="margin: 0.5rem 0; color: #15803d;">
                {''.join([f"<li>{item}</li>" for item in mentor['available_for']])}
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_scholarship_card(scholarship):
    """Display scholarship opportunity"""
    deadline_date = datetime.strptime(scholarship['deadline'], '%Y-%m-%d')
    days_left = (deadline_date - datetime.now()).days
    urgency_color = "#dc2626" if days_left < 30 else "#ea580c" if days_left < 60 else "#16a34a"
    
    st.markdown(f"""
    <div style="background: white; border-left: 5px solid {urgency_color}; 
                padding: 1.5rem; margin: 1rem 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h3 style="margin: 0; color: #1e293b;">{scholarship['name']}</h3>
        <p style="margin: 0.5rem 0; color: #64748b;">by {scholarship['provider']}</p>
        <div style="display: flex; gap: 2rem; margin: 1rem 0;">
            <div>
                <strong style="color: #16a34a;">💰 Amount:</strong> {scholarship['amount']}
            </div>
            <div>
                <strong style="color: {urgency_color};">⏰ Deadline:</strong> {scholarship['deadline']} ({days_left} days left)
            </div>
        </div>
        <p style="margin: 1rem 0;"><strong>Eligibility:</strong> {scholarship['eligibility']}</p>
        <p style="margin: 0.5rem 0;"><strong>Regions:</strong> {', '.join(scholarship['regions'])}</p>
        <a href="{scholarship['link']}" target="_blank" 
           style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%); 
                  color: white; padding: 0.7rem 1.5rem; border-radius: 8px; 
                  text-decoration: none; font-weight: 600; margin-top: 1rem;">
            Apply Now →
        </a>
    </div>
    """, unsafe_allow_html=True)

def mentorship_matching_ui():
    """UI for mentorship matching feature"""
    st.markdown("### 🤝 Find Your Perfect Mentor")
    st.markdown("Tell us about yourself and we'll match you with mentors who share your journey")
    
    col1, col2 = st.columns(2)
    with col1:
        user_industry = st.selectbox("Your Target Industry", 
            ["Healthcare", "Finance", "Retail", "Manufacturing", "Marketing", "Automotive", "Energy", "Technology"])
        user_ethnicity = st.selectbox("Your Ethnicity (optional)", 
            ["Prefer not to say", "South Asian", "Black", "Hispanic/Latino", "East Asian", "White", "Other"])
    with col2:
        user_career_stage = st.selectbox("Your Career Stage", 
            ["Student", "Early Career (0-3 years)", "Mid Career (4-10 years)", "Senior (10+ years)", "Career Changer"])
        user_interests = st.multiselect("What do you need help with?", 
            ["Career transition", "Technical skills", "Leadership development", "Work-life balance", 
             "Overcoming bias", "Networking", "Salary negotiation"])
    
    if st.button("🔍 Find Matching Mentors", type="primary"):
        women_data = load_women_in_ai_data()
        mentors = women_data['mentors']
        
        # Simple matching logic
        matched_mentors = []
        for mentor in mentors:
            score = 0
            if user_industry.lower() in mentor['industry'].lower():
                score += 3
            if user_ethnicity != "Prefer not to say" and user_ethnicity == mentor['ethnicity']:
                score += 2
            # Check if any user interests overlap with mentor's available_for
            for interest in user_interests:
                if any(interest.lower() in avail.lower() for avail in mentor['available_for']):
                    score += 1
            if score > 0:
                matched_mentors.append((mentor, score))
        
        # Sort by score
        matched_mentors.sort(key=lambda x: x[1], reverse=True)
        
        if matched_mentors:
            st.success(f"✨ Found {len(matched_mentors)} matching mentors!")
            for mentor, score in matched_mentors[:5]:  # Show top 5
                display_mentor_card(mentor)
        else:
            st.info("No exact matches found, but here are some inspiring mentors:")
            for mentor in mentors[:3]:
                display_mentor_card(mentor)

def translate_skills_for_industry(skills, industry_data):
    """Translate generic skills to industry-specific applications"""
    translations = {}
    for skill_name in skills:
        skill_lower = skill_name.lower()
        found = False
        for key, value in industry_data['skill_translations'].items():
            if key.lower() in skill_lower or skill_lower in key.lower():
                translations[skill_name] = value
                found = True
                break
        if not found:
            translations[skill_name] = skill_name
    return translations

def display_industry_pathway(current_industry, target_roles, industry_data):
    """Display skill progression pathway for industry transition"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); 
                color: white; padding: 2rem; border-radius: 15px; margin: 2rem 0;">
        <h3 style="margin: 0 0 1rem 0;">🎯 Your Pathway: {current_industry} → AI</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1.5rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px;">
                <h4 style="margin: 0;">📚 Learn</h4>
                <p style="margin: 0.5rem 0; font-size: 0.9rem;">
                    Technical foundations in AI/ML
                </p>
            </div>
            <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px;">
                <h4 style="margin: 0;">🔨 Build</h4>
                <p style="margin: 0.5rem 0; font-size: 0.9rem;">
                    Portfolio projects in {current_industry}
                </p>
            </div>
            <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px;">
                <h4 style="margin: 0;">🚀 Launch</h4>
                <p style="margin: 0.5rem 0; font-size: 0.9rem;">
                    Apply to {current_industry} AI roles
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 📚 Recommended Learning Paths")
    cols = st.columns(len(industry_data['certifications'][:3]))
    for idx, cert in enumerate(industry_data['certifications'][:3]):
        with cols[idx]:
            st.markdown(f"""
            <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px; 
                        border-left: 4px solid #0284c7;">
                <strong style="color: #0369a1;">{cert}</strong>
            </div>
            """, unsafe_allow_html=True)

def display_dei_company_card(company_info):
    """Display company DEI insights"""
    score_color = "#16a34a" if company_info['dei_score'] >= 4.5 else "#ea580c" if company_info['dei_score'] >= 4.0 else "#dc2626"
    
    st.markdown(f"""
    <div style="background: white; border: 2px solid #e5e7eb; border-radius: 12px; 
                padding: 1.5rem; margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <h3 style="margin: 0; color: #1e293b;">{company_info['company']}</h3>
                <div style="display: flex; gap: 2rem; margin: 1rem 0; flex-wrap: wrap;">
                    <div>
                        <strong>👩‍💻 Women in Tech:</strong> {company_info['women_in_tech']}
                    </div>
                    <div>
                        <strong>🌍 Underrepresented Minorities:</strong> {company_info['underrepresented_minorities']}
                    </div>
                </div>
            </div>
            <div style="text-align: center;">
                <div style="background: {score_color}; color: white; 
                            padding: 0.5rem 1rem; border-radius: 8px; font-weight: 700; font-size: 1.5rem;">
                    {company_info['dei_score']}/5
                </div>
                <small style="color: #64748b;">DEI Score</small>
            </div>
        </div>
        <div style="margin: 1rem 0;">
            <strong>🎯 DEI Initiatives:</strong>
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem;">
                {''.join([f'<span style="background: #dbeafe; color: #1e40af; padding: 0.3rem 0.7rem; border-radius: 15px; font-size: 0.9rem;">{initiative}</span>' for initiative in company_info['initiatives']])}
            </div>
        </div>
        <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <div style="margin-bottom: 0.5rem;">
                <strong>👶 Parental Leave:</strong> {company_info['parental_leave']}
            </div>
            <div style="margin-bottom: 0.5rem;">
                <strong>🏠 Flexible Work:</strong> {company_info['flexible_work']}
            </div>
            <div>
                <strong>♿ Accessibility:</strong> {company_info['accessibility']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Skill Recognition Engine - Enhanced",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #64748B;
        margin-bottom: 0.5rem;
    }
    .skill-tag-hard {
        display: inline-block;
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .skill-tag-soft {
        display: inline-block;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .role-card {
        background: white;
        border: 2px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

if 'text' not in st.session_state:
    st.session_state.text = ""
if 'recognized_skills' not in st.session_state:
    st.session_state.recognized_skills = []
if 'user_vector' not in st.session_state:
    st.session_state.user_vector = None
if 'matches' not in st.session_state:
    st.session_state.matches = []
if 'demographic_info' not in st.session_state:
    st.session_state.demographic_info = {}
if 'show_equity_analysis' not in st.session_state:
    st.session_state.show_equity_analysis = False
if 'industry_selection' not in st.session_state:
    st.session_state.industry_selection = None
if 'anonymous_mode' not in st.session_state:
    st.session_state.anonymous_mode = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Welcome & Introduction"
if 'visited_pages' not in st.session_state:
    st.session_state.visited_pages = set()

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<h1 class="main-title">🧭 AI Skills Recognition Engine</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Empowering Women, Diverse Communities & Career Changers in AI</p>', unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Select a section:",
    [
        "🏠 Welcome",
        "🏢 Industry Customization",
        "📄 Upload Your CV",
        "👤 Your Profile",
        "✨ Your Strengths",
        "📈 Gap Analysis",
        "🪪 Digital Passport",
        "💬 Community Forums",
        "🤝 Support Resources",
        "🌟 Women Leaders"
    ],
    key='nav_radio'
)

st.sidebar.markdown("---")

# ============================================================================
# PROGRESS TRACKER IN SIDEBAR
# ============================================================================

st.sidebar.markdown("### 📍 Your Progress")

# Track the current page visit
st.session_state.visited_pages.add(page)

# Check completion status based on VISITING pages, not just data existence
has_cv_uploaded = bool(st.session_state.text)
has_profile = bool(st.session_state.demographic_info and 
                   any([st.session_state.demographic_info.get('gender'),
                        st.session_state.demographic_info.get('ethnicity'),
                        st.session_state.demographic_info.get('background')]))

# Check if user has visited the pages (not just if data exists)
has_viewed_strengths = "✨ Your Strengths" in st.session_state.visited_pages
has_viewed_gaps = "📈 Gap Analysis" in st.session_state.visited_pages
has_viewed_passport = "🪪 Digital Passport" in st.session_state.visited_pages

# Progress items - now based on page visits
progress_items = [
    ("📄 Upload CV", has_cv_uploaded, "Upload Your CV"),
    ("👤 Complete Profile", has_profile, "Your Profile"),
    ("✨ View Strengths", has_viewed_strengths, "Your Strengths"),
    ("📈 Check Gaps", has_viewed_gaps, "Gap Analysis"),
    ("🪪 Get Passport", has_viewed_passport, "Digital Passport")
]

# Display progress
for label, completed, page_name in progress_items:
    if completed:
        st.sidebar.markdown(f"✅ **{label}**")
    else:
        st.sidebar.markdown(f"⬜ {label}")

# Calculate completion percentage
completed_count = sum(1 for _, completed, _ in progress_items if completed)
progress_percent = (completed_count / len(progress_items)) * 100

st.sidebar.progress(progress_percent / 100)
st.sidebar.caption(f"{int(progress_percent)}% Complete")

# Next step suggestion
if not has_cv_uploaded:
    st.sidebar.info("👉 **Next:** Upload your CV to get started")
elif not bool(st.session_state.recognized_skills):
    st.sidebar.info("👉 **Next:** Analyze your CV to extract skills")
elif not has_profile:
    st.sidebar.info("👉 **Next:** Complete your profile (optional)")
elif not has_viewed_strengths:
    st.sidebar.info("👉 **Next:** View your strengths and AI role matches")
elif not has_viewed_gaps:
    st.sidebar.info("👉 **Next:** Check your skill gaps")
elif not has_viewed_passport:
    st.sidebar.info("👉 **Next:** Get your digital skills passport")
else:
    st.sidebar.success("🎉 **All done!** Explore resources and communities")

# Anonymous mode toggle
st.sidebar.markdown("---")
anonymous_mode = st.sidebar.checkbox(
    "🔒 Anonymous Analysis Mode",
    value=st.session_state.anonymous_mode,
    help="Scrub identifying information for bias-free analysis"
)
st.session_state.anonymous_mode = anonymous_mode

if anonymous_mode:
    st.sidebar.info("🔒 Anonymous mode active: Demographic info will not influence recommendations")

# ============================================================================
# SCROLL TO TOP ON PAGE CHANGE
# ============================================================================

# Always scroll to top when page loads - use a unique key based on page
st.components.v1.html(
    f"""
    <script>
        // Multiple scroll methods for maximum compatibility
        var scrollToTop = function() {{
            window.parent.document.querySelector('section.main').scrollTo(0, 0);
            window.parent.document.body.scrollTop = 0;
            window.parent.document.documentElement.scrollTop = 0;
            window.scrollTo(0, 0);
        }};
        
        // Execute immediately
        scrollToTop();
        
        // Also execute after a small delay to catch any late-loading content
        setTimeout(scrollToTop, 100);
    </script>
    """,
    height=0,
)

# ============================================================================
# PAGE: WELCOME
# ============================================================================

if page == "🏠 Welcome":
    st.header("🏠 Welcome to the AI Skills Recognition Engine")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🎯 What This Tool Does
        
        This intelligent platform helps you **discover your AI potential** by:
        
        1. **📄 Analyzing Your Experience** - Upload your CV or paste your profile
        2. **✨ Recognizing Your Skills** - Automatically extract technical and soft skills
        3. **🎯 Matching AI Roles** - Find the best AI career paths for you
        4. **📚 Closing Skill Gaps** - Get personalized learning recommendations
        5. **🪪 Creating Your Passport** - Generate a professional skills certificate
        
        ### 🌟 Why Use This Tool?
        
        - **For Career Changers**: Discover how your existing skills transfer to AI
        - **For Women in Tech**: Find role models, mentors, and supportive communities
        - **For Everyone**: Get objective, data-driven career guidance
        
        ### 🚀 Getting Started
        
        **Follow these simple steps:**
        
        1. **Industry Customization** → Choose your target industry
        2. **Your Profile** → (Optional) Share your background for personalized insights
        3. **Upload CV** → Let our AI analyze your experience
        4. **View Results** → See your skills, matched roles, and learning path
        5. **Generate Passport** → Download your professional skills certificate
        
        **All your data stays private and secure on your device!**
        """)
    
    with col2:
        st.markdown("""
        ### 📊 By the Numbers
        """)
        st.metric("AI Roles", "8+", delta="High Demand")
        st.metric("Skills Tracked", "30+", delta="Technical & Soft")
        st.metric("Learning Resources", "12+", delta="Free & Paid")
        st.metric("Industry Paths", "8", delta="Customized")
        
        st.markdown("---")
        st.info("""
        **💡 Quick Tip**
        
        Complete your profile for personalized insights including salary equity analysis and community connections!
        """)
        
        st.markdown("---")
        st.success("""
        **✓ 100% Private**
        
        Your CV never leaves your device. All processing happens locally.
        """)
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### 🎓 Who This Tool Helps")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <h3 style="margin: 0; color: white;">👩‍💻 Women in AI</h3>
            <p style="margin: 0.5rem 0;">Find role models, mentors, and supportive communities</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <h3 style="margin: 0; color: white;">🔄 Career Changers</h3>
            <p style="margin: 0.5rem 0;">Discover how your skills transfer to AI roles</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <h3 style="margin: 0; color: white;">🌍 Diverse Talent</h3>
            <p style="margin: 0.5rem 0;">Get equity insights and fair salary guidance</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #f0f9ff; border-radius: 12px;">
        <h3>Ready to discover your AI potential? 🚀</h3>
        <p style="font-size: 1.1rem; color: #1e3a8a;">
            Use the navigation on the left to start your journey!
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE: WOMEN'S HUB
# ============================================================================

elif page == "👩‍💼 Women's Hub":
    st.header("👩‍💼 Women's Hub: Resources, Scholarships & Programs")
    
    tab1, tab2, tab3 = st.tabs(["💰 Scholarships", "🤝 Mentorship Programs", "🌐 Communities"])
    
    women_data = load_women_in_ai_data()
    hub_data = women_data['women_hub']
    
    with tab1:
        st.markdown("### 💰 Available Scholarships & Grants")
        st.markdown("Updated opportunities for women and underrepresented groups in AI")
        
        # Sort by deadline
        scholarships = sorted(hub_data['scholarships'], 
                            key=lambda x: datetime.strptime(x['deadline'], '%Y-%m-%d'))
        
        for scholarship in scholarships:
            display_scholarship_card(scholarship)
        
        # Alert setup
        st.markdown("---")
        st.markdown("### 🔔 Get Alerts for New Opportunities")
        email = st.text_input("Enter your email to receive notifications")
        if st.button("Subscribe to Alerts"):
            if email:
                st.success(f"✅ You'll receive alerts at {email} when new scholarships open!")
            else:
                st.error("Please enter a valid email address")
    
    with tab2:
        st.markdown("### 🤝 Mentorship Programs")
        for program in hub_data['mentorship_programs']:
            st.markdown(f"""
            <div style="background: white; border-left: 5px solid #8b5cf6; 
                        padding: 1.5rem; margin: 1rem 0; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <h3 style="margin: 0; color: #5b21b6;">{program['name']}</h3>
                <p style="margin: 0.8rem 0; line-height: 1.6;">{program['description']}</p>
                <div style="display: flex; gap: 2rem; margin: 1rem 0;">
                    <div><strong>Duration:</strong> {program['duration']}</div>
                    <div><strong>Cost:</strong> {program['cost']}</div>
                    <div><strong>For:</strong> {program['target_audience']}</div>
                </div>
                <a href="{program['application_link']}" target="_blank"
                   style="display: inline-block; background: #8b5cf6; color: white; 
                          padding: 0.7rem 1.5rem; border-radius: 8px; text-decoration: none; 
                          font-weight: 600; margin-top: 1rem;">
                    Apply Now →
                </a>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🌐 Women in Tech Communities")
        cols = st.columns(2)
        for idx, community in enumerate(hub_data['communities']):
            with cols[idx % 2]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ec4899 0%, #be185d 100%); 
                            color: white; padding: 1.5rem; border-radius: 12px; margin: 0.5rem 0;">
                    <h4 style="margin: 0;">{community['name']}</h4>
                    <p style="margin: 0.5rem 0; opacity: 0.9;">👥 {community['members']} members</p>
                    <p style="margin: 0.5rem 0;">Focus: {community['focus']}</p>
                    <a href="{community['link']}" target="_blank"
                       style="color: white; text-decoration: underline; font-weight: 600;">
                        Join Community →
                    </a>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# PAGE: MENTORSHIP MATCHING
# ============================================================================

elif page == "🤝 Mentorship Matching":
    st.header("🤝 Find Your Mentor")
    st.markdown("""
    Connect with experienced professionals who understand your journey. Our mentors 
    have overcome similar challenges and are here to guide you.
    """)
    
    mentorship_matching_ui()

# ============================================================================
# PAGE: INDUSTRY CUSTOMIZATION
# ============================================================================

elif page == "🏢 Industry Customization":
    st.header("🏢 Industry-Specific AI Career Paths")
    
    st.markdown("""
    ### 💡 Why This Matters
    AI looks different in every industry. Healthcare AI focuses on diagnosis and patient care, while Finance AI 
    deals with fraud detection and trading. Understanding industry-specific applications helps you target the right roles.
    
    ### 🎯 How to Use This Section
    - Select your **target industry** (or current field)
    - Learn how **AI is applied** in that domain
    - Discover **specific skills** needed for industry AI roles
    - See **top companies** hiring in that space
    """)
    
    industry_data_full = load_industry_data()
    industries = industry_data_full['industries']
    
    # Industry selection
    industry_options = {ind['name']: ind for ind in industries}
    selected_industry_name = st.selectbox(
        "Select Your Industry",
        options=list(industry_options.keys()),
        format_func=lambda x: f"{industry_options[x]['icon']} {x}"
    )
    
    selected_industry = industry_options[selected_industry_name]
    st.session_state.industry_selection = selected_industry
    
    # Display industry overview
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%); 
                color: white; padding: 2rem; border-radius: 15px; margin: 2rem 0;">
        <h2 style="margin: 0;">{selected_industry['icon']} {selected_industry['name']}</h2>
        <p style="margin: 1rem 0; font-size: 1.1rem; opacity: 0.95;">
            AI Applications in this industry
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Applications
    st.markdown("### 🎯 AI Applications")
    cols = st.columns(3)
    for idx, app in enumerate(selected_industry['ai_applications']):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px; 
                        margin: 0.5rem 0; border-left: 4px solid #0284c7;">
                {app}
            </div>
            """, unsafe_allow_html=True)
    
    # Key Skills
    st.markdown("### 🔑 Key Skills Needed")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Technical Skills:**")
        for skill in selected_industry['key_skills']['technical']:
            st.markdown(f"• {skill}")
    with col2:
        st.markdown("**Domain Knowledge:**")
        for skill in selected_industry['key_skills']['domain']:
            st.markdown(f"• {skill}")
    
    # Target Roles
    st.markdown("### 💼 Target AI Roles")
    for role in selected_industry['roles']:
        st.markdown(f"""
        <div style="background: white; border: 2px solid #e5e7eb; padding: 1rem; 
                    border-radius: 8px; margin: 0.5rem 0;">
            <strong style="color: #1e293b;">🎯 {role}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Learning Path
    display_industry_pathway(selected_industry['name'], selected_industry['roles'], selected_industry)
    
    # Top Companies
    st.markdown("### 🏢 Top Companies Hiring")
    cols = st.columns(4)
    for idx, company in enumerate(selected_industry['companies']):
        with cols[idx % 4]:
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 0.8rem; border-radius: 6px; 
                        text-align: center; border: 1px solid #e2e8f0;">
                <strong>{company}</strong>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# PAGE: UPLOAD YOUR CV
# ============================================================================

elif page == "📄 Upload Your CV":
    st.header("📄 Upload Your CV or Profile")
    
    st.markdown("""
    ### 💡 Why This Matters
    Your CV contains valuable information about your skills and experience. Our AI analyzes this to identify 
    both obvious and hidden talents, then matches you with suitable AI roles.
    
    ### 🎯 How to Use This Section
    - **Upload** your CV file (PDF/TXT recommended)
    - **Paste** text from LinkedIn or resume if you prefer
    - **Take the quiz** if you don't have a formatted CV
    - Click **Analyze** to extract your skills automatically
    """)
    
    # Input method selection
    input_method = st.radio("Choose input method:", ["📤 Upload File", "📋 Paste Text", "❓ Quick Skill Quiz"], horizontal=True)
    
    if input_method == "📤 Upload File":
        uploaded_file = st.file_uploader("Upload your CV (PDF/TXT)", type=['pdf', 'txt'], key="cv_uploader")
        if uploaded_file:
            try:
                if uploaded_file.type == "text/plain":
                    st.session_state.text = uploaded_file.read().decode('utf-8')
                else:
                    st.session_state.text = ingest_and_clean(uploaded_file)
                st.success("✅ File uploaded successfully!")
                with st.expander("View extracted text"):
                    st.text_area("Content", st.session_state.text, height=200, key="extracted_text_preview")
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                st.info("💡 Try one of these solutions:")
                st.markdown("""
                - **Use 'Paste Text' instead**: Copy your resume text and paste it directly
                - **Check file size**: Ensure your file is under 200MB
                - **Try a different format**: Convert PDF to TXT if having issues
                - **Refresh the page**: Press Ctrl+R or F5 and try again
                """)
    
    elif input_method == "📋 Paste Text":
        text_input = st.text_area("Paste your CV or profile text here:", height=300)
        if text_input:
            st.session_state.text = text_input
            st.success("✅ Text captured!")
    
    else:  # Quick Skill Quiz
        st.markdown("### ❓ Quick Skill Assessment")
        st.markdown("Answer a few questions to identify your skills")
        
        q1 = st.multiselect("What programming languages do you know?",
            ["Python", "R", "Java", "JavaScript", "C++", "SQL", "None"])
        q2 = st.multiselect("What tools/frameworks have you used?",
            ["TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "Excel", "Tableau", "Power BI", "None"])
        q3 = st.multiselect("What domains have you worked in?",
            ["Data Analysis", "Machine Learning", "Statistics", "Project Management", 
             "Customer Service", "Sales", "Marketing", "Healthcare", "Finance"])
        q4 = st.text_area("Describe your most significant project or achievement:", height=100)
        
        if st.button("Generate Skills from Quiz"):
            quiz_text = f"""
            Programming: {', '.join(q1)}
            Tools: {', '.join(q2)}
            Domains: {', '.join(q3)}
            Project: {q4}
            """
            st.session_state.text = quiz_text
            st.success("✅ Skills captured from quiz!")
    
    # Analyze button
    if st.session_state.text:
        if st.button("🔍 Analyze Skills", type="primary"):
            with st.spinner("Analyzing your skills..."):
                # Apply anonymous mode if enabled
                text_to_analyze = st.session_state.text
                if st.session_state.anonymous_mode:
                    # Simple anonymization: remove potential names/identifiers
                    import re
                    text_to_analyze = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[REDACTED]', text_to_analyze)
                
                skills = extract_skills(text_to_analyze)
                st.session_state.recognized_skills = skills
                
                # Combine all skill IDs for vector computation
                all_skill_ids = []
                if isinstance(skills, dict):
                    all_skill_ids = skills.get('hard_skills', []) + skills.get('soft_skills', [])
                else:
                    # Fallback for old format
                    all_skill_ids = skills
                
                st.session_state.user_vector = compute_user_vector(all_skill_ids)
                
                # Get skill names for match_roles function
                skill_names = get_skill_names(all_skill_ids)
                matches = match_roles(st.session_state.user_vector, skill_names)
                st.session_state.matches = matches
                st.success("✅ Analysis complete!")
                
                # Next step guidance
                st.markdown("---")
                st.markdown("""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                            color: white; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                    <h3 style="margin: 0; color: white;">🎉 Great! Your skills have been analyzed</h3>
                    <p style="margin: 0.5rem 0; opacity: 0.9;">What's next?</p>
                    <ul style="margin: 0.5rem 0;">
                        <li><strong>Your Profile</strong> - Add demographic info for personalized insights (optional)</li>
                        <li><strong>Your Strengths</strong> - See your recognized skills and AI role matches</li>
                        <li><strong>Gap Analysis</strong> - Find out what skills you need to develop</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# PAGE: YOUR PROFILE
# ============================================================================

elif page == "👤 Your Profile":
    st.header("👤 Your Profile")
    
    st.markdown("""
    ### 💡 Why This Matters
    Sharing your demographic information (optional) allows us to provide personalized equity analysis, representation 
    insights, and connect you with relevant communities and mentors who share similar backgrounds.
    
    ### 🎯 How to Use This Section
    - Fill in **optional profile fields** (gender, ethnicity, background)
    - Review **equity analysis** showing representation in your target roles
    - Understand **salary gaps** and fair compensation ranges
    - All data stays **on your device** - completely confidential
    
    **All information is confidential and stored only on your device.**
    """)
    
    if st.session_state.anonymous_mode:
        st.warning("🔒 Anonymous mode is active. Demographic info will not be collected.")
    else:
        # Profile input section (no tabs)
        st.markdown("## 📝 Your Profile Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox(
                "Gender Identity",
                ["Prefer not to say", "Woman", "Man", "Non-binary", "Other"],
                help="Helps us understand salary equity gaps"
            )
            
            ethnicity = st.selectbox(
                "Ethnicity",
                ["Prefer not to say", "White", "Black or African American", "Hispanic or Latino", 
                 "South Asian", "East Asian", "Southeast Asian", "Middle Eastern", "Native American", "Pacific Islander", "Other"],
                help="Helps us provide targeted support and community connections"
            )
            
            years_experience = st.slider("Years of Professional Experience", 0, 40, 5)
        
        with col2:
            background = st.selectbox(
                "Educational/Professional Background",
                ["Prefer not to say", "AI/ML (Direct)", "STEM (Non-AI)", "Non-STEM", 
                 "Career Break (3+ years)", "Self-taught / Bootcamp"],
                help="Helps us provide relevant transition guidance"
            )
            
            current_industry = st.selectbox(
                "Current Industry",
                ["Technology", "Healthcare", "Finance", "Retail", "Manufacturing", 
                 "Education", "Government", "Non-profit", "Other", "Student"]
            )
            
            first_gen = st.checkbox("First-generation college student/professional")
        
        if st.button("💾 Save Profile & Show Equity Analysis", type="primary"):
            st.session_state.demographic_info = {
                'gender': gender if gender != "Prefer not to say" else None,
                'ethnicity': ethnicity if ethnicity != "Prefer not to say" else None,
                'background': background if background != "Prefer not to say" else None,
                'years_experience': years_experience,
                'current_industry': current_industry,
                'first_gen': first_gen
            }
            st.session_state.show_equity_analysis = True
            st.success("✅ Profile saved! Scroll down to see your equity analysis.")
            st.rerun()  # Rerun to show the equity analysis immediately
        
        # Equity analysis section (shown directly below profile if data exists)
        st.markdown("---")
        
        # Check if demographic info exists and has any values
        has_demographic_data = (st.session_state.demographic_info and 
                               any([st.session_state.demographic_info.get('gender'),
                                    st.session_state.demographic_info.get('ethnicity'),
                                    st.session_state.demographic_info.get('background')]))
        
        if not has_demographic_data:
            st.info("� Fill out your profile above and click 'Save Profile' to see personalized equity insights below")
            st.markdown("### 🌍 What You'll See After Saving:")
            st.markdown("""
            - 📊 **Representation Analysis**: See how your background is represented in AI roles
            - 💰 **Salary Equity Insights**: Understand potential pay gaps and how to negotiate
            - 🤝 **Community Connections**: Find support groups and mentorship opportunities
            - 💪 **Strength Recognition**: Get credit for unique perspectives you bring
            - 🏢 **DEI Company Insights**: Find companies with strong diversity initiatives
            
            All demographic data is optional and stored locally on your device.
            """)
        else:
            st.markdown("## 🌍 Your Equity Analysis & Support Resources")
            
            demo = st.session_state.demographic_info or {}
            gender = demo.get('gender')
            ethnicity = demo.get('ethnicity')
            background = demo.get('background')
            
            # Get demographic profile
            profile = get_demographic_profile(gender, ethnicity, background)
            
            if profile:
                # Display profile summary
                st.markdown("### 🌟 Your Unique Profile")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if gender:
                        st.markdown(f"**Gender:** {gender}")
                        if 'salary_adjustment' in profile:
                            adjustment = profile['salary_adjustment']
                            if adjustment < 1.0:
                                gap_percent = int((1 - adjustment) * 100)
                                st.warning(f"⚠️ Typical salary gap: {gap_percent}%")
                    
                    if ethnicity:
                        st.markdown(f"**Ethnicity:** {ethnicity}")
                        if 'representation' in profile:
                            st.info(f"📊 {profile['representation']}")
                
                with col2:
                    if background:
                        st.markdown(f"**Background:** {background}")
                        if 'transition_difficulty' in profile:
                            st.markdown(f"**Transition Path:** {profile['transition_difficulty']}")
                        if 'success_rate' in profile:
                            st.markdown(f"**Success Rate:** {profile['success_rate']}")
                
                # Challenges and strengths
                if 'challenges' in profile:
                    st.markdown("### 💪 Challenges & Strengths")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Challenges:**")
                        for challenge in profile['challenges']:
                            st.markdown(f"• {challenge}")
                    with col2:
                        st.markdown("**Your Strengths:**")
                        for strength in profile.get('advantages', []):
                            st.markdown(f"• {strength}")
                
                # Representation gap analysis
                if ethnicity:
                    st.markdown("---")
                    st.markdown("### 📊 Representation Analysis")
                    gap_data = analyze_representation_gap(ethnicity)
                    if gap_data and gap_data.get('tech_percent') != "N/A":
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("In Tech Industry", f"{gap_data['tech_percent']}%")
                        with col2:
                            st.metric("In General Population", f"{gap_data['population_percent']}%")
                        with col3:
                            gap_color = "🔴" if gap_data['status'] == "underrepresented" else "🟢" if gap_data['status'] == "overrepresented" else "🟡"
                            st.metric("Gap", f"{gap_data['gap']} {gap_color}")
                        
                        if gap_data['status'] == "underrepresented":
                            st.warning(f"⚠️ **{ethnicity}** professionals are underrepresented in tech. Your perspective is especially valuable!")
                        else:
                            st.info(f"ℹ️ Representation status: {gap_data['status'].title()}")
                
                # Next step guidance after completing profile
                st.markdown("---")
                st.markdown("""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                            color: white; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                    <h3 style="margin: 0; color: white;">✅ Profile Complete!</h3>
                    <p style="margin: 0.5rem 0; opacity: 0.9;">Continue your journey:</p>
                    <ul style="margin: 0.5rem 0;">
                        <li><strong>Your Strengths</strong> - View your skills and role matches</li>
                        <li><strong>Gap Analysis</strong> - See what skills to develop next</li>
                        <li><strong>Support Resources</strong> - Find scholarships, mentors, and communities</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# PAGE: YOUR STRENGTHS
# ============================================================================

elif page == "✨ Your Strengths":
    st.header("✨ Your Strengths & AI Role Matches")
    
    st.markdown("""
    ### 💡 Why This Matters
    Understanding your skills helps you identify career paths where you'll excel. This analysis reveals both 
    your technical abilities and soft skills, then matches you with AI roles that align with your strengths.
    
    ### 🎯 How to Use This Section
    - Review your **recognized skills** (technical and soft)
    - Explore **AI role matches** based on your profile
    - Check **match scores** to see how well you fit each role
    - Review **salary ranges** for different positions
    """)
    
    if not st.session_state.recognized_skills:
        st.warning("👆 Please upload your CV in the 'Upload Your CV' section first")
        st.markdown("""
        ### What you'll see here:
        1. **Your Recognized Skills** - Technical and soft skills we found
        2. **AI Role Matches** - Top career paths based on your skills
        3. **Match Scores** - How well you fit each role
        4. **Salary Ranges** - Expected compensation for each role
        """)
    else:
        # SECTION 1: YOUR RECOGNIZED SKILLS
        st.markdown("## ✨ Your Recognized Skills")
        
        skills = st.session_state.recognized_skills
        
        # Extract skills properly from the dictionary format
        if isinstance(skills, dict):
            hard_skill_ids = skills.get('hard_skills', [])
            soft_skill_ids = skills.get('soft_skills', [])
            
            # Convert IDs to names
            hard_skills = get_skill_names(hard_skill_ids)
            soft_skills = get_skill_names(soft_skill_ids)
            all_skill_names = hard_skills + soft_skills
        else:
            # Fallback for old format
            hard_skills = []
            soft_skills = []
            for s in skills:
                if isinstance(s, dict):
                    if s.get('category') == 'hard':
                        hard_skills.append(s.get('name', str(s)))
                    else:
                        soft_skills.append(s.get('name', str(s)))
                else:
                    hard_skills.append(str(s))
            all_skill_names = hard_skills + soft_skills
        
        # Apply equity enhancement if demographic info provided
        inferred_skills = []
        if st.session_state.demographic_info and not st.session_state.anonymous_mode:
            gender = st.session_state.demographic_info.get('gender')
            ethnicity = st.session_state.demographic_info.get('ethnicity')
            background = st.session_state.demographic_info.get('background')
            
            if (gender or ethnicity or background) and all_skill_names:
                enhanced_skills, inferred_skills = enhance_skills_with_confidence(
                    all_skill_names, gender, ethnicity, background
                )
                
                # Show confidence message
                conf_msg = generate_confidence_message(gender, ethnicity, background)
                if conf_msg:
                    st.info(f"💡 {conf_msg}")
                
                # Display inferred skills
                if inferred_skills:
                    st.markdown("### ⭐ Skills You Likely Have (Based on Your Profile)")
                    st.markdown("You may be underselling yourself! Here are skills commonly associated with your background:")
                    cols = st.columns(4)
                    for idx, skill in enumerate(inferred_skills):
                        with cols[idx % 4]:
                            st.markdown(f'<span class="skill-tag-soft">⭐ {skill}</span>', unsafe_allow_html=True)
                    st.markdown("---")
        
        # Display skills summary
        total_skills = len(hard_skills) + len(soft_skills)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Skills", total_skills)
        with col2:
            st.metric("Technical Skills", len(hard_skills))
        with col3:
            st.metric("Soft Skills", len(soft_skills))
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💻 Technical Skills")
            if hard_skills:
                # Display in horizontal rows
                cols = st.columns(4)
                for idx, skill_name in enumerate(hard_skills):
                    with cols[idx % 4]:
                        st.markdown(f'<span class="skill-tag-hard">{skill_name}</span>', unsafe_allow_html=True)
            else:
                st.info("No technical skills detected. Try uploading a more detailed CV.")
        
        with col2:
            st.markdown("### 🤝 Soft Skills")
            if soft_skills:
                # Display in horizontal rows
                cols = st.columns(4)
                for idx, skill_name in enumerate(soft_skills):
                    with cols[idx % 4]:
                        st.markdown(f'<span class="skill-tag-soft">{skill_name}</span>', unsafe_allow_html=True)
            else:
                st.info("No soft skills detected. Try uploading a more detailed CV.")
        
        # Industry translation if industry selected
        if st.session_state.industry_selection:
            st.markdown("---")
            st.markdown(f"### 🏢 Your Skills in {st.session_state.industry_selection['name']}")
            st.markdown("Here's how your skills translate to this industry:")
            
            translations = translate_skills_for_industry(all_skill_names, st.session_state.industry_selection)
            
            for skill, translation in translations.items():
                if translation != skill:
                    st.markdown(f"""
                    <div style="background: #f0fdf4; border-left: 4px solid #16a34a; 
                                padding: 1rem; margin: 0.5rem 0; border-radius: 4px;">
                        <strong style="color: #15803d;">{skill}</strong> → {translation}
                    </div>
                    """, unsafe_allow_html=True)
        
        # SECTION 2: AI ROLE MATCHES (shown directly below skills, not in a tab)
        st.markdown("---")
        st.markdown("## 🧠 Your Top AI Role Matches")
        
        if not st.session_state.matches:
            st.info("No role matches yet. Make sure you've analyzed your CV.")
        else:
            matches = st.session_state.matches
            
            # Apply equity adjustments if available
            if st.session_state.demographic_info and not st.session_state.anonymous_mode:
                matches = get_targeted_role_recommendations(
                    matches,
                    st.session_state.demographic_info.get('gender'),
                    st.session_state.demographic_info.get('ethnicity'),
                    st.session_state.demographic_info.get('background')
                )
            
            # Show top match prominently
            st.markdown("### 🎯 Your Best Match")
            top_role = matches[0]
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%); 
                        color: white; padding: 2rem; border-radius: 12px; margin-bottom: 1rem;">
                <h2 style="margin: 0; color: white;">{top_role['icon']} {top_role['role_name']}</h2>
                <p style="margin: 1rem 0; font-size: 1.1rem;">{top_role.get('description', 'N/A')}</p>
                <div style="display: flex; gap: 2rem; margin-top: 1rem;">
                    <div>
                        <strong>Match Score:</strong> {top_role['similarity']:.1%}
                    </div>
                    <div>
                        <strong>Salary:</strong> {top_role.get('pay_range', 'N/A')}
                    </div>
                    <div>
                        <strong>Demand:</strong> {top_role.get('demand', 'N/A').upper()}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show equity insight if available
            if 'equity_insight' in top_role:
                st.info(f"💡 {top_role['equity_insight']}")
            
            # Other matches
            st.markdown("### 📊 Other Good Matches")
            for idx, role in enumerate(matches[1:5], 2):
                with st.expander(f"{idx}. {role['role_name']} - {role['similarity']:.1%} match"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Description:** {role.get('description', 'N/A')}")
                        st.markdown(f"**Required Skills:** {', '.join(role.get('matched_skills', [])[:5])}")
                        
                        if role.get('gaps'):
                            st.markdown(f"**Skills to Learn:** {', '.join(role['gaps'][:5])}")
                        
                        # Show equity insight if available
                        if 'equity_insight' in role:
                            st.info(f"💡 {role['equity_insight']}")
                    
                    with col2:
                        st.metric("Match Score", f"{role['similarity']:.1%}")
                        st.metric("Coverage", f"{role.get('coverage', 0):.1%}")
                        
                        # Salary with equity adjustment
                        if 'pay_range' in role:
                            salary_range = role['pay_range']
                            st.markdown(f"**💰 Salary Range:** {salary_range}")
            
            # Next step guidance
            st.markdown("---")
            st.markdown("""
            <div style="background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); 
                        color: white; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                <h3 style="margin: 0; color: white;">🚀 Ready for the next step?</h3>
                <p style="margin: 0.5rem 0; opacity: 0.9;">Here's what to do next:</p>
                <ul style="margin: 0.5rem 0;">
                    <li><strong>Gap Analysis</strong> - Identify exactly what skills you need to develop</li>
                    <li><strong>Digital Passport</strong> - Create a shareable credential of your skills</li>
                    <li><strong>Support Resources</strong> - Find scholarships, courses, and mentorship</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# PAGE: RECOGNIZED SKILLS (OLD - NOW REMOVED, MERGED ABOVE)
# ============================================================================

# ============================================================================
# PAGE: AI ROLE MATCHES (OLD - NOW REMOVED, MERGED ABOVE)
# ============================================================================

# ============================================================================
# PAGE: GAP ANALYSIS
# ============================================================================

elif page == "📈 Gap Analysis":
    st.header("📈 Gap Analysis & Learning Recommendations")
    
    st.markdown("""
    ### 💡 Why This Matters
    Identify exactly what skills you need to develop to reach your target role. This analysis compares your 
    current skills against role requirements and provides personalized learning recommendations.
    
    ### 🎯 How to Use This Section
    - Select a **target AI role** you're interested in
    - Review **skills you have** that match the role
    - Identify **missing skills** you need to develop
    - Get **learning resources** and courses to close gaps
    """)
    
    if not st.session_state.matches or not st.session_state.recognized_skills:
        st.info("👆 Please analyze your CV and check role matches first")
    else:
        st.markdown("Select a target role to see what skills you need to develop:")
        
        role_names = [r['role_name'] for r in st.session_state.matches[:10]]
        selected_role = st.selectbox("Target Role", role_names)
        
        # Find the selected role
        role_data = next(r for r in st.session_state.matches if r['role_name'] == selected_role)
        
        # Get ALL user skills from resume (not just matched ones)
        user_skills_dict = st.session_state.recognized_skills
        if isinstance(user_skills_dict, dict):
            hard_skill_ids = user_skills_dict.get('hard_skills', [])
            soft_skill_ids = user_skills_dict.get('soft_skills', [])
            all_skill_ids = hard_skill_ids + soft_skill_ids
            user_skill_names = get_skill_names(all_skill_ids)
        else:
            user_skill_names = [s.get('name', str(s)) if isinstance(s, dict) else str(s) for s in user_skills_dict]
        
        # Get gaps from role data
        gaps = role_data.get('gaps', [])
        matched_skills = role_data.get('matched_skills', [])
        
        # Display
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Skills You Have (From Your Resume)")
            st.markdown(f"**Total: {len(user_skill_names)} skills extracted from your CV**")
            st.markdown("---")
            # Show ALL skills from resume in horizontal format
            if user_skill_names:
                cols = st.columns(3)
                for idx, skill in enumerate(user_skill_names):
                    with cols[idx % 3]:
                        st.markdown(f'<span class="skill-tag-hard">{skill}</span>', unsafe_allow_html=True)
            else:
                st.info("No skills found in your resume.")
        
        with col2:
            st.markdown("### 📚 Skills to Learn for This Role")
            st.markdown(f"**Gap: {len(gaps)} skills needed**")
            st.markdown("---")
            if gaps:
                for skill in gaps[:10]:  # Show top 10 gaps
                    st.markdown(f"• {skill.title()}")
            else:
                st.success("🎉 You have all the required skills for this role!")
        
        # Show which of user's skills match this role
        st.markdown("---")
        st.markdown(f"### 🎯 Your Skills That Match {selected_role}")
        if matched_skills:
            st.success(f"✅ {len(matched_skills)} of your skills match this role!")
            cols = st.columns(4)
            for idx, skill in enumerate(matched_skills):
                with cols[idx % 4]:
                    st.markdown(f'<span class="skill-tag-soft">✓ {skill.title()}</span>', unsafe_allow_html=True)
        else:
            st.warning("No direct matches found. Consider the learning resources below to bridge the gap.")
        
        # Learning recommendations
        if gaps:
            st.markdown("---")
            st.markdown("### 🎓 Recommended Learning Resources")
            
            bridges = recommend_bridges(list(gaps), user_skill_names)
            for bridge in bridges[:5]:
                st.markdown(f"""
                <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; 
                            margin: 1rem 0; border-radius: 12px;">
                    <h4 style="margin: 0; color: #1e293b;">{bridge['course_name']}</h4>
                    <p style="margin: 0.5rem 0;">{bridge.get('description', '')}</p>
                    <p style="margin: 0.5rem 0; font-size: 0.9rem; color: #64748b;">
                        <strong>Provider:</strong> {bridge.get('provider', 'N/A')} | 
                        <strong>Duration:</strong> {bridge.get('duration_hours', 'N/A')} hours | 
                        <strong>Cost:</strong> {'Free' if bridge.get('cost', 0) == 0 else f"${bridge.get('cost', 'N/A')}"}
                    </p>
                    <p style="margin: 0.5rem 0; font-size: 0.9rem;">
                        <strong>Fills gaps:</strong> {', '.join(bridge.get('fills_gaps', [])[:3])}
                    </p>
                    <div style="margin-top: 1rem;">
                        <a href="{bridge.get('url', '#')}" target="_blank"
                           style="background: #3b82f6; color: white; padding: 0.6rem 1.2rem; 
                                  border-radius: 8px; text-decoration: none; font-weight: 600;">
                            Start Learning →
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# ============================================================================
# PAGE: DIGITAL PASSPORT
# ============================================================================

elif page == "🪪 Digital Passport":
    st.header("🪪 Generate Your Digital Passport")
    
    st.markdown("""
    ### 💡 Why This Matters
    A digital passport is a verified, portable record of your skills that you can share with employers, 
    universities, or training programs. It provides instant credibility and saves time in applications.
    
    ### 🎯 How to Use This Section
    - Click to **generate your passport** (JSON and PDF formats)
    - **Download** both versions for different uses
    - **Share with employers** to showcase verified skills
    - **Use for applications** to educational programs or certifications
    """)
    
    if not st.session_state.recognized_skills:
        st.info("👆 Please analyze your CV first to generate a passport")
    else:
        if st.button("🎨 Generate Digital Passport", type="primary"):
            with st.spinner("Creating your passport..."):
                # Prepare user data
                user_data = {
                    'name': st.session_state.demographic_info.get('name', 'Anonymous') if st.session_state.demographic_info else 'Anonymous',
                    'email': st.session_state.demographic_info.get('email', '') if st.session_state.demographic_info else '',
                    'profile_completed': bool(st.session_state.demographic_info)
                }
                
                # Get skills dictionary
                skills = st.session_state.recognized_skills
                
                # Get top roles
                top_roles = st.session_state.matches[:5] if st.session_state.matches else []
                
                # Get bridges/learning resources if available
                bridges = []
                if top_roles and isinstance(skills, dict):
                    all_skill_ids = skills.get('hard_skills', []) + skills.get('soft_skills', [])
                    user_skill_names = get_skill_names(all_skill_ids)
                    gaps = top_roles[0].get('gaps', []) if top_roles else []
                    if gaps:
                        bridges = recommend_bridges(list(gaps), user_skill_names)[:5]
                
                # Generate passport
                json_path, passport_data = generate_skill_passport(
                    user_data,
                    skills,
                    top_roles,
                    bridges
                )
                
                # Store in session state for PDF generation
                st.session_state.passport_data = passport_data
                st.session_state.passport_generated = True
                
                # Display passport
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; padding: 3rem; border-radius: 20px; margin: 2rem 0;">
                    <h2 style="margin: 0; text-align: center;">🪪 AI Skills Passport</h2>
                    <p style="text-align: center; margin: 1rem 0; opacity: 0.9;">
                        Verified Skill Recognition | {datetime.now().strftime('%B %d, %Y')}
                    </p>
                    <div style="background: rgba(255,255,255,0.2); padding: 2rem; 
                                border-radius: 12px; margin-top: 2rem;">
                        <h3>Verified Skills: {passport_data['verified_skills']['total_count']}</h3>
                        <h3>Top Role: {passport_data.get('top_role_match', {}).get('role', 'N/A') if passport_data.get('top_role_match') else 'N/A'}</h3>
                        <h3>Recommended Courses: {len(passport_data.get('recommended_courses', []))}</h3>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate PDF immediately
                with st.spinner("Creating PDF..."):
                    demographic_info = st.session_state.demographic_info if st.session_state.demographic_info else {}
                    pdf_path = create_pdf_passport(st.session_state.passport_data, demographic_info)
                
                # Download options
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 Download JSON",
                        data=json.dumps(st.session_state.passport_data, indent=2),
                        file_name="skill_passport.json",
                        mime="application/json",
                        use_container_width=True
                    )
                with col2:
                    if pdf_path and os.path.exists(pdf_path):
                        # Read PDF file for download
                        with open(pdf_path, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()
                        
                        st.download_button(
                            "📄 Download PDF",
                            data=pdf_bytes,
                            file_name="ai_skills_passport.pdf",
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True
                        )
                    else:
                        st.error("❌ PDF generation failed. Download JSON instead.")

# ============================================================================
# PAGE: SUPPORT RESOURCES
# ============================================================================

elif page == "🤝 Support Resources":
    st.header("🤝 Support Resources & Communities")
    
    st.markdown("""
    ### 💡 Why This Matters
    Access scholarships, mentorship programs, professional communities, and companies with strong DEI commitments. 
    These resources can help advance your career, provide financial support, and connect you with like-minded professionals.
    
    ### 🎯 How to Use This Section
    - Browse **scholarships** for financial support opportunities
    - Explore **mentorship programs** to find guidance
    - Join **communities** to network with peers
    - Discover **companies** with inclusive cultures
    """)
    
    women_data = load_women_in_ai_data()
    hub_data = women_data['women_hub']
    
    # Tabs for different resources
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Scholarships", "🤝 Mentorship Programs", "🌐 Communities", "🏢 DEI Companies"])
    
    with tab1:
        st.markdown("### 💰 Available Scholarships & Grants")
        st.markdown("Updated opportunities for women and underrepresented communities in AI")
        
        # Sort by deadline
        scholarships = sorted(hub_data['scholarships'], 
                            key=lambda x: datetime.strptime(x['deadline'], '%Y-%m-%d'))
        
        for scholarship in scholarships:
            display_scholarship_card(scholarship)
        
        # Alert setup
        st.markdown("---")
        st.markdown("#### 🔔 Get Alerts for New Opportunities")
        email = st.text_input("Enter your email to receive notifications", key="scholarship_email")
        if st.button("Subscribe to Alerts"):
            if email:
                st.success(f"✅ You'll receive alerts at {email} when new scholarships open!")
            else:
                st.error("Please enter a valid email address")
    
    with tab2:
        st.markdown("### 🤝 Mentorship Programs")
        st.markdown("Connect with structured mentorship programs designed for women and underrepresented communities in tech")
        
        for program in hub_data['mentorship_programs']:
            st.markdown(f"""
            <div style="background: white; border-left: 5px solid #8b5cf6; 
                        padding: 1.5rem; margin: 1rem 0; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <h3 style="margin: 0; color: #5b21b6;">{program['name']}</h3>
                <p style="margin: 0.8rem 0; line-height: 1.6;">{program['description']}</p>
                <div style="display: flex; gap: 2rem; margin: 1rem 0; flex-wrap: wrap;">
                    <div><strong>Duration:</strong> {program['duration']}</div>
                    <div><strong>Cost:</strong> {program['cost']}</div>
                    <div><strong>For:</strong> {program['target_audience']}</div>
                </div>
                <a href="{program['application_link']}" target="_blank"
                   style="display: inline-block; background: #8b5cf6; color: white; 
                          padding: 0.7rem 1.5rem; border-radius: 8px; text-decoration: none; 
                          font-weight: 600; margin-top: 1rem;">
                    Apply Now →
                </a>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🌐 Women in Tech Communities")
        st.markdown("Join professional communities for networking, support, and career growth")
        
        cols = st.columns(2)
        for idx, community in enumerate(hub_data['communities']):
            with cols[idx % 2]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ec4899 0%, #be185d 100%); 
                            color: white; padding: 1.5rem; border-radius: 12px; margin: 0.5rem 0;">
                    <h4 style="margin: 0; color: white;">{community['name']}</h4>
                    <p style="margin: 0.5rem 0; opacity: 0.9;">👥 {community['members']} members</p>
                    <p style="margin: 0.5rem 0; opacity: 0.9;">Focus: {community['focus']}</p>
                    <a href="{community['link']}" target="_blank"
                       style="color: white; text-decoration: underline; font-weight: 600;">
                        Join Community →
                    </a>
                </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 🏢 Companies with Strong DEI Commitment")
        st.markdown("""
        These companies have demonstrated strong commitment to diversity, equity, and inclusion in tech. 
        The insights show their current diversity metrics, initiatives, and policies.
        
        **What the scores mean:**
        - 🟢 **4.5+** = Excellent DEI practices
        - 🟠 **4.0-4.4** = Good DEI practices
        - 🔴 **Below 4.0** = Developing DEI practices
        """)
        
        industry_data = load_industry_data()
        dei_companies = industry_data['company_dei_insights']
        
        # Show top DEI companies
        for company in dei_companies[:7]:
            display_dei_company_card(company)


# ============================================================================
# # PAGE: WOMEN LEADERS (MERGED WITH MENTORSHIP)
# ============================================================================

elif page == "🌟 Women Leaders":
    st.header("🌟 Women Leaders in AI & Mentorship")
    
    st.markdown("""
    ### 💡 Why This Matters
    Learn from successful women leaders who have paved the way in AI, and connect with experienced mentors 
    who can guide you through your career journey. Representation matters, and seeing others who have succeeded 
    in similar circumstances can inspire and inform your own path.
    
    ### 🎯 How to Use This Section
    - **Toggle mentorship mode** to see mentors first if you're actively seeking guidance
    - **Filter by location and specialization** to find relevant role models
    - **Read their stories** to understand different career trajectories
    - **Contact mentors** if you're looking for one-on-one guidance
    """)
    
    # Check if user is seeking mentorship
    seeking_mentorship = st.checkbox("🤝 I'm seeking mentorship", value=False)
    
    if seeking_mentorship:
        # SHOW MENTORSHIP FIRST
        st.markdown("---")
        st.markdown("## 🤝 Find Your Perfect Mentor")
        st.markdown("""
        Connect with experienced professionals who have overcome similar challenges and are here 
        to guide you through your AI journey. Match with mentors based on your industry, background, and career goals.
        """)
        
        mentorship_matching_ui()
        
        # THEN SHOW WOMEN LEADERS BELOW
        st.markdown("---")
        st.markdown("## 👩‍💼 Women Leaders in AI")
    else:
        # SHOW WOMEN LEADERS FIRST
        st.markdown("## 👩‍💼 Discover Inspiring Women in AI")
    
    st.markdown("""
    Learn from successful women who are shaping the future of AI. Filter by location and 
    specialization to find role models in your area of interest.
    """)
    
    women_data = load_women_in_ai_data()
    leaders = women_data['women_leaders']
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        countries = ["All"] + sorted(list(set([l['country'] for l in leaders])))
        selected_country = st.selectbox("🌍 Filter by Country", countries)
    with col2:
        specializations = ["All"] + sorted(list(set([l['specialization'] for l in leaders])))
        selected_specialization = st.selectbox("🎯 Filter by Specialization", specializations)
    
    # Filter and display
    filtered_leaders = filter_women_leaders(leaders, selected_country, None, selected_specialization)
    
    st.markdown(f"### Showing {len(filtered_leaders)} leader(s)")
    
    for leader in filtered_leaders:
        display_leader_card(leader)
    
    if len(filtered_leaders) == 0:
        st.info("No leaders match your filters. Try adjusting your selection.")
    
    # If NOT seeking mentorship, show mentorship section at bottom
    if not seeking_mentorship:
        st.markdown("---")
        st.markdown("## 🤝 Interested in Mentorship?")
        st.info("💡 Check the box at the top of this page to find mentors who can guide your AI journey!")

# ============================================================================
# PAGE: COMMUNITY FORUMS
# ============================================================================

elif page == "💬 Community Forums":
    st.header("💬 Community Discussion Forums")
    
    st.markdown("""
    ### 💡 Why This Matters
    Connecting with peers who share your background, industry, or career goals provides emotional support, 
    practical advice, and networking opportunities. You're not alone in your journey.
    
    ### 🎯 How to Use This Section
    - Browse **forum categories** (Women in AI, Identity-Based, Industry, Career Stage)
    - Select a **specific forum** that matches your interests
    - Read **discussions** to learn from others' experiences
    - **Ask questions** and share your own insights
    """)
    
    # Forum categories
    forum_categories = {
        "👩‍💼 Women in AI": [
            "Women in Healthcare AI",
            "Women in Finance AI",
            "Women in Tech Leadership",
            "Returning to Tech After Career Break"
        ],
        "🌍 Identity-Based Groups": [
            "Black in AI",
            "Latinx in AI",
            "South Asian AI Professionals",
            "LGBTQ+ in Tech",
            "First-Generation Professionals"
        ],
        "🏢 Industry Groups": [
            "Healthcare AI Practitioners",
            "Financial AI Professionals",
            "Retail & E-commerce AI",
            "Manufacturing & IoT AI"
        ],
        "🎓 Skill Level": [
            "Beginners Transitioning to AI",
            "Career Changers (Non-STEM to AI)",
            "Self-Taught & Bootcamp Graduates",
            "Advanced ML Practitioners"
        ]
    }
    
    # Display forum categories
    for category, forums in forum_categories.items():
        with st.expander(f"{category} ({len(forums)} groups)", expanded=False):
            for forum in forums:
                st.markdown(f"""
                <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; 
                            margin: 1rem 0; border-radius: 12px; cursor: pointer;">
                    <h4 style="margin: 0; color: #1e293b;">💬 {forum}</h4>
                    <p style="margin: 0.5rem 0; color: #64748b;">
                        Join the conversation • 150+ members • 45 discussions
                    </p>
                    <div style="margin-top: 1rem;">
                        <span style="background: #dbeafe; color: #1e40af; padding: 0.4rem 0.8rem; 
                                     border-radius: 15px; font-size: 0.9rem; margin-right: 0.5rem;">
                            Active
                        </span>
                        <span style="background: #fef3c7; color: #b45309; padding: 0.4rem 0.8rem; 
                                     border-radius: 15px; font-size: 0.9rem;">
                            Moderated
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Placeholder join button
                if st.button(f"Join {forum}", key=f"join_{forum}"):
                    st.success(f"✅ Joined {forum}! Welcome to the community.")
    
    st.markdown("---")
    st.info("""
    **🛡️ Community Guidelines:**
    • Respect and support all members
    • Share experiences and knowledge
    • No discrimination or harassment
    • Maintain confidentiality of sensitive discussions
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 2rem 0;">
    <p>🧭 Skill Recognition Engine | Empowering Diverse Talent in AI</p>
    <p style="font-size: 0.9rem;">
        Made with ❤️ for women, underrepresented communities, and career transitioners
    </p>
</div>
""", unsafe_allow_html=True)
