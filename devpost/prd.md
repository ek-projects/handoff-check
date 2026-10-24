> Historical initial draft. Superseded on 23 October 2026 by [evidence-verifier-plan.md](evidence-verifier-plan.md), following the user's authorized change of direction.

---
doc: prd
status: draft
---
# Handoff Check — Product Requirements

A local command-line report for a solo developer with project handoffs.
Source: `scope.md > The Core Loop` and `scope.md > The Unique Kernel`.

## The Core Journey
1. User prepares a Markdown/TXT handoff with explicit task boxes and/or labeled notes.
2. User runs `python3 -m handoffcheck INPUT`.
3. Tool prints counts and a checklist referencing the original section and input line for each item.
4. User inspects outstanding items and source evidence, or chooses machine-readable JSON via `--format json`.

## Interaction Surface and Output
Single CLI, one positional input path, optional format and output path. Report shows source name, totals, a disclaimer about source assertions, checklist, explicit blockers, constraints and verification notes.

## Look and Feel
Scannable, textual, neutral. No presentation polish is required; a demonstrable end-to-end behavior is more important.

## Features and Behavior

### Explicit Task Extraction
Given `- [ ]` or `- [x]` lines, extract item text, source line and enclosing Markdown or numbered uppercase section. Mark unchecked as open, checked as source-marked done.

### Named Operational Notes
Recognize explicitly labeled `BLOCCO`, `BLOCKER`, `BLOCKED`, `VINCOLO`, `CONSTRAINT`, `VERIFICA`, `VERIFICATION`. Avoid interpreting unstructured prose as status.

### Evidence-Linked Report
Produce Markdown by default or JSON. Include precise `file:line` citations in Markdown and separate line/section fields in JSON.

### Safe File Handling
No execution of commands from the handoff. Do not overwrite the input with `-o`. Clear errors for non-UTF-8, missing files and oversized files.

## States and Boundaries
- **No marked items:** explain that no explicit items were found; never say the project is complete.
- **Checked input:** report it as *marked done*, not independently validated.
- **Input limits:** UTF-8 plain .md/.txt; maximum 1 MiB.
- **Code fences:** ignore Markdown code-fenced examples to reduce false positives.
- **Data storage:** none; input remains on local filesystem and is never uploaded.

## What We're Building
One CLI with deterministic parser, Markdown/JSON renderer, synthetic sample, repeatable tests and repository instructions.

## Deferred From the POC
Interactive task updates, advanced NLP, video capture, cloud integration.

## Non-Goals
No AI model calls in runtime, no assertion that verification commands have run, no import of private project handoffs.

## Product Decisions and Open Questions
This is an **agent-selected draft** based on the handoff's proposed Handoff Check idea and hackathon feasibility, not a finished learner interview. Product direction remains pending review.
