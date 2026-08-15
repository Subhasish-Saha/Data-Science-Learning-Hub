#!/usr/bin/env python3
"""Build the Classical ML subject shells: reuse the shared design system from the
RAG Part 1 file, swap in a Classical-ML tracker (own localStorage key:
cmlPrepStatus_v1), per-part chrome, and the interactive-widget CSS layer.
Each shell carries a <!--CONTENT_INSERT--> marker that the content fragments are
spliced into by insert.py."""
import re, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent
SRC  = SITE / "rag" / "RAG_Interview_Prep_Part1_Foundations.html"
MD   = SITE.parent / "classical-ml-study-guide.md"
NP   = 7            # number of parts

LEVEL_KEY = {
 "Level 0 — What ML Actually Is": ("l0","Level 0 · What ML Is"),
 "Level 1 — The Mathematical Toolkit": ("l1","Level 1 · Math Toolkit"),
 "Level 2 — Data Before Models": ("l2","Level 2 · Data Before Models"),
 "Level 3 — The Learning Problem": ("l3","Level 3 · The Learning Problem"),
 "Level 4 — Linear Models": ("l4","Level 4 · Linear Models"),
 "Level 5 — Distance- and Probability-Based Models": ("l5","Level 5 · Distance &amp; Probability"),
 "Level 6 — Decision Trees": ("l6","Level 6 · Decision Trees"),
 "Level 7 — Ensembles & Gradient Boosting": ("l7","Level 7 · Ensembles &amp; Boosting"),
 "Level 8 — Unsupervised Learning": ("l8","Level 8 · Unsupervised"),
 "Level 9 — Beyond Plain Supervised Learning": ("l9","Level 9 · Beyond Supervised"),
 "Level 10 — Model Selection & Validation": ("l10","Level 10 · Validation"),
 "Level 11 — Metrics (the part most candidates fail)": ("l11","Level 11 · Metrics"),
 "Level 12 — Feature Engineering & Selection": ("l12","Level 12 · Feature Engineering"),
 "Level 13 — Interpretability & Fairness": ("l13","Level 13 · Interpretability"),
 "Level 14 — Production ML Engineering": ("l14","Level 14 · Production"),
 "Level 15 — Frontier & Senior Signal": ("l15","Level 15 · Frontier"),
}
CAT = {"l0":"Theory","l1":"Theory","l2":"Practical","l3":"Theory","l4":"Theory","l5":"Theory",
       "l6":"Theory","l7":"Theory","l8":"Theory","l9":"Practical","l10":"Practical","l11":"Practical",
       "l12":"Practical","l13":"Practical","l14":"Practical","l15":"Theory"}
HIGH = {"l2","l3","l6","l7","l10","l11","l12","l13","l14"}

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
 "High-frequency: foundations &amp; framing (7 questions)",
 "High-frequency: bias, variance &amp; generalization (6 questions)",
 "High-frequency: regularization (5 questions)",
 "High-frequency: linear models &amp; GLMs (6 questions)",
 "High-frequency: trees &amp; ensembles (13 questions)",
 "High-frequency: kNN, Naive Bayes, SVM, LDA (5 questions)",
 "High-frequency: unsupervised — clustering, PCA, anomalies (6 questions)",
 "High-frequency: validation &amp; cross-validation (7 questions)",
 "High-frequency: metrics, thresholds &amp; calibration (10 questions)",
 "High-frequency: imbalance &amp; leakage (6 questions)",
 "High-frequency: feature engineering &amp; selection (6 questions)",
 "High-frequency: missing data &amp; preprocessing (4 questions)",
 "High-frequency: interpretability &amp; fairness (5 questions)",
 "High-frequency: production ML (10 questions)",
 "High-frequency: frontier &amp; senior signal (9 questions)",
 "The 15 trap questions (answered correctly, out loud)",
 "Your own PDF question set, mapped — and the gap it reveals",
 "Behavioural / context questions (12 stories prepared)",
]]
MQ = [("mq","Theory","High",t) for t in [
 "Derivation: the normal equation, and why not to invert XᵀX",
 "Derivation: the logistic log-loss gradient (same form as OLS)",
 "Derivation: the bias-variance decomposition for squared loss",
 "Derivation: Ridge = MAP with a Gaussian prior; Lasso = Laplace",
 "Geometry: why the L1 diamond produces exact zeros",
 "Derivation: entropy, Gini and information gain",
 "Derivation: the 63.2% bootstrap result and OOB error",
 "Derivation: why the new boosting learner fits the negative gradient",
 "Derivation: XGBoost's optimal leaf weight and split gain",
 "Derivation: the SVM max-margin objective and where the kernel enters",
 "Derivation: PCA as the SVD of the centred data matrix",
 "Proof: micro-F1 = accuracy in single-label multi-class",
 "Proof: ROC-AUC = P(random positive ranks above random negative)",
 "Derivation: the EM update for a Gaussian mixture",
 "Derivation: the pinball loss recovers the τ-th quantile",
]]
CQ = [("cq","Practical","High",t) for t in [
 "Code: linear regression by normal equation and by gradient descent",
 "Code: logistic regression with L2 from scratch",
 "Code: k-means with k-means++, elbow and silhouette",
 "Code: a decision tree with Gini and recursive splitting",
 "Code: gradient boosting from scratch with stumps",
 "Code: k-fold and StratifiedGroupKFold by hand",
 "Code: a time-series split with a purge/embargo gap",
 "Code: precision, recall, F1, ROC curve and AUC from raw scores",
 "Code: PR curve and average precision under imbalance",
 "Code: reliability diagram + ECE, then Platt vs isotonic",
 "Code: out-of-fold target encoding that provably does not leak",
 "Code: ColumnTransformer + Pipeline with a custom transformer",
 "Code: permutation importance, and its instability under correlation",
 "Code: split conformal prediction + empirical coverage check",
 "Code: PSI and a KS test to flag drifted features",
 "Code: a bootstrap CI for the difference between two models",
]]
SD = [("sd","Interview Prep","High",t) for t in [
 "Case: credit default scoring — explainable, monotonic, audited",
 "Case: real-time payment fraud at a ~150 ms budget",
 "Case: churn + retention offers (the uplift trap)",
 "Case: demand forecasting for 10,000 SKUs",
 "Case: dynamic pricing / price elasticity (causal, not predictive)",
 "Case: predictive maintenance with censoring and cost asymmetry",
 "Case: lead scoring under a fixed sales capacity",
 "Case: insurance claim severity — Tweedie GLM vs GBM",
 "Case: marketing budget allocation and incrementality",
 "Case: great offline, failing in production — debug it systematically",
]]
PP = [("pp","Project","High",t) for t in [
 "Project 1: the leakage post-mortem (build it, break it, fix it)",
 "Project 2: the baseline ladder with an honest cost table",
 "Project 3: the metric that changed the decision",
 "Project 4: calibration study — including a case where it hurt",
 "Project 5: time series done properly (walk-forward + MASE)",
 "Project 6: uplift vs propensity, with a Qini curve",
 "Project 7: conformal intervals, and coverage under drift",
 "Project 8: a drift monitor that does not cry wolf",
]]
rows += [[k,c,p,t] for k,c,p,t in IV+MQ+CQ+SD+PP]

PHASES = {k:v for k,v in LEVEL_KEY.values()}
PHASES.update({"iv":"Interview Q&amp;A Bank","mq":"Math &amp; Derivations","cq":"Coding Questions",
               "sd":"Case &amp; System Design","pp":"Portfolio Projects"})
ORDER = [f"l{i}" for i in range(16)] + ["iv","mq","cq","sd","pp"]
tracker_js = "[\n" + ",\n".join(f'[{i+1},"{r[0]}","{r[1]}","{r[2]}",0,{json.dumps(r[3])}]' for i,r in enumerate(rows)) + "\n]"
TOTAL = len(rows)
print(f"tracker: {TOTAL} items / {len(ORDER)} groups")

# ---------------------------------------------------------------- widget layer
WIDGET_CSS = """
/* ---- interactive widgets (Classical ML) ---- */
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
"""

def build_shell_common(html):
    html = html.replace("</style>", WIDGET_CSS + "</style>", 1)
    return html

P = {
 1: dict(file="CML_Part1_Foundations.html", title="Foundations", pk="L0-3",
   groups=[("L0","What ML Actually Is",[("c1-1","1.1 · The framing question ⭐"),("c1-2","1.2 · The lifecycle"),
     ("c1-3","1.3 · Framing a problem"),("c1-4","1.4 · Baselines you must report")]),
    ("L1","The Mathematical Toolkit",[("c1-5","1.5 · Linear algebra"),("c1-6","1.6 · Calculus &amp; optimization"),
     ("c1-7","1.7 · Probability"),("c1-8","1.8 · Statistics"),("c1-9","1.9 · Distance &amp; similarity")]),
    ("L2","Data Before Models",[("c1-10","1.10 · EDA that earns its time"),("c1-11","1.11 · Missing data"),
     ("c1-12","1.12 · Outliers &amp; robustness"),("c1-13","1.13 · Scaling &amp; transformation"),
     ("c1-14","1.14 · Categorical encoding"),("c1-15","1.15 · Splitting ⭐"),("c1-16","1.16 · Data leakage ⭐⭐")]),
    ("L3","The Learning Problem",[("c1-17","1.17 · Loss functions"),("c1-18","1.18 · ERM &amp; generalization"),
     ("c1-19","1.19 · Bias &amp; variance ⭐"),("c1-20","1.20 · Regularization ⭐"),
     ("c1-21","1.21 · Over- &amp; underfitting"),("c1-22","1.22 · Discriminative vs generative"),
     ("c1-23","1.23 · Interview focus")])],
   h1="The part that decides whether you are trusted",
   sub="What ML actually is and when not to use it, the mathematics you will genuinely be asked about, everything that must happen to data before a model sees it — and the learning problem itself: loss, generalization, bias-variance and regularization.",
   thesis="Almost every senior-level rejection in classical ML traces back to something in this part — a <strong>leaked feature</strong>, a random split on grouped data, a metric chosen before the decision was understood. That is why it comes first and why it is the largest part. Two sections carry disproportionate weight: <strong>1.16 on data leakage</strong>, the most examinable topic in the whole subject, and <strong>1.19–1.20</strong>, the bias-variance decomposition and regularization, which are asked in some form in nearly every interview. Everything here is model-agnostic: it applies equally whether you end up shipping a logistic regression or a tuned LightGBM.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 0–3</b></span>\n          <span class="chip"><b>111</b> topics</span>\n          <span class="chip">📐 <b>14</b> diagrams</span>\n          <span class="chip">🎛 <b>4</b> interactive</span>\n          <span class="chip">⏱ <b>~10h</b></span>',
   prev=("Learning Hub","All subjects"), prevhref="../index.html",
   nxt=("Part 2 · Linear, Distance &amp; Trees",["Linear/logistic, GLMs, SVM","How a tree actually splits"])),
 2: dict(file="CML_Part2_LinearDistanceTrees.html", title="Linear, Distance &amp; Trees", pk="L4-6",
   groups=[("L4","Linear Models",[("c2-1","2.1 · Linear regression"),("c2-2","2.2 · Ridge, Lasso, Elastic Net"),
     ("c2-3","2.3 · Logistic regression ⭐"),("c2-4","2.4 · GLMs and beyond")]),
    ("L5","Distance &amp; Probability",[("c2-5","2.5 · k-Nearest Neighbours"),("c2-6","2.6 · Naive Bayes"),
     ("c2-7","2.7 · LDA &amp; QDA"),("c2-8","2.8 · Support Vector Machines ⭐")]),
    ("L6","Decision Trees",[("c2-9","2.9 · How a tree is built ⭐"),("c2-10","2.10 · Controlling complexity"),
     ("c2-11","2.11 · Properties &amp; the importance trap ⭐"),("c2-12","2.12 · Interview focus")])],
   h1="The model zoo, one honest paragraph each",
   sub="Linear and regularized regression, logistic regression as the interpretability baseline, GLMs for counts and claims, kNN, Naive Bayes, discriminant analysis and SVMs — then the decision tree, split by split.",
   thesis="Interviewers do not ask you to <em>list</em> models; they ask you to <strong>choose</strong> one and defend it. The through-line here is the trade-off each family makes. Linear models buy you interpretability, calibration and a coefficient you can put in an adverse-action notice — which is why <strong>credit scoring still runs on logistic regression</strong>. Distance- and kernel-based models buy you flexibility and charge you scaling sensitivity and <code class=\"ic\">O(n²)</code> training. The <strong>decision tree</strong> is the most important model in this part despite being the weakest, because it is the building block of everything in Part 3 — and because its <strong>feature-importance trap</strong> is one of the most reliable senior filters in the subject.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 4–6</b></span>\n          <span class="chip"><b>45</b> topics</span>\n          <span class="chip">📐 <b>13</b> diagrams</span>\n          <span class="chip">🎛 <b>4</b> interactive</span>\n          <span class="chip">⏱ <b>~7h</b></span>',
   prev=("Part 1 · Foundations","Leakage, bias-variance, regularization"), prevhref="CML_Part1_Foundations.html",
   nxt=("Part 3 · Ensembles &amp; Unsupervised",["Bagging, boosting, XGB/LGBM/CatBoost","Clustering, PCA, time series"])),
 3: dict(file="CML_Part3_EnsemblesUnsupervised.html", title="Ensembles &amp; Unsupervised", pk="L7-9",
   groups=[("L7","Ensembles &amp; Boosting",[("c3-1","3.1 · Why ensembles work"),("c3-2","3.2 · Bagging &amp; Random Forest ⭐"),
     ("c3-3","3.3 · Boosting fundamentals ⭐"),("c3-4","3.4 · XGBoost vs LightGBM vs CatBoost ⭐⭐"),
     ("c3-5","3.5 · Stacking &amp; blending"),("c3-6","3.6 · Sample weighting &amp; costs")]),
    ("L8","Unsupervised Learning",[("c3-7","3.7 · Clustering ⭐"),("c3-8","3.8 · Dimensionality reduction ⭐"),
     ("c3-9","3.9 · Anomaly detection"),("c3-10","3.10 · Association rules &amp; MF")]),
    ("L9","Beyond Supervised",[("c3-11","3.11 · Learning with few labels"),("c3-12","3.12 · Structured &amp; special targets"),
     ("c3-13","3.13 · Ranking &amp; recommendation"),("c3-14","3.14 · Time series with ML ⭐"),
     ("c3-15","3.15 · Interview focus")])],
   h1="What actually wins on tabular data",
   sub="Bagging and Random Forest, gradient boosting from the residual up, the real differences between XGBoost, LightGBM and CatBoost, stacking — then clustering, PCA/t-SNE/UMAP, anomaly detection, survival, ranking and time series.",
   thesis="Level 7 is the most examined level in classical ML, for the simple reason that it is what <strong>wins</strong>. If you can explain, unprompted, that <em>bagging attacks variance and boosting attacks bias</em>, that each new boosting tree is fitted to the <strong>negative gradient of the loss</strong>, and what <strong>leaf-wise growth</strong>, <strong>GOSS</strong> and <strong>ordered boosting</strong> actually change, you have covered a large fraction of the technical surface of a tabular ML interview. The unsupervised half is asked more narrowly but predictably: k-means' assumptions, PCA's scaling requirement, and the <strong>t-SNE trap</strong> — cluster distances and sizes in a t-SNE plot mean nothing.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 7–9</b></span>\n          <span class="chip"><b>66</b> topics</span>\n          <span class="chip">📐 <b>15</b> diagrams</span>\n          <span class="chip">🎛 <b>4</b> interactive</span>\n          <span class="chip">⏱ <b>~9h</b></span>',
   prev=("Part 2 · Linear, Distance &amp; Trees","Logistic, SVM, tree splits"), prevhref="CML_Part2_LinearDistanceTrees.html",
   nxt=("Part 4 · Validation &amp; Metrics",["CV, nested CV, HPO","Thresholds, calibration, imbalance"])),
 4: dict(file="CML_Part4_ValidationMetrics.html", title="Validation &amp; Metrics", pk="L10-11",
   groups=[("L10","Model Selection &amp; Validation",[("c4-1","4.1 · Cross-validation ⭐"),("c4-2","4.2 · Nested CV ⭐"),
     ("c4-3","4.3 · Hyperparameter optimization"),("c4-4","4.4 · Diagnostics"),
     ("c4-5","4.5 · Comparing models honestly")]),
    ("L11","Metrics",[("c4-6","4.6 · Classification metrics ⭐"),("c4-7","4.7 · Regression metrics"),
     ("c4-8","4.8 · Ranking metrics"),("c4-9","4.9 · Choosing a threshold ⭐"),
     ("c4-10","4.10 · Calibration ⭐"),("c4-11","4.11 · Imbalanced classification ⭐⭐"),
     ("c4-12","4.12 · Interview focus")])],
   h1="Where interviews are actually lost",
   sub="Cross-validation and its variants, nested CV, modern hyperparameter search, honest model comparison — then the metrics level: ROC vs PR, thresholds as a business decision, calibration, and the right order of operations for imbalance.",
   thesis="This is the part most candidates fail, and they fail it in a recognisable way: they report a number the metric cannot support. Accuracy under 1:1000 imbalance. ROC-AUC quoted as if it said something about <strong>calibration</strong>. A tuned score reported from the same CV it was tuned on. A 0.5 threshold treated as a decision rather than a default. Each of those has a one-sentence correction and this part gives you all of them, with the tooling that makes them cheap — <code class=\"ic\">TunedThresholdClassifierCV</code>, reliability diagrams, purged time-series splits, and the <strong>imbalance order of operations</strong>: threshold first, class weights second, resampling last and only if needed.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 10–11</b></span>\n          <span class="chip"><b>57</b> topics</span>\n          <span class="chip">📐 <b>14</b> diagrams</span>\n          <span class="chip">🎛 <b>4</b> interactive</span>\n          <span class="chip">⏱ <b>~9h</b></span>',
   prev=("Part 3 · Ensembles &amp; Unsupervised","Boosting, clustering, time series"), prevhref="CML_Part3_EnsemblesUnsupervised.html",
   nxt=("Part 5 · Features &amp; Interpretability",["Feature stores, point-in-time","SHAP, ALE, fairness"])),
 5: dict(file="CML_Part5_FeaturesInterpretability.html", title="Features &amp; Interpretability", pk="L12-13",
   groups=[("L12","Feature Engineering",[("c5-1","5.1 · Why it still matters"),("c5-2","5.2 · Numeric features"),
     ("c5-3","5.3 · Categorical, datetime &amp; text"),("c5-4","5.4 · Feature selection"),
     ("c5-5","5.5 · Pipelines &amp; feature stores ⭐")]),
    ("L13","Interpretability &amp; Fairness",[("c5-6","5.6 · The taxonomy"),
     ("c5-7","5.7 · The three feature importances ⭐"),("c5-8","5.8 · PDP, ICE, ALE, LIME, SHAP ⭐"),
     ("c5-9","5.9 · Fairness ⭐"),("c5-10","5.10 · Interview focus")])],
   h1="Exposing structure, then explaining it",
   sub="Feature engineering that beats model choice on tabular data, selection done inside the CV loop, production feature pipelines and point-in-time correctness — then the interpretability toolkit and the fairness questions that follow it.",
   thesis="On tabular data, <strong>feature engineering routinely beats model choice</strong> — a model can only use structure you expose. But the two ideas that make this part senior-level are less obvious. The first is <strong>point-in-time correctness</strong>: reconstructing what a feature's value <em>was</em> at prediction time rather than what it is now, which is simultaneously a feature-store design problem and the deepest form of the leakage question from Part 1. The second is that there are <strong>three different feature importances</strong> answering three different questions, and that <strong>SHAP is not an oracle</strong> — KernelSHAP assumes independence, path-dependent TreeSHAP can hand non-zero credit to features that do not affect the prediction, and correlated features distort all of them.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 12–13</b></span>\n          <span class="chip"><b>39</b> topics</span>\n          <span class="chip">📐 <b>12</b> diagrams</span>\n          <span class="chip">🎛 <b>3</b> interactive</span>\n          <span class="chip">⏱ <b>~6h</b></span>',
   prev=("Part 4 · Validation &amp; Metrics","CV, calibration, imbalance"), prevhref="CML_Part4_ValidationMetrics.html",
   nxt=("Part 6 · Production &amp; Frontier",["Serving, drift, retraining, A/B","TabPFN, conformal, causal"])),
 6: dict(file="CML_Part6_ProductionFrontier.html", title="Production &amp; Frontier", pk="L14-15",
   groups=[("L14","Production ML",[("c6-1","6.1 · The architecture"),("c6-2","6.2 · Serving"),
     ("c6-3","6.3 · Monitoring &amp; drift ⭐"),("c6-4","6.4 · Retraining &amp; deployment"),
     ("c6-5","6.5 · A/B testing a model"),("c6-6","6.6 · Engineering hygiene")]),
    ("L15","Frontier &amp; Senior Signal",[("c6-7","6.7 · Tabular foundation models ⭐⭐"),
     ("c6-8","6.8 · Uncertainty &amp; conformal ⭐"),("c6-9","6.9 · Causal inference ⭐"),
     ("c6-10","6.10 · Data-centric ML"),("c6-11","6.11 · Shift, robustness &amp; the big question"),
     ("c6-12","6.12 · Interview focus")])],
   h1="Shipping it, and the questions that are still open",
   sub="Training/serving architecture, latency budgets, drift detection when labels arrive late, retraining triggers and A/B testing — then the frontier: tabular foundation models, conformal prediction, causal inference and data-centric ML.",
   thesis="The production half is where senior interviews spend most of their time, and the highest-value idea in it is negative: <strong>not every drift alert warrants a retrain</strong>. Confirm the distribution change actually degraded the metric first — alert fatigue kills monitoring programmes faster than missing drift does. The frontier half exists to give you defensible positions on the four questions that separate a 2026 candidate from a 2019 one: whether <strong>GBDTs still beat deep learning on tabular data</strong> (genuinely contested now — <strong>TabPFN-3</strong>), how you attach a <strong>guarantee</strong> to a prediction (conformal), why a churn model is the <em>wrong</em> model for deciding who gets a discount (<strong>uplift/CATE</strong>), and why most of the remaining accuracy is in the data rather than the model.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 14–15</b></span>\n          <span class="chip"><b>54</b> topics</span>\n          <span class="chip">📐 <b>14</b> diagrams</span>\n          <span class="chip">🎛 <b>3</b> interactive</span>\n          <span class="chip">⏱ <b>~8h</b></span>',
   prev=("Part 5 · Features &amp; Interpretability","Feature stores, SHAP, fairness"), prevhref="CML_Part5_FeaturesInterpretability.html",
   nxt=("Part 7 · Interview Q&amp;A Bank",["105 questions + 15 traps","15 derivations, 10 cases"])),
 7: dict(file="CML_Part7_QABank.html", title="Interview Q&amp;A Bank", pk="QA",
   groups=[("QA","The Question Bank",[("c7-1","7.1 · Foundations &amp; framing"),
     ("c7-2","7.2 · Bias, variance &amp; generalization"),("c7-3","7.3 · Regularization"),
     ("c7-4","7.4 · Linear models"),("c7-5","7.5 · Trees &amp; ensembles"),("c7-6","7.6 · Other models"),
     ("c7-7","7.7 · Unsupervised"),("c7-8","7.8 · Validation"),("c7-9","7.9 · Metrics"),
     ("c7-10","7.10 · Imbalance &amp; leakage"),("c7-11","7.11 · Feature engineering"),
     ("c7-12","7.12 · Missing data &amp; preprocessing"),("c7-13","7.13 · Interpretability"),
     ("c7-14","7.14 · Production"),("c7-15","7.15 · Frontier &amp; senior signal")]),
    ("REF","Traps &amp; Reference",[("c7-16","7.16 · The 15 traps ⭐⭐"),("c7-17","7.17 · Your PDF map ⭐"),
     ("c7-18","7.18 · Math &amp; derivations"),("c7-19","7.19 · Coding questions"),
     ("c7-20","7.20 · Case &amp; system design"),("c7-21","7.21 · Behavioural questions"),
     ("c7-22","7.22 · Formula sheet &amp; legacy→modern map")])],
   h1="The question bank",
   sub="105 high-frequency questions with model answers, the 15 trap questions, your own PDF set mapped honestly, 15 derivations, 16 coding exercises, 10 case designs, 12 behavioural questions, and the reference sheets.",
   thesis="The consolidated <strong>drill</strong>. Read the question, answer it out loud, <em>then</em> expand the answer and compare — reading answers you already half-know is the least efficient possible use of this page. Two sections deserve the most attention. <strong>§7.16, the traps</strong>, because classical ML interviews are lost on a small number of confidently-wrong answers: &ldquo;95% accurate&rdquo; on an imbalanced problem, SMOTE reached for first, <code class=\"ic\">feature_importances_</code> quoted without qualification, a 0.99 AUC celebrated rather than investigated. And <strong>§7.17</strong>, which maps your own PDF set — and states plainly that it contains almost no classical ML, which is a gap in your prep rather than a coverage overlap.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Q&amp;A Bank</b></span>\n          <span class="chip"><b>105</b> questions</span>\n          <span class="chip">15 <b>traps</b></span>\n          <span class="chip">🎛 <b>2</b> interactive</span>\n          <span class="chip">⏱ <b>~6h</b> drill</span>',
   prev=("Part 6 · Production &amp; Frontier","Drift, TabPFN, conformal, causal"), prevhref="CML_Part6_ProductionFrontier.html",
   nxt=("Learning Hub",["All subjects"])),
}

def build(pn):
    c = P[pn]; html = SRC.read_text()
    s = html.index("</section>", html.index('id="tracker"')) + len("</section>")
    e = html.index("      <!-- PART NAV -->")
    html = html[:s] + "\n\n<!--CONTENT_INSERT-->\n\n      " + html[e:]
    html = html.replace("<title>RAG Interview Prep — Part 1: Foundations</title>",
                        f"<title>Classical ML Interview Prep — Part {pn}: {c['title']}</title>")
    html = html.replace('<div class="tt"><small>Part 1 / 6</small>Foundations</div>',
                        f'<div class="tt"><small>Part {pn} / {NP}</small>{c["title"]}</div>')
    html = html.replace('<div class="brand-txt">RAG Prep<small>Knowledge Base</small></div>',
                        '<div class="brand-txt">Classical ML<small>Tabular · Metrics · Production</small></div>')
    html = html.replace('<div class="k">Part 1 of 6</div>\n      <div class="v">Foundations</div>',
                        f'<div class="k">Part {pn} of {NP}</div>\n      <div class="v">{c["title"]}</div>')
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
           '<li><a href="index.html">← Classical ML home</a></li></ul>\n      </div>\n    </nav>')
    html = re.sub(r'<nav class="toc" id="toc">.*?</nav>', lambda m: nav, html, count=1, flags=re.DOTALL)
    html = re.sub(r'<div class="sb-foot">.*?</div>',
        f'<div class="sb-foot">\n      Classical Machine Learning<br>Part {pn} — {c["title"]}<br>© your study kit\n    </div>',
        html, count=1, flags=re.DOTALL)
    hero = (f'<header class="hero">\n        <div class="eyebrow">Part {pn} of {NP} · {c["title"]}</div>\n'
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
      f'<div class="doc-foot">\n        Classical Machine Learning — Part {pn} of {NP} · {c["title"]}<br>\n'
      f'        Library-current as of <b>Aug 2026</b> — scikit-learn <b>1.9.0</b> · XGBoost <b>3.4.1</b> · '
      f'LightGBM <b>4.7.0</b> · CatBoost <b>1.2.10</b>.<br>\n'
      f'        Progress is stored locally under key <code style="color:#8892a0">cmlPrepStatus_v1</code> and is shared by every part of this subject.\n      </div>',
      html, count=1, flags=re.DOTALL)
    _ph = "const PHASES = " + json.dumps(PHASES, ensure_ascii=False) + ";"
    _or = "const ORDER = " + json.dumps(ORDER) + ";"
    _tk = "const TRACKER = " + tracker_js + ";"
    html = re.sub(r'const PHASES = \{.*?\};', lambda m:_ph, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const ORDER = \[.*?\];', lambda m:_or, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const TRACKER = \[.*?\n\];', lambda m:_tk, html, count=1, flags=re.DOTALL)
    html = html.replace('const LS_KEY="ragPrepStatus_v1";','const LS_KEY="cmlPrepStatus_v1";').replace("206",str(TOTAL))
    html = re.sub(r'<p class="tk-sub">.*?</p>',
      f'<p class="tk-sub">One tracker for the whole Classical ML subject — all {TOTAL} topics across all {NP} parts. '
      f'Set a status on any row; your progress saves in this browser and prints as a clean checklist.</p>',
      html, count=1, flags=re.DOTALL)
    html = build_shell_common(html)
    (HERE/c["file"]).write_text(html)
    assert "<!--CONTENT_INSERT-->" in html and "ragPrepStatus" not in html
    print(f"  {c['file']} ({len(html):,}b)")

if __name__ == "__main__":
    for p in ([int(a) for a in sys.argv[1:]] or P): build(p)
