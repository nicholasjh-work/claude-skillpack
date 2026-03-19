---
name: "resume-bullet-rewriter"
version: "1.0.0"
description: "Rewrites a single resume bullet to be metric-backed, action-verb-led, and free of banned phrases."
allowed-tools: [Read, Write]
humanizer_patterns: [1, 4, 7, 8, 22]
nick_mode_profile: "resume"
resume_banned_version: "1.0.0"
tone_presets: [direct]
temperature: 0.0
seed: "BULLET_REWRITER_SEED_001"
---

# resume-bullet-rewriter

**Purpose:** Targeted single-bullet rewriter. Accepts one weak bullet and returns a strengthened version plus a metric-gap warning if no number is available.

## Input Schema

| Field | Type | Required |
|---|---|---|
| `bullet` | string | yes |
| `context` | string | no - role, company, level |
| `available_metrics` | string[] | no - numbers to work in |
| `preserve_facts` | string[] | yes |

```json
{
  "bullet": "Responsible for improving the checkout experience and working with design.",
  "context": "Senior Product Manager, e-commerce startup",
  "available_metrics": ["checkout conversion up 12%", "reduced 3-step flow to 1-step"],
  "preserve_facts": ["12%", "1-step"]
}
```

## Output Schema

```json
{
  "original": "...",
  "revised": "...",
  "changes": ["removed 'responsible for'", "added metric 12%", "started with action verb 'Redesigned'"],
  "metric_warning": null
}
```

## Prompt Flow

**Pass 1:** Rewrite starting with action verb. Inject best available metric from `available_metrics`. Remove all banned phrases. Preserve `preserve_facts`.

**Pass 2:** If no metric available, output revised bullet + `metric_warning: "No metric available - add a number before publishing."` Never fabricate a metric.

## Examples

### Short
**Before:** "Responsible for improving the checkout experience."
**After:** "Redesigned checkout from a 3-step to 1-step flow, lifting conversion by 12%."

### Medium
**Before:** "Helped to streamline the onboarding process and assisted with implementation."
**After:** "Wrote the engineer onboarding runbook adopted across 3 teams; ramp time dropped from 6 weeks to 3."

### Long (with context)
**Before:** "Results-driven PM passionate about delivering innovative solutions that leverage data to drive business outcomes at scale."
**After:** "Shipped 6 product features in Q2 2024 driven by customer cohort analysis; 4 of 6 exceeded their 90-day retention targets."

## Unit Tests

```python
# tests/skills/test_resume_bullet_rewriter.py
from resume_banned import flag_banned_phrases
from ai_pattern_scrubber import detect_patterns
import re

REVISED = "Redesigned checkout from a 3-step to 1-step flow, lifting conversion by 12%."
METRIC_PATTERN = re.compile(r'\d+[%xKMB]?|\$[\d,]+|\d+\s*(weeks?|days?|steps?)')

def test_revised_no_banned_phrases():
    assert flag_banned_phrases(REVISED) == []

def test_revised_contains_metric():
    assert METRIC_PATTERN.search(REVISED), "Revised bullet must contain a metric"

def test_revised_no_high_severity():
    assert not [h for h in detect_patterns(REVISED) if h.severity == "high"]
```
