---
source: farmer/rss
feed: https://simonwillison.net/atom/everything/
date: 2026-10-04
entry_count: 2
---

# RSS: simonwillison-net — 2026-10-04

*2 entries from `https://simonwillison.net/atom/everything/`*

---

## 1. We're going to need default hard budget caps on pretty much everything

**Published:** 2026-10-03 23:34 UTC  
**Link:** [https://simonwillison.net/2026/Oct/3/default-hard-budget-caps/](https://simonwillison.net/2026/Oct/3/default-hard-budget-caps/)

Here's a product feature which the world is going to need a whole lot more of over the coming months and years: default hard budget caps. I'm talking about the feature of pay-by-usage services and APIs that lets you say "after $X/month, cut this thing off and return errors". These need to be hard limits. Soft caps, "after $X/month, send me a warning email", will not cut it.
Coding agents, and personal agents (coding agents wrapped in a less threatening UI), greatly reduce the friction of spinning up code that can do useful things. Sometimes those things cost money - calls to paid APIs, or hosted web applications, or systems that can bill for additional storage and compute.
Nobody wants to wake up to an email sent at midnight warning about a budget limit and find that, while they slept, their rogue service had consumed several hundred (or several thousand) more dollars of usage.
An argument against this is that businesses don't want their hosted applications to start throwing errors because some budget was exceeded. I expect that most businesses and individuals would prefer errors to a surprise $10,000+ bill.
I think hard budget caps need to be the default. If someone wants to live dangerously they should be able to do that, but it needs to be on an opt-in basis. Have a nice, clear checkbox somewhere prominent:

 Remove the budget cap. My application will not be shut down if I exceed the configured budget limit, and I will be responsible for subsequent charges.

The service I most want to see this from is AWS. I've heard plenty of stories from people who refuse to use AWS for personal projects out of (justified) fear that a runaway service might bankrupt them. I've also heard stories from people who didn't anticipate this and ended up seriously burned.
... and it turns out AWS finally launched spending limits a few weeks ago! From their announcement New AWS experience helps builders get started and ship faster on 16th September:

When you're ready to upgrade to a paid plan, you can set a monthly spend limit for your project based on your usage patterns so that you stay within your budget. If a project's usage reaches its spend limit, your project is paused for that month.

See also Create a spend limit in AWS Settings, though that page warns that "We're currently releasing our new experience to a limited number of customers." Here's hoping that hits general availability for existing accounts soon.
Google Cloud launched a similar feature in July, called Spend Caps, which lets you "set a monthly financial cap on specific services within a project". Looks like this is becoming a trend!
In an ideal world, our agents could help with this. It would be great if agents started biasing towards recommending providers with hard budget caps, and warning new and inexperienced builders against deploying applications using uncapped services that might get them into trouble.
    
        Tags: amazon-web-services, ai, coding-agents

---

## 2. September sponsors-only newsletter

**Published:** 2026-10-03 22:00 UTC  
**Link:** [https://simonwillison.net/2026/Oct/3/newsletter/](https://simonwillison.net/2026/Oct/3/newsletter/)

I just sent the September edition of my sponsors-only monthly newsletter. If you are a sponsor (or start a sponsorship now) you can access it here.
This month:

More Fable class models
A pricing war
3D graphics, Blender, and pixel art
LLMs come for mathematics
So many more accidental cyberattacks
The vulnapocalypse comes for Datasette
What I'm using right now
My software releases this month
2026 in LLMs (so far)

Here's a copy of the August newsletter as a preview of what you'll get. Pay $10/month to stay a month ahead of the free copy!

    Tags: newsletter
