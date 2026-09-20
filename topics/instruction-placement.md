---
type: topic
name: instruction-placement
updated: YYYY-MM-DD
topics: [wiki-architecture]
---

# Where rules should live

A wiki like this has several places to put instructions: the standing instruction files (AGENTS.md,
preferences/), the style system (style/), the skills (.github/skills/), and client-specific files
(CLAUDE.md, .github/copilot-instructions.md). The question of which file gets a rule matters more
than it looks, because a rule filed in the wrong place will silently fail to load in the sessions
where it is needed.

## The test

Name the sessions where a rule should apply. If the answer is "all of them," it lives in a file
that is loaded unconditionally -- AGENTS.md or preferences/. If the answer is "only when I am
drafting" or "only in a meeting," it lives in a skill that fires on that trigger.

A rule that applies in all sessions may not live behind a trigger, whatever file it is written in.
A skill loads only when its trigger fires. A topic file loads only when the assistant decides to
read it. Neither of those is "always."

## Why this matters

The failure mode is not dramatic. The assistant does not refuse to follow the rule -- it never sees
it. Spelling conventions, for example, apply in every session. If they live only in a style file
that loads before drafting tasks, they will not be in the room when the assistant is writing a hook
script, a test harness, or a commit message. The drift happens in the genres where the rule was
never loaded.

## The layers

1. **preferences/** -- loaded unconditionally at the start of every interaction. Governs
   conversation: how the assistant talks to you.
2. **AGENTS.md** -- loaded unconditionally. Governs standing behaviors: contextual retrieval,
   capture, staleness detection, the directory map, the writing procedure, immutability rules.
3. **style/** -- loaded before drafting tasks. Governs artifacts that leave the repo.
4. **skills/** -- loaded on trigger. Each skill prescribes which style files to read.
5. **Client-specific files** (CLAUDE.md, .github/copilot-instructions.md) -- loaded by one client
   only. Carry only what is specific to that client.

A rule that you want enforced mechanically (not just followed when the assistant remembers)
belongs in a hook or a checker, not in any of these files. See `hooks/policy/` if you build
enforcement infrastructure.
