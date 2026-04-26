import os
import re
import urllib.request
import certifi
import ssl
from bs4 import BeautifulSoup
import copy

BASE_DIR = '/Volumes/Ext SSD/Phipps Global/New Site'
TEMPLATE_PATH = os.path.join(BASE_DIR, 'hendricks.html')

with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    template_soup = BeautifulSoup(f.read(), 'html.parser')

def get_local_projects():
    # To handle mismatches like "hendricks-hotel" vs "hendricks", we just check what's there
    html_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.html')]
    return set([f.replace('.html', '') for f in html_files])

def extract_live_urls(filepath, sector):
    urls = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Looking for lines like "#### [Project Name](https://phippsglobal.com/project-url/)"
    # Or just extract all URLs
    matches = re.findall(r'https://phippsglobal\.com/([^/]+)/', content)
    for u in matches:
        if u not in ['hotels', 'residential', 'projects', 'our-firm', 'services', 'contact-us', 'cookie-policy', 'privacy-policy', 'terms-and-conditions', 'terms-of-use', 'cdn-cgi', 'wp-content', 'artwork', 'bathroom-accessories', 'carpet-tiles', 'ffe', 'glass', 'led-mirrors', 'lvt', 'plumbing-fixtures', 'shower-enclosures', 'stone', 'tiles', 'wood-flooring', 'safety', 'leadership', 'careers', 'history', 'sustainability']:
            if not u.endswith(')') and not u.startswith(')'):
                urls.append((u, sector))
    return urls

hotel_urls = extract_live_urls('/Users/schneiderjean/.gemini/antigravity/brain/73ba07f4-c73f-46e2-a0fb-3a7a4055d17e/.system_generated/steps/196/content.md', 'Hotels')
res_urls = extract_live_urls('/Users/schneiderjean/.gemini/antigravity/brain/73ba07f4-c73f-46e2-a0fb-3a7a4055d17e/.system_generated/steps/197/content.md', 'Residential')

all_live = hotel_urls + res_urls
# Deduplicate
unique_live = {}
for u, s in all_live:
    if u not in unique_live:
        unique_live[u] = s

local_files = get_local_projects()

# Normalization mapping (live_url -> local_file)
# If local file already exists, we skip it.
missing_projects = {}
for u, s in unique_live.items():
    # Basic check if it already exists exactly
    if u in local_files:
        continue
    # Check common aliases
    alias = u
    if u == 'hendricks-hotel': alias = 'hendricks'
    if u == '520-west-28th-street-by-zaha-hadid': alias = '520-west-28th'
    if u == '520-west-30th-street': alias = '520-west-30th'
    if u == '182-west-82nd-street': alias = '182-west-82nd'
    if alias in local_files:
        continue
    
    missing_projects[u] = s

print(f"Found {len(missing_projects)} missing projects. Starting scrape...")

ssl_context = ssl.create_default_context(cafile=certifi.where())

def fetch_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, context=ssl_context)
        return response.read()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def download_image(img_url, img_name):
    if img_url.startswith('/'):
        img_url = 'https://phippsglobal.com' + img_url
        
    ext = img_url.split('.')[-1].split('?')[0]
    if ext not in ['jpg', 'jpeg', 'png', 'webp', 'svg']:
        ext = 'jpg'
        
    local_path = f"images/{img_name}.{ext}"
    full_path = os.path.join(BASE_DIR, local_path)
    
    if os.path.exists(full_path):
        return local_path
        
    try:
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, context=ssl_context)
        with open(full_path, 'wb') as f:
            f.write(response.read())
        return local_path
    except Exception as e:
        print(f"Error downloading image {img_url}: {e}")
        return "images/placeholder.jpg"

for slug, sector in missing_projects.items():
    print(f"Scraping: {slug}...")
    url = f"https://phippsglobal.com/{slug}/"
    html_content = fetch_html(url)
    if not html_content:
        continue
        
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Title
    title_tag = soup.select_one('h1')
    title = title_tag.get_text(strip=True) if title_tag else slug.replace('-', ' ').title()
    
    # Hero Image
    hero_img = "images/placeholder.jpg"
    img_tag = soup.select_one('.wp-block-image img, .site-main img')
    if img_tag and img_tag.has_attr('src'):
        hero_img = download_image(img_tag['src'], slug)
        
    # Meta data (Location, Developer, Architect, Services)
    location = "USA"
    developer = "Private Developer"
    architect = "Various"
    services = []
    desc_paragraphs = []
    
    # Extract from text content
    content_area = soup.select_one('.site-main, .entry-content')
    if content_area:
        for p in content_area.find_all('p'):
            text = p.get_text(strip=True)
            if not text: continue
            
            lower_text = text.lower()
            if 'location:' in lower_text:
                location = text.split(':', 1)[1].strip()
            elif 'developer:' in lower_text:
                developer = text.split(':', 1)[1].strip()
            elif 'architect:' in lower_text:
                architect = text.split(':', 1)[1].strip()
            elif 'services:' in lower_text:
                services_str = text.split(':', 1)[1].strip()
                services = [s.strip() for s in services_str.split(',')]
            else:
                desc_paragraphs.append(text)
                
    if not desc_paragraphs:
        desc_paragraphs = [
            f"{title} represents another milestone in our factory-direct procurement portfolio.",
            f"Phipps Global provided end-to-end procurement for this {sector.lower()} project — sourcing premium materials from our international manufacturing network while maintaining strict quality control."
        ]
        
    # CREATE NEW PAGE BASED ON TEMPLATE
    new_soup = copy.copy(template_soup)
    
    if new_soup.title:
        new_soup.title.string = f"{title} | Phipps Global"
        
    # Update Hero
    hero = new_soup.select_one('.loc-hero')
    if hero:
        bg_img = hero.select_one('.loc-hero-bg')
        if bg_img:
            bg_img['src'] = hero_img
            bg_img['alt'] = title
            
        breadcrumb_spans = hero.select('.breadcrumb span[style*="#fff"]')
        for s in breadcrumb_spans:
            s.string = title
            
        breadcrumb_links = hero.select('.breadcrumb a')
        if len(breadcrumb_links) >= 2:
            breadcrumb_links[1].string = sector
            breadcrumb_links[1]['href'] = 'hotels.html' if sector == 'Hotels' else 'residential.html'
                
        eyebrow = hero.select_one('.eyebrow')
        if eyebrow:
            eyebrow.string = f"{sector.upper()} PROJECT"
            
        h1 = hero.select_one('h1')
        if h1:
            h1.string = title
            
        p = hero.select_one('.loc-hero-inner p')
        if p and len(desc_paragraphs) > 0:
            p.string = desc_paragraphs[0]
            
    # Update Stats Bar
    stats_grid = new_soup.select_one('.loc-stats-grid')
    if stats_grid:
        items = stats_grid.select('.loc-stat-item')
        if len(items) >= 4:
            items[0].select_one('.loc-stat-value').string = location.split(',')[0].strip() if ',' in location else location
            items[0].select_one('.loc-stat-sub').string = location.split(',')[1].strip() if ',' in location else ''
            items[1].select_one('.loc-stat-value').string = sector
            items[1].select_one('.loc-stat-sub').string = "Real Estate"
            items[2].select_one('.loc-stat-value').string = developer
            items[2].select_one('.loc-stat-sub').string = "Developer"
            items[3].select_one('.loc-stat-value').string = architect
            items[3].select_one('.loc-stat-sub').string = "Architecture"
            
    # Update Story Section
    story_text = new_soup.select_one('.loc-story-text')
    if story_text:
        h2 = story_text.select_one('h2')
        if h2: h2.string = f"Premium Finishes for {title}"
        for p in story_text.find_all('p'): p.decompose()
        for p_text in desc_paragraphs:
            new_p = new_soup.new_tag('p')
            new_p['style'] = "margin-bottom:20px;"
            new_p.string = p_text
            story_text.append(new_p)
            
    story_visual = new_soup.select_one('.loc-story-visual')
    if story_visual:
        img = story_visual.select_one('img')
        if img:
            img['src'] = hero_img
            img['alt'] = title
        quote = story_visual.select_one('.loc-story-quote p')
        if quote:
            quote.string = f"{title} represents our commitment to delivering premium factory-direct materials on timeline and on budget."
            
    # Update Scope of Work
    scope_grid = new_soup.select_one('.loc-scope-grid')
    if scope_grid:
        scope_grid.clear()
        if not services: services = ["Tile", "Wood Flooring", "Custom FF&E"]
        delays = ["", "d1", "d2"]
        for i, service in enumerate(services):
            delay_class = delays[i % 3]
            card = new_soup.new_tag('div', attrs={'class': f'loc-scope-card reveal {delay_class}'.strip()})
            icon_div = new_soup.new_tag('div', attrs={'class': 'loc-scope-icon'})
            svg = BeautifulSoup('<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M8 12l2 2 4-4"/></svg>', 'html.parser')
            icon_div.append(svg)
            card.append(icon_div)
            h4 = new_soup.new_tag('h4')
            h4.string = service
            card.append(h4)
            p = new_soup.new_tag('p')
            p.string = f"Premium {service.lower()} sourced factory-direct to meet exacting design and performance specifications."
            card.append(p)
            scope_grid.append(card)
            
    # Save the modified file
    file_path = os.path.join(BASE_DIR, f"{slug}.html")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(new_soup))
        
    print(f"Successfully generated {slug}.html")

print("All missing projects scraped and generated!")
