# Models and Architectures

> Concept page — updated as new sources are ingested.

Scope: New model releases, transformer variants, non-autoregressive and diffusion LMs, SSMs, MoE, small specialised models.

Last updated: 2026-10-08.

## Current state of knowledge

### Looped models (pattern declared 2026-10-04, extended 2026-10-08)

- A looped model reuses one block of layers several times. Depth grows and the parameter count does not.
- Rethinking at Fixed Points (2026-10-04): near a fixed point the path stops mattering. Terminal KV sharing keeps only the last loop's KV cache. A 1.6B looped model with a 4-block memory footprint lands within 1.5 points of a 12-block Transformer. A model trained at fixed depth 5 breaks under the same sharing. A learned depth prior and orthogonal input injection fix it.
- Loop Scaling Laws (Meta, 2026-10-04): about 2x total-parameter efficiency on reasoning from looping.
- Looped-DiT (2026-10-04): a 260M looped diffusion model beats one 6.5x larger. LoopCD (Apple, 2026-10-04) contrasts early and final loop predictions at decode time.
- [LiFT](2026-10-08-lift-loop-flow-transformers.md) (2026-10-08): each loop targets a point on a straight path from the first estimate to the true target, indexed by a continuous depth coordinate. A model trained with 2 loops improves up to 16 loops at inference.
- Shared lesson from fixed points and LiFT: a loop must not learn that it is the last one. Depth overfitting is the main failure, and both fixes randomize or continuize depth during training.
- Recurrent Looped Transformer (2026-10-08, first part of overview only): recurrence across tokens instead of within a token. A parallel causal encoder plus a decoder whose final state feeds the next token, tested on length generalization for parity and permutation tasks.
- DLoop (NAVER, 2026-10-08, first part of overview only): loops the drafting stage of speculative decoding, deciding whether to draft another block before verification.

### Releases and serving-oriented designs

- DeepSeek-V4.1-Flash (via the vLLM blog, 2026-10-08): causal encoder-decoder design that activates 16B parameters per token in decode and 8B in prefill, with a global KV cache of about 890 bytes per token.
- Mellum2.1 (JetBrains, 2026-10-08): 12B mixture-of-experts with 2.5B active parameters, Apache 2.0.
- Claude Haiku 5.5 and GPT-6 shipped in this window. See the [2026-10-08 digest](../daily-digest/2026-10/2026-10-08.md).
- Encoder-free multimodal designs appeared twice on 2026-10-04 (a thread and NVIDIA's PixelUMM). Not yet a pattern.

## Open questions

- Adaptive depth per token or per input at inference. Nothing yet learns when to stop looping.
- Does continuous-depth training transfer from diffusion to language models?
- Is loops-to-convergence a usable difficulty signal for a router?

## Key sources

- 2026-10-08 · [LiFT: Loop Flow Transformers](2026-10-08-lift-loop-flow-transformers.md)
- 2026-10-04 · Towards Looped Models Done Right, Part II: see the [2026-10-04 digest](../daily-digest/2026-10/2026-10-04.md). Its summary page is not on disk.
- Unread, listed on HuggingFace 2026-10-08 without abstracts: Mechanics of Long-Context Hybrid Models Part 1.1 (arXiv 2610.10114), TIDES (2605.09742).
