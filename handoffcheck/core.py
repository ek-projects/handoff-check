"""Parse explicitly marked handoff entries. Never infer completion or verification."""
from __future__ import annotations

import re
from pathlib import Path

TASK = re.compile(r"^\s*(?:[-*]\s*)?\[([ xX])\]\s+(.+?)\s*$")
HEADING = re.compile(r"^\s*(#{1,6})\s+(.+?)\s*#*\s*$")
NUMBERED = re.compile(r"^\s*\d+\)\s+([A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ0-9 /_-]{3,})\s*$")
NOTE = re.compile(r"^\s*(?:[-*]\s*)?(BLOCCO|BLOCKER|BLOCKED|VINCOLO|CONSTRAINT|VERIFICA|VERIFICATION)\s*:\s*(.+?)\s*$", re.I)
KINDS = {"blocco": "blocker", "blocker": "blocker", "blocked": "blocker",
         "vincolo": "constraint", "constraint": "constraint",
         "verifica": "verification", "verification": "verification"}
NONE_VALUES = {"nessuno", "nessuna", "none", "n/a", "no blockers", "no blocker", "non presenti"}

def analyze(text: str, filename: str = "<input>") -> dict:
    """Return traceable items from only explicit task markers and note labels."""
    tasks: list[dict] = []
    notes: list[dict] = []
    sections: list[tuple[int, str]] = []
    fence = None

    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        marker = re.match(r"^(`{3,}|~{3,})", stripped)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and stripped == token:
                fence = None
            continue
        if fence or not stripped:
            continue

        h = HEADING.match(line)
        if h:
            depth, name = len(h.group(1)), h.group(2).strip()
            sections = [s for s in sections if s[0] < depth]
            sections.append((depth, name))
            continue

        n = NUMBERED.match(line)
        if n:
            sections = [(1, n.group(1).strip())]
            continue

        section = " > ".join(name for _, name in sections) or "(top-level)"
        task = TASK.match(line)
        if task:
            tasks.append({
                "text": task.group(2).strip(),
                "status": "done" if task.group(1).lower() == "x" else "open",
                "section": section,
                "line": lineno,
            })
            continue

        note = NOTE.match(line)
        if note and note.group(2).strip().casefold() not in NONE_VALUES:
            notes.append({
                "kind": KINDS[note.group(1).casefold()],
                "text": note.group(2).strip(),
                "section": section,
                "line": lineno,
            })
    done = sum(t["status"] == "done" for t in tasks)
    return {"source": filename, "summary": {
        "tasks_total": len(tasks), "open": len(tasks) - done, "marked_done": done,
        "explicit_blockers": sum(n["kind"] == "blocker" for n in notes),
        "constraints": sum(n["kind"] == "constraint" for n in notes),
        "verification_notes": sum(n["kind"] == "verification" for n in notes),
    }, "tasks": tasks, "notes": notes}


def render_markdown(result: dict) -> str:
    """Generate a readable report with source file:line citations for every finding."""
    source = result["source"]
    s = result["summary"]
    rows = [
        "# Handoff Check report",
        "",
        "Source: \x60" + source.replace("\x60", "'") + "\x60",
        "",
        f"Tasks: {s['tasks_total']} | Open: {s['open']} | Marked done: {s['marked_done']} | Explicit blockers: {s['explicit_blockers']}",
        "",
        "**Important:** 'marked done' reflects only a checked box in the input; no work or test was independently verified.",
        ""
    ]
    if not result["tasks"] and not result["notes"]:
        rows.extend(["No explicitly marked items found. No completion claims can be made.", ""])
    if result["tasks"]:
        rows.extend(["## Checklist", ""])
        for t in result["tasks"]:
            status = "x" if t["status"] == "done" else " "
            rows.append(f"- [{status}] {t['text']} — {t['section']} ({source}:{t['line']})")
        rows.append("")
    for kind, heading in (("blocker", "Explicit blockers"), ("constraint", "Constraints"), ("verification", "Verification notes (not independently checked)")):
        entries = [n for n in result["notes"] if n["kind"] == kind]
        if entries:
            rows.extend([f"## {heading}", ""])
            rows.extend(f"- {n['text']} — {n['section']} ({source}:{n['line']})" for n in entries)
            rows.append("")
    return "\n".join(rows).rstrip() + "\n"
