# Agent Harness and Model Routing

> Concept page, updated as new sources are ingested.

Scope: Harness engineering, LLM and agent routing, orchestration.

A harness is the program between the world and the model. It decides what each model call sees, which tools exist, and how the next action is chosen.

## Current state of knowledge

*Last updated 2026-10-11. Three digests feed this page: [10-04](../daily-digest/2026-10/2026-10-04.md), [10-09](../daily-digest/2026-10/2026-10-09.md) and [10-11](../daily-digest/2026-10/2026-10-11.md).*

### 1. The harness is a training variable (established pattern, six results)

The 10-04 digest named this across four results: the multi-harness RL guide (train the model inside the harnesses it will ship in), AutoCompact (train a coding agent to decide when to compact its own context, for 9.2 points on SWE-bench Verified), CMU's harness learning (a 4B model trained with RL to edit harness code) and ScholarEvolve (which mines papers for harness changes). The 10-09 window adds two:

- **[RSIGym](2026-10-09-rsigym.md)** gives a research agent training, inference, rollouts, evaluation and sandboxes as services under one budget, and lets it change data, training settings and harness together. With $500 per benchmark run, Opus 5 as researcher takes a base model with a minimal harness from 17.67% to 50.33% on SWE-bench Verified.
- **VERA** (NVIDIA, noted in the 10-09 digest) alternates model and harness updates with acceptance gates. A harness edit is kept only if it passes self-tests and adds at least 5 points on a development set.

### 2. Where the gain comes from: first evidence favours the harness

RSIGym's single-track runs are the first attempt at credit assignment. With only training data open, the score barely moved (6 of 300 attempts gained on SWE-bench Verified, 5 of 267 lost on Terminal-Bench). With only the harness open and weights fixed, the score rose by 0.1667 and 0.1198 on the same two benchmarks. In eight of ten matched comparisons the more heavily trained candidate scored lower. The evidence is weak: the two tracks start from different models and each configuration ran once.

### 3. A harness can decide how far training generalizes

**[Harnesses as compositional generalizers](2026-10-09-harness-as-compositional-generalizer-rlm.md)** argues that a good harness makes every model call "locally in-distribution" even when the whole task is not. A Recursive Language Model (the root model keeps context in REPL variables and delegates detail to sub-calls) trained with RL on short tasks improves on tasks 8 to 32 times longer by as much as it improved in training. The same model trained as a plain transformer does not. The essay criticizes appended-history harnesses such as Claude Code and Codex for drifting out of distribution.

### 4. Open tension: does the choice of harness matter?

- **It does not, for strong models and mature harnesses.** "What Does a Harness Buy? Tokens, Mostly" (10-09 digest) found Claude Code and mini-SWE-agent within 5 points on 447 SWE-bench Verified tasks with the model fixed. Swapping the harness flipped no more tasks than rerunning the same one.
- **It does, for small models.** The 10-04 multi-harness guide reported one 2.6B model at 62% and 33% in two harnesses.
- **It does, when the harness changes structure.** The RLM essay and RSIGym's harness track both show large gains, from a different decomposition in one case and from repairing a minimal harness in the other.

These may be compatible: shipped harnesses could be interchangeable because they share one design. No source tests a structured harness against a standard one under matched training. Do not treat this as resolved.

### 5. Multi-agent systems as context engineering

The essay "On the Nature of the Swarm" (10-09 Global View) frames agents as structured inference scaling: compaction bets on what will matter later, a sub-agent writes its summary after the question is known, and persistent peers give roughly one context window each. DeLM replaces the main agent with a shared context and a task queue and reports up to 17.5 points better accuracy and up to 2.49 times faster runs on long-horizon coding tasks, at higher total cost. Proposals in this area report different metrics (accuracy against tokens, wall-clock time or agent count), so they cannot yet be compared.

### 6. Harnesses that test what they build

**[Recursive Game Creator](2026-10-09-recursive-game-creator.md)** adds a Player that writes reusable play policies and runs them through the game's programmatic interface, so play experience can be assessed on every iteration. It was read from a partial overview with no result numbers. OverclaimBench (10-09 digest) supplies the motive for checks that execute: coding agents' final reports often claim work the transcript shows was not done.

### 7. Routing

The routing gate in front of large models is becoming a commodity through open decision models. That material lives on the [decision models page](../decision-models/decision-models.md).

### 8. Swarms with persistent memory: the measurement (10-11)

**[GitSwarm](2026-10-11-gitswarm-compounding-inference.md)** gives hundreds of identical asynchronous agents one branchable Git repository and no planner. Each commit records the earlier commits it builds on. On ProgramBench it scores 79.4% against 65.1% for a single agent told to continue, rises from 73.1% at 100 workers to 79.4% at 500, and 94.7% of contributions are later built upon. This is the experiment behind section 5's essay: with persistent, structured memory, score scales with head count where one long run plateaus. Prime Intellect's Rust rewrite of its coding agent (2,209 agents, 228.7 billion tokens) is the production case, with a root orchestrator and four agents per task: planner, implementer, adversarial reviewer on a different model, verifier in a fresh sandbox. The human work was building objective parity checks.

### 9. The harness as a training variable: eight results (10-11)

Section 1 counted six. Two more: **HarnessSQL** trains Qwen3-14B inside the execution harness it uses at deployment and goes from 22.2% to 54.8% on Spider 2.0-SQLite. **MASS** (Sakana) has one model propose, run and grade multi-agent workflows and fine-tunes it on its own traces, for 1.2 to 1.6 times higher performance per output token after two cycles. CMU's harness learning (section 1) resurfaced with one new detail: its 4B proposer beats the 35B teacher at single-step revision.

### 10. A component-level answer to "does the harness matter?" (10-11)

"An Empirical Study of Harness Design for Coding Agents" (arXiv 2609.20804, abstract and introduction read) fixes the execution loop and varies planning, action space and context management over 176 matched settings. Context management matters more as the budget tightens, mostly by preventing overflow. Rule-based elision before LLM summarization is the most efficient strategy. Planning is an accuracy scaffold for weak models and a cost saver for strong ones. Predefined tools help only models that are weak at bash. This supports the reconciliation in section 4: each component's value depends on model strength and budget, so strong models with large windows make harnesses look interchangeable.

### 11. Routing inside the harness (10-11)

LangChain moved model choice into the harness for Open SWE and reports a 64% drop in median cost per coding task with no noticeable quality change. Its argument is that a gateway lacks the task context the harness already assembles. TokenRouter (NeurIPS 2026) is a serving system for token-level routing between a small and a large model, reporting 2.01 to 64.15 times the decoding throughput of existing systems. Decision-model cascades are on the [decision models page](../decision-models/decision-models.md).

### 12. Measuring learning from experience (10-11)

Agent Plasticity (Meta, summary read) defines plasticity as held-out gain per dollar of learning, with weights frozen, fresh context each episode, and inherited notes, skills and tools. The model with the best final score is often not the most efficient learner. Slow learners often ignore artifacts they already wrote.

## Open questions

- What share of a jointly tuned system's gain comes from data, from training settings and from the harness, measured from one starting point with repeats?
- Does a structured harness such as an RLM beat a standard coding harness when both get the same RL budget?
- Do gains from automated harness and model tuning compound across cycles? RSIGym's one self-research run went from 56.66% to 56.26%.
- Where should a decomposition come from: a person, a search over harness code, or the model itself?
- Will model cards report per-harness scores? The 10-04 prediction (two open coding model cards by 2027-01-02) is open and looks less likely.
- Which metric should multi-agent designs be compared on?
- Can the commit graph of a swarm be used for credit assignment and as a training signal for workers?
- Does a swarm of cheap models with a few strong verifiers match a swarm of frontier models?
- Do the component-study findings hold for multi-agent harnesses, where context is divided and not managed?

## Key sources

- [2026-10-09 · Language model harnesses are compositional generalizers (RLM trained with RL)](2026-10-09-harness-as-compositional-generalizer-rlm.md)
- [2026-10-09 · RSIGym](2026-10-09-rsigym.md)
- [2026-10-09 · Recursive Game Creator](2026-10-09-recursive-game-creator.md)
- [2026-10-11 · GitSwarm: decentralized compounding inference (with Prime Agent's Rust rewrite and the harness component study)](2026-10-11-gitswarm-compounding-inference.md)
- Covered in the 10-11 digest without a summary page: HarnessSQL, MASS, Agent Plasticity, the LangChain harness router, TokenRouter and LLM-as-a-Verifier V3.
- Covered in digests without a summary page: the multi-harness RL guide, AutoCompact, CMU harness learning and ScholarEvolve ([10-04](../daily-digest/2026-10/2026-10-04.md)); "What Does a Harness Buy?", VERA, DeLM, "On the Nature of the Swarm" and OverclaimBench ([10-09](../daily-digest/2026-10/2026-10-09.md)).
