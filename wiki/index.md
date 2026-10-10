# Wiki Index

Catalog of all pages in this wiki. Updated automatically on every ingest.

---

## Concept pages

- [Reinforcement learning](reinforcement-learning/reinforcement-learning.md): RL environments as shared infrastructure, quiet reward-design failures, and two defences against them.
- [Training and fine-tuning](training-finetuning/training-finetuning.md): the shrinking premium on on-policy training, tuned SFT baselines, and weight merging.
- [Models and architectures](models-architectures/models-architectures.md): looped models, adaptive depth per token, and diffusion language models catching their autoregressive base.
- [Decision models and System 1 / System 2](decision-models/decision-models.md): the open decision-model stack, three head designs, and the unresolved calibration gap.
- [World models and machine reasoning](world-models-reasoning/world-models-reasoning.md): hierarchical JEPAs and three sources of abstraction (timescale, factor, external program).
- [Agent harness and model routing](agent-harness-routing/agent-harness-routing.md): the harness as a training variable, whether harness choice matters, and multi-agent systems as context engineering.
- [Cognition, concepts and decision-making](cognition-decision/cognition-decision.md): no sources ingested yet.

## Reinforcement learning

- [2026-10-09 · Two-thirds of MiMo v2.6's coding tasks leak the answer](reinforcement-learning/2026-10-09-mimo-rl-environments-reward-hacking-audit.md): Vals AI's audit finds the reference fix readable in 1,795 of 2,698 open training tasks, and the model moves to the next leak as each is closed.
- [2026-10-09 · Simulation RL environments, part 1: PortSimEnv](reinforcement-learning/2026-10-09-portsimenv-simulation-rl-environments.md): a berth-planning environment built from real port records, with reward defined as the gap to a solver-proven optimum.

## Training and fine-tuning

- [2026-10-09 · Multi-teacher on-policy distillation versus SFT](training-finetuning/2026-10-09-multi-teacher-opd-vs-sft.md): four ways to merge expert models reach nearly identical accuracy, and the on-policy one costs 14.8 to 23.1 times the GPU-hours.

## Models and architectures

- [2026-10-09 · ALoDLM: adaptively looped diffusion language models](models-architectures/2026-10-09-alodlm-adaptively-looped-diffusion-lm.md): a diffusion language model with a learned exit gate that gives hard tokens more latent passes and beats its autoregressive base on average.

## Decision models

- [2026-10-09 · Open d1 and "Train your own decision model"](decision-models/2026-10-09-open-d1-and-train-your-own-decision-model.md): Liquid's open decider weights and Unsloth's recipe for converting an LLM into a decision model, with calibration still about labels and not outcomes.

## World models and machine reasoning

- [2026-10-09 · H-JEPA: hierarchical world models for visual planning](world-models-reasoning/2026-10-09-h-jepa-hierarchical-world-models.md): stacked latent world models plan top-down, and higher levels learn to keep slow state and drop fast detail.

## Agent harness and model routing

- [2026-10-09 · Language model harnesses are compositional generalizers](agent-harness-routing/2026-10-09-harness-as-compositional-generalizer-rlm.md): an RL-trained Recursive Language Model carries short-task training to tasks 8 to 32 times longer, which the plain transformer does not.
- [2026-10-09 · RSIGym](agent-harness-routing/2026-10-09-rsigym.md): a service-based environment where a research agent tunes data, training settings and harness under one budget. Harness-only edits gave a clear gain and data-only edits barely moved the score.
- [2026-10-09 · Recursive Game Creator](agent-harness-routing/2026-10-09-recursive-game-creator.md): a game-generation harness whose Player writes code to play the game, so play experience can be assessed on every iteration.

## Daily digests and Media Zone

- [Digest 2026-10-04](daily-digest/2026-10/2026-10-04.md) · [Digest 2026-10-09](daily-digest/2026-10/2026-10-09.md)
- [Media Zone 2026-10-09](media-zone/2026-10/2026-10-09.md)
