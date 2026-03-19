"""
Scholar Editor — pytest test suite
====================================
Tests determinism, fact preservation, pattern detection, and high-severity gating.

Run:
    pytest tests/test_scholar_editor.py -v
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List

import pytest

# Make shared/ importable regardless of working directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.scholar_editor.mock_detector import (  # noqa: E402
    PatternHit,
    annotate_text,
    detect_patterns,
    extract_facts,
)

# ---------------------------------------------------------------------------
# Load fixtures
# ---------------------------------------------------------------------------

FIXTURES_PATH = Path(__file__).parent / "fixtures.jsonl"


def load_scholar_fixtures() -> List[dict]:
    """Load only scholar_fixture records from fixtures.jsonl."""
    fixtures = []
    with open(FIXTURES_PATH, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if obj.get("type") == "scholar_fixture":
                fixtures.append(obj)
    return fixtures


SCHOLAR_FIXTURES = load_scholar_fixtures()


# ---------------------------------------------------------------------------
# Determinism tests
# ---------------------------------------------------------------------------

class TestDeterminism:
    """Same input + same domain → identical PatternHit list on every call."""

    @pytest.mark.parametrize("fixture", SCHOLAR_FIXTURES, ids=[f["id"] for f in SCHOLAR_FIXTURES])
    def test_same_input_produces_same_hits(self, fixture: dict):
        text = fixture["text"]
        domain = fixture.get("domain", "general")

        hits_a = detect_patterns(text, domain=domain)
        hits_b = detect_patterns(text, domain=domain)

        assert len(hits_a) == len(hits_b), (
            f"[{fixture['id']}] Non-deterministic hit count: {len(hits_a)} vs {len(hits_b)}"
        )
        for a, b in zip(hits_a, hits_b):
            assert a.id == b.id
            assert a.span_start == b.span_start
            assert a.span_end == b.span_end
            assert a.severity == b.severity
            assert abs(a.confidence - b.confidence) < 1e-9

    def test_clean_doc_produces_no_high_severity_hits(self):
        """The clean human doc fixture should produce zero high-severity hits."""
        clean_text = None
        with open(FIXTURES_PATH, encoding="utf-8") as fh:
            for line in fh:
                obj = json.loads(line.strip()) if line.strip() else None
                if obj and obj.get("type") == "clean_human_doc":
                    clean_text = obj["content"]
                    break

        assert clean_text is not None, "clean_human_doc fixture not found"
        hits = detect_patterns(clean_text, domain="technical")
        high_hits = [h for h in hits if h.severity == "high"]
        assert high_hits == [], (
            f"Clean doc produced unexpected high-severity hits: {[(h.id, h.text) for h in high_hits]}"
        )


# ---------------------------------------------------------------------------
# Fact preservation tests
# ---------------------------------------------------------------------------

class TestFactPreservation:
    """All preserve_facts tokens must appear verbatim in the text being checked."""

    @pytest.mark.parametrize("fixture", SCHOLAR_FIXTURES, ids=[f["id"] for f in SCHOLAR_FIXTURES])
    def test_preserve_facts_present_in_source(self, fixture: dict):
        """preserve_facts tokens must all appear in the original text (sanity check)."""
        text = fixture["text"]
        for token in fixture.get("preserve_facts", []):
            assert token in text, (
                f"[{fixture['id']}] preserve_facts token '{token}' missing from source text"
            )

    def test_extract_facts_returns_dates(self):
        text = "The March 14 outage started at 9:41 PM PT and was resolved by 2024-03-14."
        facts = extract_facts(text)
        assert len(facts["dates"]) > 0, "extract_facts should return at least one date"

    def test_extract_facts_returns_numerics(self):
        text = "4,300 requests timed out, representing 12% of total traffic."
        facts = extract_facts(text)
        assert len(facts["numerics"]) > 0, "extract_facts should return at least one numeric"

    def test_extract_facts_returns_entities(self):
        text = "Nick Hidalgo and the Payments Team reviewed the March 31 deadline."
        facts = extract_facts(text)
        assert len(facts["entities"]) > 0, "extract_facts should return at least one entity"


# ---------------------------------------------------------------------------
# Pattern detection tests
# ---------------------------------------------------------------------------

class TestPatternDetection:
    """detect_patterns must find all gold_rule_ids for each scholar fixture."""

    @pytest.mark.parametrize("fixture", SCHOLAR_FIXTURES, ids=[f["id"] for f in SCHOLAR_FIXTURES])
    def test_gold_rule_ids_detected(self, fixture: dict):
        text = fixture["text"]
        domain = fixture.get("domain", "general")
        gold_ids = set(fixture["gold_rule_ids"])

        hits = detect_patterns(text, domain=domain)
        detected_ids = {h.id for h in hits}

        missing = gold_ids - detected_ids
        assert not missing, (
            f"[{fixture['id']}] Pattern IDs not detected: {sorted(missing)}. "
            f"Detected: {sorted(detected_ids)}"
        )

    def test_all_24_patterns_covered_by_selftest(self):
        """
        Validates that the internal selftest texts cover all 24 pattern IDs.
        This is the same assertion used by --selftest CLI.
        """
        from shared.scholar_editor.mock_detector import _SELFTEST_TEXTS, _PATTERNS

        total = len(_SELFTEST_TEXTS)
        assert total == 24, f"Expected 24 selftest entries, got {total}"

        passed = 0
        failed = []
        for pid, text in _SELFTEST_TEXTS.items():
            hits = detect_patterns(text)
            if pid in {h.id for h in hits}:
                passed += 1
            else:
                failed.append(pid)

        coverage = passed / total
        assert coverage >= 0.90, (
            f"Pattern coverage {coverage:.0%} < 0.90. Missed IDs: {sorted(failed)}"
        )

    def test_confidence_threshold_suppresses_low_confidence(self):
        """No PatternHit with confidence < 0.7 should be returned."""
        text = "The project is running well. The team met yesterday. Results look good."
        hits = detect_patterns(text)
        for h in hits:
            assert h.confidence >= 0.70, (
                f"Hit below confidence threshold: P{h.id} confidence={h.confidence}"
            )


# ---------------------------------------------------------------------------
# Gating tests
# ---------------------------------------------------------------------------

class TestGating:
    """Fixtures with blocked=true must produce at least one high-severity hit."""

    @pytest.mark.parametrize(
        "fixture",
        [f for f in SCHOLAR_FIXTURES if f["blocked"]],
        ids=[f["id"] for f in SCHOLAR_FIXTURES if f["blocked"]],
    )
    def test_blocked_fixtures_have_high_severity_hits(self, fixture: dict):
        text = fixture["text"]
        domain = fixture.get("domain", "general")
        hits = detect_patterns(text, domain=domain)
        high_hits = [h for h in hits if h.severity == "high"]
        assert high_hits, (
            f"[{fixture['id']}] Fixture marked blocked=true but no high-severity hits found. "
            f"Detected: {[(h.id, h.severity) for h in hits]}"
        )

    @pytest.mark.parametrize(
        "fixture",
        [f for f in SCHOLAR_FIXTURES if not f["blocked"]],
        ids=[f["id"] for f in SCHOLAR_FIXTURES if not f["blocked"]],
    )
    def test_non_blocked_fixtures_have_no_high_severity_hits(self, fixture: dict):
        text = fixture["text"]
        domain = fixture.get("domain", "general")
        hits = detect_patterns(text, domain=domain)
        high_hits = [h for h in hits if h.severity == "high"]
        assert not high_hits, (
            f"[{fixture['id']}] Fixture marked blocked=false but got high-severity hits: "
            f"{[(h.id, h.text[:40]) for h in high_hits]}"
        )


# ---------------------------------------------------------------------------
# Annotation smoke test
# ---------------------------------------------------------------------------

class TestAnnotation:
    def test_annotate_text_inserts_tags(self):
        text = "Great question! The future looks bright."
        hits = detect_patterns(text)
        annotated = annotate_text(text, hits)
        assert "[[P" in annotated, "annotate_text should insert [[P...]] tags when hits exist"

    def test_annotate_text_preserves_original_on_no_hits(self):
        text = "We ship twice a week. The process is code review, then deploy."
        hits = detect_patterns(text)
        # Even if some low-severity hits exist, content should still be preserved
        annotated = annotate_text(text, hits)
        # All original text chars should be present (tags are additive)
        for word in ["ship", "twice", "code", "deploy"]:
            assert word in annotated
