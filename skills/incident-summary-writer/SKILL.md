---
name: "incident-summary-writer"
version: "1.0.0"
description: "Generates a structured, factual incident summary from raw on-call notes."
allowed-tools: [Read, Write]
humanizer_patterns: [1, 4, 5, 7, 20, 22, 23]
nick_mode_profile: "technical"
tone_presets: [direct, neutral]
temperature: 0.0
seed: "INCIDENT_SEED_001"
---

# incident-summary-writer

**Purpose:** Convert messy on-call notes into a clean, timeline-based incident summary with root cause, impact, and action items. No hedging, no vague attribution.

## Input Schema

| Field | Type | Required |
|---|---|---|
| `incident_id` | string | yes |
| `timeline_notes` | string | yes - raw notes with timestamps |
| `severity` | string | yes - SEV1/SEV2/SEV3 |
| `affected_systems` | string[] | yes |
| `root_cause` | string | yes |
| `action_items` | string[] | yes |
| `preserve_facts` | string[] | yes |

```json
{
  "incident_id": "INC-2024-0314",
  "timeline_notes": "9:41pm pages fired. checked logs. 11:23pm resolved. load balancer config was wrong after the deploy",
  "severity": "SEV2",
  "affected_systems": ["checkout", "payments-api"],
  "root_cause": "Misconfigured load balancer after 11pm deploy",
  "action_items": ["Add LB config validation to deploy checklist", "Lower alert threshold to p95 > 500ms"],
  "preserve_facts": ["INC-2024-0314", "9:41 PM", "11:23 PM", "4,300 timed-out requests"]
}
```

## Output Schema

```json
{
  "title": "INC-2024-0314 - SEV2 - Checkout outage (March 14)",
  "summary": "...",
  "timeline": [{"time": "9:41 PM", "event": "..."}, ...],
  "root_cause": "...",
  "impact": "...",
  "action_items": [{"owner": "TBD", "item": "...", "due": "TBD"}]
}
```

## Prompt Flow

**Pass 1:** Structure into title, summary, timeline, root cause, impact, action items. Remove: significance inflation (P1), promotional adjectives (P4), weasel words (P5), AI vocab (P7), knowledge-cutoff disclaimers (P20), filler (P22), excessive hedging (P23).

**Pass 2:** "What sounds like AI-generated filler in this report?" -> final clean rewrite.

## Examples

### Short
**Before:** "We experienced some technical difficulties that may have potentially caused issues for certain users."
**After:** "Checkout returned 502s for 4,300 requests between 9:41 PM and 11:23 PM PT on March 14."

### Medium (summary)
**Before:** "The incident marks a pivotal moment in our infrastructure journey, underscoring the vital importance of robust configuration management going forward."
**After:** "Root cause: a load balancer config pushed at 11 PM set the health check timeout to 1ms instead of 500ms. Every backend instance failed health checks and was removed from the pool."

### Long (full report)

## Unit Tests

```python
# tests/skills/test_incident_summary_writer.py
from ai_pattern_scrubber import detect_patterns

SUMMARY = "Checkout returned 502s for 4,300 requests between 9:41 PM and 11:23 PM PT on March 14."
ROOT_CAUSE = "Root cause: a load balancer config pushed at 11 PM set the health check timeout to 1ms instead of 500ms."

def test_summary_no_hedging():
    assert not [h for h in detect_patterns(SUMMARY) if h.id == 23]

def test_root_cause_no_weasel_words():
    assert not [h for h in detect_patterns(ROOT_CAUSE) if h.id == 5]

def test_summary_no_high_severity():
    assert not [h for h in detect_patterns(SUMMARY) if h.severity == "high"]
```
