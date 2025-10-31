with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the support resources section
start_marker = 'elif page == "🤝 Support Resources":'
end_marker = '# PAGE: WOMEN LEADERS (MERGED WITH MENTORSHIP)'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    # Read new section
    with open('support_resources_section.txt', 'r', encoding='utf-8') as f:
        new_section = f.read()
    
    # Replace the section
    new_content = content[:start_idx] + new_section + '\n\n# ============================================================================\n# ' + content[end_idx:]
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print('✅ Successfully replaced Support Resources section')
    print(f'   Start index: {start_idx}')
    print(f'   End index: {end_idx}')
else:
    print('❌ Could not find section markers')
    print(f'   Start marker found: {start_idx != -1}')
    print(f'   End marker found: {end_idx != -1}')
