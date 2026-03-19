---
name: "resume-writer"
version: "1.0.0"
description: "Writes full resume sections from raw experience notes. Enforces metric-backed bullets and bans all AI vocabulary."
allowed-tools: [Read, Write]
humanizer_patterns: [1, 4, 7, 8, 19, 21, 22]
nick_mode_profile: "resume"
resume_banned_version: "1.0.0"
tone_presets: [direct, technical, executive]
temperature: 0.0
seed: "RESUME_WRITER_SEED_001"
---

# resume-writer

**Purpose:** Generate polished, metric-backed resume sections from raw experience notes. Every bullet must contain a concrete outcome or number.

## Input Schema

| Field | Type | Required |
|---|---|---|
| `role_title` | string | yes |
| `company` | string | yes |
| `dates` | string | yes |
| `raw_notes` | string | yes - bullet-point brain dump |
| `impact_facts` | string[] | yes - metrics to weave in |
| `target_role` | string | no - used to tailor emphasis |
| `tone` | string | yes |

```json
{
  "role_title": "Senior Software Engineer",
  "company": "Acme Corp",
  "dates": "Jan 2022 - Mar 2024",
  "raw_notes": "Led backend rewrite of the payments service. Worked with product and design. Reduced latency. Mentored 2 junior engineers. On-call rotation.",
  "impact_facts": ["latency dropped 60%", "zero downtime migration", "service handles 800K req/day"],
  "target_role": "Staff Engineer",
  "tone": "direct"
}
```

## Output Schema

```json
{
  "header": "Senior Software Engineer - Acme Corp (Jan 2022 - Mar 2024)",
  "bullets": [
    "Rewrote the payments service backend, cutting p99 latency by 60% and migrating 800K daily requests with zero downtime.",
    "Mentored 2 junior engineers through design review and on-call onboarding; both shipped independently within 3 months."
  ],
  "patterns_removed": [1, 4, 7, 22],
  "banned_phrases_removed": ["responsible for", "helped to"],
  "metric_coverage": "100%"
}
```

## Prompt Flow

**Pass 1:** For each raw note, generate a bullet that: starts with an action verb, contains a metric or outcome from `impact_facts`, avoids all banned phrases (RBL-001-020), and does not use AI vocabulary (P7).

**Pass 2 Audit:** "What makes these bullets sound AI-generated?" -> list tells.

**Pass 2 Final:** Rewrite any flagged bullets. Verify every bullet has a number or concrete deliverable.

## Examples

### Short - single bullet
**Before:** "Responsible for improving the onboarding experience."
**After:** "Cut new-engineer ramp time from 6 weeks to 3 by rewriting the onboarding runbook."

### Medium - 3 bullets from notes
**Before notes:** "Worked on the data pipeline. Helped with reliability. Did some mentoring."
**After:**
- "Built a Kafka-based event pipeline processing 2M events/day, replacing a polling approach that failed above 100K."
- "Reduced on-call pages 60% by adding alert deduplication and a runbook for the top 5 incident types."
- "Mentored 3 engineers on distributed systems design; all 3 shipped independently within 2 months."

### Long - full role section
**Before notes:** "Led the platform team. Cross-functional work. Improved developer velocity. Streamlined processes. Launched new features. Worked with infra."
**After:**
- "Owned the platform team (6 engineers) responsible for the CI/CD pipeline, internal tooling, and dev environment."
- "Cut CI build time from 18 minutes to 6 by parallelizing test suites - saving ~200 engineer-hours/month."
- "Shipped the internal feature-flag system used by 30+ engineers, enabling partial rollouts and eliminating coordinated deploys."
- "Partnered with infra to migrate 40 services to Kubernetes; zero production incidents during the 8-month rollout."

## Unit Tests

```python
# tests/skills/test_resume_writer.py
from ai_pattern_scrubber import detect_patterns
from resume_banned import flag_banned_phrases

BULLETS = [
    "Rewrote the payments service backend, cutting p99 latency by 60% and migrating 800K daily requests with zero downtime.",
    "Mentored 2 junior engineers through design review; both shipped independently within 3 months.",
    "Cut new-engineer ramp time from 6 weeks to 3 by rewriting the onboarding runbook.",
]

def test_bullets_no_high_severity_ai_patterns():
    for b in BULLETS:
        hits = [h for h in detect_patterns(b) if h.severity == "high"]
        assert hits == [], f"High-severity hit in: {b}"

def test_bullets_no_banned_phrases():
    for b in BULLETS:
        flags = flag_banned_phrases(b)
        assert flags == [], f"Banned phrase in: {b}: {flags}"

def test_bullets_contain_metric():
    import re
    metric_pattern = re.compile(r'\d+[%xKMB]?|\$[\d,]+')
    for b in BULLETS:
        assert metric_pattern.search(b), f"No metric found in bullet: {b}"
```
