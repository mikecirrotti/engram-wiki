---
type: skill
trigger: drafting any artifact (memo, slide, email, technical doc, one-pager)
updated: YYYY-MM-DD
---

# Draft Artifact

## Before writing a single line

1. Identify the artifact type -- memo, deck, Slack/email, technical doc, correspondence, etc. If
   unclear, ask once.
2. Identify the audience -- e.g. executives, technical peers, business partners, non-technical
   peers, one named person. If unclear, default to non-technical senior leaders and note the
   assumption.
3. Read the style files in this order:
   - `style/voice.md` (always)
   - `style/tells.md` (always, if it exists and is populated)
   - `style/target.md` (always, if it exists)
   - `style/<artifact-type>.md` (memo, slides, email, technical-docs, correspondence)
   - `style/audiences/<audience>.md`
   - `style/positioning.md` (if the artifact speaks publicly as the user)
   - Corpus samples in `style/corpus/` (if they exist -- read two or three for calibration)
4. Read any project context: `projects/<project>.md` if the artifact is project-specific.
5. THEN draft.

## While drafting

If `style/tells.md` is populated, actively check your draft against the convergence rule: no
cluster of three or more tells in the same passage. Fix clusters before presenting the draft.

If `style/target.md` exists and has a populated "Cut" list, apply those concision rules before
presenting. The user should see the tightened version, not the first pass.

## After delivering the draft

Briefly note which style files you consulted and any rules you deliberately broke (with reasoning).
The user values knowing what conventions are in play.

If style files contradict each other or the user's request, surface the contradiction rather than
silently picking a side.

If you find yourself wanting to apply a convention that is not yet in the style files, mention it
at the end -- it might be worth adding. The style files grow through this kind of suggestion.

## After the user reviews the draft

If the user makes substantive edits, offer to extract conventions from those edits and propose
additions to the relevant style file. Phrasing: "Want me to capture the patterns in your edits
as additions to `style/<file>.md`?" This is the primary growth mechanism for the style guides
(the same loop as the feedback-to-wiki skill).

## Optional: run the voice-reviewer

For anything public-facing or high-stakes, invoke `.github/agents/voice-reviewer.md` on the draft
before presenting. It enumerates tells without rewriting. Fix convergence clusters it flags, then
present the clean version.
