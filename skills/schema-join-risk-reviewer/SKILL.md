---
name: schema-join-risk-reviewer
description: Review SQL or report logic for many-to-many joins, duplicate-grain risk, unsafe aggregation, and filter side effects.
version: "1.0.0"
---

# Purpose
Review data logic before it breaks reporting.

## Check for
- unclear base grain
- one-to-many or many-to-many joins
- double counting risk
- filter placement issues
- late aggregation
- unsafe distinct usage
- date-table mismatches
- left join versus inner join consequences

## Output format
1. Primary risks
2. Why each risk matters
3. Safer rewrite guidance
4. Residual assumptions
