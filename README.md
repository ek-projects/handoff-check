# Handoff Check
Verify explicit agent handoff claims against local evidence. Python 3.10+, Git for commit checks; no packages, keys or network.

## Quick start
```sh
python3 -m handoffcheck examples/evidence_handoff.md --root .
python3 -m handoffcheck examples/evidence_handoff.md --root . --format json
python3 -m unittest discover -s tests -v
python3 scripts/demo_evidence.py
```

## Claim format
One claim per line, outside Markdown code fences:
```text
FILE: relative/path.py
COMMIT: 2756070 | scripts/demo_screen.py
COMPLETE: yes
TESTS: reported passing
```
FILE checks regular-file presence within the selected root, rejecting absolute paths, traversal and escaping symlinks. COMMIT accepts 7–40 hexadecimal characters and optionally checks a changed path (merge commits compare each parent). Use a repository root, not its subdirectory.
COMPLETE checks for explicit open boxes and labeled blockers anywhere in this document. No conflict does not prove completion.
TESTS stays unverifiable: commands from handoffs are never executed.

Results are **verified**, **contradicted**, or **unverifiable**, with source lines, evidence, scope and a UTC observation timestamp in JSON. Observations may become stale after files change. Git existence does not prove the current checkout contains a change, or that a change works. Missing local commits may exist remotely; nothing is fetched.

Use --strict for automation: 0 only when at least one claim exists and all are verified, 1 for contradicted/unknown/empty verification, 2 for input/output errors. Without --root, legacy checklist extraction remains available.
Input is UTF-8 Markdown/TXT, max 1 MiB. -o creates a new report and refuses existing files. All input remains local.

## Reproducible before/after demo
scripts/demo_evidence.py builds a temporary synthetic Git repository, runs the real CLI, shows false claims, then fixes the file and task state and runs it again. It never modifies your project repository.

## Boundaries
This is a proof of concept with an explicit claim language, not natural-language understanding or a security audit. A checked task remains a source assertion. No claim of uniqueness against existing tools.
MIT licensed. Planning history is in devpost/. The user challenged the initial checklist concept and authorized the evidence-verification direction; the earlier full learner interview was not retroactively completed.
