with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# I will just remove the last line if it is "});"
lines = js.split('\n')
if lines[-1].strip() == "});":
    lines = lines[:-1]
elif lines[-2].strip() == "});":
    lines = lines[:-2] + [lines[-1]]

js = '\n'.join(lines)
with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
