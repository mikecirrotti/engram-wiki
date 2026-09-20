---
type: style_guide
scope: tells
updated: YYYY-MM-DD
---

# Tells

The patterns that make writing read as machine-generated. [[style/voice]] says what to do; this
file says what to avoid, and it is about *pattern* rather than vocabulary. Banned-word lists catch
corporate filler, which was the 2015 failure mode. Nothing there catches the 2026 one.

Read this before drafting anything that leaves the repo. Run `style/slopcheck.py` on the draft
before presenting it (once you have built the checker).

## The rule that governs the rest

No single pattern below convicts a draft. Careful writers use em dashes. Formal arguments stack
transitions. A short letter has low lexical variety because it is short. Every signal here has an
innocent explanation on its own.

Convergence is the fingerprint. Three or four of these failing at once inside the same few hundred
words is what a reader picks up on, even a reader who could not name a single one of them. Fix the
cluster, not the instance.

## Architecture tells

These are the loudest. A reader clocks the shape of a page before reading a word of it.

<!-- Add the patterns you notice in your own AI-generated drafts. Common ones:

- **Headings imposed on an argument.** A letter to a neighbor with eight section headers announces
  itself. Not a ban on structure: a section label that carries a verdict rather than a topic, over
  content that genuinely has parts, can be fine. Count is not the test.
- **Tables where prose belongs.** A comparison grid in a personal document is damning.
- **Bolded lead-ins on list items.** "- **Option 1 -- put it on record.**" is a slide, not a
  sentence.
- **"At a glance" summaries** and any structure whose job is to restate what was already said.
- **Symmetry.** Two options presented at identical length, three bullets under each heading, every
  section the same size. Real documents are lopsided because real arguments are lopsided.

The test: would you have typed this into an email client at 9pm? If the answer needs a build
step, the architecture is wrong.
-->

- 

## Rhetorical tells

<!-- Common ones:

- **The antithesis flip.** "It's not X, it's Y." This is the strongest single marker in current
  detection. Usually the fix is to cut the first half and keep the conclusion.
- **Tricolons.** Three-item lists that arrive in a rhythm. One per page is fine. Two is a pattern.
- **Summative recaps.** A sentence at the end of a paragraph that restates the paragraph.
- **Engineered closers.** A line at the end of a section built to be quotable. Good line. Wrong
  place, every time.
- **Signposting.** "What this is," "Here's the thing." Say the thing instead of announcing it.
-->

- 

## How this file grows

Start empty. After your first few drafts, read them against your own writing samples in
`style/corpus/` and note the differences. The patterns that distinguish AI output from your real
writing are the tells that belong here.

Every rule added should record the date and the draft that prompted it, so you can judge whether
the rule was derived from enough evidence. Rules calibrated against your corpus are stronger than
rules borrowed from someone else's anti-slop guide.

If a rule flags a genuine sample of your own writing in `style/corpus/`, the rule is wrong.
Remove it or narrow it. The corpus is the authority on what your voice actually sounds like.
