import os
import glob
from bs4 import BeautifulSoup
import re
import copy

BASE_DIR = '/Volumes/Ext SSD/Phipps Global/New Site'

# Load the template (hendricks.html)
template_path = os.path.join(BASE_DIR, 'hendricks.html')
with open(template_path, 'r', encoding='utf-8') as f:
    template_soup = BeautifulSoup(f.read(), 'html.parser')

# Find all HTML files
all_html_files = glob.glob(os.path.join(BASE_DIR, '*.html'))

# Exclude non-project pages
exclude_files = [
    'index.html', 'hotels.html', 'residential.html', 'projects.html', 'our-firm.html',
    'services.html', 'get-in-touch.html', 'contact.html', 'hendricks.html',
    'artwork.html', 'bathroom-accessories.html', 'carpet-tiles.html', 'ffe.html',
    'glass.html', 'led-mirrors.html', 'lvt.html', 'plumbing-fixtures.html',
    'shower-enclosures.html', 'stone.html', 'tiles.html', 'wood-flooring.html'
]

project_files = [f for f in all_html_files if os.path.basename(f) not in exclude_files]

print(f"Found {len(project_files)} project files to process.")

def safe_extract(soup, selector, default=""):
    el = soup.select_one(selector)
    return el.get_text(strip=True) if el else default

def extract_meta_item(soup, label):
    for item in soup.select('.proj-meta-item'):
        lbl = item.select_one('.proj-meta-label')
        if lbl and label.lower() in lbl.get_text().lower():
            val = item.select_one('.proj-meta-value')
            if val:
                return val.get_text(strip=True)
    return ""

def extract_services(soup):
    services = []
    for item in soup.select('.proj-meta-item'):
        lbl = item.select_one('.proj-meta-label')
        if lbl and 'services' in lbl.get_text().lower():
            tags = item.select('.tag')
            for tag in tags:
                services.append(tag.get_text(strip=True))
    return services

for file_path in project_files:
    file_name = os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    print(f"Processing {file_name}...")

    # Extract Data from old file
    title = soup.title.string.split('|')[0].strip() if soup.title else ""
    if not title:
        h2 = soup.select_one('.proj-desc h2')
        if h2:
            title = h2.get_text(strip=True)
            
    # Main Image
    hero_img = soup.select_one('.proj-hero img')
    img_src = hero_img['src'] if hero_img and hero_img.has_attr('src') else "images/placeholder.jpg"
    
    # Metadata
    location = extract_meta_item(soup, "Location")
    sector = extract_meta_item(soup, "Sector")
    developer = extract_meta_item(soup, "Developer")
    architect = extract_meta_item(soup, "Architect")
    services = extract_services(soup)
    
    # Description
    desc_container = soup.select_one('.proj-desc .reveal.d1') or soup.select_one('.proj-desc p')
    if desc_container:
        desc_paragraphs = [p.get_text(strip=True) for p in desc_container.find_all('p')]
        if not desc_paragraphs: # maybe just text directly in the div
             desc_paragraphs = [desc_container.get_text(strip=True)]
    else:
        desc_paragraphs = ["Phipps Global provided factory-direct procurement for this project."]
    
    # Check if placeholder text is used
    if "With stylish interiors designed by Marchello Pozzi" in desc_paragraphs[0] and title != "Hendrick's Hotel":
        # Fallback description
        desc_paragraphs = [
            f"{title} represents another milestone in our factory-direct procurement portfolio.",
            f"Phipps Global provided end-to-end procurement for this {sector.lower()} project — sourcing premium materials from our international manufacturing network while maintaining strict quality control.",
            "Every material was hand-selected and quality-inspected to ensure the finished product matched the architect's exacting design vision."
        ]
        
    if not architect: architect = "Various"
    if not developer: developer = "Private Developer"
    if not location: location = "USA"

    # CREATE NEW PAGE BASED ON TEMPLATE
    new_soup = copy.copy(template_soup)
    
    # Update Title & Meta
    if new_soup.title:
        new_soup.title.string = f"{title} | Phipps Global"
    
    for meta in new_soup.find_all('meta'):
        if meta.get('property') == 'og:title':
            meta['content'] = f"{title} | Phipps Global"
        if meta.get('property') == 'og:url':
            meta['content'] = f"https://phippsglobal.com/{file_name}"
            
    # Update Hero
    hero = new_soup.select_one('.loc-hero')
    if hero:
        bg_img = hero.select_one('.loc-hero-bg')
        if bg_img:
            bg_img['src'] = img_src
            bg_img['alt'] = title
            
        breadcrumb_spans = hero.select('.breadcrumb span[style*="#fff"]')
        for s in breadcrumb_spans:
            s.string = title
            
        # Sector in breadcrumb
        breadcrumb_links = hero.select('.breadcrumb a')
        if len(breadcrumb_links) >= 2:
            breadcrumb_links[1].string = sector
            if sector.lower() == 'hotels':
                breadcrumb_links[1]['href'] = 'hotels.html'
            else:
                breadcrumb_links[1]['href'] = 'residential.html'
                
        eyebrow = hero.select_one('.eyebrow')
        if eyebrow:
            eyebrow.string = f"{sector.upper()} PROJECT"
            
        h1 = hero.select_one('h1')
        if h1:
            h1.string = title
            
        p = hero.select_one('.loc-hero-inner p')
        if p:
            p.string = desc_paragraphs[0]
            
    # Update Stats Bar
    stats_grid = new_soup.select_one('.loc-stats-grid')
    if stats_grid:
        items = stats_grid.select('.loc-stat-item')
        if len(items) >= 4:
            # Location
            items[0].select_one('.loc-stat-value').string = location.split('(')[0].strip() if location else 'USA'
            items[0].select_one('.loc-stat-sub').string = location.split('(')[1].replace(')','') if '(' in location else ''
            # Sector
            items[1].select_one('.loc-stat-value').string = sector if sector else 'Project'
            items[1].select_one('.loc-stat-sub').string = "Real Estate"
            # Developer
            items[2].select_one('.loc-stat-value').string = developer
            items[2].select_one('.loc-stat-sub').string = "Developer"
            # Architect
            items[3].select_one('.loc-stat-value').string = architect
            items[3].select_one('.loc-stat-sub').string = "Architecture"
            
    # Update Story Section
    story_text = new_soup.select_one('.loc-story-text')
    if story_text:
        h2 = story_text.select_one('h2')
        if h2:
            h2.string = f"Premium Finishes for {title}"
            
        # remove existing paragraphs
        for p in story_text.find_all('p'):
            p.decompose()
            
        # add new paragraphs
        for p_text in desc_paragraphs:
            new_p = new_soup.new_tag('p')
            new_p['style'] = "margin-bottom:20px;"
            new_p.string = p_text
            story_text.append(new_p)
            
    story_visual = new_soup.select_one('.loc-story-visual')
    if story_visual:
        img = story_visual.select_one('img')
        if img:
            img['src'] = img_src
            img['alt'] = title
        quote = story_visual.select_one('.loc-story-quote p')
        if quote:
            quote.string = f"{title} represents our commitment to delivering premium factory-direct materials on timeline and on budget."
            
    # Update Scope of Work
    scope_grid = new_soup.select_one('.loc-scope-grid')
    if scope_grid:
        # Clear existing cards
        scope_grid.clear()
        
        # Add new cards for each service
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
            
        if not services:
            # Add a generic service if none found
            card = new_soup.new_tag('div', attrs={'class': 'loc-scope-card reveal'})
            icon_div = new_soup.new_tag('div', attrs={'class': 'loc-scope-icon'})
            svg = BeautifulSoup('<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M8 12l2 2 4-4"/></svg>', 'html.parser')
            icon_div.append(svg)
            card.append(icon_div)
            h4 = new_soup.new_tag('h4')
            h4.string = "Custom FF&E"
            card.append(h4)
            p = new_soup.new_tag('p')
            p.string = "Comprehensive FF&E procurement delivered on timeline and budget."
            card.append(p)
            scope_grid.append(card)
            
    # Update Related Projects (Based on sector)
    related_h3 = new_soup.select_one('.section-sm h3.reveal')
    if related_h3:
        if sector.lower() == 'hotels':
            related_h3.string = "Related Hotel Projects"
            # Hendricks related projects: Gurney's, Hugo, Tantalo (already set in template)
        else:
            related_h3.string = "Related Residential Projects"
            view_all_btn = new_soup.select_one('.section-sm h3.reveal + a')
            if view_all_btn:
                view_all_btn['href'] = 'residential.html'
                view_all_btn.string = "View All Residential"
                
            port_grid = new_soup.select_one('.portfolio-grid')
            if port_grid:
                port_grid.clear()
                # Add 3 residential projects
                projects = [
                    {'url': '70-vestry-street.html', 'img': 'images/70-vestry-street-001-e1733387902509.jpg', 'title': '70 Vestry Street'},
                    {'url': '520-west-28th.html', 'img': 'images/520-west-28th-01-1.jpg', 'title': '520 West 28th St'},
                    {'url': '35-hudson-yard.html', 'img': 'images/35-hudson-yard-01.jpg', 'title': '35 Hudson Yard'}
                ]
                delays = ["", "d1", "d2"]
                for i, p in enumerate(projects):
                    if p['url'] == file_name: continue # avoid self link if possible, but fine for now
                    a = new_soup.new_tag('a', href=p['url'], attrs={'class': f'portfolio-card reveal {delays[i]}'.strip()})
                    img = new_soup.new_tag('img', alt=p['title'], src=p['img'], loading="lazy")
                    a.append(img)
                    info = new_soup.new_tag('div', attrs={'class': 'portfolio-card-info'})
                    h4 = new_soup.new_tag('h4')
                    h4.string = p['title']
                    span = new_soup.new_tag('span')
                    span.string = 'Residential'
                    info.append(h4)
                    info.append(span)
                    a.append(info)
                    port_grid.append(a)

    # Save the modified file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(new_soup))
        
    print(f"Successfully updated {file_name}")

print("All projects updated!")
