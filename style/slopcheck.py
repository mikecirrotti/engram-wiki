#!/usr/bin/env python3
"""Report the measurable signals that make prose read as machine-generated.

Doctrine lives in style/tells.md. This file only measures it.

    python3 style/slopcheck.py DRAFT.md [--artifact-type correspondence] [--json] [--quiet]

Two rules govern the design, both inherited from the US-English sweep in style/voice.md:

  1. It REPORTS CANDIDATES AND NEVER REWRITES. Quoted material, identifiers and genuinely
     enumerable content are all legitimate, so an auto-fix would silently damage sources.
  2. NO SINGLE SIGNAL CONVICTS. Every one of these has an innocent explanation on its own.
     Convergence is the fingerprint, so the verdict keys off how many fail at once.

Exit codes:  0 clean or advisory   1 revise (>= FAIL_AT signals failed)   2 bad usage

CALIBRATION. The thresholds below were tuned against one writer's corpus: about a dozen real sent
emails and letters, plus pairs of model drafts that writer approved or rejected. The evidence is
summarized in the comments, anonymized. Your writing will differ. Before trusting a verdict, run it
over your own samples in style/corpus/ (sandbox/tests/run-slopcheck.sh does this). The rule:
  - a FIDELITY signal that fires on your own writing is wrong for you -- loosen it or move it to
    INFORMATIONAL;
  - a CONCISION signal that fires on your own writing is working as intended, since
    style/target.md is meant to be tighter than you write.

Prior art this borrows from, with thanks. Credited in full, with what each contributed, under
"Prior art" in style/tells.md:
  slopdetector.org/blog/signs-of-ai-writing   starting thresholds, and the convergence rule above
  github.com/hardikpandya/stop-slop           score-with-a-threshold rather than a judgment call
  github.com/jalaalrd/anti-ai-slop-writing    the category structure of BANNED below
  github.com/BioInfo/slopless                 the starting rhythm numbers, and planted-string testing
The corpus calibration, the voice/concision split, and the dash, cadence and marker signals are this
repo's own and should not be read as anything those projects recommend.
"""

import argparse
import json
import re
import statistics as st
import sys

# --- thresholds -------------------------------------------------------------------------------
# Tune these from evidence -- your corpus and drafts you have judged -- not from taste. Record what
# moved and why, so the next change has something to argue with.

FAIL_AT = 3          # how many failed signals means "revise"

# Every threshold below was calibrated against measured text, not taken on faith from the sources
# in style/tells.md. Two of them moved on first contact with real human writing:
# burstiness started at 0.75 and a genuine spoken transcript scored 0.70, so a checker set there
# would have convicted a person talking. Same for the long-sentence share.
SHORT_W = 8          # a "short" sentence, in words
LONG_W = 30          # a "long" sentence, in words
MIN_WORDS = 120      # below this, rhythm statistics are noise and get skipped

# Reported for context but never scored. All of these were pass/fail signals until the original
# writer's corpus arrived and showed they ran backwards. That writer's real emails scored 0.33-0.46
# burstiness and 0-25% short sentences, while model drafts scored 0.55-1.04 and 10-22%. The advice
# they came from is about published essay prose, and enforcing it pushed drafts away from the
# writer's voice. The same happened with evenly sized paragraphs (cv 0.23-0.39 in real mail), long
# sentences (a third over 30 words) and tricolons (6.7 per thousand in real mail against 2.9 in the
# draft that started all this -- people build three-item lists constantly). What survived as
# scoreable is the set that actually separated real writing from drafts: turning dashes, flips,
# headings and banned patterns. Re-check this list against your own corpus.
INFORMATIONAL = ("burstiness", "short_share", "para_cv", "long_share", "tricolon_per_1k",
                 "emdash_per_1k", "cadence_dash_per_1k",
                 "fragment_share", "colon_setup_per_1k", "hedge_per_100w", "markers_per_1k")

# Added from a matched pair in style/corpus/assisted/: two drafts of one brief, both clean on every
# fidelity signal above, one read by the writer as machine-written and one approved. What separated
# them was cadence the subtractive signals cannot see (style/tells.md, "Verdict cadence") and the
# presence of the writer's own habits. These four are REPORTED and never scored, per the rule that a
# threshold needs measured text behind it.
#   fragment_share      units of 1-4 words ending in terminal punctuation ("Not that one.")
#   colon_setup_per_1k  a short lead-in, a colon, then the payoff ("The mandate version: ...")
#   hedge_per_100w      hedges per hundred words; too FEW is the assisted tell, not too many
#   markers_per_1k      scare-quoted short terms, slashes joining words, etc./e.g./i.e./vs.,
#                       and a paragraph-turning connective opening a sentence. These are one
#                       writer's markers; swap in yours.
FRAGMENT_MAX_WORDS = 4
COLON_SETUP = re.compile(r"^(?:\S+\s+){0,7}\S+:\s+\S+(?:\s+\S+){5,}")
MARKERS = (
    r"[\u201c\"][^\u201d\"\n]{1,40}[\u201d\"]",                    # scare quotes, short phrase
    r"\w\s?/\s?\w",                                                 # practice / exercise, and/or
    r"\b(?:etc|e\.g|i\.e|vs)\.",
    r"(?:^|(?<=[.!?]\s))(?:However|Again|Now|Then|Ultimately|Additionally|In other words),",
)

# Position, not density, is what separated the writer's em dashes from the model's. Every one in the
# original corpus was a LABEL dash opening a unit -- "[Name] — try this link", "All — as you
# know". None was the mid-sentence claim-then-turn cadence. The draft's sat 11 to 20 words in.
LABEL_DASH_MAX_WORDS = 4

# One sample broke the position-only rule: a sentence like "we would park the two trucks in a
# staggered arrangement — one on each side of the road", a mid-sentence dash 20 words in. What follows it is a SPECIFICATION of the noun
# just named, standing in for a colon. The tell is a dash that TURNS on the claim -- "they agreed — not
# because they had to, but", "I'll adapt — and if the answer is no". Counted this way: zero across the
# real samples, present in 12 of 13 model drafts. Sharper than position.
TURN_AFTER_DASH = re.compile(
    r"^\s*(?:and|but|so|not|yet|which|though|although|because|while|or|then|"
    r"it'?s|that'?s|this is)\b", re.I)

# Rate-per-1000 signals are unstable on short text: one tricolon in a 180-word email reads as
# 5.6 per thousand. A rate cannot convict until the raw count reaches MIN_COUNT_TO_CONVICT.
#
# A house format for a work notice may label its sections with a short line carrying the VERDICT,
# not the topic -- "Conflicts of Interest: None I've identified", "How I'd run it:". Those are
# structure, not prose, so they end a unit and are not measured. Bounded in length so a soft-wrapped
# prose line cannot be mistaken for one. See style/correspondence.md.
LABEL_LINE = re.compile(r"^[ \t]*(?=.{0,70}$)(?![-*+] )[^\n.!?]*?:(?:[^\n.!?]*)$", re.M)

MIN_COUNT_TO_CONVICT = 2

# Sentences are scored in two classes, and the difference matters more than any threshold.
#
#   FIDELITY  - calibrated to style/corpus/. These are habits the model has and the writer does
#               not. If one of these convicts a corpus sample, the RULE IS WRONG.
#
#   CONCISION - calibrated to style/target.md, which is deliberately tighter than the writer
#               writes. These SHOULD flag the corpus. That is not a bug and must not be "fixed" by
#               relaxing them to fit the samples. The goal is the writer's voice, in fewer words.
FIDELITY  = {"turn_dash", "flip_per_1k", "heading_per_500", "banned"}
CONCISION = {"mean_sentence", "max_sentence", "hedge_stack", "restatement"}

# Hedges are voice, not noise -- they mark what the writer knows from what they are guessing. The problem is
# stacking two or three in one sentence, where the second and third add nothing.
# Function words legitimately repeat in parallel constructions ("whether X, or whether Y"). Only a
# repeated CONTENT word means the sentence is circling.
FUNCTION_WORDS = {
    "whether", "which", "would", "could", "should", "there", "their", "about", "because",
    "before", "after", "while", "where", "these", "those", "other", "another", "every",
    "still", "might", "being", "having", "than", "then", "with", "that", "this", "what",
    "when", "your", "yours", "ours", "something", "anything", "nothing", "myself", "really",
}

HEDGE = (r"\b(?:would think|I would|should|might|may|some kind of|kind of|sort of|quite|really|"
         r"fairly|pretty much|I think|it seems|seems like|probably|likely|a bit|somewhat|just|"
         r"actually|basically|generally|ultimately|essentially)\b")

THRESHOLDS = {
    # concision -- aspirational, tighter than the corpus on purpose
    "mean_sentence":    ("<=", 26.0, "mean sentence length, words"),
    "max_sentence":     ("<=", 40.0, "longest sentence, words"),
    "hedge_stack":      ("<=", 0.0,  "sentences stacking 2+ hedges"),
    "restatement":      ("<=", 0.0,  "sentences that repeat their own key word"),
    "turn_dash":        ("<=", 0.0,  "em dashes that turn on the claim"),
    "flip_per_1k":      ("<=", 1.0,  "antithesis flips per 1,000 words"),
    "heading_per_500":  ("<=", 2.0,  "headings per 500 words"),
    "banned":           ("<=", 1.0,  "banned patterns from style/tells.md"),
}

# Which signals apply to which artifact type. Structure has to be earned by the artifact, not
# applied by default -- a deck legitimately has headings, a report legitimately has tables.
ARTIFACT_EXEMPT = {
    "correspondence": {},                             # everything applies, strictly
    "email":          {"heading_per_500"},
    "memo":           {"heading_per_500"},
    "report":         {"heading_per_500"},
    "slides":         {"heading_per_500"},
    "public":         {},
    "feedback":       set(CONCISION) | {"heading_per_500"},  # rough notes, not a deliverable
    "any":            {"heading_per_500"},
}
# Correspondence gets a stricter heading rule than every other type (see style/correspondence.md).
CORRESPONDENCE_HEADING_MAX = 0.0

# Prose-level patterns, matched against the stripped text.
BANNED = [
    (r"\b(?:it|this|that)(?:'?s| is| was) not\b[^.\n]{0,50}?,?\s*(?:it|that)(?:'?s| is)\b",
     "antithesis flip (\"it's not X, it's Y\")"),
    (r"\b(?:is|was|are|were)? ?not\b[^.,]{0,40}?, but\b",  "antithesis flip (\"not X, but Y\")"),
    (r"\bworth (?:flagging|noting) (?:honestly|here)\b", "performed candor"),
    (r"\bto be clear\b",                                  "performed candor"),
    (r"\bhere(?:'?s| is) the thing\b",                     "signposting"),
    (r"\bin today'?s [\w\s]{0,20}landscape\b",            "delayed opener"),
    (r"\bit'?s worth noting that\b",                      "delayed opener"),
    (r"\b(?:delve|leverage|synergy|holistic|seamless|robust|best-in-class)\b", "corporate filler"),
    (r"\b(?:cutting-edge|revolutionary|game-changing|next-generation)\b",      "hype"),
    (r"\b(?:passionate about|thought leader|visionary)\b",                     "self-branding"),
    (r"\b(?:responsible for|helped to|involved in)\b",                         "resume-speak"),
    (r"\b(?:arguably|somewhat|it could be said|in many ways)\b",               "hedge"),
    (r"\bat a glance\b",                                  "summary furniture"),
]

# Structure-level patterns, matched against the RAW markdown. strip() removes list markers and
# emphasis before the prose checks run, so these would never fire there.
BANNED_RAW = [
    # A bolded multi-word PHRASE that opens a list item and is followed by prose. A single
    # bolded term (or a `code` term) opening a definition list is a glossary, not a slide.
    (r"^\s*[-*+]\s+\*\*(?![`\w-]+\*\*)[^*\n]*\s[^*\n]*\*\*[^\n]*\w",
     "bolded list lead-in"),
    (r"^#+\s*(?:what this is|last thing|the ask|at a glance)\b", "signposting heading"),
    (r"^#+.*\bat a glance\b",                            "summary furniture heading"),
]


def _letterhead(md):
    """Drop a formal letter's address block. It is metadata, not prose, and read as a sentence it
    lands as a 70-word run-on that nothing in the letter is responsible for."""
    lines = md.split("\n")
    end = 0
    for i, line in enumerate(lines[:18]):
        s = line.strip()
        if not s:
            continue
        # a salutation closes the block
        if re.match(r"^(to whom it may concern|dear\b|attn\b)", s, re.I) and s.endswith((":", ",")):
            end = i + 1
            break
        # markdown structure is never letterhead
        if re.match(r"^(#{1,6}\s|[-*+>]\s|\||```)", s):
            break
        # contact-block lines are short and carry no sentence punctuation
        if len(s.split()) <= 12 and not s.endswith((".", "!", "?")):
            end = i + 1
        else:
            break
    return "\n".join(lines[end:]) if end else md


def _scope(md):
    """The part of the file that actually gets sent, before any markdown is removed."""
    md = re.sub(r"\A---\n.*?\n---\n", "", md, count=1, flags=re.S)
    md = re.split(r"^#+\s*Notes on the draft\b", md, maxsplit=1, flags=re.M | re.I)[0]
    parts = re.split(r"^---\s*$", md, maxsplit=1, flags=re.M)
    if len(parts) == 2 and len(parts[1].split()) > 80:
        md = parts[1]
    md = _letterhead(md)
    return _letterhead(md)


def strip(md):
    """Reduce markdown to the prose a reader actually reads.

    Everything removed here is exempt by doctrine: quoted material keeps its source's habits,
    identifiers are not prose, and tables/headings are counted separately rather than parsed.
    """
    md = re.sub(r"\A---\n.*?\n---\n", "", md, count=1, flags=re.S)   # frontmatter
    # A draft may keep internal commentary under a "Notes on the draft" heading in the same file.
    # Only the part that actually gets sent is measured.
    md = re.split(r"^#+\s*Notes on the draft\b", md, maxsplit=1, flags=re.M | re.I)[0]
    # A draft in exports/ may wrap the sendable text in an internal preamble (a title, a "Not sent"
    # banner, a status note) separated by a horizontal rule. Measure what actually gets sent, not
    # the wrapper around it.
    parts = re.split(r"^---\s*$", md, maxsplit=1, flags=re.M)
    if len(parts) == 2 and len(parts[1].split()) > 80:
        md = parts[1]
    md = re.sub(r"```.*?```", " ", md, flags=re.S)                    # code fences
    md = re.sub(r"^\s*>.*$", "", md, flags=re.M)                      # blockquotes (quoted source)
    md = re.sub(r"^\s*\|.*$", "", md, flags=re.M)                     # tables
    md = re.sub(r"^\s*#{1,6}\s.*$", "", md, flags=re.M)               # headings
    # A list item is its own unit. Terminate it so it does not merge with the next one, then let
    # ordinary soft-wrapped prose rejoin normally in sentences().
    # Each becomes its own block, so consecutive bullets cannot merge into one giant unit -- the
    # terminal-punctuation split alone will not separate them when the next item starts lowercase.
    md = re.sub(r"^\s*(?:[-*+]|\d+[.)]|\(?[a-z][.)])\s+(.*?)([.!?:;]?)\s*$",
                lambda m: "\n" + m.group(1) + (m.group(2) or ".") + "\n", md, flags=re.M)
    md = re.sub(r"\[\[[^\]]*\]\]", "X", md)                           # wikilinks
    md = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", md)                # links/images
    md = re.sub(r"`[^`]*`", "X", md)                                  # inline code
    md = re.sub(r"\*\*|\*|__|^---+$", "", md, flags=re.M)             # emphasis, rules
    md = re.sub(r"</?(?:u|b|i|strong|em)>", "", md)                   # inline html emphasis
    return md


def sentences(text):
    # Source files are hard-wrapped, so a single newline inside a paragraph is a soft wrap and must
    # rejoin. Paragraph breaks (blank lines) end a unit; list items were terminated in strip().
    out = []
    for para in re.split(r"\n\s*\n", text):
        # A label line ends a unit the way a blank line does. Without this, "Conflicts of Interest:
        # None I've identified" glues onto the sentence below it and invents a 44-word sentence that
        # nobody wrote. Labels are furniture, so they are dropped
        # rather than measured -- LABEL_LINE runs after strip() has already removed emphasis, so a
        # bold label is caught too.
        for block in LABEL_LINE.split(para):
            flat = re.sub(r"\s+", " ", block).strip()
            if not flat or LABEL_LINE.fullmatch(flat):
                continue
            out += re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", flat)
    return [s.strip() for s in out if len(s.split()) > 2]


def units(text):
    """Every unit the splitter produces, including the ones too short to be a sentence. The
    fragment signal needs these; sentences() drops them on purpose."""
    out = []
    for para in re.split(r"\n\s*\n", text):
        for block in LABEL_LINE.split(para):
            flat = re.sub(r"\s+", " ", block).strip()
            if not flat or LABEL_LINE.fullmatch(flat):
                continue
            out += re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", flat)
    return [s.strip() for s in out if s.strip()]


def measure(md, artifact="any"):
    scope = _scope(md)          # the sendable region, headings and all
    prose = strip(md)
    words = len(prose.split())
    if words == 0:
        raise ValueError("no prose found after stripping markdown")

    sents = sentences(prose)
    L = [len(s.split()) for s in sents]
    paras = [len(p.split()) for p in re.split(r"\n\s*\n", prose) if len(p.split()) > 10]

    # An em dash within the first few words of a unit is a label separator, a common human habit.
    # Past that it is the cadence tell.
    cadence = turn = 0
    for s in sents:
        for match in re.finditer("—", s):
            if len(s[:match.start()].split()) > LABEL_DASH_MAX_WORDS:
                cadence += 1
                if TURN_AFTER_DASH.match(s[match.end():].strip()):
                    turn += 1

    per1k = lambda n: n * 1000.0 / words
    m = {
        "words": words,
        "sentences": len(L),
        "emdash_per_1k": per1k(prose.count("—")),
        "cadence_dash_per_1k": per1k(cadence),
        "turn_dash": float(turn),
        "tricolon_per_1k": per1k(len(re.findall(r"\b\w+, [\w\s'-]{1,30}, and \w", prose))),
        "_tricolon_n": len(re.findall(r"\b\w+, [\w\s'-]{1,30}, and \w", prose)),
        "_flip_n": len(re.findall(
            r"\b(?:isn'?t|aren'?t|wasn'?t|not|never)\b[^.\n]{0,70}?"
            r"(?:,\s?but\b|—\s?it'?s\b|\.\s+It'?s\b|,\s?it'?s\b)", prose, re.I)),
        "flip_per_1k": per1k(len(re.findall(
            r"\b(?:isn'?t|aren'?t|wasn'?t|not|never)\b[^.\n]{0,70}?"
            r"(?:,\s?but\b|—\s?it'?s\b|\.\s+It'?s\b|,\s?it'?s\b)", prose, re.I))),
        "heading_per_500": len(re.findall(r"^\s*#{1,6}\s", scope, flags=re.M)) * 500.0 / words,
    }
    allu = units(prose)
    frag = [u for u in allu if len(u.split()) <= FRAGMENT_MAX_WORDS and u[-1:] in ".!?"]
    m["fragment_share"] = len(frag) / len(allu) if allu else 0.0
    m["colon_setup_per_1k"] = per1k(sum(1 for s in sents if COLON_SETUP.match(s)))
    m["hedge_per_100w"] = len(re.findall(HEDGE, prose, re.I)) * 100.0 / words
    m["markers_per_1k"] = per1k(sum(len(re.findall(pat, prose, re.M)) for pat in MARKERS))
    if L:
        m["max_sentence"] = float(max(L))
        stack = 0
        restate = 0
        for s in sents:
            if len(re.findall(HEDGE, s, re.I)) >= 2:
                stack += 1
            words = [w.lower() for w in re.findall(r"\b[a-z]{5,}\b", s)
                     if w.lower() not in FUNCTION_WORDS]
            if any(words.count(w) > 1 for w in set(words)):
                restate += 1
        m["hedge_stack"] = float(stack)
        m["restatement"] = float(restate)
        mean = st.mean(L)
        m["burstiness"] = st.pstdev(L) / mean if mean else 0.0
        m["short_share"] = sum(1 for x in L if x < SHORT_W) / len(L)
        m["long_share"] = sum(1 for x in L if x > LONG_W) / len(L)
        m["mean_sentence"] = mean
    if len(paras) >= 3:
        pm = st.mean(paras)
        m["para_cv"] = st.pstdev(paras) / pm if pm else 0.0

    hits = []
    for patterns, source in ((BANNED, prose), (BANNED_RAW, scope)):
        for pat, label in patterns:
            for match in re.finditer(pat, source, re.I | re.M):
                line = source[:match.start()].count("\n") + 1
                hits.append({"label": label, "text": match.group(0).strip()[:70], "line": line})
    m["banned"] = float(len(hits))
    m["_hits"] = hits
    return m


def evaluate(m, artifact="any", path=""):
    exempt = set(ARTIFACT_EXEMPT.get(artifact, ARTIFACT_EXEMPT["any"]))
    # style/voice.md puts imports/ out of scope wholesale: it is somebody else's writing, and
    # their habits are not ours to score.
    if re.search(r"(^|/)imports/", path):
        exempt |= {"banned"}

    results = []
    for key, (op, limit, label) in THRESHOLDS.items():
        if key in exempt or key not in m:
            continue
        if key == "heading_per_500" and artifact == "correspondence":
            limit = CORRESPONDENCE_HEADING_MAX
        val = m[key]
        ok = val >= limit if op == ">=" else val <= limit
        # A rate signal needs enough raw instances before it means anything.
        n = m.get("_" + key.replace("_per_1k", "_n"))
        if not ok and n is not None and n < MIN_COUNT_TO_CONVICT:
            ok = True
        results.append({"key": key, "label": label, "value": val, "op": op, "limit": limit,
                        "ok": ok, "group": "concision" if key in CONCISION else "fidelity"})
    return results


def report(path, m, results, artifact):
    failed = [r for r in results if not r["ok"]]
    print(f"\n\033[1m{path}\033[0m  ({artifact}, {m['words']} words, {m['sentences']} sentences)\n")
    for group, title in (("fidelity", "voice — does this sound like the model wrote it"),
                         ("concision", "concision — your voice, fewer words")):
        rows = [r for r in results if r["group"] == group]
        if not rows:
            continue
        print(f"  \033[2m{title}\033[0m")
        for r in rows:
            mark = "\033[32mok  \033[0m" if r["ok"] else "\033[31mFAIL\033[0m"
            print(f"  {mark} {r['label']:<44} {r['value']:6.2f}  (want {r['op']} {r['limit']:.2f})")
        print()

    info = [(k, m[k]) for k in INFORMATIONAL if k in m]
    if info:
        print("\n  for context, not scored:")
        for k, v in info:
            print(f"    {k:<16} {v:6.2f}")

    if m["_hits"]:
        print("\n  banned patterns:")
        for h in m["_hits"][:20]:
            print(f"    line ~{h['line']:<4} {h['label']:<28} \"{h['text']}\"")
        if len(m["_hits"]) > 20:
            print(f"    ... and {len(m['_hits']) - 20} more")

    nf = len([r for r in failed if r["group"] == "fidelity"])
    nc = len([r for r in failed if r["group"] == "concision"])
    print()
    if nf >= FAIL_AT:
        print(f"  \033[31mREVISE — voice\033[0m  {nf} signals. This reads as machine-written. "
              f"Convergence is the fingerprint; fix the cluster, not the instance.")
    elif nf:
        print(f"  \033[33madvisory — voice\033[0m  {nf} signal(s), below the {FAIL_AT}-signal "
              f"threshold. Each has an innocent explanation on its own.")
    else:
        print("  \033[32mvoice: clean\033[0m")

    if nc:
        print(f"  \033[33mTIGHTEN\033[0m  {nc} concision signal(s). Not a slop problem — this is "
              f"the writer's own habit. See style/target.md for what to cut and what to keep.")
    else:
        print("  \033[32mconcision: clean\033[0m")
    print("\n  Reported, not corrected. See style/tells.md.\n")
    return nf


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--artifact-type", default="any", choices=sorted(ARTIFACT_EXEMPT))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="one line per file")
    a = ap.parse_args()

    worst = 0
    out = []
    for path in a.files:
        try:
            md = open(path, encoding="utf-8").read()
            m = measure(md, a.artifact_type)
        except (OSError, ValueError) as e:
            print(f"{path}: {e}", file=sys.stderr)
            worst = max(worst, 2)
            continue
        results = evaluate(m, a.artifact_type, path)
        n = len([r for r in results if not r["ok"] and r["group"] == "fidelity"])
        nc = len([r for r in results if not r["ok"] and r["group"] == "concision"])
        if a.json:
            out.append({"file": path, "artifact_type": a.artifact_type, "failed": n,
                        "metrics": {k: v for k, v in m.items() if not k.startswith("_")},
                        "signals": results, "hits": m["_hits"]})
        elif a.quiet:
            verdict = "REVISE" if n >= FAIL_AT else ("advisory" if n else "clean")
            print(f"voice {n} {verdict:<9} tighten {nc}   {path}")
        else:
            report(path, m, results, a.artifact_type)
        worst = max(worst, 1 if n >= FAIL_AT else 0)

    if a.json:
        print(json.dumps(out, indent=2))
    return worst


if __name__ == "__main__":
    sys.exit(main())
