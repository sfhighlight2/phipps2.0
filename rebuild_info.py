import os
from bs4 import BeautifulSoup
import copy

BASE_DIR = '/Volumes/Ext SSD/Phipps Global/New Site'

def get_base_soup():
    with open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    nav = soup.select_one('nav#navbar')
    mobile_menu = soup.select_one('#mobileMenu')
    footer = soup.select_one('footer.site-footer')
    floating_phone = soup.select_one('.floating-phone')
    scripts = soup.select('script')
    
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
    
    content_placeholder = new_soup.new_tag('div', id='page-content')
    new_soup.body.append(content_placeholder)
    
    if footer: new_soup.body.append(copy.copy(footer))
    for s in scripts:
        if 'src' in s.attrs and 'script.js' in s['src']:
            new_soup.body.append(copy.copy(s))
    if floating_phone: new_soup.body.append(copy.copy(floating_phone))
    
    return new_soup

def build_our_firm():
    soup = get_base_soup()
    title = "Our Firm"
    desc = "About Phipps Global — a dynamic and comprehensive factory-direct manufacturing company serving hotels and residential properties."
    soup.title.string = f"{title} | Phipps Global"
    soup.find('meta', attrs={'name': 'description'})['content'] = desc
    
    content = soup.find(id='page-content')
    
    # Hero Section
    hero_html = f"""
    <div class="loc-hero" style="min-height:75vh;">
        <img src="images/poland-warsaw-seating-furniture-at-lounge-of-hotel-e1733913658549.jpg" alt="Our Firm" class="loc-hero-bg">
        <div class="loc-hero-overlay"></div>
        <div class="container" style="position:relative; z-index:3; padding-bottom:80px;">
            <nav aria-label="breadcrumb" class="breadcrumb" style="margin-bottom:24px;">
                <a href="index.html" style="color:rgba(255,255,255,0.7);">Home</a>
                <span style="color:rgba(255,255,255,0.4);">/</span>
                <span style="color:#fff;">Our Firm</span>
            </nav>
            <span class="eyebrow reveal" style="color:var(--accent);">About Us</span>
            <h1 class="reveal d1" style="color:#fff; font-size:clamp(40px, 6vw, 72px); margin-bottom:20px;">The Phipps <span class="accent" style="color:var(--accent);">Advantage</span></h1>
            <p class="lead reveal d2" style="max-width:600px; color:rgba(255,255,255,0.8);">Flexible, focused, and innovative — we are committed to achieving your project vision and business goals through unprecedented factory-direct access.</p>
        </div>
    </div>
    """
    content.append(BeautifulSoup(hero_html, 'html.parser'))
    
    # Who we are - large text block
    intro_html = """
    <section class="section" style="background:var(--bg-dark);">
        <div class="container" style="max-width:900px; text-align:center;">
            <span class="eyebrow reveal" style="color:var(--accent);">Who We Are</span>
            <h2 class="reveal d1" style="font-size:clamp(28px, 4vw, 42px); font-weight:300; line-height:1.4; color:#fff; margin-bottom:40px;">
                Phipps Global is a dynamic and comprehensive factory-direct manufacturing company specializing in serving the needs of hotels, multi-family residential properties, and commercial developments globally.
            </h2>
            <div class="reveal d2" style="display:flex; justify-content:center; gap:32px;">
                <div style="text-align:center;">
                    <div style="font-size:48px; font-weight:700; color:var(--accent);">18+</div>
                    <div style="font-size:14px; text-transform:uppercase; letter-spacing:0.1em; color:rgba(255,255,255,0.6); margin-top:8px;">Countries Sourced</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:48px; font-weight:700; color:var(--accent);">50+</div>
                    <div style="font-size:14px; text-transform:uppercase; letter-spacing:0.1em; color:rgba(255,255,255,0.6); margin-top:8px;">Projects Delivered</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:48px; font-weight:700; color:var(--accent);">100%</div>
                    <div style="font-size:14px; text-transform:uppercase; letter-spacing:0.1em; color:rgba(255,255,255,0.6); margin-top:8px;">Factory Direct</div>
                </div>
            </div>
        </div>
    </section>
    """
    content.append(BeautifulSoup(intro_html, 'html.parser'))
    
    # Split Section 1
    split1_html = """
    <section class="section" style="background:var(--bg-light);">
        <div class="container">
            <div class="about-grid">
                <div class="about-text">
                    <span class="eyebrow reveal">Our Network</span>
                    <h2 class="reveal d1">Global Reach, <span class="accent">Local Focus</span></h2>
                    <p class="reveal d2" style="font-size:17px; line-height:1.7; color:var(--text-secondary); margin-bottom:24px;">As one of the top commercial building developers with a global reach, we procure materials from over 18 countries worldwide, tailoring them to meet your specific project requirements. </p>
                    <p class="reveal d3" style="font-size:17px; line-height:1.7; color:var(--text-secondary);">Our close partnerships with factories grant us access to priority production lines. We navigate the complexities of production processes, sourcing locations, and pricing to empower our clients to achieve their project goals within budgetary constraints.</p>
                </div>
                <div class="about-image reveal-right" style="border-radius:var(--radius-lg); overflow:hidden;">
                    <img src="images/modern-glass-buildings-e1733913526693.jpg" alt="Global Reach" style="width:100%; height:100%; object-fit:cover; min-height:500px;">
                </div>
            </div>
        </div>
    </section>
    """
    content.append(BeautifulSoup(split1_html, 'html.parser'))
    
    # Split Section 2
    split2_html = """
    <section class="section" style="background:#fff;">
        <div class="container">
            <div class="about-grid" style="direction:rtl;">
                <div class="about-text" style="direction:ltr;">
                    <span class="eyebrow reveal">The Philosophy</span>
                    <h2 class="reveal d1">Value Through <span class="accent">Innovation</span></h2>
                    <p class="reveal d2" style="font-size:17px; line-height:1.7; color:var(--text-secondary); margin-bottom:24px;">Phipps Global stands out as a leading name offering comprehensive factory-direct development services. Based in Florida, we extend our expertise across the USA and internationally.</p>
                    <p class="reveal d3" style="font-size:17px; line-height:1.7; color:var(--text-secondary);">Our approach is to create value through innovation and efficiency. We ensure that every hotel, residential complex, and commercial facility meets the highest standards of quality and design while remaining economically advantageous. Our clients trust us to bring their vision to life with precision and care.</p>
                    <a href="images/PHIPPS-GLOBAL-PRESENTATION-2026.pdf" target="_blank" class="btn btn-dark btn-pill btn-arrow reveal d4" style="margin-top:24px;">View Full Presentation</a>
                </div>
                <div class="about-image reveal-left" style="border-radius:var(--radius-lg); overflow:hidden; direction:ltr;">
                    <img src="images/interior-setting-e1733914733183.jpg" alt="Innovation" style="width:100%; height:100%; object-fit:cover; min-height:500px;">
                </div>
            </div>
        </div>
    </section>
    """
    content.append(BeautifulSoup(split2_html, 'html.parser'))

    # CTA
    cta_html = """
    <section class="section-sm" style="background:var(--bg-light);">
        <div class="cta-section">
            <span class="eyebrow reveal" style="color:var(--accent);">Let's Build Together</span>
            <h2 class="reveal d1" style="color:#fff;">Ready to Start Your <span class="accent">Project</span>?</h2>
            <p class="reveal d2" style="color:rgba(255,255,255,0.7);">Get in touch with our team today to discuss how we can bring your vision to life.</p>
            <a href="get-in-touch.html" class="btn btn-accent btn-pill btn-lg btn-arrow reveal d3">Contact Us</a>
        </div>
    </section>
    """
    content.append(BeautifulSoup(cta_html, 'html.parser'))
    
    with open(os.path.join(BASE_DIR, 'our-firm.html'), 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Generated our-firm.html")

def build_services():
    soup = get_base_soup()
    title = "Services"
    desc = "Phipps Global Services — Exquisite tile, flooring, countertops, showers, furniture, FF&E, bathroom furnishings, millwork and more, all factory-direct."
    soup.title.string = f"{title} | Phipps Global"
    soup.find('meta', attrs={'name': 'description'})['content'] = desc
    
    content = soup.find(id='page-content')
    
    # Hero Section
    hero_html = f"""
    <div class="loc-hero" style="min-height:60vh;">
        <img src="images/white-living-room-with-carpet-e1733913999924.jpg" alt="Our Services" class="loc-hero-bg">
        <div class="loc-hero-overlay"></div>
        <div class="container" style="position:relative; z-index:3; padding-bottom:60px;">
            <nav aria-label="breadcrumb" class="breadcrumb" style="margin-bottom:24px;">
                <a href="index.html" style="color:rgba(255,255,255,0.7);">Home</a>
                <span style="color:rgba(255,255,255,0.4);">/</span>
                <span style="color:#fff;">Services</span>
            </nav>
            <span class="eyebrow reveal" style="color:var(--accent);">What We Do</span>
            <h1 class="reveal d1" style="color:#fff; font-size:clamp(40px, 6vw, 72px); margin-bottom:20px;">Our <span class="accent" style="color:var(--accent);">Services</span></h1>
            <p class="lead reveal d2" style="max-width:600px; color:rgba(255,255,255,0.8);">Comprehensive product categories, all sourced factory-direct from our global network of manufacturers across 18+ countries.</p>
        </div>
    </div>
    """
    content.append(BeautifulSoup(hero_html, 'html.parser'))
    
    # Services Grid (Card-based immersive grid)
    services_data = [
        {"name": "Tile & Stone", "desc": "Thin tile, pavers, sintered stone, large format porcelain, ceramic, glass, terrazzo, and mosaic.", "img": "images/3d-rendering-modern-tile-living-room-and-dining-room-e1733914643525.jpg", "link": "tiles.html"},
        {"name": "Wood Flooring", "desc": "Solid wood, engineered wood, and custom flooring options for every residential or commercial application.", "img": "images/living-room-with-wood-flooring-e1733914178998.jpg", "link": "wood-flooring.html"},
        {"name": "Countertops", "desc": "Granite, marble, quartz, solid surface, and porcelain slab manufactured to exact specifications.", "img": "images/interior-setting-e1733914733183.jpg", "link": "stone.html"},
        {"name": "Showers & Baths", "desc": "Glass shower enclosures and designer bathtubs designed to elevate any hospitality bathroom experience.", "img": "images/luxurious-modern-bathroom-with-marble-walls-and-glass-shower--e1733913328449.jpg", "link": "shower-enclosures.html"},
        {"name": "Furniture", "desc": "Multifunctional and outdoor furniture designed and manufactured to your exact specifications.", "img": "images/poland-warsaw-seating-furniture-at-lounge-of-hotel-e1733913658549.jpg", "link": "ffe.html"},
        {"name": "Bathroom Accessories", "desc": "Medicine cabinets, LED mirrors, vanities, sinks, faucets, and comprehensive plumbing fixtures.", "img": "images/luxurious-modern-bathroom-with-marble-walls-and-glass-shower--e1733913328449.jpg", "link": "bathroom-accessories.html"},
        {"name": "LVT", "desc": "Luxury Vinyl Tile crafted for high-traffic commercial durability and stunning visual appeal.", "img": "images/living-room-with-wood-flooring-e1733914178998.jpg", "link": "lvt.html"},
        {"name": "Artwork", "desc": "Curated and custom-manufactured artwork to complete your interior design narrative.", "img": "images/white-living-room-with-carpet-e1733913999924.jpg", "link": "artwork.html"},
        {"name": "LED Mirrors", "desc": "Custom LED mirrors offering flawless illumination and modern aesthetics for guestrooms.", "img": "images/luxurious-modern-bathroom-with-marble-walls-and-glass-shower--e1733913328449.jpg", "link": "led-mirrors.html"},
    ]
    
    grid_html = """
    <section class="section" style="background:var(--bg-light);">
        <div class="container">
            <div class="masonry-grid" style="columns:auto; column-count:3; gap:24px;">
    """
    for i, s in enumerate(services_data):
        delay = ["", "d1", "d2"][i % 3]
        grid_html += f"""
        <a href="{s['link']}" class="masonry-item reveal {delay}" style="display:block; margin-bottom:24px; aspect-ratio:4/5;">
            <img src="{s['img']}" alt="{s['name']}" style="height:100%; object-fit:cover;">
            <div class="masonry-overlay" style="background:linear-gradient(to top, rgba(0,0,0,0.9), transparent 80%); padding:32px;">
                <h3 style="color:#fff; font-size:24px; margin-bottom:8px;">{s['name']}</h3>
                <p style="color:rgba(255,255,255,0.7); font-size:14px; line-height:1.5; margin-bottom:16px;">{s['desc']}</p>
                <span style="color:var(--accent); font-size:13px; text-transform:uppercase; letter-spacing:0.05em; font-weight:600;">Explore Service &rarr;</span>
            </div>
        </a>
        """
    grid_html += """
            </div>
        </div>
    </section>
    """
    content.append(BeautifulSoup(grid_html, 'html.parser'))
    
    # CTA
    cta_html = """
    <section class="section-sm" style="background:var(--bg-light);">
        <div class="cta-section">
            <span class="eyebrow reveal" style="color:var(--accent);">Get Started</span>
            <h2 class="reveal d1" style="color:#fff;">Need Materials for <span class="accent">Your Project</span>?</h2>
            <p class="reveal d2" style="color:rgba(255,255,255,0.7);">Tell us what you need — we'll source it factory-direct from our global network.</p>
            <a href="get-in-touch.html" class="btn btn-accent btn-pill btn-lg btn-arrow reveal d3">Request a Quote</a>
        </div>
    </section>
    """
    content.append(BeautifulSoup(cta_html, 'html.parser'))
    
    with open(os.path.join(BASE_DIR, 'services.html'), 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Generated services.html")

build_our_firm()
build_services()
