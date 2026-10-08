# Recursive Game Creator: An Agentic Product-Level Experience-Oriented Game Harness

> Source summary · 2026-10-08 · arXiv 2610.08621. HuggingFace Daily Papers and Kurate cs.AI rank 8: cross-source confirmed (HF + Kurate). Written from the first part of alphaxiv's overview only.

**TL;DR.** A harness from HKU MMLab that makes play experience, not just functional correctness, the target of repeated game development. It couples game construction with executable playtesting, behavioural and visual assessment, preference feedback and version selection. Its Player is coding-native: it writes reusable policies that drive the game through a programmatic interface.

No diagram: the portion of the source that was read does not describe the pipeline in enough detail to draw it faithfully.

## Key points

- Gap addressed: a game can run and meet requirements while having unclear controls, weak pacing or poor feedback.
- Policy-based play yields more frequent and varied trajectories and keeps structured state and event information that screenshot-driven testing loses.
- Results and the scoring method were not in the portion read. No numbers are recorded.
- Kurate's score is the default 1200 for every entry this week, so the rank carries no information.

## How this relates to the wiki

- Another verifier-style harness component, alongside [OverclaimBench and ThinkingBox](2026-10-08-overclaimbench-thinkingbox.md): evidence is gathered by a second agent instead of trusted from the first.
- Concept page: [Agent Harness and Model Routing](agent-harness-routing.md).

## Links

- [Paper](https://arxiv.org/abs/2610.08621)
- Digest: [2026-10-08](../daily-digest/2026-10/2026-10-08.md)
- Raw: [HuggingFace](../../raw/huggingface/2026-10-08-recursive-game-creator-an-agentic-product-level-ex.md) · [Kurate cs.AI](../../raw/kurate/2026-10-08-cs-ai.md)
