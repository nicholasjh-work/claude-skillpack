---
name: "meeting-notes-to-decision-memo"
version: "1.0.0"
description: "Converts raw meeting notes into a structured decision memo with owners and deadlines."
allowed-tools: [Read, Write]
humanizer_patterns: [1, 7, 19, 21, 22, 24]
nick_mode_profile: "email"
tone_presets: [direct, concise]
temperature: 0.0
seed: "MEMO_SEED_001"
---

# meeting-notes-to-decision-memo

**Purpose:** Turn messy meeting notes into a concise decision memo: decisions made, action items with owners and dates, open questions.

## Input Schema

| Field | Type | Required |
|---|---|---|
| `meeting_title` | string | yes |
| `date` | string | yes |
| `attendees` | string[] | yes |
| `raw_notes` | string | yes |
| `preserve_facts` | string[] | yes |

```json
{
  "meeting_title": "Checkout v2 Go/No-Go",
  "date": "2024-03-18",
  "attendees": ["Nick", "Sarah (PM)", "Dev (Eng Lead)"],
  "raw_notes": "we talked about the launch. sarah said we should delay. nick pushed back. decided to do soft launch march 25 with 5% traffic. dev to set up flags by thursday. lots of debate about support readiness. open q: does support need more training?",
  "preserve_facts": ["March 25", "5% traffic", "Thursday deadline for flags"]
}
```

## Output Schema

```json
{
  "memo_title": "Decision Memo: Checkout v2 Go/No-Go (March 18)",
  "decisions": [{"decision": "...", "rationale": "..."}],
  "action_items": [{"item": "...", "owner": "...", "due": "..."}],
  "open_questions": ["..."],
  "next_meeting": "TBD"
}
```

## Prompt Flow

**Pass 1:** Extract decisions, actions, open questions. Assign owners where named in notes. Remove: chatbot artifacts (P19), sycophancy (P21), filler (P22), generic conclusions (P24), AI vocab (P7), significance inflation (P1).

**Pass 2:** Verify every action item has an owner and due date (mark TBD if not stated - do not fabricate).

## Examples

### Short
**Before notes:** "We decided to go with option B. John will do the thing by next week."
**After:**
- **Decision:** Option B selected.
- **Action:** John to complete implementation. Due: March 25.

### Medium
**Before notes:** "big discussion about launch. ultimately decided soft launch. eng will set feature flags. pm will brief support. support training might be needed."
**After:**
- **Decision:** Soft launch at 5% traffic on March 25.
- **Actions:** Dev - set feature flags by March 21. Sarah - brief support by March 22.
- **Open question:** Does support need additional training before full rollout?

### Long

## Unit Tests

```python
# tests/skills/test_meeting_notes_to_decision_memo.py
from ai_pattern_scrubber import detect_patterns

DECISION = "Decision: Soft launch at 5% traffic on March 25."
ACTION = "Dev to set feature flags by March 21. Sarah to brief support by March 22."

def test_decision_no_filler():
    assert not [h for h in detect_patterns(DECISION) if h.id == 22]

def test_action_no_high_severity():
    assert not [h for h in detect_patterns(ACTION) if h.severity == "high"]

def test_decision_no_ai_vocab():
    assert not [h for h in detect_patterns(DECISION) if h.id == 7]
```
