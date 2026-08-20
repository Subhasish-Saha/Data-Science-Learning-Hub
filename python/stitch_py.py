#!/usr/bin/env python3
"""Stitch all 11 Python part files into one print/PDF-ready PY_Complete.html.
Reuses Part 1's head/CSS/tracker/script (including the Pyodide runtime block);
concatenates each part's content with a part divider; builds a combined sidebar
nav. Re-run after editing any part."""
import re, pathlib

OUT = pathlib.Path(__file__).resolve().parent      # run from the python/ folder
NP  = 11
PARTS = [
    ("PY_Part01_DataModel.html", "The Python Data Model",
     "Bindings, mutability, identity, hashability, copies, scope, late binding, memory"),
    ("PY_Part02_DataStructures.html", "Data Structures &amp; Complexity",
     "The four-way choice, the complexity table, the accidental O(n²), collections, sorting"),
    ("PY_Part03_Functions.html", "Functions, Closures &amp; Decorators",
     "Signature grammar, closures, decorators from scratch, functools, type hints"),
    ("PY_Part04_Generators.html", "Iterators, Generators &amp; Laziness",
     "The iterator protocol, generators, streaming a file too big for RAM, itertools, context managers"),
    ("PY_Part05_OOP.html", "OOP, Dataclasses &amp; Protocols",
     "Class vs instance attributes, properties, dunders, dataclasses, MRO, sklearn estimators"),
    ("PY_Part06_NumPy.html", "NumPy",
     "ndarray anatomy, strides, views vs copies, broadcasting, axis semantics, vectorising"),
    ("PY_Part07_PandasCore.html", "pandas Core",
     "Index alignment, dtypes after 3.0, loc vs iloc, Copy-on-Write, missing data, reading properly"),
    ("PY_Part08_PandasTransform.html", "pandas Transformation",
     "Split-apply-combine, agg vs transform vs apply, joins that explode, windows without leakage, SQL"),
    ("PY_Part09_Performance.html", "Performance, Memory &amp; Concurrency",
     "Measuring, the vectorisation ladder, halving memory, the GIL and free-threaded 3.14"),
    ("PY_Part10_Production.html", "Production Python for Data Science",
     "Notebook to module, lockfiles, logging, testing data code, pipelines, data leakage"),
    ("PY_Part11_QABank.html", "Interview Q&amp;A Bank &amp; Playground",
     "130 questions, 14 traps, 8 live-coding exercises, a free playground, SQL drill, cheat sheets"),
]

def read(fn): return (OUT / fn).read_text()

def content_of(html):
    s = html.index("</section>", html.index('id="tracker"')) + len("</section>")
    e = html.index("      <!-- PART NAV -->")
    return html[s:e].strip("\n")

def nav_grps(html, skip_tracker=True):
    nav = re.search(r'<nav class="toc" id="toc">(.*?)</nav>', html, re.DOTALL).group(1)
    grps = re.findall(r'<div class="grp">.*?</div>', nav, re.DOTALL)
    return grps[1:] if skip_tracker else grps

p1 = read(PARTS[0][0])

top    = p1[: p1.index("</section>", p1.index('id="tracker"')) + len("</section>")]
bottom = p1[p1.index('<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js'):]

top = top.replace("<title>Python for Data Science — Part 1: The Python Data Model</title>",
                  "<title>Python for Data Science — Complete (All 11 Parts)</title>")
top = top.replace('<div class="tt"><small>Part 1 / 11</small>The Python Data Model</div>',
                  '<div class="tt"><small>Complete</small>All 11 Parts</div>')
top = top.replace('<div class="k">Part 1 of 11</div>\n      <div class="v">The Python Data Model</div>',
                  '<div class="k">Complete edition</div>\n      <div class="v">All 11 Parts</div>')

new_hero = ('<header class="hero">\n'
  '        <div class="eyebrow">Complete Resource · All 11 Parts</div>\n'
  '        <h1 class="title">Python for data science interviews, end to end\n'
  '          <span class="sub">The full curriculum in one document — the data model, containers and complexity, '
  'functions and decorators, generators, OOP and dataclasses, NumPy, pandas core and transformation, '
  'performance and concurrency, production engineering, and a consolidated 130-question interview bank.</span>\n'
  '        </h1>\n'
  '        <p class="thesis">This is the stitched edition of all eleven parts, print- and PDF-ready. The master tracker '
  'below covers every one of the 191 topics across 106 sections; your progress is shared with the individual part files '
  '(same browser). Library-current as of <b>Aug 2026</b> — Python <b>3.14</b> (PEP 779 free-threading), '
  'pandas <b>3.0</b> (Copy-on-Write only), NumPy <b>2.5</b>, scikit-learn <b>1.9</b>. '
  'The <b>95 runnable cells</b> execute real CPython 3.14 in your browser via Pyodide and work in this combined file '
  'too — nothing is sent to a server. Use the sidebar to jump to any part or section.</p>\n'
  '        <div class="meta-chips">\n'
  '          <span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>11 parts</b> · 10 levels</span>\n'
  '          <span class="chip"><b>106</b> sections · <b>191</b> tracked topics</span>\n'
  '          <span class="chip">📐 <b>13</b> diagrams</span>\n'
  '          <span class="chip">▶ <b>95</b> runnable cells</span>\n'
  '          <span class="chip">💬 <b>310</b> Q&amp;A + 14 traps</span>\n'
  '        </div>\n'
  '      </header>')
top = re.sub(r'<header class="hero">.*?</header>', lambda m: new_hero, top, count=1, flags=re.DOTALL)

tracker_grp = nav_grps(p1, skip_tracker=False)[0]
jump = ('      <div class="grp">\n'
  '        <button class="ghead" data-t><span class="num">§</span> Jump to Part <span class="chev">▾</span></button>\n'
  '        <ul class="links">\n'
  + "\n".join('          <li><a href="#part%d">Part %d · %s</a></li>' % (i + 1, i + 1, re.sub("&amp;", "&", t))
              for i, (_, t, _) in enumerate(PARTS))
  + '\n        </ul>\n      </div>\n')
all_grps = ""
for fn, _, _ in PARTS:
    all_grps += "".join("      " + g + "\n" for g in nav_grps(read(fn)))
combined_nav = ('<nav class="toc" id="toc">\n      ' + tracker_grp + '\n' + jump + all_grps + '    </nav>')
top = re.sub(r'<nav class="toc" id="toc">.*?</nav>', lambda m: combined_nav, top, count=1, flags=re.DOTALL)

def divider(i, title, sub):
    return ('\n      <div class="part-divider" id="part%d">\n'
            '        <div class="pdk">Part %d of %d</div>\n'
            '        <div class="pdt">%s</div>\n'
            '        <div class="pds">%s</div>\n'
            '      </div>\n') % (i, i, NP, title, sub)

body = ""
for i, (fn, title, sub) in enumerate(PARTS, start=1):
    body += divider(i, title, sub) + "\n" + content_of(read(fn)) + "\n"

foot = ('\n      <div class="doc-foot">\n'
  '        Python for Data Science Interviews — <b>Complete edition</b> · all 11 parts · 106 sections · '
  '191 tracked topics · 13 diagrams · 95 runnable cells · 310 Q&amp;A.<br>\n'
  '        Library-current as of <b>Aug 2026</b> — Python <b>3.14</b> · pandas <b>3.0</b> · NumPy <b>2.5</b> · '
  'scikit-learn <b>1.9</b>.<br>\n'
  '        Runnable cells execute <b>real CPython 3.14</b> in your browser via Pyodide; nothing is uploaded.<br>\n'
  '        Progress is stored locally under key <code style="color:#8892a0">pyPrepStatus_v1</code>, shared with every part file.<br>\n'
  '        Regenerate this file after editing any part with: '
  '<code style="color:#8892a0">python3 stitch_py.py</code> · '
  '<a href="../index.html" style="color:#8892a0">← Learning Hub</a>\n'
  '      </div>\n')

divider_css = ('\n.part-divider{margin:80px 0 10px;padding:26px 28px;border-radius:16px;'
  'background:linear-gradient(135deg,#161b23,#252d3a);border:1px solid #2c3542;color:#fff;'
  'scroll-margin-top:20px;box-shadow:var(--shadow)}\n'
  '.part-divider .pdk{font-family:var(--mono);font-size:12px;letter-spacing:2.4px;'
  'text-transform:uppercase;color:var(--gold-2)}\n'
  '.part-divider .pdt{font-family:var(--disp);font-weight:700;font-size:2rem;letter-spacing:-.6px;margin:6px 0 4px}\n'
  '.part-divider .pds{color:#aeb7c4;font-size:1rem}\n'
  '@media print{.part-divider{break-before:page;page-break-before:always}}\n')
top = top.replace("</style>", divider_css + "</style>", 1)

close = '\n    </div>\n  </main>\n</div>\n\n'
complete = top + "\n" + body + foot + close + bottom
(OUT / "PY_Complete.html").write_text(complete)
print("wrote PY_Complete.html", "{:,} bytes".format(len(complete)))
