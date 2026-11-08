---
source: farmer/rss
feed: https://simonwillison.net/atom/everything/
date: 2026-11-08
entry_count: 1
---

# RSS: simonwillison-net — 2026-11-08

*1 entries from `https://simonwillison.net/atom/everything/`*

---

## 1. datasette #3046: Don't serve link: rel=next HTTP headers to Firefox for HTML pages

**Published:** 2026-11-07 23:57 UTC  
**Link:** [https://simonwillison.net/2026/Nov/7/link-rel-next/](https://simonwillison.net/2026/Nov/7/link-rel-next/)

datasette #3046: Don&#x27;t serve link: rel=next HTTP headers to Firefox for HTML pages
I was looking at the Firefox network panel today when I noticed that requests to a Datasette table page were triggering an HTTP prefetch to the next page of rows in that table.
This was happening because Datasette pages serve an HTTP link header like this:
link: &lt;https://latest.datasette.io/fixtures/compound_three_primary_keys?_next=a%2Cd%2Cv&gt;; rel="next"
This is bad. A tiny fraction of the visitors to one of those pages will click the "next" link, which means their browser is fetching unnecessary data and the Datasette server is having to render an entire page that then gets thrown away.
I dug in and learned that Firefox has an issue that has been open for 24 years about this behavior...
And one of the early comments on that issue links to my blog post from 2002 complaining about this feature. I hadn't just forgotten that I had written about it, I had forgotten the feature entirely!

    Tags: firefox, html, mozilla, datasette
