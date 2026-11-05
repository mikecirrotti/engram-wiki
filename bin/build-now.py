#!/usr/bin/env python3
"""Build now.md: a short, generated snapshot of what is in motion, loaded at the start of a session.

    python3 bin/build-now.py            write now.md if its content changed
    python3 bin/build-now.py --check    exit 1 if now.md is out of date, write nothing
    python3 bin/build-now.py --stdout   print what would be written

The idea is borrowed from Meta Muse, which injects a curated MEMORY.md into every turn. AGENTS.md
and preferences/ already load the rules every session; this file loads the state, so a session
starts knowing what is open instead of searching for it.

Everything here is derived from structure the wiki already has -- frontmatter fields and unchecked
checkboxes -- so no AI is involved and the output is the same every time for the same repo. That is
what lets a GitHub Action commit it unattended: there is no judgment in it to review.

Two properties keep the nightly commit quiet:
  - Dates, never ages. "updated 2026-09-20" stays true tomorrow; "21 days ago" would change every
    night and produce a commit every night.
  - The generated: date only moves when the body moves. A night with no changes writes nothing.

Standard library only, so the GitHub runner needs no install step.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "now.md"

QUIET_AFTER_DAYS = 21     # an in-motion project untouched this long is flagged
MAX_TODOS = 15
MAX_DECISIONS = 5
MAX_RECENT = 8
TODO_CHARS = 140

# Project status is free text ("moving forward -- awaiting revised quote"), so it is bucketed by
# keyword. Anything that matches none of these counts as in motion: a new status word should show
# up, not vanish.
DONE = re.compile(r"\b(shipped|done|complete|completed|archived|abandoned|dropped|closed)\b", re.I)
PARKED = re.compile(r"\b(on hold|paused|parked|deferred|blocked)\b", re.I)
EXPLORING = re.compile(r"\b(idea|exploratory|exploring)\b", re.I)

DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def frontmatter(path: Path) -> dict[str, str]:
    """Top-level `key: value` pairs from the leading --- block. Enough for this repo's notes."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip().strip("\"'")
    return fields


def first_date(value: str) -> str:
    m = DATE.search(value or "")
    return m.group(0) if m else ""


def title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def link(path: Path) -> str:
    return f"[[{path.relative_to(ROOT).with_suffix('').as_posix()}]]"


def clean_todo(text: str) -> str:
    """One line, bounded, and never a half-open wikilink or bold marker."""
    text = text.replace("**", "").strip().rstrip(" —-:")
    if len(text) > TODO_CHARS:
        text = text[:TODO_CHARS].rsplit(" ", 1)[0]
        if text.count("[[") > text.count("]]"):
            text = text[: text.rfind("[[")].rstrip()
        text = text.rstrip(" ,;.—-:") + "…"
    return text


# --- sections ------------------------------------------------------------------------------------

def projects(today: dt.date) -> list[str]:
    moving, exploring, parked = [], [], []
    for p in sorted((ROOT / "projects").glob("*.md")):
        fm = frontmatter(p)
        status = fm.get("status", "").strip()
        updated = first_date(fm.get("updated", ""))
        if DONE.search(status):
            continue
        entry = (updated, p, status)
        if PARKED.search(status):
            parked.append(entry)
        elif EXPLORING.search(status):
            exploring.append(entry)
        else:
            moving.append(entry)

    def by_recent(rows):
        return sorted(rows, key=lambda r: (r[0], r[1].name), reverse=True)

    out = ["## In motion", ""]
    for updated, p, status in by_recent(moving):
        quiet = ""
        if updated and (today - dt.date.fromisoformat(updated)).days > QUIET_AFTER_DAYS:
            quiet = f" — **quiet since {updated}**"
        out.append(f"- {link(p)} — {status or 'no status'} (updated {updated or '?'}){quiet}")
    if not moving:
        out.append("- Nothing marked active.")

    if exploring:
        out += ["", "Exploring: " + ", ".join(link(p) for _, p, _ in by_recent(exploring)) + "."]
    if parked:
        out += ["", "Parked: " + ", ".join(f"{link(p)} ({s})" for _, p, s in by_recent(parked)) + "."]
    return out


def open_loops() -> list[str]:
    """Unchecked boxes in daily/ and meetings/. The morning ritual carries todos forward, so the
    same item often appears in several dailies; the newest copy wins."""
    found: list[tuple[str, str, Path]] = []
    sources = [(p, p.stem) for p in (ROOT / "daily").glob("*.md")]
    sources += [(p, first_date(frontmatter(p).get("updated", ""))) for p in (ROOT / "meetings").glob("*.md")]
    for path, when in sources:
        lines = path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            m = re.match(r"^\s*- \[ \]\s+(\S.*)$", line)
            if not m:
                continue
            text = clean_todo(m.group(1))
            # A wrapped item continues on an indented line; show only its first line, marked as cut.
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if nxt.startswith("  ") and nxt.strip() and not text.endswith("…"):
                text = text.rstrip(" ,;.—-:") + "…"
            found.append((when or "", text, path))

    seen: set[str] = set()
    rows = []
    for when, text, path in sorted(found, key=lambda r: (r[0], r[2].name), reverse=True):
        key = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()[:40]
        if key in seen:
            continue
        seen.add(key)
        rows.append(f"- [ ] {text} — {link(path)}")

    out = ["## Open loops", ""]
    if not rows:
        return out + ["- None open."]
    out += rows[:MAX_TODOS]
    if len(rows) > MAX_TODOS:
        out.append(f"- …and {len(rows) - MAX_TODOS} more in `daily/` and `meetings/`.")
    return out


def decisions() -> list[str]:
    rows = []
    for p in (ROOT / "decisions").glob("*.md"):
        fm = frontmatter(p)
        if fm.get("superseded_by", "").strip("[] "):
            continue
        rows.append((first_date(fm.get("date", "")) or p.stem[:10], p))
    rows.sort(key=lambda r: (r[0], r[1].name), reverse=True)
    out = ["## Recent decisions", ""]
    out += [f"- {d} — {title(p)} — {link(p)}" for d, p in rows[:MAX_DECISIONS]] or ["- None yet."]
    return out


def recently_updated() -> list[str]:
    rows = []
    for folder in ("people", "projects", "topics", "meetings"):
        for p in (ROOT / folder).glob("*.md"):
            d = first_date(frontmatter(p).get("updated", ""))
            if d:
                rows.append((d, p))
    rows.sort(key=lambda r: (r[0], r[1].as_posix()), reverse=True)
    out = ["## Recently updated", ""]
    out += [f"- {d} — {link(p)}" for d, p in rows[:MAX_RECENT]] or ["- Nothing yet."]
    return out


def housekeeping() -> list[str]:
    inbox = ROOT / "inbox.md"
    pending = 0
    if inbox.exists():
        for line in inbox.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^- (.+)$", line)
            if m and m.group(1).strip() and not m.group(1).lstrip().startswith("~~"):
                pending += 1
    # No "indexes last rebuilt" line: the same nightly job rebuilds them, so the date would change
    # every night and turn a quiet night into a commit.
    return [
        "## Housekeeping",
        "",
        f"- Inbox: {pending} item{'s' if pending != 1 else ''} waiting for triage.",
    ]


# --- assembly ------------------------------------------------------------------------------------

def body(today: dt.date) -> str:
    parts = [
        "# Now",
        "",
        "Generated by `bin/build-now.py` from frontmatter and unchecked boxes. **Do not edit by hand**;",
        "the next build overwrites it. Change the source note instead.",
        "",
    ]
    for section in (projects(today), open_loops(), decisions(), recently_updated(), housekeeping()):
        parts += section + [""]
    return "\n".join(parts).rstrip() + "\n"


def existing_body() -> str:
    if not OUT.exists():
        return ""
    text = OUT.read_text(encoding="utf-8")
    m = re.match(r"^---\n.*?\n---\n\n?", text, re.S)
    return text[m.end():] if m else text


def main(argv: list[str]) -> int:
    today = dt.date.today()
    new_body = body(today)
    document = f"---\ntype: index\ngenerated: {today.isoformat()}\n---\n\n{new_body}"

    if "--stdout" in argv:
        sys.stdout.write(document)
        return 0
    changed = new_body != existing_body()
    if "--check" in argv:
        print("now.md is out of date." if changed else "now.md is current.")
        return 1 if changed else 0
    if not changed:
        print("now.md unchanged; nothing written.")
        return 0
    OUT.write_text(document, encoding="utf-8")
    print("now.md written.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
