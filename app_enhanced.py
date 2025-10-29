"""
Skill Recognition Engine - Enhanced with Women in AI, Industry Customization, and Inclusivity Features
A comprehensive Streamlit application for skill recognition and career matching with DEI focus
"""

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
    get_skill_names
)
from equity_utils import (
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
                     border-radius: 50%; border: 3px solid white;" />
            </div>
            <div style="flex-grow: 1;">
                <h3 style="margin: 0; color: white;">{leader['name']}</h3>
                <p style="margin: 0.3rem 0; font-size: 1.1rem; opacity: 0.9;">
                    {leader['title']}
                </p>
                <p style="margin: 0.5rem 0; font-size: 0.9rem;">
                    🌍 {leader['country']} | 🎯 {leader['specialization']} | 👥 {leader['ethnicity']}
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
                     border-radius: 15px; border: 3px solid #f472b6;" />
            </div>
            <div style="flex-grow: 1;">
                <h2 style="margin: 0; color: #be185d;">{mentor['name']}</h2>
                <p style="margin: 0.5rem 0; font-size: 1.2rem; color: #831843; font-weight: 600;">
                    {mentor['current_role']} at {mentor['company']}
                </p>
                <p style="margin: 0.5rem 0; color: #666;">
                    🌍 {mentor['ethnicity']} | 💼 {mentor['experience_years']} years experience | 
                    🏢 {mentor['industry']}
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
        "🏠 Home & Women Leaders",
        "👩‍💼 Women's Hub",
        "🤝 Mentorship Matching",
        "🏢 Industry Customization",
        "🔍 Upload CV & Analyze",
        "👤 Demographic Profile",
        "✨ Recognized Skills",
        "🧠 AI Role Matches",
        "📈 Skill Gap Analysis",
        "🌍 Equity & Support",
        "🪪 Skill Passport",
        "💬 Community Forums"
    ]
)

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
# PAGE: HOME & WOMEN LEADERS
# ============================================================================

if page == "🏠 Home & Women Leaders":
    st.header("🌟 Women Leaders in AI")
    st.markdown("""
    Discover inspiring women who are shaping the future of AI. Filter by location, 
    ethnicity, or specialization to find role models in your area of interest.
    """)
    
    women_data = load_women_in_ai_data()
    leaders = women_data['women_leaders']
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        countries = ["All"] + sorted(list(set([l['country'] for l in leaders])))
        selected_country = st.selectbox("🌍 Filter by Country", countries)
    with col2:
        ethnicities = ["All"] + sorted(list(set([l['ethnicity'] for l in leaders])))
        selected_ethnicity = st.selectbox("👥 Filter by Ethnicity", ethnicities)
    with col3:
        specializations = ["All"] + sorted(list(set([l['specialization'] for l in leaders])))
        selected_specialization = st.selectbox("🎯 Filter by Specialization", specializations)
    
    # Filter and display
    filtered_leaders = filter_women_leaders(leaders, selected_country, selected_ethnicity, selected_specialization)
    
    st.markdown(f"### Showing {len(filtered_leaders)} leader(s)")
    
    for leader in filtered_leaders:
        display_leader_card(leader)
    
    if len(filtered_leaders) == 0:
        st.info("No leaders match your filters. Try adjusting your selection.")

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
    st.markdown("Select your industry to get tailored AI role recommendations and skill translations")
    
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
# PAGE: UPLOAD CV & ANALYZE
# ============================================================================

elif page == "🔍 Upload CV & Analyze":
    st.header("🔍 Upload Your CV or Profile")
    st.markdown("Upload your CV, resume, or paste your LinkedIn profile to extract your skills.")
    
    # Input method selection
    input_method = st.radio("Choose input method:", ["📤 Upload File", "📋 Paste Text", "❓ Quick Skill Quiz"])
    
    if input_method == "📤 Upload File":
        uploaded_file = st.file_uploader("Upload your CV (PDF/TXT)", type=['pdf', 'txt'])
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                st.session_state.text = uploaded_file.read().decode('utf-8')
            else:
                st.session_state.text = ingest_and_clean(uploaded_file)
            st.success("✅ File uploaded successfully!")
            with st.expander("View extracted text"):
                st.text_area("Content", st.session_state.text, height=200)
    
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
                st.session_state.user_vector = compute_user_vector(skills)
                matches = match_roles(st.session_state.user_vector)
                st.session_state.matches = matches
                st.success("✅ Analysis complete! Check 'Recognized Skills' to see results.")

# ============================================================================
# PAGE: DEMOGRAPHIC PROFILE
# ============================================================================

elif page == "👤 Demographic Profile":
    st.header("👤 Your Demographic Profile (Optional)")
    st.markdown("""
    This information helps us provide personalized support, equity analysis, and connect you 
    with relevant communities. **All information is confidential and optional.**
    """)
    
    if st.session_state.anonymous_mode:
        st.warning("🔒 Anonymous mode is active. Demographic info will not be collected.")
    else:
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
        
        if st.button("💾 Save Demographic Profile", type="primary"):
            st.session_state.demographic_info = {
                'gender': gender if gender != "Prefer not to say" else None,
                'ethnicity': ethnicity if ethnicity != "Prefer not to say" else None,
                'background': background if background != "Prefer not to say" else None,
                'years_experience': years_experience,
                'current_industry': current_industry,
                'first_gen': first_gen
            }
            st.session_state.show_equity_analysis = True
            st.success("✅ Profile saved! Check 'Equity & Support' for personalized insights.")

# ============================================================================
# PAGE: RECOGNIZED SKILLS
# ============================================================================

elif page == "✨ Recognized Skills":
    st.header("✨ Your Recognized Skills")
    
    if not st.session_state.recognized_skills:
        st.info("👆 Please upload your CV in the 'Upload CV & Analyze' section first")
    else:
        skills = st.session_state.recognized_skills
        
        # Apply equity enhancement if demographic info provided
        if st.session_state.demographic_info and not st.session_state.anonymous_mode:
            gender = st.session_state.demographic_info.get('gender')
            ethnicity = st.session_state.demographic_info.get('ethnicity')
            
            if gender or ethnicity:
                enhanced_skills, inferred_skills = enhance_skills_with_confidence(skills, gender, ethnicity)
                
                # Show confidence message
                conf_msg = generate_confidence_message(gender, ethnicity, 
                                                      st.session_state.demographic_info.get('background'))
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
        
        # Display skills by category
        hard_skills = [s for s in skills if s.get('category') == 'hard']
        soft_skills = [s for s in skills if s.get('category') == 'soft']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💻 Technical Skills")
            st.markdown(f"**Found: {len(hard_skills)} skills**")
            for skill in hard_skills:
                st.markdown(f'<span class="skill-tag-hard">{skill["name"]}</span>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🤝 Soft Skills")
            st.markdown(f"**Found: {len(soft_skills)} skills**")
            for skill in soft_skills:
                st.markdown(f'<span class="skill-tag-soft">{skill["name"]}</span>', unsafe_allow_html=True)
        
        # Industry translation if industry selected
        if st.session_state.industry_selection:
            st.markdown("---")
            st.markdown(f"### 🏢 Your Skills in {st.session_state.industry_selection['name']}")
            st.markdown("Here's how your skills translate to this industry:")
            
            skill_names = [s['name'] for s in skills]
            translations = translate_skills_for_industry(skill_names, st.session_state.industry_selection)
            
            for skill, translation in translations.items():
                if translation != skill:
                    st.markdown(f"""
                    <div style="background: #f0fdf4; border-left: 4px solid #16a34a; 
                                padding: 1rem; margin: 0.5rem 0; border-radius: 4px;">
                        <strong style="color: #15803d;">{skill}</strong> → {translation}
                    </div>
                    """, unsafe_allow_html=True)

# ============================================================================
# PAGE: AI ROLE MATCHES
# ============================================================================

elif page == "🧠 AI Role Matches":
    st.header("🧠 Your Top AI Role Matches")
    
    if not st.session_state.matches:
        st.info("👆 Please analyze your CV first in the 'Upload CV & Analyze' section")
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
        
        st.markdown(f"### Found {len(matches)} matching roles")
        
        for idx, role in enumerate(matches[:10], 1):
            with st.expander(f"{idx}. {role['role']} - {role['similarity']:.1%} match", expanded=(idx <= 3)):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description:** {role.get('description', 'N/A')}")
                    st.markdown(f"**Required Skills:** {', '.join(role.get('required_skills', [])[:5])}")
                    
                    # Show equity insight if available
                    if 'equity_insight' in role:
                        st.info(f"💡 {role['equity_insight']}")
                
                with col2:
                    st.metric("Match Score", f"{role['similarity']:.1%}")
                    
                    # Salary with equity adjustment
                    if 'salary_range' in role:
                        salary_range = role['salary_range']
                        st.markdown(f"**💰 Salary Range:** {salary_range}")
                        
                        # Show equity-adjusted salary
                        if st.session_state.demographic_info and not st.session_state.anonymous_mode:
                            gender = st.session_state.demographic_info.get('gender')
                            ethnicity = st.session_state.demographic_info.get('ethnicity')
                            
                            if gender or ethnicity:
                                salary_info = calculate_equity_adjusted_salary(salary_range, gender, ethnicity)
                                if salary_info:
                                    st.markdown("**Equity-Adjusted Analysis:**")
                                    st.markdown(f"• Market range: {salary_info['market_range']}")
                                    st.markdown(f"• Typical offer: {salary_info['typical_range']}")
                                    st.markdown(f"• Target (fair): {salary_info['target_range']}")
                                    if salary_info['negotiation_tip']:
                                        st.warning(f"⚠️ {salary_info['negotiation_tip']}")

# ============================================================================
# PAGE: SKILL GAP ANALYSIS
# ============================================================================

elif page == "📈 Skill Gap Analysis":
    st.header("📈 Skill Gap Analysis & Learning Recommendations")
    
    if not st.session_state.matches or not st.session_state.recognized_skills:
        st.info("👆 Please analyze your CV and check role matches first")
    else:
        st.markdown("Select a target role to see what skills you need to develop:")
        
        role_names = [r['role'] for r in st.session_state.matches[:10]]
        selected_role = st.selectbox("Target Role", role_names)
        
        # Find the selected role
        role_data = next(r for r in st.session_state.matches if r['role'] == selected_role)
        
        # Get user skills
        user_skills = set([s['name'].lower() for s in st.session_state.recognized_skills])
        required_skills = set([s.lower() for s in role_data.get('required_skills', [])])
        
        # Calculate gaps
        missing_skills = required_skills - user_skills
        matched_skills = required_skills & user_skills
        
        # Display
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Skills You Have")
            for skill in matched_skills:
                st.markdown(f"• {skill.title()}")
        
        with col2:
            st.markdown("### 📚 Skills to Learn")
            for skill in missing_skills:
                st.markdown(f"• {skill.title()}")
        
        # Learning recommendations
        if missing_skills:
            st.markdown("---")
            st.markdown("### 🎓 Recommended Learning Resources")
            
            bridges = recommend_bridges(list(missing_skills))
            for bridge in bridges[:5]:
                st.markdown(f"""
                <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; 
                            margin: 1rem 0; border-radius: 12px;">
                    <h4 style="margin: 0; color: #1e293b;">{bridge['name']}</h4>
                    <p style="margin: 0.5rem 0;">{bridge.get('description', '')}</p>
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
# PAGE: EQUITY & SUPPORT
# ============================================================================

elif page == "🌍 Equity & Support":
    st.header("🌍 Equity Analysis & Support Resources")
    
    if not st.session_state.demographic_info or st.session_state.anonymous_mode:
        st.info("👆 Please fill out your demographic profile first (unless in anonymous mode)")
    else:
        demo = st.session_state.demographic_info
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
            if st.session_state.matches and ethnicity:
                st.markdown("---")
                st.markdown("### 📊 Representation Analysis")
                gap_analysis = analyze_representation_gap(st.session_state.matches, ethnicity)
                if gap_analysis:
                    st.info(gap_analysis)
            
            # Support resources
            st.markdown("---")
            st.markdown("### 🤝 Support Resources & Communities")
            
            resources = get_support_resources(gender, ethnicity, background)
            
            if resources.get('communities'):
                st.markdown("**🌐 Communities:**")
                cols = st.columns(3)
                for idx, community in enumerate(resources['communities'][:6]):
                    with cols[idx % 3]:
                        st.markdown(f"""
                        <div style="background: #fef3c7; border: 2px solid #f59e0b; 
                                    padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                            <strong style="color: #b45309;">{community}</strong>
                        </div>
                        """, unsafe_allow_html=True)
            
            if resources.get('companies'):
                st.markdown("**🏢 Companies with Strong DEI:**")
                cols = st.columns(4)
                for idx, company in enumerate(resources['companies'][:8]):
                    with cols[idx % 4]:
                        st.markdown(f"""
                        <div style="background: #dbeafe; padding: 0.8rem; 
                                    border-radius: 6px; text-align: center;">
                            {company}
                        </div>
                        """, unsafe_allow_html=True)
            
            # DEI company insights
            st.markdown("---")
            st.markdown("### 🏢 Detailed Company DEI Insights")
            
            industry_data = load_industry_data()
            dei_companies = industry_data['company_dei_insights']
            
            # Show top DEI companies
            for company in dei_companies[:5]:
                display_dei_company_card(company)

# ============================================================================
# PAGE: SKILL PASSPORT
# ============================================================================

elif page == "🪪 Skill Passport":
    st.header("🪪 Generate Your Skill Passport")
    st.markdown("Create a verified digital passport of your skills for employers and institutions")
    
    if not st.session_state.recognized_skills:
        st.info("👆 Please analyze your CV first to generate a passport")
    else:
        if st.button("🎨 Generate Skill Passport", type="primary"):
            with st.spinner("Creating your passport..."):
                passport_data = generate_skill_passport(
                    st.session_state.recognized_skills,
                    st.session_state.matches[:5] if st.session_state.matches else []
                )
                
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
                        <h3>Verified Skills: {len(st.session_state.recognized_skills)}</h3>
                        <h3>Top Role Matches: {len(st.session_state.matches[:5])}</h3>
                        <h3>Passport ID: {passport_data.get('id', 'N/A')}</h3>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Download options
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 Download JSON",
                        data=json.dumps(passport_data, indent=2),
                        file_name="skill_passport.json",
                        mime="application/json"
                    )
                with col2:
                    if st.button("📄 Generate PDF"):
                        pdf_path = create_pdf_passport(passport_data)
                        st.success(f"✅ PDF created: {pdf_path}")

# ============================================================================
# PAGE: COMMUNITY FORUMS
# ============================================================================

elif page == "💬 Community Forums":
    st.header("💬 Community Discussion Forums")
    st.markdown("""
    Connect with peers who share your identity, industry, or career goals. Share experiences, 
    ask questions, and find support.
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
        Made with ❤️ for women, underrepresented minorities, and career changers
    </p>
</div>
""", unsafe_allow_html=True)
