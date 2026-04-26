import os
import re

BASE_DIR = '/Volumes/Ext SSD/Phipps Global/New Site'

def get_local_projects():
    html_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.html')]
    # Exclude non-project pages
    exclude_files = [
        'index.html', 'hotels.html', 'residential.html', 'projects.html', 'our-firm.html',
        'services.html', 'get-in-touch.html', 'contact.html', 'hendricks.html',
        'artwork.html', 'bathroom-accessories.html', 'carpet-tiles.html', 'ffe.html',
        'glass.html', 'led-mirrors.html', 'lvt.html', 'plumbing-fixtures.html',
        'shower-enclosures.html', 'stone.html', 'tiles.html', 'wood-flooring.html'
    ]
    return [f.replace('.html', '') for f in html_files if f not in exclude_files]

def get_live_projects(filepath):
    projects = set()
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Looking for lines like "#### [Project Name](https://phippsglobal.com/project-url/)"
    # Or just extract all URLs that look like https://phippsglobal.com/some-project/
    urls = re.findall(r'https://phippsglobal\.com/([^/]+)/', content)
    for u in urls:
        if u not in ['hotels', 'residential', 'projects', 'our-firm', 'services', 'contact-us', 'cookie-policy', 'privacy-policy', 'terms-and-conditions', 'terms-of-use', 'cdn-cgi', 'wp-content']:
            projects.add(u)
    return projects

local = set(get_local_projects())
live_hotels = get_live_projects('/Users/schneiderjean/.gemini/antigravity/brain/73ba07f4-c73f-46e2-a0fb-3a7a4055d17e/.system_generated/steps/196/content.md')
live_res = get_live_projects('/Users/schneiderjean/.gemini/antigravity/brain/73ba07f4-c73f-46e2-a0fb-3a7a4055d17e/.system_generated/steps/197/content.md')

all_live = live_hotels.union(live_res)

missing = all_live - local

print(f"Total local projects: {len(local)}")
print(f"Total live projects: {len(all_live)}")
print(f"Missing projects to build: {len(missing)}")
for m in missing:
    if m in live_hotels:
        print(f"- {m} (Hotel)")
    else:
        print(f"- {m} (Residential)")
