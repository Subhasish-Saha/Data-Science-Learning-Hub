#!/usr/bin/env python3
"""Stitch all 12 SQL part files into one print/PDF-ready SQL_Complete.html.
Reuses Part 1's head/CSS/tracker/script (including the sql.js runtime block);
concatenates each part's content with a part divider; builds a combined sidebar
nav. Re-run after editing any part."""
import re, pathlib

OUT = pathlib.Path(__file__).resolve().parent      # run from the sql/ folder
NP  = 12
PARTS = [
    ("SQL_Part01_WarmUp.html", "The Warm-Up",
     "Execution order, the three COUNTs, GROUP BY, NULL semantics, conditional aggregation, set operators"),
    ("SQL_Part02_Joins.html", "Joins, and How They Go Wrong",
     "The five joins, the LEFT JOIN + WHERE trap, anti-joins and NULL, fan-out, self-joins, as-of joins"),
    ("SQL_Part03_Aggregation.html", "Aggregation, Subqueries and CTEs",
     "Subquery shapes, correlated subqueries, CTEs, recursion, percent of total, pivot without PIVOT"),
    ("SQL_Part04_WindowsRanking.html", "Window Functions I: Ranking",
     "OVER anatomy, ROW_NUMBER vs RANK vs DENSE_RANK, Nth highest, top-N per group, dedup, tie-breaks"),
    ("SQL_Part05_WindowsFrames.html", "Window Functions II: Frames and Offsets",
     "ROWS vs RANGE, the default frame, running totals, moving averages, LAG/LEAD, leakage-free windows"),
    ("SQL_Part06_Dates.html", "Dates, Times and Series",
     "Truncation by dialect, the date spine, gap filling, the BETWEEN bug, time zones, point-in-time"),
    ("SQL_Part07_ProductAnalytics.html", "Product Analytics Patterns",
     "DAU/MAU, funnels ordered in time, cohort retention, sessionisation, A/B readout, attribution"),
    ("SQL_Part08_GapsIslands.html", "Gaps and Islands",
     "The row_number difference, consecutive days, streaks, gap tolerance, interval merging, concurrency"),
    ("SQL_Part09_HardPatterns.html", "The Hard Patterns",
     "Median and percentiles, mode, weighted averages, combinations, recursive hierarchies, SCD Type 2"),
    ("SQL_Part10_DirtyData.html", "Dirty Data and Correctness",
     "Duplicates, collation, coercion, integer division, money in floats, assertions, reconciliation"),
    ("SQL_Part11_Performance.html", "Performance and Engine Internals",
     "EXPLAIN, index types, leftmost prefix, sargability, when indexes hurt, joins, skew, columnar"),
    ("SQL_Part12_Drill.html", "Interview Drill &amp; Reference",
     "The consolidated bank, 14 trap questions, 8 timed drills, a playground, dialect and pattern sheets"),
]

def read(fn): return (OUT / fn).read_text()

def content_of(html):
    s = html.index("</section>", html.index('id="tracker"')) + len("</section>")
    e = html.index("      <!-- PART NAV -->")
    return html[s:e].strip("\n")

def nav_grps(html, skip_tracker=True):
    nav = re.search(r'<nav class="toc" id="toc">(.*?)</nav>', html, re.DOTALL).group(1)
    grps = re.findall(r'<div class="grp">.*?</div>', nav, re.DOTALL)
    return grps[1:] if skip_tracker else grps

p1 = read(PARTS[0][0])

top    = p1[: p1.index("</section>", p1.index('id="tracker"')) + len("</section>")]
bottom = p1[p1.index('<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js'):]

top = top.replace("<title>SQL for Data Science — Part 1: The Warm-Up</title>",
                  "<title>SQL for Data Science — Complete (All 12 Parts)</title>")
top = top.replace('<div class="tt"><small>Part 1 / 12</small>The Warm-Up</div>',
                  '<div class="tt"><small>Complete</small>All 12 Parts</div>')
top = top.replace('<div class="k">Part 1 of 12</div>\n      <div class="v">The Warm-Up</div>',
                  '<div class="k">Complete edition</div>\n      <div class="v">All 12 Parts</div>')

new_hero = ('<header class="hero">\n'
  '        <div class="eyebrow">Complete Resource · All 12 Parts · easy to hard</div>\n'
  '        <h1 class="title">SQL for data science interviews, end to end\n'
  '          <span class="sub">The full curriculum in one document, ordered strictly by difficulty — the warm-up '
  'questions, joins and their traps, aggregation and CTEs, both halves of window functions, dates and series, '
  'product-analytics patterns, gaps and islands, the hard patterns, dirty data, performance internals, and a '
  'consolidated interview drill.</span>\n'
  '        </h1>\n'
  '        <p class="thesis">This is the stitched edition of all twelve parts, print- and PDF-ready. The master tracker '
  'below covers every one of the 119 topics across 127 sections; your progress is shared with the individual part files '
  '(same browser). The <b>110 runnable queries</b> execute <b>real SQLite 3.49</b> in your browser via sql.js — SQLite '
  'compiled to WebAssembly — against a seeded 12-table demo database, and they work in this combined file too. Nothing '
  'is sent to a server. Answers are written in portable SQL with dialect differences called out; the cheat sheet is in '
  '§12.11. Use the sidebar to jump to any part or section.</p>\n'
  '        <div class="meta-chips">\n'
  '          <span class="chip"><span class="dot" style="background:var(--indigo)"></span><b>12 parts</b> · 11 levels</span>\n'
  '          <span class="chip"><b>127</b> sections · <b>119</b> tracked topics</span>\n'
  '          <span class="chip">▶ <b>110</b> runnable queries</span>\n'
  '          <span class="chip">💬 <b>221</b> Q&amp;A + 14 traps</span>\n'
  '          <span class="chip">🗄 SQLite <b>3.49</b> in-browser</span>\n'
  '        </div>\n'
  '      </header>')
top = re.sub(r'<header class="hero">.*?</header>', lambda m: new_hero, top, count=1, flags=re.DOTALL)

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
combined_nav = ('<nav class="toc" id="toc">\n      ' + tracker_grp + '\n' + jump + all_grps + '    </nav>')
top = re.sub(r'<nav class="toc" id="toc">.*?</nav>', lambda m: combined_nav, top, count=1, flags=re.DOTALL)

def divider(i, title, sub):
    return ('\n      <div class="part-divider" id="part%d">\n'
            '        <div class="pdk">Part %d of %d</div>\n'
            '        <div class="pdt">%s</div>\n'
            '        <div class="pds">%s</div>\n'
            '      </div>\n') % (i, i, NP, title, sub)

body = ""
for i, (fn, title, sub) in enumerate(PARTS, start=1):
    body += divider(i, title, sub) + "\n" + content_of(read(fn)) + "\n"

foot = ('\n      <div class="doc-foot">\n'
  '        SQL for Data Science Interviews — <b>Complete edition</b> · all 12 parts · 127 sections · '
  '119 tracked topics · 110 runnable queries · 221 Q&amp;A.<br>\n'
  '        Runnable queries execute <b>real SQLite 3.49</b> in your browser via sql.js against a seeded 12-table '
  'database; nothing is uploaded.<br>\n'
  '        Answers are portable SQL; dialect differences are called out where they matter — see the cheat sheet in '
  '<a href="SQL_Part12_Drill.html#p12-11" style="color:#8892a0">§12.11</a>.<br>\n'
  '        Progress is stored locally under key <code style="color:#8892a0">sqlPrepStatus_v1</code>, shared with every part file.<br>\n'
  '        Regenerate this file after editing any part with: '
  '<code style="color:#8892a0">python3 stitch_sql.py</code> · '
  '<a href="../index.html" style="color:#8892a0">← Learning Hub</a>\n'
  '      </div>\n')

divider_css = ('\n.part-divider{margin:80px 0 10px;padding:26px 28px;border-radius:16px;'
  'background:linear-gradient(135deg,#161b23,#252d3a);border:1px solid #2c3542;color:#fff;'
  'scroll-margin-top:20px;box-shadow:var(--shadow)}\n'
  '.part-divider .pdk{font-family:var(--mono);font-size:12px;letter-spacing:2.4px;'
  'text-transform:uppercase;color:var(--gold-2)}\n'
  '.part-divider .pdt{font-family:var(--disp);font-weight:700;font-size:2rem;letter-spacing:-.6px;margin:6px 0 4px}\n'
  '.part-divider .pds{color:#aeb7c4;font-size:1rem}\n'
  '@media print{.part-divider{break-before:page;page-break-before:always}}\n')
top = top.replace("</style>", divider_css + "</style>", 1)

close = '\n    </div>\n  </main>\n</div>\n\n'
complete = top + "\n" + body + foot + close + bottom
(OUT / "SQL_Complete.html").write_text(complete)
print("wrote SQL_Complete.html", "{:,} bytes".format(len(complete)))
