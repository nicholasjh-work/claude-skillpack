---
name: sql-report-builder
description: Build report-safe SQL from business requests with grain control, join discipline, filter logic, and validation notes.
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
Turn a business request into production-grade SQL for reporting or analysis.

## Process
1. Identify business objective.
2. Define the intended grain before writing SQL.
3. List source tables, required joins, filters, and date logic.
4. Flag join-risk before generating the query.
5. Separate ad hoc SQL from report-safe SQL when relevant.
6. Add a validation checklist after the SQL.

## Required checks
- Base grain is explicit
- Join cardinality is assessed
- Aggregation level matches requested output
- Null handling is deliberate
- Date filters use business-safe logic
- Filter placement does not silently change row inclusion
- Naming is readable and consistent

## Output format
1. Assumptions and grain
2. SQL
3. Validation checklist
4. Risks or open questions

## Gotcha Enforcement

Before finalizing any SQL output, verify each rule below. A HIGH violation
must be corrected before responding. A MEDIUM violation must be flagged with
an explanation in the risks section.

| ID   | Sev    | Check                                                                           |
|------|--------|---------------------------------------------------------------------------------|
| G001 | HIGH   | No `SELECT *` in any CTE or final SELECT                                        |
| G002 | HIGH   | Every join has a stated cardinality; if unknown, provide the verification query |
| G003 | HIGH   | Every AVG, SUM, or COUNT documents its NULL behavior explicitly                 |
| G004 | HIGH   | No WHERE filter on a right-side column after a LEFT JOIN                        |
| G005 | HIGH   | Every dimension join includes an active/current filter or documents why not     |
| G006 | HIGH   | All measures in one SELECT are at the same grain; mixed grains use separate CTEs|
| G007 | HIGH   | Validation queries use a different access path than the report SQL              |
| G010 | MEDIUM | Cardinality of every join key is confirmed or a check query is provided         |
| G011 | MEDIUM | Any DISTINCT is accompanied by a root-cause note, not just applied silently     |
