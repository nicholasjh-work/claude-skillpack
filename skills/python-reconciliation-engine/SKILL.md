---
name: python-reconciliation-engine
description: Compare two datasets by key, isolate missing rows and field-level differences, and summarize reconciliation exceptions clearly.
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
Compare two datasets and explain the differences clearly.

## Workflow
1. Define the comparison key and expected grain.
2. Standardize data types and key formatting.
3. Identify rows only in left, only in right, and in both.
4. Compare important numeric and text fields.
5. Bucket exceptions by issue type.
6. Summarize count and amount deltas.

## Output format
1. Comparison setup
2. Reconciliation summary
3. Exception categories
4. Python script
5. Next action

## Gotcha Enforcement

Every reconciliation script must satisfy these rules before output.
HIGH violations block output. MEDIUM violations appear in Exception summary
with an explanation.

| ID   | Sev    | Check                                                                              |
|------|--------|------------------------------------------------------------------------------------|
| G003 | HIGH   | Every aggregation documents NA/null behavior; sums must match treatment on both sides |
| G007 | HIGH   | Reconciliation uses an independent access path; not re-running the same transform  |
| G012 | HIGH   | Confirm grain alignment, period alignment, and filter parity before comparing totals|
| G015 | MEDIUM | A net-zero variance triggers a mandatory segment-level breakdown before declaring clean|
