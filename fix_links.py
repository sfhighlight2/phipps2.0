import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    'services.html#artwork': 'artwork.html',
    'services.html#bathroom': 'bathroom-accessories.html',
    'services.html#carpet': 'carpet-tiles.html',
    'services.html#ffe': 'ffe.html',
    'services.html#glass': 'glass.html',
    'services.html#led': 'led-mirrors.html',
    'services.html#lvt': 'lvt.html',
    'services.html#plumbing': 'plumbing-fixtures.html',
    'services.html#shower': 'shower-enclosures.html',
    'services.html#stone': 'stone.html',
    'services.html#tiles': 'tiles.html',
    'services.html#wood': 'wood-flooring.html',
    
    'hotel-hendricks.html': 'hendricks.html',
    'marriott.html': 'marriott-fullerton.html',
    '70-vestry.html': '70-vestry-street.html',
    'nomad-30.html': 'nomad-30-e-31.html',
    '15-hudson-yard.html': '15-hudson-yard.html', # already correct
    '35-hudson-yard.html': '35-hudson-yard.html'  # already correct
}

for old, new in replacements.items():
    content = content.replace(f'"{old}"', f'"{new}"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Links updated in index.html")
