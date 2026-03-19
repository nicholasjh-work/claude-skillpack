# GitHub Issues — Prioritized TODO List

Copy and paste these issue templates into GitHub to create the work items. Assign to team and add to milestone "Pre-Release Cleanup" or "v1.0.0".

---

## PRIORITY 1 — UNBLOCK RELEASE (Target: Today)

### Issue 1: Add version field to 12 skills

**Title:** `chore: add missing version fields to 12 SKILL.md files`

**Body:**
```markdown
## Description
12 SKILL.md files are missing the required `version` field in frontmatter. This blocks release versioning and package management in CI/CD.

## Affected skills
- ai-pattern-scrubber
- data-integrity-investigator
- kpi-definition-governance
- nick-mode-writing-standard
- python-data-investigator
- python-reconciliation-engine
- python-report-validation
- requirements-to-report-spec
- resume-banned-language-pack
- schema-join-risk-reviewer
- sql-report-builder

(See PRODUCTION_AUDIT.md section 1 for full list)

## Required action
Add `version: "1.0.0"` to the YAML frontmatter of each skill's SKILL.md file.

**Template:**
\`\`\`yaml
---
name: "skill-name"
version: "1.0.0"
description: "..."
...
---
\`\`\`

## Success criteria
- All 26 SKILL.md files have a `version` field
- Versions follow semantic versioning (e.g., 1.0.0)
- CI validates version presence (see issue #2)

## Effort estimate
15 minutes
```

---

### Issue 2: Remove dangling examples/long.json references from 6 skills

**Title:** `fix: remove hallucinated examples/long.json references`

**Body:**
```markdown
## Description
6 skills contain documentation that references `examples/long.json` files that do not exist. This creates broken links and poor user experience.

## Affected skills
1. cover-letter-writer (line 62)
2. executive-brief-writer (line 58)
3. executive-summary-writer (line 68)
4. incident-summary-writer (line 71)
5. linkedin-message-writer (line 67)
6. meeting-notes-to-decision-memo (line 71)

## Required action
Remove the lines referencing `examples/long.json` from each skill's SKILL.md. The inline Short/Medium/Long examples in the SKILL.md documentation are sufficient.

**Search string:** `See examples/long.json`

**Replace with:** (delete the line)

## Alternative (not recommended)
If you prefer to keep the reference, create `examples/long.json` files with JSON input/output for each skill. This is higher effort with lower value.

## Success criteria
- Zero matches for "examples/" in any SKILL.md prose
- No broken documentation links
- skill-lint CI passes (see issue #2)

## Effort estimate
10 minutes
```

---

### Issue 3: Consolidate shared/scholar_editor directory naming

**Title:** `chore: consolidate scholar-editor and scholar_editor directories`

**Body:**
```markdown
## Description
Both `shared/scholar-editor/` (kebab-case) and `shared/scholar_editor/` (snake_case) directories exist. Python imports use snake_case, so imports like \`from shared.scholar_editor import ...\` may fail if both names are present and cause confusion.

## Current state
- \`shared/scholar-editor/\` contains: SPEC.md, mock_detector.py, rubric.json
- \`shared/scholar_editor/\` exists (possibly empty or with \`__pycache__\`)

## Required action
1. Consolidate all content to \`shared/scholar_editor/\` (snake_case, Python standard)
2. Delete or rename \`shared/scholar-editor/\`
3. Update any documentation or import statements that reference \`scholar-editor\`

## Success criteria
- Only \`shared/scholar_editor/\` directory exists
- All Python imports work: \`from shared.scholar_editor import ...\`
- All tests pass
- scholar-editor SKILL.md imports still work

## Effort estimate
5 minutes
```

---

## PRIORITY 2 — QUALITY CLEANUP (Target: Before public release)

### Issue 4: Replace em dashes with hyphens in 18 skills

**Title:** `chore: replace em dashes with hyphens to comply with nick-mode-writing-standard`

**Body:**
```markdown
## Description
18 SKILL.md files contain em dashes (—) in prose sections. The \`nick-mode-writing-standard\` skill explicitly forbids em dashes. Skills should model compliance with their own standards.

## Affected skills (18 total)
correction-email-writer, cover-letter-writer, email-writer, executive-brief-writer, executive-summary-writer, incident-summary-writer, linkedin-message-writer, meeting-notes-to-decision-memo, requirements-doc-writer, resume-bullet-rewriter, resume-editor, resume-writer, scholar-editor, stakeholder-update-writer, technical-writer, and 3 others.

## Scope
- **REPLACE:** Em dashes (—) in prose sections only
- **PRESERVE:** Em dashes in code blocks, JSON examples, or comments (acceptable for readability)

## Replacement rules
- **Time ranges:** Use hyphen: \`9:41-11:23 PM PT\` (not 9:41—11:23 PM PT)
- **Apposition:** Use comma: \`deprecation, a crucial event,\` (not deprecation—a crucial event)
- **List items:** Use parentheses or comma as needed

## Example
**Before:** "The v1 API deprecation — a crucial milestone — showcases evolution."
**After:** "The v1 API deprecation (a crucial milestone) showcases evolution."
OR: "The v1 API deprecation, a crucial milestone, showcases evolution."

## Success criteria
- Zero em dashes in prose sections of SKILL.md files
- Code blocks and JSON examples may retain em dashes
- skill-lint CI passes with strict non-ASCII checking

## Effort estimate
30 minutes

## Note
This is a compliance check, not a refactoring. We want the skill documentation to model the standards it teaches.
```

---

### Issue 5: Implement skill-lint CI workflow

**Title:** `ci: add skill-lint GitHub Actions workflow for SKILL.md validation`

**Body:**
```markdown
## Description
Currently there is no automated validation of SKILL.md files in CI. This allows format violations (missing version, non-ASCII chars, broken references) to slip into main branch.

## Required action
Implement \`.github/workflows/skill-lint.yml\` workflow that:

1. **Validates frontmatter** — All SKILL.md files must have:
   - \`name\` field (kebab-case)
   - \`version\` field (semantic versioning)
   - \`description\` field (single-line quoted string)
   - \`allowed-tools\` field (list or empty)

2. **Checks file size** — Body length must be < 500 lines

3. **Validates YAML syntax** — Must parse as valid YAML

4. **Checks for non-ASCII** — Em dashes (—), curly quotes ("), arrows (→) not allowed in prose (OK in code blocks)

5. **Validates resource references** — All mentioned files/directories must exist

6. **Fails CI if violations found** — PR cannot merge with violations

## Implementation
A template is already in PRODUCTION_AUDIT.md and will be provided in the skeleton branch. Install at: \`.github/workflows/skill-lint.yml\`

## Success criteria
- Workflow runs on push and PR
- Fails if any SKILL.md violates rules
- Provides clear error messages
- All existing SKILL.md files pass (after issues #1–#4 are fixed)

## Effort estimate
20 minutes (mostly copy/adjust provided template)

## References
- See PRODUCTION_AUDIT.md section 5
- See .github/workflows/skill-lint.yml template
```

---

## PRIORITY 3 — DOCUMENTATION (Target: Before launch announcement)

### Issue 6: Create repo README.md

**Title:** `docs: add comprehensive README.md for public launch`

**Body:**
```markdown
## Description
The repository needs a public-facing README that explains:
- What the skill library is and who it's for
- Quick start (for users and contributors)
- Skill inventory and status
- Research foundations
- Testing and validation methodology
- How to contribute

## Required sections
- **What's Inside** — Overview of 26 skills and shared modules
- **Quick Start** — How to install and use a skill
- **Skill Inventory** — Table of all skills with status (v1.0.0, etc.)
- **Research & References** — Citations to MIT Tech Review, ArXiv, Hunting the Muse
- **Key Features** — Deterministic execution, fact lock, gating rules, pattern coverage
- **Testing & Validation** — How to run pytest, pattern coverage, skill linter
- **Human Evaluation** — Link to evaluation/EVAL_PLAN.md
- **Contributing** — Link to CONTRIBUTING.md
- **Support** — Issues, discussions, Q&A

## Reference
A draft README.md is provided in the production-audit branch.

## Success criteria
- README is 200-300 lines
- Includes all required sections
- Links are valid (README.md, CONTRIBUTING.md, PRODUCTION_AUDIT.md)
- Tone is professional, not marketing
- No em dashes or non-ASCII characters

## Effort estimate
30 minutes (edit provided draft)
```

---

### Issue 7: Create CONTRIBUTING.md for contributors

**Title:** `docs: add CONTRIBUTING.md with skill submission checklist`

**Body:**
```markdown
## Description
Contributors need clear guidance on how to submit a new skill or modify an existing one. CONTRIBUTING.md should include:
- SKILL.md format checklist
- How to write deterministic prompts
- Fact preservation requirements
- Unit test template
- PR gating rules (what causes CI to fail)
- How to run linters and tests locally

## Required sections
- **Before You Start** — Read README, check inventory, avoid duplicates
- **Step 1-5: Write a Skill** — Directory structure, SKILL.md template, checklist
- **Step 4: Write Unit Tests** — Test template with determinism and fact-lock examples
- **Step 5: Create a PR** — Conventional commits, PR template, what CI checks
- **PR Gating Rules** — List all CI checks that fail PRs
- **Modifying Existing Skills** — How to update version, changelog, tests
- **Shared Modules** — What goes in shared/ vs skills/
- **Questions?** — Support links

## Reference
A draft CONTRIBUTING.md is provided in the production-audit branch.

## Success criteria
- 200-300 lines
- Includes all required sections
- Checklist is exhaustive and clear
- Examples are realistic
- Links work
- Tone is welcoming and specific

## Effort estimate
30 minutes (edit provided draft)
```

---

### Issue 8: Create .github/pull_request_template.md

**Title:** `ci: add GitHub pull request template`

**Body:**
```markdown
## Description
When contributors open PRs, they should see a template that reminds them to:
- Describe the skill or change
- Reference research/patterns used
- Confirm the checklist (determinism, fact-lock, tests, etc.)
- Show example input/output

## Template structure
- **Description** — What does this skill/change do?
- **Skill Purpose** (if new skill) — What problem does it solve?
- **Research & References** — Links to papers, guides, etc.
- **Example Input/Output** — Inline or code block
- **Checklist** — All items from CONTRIBUTING.md
- **Ready for Review?** — Sign-off

## Location
\`.github/pull_request_template.md\`

## Success criteria
- Template appears when PR is opened
- Includes all checklist items from CONTRIBUTING.md
- Encourages examples and clear descriptions
- Tone is helpful, not burdensome

## Effort estimate
15 minutes
```

---

## Summary

| # | Issue | Status | Effort | Priority |
|---|-------|--------|--------|----------|
| 1 | Add version fields (12 skills) | — | 15m | P1 |
| 2 | Remove dangling examples/ refs (6 skills) | — | 10m | P1 |
| 3 | Consolidate scholar_editor dir | — | 5m | P1 |
| 4 | Replace em dashes (18 skills) | — | 30m | P2 |
| 5 | Implement skill-lint CI | — | 20m | P2 |
| 6 | Create README.md | — | 30m | P3 |
| 7 | Create CONTRIBUTING.md | — | 30m | P3 |
| 8 | Create PR template | — | 15m | P3 |

**Total for P1 (unblock release):** ~30 minutes
**Total for P2 (quality):** ~50 minutes
**Total for P3 (docs):** ~75 minutes
**Grand total:** ~155 minutes (~2.5 hours)

---

## Next Steps

1. Create these 8 issues in GitHub
2. Assign P1 issues to yourself or team member
3. Assign P2/P3 to subsequent sprints
4. Use this repo's PRODUCTION_AUDIT.md as reference during implementation
5. Once all P1 issues are closed, re-run CI to confirm all SKILL.md files pass linting
6. Announce public release once P1 + P2 are complete
