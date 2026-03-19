---
name: "cover-letter-writer"
version: "1.0.0"
description: "Writes specific, story-driven cover letters. Bans generic openers, AI vocabulary, and all banned resume phrases."
allowed-tools: [Read, Write]
humanizer_patterns: [1, 4, 5, 7, 19, 21, 22, 24]
nick_mode_profile: "resume"
resume_banned_version: "1.0.0"
tone_presets: [direct, warm-professional]
temperature: 0.0
seed: "COVER_LETTER_SEED_001"
---

# cover-letter-writer

**Purpose:** Generate a cover letter that opens with a specific story or observation, connects your experience to the role with concrete examples, and closes with one clear ask.

## Input Schema

| Field | Type | Required |
|---|---|---|
| `role_title` | string | yes |
| `company` | string | yes |
| `opening_hook` | string | yes - a specific story, observation, or connection point |
| `relevant_experience` | string[] | yes - 2-3 items with metrics |
| `why_this_company` | string | yes - specific, not generic |
| `ask` | string | yes |
| `preserve_facts` | string[] | yes |

```json
{
  "role_title": "Staff Engineer",
  "company": "Stripe",
  "opening_hook": "I've been using Stripe since 2015 and recently went through your API migration guide - the versioning strategy is the clearest I've seen in fintech.",
  "relevant_experience": [
    "Built a payment routing engine at Acme that processed $40M/month, reducing failed payments by 22%",
    "Led a 6-engineer team through a PCI-DSS Level 1 certification"
  ],
  "why_this_company": "Stripe's developer-first approach to infrastructure problems is how I think about building platform tools",
  "ask": "Conversation about the staff engineering role on the payments platform team",
  "preserve_facts": ["$40M/month", "22%", "PCI-DSS Level 1", "2015"]
}
```

## Prompt Flow

**Pass 1:** Open with hook (no "I am writing to apply" or similar). Body: 2 specific examples with metrics. Close: one clear call to action. Remove: P1, P4, P7, P19, P21, P22, P24. Run against resume-banned-language-pack.

**Pass 2 Audit + Final:** Remove any remaining puffery, genericness, or AI tells.

## Examples

### Short - 1-paragraph hook
**Before:** "I am incredibly excited and passionate about this opportunity to leverage my extensive experience at your groundbreaking company."
**After:** "I've been using Stripe since 2015. When I read through your API versioning guide last month, it was the clearest versioning strategy I've seen in fintech - exactly the level of care I try to put into platform work."

### Medium - body paragraph
**Before:** "I have proven track record of results-driven leadership that has added significant value to organizations through innovative solutions."
**After:** "At Acme, I built the payment routing logic that processes $40M/month. When the first provider started failing, the system rerouted automatically - zero engineer intervention. That's the kind of reliability I want to build at scale."

### Long

## Unit Tests

```python
# tests/skills/test_cover_letter_writer.py
from ai_pattern_scrubber import detect_patterns
from resume_banned import flag_banned_phrases

HOOK = "I've been using Stripe since 2015. The API versioning guide is the clearest I've seen in fintech."
BODY = "At Acme, I built the payment routing engine processing $40M/month. When providers failed, the system rerouted automatically."

def test_hook_no_sycophancy():
    assert not [h for h in detect_patterns(HOOK) if h.id == 21]

def test_body_no_banned_phrases():
    assert flag_banned_phrases(BODY) == []

def test_hook_no_high_severity():
    assert not [h for h in detect_patterns(HOOK) if h.severity == "high"]
```
