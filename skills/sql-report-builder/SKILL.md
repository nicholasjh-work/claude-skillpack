---
name: sql-report-builder
description: Build report-safe SQL from business requests with grain control, join discipline, filter logic, and validation notes.
version: "1.0.0"
---

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
