---
type: skill
trigger: user gives feedback on a draft artifact / "use the feedback-to-wiki skill"
updated: YYYY-MM-DD
---

# Skill: feedback-to-wiki

When the user provides feedback on a draft artifact, act as a standing-instructions gardener: inspect whether the feedback reveals a gap, correction, or new convention that should be recorded in the wiki so the same mistake doesn't recur.

## Step 1 — Understand the feedback

Identify: the artifact type, the audience, the nature of the correction (density, tone, structure, vocabulary, hierarchy, length, framing), and whether it is a **one-time exception** or a **durable rule**. If it's a one-time exception, say so and stop.

## Step 2 — Scan the relevant files

- Always: `style/voice.md`
- By artifact type: `style/slides.md`, `style/memos.md`, `style/slack-and-email.md`, `style/technical-docs.md`
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
