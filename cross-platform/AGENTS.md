# AGENTS.md

This file provides agent operating instructions for repositories that want context-integrity discipline during long Codex sessions.

Drop this file at the root of any repo. Codex reads it automatically when starting a session in that repo.

---

## How to use this

Place this file at the repository root as `AGENTS.md`. No further configuration required.

If you want only some sessions to follow these rules, prefix the file with a short scope statement (for example: "These rules apply only to sessions touching the `src/etl/` directory") and Codex will respect the scope.

---

## Codex Watchdog: instructions for the agent

You are operating with context-integrity discipline. Long Codex sessions accumulate decisions, file edits, command output, errors, and partial fixes. When that context becomes too large or too noisy, the work degrades: you forget earlier constraints, repeat fixes that already failed, or miss decisions the user already made.

Your job is to monitor the health of this session and produce a Continuation Brief before the session breaks down or the user hits a usage limit.

### Tracking

Track these signals continuously throughout the session:

1. Approximate number of user turns (estimate from visible exchanges)
2. Files inspected, files changed, commands run
3. Errors encountered and whether they were resolved
4. Decisions made by the user and constraints accepted
5. Implementation density: large code edits, multi-file refactors, debugging cycles, repeated corrections

Density matters more than raw turn count. A 25-turn discussion of architecture is different from a 25-turn debugging marathon. Use the density signals to adjust your trigger thresholds.

### Trigger levels

15+ messages, or several repo decisions:
Mention once that the session is getting long. Offer to produce a Continuation Brief. Do not nag.

20+ messages, multiple files inspected or edited, or unresolved errors:
Recommend handoff before starting the next major repo task. State that the brief should be created now.

25+ messages, major implementation work, repeated debugging, or signs of context drift:
Generate the Continuation Brief at the end of your next response, before continuing other work.

### Manual trigger

If the user types `/watchdog-check` or `/handoff`, immediately produce a Continuation Brief regardless of estimated session state. Do not warn or ask first.

### The continuation brief must include

1. Current goal
2. Repo and branch
3. Files inspected
4. Files changed
5. Commands run
6. Current implementation state
7. Known errors or blockers
8. Decisions already made
9. Constraints and style rules
10. Open questions
11. Next best action
12. Exact prompt to paste into a new Codex session

Output the brief as a fenced markdown code block so the user can copy it cleanly into a fresh Codex session.

### Behavior rules

- Produce the brief once when triggered. Do not offer it again on every subsequent turn.
- Strip noise. Failed paths the user explicitly abandoned, debugging cycles that ended in revert, exploratory commands that produced nothing useful: these belong in the discarded pile, not the brief.
- Preserve constraints. Anything the user said about style, architecture, or "we are not doing X": carry it forward verbatim.
- The user controls the session. Your job is to surface the option and produce the brief on demand. Do not enforce.

The goal is to preserve context integrity before the session becomes noisy or usage limits interrupt the work.

---

## Why this exists

Codex sessions on real repo work accumulate context fast. Without active hygiene, the session degrades silently: the model starts forgetting earlier decisions, repeats fixes that already failed, or runs over the user's usage limit at the worst moment.

This file applies the same context-integrity discipline used in the Claude Token Watchdog skill, adapted to the AGENTS.md convention Codex uses for repo-level instructions.

For the Claude Skill version (which has tool-enforced thresholds rather than self-estimated ones), see https://github.com/nicholasjh-work/claude-skillforge

---

## Limitations to be aware of

Codex does not currently expose precise conversation metadata (token count, exact message count) to the agent. This pattern relies on the agent self-estimating from visible signals: turn count, files touched, commands run, error frequency. The estimation is reliable enough for practical use but is not measurement.
