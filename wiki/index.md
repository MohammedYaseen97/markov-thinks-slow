# Wiki Index

Catalog of all pages in this wiki. Updated automatically on every ingest.

---

## Concept pages

- [Reinforcement learning](reinforcement-learning/reinforcement-learning.md): RL environments as shared infrastructure, reward-design failures and their defences, the bias, variance and throughput of RL recipes, gradient streaming, score centering for sampler mismatch (now in three stacks), why RLVR prompts get stuck, judge rewards that leak the judge's taste, group-free RL from one rollout per task (GS1), and cooperative multi-agent RL.
- [Training and fine-tuning](training-finetuning/training-finetuning.md): the shrinking premium on on-policy training, tuned SFT baselines, weight merging, the fused LM head, mid-training a new modality (Carbon-X), cleaner auxiliary gradients (Soft-MTP), two full frontier recipes that split on merging experts (Beam, Inkling 2), MOPD in TRL, and grokking dynamics.
- [Models and architectures](models-architectures/models-architectures.md): looped models, adaptive depth per token, and diffusion language models catching their autoregressive base, the equal-serving-cost architecture ablation (about 2% of loss left), loops under resource constraints, coarse-to-fine generation, and the MoE training handbook.
- [Decision models and System 1 / System 2](decision-models/decision-models.md): the open decision-model stack, four head designs including decision by dynamics, and calibration that is now reported but still about labels, how an open decider is built, deciders placed on streams, tool calls and retrieval, and THX-02's uncertainty-gated thinking.
- [World models and machine reasoning](world-models-reasoning/world-models-reasoning.md): hierarchical and joint world-action JEPAs, sources of abstraction, and world models written as rules and code, and a theorem that good views make separately trained JEPAs share one representation.
- [Agent harness and model routing](agent-harness-routing/agent-harness-routing.md): the harness as a training variable, whether harness choice matters, swarms with persistent memory, routing inside the harness, self-improving harnesses that overfit, interface effects (MCP versus CLI), a controlled harness leaderboard, per-harness adapters, and latent context compression.
- [Cognition, concepts and decision-making](cognition-decision/cognition-decision.md): still thin. Chaos in random recurrent networks, evidence accumulation in streaming deciders, and sleep as the price of plasticity for persistent agents.
- [Inference optimization](inference-optimization/inference-optimization.md): started 11-01. Speculative decoding that hides the drafter's cost, architecture choices as serving choices, quantized samplers in RL, agent-driven inference compilation and tree-indexed sparse attention.
- [Interpretability and safety](interpretability-safety/interpretability-safety.md): started 11-08. Reading concepts from weights, SAE analysis of MoE experts, and safety items from RL runs.

## Reinforcement learning

- [2026-10-09 · Two-thirds of MiMo v2.6's coding tasks leak the answer](reinforcement-learning/2026-10-09-mimo-rl-environments-reward-hacking-audit.md): Vals AI's audit finds the reference fix readable in 1,795 of 2,698 open training tasks, and the model moves to the next leak as each is closed.
- [2026-10-09 · Simulation RL environments, part 1: PortSimEnv](reinforcement-learning/2026-10-09-portsimenv-simulation-rl-environments.md): a berth-planning environment built from real port records, with reward defined as the gap to a solver-proven optimum.
- [2026-10-11 · Bias, variance, and throughput in LLM reinforcement learning](reinforcement-learning/2026-10-11-bias-variance-throughput-llm-rl.md): six named RL algorithms reduced to four design choices, each judged by gradient bias, variance and pipeline throughput.
- [2026-10-11 · ThunderSyncRL](reinforcement-learning/2026-10-11-thundersyncrl.md): compute each trajectory's gradient when its reward arrives. The update is identical to synchronous GRPO and training is up to 1.9 times faster.
- [2026-10-11 · How not to build coding environments](reinforcement-learning/2026-10-11-how-not-to-build-coding-environments.md): one vulnerability task, three perfect scores by finding the published fix, a true score of zero, and a six-step checklist.
- [2026-10-11 · OpenAI's math release as 369 Lean proof environments](reinforcement-learning/2026-10-11-openai-math-lean-rl-environments.md): kernel-checked binary rewards on research-level theorems, hard to game and extremely sparse.
- [2026-11-01 · Score centering stabilizes off-policy RL](reinforcement-learning/2026-11-01-score-centering.md): sampler and trainer mismatch makes the policy gradient drift; subtracting the sampler's mean score fixes it where importance-sampling corrections collapse.
- [2026-11-01 · Unlearnability in RLVR, and Exploration-Distillation](reinforcement-learning/2026-11-01-rlvr-unlearnability-and-exploration-distillation.md): measured with 256 rollouts, stuck prompts are often ones that never got a mixed-reward group; disposable explorers can manufacture correct rollouts.
- [2026-11-01 · Simulation RL environments, part 2: AirOpsEnv](reinforcement-learning/2026-11-01-airopsenv-simulation-rl-environments.md): three agent desks with separate tools run JFK and Boston through real storm days, rewarded against a hindsight-best plan.
- [2026-11-01 · Reinforcement learning for design taste](reinforcement-learning/2026-11-01-rl-for-design-taste.md): two judges, two tastes, length hacking, and both judges preferring the Sonnet-trained model.
- [2026-11-08 · GS1: RL from one rollout per task](reinforcement-learning/2026-11-08-gs1-group-size-one.md): a per-task baseline from similar tasks in the batch, no groups or critic; effective batch size measures baseline quality offline.
- [2026-11-08 · s³ and SwarmEvolve: swarms that learn to communicate](reinforcement-learning/2026-11-08-s3-swarms-and-swarmevolve.md): cooperative multi-agent RL with one team reward beats best-of-N and individual rewards; latent swarms share KV caches.

## Training and fine-tuning

- [2026-10-09 · Multi-teacher on-policy distillation versus SFT](training-finetuning/2026-10-09-multi-teacher-opd-vs-sft.md): four ways to merge expert models reach nearly identical accuracy, and the on-policy one costs 14.8 to 23.1 times the GPU-hours.
- [2026-10-11 · TRL v1.15: the fused LM head](training-finetuning/2026-10-11-trl-fused-lm-head.md): a Triton kernel goes from hidden states to per-token log-probs without building logits, for 4 to 6.9 times longer sequences on the same GPU.
- [2026-11-01 · Carbon-X: mid-training a 14B model to read DNA](training-finetuning/2026-11-01-carbon-x-dna-midtraining.md): a 6-mer DNA vocabulary, 302B tokens of mid-training, SFT and async GRPO; near GPT-6.1 Sol on DNA tasks at about 1/1,800 the cost.
- [2026-11-01 · Multi-token prediction done right (Soft-MTP)](training-finetuning/2026-11-01-soft-multi-token-prediction.md): the MTP gradient is a KL self-distillation term plus noise; a one-line straight-through change keeps only the KL term.
- [2026-11-08 · Beam and Inkling 2 Small: two frontier recipes, two endings](training-finetuning/2026-11-08-beam-and-inkling-2-recipes.md): Beam merges RL experts by full-vocabulary MOPD; Inkling 2 runs one joint, score-centered RL job. Full recipes for both.
- [2026-11-08 · MOPD in TRL, token imbalance, and StepX-OPD](training-finetuning/2026-11-08-mopd-in-trl-and-stepx-opd.md): multi-teacher on-policy distillation as a TRL feature; token-averaged loss starves short-answer domains.
- [2026-11-08 · Subspace crystallization in grokking (Lossfunk)](training-finetuning/2026-11-08-subspace-crystallization-grokking.md): rank compression follows the grokking onset, and forcing low rank early does not speed it.

## Models and architectures

- [2026-10-09 · ALoDLM: adaptively looped diffusion language models](models-architectures/2026-10-09-alodlm-adaptively-looped-diffusion-lm.md): a diffusion language model with a learned exit gate that gives hard tokens more latent passes and beats its autoregressive base on average.
- [2026-11-01 · I tried every LLM architecture change since 2020](models-architectures/2026-11-01-architecture-ablations-since-gpt3.md): 1,129 runs at equal serving cost; MoE and linear attention are the wins, and only about 2% of loss is left for architecture.
- [2026-11-01 · How to loop your transformer, and scaling laws for looped MoE](models-architectures/2026-11-01-how-to-loop-your-transformer.md): loop the full model when parameters bind, a middle block when FLOPs bind, and pay at decode time.
- [2026-11-01 · Next-Concept Modeling](models-architectures/2026-11-01-next-concept-modeling.md): generate a coarse code stack level by level, 10 to 31 times faster than diffusion LMs at matched size.
- [2026-11-08 · The Ultimate MoE Training Handbook](models-architectures/2026-11-08-moe-training-handbook.md): Hugging Face's 800K-GPU-hour MoE guide; all-to-all checks, parity runs, fp32 routers and a ten-model router survey.

## Decision models

- [2026-10-09 · Open d1 and "Train your own decision model"](decision-models/2026-10-09-open-d1-and-train-your-own-decision-model.md): Liquid's open decider weights and Unsloth's recipe for converting an LLM into a decision model, with calibration still about labels and not outcomes.
- [2026-10-11 · Vega: a decision model that rolls a ball down a hill](decision-models/2026-10-11-vega-physics-decision-model.md): a frozen reader plus a small physics engine. Less accurate than Jev and better calibrated, with confidence read from how the particle settles.
- [2026-11-01 · Decision models enter the loop: RightNow, JevAct, DecisionRAG](decision-models/2026-11-01-decision-models-enter-the-loop.md): deciders on streaming input, on agent tool calls and on retrieval paths, plus how an open decider is built.
- [2026-11-08 · THX-02, Drex and DPDM: decision models that decide when to think](decision-models/2026-11-08-thx-02-drex-and-dpdm.md): a 4.5B decider that thinks only when unsure and a gate says reasoning helps, trained with proper scoring rules; plus two open decider families.

## World models and machine reasoning

- [2026-10-09 · H-JEPA: hierarchical world models for visual planning](world-models-reasoning/2026-10-09-h-jepa-hierarchical-world-models.md): stacked latent world models plan top-down, and higher levels learn to keep slow state and drop fast detail.
- [2026-10-11 · Memento 3: model-based recursive self-improvement through reflective rulebooks](world-models-reasoning/2026-10-11-memento-3-code-as-world-model.md): a frozen LLM keeps its world model as a rulebook plus compiled code and revises both from prediction errors. Clears all 25 public ARC-AGI-3 games.
- [2026-10-11 · LeWAM: end-to-end world and action modeling with JEPAs](world-models-reasoning/2026-10-11-lewam-joint-world-action-jepa.md): one JEPA predicts the next latent and proposes actions, so planning searches where good actions are expected and runs 32.3 times faster.
- [2026-11-01 · Proving and improving the Platonic Representation Hypothesis with JEPAs](world-models-reasoning/2026-11-01-platonic-representation-theorem-jepa.md): good views make separately trained JEPAs learn one representation up to a rotation; a 109M text JEPA out-aligns 72B LLMs.

## Agent harness and model routing

- [2026-10-09 · Language model harnesses are compositional generalizers](agent-harness-routing/2026-10-09-harness-as-compositional-generalizer-rlm.md): an RL-trained Recursive Language Model carries short-task training to tasks 8 to 32 times longer, which the plain transformer does not.
- [2026-10-09 · RSIGym](agent-harness-routing/2026-10-09-rsigym.md): a service-based environment where a research agent tunes data, training settings and harness under one budget. Harness-only edits gave a clear gain and data-only edits barely moved the score.
- [2026-10-09 · Recursive Game Creator](agent-harness-routing/2026-10-09-recursive-game-creator.md): a game-generation harness whose Player writes code to play the game, so play experience can be assessed on every iteration.
- [2026-10-11 · GitSwarm: decentralized compounding inference](agent-harness-routing/2026-10-11-gitswarm-compounding-inference.md): hundreds of agents share one Git repository with no planner, and score keeps rising with workers. Includes Prime Agent's Rust rewrite and a component study of coding harnesses.
- [2026-11-01 · Self-improving harnesses, and why the interface matters](agent-harness-routing/2026-11-01-harness-self-improvement-and-interfaces.md): Harness², RRSI, RSIHub and FlashRSI evolve harnesses with frozen weights and find overfitting; MCP versus CLI with identical capabilities diverges in 94.3% of episodes.
- [2026-11-08 · Harness adapters, the Harness Leaderboard, Harness-S and EnvOpt](agent-harness-routing/2026-11-08-harness-adapters-leaderboard-harness-s.md): per-harness LoRAs trained with guarded RL, nine harnesses at a fixed model, sibling-harness rescue of failed RL groups, and workspace optimization.
- [2026-11-08 · Tools Need Not Speak in Text (Coca-Cola)](agent-harness-routing/2026-11-08-latent-context-compression-coca-cola.md): tool outputs compressed into latent tokens trained to preserve the next action; 70% to 89% fewer tokens.

## Inference optimization

- [2026-11-01 · JetSpec++: foresight parallel drafting with self refinements](inference-optimization/2026-11-01-jetspec-plus-plus.md): draft the next block on a second GPU while the current one is verified; 7.45 times autoregressive decoding on Qwen3-8B, lossless.

## Cognition, concepts and decision-making

- [2026-11-08 · Agents that sleep](cognition-decision/2026-11-08-agents-that-sleep.md): Anthropic's offline "dreaming" for Claude's memory and Haber and Tononi's selectionist argument that continual learners must pay for plasticity with sleep.

## Interpretability and safety

- [2026-11-08 · Sparks of weight-space programming](interpretability-safety/2026-11-08-weight-space-programming.md): GPT-6 Astra reads what small networks compute from raw weights and edits weights to fix them, including a 0.016% edit that lifts a 0.8B model's MATH-500 from 7.9% to 48.1%.

## Daily digests and Media Zone

- [Digest 2026-10-04](daily-digest/2026-10/2026-10-04.md) · [Digest 2026-10-09](daily-digest/2026-10/2026-10-09.md) · [Digest 2026-10-11](daily-digest/2026-10/2026-10-11.md) · [Digest 2026-11-01](daily-digest/2026-11/2026-11-01.md) · [Digest 2026-11-08](daily-digest/2026-11/2026-11-08.md)
- [Media Zone 2026-10-09](media-zone/2026-10/2026-10-09.md) · [Media Zone 2026-10-11](media-zone/2026-10/2026-10-11.md) · [Media Zone 2026-11-01](media-zone/2026-11/2026-11-01.md) · [Media Zone 2026-11-08](media-zone/2026-11/2026-11-08.md)
