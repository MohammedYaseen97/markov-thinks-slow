# Training and Fine-tuning

> Concept page — updated as new sources are ingested.

Scope: Pretraining, fine-tuning, post-training and alignment methods, data, optimizers, distributed training.

Last updated: 2026-10-08.

## Current state of knowledge

### On-policy versus off-policy data in post-training

- Finetuning with Sampling (2026-10-04): SFT generalizes badly because its data is off-policy, not because of its loss. Metropolis-Hastings rewrites expert traces toward the base model's own distribution while keeping the privileged information. Plain SFT on the result rivals GRPO and forgets less.
- Cambridge distillation study (2026-10-04): once KL direction and learning rate are controlled, who wrote the rollouts is not central. Forward KL is robust to rollout policy. Reverse KL prefers student rollouts. Learning rate governs forgetting.
- These two remain in tension. A joint test on tasks with zero base pass rate has not been run.
- 2026-10-08, thread opener only: a claim that off-policy training works for continual learning "if done right", with "periodic grafting" named in a reply. Not read beyond that.

### What post-training changes inside the model

- [Token cues](2026-10-08-token-cues-base-model-reasoning.md) (2026-10-08): a few opening tokens decide whether a base model reasons. RL makes effective openings more likely. The association comes from the mid-training data, shown by a causal edit that turns "Chicken" into a reasoning cue.
- Consequence for evaluation: separate what a model can do from what it is likely to do. Run the base model with the best prefill before crediting an RL run.
- Consequence for data design: repeated openings in synthetic reasoning traces create strong, accidental switches. Diversity of openings is a robustness lever. A fixed opening is a control lever.
- Parallel Power Tempering (2026-10-04) reaches a similar sharpening at inference with several MCMC chains at different powers.

### Practice notes

- OPD (on-policy distillation) plumbing, from the nanopd tutorial (2026-10-04): prefix caching must be off on the student server, and the teacher must score the student's exact token ids.
- FlashAttention-3 in BF16 silently destabilized a pretraining run after 25B tokens (2026-10-04). A fix called GProj costs 4.7% step time.
- Mellum2.1 (2026-10-08): JetBrains reports RL went from a short final stage to the main part of training for a 12B open coding model, with every open RL data source filtered for broken tests and unverifiable answers before use.
- Liquid's d1 notes (2026-10-08): weight averaging across backbones and merged checkpoints from different seeds helped, and data hygiene mattered more than advanced techniques.

## Open questions

- Is the cue effect present in models whose mid-training mix has no synthetic reasoning traces?
- Does projection-sampled data behave differently under forward and reverse KL?
- Projection sampling for multi-turn agent trajectories: is turn-level resampling enough, or is environment replay needed?
- A cheap diagnostic that separates elicitation from new skill in a post-training gain.

## Key sources

- 2026-10-08 · [Base Models Can Reason By Taking a Cue From Training Data](2026-10-08-token-cues-base-model-reasoning.md)
- 2026-10-04 · Finetuning with Sampling, On-Policy or Off-Policy Learning, Parallel Power Tempering: see the [2026-10-04 digest](../daily-digest/2026-10/2026-10-04.md). Their summary pages are not on disk.
- Unread, listed on HuggingFace 2026-10-08 without abstracts: Gains and Collapse in On-Policy Distillation (arXiv 2610.03185), On-Policy Distillation with Negative-Policy Rollouts (2610.07874), Composing What Each Teacher Learned (2610.10460), ReSAIL (2609.39306).
