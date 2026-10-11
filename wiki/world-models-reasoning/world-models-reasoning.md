# World Models and Machine Reasoning

> Concept page, updated as new sources are ingested.

Scope: World models, JEPA, reasoning in concept or image space instead of tokens, abduction and discovery in machines.

A world model predicts what actions will do, so a planner can test futures before acting. A JEPA (joint-embedding predictive architecture) predicts future latent states instead of future pixels.

## Current state of knowledge

*Last updated 2026-10-11. Two digests feed this page: [10-09](../daily-digest/2026-10/2026-10-09.md) and [10-11](../daily-digest/2026-10/2026-10-11.md).*

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

### 7. An explicit world model: rules plus code, revised by prediction error (10-11)

**[Memento 3](2026-10-11-memento-3-code-as-world-model.md)** has a frozen LLM keep its world model outside the network in two forms: a natural-language rulebook of revisable hypotheses, and executable code compiled from it for prediction and planning. A prediction error triggers reflection, a rule revision, recompilation and verification by exact replay plus a rulebook-fidelity check. The paper is explicit that replay cannot choose among programs that all fit the past, and adds a population of world models that share evidence. On ARC-AGI-3 the single-model agent clears all 25 public games with 44% of the human action count. This extends section 2's "external program" route: the program is the world model itself, and its units are named rules. Held-out results were not in what was read.

### 8. One model that proposes and predicts (10-11)

**[LeWAM](2026-10-11-lewam-joint-world-action-jepa.md)** trains a JEPA with a joint objective: next-latent prediction, action flow matching and SIGReg. At test time it samples actions from its own action branch and scores them with its own dynamics. Mean visual-planning success over ten simulated tasks is 93.5% against 50.9% for the LeWM baseline with a sampling solver, and planning is 32.3 times faster. Action prediction also prevents latent collapse without SIGReg. H-JEPA cut planner cost with hierarchy. LeWAM cuts it with a learned proposal. Nobody has combined them.

### 9. More structure in the latent, and a scaling law in full (10-11)

- **SplitJEPA** (feed thread) divides the latent into an invariant block and a variant block using pairs of observations that share the invariant factors, proves the two subspaces are identified up to block-wise isometries, and reports 71.5% success under an unseen camera rotation against 48.0% for frozen R3M. With timescale (H-JEPA) and factor (JEPA-Anything), that is a third way of structuring a JEPA latent.
- **RoboJEPA** (project page read this window): imagination error follows a second-order power law in compute, extrapolates beyond the fitted scale, and correlates strongly with planning success, at up to 8B parameters across 12 embodiments, with zero-shot planning toward a goal image on a real arm.
- Kurate lists "Preserving Unstable Modes Through Inverse Dynamics in JEPA World Models" (arXiv 2610.07540). Title only.

## Open questions

- Hierarchy depth and strides are set by hand. Learning when to add a level is unsolved.
- Subgoals are points in a continuous latent space, not discrete concepts. There is nothing yet that a fast decider could choose among.
- Do separate latent spaces per level help outside AntMaze?
- Closed-loop planning with a hierarchical JEPA on a physical robot. The 10-09 digest predicts a report within 90 days.
- Can a model learn its own decomposition, the equivalence classes a harness currently supplies by hand?
- Can rule-and-code world models (Memento 3) and latent ones (H-JEPA, LeWAM) be combined, with code for discrete structure and latents for perception?
- How should an agent pick the experiment that best separates surviving hypotheses? Memento 3's population only samples.
- What decides when planning is worth its cost over direct execution? LeWAM measures the planning gain per task but has no such decider.
- Does Memento 3 hold on private ARC-AGI-3 games?

## Key sources

- [2026-10-09 · H-JEPA: end-to-end learning of hierarchical world models for visual planning](2026-10-09-h-jepa-hierarchical-world-models.md)
- [2026-10-11 · Memento 3: model-based recursive self-improvement through reflective rulebooks](2026-10-11-memento-3-code-as-world-model.md)
- [2026-10-11 · LeWAM: end-to-end world and action modeling with JEPAs](2026-10-11-lewam-joint-world-action-jepa.md)
- Covered in the 10-11 digest without a summary page: SplitJEPA, the RoboJEPA project page, Agent Plasticity and Odyssey-3.
- Covered in the [10-09 digest](../daily-digest/2026-10/2026-10-09.md) without a summary page: RoboJEPA, JEPA-Anything and MC-PhysBench.
