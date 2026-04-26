---
name: token-control
description: "Proactively compacts long Claude conversations before they hit context or usage limits by generating a Chat Continuation Brief the user pastes into a new chat window. Companion to claude-session-handoff: that skill handles on-demand handoffs at any point; this skill handles automatic threshold-based handoffs when the conversation is getting too long. Triggers automatically when the conversation reaches an estimated 15 messages (soft warning), 20 messages (strong recommendation), or 25 messages (forced handoff). Triggers earlier (around 12 messages) when the conversation is technically dense: code, debugging, architecture decisions, file paths, repo work, terminal commands, or multi-step implementation plans. Manual command: /chat-continuation. Works across Claude web/app, Claude Cowork, and Claude Code. Output only, never creates files, runs commands, or modifies the repo."
version: "1.0.0"
---

<!--
SPDX-License-Identifier: MIT
Copyright (c) 2026 Nick Hidalgo
-->

# Token Control

Proactively compacts long Claude conversations before they hit context or
usage limits. Generates a Chat Continuation Brief the user pastes into a fresh
Claude chat to resume work with zero re-explanation. Prints the brief and
stops. No file writes. No commands. No repo edits.

## Relationship to claude-session-handoff

This skill is the automatic, threshold-based companion to
`claude-session-handoff`.

| When the user wants a handoff | Use |
|---|---|
| At any point in the conversation, on demand | `claude-session-handoff` |
| Because the conversation is getting too long | `token-control` |

`claude-session-handoff` answers "I want to continue this elsewhere."
`token-control` answers "this chat is about to break, compact it now."

If both could trigger, `claude-session-handoff` wins on explicit user intent.
`token-control` only auto-triggers from length heuristics.

## Purpose

1. Avoid hitting Claude usage or context limits mid-task
2. Lower token usage by ending bloated chats early
3. Preserve project state across the cutover
4. Keep the next chat focused and immediately actionable

## Trigger Rules

### Manual trigger

Generate the brief on `/chat-continuation`.

For natural-language phrases ("create handoff", "summarize for new chat",
"move to new window"), defer to `claude-session-handoff`. Token-control's
manual surface is intentionally narrow.

When manually triggered, open with:

> Here is the continuation brief for a new chat.

### Automatic triggers (best-effort heuristic)

If exact message count is unavailable, count each visible user message plus
each visible assistant response as one message. Apply these thresholds:

| Estimated messages | Action |
|---|---|
| 15 or more (soft) | Mention that a continuation brief is available, offer to generate it. |
| 20 or more (strong) | Recommend the user accept a handoff before continuing the next task. |
| 25 or more (forced) | Generate the brief automatically before continuing any new task. |

Trigger more aggressively (drop to about 12 messages) when the conversation
includes:

- Code, debugging, or stack traces
- Architecture decisions or system design
- File paths, repo work, branches, or PRs
- Terminal commands or shell sessions
- Multi-step implementation plans
- Accumulated decisions where rework cost is high

When auto-triggered at the forced threshold, open with:

> This conversation is approaching a context/usage limit. Here is the continuation brief.

### Inference fallback

If no message counter is visible, infer based on:

- Visible conversation length (scroll depth, total tokens used)
- Number of distinct user turns
- Number of decisions accumulated
- Context density (code blocks, file paths, error logs)

Err on the side of triggering earlier, not later.

## Output Template

Print the brief in clean Markdown. Use the exact section headers below.

```markdown
# Chat Continuation Brief

## Current Goal
- 2 to 5 bullets describing the main objective.

## Decisions Already Made
- Confirmed decisions only. Do not include rejected ideas or open options.

## Files / Repos / Paths Involved
- All known repos, folders, files, branches, cloud resources, URLs, local paths.

## Commands Already Run
- Commands actually run or explicitly approved. If none, write "None confirmed."

## Current State
- What is complete.
- What is partially complete.
- What is uncertain.

## Known Issues
- Open errors, risks, blockers, unresolved decisions, warnings, constraints.

## Next Best Action
- A single best next action. Not a list.

## Constraints / User Preferences
- Be concise and direct.
- Preserve project context.
- Do not run git commands unless explicitly approved.
- Do not make destructive changes.
- Ask before major architecture changes.
- Prefer Claude Code for project execution when possible.
- Use terminal commands only when Claude Code cannot perform the task.
- Keep implementation steps small and reversible.
- Maintain production-quality standards.
- Avoid unnecessary commentary.
- Avoid repeating completed work.
- Continue from the last completed step.

## Last Completed Task
- Most recent confirmed completed action.

## Next Task
- Immediate next task to perform.

## Exact Prompt to Paste Into New Chat

[Self-contained prompt, see required contents below]
```

### Required contents of the "Exact Prompt to Paste Into New Chat"

The pasted prompt must be usable on its own, with no surrounding explanation.
It must contain:

- The current goal
- The current state
- The key decisions
- The files / repos involved
- The last completed task
- The next task
- Relevant constraints
- Commands that should or should not be run
- Clear instruction to continue exactly from the prior state

## Platform-Specific Behavior

### Claude web / app

- Output is copy/paste only.
- Do not assume access to local files unless they appear in the conversation.
- Tell the user: "Paste the prompt below into a new Claude chat to continue."

### Claude Cowork

- Preserve collaboration context: ownership, reviewers, unresolved questions.
- Include any coworker comments or review decisions visible in the conversation.
- Keep the handoff structured so another AI coworker can resume cleanly.
- Tell the user: "Paste the prompt below into a new Cowork session."

### Claude Code

- Preserve: repo path, files changed, commands run, tests run, errors seen,
  next command or edit.
- Include these lines in Constraints:
  - "Do not run git commands unless I explicitly ask."
  - "Inspect the repo before editing if current file state is uncertain."
  - "Do not repeat work already completed."
  - "Use small, reviewable edits."
- If the repo has any of `PROJECT_STATUS.md`, `DECISIONS.md`, `AGENTS.md`,
  `README.md`, or `TODO.md`, instruct Claude Code to read them first if relevant.
- Tell the user: "Paste the prompt below into a new Claude Code session in the
  same repo."

## Quality Rules

- Do not over-compress technical details needed for continuity.
- Do not include casual conversation.
- Do not invent files, commands, decisions, or completed work.
- Label assumptions explicitly.
- If information is missing, write `Unknown` instead of guessing.
- Keep the brief compact but complete.
- The "Exact Prompt to Paste Into New Chat" must be self-contained.

## Failure Modes

| Failure | What to do |
|---|---|
| User asks to continue past 25 messages without a handoff | Generate the brief first, then ask if they want to keep going in the current chat. |
| Conversation contains no project work, just casual chat | Skip the skill. Do not generate a brief. |
| Critical info (paths, decisions) is ambiguous | Mark as `Unknown` rather than fabricating. |
| User invokes both this skill and claude-session-handoff | Defer to claude-session-handoff. Manual intent wins. |
| Multi-platform handoff requested (web to Code) | Use the destination platform's section. If unspecified, default to Claude web. |

## Final Operational Instruction

Print the brief and stop. Do not create files. Do not run commands. Do not
modify the repo. The user copies the brief into a new chat. That is the entire
deliverable.
