Today is __DATE__ (IST). Follow CLAUDE.md. Work without asking questions. Do not run farmers, do not use git, use `.venv/bin/python` for scripts.

The digest `wiki/daily-digest/__YM__/__DATE__.md` and the Media Zone `wiki/media-zone/__YM__/__DATE__.md` are finished. Do NOT edit either of them. Finish the wiki pages:

1. The digest links to summary pages that do not exist yet (every `../../<topic>/__DATE__-*.md` link whose file is missing). Write each one at exactly that path, per the CLAUDE.md "Source summaries" page type: TL;DR paragraph, a house-style Mermaid diagram where there is a mechanism, key findings, how it relates to earlier wiki pages, links to related pages and to the source. Base each page on the matching Deep Dive and on the source itself: read X posts and their sources with `.venv/bin/python connectors/twitter/show_post.py --date __DATE__ <id> --max 12000` (ids are in `raw/twitter/feed/__DATE__-day-index.md` and the bookmark files in the window manifest), and papers from the raw files listed in `raw/_windows/__DATE__.md`. State no number you did not see in a source or in the digest.
2. Update the concept page of each topic touched (`wiki/<topic>/<topic>.md`), building on what is already there.
3. Add each new page to `wiki/index.md` and add entries to `wiki/log.md`.

Rules: no em dashes, gloss technical terms on first use, never expose tier vocabulary, never mention the reader's employer or career plans. When done, list the files written.
