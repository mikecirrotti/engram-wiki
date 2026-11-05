---
name: feedback-to-wiki
description: "Turn one-off feedback on a draft into durable style or preference rules. Use when: the user gives feedback on a draft artifact, or says 'use the feedback-to-wiki skill'."
type: skill
updated: YYYY-MM-DD
---

# Skill: feedback-to-wiki

When the user provides feedback on a draft artifact, act as a standing-instructions gardener: inspect whether the feedback reveals a gap, correction, or new convention that should be recorded in the wiki so the same mistake doesn't recur.

## Step 1 — Understand the feedback

Identify: the artifact type, the audience, the nature of the correction (density, tone, structure, vocabulary, hierarchy, length, framing), and whether it is a **one-time exception** or a **durable rule**. If it's a one-time exception, say so and stop.

## Step 2 — Scan the relevant files

- Always: `style/voice.md`, `style/tells.md`, `style/target.md`
- If addressed to one named person: `style/correspondence.md`
- By artifact type: `style/slides.md`, `style/memos.md`, `style/slack-and-email.md`, `style/technical-docs.md`
- Before deciding a rule is wrong: the register-matched samples in `style/corpus/`. If the feedback
  restores something a rule told you to cut, the rule is the thing that is wrong.
- By audience: all relevant files in `style/audiences/`
- Always: all files in `preferences/`
- If project-specific: the relevant `projects/` file

## Step 3 — Assess gaps

For each file, determine:
1. **Already captured** — convention exists. Note it; no change needed.
2. **Contradiction** — feedback conflicts with an existing rule. Flag explicitly.
3. **Missing convention** — feedback reveals a gap. Propose an addition.

## Step 4 — Propose, then ask

Present the exact proposed text and its location for each change. Explain why. **Never edit a file until the user explicitly approves.** Apply approved changes surgically and bump the `updated:` field.

## Scope guardrails

Only touches `style/`, `preferences/`, and (if relevant) `projects/`. Never edits `daily/`, `decisions/`, `people/`, `topics/`, `meetings/`, or `indexes/` based on artifact feedback.

## Step 5 — Offer the corpus

If the feedback took the form of a rewrite — the user replaced a passage with their own words rather
than describing what was wrong — offer to file their version into `style/corpus/` as a sample.

Phrasing: "Want me to keep your version in `style/corpus/` as a sample?"

Only the user's text becomes a sample. The draft stays in `exports/` and the sample's `note:` names
its path — `style/corpus/README.md` keeps drafted material out of the directory. If the rewrite was
a sent email, ask for the rendered message or a screenshot rather than a paste: bold, bullets,
indentation and links are structure, and a plain-text paste loses them.

This matters more than the rule extraction above. Examples of how the user actually writes steer
drafting more reliably than any rule derived from them, and a rewrite is the cleanest sample there
is: same content, their sentences.

Keep their text exactly as they wrote it. Do not tidy it.

## Step 6 — Offer the pair when there was no rewrite

The feedback may be a verdict with no words attached: *"this sounds like an LLM."* When that happens
and a redraft is later approved without the user rewriting it, the two drafts are a control, not a
sample. Offer to file them side by side in `style/corpus/assisted/` with `authorship: assisted` and
a `note:` carrying what changed between them and the user's verdict in their words. Nothing from an
assisted pair is ever read as an example of the user's voice; it is read as a diff.

Phrasing: "Want me to keep the rejected and approved drafts in `style/corpus/assisted/` as a control?"
