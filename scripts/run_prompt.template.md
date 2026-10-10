Today is __DATE__ (IST). This is the unattended daily run of the wiki. Follow CLAUDE.md throughout. Work without asking questions; there is nobody to answer.

Ground rules for this run:
- Every farmer has already run. Do not run any farmer. Do not use git. Do not publish anything.
- Run scripts with `.venv/bin/python`, never bare `python3`.
- Gmail, Reddit and LinkedIn are not enabled. Do not mention them as gaps.
- Read the earlier digests and Media Zone pages in `wiki/daily-digest/` and `wiki/media-zone/` first. Do not write up again what they already covered; if an earlier item resurfaces, say only what is new. Lead with what is NEW since the last digest. Concept pages may still be stubs: start or extend them.

Inputs (the collection window):
- `raw/_windows/__DATE__.md` lists every raw file in this window.
- X feed: read `raw/twitter/feed/__DATE__-day-index.md` FIRST. It is the whole day's feed, ranked, top 200 candidates. The ranking is evidence, not the verdict: you choose what matters for this reader. Before writing about any post, read it in full with `.venv/bin/python connectors/twitter/show_post.py <id> [<id> ...]` (add `--max 12000` for very long sources). That prints the complete post and every source the farmer fetched: X Articles, linked pages, PDFs. Write from those sources, per "Originals first" in CLAUDE.md.
- Bookmarks: every `raw/twitter/bookmarks/__DATE__-*.md` / `.json` file holds posts the reader saved since the last run (__NBM__ in this window). They are curated intent: every substantive one must appear in the Media Zone with the fullest treatment (Saved reading section), written from its full source via show_post.py. Where the paper is only in an attached image, view the image file with the Read tool (`image_paths` in the bookmark record, files under `raw/twitter/images/`). If there are none, omit the Saved reading section.
- Papers, blogs and videos: exactly the `raw/huggingface/`, `raw/kurate/`, `raw/rss/` and `raw/youtube/` files listed in the window manifest (their filenames may carry an earlier date than today; the manifest decides, not the filename).
- For each Deep Dive paper run `.venv/bin/python connectors/alphaxiv/enrich.py <arxiv_id>` and use the result if it is non-empty.

Outputs, in this order. All are required. Do not stop until all exist.
1. `wiki/media-zone/__YM__/__DATE__.md`: the Media Zone, per the CLAUDE.md Media Zone spec (Today's signal bullets, sections by attention tier, `mz-feed` cards with real 3-5 sentence blurbs, at least one house-style diagram for the anchor item, thumbnails from the posts' image URLs). Priority accounts get read in full and surfaced. Substantive items get a real explanation the reader can learn from, not a headline.
2. `wiki/daily-digest/__YM__/__DATE__.md`: the daily digest, per the CLAUDE.md Daily Digest spec: optional one-line **Opportunity:** note first if any open call appeared, then Today's 5 for you, TL;DR, Deep Dives (6 sub-sections each, house-style diagram where there is a mechanism), Industry Pulse, Global View, Looking Ahead. Fold in every substantive Media Zone item (writing rule 12).
3. For every Deep Dive: a summary page in the right `wiki/<topic>/` folder, the concept page for that topic updated, a line in `wiki/index.md`, an entry in `wiki/log.md`.

Quality bar:
- Calibrate to the Reader Profile: deep on RL, the training stack, architectures, decision models, world models and cognition; standard on harness, routing and inference optimisation. Flag anything that bears on the reader's reasoning-model project.
- Explain the mechanism from the source you read. If a source was not readable or not read, say so in the text instead of guessing. Never state a number you did not see in a source.
- No em dashes anywhere. Gloss every technical term and named paper on first use in a section. Never expose tier vocabulary.
- Skip hype, promotion and engagement bait even when ranked high.
