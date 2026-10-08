# What Does a Harness Buy? Tokens, Mostly

> Source summary · 2026-10-08 · arXiv 2610.04433 abstract and DAIR.AI curator notes, via the X feed

**TL;DR.** With the model held fixed, swapping the coding harness across Claude Code, mini-SWE-agent and OpenCode on SWE-bench Verified moves pass rates no more than rerunning the same configuration. What the harness does decide is cost: up to 3x per task, set by the system prompt and tool schemas resent at every step.

No diagram: this is an empirical study with no architecture.

## Key points

- 447 tasks, two models: Claude Code and mini-SWE-agent are equivalent within five points.
- 45-task hard subset, five models: a harness swap flips 13% of tasks, the same as a rerun. Tasks won in one run are not the ones won in the next.
- The one effect above the noise is a loss: OpenCode trails by up to 9 points. For one model half the gap is runs cut short by its output cap.
- The cost gap is set at the first call by the preamble and scaled by step count. Per-step growth and per-call tool output differ far less. Cached-input pricing scales the bill and does not reorder it.
- Resolution: 45 tasks catch a 13-point gap half the time and no gap with 80% power. 447 tasks resolve about 5 points.
- Same window. VERA (arXiv 2610.05923, NVIDIA) co-evolves weights and harness skills on 9,000+ verifiable sandboxes with explicit acceptance gates. DeLM (arXiv 2606.10662, Stanford) replaces the lead agent with a shared context and a task queue. RSIGym (arXiv 2610.10310) exposes training and evaluation as services to a research agent. A post describes an NVIDIA terminal-agent setup where a verifier picks one of 8 candidate commands per step. Its paper was not captured.

## How this relates to the wiki

- Contradicts, on its face, the multi-harness RL guide (2026-10-04): one 2.6B model at 62% under Mini-SWE-Agent and 33% under Claude Code. Possible reconciliation: harness sensitivity falls with model strength. Unmeasured.
- Qualifies the "harness as a training variable" pattern from 2026-10-04 (multi-harness guide, AutoCompact, CMU harness learning, ScholarEvolve): gains under about 5 points on a few hundred tasks are inside the noise.
- Concept page: [Agent Harness and Model Routing](agent-harness-routing.md).

## Links

- [Paper notes](https://academy.dair.ai/papers/what-does-a-harness-buy-tokens-mostly-2610.04433)
- [Post](https://x.com/dair_ai/status/2107920656788767098)
- Digest: [2026-10-08](../daily-digest/2026-10/2026-10-08.md)
- Raw: [X feed capture](../../raw/twitter/feed/2026-10-08-day-ranked.json), post id 2107920656788767098 (gitignored)
