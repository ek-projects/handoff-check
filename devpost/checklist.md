> Historical initial draft. Superseded on 23 October 2026 by [evidence-verifier-plan.md](evidence-verifier-plan.md), following the user's authorized change of direction.

---
doc: checklist
status: draft
---
# Build Checklist

Build mode: autonomous prototype based on the existing handoff instruction; NOT a recorded participant selection of the official 5-build mode.

## Slices
- [x] **1. Read handoff file and identify explicit checklist items**
  Becomes usable: CLI reads synthetic Markdown and returns task statuses with source line numbers.
  Why now: Proves the full read/parse/report loop.
  PRD ref: `prd.md > Explicit Task Extraction`
  Spec ref: `spec.md > Parser`, `spec.md > CLI`
  Build: Implement bounded input and explicit checked/unchecked recognition.
  Verify (mechanical): `python3 -m unittest discover -s tests -v`
  Learner check: Run sample and inspect each original line number.
  Commit: `Add evidence-linked handoff parser`

- [x] **2. Extract explicit blocker/constraint/verification notes and render Markdown/JSON**
  Becomes usable: One readable checklist and a JSON report.
  Why now: Shows the traceability kernel with distinct operational notes.
  PRD ref: `prd.md > Named Operational Notes`, `prd.md > Evidence-Linked Report`
  Spec ref: `spec.md > Renderer`
  Build: Add note recognition, formatting, source disclaimers.
  Verify (mechanical): tests validate counts and source references; run sample CLI.
  Learner check: Compare sample original notes with report.
  Commit: `Add operational note extraction and reports`

- [x] **3. Add sample, error paths, repeatable tests and basic docs**
  Becomes usable: A stranger can reproduce an end-to-end example without credentials.
  Why now: Makes a credible demo.
  PRD ref: `prd.md > Safe File Handling`
  Spec ref: `spec.md > Important Failure Modes`
  Build: Synthetic example, unittest suite, MIT license, README.
  Verify (mechanical): all four automated tests pass and sample CLI exits 0.
  Learner check: Follow README from clean shell.
  Commit: `Document and test MVP`

- [ ] **4. Publish and demonstrate the working entry**
  Becomes usable: Public repository and publicly playable 1–3 minute demo, with Devpost draft reviewed before submission.
  Why now: Required judging deliverables.
  PRD ref: `prd.md > The Core Journey`
  Spec ref: `spec.md > Where It Runs and How Someone Tries It`
  Build: Verify repo privacy/credentials, publish, record/upload video, fill submission questions, final check.
  Verify (mechanical): Public repo URL and license accessible; video URL playable; Devpost returns Submitted.
  Learner check: Review project and Devpost summary.
  Commit: `Prepare Devpost submission`

## Hands-on Checkpoints
- [ ] Learner reviews proposed project direction and final report.
- [ ] Learner performs final kick-the-tires check.

## Final Review
- [ ] Product scope approved and final revisions verified.
- [ ] Learner confirms readiness to submit.

## Code Tour and App Map
- [ ] Guided learning recap/code tour performed with learner.
- [ ] devpost/app-map.html created if requested by official build flow.

## Revisions
- Working prototype built without completed skill-pack participant interview; docs retain draft status and require honest review before final skill completion.
