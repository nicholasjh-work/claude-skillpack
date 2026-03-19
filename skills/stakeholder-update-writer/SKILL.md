---
name: "stakeholder-update-writer"
version: "1.0.0"
description: "Writes concise, credible stakeholder updates: status, risks, decisions needed. No puffery."
allowed-tools: [Read, Write]
humanizer_patterns: [1, 2, 4, 5, 6, 7, 19, 21, 22, 24]
nick_mode_profile: "email"
tone_presets: [direct, executive, concise]
temperature: 0.0
seed: "STAKEHOLDER_SEED_001"
---

# stakeholder-update-writer

**Purpose:** Convert raw project status into a clear stakeholder update: RAG status, what's done, what's at risk, what needs a decision.

## Input Schema

| Field | Type | Required |
|---|---|---|
| `project_name` | string | yes |
| `period` | string | yes - e.g., "Week of March 18" |
| `rag_status` | string | yes - RED/AMBER/GREEN |
| `completed` | string[] | yes |
| `in_progress` | string[] | yes |
| `risks` | string[] | yes |
| `decisions_needed` | string[] | no |
| `preserve_facts` | string[] | yes |

```json
{
  "project_name": "Checkout v2",
  "period": "Week of March 18",
  "rag_status": "AMBER",
  "completed": ["Auth integration shipped to staging", "Load test: 50K RPS sustained"],
  "in_progress": ["Payment provider switchover (60%)"],
  "risks": ["Payment provider API docs are incomplete - may delay switchover by 1 week"],
  "decisions_needed": ["Approve 1-week delay or re-scope?"],
  "preserve_facts": ["50K RPS", "March 31 deadline", "payment provider: Stripe"]
}
```

## Prompt Flow

**Pass 1:** Format as RAG + bullets structure. Remove: significance inflation (P1), promotional language (P4), chatbot artifacts (P19), sycophancy (P21), filler (P22), generic conclusions (P24).

**Pass 2 Audit + Final:** Eliminate any remaining vague attributions or puffery. Every risk must name the specific blocker and owner.

## Examples

### Short (GREEN status)
**Before:** "The project is progressing well and we are excited about the outstanding results we are achieving together as a team."
**After:** "GREEN: Auth shipped to staging. Load test passed at 50K RPS. On track for March 31."

### Medium (AMBER)
**Before:** "Despite facing some challenges typical of complex projects, the team continues to demonstrate resilience and commitment as we navigate this journey."
**After:** "AMBER: Payment provider API docs are incomplete. Switchover is at 60% but may slip 1 week. Decision needed by Thursday: approve delay or re-scope the March 31 release?"

### Long (RED escalation)
**Before:** "It is widely believed that the project has encountered some headwinds, and industry observers have noted that integration challenges are not uncommon."
**After:** "RED: Stripe's 3DS2 sandbox is returning 500s on all card-not-present transactions. We're blocked on the payment switchover. Unblocking options: (1) use Stripe test cards only through March 27, (2) switch to Adyen for the launch - needs exec sign-off by EOD Monday."

## Unit Tests

```python
# tests/skills/test_stakeholder_update_writer.py
from ai_pattern_scrubber import detect_patterns

GREEN = "GREEN: Auth shipped to staging. Load test passed at 50K RPS. On track for March 31."
AMBER = "AMBER: Payment provider API docs incomplete. Switchover at 60% - may slip 1 week. Decision needed Thursday."

def test_green_no_promotional_language():
    assert not [h for h in detect_patterns(GREEN) if h.id == 4]

def test_amber_no_high_severity():
    assert not [h for h in detect_patterns(AMBER) if h.severity == "high"]

def test_amber_no_generic_conclusion():
    assert not [h for h in detect_patterns(AMBER) if h.id == 24]
```
