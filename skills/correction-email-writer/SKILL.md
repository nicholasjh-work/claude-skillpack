---
name: "correction-email-writer"
version: "1.0.0"
description: "Writes correction or apology emails that own the mistake clearly, without over-hedging or grovelling."
allowed-tools: [Read, Write]
humanizer_patterns: [7, 19, 21, 22, 23]
tone_presets: [direct, accountable, formal]
temperature: 0.0
seed: "CORRECTION_SEED_001"
---

# correction-email-writer

**Purpose:** Convert an awkward apology or correction draft into a clean, accountable message: what went wrong, what was fixed, what changes next.

## Input Schema

| Field | Type | Required |
|---|---|---|
| `what_went_wrong` | string | yes |
| `impact` | string | yes - quantified if possible |
| `what_was_fixed` | string | yes |
| `what_changes_next` | string | yes |
| `audience` | string | yes |
| `tone` | string | yes |

```json
{
  "what_went_wrong": "Wrong pricing shown on checkout for EU customers for 4 hours on March 10",
  "impact": "142 affected orders, $8,400 overcharged",
  "what_was_fixed": "Pricing service redeployed at 3:14 PM PT; all affected orders refunded",
  "what_changes_next": "Added EU pricing validation to deploy checklist",
  "audience": "EU customers",
  "tone": "accountable"
}
```

## Prompt Flow

**Pass 1:** State mistake first. Quantify impact. State fix. State prevention. No qualifiers on the apology. Remove: P19, P21, P22, P7, P23.
**Pass 2 Audit + Final:** Identify any remaining hedging or blame-diffusion language. Rewrite direct and clean.

## Examples

### Short
**Before:** "We sincerely apologize for any inconvenience this may have potentially caused. We value your business."
**After:** "We showed incorrect pricing on March 10. Your order was refunded in full and should appear in 2-3 business days."

### Medium
**Before:** "Due to a complex technical situation involving our pricing infrastructure, some customers may have experienced incorrect pricing."
**After:** "On March 10 (11 AM-3 PM PT), EU customers saw incorrect prices at checkout. 142 orders were affected and all have been refunded. We've added a validation step to prevent this happening again."

### Long (exec escalation)
**Before:** "I hope this message finds you well. I wanted to reach out and provide transparency regarding a situation."
**After:** "On March 10, a misconfigured feature flag applied USD rates instead of EUR rates for 4 hours. 142 orders were overcharged $8,400 combined. We refunded all affected customers by 5 PM the same day. Root cause: flag validation was skipped in a hotfix deploy. Fix: flag validation is now required for all deploys; alert threshold lowered to 5 affected orders."

## Unit Tests

```python
# tests/skills/test_correction_email_writer.py
from ai_pattern_scrubber import detect_patterns

SHORT = "We showed incorrect pricing on March 10. Your order was refunded in full and should appear in 2-3 business days."
MEDIUM = "On March 10 (11 AM-3 PM PT), EU customers saw incorrect prices. 142 orders affected, all refunded. Validation step added."

def test_correction_short_no_high_severity():
    assert not [h for h in detect_patterns(SHORT) if h.severity == "high"]

def test_correction_medium_no_high_severity():
    assert not [h for h in detect_patterns(MEDIUM) if h.severity == "high"]

def test_correction_medium_no_hedging():
    assert not [h for h in detect_patterns(MEDIUM) if h.id == 23]
```
