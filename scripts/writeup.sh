#!/bin/bash
# Runs every day from cron. It always captures. Every second day it also writes the
# unattended digest + Media Zone + wiki pages over everything captured since the last
# digest, then commits and pushes. WRITEUP_EVERY_DAYS sets the gap (default 2).
REPO="$HOME/markov-thinks-slow"; cd "$REPO" || exit 1
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
D=$(TZ=Asia/Kolkata date +%Y-%m-%d); YM="${D:0:7}"; mkdir -p .claude/logs; LOG=".claude/logs/writeup-$D.log"
DIGEST="wiki/daily-digest/$YM/$D.md"
say() { echo "[$(TZ=Asia/Kolkata date '+%H:%M')] $*" >> "$LOG"; }

scripts/capture.sh                                    # no-op for X if this slot already ran
exec 9>/tmp/markov-thinks-slow.lock; flock 9

if [ -f "$DIGEST" ]; then say "digest for $D already exists, nothing to do"; exit 0; fi
LAST=$(ls wiki/daily-digest/*/20*.md 2>/dev/null | sed 's#.*/##; s#\.md##' | sort | tail -1)
EVERY="${WRITEUP_EVERY_DAYS:-2}"
if [ -n "$LAST" ]; then
  GAP=$(( ( $(date -d "$D" +%s) - $(date -d "$LAST" +%s) ) / 86400 ))
  if [ "$GAP" -lt "$EVERY" ]; then say "captured only: last digest $LAST was $GAP day(s) ago, write-up every $EVERY"; exit 0; fi
fi
SINCE=$(date -d "${LAST:-$D} +1 day" +%Y-%m-%d 2>/dev/null || echo "$D")
[[ "$SINCE" > "$D" ]] && SINCE="$D"
say "write-up for $D, feed since $SINCE (last digest ${LAST:-none})"
.venv/bin/python connectors/twitter/rank_feed.py "$D" --since "$SINCE" >> "$LOG" 2>&1
.venv/bin/python connectors/window/build_window.py --digest-date "$D" >> "$LOG" 2>&1

scripts/daily_run.sh "$D" >> "$LOG" 2>&1
if [ ! -f "$DIGEST" ]; then say "FAILED: no digest written (see .claude/logs/daily-$D.log)"; exit 1; fi

# Second pass if the first ran out of budget before the wiki pages.
MISSING=$(grep -o '(\.\./\.\./[^)]*\.md)' "$DIGEST" | tr -d '()' | sed 's#^\.\./\.\./#wiki/#' | sort -u | while read -r f; do [ -f "$f" ] || echo "$f"; done | wc -l)
if [ "$MISSING" -gt 0 ]; then
  say "$MISSING summary pages missing, running the pages pass"
  P=$(sed -e "s/__DATE__/$D/g" -e "s#__YM__#$YM#g" scripts/pages_prompt.template.md)
  env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT timeout 90m claude -p "$P" --permission-mode acceptEdits \
    --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "WebFetch" "Bash(.venv/bin/python:*)" "Bash(ls:*)" "Bash(cat:*)" \
      "Bash(grep:*)" "Bash(find:*)" "Bash(mkdir:*)" "Bash(head:*)" "Bash(tail:*)" "Bash(wc:*)" "Bash(sed:*)" \
    > ".claude/logs/pages-$D.log" 2>&1
fi
.venv/bin/python connectors/window/build_window.py --digest-date "$D" --close >> "$LOG" 2>&1

# Publish, unless something private or secret-looking is about to go out.
git add -A
# Private terms live in .private-terms.local (one per line, never committed).
PRIV=$( [ -f .private-terms.local ] && grep -v '^[[:space:]]*$' .private-terms.local | paste -sd'|' )
if { [ -n "$PRIV" ] && git diff --cached | grep -qiE "^\+.*($PRIV)"; } \
   || git diff --cached | grep -qE '^\+.*(hf_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|xox[bp]-[A-Za-z0-9-]{10,}|auth_token"?[[:space:]]*[:=][[:space:]]*"[0-9a-f]{20,})'; then
  say "NOT PUSHED: private or secret-looking text in the changes. Review with: git diff --cached"; exit 2
fi
git diff --cached --quiet || git commit -q -m "wiki: digest, Media Zone and pages for $D" >> "$LOG" 2>&1
timeout 300 git push origin main >> "$LOG" 2>&1 && say "pushed" || say "PUSH FAILED (run: git push origin main)"
