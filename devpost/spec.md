> Historical initial draft. Superseded on 23 October 2026 by [evidence-verifier-plan.md](evidence-verifier-plan.md), following the user's authorized change of direction.

---
doc: spec
status: draft
---
# Handoff Check — Technical Spec

## How This Works, In Plain Language
The CLI reads one text file, identifies only deliberately marked lines, records where each line came from and prints a concise report. It never asks an AI model to guess progress. A small standard-library implementation makes it repeatable and easy to test.

## The Core Journey Through the System
Input path → bounded UTF-8 read (`__main__.py`) → explicit-line parser (`core.py:analyze`) → structured dict → renderer (`render_markdown` or JSON serialization) → terminal or safe output path.
PRD ref: `prd.md > The Core Journey`.

## Stack
- Python 3.10+ standard library; no external dependencies.
- `re` for explicit line patterns; `argparse` for CLI, `json` for machine output, `unittest` for tests.
- No keys, API endpoints, GPU or deployed service.

This is the agent's minimal implementation selection for a draft prototype. Learner stack agreement has **not** been recorded.

## Where It Runs and How Someone Tries It
Linux/macOS/Windows with Python 3.10+. From repository root:
`python3 -m handoffcheck examples/demo_handoff.md`
`python3 -m handoffcheck examples/demo_handoff.md --format json`
`python3 -m unittest discover -s tests -v`

## Look and Feel
Plain Markdown report with counts, sections, checkboxes, explicit qualifier and source location. JSON available for other tools.

## Components

### Parser
`handoffcheck/core.py:analyze`: tokenizes headings, task boxes, and labeled operational notes, excluding code fences.
PRD refs: `Explicit Task Extraction`, `Named Operational Notes`.

### Renderer
`handoffcheck/core.py:render_markdown`: source-linked report and explicit disclaimer.
PRD ref: `Evidence-Linked Report`.

### CLI
`handoffcheck/__main__.py:main`: input validation, formats, optional output path and errors.
PRD ref: `Safe File Handling`.

## Data Model
`{"source": name, "summary": counts, "tasks": [{"text", "status", "section", "line"}], "notes": [{"kind", "text", "section", "line"}]}`. All data derived from one file; none persisted.

## File Structure
```
handoffcheck/{__init__.py,__main__.py,core.py}
examples/demo_handoff.md
tests/test_handoffcheck.py
devpost/{scope.md,prd.md,spec.md,checklist.md}
README.md
LICENSE
```

## Important Failure Modes
Missing/non-UTF-8/oversized input → actionable error and exit code 2. Ambiguous unmarked text → no inferred task. Outfile same as infile → error, not overwrite.

## What Was Simplified and Why
Recognize only explicit syntax instead of free-form language analysis: it prevents hallucinated completion, is easy to test, and fits a 1–3 minute live demo.

## Decisions and Open Issues
These technical choices are provisional agent implementation details, not user-approved product direction. Public code repository and video publishing depend on external account capabilities and final review.
