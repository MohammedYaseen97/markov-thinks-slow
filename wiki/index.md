# Wiki Index

Catalog of all pages in this wiki. Updated automatically on every ingest.

---

## Concept pages

- [Reinforcement learning](reinforcement-learning/reinforcement-learning.md): RL environments as shared infrastructure, reward-design failures and their defences, the bias, variance and throughput of RL recipes, and gradient streaming.
- [Training and fine-tuning](training-finetuning/training-finetuning.md): the shrinking premium on on-policy training, tuned SFT baselines, weight merging, and the fused LM head.
- [Models and architectures](models-architectures/models-architectures.md): looped models, adaptive depth per token, and diffusion language models catching their autoregressive base.
- [Decision models and System 1 / System 2](decision-models/decision-models.md): the open decision-model stack, four head designs including decision by dynamics, and calibration that is now reported but still about labels.
- [World models and machine reasoning](world-models-reasoning/world-models-reasoning.md): hierarchical and joint world-action JEPAs, sources of abstraction, and world models written as rules and code.
- [Agent harness and model routing](agent-harness-routing/agent-harness-routing.md): the harness as a training variable, whether harness choice matters, swarms with persistent memory, and routing inside the harness.
- [Cognition, concepts and decision-making](cognition-decision/cognition-decision.md): still thin. One theoretical neuroscience result on chaos in random recurrent networks.

## Reinforcement learning

- [2026-10-09 · Two-thirds of MiMo v2.6's coding tasks leak the answer](reinforcement-learning/2026-10-09-mimo-rl-environments-reward-hacking-audit.md): Vals AI's audit finds the reference fix readable in 1,795 of 2,698 open training tasks, and the model moves to the next leak as each is closed.
- [2026-10-09 · Simulation RL environments, part 1: PortSimEnv](reinforcement-learning/2026-10-09-portsimenv-simulation-rl-environments.md): a berth-planning environment built from real port records, with reward defined as the gap to a solver-proven optimum.
- [2026-10-11 · Bias, variance, and throughput in LLM reinforcement learning](reinforcement-learning/2026-10-11-bias-variance-throughput-llm-rl.md): six named RL algorithms reduced to four design choices, each judged by gradient bias, variance and pipeline throughput.
- [2026-10-11 · ThunderSyncRL](reinforcement-learning/2026-10-11-thundersyncrl.md): compute each trajectory's gradient when its reward arrives. The update is identical to synchronous GRPO and training is up to 1.9 times faster.
- [2026-10-11 · How not to build coding environments](reinforcement-learning/2026-10-11-how-not-to-build-coding-environments.md): one vulnerability task, three perfect scores by finding the published fix, a true score of zero, and a six-step checklist.
- [2026-10-11 · OpenAI's math release as 369 Lean proof environments](reinforcement-learning/2026-10-11-openai-math-lean-rl-environments.md): kernel-checked binary rewards on research-level theorems, hard to game and extremely sparse.

## Training and fine-tuning

- [2026-10-09 · Multi-teacher on-policy distillation versus SFT](training-finetuning/2026-10-09-multi-teacher-opd-vs-sft.md): four ways to merge expert models reach nearly identical accuracy, and the on-policy one costs 14.8 to 23.1 times the GPU-hours.
- [2026-10-11 · TRL v1.15: the fused LM head](training-finetuning/2026-10-11-trl-fused-lm-head.md): a Triton kernel goes from hidden states to per-token log-probs without building logits, for 4 to 6.9 times longer sequences on the same GPU.

## Models and architectures

- [2026-10-09 · ALoDLM: adaptively looped diffusion language models](models-architectures/2026-10-09-alodlm-adaptively-looped-diffusion-lm.md): a diffusion language model with a learned exit gate that gives hard tokens more latent passes and beats its autoregressive base on average.

## Decision models

- [2026-10-09 · Open d1 and "Train your own decision model"](decision-models/2026-10-09-open-d1-and-train-your-own-decision-model.md): Liquid's open decider weights and Unsloth's recipe for converting an LLM into a decision model, with calibration still about labels and not outcomes.
- [2026-10-11 · Vega: a decision model that rolls a ball down a hill](decision-models/2026-10-11-vega-physics-decision-model.md): a frozen reader plus a small physics engine. Less accurate than Jev and better calibrated, with confidence read from how the particle settles.

## World models and machine reasoning

- [2026-10-09 · H-JEPA: hierarchical world models for visual planning](world-models-reasoning/2026-10-09-h-jepa-hierarchical-world-models.md): stacked latent world models plan top-down, and higher levels learn to keep slow state and drop fast detail.
- [2026-10-11 · Memento 3: model-based recursive self-improvement through reflective rulebooks](world-models-reasoning/2026-10-11-memento-3-code-as-world-model.md): a frozen LLM keeps its world model as a rulebook plus compiled code and revises both from prediction errors. Clears all 25 public ARC-AGI-3 games.
- [2026-10-11 · LeWAM: end-to-end world and action modeling with JEPAs](world-models-reasoning/2026-10-11-lewam-joint-world-action-jepa.md): one JEPA predicts the next latent and proposes actions, so planning searches where good actions are expected and runs 32.3 times faster.

## Agent harness and model routing

- [2026-10-09 · Language model harnesses are compositional generalizers](agent-harness-routing/2026-10-09-harness-as-compositional-generalizer-rlm.md): an RL-trained Recursive Language Model carries short-task training to tasks 8 to 32 times longer, which the plain transformer does not.
- [2026-10-09 · RSIGym](agent-harness-routing/2026-10-09-rsigym.md): a service-based environment where a research agent tunes data, training settings and harness under one budget. Harness-only edits gave a clear gain and data-only edits barely moved the score.
- [2026-10-09 · Recursive Game Creator](agent-harness-routing/2026-10-09-recursive-game-creator.md): a game-generation harness whose Player writes code to play the game, so play experience can be assessed on every iteration.
- [2026-10-11 · GitSwarm: decentralized compounding inference](agent-harness-routing/2026-10-11-gitswarm-compounding-inference.md): hundreds of agents share one Git repository with no planner, and score keeps rising with workers. Includes Prime Agent's Rust rewrite and a component study of coding harnesses.

## Daily digests and Media Zone

- [Digest 2026-10-04](daily-digest/2026-10/2026-10-04.md) · [Digest 2026-10-09](daily-digest/2026-10/2026-10-09.md) · [Digest 2026-10-11](daily-digest/2026-10/2026-10-11.md)
- [Media Zone 2026-10-09](media-zone/2026-10/2026-10-09.md) · [Media Zone 2026-10-11](media-zone/2026-10/2026-10-11.md)
