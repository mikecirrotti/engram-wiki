#!/usr/bin/env bash
# SessionStart hook: arm the tracked git hooks.
#
# core.hooksPath lives in .git/config, which is not versioned, so it is unset in every fresh clone
# and every cloud container. Without this, .githooks/pre-commit never runs. Idempotent, never blocks
# the session, and only touches this repo's local config.

cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}" 2>/dev/null || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

if [ -d .githooks ]; then
  git config core.hooksPath .githooks 2>/dev/null
  chmod +x .githooks/* hooks/policy/*.sh 2>/dev/null || true
  echo "engram: git hooks armed (core.hooksPath=.githooks)"
else
  echo "engram: WARNING -- .githooks/ missing, content rules are not enforced at commit"
fi
exit 0
