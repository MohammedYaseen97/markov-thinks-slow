# World Models and Machine Reasoning

> Concept page — updated as new sources are ingested.

Scope: World models, JEPA, reasoning in concept or image space instead of tokens, abduction and discovery in machines.

Last updated: 2026-10-08.

## Current state of knowledge

### Latent world models (JEPA family)

- A JEPA predicts future latent states instead of future pixels. The standing risk is collapse, where every input maps to the same vector. SIGReg is the regularizer used in the current NYU line of work.
- [H-JEPA](2026-10-08-h-jepa-hierarchical-world-models.md) (2026-10-08): a stack of action-conditioned JEPAs, each predicting farther ahead in its own latent space. Planning is top-down with predictions passed down as subgoals. Three levels take Visual AntMaze from 18% to 73% success at lower planner compute.
- Abstraction from horizon: a level asked to predict far ahead drops fast, unpredictable factors and keeps slow task-relevant state. No supervision defines the abstraction.
- Separate latent spaces per level beat a shared space clearly on one of four tasks. The evidence for that specific choice is thin.
- RoboJEPA (Meta, 2026-10-08, abstract only): an 8B JEPA predictor on 12 robot embodiments. Latent rollout error follows a second-order power law in compute and correlates strongly with downstream planning, so it can stand in for real-robot evaluation.
- Caution (Kurate cs.LG, 2026-10-08, first part of overview only): a JEPA can avoid total collapse and still discard an unstable direction a controller must observe. An action-reconstruction objective is proposed to keep it.

### Video world models

- MC-PhysBench (2026-10-08, posts only): scores how long generated video stays physically valid. Best model 30%, and the authors report a no-model baseline beating the video models in 91 of 103 results.
- Odyssey-3 claims the top score on Physics-IQ Verified (2026-10-08). Launch material not read.
- NAVA-WAM (Meta, 2026-10-08): pretrains a robot action policy directly from observation-only video, then post-trains on action-labelled demonstrations.

### Reasoning outside tokens

- Looped models refine a hidden state until it settles, which is a concrete model of slow reasoning without tokens. See [Models and Architectures](../models-architectures/models-architectures.md).
- H-JEPA is the first source here where a slow level and a fast level are separate learned systems with a defined interface (subgoals in latent space).

## Open questions

- Learn the temporal strides of the hierarchy instead of fixing them.
- Replace the top level's goal search with a learned value function.
- Closed-loop results on a physical robot for hierarchical latent planning.
- How to keep task-critical fast variables while discarding nuisance ones. The two JEPA papers of 2026-10-08 pull in opposite directions.
- Whether a hierarchy of latent predictors can represent concepts useful for reasoning about non-physical domains.

## Key sources

- 2026-10-08 · [H-JEPA](2026-10-08-h-jepa-hierarchical-world-models.md)
- Unread, listed on HuggingFace 2026-10-08 without abstracts: Long-WAM (arXiv 2610.10528), UniWAM (2610.02054), Rethinking World-Action Model (2610.02368).
- Kurate, missing from HuggingFace: Think Before You Paint: Recursive Latent Reasoning for Diffusion Models (arXiv 2610.09876).
