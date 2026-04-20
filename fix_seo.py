import re

with open('/Users/schneiderjean/Documents/Claude/Projects/Phipps New Site/website-assets/PHIPPS-GLOBAL-SERVICES-CONTENT-BRIEF.md', 'r', encoding='utf-8') as f:
    md = f.read()

blocks = re.split(r'### \d{2} — ', md)[1:]

for block in blocks:
    lines = block.split('\n')
    service_name = lines[0].strip()
    
    url_slug = re.search(r'\*\*URL:\*\*.*phippsglobal\.com/([^/]+)/', block).group(1)
    file_name = url_slug + '.html'
    
    title = re.search(r'\*\*Page Title:\*\* (.*)', block).group(1).strip()
    
    intro_match = re.search(r'\*\*Intro Copy:\*\*\n(.*?)\n\n\*\*Body Copy:\*\*', block, re.DOTALL)
    intro = intro_match.group(1).strip().replace('"', '&quot;') if intro_match else ""
    
    # Let's read the file and replace the meta tags
    with open(file_name, 'r', encoding='utf-8') as f:
        existing = f.read()
        
    # Replace <title>
    existing = re.sub(r'<title>.*?</title>', f'<title>{title} | Phipps Global Procurement</title>', existing)
    
    # Replace meta description
    existing = re.sub(r'<meta content=".*?" name="description"/>', f'<meta content="{intro}" name="description"/>', existing)
    existing = re.sub(r'<meta content=".*?" property="og:description"/>', f'<meta content="{intro}" property="og:description"/>', existing)
    
    # Replace og:title
    existing = re.sub(r'<meta content=".*?" property="og:title"/>', f'<meta content="{title} | Phipps Global Procurement" property="og:title"/>', existing)
    
    # Replace json-ld service type
    existing = re.sub(r'"serviceType": ".*?"', f'"serviceType": "{title}"', existing)

    with open(file_name, 'w', encoding='utf-8') as fw:
        fw.write(existing)

print("SEO Metatags Rewritten")
