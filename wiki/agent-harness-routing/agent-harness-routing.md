# Agent Harness and Model Routing

> Concept page, updated as new sources are ingested.

Scope: Harness engineering, LLM and agent routing, orchestration.

A harness is the program between the world and the model. It decides what each model call sees, which tools exist, and how the next action is chosen.

## Current state of knowledge

*Last updated 2026-10-09. Two digests feed this page: [10-04](../daily-digest/2026-10/2026-10-04.md) and [10-09](../daily-digest/2026-10/2026-10-09.md).*

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

## Open questions

- What share of a jointly tuned system's gain comes from data, from training settings and from the harness, measured from one starting point with repeats?
- Does a structured harness such as an RLM beat a standard coding harness when both get the same RL budget?
- Do gains from automated harness and model tuning compound across cycles? RSIGym's one self-research run went from 56.66% to 56.26%.
- Where should a decomposition come from: a person, a search over harness code, or the model itself?
- Will model cards report per-harness scores? The 10-04 prediction (two open coding model cards by 2027-01-02) is open and looks less likely.
- Which metric should multi-agent designs be compared on?

## Key sources

- [2026-10-09 · Language model harnesses are compositional generalizers (RLM trained with RL)](2026-10-09-harness-as-compositional-generalizer-rlm.md)
- [2026-10-09 · RSIGym](2026-10-09-rsigym.md)
- [2026-10-09 · Recursive Game Creator](2026-10-09-recursive-game-creator.md)
- Covered in digests without a summary page: the multi-harness RL guide, AutoCompact, CMU harness learning and ScholarEvolve ([10-04](../daily-digest/2026-10/2026-10-04.md)); "What Does a Harness Buy?", VERA, DeLM, "On the Nature of the Swarm" and OverclaimBench ([10-09](../daily-digest/2026-10/2026-10-09.md)).
