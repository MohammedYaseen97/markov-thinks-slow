# World Models and Machine Reasoning

> Concept page, updated as new sources are ingested.

Scope: World models, JEPA, reasoning in concept or image space instead of tokens, abduction and discovery in machines.

A world model predicts what actions will do, so a planner can test futures before acting. A JEPA (joint-embedding predictive architecture) predicts future latent states instead of future pixels.

## Current state of knowledge

*Last updated 2026-10-09. The first sources on this topic arrived in the [10-09 digest](../daily-digest/2026-10/2026-10-09.md).*

### 1. Abstraction can come from the prediction horizon

**[H-JEPA](2026-10-09-h-jepa-hierarchical-world-models.md)** stacks several action-conditioned JEPAs. Each level has its own encoder, predictor and latent space and predicts further ahead than the one below (five, ten and twenty environment steps). Planning runs top-down, and each level's predicted states become subgoals for the level beneath. On a 50-task Visual AntMaze evaluation a three-level model reaches 73.3% success against 18.0% for the flat LeWM baseline, with less planner compute.

Why it works: a long-horizon predictor is penalized for carrying anything it cannot predict that far ahead, so it keeps only slow, task-relevant state. Decoded top-level latents keep the ant's position and the maze layout while leg pose fades. Nobody labels which is which.

Caveats: H-JEPA's edge over HWM (a prior hierarchical method that keeps all levels in one shared latent space) is largest on AntMaze and absent on FourRoom and Push-T. There is no closed-loop run on a physical robot.

### 2. Three sources of coarse units

The 10-09 window offers three different answers to where abstraction comes from:

- **By timescale.** H-JEPA, above.
- **By factor.** JEPA-Anything, surfaced via saved reading, factorizes the latent into orthogonal subspaces with separate predictors and reports gains across seven domains.
- **By an external program.** [Harnesses as compositional generalizers](../agent-harness-routing/2026-10-09-harness-as-compositional-generalizer-rlm.md) gets composition from a harness. The root model sees only a short decomposition and sub-calls handle the detail.

### 3. Scaling

Meta's RoboJEPA reports that latent rollout error follows a power law in compute and tracks real planning performance, at up to 8B parameters across 12 robot embodiments.

### 4. A caution on video world models

MC-PhysBench times how long video world models stay physically valid on simple scenes. The top model scores 30%.

### 5. Reasoning in latent state

[ALoDLM](../models-architectures/2026-10-09-alodlm-adaptively-looped-diffusion-lm.md) lets hard tokens refine a persistent latent over several passes inside one denoising step. It is reasoning in hidden state with a learned amount of effort, though the latent resets between steps.

### 6. A simulator the policy can query

[PortSimEnv](../reinforcement-learning/2026-10-09-portsimenv-simulation-rl-environments.md) gives the agent a plan checker it may call 10 times per episode. A policy that proposes, tests and revises against it is using the checker as a small world model.

## Open questions

- Hierarchy depth and strides are set by hand. Learning when to add a level is unsolved.
- Subgoals are points in a continuous latent space, not discrete concepts. There is nothing yet that a fast decider could choose among.
- Do separate latent spaces per level help outside AntMaze?
- Closed-loop planning with a hierarchical JEPA on a physical robot. The 10-09 digest predicts a report within 90 days.
- Can a model learn its own decomposition, the equivalence classes a harness currently supplies by hand?

## Key sources

- [2026-10-09 · H-JEPA: end-to-end learning of hierarchical world models for visual planning](2026-10-09-h-jepa-hierarchical-world-models.md)
- Covered in the [10-09 digest](../daily-digest/2026-10/2026-10-09.md) without a summary page: RoboJEPA, JEPA-Anything and MC-PhysBench.
