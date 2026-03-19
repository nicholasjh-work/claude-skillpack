# nick-mode-writing-standard

**Version:** 1.0.0 | [schema.json](./schema.json)

Machine-readable writing rules for Nicholas Hidalgo. Enforces direct, factual, voice-forward prose. See `schema.json` for the full rule definitions.

---

## Validation API

```python
from nick_mode import validate_against_standard

# Returns list of Violation objects
violations = validate_against_standard(text, profile="resume")
```

### `validate_against_standard(text: str, profile: str) -> list[Violation]`

| Field | Type | Description |
|---|---|---|
| `rule_id` | str | e.g. `"NICK-004"` |
| `rule_name` | str | Human-readable name |
| `severity` | `"error"` \| `"warning"` | error = must fix |
| `matched_text` | str | The flagged substring |
| `span_start` | int | Char offset (inclusive) |
| `span_end` | int | Char offset (exclusive) |
| `suggestion` | str | Replacement guidance |

**Profiles:** `default` | `resume` | `email` | `technical`

---

## 12 Canonical Rewrites

| # | Rule | Before | After |
|---|---|---|---|
| 1 | NICK-001 ban_em_dash | The result-a 40% drop-justified the refactor. | The result was a 40% drop, which justified the refactor. |
| 2 | NICK-002 ban_emojis | 🚀 Launched new checkout flow in Q3. | Launched new checkout flow in Q3. |
| 3 | NICK-003 prefer_copula | The tool serves as a unified platform for all workflows. | The tool is a unified platform for all workflows. |
| 4 | NICK-004 ban_ai_vocab | I delve into the intricate interplay of distributed systems. | I analyze how distributed systems interact. |
| 5 | NICK-005 ban_sycophantic | Great question! Here's an overview. | The French Revolution began with fiscal crisis in 1789. |
| 6 | NICK-006 ban_weasel | Experts believe the approach reduces latency. | A 2023 AWS benchmark showed a 38% latency reduction. |
| 7 | NICK-007 ban_promotional | Drove profound impact across the organization. | Reduced onboarding time by 3 weeks across 4 teams. |
| 8 | NICK-008 ban_filler | In order to achieve this, it is important to note that planning is essential. | To achieve this, plan carefully. |
| 9 | NICK-009 ban_excessive_hedging | It could potentially possibly be argued the policy might have some effect. | The policy may affect outcomes. |
| 10 | NICK-010 ban_generic_conclusions | The future looks bright as we continue this journey toward excellence. | The company plans to open two locations and hire 40 engineers. |
| 11 | NICK-011 ban_cutoff_disclaimers | While specific details are limited based on available information, it appears to have been founded in the 1990s. | The company was founded in 1994, per its SEC filing. |
| 12 | NICK-012 require_metric (resume) | Improved the onboarding experience for new engineers. | Cut new-engineer ramp time from 6 weeks to 3 weeks by rewriting the runbook. |

---

## Unit Tests

```python
# tests/test_nick_mode.py
import pytest
from nick_mode import validate_against_standard

def violations_for(text, profile="default"):
    return validate_against_standard(text, profile=profile)

def rule_ids(violations):
    return {v.rule_id for v in violations}


class TestNickModeRules:

    def test_nick001_em_dash_error(self):
        vs = violations_for("The result\u2014a 40% drop\u2014justified it.")
        assert "NICK-001" in rule_ids(vs)
        assert any(v.severity == "error" for v in vs if v.rule_id == "NICK-001")

    def test_nick001_no_em_dash_passes(self):
        vs = violations_for("The result was a 40% drop, which justified the refactor.")
        assert "NICK-001" not in rule_ids(vs)

    def test_nick002_emoji_in_bullet_error(self):
        vs = violations_for("- \U0001F680 Launched checkout flow.")
        assert "NICK-002" in rule_ids(vs)

    def test_nick003_copula_avoidance_warning(self):
        vs = violations_for("The tool serves as a unified platform.")
        assert "NICK-003" in rule_ids(vs)

    def test_nick004_ai_vocab_delve_error(self):
        vs = violations_for("Let me delve into the details.")
        assert "NICK-004" in rule_ids(vs)

    def test_nick004_ai_vocab_clean_passes(self):
        vs = violations_for("Let me explain the details.")
        assert "NICK-004" not in rule_ids(vs)

    def test_nick005_sycophantic_opener_error(self):
        vs = violations_for("Great question! Here is an overview.")
        assert "NICK-005" in rule_ids(vs)

    def test_nick006_weasel_words_warning(self):
        vs = violations_for("Experts believe this approach reduces costs.")
        assert "NICK-006" in rule_ids(vs)

    def test_nick008_filler_phrase_warning(self):
        vs = violations_for("In order to achieve this goal, planning is key.")
        assert "NICK-008" in rule_ids(vs)

    def test_nick009_stacked_hedges_warning(self):
        vs = violations_for("It could potentially possibly be argued there might be an effect.")
        assert "NICK-009" in rule_ids(vs)

    def test_nick010_generic_conclusion_error(self):
        vs = violations_for("The future looks bright as we continue this journey toward excellence.")
        assert "NICK-010" in rule_ids(vs)

    def test_nick012_resume_requires_metric(self):
        vs = violations_for(
            "Improved the onboarding experience for new engineers.",
            profile="resume"
        )
        assert "NICK-012" in rule_ids(vs)
        match = next(v for v in vs if v.rule_id == "NICK-012")
        assert match.severity == "error"
        assert "number" in match.suggestion.lower() or "metric" in match.suggestion.lower() or "{n}" in match.suggestion.lower()
```
