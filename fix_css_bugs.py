import os
import glob

files = glob.glob("*.html") + ["build.py"]
for f in files:
    if os.path.exists(f):
        with open(f, "r") as file:
            content = file.read()
        
        original = content
        
        # Fixing the undefined variable
        content = content.replace("var(--off-white)", "var(--cream-lit)")
        
        # Provide the carousel wrap
        if f == "style.css":
            if ".carousel-wrap" not in content:
                content = content.replace(".carousel-track {", ".carousel-wrap { overflow: hidden; position: relative; width: 100%; }\n.carousel-track {")
                
        if original != content:
            with open(f, "w") as file:
                file.write(content)
            print(f"Updated {f}")

print("Done fixing HTML!")
