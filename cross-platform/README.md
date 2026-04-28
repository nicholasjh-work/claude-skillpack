# Cross-Platform Watchdog Patterns

The Claude Token Watchdog skill ([core/claude-token-watchdog](../core/claude-token-watchdog/)) provides tool-enforced context-integrity discipline for Claude.ai, Claude Cowork, and Claude Code.

This folder contains the same pattern adapted to ChatGPT and Codex, where the model self-estimates from visible signals instead of using tool-level metadata.

## Files

- **[chatgpt-watchdog.md](./chatgpt-watchdog.md)**: A reusable instruction pattern that works as a one-shot conversation primer, a Custom GPT system prompt, or ChatGPT project instructions.
- **[AGENTS.md](./AGENTS.md)**: A repo-level file that gives Codex context-integrity discipline when it works in your codebase. Drop at the repository root.

## Honest caveat

The Claude version is more precise because the Skill format gives it real conversation metadata. The ChatGPT and Codex versions rely on the model self-estimating turn count and density. Reliable enough for practical use, but not measurement.
