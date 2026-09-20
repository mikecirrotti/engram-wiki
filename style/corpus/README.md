# Corpus

Unedited samples of your own writing. **A record: never edited, never cleaned up, never
reformatted.** This is enforced, not suggested -- no assistant should modify these files.

## What goes here

Real writing you actually sent -- emails, memos, letters, messages. Not drafts an AI produced for
you. Not cleaned-up versions. The originals, typos and all.

These are calibration data. The style rules in `voice.md`, `tells.md`, and `target.md` are tested
against these samples. If a rule flags a corpus sample as machine-generated, the rule is wrong and
must be fixed or narrowed. If a concision rule flags a corpus sample as too long, that is working
as intended (the target is tighter than your natural writing).

## How many samples

Five to ten is enough to start measuring. Look for variety: different audiences, different stakes,
different lengths. A short email and a long letter expose different patterns.

## The assisted/ subdirectory

`assisted/` holds AI-generated drafts that you reviewed -- both the ones you approved and the ones
you rejected. These are the *controls*: they let you calibrate which patterns actually distinguish
your voice from the model's. Filing a rejected draft here, alongside an approved one for the same
purpose, is the strongest evidence for a tells rule.

## PROFILE.md

Once you have enough samples, build a `PROFILE.md` that documents what the samples actually show:
sentence-length statistics, vocabulary patterns, structural habits, the markers that are genuinely
yours vs. the ones you borrowed. This file is the evidence base for `tells.md` and `target.md`.

Record corrections here. If a rule derived from the corpus turns out to have been measured wrong,
or was based on too few samples, note the correction with a date. The profile is a forensic log,
not a polished summary.
