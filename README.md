# Learning Hub — Interview Prep Knowledge Base

A growing set of deep, self-paced study resources for ML / AI-engineering interviews.
Each subject is a **self-contained static mini-site** (styled HTML, inline SVG diagrams,
runnable code, an interactive progress tracker, and an interview Q&A bank).

**Live:** RAG · Classical ML · NLP · LangChain & Prompt Engineering · LangGraph & Agentic AI.

## Structure

```
.
├── index.html                 # hub landing page — cards linking to each subject
├── README.md
├── rag/                       # subject: Retrieval-Augmented Generation
│   ├── index.html             # subject landing page
│   ├── RAG_Interview_Prep_Part1_Foundations.html   … Part2 … Part6
│   ├── RAG_Interview_Prep_Complete.html   # all 6 parts stitched (print/PDF-ready)
│   ├── stitch.py              # rebuilds the Complete file (dev tool, not served)
│   └── build_shell.py         # regenerates a part's shell (dev tool)
├── langchain/                 # subject: LangChain, LLMs & Prompt Engineering
│   ├── index.html
│   ├── LangChain_Part1_LLMFoundations.html  … Part2 … Part6
│   ├── LangChain_Complete.html
│   ├── stitch_lc.py           # rebuilds the Complete file
│   └── build_lc.py            # regenerates shells + tracker from the blueprint .md
├── langgraph/                 # subject: LangGraph & Agentic AI
│   ├── index.html
│   ├── LangGraph_Part1_Foundations.html  … Part2 … Part6
│   ├── LangGraph_Complete.html
│   ├── stitch_lg.py           # rebuilds the Complete file
│   └── build_lg.py            # regenerates shells + the tracker from the blueprint .md
├── nlp/                       # subject: Natural Language Processing (7 parts)
│   ├── index.html
│   ├── NLP_Part1_Foundations.html  … Part2 … Part7
│   ├── NLP_Complete.html
│   ├── stitch_nlp.py          # rebuilds the Complete file
│   ├── build_nlp.py           # regenerates shells + the tracker from the blueprint .md
│   └── insert.py              # splices a content fragment into a shell + validates it
└── cml/                       # subject: Classical Machine Learning (17 parts, one per level)
    ├── index.html
    ├── CML_Part01_WhatMLIs.html  … Part02 … Part17
    ├── CML_Complete.html
    ├── stitch_cml.py          # rebuilds the Complete file
    ├── build_cml.py           # regenerates shells + tracker + the widget CSS layer
    └── insert.py              # splices a content fragment into a shell + validates it
```

Each subject keeps its own progress-tracker localStorage key so they never collide:
`ragPrepStatus_v1`, `cmlPrepStatus_v1`, `nlpPrepStatus_v1`, `lcPrepStatus_v1` and `lgPrepStatus_v1`.
Classical ML additionally uses `cmlDrill_v1` for the Q&A drill marks, kept separate from study progress.

Everything is plain static HTML — no build step, no server. Fonts and code
syntax-highlighting load from a CDN; pages still render offline with fallbacks.

## Adding a new subject (e.g. LangChain)

1. Create a folder: `langchain/`
2. Put its pages inside, with a `langchain/index.html` landing page.
3. Add a card for it on the hub `index.html` (copy a `.card.soon` block, point its
   `href` at `langchain/index.html`, and switch the badge to `Live`).

That's it — no other wiring. Keeping each subject self-contained means they never
interfere with each other.

## Regenerating a combined file

After editing any part, rebuild that subject's stitched `Complete` file:

```bash
cd rag       && python3 stitch.py      # RAG          (6 parts)
cd cml       && python3 stitch_cml.py  # Classical ML (17 parts)
cd nlp       && python3 stitch_nlp.py  # NLP          (7 parts)
cd langchain && python3 stitch_lc.py   # LangChain    (6 parts)
cd langgraph && python3 stitch_lg.py   # LangGraph    (6 parts)
```

## Hosting (free)

**GitHub Pages** (project site — does not conflict with a `username.github.io` portfolio):
1. Push this folder to a new repo (e.g. `learning-hub`).
2. Repo → **Settings → Pages → Source: Deploy from a branch → `main` / root → Save**.
3. Live at `https://USERNAME.github.io/learning-hub/`.

**Render** (free Static Site): New → Static Site → connect the repo →
Build command: *(leave empty)* · Publish directory: `.` → Create. Auto-redeploys on push.

Both are free and rebuild automatically whenever you `git push`.

## Notes

- **Progress is per-device.** The tracker stores status in each browser's local
  storage (one key per subject), so phone and laptop track separately — there is
  no cross-device sync (that would need a backend).
- The original tracker spreadsheet and helper scripts are kept out of the served site
  via `.gitignore`.

## Subject sizes

| Subject | Parts | Tracked topics | Diagrams | Interactive | Q&A | Blueprint |
|---|---|---|---|---|---|---|
| RAG | 6 | 206 | 65 | — | 162 | `rag-learning-master-prompt.md` |
| Classical ML | **17** | 439 | 69 | **28** | **438** | `classical-ml-study-guide.md` |
| NLP | 7 | 520 | 73 | — | 171 | `nlp-study-guide.md` |
| LangChain & Prompt Engineering | 6 | 313 | 16 | — | 69 | `langchain-llm-prompt-study-guide.md` |
| LangGraph & Agentic AI | 6 | 210 | 26 | — | 78 | `langgraph-agentic-ai-study-guide.md` |

**Classical ML is structured differently** from the other subjects: **one part per level (17 parts)**, and — following the RAG pattern — **every one of its 147 topic sections ends with its own interview Q&A box**, tagged by question type (`Conceptual`, `Gotcha`, `Debugging`, `System design`, `Deep dive`). That is why its Q&A count is an order of magnitude above the others: the questions live *with* the concept rather than only in a bank at the end. Part 17 is still a consolidated, shuffled drill.

**Interactive widgets** (Classical ML only, so far) are self-contained `<canvas>` + vanilla-JS
components defined inside each content fragment, styled by the `.wdg` CSS block that
`build_cml.py` injects before `</style>`. They compute for real in the browser — least-squares
fits, coordinate-descent Lasso, Lloyd iterations, PAVA isotonic regression, exact AUC/PSI —
rather than replaying a recorded animation, and each is wrapped in an IIFE with unique element
IDs so they survive being concatenated into `CML_Complete.html`.

Each subject is generated from a Markdown blueprint in `rag_learning/` (one level per
`##` heading, one tracker row per `- [ ]` checkbox), so the tracker can always be
regenerated from the blueprint with that subject's `build_*.py`.
