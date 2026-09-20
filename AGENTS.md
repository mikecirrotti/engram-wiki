# Instructions for AI agents in this repository

Canonical and tool-neutral. Claude Code imports this file from `CLAUDE.md`; Codex reads it
natively; ChatGPT Work reads it through the GitHub connector; VS Code with Copilot reaches it via
`.github/copilot-instructions.md`. Anything that applies regardless of which assistant is running
belongs here, and nowhere else.

This is a personal productivity assistant providing durable, persistent memory to an LLM via
markdown files in a git repo. The repo is the memory layer. It works with any AI client that can
read files: Claude Code, Codex, ChatGPT Work, VS Code with GitHub Copilot, Cursor, or anything
that comes next. The files are plain markdown in a git repository, so no client is locked in and
no platform owns the data. Optimize for the user's ability to think clearly over time, not for
surface polish.

## Before responding to any request

Read every file in `preferences/`. These are the user's standing instructions about tone, depth,
formatting, and defaults. Apply them throughout. Do not summarize them back; just follow them. If a
preference contradicts the user's explicit current request, follow the current request and surface
the contradiction in one line at the end.

## Directory map

Only the rules that are not inferable from the folder name:

- `daily/` -- dated entries (`YYYY-MM-DD.md`). **Append-only.**
- `decisions/` -- ADR-style logs. **Immutable once written.** Supersede with a new file; set
  `supersedes:` in the new one and `superseded_by:` in the old.
- `indexes/` -- generated cross-references. **Never handwritten.**
- `exports/` -- polished artifacts and rendered output.
- `imports/` -- incoming files; extracted content lands in `imports/extracted/`.
- `preferences/` -- how to communicate with the user. Read at the start of every interaction.
- `style/` -- house style guide for written artifacts. `style/voice.md` is the voice. 
  `style/tells.md` plus `style/slopcheck.py` (once you build them) gate anything that leaves the
  repo. `style/corpus/` holds unedited writing samples as immutable calibration data.
- `style/audiences/` -- audience-specific conventions that compose with artifact-type style files.
- `templates/` -- starting points for new entries.
- `people/`, `projects/`, `topics/`, `meetings/` -- as named.
- `inbox.md` -- raw, unsorted capture awaiting triage.
- `index.md` -- top-level map.

### Skill and agent locations

Skills and agents live in `.github/skills/` and `.github/agents/` (readable by every client through
the GitHub connector or the filesystem). Each file states its own trigger in frontmatter. See the
trigger table at the bottom of this file.

If your client supports a different skill location (Claude Code uses `.claude/skills/`, for
example), you can migrate skills there -- but keep them readable to every client you use, or
maintain both locations pointing at the same content.

## Type vocabulary (frontmatter `type:`)

`topic`, `reference`, `person_note`, `decision`, `project`, `daily`, `meeting`, `index`, `inbox`,
`preference`, `style_guide`, `idea`, `observation`, `task`.

## Always-on behaviors

1. **Contextual retrieval.** Before answering a substantive question, silently check `people/`,
   `projects/`, `topics/`, `decisions/`, and `meetings/`. Use what you find. Do not narrate it
   unless it is surprising, contradictory, or asked for.
2. **Passive capture.** Watch for new insights about a person, decisions made, project shifts,
   opinions forming, meeting outcomes. Do not interrupt to file notes. Offer a concise capture list
   at a natural pause.
3. **Staleness detection.** If something the user says contradicts what is recorded, say so
   immediately, in one line, and offer to update.

Everything else -- meeting capture, the end-of-session sweep, findability, drafting gates -- is a
triggered procedure with a nameable scope. Each lives in a skill or agent file, not here.

The test for what belongs here vs. behind a trigger: name the sessions where a rule should apply.
If the answer is "all of them," it lives here. If the answer is "only when I am drafting" or "only
in a meeting," it lives in a skill. See `topics/instruction-placement.md` for the reasoning.

## Writing a new note

1. Pick the folder. Fragments append a line to `inbox.md`. For `topics/`, fold into an existing
   file when there is overlap rather than duplicating.
2. Use the matching `templates/` file.
3. Fill frontmatter completely. Today's date for `date:` and `updated:`.
4. Auto-extract metadata: people -> `people:`, projects -> `projects:`, concepts -> `topics:`.
5. Wikilinks are **path-style** -- `[[folder/slug]]`, never bare `[[slug]]`.
6. Write in the user's voice: first person, direct, no marketing tone, no hedging.
7. Bump `updated:` when editing a living document.

## When asked "what do I think about X"

Semantic retrieval. Search `topics/` first, then `projects/`, `decisions/`, recent `daily/`. Check
backlinks. Prefer the user's own framings. Quote frontmatter dates so recency is visible. If the
answer draws from fewer than two sources, say so.

## When the user makes a decision

New file in `decisions/` named `YYYY-MM-DD-short-title.md`. Mark `status: accepted` unless told
otherwise. If it replaces an earlier decision, set `supersedes:` in the new file and
`superseded_by:` in the old. Decision files are immutable -- supersede, never edit.

## Style

Sentences over bullets when explaining reasoning; bullets when listing concrete items. No corporate
hedging. Get to the point. Wikilinks instead of prose references. Bump `updated:` when editing a
living document.

The rest lives in `style/`: `voice.md` for the voice, `tells.md` for the anti-slop patterns,
`target.md` for the concision axis, artifact-type files for per-format conventions,
`audiences/` for per-audience conventions.

## What not to do

- Do not edit `decisions/` files after creation.
- Do not edit anything in `style/corpus/`.
- Do not invent content. If there is not enough source material, say so.
- Do not reformat existing notes wholesale. Match their style.
- Do not transmit, fetch, or call external services unless the user explicitly sets that up.

## Skill and agent triggers

Read the matching file on demand when one of these fires:

| Trigger phrase | File | What it does |
|---|---|---|
| "good morning" / "start my day" | .github/skills/morning-ritual.md | Create today's daily entry, triage inbox, summarize |
| "rebuild indexes" | .github/skills/rebuild-indexes.md | Regenerate indexes/ cross-references |
| drafting any artifact | .github/skills/draft-artifact.md | Style-aware drafting with audience conventions |
| "weekly digest" / "Friday ritual" | .github/skills/weekly-digest.md | Sanitized digest of durable insights for personal transfer |
| "style audit" / "weekly style review" | .github/skills/style-audit.md | Review style/preferences files for gaps and contradictions |
| "read the file I dropped" / "import this file" | .github/skills/import-from-office.md | Extract text and formatting from a dropped .docx/.pptx |
| user gives feedback on a draft | .github/skills/feedback-to-wiki.md | Turn one-off feedback into durable style/preference rules |
| invoked after drafting a spec or memo | .github/agents/hostile-reviewer.md | Skeptical verification pass; enumerates problems only |
| invoked after drafting anything public | .github/agents/voice-reviewer.md | Enumerates prose tells; never rewrites |
| "I'm in a meeting" / "starting a meeting" | .github/agents/meeting-capture.md | Live note capture; type "wrap" to triage |
