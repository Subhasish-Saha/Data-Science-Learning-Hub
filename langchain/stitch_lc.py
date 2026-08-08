#!/usr/bin/env python3
"""Stitch all 6 part files into one print/PDF-ready RAG_Interview_Prep_Complete.html.
Reuses Part 1's head/CSS/tracker/script; concatenates each part's content with a part
divider; builds a combined sidebar nav. Re-run any time after editing the parts."""
import re, pathlib

OUT = pathlib.Path(__file__).resolve().parent   # run from the langgraph/ folder
PARTS = [
    ("LangChain_Part1_LLMFoundations.html", "LLM Foundations", "Tokens, context, decoding, tool calling, hallucination"),
    ("LangChain_Part2_PromptEngineering.html", "Prompt Engineering", "6-category taxonomy, reasoning models, injection, context engineering"),
    ("LangChain_Part3_Core.html", "LangChain Core", "Packages, models, messages, structured output, LCEL"),
    ("LangChain_Part4_Agents.html", "Tools, Agents &amp; RAG", "Tool design, create_agent, 19 middleware, retrieval"),
    ("LangChain_Part5_Production.html", "Memory &amp; Production", "Memory chain, caching, cost, security, testing, eval"),
    ("LangChain_Part6_QABank.html", "Interview Q&amp;A Bank", "85+ questions, 12 traps, 7 designs, deprecation map"),
]

def read(fn): return (OUT / fn).read_text()

def content_of(html):
    s = html.index("</section>", html.index('id="tracker"')) + len("</section>")
    e = html.index("      <!-- PART NAV -->")
    return html[s:e].strip("\n")

def nav_grps(html, skip_tracker=True):
    nav = re.search(r'<nav class="toc" id="toc">(.*?)</nav>', html, re.DOTALL).group(1)
    grps = re.findall(r'<div class="grp">.*?</div>', nav, re.DOTALL)
    return grps[1:] if skip_tracker else grps   # grp[0] is the Progress Tracker group

p1 = read(PARTS[0][0])

# ---- TOP: head + CSS + topbar + sidebar-open + hero + tracker (through </section>) ----
top = p1[: p1.index("</section>", p1.index('id="tracker"')) + len("</section>")]

# ---- SCRIPT + close: from the highlight.js <script> to EOF ----
bottom = p1[p1.index('<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js'):]

# ---- swap chrome for the combined doc ----
top = top.replace("<title>LangChain &amp; Prompt Engineering — Part 1: LLM Foundations</title>",
                  "<title>LangChain &amp; Prompt Engineering — Complete (All 6 Parts)</title>")
top = top.replace('<div class="tt"><small>Part 1 / 6</small>LLM Foundations</div>',
                  '<div class="tt"><small>Complete</small>All 6 Parts</div>')
top = top.replace('<div class="k">Part 1 of 6</div>\n      <div class="v">LLM Foundations</div>',
                  '<div class="k">Complete edition</div>\n      <div class="v">All 6 Parts</div>')

# combined hero
new_hero = ('<header class="hero">\n'
  '        <div class="eyebrow">Complete Resource · All 6 Parts</div>\n'
  '        <h1 class="title">LangChain, LLMs &amp; Prompt Engineering, end to end\n'
  '          <span class="sub">The full curriculum in one document — LLM fundamentals, prompt engineering as a discipline, the LangChain 1.x surface, tools and middleware, retrieval, memory, production engineering, and an 85+ question interview bank.</span>\n'
  '        </h1>\n'
  '        <p class="thesis">This is the stitched edition of all six parts, print- and PDF-ready. The master tracker below '
  'covers every one of the 313 topics; your progress is shared with the individual part files (same browser). '
  'Written against <b>LangChain 1.3.14</b> (Aug 2026) — legacy 0.x APIs live in <code class="ic">langchain-classic</code>. Use the sidebar to jump to any part or section.</p>\n'
  '        <div class="meta-chips">\n'
  '          <span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>6 parts</b> · 14 levels</span>\n'
  '          <span class="chip"><b>313</b> tracked topics</span>\n'
  '          <span class="chip"><b>16</b> diagrams</span>\n'
  '          <span class="chip"><b>69</b> Q&amp;A</span>\n'
  '          <span class="chip">\U0001f40d LangChain <b>1.3</b></span>\n'
  '        </div>\n'
  '      </header>')
top = re.sub(r'<header class="hero">.*?</header>', lambda m: new_hero, top, count=1, flags=re.DOTALL)

# ---- combined sidebar nav: Progress Tracker + Jump-to-Part + every part's groups ----
tracker_grp = nav_grps(p1, skip_tracker=False)[0]
jump = ('      <div class="grp">\n'
  '        <button class="ghead" data-t><span class="num">§</span> Jump to Part <span class="chev">▾</span></button>\n'
  '        <ul class="links">\n'
  + "\n".join(f'          <li><a href="#part{i+1}">Part {i+1} · {re.sub("&amp;","&",t)}</a></li>'
              for i, (_, t, _) in enumerate(PARTS))
  + '\n        </ul>\n      </div>\n')
all_grps = ""
for fn, _, _ in PARTS:
    all_grps += "".join("      " + g + "\n" for g in nav_grps(read(fn)))
combined_nav = ('<nav class="toc" id="toc">\n'
  '      ' + tracker_grp + '\n'
  + jump
  + all_grps
  + '    </nav>')
top = re.sub(r'<nav class="toc" id="toc">.*?</nav>', lambda m: combined_nav, top, count=1, flags=re.DOTALL)

# ---- body: part divider + content, for each part ----
def divider(i, title, sub):
    return (f'\n      <div class="part-divider" id="part{i}">\n'
            f'        <div class="pdk">Part {i} of 6</div>\n'
            f'        <div class="pdt">{title}</div>\n'
            f'        <div class="pds">{sub}</div>\n'
            f'      </div>\n')

body = ""
for i, (fn, title, sub) in enumerate(PARTS, start=1):
    body += divider(i, title, sub) + "\n" + content_of(read(fn)) + "\n"

# ---- combined foot ----
foot = ('\n      <div class="doc-foot">\n'
  '        LangChain &amp; Prompt Engineering — <b>Complete edition</b> · all 6 parts · 313 tracked topics.<br>\n'
  '        API-current as of <b>Aug 2026</b> — LangChain <b>1.3.14</b> · langchain-core ≥ <b>0.3.81</b> · Python 3.10–3.14.<br>\n'
  '        Progress is stored locally under key <code style="color:#8892a0">lcPrepStatus_v1</code>, shared with every part file.<br>\n'
  '        Regenerate this file after editing any part with: '
  '<code style="color:#8892a0">python3 stitch_lc.py</code> · '
  '<a href="../index.html" style="color:#8892a0">← Learning Hub</a>\n'
  '      </div>\n')

# ---- inject a little CSS for the part divider (before </style>) ----
divider_css = ('\n.part-divider{margin:80px 0 10px;padding:26px 28px;border-radius:16px;'
  'background:linear-gradient(135deg,#161b23,#252d3a);border:1px solid #2c3542;color:#fff;'
  'scroll-margin-top:20px;box-shadow:var(--shadow)}\n'
  '.part-divider .pdk{font-family:var(--mono);font-size:12px;letter-spacing:2.4px;'
  'text-transform:uppercase;color:var(--gold-2)}\n'
  '.part-divider .pdt{font-family:var(--disp);font-weight:700;font-size:2rem;letter-spacing:-.6px;margin:6px 0 4px}\n'
  '.part-divider .pds{color:#aeb7c4;font-size:1rem}\n'
  '@media print{.part-divider{break-before:page;page-break-before:always}}\n')
top = top.replace("</style>", divider_css + "</style>", 1)

close = '\n    </div>\n  </main>\n</div>\n\n'   # close .content, .main, .layout
complete = top + "\n" + body + foot + close + bottom
(OUT / "LangChain_Complete.html").write_text(complete)
print("wrote LangChain_Complete.html", f"{len(complete):,} bytes")
