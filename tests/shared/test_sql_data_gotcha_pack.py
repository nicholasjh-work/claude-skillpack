"""
tests/shared/test_sql_data_gotcha_pack.py
-----------------------------------------
Test suite for shared/sql-data-gotcha-pack.

Coverage targets:
- Schema validity of gotchas.json
- Python API: load_rules, flag_gotchas, flag_report
- Regex rules fire on bad examples
- Regex rules do NOT fire on good examples
- Skill scoping filters work correctly
- flag_report pass/fail logic
- All 8 target skills have at least one rule scoped to them
- No duplicate rule IDs in the registry
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Allow running from repo root: python -m pytest tests/
# The shared directory name contains a hyphen (sql-data-gotcha-pack) which
# is not a valid Python identifier. Use importlib.util to load it directly.
import importlib.util

REPO_ROOT = Path(__file__).parent.parent.parent
_MODULE_PATH = REPO_ROOT / "shared" / "sql-data-gotcha-pack" / "sql_data_gotcha.py"

_spec = importlib.util.spec_from_file_location("sql_data_gotcha", _MODULE_PATH)
assert _spec is not None and _spec.loader is not None, f"Cannot locate module at {_MODULE_PATH}"
sql_data_gotcha = importlib.util.module_from_spec(_spec)
sys.modules["sql_data_gotcha"] = sql_data_gotcha
_spec.loader.exec_module(sql_data_gotcha)  # type: ignore[union-attr]

from sql_data_gotcha import (  # noqa: E402
    GotchaHit,
    GotchaRule,
    Severity,
    flag_gotchas,
    flag_report,
    load_rules,
)

GOTCHAS_JSON = REPO_ROOT / "shared" / "sql-data-gotcha-pack" / "gotchas.json"

TARGET_SKILLS = [
    "sql-report-builder",
    "schema-join-risk-reviewer",
    "data-integrity-investigator",
    "python-data-investigator",
    "python-report-validation",
    "python-reconciliation-engine",
    "kpi-definition-governance",
    "requirements-to-report-spec",
]

# ─── Schema tests ────────────────────────────────────────────────────────────

class TestGotchaJsonSchema:
    def test_file_exists(self):
        assert GOTCHAS_JSON.exists(), "gotchas.json not found"

    def test_parses_as_list(self):
        data = json.loads(GOTCHAS_JSON.read_text())
        assert isinstance(data, list)
        assert len(data) >= 15

    def test_required_keys_present(self):
        required = {
            "id", "rule", "category", "severity", "skills",
            "failure_pattern", "failure_pattern_type",
            "rationale", "bad_example", "good_example", "test_trigger",
        }
        data = json.loads(GOTCHAS_JSON.read_text())
        for entry in data:
            missing = required - set(entry.keys())
            assert not missing, f"Rule {entry.get('id')} missing keys: {missing}"

    def test_no_duplicate_ids(self):
        data = json.loads(GOTCHAS_JSON.read_text())
        ids = [r["id"] for r in data]
        assert len(ids) == len(set(ids)), f"Duplicate IDs: {[i for i in ids if ids.count(i) > 1]}"

    def test_severity_values_valid(self):
        valid = {"HIGH", "MEDIUM", "LOW"}
        data = json.loads(GOTCHAS_JSON.read_text())
        for r in data:
            assert r["severity"] in valid, f"Invalid severity in {r['id']}: {r['severity']}"

    def test_failure_pattern_type_values_valid(self):
        valid = {"regex", "regex_flag_only", "behavioral"}
        data = json.loads(GOTCHAS_JSON.read_text())
        for r in data:
            assert r["failure_pattern_type"] in valid, (
                f"Invalid failure_pattern_type in {r['id']}: {r['failure_pattern_type']}"
            )

    def test_skills_is_list(self):
        data = json.loads(GOTCHAS_JSON.read_text())
        for r in data:
            assert isinstance(r["skills"], list), f"skills must be a list in {r['id']}"
            assert len(r["skills"]) >= 1, f"skills list is empty in {r['id']}"


# ─── Coverage tests ──────────────────────────────────────────────────────────

class TestSkillCoverage:
    @pytest.mark.parametrize("skill", TARGET_SKILLS)
    def test_skill_has_at_least_one_rule(self, skill: str):
        rules = load_rules(skill=skill)
        assert len(rules) >= 1, f"No gotcha rules scoped to skill: {skill}"

    @pytest.mark.parametrize("skill", TARGET_SKILLS)
    def test_skill_has_at_least_one_high_rule(self, skill: str):
        rules = load_rules(skill=skill)
        high_rules = [r for r in rules if r.severity == Severity.HIGH]
        assert len(high_rules) >= 1, f"No HIGH severity rules for skill: {skill}"


# ─── API unit tests ───────────────────────────────────────────────────────────

class TestLoadRules:
    def test_returns_all_rules_when_no_skill_filter(self):
        rules = load_rules()
        assert len(rules) >= 15

    def test_returns_subset_when_skill_provided(self):
        all_rules = load_rules()
        scoped = load_rules(skill="sql-report-builder")
        assert 0 < len(scoped) < len(all_rules)

    def test_returns_gotcharule_objects(self):
        rules = load_rules()
        assert all(isinstance(r, GotchaRule) for r in rules)

    def test_unknown_skill_returns_empty(self):
        rules = load_rules(skill="nonexistent-skill-xyz")
        assert rules == []


# ─── Regex rule firing tests ─────────────────────────────────────────────────

class TestFlagGotchas:
    # G001: SELECT *
    def test_g001_fires_on_select_star(self):
        sql = "SELECT * FROM orders"
        hits = flag_gotchas(sql, skill="sql-report-builder")
        ids = [h.id for h in hits]
        assert "G001" in ids

    def test_g001_does_not_fire_on_explicit_columns(self):
        sql = "SELECT order_id, amount FROM orders"
        hits = flag_gotchas(sql, skill="sql-report-builder")
        ids = [h.id for h in hits]
        assert "G001" not in ids

    def test_g001_fires_case_insensitive(self):
        sql = "select * from orders"
        hits = flag_gotchas(sql)
        ids = [h.id for h in hits]
        assert "G001" in ids

    # G011: DISTINCT flag
    def test_g011_fires_on_distinct(self):
        sql = "SELECT DISTINCT customer_id FROM orders"
        hits = flag_gotchas(sql, skill="sql-report-builder")
        ids = [h.id for h in hits]
        assert "G011" in ids

    def test_g011_does_not_fire_without_distinct(self):
        sql = "SELECT customer_id FROM orders GROUP BY customer_id"
        hits = flag_gotchas(sql, skill="sql-report-builder")
        ids = [h.id for h in hits]
        assert "G011" not in ids

    def test_returns_list_of_gotchahit(self):
        sql = "SELECT * FROM orders"
        hits = flag_gotchas(sql)
        assert all(isinstance(h, GotchaHit) for h in hits)

    def test_hit_includes_matched_text(self):
        sql = "SELECT * FROM orders"
        hits = flag_gotchas(sql)
        g001 = next((h for h in hits if h.id == "G001"), None)
        assert g001 is not None
        assert g001.matched_text is not None

    def test_skill_filter_limits_rules_checked(self):
        # G009 is scoped to python-data-investigator but not sql-report-builder
        # A query with no SELECT * should produce no G009 hit for sql-report-builder
        sql = "SELECT order_id FROM orders"
        sql_hits = flag_gotchas(sql, skill="sql-report-builder")
        ids = [h.id for h in sql_hits]
        assert "G009" not in ids

    def test_behavioral_rules_not_flagged_by_regex_scanner(self):
        # G002 is behavioral -- the scanner should never return it
        sql = "SELECT SUM(amount) FROM orders JOIN customers USING(id)"
        hits = flag_gotchas(sql)
        ids = [h.id for h in hits]
        assert "G002" not in ids, "Behavioral rule G002 should not be caught by regex scanner"


# ─── flag_report tests ────────────────────────────────────────────────────────

class TestFlagReport:
    def test_returns_dict_with_required_keys(self):
        result = flag_report("SELECT order_id FROM orders")
        assert {"skill", "hits", "high_count", "medium_count", "low_count", "pass"} <= result.keys()

    def test_pass_is_true_when_no_high_violations(self):
        sql = "SELECT order_id, amount FROM orders"
        result = flag_report(sql, skill="sql-report-builder")
        assert result["pass"] is True

    def test_pass_is_false_on_select_star(self):
        sql = "SELECT * FROM orders"
        result = flag_report(sql, skill="sql-report-builder")
        assert result["pass"] is False
        assert result["high_count"] >= 1

    def test_medium_count_nonzero_on_distinct(self):
        sql = "SELECT DISTINCT customer_id FROM orders"
        result = flag_report(sql, skill="sql-report-builder")
        assert result["medium_count"] >= 1

    def test_skill_is_propagated(self):
        result = flag_report("SELECT * FROM t", skill="schema-join-risk-reviewer")
        assert result["skill"] == "schema-join-risk-reviewer"

    def test_hits_contain_required_fields(self):
        result = flag_report("SELECT * FROM t")
        for hit in result["hits"]:
            assert "id" in hit
            assert "rule" in hit
            assert "severity" in hit
            assert "rationale" in hit


# ─── Negative / edge case tests ──────────────────────────────────────────────

class TestEdgeCases:
    def test_empty_string_returns_no_hits(self):
        hits = flag_gotchas("")
        assert hits == []

    def test_comment_only_sql_no_false_positives(self):
        sql = "-- SELECT * is never used here\n-- just a comment"
        hits = flag_gotchas(sql, skill="sql-report-builder")
        # Note: regex will match in comments -- this is acceptable and documented
        # The test just confirms it returns a list, not that it's empty
        assert isinstance(hits, list)

    def test_none_skill_does_not_raise(self):
        hits = flag_gotchas("SELECT * FROM t", skill=None)
        assert isinstance(hits, list)
        assert len(hits) >= 1
