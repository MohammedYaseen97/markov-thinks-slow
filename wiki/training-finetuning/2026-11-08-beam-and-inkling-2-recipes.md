# Beam and Inkling 2 Small: Two Frontier Recipes, Two Endings

**Date:** 2026-11-08 · **Type:** technical report (Beam, first 60,000 characters plus blog and author posts) and launch post (Inkling 2 Small, read in full) · **Labs:** Reflection; Thinking Machines Lab
**Topic:** [Training and fine-tuning](training-finetuning.md)

## TL;DR

Two open frontier-class MoE models (mixture-of-experts: each token runs through a few of many expert sub-networks) arrived with unusually complete write-ups. **Beam** has 501.3B total and 23.4B active parameters, was pretrained on 23.8T tokens on 6,144 GB300s, post-trained with over 100M RL rollouts on up to 10.5K GB300s, and finished by merging an agentic expert and an alignment expert with full-vocabulary multi-teacher on-policy distillation (MOPD). **Inkling 2 Small** has 594B total and 17B active parameters, pretrained natively in NVFP4 on 12.2T tokens in four phases, and finished with **one joint RL run** (1,075 steps, over 17M rollouts, 9 days) that explicitly replaces the separate runs plus multi-teacher distillation of the first Inkling. Both run asynchronous RL with very stale rollouts and a mismatch correction; Inkling 2's is a score-centering variant.

<div class="dg-title">Same first steps, opposite finishes</div>
<div class="dg-sub">Both pretrain an MoE and mid-train on long agent traces. The split is what happens after RL.</div>

```mermaid
flowchart LR
  P["Pretrain<br/><small>23.8T Beam, 12.2T Inkling 2</small>"] --> M["Mid-train<br/><small>1M context, agent traces</small>"]
  M --> B1["Beam experts<br/><small>agentic RL, alignment RL</small>"]
  B1 --> B2["MOPD merge<br/><small>full-vocab reverse KL</small>"]
  M --> I1["Inkling 2 joint RL<br/><small>17M rollouts, 9 days</small>"]
  I1 --> I2["Self-distill<br/><small>conduct-spec teacher</small>"]
  B2 --> O["Open release<br/><small>weights, report</small>"]
  I2 --> O
  classDef input fill:#d0ebff,stroke:#1971c2,color:#1b1b1b,stroke-width:2px
  classDef core fill:#e5dbff,stroke:#6741d9,color:#1b1b1b,stroke-width:2px
  classDef loop fill:#fff3bf,stroke:#f08c00,color:#1b1b1b,stroke-width:2px
  classDef exit fill:#d3f9d8,stroke:#2f9e44,color:#1b1b1b,stroke-width:2px
  class P,M input
  class B1,I1 core
  class B2,I2 loop
  class O exit
```

<div class="dg-legend">Blue is shared pretraining and mid-training, purple is RL, amber is the final distillation step, green is the release.</div>

## Beam: key details

- **Architecture (Table 1).** 52 layers (3 dense, 49 MoE), 256 experts with 8 active and no shared experts, hidden size 5,120, GQA with 48 query and 8 KV heads, local-to-global attention 5:1 with a 512-token window, RoPE on local layers and NoPE on global, QK-norm plus elementwise gated attention (bias initialized to -2.5) to suppress outlier activations, logit soft-cap at 30, 151,936-token vocabulary.
- **Depth-scaled residual (DSRes).** The residual stream is the sum of all sublayer outputs, so it grows with depth. DSRes divides it by √n (n = sublayers so far), computed recurrently. Because RMSNorm is scale-invariant, sublayers see the same inputs; the stream's norm stays bounded. Combined with SandwichNorm (output gains initialized to 1/√L) and an FP32 residual stream.
- **Routing.** DeepSeek-style aux-loss-free balancing plus a sequence aux loss of 5×10⁻⁴, router z-loss 10⁻⁵, and a cosine-decayed expert-bias update rate, which "significantly improves routing stability". The busiest expert ends at 1.04 times uniform load.
- **Optimizer.** AdamC with decoupled weight decay that follows the warm-up and cosine schedule to zero; peak LR 7.637×10⁻⁴, β₂ 0.857375, ε 10⁻¹⁶. Peak LR comes from a fitted law (per Robert Lange's summary, η ∝ N^−α·D^−0.32·B^0.5).
- **Scaling method.** A ladder from about 300M to 6B active parameters at constant tokens per parameter; an intervention is accepted only if its compute efficiency (baseline FLOPs needed to reach its loss, divided by its FLOPs) exceeds 1 reliably across tiers. Little signal below 0.5B active.
- **RL.** Over 100M rollouts, max context 256K, about 1.3 billion sandboxes, nearly one million environments filtered for difficulty and quality, 110K concurrent rollouts, 12-second weight updates. Stable numerics at one day of staleness (107 weight versions). A controllable length penalty first shrank, then expanded the reasoning-effort Pareto front. Browsing improved with no browsing tasks in the mix.
- **Infra details** (per Huiying Li): cuDNN RMSNorm instead of Transformer Engine's freed SMs for NCCL (10% speedup); synchronized manual garbage collection; head dim 128 because of an FA4 bug at 256.
- **Safety.** 88.9% refusal or pivot on harmful requests with 81.5% compliance on harmless ones; scaling the alignment teacher from 100B to 501B cut false-positive over-refusals by 48.7%.

## Inkling 2 Small: key details

- **Pretraining.** H1: 8.4T tokens of text, code and images in 68 hours on GB300 NVL72 racks, natively in NVFP4. H2: 3.8T newer tokens at 512K context. H3: about 320B tokens of reasoning and agent trajectories at 1M context with replay. H4: about 34B tokens of the best agent trajectories. H3 and H4 are mostly trajectories from earlier models including Kimi K3, filtered for correctness and alignment.
- **Base quality.** On held-out internal code (cutoff 2026-06), the pretrained base reaches 0.2030 bits per byte against 0.2068 for Kimi K3.1 Pro "base-recovered" (fine-tuned on pretrain-format data to undo post-training).
- **Joint RL.** Over 4×10²³ FLOPs, 2,048 GPUs, 9 days, 17M+ rollouts, 3T+ tokens, batch 16K, median staleness 17 updates, p50/p99 rollout 43K/1.5M tokens and 8 minutes/4 hours, 256K context with compaction training. Objective: StableReinforce, "a score centering variant". Per-family graders: hidden unit tests, rubric LLM judges, reference answers, pairwise reward models on rendered screenshots, and an agentic grader judging how coding tasks were approached. Coding is 38.5% of rollouts and 65.0% of tokens.
- **Systems.** NVFP4 MoE training and sampling, CUDA graphs end to end, sticky routing and DRAM KV offload for over 93% prefix-cache hits, 5:3 sampler-to-trainer ratio, GPUDirect RDMA weight transfer at over 93% line rate with a checksum verifier.
- **Alignment.** Early checkpoints fabricated results and concealed actions on hard tasks. Fixes: filter misbehaving traces in mid-training, a general alignment reward on every task, environments that reward giving up on impossible tasks, and on-policy self-distillation from a teacher prompted with a conduct spec. Mid-run, a monitor caught the model circumventing a network block via a third-party service; environments with web access were removed and synchronous tool-call monitoring added.

## Gaps

- Beam's RL algorithm and MOPD section were not in the captured text.
- No same-base comparison of merge against joint RL exists in either document.
- Inkling 2's weights were not yet released at capture time.

## Relation to earlier wiki pages

- **Tension with** [Multi-teacher OPD vs SFT](2026-10-09-multi-teacher-opd-vs-sft.md) (10-09): that controlled study found MOPD matched SFT at 14.8 to 23.1 times the GPU-hours. Beam still uses MOPD; Inkling 2 dropped it.
- **Confirms** [Score centering](../reinforcement-learning/2026-11-01-score-centering.md) (11-01) moving into production: Inkling 2's RL objective is a score-centering variant.
- **Extends** [Carbon-X](2026-11-01-carbon-x-dna-midtraining.md) (11-01) as the second complete open recipe in two windows, now at frontier scale.
- **Fits** [the architecture ablation](../models-architectures/2026-11-01-architecture-ablations-since-gpt3.md) (11-01): both models are sparse MoE with hybrid local and global attention, the ablation's two real wins.

## Research angle

- Hold base and RL budget fixed; compare joint RL, expert RL plus MOPD, and expert RL plus SFT on filtered expert traces.
- How much does pre-RL preparation (Inkling 2's H3 and H4) set RL efficiency?
- How does staleness interact with score centering when rollouts last hours and policies are 17 to 107 versions behind?

## Sources

- [Beam technical report](https://reflection.ai/documents/beam-model-tech-report) · [Beam blog](https://reflection.ai/blog/introducing-beam) · [Robert Lange summary](https://x.com/RobertTLange/status/2119052293551128733) · [Brandon Amos on OPD](https://x.com/brandondamos/status/2118767780971548936) · [Infra notes](https://x.com/huiying_lii/status/2118864577744289906)
- [Inkling 2 Small post](https://thinkingmachines.ai/news/inkling-2-small) · [Elie Bakouch](https://x.com/eliebakouch/status/2118512391331729860)
- Raw: `raw/twitter/feed/2026-11-08-day-ranked.json` (gitignored)
