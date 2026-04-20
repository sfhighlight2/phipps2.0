import re
import glob
from bs4 import BeautifulSoup
import os
import shutil

# First, generate missing Project pages
missing_projects = {
    'tantalo.html': ('Tantalo Hotel - Panama City', 'Tantalo Hotel', 'Panama City'),
    'the-time.html': ('The Time Hotel - Nyack, New York', 'The Time', 'Nyack, New York')
}

with open('hendricks.html', 'r', encoding='utf-8') as f:
    project_template = f.read()

for p_file, (title, name, loc) in missing_projects.items():
    if not os.path.exists(p_file):
        new_content = project_template.replace("Hendrick's Hotel", name)
        new_content = new_content.replace('New York, New York', loc)
        new_content = new_content.replace('hendricks.html', p_file)
        with open(p_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

# Second, generate missing Service pages
missing_services = {
    'artwork.html': 'Artwork',
    'bathroom-accessories.html': 'Bathroom Accessories',
    'carpet-tiles.html': 'Carpet Tiles',
    'ffe.html': 'FF&E',
    'glass.html': 'Glass',
    'led-mirrors.html': 'LED Mirrors',
    'lvt.html': 'LVT',
    'plumbing-fixtures.html': 'Plumbing Fixtures',
    'shower-enclosures.html': 'Shower Enclosures',
    'stone.html': 'Stone',
    'tiles.html': 'Tiles',
    'wood-flooring.html': 'Wood Flooring'
}

with open('services.html', 'r', encoding='utf-8') as f:
    service_template = f.read()

# Replace main title in services
for s_file, s_name in missing_services.items():
    if not os.path.exists(s_file):
        # Extremely basic substitution
        new_content = service_template.replace('Procurement Services', f'{s_name} Procurement')
        new_content = new_content.replace('<title>Services | Phipps Global</title>', f'<title>{s_name} | Phipps Global Procurement</title>')
        with open(s_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

# Third, SEO enhancement on all files
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    head = soup.find('head')
    if not head:
        continue
        
    title_tag = soup.find('title')
    title_text = title_tag.text if title_tag else "Phipps Global | Factory Direct Architecture Procurement"
    
    # Meta description
    desc_tag = head.find('meta', attrs={'name': 'description'})
    if not desc_tag:
        desc_tag = soup.new_tag('meta', attrs={'name': 'description', 'content': f'Phipps Global offers premium factory direct procurement for {title_text}. Discover our luxury materials and custom manufacturing solutions.'})
        head.append(desc_tag)
    
    # Open Graph Tags
    og_title = head.find('meta', attrs={'property': 'og:title'})
    if not og_title:
        head.append(soup.new_tag('meta', attrs={'property': 'og:title', 'content': title_text}))
        head.append(soup.new_tag('meta', attrs={'property': 'og:description', 'content': desc_tag.get('content', '')}))
        head.append(soup.new_tag('meta', attrs={'property': 'og:type', 'content': 'website'}))
        head.append(soup.new_tag('meta', attrs={'property': 'og:image', 'content': 'https://phippsglobal.com/images/phipps-global-logo-03.svg'}))
        head.append(soup.new_tag('meta', attrs={'property': 'og:url', 'content': f'https://phippsglobal.com/{file}'}))
    
    # JSON-LD Schema
    schema_script = head.find('script', attrs={'type': 'application/ld+json'})
    if not schema_script:
        schema = ""
        if file == 'index.html':
            schema = """
            {
              "@context": "https://schema.org",
              "@type": "Organization",
              "name": "Phipps Global",
              "url": "https://phippsglobal.com",
              "logo": "https://phippsglobal.com/images/phipps-global-logo-03.svg",
              "description": "Premium factory direct procurement firm specializing in luxury hospitality and residential architectural materials.",
              "address": {
                "@type": "PostalAddress",
                "addressLocality": "New York",
                "addressRegion": "NY",
                "addressCountry": "US"
              }
            }"""
        elif file in missing_services:
            schema = f"""
            {{
              "@context": "https://schema.org",
              "@type": "Service",
              "serviceType": "{title_text}",
              "provider": {{
                "@type": "Organization",
                "name": "Phipps Global"
              }},
              "areaServed": "Worldwide"
            }}"""
        else:
            schema = f"""
            {{
              "@context": "https://schema.org",
              "@type": "WebPage",
              "name": "{title_text}",
              "publisher": {{
                "@type": "Organization",
                "name": "Phipps Global"
              }}
            }}"""
            
        script_tag = soup.new_tag('script', type='application/ld+json')
        script_tag.string = schema
        head.append(script_tag)
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

print("Created missing pages and injected SEO JSON-LD and Meta Tags across", len(glob.glob('*.html')), "pages.")
