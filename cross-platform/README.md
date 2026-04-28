<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/nh-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/nh-logo-light.svg">
    <img alt="NH" src="../assets/nh-logo-dark.svg" width="80">
  </picture>
</p>

<h1 align="center">Cross-Platform Watchdog Patterns</h1>
<p align="center"><b>Context-integrity discipline for ChatGPT and Codex, adapted from the Claude Token Watchdog skill.</b></p>

<p align="center">
  <a href="./chatgpt-watchdog.md"><img src="https://img.shields.io/badge/ChatGPT_Watchdog-10A37F?style=for-the-badge&logo=openai&logoColor=white" alt="ChatGPT Watchdog"></a>&nbsp;
  <a href="./AGENTS.md"><img src="https://img.shields.io/badge/Codex_AGENTS.md-000000?style=for-the-badge&logo=openai&logoColor=white" alt="Codex AGENTS.md"></a>&nbsp;
  <a href="../core/claude-token-watchdog/"><img src="https://img.shields.io/badge/Claude_Skill-D97706?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude Skill"></a>
</p>

---

### What is this?

The [Claude Token Watchdog skill](../core/claude-token-watchdog/) provides tool-enforced context-integrity discipline for Claude.ai, Claude Cowork, and Claude Code. It monitors conversation length, applies thresholds, and triggers a continuation handoff before you hit a usage limit.

This folder contains the same pattern adapted to ChatGPT and Codex, where the model self-estimates from visible signals instead of using tool-level metadata.

Same principle. Different surfaces.

---

### Files

<table>
<tbody>
<tr>
<td><a href="./chatgpt-watchdog.md"><img src="https://img.shields.io/badge/chatgpt--watchdog-10A37F?style=for-the-badge" alt="chatgpt-watchdog"></a></td>
<td>A reusable instruction pattern that works as a one-shot conversation primer, a Custom GPT system prompt, or ChatGPT project instructions.</td>
</tr>
<tr>
<td><a href="./AGENTS.md"><img src="https://img.shields.io/badge/AGENTS.md-000000?style=for-the-badge" alt="AGENTS.md"></a></td>
<td>A repo-level file that gives Codex context-integrity discipline when it works in your codebase. Drop at the repository root.</td>
</tr>
</tbody>
</table>

---

### How they compare

<table>
<thead>
<tr><th>Surface</th><th>Format</th><th>Threshold mechanism</th></tr>
</thead>
<tbody>
<tr><td><img src="https://img.shields.io/badge/Claude-D97706?style=flat-square&logo=anthropic&logoColor=white" alt="Claude"></td><td>Skill (SKILL.md)</td><td>Tool-enforced</td></tr>
<tr><td><img src="https://img.shields.io/badge/ChatGPT-10A37F?style=flat-square&logo=openai&logoColor=white" alt="ChatGPT"></td><td>Prompt / Custom GPT / Project</td><td>Self-estimated</td></tr>
<tr><td><img src="https://img.shields.io/badge/Codex-000000?style=flat-square&logo=openai&logoColor=white" alt="Codex"></td><td>AGENTS.md</td><td>Self-estimated</td></tr>
</tbody>
</table>

---

### Honest caveat

The Claude version is more precise because the Skill format gives it real conversation metadata. The ChatGPT and Codex versions rely on the model self-estimating turn count and density. Reliable enough for practical use, but not measurement.

---

<p align="center">
  <a href="https://www.linkedin.com/in/nicholashidalgo"><img src="https://img.shields.io/badge/LinkedIn-Nicholas_Hidalgo-blue?style=for-the-badge&logo=linkedin" alt="LinkedIn"></a>&nbsp;
  <a href="https://nicholashidalgo.com"><img src="https://img.shields.io/badge/Website-nicholashidalgo.com-teal?style=for-the-badge" alt="Website"></a>&nbsp;
  <a href="mailto:analytics@nicholashidalgo.com"><img src="https://img.shields.io/badge/Email-analytics@nicholashidalgo.com-red?style=for-the-badge" alt="Email"></a>
</p>
