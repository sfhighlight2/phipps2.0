#!/usr/bin/env python3
"""Add Presentation link to Contact footer col on all pages."""
import os, copy
from bs4 import BeautifulSoup

BASE_DIR = '/Volumes/Ext SSD/Phipps Global/New Site'
PDF = 'PHIPPS-GLOBAL-PRESENTATION-2026.pdf'

all_html = [f for f in os.listdir(BASE_DIR) if f.endswith('.html')]
patched = 0

for fname in all_html:
    fp = os.path.join(BASE_DIR, fname)
    with open(fp, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    footer = soup.select_one('footer.site-footer')
    if not footer:
        continue

    changed = False

    # Add Presentation to Contact col
    for col in footer.select('.footer-col'):
        h4 = col.select_one('h4')
        if not h4:
            continue
        heading = h4.get_text(strip=True).lower()
        if 'contact' in heading:
            existing_hrefs = [a.get('href','') for a in col.select('a')]
            if PDF not in existing_hrefs:
                tag = BeautifulSoup(
                    f'<a href="{PDF}" target="_blank" rel="noopener">View Presentation</a>',
                    'html.parser'
                )
                col.append(tag)
                changed = True

    if changed:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        patched += 1

print(f"Patched {patched} pages with Presentation link in footer Contact col.")
