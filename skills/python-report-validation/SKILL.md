---
name: python-report-validation
description: Validate report outputs with Python using row-count checks, subtotal tests, duplicate-grain checks, and comparison summaries.
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
Validate report output before release or after logic changes.

## Checks
- row counts
- duplicate grain checks
- subtotal to total tie-out
- period coverage
- category coverage
- comparison to prior or source extract
- reasonableness checks

## Output format
1. Validation scope
2. Pass or fail checks
3. Exceptions
4. Python script
5. Release risk summary

## Gotcha Enforcement

Every validation script produced must satisfy these rules.
HIGH violations block output. MEDIUM violations appear in Validation results
as warnings with explanation.

| ID   | Sev    | Check                                                                              |
|------|--------|------------------------------------------------------------------------------------|
| G002 | HIGH   | If the report involves a join, state the expected cardinality and test for fan-out  |
| G003 | HIGH   | Every aggregation in validation code documents its NA/null behavior explicitly     |
| G007 | HIGH   | Validation logic must not replicate the report's own SQL or transformation logic   |
| G009 | MEDIUM | Null rate for every critical measure column must be checked and surfaced           |
| G012 | HIGH   | Confirm grain, period, and filter alignment before comparing source to report      |
| G014 | HIGH   | At least one measure value must be reconciled; row count alone is not sufficient   |
| G015 | MEDIUM | If net difference is zero, run a segment-level check before calling the report clean|
