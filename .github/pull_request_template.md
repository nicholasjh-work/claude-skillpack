---
name: Pull Request
about: Propose changes to Scholar Editor skills or shared components
title: ''
labels: ''
assignees: ''

---

## Summary
<!-- One-sentence summary of the change -->

## Changes
- **Files changed**: list key files
- **Type**: chore | feat | fix | docs | test | ci

## Motivation
<!-- Why this change is needed and what it fixes or improves -->

## How to test
- Local steps to reproduce
```bash
pip install -r requirements.txt
pytest tests/ -q
python tools/check_pattern_coverage.py --fixtures tests/fixtures.jsonl --threshold 0.9

