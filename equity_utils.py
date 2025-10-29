"""
Equity-focused utility functions for demographic analysis and bias mitigation
"""

import json
from typing import Dict, List, Tuple

def load_equity_profiles(filepath: str = "data/equity_profiles.json") -> Dict:
    """Load equity and demographic profiles"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_demographic_profile(gender: str, ethnicity: str, background: str) -> Dict:
    """
    Get combined demographic profile with intersectional analysis
    
    Args:
        gender: 'woman', 'man', 'non_binary'
        ethnicity: 'white', 'south_asian', 'east_asian', 'black', 'hispanic_latino'
        background: 'non_ai_stem', 'non_ai_non_stem', 'career_break', 'self_taught'
    
    Returns:
        Dictionary with challenges, strengths, recommendations
    """
    profiles = load_equity_profiles()
    
    # Get individual profiles
    gender_profile = profiles['demographics']['gender'].get(gender, {})
    ethnicity_profile = profiles['demographics']['ethnicity'].get(ethnicity, {})
    background_profile = profiles['demographics']['background'].get(background, {})
    
    # Check for intersectional profile
    intersectional_key = f"{gender}_{ethnicity}_{background}"
    intersectional = profiles['intersectional_factors'].get(intersectional_key, {})
    
    return {
        'gender': gender_profile,
        'ethnicity': ethnicity_profile,
        'background': background_profile,
        'intersectional': intersectional,
        'bias_mitigation': profiles['bias_mitigation']
    }


def calculate_equity_adjusted_salary(base_salary_range: str, 
                                     gender: str, 
                                     ethnicity: str,
                                     show_gap: bool = True) -> Dict:
    """
    Calculate salary ranges considering equity gaps
    
    Args:
        base_salary_range: e.g., "$55,000 - $85,000"
        gender: Gender identity
        ethnicity: Ethnic background
        show_gap: Whether to show the gap analysis
    
    Returns:
        Dictionary with adjusted ranges and gap information
    """
    profiles = load_equity_profiles()
    
    # Parse salary range
    import re
    matches = re.findall(r'\$?([\d,]+)', base_salary_range)
    if len(matches) >= 2:
        low = int(matches[0].replace(',', ''))
        high = int(matches[1].replace(',', ''))
    else:
        return {'error': 'Invalid salary format'}
    
    # Get adjustment factors
    gender_adjustment = profiles['demographics']['gender'].get(gender, {}).get('salary_adjustment', 1.0)
    
    # Additional adjustment for underrepresented groups
    underrep_ethnicities = ['black', 'hispanic_latino']
    ethnicity_adjustment = 0.95 if ethnicity in underrep_ethnicities else 1.0
    
    # Combined adjustment
    combined_adjustment = gender_adjustment * ethnicity_adjustment
    
    # Calculate adjusted range (what they typically receive)
    adjusted_low = int(low * combined_adjustment)
    adjusted_high = int(high * combined_adjustment)
    
    # Calculate gap
    gap_low = low - adjusted_low
    gap_high = high - adjusted_high
    gap_percent = int((1 - combined_adjustment) * 100)
    
    result = {
        'market_range': base_salary_range,
        'typical_range': f"${adjusted_low:,} - ${adjusted_high:,}",
        'target_range': base_salary_range,  # What they SHOULD negotiate for
        'has_gap': combined_adjustment < 1.0,
        'gap_percent': gap_percent if show_gap else 0,
        'negotiation_tip': ''
    }
    
    if combined_adjustment < 1.0 and show_gap:
        result['negotiation_tip'] = (
            f"⚠️ Equity Alert: {gender.title()} professionals in your demographic typically earn "
            f"{gap_percent}% less. Don't undersell yourself! Negotiate for the full market range."
        )
    
    return result


def enhance_skills_with_confidence(skills: Dict[str, List[str]], 
                                   gender: str,
                                   ethnicity: str) -> Dict:
    """
    Add confidence boosting based on demographic underselling patterns
    
    Returns:
        Enhanced skills with additional inferred capabilities
    """
    profiles = load_equity_profiles()
    
    # Women and underrepresented groups often undersell
    underselling_groups = ['woman', 'non_binary']
    underrep_ethnicities = ['black', 'hispanic_latino']
    
    needs_boost = (gender in underselling_groups) or (ethnicity in underrep_ethnicities)
    
    if not needs_boost:
        return skills
    
    # Add inferred skills based on patterns
    enhanced_skills = {
        'hard_skills': skills['hard_skills'].copy(),
        'soft_skills': skills['soft_skills'].copy(),
        'inferred_skills': [],
        'confidence_note': ''
    }
    
    # If they have Excel, they likely know data analysis
    if 'excel' in skills['hard_skills'] and 'data_analysis' not in skills['hard_skills']:
        enhanced_skills['inferred_skills'].append('data_analysis')
    
    # If they have any programming, they likely know problem solving
    prog_skills = {'python', 'javascript', 'r_programming', 'sql'}
    if prog_skills.intersection(set(skills['hard_skills'])):
        if 'problem_solving' not in skills['soft_skills']:
            enhanced_skills['inferred_skills'].append('problem_solving')
    
    # If they managed anything, they have leadership
    if 'project_management' in skills['hard_skills']:
        if 'leadership' not in skills['soft_skills']:
            enhanced_skills['inferred_skills'].append('leadership')
    
    if enhanced_skills['inferred_skills']:
        enhanced_skills['confidence_note'] = (
            f"💡 We inferred {len(enhanced_skills['inferred_skills'])} additional skills based on your experience. "
            f"Research shows {gender}s often undersell their capabilities by 20-30%."
        )
    
    return enhanced_skills


def get_targeted_role_recommendations(matched_roles: List[Dict],
                                     gender: str,
                                     ethnicity: str,
                                     background: str) -> List[Dict]:
    """
    Enhance role recommendations with demographic-specific insights
    """
    profiles = load_equity_profiles()
    
    # Get recommended focus areas
    gender_profile = profiles['demographics']['gender'].get(gender, {})
    focus_areas = gender_profile.get('recommended_focus', [])
    
    # Enhance each role with demographic insights
    enhanced_roles = []
    for role in matched_roles:
        enhanced = role.copy()
        
        # Add equity insights
        enhanced['equity_insights'] = []
        
        # Check if role aligns with recommended focus
        role_keywords = role['role_name'].lower()
        for focus in focus_areas:
            if focus.lower() in role_keywords:
                enhanced['equity_insights'].append(f"✨ Recommended focus area for {gender}s")
        
        # Add representation info
        if ethnicity in ['black', 'hispanic_latino']:
            enhanced['equity_insights'].append(
                "🎯 This role values diverse perspectives - highlight your unique background"
            )
        
        # Add salary equity alert
        salary_info = calculate_equity_adjusted_salary(
            role['pay_range'], 
            gender, 
            ethnicity,
            show_gap=True
        )
        enhanced['salary_equity'] = salary_info
        
        enhanced_roles.append(enhanced)
    
    return enhanced_roles


def get_support_resources(gender: str, ethnicity: str, background: str) -> Dict:
    """
    Get targeted support programs and communities
    """
    profiles = load_equity_profiles()
    
    resources = {
        'communities': [],
        'programs': [],
        'mentorship': [],
        'companies': []
    }
    
    # Gender-specific
    if gender == 'woman':
        resources['communities'].extend([
            "Women Who Code",
            "Women in AI",
            "Girls Who Code (Alumni Network)",
            "Lean In Circles"
        ])
    
    # Ethnicity-specific
    ethnicity_communities = {
        'black': ["Black in AI", "NSBE", "AfroTech", "/dev/color"],
        'hispanic_latino': ["Latinos in Tech", "SHPE", "Techqueria"],
        'south_asian': ["South Asian Women in Tech", "Desi in Tech"],
        'east_asian': ["Ascend Leadership", "Asian in Tech"]
    }
    
    if ethnicity in ethnicity_communities:
        resources['communities'].extend(ethnicity_communities[ethnicity])
    
    # Background-specific
    if background == 'career_break':
        resources['programs'].extend([
            "Path Forward Returnship",
            "Mom Relaunch",
            "The Mom Project",
            "PowerToFly Return to Work"
        ])
    
    if background == 'non_ai_non_stem':
        resources['programs'].extend([
            "AI for Everyone (Coursera)",
            "No-Code AI Bootcamps",
            "Google AI Essentials"
        ])
    
    # Intersectional resources
    intersectional_key = f"{gender}_{ethnicity}_{background}"
    intersectional = profiles['intersectional_factors'].get(intersectional_key, {})
    
    if 'support_programs' in intersectional:
        resources['programs'].extend(intersectional['support_programs'])
    
    # Company recommendations
    profiles_data = load_equity_profiles()
    if ethnicity in ['black', 'hispanic_latino'] or gender in ['woman', 'non_binary']:
        resources['companies'] = profiles_data['company_recommendations']['high_dei_commitment']
    
    return resources


def reframe_cv_language(text: str) -> Tuple[str, List[str]]:
    """
    Reframe passive CV language to be more confident and action-oriented
    
    Returns:
        Tuple of (reframed_text, list_of_changes)
    """
    profiles = load_equity_profiles()
    replacements = profiles['bias_mitigation']['cv_keywords_to_reframe']
    
    reframed = text
    changes = []
    
    for weak, strong in replacements.items():
        if weak in text.lower():
            # Simple replacement (case-insensitive)
            import re
            pattern = re.compile(re.escape(weak), re.IGNORECASE)
            reframed = pattern.sub(strong, reframed)
            changes.append(f"'{weak}' → '{strong}'")
    
    return reframed, changes


def generate_confidence_message(gender: str, ethnicity: str, background: str) -> str:
    """
    Generate personalized confidence and encouragement message
    """
    profiles = load_equity_profiles()
    
    messages = []
    
    # Gender-specific encouragement
    gender_profile = profiles['demographics']['gender'].get(gender, {})
    if 'bias_awareness' in gender_profile:
        messages.append(gender_profile['bias_awareness'])
    
    # Background encouragement
    background_profile = profiles['demographics']['background'].get(background, {})
    if 'encouragement' in background_profile:
        messages.append(background_profile['encouragement'])
    
    # Confidence booster
    confidence_boosters = profiles['bias_mitigation']['confidence_boosters']
    
    if gender in ['woman', 'non_binary']:
        messages.append(confidence_boosters.get('woman', ''))
    
    if ethnicity in ['black', 'hispanic_latino']:
        messages.append(confidence_boosters.get('underrepresented', ''))
    
    if background == 'career_break':
        messages.append(confidence_boosters.get('career_break', ''))
    
    return '\n\n'.join([m for m in messages if m])


def analyze_representation_gap(matched_roles: List[Dict], 
                              ethnicity: str) -> Dict:
    """
    Analyze representation gaps in recommended roles
    """
    profiles = load_equity_profiles()
    ethnicity_profile = profiles['demographics']['ethnicity'].get(ethnicity, {})
    
    representation = ethnicity_profile.get('representation', 'Unknown')
    
    analysis = {
        'your_representation': representation,
        'is_underrepresented': 'Underrepresented' in representation,
        'special_opportunities': [],
        'dei_companies': []
    }
    
    if analysis['is_underrepresented']:
        analysis['special_opportunities'] = [
            "🎯 Diversity hiring initiatives actively seeking your profile",
            "💰 Some companies offer referral bonuses for diverse hires",
            "📈 Fast-track leadership programs for underrepresented groups",
            "🤝 Mentorship programs specifically for your demographic"
        ]
        
        profiles_data = load_equity_profiles()
        analysis['dei_companies'] = profiles_data['company_recommendations']['high_dei_commitment'][:5]
    
    return analysis
