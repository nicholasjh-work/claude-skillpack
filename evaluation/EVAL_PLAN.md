# Scholar Editor — Human Evaluation Plan
**Version:** 0.1.0 | **Date:** 2026-03-18

---

## Overview

3 raters × 50 examples = 150 scored records.
Examples are drawn from 5 domains (10 per domain): technical, academic, marketing, casual, mixed.
Each example presents a *before* (source text) and *after* (scholar-editor final output) pair.
Raters score the *after* on four axes.

---

## Rater Profile

Raters must:
- Hold at least a BA/BS degree or equivalent professional writing experience
- Be fluent in English (native or near-native)
- Be unfamiliar with the scholarly AI-detection rubric (blind scoring)

---

## Four-Axis Rubric

### Axis 1: Accuracy / Factuality (0–3)

Measures whether all facts, names, dates, and numeric claims from the source are preserved verbatim
in the output.

| Score | Meaning |
|---|---|
| 3 | All facts from source appear verbatim; no new facts introduced |
| 2 | One minor rephrasing (e.g., "March 31st" → "March 31") but no semantic change |
| 1 | One fact altered, omitted, or a new unsupported claim added |
| 0 | Multiple facts altered or significant fabrication present |

**Anchor examples:**
- Score 3: Source says "4,300 requests." Output says "4,300 requests." ✓
- Score 1: Source says "99.97% uptime." Output says "99.9% uptime." ✗
- Score 0: Source has no revenue figure. Output says "generating $2M in Q1." ✗

**Acceptance threshold:** All preserve_facts examples must score 3. Any 0 or 1 is a blocking failure.

---

### Axis 2: Edit Effort (0–3)

Measures how much additional human editing the output still requires before it is publishable.

| Score | Meaning |
|---|---|
| 3 | Publishable as-is; no editing needed |
| 2 | Minor polish needed (one or two word choices) |
| 1 | Substantial editing needed (structural issues or multiple awkward phrases) |
| 0 | Needs a full rewrite |

**Anchor examples:**
- Score 3: Output reads naturally, no AI tells remain.
- Score 2: One sentence is slightly stiff but the rest is clean.
- Score 1: Three or more AI vocabulary words remain; structure is outline-like.
- Score 0: Chatbot opener retained; sycophantic tone throughout.

**Acceptance threshold:** Mean edit effort across all 50 examples ≤ 2.0.

---

### Axis 3: Rhetorical Fit (0–3)

Measures whether the output matches the stated intent, audience, and domain.

| Score | Meaning |
|---|---|
| 3 | Tone, formality, and structure perfectly match the stated context |
| 2 | Mostly appropriate; one element slightly off (e.g., slightly too formal) |
| 1 | Noticeable mismatch (e.g., casual language in a formal report) |
| 0 | Wrong register throughout; would confuse the intended audience |

**Anchor examples:**
- Score 3: Direct engineering email reads as direct; no filler.
- Score 2: Academic paper summary is slightly too casual in one sentence.
- Score 1: Marketing copy is formal and stiff when it should be energetic.
- Score 0: Post-mortem report written in first-person chatbot voice.

---

### Axis 4: Naturalness (0–3)

Measures whether the output sounds like a human professional wrote it, independent of factual accuracy.

| Score | Meaning |
|---|---|
| 3 | Indistinguishable from skilled human professional writing |
| 2 | Mostly natural; one construction feels machine-generated |
| 1 | Identifiable AI tells remain (e.g., one em dash, one AI vocab word) |
| 0 | Obviously AI-generated throughout |

**Anchor examples:**
- Score 3: Varied sentence lengths, plain verbs, no AI vocabulary.
- Score 2: One "it is worth noting" remains; rest is clean.
- Score 1: "The future looks bright" retained in closing paragraph.
- Score 0: "Nestled within the breathtaking landscape... the team boasts vibrant capabilities."

**Acceptance threshold:** Mean naturalness across all 50 examples ≥ 2.0.

---

## Instructions for Raters

### Setup

1. Download the scoring spreadsheet: `evaluation/scoring_template.csv`
2. Each row corresponds to one example (50 rows total for your rater ID)
3. Do not discuss scores with other raters until after all 50 are complete

### Scoring procedure

1. Read the **source text** column first (1–2 minutes)
2. Read the **output text** column (scholar-editor final)
3. Score each axis independently (do not let one axis influence another)
4. Write a brief note in the `notes` column (1–2 sentences) explaining any score below 2

### Disagreement protocol

- If two raters differ by ≥ 2 on any axis, a third rater provides a tiebreaker
- Do not adjust scores after seeing other raters' scores
- Flag any example where source text appears to have been fabricated (rare edge case)

---

## CSV Log Format

Save results to `evaluation/results/rater_{id}_results.csv` with these columns:

```csv
rater_id,example_id,domain,accuracy,edit_effort,rhetorical_fit,naturalness,notes
R1,EX001,technical,3,2,3,3,"One sentence slightly stiff but facts all correct"
R1,EX002,academic,3,3,3,2,"'it is worth noting' survives in paragraph 2"
```

Column definitions:

| Column | Type | Values |
|---|---|---|
| `rater_id` | string | R1, R2, R3 |
| `example_id` | string | EX001–EX050 |
| `domain` | string | technical, academic, marketing, casual, mixed |
| `accuracy` | int | 0–3 |
| `edit_effort` | int | 0–3 |
| `rhetorical_fit` | int | 0–3 |
| `naturalness` | int | 0–3 |
| `notes` | string | Free text, required if any score < 2 |

---

## Acceptance Thresholds

| Metric | Threshold | Failure action |
|---|---|---|
| Factuality on preserve_facts examples | 100% score 3 | Block release; investigate fact-lock gate |
| Mean edit effort (all 50 examples) | ≤ 2.0 | Retrain or tighten Final prompt |
| Mean naturalness (all 50 examples) | ≥ 2.0 | Expand detection heuristics for missed patterns |
| Any single example with accuracy = 0 | Zero occurrences | Immediate block; root-cause in audit trail |

---

## Example Set Composition

| Domain | Count | Source |
|---|---|---|
| Technical (APIs, incident reports, specs) | 10 | Synthetic + anonymized real postmortems |
| Academic (literature reviews, abstracts) | 10 | Synthetic Wikipedia-style paragraphs |
| Marketing (product copy, announcements) | 10 | Synthetic promotional copy |
| Casual (emails, Slack summaries) | 10 | Synthetic conversational documents |
| Mixed (multi-domain docs) | 10 | Synthetic combinations |

All 50 examples are pre-reviewed by the project lead to confirm:
- At least 3 of the 24 patterns are present in each source text
- preserve_facts tokens are clearly identifiable
- Expected scholar-editor output does not fabricate any fact
