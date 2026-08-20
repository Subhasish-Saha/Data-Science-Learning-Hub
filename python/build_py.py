#!/usr/bin/env python3
"""Build the "Python for Data Science Interviews" subject shells.

One part per blueprint level (10 levels + a Q&A bank + the classic
coding questions = 12 parts), so every topic
gets room for prose, diagrams, runnable code and its OWN interview Q&A box — the
pattern the RAG / Classical ML / LangGraph subjects use.

Reuses the shared design system from the RAG Part 1 file, swaps in a Python
tracker (own localStorage key: pyPrepStatus_v1), per-part chrome, the
interactive-widget CSS layer, and the CSS for the live in-browser Python runner
(Pyodide). Each shell carries a <!--CONTENT_INSERT--> marker that the content
fragments are spliced into by insert.py."""
import re, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent          # .../output/python
SITE = HERE.parent                                       # .../output
SRC  = SITE / "rag" / "RAG_Interview_Prep_Part1_Foundations.html"
MD   = SITE.parent / "python-data-science-study-guide.md"
NP   = 12            # number of parts

LEVEL_KEY = {
 "Level 0 — The Python Data Model":            ("l0", "Level 0 · The Data Model"),
 "Level 1 — Data Structures & Complexity":     ("l1", "Level 1 · Data Structures"),
 "Level 2 — Functions, Closures & Decorators": ("l2", "Level 2 · Functions &amp; Decorators"),
 "Level 3 — Iterators, Generators & Laziness": ("l3", "Level 3 · Generators"),
 "Level 4 — OOP, Dataclasses & Protocols":     ("l4", "Level 4 · OOP &amp; Dataclasses"),
 "Level 5 — NumPy":                            ("l5", "Level 5 · NumPy"),
 "Level 6 — pandas Core":                      ("l6", "Level 6 · pandas Core"),
 "Level 7 — pandas Transformation":            ("l7", "Level 7 · pandas Transformation"),
 "Level 8 — Performance, Memory & Concurrency":("l8", "Level 8 · Performance &amp; Memory"),
 "Level 9 — Production Python for Data Science":("l9","Level 9 · Production"),
 "Level 10 — Classic Coding Questions":         ("l10","Level 10 · Classic Coding"),
}
CAT = {"l0":"Theory","l1":"Theory","l2":"Practical","l3":"Practical","l4":"Practical",
       "l5":"Practical","l6":"Practical","l7":"Practical","l8":"Practical","l9":"Practical",
       "l10":"Coding"}
HIGH = {"l0","l5","l6","l7","l8","l10"}      # the levels interviews weight most heavily

def clean(s):
    s = re.sub(r'`([^`]*)`', r'\1', s)
    s = re.sub(r'\*\*([^*]*)\*\*', r'\1', s)
    s = re.sub(r'\*([^*]*)\*', r'\1', s)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r'\s+', ' ', s).strip(" .")

rows, cur = [], None
for line in MD.read_text().split("\n"):
    m = re.match(r'^## (.+)$', line)
    if m:
        cur = LEVEL_KEY.get(m.group(1).strip())
        if m.group(1).strip() == "Interview Preparation":   cur = ("iv", None)
        if m.group(1).strip() == "Coding Exercises":        cur = ("ex", None)
    if cur and re.match(r'^\s*- \[ \]', line):
        t = clean(re.sub(r'^\s*- \[ \]\s*', '', line))
        if t:
            k = cur[0]
            cat = "Interview Prep" if k == "iv" else ("Exercise" if k == "ex" else CAT[k])
            pri = "High" if k in HIGH or k in ("iv", "ex") else "Medium"
            rows.append([k, cat, pri, t])

PHASES = {k: v for k, v in LEVEL_KEY.values()}
PHASES.update({"iv": "Interview Q&amp;A Drill", "ex": "Coding Exercises"})
ORDER = ["l0","l1","l2","l3","l4","l5","l6","l7","l8","l9","iv","ex","l10"]

tracker_js = "[\n" + ",\n".join(
    f'[{i+1},"{r[0]}","{r[1]}","{r[2]}",0,{json.dumps(r[3])}]' for i, r in enumerate(rows)) + "\n]"
TOTAL = len(rows)
print(f"tracker: {TOTAL} items across {len(ORDER)} groups")

# --------------------------------------------------------------- CSS additions
WIDGET_CSS = """
/* ---- interactive widgets (Python) ---- */
.wdg{margin:1.8rem 0;border:1px solid var(--line);border-radius:14px;background:var(--surface);box-shadow:var(--shadow);overflow:hidden}
.wdg .wh{background:linear-gradient(135deg,#161b23,#252d3a);color:#fff;padding:12px 18px;font-family:var(--disp);font-weight:600;font-size:.98rem;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.wdg .wh .wtag{font-family:var(--mono);font-size:9.5px;letter-spacing:1.6px;text-transform:uppercase;color:#14181f;background:var(--gold-2);padding:3px 8px;border-radius:20px;font-weight:600}
.wdg .wbody{padding:16px 18px 18px}
.wdg canvas{width:100%;height:auto;display:block;border-radius:10px;background:#14181f}
.wdg .wctl{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start;margin-top:14px}
.wdg .wctl label{font-family:var(--mono);font-size:11.5px;color:var(--muted);display:flex;flex-direction:column;gap:6px;min-width:170px;flex:1}
.wdg .wctl input[type=range]{width:100%;accent-color:var(--indigo);margin:0}
.wdg .wbtns{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.wdg .wbtn{font-family:var(--mono);font-size:11.5px;padding:6px 12px;border-radius:8px;border:1px solid var(--line);background:var(--paper);color:var(--text);cursor:pointer;transition:.13s}
.wdg .wbtn:hover{border-color:var(--indigo-line);background:var(--indigo-soft)}
.wdg .wbtn.on{background:var(--indigo);color:#fff;border-color:var(--indigo)}
.wdg .wbtn:disabled{opacity:.45;cursor:not-allowed}
.wdg .wout{margin-top:13px;font-family:var(--mono);font-size:12.5px;color:var(--text);background:var(--indigo-soft);border:1px solid var(--indigo-line);border-radius:10px;padding:11px 14px;line-height:1.75}
.wdg .wout .k{color:var(--muted)}
.wdg .wout .v{font-weight:600;color:var(--indigo)}
.wdg .wout .warn{color:#a5710a;font-weight:600}
.wdg .wout .good{color:#1c7a42;font-weight:600}
.wdg .wnote{margin:12px 0 0;font-size:.88rem;color:var(--muted);line-height:1.65}
.wdg .wgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:13px}
.wdg .wcell{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:9px 12px;font-family:var(--mono);font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px}
.wdg .wcell .n{display:block;font-size:1.3rem;font-weight:600;color:var(--ink);font-family:var(--disp);letter-spacing:-.4px;text-transform:none}
@media print{.wdg .wctl,.wdg .wbtns{display:none}.wdg{break-inside:avoid}}

/* ---- live Python runner (Pyodide) ---- */
.pyrun{margin:1.7rem 0;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--surface);box-shadow:var(--shadow)}
.pyrun .ph{background:#14181f;color:#e6e9ef;padding:9px 15px;font-family:var(--mono);font-size:11.5px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;border-bottom:1px solid #2c3542}
.pyrun .ph .dot3{display:inline-flex;gap:5px;margin-right:4px}
.pyrun .ph .dot3 i{width:9px;height:9px;border-radius:50%;display:block}
.pyrun .ph .ptag{font-size:9px;letter-spacing:1.5px;text-transform:uppercase;background:#2E9E5B;color:#0b1a10;padding:2px 7px;border-radius:20px;font-weight:700}
.pyrun .ph .pname{color:#8892a0}
.pyrun .ph .pspacer{flex:1}
.pyrun .ph .pstat{font-size:10.5px;color:#8892a0}
.pyrun .ph .pstat.busy{color:var(--gold-2)}
.pyrun .ph .pstat.ready{color:#7fd6a0}
.pyrun .ph .pstat.err{color:#e0929a}
.pyrun textarea{width:100%;box-sizing:border-box;border:0;outline:0;resize:vertical;display:block;
  background:#0f1319;color:#e6e9ef;font-family:var(--mono);font-size:12.6px;line-height:1.72;
  padding:14px 16px;tab-size:4;min-height:96px;caret-color:var(--gold-2)}
.pyrun textarea::selection{background:#31405c}
.pyrun .pbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:10px 14px;background:var(--paper);border-top:1px solid var(--line)}
.pyrun .pbtn{font-family:var(--mono);font-size:11.5px;padding:6px 13px;border-radius:8px;border:1px solid var(--line);background:var(--surface);color:var(--text);cursor:pointer;transition:.13s}
.pyrun .pbtn:hover{border-color:var(--indigo-line);background:var(--indigo-soft)}
.pyrun .pbtn.run{background:var(--indigo);color:#fff;border-color:var(--indigo);font-weight:600}
.pyrun .pbtn.run:hover{filter:brightness(1.08)}
.pyrun .pbtn:disabled{opacity:.45;cursor:not-allowed}
.pyrun .phint{font-family:var(--mono);font-size:10.5px;color:var(--muted);margin-left:auto}
.pyrun .pout{display:none;border-top:1px solid var(--line);background:#0f1319;color:#c9d1dc;
  font-family:var(--mono);font-size:12.4px;line-height:1.7;padding:13px 16px;white-space:pre-wrap;
  word-break:break-word;max-height:420px;overflow:auto;margin:0}
.pyrun .pout.show{display:block}
.pyrun .pout .oerr{color:#e0929a}
.pyrun .pout .ook{color:#7fd6a0}
.pyrun .pout .odim{color:#5A6472}
.pyrun .pexp{border-top:1px solid var(--line);background:var(--gold-soft);padding:11px 16px;font-size:.9rem;color:var(--text);line-height:1.7}
.pyrun .pexp b{color:#8a5c00}
@media print{.pyrun .pbar{display:none}.pyrun{break-inside:avoid}.pyrun .pout{display:block;max-height:none}}

/* the shared runtime banner */
.pyboot{margin:1.5rem 0;border:1px dashed var(--indigo-line);border-radius:12px;background:var(--indigo-soft);padding:14px 17px;font-size:.92rem;line-height:1.7;color:var(--text)}
.pyboot b{color:var(--indigo)}
.pyboot .pbootbtn{margin-top:10px;display:inline-block;font-family:var(--mono);font-size:11.5px;padding:7px 14px;border-radius:8px;border:1px solid var(--indigo);background:var(--indigo);color:#fff;cursor:pointer;font-weight:600}
.pyboot .pbootbtn:disabled{opacity:.5;cursor:not-allowed}

/* ---- deeper-structure helpers ---- */
.content h4{font-family:var(--disp);font-weight:600;font-size:1.06rem;color:var(--ink);margin:1.9rem 0 .5rem;letter-spacing:-.2px}
.content h4::before{content:"";display:inline-block;width:14px;height:2px;background:var(--gold);vertical-align:middle;margin-right:9px}
.content h5{font-family:var(--disp);font-weight:600;font-size:.96rem;color:var(--muted);margin:1.3rem 0 .4rem;letter-spacing:.2px}
.cmp{margin:1.2rem 0;border:1px solid var(--line);border-radius:13px;overflow:hidden;background:var(--surface);box-shadow:var(--shadow)}
.cmp .ch{background:var(--ink);color:#fff;padding:10px 16px;font-family:var(--disp);font-weight:600;font-size:.98rem;display:flex;align-items:center;gap:10px}
.cmp .ch .cn{font-family:var(--mono);font-size:11px;color:#14181f;background:var(--gold-2);padding:2px 8px;border-radius:20px;font-weight:600}
.cmp .crow{display:grid;grid-template-columns:132px 1fr;border-top:1px solid var(--line)}
.cmp .crow:first-child{border-top:none}
.cmp .crow .cl{background:var(--paper);padding:11px 14px;font-family:var(--mono);font-size:10.5px;letter-spacing:1.1px;text-transform:uppercase;color:var(--muted);border-right:1px solid var(--line)}
.cmp .crow .cv{padding:11px 16px;font-size:.94rem;line-height:1.6}
.cmp .crow.bad .cl{color:#a33}
.cmp .crow.good .cl{color:#1c7a42}
@media (max-width:620px){.cmp .crow{grid-template-columns:1fr}.cmp .crow .cl{border-right:none;border-bottom:1px solid var(--line)}}
"""

# the shared Pyodide bootstrap — injected once per page, just before </body>
PY_RUNTIME = r"""
<script>
/* ------------------------------------------------------------------------
   Shared in-browser Python runtime for every .pyrun cell on the page.
   Pyodide (CPython 3.14 compiled to WebAssembly) is loaded LAZILY on the
   first Run click, so the page itself stays light. numpy / pandas / sklearn
   wheels are fetched on demand the first time a cell imports them.
   ------------------------------------------------------------------------ */
window.PyRT = (function () {
  var PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v314.0.5/full/pyodide.js";
  var pyodide = null, booting = null, loaded = {};
  var listeners = [];

  function announce(msg, cls) {
    listeners.forEach(function (fn) { try { fn(msg, cls); } catch (e) {} });
  }
  function onStatus(fn) { listeners.push(fn); }

  function loadScript(src) {
    return new Promise(function (res, rej) {
      var s = document.createElement("script");
      s.src = src; s.onload = res; s.onerror = function () { rej(new Error("could not load " + src)); };
      document.head.appendChild(s);
    });
  }

  function boot() {
    if (pyodide) return Promise.resolve(pyodide);
    if (booting) return booting;
    announce("downloading Python runtime (~12 MB, once per visit)…", "busy");
    booting = loadScript(PYODIDE_URL)
      .then(function () {
        announce("starting CPython…", "busy");
        return loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v314.0.5/full/" });
      })
      .then(function (py) {
        pyodide = py;
        announce("Python ready", "ready");
        return py;
      })
      .catch(function (e) {
        booting = null;
        announce("runtime failed to load — you are probably offline. " +
                 "The expected output is shown under each cell.", "err");
        throw e;
      });
    return booting;
  }

  /* map an import name -> the Pyodide package that provides it */
  var PKG = {
    numpy: "numpy", pandas: "pandas", sklearn: "scikit-learn", scipy: "scipy",
    matplotlib: "matplotlib", pyarrow: "pyarrow", statsmodels: "statsmodels"
  };
  function neededPackages(code) {
    var want = {};
    var re = /(?:^|\n)\s*(?:import|from)\s+([A-Za-z_][\w.]*)/g, m;
    while ((m = re.exec(code))) {
      var top = m[1].split(".")[0];
      if (PKG[top] && !loaded[PKG[top]]) want[PKG[top]] = 1;
    }
    return Object.keys(want);
  }

  function run(code) {
    return boot().then(function (py) {
      var pkgs = neededPackages(code);
      var p = Promise.resolve();
      if (pkgs.length) {
        announce("fetching " + pkgs.join(", ") + "…", "busy");
        p = py.loadPackage(pkgs).then(function () {
          pkgs.forEach(function (k) { loaded[k] = 1; });
          announce("Python ready", "ready");
        });
      }
      return p.then(function () {
        var out = [];
        py.setStdout({ batched: function (s) { out.push(s); } });
        py.setStderr({ batched: function (s) { out.push(s); } });
        return py.runPythonAsync(code).then(
          function (val) {
            var txt = out.join("\n");
            /* echo the value of a trailing expression, REPL-style */
            if (val !== undefined && val !== null) {
              var r;
              try { r = py.globals.get("repr")(val); } catch (e) { r = String(val); }
              if (r !== "None") txt += (txt && !txt.endsWith("\n") ? "\n" : "") + r;
            }
            return { ok: true, text: txt };
          },
          function (err) {
            return { ok: false, text: out.join("\n") + (out.length ? "\n" : "") + String(err.message || err) };
          }
        );
      });
    }).catch(function (e) {
      return { ok: false, text: String(e.message || e), offline: true };
    });
  }

  function reset() { pyodide = null; booting = null; loaded = {}; announce("runtime discarded — next Run reloads it", ""); }
  function isReady() { return !!pyodide; }

  return { boot: boot, run: run, reset: reset, onStatus: onStatus, isReady: isReady };
})();

/* wire up every .pyrun cell */
(function () {
  var cells = document.querySelectorAll(".pyrun");
  if (!cells.length) return;

  function setStatus(el, msg, cls) {
    var s = el.querySelector(".pstat");
    if (s) { s.textContent = msg; s.className = "pstat" + (cls ? " " + cls : ""); }
  }
  window.PyRT.onStatus(function (msg, cls) {
    for (var i = 0; i < cells.length; i++) {
      var s = cells[i].querySelector(".pstat");
      if (s && !s.dataset.local) { s.textContent = msg; s.className = "pstat" + (cls ? " " + cls : ""); }
    }
  });

  for (var i = 0; i < cells.length; i++) (function (cell) {
    var ta   = cell.querySelector("textarea");
    var out  = cell.querySelector(".pout");
    var run  = cell.querySelector(".pbtn.run");
    var rst  = cell.querySelector(".pbtn.reset");
    var seed = ta ? ta.value : "";

    if (ta) {
      /* size to content, and keep Tab inside the editor */
      var fit = function () { ta.style.height = "auto"; ta.style.height = (ta.scrollHeight + 4) + "px"; };
      fit(); ta.addEventListener("input", fit);
      ta.addEventListener("keydown", function (e) {
        if (e.key === "Tab") {
          e.preventDefault();
          var s = ta.selectionStart, t = ta.selectionEnd;
          ta.value = ta.value.slice(0, s) + "    " + ta.value.slice(t);
          ta.selectionStart = ta.selectionEnd = s + 4;
        }
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); doRun(); }
      });
    }

    function doRun() {
      if (!ta || !out) return;
      run.disabled = true;
      var s = cell.querySelector(".pstat"); if (s) s.dataset.local = "1";
      setStatus(cell, "running…", "busy");
      out.classList.add("show");
      out.innerHTML = '<span class="odim">running…</span>';
      window.PyRT.run(ta.value).then(function (r) {
        run.disabled = false;
        if (s) delete s.dataset.local;
        var txt = (r.text || "").replace(/[&<>]/g, function (c) {
          return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c];
        });
        if (r.ok) {
          setStatus(cell, "ok", "ready");
          out.innerHTML = txt ? txt : '<span class="odim">(ran cleanly — no output; add a print())</span>';
        } else {
          setStatus(cell, r.offline ? "offline" : "error", "err");
          out.innerHTML = '<span class="oerr">' + (txt || "failed") + "</span>";
        }
      });
    }

    if (run) run.addEventListener("click", doRun);
    if (rst) rst.addEventListener("click", function () {
      if (ta) { ta.value = seed; ta.style.height = "auto"; ta.style.height = (ta.scrollHeight + 4) + "px"; }
      if (out) { out.classList.remove("show"); out.innerHTML = ""; }
      setStatus(cell, window.PyRT.isReady() ? "Python ready" : "idle", window.PyRT.isReady() ? "ready" : "");
    });
  })(cells[i]);

  /* page-level "warm up the runtime now" buttons (several in the stitched file) */
  var warms = document.querySelectorAll(".pbootbtn");
  for (var w = 0; w < warms.length; w++) (function (btn) {
    btn.addEventListener("click", function () {
      for (var j = 0; j < warms.length; j++) { warms[j].disabled = true; warms[j].textContent = "loading…"; }
      window.PyRT.boot().then(function () {
        for (var j = 0; j < warms.length; j++) warms[j].textContent = "Python is ready ✓";
      }).catch(function () {
        for (var j = 0; j < warms.length; j++) {
          warms[j].textContent = "failed — check your connection"; warms[j].disabled = false;
        }
      });
    });
  })(warms[w]);
})();
</script>
"""

# ------------------------------------------------------------------- part spec
P = {}

def part(n, file, title, pk, groups, h1, sub, thesis, chips, prev, prevhref, nxt):
    P[n] = dict(file=file, title=title, pk=pk, groups=groups, h1=h1, sub=sub,
                thesis=thesis, chips=chips, prev=prev, prevhref=prevhref, nxt=nxt)

def chips(level, topics, diagrams, cells, qa, hours):
    s = ('<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>%s</b></span>\n'
         '          <span class="chip"><b>%d</b> sections</span>\n') % (level, topics)
    if diagrams:
        s += '          <span class="chip">📐 <b>%d</b> diagrams</span>\n' % diagrams
    s += '          <span class="chip">💬 <b>%d</b> Q&amp;A</span>\n' % qa
    if cells:
        s += '          <span class="chip">▶ <b>%d</b> runnable cells</span>\n' % cells
    s += '          <span class="chip">⏱ <b>~%s</b></span>' % hours
    return s

def G(pk, head, links): return (pk, head, links)

part(1, "PY_Part01_DataModel.html", "The Python Data Model", "L0",
 [G("L0","The Data Model",[("p1-1","1.1 · Names, objects and bindings ⭐⭐"),
   ("p1-2","1.2 · Mutable vs immutable ⭐⭐"),("p1-3","1.3 · <code>is</code> vs <code>==</code> ⭐"),
   ("p1-4","1.4 · Hashability ⭐"),("p1-5","1.5 · The mutable default trap ⭐⭐"),
   ("p1-6","1.6 · Copies: none, shallow, deep ⭐⭐"),("p1-7","1.7 · Scope and the LEGB rule ⭐"),
   ("p1-8","1.8 · Late binding in closures ⭐"),("p1-9","1.9 · Memory and garbage collection")])],
 "Why Python does that",
 "Names as bindings rather than boxes, mutability as the root cause of most surprises, identity versus equality, "
 "hashability, the mutable-default-argument trap, the three kinds of copy, scope resolution, late binding, and how "
 "memory is actually reclaimed.",
 "Every &ldquo;wait, <em>why</em> did it do that?&rdquo; moment in Python traces back to this part. The single idea that "
 "unlocks the rest: <strong>a name is a label attached to an object, not a box containing one.</strong> Once you hold that, "
 "the mutable-default trap, aliasing bugs, <code class=\"ic\">is</code>-versus-<code class=\"ic\">==</code>, shallow copies "
 "and late binding all stop being separate pieces of trivia and become one mechanism seen from different angles. "
 "Interviewers probe here because it is where self-taught fluency and genuine understanding diverge — plenty of people "
 "write pandas daily and still cannot say what <code class=\"ic\">a = b</code> does.",
 chips("Level 0", 9, 2, 9, 22, "6h"),
 ("Learning Hub","All subjects"), "../index.html",
 ("Part 2 · Data Structures &amp; Complexity",["The four-way choice","The complexity table"]))

part(2, "PY_Part02_DataStructures.html", "Data Structures &amp; Complexity", "L1",
 [G("L1","Data Structures",[("p2-1","2.1 · The four-way choice ⭐⭐"),
   ("p2-2","2.2 · The complexity table ⭐⭐"),("p2-3","2.3 · The accidental O(n²) ⭐"),
   ("p2-4","2.4 · Dictionaries in depth ⭐"),("p2-5","2.5 · <code>collections</code> ⭐"),
   ("p2-6","2.6 · <code>deque</code>, <code>heapq</code>, <code>bisect</code>"),
   ("p2-7","2.7 · Sorting properly ⭐"),("p2-8","2.8 · Comprehensions ⭐"),
   ("p2-9","2.9 · Slicing, unpacking and <code>zip</code>")])],
 "Choosing the right container, and knowing what it costs",
 "list / tuple / set / dict as a decision rather than a habit, the complexity table you are expected to recall, the "
 "accidental quadratic that shows up in most take-homes, dictionaries in depth, the <code>collections</code> module, "
 "heaps and bisect, sorting with keys, and comprehensions.",
 "This part is where live-coding rounds are quietly won and lost. Not because anyone asks you to implement a hash table, "
 "but because the difference between a five-second solution and a five-minute one is almost always <strong>one container "
 "choice</strong> — a <code class=\"ic\">set</code> instead of a <code class=\"ic\">list</code> for membership, a "
 "<code class=\"ic\">Counter</code> instead of a hand-rolled dict, a <code class=\"ic\">heapq</code> instead of a full sort. "
 "The complexity table in §2.2 is the one piece of memorisation in this guide that genuinely pays, and §2.3 is the bug "
 "interviewers watch for you to notice unprompted.",
 chips("Level 1", 9, 1, 8, 19, "6h"),
 ("Part 1 · The Data Model","Bindings, mutability, copies"), "PY_Part01_DataModel.html",
 ("Part 3 · Functions &amp; Decorators",["Closures and capture","Decorators from scratch"]))

part(3, "PY_Part03_Functions.html", "Functions, Closures &amp; Decorators", "L2",
 [G("L2","Functions &amp; Decorators",[("p3-1","3.1 · The full signature grammar ⭐"),
   ("p3-2","3.2 · Closures and what they capture ⭐⭐"),("p3-3","3.3 · Decorators from scratch ⭐⭐"),
   ("p3-4","3.4 · Decorators with arguments ⭐"),("p3-5","3.5 · The four you will actually write ⭐"),
   ("p3-6","3.6 · <code>functools</code> ⭐"),("p3-7","3.7 · Lambdas, and their limits"),
   ("p3-8","3.8 · Type hints that earn their keep")])],
 "Functions as objects, and the decorator question",
 "The full parameter grammar including keyword-only arguments, closures and exactly what they capture, building a "
 "decorator from first principles, decorators that take arguments, the four decorators you will genuinely write, the "
 "useful half of <code>functools</code>, lambdas, and type hints.",
 "&ldquo;What is a decorator?&rdquo; is close to guaranteed, and the answer that scores is not the definition — it is "
 "<strong>writing one on the whiteboard, correctly, including <code class=\"ic\">functools.wraps</code></strong>, and then "
 "explaining what breaks without it. This part builds to that. The prerequisite is closures: a decorator is just a closure "
 "over a function object, so if §3.2 is solid, §3.3 is bookkeeping. The practical payoff is §3.5, where the timing, retry, "
 "caching and validation decorators are the ones that keep appearing in real data pipelines.",
 chips("Level 2", 8, 1, 7, 15, "6h"),
 ("Part 2 · Data Structures","Containers and complexity"), "PY_Part02_DataStructures.html",
 ("Part 4 · Generators &amp; Laziness",["The iterator protocol","Streaming a 10 GB file"]))

part(4, "PY_Part04_Generators.html", "Iterators, Generators &amp; Laziness", "L3",
 [G("L3","Generators",[("p4-1","4.1 · The iterator protocol ⭐"),
   ("p4-2","4.2 · Iterable vs iterator ⭐"),("p4-3","4.3 · Generators ⭐⭐"),
   ("p4-4","4.4 · Streaming a file too big for RAM ⭐⭐"),("p4-5","4.5 · <code>itertools</code> ⭐"),
   ("p4-6","4.6 · Generator pipelines"),("p4-7","4.7 · Context managers ⭐"),
   ("p4-8","4.8 · Exceptions in a data pipeline ⭐")])],
 "Processing more data than you have memory for",
 "The iterator protocol, the iterable-versus-iterator distinction that explains single-use generators, generator "
 "functions and expressions, streaming a file larger than RAM, the useful half of <code>itertools</code>, generator "
 "pipelines, context managers, and exception handling that fails loudly.",
 "The generator question is really a <strong>memory</strong> question, and the answer interviewers want is a number: a list "
 "comprehension over ten million rows materialises all ten million; the generator expression holds one. That is the whole "
 "point, and §4.4 turns it into the practical skill — aggregating a file bigger than your machine's RAM without ever "
 "loading it. The subtlety worth knowing cold is §4.2: a generator is <em>its own iterator</em>, which is why iterating it "
 "twice silently gives you nothing the second time, and why that bug is so hard to see in a notebook.",
 chips("Level 3", 8, 1, 8, 15, "5h"),
 ("Part 3 · Functions &amp; Decorators","Closures, decorators, functools"), "PY_Part03_Functions.html",
 ("Part 5 · OOP &amp; Dataclasses",["Dunder methods","A sklearn-compatible estimator"]))

part(5, "PY_Part05_OOP.html", "OOP, Dataclasses &amp; Protocols", "L4",
 [G("L4","OOP &amp; Dataclasses",[("p5-1","5.1 · Classes and the instance dict"),
   ("p5-2","5.2 · Class vs instance attributes ⭐⭐"),("p5-3","5.3 · Properties ⭐"),
   ("p5-4","5.4 · <code>staticmethod</code> vs <code>classmethod</code> ⭐"),
   ("p5-5","5.5 · Dunder methods ⭐"),("p5-6","5.6 · Dataclasses ⭐⭐"),
   ("p5-7","5.7 · Choosing a record type ⭐"),("p5-8","5.8 · Inheritance, MRO and composition ⭐"),
   ("p5-9","5.9 · A sklearn-compatible estimator ⭐")])],
 "Enough OOP to write clean pipeline code",
 "Classes and the instance dict, the class-attribute trap, properties for validation, static versus class methods, the "
 "dunder methods worth implementing, dataclasses, choosing between dataclass / NamedTuple / TypedDict / Pydantic, "
 "inheritance versus composition, and writing a transformer scikit-learn will accept.",
 "Data scientists get asked less OOP than backend engineers, and the questions are more practical: <strong>can you write a "
 "class that fits into someone else's framework?</strong> §5.9 is the version of that question with teeth — a custom "
 "<code class=\"ic\">fit</code>/<code class=\"ic\">transform</code> estimator that survives "
 "<code class=\"ic\">clone</code>, <code class=\"ic\">GridSearchCV</code> and a "
 "<code class=\"ic\">Pipeline</code>, which is a real skill with real rules. §5.2 is the trap: a mutable class attribute "
 "shared across every instance is the OOP twin of the mutable default argument, and it is asked because it tests whether "
 "Part 1 actually landed.",
 chips("Level 4", 9, 0, 9, 20, "6h"),
 ("Part 4 · Generators","Laziness, itertools, context managers"), "PY_Part04_Generators.html",
 ("Part 6 · NumPy",["Views vs copies","Broadcasting rules"]))

part(6, "PY_Part06_NumPy.html", "NumPy", "L5",
 [G("L5","NumPy",[("p6-1","6.1 · Anatomy of an ndarray ⭐⭐"),
   ("p6-2","6.2 · Why arrays beat lists ⭐"),("p6-3","6.3 · dtypes and silent overflow ⭐"),
   ("p6-4","6.4 · Views vs copies ⭐⭐"),("p6-5","6.5 · Strides, reshape and transpose ⭐"),
   ("p6-6","6.6 · Basic vs fancy indexing ⭐⭐"),("p6-7","6.7 · Broadcasting ⭐⭐"),
   ("p6-8","6.8 · Axis semantics ⭐"),("p6-9","6.9 · Vectorising a loop ⭐⭐"),
   ("p6-10","6.10 · Floats, NaN and reproducibility ⭐")])],
 "The array, and why it is fast",
 "The ndarray as buffer + dtype + shape + strides, why that beats a list, dtype overflow, views versus copies, how "
 "reshape and transpose avoid copying, basic versus fancy indexing, the three broadcasting rules, axis semantics, "
 "vectorising a real loop, and floating-point care.",
 "NumPy questions are a proxy for whether you understand <strong>memory</strong>. The whole library follows from one "
 "sentence: an array is a <em>flat buffer plus a dtype plus a shape plus strides</em>, and almost every operation that "
 "feels like magic — reshape, transpose, slicing — is just new strides over the same buffer. That single model answers "
 "views-versus-copies, explains why fancy indexing must copy, and tells you why a slice of an array can mutate its parent. "
 "§6.7 (broadcasting) and §6.9 (vectorising) are the two most-asked; §6.4 is the one that separates people who have "
 "debugged a real aliasing bug from people who have not.",
 chips("Level 5", 10, 2, 10, 21, "8h"),
 ("Part 5 · OOP &amp; Dataclasses","Classes, dataclasses, estimators"), "PY_Part05_OOP.html",
 ("Part 7 · pandas Core",["Copy-on-Write in pandas 3.0","loc vs iloc"]))

part(7, "PY_Part07_PandasCore.html", "pandas Core", "L6",
 [G("L6","pandas Core",[("p7-1","7.1 · Series, DataFrame, and the index ⭐⭐"),
   ("p7-2","7.2 · Index alignment ⭐"),("p7-3","7.3 · dtypes after pandas 3.0 ⭐⭐"),
   ("p7-4","7.4 · <code>.loc</code> vs <code>.iloc</code> vs <code>[]</code> ⭐⭐"),
   ("p7-5","7.5 · Copy-on-Write and the end of SettingWithCopyWarning ⭐⭐"),
   ("p7-6","7.6 · Missing data ⭐"),("p7-7","7.7 · Reading data properly ⭐"),
   ("p7-8","7.8 · Duplicates and type conversion"),("p7-9","7.9 · Method chaining ⭐")])],
 "The library you will actually be tested on",
 "Series and DataFrame as an index plus typed columns, alignment, what pandas 3.0 changed about dtypes, the three ways "
 "to select and when each is right, Copy-on-Write and the removal of <code>SettingWithCopyWarning</code>, missing data, "
 "reading files without losing your schema, and readable method chains.",
 "If an interview touches one library, it is this one. Two sections are disproportionately valuable. §7.4 is asked almost "
 "every time and the complete answer includes <em>why <code class=\"ic\">df[...]</code> is ambiguous</em>, not just that "
 "<code class=\"ic\">.loc</code> is labels. §7.5 is the <strong>currency question</strong> for 2026: pandas 3.0 made "
 "Copy-on-Write the only mode, which <em>removed</em> <code class=\"ic\">SettingWithCopyWarning</code> entirely and turned "
 "chained assignment from unpredictable into reliably silent. A candidate still reciting the 2019 answer is dating "
 "themselves; a candidate who explains what replaced it sounds current.",
 chips("Level 6", 9, 2, 9, 18, "8h"),
 ("Part 6 · NumPy","Strides, views, broadcasting"), "PY_Part06_NumPy.html",
 ("Part 8 · pandas Transformation",["agg vs transform vs apply","Joins that explode"]))

part(8, "PY_Part08_PandasTransform.html", "pandas Transformation", "L7",
 [G("L7","pandas Transformation",[("p8-1","8.1 · Split-apply-combine ⭐⭐"),
   ("p8-2","8.2 · <code>agg</code> vs <code>transform</code> vs <code>apply</code> ⭐⭐"),
   ("p8-3","8.3 · groupby gotchas ⭐"),("p8-4","8.4 · <code>merge</code>: the five joins ⭐⭐"),
   ("p8-5","8.5 · Joins that explode ⭐⭐"),("p8-6","8.6 · <code>merge_asof</code> and point-in-time joins ⭐"),
   ("p8-7","8.7 · Wide, long, and the MultiIndex ⭐"),("p8-8","8.8 · Time series ⭐"),
   ("p8-9","8.9 · Windows and lag features without leakage ⭐⭐"),
   ("p8-10","8.10 · SQL → pandas ⭐")])],
 "Reshaping, joining and aggregating without breaking the data",
 "The split-apply-combine model, the agg / transform / apply decision, groupby gotchas, the five join types and what "
 "each keeps, why row counts explode, point-in-time joins, wide-versus-long and the MultiIndex, time series, window "
 "functions and leakage-free lag features, and translating SQL.",
 "This is the part that mirrors the actual job, and the questions are correspondingly practical. Three sections carry "
 "outsized weight. §8.2 — <strong>agg reduces, transform preserves shape, apply is the slow escape hatch</strong> — is a "
 "one-line answer that immediately signals fluency. §8.5 is the bug that has cost real companies real money: a "
 "many-to-many join silently multiplying rows, which is why <code class=\"ic\">validate=</code> exists and why you assert "
 "row counts. And §8.9 is where a pandas question becomes a machine-learning question — a rolling mean computed without "
 "shifting leaks the future into your features, and the model looks brilliant until it is deployed.",
 chips("Level 7", 10, 1, 10, 20, "9h"),
 ("Part 7 · pandas Core","Selection, dtypes, Copy-on-Write"), "PY_Part07_PandasCore.html",
 ("Part 9 · Performance &amp; Memory",["The vectorisation ladder","The GIL in 2026"]))

part(9, "PY_Part09_Performance.html", "Performance, Memory &amp; Concurrency", "L8",
 [G("L8","Performance &amp; Memory",[("p9-1","9.1 · Measure first ⭐"),
   ("p9-2","9.2 · The vectorisation ladder ⭐⭐"),("p9-3","9.3 · Why <code>apply</code> is a loop ⭐"),
   ("p9-4","9.4 · Cutting memory in half ⭐⭐"),("p9-5","9.5 · Out-of-core with chunks ⭐"),
   ("p9-6","9.6 · The GIL, and Python 3.14 ⭐⭐"),
   ("p9-7","9.7 · Threads vs processes vs async ⭐⭐"),
   ("p9-8","9.8 · Escape hatches: Numba, Polars, DuckDB ⭐")])],
 "Making it fast, and knowing why it was slow",
 "Measuring before optimising, the vectorisation ladder from loop to NumPy, why <code>apply</code> is a loop in disguise, "
 "halving memory with dtypes and categories, out-of-core processing, the GIL and what free-threaded Python 3.14 changes, "
 "choosing threads / processes / async by workload, and when to leave pandas.",
 "Performance questions are really <strong>diagnosis</strong> questions: anyone can say &ldquo;vectorise it&rdquo;, but the "
 "signal is whether you profile first and can explain <em>where</em> the time went. §9.2 is the mental model — each rung "
 "of the ladder is roughly an order of magnitude — and §9.3 is the insight behind it: "
 "<code class=\"ic\">df.apply</code> is a Python-level loop with nicer syntax, which is why it is ~100× slower than the "
 "vectorised form and why &ldquo;I used apply&rdquo; is not an optimisation. §9.6 is the 2026 currency question: the GIL "
 "answer changed this year, because <strong>PEP 779 made free-threaded builds officially supported in Python 3.14</strong>, "
 "and knowing what that does and does not fix is a genuine differentiator.",
 chips("Level 8", 8, 2, 8, 15, "7h"),
 ("Part 8 · pandas Transformation","groupby, joins, windows"), "PY_Part08_PandasTransform.html",
 ("Part 10 · Production Python",["Leakage and pipelines","Testing data code"]))

part(10, "PY_Part10_Production.html", "Production Python for Data Science", "L9",
 [G("L9","Production",[("p10-1","10.1 · From notebook to module ⭐"),
   ("p10-2","10.2 · Environments and reproducible installs ⭐"),
   ("p10-3","10.3 · Config, secrets and logging ⭐"),
   ("p10-4","10.4 · Testing data code ⭐⭐"),("p10-5","10.5 · Validating data at the boundary ⭐"),
   ("p10-6","10.6 · Pipelines and <code>ColumnTransformer</code> ⭐⭐"),
   ("p10-7","10.7 · Data leakage ⭐⭐"),("p10-8","10.8 · Reproducibility ⭐"),
   ("p10-9","10.9 · The code-review checklist ⭐")])],
 "Code someone else can run next year",
 "Refactoring a notebook into modules, environments and lockfiles, config and logging, testing non-deterministic data "
 "code, schema validation at boundaries, scikit-learn pipelines and ColumnTransformer, every flavour of data leakage, "
 "reproducibility, and the code-review checklist.",
 "At four years' experience this is the part that decides your level. Two candidates can both write correct pandas; the "
 "one who gets the senior offer is the one whose code has <strong>tests, a pinned environment and no leakage</strong>. "
 "§10.7 is the highest-stakes section in the whole guide — fitting a scaler or an imputer before the split is the mistake "
 "that produces a wonderful cross-validation score and a model that fails in production, and §10.6 is the mechanism that "
 "makes it structurally impossible rather than merely discouraged. §10.4 is the section most candidates have no answer "
 "for at all, which makes even a modest one stand out.",
 chips("Level 9", 9, 1, 8, 15, "7h"),
 ("Part 9 · Performance &amp; Memory","Vectorisation, GIL, memory"), "PY_Part09_Performance.html",
 ("Part 11 · Interview Q&amp;A Bank",["The full question bank","Live-coding playground"]))

part(11, "PY_Part11_QABank.html", "Interview Q&amp;A Bank &amp; Playground", "QA",
 [G("QA","The Question Bank",[("p11-0","11.0 · How to use this bank"),
   ("p11-1","11.1 · The data model"),("p11-2","11.2 · Data structures &amp; complexity"),
   ("p11-3","11.3 · Functions, decorators, generators"),("p11-4","11.4 · OOP &amp; dataclasses"),
   ("p11-5","11.5 · NumPy"),("p11-6","11.6 · pandas core"),
   ("p11-7","11.7 · pandas transformation"),("p11-8","11.8 · Performance &amp; concurrency"),
   ("p11-9","11.9 · Production, testing &amp; leakage")]),
  G("REF","Practice &amp; Reference",[("p11-10","11.10 · The trap questions ⭐⭐"),
   ("p11-11","11.11 · Live-coding exercises ⭐"),("p11-12","11.12 · Free playground ▶"),
   ("p11-13","11.13 · SQL → pandas drill"),("p11-14","11.14 · The 90-second project story"),
   ("p11-15","11.15 · Gotchas cheat sheet ⭐"),("p11-16","11.16 · API quick reference")])],
 "The question bank",
 "The consolidated drill: high-frequency questions with model answers across every level, the trap questions, timed "
 "live-coding exercises with a real Python runtime, a free playground, a SQL-to-pandas translation drill, the gotchas "
 "sheet and an API quick reference.",
 "Every part of this subject ends its topics with the questions that topic answers — this is the <strong>consolidated "
 "drill</strong>, shuffled and stripped of context so you cannot coast on adjacency. Two sections deserve the most time. "
 "<strong>§11.10, the traps</strong>, because Python screens are lost on a small number of confidently-wrong answers — "
 "&ldquo;<code class=\"ic\">apply</code> is vectorised&rdquo;, &ldquo;the GIL means Python can't do parallelism&rdquo;, "
 "&ldquo;use <code class=\"ic\">inplace=True</code> to save memory&rdquo;. And <strong>§11.11</strong>, where the exercises "
 "run in a real CPython 3.14 in your browser, so you can actually type the solution under time pressure instead of "
 "reading one.",
 chips("Q&amp;A Bank", 17, 0, 9, 130, "7h drill"),
 ("Part 10 · Production Python","Pipelines, leakage, testing"), "PY_Part10_Production.html",
 ("Part 12 · Classic Coding Questions",["Reverse, palindrome, anagram","Fibonacci, FizzBuzz, Two Sum",
   "The whiteboard canon, done properly"]))

part(12, "PY_Part12_ClassicCoding.html", "Classic Coding Questions", "L10",
 [G("L10","The Classics",[("p12-1","12.1 · How the round is scored \u2b50\u2b50"),
   ("p12-2","12.2 · Reverse a string \u2b50\u2b50"),("p12-3","12.3 · Palindromes \u2b50\u2b50"),
   ("p12-4","12.4 · Anagrams \u2b50\u2b50"),("p12-5","12.5 · FizzBuzz \u2b50"),
   ("p12-6","12.6 · Fibonacci \u2b50\u2b50"),("p12-7","12.7 · Factorial &amp; big integers \u2b50"),
   ("p12-8","12.8 · Primes &amp; number theory \u2b50"),
   ("p12-9","12.9 · Counting &amp; first unique \u2b50\u2b50"),
   ("p12-10","12.10 · XOR, missing &amp; majority \u2b50")]),
  G("PAT","Patterns &amp; Drill",[("p12-11","12.11 · Two Sum &amp; the hash-map reflex \u2b50\u2b50"),
   ("p12-12","12.12 · Sliding window &amp; subarrays \u2b50"),
   ("p12-13","12.13 · List &amp; string surgery \u2b50"),
   ("p12-14","12.14 · Search, sort &amp; top-k \u2b50"),
   ("p12-15","12.15 · Stacks, brackets &amp; matrices"),
   ("p12-16","12.16 · The data-science versions \u2b50\u2b50"),
   ("p12-17","12.17 · Complexity cheat sheet"),
   ("p12-18","12.18 · Timed drill \u25b6")])],
 "The whiteboard canon",
 "Reverse a string, palindrome, anagram, FizzBuzz, Fibonacci, factorial, primes, duplicates, first non-repeating "
 "character, missing number, Two Sum, sliding windows, binary search, top-k, balanced brackets and matrix rotation "
 "\u2014 each with the answer they want, the follow-up they ask next, and a cell you can run.",
 "These are the questions everyone knows are coming and surprisingly many people still fumble, because the trap is not "
 "difficulty \u2014 it is <strong>depth</strong>. Anyone can type <code class=\"ic\">s[::-1]</code>. The signal is what you "
 "say in the next thirty seconds: that it is O(n) in time <em>and</em> space, that a two-pointer swap on a "
 "<code class=\"ic\">list</code> is the in-place version, that it silently corrupts text with combining accents or emoji "
 "modifiers, and how you would test it. Every section here gives you the one-liner, the from-scratch version an "
 "interviewer may insist on, the complexity to state unprompted, the edge case to raise before being asked, and the "
 "follow-up that usually comes next. And because <strong>every claim here has a runnable cell</strong>, you can "
 "watch the one-liner corrupt an accented string, watch naive Fibonacci fall off a cliff at n=35, and watch a "
 "nested loop collapse into one pass \u2014 rather than take any of it on trust.",
 chips("Level 10", 18, 4, 38, 68, "8h"),
 ("Part 11 · Interview Q&amp;A Bank","130 questions, 8 exercises"), "PY_Part11_QABank.html",
 ("Learning Hub",["All subjects"]))

# ------------------------------------------------------------------- the build
def build(pn):
    c = P[pn]
    html = SRC.read_text()

    s = html.index("</section>", html.index('id="tracker"')) + len("</section>")
    e = html.index("      <!-- PART NAV -->")
    html = html[:s] + "\n\n<!--CONTENT_INSERT-->\n\n      " + html[e:]

    html = html.replace("<title>RAG Interview Prep — Part 1: Foundations</title>",
                        f"<title>Python for Data Science — Part {pn}: {c['title']}</title>")
    html = html.replace('<div class="tt"><small>Part 1 / 6</small>Foundations</div>',
                        f'<div class="tt"><small>Part {pn} / {NP}</small>{c["title"]}</div>')
    html = html.replace('<div class="brand-txt">RAG Prep<small>Knowledge Base</small></div>',
                        '<div class="brand-txt">Python<small>Data Science Prep</small></div>')
    html = html.replace('<div class="k">Part 1 of 6</div>\n      <div class="v">Foundations</div>',
                        f'<div class="k">Part {pn} of {NP}</div>\n      <div class="v">{c["title"]}</div>')

    grp = ""
    for pk, head, links in c["groups"]:
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
           '<li><a href="index.html">← Python home</a></li></ul>\n      </div>\n    </nav>')
    html = re.sub(r'<nav class="toc" id="toc">.*?</nav>', lambda m: nav, html, count=1, flags=re.DOTALL)

    html = re.sub(r'<div class="sb-foot">.*?</div>',
        f'<div class="sb-foot">\n      Python for Data Science<br>Part {pn} — {c["title"]}<br>© your study kit\n    </div>',
        html, count=1, flags=re.DOTALL)

    hero = (f'<header class="hero">\n'
      f'        <div class="eyebrow">Part {pn} of {NP} · {c["title"]}</div>\n'
      f'        <h1 class="title">{c["h1"]}\n          <span class="sub">{c["sub"]}</span>\n        </h1>\n'
      f'        <p class="thesis">{c["thesis"]}</p>\n'
      f'        <div class="meta-chips">\n          {c["chips"]}\n        </div>\n      </header>')
    html = re.sub(r'<header class="hero">.*?</header>', lambda m: hero, html, count=1, flags=re.DOTALL)

    nl = "".join(f"<li>{x}</li>" for x in (c["nxt"][1] if isinstance(c["nxt"][1], list) else []))
    nh = "index.html" if c["nxt"][0] == "Learning Hub" else P.get(pn + 1, {}).get("file", "index.html")
    pnav = (f'<nav class="partnav">\n'
      f'        <div class="pcard"><div class="k">Previously</div><div class="t"><a href="{c["prevhref"]}">{c["prev"][0]}</a></div><ul><li>{c["prev"][1]}</li></ul></div>\n'
      f'        <div class="pcard"><div class="k">You are here</div><div class="t">Part {pn} · {c["title"]}</div></div>\n'
      f'        <div class="pcard next"><div class="k">Coming next</div><div class="t"><a href="{nh}">{c["nxt"][0]}</a></div><ul>{nl}</ul></div>\n'
      f'      </nav>')
    html = re.sub(r'<nav class="partnav">.*?</nav>', lambda m: pnav, html, count=1, flags=re.DOTALL)

    html = re.sub(r'<div class="doc-foot">.*?</div>',
      f'<div class="doc-foot">\n        Python for Data Science Interviews — Part {pn} of {NP} · {c["title"]}<br>\n'
      f'        Library-current as of <b>Aug 2026</b> — Python <b>3.14</b> (PEP 779 free-threading) · '
      f'pandas <b>3.0</b> (Copy-on-Write only) · NumPy <b>2.5</b> · scikit-learn <b>1.9</b>.<br>\n'
      f'        Runnable cells execute <b>real CPython 3.14</b> in your browser via Pyodide — nothing is sent to a server.<br>\n'
      f'        Progress is stored locally under key <code style="color:#8892a0">pyPrepStatus_v1</code> and is shared by every part of this subject.\n      </div>',
      html, count=1, flags=re.DOTALL)

    _ph = "const PHASES = " + json.dumps(PHASES, ensure_ascii=False) + ";"
    _or = "const ORDER = " + json.dumps(ORDER) + ";"
    _tk = "const TRACKER = " + tracker_js + ";"
    html = re.sub(r'const PHASES = \{.*?\};', lambda m: _ph, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const ORDER = \[.*?\];', lambda m: _or, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const TRACKER = \[.*?\n\];', lambda m: _tk, html, count=1, flags=re.DOTALL)
    html = html.replace('const LS_KEY="ragPrepStatus_v1";', 'const LS_KEY="pyPrepStatus_v1";')
    html = html.replace("206", str(TOTAL))
    html = re.sub(r'<p class="tk-sub">.*?</p>',
      f'<p class="tk-sub">One tracker for the whole Python subject — all {TOTAL} topics across all {NP} parts. '
      f'Set a status on any row; your progress saves in this browser and prints as a clean checklist.</p>',
      html, count=1, flags=re.DOTALL)

    html = html.replace("</style>", WIDGET_CSS + "</style>", 1)
    html = html.replace("</body>", PY_RUNTIME + "\n</body>", 1)

    (HERE / c["file"]).write_text(html)
    assert "<!--CONTENT_INSERT-->" in html and "ragPrepStatus" not in html and "window.PyRT" in html
    print(f"  wrote {c['file']} ({len(html):,} bytes)")

if __name__ == "__main__":
    for p in ([int(a) for a in sys.argv[1:]] or P):
        build(p)
