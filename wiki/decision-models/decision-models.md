# Decision Models and System 1 / System 2

> Concept page, updated as new sources are ingested.

Scope: Jev and open clones, RLCD and calibration training, decision heads, fast-decider plus slow-reasoner designs.

A decision model takes a state and typed questions and returns a choice with a probability in one forward pass, instead of generating text.

## Current state of knowledge

*Last updated 2026-10-09. Two digests feed this page: [10-04](../daily-digest/2026-10/2026-10-04.md) and [10-09](../daily-digest/2026-10/2026-10-09.md).*

### 1. From one vendor's API to an open stack

Jev, the commercial reference from TypeSafe, is a closed hosted API whose architecture and training are not public. The 10-04 digest covered the first open pieces: a llama.cpp endpoint, Decision 2.0's open weights, the Gero-4B build log and RSI-Jev's published failure log. The 10-09 window added ready weights and a general recipe, covered in **[Open d1 and "Train your own decision model"](2026-10-09-open-d1-and-train-your-own-decision-model.md)**. Around them: Perplexity's open pplx-decider v1.1 at $0.02 per million input tokens, Inception's Mercury Decide, an OpenAI Decisions API in public beta, multimodal decision-model support in llama.cpp v0.6.0, and a `decision-model` tag on Hugging Face with more than 1,300 models.

### 2. Three open head designs

- **Unsloth (joint scoring).** The input and every question with its options go in one prompt, read once. A small head, the same design as Cloudflare's Clef, scores all options together. LoRA adapters (small trainable matrices on a frozen model) and the head are trained, then probabilities are calibrated on held-out rows. Qwen3.5-0.8B goes from 36% to 73% on the guide's typed-decisions set and reaches 78% holdout accuracy on 4GB of VRAM in 42 minutes.
- **Liquid d1 (trained backbone).** d1-3B comes from a decoder-only vision-language backbone: average the weights of two related models, fine-tune several seeds and data mixtures, merge again. It scores 48.57 on the Decision Index v0.2.1 public split and answers one question in 8 ms on an RTX 4090. d1-omni-600M is built on a 350M bidirectional encoder.
- **Laya (masked markers).** One sequence per question with a `[MASK]` marker per option on a bidirectional encoder. The markers are scored.

An open design tension: Gero-4B (10-04) scored each option in a separate branch so option order could not matter. Unsloth scores options jointly so they can serve as context for each other. Liquid shuffles options in training to get order invariance statistically. Which is better calibrated has not been tested.

### 3. What actually helped in training

Liquid's note: long inputs, shuffled answer options and fixing shortcuts in the data "made a bigger difference than more advanced techniques".

### 4. The calibration gap (unresolved since 10-04)

The 10-04 value-function essay argued that the number a router needs is the probability that the task succeeds if the action is taken, a Q-value, and not the probability that a label is correct. Every release in the 10-09 window calibrates the second. A saved tutorial shows the cost: used as a judge, Jev scored a run that skipped the order lookup at about 86% likely correct. No 10-09 source reports a calibration metric such as expected calibration error.

### 5. Evidence quality

All accuracy numbers are vendor-reported. Unsloth's starting accuracies of 30 to 37% are near chance, so the gain measures learning the format as much as judgment.

### 6. Deciders about computation

ALoDLM's exit gate decides per token whether another latent pass is worth it and is trained jointly with the model. It is the nearest thing in the wiki to a fast decider coupled to a slow thinker, though it is trained on likelihood and not on outcomes. See [ALoDLM](../models-architectures/2026-10-09-alodlm-adaptively-looped-diffusion-lm.md).

### 7. Deciding to act

In [PortSimEnv](../reinforcement-learning/2026-10-09-portsimenv-simulation-rl-environments.md), open models lose most of their score by reasoning until the budget runs out and never submitting. When to stop thinking and commit is a decision problem in its own right.

## Open questions

- A success head trained on outcomes and validated separately from the choice distribution. The 10-04 prediction (an open release by 2027-01-02) is still open.
- Joint scoring versus per-option branches versus shuffled training: which gives the best calibration?
- "System Switch: When Should a Fast Decision Model Stop and Think?" ([arXiv 2610.09683](https://arxiv.org/abs/2610.09683)) was listed with no abstract and is unread. Read it first when an overview appears.
- Audio decision benchmarks do not exist yet, and Liquid does not report on the Decision Index's private vision split.

## Key sources

- [2026-10-09 · Open d1 and "Train your own decision model"](2026-10-09-open-d1-and-train-your-own-decision-model.md)
- Covered in digests without a summary page: the Gero-4B build log and "Is Jev secretly a value function?" ([10-04](../daily-digest/2026-10/2026-10-04.md)).
