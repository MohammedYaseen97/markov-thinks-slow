#!/bin/bash
# Unattended write-up for today (digest + Media Zone). Farmers must already have run.
# Usage: scripts/daily_run.sh [YYYY-MM-DD]
REPO="$HOME/markov-thinks-slow"; cd "$REPO" || exit 1
export PATH="$HOME/.local/bin:$PATH"
D="${1:-$(TZ=Asia/Kolkata date +%Y-%m-%d)}"; YM="${D:0:7}"
NBM=$(.venv/bin/python -c "
import json,os
n=0
try:
    w=json.load(open('raw/_windows/$D.json'))['files']
    items=[f for v in w.values() for f in v] if isinstance(w,dict) else w
    for f in items:
        p=f if isinstance(f,str) else (f.get('path') or f.get('file') or '')
        p=p[:-3]+'.json' if p.endswith('.md') else p
        if '/bookmarks/' in p and p.endswith('.json') and os.path.exists(p):
            d=json.load(open(p)); n+=len(d if isinstance(d,list) else d.get('bookmarks',[]))
except Exception: pass
print(n)")
PROMPT=$(sed -e "s/__DATE__/$D/g" -e "s#__YM__#$YM#g" -e "s/__NBM__/$NBM/g" scripts/run_prompt.template.md)
# Private reader note: local only, shapes selection, never quoted in output.
[ -f CLAUDE.local.md ] && PROMPT="$PROMPT

$(cat CLAUDE.local.md)"
mkdir -p .claude/logs
env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT timeout 150m claude -p "$PROMPT" \
  --permission-mode acceptEdits \
  --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "WebFetch" "WebSearch" \
    "Bash(.venv/bin/python:*)" "Bash(python3:*)" "Bash(ls:*)" "Bash(cat:*)" "Bash(grep:*)" "Bash(find:*)" \
    "Bash(mkdir:*)" "Bash(curl:*)" "Bash(date:*)" "Bash(head:*)" "Bash(tail:*)" "Bash(wc:*)" "Bash(sed:*)" \
    "Bash(sort:*)" "Bash(cut:*)" "Bash(echo:*)" \
  > ".claude/logs/daily-$D.log" 2>&1
echo "exit=$?" >> ".claude/logs/daily-$D.log"
ls -la "wiki/media-zone/$YM/$D.md" "wiki/daily-digest/$YM/$D.md" 2>&1
