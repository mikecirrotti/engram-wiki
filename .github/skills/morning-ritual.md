---
type: skill
trigger: "good morning" / "start my day" / "new day" / creating today's daily entry
updated: YYYY-MM-DD
---

# Morning Ritual

Execute the full sequence without asking for confirmation at each step.

## 1. Gather context (parallel reads)

- Read all files in `preferences/`
- Read `inbox.md`
- Read the most recent daily entry (yesterday's if it exists, or the last available)
- List all files in `meetings/` to identify known recurring meetings

## 2. Create today's daily entry (`daily/YYYY-MM-DD.md`)

Use `templates/daily.md` as the starting structure.

Aggregate a `## Todos` section at the top of the daily file by scanning these sources:

1. **Previous daily files** — carry forward any unchecked `- [ ]` items and unresolved open threads from the most recent daily entry.
2. **Meeting files** — scan all files in `meetings/` for unchecked `- [ ]` action items across all dated entries.
3. **Inbox** — check `inbox.md` for un-struck-through items that look actionable.
4. **People files** — check open threads sections for pending items.
5. **Project files** — check open questions for anything time-sensitive.

Use `- [ ]` checkbox syntax with `[[wikilinks]]` to the source files/people. Group or deduplicate where items overlap. Include the source context so the user knows where each item came from.

**Urgency grouping.** Reason about each item's timeline before listing:

- **Today/Tomorrow:** Hard deadline within 48 hours; someone promised a response today; a meeting depends on this being done; item is blocking someone else's work right now.
- **This week:** Soft target of "this week"; needs scheduling lead time; has been open 3+ days with no movement and a nudge is warranted; prep needed for a meeting later this week.
- **Next week or later:** Recently sent (< 3 days ago) with a longer natural response cycle; explicitly backlog; is a "watch for" or "when you get to it" item; depends on something else first.
- **Tracking others:** Someone else owns the next move and there's no reason to believe they're stuck.

Group todos under those four headers. Items that have been carrying forward unchanged for 3+ days should get a one-line note prompting the user to decide whether to nudge, defer, or drop.

The daily file should also include the standard sections (Meetings today, What I worked on, What I learned, Open threads, Promote later) below the Todos.

## 3. Backfill yesterday (mandatory)

If yesterday's "What I worked on" and "What I learned" sections are empty, infer from inbox notes and context what was done, and **fill them in directly** — do not merely offer. This is not optional. Also update any todo checkboxes in yesterday's entry based on evidence (e.g., inbox notes that confirm completion).

## 4. Triage the inbox

- Identify un-struck items that are promotable (durable enough for `topics/`, `projects/`, or `people/`)
- Identify items that are simply action items (→ today's daily todos)
- **Offer to promote** items that deserve their own file or an update to an existing file — don't auto-promote without offering first
- Strike through items that have been captured elsewhere (in today's daily or promoted files)

## 5. Deliver a brief morning summary

- Count of carry-forward todos and which are highest priority this week
- Today's known meetings or focus areas
- Inbox status (clean vs. items needing promotion)
- Any staleness flags (e.g., a todo that's been carrying forward for 3+ days)

Keep the summary concise — this is a launchpad, not a report.
