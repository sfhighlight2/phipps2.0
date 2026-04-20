import os
import glob

replacements = {
    "var(--gray-500)": "var(--text-muted)",
    "var(--gray-400)": "var(--border-dark)",
    "var(--gray-300)": "var(--border-mid)",
    "var(--gray-5)": "var(--text-muted)",
    "var(--gray-4)": "var(--border-dark)",
    "var(--gray-3)": "var(--border-mid)",
    "var(--gray-2)": "var(--border-light)",
    "var(--gold)": "var(--accent)",
    "rgba(184,154,96,": "rgba(234,88,12,",
    "font-family: var(--font-serif);": "font-family: var(--font-heading);",
    "font-family: 'Cormorant Garamond', serif; font-style: italic;": "font-family: var(--font-heading);"
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
