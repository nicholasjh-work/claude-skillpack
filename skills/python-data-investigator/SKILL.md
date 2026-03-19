---
name: python-data-investigator
description: Use Python to profile exports, find data quality issues, inspect bad records, and summarize findings in plain language.
version: "1.0.0"
---

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
