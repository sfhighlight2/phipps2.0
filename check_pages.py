import re
from bs4 import BeautifulSoup
import glob

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

links = set()
for a in soup.find('nav').find_all('a'):
    if 'href' in a.attrs:
        href = a['href']
        if href.startswith('#') or href == 'index.html': continue
        
        # strip hash if any
        base_page = href.split('#')[0]
        links.add(base_page)

existing_files = set(glob.glob('*.html'))

missing = links - existing_files
print("Missing linked pages:", missing)
