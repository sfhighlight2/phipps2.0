import glob

# Update inline border-radius in HTML files back to 2px
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = html.replace('border-radius:1px;', 'border-radius:2px;')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)
print("Updated all HTML inline radius properties to 2px.")
