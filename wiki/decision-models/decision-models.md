# Decision Models and System 1 / System 2

> Concept page, updated as new sources are ingested.

Scope: Jev and open clones, RLCD and calibration training, decision heads, fast-decider plus slow-reasoner designs.

A decision model takes a state and typed questions and returns a choice with a probability in one forward pass, instead of generating text.

## Current state of knowledge

*Last updated 2026-11-08. Five digests feed this page: [10-04](../daily-digest/2026-10/2026-10-04.md), [10-09](../daily-digest/2026-10/2026-10-09.md), [10-11](../daily-digest/2026-10/2026-10-11.md), [11-01](../daily-digest/2026-11/2026-11-01.md) and [11-08](../daily-digest/2026-11/2026-11-08.md). The 11-08 window ships the first documented decider that gates its own reasoning (section 16).*

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

### 8. Calibration is now reported, and still about labels (10-11)

Section 4 noted that no open release reported a calibration metric. That changed in the 10-11 window.

- **[Vega](2026-10-11-vega-physics-decision-model.md)** reports calibration error, negative log-likelihood and KL to a gold distribution. On 1,075 DecisionBench rows the 4B is less accurate than hosted Jev (0.633 against 0.752) and better on likelihood (1.420 against 3.196). The author reports Jev confident at 0.874 on rows it gets right 0.752 of the time. One author, one run.
- **Clef** (Cloudflare blog) is trained on a frozen backbone with LoRA, using label-smoothed cross-entropy plus a Brier score term.
- A **JEV-27B-VL** release advertises a calibration error of 0.019 on a vision decision board. Post only.

All of this is label calibration. The outcome-trained success head asked for by the 10-04 value-function essay has still not appeared.

### 9. A fourth head design: decide with dynamics (10-11)

Vega freezes the language model entirely, stops the forward pass at layer 19 of 24, never runs the LM head, and trains a 14.3M-parameter engine. Each candidate answer becomes a Gaussian well in a 64-dimensional space. A particle is placed and pushed using the situation, question and last-token vectors, and a damped integrator runs at most twelve steps. The answer is the well it settles in. The softmax temperature is predicted per decision from the final state (leftover speed, distance to the nearest well, steps used), and an `unbound` flag marks a particle that settled far from every well. Training pairs items that share an answer space but differ in the correct answer, and does not distil a teacher.

### 10. Distilling a fast decider from slow reasoning (10-11, post only)

AnyJev reads next-token logits over allowed answers from any open causal LLM with no fine-tuning and corrects option-order and label bias without labels. Its Tacit checkpoints (1.7B to 9B) are trained to reproduce in one forward pass the decision the base model reaches after reasoning, and send low-confidence cases back to full reasoning. This is the first open System 1 distilled from its own System 2. No numbers were read.

### 11. Cascades and the market (10-11)

vLLM Semantic Router shipped open decision models from 0.6B to 27B and a small-first cascade it says cuts estimated cost 54% against the large model alone. LiteLLM added one endpoint for several decision models. Microsoft announced Microsoft-Decision-1. Cloudflare released Clef-omni (audio, video, image, text) and cut Clef-flash to $0.038 per million input tokens. TypeSafe, maker of Jev, raised $870 million at a $7.5 billion valuation.

### 12. Deciders about thinking (10-11)

ConfSFT fine-tunes a reasoning model to predict its own confidence at intermediate points, with no loss on length or stopping, and thinking tokens fall by up to 25% at matched accuracy. "Thinking Hard, Not Smart" finds that models given one token budget across an exam spend it greedily by question order and ignore point values. A learned "is more thought worth it" signal is feasible. Value-aware allocation is not there yet.

### 13. How an open decider is built (11-01, explainer read in full)

Perplexity Decider v1.2, per an X Article endorsed by one of its builders: take a strong decoder (Qwen3.8-27B), make its full-attention layers non-causal (linear-attention layers stay causal), drop the LM head, insert one mask token per question and read it with a 255-way linear head masked to the question's options, train on hundreds of thousands of harmonized classification tasks with synthetic data and option shuffling and paraphrase, then calibrate post hoc by tuning the softmax temperature (T = 1.32). The 9B Flash variant is distilled with a KL loss. This is a fifth head design next to section 2's three and Vega's dynamics, and the simplest calibration story: one scalar, fitted after training.

### 14. Deciders move into control loops (11-01)

**[Three placements](2026-11-01-decision-models-enter-the-loop.md)** in one window. **RightNow System Zero** decides on streaming input (text, JSON, robot state, PDFs, images, voice, video) and updates per-option probabilities as evidence arrives, about 30 ms per text decision; its self-measured Decision Index score is 63.20 against 65 for the top open deciders. **JevAct** (IBM) gates an agent's tool calls with compiled code checks plus decider questions: Opus 4.6 on τ²-bench Telecom 39.5% to 80.7%, but the gain vanishes with a different user simulator and 42 of 101 bad calls break no compiled question. **DecisionRAG** (Cornell and ASAPP) navigates a document tree, scoring all branches in one shared context: +13.8 R@1 on MultiDoc2Dial and +17.4 Hit@1 on Natural Questions over dense retrieval plus an 8B reranker. Practitioner evidence: a weekly first-pass relevance filter over hundreds of thousands of entities, an SRE diagnosis pipeline with no LLM agent (80 of 105, 76.2%), and Hamel Husain's advice to tune thresholds per use case rather than keep 0.5. **Shift:** section 7 ("deciding to act") had only position papers; JevAct is the first measured gate, and it is trained on policy labels, not outcomes, so the success-head open question stands.

### 15. Evidence accumulation is the next question (11-01)

RightNow's claim that its model "holds back until the evidence is there, then commits" is the drift-diffusion question from decision neuroscience (accumulate noisy evidence to a bound), asked of a machine decider. No streaming decider has published a speed-accuracy or stopping-time curve. See the [cognition page](../cognition-decision/cognition-decision.md).

### 16. A decider that decides when to think (11-08, model card read)

**[THX-02](2026-11-08-thx-02-drex-and-dpdm.md)** (HAL-X, 4.5B plus a 60M LoRA think adapter) turns section 12's "deciders about thinking" into a shipped mechanism. The direct read always runs; the thinker writes a short note only when the top probability is below 0.6 and a learned gate says the question needs steps; the final answer is 0.7·p₀ + 0.3·p₁ so a bad note cannot overturn a confident read. Thoughts were kept for training only if they raised THX-02's own probability on the correct answer (10,129 of 29,990). Every stage uses a strictly proper scoring rule plus a KL anchor. Decision Index 0.3 sample: 65.06 gated, 63.83 direct; thinking added 25.2 points on GSM8K and cost one to three on taste tasks. This is the closest open design yet to a fast System 1 with an uncertainty-triggered System 2.

### 17. More open deciders, and a production benchmark (11-08)

- **Drex** (abstract): four open deciders, 8B to 35B-A3B, SFT plus "RL from adjusted feedback", stable under option reordering.
- **DPDM** (abstract): decisions as conditional prediction with a frozen tabular predictor over LLM-encoded history; 78.80% to 84.92% mean accuracy across 50 benchmarks, improving with history length.
- **Airbnb:** a fine-tuned Gemma 4 E2B classifier reached F1 0.902 (from 0.563) at 35 ms and about 1% of frontier cost; Jev was the most accurate off-the-shelf model under 100 ms, but its API offers no cached-input discount.
- **Calibration** remains claimed rather than measured in these releases (section 4, 8).

## Open questions

- Train the thinking gate on "my thought will improve the answer" rather than "needs steps", using the self-verification signal.
- Make the mixing weight depend on both reads' confidence.
- A success head trained on outcomes and validated separately from the choice distribution. The 10-04 prediction (an open release by 2027-01-02) is still open.
- Joint scoring versus per-option branches versus shuffled training: which gives the best calibration?
- "System Switch: When Should a Fast Decision Model Stop and Think?" ([arXiv 2610.09683](https://arxiv.org/abs/2610.09683)) was listed with no abstract and is unread. Read it first when an overview appears.
- Audio decision benchmarks do not exist yet, and Liquid does not report on the Decision Index's private vision split.
- Does a decision read from dynamics (settling time, leftover speed) predict error better than the final probability?
- Is a self-distilled decider (Tacit) better calibrated than a head trained on labels, and when does it escalate?
- Which public board will add likelihood or calibration error beside accuracy? The 10-11 digest predicts one within 60 days.
- Unread and directly relevant: "SanSi: A Looped Typed Decision Model for System 1.5 Thinking" (arXiv 2610.07730) and "System Switch" (arXiv 2610.09683).
- Will a streaming decision model publish accuracy or calibration as a function of input received? (11-01 prediction, 60 days.)
- Can an action gate like JevAct be trained with RL on whether the action eventually succeeded, instead of on policy labels?
- Is post-hoc temperature scaling enough for decider calibration, or do training-time methods (RLCD, Brier terms, dynamics) beat it on held-out distributions?

## Key sources

- [2026-11-08 · THX-02, Drex and DPDM: decision models that decide when to think](2026-11-08-thx-02-drex-and-dpdm.md)
- [2026-10-09 · Open d1 and "Train your own decision model"](2026-10-09-open-d1-and-train-your-own-decision-model.md)
- [2026-10-11 · Vega: a decision model that rolls a ball down a hill](2026-10-11-vega-physics-decision-model.md)
- [2026-11-01 · Decision models enter the loop: RightNow, JevAct, DecisionRAG](2026-11-01-decision-models-enter-the-loop.md)
- Covered in the 11-01 Media Zone without a summary page: decision models for evals (Hamel Husain), Jev-driven SRE diagnosis, Quail's trie classification, Constrained Decoding Models, Decision 3.0 on Core ML.
- Covered in the 10-11 digest without a summary page: Clef-omni, AnyJev and Tacit, Decision 2.0 and 3.0, ConfSFT, and the TypeSafe round.
- Covered in digests without a summary page: the Gero-4B build log and "Is Jev secretly a value function?" ([10-04](../daily-digest/2026-10/2026-10-04.md)).
