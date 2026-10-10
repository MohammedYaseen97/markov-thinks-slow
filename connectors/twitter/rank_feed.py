#!/usr/bin/env python3
"""
Feed pre-ranker for the social-media agent.

Reads the PRIVATE captured X home feed (raw/twitter/feed/<date>-*.json) and scores
every post, so the downstream synthesis (the LLM) applies judgment to a small,
pre-scored candidate set instead of the whole feed. This is deterministic
EVIDENCE, not the verdict: the synthesis makes the final call.

What a post is scored on:
  - SUBSTANCE, not the wrapper. Topic fit is judged on the post text (which already
    holds the original of a repost and the quoted post) PLUS the linked article,
    X Article or linked post the farmer fetched.
  - TOPICS come from wiki-config.json (one source of truth with the wiki and the
    site). A topic matches on one specific term, or on two different generic ones:
    a lone generic word ("architecture", "PPO", "agent") is not a match.
  - CONVERGENCE. Several accounts the reader follows reposting, quoting or linking
    the same thing is the strongest "this matters" signal the feed carries.
  - AFFINITY. Authors the reader has bookmarked or reposted before rank higher, so
    saving a post teaches the ranker instead of being needed every time.
  - PRIORITY accounts (config.json:priority_handles) always surface.
  - Engagement rate (eng / views), velocity, artifact links: supporting evidence.
  - Grift, promotion and off-topic patterns are pushed down hard.

The gate: a post is a candidate only if it has a real reason to be read (topic
match, priority account, convergence, or a known-good author). Engagement alone
never qualifies. Everything else is counted and dropped, not deleted from raw.

Run:  python3 connectors/twitter/rank_feed.py [YYYY-MM-DD]
"""

import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FEED_DIR = ROOT / "raw" / "twitter" / "feed"
BOOKMARK_DIR = ROOT / "raw" / "twitter" / "bookmarks"
CURATED_DIR = ROOT / "raw" / "twitter"
CONV_STATE = HERE / ".state" / "convergence.json"

try:
    CFG = json.loads((HERE / "config.json").read_text())
except Exception:
    CFG = {}
PRIORITY = {h.lower() for h in CFG.get("priority_handles", [])}

# ── Topics (from wiki-config.json) ─────────────────────────────────────────────
# A keyword is SPECIFIC if it is a phrase, hyphenated, or on the list below;
# otherwise it is generic and needs a second, different generic hit to count.
SPECIFIC_SINGLE = {
    "jev", "jepa", "rlhf", "rlvr", "grpo", "rlcd", "openenv", "lossfunk", "mamba",
    "neuroscience", "kahneman", "tversky", "abducti", "harness", "harnesses", "rollout", "looped", "midtraining", "opsd", "posttrain", "reinforce", "plasticity", "compaction", "quantization",
    "quantis", "distill", "pretraining", "finetun", "flashattention",
    "pagedattention", "vllm", "dopamine", "metacognition", "neurosymbolic",
    "compositionality", "deepspeed", "peft", "gymnasium", "neuroeconomics",
    "prefrontal", "interpretability", "multimodal", "sycophancy", "jailbreak",
    "deepmind", "anthropic", "openai", "huggingface", "nvidia", "gguf", "tensorrt",
    "brier", "orchestrat", "agentic", "subagent",
}


def _load_topics():
    topics = []
    try:
        for t in json.loads((ROOT / "wiki-config.json").read_text()).get("topics", []):
            kws = []
            for k in t.get("keywords", []):
                k = k.lower().strip()
                specific = (" " in k) or ("-" in k) or (k in SPECIFIC_SINGLE)
                pat = re.escape(k)
                if re.match(r"\w", k):
                    pat = r"\b" + pat          # never match inside another word
                if len(k) <= 4:
                    pat += r"\b"
                kws.append((re.compile(pat), k, specific))
            topics.append({"key": t["key"], "tier": t.get("tier", 4), "kws": kws})
    except Exception as e:
        print(f"  WARN: could not load topics from wiki-config.json: {e}")
    return topics


TOPICS = _load_topics()
TIER_POINTS = {1: 40, 2: 26, 3: 8}

# ── Low-signal patterns ────────────────────────────────────────────────────────
GRIFT = [
    r"print money", r"while you sleep", r"passive income", r"\bmoney\b.*\bsleep\b",
    r"\d+\s+(github\s+)?repos?\s+(that|you)", r"here'?s what i (learned|discovered)",
    r"steal my", r"\bhack\b.*\bproductiv", r"changed my life", r"you'?re doing .* wrong",
    r"nobody (is )?talking about", r"before it'?s too late", r"blow(s)? your account",
    r"position siz", r"\bcrypto\b", r"\baltcoin\b", r"\bwatch this\b", r"thread\s*🧵",
    r"follow me", r"drop a (comment|like)", r"bookmark this", r"\bgiveaway\b",
]
OFFTOPIC = [r"\btrading\b", r"\bforex\b", r"\bstocks?\b.*\bportfolio\b",
            r"weight loss", r"\bdiet\b", r"real estate", r"dropship"]
# Selling something: books, courses, job-board round-ups.
PROMO_URL = re.compile(r"amzn\.to|amazon\.|link\.amazon|packtpub|manning\.com|gumroad|udemy", re.I)
PROMO_TEXT = [r"\bavailable at\b", r"\buse (the )?code\b", r"\b\d+% off\b", r"\benroll now\b",
              r"\bstipend\b", r"\bis hiring\b.*\bapply\b", r"\bapply here\b"]
ARTIFACT_URL = re.compile(r"arxiv\.org|alphaxiv\.org|github\.com|huggingface\.co|hf\.space|openreview\.net|/abs/|\.pdf", re.I)


def _count(text, patterns):
    return sum(1 for p in patterns if re.search(p, text))


def _hours_since(iso):
    if not iso:
        return 24.0
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return max(0.5, (datetime.now(timezone.utc) - dt).total_seconds() / 3600.0)
    except Exception:
        return 24.0


def _readable(content: str) -> str:
    """Linked content worth scoring: skip binary PDF dumps."""
    c = content or ""
    return "" if c.startswith("%PDF") else c


def topic_match(text: str, linked: str):
    """Return (tier, [topic keys], strength). Text hits count fully; hits found only
    in linked content need several distinct terms (page chrome is full of stray words)."""
    best_tier, keys, strength = 4, [], 0.0
    for t in TOPICS:
        t_spec = t_gen = l_hits = 0
        for pat, _k, specific in t["kws"]:
            if pat.search(text):
                if specific:
                    t_spec += 1
                else:
                    t_gen += 1
            elif linked and pat.search(linked):
                l_hits += 1
        matched = t_spec >= 1 or t_gen >= 2 or (t_gen == 1 and l_hits >= 1) or l_hits >= 3
        if matched:
            keys.append(t["key"])
            s = t_spec * 1.0 + t_gen * 0.5 + min(l_hits, 6) * 0.5
            if t["tier"] < best_tier or (t["tier"] == best_tier and s > strength):
                best_tier, strength = t["tier"], s
    return best_tier, keys, strength


# ── Convergence: who else pointed at the same thing ────────────────────────────
def _norm_url(u: str) -> str:
    u = (u or "").lower().split("#")[0].split("?")[0].rstrip("/")
    u = re.sub(r"^https?://(www\.)?", "", u)
    m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", u)
    if m:
        return "arxiv:" + m.group(1)
    m = re.search(r"github\.com/([^/]+/[^/]+)", u)
    if m:
        return "github:" + m.group(1)
    return u


def _post_id(link: str) -> str:
    m = re.search(r"/status/(\d+)", link or "")
    return m.group(1) if m else ""


def _keys_for(p) -> set:
    keys = set()
    pid = p.get("tweet_id") or _post_id(p.get("link"))
    if pid:
        keys.add("x:" + pid)
    qid = _post_id(p.get("quoted_link"))
    if qid:
        keys.add("x:" + qid)
    for u in p.get("urls") or []:
        n = _norm_url(u)
        if n and not PROMO_URL.search(n):
            keys.add("u:" + n)
    return keys


def build_convergence(all_posts) -> dict:
    """key -> set of distinct accounts that posted, reposted, quoted or linked it.
    Accounts that flood the feed (auto-reposters) are not counted: their repost is
    not a signal."""
    volume = defaultdict(int)
    for p in all_posts:
        volume[(p.get("reposted_by") or p.get("handle") or "").lower()] += 1
    limit = max(40, int(0.05 * len(all_posts)))
    flooders = {h for h, n in volume.items() if n > limit}
    idx = defaultdict(set)
    for p in all_posts:
        accounts = {(p.get("handle") or "").lower(), (p.get("reposted_by") or "").lower()}
        accounts |= {r.lower() for r in p.get("reposters") or []}
        accounts = {a for a in accounts if a and a not in flooders}
        for k in _keys_for(p):
            idx[k] |= accounts
    try:   # reposters the farmer saw across earlier captures
        for tid, reps in json.loads(CONV_STATE.read_text()).items():
            idx["x:" + tid] |= {r.lower() for r in reps if r.lower() not in flooders}
    except Exception:
        pass
    return idx


# ── Affinity: authors the reader has saved or reposted before ──────────────────
def build_affinity(exclude_ids=()) -> dict:
    aff = defaultdict(int)

    def add(t):
        if (t.get("tweet_id") or _post_id(t.get("link"))) in exclude_ids:
            return
        h = (t.get("handle") or "").lower()
        if h:
            aff[h] += 1
        m = re.search(r"\[Quoting @(\w+):", t.get("text") or "")
        if m and m.group(1).lower() != h:
            aff[m.group(1).lower()] += 1

    for f in list(BOOKMARK_DIR.glob("*.json")) + list(CURATED_DIR.glob("*.json")):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        items = d if isinstance(d, list) else (d.get("bookmarks") or d.get("own_curated") or d.get("curated") or [])
        for t in items:
            if isinstance(t, dict):
                add(t)
    return aff


# ── Scoring ────────────────────────────────────────────────────────────────────
def score_post(p, conv=None, affinity=None):
    e = p.get("engagement", {})
    likes, rts = e.get("likes", 0), e.get("retweets", 0)
    replies, quotes = e.get("replies", 0), e.get("quotes", 0)
    views = max(e.get("views", 0), 1)
    text = p.get("text", "") or ""
    urls = p.get("urls", []) or []
    arts = [a for a in (p.get("articles") or []) if _readable(a.get("content"))]
    linked = " ".join(a["content"][:6000] for a in arts).lower()
    low = text.lower()

    eng = likes + 2.0 * rts + 1.5 * quotes + 0.5 * replies
    eng_rate = eng / views if e.get("views", 0) else 0.0     # no view count -> no rate
    velocity = eng / _hours_since(p.get("date_utc"))
    controversy = replies > max(likes, 1) * 0.6 and replies > 15

    tier, topics, strength = topic_match(low, linked)
    grift = _count(low, GRIFT)
    promo = bool(any(PROMO_URL.search(u) for u in urls)) or _count(low, PROMO_TEXT) > 0
    offtopic = _count(low, OFFTOPIC) > 0
    has_artifact = (not promo) and any(ARTIFACT_URL.search(u) for u in urls)
    src_chars = sum(len(a["content"]) for a in arts)
    substance = src_chars >= 1500
    x_article = any(a["content"].startswith("[X Article]") for a in arts)

    handle = (p.get("handle") or "").lstrip("@").lower()
    reposter = (p.get("reposted_by") or "").lstrip("@").lower()
    priority = bool({handle, reposter} & PRIORITY)
    accounts = set()
    for k in _keys_for(p):
        accounts |= (conv or {}).get(k, set())
    n_conv = len(accounts)
    aff = (affinity or {}).get(handle, 0)

    score = 0.0
    score += TIER_POINTS.get(tier, 0) + min(strength, 4) * 3      # topic fit dominates
    score += min(eng_rate * 4000, 20)                              # reach-normalised engagement
    score += min(velocity / 50, 8)                                 # rising signal
    score += 12 if has_artifact else 0                             # a paper, repo or write-up
    score += (12 if src_chars >= 5000 else 6) if substance else 0  # the linked source was read
    score += 6 if x_article else 0                                 # a full article, not a link
    score += min(8 * max(n_conv - 1, 0), 24)                       # convergence
    score += min(8 * aff, 20)                                      # author the reader has saved
    score -= grift * 18
    score -= 25 if promo else 0
    score -= 8 if controversy else 0
    if offtopic:
        score -= 100
    if priority:
        score = max(score, 0) + 30
        offtopic = False

    # The gate: a real reason to read it. Engagement alone never qualifies.
    on_topic = tier <= 2 and not promo and grift == 0
    reason_to_read = (priority or on_topic
                      or (n_conv >= 3 and tier <= 3 and not promo)
                      or (aff >= 1 and tier <= 3 and not promo))
    candidate = reason_to_read and not offtopic and (priority or score >= 30)

    reasons = []
    if priority: reasons.append("PRIORITY-ACCOUNT")
    if tier <= 3: reasons.append(f"tier{tier}")
    if n_conv >= 2: reasons.append(f"converged×{n_conv}")
    if aff: reasons.append(f"saved-author×{aff}")
    if has_artifact: reasons.append("artifact")
    if substance: reasons.append("source-read")
    if eng_rate > 0.005: reasons.append(f"eng-rate {eng_rate*100:.1f}%")
    if velocity > 200: reasons.append("rising")
    if controversy: reasons.append("CONTESTED")
    if grift: reasons.append(f"grift×{grift}")
    if promo: reasons.append("PROMO")
    if offtopic: reasons.append("OFF-TOPIC")

    return {
        "handle": p.get("handle"), "link": p.get("link"), "text": text,
        "is_retweet": p.get("is_retweet", False), "reposted_by": p.get("reposted_by", ""),
        "quoted_link": p.get("quoted_link", ""),
        "tier": tier, "topics": topics, "score": round(score, 1), "candidate": candidate,
        "convergence": n_conv, "converged_accounts": sorted(accounts)[:8], "affinity": aff,
        "eng": {"likes": likes, "rts": rts, "replies": replies, "quotes": quotes, "views": e.get("views", 0)},
        "eng_rate_pct": round(eng_rate * 100, 2), "velocity": round(velocity, 1),
        "has_artifact": has_artifact, "controversy": controversy,
        "grift": grift, "promo": promo, "offtopic": offtopic, "urls": urls,
        "image_urls": p.get("image_urls", []),
        "articles": [a for a in (p.get("articles") or []) if a.get("content")],
        "reasons": reasons,
    }


def _load_posts(path: Path) -> list:
    try:
        return json.loads(path.read_text()).get("posts", [])
    except Exception:
        return []


def _rank_one(path: Path, conv, affinity) -> int:
    """Rank a single feed file -> its <name>-ranked.json. Returns candidate count."""
    data = json.loads(path.read_text())
    scored = [score_post(p, conv, affinity) for p in data.get("posts", [])]
    scored.sort(key=lambda x: x["score"], reverse=True)
    candidates = [s for s in scored if s["candidate"]]
    long_tail = [s for s in scored if not s["candidate"] and s["tier"] <= 2 and not s["offtopic"]]
    out = {"date": data.get("date"), "slot": data.get("slot"), "source_file": path.name,
           "total": len(scored), "candidates": candidates, "long_tail": long_tail[:40]}
    path.with_name(path.stem + "-ranked.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"Ranked {len(scored)} posts from {path.name}: {len(candidates)} candidates, "
          f"{len(long_tail)} long-tail, {len(scored) - len(candidates) - len(long_tail)} dropped")
    return len(candidates)


def feed_files_for(date: str, days_back: int = 0) -> list:
    d0 = datetime.strptime(date, "%Y-%m-%d")
    files = []
    for i in range(days_back + 1):
        day = (d0 - timedelta(days=i)).strftime("%Y-%m-%d")
        files += [p for p in sorted(FEED_DIR.glob(f"{day}-*.json")) if not p.stem.endswith("-ranked")]
    return files


INDEX_TOP = 200


def write_day_union(date, files, conv, affinity):
    """One ranked list for the whole day: every capture unioned, each post once.
    Writes <date>-day-ranked.json (full records) and <date>-day-index.md (a compact
    list the write-up reads first; full posts via show_post.py)."""
    best = {}
    for f in files:
        for p in _load_posts(f):
            text = p.get("text") or ""
            if re.match(r"RT @\w+: ", text):
                continue   # cut-off repost stub from an old capture; the original is captured separately
            pid = p.get("tweet_id") or _post_id(p.get("link"))
            if not pid:
                continue
            old = best.get(pid)
            size = len(text) + sum(len(a.get("content") or "") for a in p.get("articles") or [])
            if old is None or size > old[0]:
                best[pid] = (size, p)
    scored = []
    for pid, (_, p) in best.items():
        s = score_post(p, conv, affinity)
        s["id"] = pid
        s["date_utc"] = p.get("date_utc")
        scored.append(s)
    scored.sort(key=lambda x: x["score"], reverse=True)
    cands = [s for s in scored if s["candidate"]]
    (FEED_DIR / f"{date}-day-ranked.json").write_text(json.dumps(
        {"date": date, "total_posts": len(scored), "candidates": cands}, indent=1, ensure_ascii=False))
    lines = [f"# X feed, ranked | {date}",
             f"> {len(scored)} distinct posts captured, {len(cands)} candidates. Top {min(INDEX_TOP, len(cands))} listed. "
             "PRIVATE, gitignored. Full text and sources of any post: "
             "`.venv/bin/python connectors/twitter/show_post.py <id> [<id> ...]`", ""]
    for i, s in enumerate(cands[:INDEX_TOP], 1):
        via = f" (reposted by @{s['reposted_by']})" if s.get("reposted_by") else ""
        srcs = "; ".join(f"{a['url']} ({len(a['content'])} chars)" for a in s["articles"][:4]) or "none read"
        lines += [f"## {i}. @{s['handle']}{via} | score {s['score']} | id {s['id']}",
                  f"topics: {', '.join(s['topics']) or '-'} | why: {', '.join(s['reasons'])}",
                  f"> {s['text'][:480]}",
                  f"link: {s['link']} | images: {len(s.get('image_urls') or [])} | sources: {srcs}", ""]
    (FEED_DIR / f"{date}-day-index.md").write_text("\n".join(lines))
    print(f"Day union: {len(scored)} distinct posts -> {len(cands)} candidates "
          f"({date}-day-index.md, {date}-day-ranked.json)")


def main():
    argv = sys.argv[1:]
    since = None
    if "--since" in argv:                       # union every capture from this date up to <date>
        i = argv.index("--since")
        since = argv[i + 1] if i + 1 < len(argv) else None
        del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    date = args[0] if args else (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d")
    today = feed_files_for(date)
    span = today
    if since and since < date:
        days = (datetime.strptime(date, "%Y-%m-%d") - datetime.strptime(since, "%Y-%m-%d")).days
        span = feed_files_for(date, days_back=days)
    if not span:
        print("No feed file found for", since or date, "to", date, "in", FEED_DIR)
        return 1
    # Convergence is judged over the last 3 days of captures, not one file.
    pool_days = max(2, (datetime.strptime(date, "%Y-%m-%d") - datetime.strptime(since, "%Y-%m-%d")).days) if since else 2
    pool = [p for f in feed_files_for(date, days_back=pool_days) for p in _load_posts(f)]
    conv = build_convergence(pool)
    affinity = build_affinity()
    total = 0
    for path in today:
        try:
            total += _rank_one(path, conv, affinity)
        except Exception as ex:
            print(f"  rank error on {path.name}: {ex}")
    write_day_union(date, span, conv, affinity)   # one ranked list for everything since the last digest
    print(f"\nRanked {len(today)} feed file(s) for {date} | {total} candidates "
          f"| {len(affinity)} saved authors | {len(pool)} posts in the convergence pool.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
