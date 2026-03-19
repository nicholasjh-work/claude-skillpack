"""
Scholar Editor — Mock Pattern Detector
=======================================
Deterministic Python 3.10 implementation of the 24 AI-writing pattern heuristics
defined in shared/scholar-editor/SPEC.md and rubric.json.

Conservative policy: confidence < 0.7 suppresses PatternHit.
No external dependencies beyond Python stdlib.

Usage:
    python mock_detector.py <file.txt>              # print JSON hits
    python mock_detector.py --selftest              # assert coverage >= 0.9

API:
    detect_patterns(text, domain="general") -> List[PatternHit]
    extract_facts(text) -> Dict
    annotate_text(text, hits) -> str
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from typing import Dict, List


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class PatternHit:
    id: int
    label: str
    span_start: int
    span_end: int
    text: str
    severity: str       # "low" | "med" | "high"
    confidence: float   # 0.0–1.0
    rationale: str


# ---------------------------------------------------------------------------
# Pattern catalogue  (id → (label, severity_default, compiled_cue, confidence_fn))
# ---------------------------------------------------------------------------

def _re(pattern: str, flags: int = 0) -> re.Pattern:
    return re.compile(pattern, flags | re.IGNORECASE)


_PATTERNS: list[dict] = [
    {
        "id": 1,
        "label": "Undue Emphasis on Significance, Legacy, and Broader Trends",
        "severity": "high",
        "regex": _re(
            r"\b(stands?\s+as|serves?\s+as|marks?\s+a\s+pivotal|testament\s+to"
            r"|underscores?\s+(the|its)|highlights?\s+(the|its)\s+(importance|significance)"
            r"|shaping\s+the|reflects?\s+broader|setting\s+the\s+stage"
            r"|indelible\s+mark|deeply\s+rooted|focal\s+point|enduring\s+legacy)\b"
        ),
        "confidence": 0.85,
        "rationale": "Significance-inflation phrasing; low token surprisal (MIT 2022).",
    },
    {
        "id": 2,
        "label": "Undue Emphasis on Notability and Media Coverage",
        "severity": "med",
        "regex": _re(
            r"\b(featured\s+in|covered\s+by|as\s+reported\s+by|cited\s+in"
            r"|independent\s+coverage|active\s+social\s+media\s+presence"
            r"|over\s+\d[\d,]+\s+followers|written\s+by\s+a\s+leading\s+expert)\b"
        ),
        "confidence": 0.80,
        "rationale": "Unverifiable notability claims; East Central faculty heuristic.",
    },
    {
        "id": 3,
        "label": "Superficial Analyses with -ing Endings",
        "severity": "med",
        "regex": _re(
            r",\s*(highlighting|underscoring|emphasizing|showcasing|symbolizing"
            r"|reflecting|cultivating|fostering|encompassing|contributing\s+to)\b"
        ),
        "confidence": 0.75,
        "rationale": "Trailing participial clauses substitute for analysis (Hunting the Muse).",
    },
    {
        "id": 4,
        "label": "Promotional and Advertisement-like Language",
        "severity": "high",
        "regex": _re(
            r"\b(boasts?|vibrant|nestled|breathtaking|stunning|must-visit"
            r"|groundbreaking|renowned|nestled\s+in\s+the\s+heart\s+of"
            r"|rich\s+(cultural\s+)?heritage|profound\s+(impact|effect))\b"
        ),
        "confidence": 0.88,
        "rationale": "Promotional adjectives; Hunting the Muse classroom heuristic.",
    },
    {
        "id": 5,
        "label": "Vague Attributions and Weasel Words",
        "severity": "med",
        "regex": _re(
            r"\b(experts?\s+(say|argue|believe|suggest)|industry\s+(reports?|observers?)"
            r"|some\s+(critics?|sources?|experts?)|observers?\s+have\s+(noted|cited)"
            r"|it\s+(is|has\s+been)\s+(widely|generally)\s+(believed|noted|argued))\b"
        ),
        "confidence": 0.80,
        "rationale": "Weasel-word attributions; GLTR low-surprisal proxy (ArXiv 1906.04043).",
    },
    {
        "id": 6,
        "label": "Outline-like Challenges and Future Prospects Sections",
        "severity": "med",
        "regex": _re(
            r"(despite\s+(its|these)\s+\w+,?\s+\w+\s+faces?\s+(several\s+)?"
            r"(challenges?|issues?)|despite\s+these\s+challenges)"
        ),
        "confidence": 0.78,
        "rationale": "Boilerplate 'challenges' section structure (East Central faculty resources).",
    },
    {
        "id": 7,
        "label": "Overused AI Vocabulary Words",
        "severity": "high",
        # Match any word from the canonical 22-word list
        "regex": _re(
            r"\b(additionally|align\s+with|crucial|delve|emphasizing|enduring|enhance"
            r"|fostering|garner|highlight|interplay|intricate|intricacies|key"
            r"|landscape|pivotal|showcase|tapestry|testament|underscore|valuable|vibrant)\b"
        ),
        "confidence": 0.90,
        "rationale": "Top-22 AI vocabulary list; high density = low token surprisal (MIT 2022, ArXiv 1906.04043).",
        "density_check": True,   # requires 3+ in 200-char window for high; 1 for med
    },
    {
        "id": 8,
        "label": "Avoidance of is/are (Copula Avoidance)",
        "severity": "high",
        "regex": _re(
            r"\b(serves?\s+as\s+(a|an|the)|stands?\s+as\s+(a|an|the)"
            r"|marks?\s+(a|an|the)|represents?\s+(a|an|the)"
            r"|boasts?\s+(a|an|the)|features?\s+(a|an|the)|offers?\s+(a|an|the))\b"
        ),
        "confidence": 0.85,
        "rationale": "Copula-avoidance constructions; GLTR low-surprisal proxy (ArXiv 1906.04043).",
    },
    {
        "id": 9,
        "label": "Negative Parallelisms",
        "severity": "med",
        "regex": _re(
            r"(not\s+(only|just|merely).{0,60}?(but(\s+also)?)\b"
            r"|it[\u2019']?s\s+not\s+(just|only|merely)\s+about.{0,80}?it[\u2019']?s\b"
            r"|it[\u2019']?s\s+not\s+(just|only|merely)\s+\w.{0,80}?it[\u2019']?s\s+part\s+of)",
            re.DOTALL,
        ),
        "confidence": 0.75,
        "rationale": "Formulaic negative-parallelism construction (Hunting the Muse).",
    },
    {
        "id": 10,
        "label": "Rule of Three Overuse",
        "severity": "med",
        "regex": _re(r"\b\w[\w\s]*,\s*\w[\w\s]*,\s*and\s+\w[\w\s]*\b"),
        "confidence": 0.72,
        "rationale": "Triadic lists preferred by AI generation (low entropy structure).",
    },
    {
        "id": 11,
        "label": "Elegant Variation (Synonym Cycling)",
        "severity": "low",
        "regex": _re(
            r"\b(protagonist|main\s+character|central\s+figure|the\s+hero|the\s+lead)\b"
        ),
        "confidence": 0.70,
        "rationale": "Synonym cycling for the same entity within short span (Hunting the Muse).",
    },
    {
        "id": 12,
        "label": "False Ranges",
        "severity": "low",
        "regex": _re(
            r"from\s+.{3,40}?\s+to\s+.{3,40}?,\s+from\s+.{3,40}?\s+to\s+.{3,40}"
        ),
        "confidence": 0.73,
        "rationale": "Compound from-to ranges across incommensurable domains (MIT 2022).",
    },
    {
        "id": 13,
        "label": "Em Dash Overuse",
        "severity": "high",
        "regex": _re(r"\u2014"),
        "confidence": 0.82,
        "rationale": "Em-dash overuse is a top practitioner signal (Hunting the Muse, East Central).",
    },
    {
        "id": 14,
        "label": "Overuse of Boldface",
        "severity": "med",
        "regex": _re(r"\*\*[^*]{2,60}\*\*"),
        "confidence": 0.78,
        "rationale": "Aggressive bolding to compensate for low information density (East Central).",
    },
    {
        "id": 15,
        "label": "Inline-Header Vertical Lists",
        "severity": "med",
        "regex": _re(r"^[-*]\s+\*\*[A-Z][^*]{2,50}:\*\*", re.MULTILINE),
        "confidence": 0.80,
        "rationale": "Inline-header bullet pattern signals LLM outline generation.",
    },
    {
        "id": 16,
        "label": "Title Case in Headings",
        "severity": "med",
        "regex": _re(r"^#{1,6}\s+([A-Z][a-z]+\s+){2,}[A-Z]", re.MULTILINE),
        "confidence": 0.75,
        "rationale": "LLMs default to title-case headings contrary to most style guides.",
    },
    {
        "id": 17,
        "label": "Emojis",
        "severity": "low",
        "regex": _re(
            r"[\U0001F300-\U0001F9FF\U00002702-\U000027B0\U0001FA00-\U0001FA6F]"
        ),
        "confidence": 0.70,
        "rationale": "Emoji in formal/technical prose signals AI decoration (East Central).",
    },
    {
        "id": 18,
        "label": "Curly Quotation Marks",
        "severity": "low",
        "regex": _re(r"[\u201C\u201D\u2018\u2019]"),
        "confidence": 0.70,
        "rationale": "Smart quotes from LLM output break code/markdown copy-paste fidelity.",
    },
    {
        "id": 19,
        "label": "Collaborative Communication Artifacts",
        "severity": "high",
        "regex": _re(
            r"\b(I\s+hope\s+(this|that)\s+helps|let\s+me\s+know\s+if\s+you('d|\s+would)\s+like"
            r"|here\s+is\s+(a|an|the|your)|of\s+course!|certainly!|feel\s+free\s+to"
            r"|would\s+you\s+like\s+me\s+to|is\s+there\s+anything\s+else)\b"
        ),
        "confidence": 0.95,
        "rationale": "Unambiguous chatbot communication artifacts (Hunting the Muse, East Central).",
    },
    {
        "id": 20,
        "label": "Knowledge-Cutoff Disclaimers",
        "severity": "low",
        "regex": _re(
            r"\b(as\s+of\s+(my\s+)?(last\s+|knowledge\s+)?(update|cutoff|training)"
            r"|up\s+to\s+my\s+(last\s+)?training|based\s+on\s+available\s+information"
            r"|while\s+specific\s+details\s+(are|remain)\s+(limited|scarce)"
            r"|it\s+(appears?|seems?)\s+to\s+have\s+been)\b"
        ),
        "confidence": 0.92,
        "rationale": "LLM-specific uncertainty disclaimers never appropriate in professional documents.",
    },
    {
        "id": 21,
        "label": "Sycophantic/Servile Tone",
        "severity": "high",
        "regex": _re(
            r"\b(great\s+question!|excellent\s+(point|question)"
            r"|you('re|\s+are)\s+absolutely\s+right"
            r"|that('s|\s+is)\s+(an\s+)?excellent|good\s+point!"
            r"|what\s+a\s+(great|thoughtful))\b"
        ),
        "confidence": 0.95,
        "rationale": "Sycophantic openers are near-universal chatbot artifacts (Hunting the Muse).",
    },
    {
        "id": 22,
        "label": "Filler Phrases",
        "severity": "med",
        "regex": _re(
            r"\b(in\s+order\s+to|due\s+to\s+the\s+fact\s+that|at\s+this\s+point\s+in\s+time"
            r"|in\s+the\s+event\s+that|has\s+the\s+ability\s+to"
            r"|it\s+is\s+important\s+to\s+note\s+that|it\s+should\s+be\s+noted\s+that"
            r"|needless\s+to\s+say|as\s+a\s+matter\s+of\s+fact"
            r"|for\s+all\s+intents\s+and\s+purposes)\b"
        ),
        "confidence": 0.88,
        "rationale": "Filler phrases cluster at high-probability token positions (MIT 2022, ArXiv 1906.04043).",
    },
    {
        "id": 23,
        "label": "Excessive Hedging",
        "severity": "med",
        "regex": _re(
            r"\b(could|might|may|possibly|potentially|arguably|perhaps"
            r"|likely|seemingly|apparently|somewhat)\b"
        ),
        "confidence": 0.72,
        "rationale": "Stacked hedges (3+ in 100 chars) signal AI over-qualification (MIT 2022).",
        "density_check": True,
    },
    {
        "id": 24,
        "label": "Generic Positive Conclusions",
        "severity": "high",
        "regex": _re(
            r"\b(the\s+future\s+(looks|is)\s+bright|exciting\s+times\s+(lie|are)\s+ahead"
            r"|continue(s)?\s+(this|our|the)\s+journey\s+(toward|towards)"
            r"|(in\s+)?(the\s+)?right\s+direction|we\s+look\s+forward\s+to"
            r"|a\s+(major|significant)\s+step\s+forward|the\s+possibilities\s+are\s+endless"
            r"|sky'?s\s+the\s+limit)\b"
        ),
        "confidence": 0.90,
        "rationale": "Generic positive conclusions are near-universal AI tell in document closings (Hunting the Muse).",
    },
]


# ---------------------------------------------------------------------------
# Core detection logic
# ---------------------------------------------------------------------------

_CONFIDENCE_THRESHOLD = 0.70
_DENSITY_WINDOW = 200  # characters
_HEDGE_WINDOW = 100


def _apply_density_check(p: dict, matches: list[re.Match], text: str) -> list[re.Match]:
    """For density-sensitive patterns, only emit hits when window threshold is met."""
    if not p.get("density_check"):
        return matches

    pid = p["id"]

    if pid == 7:
        # Require 3+ distinct AI-vocab words in any 200-char window
        qualifying = []
        for m in matches:
            window_start = max(0, m.start() - _DENSITY_WINDOW // 2)
            window_end = min(len(text), m.end() + _DENSITY_WINDOW // 2)
            window = text[window_start:window_end]
            vocab_in_window = set(p["regex"].findall(window))
            # Always flag delve/tapestry; others need density of 3+
            word = m.group(0).lower()
            if word in ("delve", "tapestry") or len(vocab_in_window) >= 3:
                qualifying.append(m)
        return qualifying

    if pid == 23:
        # Require 3+ hedge tokens in 100-char window
        qualifying = []
        hedge_re = _re(
            r"\b(could|might|may|possibly|potentially|arguably|perhaps"
            r"|likely|seemingly|apparently|somewhat)\b"
        )
        for m in matches:
            window_start = max(0, m.start() - _HEDGE_WINDOW // 2)
            window_end = min(len(text), m.end() + _HEDGE_WINDOW // 2)
            window = text[window_start:window_end]
            hedge_count = len(hedge_re.findall(window))
            if hedge_count >= 3:
                qualifying.append(m)
        return qualifying

    return matches


def detect_patterns(text: str, domain: str = "general") -> List[PatternHit]:
    """
    Detect AI writing patterns in text.

    Args:
        text: Input prose (UTF-8)
        domain: One of technical, academic, marketing, casual, general

    Returns:
        Sorted list of PatternHit objects (confidence >= 0.7 only)
    """
    if len(text) > 50_000:
        raise ValueError(f"TextTooLongError: {len(text)} > 50000 chars")

    hits: List[PatternHit] = []

    for p in _PATTERNS:
        raw_matches = list(p["regex"].finditer(text))
        matches = _apply_density_check(p, raw_matches, text)

        # Domain-based severity escalation
        severity = p["severity"]
        if domain in ("technical", "academic"):
            if p["id"] in (4, 16, 17):
                severity = "high"
        if domain == "academic" and p["id"] == 20:
            severity = "high"

        for m in matches:
            conf = p["confidence"]
            if conf < _CONFIDENCE_THRESHOLD:
                continue
            hits.append(
                PatternHit(
                    id=p["id"],
                    label=p["label"],
                    span_start=m.start(),
                    span_end=m.end(),
                    text=m.group(0),
                    severity=severity,
                    confidence=conf,
                    rationale=p["rationale"],
                )
            )

    hits.sort(key=lambda h: h.span_start)
    return hits


# ---------------------------------------------------------------------------
# Fact extraction
# ---------------------------------------------------------------------------

_DATE_RE = _re(
    r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
    r"|\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?"
    r"|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
    r"\s+\d{1,2},?\s+\d{4}"
    r"|\d{4}-\d{2}-\d{2}"
    r"|\bQ[1-4]\s+\d{4}\b)\b"
)

_NUMERIC_RE = _re(
    r"\b(\d[\d,]*(?:\.\d+)?(?:\s*%|\s*[kmb](?:illion)?)?)\b"
)

_ENTITY_RE = _re(
    r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4}|[A-Z]{2,})\b"
)


def extract_facts(text: str) -> Dict:
    """
    Extract named entities, dates, and numeric claims from text.

    Returns:
        {entities: [...], dates: [...], numerics: [...]}
    """
    entities = list(dict.fromkeys(m.group(0) for m in _ENTITY_RE.finditer(text)))
    dates = list(dict.fromkeys(m.group(0) for m in _DATE_RE.finditer(text)))
    numerics = list(dict.fromkeys(m.group(0) for m in _NUMERIC_RE.finditer(text)))
    return {"entities": entities, "dates": dates, "numerics": numerics}


# ---------------------------------------------------------------------------
# Annotation
# ---------------------------------------------------------------------------

def annotate_text(text: str, hits: List[PatternHit]) -> str:
    """
    Insert inline [[P{id}:{label}]] tags after each matched span.

    Returns:
        Annotated string (for debugging only — do not use in production output).
    """
    if not hits:
        return text

    result = []
    prev = 0
    for h in sorted(hits, key=lambda x: x.span_start):
        result.append(text[prev : h.span_start])
        result.append(text[h.span_start : h.span_end])
        result.append(f"[[P{h.id}:{h.label}]]")
        prev = h.span_end
    result.append(text[prev:])
    return "".join(result)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

_SELFTEST_TEXTS: dict[int, str] = {
    1: "This initiative marks a pivotal moment in the evolution of governance, serving as a testament to enduring legacy.",
    2: "Her work has been featured in The New York Times with an active social media presence of over 500,000 followers.",
    3: "The project launched on time, highlighting the team's efficiency and showcasing best practices.",
    4: "Nestled within the breathtaking region, the town boasts a vibrant cultural heritage.",
    5: "Experts believe the river plays a crucial role. Industry observers have noted significant changes.",
    6: "Despite its success, the city faces several challenges. Despite these challenges, growth continues.",
    7: "Additionally, the enduring testament to Italian influence showcases the crucial interplay of landscape and tapestry.",
    8: "Gallery 825 serves as LAAA's exhibition space and represents a major milestone.",
    9: "It's not just about the beat; it's part of the overall atmosphere.",
    10: "The event features innovation, inspiration, and industry insights. Attendees expect leadership, vision, and excellence.",
    11: "The protagonist faces obstacles. The central figure must overcome them. The hero prevails.",
    12: "From the singularity of the Big Bang to the cosmic web, from the birth of stars to the dance of dark matter.",
    13: "The term is promoted by institutions\u2014not the people\u2014yet mislabeling continues\u2014even officially.",
    14: "It blends **OKRs**, **KPIs**, and **Balanced Scorecard** into **a unified framework**.",
    15: "- **User Experience:** UX improved.\n- **Performance:** Speed enhanced.\n- **Security:** Hardened.",
    16: "## Strategic Negotiations And Global Partnerships\n\nContent here.",
    17: "🚀 Launch Phase: The product launches in Q3.",
    18: "\u201cHe said the project is on track\u201d but others disagreed.",
    19: "Here is an overview of the topic. I hope this helps! Let me know if you'd like more.",
    20: "While specific details are limited based on available information, it appears to have been founded in the 1990s.",
    21: "Great question! You're absolutely right that this is complex.",
    22: "In order to achieve this, it is important to note that due to the fact that resources are limited.",
    23: "It could potentially possibly be argued that the policy might perhaps have some effect.",
    24: "The future looks bright. Exciting times lie ahead as we continue this journey toward excellence.",
}


def _run_selftest() -> None:
    passed = 0
    failed_ids = []

    for pid, text in _SELFTEST_TEXTS.items():
        hits = detect_patterns(text)
        found_ids = {h.id for h in hits}
        if pid in found_ids:
            passed += 1
        else:
            failed_ids.append(pid)

    total = len(_SELFTEST_TEXTS)
    coverage = passed / total
    print(f"Coverage: {passed}/{total} patterns ({coverage:.0%})")

    if failed_ids:
        print(f"MISSED pattern IDs: {sorted(failed_ids)}")

    if coverage < 0.90:
        print("FAIL — coverage below 0.90 threshold")
        sys.exit(1)
    else:
        print("PASS")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _main() -> None:
    args = sys.argv[1:]

    if not args:
        print("Usage: python mock_detector.py <file.txt> | --selftest", file=sys.stderr)
        sys.exit(2)

    if args[0] == "--selftest":
        _run_selftest()
        return

    path = args[0]
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print(f"Error reading {path}: {exc}", file=sys.stderr)
        sys.exit(2)

    domain = args[1] if len(args) > 1 else "general"
    hits = detect_patterns(text, domain=domain)
    facts = extract_facts(text)

    output = {
        "hits": [asdict(h) for h in hits],
        "facts_locked": facts,
        "blocked": any(h.severity == "high" for h in hits),
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _main()
