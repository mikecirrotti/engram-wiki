# Engram Wiki

> **This is an empty showcase repo.** It contains only the structure, templates, and AI
> instructions for the engram-wiki pattern -- no real content, by design. **Do not add your
> actual notes here.** To run your own engram wiki, fork or clone this into a **Private** repo
> first, then fill it with your work. Real people, projects, meetings, and decisions never
> belong in a public repository. Licensed MIT -- take the idea and make it yours.

A personal knowledge wiki that gives any AI assistant durable, persistent memory about your
work -- across every platform you use, without locking you into any one of them.

## The problem

Most LLM interactions are stateless. You explain your context, get a response, and start from
scratch next time. Every new session, every new tool, every new model -- you re-explain who you
are, what you are working on, and how you like things done.

## The idea

Store your professional knowledge -- projects, people, decisions, meeting history, writing style,
communication preferences -- as `.md` files in a git repository. When these files are available
to an AI assistant, it does not just answer questions; it answers them *as someone who already
knows your context*.

Git tracks changes to code. This repo tracks changes to a person's knowledge-work in a
machine-readable format. Every commit is a snapshot of what you knew, what you decided, and
what you were paying attention to at a given point in time.

> **Why "engram"?** An engram is the physical trace of a memory in the brain -- the enduring
> network of neurons that changes when you experience something, letting you store and recall
> it later. This repo is the same idea for your work: a durable, machine-readable memory trace
> an AI can store and recall.

## Platform-agnostic memory

The files are plain markdown in a git repository. That is the whole point. No proprietary format,
no vendor lock-in, no platform-specific database. Any AI client that can read files can use this
wiki as its memory layer:

| Client | How it reads the wiki |
|---|---|
| **Claude Code** | Reads `CLAUDE.md` automatically (which imports `AGENTS.md` and `preferences/`) |
| **Codex** | Reads `AGENTS.md` natively |
| **ChatGPT Work** | Reads `AGENTS.md` through the GitHub connector |
| **VS Code + GitHub Copilot** | Reads `.github/copilot-instructions.md` (which points to `AGENTS.md`) |
| **Cursor** | Reads `.cursorrules` or the repo's instruction files |
| **Any future client** | Reads `AGENTS.md` -- it is tool-neutral by design |

The instruction architecture supports this. `AGENTS.md` carries the standing instructions that
apply regardless of which assistant is running. `CLAUDE.md` carries only what is specific to
Claude Code. `.github/copilot-instructions.md` carries only a pointer for Copilot. One set of
rules, readable everywhere, with thin client-specific adapters where needed.

This means your memory is not trapped in one tool. Switch clients, use multiple clients in the
same week, try something new -- the wiki is still there, and the next assistant picks up where
the last one left off. The git history is the audit trail.

## Who this is for

Anyone doing knowledge work: product managers, data scientists, engineers, technical leads,
strategists. The directory structure is a baseline -- different roles should evolve it to fit.
A product manager might have a `stakeholders/` folder instead of `topics/`; a data scientist
might add `models/`. The skeleton adapts; the principle -- machine-readable professional
memory -- stays the same.

## Structure

| Folder | Purpose |
|---|---|
| `daily/` | One file per day, append-only. The river: raw signal, observations. |
| `people/` | One file per recurring collaborator. Living document. |
| `projects/` | One file per project or initiative. Living document. |
| `topics/` | One file per durable concept. Your evolving thinking. The lakes. |
| `meetings/` | One file per recurring meeting; dated sections appended per occurrence. |
| `decisions/` | ADR-style decision logs. Immutable once written -- supersede, never edit. |
| `preferences/` | Standing instructions to the AI about tone, defaults, work style. |
| `style/` | House style guide for written artifacts, with layers that grow over time. |
| `templates/` | Starting structures for new entries. |
| `indexes/` | Generated cross-references. Never handwritten; rebuilt by a skill. |
| `exports/` | Polished artifacts and rendered output. |
| `imports/` | Incoming files; extracted content lands in `imports/extracted/`. |
| `inbox.md` | Raw capture. Triage into the right home periodically. |
| `index.md` | Top-level map of the wiki. |

### The style system

The style files are not just formatting rules. They are a layered system that grows from use,
designed to accumulate a calibrated picture of your voice over time:

- **`style/voice.md`** -- how you write, across every artifact type. Grows from draft feedback.
- **`style/tells.md`** -- patterns that make writing read as machine-generated. Grows from
  comparing AI drafts against your own writing samples in `style/corpus/`.
- **`style/target.md`** -- the concision axis. Separates voice fidelity (should this sound like
  me?) from concision (should this be shorter?) -- two different problems with different fixes.
- **`style/corpus/`** -- unedited samples of your own real writing. Immutable calibration data.
  The rules are tested against these; if a rule flags a corpus sample as machine-generated, the
  rule is wrong.
- **`style/positioning.md`** -- canonical public identity and claim boundaries.
- **Artifact-type files** (`memo.md`, `slides.md`, `email.md`, etc.) and **audience files**
  (`audiences/executives.md`, `audiences/peers.md`) compose with the voice.

The style system starts mostly empty. The **feedback-to-wiki** skill extracts conventions from
your draft feedback, and the **style-audit** skill catches gaps on a weekly pass. Over time, the
assistant learns not just what you want to say but how you sound saying it.

### Instruction architecture

| File | Loaded by | Scope |
|---|---|---|
| `AGENTS.md` | Every client | Tool-neutral standing instructions |
| `CLAUDE.md` | Claude Code | Claude-specific behavior; imports AGENTS.md |
| `.github/copilot-instructions.md` | VS Code + Copilot | Points to AGENTS.md |
| `preferences/` | Every client (via AGENTS.md) | Conversation style |
| `style/` | Skills, on trigger | Artifact drafting |
| `.github/skills/` | Every client, on trigger | Triggered workflows |
| `.github/agents/` | Every client, on trigger | Sub-agent roles |

The test for where a rule lives: name the sessions where it should apply. If the answer is "all
of them," it goes in `AGENTS.md` or `preferences/`. If the answer is "only when drafting," it
goes in a style file or a skill. See `topics/instruction-placement.md` for the full reasoning.

## Conventions

- Every content file starts with YAML frontmatter -- see [`templates/`](templates/).
- Cross-reference other notes with `[[wikilinks]]`, e.g. `[[people/jane-doe]]`.
- **River and lakes.** Daily files are the river: raw signal as it arrives. Topic and project
  files are the lakes. Promote durable insight from the daily stream into its permanent home,
  then link back.
- **Decisions are immutable.** Supersede with a new decision rather than editing an old one.
- **Meeting files are append-only logs** -- one file per recurring meeting, dated sections per
  occurrence. Do not create per-occurrence files.
- The `type:` frontmatter field uses a controlled vocabulary: `observation`, `task`, `idea`,
  `reference`, `person_note`, `decision`, `daily`, `project`, `topic`, `meeting`, `inbox`,
  `index`, `preference`, `style_guide`.

## Getting started

1. **Fork or clone** this repo into a private repository. Never put real content in the public
   showcase.
2. Edit [`preferences/communication.md`](preferences/communication.md) so the assistant learns
   your defaults.
3. Say **"good morning"** to run the morning ritual -- it creates today's daily entry, triages
   the inbox, and gives you a brief summary.
4. Start capturing: meetings, people, projects. The more goes in, the more the assistant knows
   next time.
5. After a few drafts, add two or three samples of your own real writing to `style/corpus/`.
   That is the seed data for the voice calibration system.

## Inspiration and acknowledgements

This pattern draws on ideas from two people whose work shaped it:

- **[Andrej Karpathy](https://x.com/karpathy)** -- on LLMs as operating systems and persistent
  context. See his [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
- **[Nate B Jones](https://x.com/natebjones)** -- on structured personal knowledge management
  with AI copilots. See [Open Brain (OB1)](https://github.com/NateBJones-Projects/OB1).

The engram-wiki is an independent reconstruction of those ideas into a portable, self-contained
scaffold. It carries nothing proprietary from any employer or third party -- you supply your own
branding and content.

## Using this safely

Sanitize before you commit -- this scaffold ships empty, but once you fill it, you own what
lands in git history. Do not commit secrets, tokens, or confidential material. Keep the repo
**Private** if it holds sensitive content. Treat API tokens like passwords: they never belong
in the repo.
