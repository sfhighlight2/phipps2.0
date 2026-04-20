with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

target = """/* ── Portfolio Section ── */
.portfolio-section { padding:100px 0; overflow:hidden; }
.portfolio-header-split { display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:48px; gap:40px; }
.ph-left { max-width:500px; }
.ph-left h2 { font-size:48px; line-height:1.1; font-weight:400; letter-spacing:-0.02em; }
.ph-right { max-width:440px; display:flex; flex-direction:column; gap:20px; align-items:flex-start; }"""

replacement = """/* ── Portfolio Section ── */
.portfolio-section { padding:100px 0; overflow:hidden; }
.portfolio-header-split { display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:48px; gap:40px; }
.ph-left { max-width:500px; }
.ph-left h2 { font-size:48px; line-height:1.1; font-weight:400; letter-spacing:-0.02em; }
.ph-right { max-width:440px; display:flex; flex-direction:column; gap:20px; align-items:flex-start; }
.portfolio-nav-arrows { display:flex; gap:12px; margin-bottom:8px; }
.portfolio-nav-arrows button { background:transparent; border:1px solid rgba(26,26,26,0.1); color:#1a1a1a; width:48px; height:48px; border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; transition:all 0.2s; font-size:18px; }
.portfolio-nav-arrows button:hover { background:var(--accent); border-color:var(--accent); color:#fff; }"""

css = css.replace(target, replacement)
with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)
