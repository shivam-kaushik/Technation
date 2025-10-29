"""
Backend utility functions for the Skill Recognition Engine
"""

import re
import json
import os
from typing import List, Dict, Tuple
from io import BytesIO

# Lazy imports for heavy libraries
_np = None
_SentenceTransformer = None
_cosine_similarity = None
_PyPDF2 = None
_Document = None

def _import_numpy():
    global _np
    if _np is None:
        import numpy as np
        _np = np
    return _np

def _import_sentence_transformers():
    global _SentenceTransformer
    if _SentenceTransformer is None:
        from sentence_transformers import SentenceTransformer
        _SentenceTransformer = SentenceTransformer
    return _SentenceTransformer

def _import_cosine_similarity():
    global _cosine_similarity
    if _cosine_similarity is None:
        from sklearn.metrics.pairwise import cosine_similarity
        _cosine_similarity = cosine_similarity
    return _cosine_similarity

def _import_pdf():
    global _PyPDF2
    if _PyPDF2 is None:
        import PyPDF2
        _PyPDF2 = PyPDF2
    return _PyPDF2

def _import_docx():
    global _Document
    if _Document is None:
        from docx import Document
        _Document = Document
    return _Document

# Load sentence transformer model (cached after first load)
_model = None

def get_embedding_model():
    """Lazy load the sentence transformer model"""
    global _model
    if _model is None:
        SentenceTransformer = _import_sentence_transformers()
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def ingest_and_clean(cv_file, file_type: str = "pdf") -> str:
    """
    Extract text from PDF/DOCX file and clean it
    
    Args:
        cv_file: File object from Streamlit uploader
        file_type: 'pdf' or 'docx'
    
    Returns:
        Cleaned text string
    """
    text = ""
    
    try:
        if file_type == "pdf":
            # Read PDF
            PyPDF2 = _import_pdf()
            pdf_reader = PyPDF2.PdfReader(BytesIO(cv_file.read()))
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        elif file_type == "docx":
            # Read DOCX
            Document = _import_docx()
            doc = Document(BytesIO(cv_file.read()))
            text = "\n".join([para.text for para in doc.paragraphs])
        
        # Clean text
        text = clean_text(text)
        
    except Exception as e:
        print(f"Error extracting text: {e}")
        text = ""
    
    return text


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    Remove PII (email, phone, address patterns)
    """
    # Remove emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    
    # Remove phone numbers (various formats)
    text = re.sub(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', '[PHONE]', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Normalize bullets
    text = re.sub(r'[•●○■◆◇▪▫]', '-', text)
    
    return text.strip()


def load_skill_ontology(filepath: str = "data/skill_ontology.json") -> Dict:
    """Load skill ontology from JSON"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_skills(text: str, ontology_path: str = "data/skill_ontology.json") -> Dict[str, List[str]]:
    """
    Extract skills from text using keyword matching and patterns
    
    Returns:
        Dictionary with 'hard_skills' and 'soft_skills' lists
    """
    ontology = load_skill_ontology(ontology_path)
    text_lower = text.lower()
    
    found_hard_skills = []
    found_soft_skills = []
    
    # Extract hard skills
    for skill in ontology['hard_skills']:
        for keyword in skill['keywords']:
            if keyword.lower() in text_lower:
                if skill['id'] not in found_hard_skills:
                    found_hard_skills.append(skill['id'])
                break
    
    # Extract soft skills
    for skill in ontology['soft_skills']:
        for keyword in skill['keywords']:
            if keyword.lower() in text_lower:
                if skill['id'] not in found_soft_skills:
                    found_soft_skills.append(skill['id'])
                break
    
    return {
        'hard_skills': found_hard_skills,
        'soft_skills': found_soft_skills
    }


def get_skill_names(skill_ids: List[str], ontology_path: str = "data/skill_ontology.json") -> List[str]:
    """Convert skill IDs to readable names"""
    ontology = load_skill_ontology(ontology_path)
    
    skill_map = {}
    for skill in ontology['hard_skills']:
        skill_map[skill['id']] = skill['name']
    for skill in ontology['soft_skills']:
        skill_map[skill['id']] = skill['name']
    
    return [skill_map.get(sid, sid) for sid in skill_ids]


def compute_user_vector(skills: List[str]):
    """
    Compute user skill embedding using Sentence-BERT
    
    Args:
        skills: List of skill IDs or names
    
    Returns:
        Mean-pooled embedding vector
    """
    np = _import_numpy()
    
    if not skills:
        return np.zeros(384)  # Default embedding size for MiniLM
    
    model = get_embedding_model()
    
    # Get skill names
    skill_names = get_skill_names(skills)
    
    # Compute embeddings
    embeddings = model.encode(skill_names)
    
    # Mean pooling
    user_vector = np.mean(embeddings, axis=0)
    
    return user_vector


def load_role_clusters(filepath: str = "data/ai_role_clusters.json") -> List[Dict]:
    """Load AI role clusters"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def match_roles(user_vector, 
                user_skills: List[str], 
                role_clusters_path: str = "data/ai_role_clusters.json") -> List[Dict]:
    """
    Match user to AI roles based on cosine similarity and skill coverage
    
    Returns:
        List of top 5 matching roles with scores, gaps, and metadata
    """
    np = _import_numpy()
    cosine_similarity = _import_cosine_similarity()
    
    roles = load_role_clusters(role_clusters_path)
    model = get_embedding_model()
    
    matched_roles = []
    
    for role in roles:
        # Get required skills
        required_skills = role['required_skills'] + role['soft_skills']
        
        # Compute role vector
        skill_names = get_skill_names(required_skills)
        role_embeddings = model.encode(skill_names)
        role_vector = np.mean(role_embeddings, axis=0)
        
        # Compute cosine similarity
        similarity = cosine_similarity(
            user_vector.reshape(1, -1),
            role_vector.reshape(1, -1)
        )[0][0]
        
        # Compute skill coverage
        user_skill_set = set(user_skills)
        required_skill_set = set(required_skills)
        
        matched_skills = user_skill_set.intersection(required_skill_set)
        coverage = len(matched_skills) / len(required_skill_set) if required_skill_set else 0
        
        # Identify gaps
        gaps = list(required_skill_set - user_skill_set)
        
        # Combined score (70% similarity + 30% coverage)
        combined_score = 0.7 * similarity + 0.3 * coverage
        
        matched_roles.append({
            'role_id': role['role_id'],
            'role_name': role['role_name'],
            'description': role['description'],
            'icon': role['icon'],
            'similarity': float(similarity),
            'coverage': float(coverage),
            'combined_score': float(combined_score),
            'gaps': gaps,
            'matched_skills': list(matched_skills),
            'pay_range': role['pay_range'],
            'demand': role['demand']
        })
    
    # Sort by combined score
    matched_roles.sort(key=lambda x: x['combined_score'], reverse=True)
    
    return matched_roles[:5]


def load_microcredentials(filepath: str = "data/microcredentials.json") -> List[Dict]:
    """Load micro-credential courses"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def recommend_bridges(gaps: List[str], 
                     user_skills: List[str],
                     microcreds_path: str = "data/microcredentials.json") -> List[Dict]:
    """
    Recommend micro-credential bridge courses to fill skill gaps
    
    Args:
        gaps: List of missing skill IDs
        user_skills: List of current user skill IDs
    
    Returns:
        List of recommended courses (sorted by efficiency)
    """
    if not gaps:
        return []
    
    courses = load_microcredentials(microcreds_path)
    user_skill_set = set(user_skills)
    gap_set = set(gaps)
    
    recommended = []
    
    for course in courses:
        # Check if course bridges to any gap skill
        bridges_to_set = set(course['bridges_to'])
        relevant_gaps = bridges_to_set.intersection(gap_set)
        
        if relevant_gaps:
            # Check prerequisites
            bridges_from_set = set(course['bridges_from'])
            has_prerequisites = True
            
            if bridges_from_set:
                has_prerequisites = bool(bridges_from_set.intersection(user_skill_set))
            
            # Calculate efficiency score
            gaps_filled = len(relevant_gaps)
            efficiency = gaps_filled / (course['duration_hours'] + 1)
            
            recommended.append({
                'course_id': course['course_id'],
                'course_name': course['course_name'],
                'description': course['description'],
                'duration_hours': course['duration_hours'],
                'cost': course['cost'],
                'provider': course['provider'],
                'url': course['url'],
                'fills_gaps': list(relevant_gaps),
                'gaps_count': gaps_filled,
                'has_prerequisites': has_prerequisites,
                'efficiency': efficiency,
                'priority': 'High' if has_prerequisites and gaps_filled >= 2 else 'Medium'
            })
    
    # Sort by efficiency and priority
    recommended.sort(key=lambda x: (x['has_prerequisites'], x['efficiency']), reverse=True)
    
    return recommended


def generate_skill_passport(user_data: Dict, 
                           skills: Dict[str, List[str]], 
                           top_roles: List[Dict],
                           bridges: List[Dict]) -> Tuple[str, Dict]:
    """
    Generate a Skill Passport (JSON + PDF path)
    
    Args:
        user_data: User metadata (name, email, etc.)
        skills: Dictionary with hard_skills and soft_skills
        top_roles: Matched roles
        bridges: Recommended courses
    
    Returns:
        Tuple of (json_path, passport_dict)
    """
    # Create passport dictionary
    passport = {
        'user_info': user_data,
        'verified_skills': {
            'hard_skills': get_skill_names(skills['hard_skills']),
            'soft_skills': get_skill_names(skills['soft_skills']),
            'total_count': len(skills['hard_skills']) + len(skills['soft_skills'])
        },
        'top_role_match': {
            'role': top_roles[0]['role_name'],
            'score': f"{top_roles[0]['combined_score']:.1%}",
            'pay_range': top_roles[0]['pay_range']
        } if top_roles else None,
        'alternative_roles': [
            {
                'role': r['role_name'],
                'score': f"{r['combined_score']:.1%}"
            } for r in top_roles[1:4]
        ] if len(top_roles) > 1 else [],
        'skill_gaps': get_skill_names(top_roles[0]['gaps']) if top_roles else [],
        'recommended_courses': [
            {
                'course': c['course_name'],
                'provider': c['provider'],
                'duration': f"{c['duration_hours']} hours",
                'cost': f"${c['cost']}" if c['cost'] > 0 else "Free"
            } for c in bridges[:5]
        ],
        'badges': {
            'skills_verified': True,
            'role_matched': bool(top_roles),
            'learning_path_created': bool(bridges)
        },
        'generated_date': "2025-10-28"
    }
    
    # Save JSON
    os.makedirs('output', exist_ok=True)
    json_path = 'output/skill_passport.json'
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(passport, f, indent=2, ensure_ascii=False)
    
    return json_path, passport


def create_pdf_passport(passport: Dict, demographic_info: Dict = None, output_path: str = "output/skill_passport.pdf"):
    """
    Create a comprehensive, visually appealing PDF version of the skill passport
    with all demographic info, skills, role matches, and skill gaps
    """
    try:
        print("Starting PDF generation...")
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.pdfgen import canvas
        import datetime
        
        print("Imports successful")
        
        # Create PDF
        os.makedirs('output', exist_ok=True)
        print(f"Creating PDF at: {output_path}")
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                               rightMargin=0.75*inch, leftMargin=0.75*inch,
                               topMargin=1*inch, bottomMargin=0.75*inch)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#3B82F6'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderColor=colors.HexColor('#3B82F6'),
            borderWidth=0,
            borderPadding=5,
            backColor=colors.HexColor('#EFF6FF')
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#374151'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=6,
            leading=14
        )
        
        # ==================== HEADER ====================
        elements.append(Paragraph("🪪 AI SKILLS PASSPORT", title_style))
        elements.append(Paragraph(f"<i>Verified Skill Recognition & Career Roadmap</i>", 
                                 ParagraphStyle('subtitle', parent=body_style, alignment=TA_CENTER, 
                                              fontSize=12, textColor=colors.HexColor('#6B7280'))))
        elements.append(Spacer(1, 0.2*inch))
        
        # Date and ID
        passport_id = f"SKP-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        date_text = f"<b>Generated:</b> {datetime.datetime.now().strftime('%B %d, %Y')} | <b>Passport ID:</b> {passport_id}"
        elements.append(Paragraph(date_text, ParagraphStyle('date', parent=body_style, alignment=TA_CENTER, fontSize=9)))
        elements.append(Spacer(1, 0.3*inch))
        
        # ==================== DEMOGRAPHIC PROFILE ====================
        if demographic_info:
            elements.append(Paragraph("👤 DEMOGRAPHIC PROFILE", heading_style))
            
            demo_data = []
            if demographic_info.get('gender'):
                demo_data.append(['Gender Identity:', demographic_info['gender']])
            if demographic_info.get('ethnicity'):
                demo_data.append(['Ethnicity:', demographic_info['ethnicity']])
            if demographic_info.get('background'):
                demo_data.append(['Background:', demographic_info['background']])
            if demographic_info.get('years_experience'):
                demo_data.append(['Experience:', f"{demographic_info['years_experience']} years"])
            if demographic_info.get('location'):
                demo_data.append(['Location:', demographic_info['location']])
            
            if demo_data:
                demo_table = Table(demo_data, colWidths=[2*inch, 4.5*inch])
                demo_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1F2937')),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                elements.append(demo_table)
                elements.append(Spacer(1, 0.2*inch))
        
        # ==================== VERIFIED SKILLS ====================
        elements.append(Paragraph("✨ VERIFIED SKILLS", heading_style))
        
        verified_skills = passport.get('verified_skills', {})
        hard_skills = verified_skills.get('hard_skills', [])
        soft_skills = verified_skills.get('soft_skills', [])
        total_count = verified_skills.get('total_count', 0)
        
        # Skills summary
        elements.append(Paragraph(f"<b>Total Skills Identified:</b> {total_count}", subheading_style))
        
        # Hard Skills
        if hard_skills:
            elements.append(Paragraph("💻 Technical Skills:", subheading_style))
            skill_text = " • ".join(hard_skills)
            elements.append(Paragraph(skill_text, body_style))
            elements.append(Spacer(1, 0.1*inch))
        
        # Soft Skills
        if soft_skills:
            elements.append(Paragraph("🤝 Soft Skills:", subheading_style))
            skill_text = " • ".join(soft_skills)
            elements.append(Paragraph(skill_text, body_style))
            elements.append(Spacer(1, 0.2*inch))
        
        # ==================== TOP ROLE MATCHES ====================
        elements.append(Paragraph("🧠 TOP AI ROLE MATCHES", heading_style))
        
        top_role = passport.get('top_role_match')
        if top_role:
            # Best match box
            best_match_data = [
                ['🎯 BEST MATCH', ''],
                ['Role:', top_role['role']],
                ['Match Score:', top_role['score']],
                ['Salary Range:', top_role.get('pay_range', 'N/A')]
            ]
            
            best_match_table = Table(best_match_data, colWidths=[2*inch, 4.5*inch])
            best_match_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('SPAN', (0, 0), (-1, 0)),
                ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#F3F4F6')),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#3B82F6')),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(best_match_table)
            elements.append(Spacer(1, 0.15*inch))
        
        # Alternative roles
        alt_roles = passport.get('alternative_roles', [])
        if alt_roles:
            elements.append(Paragraph("Alternative Career Paths:", subheading_style))
            alt_data = [['#', 'Role', 'Match Score']]
            for idx, role in enumerate(alt_roles, 2):
                alt_data.append([str(idx), role['role'], role['score']])
            
            alt_table = Table(alt_data, colWidths=[0.5*inch, 4*inch, 2*inch])
            alt_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E5E7EB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1F2937')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(alt_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # ==================== SKILL GAPS ====================
        skill_gaps = passport.get('skill_gaps', [])
        if skill_gaps:
            elements.append(Paragraph("📚 SKILL GAPS & LEARNING PATH", heading_style))
            elements.append(Paragraph("Skills to develop for your target role:", subheading_style))
            
            gap_text = " • ".join(skill_gaps)
            elements.append(Paragraph(gap_text, body_style))
            elements.append(Spacer(1, 0.15*inch))
        
        # ==================== RECOMMENDED COURSES ====================
        courses = passport.get('recommended_courses', [])
        if courses:
            elements.append(Paragraph("🎓 RECOMMENDED LEARNING RESOURCES", subheading_style))
            
            course_data = [['#', 'Course', 'Provider', 'Duration', 'Cost']]
            for idx, course in enumerate(courses, 1):
                course_data.append([
                    str(idx),
                    course['course'],
                    course['provider'],
                    course['duration'],
                    course['cost']
                ])
            
            course_table = Table(course_data, colWidths=[0.4*inch, 2.5*inch, 1.5*inch, 1*inch, 1.1*inch])
            course_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0FDF4')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#10B981')),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (3, 0), (4, -1), 'CENTER'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(course_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # ==================== BADGES & VERIFICATION ====================
        elements.append(Paragraph("🏆 ACHIEVEMENT BADGES", heading_style))
        
        badges = passport.get('badges', {})
        badge_data = []
        if badges.get('skills_verified'):
            badge_data.append(['✅ Skills Verified', 'Your skills have been analyzed and validated'])
        if badges.get('role_matched'):
            badge_data.append(['✅ Career Path Identified', 'AI roles matched based on your profile'])
        if badges.get('learning_path_created'):
            badge_data.append(['✅ Learning Roadmap Created', 'Personalized courses recommended'])
        
        if badge_data:
            badge_table = Table(badge_data, colWidths=[2*inch, 4.5*inch])
            badge_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF3C7')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#92400E')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#F59E0B')),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(badge_table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # ==================== FOOTER ====================
        footer_text = f"""
        <para alignment='center' fontSize='8' textColor='#6B7280'>
        <i>This AI Skills Passport is generated by the Enhanced Skill Recognition Engine.<br/>
        For women, underrepresented minorities, and career changers entering AI.<br/>
        © 2025 TechNation | Passport ID: {passport_id}</i>
        </para>
        """
        elements.append(Paragraph(footer_text, body_style))
        
        # Build PDF
        print("Building PDF document...")
        doc.build(elements)
        print(f"PDF created successfully at: {output_path}")
        
        return output_path
        
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Install with: pip install reportlab")
        return None
    except Exception as e:
        print(f"Error creating PDF: {e}")
        import traceback
        traceback.print_exc()
        return None
