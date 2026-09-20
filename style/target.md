---
type: style_guide
scope: target
updated: YYYY-MM-DD
---

# Target

Three sources pull in different directions, and none of them is the goal on its own.

- **[[style/corpus]]** is how you actually write. It is the authority on voice, and it is *not*
  necessarily the authority on length. Most people take more words to make a point than they need to.
- **[[style/tells]]** is the anti-slop rule set. It keeps drafts from sounding like the model, and
  left alone it can produce clipped, punchy prose that is not yours.
- **Concision** is the thing neither source supplies. The corpus does not model it and the anti-slop
  rules may reach for it by amputating voice.

The target is your voice, saying the same thing in fewer words. That is deliberately not what you
would have written by yourself, and it is deliberately not what the rules alone would produce.

## The two classes of signal

`style/slopcheck.py` (once you build it) should score these separately. The difference is the
whole design:

| | Calibrated to | If it flags a corpus sample |
|---|---|---|
| **Voice** -- em dashes, antithesis flips, headings, banned vocabulary | [[style/corpus]] | **The rule is wrong.** Fix the rule. |
| **Concision** -- mean sentence length, longest sentence, stacked hedges, restatement | this file | **Working as intended.** Do not relax it to fit the samples. |

A voice failure means it sounds like a machine. A concision failure means it sounds like you on a
long day. They are different problems with different fixes, and pooling them is a design mistake.

## Keep

These are voice. Cutting them to save words is the wrong trade. Populate this list from your
corpus once you have samples.

<!-- Examples of what might belong here:
- The one hedge that marks real uncertainty ("I would think," "should," "may")
- The escape hatch at the end of an ask
- The unprompted concession that shows intellectual honesty
- Naming your own limits plainly
-->

- 

## Cut

These are habit, not voice. Populate this from your own sent writing -- the patterns you want
tightened, with before/after examples from your own words.

<!-- Common categories:
- **Stacked hedges.** Keep the first, cut the rest.
- **The restated noun.** If the sentence says the word twice, it is circling.
- **The trailing generality.** The sentence has already landed; the last clause reaches for
  completeness nobody asked for.
- **Doubled synonyms joined by a slash.** Usually one word does the work of both.
-->

- 

## Who does the cutting

Concision is the assistant's job by default. Tighten a draft before showing it, not after. Cut the
hedge that adds nothing; keep the one that marks a guess. Never at the cost of the voice markers
in the Keep list above.
