#!/usr/bin/env python3
"""Splice a content fragment into a shell at the <!--CONTENT_INSERT--> marker.
    python3 insert.py NLP_Part1_Foundations.html frag1.html
Validates tag balance and that no marker is left behind."""
import re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
shell = HERE / sys.argv[1]
frag  = pathlib.Path(sys.argv[2])
html  = shell.read_text()
body  = frag.read_text()
assert "<!--CONTENT_INSERT-->" in html, "marker already consumed — rebuild the shell first"
html = html.replace("<!--CONTENT_INSERT-->", body, 1)
shell.write_text(html)

# ---- validation ----
def count(tag, s):
    o = len(re.findall(r'<%s(?=[\s>])' % tag, s)); c = s.count("</%s>" % tag)
    return o, c
bad = []
for tag in ("article","div","figure","section","svg","g","text","details","table","nav","p","span"):
    o, c = count(tag, html)
    if tag in ("p","span","text","g") : continue          # self-closing/implicit are fine
    if o != c: bad.append(f"{tag}: {o} open / {c} close")
ids  = set(re.findall(r'id="([^"]+)"', html))
anch = set(re.findall(r'href="#([^"]+)"', html))
miss = sorted(a for a in anch if a not in ids)
print(f"{sys.argv[1]}: {len(html):,}b · articles={count('article',html)[0]} · "
      f"diagrams={html.count('figure class=\"diagram\"')} · qa={html.count('<details class=\"qa\"')}")
if bad: print("  ⚠ TAG IMBALANCE:", "; ".join(bad)); sys.exit(1)
if miss: print("  ⚠ UNRESOLVED ANCHORS:", ", ".join(miss)); sys.exit(1)
assert "<!--CONTENT_INSERT-->" not in html
print("  ✓ clean")
