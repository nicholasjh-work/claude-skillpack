# ai-pattern-scrubber - Component Specification

**Version:** 1.0.0
**Source:** [`blader/humanizer`](https://github.com/blader/humanizer) SKILL.md v2.2.0
**Basis:** Wikipedia "Signs of AI Writing" - WikiProject AI Cleanup

---

## 1. Overview

`ai-pattern-scrubber` is a deterministic, heuristic-driven Python library that scans text for the 24 canonical AI-writing patterns defined in the Humanizer skill. It returns structured, span-level annotations so downstream rewrite components can surgically replace only the flagged regions.

It does **not** rewrite text. Rewriting is the responsibility of `humanizer-flow`.

---

## 2. API Specification

### 2.1 `detect_patterns(text: str) -> list[PatternHit]`

Scans `text` for all 24 patterns. Returns every hit found, sorted by `span_start`.

```python
def detect_patterns(text: str) -> list[PatternHit]:
    """
    Scan text for all 24 Humanizer AI-writing patterns.

    Args:
        text: Raw input string (plain text or lightly marked-up markdown).
              No preprocessing is applied; pass pre-cleaned text if needed.
              Recommended max length: 8,000 tokens (~32,000 chars). For
              longer documents, chunk before calling.

    Returns:
        List of PatternHit objects, sorted by span_start ascending.
        Returns empty list if no patterns are detected.

    Raises:
        ValueError: If text is None or not a string.
        TextTooLongError: If text exceeds MAX_CHARS (configurable, default 100_000).
    """
```

### 2.2 `annotate_text(text: str) -> AnnotatedDocument`

Wraps `detect_patterns` and returns both the original text and all hits bundled in an `AnnotatedDocument`, plus aggregate statistics.

```python
def annotate_text(text: str) -> AnnotatedDocument:
    """
    Detect all patterns and return a fully annotated document object.

    Args:
        text: Same contract as detect_patterns().

    Returns:
        AnnotatedDocument with fields:
          - original_text: str          - the unmodified input
          - hits: list[PatternHit]      - all pattern hits, sorted by span_start
          - pattern_counts: dict[int, int] - hit count per pattern id (1-24)
          - severity_summary: dict[str, int] - counts per severity level
          - coverage: float             - fraction of chars inside at least one hit span
          - has_hits: bool              - True if any hits found

    Raises:
        ValueError, TextTooLongError (same as detect_patterns).
    """
```

---

## 3. Output Schema

### 3.1 `PatternHit` (dataclass)

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class PatternHit:
    id: int                              # Pattern number 1-24
    label: str                           # Human-readable pattern name
    span_start: int                      # Inclusive char offset into original text
    span_end: int                        # Exclusive char offset into original text
    severity: Literal["low", "med", "high"]
    confidence: float                    # 0.0-1.0; lexical matches = 1.0,
                                         # heuristic/contextual = 0.5-0.9
    rationale: str                       # One-sentence explanation of why it triggered
    matched_text: str                    # text[span_start:span_end]
    category: str                        # "CONTENT" | "LANGUAGE" | "STYLE" |
                                         # "COMMUNICATION" | "FILLER"
```

### 3.2 JSON Serialisation Example

```json
{
  "id": 7,
  "label": "Overused AI Vocabulary Words",
  "span_start": 142,
  "span_end": 159,
  "severity": "med",
  "confidence": 0.95,
  "rationale": "High-frequency AI word 'delve' detected in isolation.",
  "matched_text": "delve into the data",
  "category": "LANGUAGE"
}
```

### 3.3 Severity Calibration

| Severity | Definition |
|---|---|
| `high` | Nearly always indicates AI authorship; rarely appears in human writing (patterns 1, 4, 7, 8, 13, 19, 21, 24) |
| `med` | Common in AI output; also found in weak human writing (patterns 2, 3, 5, 6, 9, 10, 14, 15, 16, 22, 23) |
| `low` | Stylistic tells; legitimate in some contexts (patterns 11, 12, 17, 18, 20) |

---

## 4. Detection Heuristics (Patterns 1-24)

For each pattern: **category, severity, detection rule, positive example** (should trigger), **negative example** (should NOT trigger).

---

### CONTENT PATTERNS

---

#### Pattern 1 - Undue Emphasis on Significance, Legacy, and Broader Trends

- **Severity:** `high`
- **Rule:** Regex match on `\b(stands? as|serves? as|marks? a pivotal|testament to|underscores? (the|its)|highlights? (the|its) (importance|significance)|shaping the|reflects? broader|setting the stage|indelible mark|deeply rooted|focal point|enduring legacy)\b` (case-insensitive)
- **Confidence:** 1.0 for multi-word trigger phrases; 0.75 for single-word triggers in isolation
- **Positive (triggers):** `"This initiative marks a pivotal moment in the evolution of regional governance."`
- **Negative (does not trigger):** `"The 1989 statute gave the institute legal standing to publish its own figures."`

---

#### Pattern 2 - Undue Emphasis on Notability and Media Coverage

- **Severity:** `med`
- **Rule:** Regex `\b(featured in|covered by|as reported by|cited in|independent coverage|active social media presence|over \d[\d,]+ followers|written by a leading expert)\b` combined with a list of outlet names (`New York Times|BBC|Wired|Forbes|The Verge` etc.)
- **Confidence:** 0.9 when outlet name + notability phrase co-occur within 60 chars; 0.6 for outlet name alone
- **Positive:** `"Her work has been featured in The New York Times and maintains an active social media presence with 500,000 followers."`
- **Negative:** `"A 2024 New York Times profile quoted her arguing for outcome-based AI regulation."`

---

#### Pattern 3 - Superficial Analyses with -ing Endings

- **Severity:** `med`
- **Rule:** Regex `,\s*(highlighting|underscoring|emphasizing|showcasing|symbolizing|reflecting|cultivating|fostering|encompassing|contributing to)\b` - a trailing participial clause tacked onto a complete sentence (comma + -ing verb)
- **Confidence:** 0.85; reduce to 0.6 if the -ing phrase contains a concrete measurable claim
- **Positive:** `"The temple uses blue and gold colors, symbolizing the region's deep connection to the land."`
- **Negative:** `"The temple uses blue and gold colors. The architect cited local bluebonnets as the reference."`

---

#### Pattern 4 - Promotional and Advertisement-like Language

- **Severity:** `high`
- **Rule:** Lexical match against banned adjective list: `\b(boasts?|vibrant|nestled|breathtaking|stunning|must-visit|groundbreaking|renowned|nestled in the heart of|rich (cultural )?heritage|profound (impact|effect))\b`
- **Confidence:** 1.0 for `nestled in the heart of`; 0.8 for single adj; 0.95 for 2+ adjectives co-occurring in same sentence
- **Positive:** `"Nestled within the breathtaking region of Gonder, the town boasts a vibrant cultural heritage."`
- **Negative:** `"Gonder is a city in northern Ethiopia, roughly 700 km north of Addis Ababa."`

---

#### Pattern 5 - Vague Attributions and Weasel Words

- **Severity:** `med`
- **Rule:** Regex `\b(experts? (say|argue|believe|suggest)|industry (reports?|observers?)|some (critics?|sources?|experts?)|observers? have (noted|cited)|it (is|has been) (widely|generally) (believed|noted|argued))\b`
- **Confidence:** 0.9; reduce to 0.6 if a footnote or citation marker follows within 30 chars
- **Positive:** `"Experts believe the river plays a crucial role in the regional ecosystem."`
- **Negative:** `"According to a 2019 Chinese Academy of Sciences survey, the river supports twelve endemic fish species."`

---

#### Pattern 6 - Outline-like "Challenges and Future Prospects" Sections

- **Severity:** `med`
- **Rule:** Heading/section detection: regex on `(?i)^#+\s*(challenges?|future (prospects?|outlook)|despite (its|these) (challenges?|limitations?))`; OR within body text: `despite (its|these) \w+,? \w+ faces? (several )?(challenges?|issues?)` followed within 200 chars by `despite these challenges`
- **Confidence:** 1.0 for heading match; 0.85 for body text boilerplate pair
- **Positive:** `"Despite its industrial success, the city faces several challenges. Despite these challenges, growth continues."`
- **Negative:** `"Traffic congestion worsened after three IT parks opened in 2015; the municipality started a drainage project in 2022."`

---

### LANGUAGE AND GRAMMAR PATTERNS

---

#### Pattern 7 - Overused "AI Vocabulary" Words

- **Severity:** `high`
- **Rule:** Count occurrences of a curated 22-word list: `{additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight, interplay, intricate, intricacies, key, landscape, pivotal, showcase, tapestry, testament, underscore, valuable, vibrant}`. Trigger if **3 or more** distinct list words appear in 200-char window; OR if `delve` or `tapestry` (abstract noun sense) appears anywhere.
- **Confidence:** 1.0 for `delve`/`tapestry`; 0.85 for 3+ co-occurrences; 0.5 for 1-2 occurrences
- **Positive:** `"Additionally, the enduring testament to Italian influence showcases how crucial the interplay between landscape and tapestry remains."`
- **Negative:** `"Somali cuisine includes camel meat. Pasta arrived during Italian colonization and is still common in the south."`

---

#### Pattern 8 - Avoidance of "is"/"are" (Copula Avoidance)

- **Severity:** `high`
- **Rule:** Regex `\b(serves? as (a|an|the)|stands? as (a|an|the)|marks? (a|an|the)|represents? (a|an|the)|boasts? (a|an|the)|features? (a|an|the)|offers? (a|an|the))\b` where the following noun phrase would be grammatically replaceable by `is/are/has`
- **Confidence:** 0.9
- **Positive:** `"Gallery 825 serves as LAAA's exhibition space and boasts over 3,000 square feet."`
- **Negative:** `"Gallery 825 is LAAA's exhibition space; it has four rooms totalling 3,000 square feet."`

---

#### Pattern 9 - Negative Parallelisms

- **Severity:** `med`
- **Rule:** Regex `\b(not (only|just|merely).{0,60}(but (also)?|it['']?s)\b|it['']?s not (just|only|merely) about.{0,80}it['']?s (about)?)\b`
- **Confidence:** 0.95
- **Positive:** `"It's not just about the beat; it's part of the overall aggression and atmosphere."`
- **Negative:** `"The heavy beat intensifies the aggressive tone."`

---

#### Pattern 10 - Rule of Three Overuse

- **Severity:** `med`
- **Rule:** Count noun phrases in a list: regex `(\w[\w\s]*,\s*\w[\w\s]*,\s*and \w[\w\s]*)` within a single sentence. Trigger if 2 or more such triadic lists appear in a 300-char window, or if the same sentence ends in `X, Y, and Z` where X/Y/Z are clearly abstract/parallel.
- **Confidence:** 0.8 for double-triad; 0.6 for single triad with abstract nouns
- **Positive:** `"The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights."`
- **Negative:** `"The conference has talks, panels, and a dinner - plus time to visit the vendor floor."`

---

#### Pattern 11 - Elegant Variation (Synonym Cycling)

- **Severity:** `low`
- **Rule:** Within a 300-char window, detect 3+ distinct referring expressions for the same entity (noun phrase + synonyms). Heuristic: POS-tag sequence `DET? ADJ* NOUN` that changes label but maintains referential identity. Practical trigger: sequence `protagonist...main character...central figure...hero` (configurable synonym groups loaded from config.yaml).
- **Confidence:** 0.75 (heuristic); 0.95 when synonym group is explicitly matched
- **Positive:** `"The protagonist faces many challenges. The main character must overcome obstacles. The central figure triumphs. The hero returns."`
- **Negative:** `"The protagonist faces challenges but triumphs and returns home."`

---

#### Pattern 12 - False Ranges

- **Severity:** `low`
- **Rule:** Regex `from .{3,40} to .{3,40}, from .{3,40} to .{3,40}` (compound from-to-from-to structure). Also single: `from (the)? \w+ (of|in) .{5,50} to (the)? \w+ (of|in)` where operands are not on a numeric or temporal scale.
- **Confidence:** 0.9 for compound; 0.65 for single non-numeric `from...to`
- **Positive:** `"Our journey has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth of stars to the dance of dark matter."`
- **Negative:** `"Marathon times range from under two hours for elites to over six hours for recreational runners."`

---

### STYLE PATTERNS

---

#### Pattern 13 - Em Dash Overuse

- **Severity:** `high`
- **Rule:** Count `-` (U+2014) occurrences. Trigger if count > 2 per 300-char window, or if em dash appears more than once in a single sentence.
- **Confidence:** 1.0
- **Positive:** `"The term is promoted by Dutch institutions-not by the people themselves-yet this mislabeling continues-even in official documents."`
- **Negative:** `"The term is promoted by Dutch institutions, not by the people themselves, and it continues in official documents."`

---

#### Pattern 14 - Overuse of Boldface

- **Severity:** `med`
- **Rule:** Regex `\*\*[^*]{2,60}\*\*` - count markdown bold spans. Trigger if > 3 bold spans in 300-char window, or if consecutive sentences both contain bold spans.
- **Confidence:** 1.0
- **Positive:** `"It blends **OKRs**, **KPIs**, and **Balanced Scorecard (BSC)** into **a unified framework**."`
- **Negative:** `"It blends OKRs, KPIs, and the Balanced Scorecard into a unified framework."`

---

#### Pattern 15 - Inline-Header Vertical Lists

- **Severity:** `med`
- **Rule:** Regex on list items: `^[-*]\s+\*\*[A-Z][^*]{2,50}:\*\*` (markdown bullet + bold title + colon). Trigger on 2+ consecutive such items.
- **Confidence:** 1.0 for 3+ items; 0.8 for 2 items
- **Positive (multiline):**
  ```
  - **User Experience:** The UX has been improved.
  - **Performance:** Speed has been enhanced.
  - **Security:** End-to-end encryption added.
  ```
- **Negative:** `"The update improves the interface, speeds up load times, and adds end-to-end encryption."`

---

#### Pattern 16 - Title Case in Headings

- **Severity:** `med`
- **Rule:** Regex `^#{1,6}\s+([A-Z][a-z]+ ){2,}[A-Z]` - markdown heading where 3+ consecutive words are title-cased. Exclude known proper nouns by comparing against a proper-noun allowlist.
- **Confidence:** 0.9
- **Positive:** `"## Strategic Negotiations And Global Partnerships\n"`
- **Negative:** `"## Strategic negotiations and global partnerships\n"`

---

#### Pattern 17 - Emojis

- **Severity:** `low`
- **Rule:** Unicode emoji regex `[\U0001F300-\U0001FFFF\u2600-\u27BF]` matched in heading lines (`^#+`) or at list-item start (`^[-*]\s*[\U0001F300-\U0001FFFF]`)
- **Confidence:** 1.0 in headings; 0.9 in list bullets; 0.3 in body prose (allowed in informal writing)
- **Positive:** `"🚀 **Launch Phase:** The product launches in Q3"`
- **Negative:** `"The product launches in Q3. We're excited (we even added a confetti animation 🎉)."`

---

#### Pattern 18 - Curly Quotation Marks

- **Severity:** `low`
- **Rule:** Regex `[\u201C\u201D\u2018\u2019]` - detect Unicode curly/smart quotes
- **Confidence:** 1.0
- **Positive:** `'He said \u201cthe project is on track\u201d but others disagreed.'`
- **Negative:** `'He said "the project is on track" but others disagreed.'`

---

### COMMUNICATION PATTERNS

---

#### Pattern 19 - Collaborative Communication Artifacts

- **Severity:** `high`
- **Rule:** Regex `\b(I hope (this|that) helps|let me know if you('d| would) like|here is (a|an|the|your)|of course!|certainly!|feel free to|would you like me to|is there anything else)\b` (case-insensitive)
- **Confidence:** 1.0
- **Positive:** `"Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand."`
- **Negative:** `"The French Revolution began in 1789 when financial crises and food shortages sparked widespread unrest."`

---

#### Pattern 20 - Knowledge-Cutoff Disclaimers

- **Severity:** `low`
- **Rule:** Regex `\b(as of (my )?(last |knowledge )?(update|cutoff|training)|up to my (last )?training|based on available information|while specific details (are|remain) (limited|scarce)|it (appears?|seems?) to have been)\b` (case-insensitive)
- **Confidence:** 1.0
- **Positive:** `"While specific details are limited based on available information, the company appears to have been founded in the 1990s."`
- **Negative:** `"The company was founded in 1994, according to its registration documents."`

---

#### Pattern 21 - Sycophantic/Servile Tone

- **Severity:** `high`
- **Rule:** Regex `\b(great question!|excellent (point|question)|you('re| are) absolutely right|that('s| is) (an )?excellent|good point!|what a (great|thoughtful))\b` (case-insensitive)
- **Confidence:** 1.0
- **Positive:** `"Great question! You're absolutely right that this is a complex topic."`
- **Negative:** `"The economic factors you mentioned are relevant here."`

---

### FILLER AND HEDGING PATTERNS

---

#### Pattern 22 - Filler Phrases

- **Severity:** `med`
- **Rule:** Exact phrase match against filler list (case-insensitive):
  - `in order to` (-> "to")
  - `due to the fact that` (-> "because")
  - `at this point in time` (-> "now")
  - `in the event that` (-> "if")
  - `has the ability to` (-> "can")
  - `it is important to note that`
  - `it should be noted that`
  - `needless to say`
  - `as a matter of fact`
  - `for all intents and purposes`
- **Confidence:** 1.0 for exact match
- **Positive:** `"In order to achieve this goal, it is important to note that due to the fact that resources are limited, planning is key."`
- **Negative:** `"To meet the goal, plan for limited resources."`

---

#### Pattern 23 - Excessive Hedging

- **Severity:** `med`
- **Rule:** Count stacked hedge modals/adverbs in a single clause. Trigger if 3+ hedge tokens from `{could, might, may, possibly, potentially, arguably, perhaps, likely, seemingly, apparently, somewhat}` appear within a 100-char window.
- **Confidence:** 1.0 for 3+ stacked; 0.6 for 2 stacked; 0.0 for single (not a trigger alone)
- **Positive:** `"It could potentially possibly be argued that the policy might have some effect."`
- **Negative:** `"The policy may affect outcomes."`

---

#### Pattern 24 - Generic Positive Conclusions

- **Severity:** `high`
- **Rule:** Regex targeting closing-paragraph clichés: `\b(the future (looks|is) bright|exciting times (lie|are) ahead|continue(s)? (this|our|the) journey (toward|towards)|(in )?(the )?right direction|we look forward to|a (major|significant) step forward|the possibilities are endless|sky['']?s the limit)\b` at or near end of document (last 20% of text length), or anywhere in isolation.
- **Confidence:** 0.95 in last 20% of doc; 0.8 elsewhere
- **Positive:** `"The future looks bright. Exciting times lie ahead as we continue this journey toward excellence."`
- **Negative:** `"The company plans to open two more locations next year and hire 40 engineers."`

---

## 5. Unit Tests (pytest)

```python
# tests/test_scrubber.py
"""
30 unit tests for ai-pattern-scrubber.
  - Tests 1-24: one targeted test per pattern (positive detection).
  - Tests 25-30: adversarial / negative cases (should NOT trigger).

Run: pytest tests/test_scrubber.py -v
"""

import pytest
from ai_pattern_scrubber import detect_patterns, annotate_text
from ai_pattern_scrubber.models import PatternHit


# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

def hits_for_pattern(text: str, pattern_id: int) -> list[PatternHit]:
    return [h for h in detect_patterns(text) if h.id == pattern_id]


def assert_no_hits(text: str, pattern_id: int):
    hits = hits_for_pattern(text, pattern_id)
    assert hits == [], (
        f"Expected no hits for pattern {pattern_id}, got: {hits}"
    )


# ──────────────────────────────────────────────
# PATTERN TESTS (1-24)
# ──────────────────────────────────────────────

class TestContentPatterns:

    def test_p01_significance_triggers(self):
        text = "This initiative marks a pivotal moment in the evolution of regional governance."
        hits = hits_for_pattern(text, 1)
        assert len(hits) >= 1
        assert hits[0].severity == "high"
        assert hits[0].span_start < hits[0].span_end

    def test_p02_notability_triggers(self):
        text = (
            "Her work has been featured in The New York Times and she maintains "
            "an active social media presence with over 500,000 followers."
        )
        hits = hits_for_pattern(text, 2)
        assert len(hits) >= 1
        assert hits[0].confidence >= 0.8

    def test_p03_ing_ending_triggers(self):
        text = "The temple uses blue and gold, symbolizing the region's deep connection to the land."
        hits = hits_for_pattern(text, 3)
        assert len(hits) >= 1
        assert "symbolizing" in hits[0].matched_text

    def test_p04_promotional_language_triggers(self):
        text = "Nestled within the breathtaking region, the town boasts a vibrant cultural heritage."
        hits = hits_for_pattern(text, 4)
        assert len(hits) >= 1
        assert hits[0].severity == "high"

    def test_p05_weasel_words_triggers(self):
        text = "Experts believe the river plays a crucial role in the regional ecosystem."
        hits = hits_for_pattern(text, 5)
        assert len(hits) >= 1

    def test_p06_challenges_section_triggers(self):
        text = (
            "Despite its industrial success, the city faces several challenges. "
            "Despite these challenges, with its strategic location, Korattur continues to thrive."
        )
        hits = hits_for_pattern(text, 6)
        assert len(hits) >= 1
        assert hits[0].severity == "med"

    def test_p07_ai_vocab_triggers(self):
        text = (
            "Additionally, the enduring testament to Italian influence showcases "
            "how crucial the interplay between landscape and tapestry remains."
        )
        hits = hits_for_pattern(text, 7)
        assert len(hits) >= 1
        assert hits[0].severity == "high"

    def test_p08_copula_avoidance_triggers(self):
        text = "Gallery 825 serves as LAAA's exhibition space and boasts over 3,000 square feet."
        hits = hits_for_pattern(text, 8)
        assert len(hits) >= 1
        assert hits[0].severity == "high"

    def test_p09_negative_parallelisms_triggers(self):
        text = "It's not just about the beat; it's part of the aggression and atmosphere."
        hits = hits_for_pattern(text, 9)
        assert len(hits) >= 1

    def test_p10_rule_of_three_triggers(self):
        text = (
            "The event features keynote sessions, panel discussions, and networking opportunities. "
            "Attendees can expect innovation, inspiration, and industry insights."
        )
        hits = hits_for_pattern(text, 10)
        assert len(hits) >= 1

    def test_p11_synonym_cycling_triggers(self):
        text = (
            "The protagonist faces many challenges. The main character must overcome obstacles. "
            "The central figure eventually triumphs. The hero returns home."
        )
        hits = hits_for_pattern(text, 11)
        assert len(hits) >= 1
        assert hits[0].category == "LANGUAGE"

    def test_p12_false_ranges_triggers(self):
        text = (
            "Our journey has taken us from the singularity of the Big Bang to the grand cosmic web, "
            "from the birth and death of stars to the enigmatic dance of dark matter."
        )
        hits = hits_for_pattern(text, 12)
        assert len(hits) >= 1

    def test_p13_em_dash_overuse_triggers(self):
        text = (
            "The term is promoted by Dutch institutions\u2014not by the people themselves\u2014"
            "yet this mislabeling continues\u2014even in official documents."
        )
        hits = hits_for_pattern(text, 13)
        assert len(hits) >= 1
        assert hits[0].severity == "high"

    def test_p14_boldface_overuse_triggers(self):
        text = "It blends **OKRs**, **KPIs**, **BMC**, and **BSC** into **a single framework**."
        hits = hits_for_pattern(text, 14)
        assert len(hits) >= 1

    def test_p15_inline_header_lists_triggers(self):
        text = (
            "- **User Experience:** UX improved with a new interface.\n"
            "- **Performance:** Speed enhanced via optimized algorithms.\n"
            "- **Security:** End-to-end encryption added.\n"
        )
        hits = hits_for_pattern(text, 15)
        assert len(hits) >= 1

    def test_p16_title_case_headings_triggers(self):
        text = "## Strategic Negotiations And Global Partnerships\n"
        hits = hits_for_pattern(text, 16)
        assert len(hits) >= 1

    def test_p17_emojis_in_heading_triggers(self):
        text = "🚀 **Launch Phase:** The product launches in Q3.\n"
        hits = hits_for_pattern(text, 17)
        assert len(hits) >= 1

    def test_p18_curly_quotes_triggers(self):
        text = "He said \u201cthe project is on track\u201d but others disagreed."
        hits = hits_for_pattern(text, 18)
        assert len(hits) >= 1
        assert hits[0].confidence == 1.0

    def test_p19_collaborative_artifacts_triggers(self):
        text = "Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like more."
        hits = hits_for_pattern(text, 19)
        assert len(hits) >= 1
        assert hits[0].severity == "high"

    def test_p20_knowledge_cutoff_triggers(self):
        text = (
            "While specific details are limited based on available information, "
            "the company appears to have been founded in the 1990s."
        )
        hits = hits_for_pattern(text, 20)
        assert len(hits) >= 1

    def test_p21_sycophantic_tone_triggers(self):
        text = "Great question! You're absolutely right that this is a complex topic."
        hits = hits_for_pattern(text, 21)
        assert len(hits) >= 1
        assert hits[0].severity == "high"

    def test_p22_filler_phrases_triggers(self):
        text = "In order to achieve this, it is important to note that due to the fact that planning matters."
        hits = hits_for_pattern(text, 22)
        assert len(hits) >= 2  # Multiple fillers present

    def test_p23_excessive_hedging_triggers(self):
        text = "It could potentially possibly be argued that the policy might have some effect."
        hits = hits_for_pattern(text, 23)
        assert len(hits) >= 1
        assert hits[0].confidence == 1.0

    def test_p24_generic_positive_conclusion_triggers(self):
        text = "The future looks bright. Exciting times lie ahead as we continue this journey toward excellence."
        hits = hits_for_pattern(text, 24)
        assert len(hits) >= 1
        assert hits[0].severity == "high"


# ──────────────────────────────────────────────
# ADVERSARIAL / NEGATIVE TESTS (25-30)
# ──────────────────────────────────────────────

class TestAdversarialCases:

    def test_adv_25_specific_citation_not_weasel(self):
        """Verified citation should NOT trigger pattern 5 (weasel words)."""
        text = "A 2019 Chinese Academy of Sciences survey found twelve endemic fish species in the Haolai River."
        assert_no_hits(text, 5)

    def test_adv_26_legitimate_em_dash(self):
        """A single em dash used correctly should NOT trigger pattern 13."""
        text = "The result\u2014a 40% reduction in latency\u2014justified the refactor."
        assert_no_hits(text, 13)

    def test_adv_27_human_first_person_opinion(self):
        """First-person opinion prose should NOT trigger pattern 21 (sycophancy)."""
        text = "I genuinely don't know how to feel about this. The numbers are impressive but something feels off."
        assert_no_hits(text, 21)

    def test_adv_28_technical_range_not_false_range(self):
        """A numeric range should NOT trigger pattern 12 (false ranges)."""
        text = "Marathon finishing times range from 1:59 for elite runners to over 6:00 for recreational participants."
        assert_no_hits(text, 12)

    def test_adv_29_legitimate_hedge_single(self):
        """A single hedge word should NOT trigger pattern 23 (excessive hedging)."""
        text = "The policy may affect pricing in regulated markets."
        assert_no_hits(text, 23)

    def test_adv_30_outcome_sentence_not_generic_conclusion(self):
        """A concrete factual closing should NOT trigger pattern 24."""
        text = "The company plans to open two additional locations next year and hire 40 engineers."
        assert_no_hits(text, 24)


# ──────────────────────────────────────────────
# ANNOTATE_TEXT CONTRACT TESTS
# ──────────────────────────────────────────────

class TestAnnotateTextContract:

    def test_annotate_returns_annotated_document(self):
        text = "Great question! The future looks bright as we continue this journey toward excellence."
        doc = annotate_text(text)
        assert doc.original_text == text
        assert isinstance(doc.hits, list)
        assert doc.has_hits is True

    def test_annotate_coverage_calculation(self):
        """coverage should be > 0 when hits are found."""
        text = "Nestled in the heart of the city, the venue boasts a vibrant cultural heritage."
        doc = annotate_text(text)
        assert 0 < doc.coverage <= 1.0

    def test_annotate_empty_input(self):
        doc = annotate_text("No AI patterns here. Short sentence. Done.")
        assert isinstance(doc.hits, list)

    def test_annotate_span_bounds_within_text(self):
        text = "It could potentially possibly be argued this serves as a pivotal moment."
        doc = annotate_text(text)
        for hit in doc.hits:
            assert 0 <= hit.span_start < hit.span_end <= len(text)
            assert hit.matched_text == text[hit.span_start:hit.span_end]
```

---

## 6. Integration Test - Pipeline Coverage Assertion

```python
# tests/test_integration_pipeline.py
"""
Integration test: run detect_patterns on a 300-word AI-heavy document.
Assert pattern coverage >= 0.9 (at least 21 of 24 patterns detected).
"""

import pytest
from ai_pattern_scrubber import detect_patterns, annotate_text

# 300-word synthetic document deliberately containing all 24 patterns.
SYNTHETIC_AI_DOC = """
Great question! Here is an overview of AI coding tools. I hope this helps!

AI-assisted coding serves as an enduring testament to the transformative potential of large language
models, marking a pivotal moment in the evolution of software development. In today\u2019s rapidly
evolving technological landscape, these groundbreaking tools\u2014nestled at the intersection of
research and practice\u2014are reshaping how engineers ideate, iterate, and deliver, underscoring
their vital role in modern workflows.

The value proposition is clear: streamlining processes, enhancing collaboration, and fostering
alignment. It\u2019s not just about autocomplete; it\u2019s about unlocking creativity at scale.
The tool serves as a catalyst. The assistant functions as a partner. The system stands as a
foundation for innovation.

Industry observers have noted that adoption has accelerated from hobbyist experiments to
enterprise-wide rollouts. The technology has been featured in The New York Times, Wired, and
The Verge. Additionally, the ability to generate documentation, tests, and refactors showcases
how AI can contribute to better outcomes, highlighting the intricate interplay between automation
and human judgment.

- \U0001F680 **Speed:** Code generation is significantly faster, reducing friction.
- \U0001F4A1 **Quality:** Output quality has been enhanced through improved training.
- \u2705 **Adoption:** Usage continues to grow, reflecting broader industry trends.

While specific details are limited based on available information, it could potentially possibly
be argued that these tools might have some positive effect. In order to fully realize this
potential, teams must align with best practices. He said \u201cresults speak for themselves.\u201d

In conclusion, the future looks bright. Exciting times lie ahead as we continue this journey
toward excellence. Let me know if you\u2019d like me to expand on any section!
""".strip()


class TestIntegrationPipeline:

    def test_detect_patterns_returns_list(self):
        hits = detect_patterns(SYNTHETIC_AI_DOC)
        assert isinstance(hits, list)
        assert len(hits) > 0

    def test_pattern_coverage_gte_90_percent(self):
        """At least 21 of 24 patterns must be detected in the synthetic document."""
        hits = detect_patterns(SYNTHETIC_AI_DOC)
        detected_ids = {h.id for h in hits}
        coverage = len(detected_ids) / 24
        assert coverage >= 0.9, (
            f"Pattern coverage {coverage:.1%} < 90%. "
            f"Missing pattern IDs: {set(range(1, 25)) - detected_ids}"
        )

    def test_all_hits_have_valid_schema(self):
        """Every hit must conform to PatternHit field constraints."""
        hits = detect_patterns(SYNTHETIC_AI_DOC)
        for hit in hits:
            assert 1 <= hit.id <= 24
            assert isinstance(hit.label, str) and len(hit.label) > 0
            assert hit.span_start >= 0
            assert hit.span_end > hit.span_start
            assert hit.severity in ("low", "med", "high")
            assert 0.0 <= hit.confidence <= 1.0
            assert isinstance(hit.rationale, str) and len(hit.rationale) > 0
            assert hit.matched_text == SYNTHETIC_AI_DOC[hit.span_start:hit.span_end]
            assert hit.category in (
                "CONTENT", "LANGUAGE", "STYLE", "COMMUNICATION", "FILLER"
            )

    def test_hits_sorted_by_span_start(self):
        hits = detect_patterns(SYNTHETIC_AI_DOC)
        starts = [h.span_start for h in hits]
        assert starts == sorted(starts), "Hits must be sorted by span_start ascending"

    def test_annotate_coverage_metric(self):
        """annotate_text coverage should reflect majority of doc is flagged."""
        doc = annotate_text(SYNTHETIC_AI_DOC)
        # The synthetic doc is intentionally dense - expect > 30% char coverage
        assert doc.coverage > 0.30, (
            f"Expected >30% char coverage on dense AI doc, got {doc.coverage:.1%}"
        )

    def test_severity_distribution_contains_high(self):
        doc = annotate_text(SYNTHETIC_AI_DOC)
        assert doc.severity_summary.get("high", 0) >= 3, (
            "Synthetic doc should produce at least 3 high-severity hits"
        )
```

---

## 7. Configuration

```yaml
# ai_pattern_scrubber/config.yaml
max_chars: 100_000
default_chunk_size: 32_000

# Pattern-level sensitivity overrides (strict | balanced | lenient)
sensitivity: balanced

# Synonym groups for Pattern 11 (Elegant Variation)
synonym_groups:
  - [protagonist, main character, central figure, hero, the character]
  - [company, firm, organization, enterprise, institution]
  - [study, research, paper, report, findings, work]

# Outlet names for Pattern 2 (Notability)
media_outlets:
  - New York Times
  - BBC
  - Wired
  - Forbes
  - The Verge
  - Financial Times
  - The Guardian
  - Wall Street Journal

# AI vocabulary word list for Pattern 7
ai_vocabulary:
  - additionally
  - align with
  - crucial
  - delve
  - emphasizing
  - enduring
  - enhance
  - fostering
  - garner
  - highlight
  - interplay
  - intricate
  - intricacies
  - key
  - landscape
  - pivotal
  - showcase
  - tapestry
  - testament
  - underscore
  - valuable
  - vibrant

# Hedge tokens for Pattern 23 (Excessive Hedging)
hedge_tokens:
  - could
  - might
  - may
  - possibly
  - potentially
  - arguably
  - perhaps
  - likely
  - seemingly
  - apparently
  - somewhat
```

---

## 8. Error Types

```python
class TextTooLongError(ValueError):
    """Raised when input text exceeds MAX_CHARS."""

class PatternConfigError(RuntimeError):
    """Raised when config.yaml is missing or malformed."""
```

---

## 9. Non-Goals (Out of Scope for This Component)

- **Rewriting** - handled by `humanizer-flow` and `nick-mode-writing-standard`
- **LLM inference** - this component is fully deterministic; no API calls
- **Language detection** - English only; no i18n
- **Sentence tokenisation** - basic heuristics only; no full NLP pipeline dependency
- **Diff rendering** - handled by `humanizer-flow/diff_formatter.py`

---

## 10. Versioning

| Version | Change |
|---|---|
| 1.0.0 | Initial spec; all 24 patterns from humanizer v2.2.0 |

---

*Source of truth: [SKILL.md v2.2.0](https://github.com/blader/humanizer/blob/main/SKILL.md) - Wikipedia "Signs of AI Writing"*
