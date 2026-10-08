#!/usr/bin/env python3
"""Print the full text and every fetched source of ranked X posts, by id.

Usage: .venv/bin/python connectors/twitter/show_post.py <id> [<id> ...] [--date YYYY-MM-DD] [--max N]
--max caps each source at N characters (default: no cap). Bookmarks are searched too.
"""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
args = sys.argv[1:]
date = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d")
cap = None
if "--date" in args:
    date = args[args.index("--date") + 1]
if "--max" in args:
    cap = int(args[args.index("--max") + 1])
ids = [a for a in args if a.isdigit() and len(a) > 10]

posts = {}
f = ROOT / "raw" / "twitter" / "feed" / f"{date}-day-ranked.json"
if f.exists():
    for s in json.loads(f.read_text())["candidates"]:
        posts[s["id"]] = s
for b in (ROOT / "raw" / "twitter" / "bookmarks").glob("*.json"):
    d = json.loads(b.read_text())
    for t in (d if isinstance(d, list) else d.get("bookmarks", [])):
        tid = t.get("tweet_id") or (t.get("link") or "").rsplit("/", 1)[-1]
        posts.setdefault(tid, t)

for i in ids:
    p = posts.get(i)
    if not p:
        print(f"=== {i}: not found for {date}\n")
        continue
    via = f" (reposted by @{p['reposted_by']})" if p.get("reposted_by") else ""
    print(f"=== @{p.get('handle')}{via} | {p.get('link')}")
    print(p.get("text") or "")
    for u in p.get("image_urls") or []:
        print(f"[image] {u}")
    for path in p.get("image_paths") or []:
        print(f"[image file, view with the Read tool] {path}")
    for a in p.get("articles") or []:
        c = a.get("content") or ""
        print(f"\n--- source: {a.get('url')} ({len(c)} chars)")
        print(c[:cap] if cap else c)
    print()
