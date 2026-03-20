---
name: python-data-investigator
description: Use Python to profile exports, find data quality issues, inspect bad records, and summarize findings in plain language.
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
Use Python for disciplined file and extract investigation.

## Workflow
1. Load the file safely.
2. Inspect schema, types, row counts, and date coverage.
3. Profile nulls, duplicates, distinct counts, outliers, and suspicious categories.
4. Trace exceptions back to specific records.
5. Summarize findings in business language.

## Preferred libraries
- pandas
- openpyxl when Excel handling matters
- pathlib
- re
- datetime

## Output format
1. What was inspected
2. Key findings
3. Python script
4. Recommended next checks

## Gotcha Enforcement

Apply these rules when writing profiling and investigation code.
A HIGH violation in generated code must be corrected. MEDIUM violations
must appear in the findings summary with an explanation.

| ID   | Sev    | Check                                                                              |
|------|--------|------------------------------------------------------------------------------------|
| G003 | HIGH   | Every mean/sum/aggregation documents its NA/NaN behavior (skipna, fillna, or note) |
| G009 | MEDIUM | Null rate check is mandatory for every measure column, not optional                |
| G012 | HIGH   | Before comparing two datasets, confirm they share the same grain, period, and filters |
