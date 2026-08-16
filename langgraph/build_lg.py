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

WIDGET_CSS = """
/* ---- interactive widgets (LangGraph) ---- */
.wdg{margin:1.8rem 0;border:1px solid var(--line);border-radius:14px;background:var(--surface);box-shadow:var(--shadow);overflow:hidden}
.wdg .wh{background:linear-gradient(135deg,#161b23,#252d3a);color:#fff;padding:12px 18px;font-family:var(--disp);font-weight:600;font-size:.98rem;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.wdg .wh .wtag{font-family:var(--mono);font-size:9.5px;letter-spacing:1.6px;text-transform:uppercase;color:#14181f;background:var(--gold-2);padding:3px 8px;border-radius:20px;font-weight:600}
.wdg .wbody{padding:16px 18px 18px}
.wdg canvas{width:100%;height:auto;display:block;border-radius:10px;background:#14181f}
.wdg .wctl{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start;margin-top:14px}
.wdg .wctl label{font-family:var(--mono);font-size:11.5px;color:var(--muted);display:flex;flex-direction:column;gap:6px;min-width:170px;flex:1}
.wdg .wctl input[type=range]{width:100%;accent-color:var(--indigo);margin:0}
.wdg .wctl b{color:var(--indigo);font-weight:600}
.wdg .wbtns{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.wdg .wbtn{font-family:var(--mono);font-size:11.5px;padding:6px 12px;border-radius:8px;border:1px solid var(--line);background:var(--paper);color:var(--text);cursor:pointer;transition:.13s}
.wdg .wbtn:hover{border-color:var(--indigo-line);background:var(--indigo-soft)}
.wdg .wbtn.on{background:var(--indigo);color:#fff;border-color:var(--indigo)}
.wdg .wout{margin-top:13px;font-family:var(--mono);font-size:12.5px;color:var(--text);background:var(--indigo-soft);border:1px solid var(--indigo-line);border-radius:10px;padding:11px 14px;line-height:1.75}
.wdg .wout .k{color:var(--muted)}
.wdg .wout .v{font-weight:600;color:var(--indigo)}
.wdg .wout .warn{color:#a5710a;font-weight:600}
.wdg .wout .good{color:#1c7a42;font-weight:600}
.wdg .wnote{margin:12px 0 0;font-size:.88rem;color:var(--muted);line-height:1.65}
.wdg .wgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:13px}
.wdg .wcell{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:9px 12px;font-family:var(--mono);font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px}
.wdg .wcell .n{display:block;font-size:1.3rem;font-weight:600;color:var(--ink);font-family:var(--disp);letter-spacing:-.4px;text-transform:none}
.wdg .cm{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-top:13px;max-width:420px}
.wdg .cm div{border-radius:10px;padding:10px 12px;font-family:var(--mono);font-size:11px;letter-spacing:.6px;text-transform:uppercase}
.wdg .cm .tp{background:var(--green-soft);border:1px solid #bfe3cc;color:#1c7a42}
.wdg .cm .fp{background:var(--gold-soft);border:1px solid var(--gold-line);color:#a5710a}
.wdg .cm .fn{background:#fdecec;border:1px solid #f3c9c9;color:#a33}
.wdg .cm .tn{background:var(--paper);border:1px solid var(--line);color:var(--muted)}
.wdg .cm b{display:block;font-family:var(--disp);font-size:1.4rem;color:var(--ink);letter-spacing:-.5px;text-transform:none}
@media print{.wdg .wctl,.wdg .wbtns{display:none}.wdg{break-inside:avoid}}
/* ---- deeper-structure helpers ---- */
.content h4{font-family:var(--disp);font-weight:600;font-size:1.06rem;color:var(--ink);margin:1.9rem 0 .5rem;letter-spacing:-.2px}
.content h4::before{content:"";display:inline-block;width:14px;height:2px;background:var(--gold);vertical-align:middle;margin-right:9px}
.content h5{font-family:var(--disp);font-weight:600;font-size:.96rem;color:var(--muted);margin:1.3rem 0 .4rem;letter-spacing:.2px}
.assump{margin:1.2rem 0;border:1px solid var(--line);border-radius:13px;overflow:hidden;background:var(--surface);box-shadow:var(--shadow)}
.assump .ah{background:var(--ink);color:#fff;padding:10px 16px;font-family:var(--disp);font-weight:600;font-size:.98rem;display:flex;align-items:center;gap:10px}
.assump .ah .an{font-family:var(--mono);font-size:11px;color:#14181f;background:var(--gold-2);padding:2px 8px;border-radius:20px;font-weight:600}
.assump .abody{padding:2px 0}
.assump .arow{display:grid;grid-template-columns:132px 1fr;gap:0;border-top:1px solid var(--line)}
.assump .arow:first-child{border-top:none}
.assump .arow .al{background:var(--paper);padding:11px 14px;font-family:var(--mono);font-size:10.5px;letter-spacing:1.1px;text-transform:uppercase;color:var(--muted);border-right:1px solid var(--line)}
.assump .arow .av{padding:11px 16px;font-size:.94rem;line-height:1.6}
.assump .arow.brk .al{color:#a33}
.assump .arow.fix .al{color:#1c7a42}
@media (max-width:620px){.assump .arow{grid-template-columns:1fr}.assump .arow .al{border-right:none;border-bottom:1px solid var(--line)}}
"""

# ---------------- per-part config (v2: one part per level, 12 parts) ----------------
NP = 12

def chips(level, topics, diagrams, qa, inter, hours):
    s = ('<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>%s</b></span>\n'
         '          <span class="chip"><b>%d</b> sections</span>\n'
         '          <span class="chip">📐 <b>%d</b> diagrams</span>\n'
         '          <span class="chip">💬 <b>%d</b> Q&amp;A</span>\n') % (level, topics, diagrams, qa)
    if inter:
        s += '          <span class="chip">🎛 <b>%d</b> interactive</span>\n' % inter
    s += '          <span class="chip">⏱ <b>~%s</b></span>' % hours
    return s

PARTS = {
 1: dict(file="LangGraph_Part01_Prerequisites.html", title="Prerequisites &amp; the LLM Substrate", pk="L0",
   groups=[("L0","Prerequisites",[("g1-1","1.1 · Python you actually need"),("g1-2","1.2 · Typing, TypedDict &amp; Pydantic ⭐"),
     ("g1-3","1.3 · Async, concurrency &amp; the event loop ⭐"),("g1-4","1.4 · The LLM substrate"),
     ("g1-5","1.5 · Structured output ⭐"),("g1-6","1.6 · The LangChain layer in 2026 ⭐")])],
   h1="What you must know before the graph makes sense",
   sub="The Python that LangGraph actually leans on — TypedDict, Annotated, Pydantic v2, async and the event loop — plus the LLM substrate underneath it: tokens, context windows, structured output, and where LangChain sits relative to LangGraph in 2026.",
   thesis="Skipping this part is the single most common reason LangGraph feels like magic. Three things here are load-bearing for everything that follows. <strong>Annotated[T, reducer]</strong> is the mechanism behind every state channel — if you don't know what <code class=\"ic\">Annotated</code> does in Python, reducers will never make sense. <strong>Async</strong> is why parallel <code class=\"ic\">Send</code> fan-out actually runs concurrently, and why one blocking call inside a node silently serialises your whole graph. And the <strong>LangChain-vs-LangGraph layering</strong> is the question you will be asked in the first five minutes — it is a layering question, not a rivalry, and getting that framing right sets the tone.",
   chips=chips("Level 0", 6, 6, 20, 0, "5h"),
   prev=("Learning Hub","All subjects"), prevhref="../index.html",
   nxt=("Part 2 · Agentic AI Foundations",["Workflow vs agent, ReAct","When NOT to build an agent"])),

 2: dict(file="LangGraph_Part02_AgenticFoundations.html", title="Agentic AI Foundations", pk="L1",
   groups=[("L1","Agentic AI Foundations",[("g2-1","2.1 · The capability ladder ⭐⭐"),("g2-2","2.2 · Anatomy of an agent"),
     ("g2-3","2.3 · ReAct and its descendants ⭐"),("g2-4","2.4 · Planning &amp; decomposition"),
     ("g2-5","2.5 · Reflection &amp; self-critique"),("g2-6","2.6 · Autonomy vs control ⭐"),
     ("g2-7","2.7 · When NOT to build an agent ⭐⭐"),("g2-8","2.8 · The 2026 agent landscape")])],
   h1="What an agent is, and when you shouldn't build one",
   sub="The capability ladder from a single LLM call to a full agent, the anatomy of the agent loop, ReAct and what replaced it, planning and reflection patterns, the autonomy-versus-control trade-off — and the senior answer about when a workflow beats an agent.",
   thesis="Almost every agentic-AI interview opens here, and the two highest-value answers are both about <em>restraint</em>. The first is the <strong>capability ladder</strong>: a single call, then a chain, then a router, then a workflow, then an agent — and you climb it only as far as the problem forces you, because every rung adds non-determinism, latency and cost. The second is <strong>&ldquo;when would you not build an agent?&rdquo;</strong>, where the correct answer is that if the control flow is knowable in advance you should <em>encode</em> it rather than ask an LLM to rediscover it on every request. Candidates who lead with an agent for a problem a switch statement solves are the ones who don't get hired.",
   chips=chips("Level 1", 8, 8, 26, 1, "7h"),
   prev=("Part 1 · Prerequisites","Typing, async, structured output"), prevhref="LangGraph_Part01_Prerequisites.html",
   nxt=("Part 3 · LangGraph Core Primitives",["StateGraph, nodes, edges","Reducers, Send, Command"])),

 3: dict(file="LangGraph_Part03_CorePrimitives.html", title="LangGraph Core Primitives", pk="L2",
   groups=[("L2","Core Primitives",[("g3-1","3.1 · Why a graph at all ⭐"),("g3-2","3.2 · StateGraph &amp; the schema ⭐⭐"),
     ("g3-3","3.3 · Nodes ⭐"),("g3-4","3.4 · Edges &amp; conditional edges ⭐"),
     ("g3-5","3.5 · Reducers ⭐⭐"),("g3-6","3.6 · The superstep model ⭐⭐"),
     ("g3-7","3.7 · Send &amp; the map-reduce pattern ⭐"),("g3-8","3.8 · Command ⭐"),
     ("g3-9","3.9 · Subgraphs"),("g3-10","3.10 · Compilation &amp; runtime config")])],
   h1="The primitives everything else is assembled from",
   sub="StateGraph and the state schema, nodes as pure state transformers, conditional edges, reducers and why they exist, the superstep execution model, Send for dynamic fan-out, Command for combined update-and-route, subgraphs, and compilation.",
   thesis="This is the densest part of the subject and the one that separates people who have <em>used</em> LangGraph from people who have <em>read about</em> it. Four concepts carry it. <strong>Reducers</strong> — because the default is overwrite, and every &ldquo;my messages keep disappearing&rdquo; bug is a missing <code class=\"ic\">add_messages</code>. The <strong>superstep model</strong>, borrowed from Pregel — nodes in a superstep run in parallel, all writes are applied together at the barrier, and that single fact explains parallel-write conflicts, why reducers are mandatory for fan-out, and what a checkpoint actually contains. <strong>Send</strong>, which is how you fan out to a number of branches you don't know until runtime. And <strong>Command</strong>, which collapses &ldquo;update the state&rdquo; and &ldquo;decide where to go&rdquo; into one return value.",
   chips=chips("Level 2", 10, 12, 34, 2, "10h"),
   prev=("Part 2 · Agentic AI Foundations","Ladder, ReAct, autonomy"), prevhref="LangGraph_Part02_AgenticFoundations.html",
   nxt=("Part 4 · Workflow Patterns",["Sequential, parallel, routing","Orchestrator-worker, evaluator loops"])),

 4: dict(file="LangGraph_Part04_WorkflowPatterns.html", title="Workflow Patterns", pk="L3",
   groups=[("L3","Workflow Patterns",[("g4-1","4.1 · Prompt chaining"),("g4-2","4.2 · Parallelisation ⭐"),
     ("g4-3","4.3 · Routing ⭐"),("g4-4","4.4 · Orchestrator-worker ⭐"),
     ("g4-5","4.5 · Evaluator-optimizer loops ⭐"),("g4-6","4.6 · The agent loop as a pattern"),
     ("g4-7","4.7 · Choosing a pattern ⭐⭐")])],
   h1="The six shapes almost every system is made of",
   sub="Prompt chaining, parallelisation (sectioning and voting), routing, orchestrator-worker, evaluator-optimizer loops, and the agent loop — each with the LangGraph construct that implements it and the failure mode that kills it.",
   thesis="Anthropic's <em>Building Effective Agents</em> put names to a small set of shapes, and interviewers now use those names as shared vocabulary — so being able to say &ldquo;that's an orchestrator-worker with an evaluator gate&rdquo; is worth a surprising amount. The section that matters most is the last one: <strong>choosing</strong>. Every pattern here trades determinism for flexibility, and the senior move is to pick the <em>least</em> flexible pattern that solves the problem, because determinism is what makes a system testable, debuggable and cheap. An evaluator-optimizer loop with no iteration cap is the most common way to turn a working demo into a runaway bill.",
   chips=chips("Level 3", 7, 8, 22, 1, "6h"),
   prev=("Part 3 · Core Primitives","Reducers, supersteps, Send"), prevhref="LangGraph_Part03_CorePrimitives.html",
   nxt=("Part 5 · State, Persistence &amp; Memory",["Checkpointers, threads, HITL","Short vs long-term memory"])),

 5: dict(file="LangGraph_Part05_StateMemory.html", title="State, Persistence &amp; Memory", pk="L4",
   groups=[("L4","State &amp; Memory",[("g5-1","5.1 · What state actually is ⭐"),("g5-2","5.2 · Checkpointers ⭐⭐"),
     ("g5-3","5.3 · Threads &amp; thread_id ⭐"),("g5-4","5.4 · Time travel &amp; state editing"),
     ("g5-5","5.5 · Human-in-the-loop ⭐⭐"),("g5-6","5.6 · Short-term memory &amp; the context window ⭐"),
     ("g5-7","5.7 · Long-term memory &amp; the Store ⭐⭐"),("g5-8","5.8 · Durability &amp; crash recovery ⭐")])],
   h1="Why LangGraph exists at all",
   sub="State as a typed channel set, checkpointers and what a checkpoint contains, threads and thread_id, time travel, interrupt-based human-in-the-loop, context-window management, the cross-thread Store, and durable execution across crashes.",
   thesis="If you had to justify LangGraph over a plain <code class=\"ic\">while</code> loop in one sentence, it would be this part. <strong>Persistence is the feature</strong> — a checkpointer turns an agent from a function call into a resumable process, and everything valuable follows: human-in-the-loop approval that can wait three days, crash recovery that resumes mid-graph rather than restarting, and time travel for debugging. The distinction interviewers probe hardest is <strong>checkpointer versus store</strong>: the checkpointer is <em>within-thread</em> execution state, the store is <em>cross-thread</em> long-term memory, and conflating them is the tell that someone has only done tutorials.",
   chips=chips("Level 4", 8, 10, 28, 1, "9h"),
   prev=("Part 4 · Workflow Patterns","The six shapes, choosing one"), prevhref="LangGraph_Part04_WorkflowPatterns.html",
   nxt=("Part 6 · Tools &amp; Agent Capabilities",["Tool design, errors, MCP","Structured output, sandboxing"])),

 6: dict(file="LangGraph_Part06_Tools.html", title="Tools &amp; Agent Capabilities", pk="L5",
   groups=[("L5","Tools",[("g6-1","6.1 · What a tool is ⭐"),("g6-2","6.2 · Designing a tool the LLM can use ⭐⭐"),
     ("g6-3","6.3 · Tool errors &amp; retries ⭐"),("g6-4","6.4 · Tool choice &amp; too many tools ⭐"),
     ("g6-5","6.5 · Dangerous tools &amp; sandboxing ⭐"),("g6-6","6.6 · MCP ⭐"),
     ("g6-7","6.7 · The middleware layer")])],
   h1="The interface between the model and the world",
   sub="Tool definition and binding, designing a schema and docstring the model can actually use, error handling that lets the agent recover, tool selection under a large catalogue, sandboxing destructive operations, the Model Context Protocol, and LangChain's middleware layer.",
   thesis="Tool <em>design</em> is a prompt-engineering problem wearing an API-design costume, and this is where most real agent failures actually live — not in the graph. Three ideas carry the part. A tool's <strong>docstring and schema are prompt</strong>: the model chooses tools by reading them, so an ambiguous description is a bug in the model's decision-making. <strong>Errors should be returned to the model, not raised</strong>, because an agent that receives &ldquo;invalid date format, expected YYYY-MM-DD&rdquo; can fix itself, while an exception just ends the run. And <strong>too many tools degrades selection</strong> — past roughly 15–20 the model starts confusing them, which is what tool retrieval and namespacing exist to fix.",
   chips=chips("Level 5", 7, 8, 24, 1, "7h"),
   prev=("Part 5 · State &amp; Memory","Checkpointers, HITL, the Store"), prevhref="LangGraph_Part05_StateMemory.html",
   nxt=("Part 7 · RAG in Agents",["The retrieval ladder","Agentic RAG, CRAG, Self-RAG"])),

 7: dict(file="LangGraph_Part07_RAG.html", title="RAG in Agents", pk="L6",
   groups=[("L6","RAG in Agents",[("g7-1","7.1 · Why RAG is a tool, not a stage ⭐"),("g7-2","7.2 · The retrieval ladder ⭐"),
     ("g7-3","7.3 · Agentic RAG ⭐⭐"),("g7-4","7.4 · CRAG &amp; Self-RAG ⭐"),
     ("g7-5","7.5 · Grounding &amp; citation"),("g7-6","7.6 · Evaluating retrieval inside an agent ⭐")])],
   h1="Retrieval as something the agent decides to do",
   sub="Why an agent turns RAG from a fixed pipeline stage into a tool call, the retrieval ladder from naive to hybrid to reranked, agentic RAG with query rewriting and retry, Corrective RAG and Self-RAG, grounding and citation, and how to evaluate retrieval inside a multi-step trace.",
   thesis="The single framing that matters: in a pipeline, retrieval <em>always</em> happens; in an agent, retrieval is <strong>a tool the model chooses to call, possibly several times, possibly with a rewritten query</strong>. That one change is what makes <strong>agentic RAG</strong> strictly more capable than naive RAG — and strictly harder to evaluate, because a bad final answer might come from bad retrieval, bad query formulation, or a good retrieval the model ignored. <strong>CRAG</strong> grades the retrieved documents and falls back to search when they're poor; <strong>Self-RAG</strong> has the model decide whether to retrieve at all and then critique its own grounding. This subject owns the <em>agentic</em> half; the RAG guide owns the retrieval internals.",
   chips=chips("Level 6", 6, 7, 20, 0, "6h"),
   prev=("Part 6 · Tools","Tool design, MCP, middleware"), prevhref="LangGraph_Part06_Tools.html",
   nxt=("Part 8 · Multi-Agent Architectures",["Supervisor, swarm, hierarchical","Handoffs and shared state"])),

 8: dict(file="LangGraph_Part08_MultiAgent.html", title="Multi-Agent Architectures", pk="L7",
   groups=[("L7","Multi-Agent",[("g8-1","8.1 · When multi-agent earns its cost ⭐⭐"),("g8-2","8.2 · Supervisor ⭐"),
     ("g8-3","8.3 · Swarm &amp; handoffs ⭐"),("g8-4","8.4 · Hierarchical teams"),
     ("g8-5","8.5 · Shared state vs message passing ⭐"),("g8-6","8.6 · Failure modes ⭐")])],
   h1="Several agents, and whether you need them",
   sub="The cost-benefit of multi-agent systems, the supervisor pattern, swarm architectures with handoffs, hierarchical teams, the shared-state-versus-message-passing decision, and the failure modes that make multi-agent systems fragile.",
   thesis="The most valuable thing you can say about multi-agent architectures is <strong>when not to use one</strong>. Every additional agent multiplies latency, cost and the number of places a conversation can go wrong, and the honest default is that <em>one agent with well-designed tools beats three agents passing messages</em> for most problems. Multi-agent earns its cost in exactly three situations: genuinely <strong>separable expertise</strong> with different tools and prompts, a <strong>context-window</strong> problem that forces you to split work, and <strong>organisational</strong> boundaries where different teams own different agents. Anything else is usually complexity you'll be debugging at 2 a.m.",
   chips=chips("Level 7", 6, 7, 20, 1, "6h"),
   prev=("Part 7 · RAG in Agents","Agentic RAG, CRAG, Self-RAG"), prevhref="LangGraph_Part07_RAG.html",
   nxt=("Part 9 · Observability &amp; Evaluation",["Tracing, LangSmith","Trajectory evals, LLM judges"])),

 9: dict(file="LangGraph_Part09_Observability.html", title="Observability &amp; Evaluation", pk="L8",
   groups=[("L8","Observability &amp; Eval",[("g9-1","9.1 · Why agents need tracing ⭐"),("g9-2","9.2 · Traces, runs &amp; spans ⭐"),
     ("g9-3","9.3 · What to evaluate in an agent ⭐⭐"),("g9-4","9.4 · Trajectory evaluation ⭐"),
     ("g9-5","9.5 · LLM-as-judge &amp; its bias controls ⭐"),("g9-6","9.6 · Datasets &amp; regression gates ⭐"),
     ("g9-7","9.7 · Online eval &amp; feedback")])],
   h1="Knowing whether it works",
   sub="Why a multi-step agent is untestable without tracing, the trace/run/span model, the four things worth evaluating in an agent, trajectory evaluation against golden paths, LLM-as-judge with bias controls, dataset-driven regression gates in CI, and online evaluation.",
   thesis="An agent is a <strong>non-deterministic multi-step program</strong>, which means the single-number accuracy score you'd use for a classifier is close to meaningless. This part is about what replaces it. <strong>Four things are worth evaluating</strong>, and they fail independently: the <em>final answer</em>, the <em>trajectory</em> (did it take a sensible path?), <em>tool-call correctness</em>, and the <em>cost/latency budget</em>. The technique that separates senior candidates is <strong>trajectory evaluation</strong> — comparing the sequence of tool calls against a golden path — because it catches an agent that reaches the right answer by an absurd route, which is exactly the agent that will break next week.",
   chips=chips("Level 8", 7, 8, 24, 1, "7h"),
   prev=("Part 8 · Multi-Agent","Supervisor, swarm, handoffs"), prevhref="LangGraph_Part08_MultiAgent.html",
   nxt=("Part 10 · Production Engineering",["Deployment, streaming, durability","Cost, security, reliability"])),

 10: dict(file="LangGraph_Part10_Production.html", title="Production Engineering", pk="L9",
   groups=[("L9","Production",[("g10-1","10.1 · Deployment options ⭐"),("g10-2","10.2 · Streaming ⭐⭐"),
     ("g10-3","10.3 · Durability &amp; idempotency ⭐⭐"),("g10-4","10.4 · Timeouts, retries &amp; error handlers ⭐"),
     ("g10-5","10.5 · Cost control ⭐⭐"),("g10-6","10.6 · Latency engineering ⭐"),
     ("g10-7","10.7 · Security &amp; prompt injection ⭐⭐"),("g10-8","10.8 · Multi-tenancy &amp; scale"),
     ("g10-9","10.9 · Testing an agent ⭐"),("g10-10","10.10 · Rollout &amp; incident response")])],
   h1="Shipping something people depend on",
   sub="Deployment options from self-hosted to LangGraph Platform, the streaming modes and which to use, durability and idempotency across crashes, per-node timeouts and error handlers, cost control, latency engineering, prompt injection, multi-tenancy, testing, and incident response.",
   thesis="The largest level in the subject, because agents fail in more ways than models do. Three ideas recur. <strong>Idempotency</strong>: durable execution means a node can be <em>re-run after a crash</em>, so any node with a side effect — charging a card, sending an email — must be safe to execute twice, and that is a design constraint, not an afterthought. <strong>Cost</strong>: an agent's spend is unbounded by construction unless you cap iterations, cap tokens and cascade models, and &ldquo;we'll watch the dashboard&rdquo; is not a cost control. And <strong>prompt injection</strong>, which for agents is not a content-filtering problem but a <em>privilege</em> problem — the fix is to constrain what the tools can do, because you cannot reliably constrain what the model will be persuaded to attempt.",
   chips=chips("Level 9", 10, 11, 32, 2, "11h"),
   prev=("Part 9 · Observability &amp; Evaluation","Tracing, trajectory evals"), prevhref="LangGraph_Part09_Observability.html",
   nxt=("Part 11 · Advanced &amp; Frontier",["Computer use, long-horizon agents","Agent protocols, the 2026 debate"])),

 11: dict(file="LangGraph_Part11_Frontier.html", title="Advanced &amp; Frontier", pk="L10",
   groups=[("L10","Frontier",[("g11-1","11.1 · Long-horizon agents ⭐"),("g11-2","11.2 · Computer use &amp; browser agents"),
     ("g11-3","11.3 · Agent protocols — MCP, A2A, AG-UI ⭐"),("g11-4","11.4 · Self-improving agents"),
     ("g11-5","11.5 · Context engineering ⭐⭐"),("g11-6","11.6 · The 2026 positions ⭐")])],
   h1="The positions that make you sound current",
   sub="Long-horizon agents that run for days, computer-use and browser agents, the protocol layer (MCP, A2A, AG-UI), self-improving agents, context engineering as the discipline that replaced prompt engineering, and defensible positions on the open debates.",
   thesis="This part exists to give you <em>positions</em> rather than facts. The reframing that lands hardest is <strong>context engineering</strong>: the job is no longer writing a clever prompt, it is deciding — for every single LLM call — what goes into a finite context window and what gets summarised, retrieved, or dropped. Once you see agent design that way, memory management, RAG, tool selection and message trimming stop being separate topics and become one problem. The other positions worth holding: <strong>MCP won the tool-interface layer</strong>, agent-to-agent protocols have not settled, and the honest answer to &ldquo;are multi-agent systems the future?&rdquo; is that most production systems in 2026 are still <em>one</em> well-instrumented agent with good tools.",
   chips=chips("Level 10", 6, 7, 20, 0, "5h"),
   prev=("Part 10 · Production Engineering","Durability, cost, security"), prevhref="LangGraph_Part10_Production.html",
   nxt=("Part 12 · Interview Q&amp;A Bank",["Full question bank + traps","System designs and projects"])),

 12: dict(file="LangGraph_Part12_QABank.html", title="Interview Q&amp;A Bank", pk="QA",
   groups=[("QA","The Question Bank",[("g12-0","12.0 · How to use this bank"),("g12-1","12.1 · Conceptual foundations"),
     ("g12-2","12.2 · LangGraph mechanics"),("g12-3","12.3 · State &amp; memory"),
     ("g12-4","12.4 · HITL &amp; durability"),("g12-5","12.5 · Tools &amp; MCP"),
     ("g12-6","12.6 · RAG in agents"),("g12-7","12.7 · Multi-agent"),
     ("g12-8","12.8 · Evaluation &amp; observability"),("g12-9","12.9 · Production &amp; cost"),
     ("g12-10","12.10 · Frontier &amp; senior signal")]),
    ("REF","Traps &amp; Reference",[("g12-11","12.11 · The trap questions ⭐⭐"),("g12-12","12.12 · System design scenarios"),
     ("g12-13","12.13 · Coding exercises"),("g12-14","12.14 · Portfolio projects"),
     ("g12-15","12.15 · Gotchas cheat sheet"),("g12-16","12.16 · API quick reference")])],
   h1="The question bank",
   sub="The consolidated drill: high-frequency questions with model answers across every level, the trap questions, system-design scenarios, coding exercises, portfolio projects, the gotchas sheet and an API quick reference.",
   thesis="Every part of this subject ends its topics with the questions that topic answers — this is the <strong>consolidated drill</strong>, shuffled and stripped of context so you cannot coast on adjacency. Read the question, answer out loud, <em>then</em> expand and compare. Two sections deserve the most attention: <strong>§12.11, the traps</strong>, because agentic-AI interviews are lost on a small number of confidently-wrong answers — &ldquo;we'll use multi-agent&rdquo; for a problem one agent solves, &ldquo;the checkpointer stores memory&rdquo;, &ldquo;we'll add a guardrail prompt&rdquo; for prompt injection — and <strong>§12.16</strong>, which is the API surface you should be able to write from memory.",
   chips=chips("Q&amp;A Bank", 17, 2, 96, 1, "6h drill"),
   prev=("Part 11 · Advanced &amp; Frontier","Context engineering, protocols"), prevhref="LangGraph_Part11_Frontier.html",
   nxt=("Learning Hub",["All subjects"])),
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
                        f'<div class="tt"><small>Part {pn} / {NP}</small>{cfg["title"]}</div>')
    html = html.replace('<div class="brand-txt">RAG Prep<small>Knowledge Base</small></div>',
                        '<div class="brand-txt">LangGraph<small>Agentic AI Prep</small></div>')
    html = html.replace('<div class="k">Part 1 of 6</div>\n      <div class="v">Foundations</div>',
                        f'<div class="k">Part {pn} of {NP}</div>\n      <div class="v">{cfg["title"]}</div>')

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
      f'        <div class="eyebrow">Part {pn} of {NP} · {cfg["title"]}</div>\n'
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
      f'<div class="doc-foot">\n        LangGraph &amp; Agentic AI — Part {pn} of {NP} · {cfg["title"]}<br>\n'
      f'        API-current as of <b>Aug 2026</b> — LangChain <b>1.3.15</b> · LangGraph <b>1.2.11</b> · Python 3.10–3.14. <code style="color:#8892a0">create_agent</code> replaces the deprecated '
      f'<code style="color:#8892a0">create_react_agent</code>.<br>\n'
      f'        Progress is stored locally under key <code style="color:#8892a0">lgPrepStatus_v1</code> and is shared by every part of this subject.\n      </div>',
      html, count=1, flags=re.DOTALL)

    html = html.replace("</style>", WIDGET_CSS + "</style>", 1)

    # ---- swap tracker payload ----
    _ph = "const PHASES = " + json.dumps(PHASES, ensure_ascii=False) + ";"
    _or = "const ORDER = " + json.dumps(ORDER) + ";"
    _tk = "const TRACKER = " + tracker_js + ";"
    html = re.sub(r'const PHASES = \{.*?\};', lambda m: _ph, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const ORDER = \[.*?\];', lambda m: _or, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const TRACKER = \[.*?\n\];', lambda m: _tk, html, count=1, flags=re.DOTALL)
    html = html.replace('const LS_KEY="ragPrepStatus_v1";', 'const LS_KEY="lgPrepStatus_v1";')
    html = html.replace("206", str(TOTAL))
    html = re.sub(r'<p class="tk-sub">.*?</p>',
      f'<p class="tk-sub">One tracker for the whole LangGraph subject — all {TOTAL} topics across all {NP} parts. '
      f'Set a status on any row; your progress saves in this browser and prints as a clean checklist.</p>',
      html, count=1, flags=re.DOTALL)

    (HERE / cfg["file"]).write_text(html)
    assert "<!--CONTENT_INSERT-->" in html and "ragPrepStatus" not in html
    print(f"  wrote {cfg['file']} ({len(html):,} bytes)")

if __name__ == "__main__":
    args = sys.argv[1:]
    for p in ([int(a) for a in args] if args else PARTS):
        build(p)
