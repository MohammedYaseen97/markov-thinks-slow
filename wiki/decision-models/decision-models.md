# Decision Models and System 1 / System 2

> Concept page — updated as new sources are ingested.

Scope: Jev and open clones, RLCD and calibration training, decision heads, fast-decider plus slow-reasoner designs.

Last updated: 2026-10-08.

## Current state of knowledge

### What a decision model is

- State and typed questions go in. A choice with a probability per option comes out in one forward pass. No text is generated. Jev (TypeSafe, released 2026-09-15) is the commercial reference, with three primitives: choice, score on an ordered scale, and a yes or no probability.
- TypeSafe names its training method Reinforcement Learning for Calibrated Decisions (RLCD). Its architecture is not public. Jev served over a trillion tokens in its first three days, per Modal's case study (2026-10-08).

### Architectures seen in the open

- Branch readout (Gero-4B, 2026-10-04): encode the context once, run each option as a branch that cannot see the others, score with one shared linear layer, softmax. Order-invariant by construction.
- Clef-style head (Unsloth guide, 2026-10-08): everything in one prompt read once, a small head scores every option over the backbone's outputs and decides all questions together.
- Encoder with one `[MASK]` per option (Laya, 2026-10-08).
- Decoder-only VLM backbone (d1-3B) and bidirectional encoder with audio and vision adapters (d1-omni-600M), both 2026-10-08.
- Truncated backbone: RSI-Jev found Qwen3.5-4B cut at layer 20 of 32 decides as well as the full model (2026-10-04).

### Calibration

- Reward maximization does not give calibration: the best policy always picks the likelier option, so selection probabilities go to 1 while correctness stays at 60% (value-function essay, 2026-10-04).
- Proper scoring rules do. Gero-4B's reward pays the log-probability of sampled real outcomes plus an honest-confidence term. A naive self-prediction reward drove the right answer's probability from 0.418 to 0.001.
- Any extra loss term must have zero gradient where the model's probabilities equal the truth, or it moves the optimum.
- The supervised shortcut ([Open d1 and Clef-head recipe](2026-10-08-open-d1-and-clef-head-training.md), 2026-10-08): train for accuracy, then calibrate on held-out rows. This yields single-step correctness probabilities.

### What a router should threshold on

- The value-function essay (2026-10-04): the useful number is the probability the task succeeds if this action is taken and a given policy continues. With a binary end reward that is exactly Q(s, a). Route to the slow system when the value of the best action is low, not when entropy across actions is high.
- Vendor "confidence" fields derived from the output distribution are not correctness estimates (two independent sources, 2026-10-04).
- No release so far ships a success estimate validated separately from the choice distribution. Unsloth's calibration step is partial progress.

### The open stack (as of 2026-10-08)

- Serving: llama.cpp `/v1/systemone` (2026-10-04), multimodal support in v0.6.0 (2026-10-08). Hugging Face `decision-model` tag with 1,300+ models.
- Weights: Decision 2.0 (0.6B to 27B), Open d1 (3B and 600M, multimodal), pplx-decider v1.1 27B, Vela 2.0 span-level routing models.
- Training: Gero-4B build log, Unsloth guide.
- Speed reference: d1-3B answers one question in 8 ms on an RTX 4090 and 50 ms on a Jetson Orin Nano.

## Open questions

- A success head trained on task outcomes, with its own reliability table.
- Q under "fast only" and Q under "fast plus slow system" differ. A router needs both to know whether switching helps.
- Credit assignment from a terminal label back to the decision that caused failure.
- Audio decision benchmarks do not exist (Liquid, 2026-10-08).
- A decider over concepts or latent world-model states. Nothing in the formulation requires tokens.

## Key sources

- 2026-10-08 · [Open d1 and the Clef-head training recipe](2026-10-08-open-d1-and-clef-head-training.md)
- 2026-10-04 · Gero-4B build log, "Is Jev Secretly a Value Function?": see the [2026-10-04 digest](../daily-digest/2026-10/2026-10-04.md). Their summary pages are not on disk.
- Unread and a priority: System Switch: When Should a Fast Decision Model Stop and Think? (arXiv 2610.09683), listed on HuggingFace 2026-10-08 without an abstract.
