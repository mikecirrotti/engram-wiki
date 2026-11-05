---
name: draft-artifact
description: "Style-aware drafting with audience conventions; reports length against the target band and names the cuts. Use when: drafting any artifact (memo, slide, email, technical doc, one-pager)."
type: skill
updated: YYYY-MM-DD
---

# Draft Artifact

## Before writing a single line

1. Identify the artifact type -- memo, deck, Slack/email, technical doc, correspondence, etc. If
   unclear, ask once. **If it is addressed to one named person who knows the user, the type is
   correspondence**, and `style/correspondence.md` governs it. Do not treat it as a deliverable.
2. Identify the audience -- e.g. executives, technical peers, business partners, non-technical
   peers, one named person. If unclear, default to non-technical senior leaders and note the
   assumption.
3. Read the style files in this order:
   - `style/voice.md` (always)
   - `style/tells.md` (always, if it exists and is populated)
   - `style/target.md` (always, if it exists)
   - `style/<artifact-type>.md` (memo, slides, email, technical-docs, correspondence)
   - `style/audiences/<audience>.md`
   - `style/positioning.md` (if the artifact speaks publicly as the user -- bio, case study, site
     copy, social post, proposal introduction). Use the canonical wording verbatim and respect the
     claim boundaries.
4. Read two or three samples from `style/corpus/` matching the register, if any exist, and hold them
   as examples of how the user actually writes. Do not extract rules from them -- the examples
   themselves do the steering, and summarizing them throws that away. **Check what is actually
   present rather than assuming.** If the register you need has no sample, say so plainly in the
   notes. Never claim the corpus was consulted when it was not there.
5. Read any project context: `projects/<project>.md` if the artifact is project-specific.
6. THEN draft.

## Before showing the draft

If `style/slopcheck.py` exists, run it:

```
python3 style/slopcheck.py <draft> --artifact-type <type>
```

It reports two different problems:

- **Voice** -- does this sound like the model wrote it. Fix the cluster before showing it. These
  signals should be calibrated to `style/corpus/`, so if one fires on a corpus sample, the rule is
  wrong and should be reported rather than obeyed.
- **Concision** -- it is the user's voice but longer than it needs to be. Calibrated to
  `style/target.md`, which is usually tighter than the user writes, so these *will* fire on the
  corpus. That is intended.

Without the checker, do the same two passes by hand against `style/tells.md` (no cluster of three or
more tells in one passage) and `style/target.md`.

**Do the cutting before showing the draft, not after.** Cut the stacked hedges, the restated nouns
and the trailing generalities; keep the hedge that marks real uncertainty, the concession and the
escape hatch. Then say what came out and give the word count before and after, so the judgment stays
the user's. A flag you leave standing needs a reason, and "it is their voice" is not one. Cutting
hedges to zero is the opposite failure and just as bad.

**It reports; it never rewrites.** Every signal has an innocent explanation on its own, so read the
flagged lines and decide. A tricolon that is genuinely three things stays.

**The markers no checker can look for.** Every signal a tells list catches is *subtractive* -- it
tests for what should not be there. Nothing tests for the habits that make the prose the user's, so
a draft can score clean while carrying none of them. If `style/corpus/` has a profile or the samples
show recurring habits (how they hedge, how they introduce a term, how they lead into a list, how they
close a letter), name which are present in the draft and which you dropped, and say why. Dropping one
is fine when the register does not want it; dropping all of them is how a draft ends up sounding like
nobody.

Two things to check by hand, because no metric sees them:

- **Architecture.** Would this have been typed in one sitting? Headings, tables and bolded lead-ins
  in something personal are the loudest tell there is.
- **Specificity.** Is there anything in here only this writer could have written? A real detail, a
  digression, an opinion with a temperature. Generated prose is about the subject in general.

For anything public-facing or high-stakes, also invoke `.claude/skills/voice-reviewer/SKILL.md`
on the draft before presenting. It enumerates tells without rewriting.

## After delivering the draft

Briefly note which style files and corpus samples you consulted and any rules you deliberately broke
(with reasoning). The user values knowing what conventions are in play.

If style files contradict each other or the user's request, surface the contradiction rather than
silently picking a side.

If you find yourself wanting to apply a convention that is not yet in the style files, mention it at
the end -- it might be worth adding. The style files grow through this kind of suggestion.

If a draft passes every check and still reads wrong to the user, that is the more valuable signal of
the two. Get the specific reason in their words and put it in `style/tells.md`. The checks are
proxies for exactly that reaction.

## When the user shares their own writing

The third path. Drafting is when the assistant writes; the section below is when the user edits what
it wrote. This is when they hand over something they wrote themselves and want it tightened.

It is mostly about restraint.

- **Report the mean and the longest sentence against the band** in `style/target.md`, if it sets
  one. Report, do not grade. A length band never governs voice.
- **Name the specific cuts, quoting the line each time.** The trailing generality, the stacked
  hedge, the restated noun, the sentence carrying three ideas. Worked before-and-after pairs in
  `style/target.md` are the shape to use, rather than a general note about length.
- **Never touch the voice markers.** The hedge that marks real uncertainty, the escape hatch, the
  unprompted concession, the user's own punctuation habits. When a cut would take one, say so and
  leave it.
- **Never edit a corpus sample.** If what they share is also going into `style/corpus/`, the sample
  is a record and stays exactly as typed, typos included. The tightening advice is for the next thing
  they write.
- **Offer, do not impose.** Something already sent gets feedback only if they ask for it.

If their own writing keeps flagging the same pattern, that is a candidate for the feedback-to-wiki
skill rather than something to repeat every time.

## After the user reviews the draft

**If a draft comes back edited after it was sent, that is the highest-value signal in the loop.** A
sent version is a control the corpus otherwise never has: same content, their sentences. Diff the
two word by word and route what the diff shows -- voice rules to `style/`, and a tension you cannot
resolve to an open question rather than a rule invented from one instance. Then offer the sent text
as a corpus sample. Ask for a screenshot or the rendered message rather than a plain-text paste:
formatting is structure, and pasting flattens it.

If the user makes substantive edits, offer to extract conventions from those edits and propose
additions to the relevant style file. Phrasing: "Want me to capture the patterns in your edits as
additions to `style/<file>.md`?" This is the primary growth mechanism for the style guides (the same
loop as the feedback-to-wiki skill).
