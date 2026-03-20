---
name: kpi-definition-governance
description: Define KPIs with formula, grain, source, exclusions, ownership, cadence, caveats, and business interpretation notes.
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
Create formal KPI definitions that are usable across reporting and governance.

## Required fields
- KPI name
- business purpose
- formula
- grain
- source system or source table
- inclusions and exclusions
- owner
- refresh cadence
- caveats
- interpretation notes

## Rules
- Distinguish business definition from technical implementation.
- Document edge cases.
- State where competing definitions may exist.

## Output format
Return a clean data-dictionary-style KPI entry.

## Gotcha Enforcement

A KPI definition that violates any HIGH rule below is incomplete. Do not
return a definition until all HIGH rules pass. Flag MEDIUM violations in
the Governance risks section.

| ID   | Sev    | Check                                                                              |
|------|--------|------------------------------------------------------------------------------------|
| G003 | HIGH   | Formula must specify NULL treatment explicitly                                     |
| G006 | HIGH   | Calculation grain and reporting grain must be separately stated                    |
| G008 | HIGH   | Inclusions AND exclusions must both be populated; no exclusions = incomplete       |
| G013 | LOW    | If the KPI is used in a ranked output, tie-break behavior must be documented       |
