---
name: ai-pattern-scrubber
description: Final-pass prose scrubber for stale AI-style writing patterns and generic phrasing.
version: "1.0.0"
---

# AI Pattern Scrubber

Use this skill as a final pass on any prose. The goal is not to hide authorship. The goal is to remove stale, generic, machine-smoothed writing patterns and replace them with clean professional language.

## What to scan for
1. Em dashes
2. Decorative arrows or symbols
3. Emoji unless explicitly requested
4. "Here's the..." openers
5. Contrast framing such as "it's not X, it's Y"
6. Rule-of-three phrasing used for effect rather than substance
7. Repetitive sentence openings
8. Corporate -ing verbs like highlighting, emphasizing, facilitating when a simple verb is stronger
9. Empty transition questions such as "The catch?" or "The kicker?"
10. Vague statements that need a concrete noun, number, system, date, or action

## Rewrite standard
- Make the sentence more direct.
- Replace abstraction with specific nouns and verbs.
- Delete filler instead of rephrasing it.
- Break overly smooth rhythm.
- Keep only what changes meaning.
- Preserve the user's actual point of view.

## Output format
Return:
1. Brief diagnosis of the main patterns found
2. Revised draft
3. Optional notes on any line that still needs user-specific details
