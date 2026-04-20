import glob
import re

files = [
    'artwork.html', 'bathroom-accessories.html', 'carpet-tiles.html',
    'ffe.html', 'glass.html', 'led-mirrors.html', 'lvt.html',
    'plumbing-fixtures.html', 'shower-enclosures.html', 'stone.html',
    'tiles.html', 'wood-flooring.html'
]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strip the page-header block
    content = re.sub(r'<div class="page-header">.*?</div>\n</div>', '', content, flags=re.DOTALL)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Headers stripped successfully.")
