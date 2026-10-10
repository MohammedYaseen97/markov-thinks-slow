# Training and Fine-tuning

> Concept page, updated as new sources are ingested.

Scope: Pretraining, fine-tuning, post-training and alignment methods, data, optimizers, distributed training.

## Current state of knowledge

*Last updated 2026-10-09. Two digests feed this page: [10-04](../daily-digest/2026-10/2026-10-04.md) and [10-09](../daily-digest/2026-10/2026-10-09.md).*

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

## Open questions

- A compute-matched comparison on tasks with zero base pass rate, where the student cannot stumble on the answer and state coverage should finally matter.
- Does the result hold for strong-to-weak distillation?
- Five more on-policy distillation papers were listed on HuggingFace in the 10-09 window without readable abstracts (on gains and collapse, negative-policy rollouts, teacher-relative shifts, vision-language-action models, and agent self-distillation collapse). Their claims are unread.
- Will a lab report a tuned SFT baseline next to its on-policy numbers? The 10-09 digest predicts one by 2026-12-08.
- Projection sampling for multi-turn agent trajectories (10-04 prediction): no new evidence.

## Key sources

- [2026-10-09 · Multi-teacher on-policy distillation versus SFT](2026-10-09-multi-teacher-opd-vs-sft.md)
- Covered in digests without a summary page: Finetuning with Sampling and the on-policy versus off-policy distillation study ([10-04](../daily-digest/2026-10/2026-10-04.md)); the MOPD2 explainer thread ([10-09](../daily-digest/2026-10/2026-10-09.md)).
