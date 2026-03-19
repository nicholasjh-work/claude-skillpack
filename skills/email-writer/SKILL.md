---
name: "email-writer"
version: "1.0.0"
description: "Writes clear, direct professional emails. Removes sycophancy, filler, and AI tells."
allowed-tools: [Read, Write]
humanizer_patterns: [7, 8, 9, 13, 19, 21, 22, 23]
tone_presets: [direct, formal, concise, warm-professional]
temperature: 0.0
seed: "EMAIL_SEED_001"
---

# email-writer

**Purpose:** Convert a brief or messy email draft into a direct, natural-sounding professional email free of AI tells.

## Input Schema

| Field | Type | Required | Notes |
|---|---|---|---|
| `subject_line` | string | yes | Proposed subject or topic |
| `intent` | string | yes | What the email needs to accomplish |
| `key_facts` | string[] | yes | Facts, names, dates that must be preserved |
| `tone` | string | yes | One of: direct, formal, concise, warm-professional |
| `raw_draft` | string | no | Rough draft to clean up |

```json
{
  "subject_line": "API deprecation timeline",
  "intent": "Notify the payments team that v1 API endpoints are deprecated and cutover is required by March 31.",
  "key_facts": ["March 31 deadline", "v1 API", "payments team", "docs at /api/migration"],
  "tone": "direct",
  "raw_draft": "I hope this email finds you well! I wanted to reach out and touch base regarding the important and crucial matter of our API deprecation timeline going forward."
}
```

## Output Schema

```json
{
  "subject": "v1 API deprecation - cutover required by March 31",
  "body": "The v1 API endpoints will be shut off March 31. If your team is still using them, migrate before then - the guide is at /api/migration. Reply here or ping me in Slack if you hit anything unexpected.",
  "patterns_removed": [7, 19, 22],
  "word_count": 52
}
```

## Prompt Flow

**Pass 1:** Apply core email rewrite. Remove: chatbot openers (P19), sycophancy (P21), em dashes (P13), AI vocab (P7), filler (P22), negative parallelisms (P9), excessive hedging (P23), copula avoidance (P8). Preserve `key_facts`.

**Pass 2 Audit:** "What makes this email so obviously AI-generated?" - list remaining tells.

**Pass 2 Final:** Rewrite removing remaining tells. Keep under 150 words unless facts require more.

## Examples

### Short - API notification
**Before:** "I hope this email finds you well! I wanted to reach out regarding the crucial API deprecation timeline, which stands as a pivotal moment in our infrastructure evolution."
**After:** "The v1 API endpoints shut down March 31. Migrate before then - guide at /api/migration."

### Medium - Status update
**Before:** "Just wanted to circle back and provide an update. At this point in time, we have completed the initial phase of the project."
**After:** "Quick status: phase 1 is done. Phase 2 (auth integration) starts Monday. We're on track for the April 15 launch."

### Long - Escalation with context
**Before:** "Great question regarding the outage. Additionally, industry observers have noted that distributed systems face challenges typical of complex environments. The future looks bright."
**After:** "The March 14 outage (9:41-11:23 PM PT) was a misconfigured load balancer after the 11 PM deploy. 4,300 requests timed out. Fix: config rollback. Post-mortem at [link]. I've added a deploy checklist item to catch this going forward."

## Unit Tests

```python
# tests/skills/test_email_writer.py
import pytest
from ai_pattern_scrubber import detect_patterns

SHORT_FINAL = "The v1 API endpoints shut down March 31. Migrate before then - guide at /api/migration."
MEDIUM_FINAL = "Quick status: phase 1 is done. Phase 2 (auth integration) starts Monday. On track for April 15."
LONG_FINAL = (
    "The March 14 outage (9:41\u201311:23 PM PT) was a misconfigured load balancer. "
    "4,300 requests timed out. Fix: config rollback. Post-mortem at [link]."
)

def high_severity_hits(text):
    return [h for h in detect_patterns(text) if h.severity == "high"]

def test_email_short_no_high_severity_flags():
    assert high_severity_hits(SHORT_FINAL) == []

def test_email_medium_no_high_severity_flags():
    assert high_severity_hits(MEDIUM_FINAL) == []

def test_email_long_no_high_severity_flags():
    assert high_severity_hits(LONG_FINAL) == []
```
