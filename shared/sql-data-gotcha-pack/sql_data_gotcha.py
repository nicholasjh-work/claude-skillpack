"""
sql_data_gotcha.py
------------------
Machine-readable enforcement API for the sql-data-gotcha-pack.

Mirrors the interface of resume_banned.py so CI tooling can treat
both packs uniformly.

Public API
----------
    flag_gotchas(text: str, skill: str | None = None) -> list[GotchaHit]
    load_rules(skill: str | None = None) -> list[GotchaRule]
    GOTCHA_VERSION: str

Usage
-----
    from sql_data_gotcha import flag_gotchas, GotchaHit

    hits = flag_gotchas("SELECT * FROM orders", skill="sql-report-builder")
    for h in hits:
        print(h.id, h.severity, h.rule)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

GOTCHA_VERSION = "1.0.0"
_RULES_PATH = Path(__file__).parent / "gotchas.json"


class Severity(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass(frozen=True)
class GotchaRule:
    id: str
    rule: str
    category: str
    severity: Severity
    skills: list[str]
    failure_pattern: str
    failure_pattern_type: str
    rationale: str
    bad_example: str
    good_example: str
    test_trigger: str

    @classmethod
    def from_dict(cls, d: dict) -> "GotchaRule":
        return cls(
            id=d["id"],
            rule=d["rule"],
            category=d["category"],
            severity=Severity(d["severity"]),
            skills=d["skills"],
            failure_pattern=d["failure_pattern"],
            failure_pattern_type=d["failure_pattern_type"],
            rationale=d["rationale"],
            bad_example=d["bad_example"],
            good_example=d["good_example"],
            test_trigger=d["test_trigger"],
        )


@dataclass
class GotchaHit:
    id: str
    rule: str
    severity: Severity
    rationale: str
    good_example: str
    matched_text: Optional[str] = None


def _load_all_rules() -> list[GotchaRule]:
    raw = json.loads(_RULES_PATH.read_text(encoding="utf-8"))
    return [GotchaRule.from_dict(r) for r in raw]


def load_rules(skill: Optional[str] = None) -> list[GotchaRule]:
    """Return all rules, optionally filtered to a specific skill."""
    rules = _load_all_rules()
    if skill:
        rules = [r for r in rules if skill in r.skills]
    return rules


def flag_gotchas(text: str, skill: Optional[str] = None) -> list[GotchaHit]:
    """
    Scan text for regex-detectable gotcha violations.

    Only rules with failure_pattern_type == 'regex' or
    'regex_flag_only' are evaluated here. Behavioral rules
    require LLM-side enforcement (they are injected into the
    SKILL.md enforcement block, not checked by this function).

    Parameters
    ----------
    text:
        The SQL string or document to scan.
    skill:
        Optional skill name to limit rule scope.

    Returns
    -------
    list[GotchaHit]
        One entry per matched rule (not per match occurrence).
    """
    rules = load_rules(skill)
    hits: list[GotchaHit] = []

    for rule in rules:
        if rule.failure_pattern_type not in ("regex", "regex_flag_only"):
            continue
        try:
            match = re.search(rule.failure_pattern, text, re.IGNORECASE)
        except re.error:
            continue
        if match:
            hits.append(
                GotchaHit(
                    id=rule.id,
                    rule=rule.rule,
                    severity=rule.severity,
                    rationale=rule.rationale,
                    good_example=rule.good_example,
                    matched_text=match.group(0),
                )
            )
    return hits


def flag_report(text: str, skill: Optional[str] = None) -> dict:
    """
    Return a structured report dict, parallel to the resume-banned API.

    {
        "skill": str | None,
        "hits": [ {id, rule, severity, rationale, matched_text} ],
        "high_count": int,
        "medium_count": int,
        "low_count": int,
        "pass": bool   # True only if zero HIGH hits
    }
    """
    hits = flag_gotchas(text, skill)
    return {
        "skill": skill,
        "hits": [
            {
                "id": h.id,
                "rule": h.rule,
                "severity": h.severity.value,
                "rationale": h.rationale,
                "matched_text": h.matched_text,
            }
            for h in hits
        ],
        "high_count": sum(1 for h in hits if h.severity == Severity.HIGH),
        "medium_count": sum(1 for h in hits if h.severity == Severity.MEDIUM),
        "low_count": sum(1 for h in hits if h.severity == Severity.LOW),
        "pass": all(h.severity != Severity.HIGH for h in hits),
    }
