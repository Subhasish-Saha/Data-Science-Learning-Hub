#!/usr/bin/env python3
"""Build the "SQL for Data Science Interviews" subject shells.

One part per blueprint level (11 levels + an interview drill = 12 parts), ordered
strictly easy -> hard, so every topic gets room for prose, a worked query, its own
interview Q&A box, and a runnable cell.

Reuses the shared design system from the RAG Part 1 file, swaps in a SQL tracker
(own localStorage key: sqlPrepStatus_v1), per-part chrome, and the CSS + JS for
the live in-browser SQL runner: sql.js 1.14.2, which is SQLite 3.49.1 compiled to
WebAssembly (~660 KB), seeded with a 12-table demo database. Each shell carries a
<!--CONTENT_INSERT--> marker that content fragments are spliced into by insert.py."""
import re, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent          # .../output/sql
SITE = HERE.parent                                       # .../output
SRC  = SITE / "rag" / "RAG_Interview_Prep_Part1_Foundations.html"
MD   = SITE.parent / "sql-data-science-study-guide.md"
NP   = 12            # number of parts

LEVEL_KEY = {
 "Level 0 — The Warm-Up You Must Not Fumble":        ("l0",  "Level 0 · Warm-Up"),
 "Level 1 — Joins, and How They Go Wrong":           ("l1",  "Level 1 · Joins"),
 "Level 2 — Aggregation, Subqueries and CTEs":       ("l2",  "Level 2 · Aggregation &amp; CTEs"),
 "Level 3 — Window Functions I: Ranking":            ("l3",  "Level 3 · Windows I"),
 "Level 4 — Window Functions II: Frames and Offsets":("l4",  "Level 4 · Windows II"),
 "Level 5 — Dates, Times and Series":                ("l5",  "Level 5 · Dates &amp; Series"),
 "Level 6 — Product Analytics Patterns":             ("l6",  "Level 6 · Product Analytics"),
 "Level 7 — Gaps and Islands":                       ("l7",  "Level 7 · Gaps &amp; Islands"),
 "Level 8 — The Hard Patterns":                      ("l8",  "Level 8 · Hard Patterns"),
 "Level 9 — Dirty Data and Correctness":             ("l9",  "Level 9 · Dirty Data"),
 "Level 10 — Performance and Engine Internals":      ("l10", "Level 10 · Performance"),
}
CAT = {"l0":"Fundamentals","l1":"Joins","l2":"Aggregation","l3":"Windows","l4":"Windows",
       "l5":"Dates","l6":"Analytics","l7":"Patterns","l8":"Patterns","l9":"Correctness",
       "l10":"Performance"}
HIGH = {"l0","l1","l3","l4","l6","l7"}      # the levels interviews weight most heavily

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
    if cur and re.match(r'^\s*- \[ \]', line):
        t = clean(re.sub(r'^\s*- \[ \]\s*', '', line))
        if t:
            k = cur[0]
            cat = "Interview Prep" if k == "iv" else CAT[k]
            pri = "High" if k in HIGH or k == "iv" else "Medium"
            rows.append([k, cat, pri, t])

PHASES = {k: v for k, v in LEVEL_KEY.values()}
PHASES.update({"iv": "Interview Drill"})
ORDER = ["l0","l1","l2","l3","l4","l5","l6","l7","l8","l9","l10","iv"]

tracker_js = "[\n" + ",\n".join(
    f'[{i+1},"{r[0]}","{r[1]}","{r[2]}",0,{json.dumps(r[3])}]' for i, r in enumerate(rows)) + "\n]"
TOTAL = len(rows)
print(f"tracker: {TOTAL} items across {len(ORDER)} groups")

# --------------------------------------------------------------- CSS additions
WIDGET_CSS = """
/* ---------------- runnable SQL cell ---------------- */
.sqlrun{margin:1.7rem 0;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--surface);box-shadow:var(--shadow)}
.sqlrun .sh{background:#14181f;color:#e6e9ef;padding:9px 15px;font-family:var(--mono);font-size:11.5px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;border-bottom:1px solid #2c3542}
.sqlrun .sh .dot3{display:inline-flex;gap:5px;margin-right:4px}
.sqlrun .sh .dot3 i{width:9px;height:9px;border-radius:50%;display:block}
.sqlrun .sh .stag{font-size:9px;letter-spacing:1.5px;text-transform:uppercase;background:#3B8CC4;color:#04121c;padding:2px 7px;border-radius:20px;font-weight:700}
.sqlrun .sh .stag.drill{background:#F0A81E;color:#1a1204}
.sqlrun .sh .stag.trap{background:#c9564f;color:#fff}
.sqlrun .sh .sname{color:#8892a0}
.sqlrun .sh .sspacer{flex:1}
.sqlrun .sh .sstat{font-size:10.5px;color:#8892a0}
.sqlrun .sh .sstat.busy{color:var(--gold-2)}
.sqlrun .sh .sstat.ready{color:#7fd6a0}
.sqlrun .sh .sstat.err{color:#e0929a}
.sqlrun textarea{width:100%;box-sizing:border-box;border:0;outline:0;resize:vertical;display:block;
  background:#0f1319;color:#e6e9ef;font-family:var(--mono);font-size:12.6px;line-height:1.72;
  padding:14px 16px;tab-size:2;min-height:88px;caret-color:var(--gold-2)}
.sqlrun textarea::selection{background:#31405c}
.sqlrun .sbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:10px 14px;background:var(--paper);border-top:1px solid var(--line)}
.sqlrun .sbtn{font-family:var(--mono);font-size:11.5px;padding:6px 13px;border-radius:8px;border:1px solid var(--line);background:var(--surface);color:var(--text);cursor:pointer;transition:.13s}
.sqlrun .sbtn:hover{border-color:var(--indigo-line);background:var(--indigo-soft)}
.sqlrun .sbtn.run{background:var(--indigo);color:#fff;border-color:var(--indigo);font-weight:600}
.sqlrun .sbtn.run:hover{filter:brightness(1.08)}
.sqlrun .sbtn:disabled{opacity:.45;cursor:not-allowed}
.sqlrun .shint{font-family:var(--mono);font-size:10.5px;color:var(--muted);margin-left:auto}
.sqlrun .sout{display:none;border-top:1px solid var(--line);background:#0f1319;color:#c9d1dc;
  font-family:var(--mono);font-size:12.2px;line-height:1.6;padding:12px 14px;
  max-height:460px;overflow:auto;margin:0}
.sqlrun .sout.show{display:block}
.sqlrun .sout .oerr{color:#e0929a;white-space:pre-wrap}
.sqlrun .sout .ook{color:#7fd6a0}
.sqlrun .sout .odim{color:#5A6472}
.sqlrun .sexp{border-top:1px solid var(--line);background:var(--gold-soft);padding:11px 16px;font-size:.9rem;color:var(--text);line-height:1.7}
.sqlrun .sexp b{color:#8a5c00}
@media print{.sqlrun .sbar{display:none}.sqlrun{break-inside:avoid}.sqlrun .sout{display:block;max-height:none}}

/* result grid rendered inside .sout */
table.sqltbl{border-collapse:collapse;font-family:var(--mono);font-size:11.8px;margin:0 0 8px;min-width:100%}
table.sqltbl th{background:#1b2husk;padding:0}
table.sqltbl thead th{background:#1b2129;color:#8fa0ff;text-align:left;padding:6px 11px;border:1px solid #2c3542;white-space:nowrap;font-weight:600}
table.sqltbl td{padding:5px 11px;border:1px solid #232b35;color:#dbe1ea;white-space:nowrap}
table.sqltbl tbody tr:nth-child(even) td{background:#131820}
table.sqltbl .snull{color:#6b7480;font-style:italic}
.sqlrun .sout .snote{color:#5A6472;font-size:10.8px;margin:2px 0 12px}
.sqlrun .sout .slabel{color:#8fa0ff;font-size:10.5px;letter-spacing:.6px;text-transform:uppercase;margin:0 0 5px}

/* the shared runtime banner */
.sqlboot{margin:1.5rem 0;border:1px dashed var(--indigo-line);border-radius:12px;background:var(--indigo-soft);padding:14px 17px;font-size:.92rem;line-height:1.7;color:var(--text)}
.sqlboot b{color:var(--indigo)}
.sqlboot .sbootbtn{margin-top:10px;display:inline-block;font-family:var(--mono);font-size:11.5px;padding:7px 14px;border-radius:8px;border:1px solid var(--indigo);background:var(--indigo);color:#fff;cursor:pointer}
.sqlboot .sbootbtn:hover{filter:brightness(1.08)}
.sqlboot .sbootbtn:disabled{opacity:.5;cursor:default}

/* schema reference strip */
.schemastrip{display:flex;flex-wrap:wrap;gap:7px;margin:1rem 0 1.4rem}
.schemastrip .tchip{font-family:var(--mono);font-size:11px;padding:5px 10px;border-radius:7px;
  border:1px solid var(--line);background:var(--paper);color:var(--muted)}
.schemastrip .tchip b{color:var(--indigo);font-weight:600}

/* comparison cards */
.cmp{display:grid;gap:12px;margin:1.4rem 0}
@media(min-width:720px){.cmp.two{grid-template-columns:1fr 1fr}.cmp.three{grid-template-columns:1fr 1fr 1fr}}
.crow{border:1px solid var(--line);border-radius:12px;padding:13px 15px;background:var(--surface)}
.crow .cl{font-family:var(--mono);font-size:10.5px;letter-spacing:1.2px;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.crow .cv{font-size:.94rem;line-height:1.72}
.crow.good{border-color:#bfe0cb;background:#f3fbf6}
.crow.bad{border-color:#e8c9c9;background:#fdf5f5}

h4{font-family:var(--disp);font-size:1.12rem;font-weight:600;letter-spacing:-.2px;margin:1.7rem 0 .5rem;color:var(--text)}
h5{font-family:var(--mono);font-size:.82rem;letter-spacing:1.1px;text-transform:uppercase;color:var(--muted);margin:1.3rem 0 .4rem}
"""
WIDGET_CSS = WIDGET_CSS.replace("#1b2husk", "#1b2129")   # guard against a stray edit

# --------------------------------------------------------- the seeded database
SEED = r"""
CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
INSERT INTO departments VALUES
 (1,'engineering','Chennai'),(2,'marketing','Mumbai'),(3,'sales','Chennai'),
 (4,'research','Bengaluru');

CREATE TABLE employees (
  id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, manager_id INTEGER,
  salary INTEGER, hire_date TEXT);
INSERT INTO employees VALUES
 ( 1,'Asha',      1, NULL, 210000,'2019-04-01'),
 ( 2,'Bhavin',    1,    1, 145000,'2020-06-15'),
 ( 3,'Chandra',   1,    1, 145000,'2021-01-11'),
 ( 4,'Deepa',     1,    2, 120000,'2022-03-02'),
 ( 5,'Eshan',     2,    1, 132000,'2020-09-21'),
 ( 6,'Farida',    2,    5,  98000,'2023-07-17'),
 ( 7,'Gagan',     2,    5,  98000,'2023-08-01'),
 ( 8,'Hema',      3,    1, 156000,'2018-11-05'),
 ( 9,'Irfan',     3,    8,  87000,'2024-02-19'),
 (10,'Jaya',      3,    8, 210000,'2021-05-30'),
 (11,'Kabir',  NULL,    1,  90000,'2025-01-06'),
 (12,'Lakshmi',   1,    2, 120000,'2024-10-14');

CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, country TEXT, signup_date TEXT);
INSERT INTO customers VALUES
 (1,'Ada','IN','2026-01-03'),(2,'Ben','IN','2026-01-17'),(3,'Cleo','UK','2026-02-02'),
 (4,'Dev','IN','2026-02-11'),(5,'Elif','DE','2026-02-25'),(6,'Fabio','IT','2026-03-04'),
 (7,'Gita','IN','2026-03-19'),(8,'Hugo','UK','2026-03-28');

CREATE TABLE orders (
  id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT,
  amount REAL, status TEXT);
INSERT INTO orders VALUES
 ( 1,1,'2026-01-05', 120.00,'completed'),
 ( 2,1,'2026-01-06',  80.00,'completed'),
 ( 3,1,'2026-01-07',  45.00,'cancelled'),
 ( 4,2,'2026-01-20', 300.00,'completed'),
 ( 5,2,'2026-02-20', 150.00,'completed'),
 ( 6,2,'2026-03-20', 220.00,'completed'),
 ( 7,3,'2026-02-05', 500.00,'completed'),
 ( 8,3,'2026-02-06',  60.00,'refunded'),
 ( 9,4,'2026-02-12',  90.00,'completed'),
 (10,4,'2026-02-13',  90.00,'completed'),
 (11,4,'2026-02-14', 110.00,'completed'),
 (12,4,'2026-02-16',  70.00,'completed'),
 (13,5,'2026-02-26', 410.00,'completed'),
 (14,5,'2026-03-26', 380.00,'completed'),
 (15,6,'2026-03-06', 200.00,'cancelled'),
 (16,7,'2026-03-21',  35.00,'completed'),
 (17,7,'2026-03-22',  35.00,'completed'),
 (18,7,'2026-03-23',  35.00,'completed'),
 (19,7,'2026-03-24',  35.00,'completed'),
 (20,1,'2026-03-01', 640.00,'completed'),
 (21,3,'2026-03-15', 275.00,'completed'),
 (22,2,'2026-03-29',  95.00,'completed'),
 (23,4,'2026-03-30', 130.00,'completed'),
 (24,5,'2026-01-31', 150.00,'completed');

CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL);
INSERT INTO products VALUES
 (1,'keyboard','hardware', 60.0),(2,'mouse','hardware', 25.0),
 (3,'monitor','hardware',220.0),(4,'licence','software',120.0),
 (5,'support','service',  90.0),(6,'cable','hardware',  10.0);

CREATE TABLE order_items (order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO order_items VALUES
 (1,1,1),(1,2,2),(2,4,1),(4,3,1),(4,6,3),(5,5,1),(7,3,2),(7,4,1),
 (9,2,1),(10,2,1),(11,1,1),(13,3,1),(13,4,1),(14,5,1),(20,3,2),(20,4,2),(21,1,3);

CREATE TABLE events (user_id INTEGER, event_name TEXT, ts TEXT);
INSERT INTO events VALUES
 (1,'view','2026-03-01 09:00:00'),(1,'add_to_cart','2026-03-01 09:04:00'),
 (1,'checkout','2026-03-01 09:09:00'),(1,'purchase','2026-03-01 09:12:00'),
 (2,'view','2026-03-01 10:00:00'),(2,'add_to_cart','2026-03-01 10:02:00'),
 (3,'view','2026-03-01 11:00:00'),
 (4,'view','2026-03-01 12:00:00'),(4,'add_to_cart','2026-03-01 12:20:00'),
 (4,'checkout','2026-03-01 12:26:00'),
 (5,'view','2026-03-02 08:00:00'),(5,'checkout','2026-03-02 08:03:00'),
 (5,'add_to_cart','2026-03-02 08:05:00'),(5,'purchase','2026-03-02 08:10:00'),
 (6,'view','2026-03-02 14:00:00'),(6,'add_to_cart','2026-03-02 14:07:00'),
 (6,'checkout','2026-03-02 14:40:00'),(6,'purchase','2026-03-02 14:44:00'),
 (1,'view','2026-03-01 11:30:00'),(1,'view','2026-03-01 11:33:00'),
 (7,'view','2026-03-03 07:15:00'),(7,'add_to_cart','2026-03-03 07:19:00');

CREATE TABLE logins (user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2026-03-01'),(1,'2026-03-02'),(1,'2026-03-03'),(1,'2026-03-07'),(1,'2026-03-08'),
 (2,'2026-03-01'),(2,'2026-03-03'),(2,'2026-03-05'),
 (3,'2026-03-01'),(3,'2026-03-02'),(3,'2026-03-03'),(3,'2026-03-04'),(3,'2026-03-05'),
 (4,'2026-03-10'),
 (5,'2026-03-01'),(5,'2026-03-01'),(5,'2026-03-02'),
 (6,'2026-03-02'),(6,'2026-03-03'),(6,'2026-03-06'),(6,'2026-03-07'),(6,'2026-03-08');

CREATE TABLE subscriptions (user_id INTEGER, plan TEXT, start_date TEXT, end_date TEXT);
INSERT INTO subscriptions VALUES
 (1,'basic','2026-01-01','2026-01-31'),
 (1,'pro',  '2026-01-20','2026-03-15'),
 (1,'pro',  '2026-04-01','2026-05-31'),
 (2,'basic','2026-02-01','2026-02-10'),
 (2,'basic','2026-02-10','2026-02-28'),
 (3,'pro',  '2026-01-05','2026-06-30'),
 (3,'basic','2026-02-01','2026-02-20');

CREATE TABLE salary_history (emp_id INTEGER, salary INTEGER, valid_from TEXT, valid_to TEXT);
INSERT INTO salary_history VALUES
 (2,120000,'2020-06-15','2022-04-01'),
 (2,135000,'2022-04-01','2024-04-01'),
 (2,145000,'2024-04-01','9999-12-31'),
 (5,110000,'2020-09-21','2023-01-01'),
 (5,132000,'2023-01-01','9999-12-31');

CREATE TABLE ab_test (user_id INTEGER, variant TEXT, converted INTEGER, revenue REAL);
INSERT INTO ab_test VALUES
 (1,'control',1, 42.0),(2,'control',0, 0.0),(3,'control',0, 0.0),(4,'control',1, 18.0),
 (5,'control',0, 0.0),(6,'control',0, 0.0),(7,'control',1, 25.0),(8,'control',0, 0.0),
 (9,'control',0, 0.0),(10,'control',0,0.0),
 (11,'treatment',1,55.0),(12,'treatment',1,31.0),(13,'treatment',0,0.0),
 (14,'treatment',1,47.0),(15,'treatment',0,0.0),(16,'treatment',1,22.0),
 (17,'treatment',0,0.0),(18,'treatment',0,0.0),(19,'treatment',1,39.0),
 (20,'treatment',0,0.0);

CREATE TABLE dirty_customers (id INTEGER, email TEXT, name TEXT, created TEXT);
INSERT INTO dirty_customers VALUES
 (1,'ada@x.com','Ada','2026-01-03'),
 (2,'ADA@x.com','Ada L','2026-01-05'),
 (3,' ada@x.com ','ada','2026-01-09'),
 (4,'ben@x.com','Ben','2026-01-17'),
 (5,'ben@x.com','Ben','2026-01-17'),
 (6,'cleo@x.com','Cleo','2026-02-02'),
 (7,NULL,'Unknown','2026-02-03');
"""

# ------------------------------------------------------- the in-browser runtime
SQL_RUNTIME = r"""
<script>
/* ------------------------------------------------------------------------
   Live SQL runtime: sql.js 1.14.2 == SQLite 3.49.1 compiled to WebAssembly.
   Lazy: nothing is fetched until the first Run click. One shared database per
   page, seeded with the demo schema. Nothing leaves the browser.
   ------------------------------------------------------------------------ */
window.SqlRT = (function () {
  var JSURL = "https://cdn.jsdelivr.net/npm/sql.js@1.14.2/dist/sql-wasm.js";
  var BASE  = "https://cdn.jsdelivr.net/npm/sql.js@1.14.2/dist/";
  var SQL = null, db = null, booting = null, cbs = [];
  var SEED = __SEED__;

  function status(s) { cbs.forEach(function (f) { try { f(s); } catch (e) {} }); }

  function loadScript(src) {
    return new Promise(function (res, rej) {
      if (window.initSqlJs) { res(); return; }
      var t = document.createElement("script");
      t.src = src;
      t.onload = function () { res(); };
      t.onerror = function () { rej(new Error("could not reach the CDN to load sql.js")); };
      document.head.appendChild(t);
    });
  }

  function boot() {
    if (db) return Promise.resolve(db);
    if (booting) return booting;
    status("fetching SQLite (~0.7 MB)");
    booting = loadScript(JSURL)
      .then(function () { return window.initSqlJs({ locateFile: function (f) { return BASE + f; } }); })
      .then(function (mod) {
        SQL = mod;
        db = new SQL.Database();
        db.run(SEED);
        status("ready");
        return db;
      })
      .catch(function (e) { booting = null; status("failed"); throw e; });
    return booting;
  }

  function exec(sql) { return boot().then(function (d) { return d.exec(sql); }); }

  function changes() { try { return db.getRowsModified(); } catch (e) { return 0; } }

  function reseed() {
    if (db) { try { db.close(); } catch (e) {} db = null; }
    booting = null;
    return boot();
  }

  function tables() {
    return exec("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
      .then(function (r) { return r.length ? r[0].values.map(function (v) { return v[0]; }) : []; });
  }

  return { boot: boot, exec: exec, reseed: reseed, changes: changes, tables: tables,
           onStatus: function (f) { cbs.push(f); },
           isReady: function () { return !!db; },
           seedSql: function () { return SEED; } };
})();

/* ---------------------------- cell wiring ---------------------------- */
(function () {
  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function cellv(v) {
    if (v === null || v === undefined) return '<span class="snull">NULL</span>';
    if (v instanceof Uint8Array) return '<span class="snull">blob</span>';
    return esc(v);
  }
  var ROWCAP = 200;
  function renderResult(r, idx, many) {
    var h = "";
    if (many) h += '<div class="slabel">result ' + (idx + 1) + '</div>';
    h += '<table class="sqltbl"><thead><tr>';
    r.columns.forEach(function (c) { h += "<th>" + esc(c) + "</th>"; });
    h += "</tr></thead><tbody>";
    r.values.slice(0, ROWCAP).forEach(function (row) {
      h += "<tr>";
      row.forEach(function (v) { h += "<td>" + cellv(v) + "</td>"; });
      h += "</tr>";
    });
    h += "</tbody></table>";
    var n = r.values.length;
    h += '<div class="snote">' + n + (n === 1 ? " row" : " rows") + " &middot; " +
         r.columns.length + (r.columns.length === 1 ? " column" : " columns");
    if (n > ROWCAP) h += " &middot; showing the first " + ROWCAP;
    h += "</div>";
    return h;
  }

  function wire(cell) {
    var ta   = cell.querySelector("textarea");
    var out  = cell.querySelector(".sout");
    var stat = cell.querySelector(".sstat");
    var runB = cell.querySelector(".sbtn.run");
    var rstB = cell.querySelector(".sbtn.reset");
    var schB = cell.querySelector(".sbtn.schema");
    var seedB = cell.querySelector(".sbtn.reseed");
    if (!ta || !out || !runB) return;
    var original = ta.value;

    function grow() { ta.style.height = "auto"; ta.style.height = (ta.scrollHeight + 2) + "px"; }
    grow();
    ta.addEventListener("input", grow);
    ta.addEventListener("keydown", function (e) {
      if (e.key === "Tab") {
        e.preventDefault();
        var s = ta.selectionStart, t = ta.selectionEnd;
        ta.value = ta.value.slice(0, s) + "  " + ta.value.slice(t);
        ta.selectionStart = ta.selectionEnd = s + 2;
      } else if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        go();
      }
    });

    function say(txt, cls) { stat.textContent = txt; stat.className = "sstat" + (cls ? " " + cls : ""); }

    function go() {
      var sql = ta.value;
      runB.disabled = true;
      out.classList.add("show");
      if (!window.SqlRT.isReady()) {
        out.innerHTML = '<span class="odim">starting SQLite in your browser…</span>';
        say("loading", "busy");
      } else {
        say("running", "busy");
      }
      window.SqlRT.exec(sql).then(function (res) {
        if (!res || !res.length) {
          var ch = window.SqlRT.changes();
          out.innerHTML = '<span class="ook">OK</span> <span class="odim">&mdash; statement ran and returned no rows' +
                          (ch ? " (" + ch + " row" + (ch === 1 ? "" : "s") + " changed)" : "") + "</span>";
        } else {
          out.innerHTML = res.map(function (r, i) { return renderResult(r, i, res.length > 1); }).join("");
        }
        say("ok", "ready");
        runB.disabled = false;
      }).catch(function (e) {
        out.innerHTML = '<span class="oerr">' + esc(e && e.message ? e.message : e) + "</span>";
        say("error", "err");
        runB.disabled = false;
      });
    }

    runB.addEventListener("click", go);
    if (rstB) rstB.addEventListener("click", function () {
      ta.value = original; grow(); out.classList.remove("show"); out.innerHTML = ""; say("idle", "");
    });
    if (schB) schB.addEventListener("click", function () {
      out.classList.add("show");
      say("schema", "busy");
      window.SqlRT.exec("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name")
        .then(function (r) {
          var h = '<div class="slabel">tables in this database</div>';
          (r.length ? r[0].values : []).forEach(function (row) {
            h += '<div class="ook">' + esc(row[0]) + "</div><div class=\"snote\">" +
                 esc(String(row[1]).replace(/\s+/g, " ")) + "</div>";
          });
          out.innerHTML = h;
          say("ok", "ready");
        }).catch(function (e) {
          out.innerHTML = '<span class="oerr">' + esc(e.message || e) + "</span>"; say("error", "err");
        });
    });
    if (seedB) seedB.addEventListener("click", function () {
      out.classList.add("show");
      out.innerHTML = '<span class="odim">rebuilding the demo database…</span>';
      say("reseeding", "busy");
      window.SqlRT.reseed().then(function () {
        out.innerHTML = '<span class="ook">OK</span> <span class="odim">&mdash; every table is back to its seeded state</span>';
        say("ok", "ready");
      }).catch(function (e) {
        out.innerHTML = '<span class="oerr">' + esc(e.message || e) + "</span>"; say("error", "err");
      });
    });
  }

  document.querySelectorAll(".sqlrun").forEach(wire);

  document.querySelectorAll(".sbootbtn").forEach(function (b) {
    b.addEventListener("click", function () {
      b.disabled = true;
      var t = b.textContent;
      b.textContent = "starting SQLite…";
      window.SqlRT.boot().then(function () {
        b.textContent = "SQLite is ready — every query on this page will run instantly";
      }).catch(function (e) {
        b.disabled = false;
        b.textContent = t;
        alert("Could not load SQLite: " + (e.message || e) + "\nThe expected output is written under every query, so the page still works.");
      });
    });
  });
})();
</script>
"""
SQL_RUNTIME = SQL_RUNTIME.replace("__SEED__", json.dumps(SEED))

# --------------------------------------------------------------- part registry
P = {}
def part(n, file, title, pk, groups, h1, sub, thesis, chips, prev, prevhref, nxt):
    P[n] = dict(file=file, title=title, pk=pk, groups=groups, h1=h1, sub=sub,
                thesis=thesis, chips=chips, prev=prev, prevhref=prevhref, nxt=nxt)

def chips(level, topics, queries, qa, hours):
    s = ('<span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>%s</b></span>\n'
         '          <span class="chip"><b>%d</b> sections</span>\n') % (level, topics)
    if queries:
        s += '          <span class="chip">▶ <b>%d</b> runnable queries</span>\n' % queries
    s += '          <span class="chip">💬 <b>%d</b> Q&amp;A</span>\n' % qa
    s += '          <span class="chip">⏱ <b>~%s</b></span>' % hours
    return s

def G(pk, head, links): return (pk, head, links)

STAR  = ' <span style="color:var(--gold)">⭐</span>'
STAR2 = ' <span style="color:var(--gold)">⭐⭐</span>'

part(1, "SQL_Part01_WarmUp.html", "The Warm-Up", "L0",
 [G("L0","Warm-Up",[("p1-1","1.1 · The order of execution ⭐⭐"),
   ("p1-2","1.2 · SELECT, WHERE, ORDER BY, LIMIT"),
   ("p1-3","1.3 · The three COUNTs ⭐"),
   ("p1-4","1.4 · GROUP BY properly ⭐"),
   ("p1-5","1.5 · WHERE vs HAVING vs QUALIFY ⭐"),
   ("p1-6","1.6 · NULL and three-valued logic ⭐⭐"),
   ("p1-7","1.7 · NULLs inside aggregates ⭐"),
   ("p1-8","1.8 · COALESCE, NULLIF, safe division"),
   ("p1-9","1.9 · DISTINCT vs GROUP BY"),
   ("p1-10","1.10 · CASE WHEN and conditional aggregation ⭐"),
   ("p1-11","1.11 · UNION, UNION ALL, INTERSECT, EXCEPT")])],
 "The questions you cannot afford to fumble",
 "Logical execution order, the three COUNTs, GROUP BY and HAVING, NULL semantics and three-valued logic, "
 "COALESCE and safe division, conditional aggregation, and UNION versus UNION ALL.",
 "None of this is hard, which is exactly why it is dangerous. A SQL screen almost never fails a candidate on a "
 "window function &mdash; it fails them on <strong>a <code class=\"ic\">COUNT</code> that silently skipped NULLs</strong>, "
 "a <code class=\"ic\">NOT IN</code> that returned nothing, or an alias referenced in <code class=\"ic\">WHERE</code>. "
 "Every topic here is one an interviewer expects you to answer without pausing, and each ends with the questions "
 "actually asked about it. Work this part until the answers are reflexes, because the rest of this subject assumes them.",
 chips("Level 0", 11, 14, 30, "5h"),
 ("Learning Hub","All subjects"), "../index.html",
 ("Part 2 · Joins, and how they go wrong",["The LEFT JOIN + WHERE trap","Anti-joins and NULL"]))

part(2, "SQL_Part02_Joins.html", "Joins, and How They Go Wrong", "L1",
 [G("L1","Joins",[("p2-1","2.1 · The five join types ⭐"),
   ("p2-2","2.2 · The LEFT JOIN + WHERE trap ⭐⭐"),
   ("p2-3","2.3 · Filter in ON vs in WHERE ⭐"),
   ("p2-4","2.4 · Anti-joins, and NOT IN with NULL ⭐⭐"),
   ("p2-5","2.5 · Semi-joins: EXISTS vs IN vs JOIN ⭐"),
   ("p2-6","2.6 · Fan-out: the join that doubles revenue ⭐⭐"),
   ("p2-7","2.7 · Self-joins ⭐"),
   ("p2-8","2.8 · CROSS JOIN, deliberately"),
   ("p2-9","2.9 · Range joins and the as-of join ⭐"),
   ("p2-10","2.10 · Composite-key joins")])],
 "Where most wrong answers actually come from",
 "The five join types stated precisely, the LEFT JOIN that silently becomes an INNER JOIN, ON versus WHERE, "
 "anti-joins three ways and why NOT IN breaks on NULL, row fan-out, self-joins, range joins and as-of joins.",
 "Ask an interviewer where candidates lose SQL rounds and you will hear the same answer: <strong>joins that are "
 "syntactically fine and semantically wrong</strong>. The query runs, returns plausible numbers, and is off by a "
 "factor of two. Three failures account for most of it &mdash; a <code class=\"ic\">WHERE</code> clause quietly "
 "demoting a <code class=\"ic\">LEFT JOIN</code>, a <code class=\"ic\">NOT IN</code> annihilated by a single "
 "<code class=\"ic\">NULL</code>, and a one-to-many join multiplying the rows you then sum. All three are visible "
 "in the demo database on this page, and you can watch each one happen.",
 chips("Level 1", 10, 15, 28, "6h"),
 ("Part 1 · The Warm-Up","Execution order, NULLs, GROUP BY"), "SQL_Part01_WarmUp.html",
 ("Part 3 · Aggregation, subqueries and CTEs",["Correlated subqueries","Recursive CTEs","Pivot without PIVOT"]))

part(3, "SQL_Part03_Aggregation.html", "Aggregation, Subqueries and CTEs", "L2",
 [G("L2","Aggregation &amp; CTEs",[("p3-1","3.1 · Scalar, row and table subqueries"),
   ("p3-2","3.2 · Correlated subqueries and their cost ⭐"),
   ("p3-3","3.3 · CTEs vs subqueries vs temp tables ⭐"),
   ("p3-4","3.4 · Recursive CTEs ⭐"),
   ("p3-5","3.5 · Aggregating an aggregate ⭐"),
   ("p3-6","3.6 · Percent of total and of group ⭐"),
   ("p3-7","3.7 · Pivot without PIVOT ⭐⭐"),
   ("p3-8","3.8 · Unpivot without UNPIVOT"),
   ("p3-9","3.9 · GROUPING SETS, ROLLUP, CUBE"),
   ("p3-10","3.10 · FILTER (WHERE ...) ⭐")])],
 "Composing a query out of parts",
 "Subquery kinds and where each is legal, correlated subqueries and what they cost, CTEs versus subqueries, "
 "recursive CTEs, aggregating an aggregate, percent of total, and pivoting with conditional aggregation.",
 "This is the level where SQL stops being a single statement and becomes <strong>composition</strong>. The skill "
 "being tested is decomposition: can you name the intermediate result you need, build it, and join it back? "
 "Candidates who can do that write readable CTEs and solve hard problems in stages; candidates who cannot write "
 "one enormous nested statement and lose track of it under pressure. The specific thing to have cold is "
 "<strong>conditional aggregation</strong> &mdash; <code class=\"ic\">SUM(CASE WHEN ... )</code> &mdash; because it "
 "is the portable answer to pivoting, funnel counts and per-segment metrics all at once.",
 chips("Level 2", 10, 14, 26, "6h"),
 ("Part 2 · Joins","Fan-out, anti-joins, as-of joins"), "SQL_Part02_Joins.html",
 ("Part 4 · Window functions I",["ROW_NUMBER vs RANK vs DENSE_RANK","Nth highest salary","Top-N per group"]))

part(4, "SQL_Part04_WindowsRanking.html", "Window Functions I: Ranking", "L3",
 [G("L3","Windows I",[("p4-1","4.1 · The anatomy of OVER ⭐⭐"),
   ("p4-2","4.2 · Why a window is not an aggregate ⭐"),
   ("p4-3","4.3 · ROW_NUMBER vs RANK vs DENSE_RANK ⭐⭐"),
   ("p4-4","4.4 · Nth highest salary, four ways ⭐⭐"),
   ("p4-5","4.5 · Top-N per group ⭐⭐"),
   ("p4-6","4.6 · Dedup with ROW_NUMBER ⭐"),
   ("p4-7","4.7 · NTILE and buckets"),
   ("p4-8","4.8 · PERCENT_RANK and CUME_DIST"),
   ("p4-9","4.9 · Windows in WHERE: why it fails ⭐"),
   ("p4-10","4.10 · Deterministic tie-breaks ⭐")])],
 "The single most-tested topic in a SQL screen",
 "The anatomy of OVER, why a window function does not collapse rows, the three ranking functions on real ties, "
 "Nth highest salary four ways, top-N per group, deduplication, NTILE, and why a window function cannot go in WHERE.",
 "If a SQL interview has exactly one hard question, it is a window function, and if it has exactly one <em>trick</em> "
 "question it is <strong>ties</strong>. The demo table on this page has deliberate duplicate salaries, so "
 "<code class=\"ic\">ROW_NUMBER</code>, <code class=\"ic\">RANK</code> and <code class=\"ic\">DENSE_RANK</code> "
 "return visibly different answers and you can see which one the question actually wanted. §4.4 is the canonical "
 "&ldquo;second highest salary&rdquo; problem &mdash; a question so common that the interesting part is no longer "
 "solving it but knowing why <code class=\"ic\">LIMIT 1 OFFSET 1</code> is wrong.",
 chips("Level 3", 10, 16, 30, "7h"),
 ("Part 3 · Aggregation &amp; CTEs","Conditional aggregation, recursion"), "SQL_Part03_Aggregation.html",
 ("Part 5 · Window functions II",["Frames: ROWS vs RANGE","Running totals","LAG, LEAD and growth"]))

part(5, "SQL_Part05_WindowsFrames.html", "Window Functions II: Frames and Offsets", "L4",
 [G("L4","Windows II",[("p5-1","5.1 · The frame clause ⭐⭐"),
   ("p5-2","5.2 · The default frame and its tie bug ⭐⭐"),
   ("p5-3","5.3 · Running totals ⭐"),
   ("p5-4","5.4 · Moving averages ⭐"),
   ("p5-5","5.5 · LAG and LEAD ⭐⭐"),
   ("p5-6","5.6 · Month-over-month and year-over-year ⭐"),
   ("p5-7","5.7 · FIRST_VALUE, LAST_VALUE and the frame bug ⭐"),
   ("p5-8","5.8 · Rolling metrics without leakage ⭐"),
   ("p5-9","5.9 · Named windows"),
   ("p5-10","5.10 · Cumulative distinct count")])],
 "The half of window functions nobody reads about",
 "ROWS versus RANGE versus GROUPS, the default frame and the duplicate-date bug it causes, running totals, "
 "moving averages, LAG and LEAD, period-over-period growth, the LAST_VALUE frame trap, and leakage-free rolling metrics.",
 "Most people learn <code class=\"ic\">OVER (PARTITION BY ... ORDER BY ...)</code> and stop, never learning the "
 "third component. That is a problem, because <strong>the frame is where the silent bugs live</strong>. Adding "
 "<code class=\"ic\">ORDER BY</code> to an aggregate window changes the default frame from the whole partition to "
 "everything up to the current row &mdash; and with <code class=\"ic\">RANGE</code>, &ldquo;up to the current row&rdquo; "
 "includes every <em>tied</em> row, so a running total over a date with two orders jumps by both. "
 "<code class=\"ic\">LAST_VALUE</code> without an explicit frame returns the current row, which looks like a broken "
 "function and is actually the spec. Both are demonstrated here.",
 chips("Level 4", 10, 15, 28, "7h"),
 ("Part 4 · Window functions I","Ranking, top-N, dedup"), "SQL_Part04_WindowsRanking.html",
 ("Part 6 · Dates, times and series",["The date spine","Filling gaps","Rolling actives"]))

part(6, "SQL_Part06_Dates.html", "Dates, Times and Series", "L5",
 [G("L5","Dates &amp; Series",[("p6-1","6.1 · Truncating a date, five dialects ⭐"),
   ("p6-2","6.2 · Date arithmetic and intervals ⭐"),
   ("p6-3","6.3 · Generating a date spine ⭐⭐"),
   ("p6-4","6.4 · Filling gaps in a series ⭐⭐"),
   ("p6-5","6.5 · BETWEEN on timestamps: the last-day bug ⭐⭐"),
   ("p6-6","6.6 · Week boundaries and ISO weeks"),
   ("p6-7","6.7 · Time zones and UTC discipline ⭐"),
   ("p6-8","6.8 · Tenure, age and day differences"),
   ("p6-9","6.9 · Rolling 7-day and 28-day actives ⭐"),
   ("p6-10","6.10 · Point-in-time correctness ⭐⭐")])],
 "Where correct-looking answers quietly lose rows",
 "Date truncation across dialects, interval arithmetic, generating a date spine with a recursive CTE, filling gaps, "
 "the BETWEEN-on-timestamp bug, ISO weeks, time zones, rolling actives, and point-in-time correctness.",
 "Two date bugs are so common that interviewers use them as a filter. The first is "
 "<strong><code class=\"ic\">BETWEEN '2026-03-01' AND '2026-03-31'</code> on a timestamp column</strong>, which "
 "silently drops almost the whole of the 31st, because the implicit time is midnight. The second is "
 "<strong>a missing date spine</strong>: group by day and days with zero activity simply do not appear, so a "
 "line chart interpolates over the outage and a &ldquo;7-day average&rdquo; averages over however many rows "
 "happen to exist. Both are shown here with real rows, and both are fixed the same way &mdash; generate the "
 "calendar first, then left-join the data onto it.",
 chips("Level 5", 10, 15, 26, "6h"),
 ("Part 5 · Window functions II","Frames, offsets, growth"), "SQL_Part05_WindowsFrames.html",
 ("Part 7 · Product analytics patterns",["Funnels","Cohort retention","Sessionisation"]))

part(7, "SQL_Part07_ProductAnalytics.html", "Product Analytics Patterns", "L6",
 [G("L6","Product Analytics",[("p7-1","7.1 · DAU, WAU, MAU and stickiness ⭐"),
   ("p7-2","7.2 · Funnel conversion ⭐⭐"),
   ("p7-3","7.3 · The funnel that must be ordered ⭐⭐"),
   ("p7-4","7.4 · Cohort retention as a triangle ⭐⭐"),
   ("p7-5","7.5 · Day-N retention and the denominator ⭐"),
   ("p7-6","7.6 · New, retained, churned, reactivated ⭐"),
   ("p7-7","7.7 · Sessionisation ⭐⭐"),
   ("p7-8","7.8 · A/B test readout in SQL ⭐"),
   ("p7-9","7.9 · First-touch and last-touch attribution"),
   ("p7-10","7.10 · Co-purchase pairs")])],
 "The questions product companies actually ask",
 "Active-user metrics, funnel conversion and the ordered funnel, cohort retention triangles, day-N retention, "
 "the new/retained/churned/reactivated decomposition, sessionisation, an A/B readout, attribution and basket pairs.",
 "Meta, Amazon, Uber, Stripe and every consumer company built on an event table ask from this list, and they ask "
 "it because the SQL is a proxy for <strong>whether you can define a metric</strong>. &ldquo;What is the conversion "
 "rate?&rdquo; has at least four defensible answers depending on the denominator and on whether the steps must "
 "happen in order &mdash; and the demo event table here deliberately contains a user who checked out "
 "<em>before</em> adding to cart, so the naive funnel and the ordered funnel disagree. Getting the query right is "
 "table stakes; saying which definition you chose and why is the actual answer.",
 chips("Level 6", 10, 16, 30, "8h"),
 ("Part 6 · Dates &amp; series","Spines, gaps, point-in-time"), "SQL_Part06_Dates.html",
 ("Part 8 · Gaps and islands",["The row_number difference","Consecutive days","Longest streak"]))

part(8, "SQL_Part08_GapsIslands.html", "Gaps and Islands", "L7",
 [G("L7","Gaps &amp; Islands",[("p8-1","8.1 · The pattern, and the one trick ⭐⭐"),
   ("p8-2","8.2 · Consecutive days ⭐⭐"),
   ("p8-3","8.3 · Three or more consecutive days ⭐⭐"),
   ("p8-4","8.4 · The longest streak per user ⭐⭐"),
   ("p8-5","8.5 · Current streak vs longest streak ⭐"),
   ("p8-6","8.6 · Islands with a gap tolerance ⭐"),
   ("p8-7","8.7 · Merging overlapping intervals ⭐⭐"),
   ("p8-8","8.8 · Periods where a value held ⭐"),
   ("p8-9","8.9 · Gaps: what is missing"),
   ("p8-10","8.10 · Peak concurrency ⭐")])],
 "One trick, ten questions",
 "The row_number difference that turns a run into a group, consecutive days, the three-day streak, longest and "
 "current streaks, gap tolerance, merging overlapping intervals, unchanged-value periods, and peak concurrency.",
 "This is the family that separates candidates, and it deserves its own level because <strong>every member is the "
 "same two lines of insight</strong>. If a sequence is consecutive, then value minus row-number is constant, so "
 "that difference <em>is</em> a group key. If instead you have a gap rule, flag every row whose predecessor is too "
 "far back and take a running sum of the flags &mdash; the running sum is the island id. Once those two moves are "
 "reflexive, &ldquo;users active three days running&rdquo;, &ldquo;longest login streak&rdquo;, &ldquo;sessionise "
 "these events&rdquo;, &ldquo;merge these subscriptions&rdquo; and &ldquo;how long did the price hold&rdquo; are "
 "all the same question. Recognising that out loud is worth more than any single solution.",
 chips("Level 7", 10, 16, 26, "8h"),
 ("Part 7 · Product analytics","Funnels, retention, sessions"), "SQL_Part07_ProductAnalytics.html",
 ("Part 9 · The hard patterns",["Median without a percentile","Recursive hierarchies","SCD Type 2"]))

part(9, "SQL_Part09_HardPatterns.html", "The Hard Patterns", "L8",
 [G("L8","Hard Patterns",[("p9-1","9.1 · Median without a percentile ⭐⭐"),
   ("p9-2","9.2 · Percentiles, discrete and continuous ⭐"),
   ("p9-3","9.3 · Mode, and ties in the mode"),
   ("p9-4","9.4 · Weighted averages and compressed histograms ⭐"),
   ("p9-5","9.5 · Combinations and pairs ⭐"),
   ("p9-6","9.6 · Recursive hierarchy traversal ⭐⭐"),
   ("p9-7","9.7 · Running maximum and drawdown ⭐"),
   ("p9-8","9.8 · Near-duplicate detection"),
   ("p9-9","9.9 · SCD Type 2 history ⭐⭐"),
   ("p9-10","9.10 · The query you should refuse to write")])],
 "The ones that are genuinely hard",
 "Median and percentiles from first principles, mode with ties, weighted averages over compressed data, "
 "combinations via self-join, recursive hierarchy traversal with path building, drawdown, near-duplicates, "
 "and slowly changing dimensions.",
 "Everything up to here is a pattern you can recognise. This level is where you have to <strong>derive</strong>. "
 "Median without a builtin is the classic: it is not a hard idea, but it forces you to think about even versus odd "
 "counts, about whether you want the discrete or the interpolated value, and about ties &mdash; and the "
 "row-number-from-both-ends solution is genuinely elegant. The other item to have ready is the "
 "<strong>recursive CTE over a hierarchy</strong>, because the employee-manager table on this page is exactly the "
 "shape every interviewer uses, and building the reporting path with it is a three-minute answer that looks like a "
 "twenty-minute one.",
 chips("Level 8", 10, 15, 26, "8h"),
 ("Part 8 · Gaps &amp; islands","Streaks, intervals, concurrency"), "SQL_Part08_GapsIslands.html",
 ("Part 10 · Dirty data and correctness",["Duplicates","Coercion","Assertions"]))

part(10, "SQL_Part10_DirtyData.html", "Dirty Data and Correctness", "L9",
 [G("L9","Dirty Data",[("p10-1","10.1 · Finding duplicates ⭐⭐"),
   ("p10-2","10.2 · Deleting duplicates, keeping one ⭐"),
   ("p10-3","10.3 · Case, whitespace and collation ⭐⭐"),
   ("p10-4","10.4 · Implicit type coercion ⭐"),
   ("p10-5","10.5 · Divide by zero and integer division ⭐"),
   ("p10-6","10.6 · Floating point and money ⭐"),
   ("p10-7","10.7 · Assertions: did the total survive ⭐⭐"),
   ("p10-8","10.8 · Reconciling two sources ⭐"),
   ("p10-9","10.9 · Row-count and ratio checks"),
   ("p10-10","10.10 · Making a query reproducible")])],
 "Correct on clean data is not correct",
 "Defining and finding duplicates, deleting all but one, case-folding and collation, silent type coercion, "
 "integer division and divide-by-zero, money in floating point, assertion queries, reconciliation and "
 "reproducibility.",
 "Interviewers who have shipped anything ask from this level, because it is the difference between a query that "
 "is right and a query that is right <em>on the data you have</em>. Three things recur. "
 "<strong>Duplicates are a definition, not a fact</strong> &mdash; the demo table here has the same customer three "
 "times with different casing and whitespace, so &ldquo;how many customers&rdquo; has three defensible answers. "
 "<strong>Integer division truncates</strong>, so a conversion rate computed as <code class=\"ic\">wins/total</code> "
 "is zero. And <strong>an aggregation should conserve its total</strong> &mdash; the habit of writing an assertion "
 "query after a join is the single most senior-looking thing you can volunteer in a SQL round.",
 chips("Level 9", 10, 15, 24, "6h"),
 ("Part 9 · The hard patterns","Median, recursion, SCD2"), "SQL_Part09_HardPatterns.html",
 ("Part 11 · Performance and engine internals",["EXPLAIN","Indexes","Sargability","Skew"]))

part(11, "SQL_Part11_Performance.html", "Performance and Engine Internals", "L10",
 [G("L10","Performance",[("p11-1","11.1 · Logical order vs physical plan ⭐"),
   ("p11-2","11.2 · Reading an EXPLAIN plan ⭐⭐"),
   ("p11-3","11.3 · Index types ⭐⭐"),
   ("p11-4","11.4 · The leftmost-prefix rule ⭐"),
   ("p11-5","11.5 · Sargability ⭐⭐"),
   ("p11-6","11.6 · When an index hurts ⭐⭐"),
   ("p11-7","11.7 · Join algorithms ⭐"),
   ("p11-8","11.8 · Partitioning and pruning ⭐"),
   ("p11-9","11.9 · Data skew and the straggler ⭐"),
   ("p11-10","11.10 · OLTP vs OLAP, rows vs columns ⭐"),
   ("p11-11","11.11 · Cost on a scanned-bytes engine ⭐"),
   ("p11-12","11.12 · Materialised views and incremental models")])],
 "Why the query is slow, and what you would change",
 "The physical plan behind the logical order, reading EXPLAIN, index types and the leftmost-prefix rule, "
 "sargability, when an index hurts, join algorithms, partition pruning, skew, columnar storage, and "
 "scanned-bytes cost control.",
 "&ldquo;This query takes forty minutes. What do you do?&rdquo; is the most common senior SQL question, and the "
 "answer almost never involves rewriting the SELECT list. What is being tested is whether you have a "
 "<strong>mental model of the engine</strong>: that a function wrapped around an indexed column makes the index "
 "unusable, that an index is a write tax you pay on every insert, that a composite index on "
 "<code class=\"ic\">(a, b)</code> cannot serve a query filtering only on <code class=\"ic\">b</code>, and that on "
 "BigQuery the cost is bytes scanned, so <code class=\"ic\">SELECT *</code> is a line item on an invoice. "
 "You can run <code class=\"ic\">EXPLAIN QUERY PLAN</code> on this page and watch an index change the plan.",
 chips("Level 10", 12, 14, 28, "7h"),
 ("Part 10 · Dirty data","Duplicates, coercion, assertions"), "SQL_Part10_DirtyData.html",
 ("Part 12 · Interview drill",["The trap questions","Timed drills","The dialect cheat sheet"]))

part(12, "SQL_Part12_Drill.html", "Interview Drill &amp; Reference", "QA",
 [G("QA","Drill",[("p12-1","12.1 · How to use this drill"),
   ("p12-2","12.2 · The warm-up questions"),
   ("p12-3","12.3 · Joins and NULLs"),
   ("p12-4","12.4 · Windows and ranking"),
   ("p12-5","12.5 · Dates, funnels and retention"),
   ("p12-6","12.6 · Gaps, islands and hard patterns"),
   ("p12-7","12.7 · Correctness and performance")]),
  G("REF","Practice &amp; Reference",[("p12-8","12.8 · The trap questions ⭐⭐"),
   ("p12-9","12.9 · Timed drills ▶"),
   ("p12-10","12.10 · Free query playground ▶"),
   ("p12-11","12.11 · The dialect cheat sheet ⭐"),
   ("p12-12","12.12 · Clarifying before you write ⭐"),
   ("p12-13","12.13 · The company problem index"),
   ("p12-14","12.14 · One-page pattern reference ⭐")])],
 "The consolidated drill",
 "Every high-frequency question in one shuffled bank, the trap questions answered correctly, timed drills you "
 "type yourself against a live database, a free playground, the dialect cheat sheet, and a one-page pattern reference.",
 "Every part of this subject ends its topics with the questions that topic answers &mdash; this is the "
 "<strong>consolidated drill</strong>, stripped of context so you cannot coast on adjacency. Two sections earn "
 "the most time. <strong>§12.8, the traps</strong>, because SQL screens are lost on a small number of confidently "
 "wrong answers &mdash; &ldquo;<code class=\"ic\">COUNT(*)</code> and <code class=\"ic\">COUNT(col)</code> are the "
 "same&rdquo;, &ldquo;<code class=\"ic\">NOT IN</code> and <code class=\"ic\">NOT EXISTS</code> are "
 "interchangeable&rdquo;, &ldquo;<code class=\"ic\">LIMIT 1 OFFSET 1</code> gives the second highest salary&rdquo;. "
 "And <strong>§12.9</strong>, where the drills run against the real SQLite in your browser, so you type the query "
 "under time pressure instead of reading one.",
 chips("Q&amp;A Bank", 14, 18, 84, "7h drill"),
 ("Part 11 · Performance","EXPLAIN, indexes, skew"), "SQL_Part11_Performance.html",
 ("Learning Hub",["All subjects"]))

# ------------------------------------------------------------------- the build
def build(pn):
    c = P[pn]
    html = SRC.read_text()

    s = html.index("</section>", html.index('id="tracker"')) + len("</section>")
    e = html.index("      <!-- PART NAV -->")
    html = html[:s] + "\n\n<!--CONTENT_INSERT-->\n\n      " + html[e:]

    html = html.replace("<title>RAG Interview Prep — Part 1: Foundations</title>",
                        f"<title>SQL for Data Science — Part {pn}: {re.sub('&amp;','&',c['title'])}</title>")
    html = html.replace('<div class="tt"><small>Part 1 / 6</small>Foundations</div>',
                        f'<div class="tt"><small>Part {pn} / {NP}</small>{c["title"]}</div>')
    html = html.replace('<div class="brand-txt">RAG Prep<small>Knowledge Base</small></div>',
                        '<div class="brand-txt">SQL<small>Data Science Prep</small></div>')
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
           '<li><a href="index.html">← SQL home</a></li></ul>\n      </div>\n    </nav>')
    html = re.sub(r'<nav class="toc" id="toc">.*?</nav>', lambda m: nav, html, count=1, flags=re.DOTALL)

    html = re.sub(r'<div class="sb-foot">.*?</div>',
        f'<div class="sb-foot">\n      SQL for Data Science<br>Part {pn} — {c["title"]}<br>© your study kit\n    </div>',
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
      f'<div class="doc-foot">\n        SQL for Data Science Interviews — Part {pn} of {NP} · {c["title"]}<br>\n'
      f'        Runnable queries execute <b>real SQLite 3.49</b> in your browser via sql.js (SQLite compiled to '
      f'WebAssembly) — nothing is sent to a server.<br>\n'
      f'        Answers are written in portable SQL; dialect differences are called out where they matter — see the '
      f'cheat sheet in <a href="SQL_Part12_Drill.html#p12-11" style="color:#8892a0">§12.11</a>.<br>\n'
      f'        Progress is stored locally under key <code style="color:#8892a0">sqlPrepStatus_v1</code> and is shared by every part of this subject.\n      </div>',
      html, count=1, flags=re.DOTALL)

    _ph = "const PHASES = " + json.dumps(PHASES, ensure_ascii=False) + ";"
    _or = "const ORDER = " + json.dumps(ORDER) + ";"
    _tk = "const TRACKER = " + tracker_js + ";"
    html = re.sub(r'const PHASES = \{.*?\};', lambda m: _ph, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const ORDER = \[.*?\];', lambda m: _or, html, count=1, flags=re.DOTALL)
    html = re.sub(r'const TRACKER = \[.*?\n\];', lambda m: _tk, html, count=1, flags=re.DOTALL)
    html = html.replace('const LS_KEY="ragPrepStatus_v1";', 'const LS_KEY="sqlPrepStatus_v1";')
    html = html.replace("206", str(TOTAL))
    html = re.sub(r'<p class="tk-sub">.*?</p>',
      f'<p class="tk-sub">One tracker for the whole SQL subject — all {TOTAL} topics across all {NP} parts, ordered '
      f'easy to hard. Set a status on any row; your progress saves in this browser and prints as a clean checklist.</p>',
      html, count=1, flags=re.DOTALL)

    html = html.replace("</style>", WIDGET_CSS + "</style>", 1)
    html = html.replace("</body>", SQL_RUNTIME + "\n</body>", 1)

    (HERE / c["file"]).write_text(html)
    assert "<!--CONTENT_INSERT-->" in html and "ragPrepStatus" not in html and "window.SqlRT" in html
    print(f"  wrote {c['file']} ({len(html):,} bytes)")

if __name__ == "__main__":
    for p in ([int(a) for a in sys.argv[1:]] or P):
        build(p)
