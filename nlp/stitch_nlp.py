#!/usr/bin/env python3
"""Stitch all 7 NLP part files into one print/PDF-ready NLP_Complete.html.
Reuses Part 1's head/CSS/tracker/script; concatenates each part's content with a
part divider; builds a combined sidebar nav. Re-run after editing any part."""
import re, pathlib

OUT = pathlib.Path(__file__).resolve().parent      # run from the nlp/ folder
NP  = 7
PARTS = [
    ("NLP_Part1_Foundations.html", "Foundations &amp; Classical NLP",
     "Task taxonomy, the linguistic pipeline, BoW/TF-IDF/LSA/LDA"),
    ("NLP_Part2_ModelsAndEmbeddings.html", "Models, LMs &amp; Embeddings",
     "Naive Bayes → HMM/Viterbi → CRF, n-gram LMs, perplexity, Word2Vec"),
    ("NLP_Part3_SequencesAndTokenization.html", "Sequences &amp; Tokenization",
     "RNN → LSTM → seq2seq → attention; BPE, WordPiece, Unigram"),
    ("NLP_Part4_Transformers.html", "Transformers &amp; Pretraining",
     "Attention, RoPE, KV cache, objectives, the model zoo, sentence embeddings"),
    ("NLP_Part5_EfficiencyAndFinetuning.html", "Efficiency &amp; Fine-Tuning",
     "GQA/MLA, FlashAttention, Mamba hybrids, MoE, LoRA/QLoRA, DPO/GRPO"),
    ("NLP_Part6_TasksEvalProduction.html", "Tasks, Evaluation &amp; Production",
     "The task catalogue, metrics, LLM-as-judge, serving, drift, multimodal"),
    ("NLP_Part7_QABank.html", "Interview Q&amp;A Bank",
     "115 questions, 15 traps, your PDF map, derivations, coding, designs"),
]

def read(fn): return (OUT / fn).read_text()

def content_of(html):
    s = html.index("</section>", html.index('id="tracker"')) + len("</section>")
    e = html.index("      <!-- PART NAV -->")
    return html[s:e].strip("\n")

def nav_grps(html, skip_tracker=True):
    nav = re.search(r'<nav class="toc" id="toc">(.*?)</nav>', html, re.DOTALL).group(1)
    grps = re.findall(r'<div class="grp">.*?</div>', nav, re.DOTALL)
    return grps[1:] if skip_tracker else grps    # grps[0] is the Progress Tracker group

p1 = read(PARTS[0][0])

# ---- TOP: head + CSS + topbar + sidebar + hero + tracker (through </section>) ----
top = p1[: p1.index("</section>", p1.index('id="tracker"')) + len("</section>")]

# ---- SCRIPT + close: from the highlight.js <script> to EOF ----
bottom = p1[p1.index('<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js'):]

# ---- swap chrome for the combined doc ----
top = top.replace("<title>NLP Interview Prep — Part 1: Foundations &amp; Classical NLP</title>",
                  "<title>NLP Interview Prep — Complete (All 7 Parts)</title>")
top = top.replace('<div class="tt"><small>Part 1 / 7</small>Foundations &amp; Classical NLP</div>',
                  '<div class="tt"><small>Complete</small>All 7 Parts</div>')
top = top.replace('<div class="k">Part 1 of 7</div>\n      <div class="v">Foundations &amp; Classical NLP</div>',
                  '<div class="k">Complete edition</div>\n      <div class="v">All 7 Parts</div>')

new_hero = ('<header class="hero">\n'
  '        <div class="eyebrow">Complete Resource · All 7 Parts</div>\n'
  '        <h1 class="title">Natural Language Processing, end to end\n'
  '          <span class="sub">The full curriculum in one document — classical and linguistic NLP, statistical language '
  'models and embeddings, sequence models and tokenization, transformers and pretraining, efficiency and fine-tuning, '
  'tasks, evaluation, production engineering, and a 115-question interview bank.</span>\n'
  '        </h1>\n'
  '        <p class="thesis">This is the stitched edition of all seven parts, print- and PDF-ready. The master tracker below '
  'covers every one of the 520 topics; your progress is shared with the individual part files (same browser). '
  'Library-current as of <b>Aug 2026</b> — <code class="ic">transformers</code> <b>5.15</b> (PyTorch-only; the slow/fast '
  'tokenizer split was removed in v5), spaCy <b>3.8.15</b>, sentence-transformers <b>5.7</b>. Use the sidebar to jump to any part or section.</p>\n'
  '        <div class="meta-chips">\n'
  '          <span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>7 parts</b> · 16 levels</span>\n'
  '          <span class="chip"><b>520</b> tracked topics</span>\n'
  '          <span class="chip"><b>73</b> diagrams</span>\n'
  '          <span class="chip"><b>115</b> Q&amp;A</span>\n'
  '          <span class="chip">\U0001f9ee classical → transformers</span>\n'
  '        </div>\n'
  '      </header>')
top = re.sub(r'<header class="hero">.*?</header>', lambda m: new_hero, top, count=1, flags=re.DOTALL)

# ---- combined sidebar nav: Progress Tracker + Jump-to-Part + every part's groups ----
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
combined_nav = ('<nav class="toc" id="toc">\n'
  '      ' + tracker_grp + '\n'
  + jump
  + all_grps
  + '    </nav>')
top = re.sub(r'<nav class="toc" id="toc">.*?</nav>', lambda m: combined_nav, top, count=1, flags=re.DOTALL)

# ---- body: part divider + content, for each part ----
def divider(i, title, sub):
    return ('\n      <div class="part-divider" id="part%d">\n'
            '        <div class="pdk">Part %d of %d</div>\n'
            '        <div class="pdt">%s</div>\n'
            '        <div class="pds">%s</div>\n'
            '      </div>\n') % (i, i, NP, title, sub)

body = ""
for i, (fn, title, sub) in enumerate(PARTS, start=1):
    body += divider(i, title, sub) + "\n" + content_of(read(fn)) + "\n"

# ---- combined foot ----
foot = ('\n      <div class="doc-foot">\n'
  '        Natural Language Processing — <b>Complete edition</b> · all 7 parts · 520 tracked topics · 73 diagrams · 115 Q&amp;A.<br>\n'
  '        Library-current as of <b>Aug 2026</b> — transformers <b>5.15.0</b> (PyTorch only; no slow/fast tokenizer split) · '
  'spaCy <b>3.8.15</b> · sentence-transformers <b>5.7.0</b> · Python 3.10–3.14.<br>\n'
  '        Progress is stored locally under key <code style="color:#8892a0">nlpPrepStatus_v1</code>, shared with every part file.<br>\n'
  '        Regenerate this file after editing any part with: '
  '<code style="color:#8892a0">python3 stitch_nlp.py</code> · '
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

close = '\n    </div>\n  </main>\n</div>\n\n'      # close .content, .main, .layout
complete = top + "\n" + body + foot + close + bottom
(OUT / "NLP_Complete.html").write_text(complete)
print("wrote NLP_Complete.html", "{:,} bytes".format(len(complete)))
