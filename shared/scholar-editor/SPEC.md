# Scholar Editor - Expert Audit SPEC
**Version:** 0.1.0 | **Temperature:** 0.0 | **Seed:** SCHOLAR_SPEC_SEED_001

---

## 1. Overview

The Scholar Editor audit pipeline replaces the informal Humanizer two-pass flow with a rigorous
three-pass editorial pipeline. Detection is grounded in:

- **Statistical/lexical cues**: MIT Technology Review (2022) analysis of token-probability patterns
  in AI-generated text - high-frequency function words, low perplexity phrases, and smooth syntactic
  transitions are primary signals. Reference: https://www.technologyreview.com/2022/12/19/1065596/how-to-spot-ai-generated-text/
- **GLTR-style heuristics**: ArXiv 1906.04043 (Gehrmann et al., 2019) shows that AI text clusters
  in the top-k most probable token positions. Lexical cues that proxy for low-surprisal generation
  (e.g., AI vocabulary list, copula avoidance, filler phrases) are used as practical approximations.
  Reference: https://arxiv.org/abs/1906.04043
- **Classroom heuristics**: Hunting the Muse (https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai)
  and East Central faculty resources (https://www.eastcentral.edu/free/ai-faculty-resources/detecting-ai-generated-text/)
  provide practitioner-validated lexical signals: sycophantic openers, em-dash overuse, promotional
  adjectives, and chatbot communication artifacts.

Conservative policy: **prefer false negatives over false positives**. A `confidence` score below
0.7 suppresses the PatternHit. The goal is to flag only high-confidence tells.

---

## 2. API

### 2.1 `detect_patterns(text: str, domain: str = "general") -> List[PatternHit]`

Scans `text` for all 24 patterns from `rubric.json`. Returns a list of `PatternHit` objects.

**Parameters:**
- `text`: The prose to analyze (UTF-8 string, max 50,000 characters)
- `domain`: One of `"technical"`, `"academic"`, `"marketing"`, `"casual"`, `"general"`.
  Domain affects severity escalation rules (see rubric.json `when_high` fields).

**Returns:** `List[PatternHit]` - may be empty. Sorted by `span_start`.

**Raises:**
- `TextTooLongError`: if `len(text) > 50000`
- `PatternConfigError`: if `rubric.json` fails to load

### 2.2 `audit_draft(text: str, preserve_facts: List[str], domain: str = "general") -> AuditResult`

Runs the full Expert Audit pipeline: fact-lock pre-pass -> domain classification -> pattern detection.

**Parameters:**
- `text`: Draft text to audit
- `preserve_facts`: List of strings that must appear verbatim in any edited output
- `domain`: Domain hint (see above)

**Returns:** `AuditResult` with fields:
- `issues`: `List[Issue]`
- `facts_locked`: `Dict` from `extract_facts(text)`
- `domain_detected`: `str`
- `blocked`: `bool` - true if any `Issue.severity == "high"` or if any `preserve_facts` token
  is absent from `text`

---

## 3. Data Schemas

### 3.1 `PatternHit` (internal detector output)

```python
@dataclass
class PatternHit:
    id: int               # Pattern ID 1-24
    label: str            # Pattern label from rubric.json
    span_start: int       # Character offset of match start
    span_end: int         # Character offset of match end
    text: str             # Matched text substring
    severity: str         # "low" | "med" | "high"
    confidence: float     # 0.0-1.0; hits below 0.7 are suppressed
    rationale: str        # One-line explanation citing research source
```

### 3.2 `Issue` (audit output, matches SKILL.md output schema)

```json
{
  "rule_id": 7,
  "label": "Overused AI Vocabulary Words",
  "span_start": 42,
  "span_end": 57,
  "text": "crucial interplay",
  "severity": "high",
  "confidence": 0.95,
  "rationale": "Two AI vocabulary words in 17 chars. MIT (2022): high-frequency AI vocab clusters at low token-surprisal positions.",
  "suggested_fix": "Replace with specific noun: 'the tension between X and Y'"
}
```

### 3.3 `AuditResult`

```python
@dataclass
class AuditResult:
    issues: List[Issue]
    facts_locked: Dict        # {entities: [], dates: [], numerics: []}
    domain_detected: str
    blocked: bool
```

---

## 4. Expert Audit Prompt

Use this prompt when running the Scholar Editor audit pass via Claude API.
Settings: `temperature=0.0`, `top_p=0.0`, `seed=SCHOLAR_SPEC_SEED_001`.

### 4.1 System Prompt

```
You are a senior editorial auditor applying an evidence-based AI-writing detection rubric.

Your analysis is grounded in:
- MIT Technology Review (2022): statistical token-probability patterns in AI text
  (low perplexity, high-frequency function words, smooth syntactic transitions)
- ArXiv 1906.04043 - GLTR (Gehrmann et al., 2019): AI text clusters in top-k most probable
  token positions; lexical proxies include AI vocabulary lists and filler phrases
- Hunting the Muse practitioner heuristics: sycophantic openers, chatbot artifacts, em-dash overuse
- East Central faculty resources: promotional language, vague attributions, copula avoidance

You have access to rubric.json containing 24 pattern rules with detection_hint, severity_default,
when_high, and suggested_fix for each pattern ID (1-24).

Operating principles:
- Conservative: confidence < 0.7 -> do not emit an Issue
- Fact-lock: any preserve_facts token absent from the text -> blocked=true regardless of issues
- Never invent facts; never alter named entities, dates, or numeric claims
- Return ONLY valid JSON. No prose, no markdown, no explanation outside the JSON object.
```

### 4.2 User Prompt Template

```
DOMAIN: {domain}
PRESERVE_FACTS: {preserve_facts_json_array}

TEXT TO AUDIT:
---
{text}
---

TASK:
1. FACT-LOCK PRE-PASS: Extract all named entities (proper nouns), dates, and numeric claims
   from TEXT TO AUDIT. Store in facts_locked.

2. DOMAIN CLASSIFICATION: Classify the text as one of: technical, academic, marketing, casual.
   Use the DOMAIN hint if provided; override only if the text clearly contradicts it.

3. PATTERN DETECTION: For each of the 24 patterns in rubric.json, scan the text using
   the detection_hint regex/lexical cues. For each match:
   - Record span_start, span_end, matched text
   - Assign severity per severity_default; escalate to "high" if when_high condition is met
   - Compute confidence (0.0-1.0); suppress if < 0.7
   - Write a one-line rationale citing MIT (2022) or ArXiv 1906.04043 for patterns 7, 8, 22, 23;
     cite Hunting the Muse or East Central for patterns 4, 13, 19, 21.

4. GATING: Set blocked=true if:
   - Any issue has severity == "high", OR
   - Any string in preserve_facts is absent or altered in the text

5. OUTPUT: Return exactly this JSON object and nothing else:
{
  "issues": [
    {
      "rule_id": <int>,
      "label": "<string>",
      "span_start": <int>,
      "span_end": <int>,
      "text": "<matched substring>",
      "severity": "<low|med|high>",
      "confidence": <float>,
      "rationale": "<one-line>",
      "suggested_fix": "<from rubric.json suggested_fix>"
    }
  ],
  "facts_locked": {
    "entities": ["<string>"],
    "dates": ["<string>"],
    "numerics": ["<string>"]
  },
  "domain_detected": "<technical|academic|marketing|casual>",
  "blocked": <true|false>
}
```

---

## 5. Severity Escalation Rules

| Pattern ID | Default | Escalate to high when |
|---|---|---|
| 1 | high | 2+ significance phrases in one paragraph |
| 2 | med | Unverifiable outlet names not in preserve_facts |
| 3 | med | Participial clause is only analytical content |
| 4 | high | Always high in technical/academic domain |
| 5 | med | Sole support for a causal/statistical claim |
| 6 | med | No specific challenges named (all abstract nouns) |
| 7 | high | 3+ vocab words in 200-char window OR delve/tapestry anywhere |
| 8 | high | 2+ copula-avoidance constructions in one paragraph |
| 9 | med | Positive clause adds no specific information |
| 10 | med | 2+ triadic lists in 300 chars with abstract nouns |
| 11 | low | Technical doc where synonym cycling causes ambiguity |
| 12 | low | Incompatible conceptual categories in range |
| 13 | high | >2 em dashes in 300 chars OR >1 in single sentence |
| 14 | med | Bold in consecutive sentences or >3 in 300 chars |
| 15 | med | 3+ consecutive inline-header bullets |
| 16 | med | Style guide specifies sentence case (academic/technical) |
| 17 | low | Emoji in section heading (formal context) |
| 18 | low | Code doc or markdown where curly quotes break syntax |
| 19 | high | Always high - unambiguous chatbot artifact |
| 20 | low | Document presented as authoritative/published |
| 21 | high | Always high - sycophantic openers in any context |
| 22 | med | Multiple fillers stack in single sentence |
| 23 | med | 3+ hedge tokens in 100-char window |
| 24 | high | Appears in final 20% of document |

---

## 6. Error Types

- `TextTooLongError(text_length, max_length=50000)`: text exceeds processing limit
- `PatternConfigError(missing_key)`: rubric.json is malformed or a required field is absent

---

## 7. Non-Goals

- This spec does not define the Draft or Final prompts (see `skills/scholar-editor/SKILL.md`)
- This spec does not define the human evaluation rubric (see `evaluation/EVAL_PLAN.md`)
- The mock_detector.py is a deterministic approximation; it does not call any LLM

---

## 8. Versioning

| Version | Change |
|---|---|
| 0.1.0 | Initial release; 24 patterns from Humanizer SPEC.md; Expert Audit prompt v1 |
