import os
import glob

replacements = {
    "var(--text-muted)": "var(--gray-5)",
    "var(--border-dark)": "var(--gray-4)",
    "var(--border-mid)": "var(--gray-3)",
    "var(--border-light)": "var(--gray-2)",
    "var(--accent)": "var(--gold)",
    "rgba(234,88,12,": "rgba(184,154,96,",
    "font-family: var(--font-heading);": "font-family: var(--font-serif);",
    "btn-accent": "btn-gold",
    "text-accent": "text-gold",
    "bg-alt": "bg-cream"
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

# And let's fix the specific index.html replace we did earlier
index_path = "index.html"
with open(index_path, "r") as f:
    idx = f.read()
idx = idx.replace("font-family: var(--font-serif); font-size: 3rem; color: var(--gray-3); border-right: 1px solid var(--gray-2);", "font-family: var(--font-serif); font-size: 3rem; color: rgba(184,154,96,0.25); border-right: 1px solid var(--gray-2);")
with open(index_path, "w") as f:
    f.write(idx)

print("Done! Reverting HTML completed.")
