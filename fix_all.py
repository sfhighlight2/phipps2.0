#!/usr/bin/env python3
"""Fix: hero overlap, stat contrast, CTA accent, font, projects layout, services redesign."""
import os, copy
from bs4 import BeautifulSoup

BASE_DIR = '/Volumes/Ext SSD/Phipps Global/New Site'

# ── 1. CSS FIXES ──────────────────────────────────────────────────────────────
CSS_PATH = os.path.join(BASE_DIR, 'style.css')
with open(CSS_PATH, 'r') as f:
    css = f.read()

# Fix: .cta-section h2 .accent should be white/gold not dark navy
css = css.replace(
    '.cta-section h2 .accent { color:var(--accent); }',
    '.cta-section h2 .accent { color:#dcb974; }'
)
# Fix: .loc-hero container needs top padding to clear nav
# The hero containers in hotels/res use inline style on .container — we fix via CSS
css += """
/* ── Hero padding fix (clears 80px fixed nav) ── */
.loc-hero > .container {
  position: relative;
  z-index: 3;
  padding-top: calc(var(--nav-h) + 60px);
}

/* ── Services grid ── */
.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2px;
}
.service-tile {
  position: relative;
  overflow: hidden;
  aspect-ratio: 4/5;
  display: block;
  background: var(--bg-dark);
}
.service-tile img {
  width: 100%; height: 100%;
  object-fit: cover;
  transition: transform 0.7s cubic-bezier(0.25,1,0.5,1);
  display: block;
}
.service-tile:hover img { transform: scale(1.08); }
.service-tile-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.1) 55%);
  display: flex; flex-direction: column; justify-content: flex-end;
  padding: 32px 28px;
  transition: background 0.4s;
}
.service-tile:hover .service-tile-overlay {
  background: linear-gradient(to top, rgba(0,34,58,0.95) 0%, rgba(0,34,58,0.4) 55%);
}
.service-tile-overlay h3 {
  color: #fff; font-size: 1.3rem; font-weight: 600;
  font-family: var(--font-alt); margin-bottom: 8px;
}
.service-tile-overlay p {
  color: rgba(255,255,255,0.7); font-size: 13px; line-height: 1.5;
  margin-bottom: 14px; max-height: 0; overflow: hidden;
  transition: max-height 0.4s ease;
}
.service-tile:hover .service-tile-overlay p { max-height: 80px; }
.service-tile-cta {
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.1em; color: #dcb974;
  display: flex; align-items: center; gap: 6px;
  opacity: 0; transform: translateY(6px);
  transition: all 0.3s 0.05s;
}
.service-tile:hover .service-tile-cta { opacity: 1; transform: none; }

@media(max-width:1024px) { .services-grid { grid-template-columns: repeat(2,1fr); } }
@media(max-width:640px)  { .services-grid { grid-template-columns: 1fr; } }
"""
with open(CSS_PATH, 'w') as f:
    f.write(css)
print("CSS fixed.")

# ── 2. REBUILD rebuild_hotels_res.py INLINE FIX ───────────────────────────────
# Instead of modifying the script, directly patch the two generated HTML files.

def fix_hero_stats_cta(filepath, label):
    with open(filepath, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Fix stats: replace dark navy accent color with gold
    for div in soup.find_all('div', style=True):
        s = div.get('style', '')
        if 'color:var(--accent)' in s and 'font-size:36px' in s:
            div['style'] = s.replace('color:var(--accent)', 'color:#dcb974')

    # Fix CTA eyebrow on dark bg
    for span in soup.find_all('span', class_='eyebrow'):
        parent = span.find_parent('div', class_='cta-section')
        if parent and 'color:var(--accent)' in span.get('style',''):
            span['style'] = span['style'].replace('color:var(--accent)', 'color:#dcb974')

    # Fix CTA h2 span.accent
    cta = soup.select_one('.cta-section')
    if cta:
        for span in cta.select('span.accent'):
            span['style'] = 'color:#ffffff;'

    # Fix hero container: add padding-top to clear nav (80px nav + 60px space)
    hero = soup.select_one('.loc-hero')
    if hero:
        container = hero.select_one('.container')
        if container:
            existing = container.get('style', '')
            if 'padding-top' not in existing:
                container['style'] = f"padding-top:calc(var(--nav-h) + 60px);{existing}"

    # Fix h1 font
    hero_h1 = soup.select_one('.loc-hero h1')
    if hero_h1:
        s = hero_h1.get('style','')
        if 'font-family' not in s:
            hero_h1['style'] = s + ';font-family:var(--font-alt);'

    with open(filepath, 'w') as f:
        f.write(str(soup))
    print(f"Fixed {label}")

fix_hero_stats_cta(os.path.join(BASE_DIR, 'hotels.html'), 'hotels.html')
fix_hero_stats_cta(os.path.join(BASE_DIR, 'residential.html'), 'residential.html')

# ── 3. REBUILD projects.html ──────────────────────────────────────────────────
def get_all_projects():
    exclude = [
        'index.html','hotels.html','residential.html','projects.html','our-firm.html',
        'services.html','get-in-touch.html','contact.html','hendricks.html',
        'artwork.html','bathroom-accessories.html','carpet-tiles.html','ffe.html',
        'glass.html','led-mirrors.html','lvt.html','plumbing-fixtures.html',
        'shower-enclosures.html','stone.html','tiles.html','wood-flooring.html',
    ]
    projects = []
    for f in sorted(os.listdir(BASE_DIR)):
        if not f.endswith('.html') or f in exclude: continue
        with open(os.path.join(BASE_DIR, f)) as fp:
            soup = BeautifulSoup(fp.read(), 'html.parser')
        h1 = soup.select_one('h1')
        title = h1.get_text(strip=True) if h1 else f.replace('.html','').replace('-',' ').title()
        hero_bg = soup.select_one('.loc-hero-bg')
        img_src = hero_bg['src'] if hero_bg and hero_bg.get('src') else None
        if not img_src or img_src == 'images/placeholder.jpg': continue
        if not os.path.exists(os.path.join(BASE_DIR, img_src)): continue
        eyebrow = soup.select_one('.eyebrow')
        cat = 'hotels' if eyebrow and 'hotel' in eyebrow.get_text().lower() else 'residential'
        stat_items = soup.select('.loc-stat-item')
        location = ''
        if stat_items:
            val = stat_items[0].select_one('.loc-stat-value')
            sub = stat_items[0].select_one('.loc-stat-sub')
            if val:
                location = val.get_text(strip=True)
                if sub and sub.get_text(strip=True):
                    location += ', ' + sub.get_text(strip=True)
        projects.append({'href': f, 'img': img_src, 'title': title, 'location': location, 'cat': cat})
    return projects

def get_base_soup():
    with open(os.path.join(BASE_DIR, 'index.html'), 'r') as f:
        idx = BeautifulSoup(f.read(), 'html.parser')
    nav = idx.select_one('nav#navbar')
    mobile = idx.select_one('#mobileMenu')
    footer = idx.select_one('footer.site-footer')
    phone = idx.select_one('.floating-phone')
    scripts = idx.select('script')
    s = BeautifulSoup('<!DOCTYPE html><html lang="en"><head></head><body></body></html>', 'html.parser')
    s.head.append(BeautifulSoup('<meta charset="UTF-8">', 'html.parser'))
    s.head.append(BeautifulSoup('<meta name="viewport" content="width=device-width,initial-scale=1.0">', 'html.parser'))
    s.head.append(BeautifulSoup('<meta name="description" content="">', 'html.parser'))
    s.head.append(BeautifulSoup('<title></title>', 'html.parser'))
    s.head.append(BeautifulSoup('<link rel="stylesheet" href="style.css?v=3.0">', 'html.parser'))
    s.body.append(BeautifulSoup('<div class="loading-line"></div>', 'html.parser'))
    if nav: s.body.append(copy.copy(nav))
    if mobile: s.body.append(copy.copy(mobile))
    main = s.new_tag('main', id='page-content')
    s.body.append(main)
    if footer: s.body.append(copy.copy(footer))
    for sc in scripts:
        if 'src' in sc.attrs and 'script.js' in sc['src']:
            s.body.append(copy.copy(sc))
    if phone: s.body.append(copy.copy(phone))
    return s

projects = get_all_projects()
soup = get_base_soup()
soup.find('title').string = 'All Projects | Phipps Global'
soup.find('meta', attrs={'name':'description'})['content'] = (
    'Browse 50+ completed hotel and residential procurement projects by Phipps Global — '
    'factory-direct sourcing for the world\'s finest properties.'
)

content = soup.find(id='page-content')

# Hero
hero_html = f"""
<header class="loc-hero" style="min-height:65vh;" aria-label="Projects hero">
  <img src="images/stone-staircase-with-stone-walls-and-greenery-against-the-blue-sky-e1733914424854.jpg"
       alt="Phipps Global Projects" class="loc-hero-bg" fetchpriority="high">
  <div class="loc-hero-overlay"></div>
  <div class="container" style="position:relative;z-index:3;padding-top:calc(var(--nav-h) + 60px);padding-bottom:72px;">
    <nav aria-label="Breadcrumb" class="breadcrumb" style="margin-bottom:20px;">
      <a href="index.html" style="color:rgba(255,255,255,.65);">Home</a>
      <span style="color:rgba(255,255,255,.35);margin:0 8px;">/</span>
      <span style="color:#fff;">Projects</span>
    </nav>
    <span class="eyebrow reveal" style="color:#dcb974;letter-spacing:0.1em;font-weight:600;">Our Portfolio</span>
    <h1 class="reveal d1" style="color:#fff;font-size:clamp(36px,5.5vw,68px);margin:12px 0 20px;font-weight:700;line-height:1.1;font-family:var(--font-alt);">
      {len(projects)} Completed<br><span style="color:#dcb974;">Procurement Projects</span>
    </h1>
    <p class="lead reveal d2" style="max-width:540px;color:rgba(255,255,255,.78);font-size:18px;line-height:1.6;margin-bottom:32px;">
      Hotels, luxury residences and commercial developments — all delivered factory-direct on time and on budget.
    </p>
    <div class="reveal d3" style="display:flex;gap:16px;flex-wrap:wrap;">
      <a href="hotels.html" class="btn btn-accent btn-pill">Hotels Portfolio</a>
      <a href="residential.html" class="btn btn-outline btn-pill" style="color:#fff;border-color:rgba(255,255,255,.4);">Residential Portfolio</a>
    </div>
  </div>
</header>
"""
content.append(BeautifulSoup(hero_html, 'html.parser'))

# Filter bar
filter_html = """
<div style="background:#fff;border-bottom:1px solid var(--border);position:sticky;top:80px;z-index:50;">
  <div class="container">
    <div class="filter-bar" style="padding:16px 0;">
      <button class="filter-btn active" data-filter="all">All Projects</button>
      <button class="filter-btn" data-filter="hotels">Hotels</button>
      <button class="filter-btn" data-filter="residential">Residential</button>
    </div>
  </div>
</div>
"""
content.append(BeautifulSoup(filter_html, 'html.parser'))

# Gallery — editorial grid
cards_html = ''
for i, p in enumerate(projects):
    d = ['','d1','d2'][i % 3]
    loc_span = f"<span>{p['location']}</span>" if p['location'] else '<span>&nbsp;</span>'
    cards_html += f"""
    <a href="{p['href']}" class="editorial-card reveal {d}" data-cat="{p['cat']}"
       aria-label="View {p['title']} project">
      <div class="editorial-card-img-wrapper">
        <img src="{p['img']}" alt="{p['title']}" class="editorial-card-img" loading="lazy">
      </div>
      <div class="editorial-card-content">
        <h3>{p['title']}</h3>
        <div class="editorial-card-meta">
          {loc_span}
          <span class="editorial-badge">{'Hotels' if p['cat']=='hotels' else 'Residential'}</span>
        </div>
      </div>
    </a>
    """

gallery_html = f"""
<section class="section" style="background:var(--bg-light);padding-top:64px;">
  <div class="container">
    <div class="editorial-grid" id="proj-grid">{cards_html}</div>
  </div>
</section>
"""
content.append(BeautifulSoup(gallery_html, 'html.parser'))

# CTA
cta_html = """
<section class="section-sm">
  <div class="cta-section">
    <span class="eyebrow reveal" style="color:#dcb974;">Start Today</span>
    <h2 class="reveal d1" style="color:#fff;">Ready to Start Your <span style="color:#dcb974;">Next Project?</span></h2>
    <p class="reveal d2" style="color:rgba(255,255,255,.72);max-width:500px;margin:0 auto 32px;">
      Let's discuss how Phipps Global can deliver factory-direct procurement for your development.
    </p>
    <a href="get-in-touch.html" class="btn btn-accent btn-pill btn-lg btn-arrow reveal d3">Get in Touch</a>
  </div>
</section>
"""
content.append(BeautifulSoup(cta_html, 'html.parser'))

with open(os.path.join(BASE_DIR, 'projects.html'), 'w') as f:
    f.write(str(soup))
print(f"Built projects.html with {len(projects)} items.")

# ── 4. REBUILD services.html ──────────────────────────────────────────────────
services_data = [
    {"name": "Tile & Stone",         "desc": "Thin tile, pavers, sintered stone, large-format porcelain, ceramic, glass, terrazzo and mosaic — manufactured to spec.", "img": "images/3d-rendering-modern-tile-living-room-and-dining-room-e1733914643525.jpg", "link": "tiles.html"},
    {"name": "Wood Flooring",         "desc": "Solid wood, engineered hardwood, and custom flooring for residential and hospitality applications worldwide.", "img": "images/living-room-with-wood-flooring-e1733914178998.jpg", "link": "wood-flooring.html"},
    {"name": "Luxury Vinyl Tile",     "desc": "High-traffic LVT crafted for commercial durability and stunning visual appeal — perfect for hotels and multifamily.", "img": "images/hand-installing-vinyl-flooring-e1733914084283.jpg", "link": "lvt.html"},
    {"name": "Shower Enclosures",     "desc": "Custom glass shower enclosures and designer bathtubs engineered to elevate any hospitality or residential bathroom.", "img": "images/luxurious-modern-bathroom-with-marble-walls-and-glass-shower--e1733913328449.jpg", "link": "shower-enclosures.html"},
    {"name": "FF&E",                  "desc": "Multifunctional furniture, fixtures and equipment designed and manufactured to your exact project specifications.", "img": "images/poland-warsaw-seating-furniture-at-lounge-of-hotel-e1733913658549.jpg", "link": "ffe.html"},
    {"name": "Bathroom Accessories",  "desc": "Medicine cabinets, vanities, sinks, faucets and comprehensive plumbing fixtures — sourced factory-direct.", "img": "images/washbasin-in-a-modern-bathroom-with-ornamental-plants-and-bathroom-accessories-.jpg", "link": "bathroom-accessories.html"},
    {"name": "LED Mirrors",           "desc": "Custom LED mirrors providing flawless illumination and modern aesthetics for hotel guestrooms and residences.", "img": "images/modern-sink-and-round-mirror-with-led-light-in-a-luxury-bathroom-e1734150333658.jpg", "link": "led-mirrors.html"},
    {"name": "Glass",                 "desc": "Architectural glass panels, partitions, facades and specialty glass sourced from our global manufacturing network.", "img": "images/modern-glass-buildings-e1733913526693.jpg", "link": "glass.html"},
    {"name": "Artwork",               "desc": "Curated and custom-manufactured artwork to complete your interior design narrative for any space.", "img": "images/blank-frame-mockup-for-artwork-or-print-on-green-wall-background--e1734085709229.jpg", "link": "artwork.html"},
    {"name": "Carpet Tiles",          "desc": "Commercial-grade carpet tiles in hundreds of patterns and textures — designed for hospitality performance.", "img": "images/rich-pattern-carpet-e1734091765677.jpg", "link": "carpet-tiles.html"},
    {"name": "Plumbing Fixtures",     "desc": "Designer plumbing fixtures and fittings sourced from world-class factories across Europe and Asia.", "img": "images/sink-drainage-pipe-and-plumbing-e1734154798147.jpg", "link": "plumbing-fixtures.html"},
    {"name": "Stone & Countertops",   "desc": "Granite, marble, quartz, solid surface and porcelain slab manufactured to exact project specifications.", "img": "images/stone-staircase-with-stone-walls-and-greenery-against-the-blue-sky-e1733914424854.jpg", "link": "stone.html"},
]

soup2 = get_base_soup()
soup2.find('title').string = 'Services | Phipps Global'
soup2.find('meta', attrs={'name':'description'})['content'] = (
    'Phipps Global services — tile, stone, wood flooring, LVT, shower enclosures, FF&E, LED mirrors, '
    'bathroom accessories and more. All sourced factory-direct from 18+ countries.'
)

c2 = soup2.find(id='page-content')

svc_hero = f"""
<header class="loc-hero" style="min-height:65vh;" aria-label="Services hero">
  <img src="images/interior-setting-e1733914733183.jpg" alt="Phipps Global Services"
       class="loc-hero-bg" fetchpriority="high">
  <div class="loc-hero-overlay"></div>
  <div class="container" style="position:relative;z-index:3;padding-top:calc(var(--nav-h) + 60px);padding-bottom:72px;">
    <nav aria-label="Breadcrumb" class="breadcrumb" style="margin-bottom:20px;">
      <a href="index.html" style="color:rgba(255,255,255,.65);">Home</a>
      <span style="color:rgba(255,255,255,.35);margin:0 8px;">/</span>
      <span style="color:#fff;">Services</span>
    </nav>
    <span class="eyebrow reveal" style="color:#dcb974;letter-spacing:0.1em;font-weight:600;">What We Do</span>
    <h1 class="reveal d1" style="color:#fff;font-size:clamp(36px,5.5vw,68px);margin:12px 0 20px;font-weight:700;line-height:1.1;font-family:var(--font-alt);">
      Factory-Direct<br><span style="color:#dcb974;">Material Sourcing</span>
    </h1>
    <p class="lead reveal d2" style="max-width:540px;color:rgba(255,255,255,.78);font-size:18px;line-height:1.6;margin-bottom:32px;">
      Comprehensive product categories — all sourced factory-direct from our global network of manufacturers across 18+ countries.
    </p>
    <a href="get-in-touch.html" class="btn btn-accent btn-pill btn-arrow reveal d3">Request a Quote</a>
  </div>
</header>
"""
c2.append(BeautifulSoup(svc_hero, 'html.parser'))

# Stats strip
stats = """
<div style="background:var(--bg-dark);border-bottom:1px solid rgba(255,255,255,.07);">
  <div class="container">
    <div style="display:grid;grid-template-columns:repeat(4,1fr);">
      <div style="padding:28px 24px;border-right:1px solid rgba(255,255,255,.07);text-align:center;">
        <div style="font-size:32px;font-weight:700;color:#dcb974;">12</div>
        <div style="font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.5);margin-top:4px;">Product Categories</div>
      </div>
      <div style="padding:28px 24px;border-right:1px solid rgba(255,255,255,.07);text-align:center;">
        <div style="font-size:32px;font-weight:700;color:#dcb974;">18+</div>
        <div style="font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.5);margin-top:4px;">Countries Sourced</div>
      </div>
      <div style="padding:28px 24px;border-right:1px solid rgba(255,255,255,.07);text-align:center;">
        <div style="font-size:32px;font-weight:700;color:#dcb974;">100%</div>
        <div style="font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.5);margin-top:4px;">Factory Direct</div>
      </div>
      <div style="padding:28px 24px;text-align:center;">
        <div style="font-size:32px;font-weight:700;color:#dcb974;">50+</div>
        <div style="font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.5);margin-top:4px;">Projects Delivered</div>
      </div>
    </div>
  </div>
</div>
"""
c2.append(BeautifulSoup(stats, 'html.parser'))

# Services grid header
grid_header = f"""
<section style="background:var(--bg-light);padding:72px 0 48px;">
  <div class="container">
    <div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:48px;flex-wrap:wrap;gap:16px;">
      <div>
        <span class="eyebrow" style="color:var(--text-secondary);">Our Capabilities</span>
        <h2 class="reveal" style="margin:8px 0 0;font-size:clamp(24px,3.5vw,38px);">
          All <span class="accent">Services</span>
          <span style="font-size:16px;font-weight:400;color:var(--text-secondary);margin-left:12px;">({len(services_data)} categories)</span>
        </h2>
      </div>
      <a href="get-in-touch.html" class="btn btn-dark btn-pill btn-sm reveal">Request Proposal &#8594;</a>
    </div>
  </div>
</section>
"""
c2.append(BeautifulSoup(grid_header, 'html.parser'))

# Services tile grid
tiles_html = '<div class="services-grid" style="max-width:1400px;margin:0 auto;">'
for i, s in enumerate(services_data):
    tiles_html += f"""
    <a href="{s['link']}" class="service-tile" aria-label="{s['name']}">
      <img src="{s['img']}" alt="{s['name']} — Phipps Global" loading="{'eager' if i < 3 else 'lazy'}">
      <div class="service-tile-overlay">
        <h3>{s['name']}</h3>
        <p>{s['desc']}</p>
        <div class="service-tile-cta">Explore &#8594;</div>
      </div>
    </a>
    """
tiles_html += '</div>'
c2.append(BeautifulSoup(tiles_html, 'html.parser'))

# CTA
svc_cta = """
<section class="section-sm" style="margin-top:72px;">
  <div class="cta-section">
    <span class="eyebrow reveal" style="color:#dcb974;">Get Started</span>
    <h2 class="reveal d1" style="color:#fff;">Need Materials for <span style="color:#dcb974;">Your Project?</span></h2>
    <p class="reveal d2" style="color:rgba(255,255,255,.72);max-width:500px;margin:0 auto 32px;">
      Tell us what you need — we'll source it factory-direct from our global network and deliver on time.
    </p>
    <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;" class="reveal d3">
      <a href="get-in-touch.html" class="btn btn-accent btn-pill btn-lg btn-arrow">Request a Quote</a>
      <a href="projects.html" class="btn btn-outline btn-pill btn-lg" style="color:#fff;border-color:rgba(255,255,255,.35);">View Projects</a>
    </div>
  </div>
</section>
"""
c2.append(BeautifulSoup(svc_cta, 'html.parser'))

with open(os.path.join(BASE_DIR, 'services.html'), 'w') as f:
    f.write(str(soup2))
print(f"Built services.html with {len(services_data)} tiles.")

# ── 5. PROPAGATE NAV TO ALL PAGES ─────────────────────────────────────────────
with open(os.path.join(BASE_DIR, 'index.html'), 'r') as f:
    idx = BeautifulSoup(f.read(), 'html.parser')
new_nav = idx.select_one('nav#navbar')
new_mobile = idx.select_one('#mobileMenu')

updated = 0
for fname in os.listdir(BASE_DIR):
    if not fname.endswith('.html') or fname == 'index.html': continue
    fp = os.path.join(BASE_DIR, fname)
    with open(fp, 'r') as f:
        pg = BeautifulSoup(f.read(), 'html.parser')
    old_nav = pg.select_one('nav#navbar')
    old_mob = pg.select_one('#mobileMenu')
    if old_nav and new_nav: old_nav.replace_with(copy.copy(new_nav))
    if old_mob and new_mobile: old_mob.replace_with(copy.copy(new_mobile))
    with open(fp, 'w') as f:
        f.write(str(pg))
    updated += 1

print(f"Nav propagated to {updated} pages.")
print("ALL DONE.")
