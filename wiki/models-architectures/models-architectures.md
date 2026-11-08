# Models and Architectures

> Concept page, updated as new sources are ingested.

Scope: New model releases, transformer variants, non-autoregressive and diffusion LMs, SSMs, MoE, small specialised models.

## Current state of knowledge

*Last updated 2026-11-08 (sections 10 and 11 from the [11-08 digest](../daily-digest/2026-11/2026-11-08.md)). Earlier digests feeding this page: [10-04](../daily-digest/2026-10/2026-10-04.md), [10-09](../daily-digest/2026-10/2026-10-09.md), [10-11](../daily-digest/2026-10/2026-10-11.md) and [11-01](../daily-digest/2026-11/2026-11-01.md). The 11-01 window is the first to test architecture claims at equal serving cost (section 6), which tempers section 1.*

### 1. Looped models (well past a pattern)

A looped model applies the same block of layers several times, so depth becomes a quantity that can vary. The 10-04 digest counted three looping papers and declared a pattern. Its Deep Dive on looped models at fixed points ended with "adaptive depth per token at inference" as the open problem. The 10-09 window adds five more results:

- **[ALoDLM](2026-10-09-alodlm-adaptively-looped-diffusion-lm.md)** delivers adaptive depth per token, in a diffusion language model, with a learned gate. Details below.
- **Shared-memory looped pretraining.** Only the first pass writes the KV cache (the stored attention keys and values for past tokens). It reports 76 to 79% less context memory and lower perplexity at 150M to 1B parameters.
- **LiFT.** Flow-matching loops trained at 2 passes keep improving up to 16.
- **Recurrent Looped Transformer.** Synthetic tasks only.
- **DLoop.** Loops the draft stage of speculative decoding.

### 2. Diffusion language models catch their autoregressive base

A diffusion language model (DLM) starts from a masked sequence and fills in many tokens in parallel over a few denoising steps. DLMs have trailed same-size autoregressive models on quality. ALoDLM (Amazon AGI) names the cause as a computation-difficulty mismatch: within one step, easy and hard tokens get the same fixed depth. Its fix is an inner loop with persistent latent state. A Prelude encodes the sequence once, a shared Recurrent Core runs up to 4 times, and a Coda feeds an LM head and an exit gate. Low-entropy tokens are committed and return as context. Unresolved tokens keep their latent and refine it.

- Average over eleven benchmarks: ALoDLM-8B 80.3 against Qwen3-8B 78.5, and ALoDLM-1.7B 65.5 against Qwen3-1.7B 63.8.
- On GSM8K the 8B model runs at 612.4 tokens per second against 229.3 for vLLM-served Qwen3-8B.
- Both are trained from their Qwen3 base by direct SFT on a 5B-token corpus.

Why it works: committing an easy token changes the conditional distribution of the hard ones in the same step. The loop turns one parallel guess into a short chain of conditioned guesses and keeps the hard tokens' partial computation.

Caveat: the quality table uses a single-token preset and the speed figures use the parallel decoder, so quality and speed are not reported at one operating point in what was read.

### 3. The exit gate is a decider about computation

ALoDLM's gate decides whether more thought is worth it, and it is trained jointly with the model that does the thinking. It is trained on likelihood, not on task success, so it has no notion of stakes. This links to the [decision models page](../decision-models/decision-models.md).

### 4. Releases noted

JetBrains Mellum2.1 (a 12B mixture-of-experts coding model, crediting scaled RL post-training), Claude Haiku 5.5 and the GPT-6 rollout in ChatGPT are recorded in the 10-09 Industry Pulse.

### 5. Light additions from the 10-11 window (posts and titles only)

Nothing on architectures was read in depth in the [10-11 digest](../daily-digest/2026-10/2026-10-11.md). Noted for follow-up:

- **Diffusion language models, post-training and decoding.** DiPOD ("Diffusion Policy Optimization without Drifting Apart") claims stable post-training for diffusion language models, with Sudoku rising from 22% to 97% from a one-line change. Mosaic is a constrained-decoding framework for diffusion language models aimed at function calling. Both are posts only. They bear on section 2: a diffusion model that matches its autoregressive base still needs RL post-training and structured output to be usable in agents.
- **Loops.** HuggingFace lists "Scaling to Tens of Thousands of Test-Time Iterations with Loop-Native Attention Residuals" (arXiv 2610.11570) and "One Block, Multiple Depths: Recurrent Vision Transformers with Depth-Programmed Experts" (arXiv 2610.12448). Titles only.
- **State-space models.** Cerberus applies a bidirectional Mamba (Hydra) to long-sequence genomic prediction at higher nucleotide resolution. Post only.
- **A caution.** One post warns that engram or n-gram memory can markedly amplify overfitting when data repeats.

### 6. Architecture has about 2% of loss left (11-01)

**[The 1,129-run architecture ablation](2026-11-01-architecture-ablations-since-gpt3.md)** judges every change at equal serving cost (vLLM, coding-agent workload, FP8) and extrapolates with a scaling law to 1T tokens. Fine-grained MoE (an active parameter worth 4 to 5 dense ones) and linear-attention hybrids (2 to 7 times cheaper to serve) are the real wins; GQA, MQA, MLA and sliding windows win only through KV-cache savings; norms, MLPs and positions give 1 to 2% at best. The final stack is predicted 9.4% better than GPT-3 and 1.0% better than a 2026 KDA hybrid. Gains at trained sizes are 1.5 to 3 times larger than at serving size, and for the modern hybrid only about 2% of predicted loss is parameter-limited (about 11% for the 2021 reference). Muon is worth about one round of stacking. **Shift from the prior state:** small-model architecture wins, including loops, must now be discounted heavily; the remaining levers are data, optimizer, serving efficiency and the training objective.

### 7. Loops under resource constraints (11-01)

**[How to Loop Your Transformer](2026-11-01-how-to-loop-your-transformer.md)** (Meta, up to 1B, 32 loops): loop the full model when parameters bind, a middle block when training FLOPs bind; gains saturate or reverse with more loops; loop-specific LoRA adapters help more as loops grow; Parallel Loop Transformers need the current-token embedding preserved and separately normalized. Meta's looped-MoE law (first noted 10-04 as about 2x parameter efficiency) resurfaced with its cost: 1.8 times the inference compute and a lower 14-benchmark mean (46.9% against 50.2%) for a 5-loop MoE matching a larger one on reasoning. **Shift:** section 1's pattern stands, but the evidence now says loops are a parameter-saving trade paid at decode time, not free reasoning. Saved in the same window: GRAM (stochastic recursive reasoning keeping several hypotheses), Quotient Recurrent Reasoner, and Recurrent Looped Transformer results on 256-bit parity.

### 8. Generation without tokens first (11-01)

**[Next-Concept Modeling](2026-11-01-next-concept-modeling.md)** (Stanford and Together AI) generates a multiscale residual VQ-VAE code stack coarse to fine, each level in parallel: 21 times faster than the strongest diffusion LM on LM1B with better generative perplexity, 31 times on XSum at equal ROUGE-L, better on Sudoku, up to 725M parameters with per-task tokenizers. With [Soft-MTP](../training-finetuning/2026-11-01-soft-multi-token-prediction.md) (cleaner multi-token objective) and the [Platonic Representation theorem](../world-models-reasoning/2026-11-01-platonic-representation-theorem-jepa.md) (good views beat next-token prediction 42 times on sample efficiency), this is the third result in one window that moves gains to the objective or unit of prediction rather than the block design. A forming pattern.

### 9. Releases noted (11-01)

Carbon-X (14.8B, Qwen3-14B base with a 6-mer DNA vocabulary; see the [training page](../training-finetuning/training-finetuning.md)), NVIDIA Nemotron 3.5 Super VL (120B total, 12B active, open weights and recipes), Mistral Large 4 (1T total, 52B active, open weights), RWKV-7 G1L (pure RNN). ReplaySSM (caching an SSM's inputs rather than its state) is reported running in production for GLM-5.3-Flash and Kimi-K3 serving.

### 10. How MoEs are trained, written down (11-08)

**[The Ultimate MoE Training Handbook](2026-11-08-moe-training-handbook.md)** (Hugging Face, about 800K GPU hours) answers section 6's implication: if architecture has about 2% of loss left, the gains are in training the winning architectures well. Captured chapters: test all-to-all bandwidth per node count (77.14 GB/s on two nodes, 30.91 on eight), keep a 1-expert upcycled parity run (within 0.00087 of dense), keep the router in fp32 because bf16 ties change winners, and a ten-model router survey (sigmoid dominant, DeepSeek-V4 on sqrt(softplus), no agreement on the routed scaling factor). Beam's report agrees on sigmoid gating, loss-free bias plus a sequence aux loss and z-loss, and adds a cosine-decayed bias update rate that ended at 1.04 times uniform load. SAE Interprets MoE (ByteDance Seed, abstract) finds expert contribution far more concentrated than gating, with fine-grained specialization.

### 11. Releases and attention variants (11-08)

- Beam (501.3B MoE, 5:1 local-global attention, NoPE on global layers, DSRes residual scaling), Inkling 2 Small (594B MoE, images), Kimi K3.1 Pro (2.8T total, 104B active, 1M context), Marin Mochi 535B-A23B (pretraining done). All sparse MoE.
- Muir (abstract): linear attention with one low-rank gate projection and matched-filter readout; 1.8 to 2.0% lower perplexity than Gated DeltaNet-2 up to 1.34B, extrapolates from 4K training to 10M-token streams.
- Zyphra Hierarchical Attention: a tree index over the KV cache, subquadratic, retrofitted with about 1B tokens of distillation. See the [inference page](../inference-optimization/inference-optimization.md).

## Open questions

- What controls router sharpening and flattening during training, and how should bias-update schedules interact with LR decay?
- Is expert specialization semantic enough to route by concept?
- Can a learned per-token halting gate be trained in an autoregressive looped model above 1B parameters? The 10-09 digest predicts a release within 90 days.
- Can the gate be trained on task outcomes instead of likelihood?
- ALoDLM's latents reset between denoising steps. Can latent state persist across steps?
- Do ALoDLM's results hold on agentic and long-context workloads? None are reported on the project page.
- "Think Before You Paint: Recursive Latent Reasoning for Diffusion Models" sits in Kurate's top 5 and is unread. It is worth reading beside ALoDLM.
- Does the "about 2% left for architecture" estimate hold for objectives other than next-token prediction, and under long-context metrics such as RULER?
- Does Next-Concept Modeling keep a large speedup over diffusion above 1B parameters and with a shared tokenizer? (11-01 prediction, 90 days.)
- Do NCM's coarse codes carry transferable semantics, and can RL reward them before expansion?

## Key sources

- [2026-11-08 · The Ultimate MoE Training Handbook](2026-11-08-moe-training-handbook.md)
- [2026-10-09 · ALoDLM: adaptively looped diffusion language models](2026-10-09-alodlm-adaptively-looped-diffusion-lm.md)
- [2026-11-01 · I tried every LLM architecture change since 2020](2026-11-01-architecture-ablations-since-gpt3.md)
- [2026-11-01 · How to loop your transformer, and scaling laws for looped MoE](2026-11-01-how-to-loop-your-transformer.md)
- [2026-11-01 · Next-Concept Modeling](2026-11-01-next-concept-modeling.md)
- Covered in the 11-01 Media Zone without a summary page: GRAM, Quotient Recurrent Reasoner, FlashMask-3, ReplaySSM.
- Covered in digests without a summary page: Towards Looped Models Done Right, Part II and Loop Scaling Laws ([10-04](../daily-digest/2026-10/2026-10-04.md)); shared-memory looped pretraining, LiFT, Recurrent Looped Transformer and DLoop ([10-09](../daily-digest/2026-10/2026-10-09.md)).
