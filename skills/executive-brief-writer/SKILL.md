---
name: "executive-brief-writer"
version: "1.0.0"
description: "Writes a 1-page executive brief from dense technical or project content. No puffery, every sentence earns its place."
allowed-tools: [Read, Write]
humanizer_patterns: [1, 2, 4, 5, 6, 7, 14, 15, 22, 24]
nick_mode_profile: "default"
tone_presets: [executive, direct, concise]
temperature: 0.0
seed: "EXEC_BRIEF_SEED_001"
---

# executive-brief-writer

**Purpose:** Distill a complex project, proposal, or decision into a 1-page executive brief with situation, recommendation, evidence, and ask.

## Input Schema

| Field | Type | Required |
|---|---|---|
| `title` | string | yes |
| `situation` | string | yes - 2-3 sentence context |
| `recommendation` | string | yes |
| `supporting_evidence` | string[] | yes - 3-5 data points |
| `risks` | string[] | yes |
| `ask` | string | yes - what exec needs to decide or approve |
| `preserve_facts` | string[] | yes |

```json
{
  "title": "Migrate billing to Stripe - Q2 decision",
  "situation": "Current billing provider charges 2.9% + $0.30 per transaction. Stripe charges 2.5% + $0.15. At $3M/month volume, the delta is $12,000/month.",
  "recommendation": "Migrate to Stripe by June 30.",
  "supporting_evidence": ["$12K/month savings = $144K/year", "Migration estimated 6 weeks engineering", "Zero-downtime cutover proven via 3 internal dry runs"],
  "risks": ["1-week risk window during cutover", "EU tax reporting requires Stripe Tax add-on ($500/month)"],
  "ask": "Approve migration budget ($15K eng time + $500/mo Stripe Tax)",
  "preserve_facts": ["$12K/month", "$144K/year", "June 30", "3 dry runs"]
}
```

## Prompt Flow

**Pass 1:** Write tight, structured brief: Situation (2 sentences), Recommendation (1-2 sentences), Evidence (3-5 bullets), Risks (2-3 bullets), Ask (1 sentence). Remove: P1, P4, P5, P7, P14, P15, P22, P24.

**Pass 2:** "What in this brief wastes a busy exec's time?" -> trim aggressively. Final should be under 350 words.

## Examples

### Short - situation sentence
**Before:** "The current billing infrastructure serves as a pivotal component in our financial ecosystem, underscoring the transformative potential of modernization."
**After:** "Our billing provider charges $12K/month more than Stripe at current transaction volume."

### Medium - evidence section
**Before:** "Additionally, industry observers have noted that payment infrastructure modernization fosters long-term scalability and vibrant growth opportunities."
**After:** "Evidence: (1) $144K/year savings at $3M/month volume. (2) 6-week migration with 3 completed dry runs. (3) Zero-downtime cutover confirmed in staging."

### Long

## Unit Tests

```python
# tests/skills/test_executive_brief_writer.py
from ai_pattern_scrubber import detect_patterns

SITUATION = "Our billing provider charges $12K/month more than Stripe at current transaction volume."
EVIDENCE = "Evidence: $144K/year savings. 6-week migration, 3 dry runs completed. Zero-downtime confirmed in staging."

def test_situation_no_significance_inflation():
    assert not [h for h in detect_patterns(SITUATION) if h.id == 1]

def test_evidence_no_ai_vocab():
    assert not [h for h in detect_patterns(EVIDENCE) if h.id == 7]

def test_evidence_no_weasel_words():
    assert not [h for h in detect_patterns(EVIDENCE) if h.id == 5]
```
