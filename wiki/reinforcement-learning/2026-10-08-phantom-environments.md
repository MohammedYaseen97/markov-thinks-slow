# PhantomEnvironments: Training LLM Agents in Fictional Worlds

> Source summary · 2026-10-08 · arXiv 2609.40221 abstract and author thread, via the X feed. The paper body was not captured.

**TL;DR.** Rule-generated, fully synthetic multi-turn RL environments built from fictional worlds. Agents search a corpus of templated articles to answer multi-hop questions. No LLM is used in generation, so each environment has zero marginal cost and a known answer. Agents trained there transfer to real multi-hop search benchmarks, often beating real-world training data on newer benchmarks.

No diagram: the mechanism is a generator plus a checker, and the abstract gives no further structure.

## Key points

- Trained agents generalize to unseen fictional universes.
- Qwen models learn to scale their search budget roughly linearly with question difficulty.
- Ablation: hop count drives transfer more than constraints or comparisons.
- Author's thread: a 7B model trained this way performs like an agent ten times its size. That figure is not in the abstract.
- Limits: one skill (agentic search), no numbers in the abstract, code marked coming soon.

## How this relates to the wiki

- A structural answer to the leak problem in the [MiMo audit](2026-10-08-mimo-reward-hacking-audit.md): a fictional world has no Git history or web page to leak from.
- Bears on the sharpening debate from 2026-10-04 (Sharpening Tax, Finetuning with Sampling) and on [token cues](../training-finetuning/2026-10-08-token-cues-base-model-reasoning.md): here RL appears to teach a procedure and a budget policy, not just relocate probability mass.
- Concept page: [Reinforcement Learning](reinforcement-learning.md).

## Links

- [Paper](https://arxiv.org/abs/2609.40221)
- [Post](https://x.com/anmolkabra/status/2108227458256482675)
- [Code](https://github.com/kilian-group/phantom-envs)
- Digest: [2026-10-08](../daily-digest/2026-10/2026-10-08.md)
- Raw: [X feed capture](../../raw/twitter/feed/2026-10-08-day-ranked.json), post id 2108227458256482675 (gitignored)
