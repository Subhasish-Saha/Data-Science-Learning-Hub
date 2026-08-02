#!/usr/bin/env python3
"""Build LangGraph subject shells: reuse the RAG design system (CSS + tracker engine),
swap in a LangGraph tracker (own localStorage key) and per-part chrome.
Leaves a <!--CONTENT_INSERT--> marker in each part to fill."""
import re, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent          # .../output/langgraph
SITE = HERE.parent                                       # .../output
SRC  = SITE / "rag" / "RAG_Interview_Prep_Part1_Foundations.html"
MD   = SITE.parent / "langgraph-agentic-ai-study-guide.md"

# ---------------- tracker: parse the blueprint's checkboxes ----------------
LEVEL_KEY = {
    "Level 0 — Prerequisites": ("l0", "Level 0 · Prerequisites"),
    "Level 1 — Agentic AI Foundations": ("l1", "Level 1 · Agentic AI Foundations"),
    "Level 2 — LangGraph Core Primitives": ("l2", "Level 2 · LangGraph Core Primitives"),
    "Level 3 — Workflow Patterns": ("l3", "Level 3 · Workflow Patterns"),
    "Level 4 — State, Persistence & Memory": ("l4", "Level 4 · State, Persistence & Memory"),
    "Level 5 — Tools & Agent Capabilities": ("l5", "Level 5 · Tools & Agent Capabilities"),
    "Level 6 — RAG and Advanced RAG": ("l6", "Level 6 · RAG &amp; Advanced RAG"),
    "Level 7 — Multi-Agent Architectures": ("l7", "Level 7 · Multi-Agent Architectures"),
    "Level 8 — Observability & Evaluation (LangSmith)": ("l8", "Level 8 · Observability &amp; Evaluation"),
    "Level 9 — Production Engineering": ("l9", "Level 9 · Production Engineering"),
    "Level 10 — Advanced & Frontier Topics": ("l10", "Level 10 · Advanced &amp; Frontier"),
}
CAT = {"l0": "Theory", "l1": "Theory", "l2": "Theory", "l3": "Practical", "l4": "Theory",
       "l5": "Practical", "l6": "Practical", "l7": "Theory", "l8": "Practical",
       "l9": "Practical", "l10": "Theory"}
HIGH = {"l2", "l4", "l8", "l9"}     # levels the guide flags as most interview-critical

def clean(s):
    s = re.sub(r'`([^`]*)`', r'\1', s)                 # strip code ticks
    s = re.sub(r'\*\*([^*]*)\*\*', r'\1', s)           # strip bold
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)     # strip links
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r'\s+', ' ', s).strip(" .")
    return s

rows, cur = [], None
for line in MD.read_text().split("\n"):
    m = re.match(r'^## (.+)$', line)
    if m:
        cur = LEVEL_KEY.get(m.group(1).strip())
    if cur and re.match(r'^\s*- \[ \]', line):
        txt = clean(re.sub(r'^\s*- \[ \]\s*', '', line))
        if txt:
            rows.append([cur[0], CAT[cur[0]], "High" if cur[0] in HIGH else "Medium", txt])

# interview-track rows (not checkboxes in the source)
IV = [("iv", "Interview Prep", "High", t) for t in [
    "High-frequency: Conceptual questions (agent vs workflow, ReAct, LangChain vs LangGraph)",
    "High-frequency: LangGraph mechanics (reducers, Send, Command, supersteps, loops)",
    "High-frequency: State &amp; memory (checkpointer vs store, thread_id, context window)",
    "High-frequency: HITL &amp; production (approval gates, crash recovery, idempotency, durability)",
    "High-frequency: Tools &amp; RAG (tool choice, tool errors, MCP, the RAG ladder)",
    "High-frequency: Evaluation (agent eval, golden trajectories, regression gates)",
    "The 7 trap questions (answered correctly, out loud)",
]]
SD = [("sd", "Interview Prep", "High", t) for t in [
    "System design: Customer support triage agent",
    "System design: Research assistant (parallel Send + reflection)",
    "System design: SQL analytics agent (guarding destructive SQL)",
    "System design: Code review agent (tool design)",
    "System design: Multi-tenant chatbot at 10k users",
    "System design: Long-running campaign agent (weeks, durability)",
]]
PP = [("pp", "Project", "High", t) for t in [
    "Project 1: Multi-pattern workflow set (sequential/parallel/conditional/iterative)",
    "Project 2: Persistent chatbot (Streamlit + SQLite checkpointer + streaming)",
    "Project 3: Research agent built twice (hand-rolled vs create_agent)",
    "Project 4: Agentic RAG with CRAG + Self-RAG",
    "Project 5: Multi-agent report writer (planner/researcher/writer/evaluator + HITL)",
    "Project 6: Fully instrumented agent (LangSmith traces, trajectory evals, CI gate)",
]]
rows += [[k, c, p, t] for k, c, p, t in IV + SD + PP]

PHASES = {k: v for k, v in LEVEL_KEY.values()}
PHASES.update({"iv": "Interview Q&amp;A Bank", "sd": "System Design Scenarios", "pp": "Portfolio Projects"})
ORDER = ["l0","l1","l2","l3","l4","l5","l6","l7","l8","l9","l10","iv","sd","pp"]

tracker_js = "[\n" + ",\n".join(
    f'[{i+1},"{r[0]}","{r[1]}","{r[2]}",0,{json.dumps(r[3])}]' for i, r in enumerate(rows)) + "\n]"
TOTAL = len(rows)
print(f"tracker: {TOTAL} items across {len(ORDER)} groups")

# ---------------- per-part config ----------------
PARTS = {
 1: dict(file="LangGraph_Part1_Foundations.html", title="Foundations &amp; Core Primitives", pk="L0-2",
   groups=[("L0–L1","Foundations",[("g1-1","1.1 · Prerequisites &amp; typing"),("g1-2","1.2 · The capability ladder"),
     ("g1-3","1.3 · Anatomy of an agent"),("g1-4","1.4 · Agent architectures"),("g1-5","1.5 · When NOT to build an agent"),
     ("g1-6","1.6 · Framework landscape")]),
    ("L2","Core Primitives",[("g1-7","1.7 · First graph &amp; mental model"),("g1-8","1.8 · State schemas"),
     ("g1-9","1.9 · Reducers ⭐"),("g1-10","1.10 · Edges &amp; routing"),("g1-11","1.11 · Command"),
     ("g1-12","1.12 · Send &amp; map-reduce"),("g1-13","1.13 · Interview focus")])],
   h1="The graph is the agent", sub="Why agentic systems need a runtime, and the LangGraph primitives everything else is built from — state, nodes, reducers, edges, <code>Command</code>, and <code>Send</code>.",
   thesis="Agents fail interviews at the <strong>primitive</strong> layer. Candidates can name ReAct but can't say what happens when two parallel nodes write the same state key, or when <code>Send</code> beats a static fan-out. This part fixes that: first the conceptual ladder (what makes something <em>agentic</em>, and when a plain workflow is the better engineering call), then LangGraph's core — <strong>state schemas, reducers, supersteps, conditional edges, <code>Command</code>, and <code>Send</code></strong> — built from runnable first principles.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 0–2</b></span>\n          <span class="chip"><b>54</b> tracked topics</span>\n          <span class="chip">⏱ <b>~6–8h</b></span>\n          <span class="chip">🐍 LangGraph <b>v1</b></span>',
   prev=("Learning Hub","All subjects"), prevhref="../index.html",
   nxt=("Part 2 · Patterns, State &amp; Memory",["4 workflow patterns","Checkpointers, Store, HITL"])),
 2: dict(file="LangGraph_Part2_State.html", title="Patterns, State &amp; Memory", pk="L3-4",
   groups=[("L3","Workflow Patterns",[("g2-1","2.1 · Sequential"),("g2-2","2.2 · Parallel fan-out/in"),
     ("g2-3","2.3 · Conditional branching"),("g2-4","2.4 · Iterative cycles"),("g2-5","2.5 · Deferred nodes")]),
    ("L4","State &amp; Memory",[("g2-6","2.6 · Checkpointers"),("g2-7","2.7 · Inspect &amp; time travel"),
     ("g2-8","2.8 · The Store ⭐"),("g2-9","2.9 · Long-term memory pipeline"),
     ("g2-10","2.10 · Context window management"),("g2-11","2.11 · Human-in-the-loop"),("g2-12","2.12 · Interview focus")])],
   h1="Patterns, memory, and the human in the loop", sub="The four workflow shapes every agentic system is assembled from — then persistence, the checkpointer/Store distinction, time travel, context management, and HITL approval gates.",
   thesis="This is where junior and senior candidates separate. Anyone can wire a linear chain; the signal is knowing <strong>which of the four patterns</strong> a business process needs, and then the memory model: a <strong>checkpointer</strong> gives thread-scoped memory keyed by <code>thread_id</code>, a <strong>Store</strong> gives cross-thread memory keyed by user. Confusing them is the classic telling mistake. We also cover time travel, three context-window strategies, and the <code>interrupt()</code> pattern behind every approval gate.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 3–4</b></span>\n          <span class="chip"><b>29</b> tracked topics</span>\n          <span class="chip">⏱ <b>~6–7h</b></span>\n          <span class="chip">💾 persistence &amp; HITL</span>',
   prev=("Part 1 · Foundations &amp; Primitives","State, reducers, Send"), prevhref="LangGraph_Part1_Foundations.html",
   nxt=("Part 3 · Tools, MCP &amp; RAG",["create_agent + middleware","Agentic RAG, CRAG, Self-RAG"])),
 3: dict(file="LangGraph_Part3_Tools.html", title="Tools, MCP &amp; RAG", pk="L5-6",
   groups=[("L5","Tools &amp; Agents",[("g3-1","3.1 · Defining tools"),("g3-2","3.2 · Wiring the ReAct loop"),
     ("g3-3","3.3 · create_agent (current API)"),("g3-4","3.4 · Advanced tool topics"),("g3-5","3.5 · MCP")]),
    ("L6","RAG in LangGraph",[("g3-6","3.6 · Baseline RAG"),("g3-7","3.7 · RAG as a tool = Agentic RAG"),
     ("g3-8","3.8 · Corrective RAG"),("g3-9","3.9 · Self-RAG"),("g3-10","3.10 · The RAG ladder"),("g3-11","3.11 · Interview focus")])],
   h1="Giving the agent hands", sub="Tool design (the docstring <em>is</em> the prompt), the modern <code>create_agent</code> API and its middleware, MCP for standardised integrations — then the RAG ladder from baseline to Self-RAG, built as graphs.",
   thesis="An agent without tools is a chatbot. This part covers <strong>tool design</strong> — where the docstring is literally the prompt that drives selection — the ReAct loop wired by hand and then via <strong><code>create_agent</code></strong> (note: <code>create_react_agent</code> is deprecated in v1), error handling that returns <code>ToolMessage</code>s instead of crashing, and <strong>MCP</strong> as the emerging integration standard. Then the RAG ladder: naive → <strong>agentic</strong> (retrieval as a tool the model chooses) → <strong>CRAG</strong> (grade and correct) → <strong>Self-RAG</strong> (grade your own output), each as a LangGraph graph.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 5–6</b></span>\n          <span class="chip"><b>37</b> tracked topics</span>\n          <span class="chip">⏱ <b>~7–8h</b></span>\n          <span class="chip">🔧 tools · MCP · RAG</span>',
   prev=("Part 2 · Patterns, State &amp; Memory","Checkpointers, Store, HITL"), prevhref="LangGraph_Part2_State.html",
   nxt=("Part 4 · Multi-Agent &amp; Observability",["Supervisor, subgraphs, handoffs","LangSmith + trajectory eval"])),
 4: dict(file="LangGraph_Part4_MultiAgent.html", title="Multi-Agent &amp; Observability", pk="L7-8",
   groups=[("L7","Multi-Agent",[("g4-1","4.1 · Topologies"),("g4-2","4.2 · Subgraphs"),
     ("g4-3","4.3 · Handoffs &amp; context isolation"),("g4-4","4.4 · Orchestrator–worker capstone")]),
    ("L8","LangSmith",[("g4-5","4.5 · Tracing setup"),("g4-6","4.6 · Runs, traces &amp; spans"),
     ("g4-7","4.7 · Datasets &amp; evaluators"),("g4-8","4.8 · Trajectory evaluation ⭐"),("g4-9","4.9 · Interview focus")])],
   h1="Teams of agents, and proving they work", sub="Multi-agent topologies (network, supervisor, hierarchical), subgraphs and handoffs — then LangSmith tracing, datasets, and the trajectory evaluation that senior interviews hinge on.",
   thesis="Two topics that decide senior offers. First <strong>multi-agent architecture</strong>: the topology menu (network / supervisor / supervisor-as-tools / hierarchical / handoff), subgraphs for reuse, and what context transfers on a handoff. Then <strong>observability</strong> — reportedly the round that fails the most candidates. Final-answer accuracy is <em>not</em> enough for agents: you evaluate the <strong>trajectory</strong> (golden paths, step-level tool choice, cost and step-count as first-class metrics), and you build datasets from real production traces.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 7–8</b></span>\n          <span class="chip"><b>27</b> tracked topics</span>\n          <span class="chip">⏱ <b>~6–7h</b></span>\n          <span class="chip">📊 LangSmith</span>',
   prev=("Part 3 · Tools, MCP &amp; RAG","create_agent, CRAG, Self-RAG"), prevhref="LangGraph_Part3_Tools.html",
   nxt=("Part 5 · Production Engineering",["Durability &amp; idempotency","Streaming, deploy, security"])),
 5: dict(file="LangGraph_Part5_Production.html", title="Production Engineering", pk="L9-10",
   groups=[("L9","Production",[("g5-1","5.1 · Durability &amp; recovery"),("g5-2","5.2 · Idempotency ⭐"),
     ("g5-3","5.3 · Reliability primitives"),("g5-4","5.4 · Node caching"),("g5-5","5.5 · Streaming"),
     ("g5-6","5.6 · Deployment"),("g5-7","5.7 · Cost, latency &amp; security"),("g5-8","5.8 · Testing")]),
    ("L10","Frontier",[("g5-9","5.9 · Functional API &amp; Pregel"),("g5-10","5.10 · Context engineering"),
     ("g5-11","5.11 · Frontier topics"),("g5-12","5.12 · Interview focus")])],
   h1="Shipping agents that survive contact with production", sub="Durability modes, the idempotency answer that lands senior offers, retries and caching, streaming, deployment, cost and security — plus the frontier topics worth naming.",
   thesis="The gap between a demo and a system you'd put on-call for. <strong>Checkpoints make state recoverable — they do not make side effects exactly-once</strong>; knowing that, and adding idempotency keys so a resumed run can't re-charge a card, is one of the strongest answers you can give. Also: durability modes, retry policies and node caching, the five streaming modes (perceived latency <em>is</em> latency), deployment and double-texting, cost routing, prompt-injection defence, and how to unit-test a graph by stubbing the LLM.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 9–10</b></span>\n          <span class="chip"><b>44</b> tracked topics</span>\n          <span class="chip">⏱ <b>~7–8h</b></span>\n          <span class="chip">🚀 production</span>',
   prev=("Part 4 · Multi-Agent &amp; Observability","Supervisor, subgraphs, LangSmith"), prevhref="LangGraph_Part4_MultiAgent.html",
   nxt=("Part 6 · Interview Q&amp;A Bank",["46 questions + 7 traps","6 system-design scenarios"])),
 6: dict(file="LangGraph_Part6_QABank.html", title="Interview Q&amp;A Bank", pk="QA",
   groups=[("QA","Interview Q&amp;A",[("g6-1","6.1 · Conceptual"),("g6-2","6.2 · LangGraph mechanics"),
     ("g6-3","6.3 · State &amp; memory"),("g6-4","6.4 · HITL &amp; production"),("g6-5","6.5 · Tools &amp; RAG"),
     ("g6-6","6.6 · Evaluation"),("g6-7","6.7 · The trap questions ⭐"),("g6-8","6.8 · System design scenarios"),
     ("g6-9","6.9 · Gotchas cheat sheet"),("g6-10","6.10 · Portfolio &amp; study plan")])],
   h1="The question bank", sub="Every high-frequency LangGraph interview question with a model answer — conceptual, mechanics, state, HITL, tools, evaluation — plus the seven trap questions, six system-design scenarios, and the gotchas cheat sheet.",
   thesis="The consolidated <strong>drill</strong>. Read the question, answer out loud, <em>then</em> expand the model answer and compare. The <strong>trap questions</strong> (§6.7) deserve special attention — they're designed to separate people who've read about LangGraph from people who've shipped it, and each has a naive answer that sounds right and a correct answer that doesn't. Every answer links back to the section in Parts 1–5 where it's derived.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Q&amp;A Bank</b></span>\n          <span class="chip"><b>60+</b> questions</span>\n          <span class="chip">7 <b>traps</b></span>\n          <span class="chip">⏱ <b>~4–5h</b> drill</span>',
   prev=("Part 5 · Production Engineering","Durability, streaming, security"), prevhref="LangGraph_Part5_Production.html",
   nxt=("Learning Hub","All subjects")),
}

def build(pn):
    cfg = PARTS[pn]
    html = SRC.read_text()

    # content region -> marker
    s = html.index("</section>", html.index('id="tracker"')) + len("</section>")
    e = html.index("      <!-- PART NAV -->")
    html = html[:s] + "\n\n<!--CONTENT_INSERT-->\n\n      " + html[e:]

    plain_title = re.sub("&amp;", "&", cfg["title"])
    html = html.replace("<title>RAG Interview Prep — Part 1: Foundations</title>",
                        f"<title>LangGraph &amp; Agentic AI — Part {pn}: {cfg['title']}</title>")
    html = html.replace('<div class="tt"><small>Part 1 / 6</small>Foundations</div>',
                        f'<div class="tt"><small>Part {pn} / 6</small>{cfg["title"]}</div>')
    html = html.replace('<div class="brand-txt">RAG Prep<small>Knowledge Base</small></div>',
                        '<div class="brand-txt">LangGraph<small>Agentic AI Prep</small></div>')
    html = html.replace('<div class="k">Part 1 of 6</div>\n      <div class="v">Foundations</div>',
                        f'<div class="k">Part {pn} of 6</div>\n      <div class="v">{cfg["title"]}</div>')

    # nav
    grp = ""
    for pk, head, links in cfg["groups"]:
        lis = "\n".join(f'          <li><a href="#{i}">{t}</a></li>' for i, t in links)
        grp += (f'      <div class="grp">\n'
                f'        <button class="ghead" data-t><span class="num">{pk}</span> {head} <span class="chev">▾</span></button>\n'
                f'        <ul class="links">\n{lis}\n        </ul>\n      </div>\n')
    nav = ('<nav class="toc" id="toc">\n'
           '      <div class="grp">\n'
           '        <button class="ghead" data-t><span class="num">◆</span> Progress Tracker</button>\n'
           '        <ul class="links"><li><a href="#tracker">Master tracker (all parts)</a></li></ul>\n'
           '      </div>\n' + grp +
           '      <div class="grp">\n'
           '        <button class="ghead" data-t><span class="num">↩</span> Hub</button>\n'
           '        <ul class="links"><li><a href="../index.html">← All subjects</a></li>'
           '<li><a href="index.html">← LangGraph home</a></li></ul>\n      </div>\n    </nav>')
    html = re.sub(r'<nav class="toc" id="toc">.*?</nav>', lambda m: nav, html, count=1, flags=re.DOTALL)

    html = re.sub(r'<div class="sb-foot">.*?</div>',
        f'<div class="sb-foot">\n      LangGraph &amp; Agentic AI<br>Part {pn} — {cfg["title"]}<br>© your study kit\n    </div>',
        html, count=1, flags=re.DOTALL)

    hero = (f'<header class="hero">\n'
      f'        <div class="eyebrow">Part {pn} of 6 · {cfg["title"]}</div>\n'
      f'        <h1 class="title">{cfg["h1"]}\n          <span class="sub">{cfg["sub"]}</span>\n        </h1>\n'
      f'        <p class="thesis">{cfg["thesis"]}</p>\n'
      f'        <div class="meta-chips">\n          {cfg["chips"]}\n        </div>\n      </header>')
    html = re.sub(r'<header class="hero">.*?</header>', lambda m: hero, html, count=1, flags=re.DOTALL)

    nxt_l = "".join(f"<li>{x}</li>" for x in (cfg["nxt"][1] if len(cfg["nxt"]) > 1 and isinstance(cfg["nxt"][1], list) else []))
    nxt_href = "index.html" if cfg["nxt"][0] == "Learning Hub" else PARTS.get(pn+1, {}).get("file", "index.html")
    partnav = (f'<nav class="partnav">\n'
      f'        <div class="pcard"><div class="k">Previously</div><div class="t"><a href="{cfg["prevhref"]}">{cfg["prev"][0]}</a></div><ul><li>{cfg["prev"][1]}</li></ul></div>\n'
      f'        <div class="pcard"><div class="k">You are here</div><div class="t">Part {pn} · {cfg["title"]}</div></div>\n'
      f'        <div class="pcard next"><div class="k">Coming next</div><div class="t"><a href="{nxt_href}">{cfg["nxt"][0]}</a></div><ul>{nxt_l}</ul></div>\n'
      f'      </nav>')
    html = re.sub(r'<nav class="partnav">.*?</nav>', lambda m: partnav, html, count=1, flags=re.DOTALL)

    html = re.sub(r'<div class="doc-foot">.*?</div>',
      f'<div class="doc-foot">\n        LangGraph &amp; Agentic AI — Part {pn} of 6 · {cfg["title"]}<br>\n'
      f'        API-current for <b>LangGraph v1</b> (Oct 2025 LTS): <code style="color:#8892a0">create_agent</code> replaces the deprecated '
      f'<code style="color:#8892a0">create_react_agent</code>.<br>\n'
      f'        Progress is stored locally under key <code style="color:#8892a0">lgPrepStatus_v1</code> and is shared by every part of this subject.\n      </div>',
      html, count=1, flags=re.DOTALL)

    # ---- swap tracker payload ----
    _ph = "const PHASES = " + json.dumps(PHASES, ensure_ascii=False) + ";"
    _or = "const ORDER = " + json.dumps(ORDER) + ";"
    _tk = "const TRACKER = " + tracker_js + ";"
    html = re.sub(r'const PHASES = \{.*?\};', lambda m: _ph, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const ORDER = \[.*?\];', lambda m: _or, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const TRACKER = \[.*?\n\];', lambda m: _tk, html, count=1, flags=re.DOTALL)
    html = html.replace('const LS_KEY="ragPrepStatus_v1";', 'const LS_KEY="lgPrepStatus_v1";')
    html = html.replace("206", str(TOTAL))
    html = html.replace("all 6 parts", "all 6 parts").replace(
        "One tracker for the entire resource — all 6 parts across all 6 parts.",
        "One tracker for the entire subject — every topic across all 6 parts.")
    html = re.sub(r'<p class="tk-sub">.*?</p>',
      f'<p class="tk-sub">One tracker for the whole LangGraph subject — all {TOTAL} topics across all 6 parts. '
      f'Set a status on any row; your progress saves in this browser and prints as a clean checklist.</p>',
      html, count=1, flags=re.DOTALL)

    (HERE / cfg["file"]).write_text(html)
    assert "<!--CONTENT_INSERT-->" in html and "ragPrepStatus" not in html
    print(f"  wrote {cfg['file']} ({len(html):,} bytes)")

if __name__ == "__main__":
    args = sys.argv[1:]
    for p in ([int(a) for a in args] if args else PARTS):
        build(p)
