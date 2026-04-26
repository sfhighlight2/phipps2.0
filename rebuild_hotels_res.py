#!/usr/bin/env python3
"""
Rebuild hotels.html and residential.html with:
- Premium editorial masonry grid
- Fixed image paths (no placeholders)
- SEO-optimized structure
- Improved UX (count badge, category label, hover CTA)
"""
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
    
    # Head
    new_soup.head.append(BeautifulSoup('<meta charset="UTF-8">', 'html.parser'))
    new_soup.head.append(BeautifulSoup('<meta name="viewport" content="width=device-width, initial-scale=1.0">', 'html.parser'))
    new_soup.head.append(BeautifulSoup('<meta name="description" content="">', 'html.parser'))
    new_soup.head.append(BeautifulSoup('<meta property="og:type" content="website">', 'html.parser'))
    new_soup.head.append(BeautifulSoup('<title></title>', 'html.parser'))
    new_soup.head.append(BeautifulSoup('<link rel="stylesheet" href="style.css?v=2.0">', 'html.parser'))
    
    new_soup.body.append(BeautifulSoup('<div class="loading-line"></div>', 'html.parser'))
    if nav: new_soup.body.append(copy.copy(nav))
    if mobile_menu: new_soup.body.append(copy.copy(mobile_menu))

    content_placeholder = new_soup.new_tag('main', id='page-content')
    new_soup.body.append(content_placeholder)

    if footer: new_soup.body.append(copy.copy(footer))
    for s in scripts:
        if 'src' in s.attrs and 'script.js' in s['src']:
            new_soup.body.append(copy.copy(s))
    if floating_phone: new_soup.body.append(copy.copy(floating_phone))

    return new_soup


def get_all_projects(category_filter=None):
    html_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.html')]
    exclude = [
        'index.html','hotels.html','residential.html','projects.html','our-firm.html',
        'services.html','get-in-touch.html','contact.html','hendricks.html',
        'artwork.html','bathroom-accessories.html','carpet-tiles.html','ffe.html',
        'glass.html','led-mirrors.html','lvt.html','plumbing-fixtures.html',
        'shower-enclosures.html','stone.html','tiles.html','wood-flooring.html',
    ]
    projects = []
    for f in sorted(html_files):
        if f in exclude: continue
        with open(os.path.join(BASE_DIR, f), 'r') as fp:
            soup = BeautifulSoup(fp.read(), 'html.parser')

        h1 = soup.select_one('h1')
        title = h1.get_text(strip=True) if h1 else f.replace('.html','').replace('-',' ').title()

        hero_bg = soup.select_one('.loc-hero-bg')
        img_src = hero_bg['src'] if hero_bg and hero_bg.get('src') else None
        if not img_src or img_src == 'images/placeholder.jpg':
            continue
        if not os.path.exists(os.path.join(BASE_DIR, img_src)):
            continue

        eyebrow = soup.select_one('.eyebrow')
        eyebrow_text = eyebrow.get_text(strip=True).lower() if eyebrow else ''
        cat = 'hotels' if 'hotel' in eyebrow_text else 'residential'

        stat_items = soup.select('.loc-stat-item')
        location = ''
        if stat_items:
            val = stat_items[0].select_one('.loc-stat-value')
            sub = stat_items[0].select_one('.loc-stat-sub')
            if val:
                location = val.get_text(strip=True)
                if sub and sub.get_text(strip=True):
                    location += ', ' + sub.get_text(strip=True)

        if category_filter and cat != category_filter:
            continue

        projects.append({
            'href': f,
            'img': img_src,
            'title': title,
            'location': location,
            'category': cat,
        })

    return projects


# ─── HOTELS PAGE ──────────────────────────────────────────────────────────────
def build_hotels():
    projects = get_all_projects('hotels')
    soup = get_base_soup()

    title_str = 'Hotels & Hospitality | Phipps Global'
    desc_str = ('World-renowned hotels partner with Phipps Global for factory-direct procurement — '
                'tile, stone, flooring, glass, FF&E and more across 20+ landmark hospitality projects.')

    soup.find('title').string = title_str
    soup.find('meta', attrs={'name': 'description'})['content'] = desc_str
    soup.find('meta', attrs={'property': 'og:type'})  # already set

    content = soup.find(id='page-content')

    # ── Hero ─────────────────────────────────────────────────────────────────
    hero_html = f"""
    <header class="loc-hero" style="min-height:72vh;" aria-label="Hotels portfolio hero">
      <img src="images/hotel-lobby-luxury.webp" alt="Luxury hotel interior by Phipps Global"
           class="loc-hero-bg" fetchpriority="high">
      <div class="loc-hero-overlay"></div>
      <div class="container" style="position:relative;z-index:3;padding-bottom:72px;">
        <nav aria-label="Breadcrumb" class="breadcrumb" style="margin-bottom:20px;">
          <a href="index.html" style="color:rgba(255,255,255,.65);">Home</a>
          <span style="color:rgba(255,255,255,.35);margin:0 8px;">/</span>
          <span style="color:#fff;">Hotels</span>
        </nav>
        <span class="eyebrow reveal" style="color:#dcb974; letter-spacing:0.1em; font-weight:600;">Hospitality Portfolio</span>
        <h1 class="reveal d1" style="color:#fff;font-size:clamp(36px,5.5vw,68px);margin:12px 0 20px;font-weight:700;line-height:1.1;">
          Hotel &amp; Hospitality<br><span style="color:#dcb974;">Procurement Projects</span>
        </h1>
        <p class="lead reveal d2"
           style="max-width:560px;color:rgba(255,255,255,.78);font-size:18px;line-height:1.6;margin-bottom:32px;">
          Factory-direct procurement for the world's finest hotels — from flagship Marriotts to boutique 
          independents. {len(projects)} completed hospitality projects worldwide.
        </p>
        <div class="reveal d3" style="display:flex;gap:16px;flex-wrap:wrap;">
          <a href="get-in-touch.html" class="btn btn-accent btn-pill btn-arrow">Start Your Project</a>
          <a href="projects.html" class="btn btn-outline btn-pill" style="color:#fff;border-color:rgba(255,255,255,.4);">All Projects</a>
        </div>
      </div>
    </header>
    """
    content.append(BeautifulSoup(hero_html, 'html.parser'))

    # ── Stats Strip ──────────────────────────────────────────────────────────
    stats_html = """
    <div style="background:var(--bg-dark);border-top:1px solid rgba(255,255,255,.07);border-bottom:1px solid rgba(255,255,255,.07);">
      <div class="container">
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0;padding:0;">
          <div style="padding:28px 24px;border-right:1px solid rgba(255,255,255,.07);text-align:center;">
            <div style="font-size:36px;font-weight:700;color:var(--accent);">20+</div>
            <div style="font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.5);margin-top:4px;">Hotel Projects</div>
          </div>
          <div style="padding:28px 24px;border-right:1px solid rgba(255,255,255,.07);text-align:center;">
            <div style="font-size:36px;font-weight:700;color:var(--accent);">18+</div>
            <div style="font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.5);margin-top:4px;">Countries Sourced</div>
          </div>
          <div style="padding:28px 24px;border-right:1px solid rgba(255,255,255,.07);text-align:center;">
            <div style="font-size:36px;font-weight:700;color:var(--accent);">100%</div>
            <div style="font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.5);margin-top:4px;">Factory Direct</div>
          </div>
          <div style="padding:28px 24px;text-align:center;">
            <div style="font-size:36px;font-weight:700;color:var(--accent);">On-Time</div>
            <div style="font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.5);margin-top:4px;">Delivery Record</div>
          </div>
        </div>
      </div>
    </div>
    """
    content.append(BeautifulSoup(stats_html, 'html.parser'))

    # ── Gallery Grid ─────────────────────────────────────────────────────────
    # Build full gallery section as one block
    cards_html = ''
    delays = ['', 'd1', 'd2']
    for i, p in enumerate(projects):
        d = delays[i % 3]
        loc_span = f"<span>{p['location']}</span>" if p['location'] else '<span>Various</span>'
        cards_html += f"""
        <a href="{p['href']}" class="editorial-card reveal {d}" aria-label="View {p['title']} project">
          <div class="editorial-card-img-wrapper">
            <img src="{p['img']}" alt="{p['title']} — Phipps Global hotel procurement" class="editorial-card-img" loading="lazy">
          </div>
          <div class="editorial-card-content">
            <h3>{p['title']}</h3>
            <div class="editorial-card-meta">
              {loc_span}
              <span class="editorial-badge">Hotels</span>
            </div>
          </div>
        </a>
        """

    gallery_section = f"""
    <section class="section" style="background:var(--bg-light);padding-top:64px;" aria-label="Hotels portfolio gallery">
      <div class="container">
        <div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:48px;flex-wrap:wrap;gap:16px;">
          <div>
            <span class="eyebrow" style="color:var(--text-secondary);">Our Work</span>
            <h2 class="reveal" style="margin:8px 0 0;font-size:clamp(24px,3.5vw,38px);">Hospitality <span class="accent">Projects</span> <span style="font-size:16px;font-weight:400;color:var(--text-secondary);margin-left:12px;">({len(projects)} projects)</span></h2>
          </div>
          <a href="get-in-touch.html" class="btn btn-dark btn-pill btn-sm reveal">Request Proposal &#8594;</a>
        </div>
        <div class="editorial-grid">{cards_html}</div>
      </div>
    </section>
    """
    content.append(BeautifulSoup(gallery_section, 'html.parser'))

    # ── CTA ──────────────────────────────────────────────────────────────────
    cta_html = """
    <section class="section-sm" aria-label="Contact call to action">
      <div class="cta-section">
        <span class="eyebrow reveal" style="color:var(--accent);">Partner With Us</span>
        <h2 class="reveal d1" style="color:#fff;">
          Sourcing Materials for<br><span class="accent">Your Next Hotel?</span>
        </h2>
        <p class="reveal d2" style="color:rgba(255,255,255,.72);max-width:520px;margin:0 auto 32px;">
          From tile and stone to FF&amp;E and glass — we deliver factory-direct on time and on budget.
          Let's discuss your project requirements.
        </p>
        <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;" class="reveal d3">
          <a href="get-in-touch.html" class="btn btn-accent btn-pill btn-lg btn-arrow">Get in Touch</a>
          <a href="images/PHIPPS-GLOBAL-PRESENTATION-2026.pdf" target="_blank" rel="noopener"
             class="btn btn-outline btn-pill btn-lg" style="color:#fff;border-color:rgba(255,255,255,.35);">
            View Presentation
          </a>
        </div>
      </div>
    </section>
    """
    content.append(BeautifulSoup(cta_html, 'html.parser'))

    with open(os.path.join(BASE_DIR, 'hotels.html'), 'w') as f:
        f.write(str(soup))
    print(f"Built hotels.html with {len(projects)} projects.")


# ─── RESIDENTIAL PAGE ─────────────────────────────────────────────────────────
def build_residential():
    projects = get_all_projects('residential')
    soup = get_base_soup()

    title_str = 'Luxury Residential Procurement | Phipps Global'
    desc_str = ('Phipps Global delivers factory-direct procurement for New York and Chicago\'s most prestigious '
                'luxury residential towers — stone, tile, flooring, FF&E and more.')

    soup.find('title').string = title_str
    soup.find('meta', attrs={'name': 'description'})['content'] = desc_str

    content = soup.find(id='page-content')

    # ── Hero ─────────────────────────────────────────────────────────────────
    hero_html = f"""
    <header class="loc-hero" style="min-height:72vh;" aria-label="Residential portfolio hero">
      <img src="images/modern-glass-buildings-e1733913526693.jpg"
           alt="Luxury residential tower — Phipps Global procurement" class="loc-hero-bg" fetchpriority="high">
      <div class="loc-hero-overlay"></div>
      <div class="container" style="position:relative;z-index:3;padding-bottom:72px;">
        <nav aria-label="Breadcrumb" class="breadcrumb" style="margin-bottom:20px;">
          <a href="index.html" style="color:rgba(255,255,255,.65);">Home</a>
          <span style="color:rgba(255,255,255,.35);margin:0 8px;">/</span>
          <span style="color:#fff;">Residential</span>
        </nav>
        <span class="eyebrow reveal" style="color:#dcb974; letter-spacing:0.1em; font-weight:600;">Luxury Residential</span>
        <h1 class="reveal d1" style="color:#fff;font-size:clamp(36px,5.5vw,68px);margin:12px 0 20px;font-weight:700;line-height:1.1;">
          Residential<br><span style="color:#dcb974;">Procurement Portfolio</span>
        </h1>
        <p class="lead reveal d2"
           style="max-width:560px;color:rgba(255,255,255,.78);font-size:18px;line-height:1.6;margin-bottom:32px;">
          From Hudson Yards to One Bennett Park — premium materials sourced factory-direct for 
          New York and Chicago's most iconic luxury residences. {len(projects)} projects completed.
        </p>
        <div class="reveal d3" style="display:flex;gap:16px;flex-wrap:wrap;">
          <a href="get-in-touch.html" class="btn btn-accent btn-pill btn-arrow">Start Your Project</a>
          <a href="projects.html" class="btn btn-outline btn-pill" style="color:#fff;border-color:rgba(255,255,255,.4);">All Projects</a>
        </div>
      </div>
    </header>
    """
    content.append(BeautifulSoup(hero_html, 'html.parser'))

    # ── Stats Strip ──────────────────────────────────────────────────────────
    stats_html = f"""
    <div style="background:var(--bg-dark);border-top:1px solid rgba(255,255,255,.07);border-bottom:1px solid rgba(255,255,255,.07);">
      <div class="container">
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0;padding:0;">
          <div style="padding:28px 24px;border-right:1px solid rgba(255,255,255,.07);text-align:center;">
            <div style="font-size:36px;font-weight:700;color:var(--accent);">{len(projects)}+</div>
            <div style="font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.5);margin-top:4px;">Residential Projects</div>
          </div>
          <div style="padding:28px 24px;border-right:1px solid rgba(255,255,255,.07);text-align:center;">
            <div style="font-size:36px;font-weight:700;color:var(--accent);">NYC</div>
            <div style="font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.5);margin-top:4px;">Primary Market</div>
          </div>
          <div style="padding:28px 24px;border-right:1px solid rgba(255,255,255,.07);text-align:center;">
            <div style="font-size:36px;font-weight:700;color:var(--accent);">100%</div>
            <div style="font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.5);margin-top:4px;">Factory Direct</div>
          </div>
          <div style="padding:28px 24px;text-align:center;">
            <div style="font-size:36px;font-weight:700;color:var(--accent);">Premium</div>
            <div style="font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.5);margin-top:4px;">Grade Materials</div>
          </div>
        </div>
      </div>
    </div>
    """
    content.append(BeautifulSoup(stats_html, 'html.parser'))

    # ── Gallery Grid ─────────────────────────────────────────────────────────
    # Build full gallery section as one block
    cards_html = ''
    delays = ['', 'd1', 'd2']
    for i, p in enumerate(projects):
        d = delays[i % 3]
        loc_span = f"<span>{p['location']}</span>" if p['location'] else '<span>Various</span>'
        cards_html += f"""
        <a href="{p['href']}" class="editorial-card reveal {d}" aria-label="View {p['title']} project">
          <div class="editorial-card-img-wrapper">
            <img src="{p['img']}" alt="{p['title']} — Phipps Global residential procurement" class="editorial-card-img" loading="lazy">
          </div>
          <div class="editorial-card-content">
            <h3>{p['title']}</h3>
            <div class="editorial-card-meta">
              {loc_span}
              <span class="editorial-badge">Residential</span>
            </div>
          </div>
        </a>
        """

    gallery_section = f"""
    <section class="section" style="background:var(--bg-light);padding-top:64px;" aria-label="Residential portfolio gallery">
      <div class="container">
        <div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:48px;flex-wrap:wrap;gap:16px;">
          <div>
            <span class="eyebrow" style="color:var(--text-secondary);">Our Work</span>
            <h2 class="reveal" style="margin:8px 0 0;font-size:clamp(24px,3.5vw,38px);">Residential <span class="accent">Projects</span> <span style="font-size:16px;font-weight:400;color:var(--text-secondary);margin-left:12px;">({len(projects)} properties)</span></h2>
          </div>
          <a href="get-in-touch.html" class="btn btn-dark btn-pill btn-sm reveal">Request Proposal &#8594;</a>
        </div>
        <div class="editorial-grid">{cards_html}</div>
      </div>
    </section>
    """
    content.append(BeautifulSoup(gallery_section, 'html.parser'))

    # ── CTA ──────────────────────────────────────────────────────────────────
    cta_html = """
    <section class="section-sm" aria-label="Contact call to action">
      <div class="cta-section">
        <span class="eyebrow reveal" style="color:var(--accent);">Partner With Us</span>
        <h2 class="reveal d1" style="color:#fff;">
          Sourcing Materials for<br><span class="accent">Your Residential Development?</span>
        </h2>
        <p class="reveal d2" style="color:rgba(255,255,255,.72);max-width:520px;margin:0 auto 32px;">
          Premium stone, tile, flooring and FF&amp;E delivered factory-direct for your luxury residential tower. 
          Let's discuss your project.
        </p>
        <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;" class="reveal d3">
          <a href="get-in-touch.html" class="btn btn-accent btn-pill btn-lg btn-arrow">Get in Touch</a>
          <a href="images/PHIPPS-GLOBAL-PRESENTATION-2026.pdf" target="_blank" rel="noopener"
             class="btn btn-outline btn-pill btn-lg" style="color:#fff;border-color:rgba(255,255,255,.35);">
            View Presentation
          </a>
        </div>
      </div>
    </section>
    """
    content.append(BeautifulSoup(cta_html, 'html.parser'))

    with open(os.path.join(BASE_DIR, 'residential.html'), 'w') as f:
        f.write(str(soup))
    print(f"Built residential.html with {len(projects)} projects.")


build_hotels()
build_residential()
print("Done!")
