#!/usr/bin/env python3
"""
Fix broken images by:
1. Downloading images from the live site for each broken project page
2. Updating the HTML files with the correct image paths
"""
import os
import re
import urllib.request
import ssl
import certifi
from bs4 import BeautifulSoup

BASE_DIR = '/Volumes/Ext SSD/Phipps Global/New Site'

ssl_context = ssl.create_default_context(cafile=certifi.where())

# Map of slug -> known local image (for ones we already have)
KNOWN_IMAGES = {
    'tantalo-hotel': 'images/tantalo-hotel-01.jpg',
    'moxy-hotel': 'images/moxy-hotel-01.jpg',
    'jekyll-island-club-resort': 'images/jekyll-island-club-resort-01.jpg',
    'sir-francis-drake-hotel': 'images/sir-francis-drake-hotel-01.webp',
    'ritz-carlton': 'images/ritz-carlton-01.jpg',
    'the-boca-resort': 'images/the-boca-resort-01.jpg',
    'virgin-hotel': 'images/virgin-hotel-01.jpg',
    'the-westin-flushing-laguardia-airport': 'images/the-westin-flushing-01.jpg',
    'the-west-hollywood-edition': 'images/editionhotels-01-scaled.jpg',
    'the-gatsby': 'images/the-gatsby-01.webp',
    'the-paul': 'images/the-paul-04.jpg',
    'the-row': 'images/the-row-hotel-01.jpg',
    'the-dean': 'images/the-dean-05.jpg',
    'the-ludlow': 'images/the-lodlow-01.jpg',
    'the-marlton': 'images/the-marlton-02-scaled.jpg',
    'the-sutton': 'images/the-sutton-01.jpg',
    'the-harrison-street': 'images/the-harrison-street-01-e1733478145214.jpg',
    'the-castle': 'images/the-castle-001.png',
    'tribeca-green': 'images/tribeca-green-01-e1733483575791.jpg',
    'transbay-block': 'images/transbay-block-03-01.gif',
    'one-hill-south': 'images/one-hill-south-01-scaled-e1733469076378.jpg',
    'slate-building': 'images/slate-building-01.webp',
    'yorkshire-towers': 'images/the-sutton-6.jpg',  # fallback similar image
    '1080-amsterdam': 'images/1080-amsterdam-01.jpg',
    '205-ea-92nd-st': 'images/205-ea-92nd-st-01.jpg',
    '280-met': 'images/280-metropolitan-1.webp',
    '340-court-street': 'images/340-court-street-01.jpg',
    '456-washington-st': 'images/456-washington-st-04.jpg',
    '465-pacific': 'images/465-pacific-01-scaled.jpg',
    '50-north-5th-street': 'images/50-north-5th-street-01.jpg',
    '71-reade-chambers': 'images/71-reade-chambers-01.webp',
    'lafayette-estates': 'images/lafayette-estates-01.jpg',
    'livmor-115th-st': 'images/livmor-115th-st-01.webp',
}

# Fallback images by category (luxury interior/hotel/residential photos)
HOTEL_FALLBACKS = [
    'images/hotel-lobby-luxury.webp',
    'images/poland-warsaw-seating-furniture-at-lounge-of-hotel-e1733913658549.jpg',
    'images/interior-setting-e1733914733183.jpg',
    'images/luxurious-modern-bathroom-with-marble-walls-and-glass-shower--e1733913328449.jpg',
]
RES_FALLBACKS = [
    'images/modern-glass-buildings-e1733913526693.jpg',
    'images/white-living-room-with-carpet-e1733913999924.jpg',
    'images/interior-setting-e1733914733183.jpg',
    'images/living-room-with-wood-flooring-e1733914178998.jpg',
]

def download_image_from_live(slug):
    """Try to download hero image from live site."""
    url = f"https://phippsglobal.com/{slug}/"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, context=ssl_context, timeout=10)
        soup = BeautifulSoup(response.read(), 'html.parser')
        
        # Look for the main/hero image on live page
        img_selectors = [
            '.wp-post-image',
            '.wp-block-image img',
            '.site-main img',
            'article img',
        ]
        for sel in img_selectors:
            img = soup.select_one(sel)
            if img and img.get('src'):
                img_url = img['src']
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                elif img_url.startswith('/'):
                    img_url = 'https://phippsglobal.com' + img_url
                
                # Get extension
                ext = img_url.split('?')[0].split('.')[-1].lower()
                if ext not in ['jpg','jpeg','png','webp','gif','svg']:
                    ext = 'jpg'
                
                local_name = f"images/{slug}-hero.{ext}"
                local_path = os.path.join(BASE_DIR, local_name)
                
                if not os.path.exists(local_path):
                    img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                    img_resp = urllib.request.urlopen(img_req, context=ssl_context, timeout=10)
                    with open(local_path, 'wb') as f:
                        f.write(img_resp.read())
                
                return local_name
    except Exception as e:
        print(f"  Could not fetch from live: {e}")
    return None

html_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.html')]
exclude = ['index.html','hotels.html','residential.html','projects.html','our-firm.html','services.html','get-in-touch.html','contact.html','hendricks.html','artwork.html','bathroom-accessories.html','carpet-tiles.html','ffe.html','glass.html','led-mirrors.html','lvt.html','plumbing-fixtures.html','shower-enclosures.html','stone.html','tiles.html','wood-flooring.html']

fallback_hotel_idx = 0
fallback_res_idx = 0

for fname in sorted(html_files):
    if fname in exclude: continue
    
    fpath = os.path.join(BASE_DIR, fname)
    with open(fpath, 'r') as fp:
        soup = BeautifulSoup(fp.read(), 'html.parser')
    
    hero_bg = soup.select_one('.loc-hero-bg')
    if not hero_bg: continue
    
    current_src = hero_bg.get('src', '')
    if current_src != 'images/placeholder.jpg' and os.path.exists(os.path.join(BASE_DIR, current_src)):
        continue  # Already good
    
    slug = fname.replace('.html', '')
    print(f"Fixing {fname}...")
    
    # Step 1: Check known images map
    if slug in KNOWN_IMAGES:
        img_path = KNOWN_IMAGES[slug]
        if os.path.exists(os.path.join(BASE_DIR, img_path)):
            print(f"  -> Using known image: {img_path}")
        else:
            img_path = None
    else:
        img_path = None
    
    # Step 2: Try downloading from live site
    if not img_path:
        print(f"  -> Trying live download...")
        img_path = download_image_from_live(slug)
    
    # Step 3: Use smart fallback based on category
    if not img_path:
        eyebrow = soup.select_one('.eyebrow')
        is_hotel = eyebrow and 'hotel' in eyebrow.get_text().lower()
        
        if is_hotel:
            img_path = HOTEL_FALLBACKS[fallback_hotel_idx % len(HOTEL_FALLBACKS)]
            fallback_hotel_idx += 1
        else:
            img_path = RES_FALLBACKS[fallback_res_idx % len(RES_FALLBACKS)]
            fallback_res_idx += 1
        print(f"  -> Using fallback: {img_path}")
    
    # Update all img tags that were placeholder
    for img in soup.select('img'):
        if img.get('src') == 'images/placeholder.jpg':
            img['src'] = img_path
    
    with open(fpath, 'w') as fp:
        fp.write(str(soup))
    print(f"  Updated {fname}")

print("Image fixing complete!")
