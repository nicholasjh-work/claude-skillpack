---
name: "resume-editor"
version: "1.0.0"
description: "Edits existing resume bullets to remove banned language and add metrics without changing meaning."
allowed-tools: [Read, Write]
humanizer_patterns: [1, 4, 7, 8, 19, 21, 22]
nick_mode_profile: "resume"
resume_banned_version: "1.0.0"
tone_presets: [direct, technical]
temperature: 0.0
seed: "RESUME_EDITOR_SEED_001"
---

# resume-editor

**Purpose:** Take existing resume bullets and improve them: remove banned phrases, add or surface metrics, start with action verbs. Preserve all factual claims.

## Input Schema

| Field | Type | Required |
|---|---|---|
| `bullets` | string[] | yes - existing resume bullets |
| `context` | string | no - additional context for metric inference |
| `preserve_facts` | string[] | yes - must not change these |
| `tone` | string | yes |

```json
{
  "bullets": [
    "Responsible for managing the data pipeline",
    "Helped improve system reliability",
    "Strong communicator who worked with stakeholders"
  ],
  "context": "Senior Data Engineer at a fintech startup, 2021-2023",
  "preserve_facts": ["data pipeline", "fintech"],
  "tone": "direct"
}
```

## Output Schema

```json
{
  "edited_bullets": [
    {"original": "...", "revised": "...", "changes": ["removed 'responsible for'", "added action verb 'Owned'"]}
  ],
  "banned_phrases_removed": ["responsible for", "helped", "strong communicator"],
  "metric_warnings": ["bullet 2: no metric found - add a number before publishing"]
}
```

## Prompt Flow

**Pass 1:** For each bullet: flag banned phrases -> rewrite starting with action verb -> inject metric if known -> preserve preserve_facts.
**Pass 2:** Audit for remaining AI tells. Flag bullets with no metric as warnings (do not fabricate metrics).

## Examples

### Short
**Before:** "Responsible for managing the data pipeline."
**After:** "Owned and maintained the Airflow-based data pipeline processing 500GB nightly."

### Medium
**Before:** "Helped improve system reliability and worked with the on-call team."
**After:** "Reduced mean time to recovery from 45 min to 12 min by documenting the top 8 incident runbooks."

### Long
**Before:** "Results-driven professional responsible for driving cross-functional collaboration to achieve business outcomes."
**After:** "Led quarterly roadmap reviews with product, engineering, and sales (12 stakeholders); 9 of 11 Q3 commitments shipped on time."

## Unit Tests

```python
# tests/skills/test_resume_editor.py
from resume_banned import flag_banned_phrases

EDITED = [
    "Owned and maintained the Airflow-based data pipeline processing 500GB nightly.",
    "Reduced MTTR from 45 min to 12 min by documenting 8 incident runbooks.",
]

def test_edited_bullets_no_banned_phrases():
    for b in EDITED:
        assert flag_banned_phrases(b) == [], f"Banned phrase remains: {b}"

def test_edited_bullets_start_with_verb():
    action_verbs = {"owned","reduced","built","cut","shipped","led","wrote","launched","designed","managed","created"}
    for b in EDITED:
        first_word = b.split()[0].lower().rstrip(".,")
        assert first_word in action_verbs, f"Bullet doesn't start with action verb: {b}"

def test_metric_warning_issued_for_vague_bullet():
    # resume-editor should flag bullets with no metric, not fabricate one
    from resume_editor import edit_bullets
    result = edit_bullets(["Strong communicator who worked with stakeholders."], preserve_facts=[])
    assert any("metric" in w.lower() for w in result.get("metric_warnings", [])), \
        "Expected metric warning for vague bullet"
```
