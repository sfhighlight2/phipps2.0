#!/usr/bin/env python3
"""
Fixes:
1. Remove duplicate .footer-legal-links; update .footer-legal links to real pages + add Terms of Use
2. Add "Presentation" link to footer under Get in Touch column
3. Our Firm hero accent span → white
4. Fix all presentation button hrefs to PHIPPS-GLOBAL-PRESENTATION-2026.pdf
5. Fix Our Firm nav link everywhere
6. Hero h1 font-weight 700 → 400 on hotels/residential/projects hero text
"""
import os, copy, re
from bs4 import BeautifulSoup

BASE_DIR = '/Volumes/Ext SSD/Phipps Global/New Site'

all_html = [f for f in os.listdir(BASE_DIR) if f.endswith('.html')]

PDF_PATH = 'PHIPPS-GLOBAL-PRESENTATION-2026.pdf'

def fix_file(fname):
    fp = os.path.join(BASE_DIR, fname)
    with open(fp, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    changed = False

    # ── 1. Remove .footer-legal-links (the duplicate row we added) ──────────
    for el in soup.select('.footer-legal-links'):
        el.decompose()
        changed = True

    # ── 2. Update .footer-legal anchors to real pages & add Terms of Use ────
    fl = soup.select_one('.footer-legal')
    if fl:
        # Build correct links
        new_fl = BeautifulSoup("""
<div class="footer-legal">
  <a href="privacy-policy.html">Privacy Policy</a>
  <a href="terms-conditions.html">Terms &amp; Conditions</a>
  <a href="cookie-policy.html">Cookie Policy</a>
  <a href="terms-of-use.html">Terms of Use</a>
</div>""", 'html.parser')
        fl.replace_with(new_fl)
        changed = True

    # ── 3. Add "Presentation" link to footer Get in Touch column ────────────
    footer = soup.select_one('footer.site-footer')
    if footer:
        # Find the footer col that contains Get in Touch link
        for col in footer.select('.footer-col'):
            h4 = col.select_one('h4')
            if h4 and 'touch' in h4.get_text().lower():
                # Check if Presentation link already added
                existing = [a.get_text() for a in col.select('a')]
                if 'Presentation' not in existing:
                    pres_tag = BeautifulSoup(
                        f'<a href="{PDF_PATH}" target="_blank" rel="noopener">Presentation</a>',
                        'html.parser'
                    )
                    col.append(pres_tag)
                    changed = True
                break

    # ── 4. Fix all presentation button hrefs ────────────────────────────────
    for a in soup.select('a'):
        href = a.get('href', '')
        if 'PHIPPS-GLOBAL-PRESENTATION' in href or 'presentation' in a.get_text().lower() and 'pdf' in href.lower():
            a['href'] = PDF_PATH
            changed = True

    # Also fix inline "View Full Presentation" links
    for a in soup.select('a'):
        txt = a.get_text(strip=True).lower()
        if 'presentation' in txt and a.get('href', '').startswith('images/'):
            a['href'] = PDF_PATH
            changed = True

    # ── 5. Fix Our Firm nav links (already done via propagation but ensure) ─
    for a in soup.select('a'):
        if a.get_text(strip=True) == 'Our Firm' and a.get('href') in ('#', '', None):
            a['href'] = 'our-firm.html'
            changed = True

    # ── 6. Fix Our Firm hero accent span → white ────────────────────────────
    if fname == 'our-firm.html':
        for span in soup.select('span.accent'):
            s = span.get('style', '')
            span['style'] = s.replace('color:var(--accent)', 'color:#ffffff').replace('color:var(--accent);', 'color:#ffffff;')
            # If no inline style, add one
            if 'color' not in span.get('style', ''):
                span['style'] = (span.get('style','') + ';color:#ffffff;').lstrip(';')
            changed = True
        # Also fix eyebrow that says "About Us" (dark navy on dark bg → gold)
        for span in soup.select('.eyebrow'):
            parent_hero = span.find_parent(style=True)
            s = span.get('style', '')
            if 'color:var(--accent)' in s:
                span['style'] = s.replace('color:var(--accent)', 'color:#dcb974')
                changed = True
        # Fix stats numbers on dark bg (18+, 50+, 100%)
        for div in soup.find_all('div', style=True):
            s = div.get('style', '')
            if 'color:var(--accent)' in s and 'font-size:48px' in s:
                div['style'] = s.replace('color:var(--accent)', 'color:#dcb974')
                changed = True

    # ── 7. Hero h1 font-weight fix (700 → 400 for gallery page heroes) ──────
    if fname in ('hotels.html', 'residential.html', 'projects.html', 'services.html'):
        hero = soup.select_one('.loc-hero')
        if hero:
            h1 = hero.select_one('h1')
            if h1:
                s = h1.get('style', '')
                h1['style'] = s.replace('font-weight:700', 'font-weight:400')
                changed = True
            # Also fix the subtitle span inside h1 (gold text second line)
            for span in hero.select('h1 span'):
                s = span.get('style', '')
                if 'font-weight' not in s:
                    span['style'] = s + ';font-weight:400;'
                changed = True

    if changed:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(str(soup))
    return changed

fixed = 0
for fname in all_html:
    if fix_file(fname):
        fixed += 1

print(f"Fixed {fixed} files.")
print("Done.")
