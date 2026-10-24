# Evidence verifier — approved direction, 23 October 2026
The user challenged whether checklist extraction was innovative, considered changing direction, and instructed "Costruisci e concludi" after the proposal to verify files, commits and contradictions. This authorizes this implementation; it does not retroactively complete the earlier learner interview.

## Scope and PRD
For developers resuming agent projects, compare explicit handoff claims with local evidence. Preserve source lines and distinguish verified, contradicted and unverifiable. No NLP inference and no execution of handoff commands.

## Specification
verify.py adds FILE, COMMIT, COMPLETE and TESTS claim handling. --root selects the local evidence boundary; Git uses fixed argument arrays with timeout and hexadecimal commit IDs. FILE rejects traversal and symlink escapes. COMPLETE compares against parsed open tasks and blockers. TESTS remains unverifiable.
--strict: 0 only for nonempty all-verified reports, 1 for unresolved/contradicted/empty, 2 for I/O or input errors. Existing checklist mode remains available. Output creation is exclusive.

## Checklist
- [x] File existence with bounded paths.
- [x] Commit resolution and exact changed-path membership.
- [x] Completion contradiction references.
- [x] Markdown and JSON output with explicit limits.
- [x] Regression and evidence tests: 12 passed.
- [x] Real temporary-repository before/after demo: exits 1 then 0.
- [x] README and reproducible demo script.
- [ ] Public repository: server GitHub authentication invalid.
- [ ] Recorded video: capacity reservation refused; no encoding started.
- [ ] Personal submission answers and final submission.

## Verification limits
Regular-file presence does not prove correct contents. Local commit existence does not prove deployment or current checkout. No-conflict does not prove completion. This prototype is not a security audit and originality has not been established by competitor research.
