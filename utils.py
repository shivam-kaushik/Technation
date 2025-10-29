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


def create_pdf_passport(passport: Dict, output_path: str = "output/skill_passport.pdf"):
    """
    Create a simple PDF version of the skill passport
    """
    try:
        from fpdf import FPDF
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Title
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 10, "Skill Passport", ln=True, align='C')
        pdf.ln(5)
        
        # User info
        if 'user_info' in passport and passport['user_info'].get('name'):
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 8, f"Name: {passport['user_info']['name']}", ln=True)
            pdf.ln(5)
        
        # Verified Skills
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Verified Skills", ln=True)
        pdf.set_font("Arial", '', 11)
        
        hard_skills = passport['verified_skills']['hard_skills']
        soft_skills = passport['verified_skills']['soft_skills']
        
        pdf.multi_cell(0, 6, f"Hard Skills: {', '.join(hard_skills)}")
        pdf.ln(2)
        pdf.multi_cell(0, 6, f"Soft Skills: {', '.join(soft_skills)}")
        pdf.ln(5)
        
        # Top Role Match
        if passport.get('top_role_match'):
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, "Best Role Match", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 6, f"Role: {passport['top_role_match']['role']}", ln=True)
            pdf.cell(0, 6, f"Match Score: {passport['top_role_match']['score']}", ln=True)
            pdf.cell(0, 6, f"Salary Range: {passport['top_role_match']['pay_range']}", ln=True)
            pdf.ln(5)
        
        # Recommended Courses
        if passport.get('recommended_courses'):
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, "Recommended Learning Path", ln=True)
            pdf.set_font("Arial", '', 10)
            
            for i, course in enumerate(passport['recommended_courses'][:5], 1):
                pdf.multi_cell(0, 5, 
                    f"{i}. {course['course']} ({course['provider']}) - {course['duration']} - {course['cost']}")
        
        pdf.ln(10)
        pdf.set_font("Arial", 'I', 9)
        pdf.cell(0, 5, f"Generated: {passport.get('generated_date', '2025-10-28')}", ln=True)
        pdf.cell(0, 5, "Powered by EquiForce AI Dataset", ln=True)
        
        pdf.output(output_path)
        return output_path
        
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return None
