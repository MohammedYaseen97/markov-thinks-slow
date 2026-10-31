# Training and Fine-tuning

> Concept page, updated as new sources are ingested.

Scope: Pretraining, fine-tuning, post-training and alignment methods, data, optimizers, distributed training.

## Current state of knowledge

*Last updated 2026-11-01. Four digests feed this page: [10-04](../daily-digest/2026-10/2026-10-04.md), [10-09](../daily-digest/2026-10/2026-10-09.md), [10-11](../daily-digest/2026-10/2026-10-11.md) and [11-01](../daily-digest/2026-11/2026-11-01.md).*

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

### 10. Mid-training is where a new capability enters (11-01)

**[Carbon-X](2026-11-01-carbon-x-dna-midtraining.md)** (Hugging Face) is the first fully published four-stage recipe in the wiki: train only new DNA embeddings for about 10B tokens with the body frozen, mid-train on 302B tokens (55% DNA, 20% English, 15% biology text, 10% instructions), SFT on 20 subsets without distillation, then two rounds of asynchronous GRPO with code-checked rewards. It averages 66.7% on five DNA benchmarks against 67.5% for GPT-6.1 Sol. The mid-training learning rate was "the dominant knob": low keeps English and leaves DNA at chance, high learns DNA and forgets English. **Shift:** sections 1 to 3 debate post-training objectives that converge to similar accuracy; Carbon-X is a case where the step change comes before post-training starts. A HuggingFace paper in the same window, "Your LR Schedule May Not Be Principled" (abstract only), argues the effective learning-rate trajectory is the right design object and proposes an inverse-square-root schedule (AIR) that beats cosine in 128B-token MoE pretraining.

### 11. Auxiliary losses: keep the learnable part of the gradient (11-01)

**[Soft-MTP](2026-11-01-soft-multi-token-prediction.md)** shows the multi-token-prediction cross-entropy gradient splits exactly into a KL self-distillation term (match the model's own next-token prediction) and a noisy residual (the next-token model's error against one-hot targets). A one-line straight-through change keeps only the KL term with no extra memory and works with fused kernels. From 167M to 1.2B it improves perplexity, speculative decoding and zero-shot accuracy. Same structure as score centering on the [RL page](../reinforcement-learning/reinforcement-learning.md): drop the zero-information part of a gradient instead of reweighting it.

### 12. Distillation, continued (11-01, abstracts and posts)

- **Semi-OPD** (17 teacher-student pairs): distilling on offline rollouts from the initial student beats on-policy distillation in 14 of 17 pairs, up to 13.6 points and up to 11.4 times faster; on-policy helps only when teacher and student overlap heavily. Fourth item for section 1's pattern.
- **Mixture versus geometric mean** (post): with several teachers, SFT's forward KL learns their arithmetic mixture while on-policy distillation's reverse KL learns their normalized geometric mean, which explains why OPD breaks under teacher mismatch.
- **RLRT**: self-distillation with a solution-seeing teacher removes the student's hesitation tokens; RLRT upweights tokens where the student goes against the teacher on correct rollouts.
- **WISD** (abstract): distil against a deliberately weakened copy (quantized or pruned) instead of a stronger teacher; pruning lifts Qwen3.5-4B on HMMT 2025 from 57.7% to 70.5%.
- **Training Foundation Models with a Single Algorithm** (abstract): RL objectives as maximum likelihood on model-generated targets, so all stages become one likelihood method and the remaining choice is the data mixture over time.

### 13. Optimization dynamics and post-training as a service (11-01)

- Stanford CS 312's edge-of-stability explainer: a 35M transformer under full-batch gradient descent settles at sharpness about 30% above the classical 2/η limit and keeps improving.
- The [architecture ablation](../models-architectures/2026-11-01-architecture-ablations-since-gpt3.md) found swapping AdamW for Muon worth about a full round of architecture stacking.
- River now compiles user-written PyTorch losses for its post-training API; Ultramarine 1 Flash claims frontier-class knowledge work post-trained by five people for about $300k.

## Open questions

- A compute-matched comparison on tasks with zero base pass rate, where the student cannot stumble on the answer and state coverage should finally matter.
- Does the result hold for strong-to-weak distillation?
- Five more on-policy distillation papers were listed on HuggingFace in the 10-09 window without readable abstracts (on gains and collapse, negative-policy rollouts, teacher-relative shifts, vision-language-action models, and agent self-distillation collapse). Their claims are unread.
- Will a lab report a tuned SFT baseline next to its on-policy numbers? The 10-09 digest predicts one by 2026-12-08.
- Projection sampling for multi-turn agent trajectories (10-04 prediction): no new evidence.
- Does constraining SFT to an on-policy update direction (OPSFT) recover on-policy generalization at SFT cost? No numbers seen yet.
- Do the fused-head memory gains hold with real generation, flash-attention and multi-GPU, which the release did not measure?
- Does a decisive-step screen predict post-training outcomes outside coding?
- In mid-training a new modality, do per-group learning rates (higher on new embeddings, lower on the body) remove the forgetting trade-off Carbon-X reports?
- Does Soft-MTP's gain grow beyond 1.2B as the paper argues, and with more than three heads?
- How much of Carbon-X's result comes from each stage? No ablation was published in what was read.

## Key sources

- [2026-10-09 · Multi-teacher on-policy distillation versus SFT](2026-10-09-multi-teacher-opd-vs-sft.md)
- [2026-10-11 · TRL v1.15: the fused LM head](2026-10-11-trl-fused-lm-head.md)
- [2026-11-01 · Carbon-X: mid-training a 14B model to read DNA](2026-11-01-carbon-x-dna-midtraining.md)
- [2026-11-01 · Multi-token prediction done right (Soft-MTP)](2026-11-01-soft-multi-token-prediction.md)
- Covered in the 11-01 digest without a summary page: WISD, Training Foundation Models with a Single Algorithm, the AIR learning-rate schedule, Semi-OPD, RLRT, the edge-of-stability explainer.
- Covered in the 10-11 digest without a summary page: OPSFT, Latent-MOPD, Datology Curation Studio, Before They Can Solve, and the second subliminal-learning paper.
- Covered in digests without a summary page: Finetuning with Sampling and the on-policy versus off-policy distillation study ([10-04](../daily-digest/2026-10/2026-10-04.md)); the MOPD2 explainer thread ([10-09](../daily-digest/2026-10/2026-10-09.md)).
