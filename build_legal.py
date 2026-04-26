#!/usr/bin/env python3
"""Create Cookie Policy, Privacy Policy, Terms & Conditions, Terms of Use pages
and update the footer on every page to include them."""
import os, copy
from bs4 import BeautifulSoup

BASE_DIR = '/Volumes/Ext SSD/Phipps Global/New Site'

LEGAL_PAGES = [
    {
        "file": "cookie-policy.html",
        "title": "Cookie Policy",
        "subtitle": "How We Use Cookies",
        "sections": [
            ("What Are Cookies?", "Cookies are small text files placed on your device when you visit our website. They help us provide a better experience by remembering your preferences and understanding how you use our site."),
            ("How We Use Cookies", "We use cookies to: operate and improve our website, remember your preferences, analyze traffic and usage patterns, and deliver relevant content. We do not sell cookie data to third parties."),
            ("Types of Cookies We Use", "<strong>Essential Cookies</strong> — Required for the website to function. These cannot be disabled.<br><br><strong>Analytics Cookies</strong> — Help us understand how visitors interact with our site (e.g., Google Analytics).<br><br><strong>Preference Cookies</strong> — Remember your settings and choices to personalize your experience."),
            ("Third-Party Cookies", "Some pages may include content from third-party services (such as Google Maps or embedded forms) that may set their own cookies. We do not control these cookies."),
            ("Managing Cookies", "You can control cookies through your browser settings. Disabling certain cookies may affect the functionality of our website. Most browsers allow you to view, delete, and block cookies from specific websites."),
            ("Contact Us", "If you have questions about our use of cookies, please contact us at <a href='mailto:info@phippsglobal.com'>info@phippsglobal.com</a>."),
        ]
    },
    {
        "file": "privacy-policy.html",
        "title": "Privacy Policy",
        "subtitle": "Your Privacy Matters",
        "sections": [
            ("Information We Collect", "We may collect information you provide directly, such as your name, email address, phone number, and project details when you contact us through our website forms. We also collect non-personal data automatically, such as browser type, pages visited, and time spent on site."),
            ("How We Use Your Information", "We use your information to respond to inquiries, provide procurement services, improve our website, send relevant project updates (only if you have opted in), and comply with legal obligations. We do not sell your personal information."),
            ("Data Storage & Security", "Your information is stored securely and we take reasonable precautions to protect it from unauthorized access, disclosure, or loss. We use industry-standard encryption for data in transit."),
            ("Third-Party Services", "We may use trusted third-party tools (such as Google Analytics, contact form services) to operate our website. These providers have their own privacy policies and we encourage you to review them."),
            ("Your Rights", "You have the right to access, correct, or delete personal information we hold about you. To make a request, contact us at <a href='mailto:info@phippsglobal.com'>info@phippsglobal.com</a>."),
            ("Policy Updates", "We may update this Privacy Policy periodically. Changes will be posted on this page with an updated effective date. Continued use of our website constitutes acceptance of any changes."),
            ("Contact Us", "Phipps Global | 222 Lakeview Avenue, Suite 800, West Palm Beach, FL 33401 | <a href='mailto:info@phippsglobal.com'>info@phippsglobal.com</a>"),
        ]
    },
    {
        "file": "terms-conditions.html",
        "title": "Terms &amp; Conditions",
        "subtitle": "Rules Governing Use",
        "sections": [
            ("Acceptance of Terms", "By accessing and using the Phipps Global website, you accept and agree to be bound by these Terms and Conditions. If you do not agree, please discontinue use of our site immediately."),
            ("Use of Website", "This website is provided for informational purposes about Phipps Global's services. You may not use the site for any unlawful purpose or in a manner that could damage, disable, or impair its operation."),
            ("Intellectual Property", "All content on this website — including text, images, logos, and design — is the property of Phipps Global or its content suppliers and is protected by applicable copyright and intellectual property laws. No content may be reproduced without prior written permission."),
            ("Project Inquiries & Proposals", "Information submitted via our contact forms or email constitutes an inquiry only and does not form a binding contract. Formal agreements require a written contract signed by authorized representatives of both parties."),
            ("Limitation of Liability", "Phipps Global makes no warranties regarding the accuracy or completeness of information on this website. To the fullest extent permitted by law, we are not liable for any damages arising from your use of this website."),
            ("Governing Law", "These Terms and Conditions are governed by the laws of the State of Florida, United States. Any disputes will be resolved in the courts of Palm Beach County, Florida."),
            ("Changes to Terms", "We reserve the right to modify these Terms at any time. Continued use of the website after changes are posted constitutes your acceptance of the revised Terms."),
            ("Contact", "Questions? Reach us at <a href='mailto:info@phippsglobal.com'>info@phippsglobal.com</a> or call <a href='tel:+15614633390'>+1 (561) 463-3390</a>."),
        ]
    },
    {
        "file": "terms-of-use.html",
        "title": "Terms of Use",
        "subtitle": "Website Usage Guidelines",
        "sections": [
            ("Purpose of This Website", "The Phipps Global website is intended to provide information about our factory-direct procurement services and showcase our portfolio of completed projects. It is not a commercial storefront or e-commerce platform."),
            ("Acceptable Use", "You agree to use this website only for lawful purposes. You may not attempt to gain unauthorized access to any part of our site, transmit harmful code, or use automated tools to scrape content without permission."),
            ("Accuracy of Information", "While we strive to keep content current and accurate, Phipps Global does not warrant the completeness or timeliness of information on this site. Specifications, project details, and pricing are subject to change."),
            ("External Links", "Our website may contain links to third-party websites. Phipps Global is not responsible for the content or privacy practices of those sites. Links are provided for convenience only."),
            ("User-Submitted Content", "Any information or content you submit to us through contact forms or email becomes the property of Phipps Global and may be used to respond to your inquiry or improve our services. We will not publish your submissions without your consent."),
            ("Disclaimer", "This website and its content are provided 'as is' without warranties of any kind, either express or implied. Phipps Global disclaims all warranties to the fullest extent permitted by applicable law."),
            ("Contact", "For questions regarding use of this website, contact us at <a href='mailto:info@phippsglobal.com'>info@phippsglobal.com</a>."),
        ]
    },
]

# ── Build base soup ─────────────────────────────────────────────────────────
def get_base_soup():
    with open(os.path.join(BASE_DIR, 'index.html'), 'r') as f:
        idx = BeautifulSoup(f.read(), 'html.parser')
    nav = idx.select_one('nav#navbar')
    mobile = idx.select_one('#mobileMenu')
    footer = idx.select_one('footer.site-footer')
    phone = idx.select_one('.floating-phone')
    scripts = idx.select('script')
    s = BeautifulSoup('<!DOCTYPE html><html lang="en"><head></head><body></body></html>', 'html.parser')
    for tag in ['<meta charset="UTF-8">', '<meta name="viewport" content="width=device-width,initial-scale=1.0">',
                '<meta name="description" content="">', '<title></title>',
                '<link rel="stylesheet" href="style.css?v=3.0">']:
        s.head.append(BeautifulSoup(tag, 'html.parser'))
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

# ── Generate legal page HTML ─────────────────────────────────────────────────
def build_legal_page(page):
    soup = get_base_soup()
    clean_title = page['title'].replace('&amp;', '&')
    soup.find('title').string = f"{clean_title} | Phipps Global"
    soup.find('meta', attrs={'name': 'description'})['content'] = (
        f"Phipps Global {clean_title} — read our policies regarding use of our website and services."
    )
    content = soup.find(id='page-content')

    # Hero
    hero = f"""
    <header style="background:var(--bg-dark);padding:calc(var(--nav-h) + 72px) 0 72px;">
      <div class="container" style="max-width:800px;">
        <nav aria-label="Breadcrumb" class="breadcrumb" style="margin-bottom:24px;">
          <a href="index.html" style="color:rgba(255,255,255,.5);">Home</a>
          <span style="color:rgba(255,255,255,.25);margin:0 8px;">/</span>
          <span style="color:rgba(255,255,255,.8);">{clean_title}</span>
        </nav>
        <span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;color:#dcb974;">{page['subtitle']}</span>
        <h1 style="color:#fff;font-size:clamp(32px,5vw,56px);font-weight:700;font-family:var(--font-alt);margin:12px 0 16px;line-height:1.1;">{page['title']}</h1>
        <p style="color:rgba(255,255,255,.55);font-size:14px;">Last updated: April 2025 &nbsp;·&nbsp; Phipps Global</p>
      </div>
    </header>
    """
    content.append(BeautifulSoup(hero, 'html.parser'))

    # Content sections
    sections_html = '<article style="background:#fff;"><div class="container" style="max-width:800px;padding:72px 24px;">'
    for i, (heading, body) in enumerate(page['sections']):
        sections_html += f"""
        <section style="margin-bottom:48px;{'padding-bottom:48px;border-bottom:1px solid var(--border);' if i < len(page['sections'])-1 else ''}">
          <h2 style="font-size:1.25rem;font-weight:700;color:var(--text);margin-bottom:16px;font-family:var(--font-main);">{heading}</h2>
          <p style="font-size:15px;line-height:1.8;color:var(--text-secondary);">{body}</p>
        </section>
        """
    sections_html += '</div></article>'
    content.append(BeautifulSoup(sections_html, 'html.parser'))

    # CTA strip
    cta = """
    <div style="background:var(--bg-light);border-top:1px solid var(--border);padding:48px 0;text-align:center;">
      <div class="container">
        <p style="color:var(--text-secondary);margin-bottom:16px;">Questions about our policies?</p>
        <a href="get-in-touch.html" class="btn btn-dark btn-pill">Contact Us &#8594;</a>
      </div>
    </div>
    """
    content.append(BeautifulSoup(cta, 'html.parser'))

    filepath = os.path.join(BASE_DIR, page['file'])
    with open(filepath, 'w') as f:
        f.write(str(soup))
    print(f"Built {page['file']}")

for page in LEGAL_PAGES:
    build_legal_page(page)

# ── Patch footer on every page ───────────────────────────────────────────────
LEGAL_LINKS_HTML = """
<div class="footer-legal-links" style="display:flex;gap:28px;flex-wrap:wrap;justify-content:center;padding:20px 0;border-top:1px solid rgba(255,255,255,.06);margin-top:4px;">
  <a href="cookie-policy.html" style="color:rgba(255,255,255,.35);font-size:12px;transition:color .2s;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='rgba(255,255,255,.35)'">Cookie Policy</a>
  <a href="privacy-policy.html" style="color:rgba(255,255,255,.35);font-size:12px;transition:color .2s;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='rgba(255,255,255,.35)'">Privacy Policy</a>
  <a href="terms-conditions.html" style="color:rgba(255,255,255,.35);font-size:12px;transition:color .2s;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='rgba(255,255,255,.35)'">Terms &amp; Conditions</a>
  <a href="terms-of-use.html" style="color:rgba(255,255,255,.35);font-size:12px;transition:color .2s;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='rgba(255,255,255,.35)'">Terms of Use</a>
</div>
"""

def patch_footer(soup):
    """Insert legal links row inside the footer, just before the closing tag."""
    footer = soup.select_one('footer.site-footer')
    if not footer:
        return False
    # Avoid double-patching
    if footer.select_one('.footer-legal-links'):
        return False
    footer.append(BeautifulSoup(LEGAL_LINKS_HTML, 'html.parser'))
    return True

all_html = [f for f in os.listdir(BASE_DIR) if f.endswith('.html')]
patched = 0
for fname in all_html:
    fp = os.path.join(BASE_DIR, fname)
    with open(fp, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    changed = patch_footer(soup)
    if changed:
        with open(fp, 'w') as f:
            f.write(str(soup))
        patched += 1

print(f"Footer patched on {patched} pages.")
print("Legal pages DONE.")
