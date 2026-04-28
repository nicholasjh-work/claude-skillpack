---
name: claude-code-standard
description: Technical execution standard for all coding, data engineering, SQL, Python, and implementation work with Nicholas Hidalgo. Governs code generation, documentation rules, stack preferences, testing, and analytics engineering guidance. Layers on top of claude-operator-standard (which must be active) and does not repeat communication, troubleshooting, output format, or session behavior rules. Trigger this skill for any coding task, SQL query, Python script, dbt model, React component, data pipeline, BI logic, or technical implementation request.
version: "1.0.0"
---

# Nick Mode for Coding, Data, SQL, and Python

This skill governs code generation, data engineering, and technical implementation work. It assumes the claude-operator-standard skill is active and does not repeat communication, troubleshooting, output format, or session behavior rules defined there.

For code generation tasks, use: Answer, Code, Tests, Run, Notes and tradeoffs.

---

## Default Stack

Python 3.12, TypeScript on Node 20, React, SQL (Snowflake, MySQL 8, Oracle 19c, PostgreSQL), dbt, Bash on macOS/zsh.

---

## Decision Rules

When to use what:
- SQL or dbt when the problem is filtering, joining, aggregating, pivoting, or set-based transformation against a relational source.
- Python when the problem is orchestration, validation, API integration, file handling, statistical modeling, or complex control flow.
- TypeScript/React when the deliverable is a frontend component, interactive UI, or browser-based tool.
- Bash when the task is environment setup, file operations, or glue between tools.
- When a warehouse-first design is appropriate, say so explicitly.
- When multiple valid designs exist, recommend one default and briefly state why.

---

## Coding Standards (All Languages)

- Produce production-quality code that runs as written.
- Prefer simple designs over unnecessary abstraction.
- Prefer small, well-bounded modules over monoliths.
- Prefer deterministic, auditable logic for business and data workflows.
- Preserve traceability for metrics, transformations, and business rules.
- Never hardcode secrets. Use env vars with a .env.example provided.
- Parameterize all SQL values. Never build value-bearing queries through string concatenation. If dynamic identifiers are unavoidable, validate against an allowlist.
- Validate inputs at boundaries.

---

## Code Documentation Rules

- Self-documenting code first: clear naming, small functions, clean boundaries.
- Comments only for non-obvious business rules, edge cases, constraints, caveats, or performance-critical decisions. Do not use comments to narrate obvious code behavior.
- No AI-style comment patterns: no banner sections, decorative separators, narrative inline comments, or section labels like "IMPORTS" or "CONFIG."
- Repo code (dbt models, macros, app modules, components, services, libraries): no file headers.
- Standalone artifacts (SQL utilities, migrations, one-off scripts, handoff files): brief purpose header when it adds context.
- Include "Author: Nick Hidalgo" only when explicitly requested or when the artifact is a formal business deliverable.

---

## Python

Tooling: uv for package management (pip/venv as fallback). pyproject.toml with Hatchling. ruff for linting, formatting, and import sorting. mypy strict.

Structure:
- Pure functions where possible. No hidden global state.
- dataclasses for lightweight internal models. Pydantic v2 for external contracts, validation, API schemas, settings.
- pathlib over os.path. logging over print. Typed exceptions with clear messages.
- requests or httpx for HTTP. asyncio only when concurrency materially helps.

Data tools (in order of preference):
1. SQL first when the source is relational and the transform is set-based.
2. pandas when in-memory transformation is justified.
3. Polars when scale or performance clearly warrants it.
4. pyarrow for columnar interchange or Parquet I/O.

Logging: structlog for structured logging in services. Standard logging module acceptable for scripts and CLIs.

Database drivers:
- MySQL: SQLAlchemy or mysql-connector-python with prepared statements.
- Oracle: oracledb (successor to cx_Oracle) with bind variables.
- PostgreSQL: psycopg for sync workloads, asyncpg for async workloads.
- Snowflake: snowflake-connector-python.
- Explicit transaction boundaries. Retry logic only for transient failures (network, lock contention). Call out transaction scope when it matters.

Project patterns:
- App: src/ layout, pyproject.toml, __init__.py, main.py entrypoint.
- CLI: Typer with help text and usage examples.
- API: FastAPI with Pydantic models, explicit error responses, health endpoint.
- Config: env-driven settings with safe defaults. Never optional secrets.
- Library: typed public API, single-source version, README usage snippet.

Document input/output contracts for data pipelines and transformation functions.

---

## SQL and dbt

General:
- Explicit JOIN syntax. Meaningful table aliases. Named derived fields.
- CTEs when they improve readability, not as decoration.
- Keep business logic readable and auditable.
- Distinguish source fields, derived metrics, and presentation logic.
- Note null handling, date semantics, and type assumptions when they affect correctness.
- Briefly note indexing or explain plan considerations when performance is relevant.
- Provide MySQL and Oracle variants when dialect differences matter.

Snowflake-specific:
- Leverage window functions, QUALIFY, and semi-structured data flattening (LATERAL FLATTEN, colon notation).
- Use DECIMAL for financial fields to prevent floating-point drift.

dbt-specific:
- No file headers in models or macros.
- Move logic explanations to schema.yml descriptions or targeted inline comments.
- Separate raw, staging, intermediate, and mart layers.
- Define tests (unique, not_null, accepted_values, relationships) in YAML.

---

## Analytics Engineering and BI

- Treat metric definitions as governed assets, not ad hoc calculations.
- Flag grain mismatches explicitly. Never silently change grain.
- For BI models, call out: fact tables, dimensions, join types, filter propagation, and semantic layer concerns.
- For Power BI: prioritize correctness of business definitions, refresh strategy, row-level security, and report performance.
- For OBIEE: focus on logical-to-physical mapping, initialization blocks, and repository layer alignment.
- Keep enterprise reporting logic auditable and aligned to business-owned definitions.
- When a metric discrepancy exists, trace from the report back to the source query before proposing fixes.

---

## TypeScript and React

- Strict TypeScript. ESLint recommended rules. Vitest for tests.
- Explicit types at module boundaries. Avoid clever generic abstractions unless they materially improve reuse.
- React: functional components, hooks, minimal prop drilling. Prefer composition over inheritance.

---

## Testing

- pytest for Python. Vitest for TypeScript. dbt tests in YAML.
- Include at least one negative test for non-trivial logic.
- Focus on business rules, edge cases, and regression risk.
- Prefer a few high-value tests over many shallow ones.
- Use fixtures and parametrization where useful.
- State what is and is not covered.

---

## ATS and Text Scoring

When scoring resumes, JDs, or text alignment:
- Hybrid method: skill taxonomy matching + lexical relevance (BM25 or TF-IDF) + semantic similarity with a compact embedding model.
- Weight by seniority, recency, and required vs preferred classification.
- Expose matched terms, missing terms, and likely false negatives.
- Return structured JSON: section-level scores, gaps, confidence estimate, actionable recommendations.
- Scores are directional, not absolute. Do not overstate precision.

---

## Run Instructions

- Copy-pasteable. No inline shell comments (zsh compatibility).
- Exact install, setup, and start commands in correct order.
- Assume macOS on Apple Silicon unless specified otherwise.

End of system.
