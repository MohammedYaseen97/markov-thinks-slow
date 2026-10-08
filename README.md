# markov-thinks-slow

A self-maintaining research wiki. Every day it reads papers, blogs and an X feed, and writes a daily digest, a Media Zone page and topic pages on reinforcement learning, the LLM training stack, model architectures, decision models, world models and the cognitive science of reasoning.

- **Site:** https://mohammedyaseen97.github.io/markov-thinks-slow/
- **How it works:** farmers in `connectors/` collect sources into `raw/`; Claude Code reads them under the rules in `CLAUDE.md` and writes `wiki/`; the Astro site in `site/` is built and deployed by GitHub Actions on every push.
- **What is not here:** the private X feed, bookmarks and session credentials stay on the owner's machine and are excluded by `.gitignore`.

## Credit

Built on [cere-bro](https://github.com/bayesiansapien/cere-bro) by Amit Singh Bhatti, which follows Andrej Karpathy's [LLM wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). This instance changes the topics, the X capture (reposts as originals, full X articles, PDFs, priority accounts) and the feed ranker.
