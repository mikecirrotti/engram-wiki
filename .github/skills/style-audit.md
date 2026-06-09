---
type: skill
trigger: "style audit" / "review my style files" / "weekly style review"
updated: YYYY-MM-DD
---

# Skill: style-audit

A proactive complement to feedback-to-wiki. Where feedback-to-wiki is reactive (fires on explicit feedback about a specific draft), style-audit is a standing weekly hygiene pass: scan the week's activity, find the implicit corrections and gaps, and propose targeted updates to the procedural files.

## When to run

Typically at end of week, after the weekly digest is drafted. Can also be triggered ad hoc when the user notices that the assistant has been making the same correctable mistake repeatedly.

## Step 1 — Gather the week's signal

Read the following to find implicit corrections and redirects from this week:

- All `daily/` entries from the past 7 days (look for moments where assistant output was redirected, discarded context was re-added, or the user said "actually..." / "not like that" / "defer" / "different from").
- Any artifact drafts produced this week (check `exports/` for new files).
- `inbox.md` for any captures about how the assistant behaved or should behave.

You are looking for **implicit feedback signals** — not just corrections the user stated explicitly, but patterns visible in the edit history:
- Items that were immediately re-worded after being written
- Context the user had to supply that "should have been known"
- Structural choices that were consistently overridden
- Deferral or scope-narrowing language that recurred

## Step 2 — Read the procedural files

Read all of the following. Do not skip any:

**Style:** `style/voice.md`, `style/slides.md`, `style/memos.md`, `style/slack-and-email.md`, `style/technical-docs.md`, all files in `style/audiences/`

**Preferences:** all files in `preferences/`

**Instructions and skills:** `.github/copilot-instructions.md` (and `CLAUDE.md`), all skill files in `.github/skills/`

## Step 3 — Assess each signal

For each signal from Step 1, determine:

1. **Already captured** — convention exists in a procedural file. Note it; no change needed.
2. **Missing convention** — the signal reveals a gap. Propose an addition.
3. **Contradiction** — the signal conflicts with an existing rule. Flag for the user to resolve.
4. **Stale rule** — a convention that was never relevant this week and may reflect outdated behavior. Flag for potential removal (do not propose deletion unilaterally).

## Step 4 — Produce the assessment

Present a concise summary table, then detailed proposals — each with the file, section, the observed signal, the gap, and the proposed exact text. Keep proposals to single sentences where possible. Match the file's existing voice and bullet style.

## Step 5 — Confirm before acting

**CRITICAL: Do not edit any procedural file until the user explicitly approves.** Apply only what is approved, exactly as worded.

## What this skill does NOT touch

`daily/`, `people/`, `projects/`, `topics/`, `decisions/`, `meetings/`, `indexes/` — content, not process.
