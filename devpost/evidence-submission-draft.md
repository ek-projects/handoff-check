# Handoff Check
## Tagline
Can the next agent trust this handoff? Check file and commit claims against local evidence.

## Inspiration
A handoff may confidently say work is complete while files are absent or tasks remain open. We encountered this continuity problem while moving between coding-agent sessions.

## What it does
An offline Python CLI checks explicit FILE and COMMIT claims, detects COMPLETE claims contradicted by open tasks or blockers, and emits verified, contradicted or unverifiable findings with source lines and scoped evidence. Claimed test results remain unverifiable.

## How we built it
We consulted the Devpost Learn Skill Pack and created planning drafts. The user challenged the originality of the first checklist parser and authorized a change to evidence verification. An AI coding agent implemented and tested that direction. We do not claim the initial full flipped-interaction interview was completed.

## Testing
12 automated tests pass. A real before/after demo creates a temporary Git repository and runs the actual CLI: missing evidence produces exit 1; corrected claims produce exit 0. Python standard library, MIT license.

## Demo outline (90 seconds)
0–15: show explicit handoff claims.
15–45: run evidence checks and show missing file and completion contradiction.
45–70: correct the fixture, rerun and show scoped verified evidence.
70–90: show tests and explain limitations.

## Missing deliverables
Public repository and license URL: blocked by invalid GitHub CLI authentication.
Public video URL: missing. Recording reservation was refused.
Personal answers: resources used, AI costs, confidence, actual value remain to be provided.
Draft only; not submitted.
