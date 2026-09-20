# Claude Code instructions for this repository

The standing instructions are in @AGENTS.md -- imported, not pointed at, so they load by mechanism
rather than by Claude deciding to open the file. The user's communication preferences load the same
way: @preferences/communication.md

Those two files are shared with every AI client (Codex, ChatGPT Work, VS Code with Copilot).
Everything below is Claude-specific and lives here because no other client can use it.

## Skills

Skills live in `.github/skills/` (shared with every client) by default. If you migrate them to
`.claude/skills/<name>/SKILL.md` (the open Agent Skills format), each skill's `description:` field
carries its own trigger, so no trigger table needs to stay in sync. Either location works; the
shared location is portable.

Three behaviors have no skill file and stay here because they are retrieval patterns rather than
procedures:

- **"what do I think about X"** -- search `topics/` first, then `projects/`, `decisions/`, recent
  `daily/`. Check backlinks. Prefer the user's own framings, quote frontmatter dates so recency is
  visible, and say so if the answer draws on fewer than two sources.
- **"where did I put X" / "what do I know about Y"** -- filenames and frontmatter first, then
  contents, then `indexes/`, `meetings/`, `daily/`. Report paths and dates; if nothing is found,
  say so and offer to create the file.
- **User signals they are done** -- scan for files modified today across the content folders,
  report, then ask about empty daily-entry sections. Keep it light; skip it if the conversation was
  purely tactical.

## Style system

The style files in `style/` compose in layers. Before drafting anything that leaves the repo, the
draft-artifact skill prescribes the reading order:

1. `style/voice.md` (always)
2. `style/tells.md` (always, once you have built it)
3. `style/<artifact-type>.md`
4. `style/audiences/<audience>.md`
5. `style/positioning.md` (for anything public-facing)
6. Corpus samples in `style/corpus/` (for calibration, once you have collected them)
7. Run `style/slopcheck.py` on the draft (once you have built it)

The layers are documented in `style/voice.md` and the draft-artifact skill. `style/tells.md`,
`style/target.md`, `style/corpus/`, and `style/slopcheck.py` start empty or absent in a new wiki.
They grow from use: the feedback-to-wiki skill extracts conventions from draft feedback, and the
style-audit skill catches gaps. Over time, the style system accumulates a calibrated picture of
your voice that no single-session prompt can replicate.
