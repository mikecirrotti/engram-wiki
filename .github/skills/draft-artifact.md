---
type: skill
trigger: drafting any artifact (memo, slide, email, technical doc, one-pager)
updated: YYYY-MM-DD
---

# Draft Artifact

## Before writing a single line

1. Identify the artifact type — memo, deck, Slack/email, technical doc, etc. If unclear, ask once.
2. Identify the audience — e.g. executives, technical peers, business partners, non-technical peers, manager. If unclear, default to non-technical senior leaders and note the assumption.
3. Read `style/voice.md` (always).
4. Read `style/<artifact-type>.md`.
5. Read `style/audiences/<audience>.md`.
6. Read any project context: `projects/<project>.md` if the artifact is project-specific.
7. THEN draft.

## After delivering the draft

Briefly note which style files you consulted and any rules you deliberately broke (with reasoning). The user values knowing what conventions are in play.

If style files contradict each other or the user's request, surface the contradiction rather than silently picking a side.

If you find yourself wanting to apply a convention that isn't yet in the style files, mention it at the end — it might be worth adding to the relevant file. The style files grow through this kind of suggestion.

## After the user reviews the draft

If the user makes substantive edits, offer to extract conventions from those edits and propose additions to the relevant style file. Phrasing: "Want me to capture the patterns in your edits as additions to `style/<file>.md`?" This is the primary growth mechanism for the style guides. (This is the same loop as the feedback-to-wiki agent in Step 9.5.)
