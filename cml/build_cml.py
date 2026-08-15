#!/usr/bin/env python3
"""Build the Classical ML subject shells.

v2 — one part per level (16 levels + a Q&A bank = 17 parts), so every topic has
room for a full treatment: prose, diagrams, code, and its OWN interview Q&A box
(the pattern the RAG subject uses).

Reuses the shared design system from the RAG Part 1 file, swaps in a Classical-ML
tracker (own localStorage key: cmlPrepStatus_v1), per-part chrome, and the
interactive-widget CSS layer. Each shell carries a <!--CONTENT_INSERT--> marker
that the content fragments are spliced into by insert.py."""
import re, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent
SRC  = SITE / "rag" / "RAG_Interview_Prep_Part1_Foundations.html"
MD   = SITE.parent / "classical-ml-study-guide.md"
NP   = 17            # number of parts

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
HIGH = {"l2","l3","l4","l6","l7","l10","l11","l12","l13","l14"}

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

# ------------------------------------------------------------------- part spec
def G(pk, head, links): return (pk, head, links)

P = {}

def part(n, file, title, pk, groups, h1, sub, thesis, chips, prev, prevhref, nxt):
    P[n] = dict(file=file, title=title, pk=pk, groups=groups, h1=h1, sub=sub,
                thesis=thesis, chips=chips, prev=prev, prevhref=prevhref, nxt=nxt)

def chips(level, topics, diagrams, inter, hours):
    s = ('<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>%s</b></span>\n'
         '          <span class="chip"><b>%d</b> topics</span>\n'
         '          <span class="chip">📐 <b>%d</b> diagrams</span>\n') % (level, topics, diagrams)
    if inter: s += '          <span class="chip">🎛 <b>%d</b> interactive</span>\n' % inter
    s += '          <span class="chip">⏱ <b>~%s</b></span>' % hours
    return s

part(1, "CML_Part01_WhatMLIs.html", "What ML Actually Is", "L0",
 [G("L0","What ML Actually Is",[("c1-1","1.1 · Rules vs examples ⭐"),("c1-2","1.2 · The five paradigms"),
   ("c1-3","1.3 · Prediction vs inference vs decision ⭐"),("c1-4","1.4 · The ML lifecycle"),
   ("c1-5","1.5 · Framing a problem ⭐"),("c1-6","1.6 · Baselines you must report"),
   ("c1-7","1.7 · When NOT to use ML ⭐⭐")])],
 "The questions asked before any model exists",
 "What machine learning actually trades away, the five learning paradigms and where real problems fall, the difference between predicting, explaining and deciding, the lifecycle, how to frame a target — and the senior answer: when not to use ML at all.",
 "This part contains no algorithms, and it is where a surprising number of interviews are decided. Every question here is really the same question: <strong>do you understand what you are buying and what you are giving up?</strong> ML trades explicit, auditable rules for examples plus a loss function — a good trade when the rule is genuinely unknown, and a terrible one when it isn't. The three highest-value habits in this part are <strong>naming the task type before proposing anything</strong>, <strong>separating prediction from inference from decision</strong> (they are three different projects with three different methods), and <strong>always reporting baselines</strong>. Each topic ends with the interview questions it answers.",
 chips("Level 0", 7, 9, 1, "4h"), ("Learning Hub","All subjects"), "../index.html",
 ("Part 2 · The Mathematical Toolkit",["Linear algebra, calculus, probability","Distance and the curse of dimensionality"]))

part(2, "CML_Part02_MathToolkit.html", "The Mathematical Toolkit", "L1",
 [G("L1","The Mathematical Toolkit",[("c2-1","2.1 · Linear algebra"),("c2-2","2.2 · Calculus &amp; optimization ⭐"),
   ("c2-3","2.3 · Probability &amp; Bayes ⭐"),("c2-4","2.4 · Maximum likelihood &amp; MAP ⭐"),
   ("c2-5","2.5 · Statistics you actually use"),("c2-6","2.6 · Distance &amp; similarity"),
   ("c2-7","2.7 · The curse of dimensionality ⭐")])],
 "The maths you will genuinely be asked about",
 "Vectors, norms, eigenvectors and the SVD; gradients, convexity and second-order methods; Bayes and the base-rate fallacy; the MLE/MAP bridge that turns every loss into a probabilistic statement; the statistics of comparing models; and why distance stops meaning anything in high dimensions.",
 "You will not be asked to prove a theorem. You will be asked what an eigenvector has to do with PCA, why XGBoost bothers with second derivatives, and what a p-value is <em>not</em>. The single highest-value item here is the <strong>MLE/MAP bridge</strong>: least squares <em>is</em> maximum likelihood under Gaussian noise, log loss <em>is</em> maximum likelihood under a Bernoulli, <strong>Ridge is MAP with a Gaussian prior and Lasso with a Laplace prior</strong>. Once you see that, regularization stops being a trick that stops overfitting and becomes a stated belief about the coefficients — which is exactly the framing that makes §4.4 easy.",
 chips("Level 1", 7, 10, 2, "6h"), ("Part 1 · What ML Actually Is","Framing, lifecycle, baselines"), "CML_Part01_WhatMLIs.html",
 ("Part 3 · Data Before Models",["Missingness, encoding, splitting","The four kinds of leakage"]))

part(3, "CML_Part03_DataBeforeModels.html", "Data Before Models", "L2",
 [G("L2","Data Before Models",[("c3-1","3.1 · EDA that earns its time"),("c3-2","3.2 · Missing data ⭐"),
   ("c3-3","3.3 · Outliers &amp; robustness"),("c3-4","3.4 · Scaling &amp; transformation ⭐"),
   ("c3-5","3.5 · Categorical encoding ⭐"),("c3-6","3.6 · Splitting ⭐⭐"),
   ("c3-7","3.7 · Data leakage ⭐⭐"),("c3-8","3.8 · Auditing for leakage")])],
 "Where careers are made or lost",
 "The three questions EDA exists to answer, the missingness taxonomy and the indicator trick, outliers as a judgement call, who needs scaling and why, categorical encoding up to cross-fitted target encoding, the split that simulates deployment — and the four kinds of data leakage.",
 "Almost every senior-level rejection traces back to something in this part. Not a modelling mistake — a <strong>leaked feature</strong>, a random split on grouped data, an imputer fitted before the split. This is also the most examinable material in the whole subject, because it is checkable: an interviewer can hand you a notebook and ask what is wrong with it. Two sections carry the weight: <strong>3.6 on splitting</strong>, whose single rule is <em>your split must simulate how the model will actually be used</em>, and <strong>3.7 on leakage</strong>, where you must be able to name all four kinds, their symptoms, and the one structural fix that prevents most of them.",
 chips("Level 2", 8, 12, 2, "7h"), ("Part 2 · The Mathematical Toolkit","Bayes, MLE/MAP, distance"), "CML_Part02_MathToolkit.html",
 ("Part 4 · The Learning Problem",["Loss, bias-variance, regularization","Over- and underfitting in practice"]))

part(4, "CML_Part04_LearningProblem.html", "The Learning Problem", "L3",
 [G("L3","The Learning Problem",[("c4-1","4.1 · Loss functions ⭐"),("c4-2","4.2 · ERM &amp; generalization"),
   ("c4-3","4.3 · Bias-variance ⭐⭐"),("c4-4","4.4 · L1 vs L2 regularization ⭐⭐"),
   ("c4-5","4.5 · Regularization beyond penalties"),("c4-6","4.6 · Over- &amp; underfitting in practice ⭐"),
   ("c4-7","4.7 · Discriminative vs generative")])],
 "What &ldquo;best&rdquo; means, and why models fail",
 "The loss function as a definition of best, empirical risk minimization and where the i.i.d. assumption breaks, the bias-variance decomposition with its diagnostic, L1 versus L2 in all three of its answers, structural and implicit regularization, and the learning-curve reading that tells you whether more data will help.",
 "Two questions from this part appear in almost every classical ML interview: <strong>&ldquo;explain the bias-variance trade-off&rdquo;</strong> and <strong>&ldquo;L1 versus L2&rdquo;</strong>. Both have a complete answer and a partial one, and the difference is visible immediately. The complete bias-variance answer <em>writes the decomposition</em>, gives the <em>two-number diagnostic</em>, and notes that it is exact only for squared loss. The complete L1/L2 answer has a <strong>geometric half</strong> (the diamond's corners lie on the axes), a <strong>probabilistic half</strong> (MAP with a Laplace prior), and a <strong>practical half</strong> (Lasso is unstable under correlation; Elastic Net fixes it). Both widgets in this part let you watch those claims happen.",
 chips("Level 3", 7, 11, 2, "7h"), ("Part 3 · Data Before Models","Splitting, leakage, encoding"), "CML_Part03_DataBeforeModels.html",
 ("Part 5 · Linear Models",["Every LR assumption, and what breaks","Logistic, odds ratios, GLMs"]))

part(5, "CML_Part05_LinearModels.html", "Linear Models", "L4",
 [G("L4","Linear Models",[("c5-1","5.1 · The model &amp; how it's fitted ⭐"),
   ("c5-2","5.2 · The assumptions, one by one ⭐⭐"),("c5-3","5.3 · Residual diagnostics ⭐"),
   ("c5-4","5.4 · Multicollinearity &amp; VIF ⭐"),("c5-5","5.5 · R², adjusted R² &amp; friends"),
   ("c5-6","5.6 · Ridge, Lasso &amp; Elastic Net ⭐"),("c5-7","5.7 · Logistic regression ⭐⭐"),
   ("c5-8","5.8 · GLMs — links &amp; families ⭐"),("c5-9","5.9 · Quantile &amp; robust regression")])],
 "The models you must be able to defend line by line",
 "Linear regression from the normal equation to why nobody computes it that way; <strong>every assumption, what breaks when it fails, how to detect it and how to fix it</strong>; the full residual-diagnostic toolkit; multicollinearity and VIF; R² and its traps; the regularized family; logistic regression and the odds ratio; GLMs for counts, claims and skew; and quantile regression.",
 "This is the deepest part of the subject and the one interviewers use to separate people who have <em>used</em> a linear model from people who have <em>fitted</em> one. The centrepiece is <strong>§5.2</strong>: five assumptions, each with what it means, what breaks when it fails, how you detect it, and what you do about it — because &ldquo;state the assumptions of linear regression&rdquo; is asked constantly and answered badly. The two most common errors are believing <strong>normality of residuals is needed for prediction</strong> (it is not — only for inference) and believing <strong>multicollinearity hurts predictions</strong> (it usually hurts interpretation instead). Logistic regression gets the same treatment, because credit scoring runs on it for reasons you should be able to name.",
 chips("Level 4", 9, 14, 3, "9h"), ("Part 4 · The Learning Problem","Loss, bias-variance, regularization"), "CML_Part04_LearningProblem.html",
 ("Part 6 · Distance &amp; Probability Models",["kNN, Naive Bayes, LDA/QDA","SVM margins and the kernel trick"]))

part(6, "CML_Part06_DistanceProbability.html", "Distance &amp; Probability Models", "L5",
 [G("L5","Distance &amp; Probability",[("c6-1","6.1 · k-Nearest Neighbours ⭐"),("c6-2","6.2 · Naive Bayes ⭐"),
   ("c6-3","6.3 · LDA &amp; QDA ⭐"),("c6-4","6.4 · SVM — the margin ⭐"),
   ("c6-5","6.5 · Soft margin &amp; C"),("c6-6","6.6 · The kernel trick ⭐⭐"),
   ("c6-7","6.7 · When to still use these")])],
 "Four models, four different assumptions about the world",
 "kNN as a pure bias-variance dial with mandatory scaling; Naive Bayes and why a false assumption still classifies correctly; LDA and QDA as generative classifiers and as dimensionality reduction; and support vector machines from the margin through the soft-margin C to the kernel trick and the dual.",
 "None of these are likely to be your production model on tabular data in 2026, and all four are asked about constantly — because each one isolates a concept with nothing else in the way. <strong>kNN</strong> isolates distance, scaling and the bias-variance dial. <strong>Naive Bayes</strong> isolates the difference between a correct <em>argmax</em> and a correct <em>probability</em>. <strong>LDA</strong> isolates supervised versus unsupervised projection. <strong>SVM</strong> isolates constrained optimization and the kernel trick — and it is the topic where candidates most often recite &ldquo;it maps to a higher dimension&rdquo; without being able to say <em>where in the maths that happens</em>. It happens in the dual, and this part shows you exactly where.",
 chips("Level 5", 7, 11, 2, "7h"), ("Part 5 · Linear Models","Assumptions, diagnostics, GLMs"), "CML_Part05_LinearModels.html",
 ("Part 7 · Decision Trees",["Splits, impurity, information gain","Pruning and the importance trap"]))

part(7, "CML_Part07_DecisionTrees.html", "Decision Trees", "L6",
 [G("L6","Decision Trees",[("c7-1","7.1 · How a tree is built ⭐⭐"),("c7-2","7.2 · Split criteria ⭐"),
   ("c7-3","7.3 · Regression trees"),("c7-4","7.4 · Controlling complexity ⭐"),
   ("c7-5","7.5 · Pruning"),("c7-6","7.6 · Strengths &amp; failure modes ⭐"),
   ("c7-7","7.7 · The feature-importance trap ⭐⭐")])],
 "The building block of everything that wins",
 "Recursive binary splitting step by step, Gini versus entropy versus information gain (and the honest answer), variance reduction for regression, every complexity hyperparameter and what it actually controls, pre- and post-pruning, the three failure modes worth drawing — and the feature-importance trap.",
 "A single decision tree is the weakest model in this guide and the most important one to understand, because <strong>every model in Part 8 is made of these</strong>. If you cannot compute an information gain by hand, the ensembles conversation will not go well. Two things here are disproportionately examined. The first is the <strong>greedy, locally-optimal</strong> nature of the algorithm — it never revisits an earlier split, which is why the tree it builds is not the globally optimal tree. The second is the <strong>feature-importance trap</strong>: the default <code class=\"ic\">feature_importances_</code> is biased toward high-cardinality and continuous features and is computed on training data, and knowing that is one of the most reliable senior filters in the subject.",
 chips("Level 6", 7, 10, 2, "6h"), ("Part 6 · Distance &amp; Probability","kNN, NB, LDA, SVM"), "CML_Part06_DistanceProbability.html",
 ("Part 8 · Ensembles &amp; Boosting",["Bagging, Random Forest, OOB","XGBoost vs LightGBM vs CatBoost"]))

part(8, "CML_Part08_Ensembles.html", "Ensembles &amp; Gradient Boosting", "L7",
 [G("L7","Ensembles &amp; Boosting",[("c8-1","8.1 · Why ensembles work ⭐"),("c8-2","8.2 · Bagging ⭐"),
   ("c8-3","8.3 · Random Forest &amp; OOB ⭐⭐"),("c8-4","8.4 · AdaBoost"),
   ("c8-5","8.5 · Gradient boosting ⭐⭐"),("c8-6","8.6 · XGBoost, LightGBM, CatBoost ⭐⭐"),
   ("c8-7","8.7 · Tuning a GBM ⭐"),("c8-8","8.8 · Stacking &amp; blending ⭐"),
   ("c8-9","8.9 · Sample weights &amp; costs")])],
 "What actually wins on tabular data",
 "The variance formula that explains why ensembling works at all, bagging and the bootstrap, Random Forest's decorrelation trick and out-of-bag error, AdaBoost as a special case, gradient boosting derived from function-space descent, the real mechanisms behind XGBoost/LightGBM/CatBoost, a tuning order that works, and stacking's leakage trap.",
 "The most examined level in classical ML, because it is what wins. Four sentences from this part carry an unreasonable share of the marks. <strong>&ldquo;Bagging attacks variance, boosting attacks bias.&rdquo;</strong> <strong>&ldquo;Random Forest is bagging plus random feature subsetting at each split, and that subsetting is what decorrelates the trees.&rdquo;</strong> <strong>&ldquo;Each boosting tree is fitted to the negative gradient of the loss with respect to the current predictions.&rdquo;</strong> And the selection rule for the three libraries, followed by the honest caveat that <em>once tuned they are usually within noise of each other</em>. If you can say all four with the mechanism attached, you have covered a large fraction of a tabular ML interview.",
 chips("Level 7", 9, 14, 2, "9h"), ("Part 7 · Decision Trees","Splits, pruning, importance"), "CML_Part07_DecisionTrees.html",
 ("Part 9 · Unsupervised Learning",["k-means, DBSCAN, GMM","PCA, t-SNE, UMAP, anomalies"]))

part(9, "CML_Part09_Unsupervised.html", "Unsupervised Learning", "L8",
 [G("L8","Unsupervised Learning",[("c9-1","9.1 · k-means ⭐⭐"),("c9-2","9.2 · Choosing k ⭐"),
   ("c9-3","9.3 · Hierarchical clustering"),("c9-4","9.4 · DBSCAN &amp; HDBSCAN ⭐"),
   ("c9-5","9.5 · GMM and EM ⭐"),("c9-6","9.6 · PCA ⭐⭐"),
   ("c9-7","9.7 · t-SNE, UMAP &amp; the trap ⭐"),("c9-8","9.8 · Anomaly detection ⭐"),
   ("c9-9","9.9 · Association rules &amp; MF")])],
 "Structure without labels",
 "Lloyd's algorithm and k-means' three assumptions, every method for choosing k and the honest answer, hierarchical linkage and dendrograms, density-based clustering, Gaussian mixtures and EM, PCA from the covariance eigen-decomposition, the t-SNE trap everyone should state unprompted, anomaly detection without labels, and association rules.",
 "Unsupervised learning is asked about more narrowly than supervised learning but very predictably, and the questions cluster around <em>assumptions</em> rather than algorithms. k-means assumes <strong>spherical, roughly equal-variance clusters</strong> and a meaningful Euclidean distance, which is why it is scale-sensitive and fails on rings. PCA maximises <strong>variance</strong>, which has units, which is why you must scale first. And the trap that separates people who have <em>read</em> about t-SNE from people who have <em>used</em> it: <strong>distances between clusters and cluster sizes in a t-SNE plot are meaningless</strong>. Volunteering that unprompted is worth more than describing the algorithm.",
 chips("Level 8", 9, 13, 2, "8h"), ("Part 8 · Ensembles &amp; Boosting","Bagging, boosting, GBM libraries"), "CML_Part08_Ensembles.html",
 ("Part 10 · Beyond Plain Supervised",["Few labels, survival, ranking","Time series done properly"]))

part(10, "CML_Part10_BeyondSupervised.html", "Beyond Plain Supervised Learning", "L9",
 [G("L9","Beyond Supervised",[("c10-1","10.1 · Learning with few labels ⭐"),
   ("c10-2","10.2 · Multi-label &amp; ordinal targets"),("c10-3","10.3 · Survival analysis ⭐"),
   ("c10-4","10.4 · Ranking &amp; recommendation ⭐"),("c10-5","10.5 · Time series as supervised learning ⭐"),
   ("c10-6","10.6 · Forecast validation &amp; metrics ⭐⭐")])],
 "When the target isn't a plain label",
 "Active learning, weak supervision and pseudo-labelling; multi-label and ordinal targets and why treating them as multi-class throws information away; survival analysis and censoring; learning to rank and nDCG; framing forecasting as supervised learning; and walk-forward validation with purging and embargo.",
 "Recognising that a target is <em>not</em> plain binary classification is very often the whole insight a case question is testing. Four trigger phrases are worth memorising. <em>&ldquo;When will this happen?&rdquo;</em> rather than <em>&ldquo;will it happen?&rdquo;</em> ⇒ <strong>survival analysis with censoring</strong>. <em>&ldquo;Rank these for a user&rdquo;</em> ⇒ <strong>learning to rank and nDCG</strong>, not classification with a sort. <em>&ldquo;Poor / fair / good&rdquo;</em> ⇒ <strong>ordinal</strong>, not multi-class. <em>&ldquo;Forecast the next N periods&rdquo;</em> ⇒ lag features, a <strong>global model</strong>, and above all <strong>walk-forward validation with a gap</strong> — the place where more forecasting projects go wrong than anywhere else.",
 chips("Level 9", 6, 9, 1, "6h"), ("Part 9 · Unsupervised Learning","Clustering, PCA, anomalies"), "CML_Part09_Unsupervised.html",
 ("Part 11 · Model Selection &amp; Validation",["The CV family, nested CV","Hyperparameter search that works"]))

part(11, "CML_Part11_Validation.html", "Model Selection &amp; Validation", "L10",
 [G("L10","Validation",[("c11-1","11.1 · The cross-validation family ⭐⭐"),("c11-2","11.2 · Choosing k"),
   ("c11-3","11.3 · Nested cross-validation ⭐⭐"),("c11-4","11.4 · Hyperparameter search ⭐"),
   ("c11-5","11.5 · Learning &amp; validation curves ⭐"),("c11-6","11.6 · Slice analysis ⭐"),
   ("c11-7","11.7 · Comparing models honestly ⭐")])],
 "Producing a number you can defend",
 "Hold-out through k-fold, stratified, grouped and time-series splits; how k itself trades bias against variance; nested CV and the optimism it removes; grid versus random versus Bayesian search with the result that explains why; learning and validation curves as decision tools; per-slice error analysis; and the statistics of an honest model comparison.",
 "Everything you report rests on this part, which is why it comes before metrics rather than after. The single most valuable idea is that <strong>a tuned CV score is a selection statistic, not an estimate</strong> — it is the maximum of many noisy numbers, so it is optimistically biased even if every setting were equally good. That is what nested CV exists to fix. The second is that <strong>an aggregate metric tells you whether something is wrong, and only slice analysis tells you what</strong>. And the third is the answer to &ldquo;your model is 0.4% better — is it better?&rdquo;, which has a statistical half, a multiple-comparisons half and a <em>practical</em> half, and needs all three.",
 chips("Level 10", 7, 11, 2, "7h"), ("Part 10 · Beyond Plain Supervised","Survival, ranking, time series"), "CML_Part10_BeyondSupervised.html",
 ("Part 12 · Metrics",["ROC vs PR, thresholds","Calibration and imbalance"]))

part(12, "CML_Part12_Metrics.html", "Metrics, Thresholds &amp; Imbalance", "L11",
 [G("L11","Metrics",[("c12-1","12.1 · The confusion matrix ⭐⭐"),("c12-2","12.2 · Precision, recall &amp; F-β ⭐"),
   ("c12-3","12.3 · ROC-AUC vs PR-AUC ⭐⭐"),("c12-4","12.4 · Multi-class averaging ⭐"),
   ("c12-5","12.5 · Regression metrics ⭐"),("c12-6","12.6 · Ranking metrics"),
   ("c12-7","12.7 · Choosing a threshold ⭐⭐"),("c12-8","12.8 · Calibration ⭐⭐"),
   ("c12-9","12.9 · Imbalanced classification ⭐⭐")])],
 "The level most candidates fail",
 "The confusion matrix and everything derived from it, precision/recall/F-β and where each dominates, the ROC-versus-PR question with its structural explanation, micro/macro/weighted averaging, regression metrics chosen from the decision, ranking metrics that know about position, thresholds as a business decision, calibration end to end, and the correct order of operations for imbalance.",
 "Interviews are lost here, and they are lost in a recognisable way: <strong>a number is reported that the metric cannot support</strong>. Accuracy under 1:1000 imbalance. ROC-AUC quoted as though it said something about calibration. A tuned score reported from the CV it was tuned on. A 0.5 threshold treated as a decision rather than a default. Each has a one-sentence correction, and this part gives you all of them with the tooling that makes them cheap. Two ideas are worth more than the rest combined: <strong>0.5 is a default, not a decision</strong>, and the <strong>imbalance order of operations</strong> — threshold first, class weights second, resampling last and only if needed.",
 chips("Level 11", 9, 14, 3, "9h"), ("Part 11 · Model Selection &amp; Validation","CV, nested CV, comparisons"), "CML_Part11_Validation.html",
 ("Part 13 · Feature Engineering",["Ratios, aggregates, datetime","Selection and feature stores"]))

part(13, "CML_Part13_FeatureEngineering.html", "Feature Engineering &amp; Selection", "L12",
 [G("L12","Feature Engineering",[("c13-1","13.1 · Why it still matters ⭐"),("c13-2","13.2 · Numeric features ⭐"),
   ("c13-3","13.3 · Datetime features ⭐"),("c13-4","13.4 · Text &amp; geospatial on a tabular row"),
   ("c13-5","13.5 · Feature selection ⭐"),("c13-6","13.6 · Pipelines in production ⭐"),
   ("c13-7","13.7 · Feature stores &amp; point-in-time ⭐⭐")])],
 "Exposing the structure a model can use",
 "Why feature work still beats model choice on tabular data, the numeric transformations that actually earn their place, datetime done properly with cyclical encoding, text and geospatial features on a tabular row, filter/wrapper/embedded selection and the reason you select at all, production pipelines — and point-in-time correctness.",
 "A model can only use structure you expose, which is why on tabular data <strong>feature engineering routinely beats model choice</strong>. But the two ideas that make this part senior-level are less obvious than that. The first is that you usually select features <strong>not for accuracy</strong> but for latency, acquisition cost, drift surface, interpretability and maintenance — and being able to say &ldquo;I dropped features that <em>improved</em> accuracy because they cost more than they were worth&rdquo; is a genuinely strong answer. The second is <strong>point-in-time correctness</strong>: reconstructing what a feature's value <em>was</em> at prediction time rather than what it is now, which is simultaneously a feature-store design problem and the deepest form of the leakage question from Part 3.",
 chips("Level 12", 7, 11, 1, "6h"), ("Part 12 · Metrics","ROC vs PR, calibration, imbalance"), "CML_Part12_Metrics.html",
 ("Part 14 · Interpretability &amp; Fairness",["Three importances, PDP/ICE/ALE","SHAP's failure modes, fairness"]))

part(14, "CML_Part14_Interpretability.html", "Interpretability &amp; Fairness", "L13",
 [G("L13","Interpretability &amp; Fairness",[("c14-1","14.1 · The taxonomy"),("c14-2","14.2 · Intrinsically interpretable models ⭐"),
   ("c14-3","14.3 · The three importances ⭐⭐"),("c14-4","14.4 · PDP, ICE &amp; ALE ⭐"),
   ("c14-5","14.5 · LIME"),("c14-6","14.6 · SHAP ⭐⭐"),
   ("c14-7","14.7 · Counterfactuals &amp; adverse action ⭐"),("c14-8","14.8 · Fairness ⭐⭐")])],
 "Explaining it, and defending the explanation",
 "The three axes of the interpretability taxonomy, glass-box models including GAMs and EBMs, the three feature importances and the three different questions they answer, PDP versus ICE versus ALE, LIME's instability, SHAP with its failure modes named, counterfactuals and adverse-action notices, and the fairness impossibility result.",
 "The most valuable thing you can say about SHAP is what it gets <strong>wrong</strong>. KernelSHAP assumes feature independence and evaluates the model on unrealistic rows off the data manifold; path-dependent TreeSHAP avoids that by changing the value function, with the consequence that <strong>a feature which does not affect the prediction can still receive non-zero attribution</strong>; and with correlated features credit is split in ways that do not map onto causal importance. Similarly, the strongest possible answer to a fairness question is not a metric but the <strong>impossibility result</strong> — several criteria are provably incompatible when base rates differ, so &ldquo;make it fair&rdquo; is under-specified and someone must choose <em>which</em> fairness. That is a policy decision, and asking who owns it is the senior move.",
 chips("Level 13", 8, 12, 2, "7h"), ("Part 13 · Feature Engineering","Selection, pipelines, feature stores"), "CML_Part13_FeatureEngineering.html",
 ("Part 15 · Production ML Engineering",["Serving, skew, drift","Retraining and A/B testing"]))

part(15, "CML_Part15_Production.html", "Production ML Engineering", "L14",
 [G("L14","Production ML",[("c15-1","15.1 · The architecture ⭐"),("c15-2","15.2 · Batch vs real-time ⭐"),
   ("c15-3","15.3 · Serving &amp; latency ⭐"),("c15-4","15.4 · Training/serving skew ⭐⭐"),
   ("c15-5","15.5 · Monitoring &amp; drift ⭐⭐"),("c15-6","15.6 · Retraining triggers ⭐"),
   ("c15-7","15.7 · Deployment &amp; the feedback loop ⭐"),("c15-8","15.8 · A/B testing a model ⭐"),
   ("c15-9","15.9 · Engineering hygiene")])],
 "Shipping something people depend on",
 "Training and inference paths that share one feature definition, the batch-versus-real-time decision, latency budgets decomposed to p99, training/serving skew, the full drift taxonomy with detection proxies for late labels, retraining triggers, shadow/canary/A-B deployment, the feedback-loop problem, and the engineering hygiene that makes any of it auditable.",
 "Senior interviews spend most of their time here, and the highest-value idea in the whole part is a negative one: <strong>not every drift alert warrants a retrain.</strong> Confirm the distribution change actually degraded a metric first — alert fatigue kills monitoring programmes faster than missed drift does. Two more ideas recur constantly. <strong>Training/serving skew</strong>: the same feature computed two slightly different ways in two codebases, with nothing to alert you, which is why the fix is architectural rather than procedural. And the <strong>feedback loop</strong>: a fraud model never observes the transactions it blocked, a credit model never sees how rejected applicants would have performed, so the training data becomes systematically censored in a way offline evaluation cannot see.",
 chips("Level 14", 9, 13, 1, "8h"), ("Part 14 · Interpretability &amp; Fairness","SHAP, ALE, fairness"), "CML_Part14_Interpretability.html",
 ("Part 16 · Frontier &amp; Senior Signal",["TabPFN, conformal prediction","Causal inference and uplift"]))

part(16, "CML_Part16_Frontier.html", "Frontier &amp; Senior Signal", "L15",
 [G("L15","Frontier &amp; Senior Signal",[("c16-1","16.1 · Tabular foundation models ⭐⭐"),
   ("c16-2","16.2 · Aleatoric vs epistemic"),("c16-3","16.3 · Conformal prediction ⭐⭐"),
   ("c16-4","16.4 · Causal inference ⭐⭐"),("c16-5","16.5 · Uplift modelling ⭐⭐"),
   ("c16-6","16.6 · Double machine learning ⭐"),("c16-7","16.7 · Data-centric ML ⭐"),
   ("c16-8","16.8 · Shift, robustness &amp; the big question ⭐")])],
 "The positions that make you sound current",
 "Tabular foundation models and the answer that changed, the two kinds of uncertainty, conformal prediction with its guarantee and its one assumption, causal inference from potential outcomes to DML, uplift modelling and why AUC is the wrong metric for it, data-centric ML, distribution shift and strategic behaviour — and whether classical ML is dead.",
 "This part exists to give you <em>positions</em> rather than facts, on the four questions that most reliably separate a 2026 candidate from a 2019 one. Whether <strong>GBDTs still beat deep learning on tabular data</strong> — genuinely contested now, and the careful answer names both the TabPFN-3 results and the caveats. How you attach a <strong>guarantee</strong> to a prediction — conformal, distribution-free, with exchangeability as the assumption that breaks under drift. Why a churn model is the <em>wrong</em> model for deciding who gets a discount — <strong>uplift/CATE</strong>, because a predictive model is invalid under intervention. And the sentence that reframes the whole job: <strong>most of the remaining accuracy is in the data, not the model.</strong>",
 chips("Level 15", 8, 12, 2, "7h"), ("Part 15 · Production ML Engineering","Drift, retraining, A/B"), "CML_Part15_Production.html",
 ("Part 17 · Interview Q&amp;A Bank",["105 questions + 15 traps","Derivations, coding, cases"]))

part(17, "CML_Part17_QABank.html", "Interview Q&amp;A Bank", "QA",
 [G("QA","The Question Bank",[("c17-0","17.0 · How to use this bank"),("c17-1","17.1 · Foundations &amp; framing"),
   ("c17-2","17.2 · Bias, variance &amp; generalization"),("c17-3","17.3 · Regularization"),
   ("c17-4","17.4 · Linear models"),("c17-5","17.5 · Trees &amp; ensembles"),("c17-6","17.6 · Other models"),
   ("c17-7","17.7 · Unsupervised"),("c17-8","17.8 · Validation"),("c17-9","17.9 · Metrics"),
   ("c17-10","17.10 · Imbalance &amp; leakage"),("c17-11","17.11 · Feature engineering"),
   ("c17-12","17.12 · Missing data &amp; preprocessing"),("c17-13","17.13 · Interpretability"),
   ("c17-14","17.14 · Production"),("c17-15","17.15 · Frontier &amp; senior signal")]),
  G("REF","Traps &amp; Reference",[("c17-16","17.16 · The 15 traps ⭐⭐"),("c17-17","17.17 · Your PDF map ⭐"),
   ("c17-18","17.18 · Math &amp; derivations"),("c17-19","17.19 · Coding questions"),
   ("c17-20","17.20 · Case &amp; system design"),("c17-21","17.21 · Behavioural questions"),
   ("c17-22","17.22 · Formula sheet &amp; legacy→modern map")])],
 "The question bank",
 "105 high-frequency questions with model answers, the 15 trap questions, your own PDF set mapped honestly, 15 derivations, 16 coding exercises, 10 case designs, 12 behavioural questions, and the reference sheets.",
 "Every part of this subject ends its topics with the questions that topic answers — this is the <strong>consolidated drill</strong>, shuffled and stripped of context so you cannot coast on adjacency. Read the question, answer it out loud, <em>then</em> expand and compare. Two sections deserve the most attention. <strong>§17.16, the traps</strong>, because classical ML interviews are lost on a small number of confidently-wrong answers — &ldquo;95% accurate&rdquo; on an imbalanced problem, SMOTE reached for first, <code class=\"ic\">feature_importances_</code> quoted without qualification, a 0.99 AUC celebrated rather than investigated. And <strong>§17.17</strong>, which maps your own PDF set and states plainly that it contains almost no classical ML at all.",
 chips("Q&amp;A Bank", 23, 0, 2, "6h drill"), ("Part 16 · Frontier &amp; Senior Signal","TabPFN, conformal, causal"), "CML_Part16_Frontier.html",
 ("Learning Hub",["All subjects"]))

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
    html = html.replace("</style>", WIDGET_CSS + "</style>", 1)
    (HERE/c["file"]).write_text(html)
    assert "<!--CONTENT_INSERT-->" in html and "ragPrepStatus" not in html
    print(f"  {c['file']} ({len(html):,}b)")

if __name__ == "__main__":
    for p in ([int(a) for a in sys.argv[1:]] or P): build(p)
