---
name: "technical-writer"
version: "1.0.0"
description: "Writes and edits technical documentation: READMEs, runbooks, ADRs, and API docs. Enforces plain language and factual precision."
allowed-tools: [Read, Write]
humanizer_patterns: [1, 3, 4, 5, 7, 8, 14, 15, 22]
nick_mode_profile: "technical"
tone_presets: [direct, concise, neutral]
temperature: 0.0
seed: "TECH_WRITER_SEED_001"
---

# technical-writer

**Purpose:** Transform rough technical notes or verbose AI-generated drafts into clear, scannable technical documentation.

## Input Schema

| Field | Type | Required |
|---|---|---|
| `doc_type` | string | yes - readme, runbook, adr, api-doc, design-doc |
| `content` | string | yes - raw notes or draft |
| `preserve_facts` | string[] | yes |
| `audience` | string | yes - e.g., "on-call engineers", "external API consumers" |
| `tone` | string | yes |

```json
{
  "doc_type": "runbook",
  "content": "When the service goes down you should check the logs and then maybe restart it. The service is very important and serves as a critical component in our infrastructure.",
  "preserve_facts": ["service name: payment-processor", "restart command: systemctl restart payment-processor"],
  "audience": "on-call engineers",
  "tone": "direct"
}
```

## Output Schema

```json
{
  "title": "Runbook: payment-processor",
  "sections": {
    "symptoms": "...",
    "diagnosis": "...",
    "resolution": "...",
    "escalation": "..."
  },
  "patterns_removed": [1, 7, 8, 14],
  "word_count": 120
}
```

## Prompt Flow

**Pass 1:** Rewrite into appropriate doc structure for `doc_type`. Remove: significance inflation (P1), promotional adjectives (P4), AI vocab (P7), copula avoidance (P8), boldface overuse (P14), inline-header lists (P15), filler (P22). Preserve `preserve_facts`.

**Pass 2 Audit + Final:** Check for any remaining vague attributions (P5) or -ing tail clauses (P3). Rewrite to specific and direct.

## Examples

### Short - runbook symptom
**Before:** "The service serves as a critical component and may be experiencing issues that could potentially be causing downstream impact."
**After:** "Symptom: payment-processor is returning 5xx. Downstream: checkout is blocked."

### Medium - README section
**Before:** "This groundbreaking tool boasts the ability to leverage cutting-edge algorithms to enhance developer productivity."
**After:** "This tool reduces CI build time by parallelizing your test suite. It requires Python 3.11+ and a Redis instance."

### Long - ADR
**Before:** "We have decided to utilize a microservices architecture, underscoring its vital role in our evolving landscape and highlighting its significance for long-term scalability, cultivating a foundation for future growth."
**After:** "Decision: adopt a microservices architecture for the billing domain.\nContext: the monolith's deploy cycle is 2 hours; billing changes block all other deploys.\nConsequences: services will communicate over gRPC; the team needs observability tooling."

## Unit Tests

```python
# tests/skills/test_technical_writer.py
from ai_pattern_scrubber import detect_patterns

SHORT = "Symptom: payment-processor is returning 5xx. Downstream: checkout is blocked."
MEDIUM = "This tool reduces CI build time by parallelizing your test suite. It requires Python 3.11+ and a Redis instance."

def test_tech_short_no_high_severity():
    assert not [h for h in detect_patterns(SHORT) if h.severity == "high"]

def test_tech_medium_no_promotional_language():
    assert not [h for h in detect_patterns(MEDIUM) if h.id == 4]

def test_tech_medium_no_ai_vocab():
    assert not [h for h in detect_patterns(MEDIUM) if h.id == 7]
```
