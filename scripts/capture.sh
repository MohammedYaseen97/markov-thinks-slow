#!/bin/bash
# Daily capture: every farmer, then rank the X feed. No Claude usage. Safe to re-run.
REPO="$HOME/markov-thinks-slow"; cd "$REPO" || exit 1
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
D=$(TZ=Asia/Kolkata date +%Y-%m-%d); mkdir -p .claude/logs; LOG=".claude/logs/capture-$D.log"
exec 9>/tmp/markov-thinks-slow.lock; flock 9          # one pipeline step at a time
{
  echo "=== capture $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M IST')"
  for f in twitter kurate youtube rss huggingface; do
    echo "--- $f"; timeout 45m .venv/bin/python "connectors/$f/farmer.py" 2>&1 | grep -av 'Following page' | tail -15
  done
  .venv/bin/python connectors/twitter/rank_feed.py "$D" 2>&1 | tail -2
  echo "=== capture done $(TZ=Asia/Kolkata date '+%H:%M IST')"
} >> "$LOG" 2>&1
