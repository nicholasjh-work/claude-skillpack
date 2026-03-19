---
name: python-reconciliation-engine
description: Compare two datasets by key, isolate missing rows and field-level differences, and summarize reconciliation exceptions clearly.
version: "1.0.0"
---

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
