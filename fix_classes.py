import os
import glob

replacements = {
    "btn-gold": "btn-accent",
    "text-gold": "text-accent",
    "bg-cream": "bg-alt"
}

files = glob.glob("*.html") + ["build.py"]
for f in files:
    if os.path.exists(f):
        with open(f, "r") as file:
            content = file.read()
        
        original = content
        for old, new in replacements.items():
            content = content.replace(old, new)
            
        if original != content:
            with open(f, "w") as file:
                file.write(content)
            print(f"Updated {f}")
print("Done!")
