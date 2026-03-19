# Contributing to claude-writing-skillpack

Thank you for considering a contribution! This guide ensures all submissions maintain high quality, consistency, and safety standards before merge.

## Before You Start

- Read the README.md to understand the project scope
- Check the [PRODUCTION_AUDIT.md](PRODUCTION_AUDIT.md) for current known issues and priorities
- Review the [skill inventory table](README.md#skill-inventory) to avoid duplicate efforts
- Ensure you have Python 3.10+ and `pytest` installed locally

## Submitting a New Skill

### Step 1: Create Your Skill Directory

```bash
mkdir -p skills/your-skill-name
```

Follow the naming convention: **kebab-case, descriptive, under 30 characters**.

Good: `email-writer`, `resume-editor`, `incident-summary-writer`
Bad: `email_rewriter`, `Emailer`, `e-writer`

### Step 2: Write SKILL.md

Create `skills/your-skill-name/SKILL.md` using this template:

```markdown
---
name: "your-skill-name"
version: "1.0.0"
description: "One-line description of what this skill does."
allowed-tools: [Read, Write]
temperature: 0.0
seed: YOUR_SKILL_SEED_001
---

# your-skill-name

**Purpose:** What problem does this solve?

## Input Schema

| Field | Type | Required | Notes |
|---|---|---|---|
| ... | ... | ... | ... |

\`\`\`json
{
  "field1": "value1"
}
\`\`\`

## Output Schema

\`\`\`json
{
  "result": "output"
}
\`\`\`

## Prompt Flow

**Pass 1:** ...
**Pass 2:** ...

## Examples

### Short

**Before:** ...
**After:** ...

...
```

### Step 3: SKILL.md Checklist

- [ ] **Frontmatter present and valid YAML**
  - `name` (kebab-case, no special chars)
  - `version` (semantic versioning: 1.0.0)
  - `description` (single-line quoted string, no multi-line blocks)
  - `allowed-tools` (list of Claude Code tools, or empty)
  - `temperature: 0.0` (deterministic)
  - `seed: YOUR_SKILL_SEED_001` (named seed for reproducibility)

- [ ] **Description is pragmatic**
  - What does this do in one sentence?
  - Avoids marketing language or superlatives
  - No em dashes, curly quotes, or decorative symbols in prose

- [ ] **No hallucinated resources**
  - All referenced files/directories exist or are documented
  - No dangling links to `examples/`, `docs/`, or `fixtures/`
  - If you reference `shared/` modules, verify they exist

- [ ] **Input and output schemas are clear**
  - JSON format with type hints
  - Field names are snake_case
  - Example values are realistic and concise

- [ ] **Prompts are deterministic**
  - No "be creative" or "use your judgment" instructions
  - Temperature 0.0 always
  - All randomness pinned to the `seed`

- [ ] **Fact preservation**
  - If the skill outputs writing, it must have a `preserve_facts` field
  - Include explicit "do not fabricate metrics/names/dates" instructions
  - Document that any altered preserve_facts token sets `blocked: true`

- [ ] **Hallucination controls**
  - For resume skills: reference `resume_banned_language_pack`
  - For editing skills: reference `ai_pattern_scrubber` or `scholar_editor`
  - Include examples showing how fabrication is prevented

- [ ] **Body length**
  - File size < 500 lines (most will be 50–150 lines)
  - If longer, consider splitting into multiple skills or moving examples to `evaluation/`

- [ ] **Section headers match canonical structure**
  - Use: Purpose, Input Schema, Output Schema, Prompt Flow, Examples, Version History
  - Don't invent new section names

### Step 4: Write Unit Tests

Create `tests/test_your_skill.py`:

```python
import pytest
from shared.ai_pattern_scrubber import detect_patterns  # if you use it

def test_determinism():
    """Same input + seed → identical output."""
    # Call your skill twice with the same seed
    # Assert output is byte-for-byte identical
    pass

def test_preserve_facts():
    """All preserve_facts tokens appear verbatim in output."""
    facts = ["Jane Doe", "2025-12-31", "$100K"]
    output = your_skill(facts=facts)
    for fact in facts:
        assert fact in output
    pass

def test_no_fabrication():
    """No metrics/dates/names are invented."""
    # Verify that when an unknown metric is requested,
    # the skill either returns blocked=true or
    # preserves the fact verbatim (doesn't invent)
    pass
```

Run locally:
```bash
pytest tests/test_your_skill.py -v
```

### Step 5: Create a PR

1. **Fork and branch:**
   ```bash
   git checkout -b feat/your-skill-name
   ```

2. **Commit with a conventional message:**
   ```bash
   git add skills/your-skill-name/SKILL.md tests/test_your_skill.py
   git commit -m "feat: add your-skill-name

   - Adds [your-skill-name] skill for [purpose]
   - Implements Draft-Audit-Final pipeline with fact preservation
   - Includes unit tests for determinism and fact-lock
   - Passes skill-lint and pytest checks

   Fixes #NNN"
   ```

3. **Push and open a PR:**
   ```bash
   git push origin feat/your-skill-name
   ```

4. **Fill in the PR template** (see `.github/pull_request_template.md`):
   - Describe what the skill does
   - Link to any research/references
   - Confirm all checklist items are complete
   - Share example input/output

## PR Gating Rules

Your PR will automatically fail CI if:

- ❌ Any SKILL.md is missing required frontmatter fields (name, version, description)
- ❌ Description is multi-line YAML block (must be single-line quoted string)
- ❌ File size exceeds 500 lines
- ❌ Non-ASCII characters (em dashes, curly quotes) appear in prose sections
- ❌ Referenced files/directories don't exist (e.g., `examples/long.json`)
- ❌ Unit tests fail (pytest exits non-zero)
- ❌ Pattern coverage < 0.9 (if skill references shared detectors)
- ❌ Determinism test fails (same seed → different output)
- ❌ Any preserve_facts token is altered or missing in skill output

Run checks locally before pushing:

```bash
# Lint SKILL.md
python tools/skill_linter.py skills/your-skill-name/SKILL.md

# Run tests
pytest tests/test_your_skill.py -v

# Check pattern coverage
python tools/check_pattern_coverage.py
```

## Modifying Existing Skills

If you're fixing a bug, improving a prompt, or updating documentation in an existing skill:

1. Update the skill's `SKILL.md`
2. Bump the patch version (e.g., 1.0.0 → 1.0.1)
3. Add a new entry to the **Version History** section
4. Update tests if behavior changes
5. Open a PR with title: `fix: [skill-name] <short description>`

Example:
```markdown
| Version | Change |
|---|---|
| 1.0.1 | Fix em dash usage in examples; improve fact-lock heuristic |
| 1.0.0 | Initial release |
```

## Shared Modules (for reference, not skills)

The following directories in `shared/` are **reference material** to be embedded or imported by skills, NOT standalone publishable skills:

- `ai-pattern-scrubber/` — 24 AI pattern detection rules
- `resume-banned-language-pack/` — Banned language list for resumes
- `nick-mode-writing-standard/` — Style rules and examples
- `scholar-editor/` — Editorial rubric, detectors, and prompts

**Do not create a SKILL.md for these.** Instead:
- Skills that use these modules should reference them in their unit tests (e.g., `from shared.ai_pattern_scrubber import detect_patterns`)
- Document the dependency in your SKILL.md's purpose section
- Ensure the shared module is present in the repo before your PR is merged

## Questions or Issues?

- **SKILL.md format question?** Open a discussion or check SKILL.md examples in the repo
- **Found a bug in a skill?** Open an issue with a reproduction case
- **Want to propose a new pattern?** Start a discussion in the `[research]` category
- **CI is failing?** Run `python tools/skill_linter.py` locally to see the exact error

## Code of Conduct

Be respectful and constructive. We're building tools for professional writers and teams.

---

**Version:** 1.0.0
**Last Updated:** March 2026
