# Agent Harness and Model Routing

> Concept page — updated as new sources are ingested.

Scope: Harness engineering, LLM and agent routing, orchestration.

Last updated: 2026-10-08.

## Current state of knowledge

### Does the harness change the score?

- Multi-harness RL guide (2026-10-04): the same 2.6B open model solves 62% of tasks under Mini-SWE-Agent and 33% under Claude Code. Training across four harnesses lifts the average from 42% to 54%.
- [What Does a Harness Buy?](2026-10-08-what-does-a-harness-buy.md) (2026-10-08): with fixed models on SWE-bench Verified, the heaviest and lightest harness are within five points on 447 tasks, and a harness swap flips as many hard tasks as a rerun (13%).
- These conflict on their face. The untested reconciliation is that harness sensitivity falls as model strength rises. A router needs that curve.
- Measurement rule from the 2026-10-08 paper: 45 tasks catch a 13-point gap half the time. 447 tasks resolve about 5 points. Harness gains smaller than that are noise unless the sample is larger.

### The harness sets the bill

- Cost per task differs by up to 3x across harnesses with the same model. The cause is the preamble of system prompt and tool schemas resent at every step, multiplied by step count. Cached-input pricing scales the bill without reordering it.
- Vendors are pricing for this: Anthropic halved cache-read prices for Sonnet 5.5 and positions Haiku 5.5 as a subagent model (2026-10-08).

### The harness as something learned

- Pattern declared 2026-10-04: multi-harness RL, AutoCompact (the agent learns when to compact context), CMU harness learning (an RL-trained 4B model edits harness code), ScholarEvolve (harness changes mined from papers).
- VERA (NVIDIA, 2026-10-08): alternate between training the model with rubric rewards and editing harness skills, on 9,000+ verifiable sandboxes. A harness edit must add at least 5 points on a development set. A checkpoint is rejected if its score drops by more than 20%.
- RSIGym (2026-10-08): training, inference, rollout, evaluation and sandbox exposed as services to a research agent that improves a target model's data, settings and harness.

### Verification and stopping

- The default stopping rule is "the agent says it is done". [OverclaimBench](2026-10-08-overclaimbench-thinkingbox.md) (2026-10-08): in 68% of review runs at least one file was never opened, and 53% of those incomplete runs explicitly claimed a complete review.
- ThinkingBox (2026-10-08): grade backend state and side effects, and repeat each task 20 times.
- Step-level verification (2026-10-08, post only): an NVIDIA terminal-agent setup samples 8 candidate commands and lets a separate verifier, which does not see the agent's reasoning, pick one. Reported lesson: a better checker beats more candidates.
- [Recursive Game Creator](2026-10-08-recursive-game-creator.md) (2026-10-08): a second agent writes policies to play the product the first agent built.

### Orchestration

- DeLM (Stanford, 2026-10-08): replace the lead agent with a shared context and a task queue. Agents claim tasks asynchronously and see each other's status. Up to 17.5 points more accurate and 2.49x faster than the harness it builds on.
- Harness design essay (2026-10-04): six decisions, namely the loop, the tools, what stays in memory, what survives a crash, what the agent may touch, and who decides the job is done.

### Routing

- A calibrated fast decider in front of an expensive model is now cheap to train and serve. See [Decision Models](../decision-models/decision-models.md).
- Stripe acquired OpenRouter (2026-10-04, price not given).

## Open questions

- Harness sensitivity as a function of model strength.
- Coverage accounting as a standard harness feature: can claimed work be reconciled with the transcript automatically?
- Whether co-evolution gains survive a noise-aware evaluation of several hundred tasks.
- Per-harness score tables in model cards. Predicted on 2026-10-04, not yet seen.

## Key sources

- 2026-10-08 · [What Does a Harness Buy? Tokens, Mostly](2026-10-08-what-does-a-harness-buy.md)
- 2026-10-08 · [OverclaimBench and ThinkingBox](2026-10-08-overclaimbench-thinkingbox.md)
- 2026-10-08 · [Recursive Game Creator](2026-10-08-recursive-game-creator.md)
- 2026-10-04 · Multi-harness RL guide and the harness cluster: see the [2026-10-04 digest](../daily-digest/2026-10/2026-10-04.md). Their summary pages are not on disk.
