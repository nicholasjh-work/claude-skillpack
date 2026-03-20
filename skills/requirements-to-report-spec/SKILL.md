---
name: requirements-to-report-spec
description: Convert messy business requests into a clean implementation-ready report specification with grain, measures, filters, assumptions, and open questions.
version: "1.0.0"
---

## Runtime Configuration
```yaml
version: "1.0.0"
gotcha_pack: "sql-data-gotcha-pack"
gotcha_pack_version: "1.0.0"
gotcha_enforcement: "block_on_high"
```


# Purpose
Convert a stakeholder request into a build-ready report spec.

## Capture
- business objective
- intended audience
- report grain
- measures
- dimensions
- filters and prompts
- date logic
- output format
- assumptions
- unresolved questions
- delivery priority

## Rules
- Surface ambiguity early.
- Distinguish must-have from optional scope.
- Push for concrete KPI definitions.
- Document exclusions and edge cases.

## Output format
1. Objective
2. Audience
3. Grain
4. Measures and definitions
5. Dimensions and filters
6. Layout or delivery notes
7. Assumptions
8. Open questions

## Gotcha Enforcement

A spec that leaves these HIGH-risk areas unresolved is not build-ready.
Resolve each HIGH item or escalate it as a blocking open question.
Flag MEDIUM items in Implementation notes.

| ID   | Sev    | Check                                                                              |
|------|--------|------------------------------------------------------------------------------------|
| G006 | HIGH   | If the spec mixes measures from different grains, call it out as a blocking ambiguity|
| G008 | HIGH   | Every KPI in the spec must have explicit inclusions AND exclusions documented      |
| G009 | MEDIUM | If a column is listed as a measure, note that null rate must be checked before build|
| G013 | LOW    | Any top-N or ranked output must include tie-break and minimum-record behavior      |
