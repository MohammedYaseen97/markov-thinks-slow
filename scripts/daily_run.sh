#!/bin/bash
# Unattended write-up for today (digest + Media Zone). Farmers must already have run.
# Usage: scripts/daily_run.sh [YYYY-MM-DD]
REPO="$HOME/markov-thinks-slow"; cd "$REPO" || exit 1
export PATH="$HOME/.local/bin:$PATH"
D="${1:-$(TZ=Asia/Kolkata date +%Y-%m-%d)}"; YM="${D:0:7}"
NBM=$(.venv/bin/python -c "import json,glob;print(sum(len((lambda d:d if isinstance(d,list) else d.get('bookmarks',[]))(json.load(open(f)))) for f in glob.glob('raw/twitter/bookmarks/$D-*.json')))")
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
