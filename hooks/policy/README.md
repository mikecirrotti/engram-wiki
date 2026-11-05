# hooks/policy -- one home for the rules

You may work this wiki from several AI clients: Claude Code, Codex, ChatGPT Work, Copilot. Each has
its own instruction-file convention, its own hook API (if any), and its own idea of what a payload
looks like. None of that changes what the rules *are*.

So the rules live here, once, and every caller is a thin adapter around them. Change a rule here and
every layer gets it. Two copies of a rule drift as surely as fifteen; they just take longer to notice.

Two ideas from other people shaped this folder:

- **One rule, one home.** From Nate B Jones's harness audit, which found one authorship rule copied
  across fifteen skills -- fifteen apparent owners and no real one. See "The AI Harness Audit: Clean
  Your Setup Before You Upgrade" (Nate's Newsletter, 2026-07-15,
  [natesnewsletter.substack.com](https://natesnewsletter.substack.com/p/ai-harness-audit)). The same
  piece's rule that hard requirements need hard checks is the reason these rules are scripts.
- **Hooks over rules.** From [BioInfo/slopless](https://github.com/BioInfo/slopless): "a principle
  with no artifact has no enforcement."

## The files

| File | What it decides | Callers |
|---|---|---|
| `wiki-invariants.sh` | Does this change break a content rule? | `.githooks/pre-commit`, `.github/workflows/check-invariants.yml`, `sandbox/tests/run-invariants.sh` |

`style/slopcheck.py` is the prose counterpart. It reports and never blocks, so it lives with the
style files rather than here.

## What it enforces

Only the rules with no judgment in them **block**:

- `decisions/` files are never modified or deleted. Supersede with a new file.
- `style/corpus/` samples are never modified or deleted. They are a record of what you actually
  wrote; editing one destroys the evidence the voice rules are calibrated against.
- Notes in the content folders open with frontmatter and carry a `type:` from the vocabulary in
  `AGENTS.md`. Keep `TYPES` in the script in step with that list.
- Wikilinks are path-style, `[[folder/slug]]`. A bare `[[slug]]` turns ambiguous the moment two
  folders hold the same slug. A bare link to a root-level file (`[[inbox]]`) passes, since there the
  slug is already the full path.

Everything else **warns**: a path-style link that does not resolve yet (a forward reference to an
unwritten note is a legitimate wiki pattern), and a living document edited without bumping
`updated:`. A hook that blocks on judgment just teaches you `--no-verify`.

## What each layer can actually catch

| Layer | Clients with local git (Claude Code, Codex, Copilot) | Clients writing through the GitHub API |
|---|---|---|
| `.githooks/pre-commit` | yes, once armed | **no** -- API writes never touch a local hook |
| `.github/workflows/check-invariants.yml` | yes | **yes** |

The workflow is the only layer that covers every client, including one you have not adopted yet. It
reports rather than repairs: a red X on the commit and an email to whoever pushed it.

## Arming

`.githooks/` runs only when `core.hooksPath` points at it, and that setting lives in `.git/config`,
which is not versioned -- so it is unset in every fresh clone.

- Claude Code arms it automatically: `.claude/settings.json` runs `.claude/hooks/session-start.sh`
  at session start.
- Anywhere else, run once per clone: `git config core.hooksPath .githooks`

## Verifying

```
bash sandbox/tests/run-invariants.sh   # content rules, staged and range modes, in a throwaway repo
bash sandbox/tests/run-slopcheck.sh    # the prose checker: planted tells, your corpus, exemptions
```

`.github/workflows/run-tests.yml` runs both on every push. Run them yourself after touching
anything here or in `style/slopcheck.py`.

## Possible next layers

The private wiki this scaffold came from also enforces a house spelling at write time and gates
pushes to `main`. Both are taste rather than structure, so they are left out here. If you add one,
put the rule in this folder and keep each client's adapter to a few lines.
