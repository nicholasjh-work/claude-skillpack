<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/nh-logo-dark.svg" width="120">
  <source media="(prefers-color-scheme: light)" srcset="assets/nh-logo-light.svg" width="120">
  <img alt="Hidalgo Systems Labs" src="assets/nh-logo-light.svg" width="120">
</picture>

<h1 align="center">Claude Skillforge</h1>
<p align="center"><b>Production-ready Claude Skills you can install and use. Not a list. A library.</b></p>

<p align="center">
  <a href="https://github.com/nicholasjh-work/claude-skillforge/actions/workflows/ci.yml"><img src="https://github.com/nicholasjh-work/claude-skillforge/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/nicholasjh-work/claude-skillforge/actions/workflows/skill-lint.yml"><img src="https://github.com/nicholasjh-work/claude-skillforge/actions/workflows/skill-lint.yml/badge.svg" alt="Skill Lint"></a>
  <a href="https://github.com/nicholasjh-work/claude-skillforge/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License"></a>
  <a href="https://github.com/nicholasjh-work/claude-skillforge/stargazers"><img src="https://img.shields.io/github/stars/nicholasjh-work/claude-skillforge?style=for-the-badge" alt="Stars"></a>
</p>

---

### What is this?

Claude Skillforge is a multi-category library of production-ready Claude Skills. It is not a writing-skills repo. It spans foundational operating standards, data engineering, professional writing, and career tools - every skill battle-tested in real workflows, not written as a demo.

Skills are instruction files that teach Claude how to perform specific tasks in a repeatable, high-quality way. They load on demand and cost roughly 100 tokens until activated.

---

### What are Claude Skills?

Claude Skills are specialized instruction folders that Claude dynamically discovers and loads when relevant to a task. Each skill contains a `SKILL.md` file with YAML frontmatter (name and description for routing) and detailed execution instructions.

Skills use progressive disclosure: Claude scans metadata first (~100 tokens), loads full instructions only when the skill matches (~2-5K tokens), and accesses bundled resources only as needed. Multiple skills can be active simultaneously without overwhelming the context window.

---

### How to install

**Claude.ai (Web/Desktop)**
1. Go to Settings > Capabilities > Skills
2. Upload skill folders or point to this repository

**Claude Code (CLI)**
```bash
git clone https://github.com/nicholasjh-work/claude-skillforge.git
# Copy desired skill folders into your project's .claude/skills/ directory
```

**Manual**
Copy any skill folder into your Claude skills directory. Each folder is self-contained.

---

### Spotlight

<table>
<tr>
<td width="50%" align="center">

**Skill of the Week**

[![claude-token-watchdog](https://img.shields.io/badge/this%20week-claude--token--watchdog-0550ae?style=for-the-badge)](core/claude-token-watchdog/)

Watches conversation length and auto-fires a continuation handoff before you hit the token limit. Companion to `claude-session-handoff`.

</td>
<td width="50%" align="center">

**Skill of the Month**

[![scholar-editor](https://img.shields.io/badge/april%202026-scholar--editor-b35900?style=for-the-badge)](writing/ai-prose-humanizer/)

Detects and removes 38 documented AI writing patterns. Two modes: CLEAN for professional docs, VOICE for creative writing.

</td>
</tr>
</table>

> Updating the spotlight: edit this section in `README.md`. Replace the badge `label-name-color` and the description paragraph. Keep the `for-the-badge` style and category color (Core `0550ae`, Data Engineering `0d6e3f`, Writing `b35900`, Career `6f42c1`).

---

### Core

Foundational operating standards that govern how Claude behaves across all tasks.

<table>
<thead>
<tr><th>Skill</th><th>What it does</th></tr>
</thead>
<tbody>
<tr><td><a href="core/claude-operator-standard/"><img src="https://img.shields.io/badge/claude--operator--standard-0550ae?style=for-the-badge" alt="claude-operator-standard"></a></td><td>Universal operating standard for Claude sessions. Governs communication style, troubleshooting method, output format, session behavior, and handoff protocol.</td></tr>
<tr><td><a href="core/claude-code-standard/"><img src="https://img.shields.io/badge/claude--code--standard-0550ae?style=for-the-badge" alt="claude-code-standard"></a></td><td>Technical execution standard for coding, SQL, Python, dbt, and data engineering. Covers stack preferences, documentation rules, testing, and analytics engineering guidance.</td></tr>
<tr><td><a href="core/claude-session-handoff/"><img src="https://img.shields.io/badge/claude--session--handoff-0550ae?style=for-the-badge" alt="claude-session-handoff"></a></td><td>Generates a structured handoff block that captures full technical state so a conversation can continue in a new window with zero re-explanation.</td></tr>
<tr><td><a href="core/claude-token-watchdog/"><img src="https://img.shields.io/badge/claude--token--watchdog-0550ae?style=for-the-badge" alt="claude-token-watchdog"></a></td><td>Watches conversation length and fires a continuation handoff at three thresholds (15 / 20 / 25 messages). Delegates to claude-session-handoff at the forced threshold to avoid hitting Claude token or context limits. Manual command: `/watchdog-check`.</td></tr>
</tbody>
</table>

---

### Data Engineering

Tools for data quality, SQL, reporting, KPI governance, and analytics engineering.

<table>
<thead>
<tr><th>Skill</th><th>What it does</th></tr>
</thead>
<tbody>
<tr><td><a href="data-engineering/data-defect-investigator/"><img src="https://img.shields.io/badge/data--defect--investigator-0d6e3f?style=for-the-badge" alt="data-defect-investigator"></a></td><td>Investigates data defects, mismatches, duplicates, null issues, broken joins, and reconciliation failures.</td></tr>
<tr><td><a href="data-engineering/data-file-profiler/"><img src="https://img.shields.io/badge/data--file--profiler-0d6e3f?style=for-the-badge" alt="data-file-profiler"></a></td><td>Profiles CSV/Excel files: schema inspection, duplicate detection, null analysis, outliers, and data mismatches.</td></tr>
<tr><td><a href="data-engineering/dataset-reconciler/"><img src="https://img.shields.io/badge/dataset--reconciler-0d6e3f?style=for-the-badge" alt="dataset-reconciler"></a></td><td>Compares two datasets and explains count, amount, and field-level differences. Source vs target, old vs new, ERP vs DW.</td></tr>
<tr><td><a href="data-engineering/report-output-validator/"><img src="https://img.shields.io/badge/report--output--validator-0d6e3f?style=for-the-badge" alt="report-output-validator"></a></td><td>Validates report outputs, totals, grain, subtotals, and regression changes before release.</td></tr>
<tr><td><a href="data-engineering/sql-join-risk-reviewer/"><img src="https://img.shields.io/badge/sql--join--risk--reviewer-0d6e3f?style=for-the-badge" alt="sql-join-risk-reviewer"></a></td><td>Reviews schemas, joins, and SQL logic for grain violations, duplicate risk, orphan rows, and aggregation errors.</td></tr>
<tr><td><a href="data-engineering/sql-report-query-builder/"><img src="https://img.shields.io/badge/sql--report--query--builder-0d6e3f?style=for-the-badge" alt="sql-report-query-builder"></a></td><td>Builds production-grade SQL for reporting. Translates business requests into safe, auditable query logic.</td></tr>
<tr><td><a href="data-engineering/kpi-definition-standard/"><img src="https://img.shields.io/badge/kpi--definition--standard-0d6e3f?style=for-the-badge" alt="kpi-definition-standard"></a></td><td>Defines KPIs with precise formulas, grain, source logic, exclusions, and governance notes.</td></tr>
<tr><td><a href="data-engineering/report-requirements-translator/"><img src="https://img.shields.io/badge/report--requirements--translator-0d6e3f?style=for-the-badge" alt="report-requirements-translator"></a></td><td>Converts messy business requests into clean report or dashboard specifications.</td></tr>
</tbody>
</table>

---

### Writing

Professional and editorial writing tools for business communication, technical documentation, and AI prose cleanup.

<table>
<thead>
<tr><th>Skill</th><th>What it does</th></tr>
</thead>
<tbody>
<tr><td><a href="writing/business-email-drafter/"><img src="https://img.shields.io/badge/business--email--drafter-b35900?style=for-the-badge" alt="business-email-drafter"></a></td><td>Drafts natural business emails that are direct, specific, and free of canned language.</td></tr>
<tr><td><a href="writing/correction-email-drafter/"><img src="https://img.shields.io/badge/correction--email--drafter-b35900?style=for-the-badge" alt="correction-email-drafter"></a></td><td>Writes correction, clarification, and reset emails that are precise, calm, and not defensive.</td></tr>
<tr><td><a href="writing/cover-letter-drafter/"><img src="https://img.shields.io/badge/cover--letter--drafter-b35900?style=for-the-badge" alt="cover-letter-drafter"></a></td><td>Writes cover letters grounded in real experience and specific to the role.</td></tr>
<tr><td><a href="writing/linkedin-message-drafter/"><img src="https://img.shields.io/badge/linkedin--message--drafter-b35900?style=for-the-badge" alt="linkedin-message-drafter"></a></td><td>Writes concise LinkedIn messages for recruiters, hiring managers, and networking.</td></tr>
<tr><td><a href="writing/executive-brief-drafter/"><img src="https://img.shields.io/badge/executive--brief--drafter-b35900?style=for-the-badge" alt="executive-brief-drafter"></a></td><td>Writes short executive briefs: issue, impact, risk, and next step.</td></tr>
<tr><td><a href="writing/technical-to-business-summarizer/"><img src="https://img.shields.io/badge/technical--to--business--summarizer-b35900?style=for-the-badge" alt="technical-to-business-summarizer"></a></td><td>Translates technical findings into concise business-facing summaries for leadership.</td></tr>
<tr><td><a href="writing/stakeholder-status-update/"><img src="https://img.shields.io/badge/stakeholder--status--update-b35900?style=for-the-badge" alt="stakeholder-status-update"></a></td><td>Writes concise stakeholder updates on project status, issues, risks, and next steps.</td></tr>
<tr><td><a href="writing/internal-technical-doc-writer/"><img src="https://img.shields.io/badge/internal--technical--doc--writer-b35900?style=for-the-badge" alt="internal-technical-doc-writer"></a></td><td>Writes internal technical documents, SOPs, incident notes, and decision memos.</td></tr>
<tr><td><a href="writing/incident-root-cause-writer/"><img src="https://img.shields.io/badge/incident--root--cause--writer-b35900?style=for-the-badge" alt="incident-root-cause-writer"></a></td><td>Writes incident summaries separating facts, impact, root cause, and corrective action.</td></tr>
<tr><td><a href="writing/requirements-doc-drafter/"><img src="https://img.shields.io/badge/requirements--doc--drafter-b35900?style=for-the-badge" alt="requirements-doc-drafter"></a></td><td>Writes requirements documents with scope, logic, assumptions, dependencies, and acceptance criteria.</td></tr>
<tr><td><a href="writing/meeting-to-decision-memo/"><img src="https://img.shields.io/badge/meeting--to--decision--memo-b35900?style=for-the-badge" alt="meeting-to-decision-memo"></a></td><td>Converts meeting notes into decision memos with outcomes, owners, and next actions.</td></tr>
<tr><td><a href="writing/ai-writing-pattern-remover/"><img src="https://img.shields.io/badge/ai--writing--pattern--remover-b35900?style=for-the-badge" alt="ai-writing-pattern-remover"></a></td><td>Detects and removes AI writing patterns based on Wikipedia's "Signs of AI writing" guide.</td></tr>
<tr><td><a href="writing/ai-prose-humanizer/"><img src="https://img.shields.io/badge/ai--prose--humanizer-b35900?style=for-the-badge" alt="ai-prose-humanizer"></a></td><td>Removes AI patterns and adds human voice to prose. Two modes: CLEAN for professional docs, VOICE for creative writing.</td></tr>
</tbody>
</table>

---

### Career

Resume optimization, salary negotiation, and job application tools.

<table>
<thead>
<tr><th>Skill</th><th>What it does</th></tr>
</thead>
<tbody>
<tr><td><a href="career/resume-bullet-rewriter/"><img src="https://img.shields.io/badge/resume--bullet--rewriter-6f42c1?style=for-the-badge" alt="resume-bullet-rewriter"></a></td><td>Rewrites a single resume bullet to be metric-backed, action-verb-led, and free of banned phrases.</td></tr>
<tr><td><a href="career/resume-bullet-editor/"><img src="https://img.shields.io/badge/resume--bullet--editor-6f42c1?style=for-the-badge" alt="resume-bullet-editor"></a></td><td>Edits existing resume bullets to remove banned language, add metrics, and strengthen impact.</td></tr>
<tr><td><a href="career/resume-section-writer/"><img src="https://img.shields.io/badge/resume--section--writer-6f42c1?style=for-the-badge" alt="resume-section-writer"></a></td><td>Writes resume sections from raw notes, brain dumps, or bullet lists.</td></tr>
<tr><td><a href="career/resume-one-page-optimizer/"><img src="https://img.shields.io/badge/resume--one--page--optimizer-6f42c1?style=for-the-badge" alt="resume-one-page-optimizer"></a></td><td>ATS-optimized one-page resume evaluator and rewriter. Scores, gaps, and full rewrite against a job description.</td></tr>
<tr><td><a href="career/resume-two-page-optimizer/"><img src="https://img.shields.io/badge/resume--two--page--optimizer-6f42c1?style=for-the-badge" alt="resume-two-page-optimizer"></a></td><td>ATS-optimized two-page resume evaluator for senior/director/VP roles.</td></tr>
<tr><td><a href="career/salary-negotiation-framework/"><img src="https://img.shields.io/badge/salary--negotiation--framework-6f42c1?style=for-the-badge" alt="salary-negotiation-framework"></a></td><td>Data-driven salary and total compensation negotiation framework. Covers tech, finance, PE/VC, healthcare, and B2B.</td></tr>
</tbody>
</table>

---

### Design philosophy

These skills follow two layers of standards:

**Standards-backed rules** grounded in published engineering guidance (PEP 8, Twelve-Factor App, OWASP, dbt best practices, Microsoft Power BI documentation). See [docs/rationale-and-references.md](docs/rationale-and-references.md).

**House operating conventions** that are intentional working preferences for AI-assisted engineering: lead with the answer, sparse comments, no AI-style clutter, fixed output structures. These are not claimed as universal standards. See [docs/adr/0001-ai-session-operating-standard.md](docs/adr/0001-ai-session-operating-standard.md).

---

### Documentation

| Document | Purpose |
|---|---|
| [docs/rationale-and-references.md](docs/rationale-and-references.md) | Standards-backed justification for skill rules with source citations |
| [docs/adr/0001-ai-session-operating-standard.md](docs/adr/0001-ai-session-operating-standard.md) | Architecture Decision Record explaining why these standards exist |

---

### Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

### License

MIT License. See [LICENSE](LICENSE) for details.

---

<p align="center">
  <a href="https://www.linkedin.com/in/nicholashidalgo"><img src="https://img.shields.io/badge/LinkedIn-Nicholas_Hidalgo-blue?style=for-the-badge&logo=linkedin" alt="LinkedIn"></a>&nbsp;
  <a href="https://nicholashidalgo.com"><img src="https://img.shields.io/badge/Website-nicholashidalgo.com-teal?style=for-the-badge" alt="Website"></a>&nbsp;
  <a href="mailto:analytics@nicholashidalgo.com"><img src="https://img.shields.io/badge/Email-analytics@nicholashidalgo.com-red?style=for-the-badge" alt="Email"></a>
</p>
