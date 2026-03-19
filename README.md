# writing-skills

A mono-repository of Claude writing skills, shared detectors, and supporting
tooling. Every skill transforms AI-drafted or human prose into clean,
credible writing by detecting and removing the patterns that make text sound
machine-generated.

**Scholar Editor** is the flagship skill: a research-grounded editorial
pipeline covering 38 documented AI writing patterns, grounded in peer-reviewed
detection research from Princeton, Stanford, MIT, Maryland, and Cell Press.

---

## How Skills Work

Each skill is a `SKILL.md` file that Claude reads before responding to your
request. Claude loads the skill automatically when your message matches the
skill's trigger phrases -- no slash commands or manual activation required.

Skills in this repo come in two surfaces:

| Surface | How to install | How it triggers |
|---|---|---|
| Claude.ai / Claude app | Upload `.skill` file via Settings > Customize > Skills | Automatic, based on what you say |
| Claude Code | Place skill folder in `.claude/skills/` | Automatic, or via `/skill-name` |

---

## Quick Start

### Claude.ai

1. Go to **Settings > Customize > Skills > Upload**
2. Upload any `.skill` file from the `dist/` directory
3. Say something that matches the skill's trigger phrases (see table below)

### Claude Code

```bash
git clone https://github.com/nicholasjh-work/claude-writing-skillpack.git
cp -r claude-writing-skillpack/skills/email-writer ~/.claude/skills/
```

Or install all skills at once:

```bash
cp -r claude-writing-skillpack/skills/* ~/.claude/skills/
```

---

## Skill Inventory and Trigger Map

Say any of these phrases and the matching skill activates automatically.

### Editorial

| Skill | Version | Say something like... |
|---|---|---|
| `scholar-editor` | 2.0.0 | "humanize this", "remove AI patterns", "this sounds like AI", "final pass", "clean up this text", "add personality to this", "editorial review" |

### Resume and Career

| Skill | Version | Say something like... |
|---|---|---|
| `resume-one-page` | 1.0.0 | "rewrite my resume for this job", "one page resume", "ATS score", "optimize my resume" + paste JD |
| `resume-two-page` | 1.0.0 | "two page resume", "director resume", "VP resume", "senior manager resume" + paste JD |
| `resume-writer` | 1.1.0 | "write my resume bullets", "turn these notes into resume bullets", "draft a resume section" -- no JD |
| `resume-editor` | 1.1.0 | "fix my resume bullets", "clean up this bullet", "remove weak language" -- no JD |
| `resume-bullet-rewriter` | 1.1.0 | "rewrite this bullet", "fix this one line", "this bullet is weak" |
| `cover-letter-writer` | 1.0.0 | "write a cover letter", "cover letter for this role" |

### Professional Writing

| Skill | Version | Say something like... |
|---|---|---|
| `email-writer` | 1.0.0 | "write this email", "draft a professional email", "clean up this email" |
| `correction-email-writer` | 1.0.0 | "write a correction email", "I need to apologize for", "I made a mistake in my last email" |
| `linkedin-message-writer` | 1.0.0 | "write a LinkedIn message", "outreach to a recruiter", "follow up on LinkedIn" |
| `stakeholder-update-writer` | 1.0.0 | "write a stakeholder update", "project status update", "executive status" |
| `meeting-notes-to-decision-memo` | 1.0.0 | "turn these meeting notes into a memo", "decision memo from my notes" |

### Leadership and Executive

| Skill | Version | Say something like... |
|---|---|---|
| `executive-brief-writer` | 1.0.0 | "write an executive brief", "one-page brief", "exec brief from this content" |
| `executive-summary-writer` | 1.0.0 | "write an executive summary", "summarize this for leadership", "distill this report" |
| `incident-summary-writer` | 1.0.0 | "write an incident summary", "post-mortem from my notes", "summarize this outage" |

### Technical Documentation

| Skill | Version | Say something like... |
|---|---|---|
| `technical-writer` | 1.0.0 | "write a README", "write a runbook", "document this API", "ADR for this decision" |
| `requirements-doc-writer` | 1.0.0 | "write a requirements doc", "turn this brief into requirements", "PRD from these notes" |
| `requirements-to-report-spec` | 1.0.0 | "turn this request into a report spec", "build a report spec from these requirements" |

### Data and SQL

| Skill | Version | Say something like... |
|---|---|---|
| `sql-report-builder` | 1.0.0 | "write this SQL report", "build a query for", "report-safe SQL for" |
| `schema-join-risk-reviewer` | 1.0.0 | "review this SQL for join risks", "check this query for double counting" |
| `data-integrity-investigator` | 1.0.0 | "investigate this data issue", "find missing records", "why don't these numbers match" |
| `python-data-investigator` | 1.0.0 | "profile this data file", "find quality issues in this CSV", "inspect this extract" |
| `python-report-validation` | 1.0.0 | "validate this report output", "check subtotals", "verify these numbers before release" |
| `python-reconciliation-engine` | 1.0.0 | "reconcile these two datasets", "compare source vs target", "find the differences" |
| `kpi-definition-governance` | 1.0.0 | "define this KPI", "write a metric definition", "KPI governance doc" |

---

## Scholar Editor -- Flagship Skill

Scholar Editor detects and removes 38 documented AI writing patterns across
two modes. It is the most research-grounded skill in this repo.

### Two Modes

**CLEAN mode** -- for professional writing where facts must not change.
- Hard fact-lock: any token in `preserve_facts[]` that is altered blocks output
- Severity gating: HIGH severity issues require human review before Pass 3 runs
- Structured JSON output: audit report, applied rules, changelog
- Best for: emails, technical docs, reports, anything with named metrics or dates

**VOICE mode** -- for writing that needs a human pulse.
- No fact-lock: rewrites freely for rhythm and personality
- Soul audit in Pass 2: asks "what still makes this obviously AI-generated?"
- Injects personality: opinions, varied rhythm, first-person where appropriate
- Best for: blog posts, essays, creative writing, LinkedIn posts

**Auto-detection:** Claude infers the mode from context. If you provide
`preserve_facts` and a technical domain, it runs CLEAN. Creative or casual
domains without `preserve_facts` get VOICE. You can override: "run this in
CLEAN mode" or "run this in VOICE mode."

### Pattern Coverage

38 patterns across three source layers:

| Layer | Patterns | Source |
|---|---|---|
| Wikipedia (P1-P24) | Significance inflation, AI vocabulary, em dash overuse, sycophancy, filler, generic conclusions, and 18 more | Wikipedia:Signs_of_AI_writing (WikiProject AI Cleanup) |
| Research-grounded (P25-P38) | Burstiness, transition imbalance, impersonal hedging, register uniformity, syntactic templates, positivity bias, nominalization, experiential specificity absence, and 6 more | Desaire et al. 2023, GPTZero/Princeton 2023, Hans et al. 2024, Georgiou et al. 2024, Kendro et al. 2025, Shaib et al. 2024, VERMILLION framework 2025, and others |

---

## Shared Libraries

These are NOT standalone skills. They are reference libraries loaded by skills
that need them. They live in `shared/` and are embedded into dependent skill
packages at build time.

| Library | What it provides | Used by |
|---|---|---|
| `nick-mode-writing-standard` | Voice rules, banned pattern list, 12 canonical rewrites, Python validator API | All writing skills (Pass 3) |
| `resume-banned-language-pack` | 20 forbidden resume phrases with metric-backed replacements, Python flag API | All resume skills |
| `ai-pattern-scrubber` | Fast 10-pattern pre-flight scan | Embedded in scholar-editor |
| `humanizer-flow` | Original two-pass humanizer pipeline | Superseded by scholar-editor v2 |

---

## Repository Structure

```
claude-writing-skillpack/
+-- skills/                      <- 26 Claude skills, one folder each
|   +-- scholar-editor/
|   |   +-- SKILL.md
|   |   +-- references/
|   |       +-- patterns-24.md
|   |       +-- patterns-research.md
|   |       +-- soul-injection.md
|   |       +-- nick-mode-voice.md
|   +-- email-writer/
|   |   +-- SKILL.md
|   +-- ...
+-- shared/                      <- Shared detectors and rule libraries
|   +-- nick-mode-writing-standard/
|   +-- resume-banned-language-pack/
|   +-- ai-pattern-scrubber/
|   +-- scholar-editor/          <- Python package for CI and testing
+-- tests/                       <- Unit tests and fixtures
|   +-- shared/
|   +-- test_email_writer.py
|   +-- test_scholar_editor.py
+-- tools/                       <- Linting and validation tools
|   +-- skill_linter.py
|   +-- check_pattern_coverage.py
+-- evaluation/                  <- Human evaluation plan and rubrics
|   +-- EVAL_PLAN.md
+-- .github/
|   +-- workflows/
|       +-- ci.yml
|       +-- skill-lint.yml
+-- README.md
+-- CONTRIBUTING.md
+-- CHANGELOG.md
```

---

## Testing

Run the full test suite:

```bash
pytest -v tests/
```

Run pattern coverage check:

```bash
python tools/check_pattern_coverage.py
```

Lint all SKILL.md files:

```bash
python tools/skill_linter.py skills/
```

The linter checks every SKILL.md for:
- Single-line quoted description (not multi-line YAML block)
- ASCII-only content (no em dashes, curly quotes, Unicode arrows)
- Allowed frontmatter keys only
- Body under 500 lines
- No dangling file references

---

## Research Sources

Scholar Editor and the shared detectors are grounded in the following research.
Full citations are in `skills/scholar-editor/references/patterns-research.md`.

**Statistical detection**
- Gehrmann, Strobelt, Rush (2019). GLTR. ACL. arXiv:1906.04043
- Mitchell et al. (2023). DetectGPT. Stanford. ICML 2023
- Hans et al. (2024). Binoculars. University of Maryland. ICML 2024
- Bao et al. (2024). Fast-DetectGPT. ICLR 2024

**Linguistic and stylometric analysis**
- Desaire et al. (2023). >99% accuracy classifier. Cell Reports Physical Science
- Georgiou et al. (2024). LASSO linguistic analysis. MDPI
- Kendro, Maloney & Jarvis (2025). Lexical diversity. eScholarship/UC
- Shaib et al. (2024). Syntactic template repetition. CR-POS metric
- Tercon (2025). Linguistic survey. arXiv:2510.05136
- Munoz-Ortiz et al. (2024). Positivity bias. PLOS ONE

**Bias and detection limits**
- Liang et al. (2023). GPT detector bias against non-native writers. Stanford. Patterns
- Sadasivan et al. (2023). Detection impossibility result. University of Maryland

**Industry methodology**
- GPTZero / Tian (2023). Perplexity and burstiness. Princeton
- Turnitin (2023/2024). AI Writing Detection Model Architecture whitepaper
- Dathathri et al. (2024). SynthID. Google DeepMind. Nature
- VERMILLION framework (ResearchLeap, 2025)
- Originality.ai LinkedIn study (2025)

**Practitioner sources**
- Wikipedia:Signs_of_AI_writing (WikiProject AI Cleanup)
- Willo (2025). Resume AI detection study

---

## Human Evaluation

See `evaluation/EVAL_PLAN.md` for the full methodology:

- 3 raters x 50 examples per skill
- 4-point rubric: accuracy, edit effort, rhetorical fit, naturalness
- Acceptance thresholds: 100% fact preservation, avg edit effort <= 2,
  avg naturalness >= 2.0

---

## CI/CD

Every push and pull request runs:

- `skill-lint.yml` -- validates all 26 SKILL.md files (frontmatter, ASCII,
  line count, description format, broken references)
- `ci.yml` -- runs pytest, pattern coverage check, and schema validation

A PR cannot merge if any SKILL.md fails lint or any test fails.

---

## Contributing

See **CONTRIBUTING.md** for the full guide. Short version:

1. Fork the repo and create a feature branch
2. Add your skill to `skills/your-skill-name/SKILL.md`
3. Run `python tools/skill_linter.py skills/your-skill-name/SKILL.md`
4. Add at least 3 test cases to `tests/`
5. Open a PR -- CI must pass before review

New skills must include:
- Single-line quoted description with trigger phrases
- `version: "1.0.0"` in the Runtime Configuration block
- Hallucination controls (no fabricated metrics, dates, or employers)
- At least one before/after example

---

## License

MIT License. Copyright (c) 2026 Nick Hidalgo.

Each skill's `SKILL.md` carries an MIT license header. Shared libraries
carry the same license. See `LICENSE` for full terms.

---

**Version:** 1.0.0
**Last updated:** March 2026
**Maintainer:** Nick Hidalgo
