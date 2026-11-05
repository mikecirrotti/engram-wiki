#!/usr/bin/env python3
"""Regenerate the cross-references in indexes/ from frontmatter.

    python3 bin/build-indexes.py            write any index whose content changed
    python3 bin/build-indexes.py --check    exit 1 if any index is out of date, write nothing

This is the rebuild-indexes skill turned into code, so it can run nightly with no AI. The skill
asked a model to scan every file and regroup it by hand, which meant the indexes were only as fresh
as the last time someone remembered to ask.

Five indexes, same shapes as before:
  by-person.md   every note, grouped by the people: field
  by-topic.md    every note, grouped by the topics: field
  by-type.md     every note, grouped by type:
  recent.md      notes dated in the last 30 days
  network.md     person_note files by last_contact, coldest first

Scope: decisions/, meetings/, people/, topics/, projects/ with its subfolders, and top-level
exports/. daily/ is the river and is left out, as it always was.

Like build-now.py: standard library only, and generated: moves only when the body moves, so a night
with no changes writes nothing.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "indexes"
RECENT_DAYS = 30

DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
LINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")


# --- reading notes -------------------------------------------------------------------------------

def frontmatter(path: Path) -> dict[str, str]:
    """Top-level fields. A key with an empty value followed by `- item` lines gets those items
    joined with commas, so list-form and inline-form fields parse the same way."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields: dict[str, str] = {}
    key = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            fields[key] = m.group(2).strip()
            continue
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and key:
            fields[key] = (fields[key] + ", " if fields[key] else "") + item.group(1).strip()
    return fields


def values(raw: str) -> list[str]:
    """Wikilink targets if there are any, otherwise bare comma-separated words."""
    raw = re.sub(r"\s+#.*$", "", raw or "")          # trailing YAML comment
    links = LINK.findall(raw)
    if links:
        return [l.strip() for l in links]
    raw = raw.strip().strip("[]")
    return [w.strip().strip("\"'") for w in raw.split(",") if w.strip().strip("\"'")]


def slug(word: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", word.lower()).strip("-")


def note_date(path: Path, fm: dict[str, str]) -> str:
    for key in ("updated", "date"):
        m = DATE.search(fm.get(key, ""))
        if m:
            return m.group(0)
    m = DATE.match(path.name)
    return m.group(0) if m else ""


def notes() -> list[dict]:
    paths = []
    for folder in ("decisions", "meetings", "people", "topics"):
        paths += sorted((ROOT / folder).glob("*.md"))
    # projects/ includes its subfolders, so notes filed under a project folder are indexed.
    # build-now.py deliberately does not: a supporting note is not a project in motion.
    paths += sorted((ROOT / "projects").rglob("*.md"))
    paths += sorted((ROOT / "exports").glob("*.md"))
    out = []
    for p in paths:
        fm = frontmatter(p)
        t = fm.get("type", "").strip().strip("\"'")
        if not t:
            continue
        rel = p.relative_to(ROOT).with_suffix("").as_posix()
        out.append({"path": rel, "type": t, "date": note_date(p, fm), "fm": fm})
    return out


def newest_first(rows: list[dict]) -> list[dict]:
    return sorted(rows, key=lambda n: (n["date"], n["path"]), reverse=True)


def heading(target: str, folder: str, kind: str) -> tuple[str, str]:
    """(sort key, heading text). A link that resolves gets a wikilink; a bare word that matches a
    file is linked too; anything else is named and marked as having no file."""
    if "/" in target:
        name = target.split("/")[-1]
        if (ROOT / f"{target}.md").exists():
            return name, f"[[{target}]]"
        # A link to a note not written yet. Named, not linked, so the index carries no dead links.
        return name, f"{name} *(no {kind} file)*"
    s = slug(target)
    if (ROOT / folder / f"{s}.md").exists():
        return s, f"[[{folder}/{s}]]"
    return s, f"{s} *(no {kind} file)*"


# --- the indexes ---------------------------------------------------------------------------------

def grouped(all_notes: list[dict], field: str, folder: str, kind: str, title: str) -> str:
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for n in all_notes:
        for v in values(n["fm"].get(field, "")):
            groups[heading(v, folder, kind)].append(n)
    lines = [f"# Index — {title}", ""]
    for (_, head), rows in sorted(groups.items()):
        lines += [f"## {head}", ""]
        lines += [f"- [[{n['path']}]] ({n['type']}) — {n['date'] or 'undated'}" for n in newest_first(rows)]
        lines.append("")
    return "\n".join(lines)


def by_type(all_notes: list[dict]) -> str:
    groups: dict[str, list[dict]] = defaultdict(list)
    for n in all_notes:
        groups[n["type"]].append(n)
    lines = ["# Index — By Type", ""]
    for t in sorted(groups):
        lines += [f"## {t}", ""]
        lines += [f"- [[{n['path']}]] — {n['date'] or 'undated'}" for n in newest_first(groups[t])]
        lines.append("")
    return "\n".join(lines)


def recent(all_notes: list[dict], today: dt.date) -> str:
    cutoff = (today - dt.timedelta(days=RECENT_DAYS)).isoformat()
    rows = [n for n in all_notes if n["date"] and n["date"] >= cutoff]
    lines = [f"# Index — Recent (last {RECENT_DAYS} days)", ""]
    lines += [f"- {n['date']} — [[{n['path']}]] ({n['type']})" for n in newest_first(rows)]
    return "\n".join(lines) + "\n"


def network(all_notes: list[dict]) -> str:
    known, unknown = [], []
    for n in all_notes:
        if n["type"] != "person_note":
            continue
        m = DATE.search(n["fm"].get("last_contact", ""))
        (known if m else unknown).append((m.group(0) if m else "", n["path"]))
    lines = ["# Index — Network (by last contact, coldest first)", ""]
    lines += [f"- [[{p}]] — last contact {d}" for d, p in sorted(known)]
    if unknown:
        lines += ["", "## Unknown last contact", ""]
        lines += [f"- [[{p}]]" for _, p in sorted(unknown)]
    return "\n".join(lines) + "\n"


# --- writing -------------------------------------------------------------------------------------

def body_of(path: Path) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n.*?\n---\n\n?", text, re.S)
    return text[m.end():] if m else text


def main(argv: list[str]) -> int:
    today = dt.date.today()
    all_notes = notes()
    built = {
        "by-person.md": grouped(all_notes, "people", "people", "person", "By Person"),
        "by-topic.md": grouped(all_notes, "topics", "topics", "topic", "By Topic"),
        "by-type.md": by_type(all_notes),
        "recent.md": recent(all_notes, today),
        "network.md": network(all_notes),
    }
    stale = []
    for name, body in built.items():
        body = body.rstrip() + "\n"
        path = OUT / name
        if body == body_of(path):
            continue
        stale.append(name)
        if "--check" not in argv:
            path.write_text(f"---\ntype: index\ngenerated: {today.isoformat()}\n---\n\n{body}", encoding="utf-8")

    if "--check" in argv:
        print(f"Out of date: {', '.join(stale)}." if stale else "Indexes are current.")
        return 1 if stale else 0
    print(f"Rebuilt: {', '.join(stale)}." if stale else "Indexes unchanged; nothing written.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
