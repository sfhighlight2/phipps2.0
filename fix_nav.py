import os
import glob
import re

with open('index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

# Fix inline border-radius: 0 in index.html BEFORE extracting
idx_content = idx_content.replace('border-radius:0;', '')
idx_content = idx_content.replace('border-radius: 0;', '')
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx_content)

# Now, extract the nav area
start_str = '<nav class="site-nav"'
end_str = '</nav>'
start_idx = idx_content.find(start_str)
end_idx = idx_content.find(end_str) + len(end_str)
nav_html = idx_content[start_idx:end_idx]

for file in glob.glob('*.html'):
    if file == 'index.html': continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove border-radius: 0 inline anywhere it exists
    content = content.replace('border-radius:0;', '')
    content = content.replace('border-radius: 0;', '')

    fs = content.find(start_str)
    fe = content.find(end_str)
    if fs != -1 and fe != -1:
        fe += len(end_str)
        new_content = content[:fs] + nav_html + content[fe:]
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)

print("Done propagating nav and fixing button radius")
