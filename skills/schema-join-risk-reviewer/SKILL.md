---
name: schema-join-risk-reviewer
description: Review SQL or report logic for many-to-many joins, duplicate-grain risk, unsafe aggregation, and filter side effects.
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

## Gotcha Enforcement

Every review must explicitly check each rule below. Call out violations by
ID in the Major risks found section with the appropriate severity label.

| ID   | Sev    | Check                                                                           |
|------|--------|---------------------------------------------------------------------------------|
| G001 | HIGH   | Flag any `SELECT *` in the reviewed SQL                                         |
| G002 | HIGH   | Each join must have a cardinality classification; unknown = flag as HIGH risk   |
| G003 | HIGH   | Every aggregation column must document NULL treatment                           |
| G004 | HIGH   | Flag WHERE filters on right-side columns after LEFT JOINs                       |
| G005 | HIGH   | Flag dimension joins missing active/current row filter                          |
| G006 | HIGH   | Flag any SELECT that mixes measures from different grains                       |
| G010 | MEDIUM | Flag any join whose cardinality was assumed, not verified                       |
| G011 | MEDIUM | Flag DISTINCT usage that suppresses rather than prevents duplication            |
