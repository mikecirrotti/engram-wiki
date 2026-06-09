# Engram Wiki

> ⚠️ **This is an empty showcase repo.** It contains only the structure, templates, and AI
> instructions for the engram-wiki pattern — no real content, by design. **Do not add your
> actual notes here.** To run your own engram wiki, fork or clone this into a **Private** repo
> first, then fill it with your work. Real people, projects, meetings, and decisions never
> belong in a public repository. Licensed MIT — take the idea and make it yours.

A personal knowledge wiki that gives an AI assistant durable, persistent memory about your
work. It is a folder of markdown files in a local git repository: projects, people, decisions,
meeting history, writing style, and communication preferences. When these files are available
to an LLM, it doesn't just answer questions — it answers them *as someone who already knows
your context*.

Git tracks changes to code. This repo tracks changes to a person's knowledge-work in a
machine-readable format. Every commit is a snapshot of what you knew, what you decided, and
what you were paying attention to at a point in time.

> **Why "engram"?** An engram is the physical trace of a memory in the brain — the enduring
> network of neurons that changes when you experience something, letting you store and recall
> it later. This repo is the same idea for your work: a durable, machine-readable memory trace
> an AI can store and recall.

**This repo ships empty on purpose.** The structure, templates, and AI instructions are here;
the knowledge is yours to fill in over time.

## Structure

| Folder | Purpose |
|---|---|
| `daily/` | One file per day, append-only. The river: raw signal, observations. |
| `people/` | One file per recurring collaborator. Living document. |
| `projects/` | One file per project or initiative. Living document. |
| `topics/` | One file per durable concept. Your evolving thinking. The lakes. |
| `meetings/` | One file per recurring meeting; dated sections appended per occurrence. |
| `decisions/` | ADR-style decision logs. Immutable once written — supersede, never edit. |
| `preferences/` | Standing instructions to the AI about tone, defaults, work style. |
| `style/` | House style guide for written artifacts; `style/audiences/` for audience profiles. |
| `templates/` | Starting structures for new entries. |
| `indexes/` | Generated cross-references. Never handwritten; rebuilt by a skill. |
| `exports/` | Polished artifacts and rendered output. |
| `imports/` | Incoming files; extracted content lands in `imports/extracted/`. |
| `.github/` | AI behavioral instructions (`copilot-instructions.md`) and invokable skills/agents. |
| `inbox.md` | Raw capture. Triage into the right home periodically. |
| `index.md` | Top-level map of the wiki. |

The AI's canonical behavioral instructions live in [`CLAUDE.md`](CLAUDE.md) (Claude Code reads
it automatically); [`.github/copilot-instructions.md`](.github/copilot-instructions.md) points
Copilot-based assistants to the same file.

## Conventions

- Every content file starts with YAML frontmatter — see [`templates/`](templates/).
- Cross-reference other notes with `[[wikilinks]]`, e.g. `[[people/jane-doe]]`.
- **River and lakes.** Daily files are the river: raw signal as it arrives. Topic and project
  files are the lakes. Promote durable insight from the daily stream into its permanent home,
  then link back.
- **Decisions are immutable.** Supersede with a new decision rather than editing an old one.
- **Meeting files are append-only logs** — one file per recurring meeting, dated sections per
  occurrence. Don't create per-occurrence files.
- The `type:` frontmatter field uses a controlled vocabulary: `observation`, `task`, `idea`,
  `reference`, `person_note`, `decision`, `daily`, `project`, `topic`, `meeting`, `inbox`,
  `index`, `preference`, `style_guide`.

## Getting started

1. Edit [`preferences/communication.md`](preferences/communication.md) so the assistant learns
   your voice and defaults.
2. Say **"good morning"** to run the morning ritual — it creates today's daily entry, triages
   the inbox, and gives you a brief summary.
3. Start capturing: meetings, people, projects. The more goes in, the more the assistant knows
   next time.

## Using this safely

Sanitize before you commit — this scaffold ships empty, but once you fill it, you own what
lands in git history. Don't commit secrets, tokens, or confidential material. Keep the repo
**Private** if it holds sensitive content. Treat API tokens like passwords: they never belong
in the repo.
