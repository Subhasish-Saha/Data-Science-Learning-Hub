#!/usr/bin/env python3
"""Build the NLP subject shells: reuse the shared design system from the RAG
Part 1 file, swap in an NLP tracker (its own localStorage key: nlpPrepStatus_v1)
and per-part chrome. Each shell carries a <!--CONTENT_INSERT--> marker that the
content fragments are spliced into by insert.py."""
import re, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent
SRC  = SITE / "rag" / "RAG_Interview_Prep_Part1_Foundations.html"
MD   = SITE.parent / "nlp-study-guide.md"
NP   = 7            # number of parts

LEVEL_KEY = {
 "Level 0 — What NLP Actually Is": ("l0","Level 0 · What NLP Is"),
 "Level 1 — The Linguistic Preprocessing Pipeline": ("l1","Level 1 · Linguistic Pipeline"),
 "Level 2 — Classical Text Representation": ("l2","Level 2 · Classical Representation"),
 "Level 3 — Classical Models for Text": ("l3","Level 3 · Classical Models"),
 "Level 4 — Statistical Language Modelling": ("l4","Level 4 · Statistical LMs"),
 "Level 5 — Word Embeddings": ("l5","Level 5 · Word Embeddings"),
 "Level 6 — Sequence Models: RNN → LSTM → Seq2Seq → Attention": ("l6","Level 6 · Sequence Models"),
 "Level 7 — Subword Tokenization (deep dive)": ("l7","Level 7 · Subword Tokenization"),
 "Level 8 — The Transformer, Component by Component": ("l8","Level 8 · The Transformer"),
 "Level 9 — Pretraining Paradigms & Model Families": ("l9","Level 9 · Pretraining &amp; Families"),
 "Level 10 — Efficiency & Modern Architecture": ("l10","Level 10 · Efficiency &amp; Architecture"),
 "Level 11 — Fine-Tuning & Adaptation": ("l11","Level 11 · Fine-Tuning"),
 "Level 12 — The Task Catalogue": ("l12","Level 12 · The Task Catalogue"),
 "Level 13 — Evaluation (the part most candidates fail)": ("l13","Level 13 · Evaluation"),
 "Level 14 — Production NLP Engineering": ("l14","Level 14 · Production"),
 "Level 15 — Frontier & Senior Signal": ("l15","Level 15 · Frontier"),
}
CAT = {"l0":"Theory","l1":"Practical","l2":"Theory","l3":"Theory","l4":"Theory","l5":"Theory",
       "l6":"Theory","l7":"Practical","l8":"Theory","l9":"Theory","l10":"Theory","l11":"Practical",
       "l12":"Practical","l13":"Practical","l14":"Practical","l15":"Theory"}
HIGH = {"l2","l4","l5","l6","l7","l8","l9","l10","l11","l13"}

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
 "High-frequency: foundations &amp; preprocessing (8 questions)",
 "High-frequency: representation — BoW, TF-IDF, LSA/LDA (9 questions)",
 "High-frequency: embeddings — Word2Vec, FastText, SBERT (12 questions)",
 "High-frequency: sequence models — RNN, LSTM, seq2seq, attention (9 questions)",
 "High-frequency: tokenization — BPE/WordPiece/Unigram, token premium (9 questions)",
 "High-frequency: transformers — attention, RoPE, KV cache (13 questions)",
 "High-frequency: pretraining &amp; model families — BERT/GPT/T5/ModernBERT (11 questions)",
 "High-frequency: efficiency — MQA/GQA/MLA, FlashAttention, Mamba, MoE (9 questions)",
 "High-frequency: fine-tuning — LoRA/QLoRA, SFT/DPO/GRPO, fine-tune vs RAG (9 questions)",
 "High-frequency: tasks — classification, NER, summarization, search (8 questions)",
 "High-frequency: evaluation — micro/macro, perplexity, BLEU/ROUGE/COMET, judges (11 questions)",
 "High-frequency: production — pipelines, drift, cost, PII, reproducibility (7 questions)",
 "The 15 trap questions (answered correctly, out loud)",
 "Your own PDF question set, mapped section by section (73 items)",
]]
MQ = [("mq","Theory","High",t) for t in [
 "Derivation: softmax gradient and why √d_k exists",
 "Derivation: cross-entropy ↔ perplexity ↔ bits-per-byte",
 "Derivation: why ∏Wₕ vanishes/explodes; the LSTM additive path",
 "Derivation: multi-head attention shapes + parameters per block",
 "Calculation: KV-cache size for MHA vs GQA vs MQA",
 "Derivation: SGNS objective and the shifted-PMI equivalence",
 "Derivation: Viterbi recursion and its complexity",
 "Derivation: modified Kneser-Ney interpolation and continuation counts",
 "Derivation: BLEU's brevity penalty vs ROUGE's recall bias",
 "Calculation: training FLOPs (6ND) and AdamW memory in mixed precision",
]]
CQ = [("cq","Practical","High",t) for t in [
 "Code: BPE training loop + BPE encoding from a merge list",
 "Code: TF-IDF from scratch, reconciled with TfidfVectorizer",
 "Code: scaled dot-product attention → multi-head → causal mask",
 "Code: sinusoidal positional encoding, then RoPE applied to Q/K",
 "Code: Viterbi decoding in log-space with backpointers",
 "Code: beam search with length normalisation, then top-p sampling",
 "Code: n-gram LM with add-k and interpolation + perplexity",
 "Code: entity-level F1 (seqeval-style) from BIO sequences",
 "Code: sub-token label alignment with word_ids() and -100 masking",
 "Code: brute-force top-k cosine search, then the ANN upgrade path",
 "Code: MinHash/LSH near-duplicate detection",
 "Code: sentence-safe sliding-window chunker",
 "Code: batched inference with length bucketing, measure p95",
 "Code: a LoRA-wrapped nn.Linear, including the merge",
]]
SD = [("sd","Interview Prep","High",t) for t in [
 "System design: support-ticket triage, 200 intents, 5k QPS, p95 &lt; 100 ms",
 "System design: resume ↔ JD matching with a fairness audit",
 "System design: clinical de-identification, recall ≥ 0.99, on-prem",
 "System design: multilingual content moderation across 30 languages",
 "System design: financial-news entity &amp; event extraction, near-real-time",
 "System design: 100-page document summarization with contractual faithfulness",
 "System design: semantic search over 50M noisy product titles",
 "System design: text-to-SQL for analysts, with guardrails",
 "System design: cut the NLP inference bill 10× without losing accuracy",
 "System design: should you pretrain a domain LM? (show the arithmetic)",
]]
PP = [("pp","Project","High",t) for t in [
 "Project 1: classical baseline showdown (5 representations, one honest table)",
 "Project 2: build your own tokenizer (BPE/WordPiece/Unigram + token premium)",
 "Project 3: transformer from scratch, then add RoPE + GQA + KV cache",
 "Project 4: NER with zero labels → distilled encoder, entity-level F1",
 "Project 5: summarization faithfulness harness (4 metrics that disagree)",
 "Project 6: 10× cheaper — distil, quantize, batch, with a measured table",
 "Project 7: drift monitor with no fresh labels",
]]
rows += [[k,c,p,t] for k,c,p,t in IV+MQ+CQ+SD+PP]

PHASES = {k:v for k,v in LEVEL_KEY.values()}
PHASES.update({"iv":"Interview Q&amp;A Bank","mq":"Math &amp; Derivations","cq":"Coding Questions",
               "sd":"System Design Scenarios","pp":"Portfolio Projects"})
ORDER = [f"l{i}" for i in range(16)] + ["iv","mq","cq","sd","pp"]
tracker_js = "[\n" + ",\n".join(f'[{i+1},"{r[0]}","{r[1]}","{r[2]}",0,{json.dumps(r[3])}]' for i,r in enumerate(rows)) + "\n]"
TOTAL = len(rows)
print(f"tracker: {TOTAL} items / {len(ORDER)} groups")

P = {
 1: dict(file="NLP_Part1_Foundations.html", title="Foundations &amp; Classical NLP", pk="L0-2",
   groups=[("L0","What NLP Is",[("c1-1","1.1 · Why language is hard"),("c1-2","1.2 · The task taxonomy ⭐"),
     ("c1-3","1.3 · The five eras"),("c1-4","1.4 · Data before models")]),
    ("L1","The Linguistic Pipeline",[("c1-5","1.5 · Normalization"),("c1-6","1.6 · Classical tokenization"),
     ("c1-7","1.7 · Stemming vs lemmatization"),("c1-8","1.8 · Stopwords"),("c1-9","1.9 · POS tagging"),
     ("c1-10","1.10 · Syntactic parsing"),("c1-11","1.11 · NER &amp; BIO tagging"),("c1-12","1.12 · The other layers &amp; spaCy")]),
    ("L2","Classical Representation",[("c1-13","1.13 · One-hot, BoW &amp; n-grams"),("c1-14","1.14 · TF-IDF ⭐"),
     ("c1-15","1.15 · Similarity &amp; distance"),("c1-16","1.16 · LSA, NMF &amp; LDA"),
     ("c1-17","1.17 · The distributional hypothesis"),("c1-18","1.18 · Interview focus")])],
   h1="The layer everything else is built on",
   sub="Why language is hard, the task taxonomy that decides your architecture, the linguistic pipeline, and the classical representations — BoW, TF-IDF, LSA and LDA — that modern NLP is a reaction to.",
   thesis="Do not skip this part because &ldquo;everything is an LLM now.&rdquo; Interviewers use it as a <strong>filter</strong>: it is where they find out whether you understand <em>why</em> the modern stack looks the way it does. Almost every trap question in this subject is a classical question wearing modern clothes — and the honest 2026 answer to &ldquo;is classical NLP dead?&rdquo; is that it <strong>moved down the stack</strong>. You still tokenize, still normalise, still run regex and gazetteer precision passes, still report entity-level F1. This part covers the <strong>task taxonomy</strong> (name the task type and the architecture family follows), the full <strong>linguistic pipeline</strong>, and the classical representation ladder up to the <strong>distributional hypothesis</strong> — the single sentence that every embedding method implements.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 0–2</b></span>\n          <span class="chip"><b>90</b> topics</span>\n          <span class="chip">📐 <b>11</b> diagrams</span>\n          <span class="chip">⏱ <b>~8h</b></span>',
   prev=("Learning Hub","All subjects"), prevhref="../index.html",
   nxt=("Part 2 · Models, LMs &amp; Embeddings",["Naive Bayes → HMM → CRF","n-grams, perplexity, Word2Vec"])),
 2: dict(file="NLP_Part2_ModelsAndEmbeddings.html", title="Models, LMs &amp; Embeddings", pk="L3-5",
   groups=[("L3","Classical Models",[("c2-1","2.1 · Naive Bayes"),("c2-2","2.2 · Logistic regression &amp; SVM"),
     ("c2-3","2.3 · HMM &amp; Viterbi ⭐"),("c2-4","2.4 · CRF and label bias ⭐"),
     ("c2-5","2.5 · Feature engineering"),("c2-6","2.6 · Classification metrics")]),
    ("L4","Statistical LMs",[("c2-7","2.7 · What a language model is"),("c2-8","2.8 · N-gram LMs"),
     ("c2-9","2.9 · Smoothing &amp; Kneser-Ney"),("c2-10","2.10 · Perplexity &amp; its traps ⭐"),
     ("c2-11","2.11 · Decoding strategies")]),
    ("L5","Word Embeddings",[("c2-12","2.12 · The idea"),("c2-13","2.13 · Word2Vec ⭐"),
     ("c2-14","2.14 · GloVe &amp; FastText"),("c2-15","2.15 · Using &amp; evaluating embeddings"),
     ("c2-16","2.16 · Bias in embeddings"),("c2-17","2.17 · Static vs contextual ⭐"),("c2-18","2.18 · Interview focus")])],
   h1="Counting, predicting, and the first real vectors",
   sub="Naive Bayes to CRFs, n-gram language models with smoothing and perplexity, decoding strategies, and the embedding revolution — Word2Vec, GloVe, FastText — up to the static/contextual pivot.",
   thesis="Three things live here that interviewers return to constantly. <strong>Sequence models before neural nets</strong> — HMM, Viterbi and CRF — because &ldquo;HMM vs CRF&rdquo; is a clean test of generative vs discriminative thinking, and because a <strong>CRF head on top of BERT still helps</strong>. <strong>Perplexity</strong>, which almost everyone can define and almost nobody can criticise (it is not comparable across tokenizers). And <strong>Word2Vec</strong>, where the real question is never &ldquo;what is an embedding&rdquo; but <em>CBOW vs skip-gram</em>, <em>negative sampling</em>, and why &ldquo;good&rdquo; and &ldquo;bad&rdquo; end up close together. We finish on the pivot that sets up the rest of the subject: one vector per <em>word</em> versus one vector per <em>word in context</em>.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 3–5</b></span>\n          <span class="chip"><b>75</b> topics</span>\n          <span class="chip">📐 <b>11</b> diagrams</span>\n          <span class="chip">⏱ <b>~8h</b></span>',
   prev=("Part 1 · Foundations","Pipeline, BoW, TF-IDF, LDA"), prevhref="NLP_Part1_Foundations.html",
   nxt=("Part 3 · Sequences &amp; Tokenization",["RNN → LSTM → attention","BPE, WordPiece, Unigram"])),
 3: dict(file="NLP_Part3_SequencesAndTokenization.html", title="Sequences &amp; Tokenization", pk="L6-7",
   groups=[("L6","Sequence Models",[("c3-1","3.1 · RNN mechanics"),("c3-2","3.2 · Vanishing &amp; exploding gradients ⭐"),
     ("c3-3","3.3 · LSTM ⭐"),("c3-4","3.4 · GRU"),("c3-5","3.5 · Bidirectional &amp; deep RNNs"),
     ("c3-6","3.6 · Seq2Seq &amp; the bottleneck"),("c3-7","3.7 · Attention before transformers ⭐"),
     ("c3-8","3.8 · Would you ship an RNN in 2026?")]),
    ("L7","Subword Tokenization",[("c3-9","3.9 · Why subwords"),("c3-10","3.10 · BPE ⭐"),
     ("c3-11","3.11 · WordPiece"),("c3-12","3.12 · Unigram &amp; SentencePiece ⭐"),
     ("c3-13","3.13 · Vocabulary size"),("c3-14","3.14 · Where tokenization breaks ⭐"),
     ("c3-15","3.15 · Practicalities &amp; label alignment"),("c3-16","3.16 · Interview focus")])],
   h1="Memory, then the units the model actually sees",
   sub="RNN mechanics through LSTM gates, GRUs, the seq2seq bottleneck and the attention mechanism that broke it — then a full level on subword tokenization, the topic with the worst answer-to-importance ratio in NLP interviews.",
   thesis="The first half is the lineage: an RNN's hidden state, <em>exactly</em> why gradients vanish, and <em>exactly</em> how the LSTM cell state fixes it (the additive gated path — the &ldquo;constant error carousel&rdquo;). Then the seq2seq bottleneck and Bahdanau/Luong attention, which is the direct ancestor of everything in Part 4. The second half is <strong>tokenization</strong>, and it is disproportionately valuable: it is asked constantly, it explains a dozen otherwise-baffling model behaviours — the strawberry problem, arithmetic errors, your Hindi app costing 3× as much — and most candidates can only say &ldquo;BPE splits words into pieces.&rdquo; You will be able to write the merge loop.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 6–7</b></span>\n          <span class="chip"><b>59</b> topics</span>\n          <span class="chip">📐 <b>11</b> diagrams</span>\n          <span class="chip">⏱ <b>~7h</b></span>',
   prev=("Part 2 · Models, LMs &amp; Embeddings","HMM/CRF, perplexity, Word2Vec"), prevhref="NLP_Part2_ModelsAndEmbeddings.html",
   nxt=("Part 4 · Transformers",["Attention, RoPE, KV cache","BERT vs GPT vs T5"])),
 4: dict(file="NLP_Part4_Transformers.html", title="Transformers &amp; Pretraining", pk="L8-9",
   groups=[("L8","The Transformer",[("c4-1","4.1 · Why kill recurrence"),("c4-2","4.2 · Scaled dot-product attention ⭐"),
     ("c4-3","4.3 · Multi-head attention ⭐"),("c4-4","4.4 · Positional information ⭐⭐"),
     ("c4-5","4.5 · FFN, residuals &amp; normalization"),("c4-6","4.6 · Encoder, decoder &amp; causal masking"),
     ("c4-7","4.7 · Complexity, KV cache &amp; context ⭐")]),
    ("L9","Pretraining &amp; Families",[("c4-8","4.8 · Self-supervised objectives ⭐"),
     ("c4-9","4.9 · Choosing an architecture family ⭐"),("c4-10","4.10 · The model zoo"),
     ("c4-11","4.11 · Scaling &amp; training economics"),("c4-12","4.12 · Sentence embeddings ⭐"),
     ("c4-13","4.13 · Interview focus")])],
   h1="Attention, and everything built on it",
   sub="The transformer block component by component — including why √d_k exists and the full positional-encoding lineage up to RoPE and YaRN — then pretraining objectives, the model zoo, scaling laws and sentence embeddings.",
   thesis="This is the densest part of the subject and the highest-yield. Two ideas carry it. First, <strong>attention as content-based routing</strong>: `softmax(QKᵀ/√d_k)V`, why the scale factor is not cosmetic, why multiple heads mean subspaces rather than capacity, and the <strong>KV cache</strong> — the single most useful concept for answering any serving question, because it explains why decoding is memory-bandwidth-bound rather than compute-bound. Second, <strong>the objective determines the family</strong>: masked LM gives you a strong per-token representation, causal LM gives you a samplable generator, denoising gives you transduction. Getting that mapping right is how you answer the question this subject exists for — <em>should this be a fine-tuned encoder or a prompted LLM?</em>",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 8–9</b></span>\n          <span class="chip"><b>71</b> topics</span>\n          <span class="chip">📐 <b>13</b> diagrams</span>\n          <span class="chip">⏱ <b>~10h</b></span>',
   prev=("Part 3 · Sequences &amp; Tokenization","LSTM, attention, BPE"), prevhref="NLP_Part3_SequencesAndTokenization.html",
   nxt=("Part 5 · Efficiency &amp; Fine-Tuning",["GQA/MLA, FlashAttention, Mamba","LoRA, QLoRA, DPO, GRPO"])),
 5: dict(file="NLP_Part5_EfficiencyAndFinetuning.html", title="Efficiency &amp; Fine-Tuning", pk="L10-11",
   groups=[("L10","Efficiency &amp; Architecture",[("c5-1","5.1 · KV cache &amp; attention variants ⭐⭐"),
     ("c5-2","5.2 · FlashAttention"),("c5-3","5.3 · Approximating attention"),
     ("c5-4","5.4 · SSMs, Mamba &amp; hybrids ⭐"),("c5-5","5.5 · Mixture of Experts"),
     ("c5-6","5.6 · Inference-time efficiency ⭐")]),
    ("L11","Fine-Tuning",[("c5-7","5.7 · The adaptation ladder ⭐"),("c5-8","5.8 · Fine-tuning mechanics"),
     ("c5-9","5.9 · LoRA, QLoRA &amp; the PEFT family ⭐"),("c5-10","5.10 · Post-training: SFT → DPO → GRPO ⭐"),
     ("c5-11","5.11 · Data strategy"),("c5-12","5.12 · Interview focus")])],
   h1="Making it cheap, and making it yours",
   sub="MHA → MQA → GQA → MLA, FlashAttention, sparse attention, Mamba hybrids and MoE — then the adaptation ladder, LoRA and QLoRA, and the modern post-training stack.",
   thesis="Every question in this part is really the same question: <strong>which axis are you short on?</strong> Latency, memory, throughput or accuracy each have a different tool, and candidates who reach for the wrong one give themselves away. The architecture half traces how the field made attention affordable — <strong>MQA and GQA share K/V heads, MLA compresses them</strong>, FlashAttention changes nothing mathematically and everything practically, and SSMs like Mamba make context <em>cheap</em> rather than merely accessible (which is why 2026 production models are <strong>hybrids</strong>, not replacements). The fine-tuning half is the adaptation ladder: stop at the first rung that hits your target metric, know exactly what <strong>LoRA</strong> freezes and what <strong>QLoRA</strong> quantizes, and be able to say why <em>fine-tuning does not inject facts</em>.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 10–11</b></span>\n          <span class="chip"><b>58</b> topics</span>\n          <span class="chip">📐 <b>13</b> diagrams</span>\n          <span class="chip">⏱ <b>~8h</b></span>',
   prev=("Part 4 · Transformers","Attention, RoPE, pretraining"), prevhref="NLP_Part4_Transformers.html",
   nxt=("Part 6 · Tasks, Evaluation &amp; Production",["NER in 2026, summarization","Metrics, judges, drift, PII"])),
 6: dict(file="NLP_Part6_TasksEvalProduction.html", title="Tasks, Evaluation &amp; Production", pk="L12-15",
   groups=[("L12","The Task Catalogue",[("c6-1","6.1 · Text classification"),("c6-2","6.2 · Extraction &amp; NER in 2026 ⭐"),
     ("c6-3","6.3 · Sentiment &amp; ABSA"),("c6-4","6.4 · Summarization ⭐"),("c6-5","6.5 · Machine translation"),
     ("c6-6","6.6 · Question answering"),("c6-7","6.7 · Similarity, search &amp; clustering"),
     ("c6-8","6.8 · Generation-adjacent &amp; multilingual")]),
    ("L13","Evaluation",[("c6-9","6.9 · Principles"),("c6-10","6.10 · Classification &amp; sequence metrics ⭐"),
     ("c6-11","6.11 · Generation metrics ⭐"),("c6-12","6.12 · LLM-as-judge ⭐"),
     ("c6-13","6.13 · Benchmarks &amp; robustness"),("c6-14","6.14 · Annotation &amp; agreement")]),
    ("L14–15","Production &amp; Frontier",[("c6-15","6.15 · Pipeline &amp; system design ⭐"),
     ("c6-16","6.16 · Serving &amp; performance"),("c6-17","6.17 · Monitoring &amp; drift"),
     ("c6-18","6.18 · Privacy, safety &amp; compliance"),("c6-19","6.19 · Reproducibility"),
     ("c6-20","6.20 · Multimodal NLP"),("c6-21","6.21 · Long context &amp; interpretability"),
     ("c6-22","6.22 · Interview focus")])],
   h1="Shipping language systems people depend on",
   sub="The task catalogue with its 2026 decision rules, the evaluation level most candidates fail, and the production engineering — serving, drift, PII, reproducibility — plus multimodal and interpretability.",
   thesis="This part is where NLP stops being modelling and becomes engineering. The <strong>task catalogue</strong> gives you a defensible answer for each family — including the one that comes up most, <em>NER for a brand-new entity type with zero labels</em> (GLiNER or an LLM teacher, then distil into an encoder). <strong>Evaluation</strong> gets the most space because it is where interviews are lost: token accuracy instead of entity-level F1, ROUGE quoted as if it could see a hallucination, perplexity compared across tokenizers, an LLM judge with no bias controls. Then <strong>production</strong>: the tiered-cascade pattern that is the highest-leverage cost move in applied NLP, drift detection when labels arrive 30 days late, and the reproducibility hygiene that makes any of it auditable.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Level 12–15</b></span>\n          <span class="chip"><b>112</b> topics</span>\n          <span class="chip">📐 <b>12</b> diagrams</span>\n          <span class="chip">⏱ <b>~11h</b></span>',
   prev=("Part 5 · Efficiency &amp; Fine-Tuning","GQA, LoRA, DPO/GRPO"), prevhref="NLP_Part5_EfficiencyAndFinetuning.html",
   nxt=("Part 7 · Interview Q&amp;A Bank",["115 questions + 15 traps","Your PDF map, 10 designs"])),
 7: dict(file="NLP_Part7_QABank.html", title="Interview Q&amp;A Bank", pk="QA",
   groups=[("QA","The Question Bank",[("c7-1","7.1 · Foundations &amp; preprocessing"),
     ("c7-2","7.2 · Representation &amp; embeddings"),("c7-3","7.3 · Sequence models"),
     ("c7-4","7.4 · Tokenization"),("c7-5","7.5 · Transformers"),("c7-6","7.6 · Pretraining &amp; families"),
     ("c7-7","7.7 · Efficiency &amp; architecture"),("c7-8","7.8 · Fine-tuning &amp; adaptation"),
     ("c7-9","7.9 · Tasks"),("c7-10","7.10 · Evaluation"),("c7-11","7.11 · Production")]),
    ("REF","Traps &amp; Reference",[("c7-12","7.12 · The 15 traps ⭐⭐"),("c7-13","7.13 · Your PDF question map ⭐"),
     ("c7-14","7.14 · Math &amp; derivations"),("c7-15","7.15 · Coding questions"),
     ("c7-16","7.16 · System design scenarios"),("c7-17","7.17 · Formula sheet &amp; legacy→modern map")])],
   h1="The question bank",
   sub="115 high-frequency questions with model answers, the 15 trap questions, your own PDF set mapped question by question, 10 derivations, 14 coding exercises, 10 system-design scenarios, and the reference sheets.",
   thesis="The consolidated <strong>drill</strong>. Read the question, answer out loud, <em>then</em> expand and compare — reading answers you already half-know is the least efficient possible use of this page. Two sections deserve the most attention. <strong>§7.12, the traps</strong>, because three things get people rejected in NLP interviews: quoting a legacy answer as if it were current (&ldquo;handle OOV with <code class=\"ic\">&lt;UNK&gt;</code>&rdquo;), reporting a metric that cannot support the claim (token accuracy for NER), and reaching for the biggest model when the constraint was latency. And <strong>§7.13</strong>, which maps every NLP question in your own PDF set to the section that answers it — including the three answers in those PDFs that are now out of date.",
   chips='<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>Q&amp;A Bank</b></span>\n          <span class="chip"><b>115</b> questions</span>\n          <span class="chip">15 <b>traps</b></span>\n          <span class="chip">⏱ <b>~6h</b> drill</span>',
   prev=("Part 6 · Tasks, Evaluation &amp; Production","Metrics, serving, drift"), prevhref="NLP_Part6_TasksEvalProduction.html",
   nxt=("Learning Hub",["All subjects"])),
}

def build(pn):
    c = P[pn]; html = SRC.read_text()
    s = html.index("</section>", html.index('id="tracker"')) + len("</section>")
    e = html.index("      <!-- PART NAV -->")
    html = html[:s] + "\n\n<!--CONTENT_INSERT-->\n\n      " + html[e:]
    html = html.replace("<title>RAG Interview Prep — Part 1: Foundations</title>",
                        f"<title>NLP Interview Prep — Part {pn}: {c['title']}</title>")
    html = html.replace('<div class="tt"><small>Part 1 / 6</small>Foundations</div>',
                        f'<div class="tt"><small>Part {pn} / {NP}</small>{c["title"]}</div>')
    html = html.replace('<div class="brand-txt">RAG Prep<small>Knowledge Base</small></div>',
                        '<div class="brand-txt">NLP Prep<small>Classical → Transformers</small></div>')
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
           '<li><a href="index.html">← NLP home</a></li></ul>\n      </div>\n    </nav>')
    html = re.sub(r'<nav class="toc" id="toc">.*?</nav>', lambda m: nav, html, count=1, flags=re.DOTALL)
    html = re.sub(r'<div class="sb-foot">.*?</div>',
        f'<div class="sb-foot">\n      Natural Language Processing<br>Part {pn} — {c["title"]}<br>© your study kit\n    </div>',
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
      f'<div class="doc-foot">\n        Natural Language Processing — Part {pn} of {NP} · {c["title"]}<br>\n'
      f'        Library-current as of <b>Aug 2026</b> — transformers <b>5.15</b> (PyTorch-only; no slow/fast tokenizer split) · '
      f'spaCy <b>3.8.15</b> · sentence-transformers <b>5.7</b>.<br>\n'
      f'        Progress is stored locally under key <code style="color:#8892a0">nlpPrepStatus_v1</code> and is shared by every part of this subject.\n      </div>',
      html, count=1, flags=re.DOTALL)
    _ph = "const PHASES = " + json.dumps(PHASES, ensure_ascii=False) + ";"
    _or = "const ORDER = " + json.dumps(ORDER) + ";"
    _tk = "const TRACKER = " + tracker_js + ";"
    html = re.sub(r'const PHASES = \{.*?\};', lambda m:_ph, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const ORDER = \[.*?\];', lambda m:_or, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const TRACKER = \[.*?\n\];', lambda m:_tk, html, count=1, flags=re.DOTALL)
    html = html.replace('const LS_KEY="ragPrepStatus_v1";','const LS_KEY="nlpPrepStatus_v1";').replace("206",str(TOTAL))
    html = re.sub(r'<p class="tk-sub">.*?</p>',
      f'<p class="tk-sub">One tracker for the whole NLP subject — all {TOTAL} topics across all {NP} parts. '
      f'Set a status on any row; your progress saves in this browser and prints as a clean checklist.</p>',
      html, count=1, flags=re.DOTALL)
    (HERE/c["file"]).write_text(html)
    assert "<!--CONTENT_INSERT-->" in html and "ragPrepStatus" not in html
    print(f"  {c['file']} ({len(html):,}b)")

if __name__ == "__main__":
    for p in ([int(a) for a in sys.argv[1:]] or P): build(p)
