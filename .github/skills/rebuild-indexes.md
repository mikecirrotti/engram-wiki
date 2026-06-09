---
type: skill
trigger: "rebuild indexes"
updated: YYYY-MM-DD
---

# Rebuild Indexes

The `indexes/` folder contains generated cross-reference files.

## Procedure

1. Scan every content file for YAML frontmatter.
2. For each index file, group entries by the relevant field, sort by date descending.
3. Update the `generated:` field in the index's frontmatter to today's date.
4. The index files to maintain: `by-person.md`, `by-topic.md`, `by-type.md`, `recent.md` (most recently modified, last 30 days).

If an index file doesn't exist yet, create it. Use this frontmatter for indexes:

```yaml
---
type: index
generated: YYYY-MM-DD
---
```
