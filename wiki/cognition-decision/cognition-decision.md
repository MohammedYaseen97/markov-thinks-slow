# Cognition, Concepts and Decision-making

> Concept page, updated as new sources are ingested.

Scope: Human and biological side: dual-process theory, abduction, concept learning, decision neuroscience, theories of the brain.

## Current state of knowledge

*Last updated 2026-11-08 (sections 4 and 5, from the [11-08 digest](../daily-digest/2026-11/2026-11-08.md)). Earlier: 2026-11-01 (light additions, section 3). This page is still thin. Sources on human and biological cognition have been low in volume for three digests, and nothing has yet been read in depth. The single entry below comes from the [10-11 digest](../daily-digest/2026-10/2026-10-11.md).*

### 1. Theories of the brain: chaos in random recurrent networks is extensive (10-11, post and abstract read)

The 1988 model of Sompolinsky, Crisanti and Sommers, a network of N randomly coupled nonlinear neurons that turns chaotic above a critical coupling strength, is a standard model of spontaneous cortical activity and the usual starting point for training recurrent networks on tasks. Its largest Lyapunov exponent (the fastest rate at which a small perturbation grows) was solved in the original paper. The full Lyapunov spectrum, one growth rate per direction, was left open. David Clark's paper ([arXiv 2610.12426](https://arxiv.org/abs/2610.12426)) derives the full spectrum at large N. The steps, as described in his post: express the count of exponents below a threshold as a response function of the tangent dynamics with a minimum-norm condition, recast that as a regularized least-squares problem with one field running forward in time and one backward, and apply the cavity method to reduce it to a self-consistent single-neuron problem. The result shows the chaos is extensive: attractor dimension and entropy rate grow in proportion to N. The abstract credits two AI models as collaborators.

Why it is filed here: it is a result about a model of cortical dynamics, not about machine learning. It says nothing yet about reasoning or decision-making.

### 2. Machine-side items with a cognitive reading (kept on other pages)

- A decision as the settling of a dynamical system, with confidence read from how it settled, is on the [decision models page](../decision-models/decision-models.md) (Vega, 10-11). The resemblance to evidence-accumulation accounts of human choice is our reading, not the author's claim.
- Hypothesis revision from prediction error, in explicit rules, is on the [world models page](../world-models-reasoning/world-models-reasoning.md) (Memento 3, 10-11).
- A machine decider that "holds back until the evidence is there, then commits" on streaming input (RightNow System Zero, 11-01) is an engineering version of evidence accumulation to a bound, as in drift-diffusion models of human choice. No speed-accuracy data was published. See the [decision models page](../decision-models/decision-models.md).

### 3. The 11-01 window: still thin (posts and titles only)

- François Chollet's one-line reminder that dopamine responds most strongly to reward prediction error, not to guaranteed reward (post, no source). This is the standard temporal-difference reading of dopamine and the bridge from this page to the RL page.
- "Large Language Models as a Cognitive Virus" (Tufts and the Santa Fe Institute) models AI dependence as social contagion with a tipping point. Post only.
- Kurate's q-bio.NC board lists "Local learning is all you need: brain-aligned predictive coding networks" (ai_rating 6.5) and "Intrinsic Goals for Autonomous Agents: Hierarchical Exploration Captures Future Volitional Action in Drosophila". Titles only, scores still at the default.

### 4. Sleep as the price of plasticity (11-08, first item read with an engineering counterpart)

**[Agents that sleep](2026-11-08-agents-that-sleep.md).** Ido Haber and Giulio Tononi (Kurate q-bio.NC) argue from the selectionist theory of sleep that persistent agents show the costs of unregulated plasticity (semantic drift, weaker retrieval, spreading errors, full capacity), map sleep's "ringing, resonance and renormalization" onto memory operations, and predict selective consolidation beats instruction-driven consolidation as stores grow. In the same week Anthropic described "dreaming", offline reflection on logs, as Claude's consolidation step, explicitly modelled on hippocampal capture and replay into neocortex, and showed the core skill is judging salience (Fable 5: nine memory files and four Pokémon badges; Sonnet 3.7: 413 files and one). This is the memory half of dual-process thinking: fast capture during action, slow rule extraction offline. Tononi also co-signed a Nature commentary (with Anil Seth and Ned Block) arguing current AI is not conscious and computation alone will not make it so.

### 5. Machine-side items with a cognitive reading (11-08)

- THX-02's uncertainty-gated thinking is a working fast-decider plus slow-reasoner. See the [decision models page](../decision-models/decision-models.md).
- Lossfunk's grokking paper locates the generalization transition in time (compression follows it), a clean case of an abrupt insight-like transition in learning. See the [training page](../training-finetuning/training-finetuning.md).
- Richard Sutton's "robot kindergarten" keynote argues for online trial-and-error learning from experience, as animals learn.

## Open questions

- Does selective consolidation beat instructed consolidation as an agent's memory store grows, with a crossover point? (11-08 prediction, 90 days.)
- Which human-cognition sources should feed this page? The neuroscience board has listed relevant titles for three digests ("Heterarchy in the Brain", "Neural Decoding as Cognitive Inference", a recurrent-dynamics account of perceptual grouping) and none has been read.
- Does settling time in a learned decision dynamic behave like human response time, slower and less confident on hard items?

## Key sources

- [2026-11-08 · Agents that sleep: Anthropic's "dreaming" and Haber and Tononi's selectionist case](2026-11-08-agents-that-sleep.md)
- Covered in the 10-11 digest without a summary page: the Lyapunov spectrum of random recurrent networks (arXiv 2610.12426).
