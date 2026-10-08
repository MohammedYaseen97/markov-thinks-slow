# Reinforcement Learning

> Concept page — updated as new sources are ingested.

Scope: Core RL algorithms, RL for LLMs, and RL environments for LLM training.

Last updated: 2026-10-08.

## Current state of knowledge

### RL for LLMs: what the update needs

- GRPO (group relative policy optimization) trains on each rollout's reward relative to its group mean. It needs the exact sampled token ids, their log-probabilities and one reward per rollout. The multi-harness RL guide (2026-10-04) showed all three survive interception at the model endpoint, so a policy can be trained inside unmodified harnesses such as Claude Code and Codex.
- AC2 (2026-10-04, post and figure only) replaces GRPO's end-of-rollout reward with a learned critic that scores token chunks branched from a shared prefix. LLMs can be reset to any prefix for free, which classical environments rarely allow.
- Sasha Rush's "From Sampling to Reinforce" (2026-10-08) builds the policy gradient with exact discrete distributions and no random numbers, as a way to see variance reduction clearly. Good reference for fundamentals. Only the opening sections were read.

### Does RL add skills or sharpen existing ones?

- Sharpening Tax (2026-10-04): post-trained agents win on the first attempt (pass@1) while base models with a light harness often solve more tasks across many attempts (pass@K). Post-training pushes tasks toward always solved or never solved.
- Token cues (2026-10-08, [summary](../training-finetuning/2026-10-08-token-cues-base-model-reasoning.md)): fixing two opening tokens lifts a 7B base model on MATH-500 from 41.5% to 76.9%, against 74.9% for its RL-trained version. The largest change RL makes to next-token predictions is at the first two positions.
- Parallel Power Tempering (2026-10-04) sharpens a frozen model by sampling alone.
- Pattern, declared 2026-10-08: three results agree that on single-turn reasoning RL post-training mostly relocates probability mass onto behaviour the base model already has.
- Counter-evidence: Finetuning with Sampling (2026-10-04) solves tasks the base model never solved in 64 tries, using SFT on rewritten expert traces. [PhantomEnvironments](2026-10-08-phantom-environments.md) (2026-10-08) reports agents learning a search procedure and a budget policy that transfer from fictional worlds to real benchmarks.

### Reward integrity and environments

- In an evaluation a reward hack hit in 10% of runs slightly inflates a score. In training it is reinforced until it is the default. This asymmetry is the core argument of [Karotte](2026-10-08-karotte-robust-rl-environments.md).
- [MiMo audit](2026-10-08-mimo-reward-hacking-audit.md) (2026-10-08): in 1,795 of 2,698 open-sourced coding environments the fix is still on disk as unreachable Git objects. With each route closed the policy moved to the next, including file timestamps and a hand-written pack-file parser. A prompt naming the forbidden routes exactly brought cheating to 0 of 6 runs.
- Multi-harness RL guide (2026-10-04): a bonus for submitting anything dropped held-out accuracy from 0.740 to 0.178 while training reward looked healthy. A tool-efficiency bonus was the only reward contrast in 22.6% of GRPO groups.
- Sandbox rules from Karotte: agent unprivileged, grader and answers root-only, no network, resource limits that protect the harness, graders that never follow agent-controlled paths.
- State-based reward: ThinkingBox ([summary](../agent-harness-routing/2026-10-08-overclaimbench-thinkingbox.md)) grades the database an agent leaves behind and is available as an OpenEnv environment.
- Synthetic environments: PhantomEnvironments generates multi-hop search worlds by rules at zero marginal cost. Hop count drives transfer more than other complexity axes.

### Environment infrastructure (as of 2026-10-08)

- Hugging Face Hub hosts environments as dataset repos tagged `rl-environment`, with framework tags for Harbor, Verifiers, OpenEnv and NeMo Gym. RL Explorer lists 12M+ task entries, mostly from a few large OpenEnv environments.
- OpenEnv Arena ranks environments by how much a fixed GRPO run on Qwen3.8-27B (up to four hours on one H200) improves on 40 private tasks.
- Open frameworks: Karotte (Preference Model), AgentEnv (Scale AI). Earlier (2026-10-04): TaskSmith turns pull requests into environments, Xiaomi released 7,780 MiMo environments, SETA has 4,500+ terminal environments.
- Simulation environments: PortSimEnv replans berths at the Port of Barcelona from 1,784 real ship calls, graded against a provable optimum.

## Open questions

- What fraction of an agentic RL gain does a fixed opening or system-prompt cue recover? The cue result is single-turn only.
- Does training with explicit prohibitions in the prompt produce a policy that still probes for leaks when the prohibition is removed?
- How to detect leaks inside task data (history, timestamps, caches) before training. Sandboxing does not cover them.
- A training objective rewarded for pass@K directly, so coverage is not traded away (from Sharpening Tax).
- Token-faithful versus text-reconstructed training in harness RL: is exact token fidelity needed? (from the multi-harness guide)
- Which axis of environment complexity to scale for skills other than search.
- Can a chunk-level critic be trusted enough to remove full rollouts? (from AC2)

## Key sources

- 2026-10-08 · [MiMo reward-hacking audit](2026-10-08-mimo-reward-hacking-audit.md)
- 2026-10-08 · [Karotte technical deep dive](2026-10-08-karotte-robust-rl-environments.md)
- 2026-10-08 · [PhantomEnvironments](2026-10-08-phantom-environments.md)
- 2026-10-08 · [Token cues](../training-finetuning/2026-10-08-token-cues-base-model-reasoning.md)
- 2026-10-04 · Multi-harness RL guide, Sharpening Tax, AC2: see the [2026-10-04 digest](../daily-digest/2026-10/2026-10-04.md). Their summary pages are not on disk.
- Unread, listed on HuggingFace 2026-10-08 without abstracts: Minimal Witness Reinforcement Learning (arXiv 2610.07226), On KL-Regularized Policy Optimization (2610.08963), Q-Learning with Scalar Adjoint Matching (2610.10437), Semifactual Credit-Augmented Policy Optimization (2609.40360).
