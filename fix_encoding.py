"""
Fix emoji encoding issues in app.py using byte-level operations
This avoids Python syntax errors from corrupted characters in string literals
"""

# Read the file as raw bytes
with open('app.py', 'rb') as f:
    data = f.read()

# The file has corrupted UTF-8. We need to find and replace the actual byte sequences
# First, let's decode as UTF-8 and work with the text
text = data.decode('utf-8', errors='replace')

# Now replace the corrupted display characters with proper emojis
# These are the actual corrupted patterns found in the file
replacements = [
    ('"Ã°Å¸âÂ¤ Demographic Profile (Optional)"', '"👤 Demographic Profile (Optional)"'),
    ('"Ã°Å¸ââ¹ Recognized Skills"', '"✨ Recognized Skills"'),
    ('"Ã°Å¸Å½Â¯ Equity & Support"', '"🌍 Equity & Support"'),
    ('"Ã°Å¸Ââ¦ Skill Passport & Download"', '"🪪 Skill Passport & Download"'),
    
    # Fix elif conditions
    ('elif page == "Ã°Å¸âÂ¤ Demographic Profile (Optional)":', 'elif page == "👤 Demographic Profile (Optional)":'),
    ('elif page == "Ã°Å¸ââ¹ Recognized Skills":', 'elif page == "✨ Recognized Skills":'),
    ('elif page == "Ã°Å¸Å½Â¯ Equity & Support":', 'elif page == "🌍 Equity & Support":'),
    ('elif page == "Ã°Å¸Ââ¦ Skill Passport & Download":', 'elif page == "🪪 Skill Passport & Download":'),
    
    # Fix section headers
    ('<h2 class="section-header">Ã°Å¸âÂ¤ Demographic Profile (Optional)</h2>', '<h2 class="section-header">👤 Demographic Profile (Optional)</h2>'),
    ('<h2 class="section-header">Ã°Å¸ââ¹ Recognized Skills</h2>', '<h2 class="section-header">✨ Recognized Skills</h2>'),
    ('<h2 class="section-header">Ã°Å¸Å½Â¯ Equity & Support</h2>', '<h2 class="section-header">🌍 Equity & Support</h2>'),
    ('<h2 class="section-header">Ã°Å¸Ââ¦ Skill Passport & Download</h2>', '<h2 class="section-header">🪪 Skill Passport & Download</h2>'),
    
    # Fix other common corrupted emojis in messages
    ('Ã°Å¸âÅ ', '📊'),
    ('Ã°Å¸ââ', '🔒'),
]

# Apply all replacements
count = 0
for old_text, new_text in replacements:
    if old_text in text:
        text = text.replace(old_text, new_text)
        count += 1
        print(f"  Fixed: {old_text[:50]}...")

# Write back as UTF-8
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"\n✅ Fixed {count} emoji encoding issues!")
print("All navigation items and page conditions should now work correctly.")
