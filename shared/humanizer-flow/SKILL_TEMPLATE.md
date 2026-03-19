---
name: "{skill_name}"
version: "1.0.0"
description: "{skill_description}"
allowed-tools:
  - Read
  - Write
  - Bash
humanizer_version: "2.2.0"
nick_mode_version: "1.0.0"
temperature: 0.0
seed: "{seed_placeholder}"
---

# {skill_name}

## Purpose

{skill_purpose_one_liner}

## Input Schema

```json
{
  "skill_name": "{skill_name}",
  "input": {
    "text": "string - the raw text to process",
    "context": "string - brief description of the document type and audience",
    "tone": "string - one of: {tone_presets}",
    "preserve_facts": ["array of strings - entities, dates, metrics that must not change"],
    "profile": "string - one of: default | resume | email | technical"
  }
}
```

**Allowed tones:** `{tone_presets}`

## Output Schema

```json
{
  "skill_name": "{skill_name}",
  "output": {
    "draft": "string - Pass 1 rewrite",
    "audit_bullets": ["string - remaining AI tells identified in self-audit"],
    "final": "string - Pass 2 final rewrite after audit",
    "changes_summary": "string - optional brief list of changes made",
    "patterns_removed": [1, 7, 13],
    "fact_check": {
      "preserved": ["list of facts confirmed present in final"],
      "warnings": ["list of facts that may have changed - requires human review"]
    }
  }
}
```

---

## Canonical Prompt Flow

### PASS 1 - Draft Rewrite

> **Settings:** temperature=0.0, seed={seed_placeholder}

```
You are a writing editor that removes signs of AI-generated text using the 24 Humanizer patterns.

CONTEXT: {context}
TONE: {tone}
PRESERVE THESE FACTS (do not alter, omit, or fabricate): {preserve_facts}

INPUT TEXT:
{text}

TASK:
1. Scan for all 24 Humanizer patterns (see pattern list below).
2. Rewrite each flagged section. Do NOT alter any item in preserve_facts.
3. Ensure the result:
   - Sounds natural when read aloud
   - Varies sentence structure
   - Uses specific details over vague claims
   - Uses simple copulas (is/are/has) where appropriate
   - Matches tone: {tone}
4. Return ONLY the rewritten text. No commentary.

PATTERN CATEGORIES TO CHECK:
- CONTENT (1-6): significance inflation, notability claims, -ing endings, promotional language, weasel words, challenges-section boilerplate
- LANGUAGE (7-12): AI vocabulary, copula avoidance, negative parallelisms, rule-of-three, synonym cycling, false ranges
- STYLE (13-18): em dashes, boldface overuse, inline-header lists, title case, emojis, curly quotes
- COMMUNICATION (19-21): chatbot artifacts, knowledge-cutoff disclaimers, sycophancy
- FILLER/HEDGING (22-24): filler phrases, stacked hedges, generic positive conclusions
```

---

### PASS 2A - Anti-AI Audit

> **Settings:** temperature=0.0, seed={seed_placeholder}

```
What makes the following so obviously AI generated? List only the remaining tells as brief bullet points. Be specific - name the phrase or construction, not just the category.

TEXT:
{draft_output}
```

---

### PASS 2B - Final Rewrite

> **Settings:** temperature=0.0, seed={seed_placeholder}

```
Now make it not obviously AI generated.

PRESERVE THESE FACTS: {preserve_facts}
REMAINING AI TELLS: {audit_bullets}

TEXT:
{draft_output}

Return ONLY the rewritten final text. No preamble, no explanation.
```

---

## Sample JSON Request

```json
{
  "skill_name": "{skill_name}",
  "input": {
    "text": "{domain_examples.short.text}",
    "context": "{domain_examples.short.context}",
    "tone": "direct",
    "preserve_facts": {domain_examples.short.preserve_facts},
    "profile": "default"
  }
}
```

## Sample JSON Response

```json
{
  "skill_name": "{skill_name}",
  "output": {
    "draft": "{domain_examples.short.expected_draft}",
    "audit_bullets": [
      "Remaining tell 1",
      "Remaining tell 2"
    ],
    "final": "{domain_examples.short.expected_final}",
    "changes_summary": "Removed 3 AI vocabulary words, replaced em dash, deleted sycophantic opener.",
    "patterns_removed": [7, 13, 21],
    "fact_check": {
      "preserved": {domain_examples.short.preserve_facts},
      "warnings": []
    }
  }
}
```

---

## Examples

See `examples/short.json`, `examples/medium.json`, `examples/long.json` for domain-specific cases.

---

## Version History

| Version | Change |
|---|---|
| 1.0.0 | Initial release using Humanizer v2.2.0 two-pass flow |
