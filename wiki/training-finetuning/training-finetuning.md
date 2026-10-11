# Training and Fine-tuning

> Concept page, updated as new sources are ingested.

Scope: Pretraining, fine-tuning, post-training and alignment methods, data, optimizers, distributed training.

## Current state of knowledge

*Last updated 2026-10-11. Three digests feed this page: [10-04](../daily-digest/2026-10/2026-10-04.md), [10-09](../daily-digest/2026-10/2026-10-09.md) and [10-11](../daily-digest/2026-10/2026-10-11.md).*

### 1. "On-policy" is losing credit as such (pattern, three papers)

On-policy training means the student model generates the text it is trained on. Three papers in two digests take credit away from that property:

- **Finetuning with Sampling (10-04)** showed plain SFT (supervised fine-tuning) rivals RL once MCMC sampling rewrites expert traces to look like the model's own text.
- **The Cambridge distillation study (10-04)** found rollout policy mattered less than KL direction and learning rate.
- **[Multi-teacher on-policy distillation versus SFT](2026-10-09-multi-teacher-opd-vs-sft.md) (10-09)** compares four ways to merge several expert models into one student: SFT on teacher trajectories, soft-label distillation, a teacher-prefix hybrid, and MOPD (multi-teacher on-policy distillation, where the student writes the rollouts and the matching teacher scores every token). Across two settings, four models and eleven benchmarks all four reach nearly identical accuracy. MOPD costs 14.8 to 23.1 times the GPU-hours of SFT.

The shared claim is sharper than "off-policy is fine". What matters is the quality and placement of the training states, not who sampled them. Rejection sampling (keep only the teacher trajectories that succeeded) is the crude version, and projection sampling is the principled one.

### 2. Reported on-policy gains depend on a weak baseline

The same study revisits four published on-policy versus off-policy comparisons. With SFT trained on rejection-sampled teacher trajectories and its hyperparameters tuned independently, the reported gains shrink substantially.

### 3. The counter-view, and where it should hold

A thread on Xiaomi's MOPD2 argues that pure student rollouts never visit states only a stronger teacher reaches. MOPD2 starts the student from teacher and demonstration prefixes and trains only on the student's continuation. That hybrid is one of the four arms in the study above and did not win. But the study is self-distillation: teachers and student share a base checkpoint, so the student can already represent what the teachers do. A strong-to-weak setting is not covered.

### 4. Weight merging as the zero-training baseline

Merging expert weights with no training recovers expert capabilities in minutes of CPU time. Accuracy degrades as model size decreases and task interference increases.

### 5. Research is ahead of practice

Industry still pays for on-policy stages. Xiaomi's MiMo-V2.6 uses MOPD2, JetBrains credits scaled RL post-training for Mellum2.1, and River's first open recipe is RL with a LoRA adapter (small trainable matrices added to a frozen model).

### 6. Training can hurt when the harness is the bottleneck

In [RSIGym](../agent-harness-routing/2026-10-09-rsigym.md), research agents tuning a model and its harness found the more heavily trained candidate scored lower in eight of ten matched comparisons. The best runs kept weight updates light.

### 7. The post-training stack got cheaper at the last layer (10-11)

**[TRL v1.15](2026-10-11-trl-fused-lm-head.md)** fuses the LM head with the reduction that follows it. A Triton kernel projects hidden states in tiles and reduces straight to per-token log-probabilities and entropy, so the batch by sequence by vocabulary logits tensor is never built. On gemma-3-1b within 79 GiB the longest trainable sequence rises from 10,240 to 59,392 tokens for DPO and from 28,672 to 114,688 for GRPO scoring. Peak memory at 8,192 tokens drops 52% to 82%. The benchmark uses random weights and measures scoring only. The same release adds selective activation checkpointing and an asynchronous GRPO path for OpenEnv harnesses. Time-side counterparts are on the [RL page](../reinforcement-learning/reinforcement-learning.md): ThunderSyncRL and the bias, variance and throughput essay.

### 8. On-policy versus SFT: two finer claims (10-11, both from posts only)

- **OPSFT** claims the on-policy benefit is the direction of the parameter update. It extracts that direction from a few on-policy steps and constrains SFT updates to it. Post and figure only, no numbers. If it holds it is a cheap middle path between section 1's sceptics and section 3's counter-view.
- **Latent-MOPD** distils several specialist teachers through hidden states as well as token predictions and claims a student that beats the best teacher on most benchmarks. Post only.
- HuggingFace lists "On-Policy Distillation Teaches New Skills but Not New Knowledge" (arXiv 2610.09639). Title only.

### 9. Data and checkpoint selection as levers (10-11)

- **Datology Curation Studio** (vendor report): with the same 39 source datasets and identical pretraining and post-training recipes, a 30B model pretrained on curated data scored 46.8% against 37.7% for the baseline after post-training, and a 12B curated model beat the 30B baseline with about a fifth of the pretraining compute. The gap persists through post-training.
- **Before They Can Solve** (NVIDIA, summary read): rank base checkpoints for agentic post-training by whether they can produce the "decisive edit" given the prefix of a solved trajectory. Three such screens agree closely with post-trained SWE-bench Verified pass@1 across ten model pairs, where end-to-end base evaluation fails because base models cannot emit tool calls.
- **Subliminal learning, part two** (post and figure only): a backdoor reportedly transfers from teacher to student through fine-tuning on number sequences. A caution for any distillation pipeline.

## Open questions

- A compute-matched comparison on tasks with zero base pass rate, where the student cannot stumble on the answer and state coverage should finally matter.
- Does the result hold for strong-to-weak distillation?
- Five more on-policy distillation papers were listed on HuggingFace in the 10-09 window without readable abstracts (on gains and collapse, negative-policy rollouts, teacher-relative shifts, vision-language-action models, and agent self-distillation collapse). Their claims are unread.
- Will a lab report a tuned SFT baseline next to its on-policy numbers? The 10-09 digest predicts one by 2026-12-08.
- Projection sampling for multi-turn agent trajectories (10-04 prediction): no new evidence.
- Does constraining SFT to an on-policy update direction (OPSFT) recover on-policy generalization at SFT cost? No numbers seen yet.
- Do the fused-head memory gains hold with real generation, flash-attention and multi-GPU, which the release did not measure?
- Does a decisive-step screen predict post-training outcomes outside coding?

## Key sources

- [2026-10-09 · Multi-teacher on-policy distillation versus SFT](2026-10-09-multi-teacher-opd-vs-sft.md)
- [2026-10-11 · TRL v1.15: the fused LM head](2026-10-11-trl-fused-lm-head.md)
- Covered in the 10-11 digest without a summary page: OPSFT, Latent-MOPD, Datology Curation Studio, Before They Can Solve, and the second subliminal-learning paper.
- Covered in digests without a summary page: Finetuning with Sampling and the on-policy versus off-policy distillation study ([10-04](../daily-digest/2026-10/2026-10-04.md)); the MOPD2 explainer thread ([10-09](../daily-digest/2026-10/2026-10-09.md)).
