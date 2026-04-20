import glob
import re

# Update inline border-radius in HTML files
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = html.replace('border-radius:12px;', 'border-radius:1px;')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

# Update hardcoded border-radius values in style.css, ignoring buttons and specific radii
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# I will replace these specific card/image hardcoded classes:
replacements = [
    ('border-radius:20px;', 'border-radius:var(--radius);'), # Mega menu block uses this
    ('border-radius:12px;', 'border-radius:var(--radius);'), # Journal card
    ('border-radius:16px;', 'border-radius:var(--radius);'), # Hero testimonial and others
    ('border-radius:10px;', 'border-radius:var(--radius);'), # mega link icon
]

for old, new in replacements:
    css = css.replace(old, new)


with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Radius changes applied.")
