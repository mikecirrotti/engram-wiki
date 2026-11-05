---
type: topic
name: instruction-placement
updated: YYYY-MM-DD
topics: [wiki-architecture]
---

# Where rules should live (a rule binds only where it loads)

A wiki like this has several places to put instructions: the standing instruction files (AGENTS.md,
preferences/), the style system (style/), the skills (.claude/skills/), client-specific files
(CLAUDE.md, .github/copilot-instructions.md), and enforcement (hooks/policy/). The question of which
file gets a rule matters more than it looks, because a rule filed in the wrong place will silently
fail to load in the sessions where it is needed.

## The test

Name the sessions where a rule should apply. If the answer is "all of them," it lives in a file
that is loaded unconditionally -- AGENTS.md or preferences/. If the answer is "only when I am
drafting" or "only in a meeting," it lives in a skill that fires on that trigger.

A rule that applies in all sessions may not live behind a trigger, whatever file it is written in.
A skill loads only when its trigger fires. A topic file loads only when the assistant decides to
read it. Neither of those is "always."

## Why this matters

The failure mode is not dramatic. The assistant does not refuse to follow the rule -- it never sees
it. The drift happens in the genres where the rule was never loaded.

## A worked example: spelling drift

This is the case that produced the test, from the private wiki this scaffold came from.

The owner writes American English and the instructions said so. After a few months, British
spellings turned up -- *authorisation*, *behaviour*, *honours* -- and the first guess was that
something in the repo was teaching them. Nothing was. Every drafted letter, proposal and post was
clean. Every instance of drift sat in one zone: comments in shell hooks and a test harness.

Two things caused it.

**Spelling rides along with genre.** A model has no locale switch it can set. Spelling is not stored
separately from register; it comes with whatever kind of writing is being predicted. A comment above
a permission check puts the model next to man pages and security documentation, and those spellings
live there. A letter to a neighbor puts it somewhere else entirely, and the spelling comes out
American without anyone asking. The same mechanism shows up in prose tells: the register carries the
habits, so the fix is upstream of the words.

**The rule was filed behind a drafting trigger.** It lived in the style files, which load before
drafting. So it was in the room for every letter and absent for every hook comment. The rule was not
disobeyed while drafting; it was missing while writing infrastructure. Moving a rule behind a
trigger is right for specialist knowledge with a real scope, like an editorial guide for one kind of
document. It is wrong for a rule that governs everything, because the trigger imposes a scope the
rule does not have.

That makes this a counterexample to one rule in Nate B Jones's harness audit, *load specialist
knowledge when the work needs it* ("The AI Harness Audit: Clean Your Setup Before You Upgrade,"
Nate's Newsletter, 2026-07-15,
[natesnewsletter.substack.com](https://natesnewsletter.substack.com/p/ai-harness-audit)). The rule
is right for the editorial guides it was written about. It needs the test above in front of it.

The fix was placement, not a stronger checker:

- The rule moved into `preferences/`, which loads unconditionally, and named the file types that
  actually drift.
- The always-loaded statement gave the rule and stopped. It had been spending more words on the
  three exceptions (quoted sources, identifiers, proper nouns) than on the rule, so what arrived at
  the writing moment was the rule plus three reasons not to enforce it. The exceptions moved to the
  style file, where checking happens.
- The commit-time check was widened to cover shell files, which it had been skipping.

## Placement and enforcement

Some rules can be checked mechanically and some cannot. A rule with no judgment in it -- decisions
are immutable, corpus samples are never edited, every note has a valid `type:` -- belongs in a hook
or checker, where it is enforced rather than remembered -- the same audit's rule that hard
requirements need hard checks. That is what `hooks/policy/` is for.

A rule with legitimate exceptions cannot be fully enforced by a check without false positives, and a
check that blocks on judgment teaches you `--no-verify`. For those rules, placement is the entire
game. Before adding another paragraph of instruction, ask which sessions will actually load it, and
whether that set matches the set the rule claims to govern.

## The layers

1. **preferences/** -- loaded unconditionally at the start of every interaction. Governs
   conversation: how the assistant talks to you.
2. **AGENTS.md** -- loaded unconditionally. Governs standing behaviors: contextual retrieval,
   capture, staleness detection, the directory map, the writing procedure, immutability rules.
3. **style/** -- loaded before drafting tasks. Governs artifacts that leave the repo.
4. **.claude/skills/** -- loaded on trigger. Each skill prescribes which style files to read.
5. **Client-specific files** (CLAUDE.md, .github/copilot-instructions.md) -- loaded by one client
   only. Carry only what is specific to that client.
6. **hooks/policy/** -- never loaded by the model at all. Runs at commit and on push, so it binds
   every client, including ones that never read your instructions.

## Open questions

- **Does a banned-word list prime the words it bans?** Plausible on general grounds. In the worked
  example the evidence pointed the other way: drift happened where the list never loaded, and
  drafting, where it did load, was clean. Worth watching rather than acting on.
- **Which of your rules are filed as drafting rules but govern everything?** Path-style wikilinks
  and the `updated:` bump are the usual candidates. Run the test above against each rule in
  `style/` once in a while.
