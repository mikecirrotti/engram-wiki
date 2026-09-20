---
type: style_guide
scope: voice
updated: YYYY-MM-DD
---

# Voice

How I write, across every artifact type. The assistant reads this before any drafting task and
offers to extend it from patterns in my edits over time.

For anything that speaks as me to an outside audience -- bio, case study, site copy, LinkedIn,
the opening of a proposal -- read [[style/positioning]] as well. It carries the canonical wording
and the claim boundaries; this file only carries the voice.

For anything that leaves the repo at all, read [[style/tells]] and run `style/slopcheck.py` on the
draft (once both exist). For a letter to one named person, read [[style/correspondence]] if it
exists.

## Default voice

- First person, direct, no marketing tone, no hedging.
- Lead with the point; supporting detail follows.
- Claims arrive with their evidence attached, in the same sentence where possible.
- Prose for reasoning, bullets for genuinely enumerable things.

## Rhythm

This section is intentionally blank until calibrated against your own writing. Add samples to
`style/corpus/` first, then derive rhythm rules from what you actually do -- not from what sounds
good in the abstract.

Common pitfalls when setting rhythm rules without corpus evidence:
- Prescribing short, punchy sentences when your natural writing runs long and loosely joined.
- Borrowing advice from published-essay anti-slop guides that describes a different author.
- Setting sentence-length variation targets that produce writing unlike yours.

Measure first, prescribe second. `style/slopcheck.py` can report the numbers without scoring them
until you have enough evidence to set thresholds.

## Words and phrases I avoid

<!-- Add words you notice yourself or your assistant overusing. Common categories:
     - Corporate filler: "leverage," "synergy," "holistic"
     - Hype: "cutting-edge," "revolutionary," "game-changing"
     - Self-branding: "passionate about," "thought leader"
     - Resume-speak that hides the verb: "responsible for," "helped to"
     - Openers that delay the point: "In today's rapidly evolving landscape"
-->

- 

## Words and phrases I prefer

<!-- These emerge over time. You might have different registers -- a public vocabulary
     for bios and case studies, and a private one for internal notes. Label them.
-->

- 

## How this file grows

This file is not meant to be filled in one sitting. It grows through two mechanisms:

1. **feedback-to-wiki** -- when you give feedback on a draft, the skill extracts conventions from
   your edits and proposes additions here.
2. **style-audit** -- a weekly pass that scans your activity for implicit corrections the style
   files do not yet capture.

Over time, the voice file accumulates a calibrated picture of how you write. Rules added here
should include the date and the evidence (the draft or edit that prompted them), so you can judge
recency and revisit rules that may have been derived from too few samples.
