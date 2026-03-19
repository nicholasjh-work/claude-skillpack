---
name: "linkedin-message-writer"
version: "1.0.0"
description: "Writes short, direct LinkedIn outreach and response messages. No flattery, no filler."
allowed-tools: [Read, Write]
humanizer_patterns: [4, 7, 19, 21, 22]
nick_mode_profile: "email"
tone_presets: [direct, warm-professional, concise]
temperature: 0.0
seed: "LINKEDIN_SEED_001"
---

# linkedin-message-writer

**Purpose:** Generate LinkedIn messages that sound like a real human wrote them - direct opener, specific reason for reaching out, one clear ask.

## Input Schema

| Field | Type | Required |
|---|---|---|
| `message_type` | string | yes - outreach, response, follow-up, referral-ask |
| `recipient_name` | string | yes |
| `context` | string | yes - why you're reaching out and what you know about them |
| `ask` | string | yes - one specific ask |
| `your_name` | string | yes |
| `tone` | string | yes |

```json
{
  "message_type": "outreach",
  "recipient_name": "Priya",
  "context": "Priya is an eng manager at Stripe, posted about their platform team, I'm interested in staff eng roles",
  "ask": "15-minute call to learn about how the platform team is structured",
  "your_name": "Nick",
  "tone": "direct"
}
```

## Output Schema

```json
{
  "message": "...",
  "subject": "optional - for InMail",
  "word_count": 65,
  "patterns_removed": [7, 19, 21]
}
```

## Prompt Flow

**Pass 1:** One specific hook, one clear ask, sign-off. Under 75 words. Remove: chatbot openers (P19), sycophancy (P21), promotional adjectives (P4), AI vocab (P7), filler (P22).

**Pass 2:** Does it pass the "would I cringe if I received this?" test? Remove any remaining flattery or AI tells.

## Examples

### Short - cold outreach
**Before:** "I hope this message finds you well! I am incredibly excited to connect with you and would love to potentially explore some opportunities."
**After:** "Hi Priya - saw your post on Stripe's platform team. I'm a staff eng focused on infra and developer experience. Would a 15-minute call make sense to talk through how you've structured the team? Happy to share what I've been working on in return."

### Medium - response to a job post
**Before:** "Great opportunity! I am passionate about leveraging my extensive experience to add value to your dynamic team and contribute to your transformative mission."
**After:** "Hi - I saw the staff eng posting. I've spent 3 years building out platform tooling (CI, feature flags, deploy automation) at Series B and Series C companies. Happy to send a resume if it looks like a fit."

### Long - referral ask

## Unit Tests

```python
# tests/skills/test_linkedin_message_writer.py
from ai_pattern_scrubber import detect_patterns

OUTREACH = "Hi Priya - saw your post on Stripe's platform team. I'm a staff eng focused on infra and developer tooling. Would a quick call make sense? Happy to share what I've been working on."
RESPONSE = "Hi - I saw the staff eng posting. 3 years of platform tooling work (CI, feature flags, deploy automation). Happy to send a resume if it's a fit."

def test_outreach_no_sycophancy():
    assert not [h for h in detect_patterns(OUTREACH) if h.id == 21]

def test_response_no_promotional_language():
    assert not [h for h in detect_patterns(RESPONSE) if h.id == 4]

def test_outreach_no_chatbot_artifacts():
    assert not [h for h in detect_patterns(OUTREACH) if h.id == 19]
```
