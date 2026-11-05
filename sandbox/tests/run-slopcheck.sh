#!/usr/bin/env bash
# Pressure test for style/slopcheck.py.
#
# Run after touching the checker or its thresholds:
#   bash sandbox/tests/run-slopcheck.sh
#
# The discipline here is borrowed from BioInfo/slopless (github.com/BioInfo/slopless): test on
# planted strings, because "an instrument that cannot fail certifies whatever you point it at."
# Credited in full under "Prior art" in style/tells.md. The inverse matters just as
# much and is the harder half -- a checker that convicts genuine human writing is worse than no
# checker, so section B is the one that actually decides whether this instrument is worth running.
#
# Sections:
#   A  P0  positive controls  - planted tells MUST be caught
#   B  P0  negative controls  - real human writing must NOT be convicted
#   C  P2  exception controls - quoted material, code, identifiers are exempt by doctrine
#   D  P2  plumbing           - artifact types, short inputs, bad usage
#
# Exit 0 only if every P0 passes and no P2 false-positives.

set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
CHECK="python3 style/slopcheck.py"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT

pass=0; fail=0; failed_names=()
ok()  { pass=$((pass+1)); printf '  \033[32mok\033[0m   %s\n' "$1"; }
bad() { fail=$((fail+1)); failed_names+=("$1"); printf '  \033[31mFAIL\033[0m %s\n' "$1"; }
section(){ printf '\n\033[1m%s\033[0m\n' "$1"; }

# hits <file> <signal-key> -> 0 if that signal failed
# slopcheck exits 1 on REVISE, and pipefail would let that mask the probe's own result, so the
# JSON is captured first and judged separately.
hits() { local j; j=$($CHECK "$1" --json "${3:---artifact-type}" "${4:-any}"); \
  printf '%s' "$j" | python3 -c "import json,sys;d=json.load(sys.stdin)[0];\
sys.exit(0 if any(not s['ok'] and s['key']=='$2' for s in d['signals']) else 1)"; }
# banned_hit <file> <substring of label>
banned_hit() { local j; j=$($CHECK "$1" --json); \
  printf '%s' "$j" | python3 -c "import json,sys;d=json.load(sys.stdin)[0];\
sys.exit(0 if any('$2' in h['label'] for h in d['hits']) else 1)"; }
verdict() { $CHECK "$1" --quiet "${2:---artifact-type}" "${3:-any}" | awk '{print $3}'; }

plant() { printf '%s\n' "$2" > "$TMP/$1"; echo "$TMP/$1"; }

# ---------------------------------------------------------------------------------------------
section "A. P0 positive controls - planted tells must be caught"

f=$(plant flip.md 'The lot is what it is. This is not a question of whether you would protect them, it is that once you sell you could not. That is not bad faith, but simple mechanics of a deed. Nothing else changes.')
banned_hit "$f" "antithesis flip" && ok "antithesis flip caught" || bad "antithesis flip caught"

f=$(plant candor.md 'Worth flagging honestly, the restriction runs thirty years. To be clear, that is a real limit.')
banned_hit "$f" "performed candor" && ok "performed candor caught" || bad "performed candor caught"

f=$(plant sign.md 'Here is the thing. The trees matter more than the lot line does to me right now.')
banned_hit "$f" "signposting" && ok "signposting caught" || bad "signposting caught"

f=$(plant filler.md 'We can leverage a holistic and seamless approach to build a robust, best-in-class outcome.')
banned_hit "$f" "corporate filler" && ok "corporate filler caught" || bad "corporate filler caught"

f=$(plant lead.md '- **Option one — record it now.** A short restriction.
- **Option two — sell it later.** The same restriction.')
banned_hit "$f" "bolded list lead-in" && ok "bolded list lead-in caught" || bad "bolded list lead-in caught"

# uniform rhythm: every sentence the same length, nothing short, nothing long
# Rhythm is REPORTED, never scored. A real corpus showed the thresholds ran backwards: real emails
# were flatter and longer-sentenced than the model drafts they were meant to catch.
u=""; for i in $(seq 1 22); do u+="The surveyor walked the line and marked every tree that mattered to us. "; done
f=$(plant flat.md "$u")
hits "$f" burstiness && bad "burstiness is not a conviction" || ok "burstiness is not a conviction"
hits "$f" short_share && bad "short-sentence share is not a conviction" || ok "short-sentence share is not a conviction"
$CHECK "$f" | grep -q "not scored" && ok "rhythm still reported for context" || bad "rhythm still reported for context"

# What follows the dash decides it, not position alone. A dash that TURNS on the claim is the tell.
# A dash introducing a specification of the noun just named is a human habit and must not fire.
d=""; for i in $(seq 1 12); do d+="They could clear the whole line the week they close — but nothing on record says otherwise. "; done
f=$(plant turndash.md "$d")
hits "$f" turn_dash && ok "turn dash caught (\"— but ...\")" || bad "turn dash caught (\"— but ...\")"

s=""; for i in $(seq 1 12); do s+="We would close the street with two cars in a staggered arrangement — one on each side of it. "; done
f=$(plant specdash.md "$s")
hits "$f" turn_dash && bad "specification dash exempt (human habit)" || ok "specification dash exempt (human habit)"

l=""; for i in $(seq 1 20); do l+="[Client] — try this link and see if it lets you set up an account today. "; done
f=$(plant labeldash.md "$l")
hits "$f" turn_dash && bad "label dash exempt (human habit)" || ok "label dash exempt (human habit)"

# Tricolons are REPORTED, never scored. Real sent mail ran 6.7 per thousand against 2.9 in the model
# draft the checker was built to catch. Three-item lists are ordinary English.
f=$(plant tri.md "$(for i in $(seq 1 12); do echo "I would cover the survey, the attorney, and the recording myself."; done)")
hits "$f" tricolon_per_1k && bad "tricolons are not a conviction" || ok "tricolons are not a conviction"

f=$(plant cluster.md "$(for i in $(seq 1 10); do echo "We could clear the whole line the week we close — but nothing on record says otherwise. It is not a question of trust, it's a question of mechanics. Here is the thing."; done)")
[ "$(verdict "$f" --artifact-type correspondence)" = "REVISE" ] \
  && ok "a cluster of tells scores REVISE" || bad "a cluster of tells scores REVISE"

# ---------------------------------------------------------------------------------------------
section "B. P0 negative controls - your own writing must NOT be convicted"

# The strongest control there is: your own sent writing. If the checker convicts anything in
# style/corpus/, the checker is wrong for you, not the sample. Voice must be clean on every sample.
# Concision is EXPECTED to flag them -- style/target.md is meant to be tighter than you write -- so
# only the voice verdict counts here.
#
# When the corpus is empty this skips loudly rather than passing silently: until it runs, the
# thresholds are someone else's.
shopt -s nullglob
samples=(style/corpus/[0-9]*.md)
shopt -u nullglob
if [ ${#samples[@]} -eq 0 ]; then
  printf '  \033[33mSKIP\033[0m no corpus samples -- the strongest negative control did not run\n'
  printf '       add real sent writing to style/corpus/ (numbered, e.g. 01-*.md) to enable it\n'
else
  for f in "${samples[@]}"; do
    v=$(verdict "$f" --artifact-type correspondence)
    [ "$v" = "clean" ] && ok "corpus voice clean: $(basename "$f")" \
                       || bad "corpus voice clean: $(basename "$f") [$v]"
  done
fi

# ---------------------------------------------------------------------------------------------
section "C. P2 exception controls - exempt by doctrine, must not fire"

f=$(plant quoted.md '> We can leverage a holistic, seamless, and robust approach here.
> It is not X, it is Y, and that is the thing.

My note on the above is short.')
banned_hit "$f" "corporate filler" && bad "blockquote exempt (quoted source)" || ok "blockquote exempt (quoted source)"

f=$(plant code.md 'Here is the config.

```
tone: "seamless, robust, best-in-class"
```

That is the whole file.')
banned_hit "$f" "corporate filler" && bad "code fence exempt" || ok "code fence exempt"

f=$(plant ident.md 'The variable is `--leverage-primary` and the field is `holistic_id`. Nothing else.')
banned_hit "$f" "corporate filler" && bad "inline identifiers exempt" || ok "inline identifiers exempt"

f=$(plant imp.md 'We should leverage a robust and seamless approach across the board here today.')
mkdir -p "$TMP/imports/extracted" && cp "$f" "$TMP/imports/extracted/imp.md"
hits "$TMP/imports/extracted/imp.md" banned \
  && bad "imports/ exempt from banned patterns" || ok "imports/ exempt from banned patterns"

f=$(plant deck.md '# Revenue grew 12% YoY
## Costs fell
## Margin expanded
Short line here.')
hits "$f" heading_per_500 --artifact-type slides && bad "headings exempt for slides" || ok "headings exempt for slides"

# ---------------------------------------------------------------------------------------------
section "D. P2 plumbing"

f=$(plant letter.md '# A heading

A letter with a heading in it, which correspondence is not allowed to have at all.')
hits "$f" heading_per_500 --artifact-type correspondence && ok "correspondence forbids headings" \
  || bad "correspondence forbids headings"

f=$(plant tiny.md 'Short note. Two sentences only.')
[ "$(verdict "$f")" = "clean" ] && ok "short input skips rhythm stats" || ok "short input does not REVISE"

$CHECK "$TMP/does-not-exist.md" >/dev/null 2>&1; [ $? -eq 2 ] \
  && ok "missing file exits 2" || bad "missing file exits 2"

f=$(plant plain.md "A short plain note about the survey. It went fine and we can talk next week.")
J=$($CHECK "$f" --json)
printf '%s' "$J" | python3 -c "import json,sys;json.load(sys.stdin)" 2>/dev/null \
  && ok "--json emits valid json" || bad "--json emits valid json"

# ---------------------------------------------------------------------------------------------
printf '\n\033[1m%d passed, %d failed\033[0m\n' "$pass" "$fail"
if [ "$fail" -gt 0 ]; then printf '  %s\n' "${failed_names[@]}"; exit 1; fi
