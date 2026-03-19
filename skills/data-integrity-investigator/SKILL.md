---
name: data-integrity-investigator
description: Investigate mismatches, duplicates, missing records, broken keys, and reconciliation defects using structured SQL or Python diagnostics.
version: "1.0.0"
---

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
