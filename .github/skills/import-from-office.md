---
type: skill
trigger: "read the file I dropped" / "import this file" / "I dropped a file in imports" / "use [file] as context"
updated: YYYY-MM-DD
---

# Skill: import-from-office

Read and use content from a `.docx` or `.pptx` file the user has dropped into `imports/inbox/`.

This skill extracts both the text/structure (via Pandoc) and the formatting metadata (via Python) so the assistant can use the file as full context for drafting, analysis, or matching style.

> Note: the extraction script (`bin/import.sh` / `bin/import.ps1`) is an optional helper that
> ships *un*built in this scaffold. Build it against Pandoc + `python-docx`/`python-pptx` when
> you first need Office import (see the setup guide's Step 8b / Step 9).

## Workflow

### Step 1 — Run the extraction script

Run `bin/import.ps1` (Windows) or `bin/import.sh` (macOS/Linux) to process any unextracted files in `imports/inbox/`. This produces two files in `imports/extracted/` for each source file:
- `<basename>.md` — full text content and document structure
- `<basename>.styles.txt` — formatting metadata (styles, fonts, sizes, layout)

### Step 2 — Read both extracted files

After extraction, read both files. Do not attempt to read the `.docx` or `.pptx` directly — they are binary.

### Step 3 — Confirm what was found

Tell the user briefly what the file contains:
- For .docx: document structure (headings, sections, approximate length), and key style conventions (heading fonts/sizes, body font, margins).
- For .pptx: number of slides, slide layouts used, theme, and a summary of slide titles.

Keep this to 3–5 bullet points. Ask what they want to do with it.

### Step 4 — Proceed with the task

Common follow-on tasks:
- **Draft a new document matching this style** → use the `.styles.txt` to inform formatting choices.
- **Analyze or summarize content** → use the `.md` file as source material.
- **Extract action items or decisions** → promote to wiki files as appropriate.
- **Use as a template reference** → note the style conventions for future drafts.
