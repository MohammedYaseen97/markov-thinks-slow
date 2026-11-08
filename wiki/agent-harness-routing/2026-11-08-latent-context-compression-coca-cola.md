# Tools Need Not Speak in Text: Latent Context Compression for Agents (Coca-Cola)

**Date:** 2026-11-08 · **Type:** paper (arXiv 2611.06500, abstract only) · **Cross-source confirmed (HF + Kurate cs.AI #16)** · **Authors:** Yuetong Liu, Zhehao Zhou, Yitong Zhang, Haorui Chen, Jia Li
**Topic:** [Agent harness and model routing](agent-harness-routing.md)

## TL;DR

Agents normally paste raw tool outputs into their context, where long noisy observations raise cost and distract. Pruning and summarization stay in discrete text, which caps compression. Coca-Cola compresses each tool observation into continuous latent tokens placed in the agent's input embedding space. **Action-Preserving Training** aligns the agent's next-action distribution under the full and compressed observations, so the latents keep what changes decisions. On web-search agents across four QA benchmarks and two model families: 70.01% to 89.24% fewer tokens and 24.45% to 55.97% less end-to-end runtime, with task performance consistently improved.

<div class="dg-title">The agent reads embeddings, not tool dumps</div>
<div class="dg-sub">Trained so the next action under compression matches the next action under the full text.</div>

```mermaid
flowchart LR
  T["Tool output<br/><small>long, noisy text</small>"] --> C["Compressor<br/><small>Coca-Cola</small>"]
  C --> Z["Latent tokens<br/><small>in input embedding space</small>"]
  Z --> A["Agent LLM<br/><small>next action</small>"]
  T -.->|training only| F["Full-context agent<br/><small>reference action</small>"]
  F -.->|align| A
  classDef input fill:#d0ebff,stroke:#1971c2,color:#1b1b1b,stroke-width:2px
  classDef loop fill:#fff3bf,stroke:#f08c00,color:#1b1b1b,stroke-width:2px
  classDef core fill:#e5dbff,stroke:#6741d9,color:#1b1b1b,stroke-width:2px
  classDef exit fill:#d3f9d8,stroke:#2f9e44,color:#1b1b1b,stroke-width:2px
  class T input
  class C loop
  class Z,A core
  class F exit
```

<div class="dg-legend">Blue is the raw observation, amber the compressor, purple what the agent sees, green the training reference.</div>

## Gaps

- Abstract only; compression ratio per observation, compressor size and training data not read.
- Web-search QA only; exact-string-sensitive settings such as coding are untested. The compressor is tied to its agent.

## Relation to earlier wiki pages

- **Extends** 11-01's cache-engineering notes (agents dropping and re-positioning their own KV cache) from cache management to representation.
- **Pairs with** [SwarmEvolve](../reinforcement-learning/2026-11-08-s3-swarms-and-swarmevolve.md) (this window): two cases of agents passing information as vectors.
- **Same principle as** decision models ([page](../decision-models/decision-models.md)): keep what changes the action.

## Research angle

- A shared compressor across agents of one family; compression of the agent's own past turns, not just tool outputs.

## Sources

- [Paper](https://arxiv.org/abs/2611.06500)
- Raw: `raw/huggingface/2026-11-08-tools-need-not-speak-in-text-latent-context-compre.md`; `raw/kurate/2026-11-08-cs-ai.md`
