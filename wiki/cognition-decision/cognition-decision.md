# Cognition, Concepts and Decision-making

> Concept page, updated as new sources are ingested.

Scope: Human and biological side: dual-process theory, abduction, concept learning, decision neuroscience, theories of the brain.

## Current state of knowledge

*Last updated 2026-10-11. This page is still thin. Sources on human and biological cognition have been low in volume for three digests, and nothing has yet been read in depth. The single entry below comes from the [10-11 digest](../daily-digest/2026-10/2026-10-11.md).*

### 1. Theories of the brain: chaos in random recurrent networks is extensive (10-11, post and abstract read)

The 1988 model of Sompolinsky, Crisanti and Sommers, a network of N randomly coupled nonlinear neurons that turns chaotic above a critical coupling strength, is a standard model of spontaneous cortical activity and the usual starting point for training recurrent networks on tasks. Its largest Lyapunov exponent (the fastest rate at which a small perturbation grows) was solved in the original paper. The full Lyapunov spectrum, one growth rate per direction, was left open. David Clark's paper ([arXiv 2610.12426](https://arxiv.org/abs/2610.12426)) derives the full spectrum at large N. The steps, as described in his post: express the count of exponents below a threshold as a response function of the tangent dynamics with a minimum-norm condition, recast that as a regularized least-squares problem with one field running forward in time and one backward, and apply the cavity method to reduce it to a self-consistent single-neuron problem. The result shows the chaos is extensive: attractor dimension and entropy rate grow in proportion to N. The abstract credits two AI models as collaborators.

Why it is filed here: it is a result about a model of cortical dynamics, not about machine learning. It says nothing yet about reasoning or decision-making.

### 2. Machine-side items with a cognitive reading (kept on other pages)

- A decision as the settling of a dynamical system, with confidence read from how it settled, is on the [decision models page](../decision-models/decision-models.md) (Vega, 10-11). The resemblance to evidence-accumulation accounts of human choice is our reading, not the author's claim.
- Hypothesis revision from prediction error, in explicit rules, is on the [world models page](../world-models-reasoning/world-models-reasoning.md) (Memento 3, 10-11).

## Open questions

- Which human-cognition sources should feed this page? The neuroscience board has listed relevant titles for three digests ("Heterarchy in the Brain", "Neural Decoding as Cognitive Inference", a recurrent-dynamics account of perceptual grouping) and none has been read.
- Does settling time in a learned decision dynamic behave like human response time, slower and less confident on hard items?

## Key sources

- Covered in the 10-11 digest without a summary page: the Lyapunov spectrum of random recurrent networks (arXiv 2610.12426).
