import glob
import os

html_snippet = """
    <a href="tel:+15614633390" class="floating-phone" aria-label="Call Phipps Global">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
    </a>
</body>"""

for file in glob.glob("*.html"):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Only add if it's not already there
    if 'class="floating-phone"' not in content:
        content = content.replace('</body>', html_snippet)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

css_snippet = """
/* ── Floating Phone Button ── */
.floating-phone {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background-color: var(--accent);
  color: #fff;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 9999;
  transition: all 0.3s ease;
}
.floating-phone:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.2);
  color:#fff;
}
.floating-phone svg {
  width: 24px;
  height: 24px;
}
"""

with open('style.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

if '.floating-phone' not in css_content:
    with open('style.css', 'a', encoding='utf-8') as f:
        f.write(css_snippet)

print("Floating phone added successfully.")
