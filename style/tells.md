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
before presenting it. Its thresholds start out tuned to someone else's writing; recalibrate them
against your own samples in `style/corpus/` before trusting a verdict.

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

## Prior art

Five public projects have converged on nearly the same shape, which is itself evidence the shape
is right. The style system here takes something specific from each, named under **Taken** so the
credit is traceable to a file:

- **[hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)** -- a skill for removing
  AI tells from prose. Eight rules, a scoring rubric across five dimensions with a threshold, and a
  pre-delivery checklist. Key idea: a prose gate needs a *score with a threshold* rather than vibes.
  **Taken:** that idea, which is why `style/slopcheck.py` returns a verdict from counted signals
  rather than a judgment call.

- **[jalaalrd/anti-ai-slop-writing](https://github.com/jalaalrd/anti-ai-slop-writing)** -- 50+
  banned words, 35+ banned phrases, 16 banned sentence openers, ten structural constructions,
  sorted into categories. Ships a SKILL.md under 500 lines. Key idea: separating the always-read
  doctrine from the on-demand reference so the drafting path stays cheap. **Taken:** the category
  structure of the `BANNED` list in `style/slopcheck.py`, and the doctrine/reference split between
  this file and the checker.

- **[BioInfo/slopless](https://github.com/BioInfo/slopless)** -- a Claude Code configuration
  system built on hooks over rules, with the line: "an instrument that cannot fail certifies
  whatever you point it at." Key ideas: positive-control testing on planted strings, and deny-list
  scanning that fails loudly rather than silently stripping. **Taken:** planted-string testing,
  which is the structure of `sandbox/tests/run-slopcheck.sh`; its rhythm rules, which are where the
  sentence-length numbers in the checker started; and the "hooks over rules" stance behind
  `hooks/policy/`.

- **[paulscode/no_ai_slop_writing_rules](https://github.com/paulscode/no_ai_slop_writing_rules)**
  -- a portable CLAUDE.md plus skills that Claude reads before writing and then self-checks output
  against. Key idea: the read-before / check-after loop. **Taken:** that loop, which is the shape
  of the draft-artifact skill (`.claude/skills/draft-artifact/SKILL.md`).

- **[slopdetector.org](https://slopdetector.org/blog/signs-of-ai-writing)** -- twelve patterns,
  each with a reproducible threshold. Key idea: *no single number convicts; every pattern has an
  innocent explanation on its own; convergence is the fingerprint.* **Taken:** the starting
  thresholds, and that governing principle, which is why `style/slopcheck.py` keys its verdict off
  how many signals fail at once and why the voice-reviewer looks for clusters.

What is original here, and so carries no one else's endorsement: calibrating every signal against
the writer's own corpus, splitting voice signals from concision signals, demoting borrowed rules
that convicted real human writing to report-only, and the dash, cadence and marker signals that came
out of that calibration.

### Research

- *Can You Make It Sound Like You? Post-Editing LLM-Generated Text for Personal Style*
  ([arXiv:2604.24444](https://arxiv.org/abs/2604.24444);
  [code](https://github.com/ctbaumler/personal_style_postedit)). Editing LLM drafts moves text toward
  the author's style, but the result still sits measurably closer to LLM output than to their
  unassisted writing. Implication: cleaning up a bad draft is structurally weaker than generating
  from the right seed. The corpus matters more than the checker.

- *Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of
  Everyday Authors* ([arXiv:2509.14543](https://arxiv.org/abs/2509.14543), EMNLP 2025 Findings).
  Few-shot consistently beats zero-shot for stylistic alignment. Implication: corpus samples held
  as exemplars steer voice more stably than verbal style instructions extracted from them.

- *Everyone prefers human writers, including AI* ([arXiv:2510.08831](https://arxiv.org/abs/2510.08831)).
  Blind, LLM judges picked AI-written passages 2.6% of the time; with authorship labels revealed,
  17.9%. Implication: any LLM-judge screen of a draft must run blind and be checked against human
  verdicts before it is trusted.

- *The Last Fingerprint: How Markdown Training Shapes LLM Prose*
  ([arXiv:2603.27006](https://arxiv.org/abs/2603.27006)). The reflex toward headings, tables and
  bolded lead-ins is trained in from markdown-heavy training data. Supports the architecture-tells
  category above.

## How this file grows

Start empty. After your first few drafts, read them against your own writing samples in
`style/corpus/` and note the differences. The patterns that distinguish AI output from your real
writing are the tells that belong here.

Every rule added should record the date and the draft that prompted it, so you can judge whether
the rule was derived from enough evidence. Rules calibrated against your corpus are stronger than
rules borrowed from someone else's anti-slop guide.

If a rule flags a genuine sample of your own writing in `style/corpus/`, the rule is wrong.
Remove it or narrow it. The corpus is the authority on what your voice actually sounds like.
