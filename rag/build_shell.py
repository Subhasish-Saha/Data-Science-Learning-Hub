#!/usr/bin/env python3
"""Generate a per-part shell from the Part 1 file: reuse CSS + tracker + JS,
swap the per-part chrome, and leave a <!--CONTENT_INSERT--> marker to fill."""
import re, sys, pathlib

OUT = pathlib.Path(__file__).resolve().parent
SRC = OUT / "RAG_Interview_Prep_Part1_Foundations.html"

# ---- per-part configuration ----
PARTS = {
  2: dict(
    file="RAG_Interview_Prep_Part2_Retrieval.html",
    part_title="Advanced Retrieval", pk="P2", phase_label="Phase 2",
    items="45–71",
    nav_head="Retrieval Quality",
    nav=[("s2-1","2.1 · Dense vs sparse"),("s2-2","2.2 · Hybrid search &amp; RRF"),
         ("s2-3","2.3 · RAG-Fusion"),("s2-4","2.4 · Reranking"),
         ("s2-5","2.5 · MMR &amp; diversity"),("s2-6","2.6 · Query transformation"),
         ("s2-7","2.7 · Metadata filtering"),("s2-8","2.8 · Better retrieval units"),
         ("s2-9","2.9 · Contextual compression"),("s2-10","2.10 · Lost-in-the-middle"),
         ("s2-11","2.11 · ColBERT / late interaction"),("s2-12","2.12 · Interview focus")],
    eyebrow="Part 2 of 6 · Advanced Retrieval",
    h1="Making retrieval actually good",
    sub="Everything you bolt onto naive RAG's online lane — hybrid search, fusion, reranking, query rewriting, and smarter retrieval units — to turn “vaguely relevant” into “exactly right.”",
    thesis="Naive RAG's weakness is <strong>retrieval</strong>: dense search alone misses exact terms, ranks imperfectly, and returns redundant or context-poor chunks. Part 2 is the toolkit that fixes each failure — <em>hybrid</em> search for exact matches, <em>RRF</em> to fuse rankings, <em>rerankers</em> to fix ordering, <em>query transformation</em> to bridge the vocabulary gap, and <em>parent/contextual</em> retrieval to restore lost context. These are the first things you add in production and the most common Phase-2 interview territory.",
    chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Phase 2</b></span>\n          <span class="chip"><b>27</b> tracked topics</span>\n          <span class="chip">⏱ <b>~5–7h</b> deep read</span>\n          <span class="chip">\U0001f40d runnable <b>Python</b></span>\n          <span class="chip"><span class="dot" style="background:var(--gold)"></span>4 <b>added</b> topics</span>',
    prev=("Part 1 · Foundations","Prereqs + naive RAG pipeline"),
    nxt=("Part 3 · Alternative &amp; Agentic",["GraphRAG, multi-hop, text-to-SQL","Self-RAG, CRAG, Adaptive RAG"]),
  ),
  3: dict(
    file="RAG_Interview_Prep_Part3_Architectures.html",
    part_title="Alternative &amp; Agentic", pk="P3", phase_label="Phase 3 + Phase 4",
    items="72–106", here_label="GraphRAG, agentic, adaptive",
    groups=[
      ("P3","Structured &amp; Graph",[
        ("s3-1","3.1 · GraphRAG"),("s3-2","3.2 · Multi-hop retrieval"),
        ("s3-3","3.3 · Text-to-SQL / structured"),("s3-4","3.4 · Multimodal RAG"),
        ("s3-5","3.5 · Hierarchical RAG")]),
      ("P4","Agentic &amp; Adaptive",[
        ("s3-6","3.6 · Agentic RAG"),("s3-7","3.7 · Self-RAG"),
        ("s3-8","3.8 · Corrective RAG"),("s3-9","3.9 · Adaptive RAG &amp; routing"),
        ("s3-10","3.10 · Agentic patterns"),("s3-11","3.11 · Cost &amp; interview focus")]),
    ],
    eyebrow="Part 3 of 6 · Alternative &amp; Agentic Architectures",
    h1="When vectors aren't enough",
    sub="Retrieval beyond similarity search — knowledge graphs, SQL, images, hierarchy — and RAG that <em>thinks</em>: agents that decide when and what to retrieve, grade their own results, and route by difficulty.",
    thesis="Even a perfect vector pipeline (Part 2) has walls: it can't answer “who connects A to B across 500 emails” (relationships), can't compute “average revenue by region” (structured math), and can't read a chart. <strong>Phase 3</strong> reaches for the right tool — GraphRAG, text-to-SQL, multimodal, hierarchy. <strong>Phase 4</strong> hands the LLM the controls — <em>agentic</em> retrieval loops, <em>Self-RAG</em> reflection, <em>Corrective</em> RAG fallbacks, and <em>Adaptive</em> routing that spends compute only when the query demands it. Power with a price tag: agentic loops cost 3–10× tokens and 2–5× latency, so knowing <em>when not to</em> is half the skill.",
    chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Phase 3 + 4</b></span>\n          <span class="chip"><b>35</b> tracked topics</span>\n          <span class="chip">⏱ <b>~7–9h</b> deep read</span>\n          <span class="chip">\U0001f40d LangGraph + <b>Python</b></span>\n          <span class="chip">\U0001f578️ graphs · agents · routing</span>',
    prev=("Part 2 · Advanced Retrieval","Hybrid, rerank, HyDE, MMR"),
    nxt=("Part 4 · Evaluation &amp; Production",["Metrics, RAGAS, LLM-as-judge","Caching, guardrails, monitoring"]),
  ),
  4: dict(
    file="RAG_Interview_Prep_Part4_Evaluation.html",
    part_title="Evaluation &amp; Production", pk="P5", phase_label="Phase 5",
    items="107–162", here_label="Metrics, RAGAS, guardrails, ops",
    groups=[
      ("P5","Evaluation",[
        ("s4-1","4.1 · Retrieval metrics"),("s4-2","4.2 · Generation metrics"),
        ("s4-3","4.3 · RAGAS"),("s4-4","4.4 · TruLens &amp; DeepEval"),
        ("s4-5","4.5 · Golden test sets"),("s4-6","4.6 · LLM-as-judge"),
        ("s4-7","4.7 · Hallucination &amp; abstention")]),
      ("OPS","Production &amp; Ops",[
        ("s4-8","4.8 · Latency &amp; cost"),("s4-9","4.9 · Caching"),
        ("s4-10","4.10 · Security &amp; guardrails"),("s4-11","4.11 · Monitoring &amp; drift"),
        ("s4-12","4.12 · Interview focus")]),
    ],
    eyebrow="Part 4 of 6 · Evaluation, Observability &amp; Production",
    h1="Knowing it works — and keeping it working",
    sub="The metrics, frameworks, and production disciplines that separate a demo from a system you'd stake your job on: retrieval &amp; generation metrics, RAGAS / TruLens / DeepEval, LLM-as-judge, caching, guardrails, and monitoring.",
    thesis="A RAG demo takes an afternoon; a RAG system you'd trust in production takes <strong>evaluation and observability</strong>. This is the most-neglected and most-interviewed phase. First you learn to <em>measure</em> — retrieval metrics (recall@k, MRR, NDCG), generation metrics (the RAG triad: faithfulness, answer + context relevance), and the frameworks that automate them. Then you learn to <em>run it</em>: budget latency and cost, cache the expensive steps, defend against prompt injection and data leakage, enforce access control, and monitor for the silent quality drift that degrades RAG over time.",
    chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Phase 5</b> · largest</span>\n          <span class="chip"><b>56</b> tracked topics</span>\n          <span class="chip">⏱ <b>~8–10h</b> deep read</span>\n          <span class="chip">\U0001f40d RAGAS + <b>Python</b></span>\n          <span class="chip"><span class="dot" style="background:var(--gold)"></span>1 <b>added</b> topic</span>',
    prev=("Part 3 · Alternative &amp; Agentic","GraphRAG, agentic, adaptive"),
    nxt=("Part 5 · System Design &amp; Reference",["Scaling, cost, vector-DB choice","Capstone + tools + papers"]),
  ),
  5: dict(
    file="RAG_Interview_Prep_Part5_SystemDesign.html",
    part_title="System Design &amp; Reference", pk="P6", phase_label="Phase 6 + Capstone + Reference",
    items="163–202", here_label="Architecture, scaling, capstone, refs",
    groups=[
      ("P6","System Design",[
        ("s5-1","5.1 · Two-pipeline architecture"),("s5-2","5.2 · Scaling"),
        ("s5-3","5.3 · Freshness &amp; updates"),("s5-4","5.4 · Cost modeling"),
        ("s5-5","5.5 · Choosing a vector DB"),("s5-6","5.6 · When NOT to use RAG"),
        ("s5-7","5.7 · Mock system design"),("s5-8","5.8 · Design interview focus")]),
      ("REF","Capstone &amp; Reference",[
        ("s5-9","5.9 · Capstone project"),("s5-10","5.10 · Tools &amp; frameworks"),
        ("s5-11","5.11 · Core papers")]),
    ],
    eyebrow="Part 5 of 6 · System Design, Capstone &amp; Reference",
    h1="Putting it all together",
    sub="The senior-level integration: the full production architecture, scaling and cost, choosing your stack, and when <em>not</em> to use RAG — plus a worked mock system design, a capstone blueprint, and quick-reference tool and paper lists.",
    thesis="System-design rounds don't test whether you know HyDE — they test whether you can assemble the whole machine and defend every trade-off. This part walks the <strong>full production architecture</strong> (separate ingestion and serving pipelines), the scaling/freshness/cost levers, how to <strong>choose a vector database</strong>, and the crucial <strong>“when NOT to use RAG”</strong> judgment. Then a complete <strong>worked mock design</strong> (support assistant · 500K docs · daily updates · sub-2s · RBAC), a <strong>capstone</strong> that proves you can build it end to end, and reference lists of the <strong>tools</strong> and <strong>papers</strong> worth knowing by name.",
    chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Phase 6 + Capstone</b></span>\n          <span class="chip"><b>40</b> tracked topics</span>\n          <span class="chip">⏱ <b>~6–8h</b> deep read</span>\n          <span class="chip">\U0001f3d7️ system design</span>\n          <span class="chip">\U0001f9f0 tools + papers</span>',
    prev=("Part 4 · Evaluation &amp; Production","Metrics, RAGAS, guardrails, ops"),
    nxt=("Part 6 · Interview Q&amp;A Bank",["40+ Q&amp;A: conceptual, design","debugging, coding"]),
  ),
  6: dict(
    file="RAG_Interview_Prep_Part6_QABank.html",
    part_title="Interview Q&amp;A Bank", pk="QA", phase_label="Q&amp;A Bank",
    items="203–206", here_label="50+ Q&amp;A across 4 types",
    groups=[
      ("QA","Interview Q&amp;A",[
        ("s6-1","6.1 · Conceptual"),("s6-2","6.2 · Design a RAG for X"),
        ("s6-3","6.3 · Debugging"),("s6-4","6.4 · Coding"),
        ("s6-5","6.5 · Rapid fire")]),
    ],
    eyebrow="Part 6 of 6 · Interview Q&amp;A Bank",
    h1="The question bank",
    sub="50+ RAG interview questions with model answers — conceptual, system-design, debugging, and coding — consolidating and extending the per-topic questions from Parts 1–5 into one drill.",
    thesis="This is the consolidated <strong>drill</strong>. Interviewers pull from four buckets: <em>conceptual</em> (do you understand the mechanisms?), <em>“design a RAG for X”</em> (can you assemble a system?), <em>debugging</em> (have you operated one?), and <em>coding</em> (can you implement the primitives?). Use it actively: read the question, answer out loud or on paper, <em>then</em> expand the model answer and compare. The one-liners in §6.5 are for last-minute review. Every answer here traces back to a section in Parts 1–5 if you want the depth.",
    chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Q&amp;A Bank</b></span>\n          <span class="chip"><b>50+</b> questions</span>\n          <span class="chip">4 question types</span>\n          <span class="chip">⏱ <b>~4–6h</b> drill</span>\n          <span class="chip">✅ model answers</span>',
    prev=("Part 5 · System Design &amp; Reference","Architecture, capstone, refs"),
    nxt=("Complete resource · all 6 parts",["Stitched: RAG_Interview_Prep_Complete.html","Print / export to PDF"]),
  ),
}

def build(pn):
    cfg = PARTS[pn]
    html = SRC.read_text()

    # 1) strip Part-1 content region -> marker
    start = html.index("</section>", html.index('id="tracker"')) + len("</section>")
    end = html.index("      <!-- PART NAV -->")
    html = html[:start] + "\n\n<!--CONTENT_INSERT-->\n\n      " + html[end:]

    # 2) title
    html = html.replace("<title>RAG Interview Prep — Part 1: Foundations</title>",
                        f"<title>RAG Interview Prep — Part {pn}: {cfg['part_title']}</title>")
    # 3) topbar
    html = html.replace('<div class="tt"><small>Part 1 / 6</small>Foundations</div>',
                        f'<div class="tt"><small>Part {pn} / 6</small>{cfg["part_title"]}</div>')
    # 4) sb-part
    html = html.replace('<div class="k">Part 1 of 6</div>\n      <div class="v">Foundations</div>',
                        f'<div class="k">Part {pn} of 6</div>\n      <div class="v">{cfg["part_title"]}</div>')
    # 5) nav.toc groups (supports one or many groups)
    groups = cfg.get("groups") or [(cfg["pk"], cfg["nav_head"], cfg["nav"])]
    grp_html = ""
    for pk, head, links in groups:
        navlinks = "\n".join(f'          <li><a href="#{i}">{t}</a></li>' for i, t in links)
        grp_html += (f'      <div class="grp">\n'
          f'        <button class="ghead" data-t><span class="num">{pk}</span> {head} <span class="chev">▾</span></button>\n'
          f'        <ul class="links">\n{navlinks}\n        </ul>\n'
          f'      </div>\n')
    newnav = (f'<nav class="toc" id="toc">\n'
      f'      <div class="grp">\n'
      f'        <button class="ghead" data-t><span class="num">◆</span> Progress Tracker</button>\n'
      f'        <ul class="links"><li><a href="#tracker">Master tracker (all parts)</a></li></ul>\n'
      f'      </div>\n'
      f'{grp_html}'
      f'    </nav>')
    html = re.sub(r'<nav class="toc" id="toc">.*?</nav>', lambda m: newnav, html, count=1, flags=re.DOTALL)
    # 6) sb-foot
    html = re.sub(r'<div class="sb-foot">.*?</div>',
      f'<div class="sb-foot">\n      RAG Interview Prep<br>Part {pn} — {cfg["part_title"]}<br>{cfg["phase_label"]}<br>© your study kit\n    </div>',
      html, count=1, flags=re.DOTALL)
    # 7) hero
    newhero = (f'<header class="hero">\n'
      f'        <div class="eyebrow">{cfg["eyebrow"]}</div>\n'
      f'        <h1 class="title">{cfg["h1"]}\n'
      f'          <span class="sub">{cfg["sub"]}</span>\n'
      f'        </h1>\n'
      f'        <p class="thesis">{cfg["thesis"]}</p>\n'
      f'        <div class="meta-chips">\n          {cfg["chips"]}\n        </div>\n'
      f'      </header>')
    html = re.sub(r'<header class="hero">.*?</header>', lambda m: newhero, html, count=1, flags=re.DOTALL)
    # 8) partnav
    nxt_lis = "".join(f"<li>{x}</li>" for x in cfg["nxt"][1])
    newpartnav = (f'<nav class="partnav">\n'
      f'        <div class="pcard"><div class="k">Previously</div><div class="t">{cfg["prev"][0]}</div><ul><li>{cfg["prev"][1]}</li></ul></div>\n'
      f'        <div class="pcard"><div class="k">You are here</div><div class="t">Part {pn} · {cfg["part_title"]}</div><ul><li>{cfg.get("here_label", cfg.get("nav_head",""))}</li></ul></div>\n'
      f'        <div class="pcard next"><div class="k">Coming next</div><div class="t">{cfg["nxt"][0]}</div><ul>{nxt_lis}</ul></div>\n'
      f'      </nav>')
    html = re.sub(r'<nav class="partnav">.*?</nav>', lambda m: newpartnav, html, count=1, flags=re.DOTALL)
    # 9) doc-foot
    html = re.sub(r'<div class="doc-foot">.*?</div>',
      f'<div class="doc-foot">\n'
      f'        RAG Interview Prep — Part {pn} of 6 · {cfg["part_title"]}<br>\n'
      f'        Covers tracker items {cfg["items"]} ({cfg["phase_label"]}). Diagrams use a fixed grammar: <span style="color:var(--gold-2)">gold = query/signal</span>, <span style="color:var(--indigo-2)">indigo = corpus/document</span>, <span style="color:var(--green)">green = relevant match</span>.<br>\n'
      f'        Progress is stored locally under key <code style="color:#8892a0">ragPrepStatus_v1</code> and is shared by every part of this resource.\n'
      f'      </div>',
      html, count=1, flags=re.DOTALL)

    (OUT / cfg["file"]).write_text(html)
    print("wrote", cfg["file"], len(html), "bytes")
    # sanity
    assert "<!--CONTENT_INSERT-->" in html
    assert f"Part {pn}: {cfg['part_title']}" in html
    assert "Part 1 of 6" not in html
    print("sanity OK")

if __name__ == "__main__":
    build(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
