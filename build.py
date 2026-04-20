#!/usr/bin/env python3
"""
Generate Phipps Global — All Project Sub-Pages (Livohaus Theme)
Run: python3 build.py
"""

import os

BASE = "/Volumes/Ext SSD/Phipps Global/New Site"

# ─── NAV HTML ─────────────────────────────────────────────────────────────────
def nav_html():
    return """
  <div class="loading-line"></div>
  <nav class="site-nav" id="navbar">
    <div class="container nav-inner">
      <a href="index.html" class="nav-logo"><img src="images/phipps-global-logo-03.svg" alt="Phipps Global"></a>
      <div class="nav-links">
        <div class="nav-item"><button>Our Firm <span class="nav-arrow">▾</span></button><div class="mega-menu"><div class="mega-menu-inner"><div class="mega-section"><div class="mega-title">About</div><a href="our-firm.html" class="mega-link"><div class="mega-link-text"><strong>Who We Are</strong><small>Our story &amp; philosophy</small></div><span class="mega-link-arrow">→</span></a><a href="get-in-touch.html" class="mega-link"><div class="mega-link-text"><strong>Get in Touch</strong><small>Start your project</small></div><span class="mega-link-arrow">→</span></a></div></div></div></div>
        <div class="nav-item"><button>Services <span class="nav-arrow">▾</span></button><div class="mega-menu wide"><div class="mega-menu-inner"><div class="mega-section"><div class="mega-title">Products</div><a href="services.html#tile" class="mega-link"><div class="mega-link-text"><strong>Tile &amp; Stone</strong></div><span class="mega-link-arrow">→</span></a><a href="services.html#flooring" class="mega-link"><div class="mega-link-text"><strong>Flooring</strong></div><span class="mega-link-arrow">→</span></a><a href="services.html#countertops" class="mega-link"><div class="mega-link-text"><strong>Countertops</strong></div><span class="mega-link-arrow">→</span></a></div><div class="mega-section"><div class="mega-title">Specialty</div><a href="services.html#furniture" class="mega-link"><div class="mega-link-text"><strong>Furniture &amp; FF&amp;E</strong></div><span class="mega-link-arrow">→</span></a><a href="services.html#millwork" class="mega-link"><div class="mega-link-text"><strong>Millwork</strong></div><span class="mega-link-arrow">→</span></a></div></div></div></div>
        <div class="nav-item"><button>Projects <span class="nav-arrow">▾</span></button><div class="mega-menu wide"><div class="mega-menu-inner"><div class="mega-section"><div class="mega-title">Portfolio</div><a href="projects.html" class="mega-link"><div class="mega-link-text"><strong>All Projects</strong></div><span class="mega-link-arrow">→</span></a><a href="hotels.html" class="mega-link"><div class="mega-link-text"><strong>Hotels</strong></div><span class="mega-link-arrow">→</span></a><a href="residential.html" class="mega-link"><div class="mega-link-text"><strong>Residential</strong></div><span class="mega-link-arrow">→</span></a></div><div class="mega-section"><div class="mega-title">Featured</div><a href="gurneys.html" class="mega-link"><img src="images/gurneys-01.webp" class="mega-link-icon" alt="Gurney's"><div class="mega-link-text"><strong>Gurney's</strong></div></a><a href="70-vestry-street.html" class="mega-link"><img src="images/70-vestry-street-001-e1733387902509.jpg" class="mega-link-icon" alt="70 Vestry"><div class="mega-link-text"><strong>70 Vestry Street</strong></div></a></div></div></div></div>
        <div class="nav-item"><a href="hotels.html">Hotels</a></div>
        <div class="nav-item"><a href="residential.html">Residential</a></div>
      </div>
      <div class="nav-cta"><a href="get-in-touch.html" class="btn btn-accent btn-pill btn-sm">Get in Touch</a></div>
      <div class="hamburger" id="burger"><span></span><span></span><span></span></div>
    </div>
  </nav>
  <div class="mobile-menu" id="mobileMenu">
    <a href="index.html" class="mobile-link">Home</a><a href="our-firm.html" class="mobile-link">Our Firm</a><a href="services.html" class="mobile-link">Services</a><a href="projects.html" class="mobile-link">Projects</a><a href="hotels.html" class="mobile-link">Hotels</a><a href="residential.html" class="mobile-link">Residential</a><a href="get-in-touch.html" class="mobile-link" style="color:var(--accent)">Get in Touch →</a>
  </div>
"""

# ─── FOOTER HTML ──────────────────────────────────────────────────────────────
def footer_html():
    return """
  <footer class="site-footer">
    <div class="footer-watermark">PHIPPS</div>
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand"><img src="images/phipps-global-cream-logo-01.svg" alt="Phipps Global"><p>Factory-direct manufacturing and procurement for hotels, multi-family residential, and commercial projects.</p><form class="newsletter-form" onsubmit="event.preventDefault();this.querySelector('input').value='';this.querySelector('button').textContent='✓';"><input type="email" placeholder="Your email address"><button type="submit">Subscribe</button></form></div>
        <div class="footer-col"><h4>Navigate</h4><a href="index.html">Home</a><a href="our-firm.html">Our Firm</a><a href="services.html">Services</a><a href="projects.html">All Projects</a><a href="get-in-touch.html">Get in Touch</a></div>
        <div class="footer-col"><h4>Portfolio</h4><a href="hotels.html">Hotels</a><a href="residential.html">Residential</a><a href="gurneys.html">Gurney's</a><a href="70-vestry-street.html">70 Vestry Street</a><a href="520-west-28th.html">520 West 28th</a></div>
        <div class="footer-col"><h4>Contact</h4><a href="mailto:info@phippsglobal.com">info@phippsglobal.com</a><a href="tel:+15614633390">(561) 463-3390</a><p style="font-size:13px;color:rgba(255,255,255,0.3);margin-top:12px;line-height:1.6;">222 Lakeview Avenue, Suite 800<br>West Palm Beach, FL 33401</p></div>
      </div>
      <div class="footer-bottom"><div class="footer-legal"><a href="#">Privacy Policy</a><a href="#">Terms &amp; Conditions</a></div><span>&copy; 2026 Phipps Global. All rights reserved.</span><span class="footer-back-top">Back to Top ↑</span></div>
    </div>
  </footer>
  <script src="script.js"></script>
"""

# ─── PROJECT PAGE TEMPLATE ────────────────────────────────────────────────────
def project_page(name, slug, location, sector, developer, architect, services, img, desc, related):
    dev_row = f'<div class="proj-meta-item"><div class="proj-meta-label">Developer</div><div class="proj-meta-value">{developer}</div></div>' if developer else ""
    arch_row = f'<div class="proj-meta-item"><div class="proj-meta-label">Architect</div><div class="proj-meta-value">{architect}</div></div>' if architect else ""
    svc_tags = "".join([f'<span class="tag">{s.strip()}</span> ' for s in services.split(",")]) if services else ""

    if desc:
        desc_html = f"<p>{desc}</p>"
    else:
        desc_html = f"<p>Phipps Global provided comprehensive factory-direct procurement services for {name}, delivering high-quality materials sourced from our network of 18+ countries.</p>"

    sector_link = "hotels" if sector == "Hotels" else "residential"

    related_html = ""
    if related:
        cards = ""
        for r in related[:3]:
            if r["slug"] == slug:
                continue
            cards += f'''
        <a href="{r['slug']}.html" class="portfolio-card reveal">
          <img src="images/{r['img']}" alt="{r['name']}" loading="lazy">
          <div class="portfolio-card-info"><h4>{r['name']}</h4><span>{r['type']}</span></div>
        </a>'''
        related_html = f'''
  <section class="section-sm" style="background:var(--bg-light);">
    <div class="container">
      <h3 style="margin-bottom:32px;" class="reveal">Related Projects</h3>
      <div class="portfolio-grid">{cards}
      </div>
    </div>
  </section>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Phipps Global provided factory-direct procurement for {name} in {location}. {services[:80] if services else 'Flooring, tile, stone and more.'}">
  <title>{name} | Phipps Global</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
{nav_html()}

  <!-- Project Hero -->
  <div class="proj-hero">
    <img src="images/{img}" alt="{name}" loading="eager">
  </div>

  <!-- Project Content -->
  <section class="section">
    <div class="container">
      <div class="proj-main">
        <div class="proj-sidebar">
          <div class="proj-meta-item">
            <div class="proj-meta-label">Location</div>
            <div class="proj-meta-value">{location}</div>
          </div>
          <div class="proj-meta-item">
            <div class="proj-meta-label">Sector</div>
            <div class="proj-meta-value">{sector}</div>
          </div>
          {dev_row}
          {arch_row}
          <div class="proj-meta-item">
            <div class="proj-meta-label">Services Provided</div>
            <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;">{svc_tags}</div>
          </div>
          <div style="margin-top:24px;">
            <a href="get-in-touch.html" class="btn btn-accent btn-pill" style="width:100%;justify-content:center;">Request Similar Services</a>
          </div>
        </div>
        <div class="proj-desc">
          <nav class="breadcrumb" aria-label="breadcrumb">
            <a href="index.html">Home</a><span>/</span><a href="{sector_link}.html">{sector}</a><span>/</span><span>{name}</span>
          </nav>
          <h2 class="reveal">{name}</h2>
          <div class="reveal d1">{desc_html}</div>
          <a href="get-in-touch.html" class="btn btn-dark btn-pill btn-arrow reveal d2" style="margin-top:32px;">Start Your Project</a>
        </div>
      </div>
    </div>
  </section>

  {related_html}

  <!-- CTA -->
  <section class="section-sm">
    <div class="cta-section">
      <span class="eyebrow" style="color:var(--accent);">Your Next Project</span>
      <h2>Ready to Get <span class="accent">Started</span>?</h2>
      <p>Let's discuss how Phipps Global can deliver factory-direct procurement for your project.</p>
      <a href="get-in-touch.html" class="btn btn-accent btn-pill btn-lg btn-arrow">Get in Touch</a>
    </div>
  </section>

{footer_html()}
</body>
</html>'''
    return html


# ─── PROJECT DATA ─────────────────────────────────────────────────────────────
HOTEL_RELATED = [
    {"name":"Gurney's","slug":"gurneys","img":"gurneys-01.webp","type":"Hotels"},
    {"name":"Hugo Hotel","slug":"hugo","img":"hugo-hotel-01.jpg","type":"Hotels"},
    {"name":"Hendrick's Hotel","slug":"hendricks","img":"hotel-hendricks-03.webp","type":"Hotels"},
]
RES_RELATED = [
    {"name":"70 Vestry Street","slug":"70-vestry-street","img":"70-vestry-street-001-e1733387902509.jpg","type":"Residential"},
    {"name":"520 West 28th St","slug":"520-west-28th","img":"520-west-28th-01-1.jpg","type":"Residential"},
    {"name":"35 Hudson Yard","slug":"35-hudson-yard","img":"35-hudson-yard-01.jpg","type":"Residential"},
]

PROJECTS = [
    # Hotels
    {"name":"Hugo Hotel","slug":"hugo","loc":"New York, NY (SoHo)","sector":"Hotels",
     "dev":"Fortuna Realty","arch":"Marcello Pozzi","img":"hugo-hotel-01.jpg",
     "svc":"Flooring, Vanities, Shower Enclosures, Stainless Steel Sinks, Bathroom Accessories",
     "desc":"Hugo embodies the contemporary luxury and bohemian chic that captivates visitors of trendy Lower Manhattan. Hotel Hugo pays tribute to the storied history of SoHo with Marcello Pozzi architecture, thoughtful amenities and modern Italian cuisine.",
     "related":HOTEL_RELATED},
    {"name":"Gurney's","slug":"gurneys","loc":"Montauk, NY","sector":"Hotels",
     "dev":"Metrovest","arch":"","img":"gurneys-01.webp",
     "svc":"Flooring, Stone, Tile, Countertops, Case Goods, Furniture, Millwork, Decorative Lighting, Outdoor Furniture",
     "desc":"Situated on Montauk's most pristine stretch of oceanfront real estate, Gurney's is a Hamptons icon and the only year-round resort in Montauk. Features 146 rooms, suites, and beachfront cottages with five unique dining venues and an acclaimed spa renowned for its healing treatments and ocean-fed seawater pool.",
     "related":HOTEL_RELATED},
    {"name":"Hendrick's Hotel","slug":"hendricks","loc":"New York, NY (Midtown)","sector":"Hotels",
     "dev":"Fortuna Realty","arch":"Marchello Pozzi","img":"hotel-hendricks-03.webp",
     "svc":"Bathroom Accessories, Plumbing Fixtures, Shower Enclosures, Vanities, Countertops, Reading Lights",
     "desc":"With stylish interiors designed by Marchello Pozzi, floor-to-ceiling mahogany and Italian millwork, and bathrooms fitted with premium Waterworks fixtures and frosted glass, Hotel Hendricks stands a world apart from other Midtown Manhattan hotels.",
     "related":HOTEL_RELATED},
    {"name":"Garden City Hotel","slug":"garden-city","loc":"Long Island, NY","sector":"Hotels",
     "dev":"","arch":"","img":"gardencityhotel-01.jpg",
     "svc":"Custom Flooring, Interior Finishes",
     "desc":"Located on Long Island New York, this world class luxury hotel dates back to 1874. A perfect blend between classic French design and modern comfort, just a short distance from New York City.",
     "related":HOTEL_RELATED},
    {"name":"Jekyll Island Club Resort","slug":"jekyll-island","loc":"Jekyll Island, GA","sector":"Hotels",
     "dev":"","arch":"","img":"jekyll-island-club-resort-01.jpg",
     "svc":"Custom Design, Manufacturing of Flooring",
     "desc":"The Jekyll Island Club Resort stands as a timeless symbol of luxury and sophistication, blending historic charm with modern-day elegance. Meticulously restored to celebrate its storied past while providing world-class amenities.",
     "related":HOTEL_RELATED},
    {"name":"Marriott Fullerton","slug":"marriott-fullerton","loc":"Fullerton, CA","sector":"Hotels",
     "dev":"HERE","arch":"","img":"marriott-fullerton-01.webp",
     "svc":"All Guestroom Furniture, Quartz Countertops, Jackpacks, LED Lights",
     "desc":"Phipps Global supplied all guestroom furniture, quartz countertops, jackpacks, and LED lights for this California Marriott property — delivered on time and within budget.",
     "related":HOTEL_RELATED},
    {"name":"Moxy Hotel","slug":"moxy","loc":"Downtown LA","sector":"Hotels",
     "dev":"","arch":"","img":"moxy-hotel-01.jpg",
     "svc":"Custom Design, Manufacturing of Flooring",
     "desc":"The Moxy Hotel redefines the hospitality experience with playful yet sophisticated design. Phipps Global provided custom-design flooring manufacturing for this vibrant urban property.",
     "related":HOTEL_RELATED},
    # Residential
    {"name":"70 Vestry Street","slug":"70-vestry-street","loc":"Tribeca, New York, NY","sector":"Residential",
     "dev":"Related Group","arch":"Robert A.M. Stern","img":"70-vestry-street-001-e1733387902509.jpg",
     "svc":"All Stones, Glass Mosaic, Shower Enclosure, Wood Flooring, Tiles",
     "desc":"70 Vestry is a thirteen-story residential building in Tribeca. Waterfront condominium homes with expansive Hudson River views. Designed by Robert A. M. Stern Architects, the classical limestone facade references the historic warehouses that once lined the Hudson riverfront.",
     "related":RES_RELATED},
    {"name":"520 West 28th Street — Zaha Hadid","slug":"520-west-28th","loc":"New York, NY","sector":"Residential",
     "dev":"Related Group","arch":"Zaha Hadid","img":"520-west-28th-01-1.jpg",
     "svc":"Custom Design, Manufacturing of Flooring",
     "desc":"39 unique loft-like residences designed by Pritzker Prize-winning architect Zaha Hadid with stunning views of Manhattan's High Line park. Soaring ceilings, private elevator entries, a 75-foot pool, spa suite, and state-of-the-art fitness center.",
     "related":RES_RELATED},
    {"name":"15 Hudson Yard","slug":"15-hudson-yard","loc":"New York, NY","sector":"Residential",
     "dev":"Related Group","arch":"Diller Scofidio + Renfro","img":"15-hudson-yard-01.jpg",
     "svc":"Custom Design, Manufacturing of Flooring",
     "desc":"Standing 88 stories tall, 15 Hudson Yards features distinctive design, custom interiors, and premier resident amenities — one of New York's most coveted addresses.",
     "related":RES_RELATED},
    {"name":"35 Hudson Yard","slug":"35-hudson-yard","loc":"New York, NY","sector":"Residential",
     "dev":"Related Group","arch":"Kohn Pedersen Fox","img":"35-hudson-yard-01.jpg",
     "svc":"Custom Design, Manufacturing of Flooring",
     "desc":"Rising 1,000 feet above Manhattan, this architectural marvel seamlessly blends residential, commercial, and wellness spaces with over 1 million square feet of meticulously crafted interiors.",
     "related":RES_RELATED},
    {"name":"520 West 30th Street","slug":"520-west-30th","loc":"New York, NY","sector":"Residential",
     "dev":"Related Group","arch":"Ismael Leyva","img":"520-west-30th-street-hudson-yard-06.jpg",
     "svc":"Custom Design, Manufacturing of Flooring",
     "desc":"The residences at 520 West 30th represent a vision for modern living in the Hudson Yards district, with generous loft-like spaces individually crafted with nuanced design.",
     "related":RES_RELATED},
    {"name":"Nomad 30 E 31","slug":"nomad-30-e-31","loc":"New York, NY","sector":"Residential",
     "dev":"Ekstein Development","arch":"","img":"nomad-30-e-31-01.jpg",
     "svc":"All Stones, Countertops, Tiles, Slabs, Medicine Cabinet",
     "desc":"Floor-to-ceiling windows with beautiful views of the Empire State Building and Madison Square Park. Rich finishes, 7-inch-wide plank European oak flooring, custom hardware, and architectural millwork throughout.",
     "related":RES_RELATED},
    {"name":"35 XV","slug":"35-xv","loc":"New York, NY","sector":"Residential",
     "dev":"Alchemy Properties","arch":"FXFowle","img":"35-xv-001.jpg",
     "svc":"Flooring, Stone, Marble, Countertops, Mosaics, Tub Decks, Vanities, Millwork",
     "desc":"Incomparable panoramic views with clean contemporary design complementing sleek geometric architecture. Winner of the 2015 Gold Award of Excellence by the Society of American Registered Architects.",
     "related":RES_RELATED},
    {"name":"One Bennett Park","slug":"one-bennett-park","loc":"Chicago, IL","sector":"Residential",
     "dev":"","arch":"Robert A.M. Stern","img":"one-bennett-park-01.jpg",
     "svc":"Custom Design, Manufacturing of Flooring",
     "desc":"An architectural masterpiece in Chicago's skyline designed by Robert A.M. Stern Architects. Classic elegance meets contemporary living with expansive Lake Michigan views and world-class amenities.",
     "related":RES_RELATED},
    {"name":"182 West 82nd Street","slug":"182-west-82nd","loc":"New York, NY","sector":"Residential",
     "dev":"Naftali Group","arch":"","img":"182-west-82nd-street-04-scaled-e1733393058913.jpg",
     "svc":"Medicine Cabinets, Vanities",
     "desc":"Eleven bespoke apartments redesigned into loft-like residences. A perfect marriage between pre-war charm and the epitome of modern construction, steps from the city's finest restaurants and cultural institutions.",
     "related":RES_RELATED},
    {"name":"175 Kent Avenue","slug":"175-kent-avenue","loc":"Williamsburg, NY","sector":"Residential",
     "dev":"The Chetrit Group","arch":"","img":"175-kent-avenue-01.jpg",
     "svc":"Shower Enclosures, Bathroom Accessories",
     "desc":"175 Kent Avenue in Brooklyn offers luxury and amenities found in a Manhattan high-rise at a fraction of the cost, with oversized windows and immaculate waterfront views.",
     "related":RES_RELATED},
    {"name":"32 Custom House","slug":"32-custom-house","loc":"Providence, RI","sector":"Residential",
     "dev":"ASH NYC","arch":"","img":"32-custom-house-01.jpg",
     "svc":"Stone, Countertops, Kitchen Cabinets, Medicine Cabinets, Vanities, Sinks, Bathroom Accessories",
     "desc":"Built in 1875, this landmark in the Custom House District offers the perfect blend of contemporary styling and modern accessories. Located in the heart of downtown Providence.",
     "related":RES_RELATED},
    {"name":"Flats Chicago","slug":"flats-chicago","loc":"Chicago, IL","sector":"Residential",
     "dev":"Method Construction","arch":"","img":"flats-chicago-01-e1733460174376.jpg",
     "svc":"Stone, Tile, Flooring, Architectural Sinks",
     "desc":"A community of micro dwelling units across the suburbs of Chicago. A multi-location project spanning 6 locations with consistent, high-quality materials and finishes throughout.",
     "related":RES_RELATED},
    {"name":"Hudson Yards","slug":"hudson-yards","loc":"New York, NY","sector":"Residential",
     "dev":"Related Group","arch":"Diller Scofidio + Renfro","img":"hudson-yards-01.jpg",
     "svc":"All Stones, Countertops, Tiles, Slabs, Glass Mosaic, Wood Flooring",
     "desc":"Residences surpassing the expectations of the most discerning buyers. 10-foot ceilings, Miele appliances, bespoke finishes and unparalleled views. Amenities include an 82-foot lap pool, bowling alley, basketball court, and penthouse terrace.",
     "related":RES_RELATED},
]

# ─── GENERATE ─────────────────────────────────────────────────────────────────
for p in PROJECTS:
    html = project_page(
        name=p["name"], slug=p["slug"], location=p["loc"],
        sector=p["sector"], developer=p["dev"], architect=p["arch"],
        services=p["svc"], img=p["img"], desc=p["desc"],
        related=p["related"]
    )
    path = os.path.join(BASE, f'{p["slug"]}.html')
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ {p['slug']}.html")

print(f"\n✅ Generated {len(PROJECTS)} project pages")
