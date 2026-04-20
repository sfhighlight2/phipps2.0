import re
import os

with open('/Users/schneiderjean/Documents/Claude/Projects/Phipps New Site/website-assets/PHIPPS-GLOBAL-SERVICES-CONTENT-BRIEF.md', 'r', encoding='utf-8') as f:
    md = f.read()

services_urls = {
    'Artwork': 'artwork.html',
    'Bathroom Accessories': 'bathroom-accessories.html',
    'Carpet Tiles': 'carpet-tiles.html',
    'FF&E': 'ffe.html',
    'Glass': 'glass.html',
    'LED Mirrors': 'led-mirrors.html',
    'LVT': 'lvt.html',
    'Plumbing Fixtures': 'plumbing-fixtures.html',
    'Shower Enclosures': 'shower-enclosures.html',
    'Stone': 'stone.html',
    'Tiles': 'tiles.html',
    'Wood Flooring': 'wood-flooring.html'
}

# Shared images
cross_img = {
    'Tiles': '3d-rendering-modern-tile-living-room-and-dining-room-e1733914643525.jpg',
    'Stone': 'stone-staircase-with-stone-walls-and-greenery-against-the-blue-sky-e1733914424854.jpg',
    'Glass': 'modern-glass-buildings-e1733913526693.jpg',
    'Bathroom Accessories': 'washbasin-in-a-modern-bathroom-with-ornamental-plants-and-bathroom-accessories-.jpg',
    'FF&E': 'poland-warsaw-seating-furniture-at-lounge-of-hotel-e1733913658549.jpg',
    'Furniture': 'poland-warsaw-seating-furniture-at-lounge-of-hotel-e1733913658549.jpg'
}

blocks = re.split(r'### \d{2} — ', md)[1:]

for block in blocks:
    lines = block.split('\n')
    service_name = lines[0].strip()
    
    url_slug = re.search(r'\*\*URL:\*\*.*phippsglobal\.com/([^/]+)/', block).group(1)
    file_name = url_slug + '.html'
    
    title = re.search(r'\*\*Page Title:\*\* (.*)', block).group(1).strip()
    tagline = re.search(r'\*\*Tagline:\*\* (.*)', block).group(1).strip()
    sub_head = re.search(r'\*\*Sub-Heading:\*\* (.*)', block).group(1).strip()
    
    intro_match = re.search(r'\*\*Intro Copy:\*\*\n(.*?)\n\n\*\*Body Copy:\*\*', block, re.DOTALL)
    intro = intro_match.group(1).strip() if intro_match else ""
    
    body_match = re.search(r'\*\*Body Copy:\*\*\n(.*?)\n\n\*\*Closing Copy:\*\*', block, re.DOTALL)
    body = body_match.group(1).strip() if body_match else ""
    
    cross_links_match = re.search(r'\*\*Explore More Cross-Links:\*\* (.*)', block)
    cross_links = [c.strip() for c in cross_links_match.group(1).split('|')] if cross_links_match else []
    
    hero_img = ""
    img_match = re.search(r'\|\s*`([^`]+)`\s*\|\s*https:\/\/.*?\*\*HERO\*\*', block)
    if img_match:
        hero_img = img_match.group(1)
        
    print(f"Parsed {service_name}: {file_name}")
    
    cross_html = ""
    for cl in cross_links:
        cl_file = services_urls.get(cl, 'services.html')
        cl_img = cross_img.get(cl, 'interior-setting-e1733914733183.jpg')
        cross_html += f'''
        <a class="portfolio-card reveal" href="{cl_file}">
            <img alt="{cl}" loading="lazy" src="images/{cl_img}"/>
            <div class="portfolio-card-info" style="justify-content:center; align-items:center; text-align:center;">
                <h4 style="font-size:24px;">{cl}</h4>
            </div>
        </a>'''

    page_html = f'''
    <!-- ═══ HERO ═══ -->
    <section class="overlay-hero" style="height:60vh; min-height:400px; position:relative; display:flex; align-items:center; justify-content:center; margin-top:var(--nav-h);">
      <img alt="{service_name}" class="hero-bg" src="images/{hero_img}" style="filter:brightness(0.5); width:100%; height:100%; object-fit:cover; position:absolute; top:0; left:0; z-index:-1;" />
      <div class="container hero-container" style="justify-content:center; align-items:center; text-align:center; position:relative; z-index:1;">
        <h1 class="reveal d1" style="font-size:52px; font-weight:400; color:#fff; margin-bottom:16px;">{title}</h1>
        <p class="reveal d2" style="font-size:18px; max-width:800px; color:rgba(255,255,255,0.8); margin:0 auto;">{tagline}</p>
      </div>
    </section>

    <!-- ═══ CONTENT ═══ -->
    <section class="section about-section" style="background:#fff;">
      <div class="container" style="max-width:900px; margin:0 auto;">
        <p class="lead reveal" style="font-size:20px; color:#1a1a1a; margin-bottom:60px; line-height:1.7;">{intro}</p>
        
        <h2 class="reveal d1" style="font-size:36px; margin-bottom:24px; font-weight:400;">{sub_head}</h2>
        <p class="reveal d2" style="font-size:16px; color:var(--text-secondary); margin-bottom:80px; line-height:1.8;">{body}</p>

        <!-- Why Choose Phipps Block -->
        <div class="why-choose-block reveal d3" style="padding-top:60px; border-top:1px solid var(--border);">
            <h3 style="font-size:24px; margin-bottom:16px; font-weight:600;">Unparalleled Products and Procurement</h3>
            <p style="margin-bottom:40px; color:var(--text-secondary); line-height:1.7;">As one of the top commercial building developers with a global reach, we procure materials from over 18 countries worldwide, tailoring them to meet your specific project requirements. Our close partnerships with factories grant us access to priority production lines, ensuring timely delivery and unwavering support.</p>
            
            <h3 style="font-size:24px; margin-bottom:16px; font-weight:600;">Unmatched Pricing and Results</h3>
            <p style="margin-bottom:40px; color:var(--text-secondary); line-height:1.7;">Our client base includes builders, architects, designers, hoteliers, and general contractors in the multifamily, affordable housing, commercial, residential, and hospitality sectors. With our deep understanding of production processes, sourcing locations, and pricing, we empower our clients to achieve their project goals within their budgetary constraints.</p>
            
            <h3 style="font-size:24px; margin-bottom:16px; font-weight:600;">The Phipps Philosophy</h3>
            <p style="margin-bottom:40px; color:var(--text-secondary); line-height:1.7;">Phipps Global is a leader in commercial building development, offering services for various projects across the USA and internationally. We ensure that every hotel, residential complex, and commercial facility meets high-quality standards. We create value through innovation and global sourcing, delivering attractive and cost-effective projects. Our clients, including builders, architects, and contractors, rely on us to realize their visions. With expertise in commercial development, Phipps Global is dedicated to excellence, effectively managing processes and pricing to help clients achieve their goals. For timely delivery and customized solutions, we are your ideal partner.</p>
            
            <h3 style="font-size:24px; margin-bottom:16px; font-weight:600;">One Unified Solution for Comprehensive Services</h3>
            <p style="margin-bottom:0; color:var(--text-secondary); line-height:1.7;">Phipps Global is a leading factory-direct manufacturing company committed to meeting the diverse needs of hotels, multi-family residential properties, and various commercial projects. Our dedication to quality and service ensures we provide exceptional products while addressing each client's specific requirements, creating ideal environments for living and working.</p>
        </div>
      </div>
    </section>

    <!-- ═══ CTA ═══ -->
    <section class="section-sm">
      <div class="cta-section">
        <h2 class="reveal d1">Ready to start your project?</h2>
        <a class="btn btn-accent btn-pill btn-lg btn-arrow reveal d3" href="get-in-touch.html" style="margin-top:24px;">Contact us</a>
      </div>
    </section>

    <!-- ═══ EXPLORE MORE ═══ -->
    <section class="section portfolio-section" style="background:#FAF8F5;">
      <div class="container">
        <div class="portfolio-header-split" style="justify-content:center; text-align:center; margin-bottom:60px;">
            <h2 class="reveal">Explore More Services</h2>
        </div>
        <div class="portfolio-grid-4">
            {cross_html}
        </div>
      </div>
    </section>
    '''

    with open(file_name, 'r', encoding='utf-8') as f:
        existing = f.read()

    # The mobile menu ends before the first section
    # Let's find '<section class="services-header"' or '<section class="overlay-hero"'
    body_start = existing.find('<!-- ═══ SERVICES HEADER ═══ -->')
    if body_start == -1: body_start = existing.find('<section class="services-header')
    if body_start == -1: body_start = existing.find('<!-- ═══ HERO ═══ -->')
    if body_start == -1: body_start = existing.find('<section class="')

    footer_start = existing.find('<footer class="site-footer">')
    
    if footer_start != -1 and body_start != -1:
        new_doc = existing[:body_start] + page_html + '\n    ' + existing[footer_start:]
        with open(file_name, 'w', encoding='utf-8') as fw:
            fw.write(new_doc)
    else:
        print(f"WARNING: Could not find insert points in {file_name}")

print("Page templates rewritten.")
