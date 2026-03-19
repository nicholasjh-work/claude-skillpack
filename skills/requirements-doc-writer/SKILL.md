---
name: "requirements-doc-writer"
version: "1.0.0"
description: "Writes structured requirements documents from product briefs or engineer notes."
allowed-tools: [Read, Write]
humanizer_patterns: [1, 4, 5, 7, 14, 15, 22]
nick_mode_profile: "technical"
tone_presets: [neutral, direct]
temperature: 0.0
seed: "REQ_DOC_SEED_001"
---

# requirements-doc-writer

**Purpose:** Convert product briefs, design notes, or meeting outputs into a structured requirements document with clear acceptance criteria.

## Input Schema

| Field | Type | Required |
|---|---|---|
| `feature_name` | string | yes |
| `problem_statement` | string | yes |
| `user_stories` | string[] | yes |
| `constraints` | string[] | yes |
| `non_goals` | string[] | yes |
| `preserve_facts` | string[] | yes |

```json
{
  "feature_name": "Saved Payment Methods",
  "problem_statement": "Users re-enter card details on every purchase. 28% of checkout abandonments cite friction.",
  "user_stories": ["As a returning user, I can save a card and use it on subsequent purchases without re-entering details"],
  "constraints": ["PCI-DSS compliance required", "Must support multi-card per user", "No server-side card storage"],
  "non_goals": ["Loyalty points", "Crypto payments"],
  "preserve_facts": ["28% abandonment", "PCI-DSS"]
}
```

## Output Schema

```json
{
  "title": "Requirements: Saved Payment Methods",
  "problem": "...",
  "user_stories": [{"id": "US-001", "story": "...", "acceptance_criteria": ["..."]}],
  "constraints": ["..."],
  "non_goals": ["..."],
  "open_questions": ["..."]
}
```

## Prompt Flow

**Pass 1:** Structure the doc. Write acceptance criteria as testable, binary pass/fail statements. Remove: significance inflation (P1), promotional adjectives (P4), weasel words (P5), AI vocab (P7), boldface overuse (P14), inline-header lists (P15), filler (P22).

**Pass 2:** Audit for any remaining vague language or non-testable requirements. Rewrite to concrete and specific.

## Examples

### Short - single AC
**Before:** "The system should provide a seamless and intuitive experience for saving payment methods, enhancing user satisfaction."
**After:** "AC: User can save a card at checkout with a single click. Saved card appears on next visit pre-selected."

### Medium - user story
**Before:** "As a user, I want to be able to leverage the platform's groundbreaking capabilities to manage my payment information in a dynamic way."
**After:** "US-001: As a returning user, I can view all saved cards, select one at checkout, and delete any card from my account settings."

### Long - constraints section
**Before:** "The solution must be built in a way that ensures compliance with all relevant regulatory frameworks and fosters trust among users."
**After:** "Constraints: (1) Card data must be tokenized via Stripe; no raw PANs stored server-side. (2) PCI-DSS SAQ A compliance required before launch. (3) Each user may store up to 5 cards."

## Unit Tests

```python
# tests/skills/test_requirements_doc_writer.py
from ai_pattern_scrubber import detect_patterns

AC = "User can save a card at checkout with one click. Saved card appears pre-selected on next visit."
CONSTRAINT = "Card data must be tokenized via Stripe; no raw PANs stored server-side. PCI-DSS SAQ A required."

def test_ac_no_ai_vocab():
    assert not [h for h in detect_patterns(AC) if h.id == 7]

def test_constraint_no_weasel_words():
    assert not [h for h in detect_patterns(CONSTRAINT) if h.id == 5]

def test_ac_no_high_severity():
    assert not [h for h in detect_patterns(AC) if h.severity == "high"]
```
