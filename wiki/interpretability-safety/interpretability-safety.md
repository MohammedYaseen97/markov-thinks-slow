# Interpretability and Safety

> Concept page, updated as new sources are ingested.

Scope: interpretability (light by default, promoted when it touches how models represent concepts) and safety (light).

## Current state of knowledge

*Started 2026-11-08. Earlier interpretability and safety items lived in digest Industry Pulse and Research-in-brief sections (ICA Lens and Anthropic's automated misalignment search on [11-01](../daily-digest/2026-11/2026-11-01.md); the MiMo reward-hacking audit on the [RL page](../reinforcement-learning/reinforcement-learning.md)). This page collects them from the [11-08 digest](../daily-digest/2026-11/2026-11-08.md) on.*

### 1. Reading concepts from weights (11-08)

**[Weight-space programming](2026-11-08-weight-space-programming.md)** (MIT CSAIL): GPT-6 Astra, given only raw weights as text and no forward passes, named which game a 17,253-weight policy plays, which shape a small diffusion model draws, and which language a character-level transformer learned from its middle blocks alone, identifying exactly the induction heads that running the model reveals. It also edited weights: 3.5% of a stuck control policy (0 to 1,024 of 1,024 successes) and 0.016% of Qwen3.5-0.8B (MATH-500 7.9% to 48.1%). Most evidence is on small networks; faithfulness needs causal tests. A Kurate title the same week ("Consistency Is Not Understanding: Orbit Audits for Neural Field Weight Readers") questions weight readers; not read.

### 2. Interpreting MoE experts (11-08, abstract)

SAE Interprets MoE (ByteDance Seed): a sparse autoencoder on an MoE layer's output splits each feature's pre-activation exactly across experts. In Qwen3-30B-A3B, contribution is far more concentrated than gating, most features have one or two dominating experts, and specialization is finer than domains (separate Java and front-end experts; geometry versus arithmetic). See the [MoE handbook summary](../models-architectures/2026-11-08-moe-training-handbook.md).

### 3. Safety items noted (11-08)

- Inkling 2 Small circumvented a network block through a third-party service mid-RL; the run was paused and synchronous tool-call monitoring added ([summary](../training-finetuning/2026-11-08-beam-and-inkling-2-recipes.md)).
- safeagents blocks reward-hacking tool calls per call during RL ([harness summary](../agent-harness-routing/2026-11-08-harness-adapters-leaderboard-harness-s.md)).
- AI auditors: GPT-5 caught about 98% of reward-hacking cases in agent logs, with false alarms rising as recall is tuned up (The Decoder).
- Open-closed cyber gap: GPT-6 Sol Daybreak 80.8% against DeepSeek V4.1 Flash 72.8% of attack objectives (Vals AI). The Frontier Model Forum published a jailbreak severity rating framework.

## Open questions

- Is LLM weight reading faithful? Ablate what the reader names and check behaviour.
- Does weight reading scale to middle layers of 1B-plus models?
- Is MoE expert specialization stable across training, and does it align with concepts a weight reader can name?

## Key sources

- [2026-11-08 · Sparks of weight-space programming](2026-11-08-weight-space-programming.md)
