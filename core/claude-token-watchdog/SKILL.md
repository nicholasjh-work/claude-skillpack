---
name: claude-token-watchdog
description: "Monitors conversation length to prevent context loss and token-limit exhaustion. Counts visible messages and fires at three thresholds: 15+ messages (soft, mention a handoff is available), 20+ messages (strong, recommend handoff before next task), 25+ messages (forced, automatically delegate to claude-session-handoff to generate the continuation brief). Triggers earlier (around 12 messages) when the conversation is technically dense: code, debugging, architecture decisions, file paths, repo work, terminal commands, or multi-step implementation plans. Manual command: /watchdog-check. Companion to claude-session-handoff: this skill watches and decides when, claude-session-handoff produces the actual brief. Output only at soft/strong tiers (notification text). At the forced tier, delegates to claude-session-handoff. Never creates files, runs commands, or modifies the repo."
version: "1.0.0"
---

<!--
SPDX-License-Identifier: MIT
Copyright (c) 2026 Nick Hidalgo
-->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/nh-logo-dark.svg" width="80">
  <source media="(prefers-color-scheme: light)" srcset="../../assets/nh-logo-light.svg" width="80">
  <img alt="Hidalgo Systems Labs" src="../../assets/nh-logo-light.svg" width="80">
</picture>

<h1 align="center">Claude Token Watchdog</h1>
<p align="center"><b>Watches conversation length and fires a handoff before you hit the token limit.</b></p>

<p align="center">
  <a href="../../README.md"><img src="https://img.shields.io/badge/category-core-0550ae?style=for-the-badge" alt="Core"></a>
  <img src="https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge" alt="Version 1.0.0">
  <a href="../../LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/role-monitor%20%2B%20delegate-lightgrey?style=for-the-badge" alt="Role: monitor and delegate">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/thresholds-15%20%2F%2020%20%2F%2025-blue?style=flat-square" alt="Thresholds: 15 / 20 / 25">
  <img src="https://img.shields.io/badge/dense--mode-12%2B-orange?style=flat-square" alt="Dense mode: 12+ messages">
  <img src="https://img.shields.io/badge/platforms-web%20%7C%20cowork%20%7C%20code-purple?style=flat-square" alt="Platforms: web, cowork, code">
  <a href="../claude-session-handoff/"><img src="https://img.shields.io/badge/delegates%20to-claude--session--handoff-0550ae?style=flat-square" alt="Delegates to claude-session-handoff"></a>
</p>

---

### Compatibility

This skill is built on the Claude SKILL.md format and works on the three Anthropic surfaces that support it.

| Platform | Supported |
|---|---|
| Claude.ai (web and desktop apps) | Yes |
| Claude Cowork | Yes |
| Claude Code (CLI) | Yes |
| ChatGPT, Gemini, Copilot, or any non-Anthropic LLM | No - SKILL.md is Anthropic-specific |
| LangChain, LiteLLM, or other orchestration frameworks | Not directly - the watchdog logic could be ported as a Python module, but that is a separate implementation |

The skill activates the same way on all three Anthropic surfaces: Claude reads the frontmatter, decides whether to load the full instructions based on the trigger phrases, and applies the threshold logic to the visible conversation. Output is identical across surfaces. Platform-specific behavior (described below) covers minor differences in how the continuation brief is consumed (paste into a new chat for web/Cowork, paste into a new Claude Code session for CLI).

---

### What this does

A token-usage watchdog. Counts visible messages, applies threshold logic, and at the forced tier delegates to `claude-session-handoff` to produce a continuation brief. Prevents token burn and avoids hitting Claude's usage or context limits mid-task.

<table>
<tr><td>

**Role**
Monitor token-usage risk. Decide when to hand off. Delegate the actual handoff to `claude-session-handoff`.

**Trigger**
Automatic at message thresholds 15 / 20 / 25 (dropped to ~12 in dense conversations). Manual via `/watchdog-check`.

**Output**
Notification text at soft and strong tiers. Forced tier invokes `claude-session-handoff` and prints the brief that skill generates.

**Side effects**
None. Print-only contract. No file writes, no commands, no repo edits.

</td></tr>
</table>

---

### Architecture

```
[User chats with Claude]
          |
          v
+---------------------------------+
|  claude-token-watchdog        |  <- this skill
|  counts messages, applies       |
|  threshold logic                |
+---------------------------------+
          |
   forced (25+) only
          |
          v
+---------------------------------+
|  claude-session-handoff         |  <- existing companion skill
|  generates the continuation     |
|  brief                          |
+---------------------------------+
          |
          v
[User pastes brief into new chat]
```

This skill **does not produce briefs**. At the forced threshold, it invokes [`claude-session-handoff`](../claude-session-handoff/) and prints whatever that skill returns.

---

### Companion to claude-session-handoff

| Concern | Skill |
|---|---|
| Decide *when* to hand off | `claude-token-watchdog` (this) |
| Produce the actual handoff brief | [`claude-session-handoff`](../claude-session-handoff/) |
| User explicitly requests a handoff | [`claude-session-handoff`](../claude-session-handoff/) directly |

If the user invokes `claude-session-handoff` directly, this skill stays silent. Manual user intent always wins over automatic monitoring.

---

### Purpose

1. Avoid hitting Claude usage or context limits mid-task
2. Lower token usage by ending bloated chats early
3. Preserve project state across the cutover
4. Keep the next chat focused and immediately actionable

---

### Threshold Logic

If exact message count is unavailable, count each visible user message plus each visible assistant response as one message.

| Estimated messages | Tier | Action |
|---|---|---|
| 15 or more | Soft | Mention a continuation brief is available. Offer to generate it. Do not invoke `claude-session-handoff` yet. |
| 20 or more | Strong | Recommend the user accept a handoff before continuing the next task. Still wait for user confirmation. |
| 25 or more | Forced | Invoke `claude-session-handoff` automatically before continuing any new task. Print the brief. |

#### Dense-mode adjustment

Drop the soft threshold to about 12 messages when the conversation includes any of:

- Code, debugging, or stack traces
- Architecture decisions or system design
- File paths, repo work, branches, or PRs
- Terminal commands or shell sessions
- Multi-step implementation plans
- Accumulated decisions where rework cost is high

Strong and forced thresholds also shift earlier (around 17 and 22 respectively) in dense mode.

#### Inference fallback

If no message counter is visible, infer based on:

- Visible conversation length (scroll depth, total tokens used)
- Number of distinct user turns
- Number of decisions accumulated
- Context density (code blocks, file paths, error logs)

Err on the side of triggering earlier, not later.

---

### Output by Tier

#### Soft tier (15+ messages)

Print a brief notification, then continue the user's current task normally:

> Heads up: this conversation is getting long. If you want to continue this work in a fresh chat with full context, just say `/handoff` and I'll generate a continuation brief.

Do not invoke `claude-session-handoff`. Do not block the current task.

#### Strong tier (20+ messages)

Before responding to the user's next request, print:

> This conversation is getting long enough that token limits are a real risk. I recommend we generate a continuation brief before starting the next task. Want me to do that now? (Or say `continue` to keep going.)

Wait for user response. If they say `continue` or anything ignoring the offer, proceed with their request but stay alert. If they accept, invoke `claude-session-handoff`.

#### Forced tier (25+ messages)

Open with:

> This conversation is approaching a context/usage limit. Generating the continuation brief now before we continue.

Then invoke `claude-session-handoff` and print the brief that skill returns. After printing, ask the user to paste the brief into a new chat before continuing.

---

### Manual trigger

The user can invoke this skill at any time with `/watchdog-check`. Response format:

> Current estimated message count: [N].
> Tier: [soft / strong / forced / below threshold].
> [Tier-specific notification text from above.]

For natural-language handoff requests ("create handoff", "summarize for new chat", "move to new window"), defer to `claude-session-handoff` directly. This skill only owns `/watchdog-check`.

---

### Platform-Specific Behavior

#### Claude web / app

- Output is copy/paste only.
- At forced tier, claude-session-handoff produces a self-contained brief the user pastes into a new Claude chat.

#### Claude Cowork

- Preserve collaboration context: ownership, reviewers, unresolved questions.
- claude-session-handoff includes coworker comments visible in the conversation.

#### Claude Code

- claude-session-handoff includes repo path, files changed, commands run, tests run, errors seen, and next command or edit.
- Watchdog adds: "Inspect the repo before editing if current file state is uncertain."

---

### Quality Rules

- Do not over-trigger. Below threshold and not in dense mode means stay silent.
- Do not invoke `claude-session-handoff` at soft or strong tiers. Only at forced.
- Do not invent message counts. If unsure, use inference fallback.
- Do not block user requests at soft tier. Notify and continue.
- At strong tier, ask once. If the user says continue, do not ask again until forced tier.
- At forced tier, generate the brief before doing any new work. No exceptions.

---

### Failure Modes

| Failure | What to do |
|---|---|
| User refuses handoff at forced tier | Generate the brief anyway. Print it. Tell the user it's available if they change their mind. Then proceed with their request. |
| Conversation contains no project work, just casual chat | Stay silent at all tiers. Watchdog only fires when there's state worth preserving. |
| User invokes claude-session-handoff directly | Stay silent. Manual intent wins. |
| Exact message count is ambiguous | Use inference fallback. Err earlier. |
| claude-session-handoff is unavailable | Print a basic continuation message with goal, last action, and next task. Tell the user to install claude-session-handoff for full briefs. |

---

### Final Operational Instruction

Watch. Notify at soft. Recommend at strong. Delegate at forced. Never produce a brief yourself - that is `claude-session-handoff`'s job. Never write files. Never run commands. Never modify the repo.

---

<p align="center">
  <a href="../../README.md"><img src="https://img.shields.io/badge/%E2%86%A9-back%20to%20skillforge-0550ae?style=for-the-badge" alt="Back to Skillforge"></a>
  <a href="../claude-session-handoff/"><img src="https://img.shields.io/badge/%E2%86%92-claude--session--handoff-0550ae?style=for-the-badge" alt="See claude-session-handoff"></a>
</p>
