> Historical initial draft. Superseded on 23 October 2026 by [evidence-verifier-plan.md](evidence-verifier-plan.md), following the user's authorized change of direction.

---
doc: scope
status: draft
---
# Handoff Check — Scope

One line: a minimal offline command-line utility that converts explicitly marked handoff notes into an evidence-linked checklist without guessing project state.

## The Unique Kernel
Every item includes an exact filename, line number and section. A checked task is described as *source-marked done*, never as independently proven complete.

## Who It's For
Solo builders managing several coding-agent projects who need to resume from existing TXT/Markdown handoff files and avoid losing blockers and constraints.

## The Core Loop
Open a local handoff; run the CLI; read open/checked tasks, explicit blockers and constraints with source references; return to the original lines to confirm.

## Inspiration & Identity
Traceability and restrained assertions rather than conversational overconfidence. Command-line output, no cloud dependencies.

## Why This Matters to the Learner
The operational handoff emphasizes continuity, verifiable tests and no invented status. This project direction is **proposed by the agent, not yet approved by the learner**.

## What "Working" Looks Like
Running `python3 -m handoffcheck examples/demo_handoff.md` returns a checklist with source:line references. An alternate JSON mode enables reuse. Automated tests validate extraction and reject false completion in free-form text.

## The POC Boundary
UTF-8 .md/.txt files under 1 MiB; explicit `[ ]`/`[x]` tasks; labeled blockers/constraints/verification notes; markdown headings; Markdown or JSON output; useful errors.

## Later
Optional free-form language extraction with human confirmation, richer UI, task tracking integrations.

## Explicitly Cut
LLM inference (risk of fabricated states); server/DB (not needed); execution of verification commands (unsafe to imply checks ran); remote storage, authentication, and personal handoff upload.

## Open decisions
Learner has not yet signed off the proposed product direction; treat as a working MVP candidate, not approved scope.
