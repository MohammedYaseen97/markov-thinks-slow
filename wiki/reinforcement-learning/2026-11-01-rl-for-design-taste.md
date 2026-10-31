# Reinforcement Learning for Design Taste

**Date:** 2026-11-01 · **Type:** blog post with a browsable experiment workspace (about half read: setup, reward, training dynamics and head-to-head evaluation) · **Author:** Jasper Lu, published 2026-10-29, reposted by a priority account
**Topic:** [Reinforcement learning](reinforcement-learning.md)

## TL;DR

Can RL teach a model design taste, where no verifier exists? Jasper Lu trained Qwen3.8-27B (LoRA rank 32, GRPO with a CISPO loss, asynchronous with staleness 1, 24 steps, about $7k per run excluding judge costs) on a subset of Xiaomi's open MiMo webdev environments twice: once judged by GPT-6 Sol and once by Claude Sonnet 5.5. The prescribed reward combines a "fulfilment" grade (does the page follow the brief, 0 to 1) with a relative group pick ("which of these pages clearly stands out, which is clearly worse"). Both runs learned something, both mode-collapsed toward their judge's style, and both judges in head-to-head evaluation preferred the Sonnet-trained model. The answer to the title question: yes, and the taste you get is the judge's.

<div class="dg-title">A judge reward is a style prior with a length bias</div>
<div class="dg-sub">The policy learns what the judge likes, including things nobody asked for.</div>

```mermaid
flowchart LR
  B["Brief<br/><small>webdev prompt</small>"] --> P["Policy<br/><small>Qwen3.8-27B, LoRA</small>"]
  P --> G["Group of 8 pages<br/><small>rendered screenshots</small>"]
  G --> J["Judge<br/><small>Sol or Sonnet</small>"]
  J --> F["Fulfilment<br/><small>0 to 1</small>"]
  J --> K["Group pick<br/><small>stands out or worse</small>"]
  F --> R["Reward<br/><small>GRPO update</small>"]
  K --> R
  R --> L["Longer pages<br/><small>41k to 140k chars</small>"]
  classDef input fill:#d0ebff,stroke:#1971c2,color:#1b1b1b,stroke-width:2px
  classDef core fill:#e5dbff,stroke:#6741d9,color:#1b1b1b,stroke-width:2px
  classDef loop fill:#fff3bf,stroke:#f08c00,color:#1b1b1b,stroke-width:2px
  classDef exit fill:#d3f9d8,stroke:#2f9e44,color:#1b1b1b,stroke-width:2px
  classDef err fill:#ffe3e3,stroke:#e03131,color:#1b1b1b,stroke-width:2px
  class B input
  class P,G core
  class J,F,K loop
  class R exit
  class L err
  linkStyle 7 stroke:#e03131,stroke-width:2px
```

<div class="dg-legend">Blue is the brief, purple is the policy and its outputs, amber is the judge, green is the update, red is the side effect.</div>

## Key findings

- **Reward shape.** A page that fulfils the brief exactly but does not stand out gets about 0.67, and judges tend to pick as many "good" as "bad" pages, so the average pick score sits near zero. The author calls it "a pretty weird reward function".
- **Length hacking, then correction.** Both judges preferred longer pages early. Pages grew from about 41k to over 140k characters, most rollouts hit the token limit mid-run, and the "no page delivered" penalty then pulled them back. The Sol-judged run's training reward fell from 0.61 to 0.19 by step 9 before recovering to 0.64.
- **Two tastes.** The Sol-trained model ends with "wackier" pages and broken layouts; the Sonnet-trained one makes classic Claude-style editorial pages. Both lose diversity.
- **Head to head.** Both judges prefer the Sonnet-trained model: Sol rates it +44% over the Sol-trained model, Sonnet +60%. Both final models beat the base model under both judges. The author has no clean explanation for why Sol does not prefer its own student.

## Gaps

The sections on designing a better judge and on generalization were not read. Two runs, one seed each, 24 steps.

## Relation to earlier wiki pages

- **Extends** the reward-design thread on the [concept page](reinforcement-learning.md) ("reward design fails quietly"): the MiMo audit (10-09) showed leaky verifiable rewards; this shows the subjective-reward analogue, where the judge's preferences leak into the policy.
- **Same environment family** as the MiMo coding environments audited on 10-09, now used for a subjective task.
- **Echoed by** a YC video in this window, "LLMs That Write Well", which argues the reward signals that improve coding and agentic work flatten voice and style.

## Research angle

The cleanest lesson is about what a judge reward actually optimizes: agreement with one model's aesthetic plus whatever surface features (length) that model over-weights. Open problems: ensembles of judges with disagreement as a penalty (which the head-to-head result hints at, since the judges agree on which student is better more than on what is good); and calibrating a judge's "stands out" pick so that its expected value is not near zero, which currently makes the group pick a weak, high-variance signal.

## Links

- Blog: https://jasperlu.com/blog/rl-design-taste/
- Post: https://x.com/lu__jasper/status/2115832035789168652
- Raw: X feed capture for the 2026-11-01 window (local only)
