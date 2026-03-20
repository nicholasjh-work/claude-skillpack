---
name: sql-data-gotcha-pack
description: "Machine-readable gotcha rules for SQL and data engineering failure patterns. Loaded by data and SQL skills to enforce Never-do-X constraints grounded in real reporting failures."
version: "1.0.0"
---

# SQL and Data Gotcha Pack

This is a shared rule library. It is not a standalone skill. Data and SQL skills
load it to enforce a common set of Never-do-X constraints.

## How it works

Every rule in this pack has:
- A unique ID (G001 through G015)
- A severity: HIGH, MEDIUM, or LOW
- A machine-readable failure pattern used by CI
- A rationale grounded in a real reporting failure class
- A bad and good example
- A skill scope list (which skills enforce which rules)

Rules with `failure_pattern_type: regex` or `regex_flag_only` are caught
automatically by `sql_data_gotcha.flag_gotchas(text, skill)`.

Rules with `failure_pattern_type: behavioral` are injected as enforcement
instructions into the dependent skill's SKILL.md and enforced by the LLM
at generation time.

## Rule Index

| ID   | Severity | Rule summary                                                       | Skills                                   |
|------|----------|--------------------------------------------------------------------|------------------------------------------|
| G001 | HIGH     | Never SELECT *                                                     | sql-report-builder, schema-join-risk-reviewer, data-integrity-investigator |
| G002 | HIGH     | Never aggregate before confirming join cardinality                 | sql-report-builder, schema-join-risk-reviewer, data-integrity-investigator, python-report-validation |
| G003 | HIGH     | Never treat NULL as zero in aggregations                           | all 6 data+SQL skills, kpi-definition-governance |
| G004 | HIGH     | Never let LEFT JOIN be silently converted to INNER JOIN            | sql-report-builder, schema-join-risk-reviewer, data-integrity-investigator |
| G005 | HIGH     | Never join SCD dimension without current/active filter             | sql-report-builder, schema-join-risk-reviewer, data-integrity-investigator |
| G006 | HIGH     | Never mix grains in the same aggregation without documenting it    | sql-report-builder, schema-join-risk-reviewer, kpi-definition-governance, requirements-to-report-spec |
| G007 | HIGH     | Never validate using the same logic as the report under test       | sql-report-builder, data-integrity-investigator, python-reconciliation-engine, python-report-validation |
| G008 | HIGH     | Never define a KPI without inclusion and exclusion criteria        | kpi-definition-governance, requirements-to-report-spec |
| G009 | MEDIUM   | Never report on a column without checking its null rate first      | python-data-investigator, data-integrity-investigator, python-report-validation, requirements-to-report-spec |
| G010 | MEDIUM   | Never infer join type from column name; verify cardinality         | schema-join-risk-reviewer, data-integrity-investigator, sql-report-builder |
| G011 | MEDIUM   | Never let DISTINCT mask a duplicate without investigating the source | sql-report-builder, schema-join-risk-reviewer, data-integrity-investigator |
| G012 | HIGH     | Never reconcile datasets without confirming shared grain+period     | python-reconciliation-engine, data-integrity-investigator, python-report-validation |
| G013 | LOW      | Never write a report spec without a sort tie-break rule            | requirements-to-report-spec, kpi-definition-governance |
| G014 | HIGH     | Never validate a report by row count only                          | python-report-validation, data-integrity-investigator |
| G015 | MEDIUM   | Never treat net-zero reconciliation as proof of correctness        | python-reconciliation-engine, data-integrity-investigator |

## Enforcement model

### For LLM skills
Dependent skills include this block in their Runtime Configuration:

```yaml
gotcha_pack: "sql-data-gotcha-pack"
gotcha_pack_version: "1.0.0"
gotcha_enforcement: "block_on_high"
```

And a Gotcha Enforcement section that lists the applicable rule IDs and
instructs Claude to check each before finalizing output.

### For CI
```python
from shared.sql_data_gotcha_pack.sql_data_gotcha import flag_report

result = flag_report(generated_sql, skill="sql-report-builder")
assert result["pass"], f"HIGH gotcha violations: {result['hits']}"
```

## Adding rules

1. Add an entry to `gotchas.json` with the next sequential ID.
2. Add the skill to the `skills` list of each affected rule.
3. Add the rule ID to the `Gotcha Enforcement` block in each affected SKILL.md.
4. Add a test case to `tests/shared/test_sql_data_gotcha_pack.py`.
5. Run `python tools/check_gotcha_coverage.py` to verify all skills are covered.
