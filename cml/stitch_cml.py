#!/usr/bin/env python3
"""Stitch all 7 Classical ML part files into one print/PDF-ready CML_Complete.html.
Reuses Part 1's head/CSS/tracker/script; concatenates each part's content with a
part divider; builds a combined sidebar nav. Re-run after editing any part."""
import re, pathlib

OUT = pathlib.Path(__file__).resolve().parent      # run from the cml/ folder
NP  = 7
PARTS = [
    ("CML_Part1_Foundations.html", "Foundations",
     "What ML is, the maths, data before models, leakage, bias-variance, regularization"),
    ("CML_Part2_LinearDistanceTrees.html", "Linear, Distance &amp; Trees",
     "Linear/logistic/GLM, kNN, Naive Bayes, LDA, SVM, and the decision tree"),
    ("CML_Part3_EnsemblesUnsupervised.html", "Ensembles &amp; Unsupervised",
     "Bagging, boosting, XGB/LGBM/CatBoost, clustering, PCA, ranking, time series"),
    ("CML_Part4_ValidationMetrics.html", "Validation &amp; Metrics",
     "CV, nested CV, HPO, ROC vs PR, thresholds, calibration, imbalance"),
    ("CML_Part5_FeaturesInterpretability.html", "Features &amp; Interpretability",
     "Feature engineering, selection, feature stores, SHAP/PDP/ALE, fairness"),
    ("CML_Part6_ProductionFrontier.html", "Production &amp; Frontier",
     "Serving, drift, retraining, A/B — then TabPFN, conformal, causal, data-centric"),
    ("CML_Part7_QABank.html", "Interview Q&amp;A Bank",
     "105 questions, 15 traps, your PDF map, 15 derivations, 16 coding, 10 cases"),
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
top = top.replace("<title>Classical ML Interview Prep — Part 1: Foundations</title>",
                  "<title>Classical ML Interview Prep — Complete (All 7 Parts)</title>")
top = top.replace('<div class="tt"><small>Part 1 / 7</small>Foundations</div>',
                  '<div class="tt"><small>Complete</small>All 7 Parts</div>')
top = top.replace('<div class="k">Part 1 of 7</div>\n      <div class="v">Foundations</div>',
                  '<div class="k">Complete edition</div>\n      <div class="v">All 7 Parts</div>')

new_hero = ('<header class="hero">\n'
  '        <div class="eyebrow">Complete Resource · All 7 Parts</div>\n'
  '        <h1 class="title">Classical machine learning, end to end\n'
  '          <span class="sub">The full curriculum in one document — foundations and leakage, the model zoo, ensembles and '
  'unsupervised learning, validation and metrics, feature engineering and interpretability, production and the 2026 frontier, '
  'and a 105-question interview bank.</span>\n'
  '        </h1>\n'
  '        <p class="thesis">This is the stitched edition of all seven parts, print- and PDF-ready. The master tracker below '
  'covers every one of the 439 topics; your progress is shared with the individual part files (same browser). '
  'Library-current as of <b>Aug 2026</b> — scikit-learn <b>1.9.0</b> (Python ≥ 3.11; free-threaded CPython support since 1.8), '
  'XGBoost <b>3.4.1</b>, LightGBM <b>4.7.0</b>, CatBoost <b>1.2.10</b>. '
  'The <b>24 interactive widgets</b> compute live in your browser — they work in this combined file too. '
  'Use the sidebar to jump to any part or section.</p>\n'
  '        <div class="meta-chips">\n'
  '          <span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>7 parts</b> · 16 levels</span>\n'
  '          <span class="chip"><b>439</b> tracked topics</span>\n'
  '          <span class="chip">📐 <b>66</b> diagrams</span>\n'
  '          <span class="chip">🎛 <b>24</b> interactive</span>\n'
  '          <span class="chip"><b>105</b> Q&amp;A + 15 traps</span>\n'
  '        </div>\n'
  '      </header>')
top = re.sub(r'<header class="hero">.*?</header>', lambda m: new_hero, top, count=1, flags=re.DOTALL)

# ---- combined sidebar nav ----
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
  '        Classical Machine Learning — <b>Complete edition</b> · all 7 parts · 439 tracked topics · 66 diagrams · '
  '24 interactive widgets · 105 Q&amp;A.<br>\n'
  '        Library-current as of <b>Aug 2026</b> — scikit-learn <b>1.9.0</b> · XGBoost <b>3.4.1</b> · '
  'LightGBM <b>4.7.0</b> · CatBoost <b>1.2.10</b>.<br>\n'
  '        Progress is stored locally under key <code style="color:#8892a0">cmlPrepStatus_v1</code>, shared with every part file; '
  'drill marks under <code style="color:#8892a0">cmlDrill_v1</code>.<br>\n'
  '        Regenerate this file after editing any part with: '
  '<code style="color:#8892a0">python3 stitch_cml.py</code> · '
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
(OUT / "CML_Complete.html").write_text(complete)
print("wrote CML_Complete.html", "{:,} bytes".format(len(complete)))
