#!/usr/bin/env python3
"""Build LangChain subject shells: reuse the RAG/LangGraph design system,
swap in a LangChain tracker (own localStorage key) and per-part chrome."""
import re, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent
SRC  = SITE / "rag" / "RAG_Interview_Prep_Part1_Foundations.html"
MD   = SITE.parent / "langchain-llm-prompt-study-guide.md"

LEVEL_KEY = {
 "Level 0 — LLM Fundamentals": ("l0","Level 0 · LLM Fundamentals"),
 "Level 1 — Prompt Engineering (in depth)": ("l1","Level 1 · Prompt Engineering"),
 "Level 2 — Prompt Security & Context Engineering": ("l2","Level 2 · Prompt Security &amp; Context"),
 "Level 3 — Architecture & Packages": ("l3","Level 3 · Architecture &amp; Packages"),
 "Level 4 — Models & Messages": ("l4","Level 4 · Models &amp; Messages"),
 "Level 5 — Prompts & Templates in LangChain": ("l5","Level 5 · Prompts &amp; Templates"),
 "Level 6 — Structured Output & Parsers": ("l6","Level 6 · Structured Output"),
 "Level 7 — Runnables & LCEL": ("l7","Level 7 · Runnables &amp; LCEL"),
 "Level 8 — Tools, Agents & Middleware": ("l8","Level 8 · Tools, Agents &amp; Middleware"),
 "Level 9 — Retrieval & RAG": ("l9","Level 9 · Retrieval &amp; RAG"),
 "Level 10 — Memory & State": ("l10","Level 10 · Memory &amp; State"),
 "Level 11 — Production Engineering": ("l11","Level 11 · Production Engineering"),
 "Level 12 — Evaluation & Observability": ("l12","Level 12 · Evaluation &amp; Observability"),
 "Level 13 — Advanced & Frontier": ("l13","Level 13 · Advanced &amp; Frontier"),
}
CAT = {"l0":"Theory","l1":"Theory","l2":"Theory","l3":"Theory","l4":"Practical","l5":"Practical",
       "l6":"Practical","l7":"Practical","l8":"Practical","l9":"Practical","l10":"Theory",
       "l11":"Practical","l12":"Practical","l13":"Theory"}
HIGH = {"l1","l3","l6","l7","l8","l10"}

def clean(s):
    s = re.sub(r'`([^`]*)`', r'\1', s)
    s = re.sub(r'\*\*([^*]*)\*\*', r'\1', s)
    s = re.sub(r'\*([^*]*)\*', r'\1', s)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    return re.sub(r'\s+',' ',s).strip(" .")

rows, cur = [], None
for line in MD.read_text().split("\n"):
    m = re.match(r'^## (.+)$', line)
    if m: cur = LEVEL_KEY.get(m.group(1).strip())
    if cur and re.match(r'^\s*- \[ \]', line):
        t = clean(re.sub(r'^\s*- \[ \]\s*','',line))
        if t: rows.append([cur[0], CAT[cur[0]], "High" if cur[0] in HIGH else "Medium", t])

IV = [("iv","Interview Prep","High",t) for t in [
 "High-frequency: LangChain conceptual (what it solves, when NOT to use it, 1.0 changes)",
 "High-frequency: Runnables &amp; LCEL (interface, pipe, LCEL vs LangGraph)",
 "High-frequency: Models, messages &amp; prompts (templates, few-shot at scale, content blocks)",
 "High-frequency: Structured output (with_structured_output vs parsers, strategies)",
 "High-frequency: Tools, agents &amp; middleware (tool choice, hooks, bounding cost)",
 "High-frequency: Retrieval, memory &amp; production (RAG chain, memory in 2026, cost, testing)",
 "The 12 trap questions (answered correctly, out loud)",
 "Prompt engineering questions (18) — taxonomy, exemplars, reasoning models, injection",
]]
SD = [("sd","Interview Prep","High",t) for t in [
 "System design: Customer support assistant","System design: Document extraction pipeline (100k PDFs)",
 "System design: Multi-provider abstraction","System design: Real-time streaming chat",
 "System design: Internal knowledge assistant with RBAC","System design: Prompt-optimisation workflow for a team",
 "System design: 70% cost-reduction mandate",
]]
CQ = [("cq","Practical","High",t) for t in [
 "Code: RAG chain in LCEL with format_docs","Code: with_structured_output over a Pydantic schema",
 "Code: @tool with args_schema + ToolMessage error handling","Code: create_agent with middleware (summarization + call limit)",
 "Code: few-shot with SemanticSimilarityExampleSelector","Code: trim_messages with correct boundaries",
 "Code: RunnableLambda + RunnableBranch router","Code: .with_retry() and .with_fallbacks()",
 "Code: custom BaseCallbackHandler logging token cost","Code: streaming tokens filtered to assistant text",
]]
PP = [("pp","Project","High",t) for t in [
 "Project 1: Prompt technique lab (8 techniques, measured)","Project 2: Structured extraction service",
 "Project 3: Multi-provider chat app","Project 4: RAG assistant in pure LCEL",
 "Project 5: Agent with middleware stack","Project 6: Instrumented + optimised app (LangSmith, CI gate)",
]]
rows += [[k,c,p,t] for k,c,p,t in IV+SD+CQ+PP]

PHASES = {k:v for k,v in LEVEL_KEY.values()}
PHASES.update({"iv":"Interview Q&amp;A Bank","sd":"System Design Scenarios","cq":"Coding Questions","pp":"Portfolio Projects"})
ORDER = [f"l{i}" for i in range(14)] + ["iv","sd","cq","pp"]
tracker_js = "[\n" + ",\n".join(f'[{i+1},"{r[0]}","{r[1]}","{r[2]}",0,{json.dumps(r[3])}]' for i,r in enumerate(rows)) + "\n]"
TOTAL = len(rows)
print(f"tracker: {TOTAL} items / {len(ORDER)} groups")

P = {
 1: dict(file="LangChain_Part1_LLMFoundations.html", title="LLM Foundations", pk="L0",
   groups=[("L0","LLM Fundamentals",[("c1-1","1.1 · Tokens &amp; tokenization"),("c1-2","1.2 · The context window"),
     ("c1-3","1.3 · Decoding &amp; sampling"),("c1-4","1.4 · Model families"),("c1-5","1.5 · Core capabilities"),
     ("c1-6","1.6 · Hallucination"),("c1-7","1.7 · Fine-tune vs prompt vs RAG"),("c1-8","1.8 · Interview focus")])],
   h1="The machine under the framework",
   sub="Tokens, context windows, decoding parameters, tool calling, and why models hallucinate — the fundamentals every LangChain question eventually reduces to.",
   thesis="Interviewers open here because it separates people who <em>understand the machine</em> from people who call an API. Every framework question — why your app costs double in Hindi, why <code>temperature=0</code> still returns different JSON, why the answer in the middle of your context got ignored — resolves to something in this part. We cover <strong>tokenization</strong>, the <strong>context window</strong> (and lost-in-the-middle), <strong>decoding parameters</strong>, <strong>tool calling and structured output</strong> at the API level, the <strong>mechanism</strong> of hallucination, and the fine-tune / prompt / retrieve decision.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 0</b></span>\n          <span class="chip"><b>36</b> topics</span>\n          <span class="chip">⏱ <b>~4–5h</b></span>',
   prev=("Learning Hub","All subjects"), prevhref="../index.html",
   nxt=("Part 2 · Prompt Engineering",["6-category taxonomy","Injection &amp; context engineering"])),
 2: dict(file="LangChain_Part2_PromptEngineering.html", title="Prompt Engineering", pk="L1-2",
   groups=[("L1","Prompt Engineering",[("c2-1","2.1 · Anatomy of a prompt"),("c2-2","2.2 · The 6 categories ⭐"),
     ("c2-3","2.3 · Zero-shot techniques"),("c2-4","2.4 · Few-shot &amp; ICL"),("c2-5","2.5 · Thought generation"),
     ("c2-6","2.6 · Decomposition"),("c2-7","2.7 · Ensembling"),("c2-8","2.8 · Self-criticism"),
     ("c2-9","2.9 · Reasoning models ⭐"),("c2-10","2.10 · Automated optimisation"),("c2-11","2.11 · Evaluating prompts")]),
    ("L2","Security &amp; Context",[("c2-12","2.12 · Injection &amp; jailbreaking"),("c2-13","2.13 · Context engineering"),
     ("c2-14","2.14 · Interview focus")])],
   h1="Prompting as an engineering discipline",
   sub="The Prompt Report's 58 techniques in 6 categories — few-shot, thought generation, decomposition, ensembling, self-criticism — plus prompting reasoning models, injection defence, and context engineering.",
   thesis="In 2026 prompting stopped being tips and became a <strong>reproducible discipline</strong>. This part is built on <strong>The Prompt Report</strong> (a systematic review of 1,500+ papers cataloguing <strong>58 text techniques in 6 categories</strong>) rather than a listicle — so you learn a framework you can reason from. It covers the <strong>six exemplar factors</strong> that decide whether few-shot helps or hurts, when chain-of-thought <em>backfires</em>, how prompting changes for <strong>reasoning models</strong>, automated optimisation (DSPy), and the security half: direct vs <strong>indirect</strong> injection, and context as a budget you allocate.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 1–2</b></span>\n          <span class="chip"><b>60</b> topics</span>\n          <span class="chip">⏱ <b>~7–8h</b></span>\n          <span class="chip">📐 6-category taxonomy</span>',
   prev=("Part 1 · LLM Foundations","Tokens, context, decoding"), prevhref="LangChain_Part1_LLMFoundations.html",
   nxt=("Part 3 · LangChain Core",["Packages, models, messages","Structured output, LCEL"])),
 3: dict(file="LangChain_Part3_Core.html", title="LangChain Core", pk="L3-7",
   groups=[("L3–L4","Architecture &amp; Models",[("c3-1","3.1 · What LangChain is for"),("c3-2","3.2 · The package split ⭐"),
     ("c3-3","3.3 · Chat models"),("c3-4","3.4 · Messages"),("c3-5","3.5 · Standard content blocks ⭐")]),
    ("L5–L7","Prompts, Output &amp; LCEL",[("c3-6","3.6 · Prompt templates"),("c3-7","3.7 · Few-shot in LangChain"),
     ("c3-8","3.8 · with_structured_output ⭐"),("c3-9","3.9 · Output parsers"),("c3-10","3.10 · Runnables"),
     ("c3-11","3.11 · LCEL"),("c3-12","3.12 · LCEL vs LangGraph ⭐"),("c3-13","3.13 · Interview focus")])],
   h1="The 1.x surface, minus the tutorial rot",
   sub="What actually lives in <code>langchain</code> after 1.0 gutted it, plus models, messages, content blocks, prompt templates, structured output strategies, Runnables and LCEL.",
   thesis="LangChain 1.0 <strong>gutted the <code>langchain</code> package</strong> — <code>LLMChain</code>, <code>ConversationChain</code>, <code>AgentExecutor</code>, the old memory classes and retrievers all moved to <strong><code>langchain-classic</code></strong>. Nearly every course from 2023–24 teaches imports that no longer live where they say. This part is the current surface: the <strong>package split</strong>, chat models and <code>init_chat_model</code>, messages (<code>.text</code> is now a <em>property</em>), <strong>standard content blocks</strong>, prompt templates and example selectors, <strong><code>with_structured_output</code></strong> with its two strategies, and <strong>Runnables/LCEL</strong> — including the question everyone gets asked: LCEL or LangGraph?",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 3–7</b></span>\n          <span class="chip"><b>78</b> topics</span>\n          <span class="chip">⏱ <b>~8–9h</b></span>\n          <span class="chip">🐍 LangChain <b>1.3</b></span>',
   prev=("Part 2 · Prompt Engineering","Taxonomy, injection, context"), prevhref="LangChain_Part2_PromptEngineering.html",
   nxt=("Part 4 · Tools, Agents &amp; RAG",["create_agent + middleware","Retrieval composition"])),
 4: dict(file="LangChain_Part4_Agents.html", title="Tools, Agents &amp; RAG", pk="L8-9",
   groups=[("L8","Tools &amp; Agents",[("c4-1","4.1 · Defining tools"),("c4-2","4.2 · create_agent ⭐"),
     ("c4-3","4.3 · Middleware ⭐⭐"),("c4-4","4.4 · Agent patterns &amp; limits")]),
    ("L9","Retrieval",[("c4-5","4.5 · The RAG pipeline"),("c4-6","4.6 · Retriever composition"),
     ("c4-7","4.7 · Building the RAG chain"),("c4-8","4.8 · Interview focus")])],
   h1="Giving it hands — and a harness",
   sub="Tool design where the docstring is the prompt, the <code>create_agent</code> API, the middleware catalogue that replaces half of what you'd hand-build, and retrieval composition in LangChain.",
   thesis="An agent is a model plus tools plus a loop — and in LangChain 1.x the loop comes from LangGraph while the <em>harness</em> comes from <strong>middleware</strong>. That middleware catalogue is the single most under-taught part of modern LangChain: <strong>19 provider-agnostic middleware</strong> covering summarization, human-in-the-loop, <strong>call limits</strong> (bounding runaway cost), <strong>tool selection</strong> (when you have too many tools), PII, retries, fallbacks, and <strong>tool emulation for testing</strong>. Plus the retrieval surface: loaders, splitters, ensemble/hybrid retrievers, compression, and building a RAG chain in LCEL.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 8–9</b></span>\n          <span class="chip"><b>40</b> topics</span>\n          <span class="chip">⏱ <b>~6–7h</b></span>\n          <span class="chip">🔧 19 middleware</span>',
   prev=("Part 3 · LangChain Core","Packages, LCEL, structured output"), prevhref="LangChain_Part3_Core.html",
   nxt=("Part 5 · Memory &amp; Production",["The memory deprecation chain","Cost, caching, security, eval"])),
 5: dict(file="LangChain_Part5_Production.html", title="Memory &amp; Production", pk="L10-13",
   groups=[("L10","Memory",[("c5-1","5.1 · The deprecation chain ⭐"),("c5-2","5.2 · Context window management")]),
    ("L11–L13","Production",[("c5-3","5.3 · Streaming"),("c5-4","5.4 · Callbacks &amp; tracing"),
     ("c5-5","5.5 · Caching"),("c5-6","5.6 · Reliability"),("c5-7","5.7 · Cost &amp; latency"),
     ("c5-8","5.8 · Security &amp; CVEs"),("c5-9","5.9 · Testing &amp; deployment"),
     ("c5-10","5.10 · Evaluation"),("c5-11","5.11 · Frontier"),("c5-12","5.12 · Interview focus")])],
   h1="Shipping it, and keeping it shipped",
   sub="The three-generation memory deprecation chain, context management, streaming, caching, reliability, cost control, security (including CVEs), testing, and evaluation.",
   thesis="Two things separate a demo from a system you'd be on call for. First <strong>memory</strong>, which in LangChain is <em>three deprecations deep</em> — <code>ConversationBufferMemory</code> → <code>RunnableWithMessageHistory</code> → <strong>LangGraph persistence</strong> — and almost everyone answers with generation one. Then <strong>production</strong>: streaming and perceived latency, callbacks and trace redaction, caching (including the semantic-cache staleness trap), retries and fallbacks, where the money actually goes, <strong>dependency security</strong> (yes, CVEs are an interview topic now), and testing an LLM app deterministically in CI.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 10–13</b></span>\n          <span class="chip"><b>62</b> topics</span>\n          <span class="chip">⏱ <b>~7–8h</b></span>\n          <span class="chip">🚀 production</span>',
   prev=("Part 4 · Tools, Agents &amp; RAG","Middleware, retrieval"), prevhref="LangChain_Part4_Agents.html",
   nxt=("Part 6 · Interview Q&amp;A Bank",["36 questions + 12 traps","7 system designs + 10 coding"])),
 6: dict(file="LangChain_Part6_QABank.html", title="Interview Q&amp;A Bank", pk="QA",
   groups=[("QA","Interview Q&amp;A",[("c6-1","6.1 · LangChain conceptual"),("c6-2","6.2 · Runnables &amp; LCEL"),
     ("c6-3","6.3 · Models, messages, prompts"),("c6-4","6.4 · Structured output"),("c6-5","6.5 · Tools, agents &amp; middleware"),
     ("c6-6","6.6 · Retrieval &amp; memory"),("c6-7","6.7 · Production"),("c6-8","6.8 · The 12 traps ⭐"),
     ("c6-9","6.9 · Prompt engineering Q&amp;A"),("c6-10","6.10 · System design"),("c6-11","6.11 · Coding questions"),
     ("c6-12","6.12 · Deprecation map &amp; gotchas")])],
   h1="The question bank",
   sub="Every high-frequency LangChain, LLM, and prompt-engineering question with a model answer — plus the 12 trap questions, 7 system-design scenarios, 10 coding questions, and the deprecation map.",
   thesis="The consolidated <strong>drill</strong>. Read the question, answer out loud, <em>then</em> expand and compare. The <strong>trap questions</strong> (§6.8) deserve the most attention — two things get people rejected in LangChain interviews: quoting <strong>0.x APIs</strong> as if they're current, and treating <strong>prompting as vibes</strong> instead of a measured discipline. The deprecation map in §6.12 is the highest-yield thing on this page.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Q&amp;A Bank</b></span>\n          <span class="chip"><b>85+</b> questions</span>\n          <span class="chip">12 <b>traps</b></span>\n          <span class="chip">⏱ <b>~5h</b> drill</span>',
   prev=("Part 5 · Memory &amp; Production","Memory chain, cost, security"), prevhref="LangChain_Part5_Production.html",
   nxt=("Learning Hub",["All subjects"])),
}

def build(pn):
    c = P[pn]; html = SRC.read_text()
    s = html.index("</section>", html.index('id="tracker"')) + len("</section>")
    e = html.index("      <!-- PART NAV -->")
    html = html[:s] + "\n\n<!--CONTENT_INSERT-->\n\n      " + html[e:]
    html = html.replace("<title>RAG Interview Prep — Part 1: Foundations</title>",
                        f"<title>LangChain &amp; Prompt Engineering — Part {pn}: {c['title']}</title>")
    html = html.replace('<div class="tt"><small>Part 1 / 6</small>Foundations</div>',
                        f'<div class="tt"><small>Part {pn} / 6</small>{c["title"]}</div>')
    html = html.replace('<div class="brand-txt">RAG Prep<small>Knowledge Base</small></div>',
                        '<div class="brand-txt">LangChain<small>+ Prompt Engineering</small></div>')
    html = html.replace('<div class="k">Part 1 of 6</div>\n      <div class="v">Foundations</div>',
                        f'<div class="k">Part {pn} of 6</div>\n      <div class="v">{c["title"]}</div>')
    grp = ""
    for pk, head, links in c["groups"]:
        lis = "\n".join(f'          <li><a href="#{i}">{t}</a></li>' for i,t in links)
        grp += (f'      <div class="grp">\n        <button class="ghead" data-t><span class="num">{pk}</span> {head} '
                f'<span class="chev">▾</span></button>\n        <ul class="links">\n{lis}\n        </ul>\n      </div>\n')
    nav = ('<nav class="toc" id="toc">\n      <div class="grp">\n'
           '        <button class="ghead" data-t><span class="num">◆</span> Progress Tracker</button>\n'
           '        <ul class="links"><li><a href="#tracker">Master tracker (all parts)</a></li></ul>\n      </div>\n'
           + grp + '      <div class="grp">\n        <button class="ghead" data-t><span class="num">↩</span> Hub</button>\n'
           '        <ul class="links"><li><a href="../index.html">← All subjects</a></li>'
           '<li><a href="index.html">← LangChain home</a></li></ul>\n      </div>\n    </nav>')
    html = re.sub(r'<nav class="toc" id="toc">.*?</nav>', lambda m: nav, html, count=1, flags=re.DOTALL)
    html = re.sub(r'<div class="sb-foot">.*?</div>',
        f'<div class="sb-foot">\n      LangChain &amp; Prompt Eng.<br>Part {pn} — {c["title"]}<br>© your study kit\n    </div>',
        html, count=1, flags=re.DOTALL)
    hero = (f'<header class="hero">\n        <div class="eyebrow">Part {pn} of 6 · {c["title"]}</div>\n'
      f'        <h1 class="title">{c["h1"]}\n          <span class="sub">{c["sub"]}</span>\n        </h1>\n'
      f'        <p class="thesis">{c["thesis"]}</p>\n        <div class="meta-chips">\n          {c["chips"]}\n        </div>\n      </header>')
    html = re.sub(r'<header class="hero">.*?</header>', lambda m: hero, html, count=1, flags=re.DOTALL)
    nl = "".join(f"<li>{x}</li>" for x in (c["nxt"][1] if isinstance(c["nxt"][1], list) else []))
    nh = "index.html" if c["nxt"][0]=="Learning Hub" else P.get(pn+1,{}).get("file","index.html")
    pnav = (f'<nav class="partnav">\n        <div class="pcard"><div class="k">Previously</div><div class="t">'
      f'<a href="{c["prevhref"]}">{c["prev"][0]}</a></div><ul><li>{c["prev"][1]}</li></ul></div>\n'
      f'        <div class="pcard"><div class="k">You are here</div><div class="t">Part {pn} · {c["title"]}</div></div>\n'
      f'        <div class="pcard next"><div class="k">Coming next</div><div class="t"><a href="{nh}">{c["nxt"][0]}</a></div><ul>{nl}</ul></div>\n      </nav>')
    html = re.sub(r'<nav class="partnav">.*?</nav>', lambda m: pnav, html, count=1, flags=re.DOTALL)
    html = re.sub(r'<div class="doc-foot">.*?</div>',
      f'<div class="doc-foot">\n        LangChain &amp; Prompt Engineering — Part {pn} of 6 · {c["title"]}<br>\n'
      f'        API-current as of <b>Aug 2026</b> — LangChain <b>1.3.14</b> · langchain-core ≥ <b>0.3.81</b> · Python 3.10–3.14. '
      f'Legacy 0.x APIs live in <code style="color:#8892a0">langchain-classic</code>.<br>\n'
      f'        Progress is stored locally under key <code style="color:#8892a0">lcPrepStatus_v1</code> and is shared by every part of this subject.\n      </div>',
      html, count=1, flags=re.DOTALL)
    _ph = "const PHASES = " + json.dumps(PHASES, ensure_ascii=False) + ";"
    _or = "const ORDER = " + json.dumps(ORDER) + ";"
    _tk = "const TRACKER = " + tracker_js + ";"
    html = re.sub(r'const PHASES = \{.*?\};', lambda m:_ph, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const ORDER = \[.*?\];', lambda m:_or, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const TRACKER = \[.*?\n\];', lambda m:_tk, html, count=1, flags=re.DOTALL)
    html = html.replace('const LS_KEY="ragPrepStatus_v1";','const LS_KEY="lcPrepStatus_v1";').replace("206",str(TOTAL))
    html = re.sub(r'<p class="tk-sub">.*?</p>',
      f'<p class="tk-sub">One tracker for the whole LangChain subject — all {TOTAL} topics across all 6 parts. '
      f'Set a status on any row; your progress saves in this browser and prints as a clean checklist.</p>',
      html, count=1, flags=re.DOTALL)
    (HERE/c["file"]).write_text(html)
    assert "<!--CONTENT_INSERT-->" in html and "ragPrepStatus" not in html
    print(f"  {c['file']} ({len(html):,}b)")

if __name__ == "__main__":
    for p in ([int(a) for a in sys.argv[1:]] or P): build(p)
