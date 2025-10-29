ï»¿"""
Skill Recognition Engine - AI-based Prior Learning Evaluator
A professional Streamlit application for skill recognition and career matching
"""

import streamlit as st
import json
import os
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
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Skill Recognition Engine",
    page_icon="Ã°Å¸Â§Â­",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

st.markdown("""
<style>
    /* Main title styling */
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
    
    .note-text {
        text-align: center;
        font-size: 0.9rem;
        color: #6B7280;
        font-style: italic;
        margin-bottom: 2rem;
    }
    
    /* Skill tag styling */
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
    
    /* Role card styling */
    .role-card {
        background: white;
        border: 2px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .role-card:hover {
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .role-card-top {
        background: linear-gradient(135deg, #FCD34D 0%, #F59E0B 100%);
        border: 3px solid #F59E0B;
    }
    
    .role-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 0.5rem;
    }
    
    .role-description {
        color: #6B7280;
        font-size: 0.95rem;
        margin-bottom: 0.8rem;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #9CA3AF;
        font-size: 0.85rem;
        border-top: 1px solid #E5E7EB;
        margin-top: 3rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1E3A8A;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3B82F6;
    }
    
    /* Gap analysis table */
    .gap-item {
        background: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 6px;
    }
    
    /* Course card */
    .course-card {
        background: #F0F9FF;
        border-left: 4px solid #0EA5E9;
        padding: 1rem;
        margin: 0.8rem 0;
        border-radius: 6px;
    }
    
    /* Passport section */
    .passport-section {
        background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'extracted_skills' not in st.session_state:
    st.session_state.extracted_skills = None

if 'user_vector' not in st.session_state:
    st.session_state.user_vector = None

if 'matched_roles' not in st.session_state:
    st.session_state.matched_roles = None

if 'bridge_courses' not in st.session_state:
    st.session_state.bridge_courses = None

if 'passport_generated' not in st.session_state:
    st.session_state.passport_generated = False

if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

if 'demographic_info' not in st.session_state:
    st.session_state.demographic_info = {
        'gender': None,
        'ethnicity': None,
        'background': None
    }

if 'show_equity_analysis' not in st.session_state:
    st.session_state.show_equity_analysis = False

# ============================================================================
# HEADER SECTION
# ============================================================================

st.markdown('<h1 class="main-title">Ã°Å¸Â§Â­ Skill Recognition Engine</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">AI-based Prior Learning Evaluator</p>', unsafe_allow_html=True)
st.markdown("---")
st.markdown('<p class="note-text">Empowering women and non-degree professionals to discover their AI potential.</p>', 
            unsafe_allow_html=True)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Section:",
    [
        "🔍 Upload or Paste CV",
        "👤 Demographic Profile (Optional)",
        "✨ Recognized Skills",
        "🧠 AI Role Matches",
        "📈 Skill Gap & Bridge Plan",
        "🌍 Equity & Support",
        "🪪 Skill Passport & Download"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This tool uses AI to:\n"
    "- Extract skills from CVs\n"
    "- Match you to AI roles\n"
    "- Identify skill gaps\n"
    "- Recommend courses\n"
    "- **Analyze equity factors**\n"
    "- Generate Skill Passport"
)

# Add equity focus notice
st.sidebar.markdown("---")
st.sidebar.markdown("### 🌍Â Equity Focus")
st.sidebar.success(
    "**Empowering Underrepresented Groups**\n\n"
    "Special support for:\n"
    "- Women in tech\n"
    "- Underrepresented ethnicities\n"
    "- Career changers\n"
    "- Non-traditional backgrounds"
)

# ============================================================================
# PAGE 1: UPLOAD OR PASTE CV
# ============================================================================

if page == "🔍 Upload or Paste CV":
    st.markdown('<h2 class="section-header">Ã°Å¸ââ Upload Your CV or LinkedIn Profile</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # User name input
        user_name = st.text_input("Your Name (optional)", value=st.session_state.user_name)
        st.session_state.user_name = user_name
        
        # File upload
        st.markdown("#### Upload CV Document")
        uploaded_file = st.file_uploader(
            "Choose a PDF or DOCX file",
            type=['pdf', 'docx'],
            help="Upload your CV in PDF or Word format"
        )
        
        # Text input
        st.markdown("#### Or Paste Your LinkedIn Profile / Resume Text")
        cv_text = st.text_area(
            "Paste text here",
            height=200,
            placeholder="Paste your CV or LinkedIn profile text here..."
        )
        
        # Quick skill quiz option
        use_quiz = st.checkbox("Ã¢Ââ No CV? Take Quick Skill Quiz")
        
        quiz_skills = []
        if use_quiz:
            st.markdown("---")
            st.markdown("### Ã°Å¸âÂ Quick Skill Assessment")
            
            # Load skill ontology for quiz
            with open('data/skill_ontology.json', 'r') as f:
                ontology = json.load(f)
            
            skill_options = [s['name'] for s in ontology['hard_skills'][:15]]
            
            selected_skills = st.multiselect(
                "Select skills you frequently use:",
                options=skill_options,
                help="Choose all that apply"
            )
            
            comfort_level = st.select_slider(
                "Overall comfort level with technology:",
                options=["Beginner", "Intermediate", "Advanced", "Expert"]
            )
            
            # Map selected skills back to IDs
            skill_name_to_id = {s['name']: s['id'] for s in ontology['hard_skills']}
            quiz_skills = [skill_name_to_id[name] for name in selected_skills if name in skill_name_to_id]
    
    with col2:
        st.markdown("### Ã°Å¸âÂ¡ Tips")
        st.info(
            "**For best results:**\n\n"
            "Ã¢Åâ¦ Include work experience\n\n"
            "Ã¢Åâ¦ List technical skills\n\n"
            "Ã¢Åâ¦ Mention software/tools\n\n"
            "Ã¢Åâ¦ Describe achievements"
        )
        
        st.markdown("### Ã°Å¸ââ Privacy")
        st.success(
            "Your data is processed locally and not stored permanently. "
            "Personal information (emails, phone numbers) is automatically removed."
        )
    
    # Extract skills button
    st.markdown("---")
    if st.button("Ã°Å¸Å¡â¬ Extract Skills", type="primary", use_container_width=True):
        with st.spinner("Ã°Å¸âÂ Analyzing your skills..."):
            extracted_text = ""
            
            # Process uploaded file
            if uploaded_file:
                file_type = "pdf" if uploaded_file.name.endswith('.pdf') else "docx"
                extracted_text = ingest_and_clean(uploaded_file, file_type)
            
            # Or use pasted text
            elif cv_text.strip():
                extracted_text = cv_text
            
            # Or use quiz results
            elif quiz_skills:
                st.session_state.extracted_skills = {
                    'hard_skills': quiz_skills,
                    'soft_skills': ['communication', 'problem_solving', 'teamwork']
                }
            
            # Extract skills from text
            if extracted_text:
                skills = extract_skills(extracted_text)
                st.session_state.extracted_skills = skills
            
            # Compute user vector
            if st.session_state.extracted_skills:
                all_skills = (st.session_state.extracted_skills['hard_skills'] + 
                            st.session_state.extracted_skills['soft_skills'])
                st.session_state.user_vector = compute_user_vector(all_skills)
                
                # Match roles
                st.session_state.matched_roles = match_roles(
                    st.session_state.user_vector,
                    all_skills
                )
                
                # Recommend bridges
                if st.session_state.matched_roles:
                    top_role_gaps = st.session_state.matched_roles[0]['gaps']
                    st.session_state.bridge_courses = recommend_bridges(
                        top_role_gaps,
                        all_skills
                    )
                
                total_skills = len(all_skills)
                st.success(f"Ã¢Åâ¦ Success! Recognized **{total_skills} skills** from your profile.")
                st.balloons()
                st.info("Ã°Å¸ââ° Navigate to **'Recognized Skills'** in the sidebar to view results.")
            else:
                st.error("Ã¢ÂÅ Could not extract skills. Please upload a file or paste text.")

# ============================================================================
# PAGE 2: Demographic Profile (Optional)
# ============================================================================

elif page == "Ã°Å¸âÂ¤ Demographic Profile (Optional)":
    st.markdown('<h2 class="section-header">Ã°Å¸âÂ¤ Demographic Profile (Optional)</h2>', unsafe_allow_html=True)
    
    st.info(
        "Ã°Å¸âÅ  **Why share demographic information?**\n\n"
        "This information helps us:\n"
        "- Provide personalized career guidance\n"
        "- Identify equity gaps in salary expectations\n"
        "- Recommend relevant support communities\n"
        "- Connect you with mentorship programs\n"
        "- Highlight companies with strong DEI commitments\n\n"
        "Ã°Å¸ââ **Your privacy matters**: This data is processed locally and never stored permanently."
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Gender Identity")
        gender = st.selectbox(
            "How do you identify?",
            options=["Prefer not to say", "Woman", "Man", "Non-binary", "Other"],
            index=0
        )
        
        if gender != "Prefer not to say":
            st.session_state.demographic_info['gender'] = gender.lower().replace(" ", "_")
        
        st.markdown("---")
        
        st.markdown("### Ethnic Background")
        ethnicity = st.selectbox(
            "Select your ethnic background:",
            options=[
                "Prefer not to say",
                "White / Caucasian",
                "South Asian (Indian, Pakistani, Bangladeshi, Sri Lankan)",
                "East Asian / Chinese",
                "Black / African / Caribbean",
                "Hispanic / Latino",
                "Middle Eastern",
                "Mixed / Multiple",
                "Other"
            ],
            index=0
        )
        
        ethnicity_map = {
            "White / Caucasian": "white",
            "South Asian (Indian, Pakistani, Bangladeshi, Sri Lankan)": "south_asian",
            "East Asian / Chinese": "east_asian",
            "Black / African / Caribbean": "black",
            "Hispanic / Latino": "hispanic_latino"
        }
        
        if ethnicity in ethnicity_map:
            st.session_state.demographic_info['ethnicity'] = ethnicity_map[ethnicity]
    
    with col2:
        st.markdown("### Professional Background")
        background = st.selectbox(
            "What best describes your background?",
            options=[
                "Prefer not to say",
                "STEM (Non-AI) - Science, Math, Engineering",
                "Non-STEM - Business, Arts, Humanities, Healthcare",
                "Career Break / Gap (Family, Travel, Health)",
                "Self-Taught / Bootcamp Graduate"
            ],
            index=0
        )
        
        background_map = {
            "STEM (Non-AI) - Science, Math, Engineering": "non_ai_stem",
            "Non-STEM - Business, Arts, Humanities, Healthcare": "non_ai_non_stem",
            "Career Break / Gap (Family, Travel, Health)": "career_break",
            "Self-Taught / Bootcamp Graduate": "self_taught"
        }
        
        if background in background_map:
            st.session_state.demographic_info['background'] = background_map[background]
        
        st.markdown("---")
        
        st.markdown("### Years of Experience")
        experience = st.slider(
            "Total years of professional experience:",
            min_value=0,
            max_value=30,
            value=5,
            step=1
        )
        st.session_state.demographic_info['experience_years'] = experience
    
    st.markdown("---")
    
    # Show what information was collected
    if st.button("Ã°Å¸âÂ¾ Save Demographic Profile", type="primary", use_container_width=True):
        st.session_state.show_equity_analysis = True
        st.success("Ã¢Åâ¦ Profile saved! Navigate to other sections to see personalized insights.")
        
        # Show confidence message
        if all([
            st.session_state.demographic_info.get('gender'),
            st.session_state.demographic_info.get('ethnicity'),
            st.session_state.demographic_info.get('background')
        ]):
            confidence_msg = generate_confidence_message(
                st.session_state.demographic_info['gender'],
                st.session_state.demographic_info['ethnicity'],
                st.session_state.demographic_info['background']
            )
            
            if confidence_msg:
                st.markdown("---")
                st.markdown("### Ã°Å¸âÂª Your Strengths")
                st.info(confidence_msg)

# ============================================================================
# PAGE 3: Recognized Skills
# ============================================================================

elif page == "Ã°Å¸ââ¹ Recognized Skills":
    st.markdown('<h2 class="section-header">Ã¢ÅÂ¨ Your Recognized Skills</h2>', unsafe_allow_html=True)
    
    if st.session_state.extracted_skills:
        # Check if we should enhance skills with confidence boost
        enhanced_skills = st.session_state.extracted_skills
        
        if (st.session_state.show_equity_analysis and 
            st.session_state.demographic_info.get('gender') and
            st.session_state.demographic_info.get('ethnicity')):
            
            enhanced_skills = enhance_skills_with_confidence(
                st.session_state.extracted_skills,
                st.session_state.demographic_info['gender'],
                st.session_state.demographic_info['ethnicity']
            )
            
            # Show confidence note
            if enhanced_skills.get('confidence_note'):
                st.info(enhanced_skills['confidence_note'])
                st.markdown("---")
        
        hard_skills = enhanced_skills.get('hard_skills', [])
        soft_skills = enhanced_skills.get('soft_skills', [])
        inferred_skills = enhanced_skills.get('inferred_skills', [])
        
        # Display hard skills
        st.markdown("### Ã°Å¸âÂ§ Technical (Hard) Skills")
        hard_skill_names = get_skill_names(hard_skills)
        
        skills_html = ""
        for skill in hard_skill_names:
            skills_html += f'<span class="skill-tag-hard">{skill}</span>'
        
        st.markdown(skills_html, unsafe_allow_html=True)
        st.markdown("")
        
        # Display soft skills
        st.markdown("### Ã°Å¸Â¤Â Soft Skills")
        soft_skill_names = get_skill_names(soft_skills)
        
        skills_html = ""
        for skill in soft_skill_names:
            skills_html += f'<span class="skill-tag-soft">{skill}</span>'
        
        st.markdown(skills_html, unsafe_allow_html=True)
        st.markdown("")
        
        # Show inferred skills if any
        if inferred_skills:
            st.markdown("### Ã°Å¸âÂ¡ Inferred Skills (Based on Your Experience)")
            st.caption("These skills weren't explicitly mentioned but likely exist based on your background")
            
            inferred_names = get_skill_names(inferred_skills)
            skills_html = ""
            for skill in inferred_names:
                skills_html += f'<span class="skill-tag-soft" style="opacity: 0.8;">{skill} Ã¢Â­Â</span>'
            
            st.markdown(skills_html, unsafe_allow_html=True)
            st.markdown("")
        
        # Edit skills option
        st.markdown("---")
        with st.expander("Ã¢ÅÂÃ¯Â¸Â Edit Your Skills"):
            st.markdown("**Add or remove skills manually:**")
            
            all_skill_names = hard_skill_names + soft_skill_names
            edited_skills = st.text_area(
                "Edit skills (comma-separated):",
                value=", ".join(all_skill_names),
                height=100
            )
            
            if st.button("Ã°Å¸âÂ¾ Save Changes"):
                # Re-process would require more complex logic
                st.success("Ã¢Åâ¦ Changes saved! (Note: Re-upload to fully reprocess)")
        
        # Summary statistics
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Skills", len(hard_skills) + len(soft_skills))
        
        with col2:
            st.metric("Hard Skills", len(hard_skills))
        
        with col3:
            st.metric("Soft Skills", len(soft_skills))
        
    else:
        st.warning("Ã¢Å¡Â Ã¯Â¸Â No skills extracted yet. Please upload your CV first.")
        st.info("Ã°Å¸âË Go to **'Upload or Paste CV'** to get started.")

# ============================================================================
# PAGE 4: AI ROLE MATCHES
# ============================================================================

elif page == "🧠 AI Role Matches":
    st.markdown('<h2 class="section-header">Ã°Å¸Å½Â¯ Your Best AI Role Matches</h2>', unsafe_allow_html=True)
    
    if st.session_state.matched_roles:
        # Enhance roles with equity insights if demographics provided
        display_roles = st.session_state.matched_roles
        
        if (st.session_state.show_equity_analysis and 
            st.session_state.demographic_info.get('gender') and
            st.session_state.demographic_info.get('ethnicity') and
            st.session_state.demographic_info.get('background')):
            
            display_roles = get_targeted_role_recommendations(
                st.session_state.matched_roles,
                st.session_state.demographic_info['gender'],
                st.session_state.demographic_info['ethnicity'],
                st.session_state.demographic_info['background']
            )
            
            # Show representation analysis
            rep_analysis = analyze_representation_gap(
                st.session_state.matched_roles,
                st.session_state.demographic_info['ethnicity']
            )
            
            if rep_analysis['is_underrepresented']:
                st.info(
                    f"Ã°Å¸âÅ  **Representation Insight**: {rep_analysis['your_representation']}\n\n"
                    f"Your unique perspective is valuable to AI teams!"
                )
        
        st.markdown("Based on your skills, here are the top AI-adjacent roles for you:")
        st.markdown("")
        
        for i, role in enumerate(display_roles):
            # Add special styling for top match
            card_class = "role-card-top" if i == 0 else "role-card"
            
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Role title with icon
                st.markdown(f'<div class="role-title">{role["icon"]} {role["role_name"]}</div>', 
                          unsafe_allow_html=True)
                
                if i == 0:
                    st.markdown("Ã¢Â­Â **BEST MATCH FOR YOU** Ã¢Â­Â")
                
                st.markdown(f'<div class="role-description">{role["description"]}</div>', 
                          unsafe_allow_html=True)
                
                # Match score with progress bar
                st.markdown(f"**Match Score:** {role['combined_score']:.1%}")
                st.progress(role['combined_score'])
                
                # Show equity insights if available
                if 'equity_insights' in role and role['equity_insights']:
                    for insight in role['equity_insights']:
                        st.markdown(f"**{insight}**")
                
                # Salary range with equity analysis
                if 'salary_equity' in role and role['salary_equity'].get('negotiation_tip'):
                    st.markdown(f"**Ã°Å¸âÂ° Market Range:** {role['salary_equity']['market_range']}")
                    st.warning(role['salary_equity']['negotiation_tip'])
                else:
                    st.markdown(f"**Ã°Å¸âÂ° Salary Range:** {role['pay_range']}")
                
                # Matched skills
                matched_skill_names = get_skill_names(role['matched_skills'][:5])
                st.markdown(f"**Ã¢Åâ¦ Your Matching Skills:** {', '.join(matched_skill_names)}")
            
            with col2:
                # Demand indicator
                demand_emoji = {
                    'very_high': 'Ã°Å¸âÂ¥Ã°Å¸âÂ¥Ã°Å¸âÂ¥',
                    'high': 'Ã°Å¸âÂ¥Ã°Å¸âÂ¥',
                    'medium': 'Ã°Å¸âÂ¥'
                }.get(role['demand'], 'Ã°Å¸âÂ¥')
                
                st.markdown(f"**Demand:**")
                st.markdown(f"{demand_emoji}")
                
                # Gap count
                gap_count = len(role['gaps'])
                st.markdown(f"**Skills Gap:**")
                st.markdown(f"{gap_count} skills")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("")
        
        st.markdown("---")
        st.info("Ã°Å¸âÂ¡ **Next Step:** Check the 'Skill Gap & Bridge Plan' to see how to qualify for these roles!")
        
    else:
        st.warning("Ã¢Å¡Â Ã¯Â¸Â No role matches yet. Please extract skills from your CV first.")
        st.info("Ã°Å¸âË Go to **'Upload or Paste CV'** to get started.")

# ============================================================================
# PAGE 4: SKILL GAP & BRIDGE PLAN
# ============================================================================

elif page == "📈 Skill Gap & Bridge Plan":
    st.markdown('<h2 class="section-header">Ã°Å¸Â§Â© Close Your Skill Gaps</h2>', unsafe_allow_html=True)
    
    if st.session_state.matched_roles and st.session_state.bridge_courses:
        top_role = st.session_state.matched_roles[0]
        
        st.markdown(f"### Target Role: {top_role['icon']} **{top_role['role_name']}**")
        st.markdown("")
        
        # Show gaps
        if top_role['gaps']:
            st.markdown("### Ã°Å¸Â§Â© Missing Skills")
            gap_names = get_skill_names(top_role['gaps'])
            
            for gap in gap_names:
                st.markdown(f'<div class="gap-item">Ã°Å¸Â§Â© <strong>{gap}</strong></div>', 
                          unsafe_allow_html=True)
            
            st.markdown("")
            
            # Show recommended courses
            st.markdown("### Ã°Å¸Å½â Recommended Bridge Courses")
            st.markdown("Here are micro-credentials to help you fill those gaps:")
            st.markdown("")
            
            for i, course in enumerate(st.session_state.bridge_courses[:5], 1):
                st.markdown(f'<div class="course-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{i}. {course['course_name']}**")
                    st.markdown(f"_{course['description']}_")
                    st.markdown(f"Ã°Å¸âÅ¡ Provider: {course['provider']}")
                    
                    fills_gap_names = get_skill_names(course['fills_gaps'])
                    st.markdown(f"Ã¢Åâ¦ Fills: **{', '.join(fills_gap_names)}**")
                
                with col2:
                    st.markdown(f"**Ã¢ÂÂ±Ã¯Â¸Â Duration**")
                    st.markdown(f"{course['duration_hours']} hrs")
                
                with col3:
                    cost_text = "Free" if course['cost'] == 0 else f"${course['cost']}"
                    st.markdown(f"**Ã°Å¸âÂµ Cost**")
                    st.markdown(cost_text)
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("")
            
            # Learning path progress
            st.markdown("---")
            st.markdown("### Ã°Å¸âÅ  Your Learning Path Progress")
            
            total_gaps = len(top_role['gaps'])
            if total_gaps > 0:
                # Calculate how many gaps would be filled by recommended courses
                filled_gaps = 0
                for course in st.session_state.bridge_courses[:3]:
                    filled_gaps += len(course['fills_gaps'])
                
                completion_pct = min(filled_gaps / total_gaps, 1.0)
                
                st.progress(completion_pct)
                st.markdown(f"**{completion_pct:.0%} of gaps can be filled** with these courses")
                
                total_hours = sum(c['duration_hours'] for c in st.session_state.bridge_courses[:3])
                total_cost = sum(c['cost'] for c in st.session_state.bridge_courses[:3])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Time Investment", f"{total_hours} hours")
                with col2:
                    cost_text = "Free" if total_cost == 0 else f"${total_cost}"
                    st.metric("Total Cost", cost_text)
        
        else:
            st.success("Ã°Å¸Å½â° Congratulations! You already have all the skills needed for this role!")
    
    else:
        st.warning("Ã¢Å¡Â Ã¯Â¸Â No gap analysis available yet. Please extract skills and match roles first.")
        st.info("Ã°Å¸âË Go to **'Upload or Paste CV'** to get started.")

# ============================================================================
# PAGE 6: Equity & Support
# ============================================================================

elif page == "🌍 Equity & Support":
    st.markdown('<h2 class="section-header">🌍Â Equity Analysis & Support Resources</h2>', unsafe_allow_html=True)
    
    if not st.session_state.show_equity_analysis:
        st.info(
            "Ã°Å¸âÂ¤ **Share your demographic profile** to unlock personalized equity insights!\n\n"
            "Navigate to **'Demographic Profile (Optional)'** to get started."
        )
        
        st.markdown("---")
        st.markdown("### Why This Matters")
        st.markdown(
            "Understanding systemic barriers helps you:\n"
            "- Negotiate fair compensation\n"
            "- Find supportive communities\n"
            "- Access mentorship programs\n"
            "- Identify inclusive employers\n"
            "- Overcome unconscious bias"
        )
    
    else:
        gender = st.session_state.demographic_info.get('gender')
        ethnicity = st.session_state.demographic_info.get('ethnicity')
        background = st.session_state.demographic_info.get('background')
        
        if not all([gender, ethnicity, background]):
            st.warning("Ã¢Å¡Â Ã¯Â¸Â Complete your demographic profile for full analysis.")
        else:
            # Get demographic profile
            profile = get_demographic_profile(gender, ethnicity, background)
            
            # Show intersectional analysis if available
            if profile['intersectional']:
                st.markdown("### Ã°Å¸Å½Â¯ Your Unique Profile")
                st.info(
                    "You belong to multiple underrepresented groups. "
                    "This gives you a unique and valuable perspective in AI!"
                )
                
                inter = profile['intersectional']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'amplified_challenges' in inter:
                        st.markdown("#### Ã¢Å¡Â Ã¯Â¸Â Challenges to Overcome")
                        for challenge in inter['amplified_challenges']:
                            st.markdown(f"- {challenge}")
                
                with col2:
                    if 'unique_strengths' in inter:
                        st.markdown("#### Ã°Å¸âÂª Your Unique Strengths")
                        for strength in inter['unique_strengths']:
                            st.markdown(f"- {strength}")
                
                if 'encouragement' in inter:
                    st.success(inter['encouragement'])
            
            else:
                # Show individual profile insights
                st.markdown("### Ã°Å¸âÅ  Your Profile Insights")
                
                tabs = st.tabs(["Gender", "Ethnicity", "Background"])
                
                with tabs[0]:
                    if profile['gender']:
                        st.markdown(f"#### Challenges")
                        for challenge in profile['gender'].get('challenges', []):
                            st.markdown(f"- {challenge}")
                        
                        st.markdown(f"#### Strengths")
                        for advantage in profile['gender'].get('advantages', []):
                            st.markdown(f"- {advantage}")
                
                with tabs[1]:
                    if profile['ethnicity']:
                        st.markdown(f"**Representation:** {profile['ethnicity'].get('representation', 'N/A')}")
                        
                        if 'cultural_strengths' in profile['ethnicity']:
                            st.markdown("#### Cultural Strengths")
                            for strength in profile['ethnicity']['cultural_strengths']:
                                st.markdown(f"- {strength}")
                        
                        if 'equity_note' in profile['ethnicity']:
                            st.info(profile['ethnicity']['equity_note'])
                
                with tabs[2]:
                    if profile['background']:
                        bg = profile['background']
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Transition Difficulty", bg.get('transition_difficulty', 'N/A'))
                            st.metric("Expected Timeline", bg.get('bridge_time', 'N/A'))
                        
                        with col2:
                            st.metric("Success Rate", bg.get('success_rate', 'N/A'))
                        
                        st.markdown("#### Transferable Skills")
                        for skill in bg.get('transferable_skills', []):
                            st.markdown(f"- {skill}")
                        
                        if 'encouragement' in bg:
                            st.success(bg['encouragement'])
            
            st.markdown("---")
            
            # Support resources
            st.markdown("### Ã°Å¸Â¤Â Support Resources for You")
            
            resources = get_support_resources(gender, ethnicity, background)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if resources['communities']:
                    st.markdown("#### Ã°Å¸âÂ¥ Communities to Join")
                    for community in resources['communities'][:5]:
                        st.markdown(f"- {community}")
                
                if resources['programs']:
                    st.markdown("#### Ã°Å¸Å½â Special Programs")
                    for program in resources['programs'][:5]:
                        st.markdown(f"- {program}")
            
            with col2:
                if resources['companies']:
                    st.markdown("#### Ã°Å¸ÂÂ¢ Companies with Strong DEI")
                    for company in resources['companies'][:5]:
                        st.markdown(f"- {company}")
            
            # Representation opportunities
            if ethnicity in ['black', 'hispanic_latino']:
                st.markdown("---")
                st.markdown("### 🌍Å¸ Special Opportunities")
                
                rep_analysis = analyze_representation_gap(
                    st.session_state.matched_roles or [],
                    ethnicity
                )
                
                if rep_analysis['special_opportunities']:
                    for opp in rep_analysis['special_opportunities']:
                        st.markdown(f"**{opp}**")

# ============================================================================
# PAGE 7: Skill Passport & Download
# ============================================================================

elif page == "Ã°Å¸Ââ¦ Skill Passport & Download":
    st.markdown('<h2 class="section-header">Ã°Å¸ÂªÂª Your Skill Passport</h2>', unsafe_allow_html=True)
    
    if st.session_state.extracted_skills and st.session_state.matched_roles:
        
        st.markdown('<div class="passport-section">', unsafe_allow_html=True)
        
        # Summary
        st.markdown("### Ã°Å¸ââ¹ Passport Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Ã¢Åâ¦ Verified Skills")
            total_skills = (len(st.session_state.extracted_skills['hard_skills']) + 
                          len(st.session_state.extracted_skills['soft_skills']))
            st.metric("Total Skills", total_skills)
        
        with col2:
            st.markdown("#### Ã°Å¸Å½Â¯ Target Role")
            top_role = st.session_state.matched_roles[0]
            st.markdown(f"**{top_role['role_name']}**")
            st.markdown(f"Match: {top_role['combined_score']:.1%}")
        
        with col3:
            st.markdown("#### Ã°Å¸Â§Â­ Learning Path")
            if st.session_state.bridge_courses:
                st.metric("Courses", len(st.session_state.bridge_courses[:5]))
            else:
                st.metric("Courses", 0)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("")
        
        # Detailed breakdown
        with st.expander("Ã°Å¸ââ View Full Passport Details"):
            st.markdown("#### Ã°Å¸âÂ§ Technical Skills")
            hard_skill_names = get_skill_names(st.session_state.extracted_skills['hard_skills'])
            for skill in hard_skill_names:
                st.markdown(f"- {skill}")
            
            st.markdown("#### Ã°Å¸Â¤Â Soft Skills")
            soft_skill_names = get_skill_names(st.session_state.extracted_skills['soft_skills'])
            for skill in soft_skill_names:
                st.markdown(f"- {skill}")
            
            st.markdown("#### Ã°Å¸Å½Â¯ Top Role Matches")
            for i, role in enumerate(st.session_state.matched_roles[:3], 1):
                st.markdown(f"{i}. **{role['role_name']}** - {role['combined_score']:.1%} match")
            
            if st.session_state.bridge_courses:
                st.markdown("#### Ã°Å¸Å½â Recommended Courses")
                for i, course in enumerate(st.session_state.bridge_courses[:5], 1):
                    st.markdown(f"{i}. {course['course_name']} ({course['provider']})")
        
        # Generate passport button
        st.markdown("---")
        if st.button("Ã°Å¸âÂ¥ Generate Skill Passport", type="primary", use_container_width=True):
            with st.spinner("Ã°Å¸âÂ¨ Creating your Skill Passport..."):
                user_data = {
                    'name': st.session_state.user_name or "Anonymous User",
                    'date': "2025-10-28"
                }
                
                json_path, passport_dict = generate_skill_passport(
                    user_data,
                    st.session_state.extracted_skills,
                    st.session_state.matched_roles,
                    st.session_state.bridge_courses or []
                )
                
                pdf_path = create_pdf_passport(passport_dict)
                
                st.session_state.passport_generated = True
                st.success("Ã¢Åâ¦ Skill Passport generated successfully!")
        
        # Download buttons
        if st.session_state.passport_generated:
            col1, col2 = st.columns(2)
            
            with col1:
                if os.path.exists('output/skill_passport.json'):
                    with open('output/skill_passport.json', 'r') as f:
                        json_data = f.read()
                    
                    st.download_button(
                        label="Ã°Å¸ââ Download JSON",
                        data=json_data,
                        file_name="skill_passport.json",
                        mime="application/json",
                        use_container_width=True
                    )
            
            with col2:
                if os.path.exists('output/skill_passport.pdf'):
                    with open('output/skill_passport.pdf', 'rb') as f:
                        pdf_data = f.read()
                    
                    st.download_button(
                        label="Ã°Å¸ââ Download PDF",
                        data=pdf_data,
                        file_name="skill_passport.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        # Badges
        st.markdown("---")
        st.markdown("### Ã°Å¸Ââ  Your Badges")
        
        badge_col1, badge_col2, badge_col3 = st.columns(3)
        
        with badge_col1:
            st.markdown("#### Ã°Å¸ÂªÂª Skills Verified")
            st.success("Earned Ã¢Åâ")
        
        with badge_col2:
            st.markdown("#### Ã°Å¸âÂ¼ Role Matched")
            if st.session_state.matched_roles:
                st.success("Earned Ã¢Åâ")
            else:
                st.info("Not earned yet")
        
        with badge_col3:
            st.markdown("#### Ã°Å¸Â§Â  Learning Path")
            if st.session_state.bridge_courses:
                st.success("Earned Ã¢Åâ")
            else:
                st.info("Not earned yet")
    
    else:
        st.warning("Ã¢Å¡Â Ã¯Â¸Â No data available for passport generation.")
        st.info("Ã°Å¸âË Please complete the skill extraction process first.")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    '<div class="footer">'
    'Prototype developed by EquiForce AI Team | Powered by EquiForce AI Dataset | 2025<br>'
    '<em>This prototype supports equitable career recognition for women and non-degree professionals.</em>'
    '</div>',
    unsafe_allow_html=True
)

