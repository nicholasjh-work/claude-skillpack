---
name: "executive-summary-writer"
version: "1.0.0"
description: "Writes an executive summary for a longer report or proposal. Distills to: what happened, what it means, what's next."
allowed-tools: [Read, Write]
humanizer_patterns: [1, 3, 4, 5, 6, 7, 14, 15, 22, 23, 24]
nick_mode_profile: "default"
tone_presets: [executive, direct, neutral]
temperature: 0.0
seed: "EXEC_SUMMARY_SEED_001"
---

# executive-summary-writer

**Purpose:** Take a full report or document and synthesize it into a 150-300 word executive summary that a decision-maker can act on without reading the full document.

## Input Schema

| Field | Type | Required |
|---|---|---|
| `source_title` | string | yes |
| `source_content` | string | yes - full document or long excerpt |
| `audience` | string | yes |
| `key_findings` | string[] | yes - top 3-5 findings to surface |
| `recommended_actions` | string[] | yes |
| `preserve_facts` | string[] | yes |

```json
{
  "source_title": "Q1 2024 Platform Engineering Report",
  "source_content": "...",
  "audience": "VP Engineering",
  "key_findings": ["CI build time improved 60%", "On-call volume down 40%", "2 critical infra migrations completed"],
  "recommended_actions": ["Approve Q2 headcount for observability", "Extend Kubernetes rollout to remaining 12 services"],
  "preserve_facts": ["60%", "40%", "12 services", "Q1 2024"]
}
```

## Output Schema

```json
{
  "title": "Executive Summary: Q1 2024 Platform Engineering",
  "summary": "...",
  "findings": ["..."],
  "recommended_actions": ["..."],
  "word_count": 215
}
```

## Prompt Flow

**Pass 1:** Three-part structure: What happened (findings), What it means (interpretation in 1-2 sentences), What's next (recommended actions). Remove: P1, P3, P4, P5, P6, P7, P14, P15, P22, P23, P24. Preserve all facts.

**Pass 2:** "What in this summary is padding?" -> cut aggressively to under 300 words. Every sentence must do work.

## Examples

### Short - findings sentence
**Before:** "The platform team has made significant strides, showcasing their commitment to fostering a culture of continuous improvement that underscores their vital role in the organization's evolving landscape."
**After:** "CI build time dropped 60% in Q1; on-call volume fell 40%."

### Medium - full summary
**Before:** "In conclusion, the future looks bright for our platform infrastructure. Exciting times lie ahead as we continue this journey toward excellence and scalability."
**After:** "Q1 work shipped two critical migrations and cut on-call load nearly in half. Q2 priority: extend Kubernetes to the remaining 12 services and hire 2 observability engineers to avoid repeating the January monitoring gap."

### Long

## Unit Tests

```python
# tests/skills/test_executive_summary_writer.py
from ai_pattern_scrubber import detect_patterns

FINDING = "CI build time dropped 60% in Q1; on-call volume fell 40%."
CLOSE = "Q2 priority: extend Kubernetes to 12 services and hire 2 observability engineers."

def test_finding_no_significance_inflation():
    assert not [h for h in detect_patterns(FINDING) if h.id == 1]

def test_close_no_generic_conclusion():
    assert not [h for h in detect_patterns(CLOSE) if h.id == 24]

def test_finding_no_high_severity():
    assert not [h for h in detect_patterns(FINDING) if h.severity == "high"]
```
