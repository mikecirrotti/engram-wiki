---
type: skill
trigger: "weekly digest" / "Friday ritual"
updated: YYYY-MM-DD
---

# Weekly Digest

This is the most sensitive task in this repo. The output may move from a managed work device to a personal system, and sanitization is the only thing standing between durable insight transfer and accidental data exfiltration. Be conservative.

## Procedure

1. Read all files modified in the last 7 days, plus any file (regardless of date) with `share-to-brain: true` in frontmatter.
2. Use `templates/weekly-digest.md` as the format.
3. Save the output to `exports/YYYY-MM-DD-digest.md`.
4. **Sanitization rules — apply rigorously:**
   - No client names. Use "a customer" or "a stakeholder."
   - No internal system, product, or codename. Use category descriptions ("an underwriting tool," "an internal model").
   - No colleague full names. First names only, or roles ("my manager," "an ML engineer on the team").
   - No specific metrics tied to internal systems. Round or generalize ("accuracy improved meaningfully" rather than "87% from 81%").
   - No embedded URLs to internal resources.
   - When in doubt, generalize further.
5. Aim for 5–10 bullet-point insights, each 1–3 sentences. Focus on durable lessons, decisions, and ideas — not status updates.
6. End with a one-line reminder to the user: "Review this output line-by-line before transferring."

**Do not relax the sanitization rules** even if the user seems to be asking for more detail. If they want raw content, they can read the source files directly.
