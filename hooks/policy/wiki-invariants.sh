#!/usr/bin/env bash
# Content invariants for the wiki. ONE home for the rules; three callers.
#
# Callers:
#   .githooks/pre-commit                    local, staged files      (every client with git)
#   .github/workflows/check-invariants.yml  server-side, pushed range (EVERY client, git or API)
#   sandbox/tests/run-invariants.sh         the test fixtures
#
# The server-side caller is the point. Connector writes (ChatGPT Work through the GitHub connector,
# for example) go straight to the GitHub API and never touch a git hook, so a local check alone
# cannot see them. The workflow runs the same script on the same rules, after the fact, and marks
# the commit red when it finds something.
#
# Usage:
#   wiki-invariants.sh --staged            what is staged right now
#   wiki-invariants.sh --range A..B        what changed between two commits
#   wiki-invariants.sh --all               every tracked file (audit mode; skips the diff rules)
#
# Exit codes:
#   0  no BLOCK findings (WARN findings may still be printed)
#   1  at least one BLOCK finding
#   2  bad usage
#
# Severity follows the rule .githooks/pre-commit already states: a check that blocks on judgment
# teaches you --no-verify. So only the binary, no-false-positive rules block.
#
#   BLOCK  decisions/ modified or deleted     immutable by design; supersede, never edit
#   BLOCK  style/corpus/ sample changed       a record of what you actually wrote
#   BLOCK  frontmatter missing or type: bad   the vocabulary in AGENTS.md, content folders only
#   BLOCK  wikilink not path-style            [[slug]] instead of [[folder/slug]]; no legitimate case
#   WARN   wikilink unresolvable              a forward reference to an unwritten note is legitimate
#   WARN   living document changed, updated: not bumped

set -uo pipefail

ROOT="${WIKI_REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null)}"
cd "$ROOT" 2>/dev/null || { echo "wiki-invariants: not a git repo" >&2; exit 2; }

MODE="${1:---staged}"
RANGE="${2:-}"

# Keep in step with "Type vocabulary" in AGENTS.md.
TYPES="observation task idea reference person_note decision daily project topic inbox index preference style_guide meeting"

blocks=0
warns=0

block() { blocks=$((blocks+1)); printf '  BLOCK  %s\n' "$1" >&2; }
warn()  { warns=$((warns+1));  printf '  warn   %s\n' "$1" >&2; }

# --- collect the change set -------------------------------------------------------------------
# name-status gives us A/M/D/R, which is what the immutability rules turn on.
changes=""
case "$MODE" in
  --staged)
    changes=$(git diff --cached --name-status --find-renames 2>/dev/null)
    ;;
  --range)
    [ -z "$RANGE" ] && { echo "wiki-invariants: --range needs A..B" >&2; exit 2; }
    changes=$(git diff --name-status --find-renames "$RANGE" 2>/dev/null)
    ;;
  --all)
    changes=$(git ls-files '*.md' | sed 's/^/A\t/')
    ;;
  *)
    echo "wiki-invariants: unknown mode '$MODE'" >&2; exit 2
    ;;
esac

[ -z "$changes" ] && { echo "wiki-invariants: nothing to check."; exit 0; }

# --- rule 1+2: immutable paths ----------------------------------------------------------------
# decisions/ files are ADR-style logs: supersede with a new file, never edit the old one.
# style/corpus/ samples are a record of your own unedited writing; editing one destroys the
# evidence the voice rules are calibrated against. README.md and PROFILE.md are meta, not samples.
while IFS=$'\t' read -r st path rest; do
  [ -z "${st:-}" ] && continue
  case "$st" in A*) continue ;; esac   # additions are always fine

  case "$path" in
    decisions/*)
      block "decisions/ is immutable -- '$path' was ${st:0:1}. Supersede it with a new file instead."
      ;;
    style/corpus/README.md|style/corpus/PROFILE.md) ;;
    style/corpus/*)
      block "style/corpus/ is a record -- '$path' was ${st:0:1}. Samples are never edited or cleaned up."
      ;;
  esac
done <<< "$changes"

# --- the file list for content rules ----------------------------------------------------------
# Added, modified and renamed markdown that still exists on disk.
files=$(awk -F'\t' '$1 !~ /^D/ {print $NF}' <<< "$changes" \
        | grep -E '\.md$' \
        | grep -vE '^(imports/|\.claude-skills/)' || true)

# --- rule 3: frontmatter ----------------------------------------------------------------------
# Scoped to the CONTENT folders, where the type vocabulary is the rule. Files outside them -- skills,
# exports, templates, READMEs -- were never meant to be governed by it, and checking them only
# produces noise.
in_content_scope() {
  case "$1" in
    style/corpus/*) return 1 ;;                      # raw records carry no frontmatter by design
    daily/*|people/*|projects/*|topics/*|decisions/*|meetings/*|preferences/*|indexes/*|style/*) return 0 ;;
    inbox.md|index.md|now.md) return 0 ;;
    *) return 1 ;;
  esac
}

for f in $files; do
  [ -f "$f" ] || continue
  in_content_scope "$f" || continue
  case "$f" in *.md) ;; *) continue ;; esac

  head -1 "$f" | grep -q '^---$' || { block "$f: no frontmatter block (must open with ---)"; continue; }

  t=$(awk 'NR>1 && /^---$/{exit} /^type:/{sub(/^type:[[:space:]]*/,""); gsub(/["\x27]/,""); print; exit}' "$f")
  if [ -z "$t" ]; then
    block "$f: frontmatter has no type: field"
  elif ! grep -qw -- "$t" <<< "$TYPES"; then
    block "$f: type '$t' is not in the vocabulary ($TYPES)"
  fi
done

# --- rule 4: wikilinks ------------------------------------------------------------------------
# Path-style, and resolving to something real. The two halves differ in severity on purpose. An
# unresolved link can be a forward reference, which is legitimate, so it warns. A bare [[slug]] has
# no legitimate case, so it blocks: it turns ambiguous the moment two folders hold the same slug,
# and the fix is mechanical. A bare link to a file at the repo root ([[inbox]]) passes, since there
# the slug IS the full path. Inline code spans and fenced blocks are skipped:
# AGENTS.md teaches the convention using [[folder/slug]] as an EXAMPLE, in backticks, and a checker
# that cannot tell an example from a link would flag the file that defines the rule.
strip_code() { sed -e '/^```/,/^```/d' -e 's/`[^`]*`//g' "$1"; }

for f in $files; do
  [ -f "$f" ] || continue
  while read -r link; do
    [ -z "$link" ] && continue
    target=${link#[[}; target=${target%]]}
    target=${target%%|*}          # [[path|alias]]
    target=${target%%#*}          # [[path#heading]]
    case "$target" in
      */*) ;;
      *) [ -f "$target.md" ] && continue   # a root-level file: [[inbox]] is already its full path
         block "$f: [[$target]] is not path-style -- use [[folder/slug]]"; continue ;;
    esac
    [ -f "$target.md" ] && continue
    [ -d "$target" ] && continue
    [ -f "$target" ] && continue
    warn "$f: [[$target]] does not resolve to a file"
  done < <(strip_code "$f" | grep -oE '\[\[[^]]+\]\]' | sort -u)
done

# --- rule 5: updated: bumped on living documents ----------------------------------------------
# Living documents only. daily/ is append-only and decisions/ is immutable, so neither applies.
if [ "$MODE" != "--all" ]; then
  today=$(date -u +%Y-%m-%d)
  while IFS=$'\t' read -r st path rest; do
    [ -z "${st:-}" ] && continue
    case "$st" in M*) ;; *) continue ;; esac
    case "$path" in
      people/*.md|projects/*.md|topics/*.md|style/*.md|style/*/*.md|preferences/*.md|meetings/*.md|index.md)
        # .md only: style/wordlist.txt is data with no frontmatter, so an updated: rule is
        # meaningless there and only produces noise.
        [ -f "$path" ] || continue
        u=$(awk 'NR>1 && /^---$/{exit} /^updated:/{print $2; exit}' "$path")
        # A scaffold ships with the literal placeholder; a filled wiki never carries it.
        [ "$u" = "YYYY-MM-DD" ] && continue
        [ "$u" = "$today" ] || warn "$path: updated: is '${u:-missing}', not today ($today)"
        ;;
    esac
  done <<< "$changes"
fi

# --- report -----------------------------------------------------------------------------------
if [ "$blocks" -gt 0 ] || [ "$warns" -gt 0 ]; then
  printf '\nwiki-invariants: %d blocking, %d advisory.\n' "$blocks" "$warns" >&2
else
  echo "wiki-invariants: clean."
fi

[ "$blocks" -gt 0 ] && exit 1
exit 0
