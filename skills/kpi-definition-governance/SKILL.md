---
name: kpi-definition-governance
description: Define KPIs with formula, grain, source, exclusions, ownership, cadence, caveats, and business interpretation notes.
version: "1.0.0"
---

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
