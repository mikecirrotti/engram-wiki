# `.agents/skills` -- a symlink, not a copy

Codex is reported to scan `.agents/skills/` walking up from the working directory. Claude Code
reads `.claude/skills/`. This symlink gives both one set of files rather than two that drift.

If your client looks somewhere else, move or add a symlink; do not copy the skills. On Windows,
git checks out symlinks as plain text files unless `core.symlinks` is enabled -- if
`.agents/skills` opens as a one-line file, that is what happened.
