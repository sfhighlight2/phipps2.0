import os
from bs4 import BeautifulSoup
import copy

BASE_DIR = '/Volumes/Ext SSD/Phipps Global/New Site'

def get_base_soup():
    # Use index.html as a base template for nav/footer
    with open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    # Remove everything between nav and footer
    nav = soup.select_one('nav#navbar')
    mobile_menu = soup.select_one('#mobileMenu')
    footer = soup.select_one('footer.site-footer')
    floating_phone = soup.select_one('.floating-phone')
    scripts = soup.select('script')
    
    # Create a fresh body
    new_soup = BeautifulSoup('<!DOCTYPE html><html lang="en"><head></head><body></body></html>', 'html.parser')
    new_soup.head.append(soup.head.find('meta', charset='utf-8'))
    new_soup.head.append(soup.head.find('meta', attrs={'name': 'viewport'}))
    
    desc = new_soup.new_tag('meta', attrs={'name': 'description', 'content': ''})
    new_soup.head.append(desc)
    
    title = new_soup.new_tag('title')
    new_soup.head.append(title)
    
    link = new_soup.new_tag('link', rel='stylesheet', href='style.css?v=2.0')
    new_soup.head.append(link)
    
    new_soup.body.append(new_soup.new_tag('div', attrs={'class': 'loading-line'}))
    if nav: new_soup.body.append(copy.copy(nav))
    if mobile_menu: new_soup.body.append(copy.copy(mobile_menu))
    
    # We will inject content here
    content_placeholder = new_soup.new_tag('div', id='page-content')
    new_soup.body.append(content_placeholder)
    
    if footer: new_soup.body.append(copy.copy(footer))
    for s in scripts:
        if 'src' in s.attrs and 'script.js' in s['src']:
            new_soup.body.append(copy.copy(s))
    if floating_phone: new_soup.body.append(copy.copy(floating_phone))
    
    return new_soup

def get_all_projects():
    projects = []
    html_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.html')]
    exclude_files = [
        'index.html', 'hotels.html', 'residential.html', 'projects.html', 'our-firm.html',
        'services.html', 'get-in-touch.html', 'contact.html', 'hendricks.html',
        'artwork.html', 'bathroom-accessories.html', 'carpet-tiles.html', 'ffe.html',
        'glass.html', 'led-mirrors.html', 'lvt.html', 'plumbing-fixtures.html',
        'shower-enclosures.html', 'stone.html', 'tiles.html', 'wood-flooring.html',
        'safety.html', 'leadership.html', 'careers.html', 'history.html', 'sustainability.html'
    ]
    
    for f in html_files:
        if f in exclude_files: continue
        
        with open(os.path.join(BASE_DIR, f), 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            
            # Extract info
            h1 = soup.select_one('h1')
            title = h1.get_text(strip=True) if h1 else f.replace('.html', '').replace('-', ' ').title()
            
            hero_bg = soup.select_one('.loc-hero-bg')
            img_src = hero_bg['src'] if hero_bg else 'images/placeholder.jpg'
            
            eyebrow = soup.select_one('.eyebrow')
            eyebrow_text = eyebrow.get_text(strip=True).lower() if eyebrow else ''
            
            if 'hotel' in eyebrow_text:
                cat = 'hotels'
                subtitle = 'Hotels'
            else:
                cat = 'residential'
                subtitle = 'Residential'
                
            projects.append({
                'href': f,
                'img': img_src,
                'title': title,
                'subtitle': subtitle,
                'category': cat
            })
            
    return projects

unique_projects = get_all_projects()

def build_gallery_page(filename, title, subtitle, desc, filter_cat=None):
    soup = get_base_soup()
    soup.title.string = f"{title} | Phipps Global"
    soup.find('meta', attrs={'name': 'description'})['content'] = desc
    
    content = soup.find(id='page-content')
    
    # Hero Section
    hero_html = f"""
    <div class="loc-hero" style="min-height:60vh;">
        <img src="images/stone-staircase-with-stone-walls-and-greenery-against-the-blue-sky-e1733914424854.jpg" alt="{title}" class="loc-hero-bg">
        <div class="loc-hero-overlay"></div>
        <div class="container" style="position:relative; z-index:3; padding-bottom:60px;">
            <nav aria-label="breadcrumb" class="breadcrumb" style="margin-bottom:24px;">
                <a href="index.html" style="color:rgba(255,255,255,0.7);">Home</a>
                <span style="color:rgba(255,255,255,0.4);">/</span>
                <span style="color:#fff;">{title}</span>
            </nav>
            <span class="eyebrow reveal" style="color:var(--accent);">{subtitle}</span>
            <h1 class="reveal d1" style="color:#fff; font-size:clamp(40px, 6vw, 72px); margin-bottom:20px;">{title}</h1>
            <p class="lead reveal d2" style="max-width:600px; color:rgba(255,255,255,0.8);">{desc}</p>
        </div>
    </div>
    """
    content.append(BeautifulSoup(hero_html, 'html.parser'))
    
    # Filter Bar (only for projects.html)
    if filename == 'projects.html':
        filter_html = """
        <div class="res-filter-section" style="background:var(--bg-light); border-bottom:1px solid var(--border);">
            <div class="container">
                <div class="filter-bar" style="justify-content:center;">
                    <button class="filter-btn active" data-filter="all">All Projects</button>
                    <button class="filter-btn" data-filter="hotels">Hotels</button>
                    <button class="filter-btn" data-filter="residential">Residential</button>
                </div>
            </div>
        </div>
        """
        content.append(BeautifulSoup(filter_html, 'html.parser'))
        
    # Gallery Grid
    gallery_html = """
    <section class="section" style="background:var(--bg-light);">
        <div class="container">
            <div class="masonry-grid" id="gallery-grid">
            </div>
        </div>
    </section>
    """
    content.append(BeautifulSoup(gallery_html, 'html.parser'))
    
    grid = content.select_one('#gallery-grid')
    delays = ["", "d1", "d2"]
    
    filtered_projects = unique_projects if not filter_cat else [p for p in unique_projects if p['category'] == filter_cat]
    
    for i, p in enumerate(filtered_projects):
        delay = delays[i % 3]
        cat = p['category']
        item_html = f"""
        <a href="{p['href']}" class="masonry-item reveal {delay}" data-cat="{cat}" style="display:block;">
            <img src="{p['img']}" alt="{p['title']}" loading="lazy">
            <div class="masonry-overlay">
                <h4>{p['title']}</h4>
                <span>{p['subtitle']}</span>
            </div>
        </a>
        """
        grid.append(BeautifulSoup(item_html, 'html.parser'))
        
    # CTA
    cta_html = """
    <section class="section-sm" style="background:var(--bg-light);">
        <div class="cta-section">
            <span class="eyebrow reveal" style="color:var(--accent);">Your Next Project</span>
            <h2 class="reveal d1" style="color:#fff;">Start Your <span class="accent">Procurement</span></h2>
            <p class="reveal d2" style="color:rgba(255,255,255,0.7);">Let's discuss how Phipps Global can deliver factory-direct procurement for your next development.</p>
            <a href="get-in-touch.html" class="btn btn-accent btn-pill btn-lg btn-arrow reveal d3">Get in Touch</a>
        </div>
    </section>
    """
    content.append(BeautifulSoup(cta_html, 'html.parser'))
    
    # Save
    with open(os.path.join(BASE_DIR, filename), 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Generated {filename} with {len(filtered_projects)} items.")

# Generate the 3 gallery pages
build_gallery_page('projects.html', 'All Projects', 'Portfolio', '50+ completed projects worldwide — from landmark hotels to prestigious residential towers. Explore our factory-direct procurement portfolio.')
build_gallery_page('hotels.html', 'Hotels & Hospitality', 'Hospitality Portfolio', 'World-renowned hotels partner with Phipps Global for comprehensive procurement — from bespoke tile and stone to custom furniture and FF&E.', 'hotels')
build_gallery_page('residential.html', 'Residential Portfolio', 'Luxury Residences', 'Luxury residential properties turn to Phipps Global for tailored procurement — high-end finishings, custom millwork, stone, and signature materials.', 'residential')

