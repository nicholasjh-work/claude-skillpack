---
name: data-integrity-investigator
description: Investigate mismatches, duplicates, missing records, broken keys, and reconciliation defects using structured SQL or Python diagnostics.
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
Investigate data issues with disciplined, staged diagnostics.

## Process
1. Restate the defect in operational terms.
2. Define expected grain, source of truth, and scope.
3. Start with row-count and date-range checks.
4. Check duplicates, orphan keys, null rates, and mapping drift.
5. Compare totals by meaningful business slices.
6. Narrow to exception populations.
7. State likely root cause and next test.

## Required mindset
- Separate confirmed facts from hypotheses.
- Do not jump to a root cause without evidence.
- Prefer targeted diagnostics over broad speculation.

## Output format
1. Issue framing
2. Diagnostic plan
3. SQL or Python checks in sequence
4. Findings
5. Most likely root cause
6. Next action

## Gotcha Enforcement

Apply these rules while building diagnostic SQL and interpreting results.
A HIGH violation in any diagnostic query you write must be corrected before
presenting it. Flag behavioral violations as part of the hypothesis tree.

| ID   | Sev    | Check                                                                              |
|------|--------|------------------------------------------------------------------------------------|
| G001 | HIGH   | No `SELECT *` in any diagnostic query produced                                     |
| G002 | HIGH   | State join cardinality before building any diagnostic join query                   |
| G003 | HIGH   | Document NULL behavior in every aggregation in the diagnostic SQL                  |
| G004 | HIGH   | Flag LEFT JOIN + WHERE on right side as a candidate root cause class               |
| G005 | HIGH   | Flag missing SCD current-row filter as a candidate root cause class                |
| G007 | HIGH   | Diagnostic queries must use a different access path than the report being tested   |
| G009 | MEDIUM | Include null rate check for every measure column in the investigation              |
| G010 | MEDIUM | Cardinality of every join key in diagnostic SQL must be stated or checked          |
| G011 | MEDIUM | If DISTINCT appears in the defective report SQL, call it out as a root-cause candidate |
| G012 | HIGH   | Confirm grain, period, and filter alignment before declaring a difference meaningful|
| G014 | HIGH   | Validation must compare a measure value, not just row count                        |
| G015 | MEDIUM | If net difference is zero, run segment-level check before declaring it clean       |
