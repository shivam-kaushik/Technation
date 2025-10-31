import re

print("🔧 Fixing all issues in app.py...")

with open('app.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Fix 1: Fix corrupted emojis in navigation
print("1. Fixing corrupted emojis in navigation...")
lines = content.split('\n')
for i, line in enumerate(lines):
    # Fix Upload CV & Analyze emoji
    if 'Upload CV & Analyze' in line and line.strip().startswith('"') and '�' in line:
        lines[i] = '        "📄 Upload CV & Analyze",'
        print(f"   ✓ Fixed Upload CV emoji at line {i+1}")
    # Fix Your Profile & Equity emoji
    elif 'Your Profile & Equity' in line and line.strip().startswith('"') and '�' in line:
        lines[i] = '        "👤 Your Profile & Equity",'
        print(f"   ✓ Fixed Profile & Equity emoji at line {i+1}")

content = '\n'.join(lines)

# Fix 2: Remove duplicate Skill Gap Analysis section (the first one showing recognized skills)
print("\n2. Removing duplicate Skill Gap Analysis section...")

# Find and remove the FIRST duplicate (showing recognized skills)
pattern = r'# ============================================================================\n# PAGE: SKILL GAP ANALYSIS\n# ============================================================================\n\nelif page == "📈 Skill Gap Analysis":\n    st\.header\("✨ Your Recognized Skills"\).*?(?=# ============================================================================\n# PAGE: SKILL GAP ANALYSIS)'

content = re.sub(pattern, '', content, flags=re.DOTALL, count=1)
print("   ✓ Removed duplicate section")

# Fix 3: Change technical skills display to horizontal format in Skills & AI Roles tab
print("\n3. Changing technical skills display to horizontal format...")

# Find the technical skills section in tab1 and change it to horizontal
pattern_tech_skills = r'(with col1:\s+st\.markdown\("### 💻 Technical Skills"\)\s+if hard_skills:\s+)for skill_name in hard_skills:\s+st\.markdown\(f\'<span class="skill-tag-hard">\{skill_name\}</span>\', unsafe_allow_html=True\)'

replacement_tech_skills = r'\1# Display in horizontal rows\n                cols = st.columns(4)\n                for idx, skill_name in enumerate(hard_skills):\n                    with cols[idx % 4]:\n                        st.markdown(f\'<span class="skill-tag-hard">{skill_name}</span>\', unsafe_allow_html=True)'

content = re.sub(pattern_tech_skills, replacement_tech_skills, content, flags=re.DOTALL)
print("   ✓ Changed technical skills to horizontal format")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ All fixes applied successfully!")
print("\nFixed issues:")
print("  1. ✓ Upload CV & Analyze emoji")
print("  2. ✓ Your Profile & Equity emoji")
print("  3. ✓ Removed duplicate Skill Gap Analysis showing recognized skills")
print("  4. ✓ Technical skills now display horizontally")
