# Learning Hub — Interview Prep Knowledge Base

A growing set of deep, self-paced study resources for ML / AI-engineering interviews.
Each subject is a **self-contained static mini-site** (styled HTML, inline SVG diagrams,
runnable code, an interactive progress tracker, and an interview Q&A bank).

**Live:** Retrieval-Augmented Generation (RAG) · LangGraph &amp; Agentic AI. **Planned:** LangChain, Classical ML, NLP.

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
└── langgraph/                 # subject: LangGraph & Agentic AI
    ├── index.html
    ├── LangGraph_Part1_Foundations.html  … Part2 … Part6
    ├── LangGraph_Complete.html
    ├── stitch_lg.py           # rebuilds the Complete file
    └── build_lg.py            # regenerates shells + the tracker from the blueprint .md
```

Each subject keeps its own progress-tracker localStorage key so they never collide:
`ragPrepStatus_v1` and `lgPrepStatus_v1`.

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
cd rag       && python3 stitch.py      # RAG
cd langgraph && python3 stitch_lg.py   # LangGraph
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
  storage (key `ragPrepStatus_v1`), so phone and laptop track separately — there is
  no cross-device sync (that would need a backend).
- The original tracker spreadsheet and helper scripts are kept out of the served site
  via `.gitignore`.
