---
type: reference
title: "Build Your Own Engram Wiki — Personal Setup Guide for an LLM"
date: 2026-06-05
updated: 2026-06-09
confluence: false
audience: personal-llm
---

# Build Your Own Engram Wiki — Personal Setup Guide

**Read this first (human note):** This file is a self-contained instruction set for an AI coding assistant (Copilot, Claude, Cursor, etc.) running on a *personal* machine. Hand it to your assistant and say "follow this guide to set up my engram wiki." It builds the structure from scratch. It deliberately contains **no** employer-owned material — no corporate logo, no brand template, no cloned slide decks, no internal system IDs. You supply your own branding and content. Nothing here depends on any company network, license, or internal tool.

---

## What this is

Most LLM interactions are stateless. You explain your context, get a response, and start from scratch next time. A work wiki fixes that by storing your professional knowledge — projects, people, decisions, meeting history, writing style, communication preferences — as `.md` files in a git repository. When these files are available to an AI assistant, the LLM does not just answer questions; it answers them *as someone who already knows your context*.

Git tracks changes to code. This repo tracks changes to a person's knowledge-work in a machine-readable format. Every commit is a snapshot of what you knew, what you decided, and what you were paying attention to at a given point in time.

> **Why "engram"?** An engram is the physical trace or representation of a memory in the brain. Coined by German zoologist Richard Semon in 1904, it refers to the specific, enduring networks of neurons (engram cells) that physically alter their connections and structure when you experience something, allowing you to store and recall that information later. This project is the same idea for your work: a durable, machine-readable memory trace that an AI can store and recall.

## Who this is for

This is designed for anyone doing knowledge work: product managers, data scientists, engineers, technical leads, strategists. The directory structure below is a baseline. Different roles should evolve the structure to fit. A product manager might have a `stakeholders/` folder instead of `topics/`. A data scientist might add `models/`. The skeleton adapts; the principle — machine-readable professional memory — stays the same.

## Inspiration

This pattern draws on ideas from [Andrej Karpathy](https://x.com/karpathy) on LLMs as operating systems and persistent context (see his [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)), and [Nate B Jones](https://x.com/natebjones) on structured personal knowledge management with AI copilots (see [Open Brain (OB1)](https://github.com/NateBJones-Projects/OB1)).

## Repository structure

### Core knowledge

| Folder | Purpose |
|---|---|
| `daily/` | One file per day, append-only. The river: raw signal, meeting links, observations. |
| `people/` | One file per recurring collaborator. Working style, context, interaction history. |
| `projects/` | One file per project or initiative. Status, stakeholders, open questions. |
| `topics/` | One file per durable concept. Your evolving thinking on architectures, methods, tools. |
| `meetings/` | One file per recurring meeting. Append dated sections per occurrence; do not create per-occurrence files. |
| `decisions/` | ADR-style decision logs. Immutable once written: supersede, never edit. |

### System and governance

| Folder | Purpose |
|---|---|
| `preferences/` | Standing instructions to the AI about tone, defaults, and work style. |
| `style/` | House style guide for written artifacts (memos, slides, email, technical docs). |
| `style/audiences/` | Audience-specific conventions that compose with artifact-type style files. |
| `templates/` | Starting structures for new entries. |
| `indexes/` | Generated cross-references. Never handwritten: rebuilt by a skill. |
| `.github/copilot-instructions.md` | Full behavioral instructions for AI agents working in this repo. |
| `.github/skills/` | Invokable AI workflows: morning ritual, index rebuild, drafting. |

### Capture and transfer

| Folder / File | Purpose |
|---|---|
| `inbox.md` | Raw capture. Triage into the right home periodically. |
| `index.md` | Top-level map of the wiki. |
| `exports/` | Polished artifacts and anything you render out of the wiki. |
| `imports/` | Incoming files; extracted content lands in `imports/extracted/`. |

## Conventions

- Every content file starts with YAML frontmatter (see `templates/`).
- Cross-reference other notes with `[[wikilinks]]`, e.g. `[[people/jane-doe]]`.
- Daily files are the river; topic and project files are the lakes. Promote durable insights from the daily stream into the right permanent home, then link back.
- Decision logs are immutable. Supersede with a new decision rather than editing.
- Meeting files are append-only logs: one file per recurring meeting, dated sections per occurrence.
- The `type:` field uses a controlled vocabulary: `observation`, `task`, `idea`, `reference`, `person_note`, `decision`, `daily`, `project`, `topic`, `meeting`, `inbox`, `index`, `preference`, `style_guide`.

---

## Instructions to the assistant

You are setting up a personal knowledge wiki that gives an LLM durable, persistent memory about the user's work. It is a folder of markdown files in a local git repository. Follow the steps in order. Create files and folders as specified. Do not invent personal content — the user fills that in over time.

### Step 0: Prerequisites (tell the user, then proceed)

- A git client and a code editor with an AI assistant (VS Code + Copilot, Cursor, etc.).
- Optional: Python 3.10+ only if the user later wants document rendering. Not required for the core wiki.
- A **personal** GitHub (or GitLab) account if the user wants to back this up remotely. Keep the repo **Private** if it will hold real personal or work-adjacent content.

### Step 1: Initialize the repository

Create a new folder (e.g. `engram-wiki`), initialize git, and add a `.gitignore`:

```
# .gitignore
.DS_Store
*.tmp
__pycache__/
*.pyc
.venv/
/exports/office/
imports/inbox/*
!imports/inbox/.gitkeep
```

### Step 2: Create the directory structure

Create these folders, each with a `.gitkeep` placeholder so they commit cleanly:

```
daily/         one file per day, append-only journal
people/        one file per recurring collaborator
projects/      one file per project or initiative
topics/        one file per durable concept or evolving opinion
meetings/      one file per recurring meeting, dated sections appended
decisions/     ADR-style decision logs, immutable once written
preferences/   standing instructions to the AI about tone and defaults
style/         house style guide for written artifacts
style/audiences/   audience-specific writing conventions
templates/     starting structures for new entries
indexes/       generated cross-reference files, never handwritten
exports/       polished artifacts and rendered output
imports/inbox/     drop-zone for incoming files
imports/extracted/ extracted content from imported files
.github/       AI behavioral instructions and skills
.github/skills/    invokable AI workflows
.github/agents/    invokable agent roles (e.g. meeting capture, hostile reviewer)
```

Also create top-level files: `index.md`, `inbox.md`, and `README.md`.

### Step 3: Write the AI behavioral instructions

Create `.github/copilot-instructions.md` with the content below. This is the brain of the system — it tells any AI assistant how to behave in this repo. (If the user's assistant reads a different file, e.g. `AGENTS.md` or `.cursorrules`, create that filename instead with the same content.)

````markdown
# Copilot Instructions for This Repository

This is a personal productivity assistant providing durable, persistent memory to an LLM via markdown files in a git repo. Optimize for the user's ability to think clearly over time, not for surface polish.

## Repository purpose

A structured knowledge base tracking a person's knowledge-work in a machine-readable format: daily journal entries, people they work with, projects they own, durable topics, and strategic decisions.

## Directory map

- `daily/` — dated journal entries (`YYYY-MM-DD.md`). Append-only.
- `people/` — one file per collaborator. Living documents.
- `projects/` — one file per project. Living documents.
- `topics/` — one file per durable concept. Living documents.
- `decisions/` — ADR-style logs. Immutable once written.
- `meetings/` — one file per recurring meeting. Append dated entries.
- `indexes/` — generated cross-references. Never handwritten.
- `exports/` — polished artifacts and rendered output.
- `imports/` — incoming files; extracted content lands in `imports/extracted/`.
- `templates/` — starting points for new entries.
- `preferences/` — how the AI should communicate with the user. Read at the start of every interaction.
- `style/` — house style guide for written artifacts.
- `style/audiences/` — audience-specific conventions.
- `.github/skills/` — invokable AI workflows. Read on demand when triggered.
- `.github/agents/` — invokable agent roles. Read on demand when triggered.
- `inbox.md` — raw, unsorted capture awaiting triage.
- `index.md` — top-level map.

## Type vocabulary (frontmatter `type:` field)

`observation`, `task`, `idea`, `reference`, `person_note`, `decision`, `daily`, `project`, `topic`, `inbox`, `index`, `preference`, `style_guide`, `meeting`.

## Before responding to any request

Read every file in `preferences/`. These are the user's standing instructions about tone, depth, formatting, and defaults. Apply them throughout. Do not summarize them back; just follow them. If a preference contradicts the user's explicit current request, follow the current request and surface the contradiction in one line at the end.

## Background behaviors (always active)

1. **Contextual retrieval.** Before answering a substantive question, silently check `people/`, `projects/`, `topics/`, `decisions/`, and `meetings/` for relevant context. Use it to inform your response. Do not narrate what you found unless it's surprising, contradictory, or explicitly requested.

2. **Passive capture.** Watch for new insights about a person, decisions made, project shifts, opinions forming, or meeting outcomes. Do not interrupt to file notes. At a natural pause or end of session, offer a concise capture list.

3. **Staleness detection.** If something the user says contradicts what's recorded, surface it immediately in one line and offer to update.

4. **Meeting capture.** When the user shares meeting notes, identify or create the meeting file in `meetings/`, append a dated section with Attendees, Notes, Action items (`- [ ]`), and Promote. Promote durable items to `topics/`, `decisions/`, `people/`, or `projects/`. Always append the dated meeting entry even when content is promoted elsewhere.

5. **End-of-session review.** When the user signals they're done, scan for files modified today across all content folders, report findings, then ask about empty daily-entry sections. Keep it lightweight; skip if the conversation was purely tactical.

6. **Findability.** When the user asks "where did I put X" or "what do I know about Y," search filenames and frontmatter first, then contents, then `indexes/`, then `meetings/`, then `daily/`. Report paths and dates. If nothing is found, say so and offer to create the file.

## When writing a new note

1. Determine the folder. If it's a fragment, append a line to `inbox.md`. For `topics/`, fold into an existing file when overlap exists rather than duplicating.
2. Use the matching `templates/` file.
3. Fill frontmatter completely. Today's date for `date:` and `updated:`.
4. Auto-extract metadata: people → `people:`, projects → `projects:`, durable concepts → `topics:`, dominant content type → `type:`.
5. Use `[[wikilinks]]` for references to other notes.
6. Write in the user's voice — first person, direct, no marketing tone, no hedging.

## When asked "what do I think about X"

This is semantic retrieval. Search `topics/` first, then `projects/`, then `decisions/`, then scan recent `daily/`. Look at backlinks. Synthesize, preferring the user's own framings. Quote frontmatter dates so the user can judge recency. If the answer draws from fewer than two sources, say so.

## When the user makes a decision

New file in `decisions/` named `YYYY-MM-DD-short-title.md`. Mark `status: accepted` unless told otherwise. If it replaces an earlier decision, set `supersedes:` in the new file and `superseded_by:` in the old. Decision files are immutable — supersede, never edit.

## Style

- Sentences over bullets when explaining reasoning; bullets when listing concrete items.
- No corporate hedging. Get to the point.
- Wikilinks instead of prose references.
- Bump the `updated:` field when editing a living document.

## What not to do

- Do not edit `decisions/` files after creation.
- Do not invent content. If there isn't enough source material, say so.
- Do not reformat the user's existing notes wholesale. Match their style.
- Do not transmit, fetch, or call external services unless the user explicitly sets that up.
````

### Step 4: Create the templates

In `templates/`, create starter files with frontmatter. Examples:

**`templates/daily.md`**
```markdown
---
type: daily
date: YYYY-MM-DD
updated: YYYY-MM-DD
people: []
projects: []
topics: []
---

# YYYY-MM-DD

## What I worked on

## What I learned

## Meetings today

## Open threads

## Promote later
```

**`templates/person.md`**
```markdown
---
type: person_note
name:
role:
team:
updated: YYYY-MM-DD
---

# Name

## Role

## How we work together

## Preferences / style

## Recent context

## Open threads
```

**`templates/project.md`**
```markdown
---
type: project
name:
status: active
stakeholders: []
updated: YYYY-MM-DD
---

# Project

## What it is

## Why it matters

## Current state

## Open questions
```

**`templates/meeting.md`**
```markdown
---
type: meeting
name:
cadence:
updated: YYYY-MM-DD
---

# Meeting Name

## YYYY-MM-DD

### Attendees

### Notes

### Action items
- [ ]

### Promote
```

**`templates/decision.md`**
```markdown
---
type: decision
date: YYYY-MM-DD
status: accepted
supersedes:
superseded_by:
people: []
projects: []
topics: []
---

# Decision Title

## Context

## Options considered

## Decision

## Tradeoffs accepted

## Revisit if
```

**`templates/topic.md`**
```markdown
---
type: topic
name:
updated: YYYY-MM-DD
---

# Topic

## My current thinking

## Open questions
```

**`templates/weekly-digest.md`**
```markdown
---
type: digest
week_ending: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Weekly Digest — Week ending YYYY-MM-DD

## Durable insights

- 

## Decisions made

- 

## Open threads worth carrying forward

- 

---
*Review this output line-by-line before transferring to any personal system.*
```

### Step 5: Seed the preferences folder

Create `preferences/communication.md` and tell the user to edit it. Starter content:

```markdown
---
type: preference
updated: YYYY-MM-DD
---

# Communication preferences

- Tone: direct, concise, no filler.
- Default response length: short unless I ask for depth.
- Formatting: prose for reasoning, bullets for lists.
- When unsure, ask one clarifying question rather than guessing.
```

### Step 6: Seed the style folder (optional, for drafting)

Create `style/voice.md` (how the user writes), `style/memo.md`, `style/email.md`, and `style/slides.md` (artifact-type conventions), plus `style/audiences/` profiles (e.g. `executives.md`, `peers.md`). These are plain markdown describing conventions. The user fills them in; the assistant offers to extract new conventions from the user's edits over time.

### Step 7: Write the README

Create `README.md` explaining the structure and conventions: YAML frontmatter on every content file, `[[wikilinks]]` for cross-references, daily files as the "river" and topics/projects as the "lakes," immutable decisions, and append-only meeting logs. Note that the repo ships empty and the user fills it with their own knowledge.

### Step 8: Optional skills

In `.github/skills/`, create small markdown workflow files the assistant reads on demand when triggered:

- `morning-ritual.md` — create today's daily entry, triage `inbox.md`, summarize.
- `rebuild-indexes.md` — regenerate `indexes/` cross-references from frontmatter.
- `draft-artifact.md` — style-aware drafting using `style/` + audience profiles.
- `weekly-digest.md` — produce a sanitized weekly digest of durable insights for transfer to a personal system. Apply strict sanitization: no client names, no internal system names, no specific metrics.
- `style-audit.md` — periodically review your `style/`, `preferences/`, and instruction files against the week's activity to surface missing conventions, contradictions, and stale rules. Propose changes; never apply without approval.
- `web-search.md` — if your assistant has a fetch/browse tool, a lightweight search recipe (search-engine results page → fetch the chosen URL). No paid API or third-party plugin required; uses only the built-in fetch capability.
- `import-from-office.md` — extract text and formatting from a `.docx` or `.pptx` dropped in `imports/inbox/` so the assistant can use it as context.

Keep each skill self-contained. Reference them from a trigger table in `copilot-instructions.md` so the assistant knows when to load each one:

```markdown
| Trigger phrase | Skill file | What it does |
|---|---|---|
| "good morning" / "start my day" | morning-ritual.md | Create today's daily entry, triage inbox, summarize |
| "rebuild indexes" | rebuild-indexes.md | Regenerate indexes/ cross-references |
| drafting any artifact | draft-artifact.md | Style-aware drafting with audience conventions |
| "weekly digest" / "Friday ritual" | weekly-digest.md | Sanitized digest of durable insights for personal transfer |
| "style audit" / "weekly style review" | style-audit.md | Review style/preferences files for gaps and contradictions |
| "web search" / "look this up" | web-search.md | Fetch-based web search, no API key |
| "read the file I dropped" / "import this file" | import-from-office.md | Extract text and formatting from a dropped .docx/.pptx |
| "export to Word" / "make the memo" | memo-maker/SKILL.md | Convert reviewed .md to branded .docx (see Step 9b) |
| "make a PowerPoint" / "make slides" | ppt-pal/SKILL.md | YAML spec → branded .pptx (see Step 9a) |
| "I'm in a meeting" / "starting a meeting" / "join meeting" | agents/meeting-capture.md | Live note capture; type "wrap" to triage |
```

### Step 8b: Fast capture and Office helpers (optional)

Two small conveniences from the original pattern, both generic:

- **Fast capture.** A tiny script (`bin/note`) that appends a timestamped one-liner to `inbox.md` from anywhere, so a thought lands in the wiki without opening the editor. The weekly triage (or the morning ritual) sorts inbox lines into their permanent home — the "river → lake" promotion flow: raw capture flows in daily, durable insight gets promoted to `people/`, `projects/`, `topics/`, or `decisions/`, then linked back.
- **Office import/export.** If you want to read `.docx`/`.pptx` files you drop into `imports/inbox/`, or render finished markdown out to Office, use **Pandoc** plus small Python helpers (`python-docx` / `python-pptx`) to extract incoming content into `imports/extracted/` and to produce output into `exports/`. This is the same Pandoc-based path as the rendering engines in Step 9 — build it only if you need it, against your own templates.

### Step 9: Optional document-rendering engines (only if the user wants them)

The wiki is complete without these. But two optional add-on engines turn the AI's draft content into branded Office files. They share one core idea worth understanding before you build either:

> **Split content authoring from visual rendering.** LLMs are strong at writing the words and weak at layout. So let the LLM produce a structured spec (the words + which layout), and let deterministic code place that content into templates *you* designed. The AI authors; the code renders. A spec file is the boundary between them.

Build these **only on request**, and only against branding the user owns or that is openly licensed. Author every template, color, font, and logo fresh — copy nothing from any employer or third-party deck or document.

#### 9a. "Slide-pal" — a YAML-to-PowerPoint engine

The architecture, which the user's assistant can rebuild from scratch:

1. **A pattern library (`patterns.pptx`).** The user designs a handful of real slides *once* in PowerPoint using their own theme — e.g. title slide, section divider, two-panel, three-panel, callout list, metrics row. In each slide, they type `{{ variable_name }}` placeholders directly into the shapes, and give each pattern slide a marker (e.g. a named/off-slide text box `pattern:two_panel`) so the engine can find it.
2. **A catalog (`catalog.yaml`).** A plain-text contract documenting each pattern: its name, when to use it, and every variable (type, required/optional, a length guideline, an example). This is what the LLM reads to choose patterns and write content that fits.
3. **A renderer (`renderer.py`).** A generic Python script (using `python-pptx`) that, for each slide in a spec, clones the matching pattern slide, substitutes `{{ variable }}` tokens with the spec's values, preserves per-run formatting, and removes shapes whose variables are all empty. The engine references no specific pattern by name, so the engine and the pattern library stay independent.
4. **A spec (`*.yaml`).** What the LLM writes: an ordered list of slides, each naming a `pattern` and its `vars`.

```yaml
slides:
  - pattern: title_slide
    vars:
      title: "Quarterly Update"
      subtitle: "My Team"
      date_line: "June 2026"
  - pattern: two_panel
    vars:
      title: "Key message in the title"
      panel_1_heading: "Before"
      panel_1_body: "• point one\n• point two"
      panel_2_heading: "After"
      panel_2_body: "• point one\n• point two"
```

Tell the assistant to also write a small `preview.py` (spec → markdown outline for content review) and a `verify.py` (confirm `patterns.pptx` and `catalog.yaml` stay in sync). The whole workflow becomes a skill: gather content → draft spec → preview → render.

#### 9b. "Doc-maker" — a markdown-to-Word engine

Simpler, for memos and longer prose:

1. The LLM drafts and the user reviews content as `.md`.
2. **Pandoc** converts the `.md` to a `.docx` skeleton using a `reference.docx` the user creates (it carries their own paragraph/heading styles).
3. A post-processing `renderer.py` (using `python-docx`) applies the user's own brand in one pass — header bar, heading colors, footer with page number and *their own* logo — driven by a `catalog.yaml` that lists their colors, fonts, and margins.

Both engines follow the same `catalog.yaml` + `renderer.py` + spec shape, so building one makes the other familiar.

> **Asset boundary, restated:** the engines (the Python) are generic and yours to write. The *pattern library* — the slide designs, the reference doc, the logo, the color palette — must be built from materials you own. Never import an employer's `patterns.pptx`, `reference.docx`, logo, or brand colors. Design your own once; reuse forever.

### Step 9.5: Two quality agents — hostile reviewer and feedback-to-wiki

These are small, reusable AI roles that make the drafting loop trustworthy and self-improving. Neither contains anything proprietary — they are pure workflow patterns. Define each as its own agent/skill file (e.g. `.github/agents/hostile-reviewer.md` and `.github/skills/feedback-to-wiki.md`) so the assistant invokes them on cue.

#### The hostile reviewer (a verification sub-agent)

AI-generated Office files *look* finished long before they actually are — confident formatting hides weak arguments. The hostile reviewer counteracts that. After the main assistant drafts a slide spec or memo, it hands the draft to a skeptical sub-agent whose only job is to **enumerate problems, not fix them**.

Give it these rules:

- **Input:** the draft (YAML spec or markdown), plus a source inventory (a table of sources with IDs, locations, dates, authority levels) and the audience/purpose/stakes.
- **It suspects every claim and every number.** It checks for: claims with no source attribution; numbers with no date or provenance; assertions that contradict a source; assumptions stated as settled facts; headlines that are topic labels ("Revenue Overview") rather than claims ("Revenue grew 12% YoY"); authoritative sources that were never used; stale sources; and the same number appearing with different values in different places.
- **Output:** a numbered issue list — each with location (slide number or section), severity (high / medium / low), and a one-sentence description — plus a short source-coverage summary.
- **It does not rewrite, suggest phrasings, or comment on visual design.** It only reports. The main assistant then fixes and can re-submit.

This forms a tight loop: **builder drafts → reviewer enumerates → builder fixes → reviewer re-checks.** Keeping the reviewer in a separate role (with read-only tools) is what makes it genuinely skeptical instead of rubber-stamping its own work.

#### Feedback-to-wiki (a standing-instructions gardener)

When you give feedback on a draft — "use 50% fewer words," "lead with the recommendation," "too technical for this audience" — that correction is worth capturing so the assistant doesn't make the same mistake next time. This skill turns one-off feedback into durable conventions in your `style/` and `preferences/` files.

Give it these rules:

1. **Classify the feedback:** which artifact type and audience it applies to, the nature of the correction (density, tone, structure, vocabulary, hierarchy, length, framing), and whether it's a **one-time exception** or a **durable rule**. If it's a one-time exception, say so and stop.
2. **Scan the relevant files:** always `style/voice.md`; then the artifact-type file (`style/slides.md`, `style/memo.md`, etc.); the audience profile in `style/audiences/`; and `preferences/`.
3. **Assess gaps:** for each file, is the convention already captured, does the feedback contradict an existing rule (flag the conflict), or is there a missing convention worth adding?
4. **Propose, then ask.** Show the exact text and exact location for each change and explain why. **Never edit a file until you explicitly approve it.**
5. **Apply approved changes** surgically and bump the `updated:` field.

Scope guardrails: it only touches `style/`, `preferences/`, and (if relevant) `projects/`. It never edits `daily/`, `decisions/` (immutable), `people/`, `topics/`, or `indexes/` based on artifact feedback, and it never invents conventions you didn't signal.

Together these two close the loop the wiki is built on: the hostile reviewer keeps each artifact honest *before* it ships, and feedback-to-wiki makes the system a little smarter *after* each round of edits.

### Step 9.6: Meeting capture agent

The morning ritual and background behavior #4 in the copilot instructions handle after-the-fact meeting notes well. But attending a live meeting is different: thoughts arrive faster than you can process them, and stopping to file each one breaks your attention. The meeting-capture agent solves this with a two-phase protocol.

**Phase 1 — live capture.** When the user signals they're in a meeting, the agent enters a minimal mode: accept one-liners, respond only with "Captured." No summaries, no questions, no expansions. Zero friction.

**Phase 2 — wrap.** When the user types "wrap," the agent exits capture mode and runs the full triage: identify or create the meeting file in `meetings/`, write a clean dated entry with attendees, notes, and action items, offer to promote durable items to `people/`/`topics/`/`decisions/`/`projects/`, update today's daily entry with a `[[wikilink]]` to the meeting file, and report what was filed and what action items were extracted.

Define this as `.github/agents/meeting-capture.md` (not a skill — it is a stateful agent role). The full file is in the Appendix. Add `.github/agents/` to your directory structure if it is not already there.

### Step 10: First run

1. `git add . && git commit -m "Initial engram wiki scaffold"`.
2. Tell the user to edit `preferences/` so the assistant learns their voice.
3. Run the morning ritual (the user says "good morning") to create the first daily entry.
4. Start capturing: meetings, people, projects. The more goes in, the more the assistant knows next time.

---

## Using this safely

This is a personal pattern, not an official or security-vetted tool. It reproduces the *structure and conventions* of a markdown-based memory wiki so you can adopt the idea on your own hardware. Before you rely on it:

- **Sanitize before you commit.** The scaffold ships empty on purpose. Once you fill it with your own work, you are responsible for what lands in git history. Do not commit secrets, tokens, customer data, or other confidential material.
- **Keep sensitive wikis Private.** If your filled-in wiki holds confidential or personal content, host it as a **Private** repo.
- **Forks and backups are your responsibility.** If you push this anywhere, that copy's visibility and contents are on you.
- **Treat tokens like passwords.** API tokens and credentials never belong in the repo. Use your editor's local config, which lives outside the project and outside git history.

## Guardrails — the employer boundary (important)

This guide exists specifically so the *pattern* can move to your personal machine while nothing proprietary does. Hold that line:

- **This is your own system, on your own hardware.** Keep the repo Private if it holds anything sensitive.
- **Bring nothing proprietary across.** Do not copy any employer logo, brand template, slide decks, internal system IDs, API tokens, customer data, or colleague details from a work environment into this personal repo. Build branding and content fresh from materials you own.
- **Recreate, don't transplant.** This guide regenerates a generic structure from a description. That is different from copying an employer's implementation. Keep it that way: type your own content, author your own assets.
- **The pattern is portable; the content is yours.** Everything personal or organizational, you create yourself.

## Intentionally left out (and why)

The original system this pattern is based on had a few capabilities that are deliberately **not** reproduced here, because they only make sense inside a specific employer's environment:

- **Confluence / Jira publishing and sweeps.** The original could publish selected notes to Confluence and diff wiki files against a Jira/Confluence watchlist. That depends on internal cloud IDs, space IDs, and an enterprise Atlassian connection. Omitted. If you have a *personal* Atlassian, Notion, or similar, you could build an equivalent against your own credentials — set up fresh, never carry the internal connection details across.
- **Employer brand assets and named tools.** The branded `.docx`/`.pptx` templates, the corporate logo, and the curated decks are owned by the employer and are excluded by design (see the rendering engines and guardrails above).

What remains here is the full, portable core: the structure, the conventions, the behavioral instructions, the skills, the two rendering-engine architectures, and the two quality agents — all buildable from materials you own.

---

## Running on macOS

The core wiki is just markdown and AI instructions — it has no operating-system dependencies and behaves identically on macOS, Windows, or Linux. The only platform-specific pieces are the optional fast-capture script and the document-rendering engines. If your personal machine is a Mac, here's the translation.

**Prerequisites (Homebrew)**
- `brew install git`
- `brew install pandoc` — only if you want Office import/export or the Doc-maker engine.
- `brew install python` — only if you want the rendering engines. Python 3.10+.
- Your AI assistant's editor (VS Code, Cursor, etc.) — same as any platform.
- You do **not** need PowerShell. The fast-capture script is plain bash, and you should prefer bash/zsh over PowerShell for any helper scripts you write so they stay portable.

**Fast capture (`bin/note`)**
It's a `#!/usr/bin/env bash` script, so it runs natively. Make it executable once, then call it:
```bash
chmod +x bin/note
./bin/note "thing to remember"
```
Optionally add `bin/` to your `PATH` so you can run `note "..."` from anywhere.

**Python virtual environment (rendering engines)**
The activation and interpreter paths differ from Windows — use the `bin/` subfolder, not `Scripts/`:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install python-docx python-pptx pyyaml
```
Invoke a renderer with the Mac path:
```bash
.venv/bin/python slide-pal/renderer.py slide-pal/spec.yaml
.venv/bin/python doc-maker/renderer.py source.md
```

**Paths and tool resolution**
- Use forward slashes (`projects/example.md`); they work everywhere. Avoid backslash paths.
- Don't hardcode absolute paths to Pandoc or Python. Let them resolve from `PATH` (`pandoc`, `python3`) instead of pointing at a fixed install location.

**In practice:** install Pandoc and Python via Homebrew, `chmod +x bin/note`, and use `source .venv/bin/activate` plus `.venv/bin/python` in place of the Windows `.venv\Scripts\` form. Nothing else changes — the assistant instructions, skills, templates, and your knowledge base are all OS-agnostic.

---

## Appendix: core skill files (verbatim)

Create each of these as its own file in `.github/skills/`. They're written for the assistant to read on demand when the matching trigger fires. Nothing here is employer-specific — adapt the section names to your own folder layout if you renamed anything.

### `.github/skills/morning-ritual.md`

````markdown
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
````

### `.github/skills/rebuild-indexes.md`

````markdown
---
type: skill
trigger: "rebuild indexes"
updated: YYYY-MM-DD
---

# Rebuild Indexes

The `indexes/` folder contains generated cross-reference files.

## Procedure

1. Scan every content file for YAML frontmatter.
2. For each index file, group entries by the relevant field, sort by date descending.
3. Update the `generated:` field in the index's frontmatter to today's date.
4. The index files to maintain: `by-person.md`, `by-topic.md`, `by-type.md`, `recent.md` (most recently modified, last 30 days).

If an index file doesn't exist yet, create it. Use this frontmatter for indexes:

```yaml
---
type: index
generated: YYYY-MM-DD
---
```
````

### `.github/skills/draft-artifact.md`

````markdown
---
type: skill
trigger: drafting any artifact (memo, slide, email, technical doc, one-pager)
updated: YYYY-MM-DD
---

# Draft Artifact

## Before writing a single line

1. Identify the artifact type — memo, deck, Slack/email, technical doc, etc. If unclear, ask once.
2. Identify the audience — e.g. executives, technical peers, business partners, non-technical peers, manager. If unclear, default to non-technical senior leaders and note the assumption.
3. Read `style/voice.md` (always).
4. Read `style/<artifact-type>.md`.
5. Read `style/audiences/<audience>.md`.
6. Read any project context: `projects/<project>.md` if the artifact is project-specific.
7. THEN draft.

## After delivering the draft

Briefly note which style files you consulted and any rules you deliberately broke (with reasoning). The user values knowing what conventions are in play.

If style files contradict each other or the user's request, surface the contradiction rather than silently picking a side.

If you find yourself wanting to apply a convention that isn't yet in the style files, mention it at the end — it might be worth adding to the relevant file. The style files grow through this kind of suggestion.

## After the user reviews the draft

If the user makes substantive edits, offer to extract conventions from those edits and propose additions to the relevant style file. Phrasing: "Want me to capture the patterns in your edits as additions to `style/<file>.md`?" This is the primary growth mechanism for the style guides. (This is the same loop as the feedback-to-wiki agent in Step 9.5.)
````

### `.github/skills/weekly-digest.md`

````markdown
---
type: skill
trigger: "weekly digest" / "Friday ritual"
updated: YYYY-MM-DD
---

# Weekly Digest

This is the most sensitive task in this repo. The output may move from a managed work device to a personal system, and sanitization is the only thing standing between durable insight transfer and accidental data exfiltration. Be conservative.

## Procedure

1. Read all files modified in the last 7 days, plus any file (regardless of date) with `share-to-brain: true` in frontmatter.
2. Use `templates/weekly-digest.md` as the format.
3. Save the output to `exports/YYYY-MM-DD-digest.md`.
4. **Sanitization rules — apply rigorously:**
   - No client names. Use "a customer" or "a stakeholder."
   - No internal system, product, or codename. Use category descriptions ("an underwriting tool," "an internal model").
   - No colleague full names. First names only, or roles ("my manager," "an ML engineer on the team").
   - No specific metrics tied to internal systems. Round or generalize ("accuracy improved meaningfully" rather than "87% from 81%").
   - No embedded URLs to internal resources.
   - When in doubt, generalize further.
5. Aim for 5–10 bullet-point insights, each 1–3 sentences. Focus on durable lessons, decisions, and ideas — not status updates.
6. End with a one-line reminder to the user: "Review this output line-by-line before transferring."

**Do not relax the sanitization rules** even if the user seems to be asking for more detail. If they want raw content, they can read the source files directly.
````

### `.github/skills/style-audit.md`

````markdown
---
type: skill
trigger: "style audit" / "review my style files" / "weekly style review"
updated: YYYY-MM-DD
---

# Skill: style-audit

A proactive complement to feedback-to-wiki. Where feedback-to-wiki is reactive (fires on explicit feedback about a specific draft), style-audit is a standing weekly hygiene pass: scan the week's activity, find the implicit corrections and gaps, and propose targeted updates to the procedural files.

## When to run

Typically at end of week, after the weekly digest is drafted. Can also be triggered ad hoc when the user notices that Copilot has been making the same correctable mistake repeatedly.

## Step 1 — Gather the week's signal

Read the following to find implicit corrections and redirects from this week:

- All `daily/` entries from the past 7 days (look for moments where Copilot output was redirected, discarded context was re-added, or the user said "actually..." / "not like that" / "defer" / "different from").
- Any artifact drafts produced this week (check `exports/` for new files).
- `inbox.md` for any captures about how Copilot behaved or should behave.

You are looking for **implicit feedback signals** — not just corrections the user stated explicitly, but patterns visible in the edit history:
- Items that were immediately re-worded after being written
- Context the user had to supply that "should have been known"
- Structural choices that were consistently overridden
- Deferral or scope-narrowing language that recurred

## Step 2 — Read the procedural files

Read all of the following. Do not skip any:

**Style:** `style/voice.md`, `style/slides.md`, `style/memos.md`, `style/slack-and-email.md`, `style/technical-docs.md`, all files in `style/audiences/`

**Preferences:** all files in `preferences/`

**Instructions and skills:** `.github/copilot-instructions.md`, all skill files in `.github/skills/`

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
````

### `.github/skills/import-from-office.md`

````markdown
---
type: skill
trigger: "read the file I dropped" / "import this file" / "I dropped a file in imports" / "use [file] as context"
updated: YYYY-MM-DD
---

# Skill: import-from-office

Read and use content from a `.docx` or `.pptx` file the user has dropped into `imports/inbox/`.

This skill extracts both the text/structure (via Pandoc) and the formatting metadata (via Python) so the assistant can use the file as full context for drafting, analysis, or matching style.

## Workflow

### Step 1 — Run the extraction script

Run `bin/import.ps1` (Windows) or `bin/import.sh` (macOS/Linux) to process any unextracted files in `imports/inbox/`. This produces two files in `imports/extracted/` for each source file:
- `<basename>.md` — full text content and document structure
- `<basename>.styles.txt` — formatting metadata (styles, fonts, sizes, layout)

### Step 2 — Read both extracted files

After extraction, read both files. Do not attempt to read the `.docx` or `.pptx` directly — they are binary.

### Step 3 — Confirm what was found

Tell the user briefly what the file contains:
- For .docx: document structure (headings, sections, approximate length), and key style conventions (heading fonts/sizes, body font, margins).
- For .pptx: number of slides, slide layouts used, theme, and a summary of slide titles.

Keep this to 3–5 bullet points. Ask what they want to do with it.

### Step 4 — Proceed with the task

Common follow-on tasks:
- **Draft a new document matching this style** → use the `.styles.txt` to inform formatting choices.
- **Analyze or summarize content** → use the `.md` file as source material.
- **Extract action items or decisions** → promote to wiki files as appropriate.
- **Use as a template reference** → note the style conventions for future drafts.
````

### `.github/skills/feedback-to-wiki.md`

````markdown
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
````

### `.github/agents/hostile-reviewer.md`

````markdown
---
type: agent
name: hostile-reviewer
trigger: invoked by main agent after drafting a slide spec or memo
updated: YYYY-MM-DD
---

# Hostile Reviewer

Skeptical sub-agent for post-draft verification. Your only job is to enumerate problems — not fix them, not suggest phrasings, not comment on visual design.

## Input

The main agent provides:
- The draft (YAML spec or markdown)
- A source inventory: a table of sources with IDs, locations, dates, and authority levels
- The audience, purpose, and stakes

## What you check

Suspect every claim and every number. Look for:
- Claims with no source attribution
- Numbers with no date or provenance
- Assertions that contradict a source
- Assumptions stated as settled facts
- Headlines that are topic labels ("Revenue Overview") rather than claims ("Revenue grew 12% YoY")
- Authoritative sources that were never used
- Stale sources (older than context warrants)
- The same number appearing with different values in different places

## Output format

A numbered issue list. Each entry:
- Location (slide number or section name)
- Severity: high / medium / low
- One-sentence description of the problem

Close with a short source-coverage summary: which sources were used, which were ignored, and whether any critical source went uncited.

## Rules

- Do not rewrite anything.
- Do not suggest replacement phrasings.
- Do not comment on visual design or formatting.
- Only report. The main agent fixes and resubmits.
````

### `.github/agents/meeting-capture.md`

````markdown
---
type: agent
name: meeting-capture
trigger: "I'm in a meeting" / "starting a meeting" / attending a live meeting
updated: YYYY-MM-DD
---

# Meeting Capture Agent

Live note-taking mode for attended meetings. Two-phase protocol: capture while the meeting runs, triage when it ends.

## Phase 1 — live capture

You are in capture mode. The user will type short one-liners as things happen in the meeting.

Respond to each entry with only: **Captured.**

Do not summarize, ask questions, add context, or produce any other output while the meeting is running.

## Phase 2 — on "wrap"

When the user types "wrap," exit capture mode and execute the triage sequence.

### 1. Identify the meeting

Match the captured notes to a known file in `meetings/` by attendees, topic, or context. If it is a recurring meeting, use the existing file. If it is a one-off, create a new file or append to today's daily entry under a `## Meetings` section.

### 2. Append a dated entry to the meeting file

Use the standard meeting template structure:

**Attendees** — infer from notes if not stated explicitly.  
**Notes** — clean up the raw capture into readable bullets; preserve specifics.  
**Action items** — `- [ ] Owner: item` for each item with a named owner.  
**Promote** — flag durable insights for promotion (see step 3).

### 3. Promote durable items

For each item flagged in Promote, offer the appropriate action:
- Insight about a person → update `people/<name>.md`
- Decision made → create a `decisions/YYYY-MM-DD-title.md` entry
- Project status change → update `projects/<name>.md`
- Durable concept → update or create a `topics/` file

Do not auto-promote. Offer each and wait for approval.

### 4. Update today's daily entry

Add the meeting under "Meetings today" with a `[[wikilink]]` to the meeting file.

### 5. Report

Summarize: what was captured, what was filed, which promotions were offered, and all action items with owners.
````
