# Models and Architectures

> Concept page, updated as new sources are ingested.

Scope: New model releases, transformer variants, non-autoregressive and diffusion LMs, SSMs, MoE, small specialised models.

## Current state of knowledge

*Last updated 2026-10-11. Three digests feed this page: [10-04](../daily-digest/2026-10/2026-10-04.md), [10-09](../daily-digest/2026-10/2026-10-09.md) and [10-11](../daily-digest/2026-10/2026-10-11.md). The 10-11 window added only light items (section 5).*

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

## Open questions

- Can a learned per-token halting gate be trained in an autoregressive looped model above 1B parameters? The 10-09 digest predicts a release within 90 days.
- Can the gate be trained on task outcomes instead of likelihood?
- ALoDLM's latents reset between denoising steps. Can latent state persist across steps?
- Do ALoDLM's results hold on agentic and long-context workloads? None are reported on the project page.
- "Think Before You Paint: Recursive Latent Reasoning for Diffusion Models" sits in Kurate's top 5 and is unread. It is worth reading beside ALoDLM.

## Key sources

- [2026-10-09 · ALoDLM: adaptively looped diffusion language models](2026-10-09-alodlm-adaptively-looped-diffusion-lm.md)
- Covered in digests without a summary page: Towards Looped Models Done Right, Part II and Loop Scaling Laws ([10-04](../daily-digest/2026-10/2026-10-04.md)); shared-memory looped pretraining, LiFT, Recurrent Looped Transformer and DLoop ([10-09](../daily-digest/2026-10/2026-10-09.md)).
