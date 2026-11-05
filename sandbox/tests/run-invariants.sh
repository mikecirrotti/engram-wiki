#!/usr/bin/env bash
# Pressure test for hooks/policy/wiki-invariants.sh.
#
#   bash sandbox/tests/run-invariants.sh
#
# Everything runs against a THROWAWAY repo in a temp dir, never the real wiki. The script under
# test is the same one the pre-commit hook and .github/workflows/check-invariants.yml call, so a
# pass here is a pass in both places.
#
# The rules that BLOCK are the ones with no judgment in them, including a bare [[slug]] wikilink.
# The rules that WARN are the ones where a false positive is possible -- an unwritten topic note
# referenced ahead of time is a legitimate wiki pattern. In one real wiki it occurred 48 times; a
# checker that blocked on those would be wrong 48 times before it was right once.

set -uo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)
SCRIPT="$REPO_ROOT/hooks/policy/wiki-invariants.sh"

pass=0; fail=0; failed_names=()
ok()   { pass=$((pass+1)); printf '  \033[32mok\033[0m   %-6s %s\n' "$1" "$2"; }
bad()  { fail=$((fail+1)); failed_names+=("$3"); printf '  \033[31mFAIL\033[0m want=%-5s got=%-5s %s\n' "$1" "$2" "$3"; }
check(){ [ "$1" = "$2" ] && ok "$2" "$3" || bad "$1" "$2" "$3"; }
section(){ printf '\n\033[1m%s\033[0m\n' "$1"; }

FIX=$(mktemp -d)
trap 'rm -rf "$FIX"' EXIT

# --- build a miniature wiki -------------------------------------------------------------------
cd "$FIX"
git init -q .
git config user.email t@example.com
git config user.name  Test
mkdir -p decisions topics people style/corpus

cat > decisions/2026-01-01-a-choice.md <<'EOF'
---
type: decision
status: accepted
---
# A choice
Made once, never edited.
EOF

cat > topics/a-topic.md <<'EOF'
---
type: topic
updated: 2026-01-01
---
# A topic
Links to [[topics/a-topic]].
EOF

cat > style/corpus/01-a-sample.md <<'EOF'
What you actually wrote, kept verbatim.
EOF

cat > style/corpus/README.md <<'EOF'
---
type: style_guide
updated: 2026-01-01
---
# Corpus
Meta, not a sample. Editable.
EOF

git add -A && git commit -qm "base"
BASE=$(git rev-parse HEAD)

run() { "$SCRIPT" "$@" >/dev/null 2>&1; echo $?; }   # 0 clean, 1 blocking
verdict() { [ "$1" = "0" ] && echo PASS || echo BLOCK; }

section "A. Immutable paths"

echo "edited" >> decisions/2026-01-01-a-choice.md && git add -A
check BLOCK "$(verdict "$(run --staged)")" "editing a decisions/ file"
git reset -q --hard

git rm -q decisions/2026-01-01-a-choice.md
check BLOCK "$(verdict "$(run --staged)")" "deleting a decisions/ file"
git reset -q --hard

cat > decisions/2026-02-02-a-newer-choice.md <<'EOF'
---
type: decision
status: accepted
supersedes: decisions/2026-01-01-a-choice
---
# A newer choice
EOF
git add -A
check PASS "$(verdict "$(run --staged)")" "ADDING a decisions/ file (the supersede path)"
git reset -q --hard && rm -f decisions/2026-02-02-a-newer-choice.md

echo "cleaned up" >> style/corpus/01-a-sample.md && git add -A
check BLOCK "$(verdict "$(run --staged)")" "editing a corpus sample"
git reset -q --hard

echo "meta note" >> style/corpus/README.md && git add -A
check PASS "$(verdict "$(run --staged)")" "editing corpus README (meta, not a sample)"
git reset -q --hard

section "B. Frontmatter"

cat > topics/no-frontmatter.md <<'EOF'
# Missing its frontmatter entirely
EOF
git add -A
check BLOCK "$(verdict "$(run --staged)")" "content file with no frontmatter"
git reset -q --hard && rm -f topics/no-frontmatter.md

cat > topics/bad-type.md <<'EOF'
---
type: musings
updated: 2026-01-01
---
# Not in the vocabulary
EOF
git add -A
check BLOCK "$(verdict "$(run --staged)")" "type outside the vocabulary"
git reset -q --hard && rm -f topics/bad-type.md

cat > people/someone.md <<'EOF'
---
type: person_note
updated: 2026-01-01
---
# Someone
EOF
git add -A
check PASS "$(verdict "$(run --staged)")" "valid frontmatter"
git reset -q --hard && rm -f people/someone.md

mkdir -p projects/a-project
cat > projects/a-project/supporting-note.md <<'EOF'
---
type: reference
updated: 2026-01-01
---
# A note in a subfolder of projects/
EOF
git add -A
check PASS "$(verdict "$(run --staged)")" "valid note in a projects/ subfolder"
git reset -q --hard && rm -rf projects/a-project

cat > style/corpus/02-another-sample.md <<'EOF'
A raw sample, no frontmatter, by design.
EOF
git add -A
check PASS "$(verdict "$(run --staged)")" "corpus sample needs no frontmatter"
git reset -q --hard && rm -f style/corpus/02-another-sample.md

section "C. Wikilinks"

cat > topics/forward-ref.md <<'EOF'
---
type: topic
updated: 2026-01-01
---
# Forward reference
Points at [[topics/not-written-yet]] on purpose.
EOF
git add -A
check PASS "$(verdict "$(run --staged)")" "unresolved path-style wikilink warns only"
out=$("$SCRIPT" --staged 2>&1)
check "yes" "$(grep -q 'not-written-yet' <<<"$out" && echo yes || echo no)" "  ...but it IS reported"
git reset -q --hard && rm -f topics/forward-ref.md

cat > topics/bare-link.md <<'EOF'
---
type: topic
updated: 2026-01-01
---
# Bare link
Points at [[a-topic]], which lives in topics/ and so needs its folder.
EOF
git add -A
check BLOCK "$(verdict "$(run --staged)")" "bare [[slug]] wikilink"
out=$("$SCRIPT" --staged 2>&1)
check "yes" "$(grep -q 'not path-style' <<<"$out" && echo yes || echo no)" "  ...and the slug is named"
git reset -q --hard && rm -f topics/bare-link.md

cat > inbox.md <<'EOF'
---
type: inbox
---
# Inbox
EOF
cat > topics/root-link.md <<'EOF'
---
type: topic
updated: 2026-01-01
---
# Root link
Captured in [[inbox]], a root-level file whose slug is its full path.
EOF
git add -A
check PASS "$(verdict "$(run --staged)")" "bare link to a root-level file"
git reset -q --hard && rm -f inbox.md topics/root-link.md

cat > topics/code-example.md <<'EOF'
---
type: topic
updated: 2026-01-01
---
# Teaching the rule
Write `[[folder/slug]]`, never `[[slug]]`.
EOF
git add -A
check PASS "$(verdict "$(run --staged)")" "bare link in inline code is an example, not a link"
git reset -q --hard && rm -f topics/code-example.md

section "D. Other advisory rules never block"

sed -i 's/^# A topic/# A topic edited/' topics/a-topic.md && git add -A
check PASS "$(verdict "$(run --staged)")" "stale updated: warns only"
out=$("$SCRIPT" --staged 2>&1)
check "yes" "$(grep -q 'updated:' <<<"$out" && echo yes || echo no)" "  ...but it IS reported"
git reset -q --hard

section "E. --range mode (what the workflow runs)"

echo "edited after the fact" >> decisions/2026-01-01-a-choice.md
git add -A && git commit -qm "an API write that should not have happened"
check BLOCK "$(verdict "$(run --range "$BASE..HEAD")")" "decisions/ edit caught across a range"

git revert --no-edit HEAD >/dev/null 2>&1
check PASS "$(verdict "$(run --range "HEAD..HEAD")")" "empty range is clean"

printf '\n\033[1mResult:\033[0m %d passed, %d failed\n' "$pass" "$fail"
if [ "$fail" -gt 0 ]; then
  printf 'Failed:\n'; printf '  - %s\n' "${failed_names[@]}"
  exit 1
fi
exit 0
