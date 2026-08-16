#!/usr/bin/env python3
"""Stitch all 12 part files into one print/PDF-ready LangGraph_Complete.html.
Reuses Part 1's head/CSS/tracker/script; concatenates each part's content with a part
divider; builds a combined sidebar nav. Re-run any time after editing the parts."""
import re, pathlib

OUT = pathlib.Path(__file__).resolve().parent   # run from the langgraph/ folder
PARTS = [
    ("LangGraph_Part01_Prerequisites.html", "Prerequisites &amp; the LLM Substrate", "Typing, Annotated, async, tokens, structured output, the LangChain layer"),
    ("LangGraph_Part02_AgenticFoundations.html", "Agentic AI Foundations", "The capability ladder, agent anatomy, ReAct, planning, reflection, when not to"),
    ("LangGraph_Part03_CorePrimitives.html", "LangGraph Core Primitives", "StateGraph, nodes, edges, reducers, supersteps, Send, Command, subgraphs"),
    ("LangGraph_Part04_WorkflowPatterns.html", "Workflow Patterns", "Chaining, parallelisation, routing, orchestrator-worker, evaluator loops"),
    ("LangGraph_Part05_StateMemory.html", "State, Persistence &amp; Memory", "Checkpointers, threads, time travel, HITL, context window, the Store, durability"),
    ("LangGraph_Part06_Tools.html", "Tools &amp; Agent Capabilities", "Tool design, errors, tool choice, sandboxing, MCP, middleware"),
    ("LangGraph_Part07_RAG.html", "RAG in Agents", "Retrieval as a tool, the ladder, agentic RAG, CRAG, Self-RAG, grounding"),
    ("LangGraph_Part08_MultiAgent.html", "Multi-Agent Architectures", "When it pays, supervisor, swarm, hierarchy, shared state, failure modes"),
    ("LangGraph_Part09_Observability.html", "Observability &amp; Evaluation", "Tracing, trajectory eval, LLM-as-judge, datasets, CI gates, online eval"),
    ("LangGraph_Part10_Production.html", "Production Engineering", "Deployment, streaming, idempotency, cost, latency, security, scale, testing"),
    ("LangGraph_Part11_Frontier.html", "Advanced &amp; Frontier", "Long-horizon agents, computer use, protocols, context engineering, 2026 positions"),
    ("LangGraph_Part12_QABank.html", "Interview Q&amp;A Bank", "125 questions, 12 traps, 6 system designs, 8 coding exercises, cheat sheets"),
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
top = top.replace("<title>LangGraph &amp; Agentic AI — Part 1: Prerequisites &amp; the LLM Substrate</title>",
                  "<title>LangGraph &amp; Agentic AI — Complete (All 12 Parts)</title>")
top = top.replace('<div class="tt"><small>Part 1 / 12</small>Prerequisites &amp; the LLM Substrate</div>',
                  '<div class="tt"><small>Complete</small>All 12 Parts</div>')
top = top.replace('<div class="k">Part 1 of 12</div>\n      <div class="v">Prerequisites &amp; the LLM Substrate</div>',
                  '<div class="k">Complete edition</div>\n      <div class="v">All 12 Parts</div>')

# combined hero
new_hero = ('<header class="hero">\n'
  '        <div class="eyebrow">Complete Resource · All 12 Parts</div>\n'
  '        <h1 class="title">LangGraph &amp; Agentic AI, end to end\n'
  '          <span class="sub">The full curriculum in one document — prerequisites and agentic foundations, the LangGraph '
  'primitives, workflow patterns, state and memory, tools and MCP, agentic RAG, multi-agent architectures, evaluation and '
  'observability, production engineering, the 2026 frontier, and a consolidated 125-question interview bank.</span>\n'
  '        </h1>\n'
  '        <p class="thesis">This is the stitched edition of all twelve parts, print- and PDF-ready. The master tracker below '
  'covers every one of the 210 topics across 98 sections; your progress is shared with the individual part files (same browser). '
  'API-current as of <b>Aug 2026</b> — LangGraph <b>1.2.11</b> · LangChain <b>1.3.15</b> (both 11 Aug 2026), Python ≥ 3.10; '
  '<code class="ic">create_agent</code>, not the deprecated <code class="ic">create_react_agent</code>. '
  'The <b>9 interactive widgets</b> compute live in your browser and work in this combined file too. '
  'Every topic ends with its own tagged Q&amp;A box — use the sidebar to jump to any part or section.</p>\n'
  '        <div class="meta-chips">\n'
  '          <span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>12 parts</b> · 11 levels</span>\n'
  '          <span class="chip"><b>98</b> sections · <b>210</b> tracked topics</span>\n'
  '          <span class="chip">📐 <b>29</b> diagrams</span>\n'
  '          <span class="chip">🎛 <b>9</b> interactive</span>\n'
  '          <span class="chip">💬 <b>342</b> Q&amp;A + 12 traps</span>\n'
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
            f'        <div class="pdk">Part {i} of 12</div>\n'
            f'        <div class="pdt">{title}</div>\n'
            f'        <div class="pds">{sub}</div>\n'
            f'      </div>\n')

body = ""
for i, (fn, title, sub) in enumerate(PARTS, start=1):
    body += divider(i, title, sub) + "\n" + content_of(read(fn)) + "\n"

# ---- combined foot ----
foot = ('\n      <div class="doc-foot">\n'
  '        LangGraph &amp; Agentic AI — <b>Complete edition</b> · all 12 parts · 98 sections · 210 tracked topics · '
  '29 diagrams · 9 interactive widgets · 342 Q&amp;A.<br>\n'
  '        API-current as of <b>Aug 2026</b> — LangChain <b>1.3.15</b> · LangGraph <b>1.2.11</b> · Python 3.10–3.14. '
  '<code style="color:#8892a0">create_agent</code> replaces the deprecated '
  '<code style="color:#8892a0">create_react_agent</code>.<br>\n'
  '        Progress is stored locally under key <code style="color:#8892a0">lgPrepStatus_v1</code>, shared with every part file.<br>\n'
  '        Regenerate this file after editing any part with: '
  '<code style="color:#8892a0">python3 stitch_lg.py</code> · '
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
(OUT / "LangGraph_Complete.html").write_text(complete)
print("wrote LangGraph_Complete.html", f"{len(complete):,} bytes")
