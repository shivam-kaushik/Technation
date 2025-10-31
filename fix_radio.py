import re

with open('app.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Fix corrupted emojis by finding and replacing the problematic lines
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'Your Profile' in line and line.strip().startswith('"') and '�' in line:
        lines[i] = '        "👤 Your Profile",'
    elif 'Upload CV & Analyze' in line and line.strip().startswith('"') and '�' in line:
        lines[i] = '        "📄 Upload CV & Analyze",'

content = '\n'.join(lines)

# Add key to radio
content = content.replace(
    '''        "🤝 Mentorship Matching"
    ]
)

# Anonymous mode toggle''',
    '''        "🤝 Mentorship Matching"
    ],
    key='nav_radio'
)

# Anonymous mode toggle''')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Fixed radio button - added key parameter and fixed corrupted emojis')
