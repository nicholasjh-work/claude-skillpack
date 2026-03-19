# Scholar Editor - Implementation Notes & Acceptance Criteria
**Version:** 0.1.0

---

## Determinism

- All three passes (Draft, Audit, Final) must use `temperature=0.0`, `top_p=0.0`, and an explicit `seed`.
- The default seed is `SCHOLAR_SEED_001`; callers may override via the `seed` input field.
- `detect_patterns()` in `mock_detector.py` is purely deterministic (no randomness); it must return
  identical output for identical input on every call.
- CI enforces this via `tests/test_scholar_editor.py::TestDeterminism`.

## Fact-Lock Constraint

- Any string in `preserve_facts` must appear **verbatim** (exact substring match) in both `draft` and `final`.
- If any token is absent after Pass 1 (draft), set `blocked=true` and return without running Pass 2 or Pass 3.
- If any token is absent after Pass 3 (final), set `blocked=true` and discard the Pass 3 output.
- The fact-lock check is the **first** gate, evaluated before severity gating.

## Conservative Detector Policy

- `PatternHit` is only emitted when `confidence >= 0.70`.
- The detector prefers **false negatives over false positives**: it is better to miss a pattern than
  to flag a genuine human phrase as AI-generated.
- `confidence` is a fixed per-pattern value based on empirical precision of the detection cue.
  It is not dynamically calibrated in the current stub implementation.
- All confidence values are ≥ 0.70 by design; the threshold can be raised per-pattern in future versions.

## Severity Gating

- Pass 3 (Final) only runs when `blocked == false` after Pass 2.
- `blocked` is true if **any** `Issue.severity == "high"`.
- Pass 3 applies `suggested_fix` only for issues with `severity` in `{"med", "low"}`.
- High-severity issues are returned in `audit` for human review; they are never auto-fixed.

## CI Gates

| Gate | Tool | Failure condition |
|---|---|---|
| Pattern coverage | `mock_detector.py --selftest` | Coverage < 0.90 -> exit 1 |
| Fixture coverage | `tools/check_pattern_coverage.py` | Coverage < 0.90 -> exit 1 |
| Gating correctness | `pytest TestGating` | blocked fixture has no high hit -> fail |
| Determinism | `pytest TestDeterminism` | Hit lists differ across calls -> fail |
| Fact preservation | `pytest TestFactPreservation` | preserve_facts token absent -> fail |

All CI steps use `continue-on-error: false`. A single failure blocks the merge.

## Module Layout

```
shared/
  scholar-editor/
    rubric.json              # 24 pattern rules (authoritative source)
    SPEC.md                  # API spec + Expert Audit prompt
    mock_detector.py         # Deterministic Python 3.10 detector
    IMPLEMENTATION_NOTES.md  # This file

skills/
  scholar-editor/
    SKILL.md                 # Three-pass prompt flow + examples

tests/
  fixtures.jsonl             # 15 records (3 legacy + 12 scholar fixtures)
  test_scholar_editor.py     # pytest suite

evaluation/
  EVAL_PLAN.md               # Human evaluation rubric and protocol
```

## Known Limitations (v0.1.0)

- `mock_detector.py` uses regex/lexical cues only; it does not implement GLTR token-probability
  scoring (ArXiv 1906.04043). Statistical detection requires integration with a language model
  probability API (future work).
- Pattern 11 (Elegant Variation) uses a narrow synonym list; broader NER-based synonym detection
  is deferred to v0.2.0.
- Pattern 2 (Notability/Media Coverage) does not validate outlet names against a reference list;
  false negatives on obscure outlet names are expected.
- The `--selftest` CLI asserts ≥ 0.90 coverage on 24 hand-crafted sentences (one per pattern).
  Real-world coverage on mixed-domain text will vary.
