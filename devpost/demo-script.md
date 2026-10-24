# Handoff Check — 1 to 3 minute demo plan (English)

**This is a recording SCRIPT, not a video or proof of upload.**

0:00–0:15 — State the problem: agent handoff files often contain tasks, constraints and blockers but lose traceability.

0:15–0:35 — Display `examples/demo_handoff.md`, including `[x]` and `[ ]`, `BLOCCO:`, `VINCOLO:` and `VERIFICA:`.

0:35–1:05 — Run `python3 -m handoffcheck examples/demo_handoff.md`. Show each task's exact source line and separate blocker/constraint groups.

1:05–1:25 — Emphasize checked means *marked as done in the source*, not tested. Display JSON: `python3 -m handoffcheck examples/demo_handoff.md --format json`.

1:25–1:45 — Run `python3 -m unittest discover -s tests -v`, show actual passing tests, explain the implementation is offline and contains no uploaded private data.

1:45–2:00 — Show README, license, `devpost/scope.md`, `devpost/prd.md`, `devpost/spec.md`. Mention the source is public only after GitHub publish is verified.

**Video status:** Not recorded or uploaded. Do not fabricate a URL or claim recording exists.
