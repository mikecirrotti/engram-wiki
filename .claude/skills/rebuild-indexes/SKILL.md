---
name: rebuild-indexes
description: "Regenerate the cross-references in indexes/ by running bin/build-indexes.py. Use when: 'rebuild indexes'."
type: skill
updated: YYYY-MM-DD
---

# Rebuild Indexes

The `indexes/` folder contains generated cross-reference files. They are built by a script, not by
hand, and the nightly workflow in `.github/workflows/build-now.yml` runs it. Run it yourself only
when you want the indexes current before tonight's build, for example right after a large batch of
new notes.

## Steps

1. Run `python3 bin/build-indexes.py`. It prints which indexes it rebuilt, or that nothing changed.
2. If it rebuilt anything, commit `indexes/` like any other change.
3. Report any `*(no person file)*` or `*(no topic file)*` headings that are new. Each one is a
   frontmatter value that does not resolve to a note: either a typo or bare name to fix in the
   source note, or a note worth creating. Offer, do not fix silently.

Never edit an index file by hand. A fix belongs in the source note's frontmatter; the next build
carries it through.

## What the script builds

`by-person.md` (grouped by `people:`), `by-topic.md` (by `topics:`), `by-type.md` (by `type:`),
`recent.md` (notes dated in the last 30 days), and `network.md` (every `person_note` by
`last_contact`, coldest first, with undated people in an "Unknown last contact" group). Scope is
`decisions/`, `meetings/`, `people/`, `projects/`, `topics/`, and top-level `exports/`. The header
of `bin/build-indexes.py` is the full specification.
