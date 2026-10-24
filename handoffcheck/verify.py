"""Check explicit claims against local evidence; never execute handoff commands."""
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from .core import analyze

CLAIM = re.compile(r"^\s*(?:[-*]\s+)?(FILE|COMMIT|COMPLETE|TESTS)\s*:\s*(.*?)\s*$", re.I)

def verify(text, root, filename="<input>"):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("root must be a directory")
    report = analyze(text, filename)
    checks = []
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        marker = re.match(r"^(`{3,}|~{3,})", stripped)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and stripped == token:
                fence = None
            continue
        if fence:
            continue
        match = CLAIM.match(line)
        if not match:
            continue
        kind, value = match.group(1).upper(), match.group(2)
        result = dict(kind=kind, claim=value, line=number, status="unverifiable",
                      evidence="", scope="")
        try:
            if kind == "FILE":
                result["scope"] = "Regular file exists now; does not prove contents or authorship."
                path = Path(value)
                if not value or path.is_absolute() or ".." in path.parts:
                    result["evidence"] = "Expected a relative path inside the selected root."
                else:
                    resolved = (root / path).resolve()
                    if not resolved.is_relative_to(root):
                        result["evidence"] = "Path resolves outside selected root."
                    else:
                        result["status"] = "verified" if resolved.is_file() else "contradicted"
                        result["evidence"] = f"{value}: " + ("regular file present" if resolved.is_file() else "regular file absent")
            elif kind == "COMMIT":
                result["scope"] = "Commit exists in this repository; optional path is changed by it. Does not prove current checkout or correctness."
                sha, separator, path = value.partition(" | ")
                if not re.fullmatch(r"[0-9a-fA-F]{7,40}", sha):
                    result["evidence"] = "Expected hexadecimal commit ID (7–40 characters), optionally: ID | relative/path"
                elif separator and (not path or Path(path).is_absolute() or ".." in Path(path).parts):
                    result["evidence"] = "Invalid commit path."
                else:
                    def git(*args):
                        return subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                                              timeout=5, env={"PATH": "/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1",
                                                             "GIT_CONFIG_GLOBAL": "/dev/null"})
                    probe = git("rev-parse", "--show-toplevel")
                    if probe.returncode or Path(probe.stdout.decode().strip()).resolve() != root:
                        result["evidence"] = "Selected root must be the Git repository root."
                    else:
                        found = git("rev-parse", "--verify", sha + "^{commit}")
                        if found.returncode:
                            result["status"] = "contradicted"
                            result["evidence"] = "Commit ID not resolvable in selected local repository."
                        else:
                            full = found.stdout.decode().strip()
                            result["status"] = "verified"
                            result["evidence"] = "Resolved commit " + full
                            if separator:
                                changed = git("diff-tree", "--root", "-m", "--no-commit-id", "--name-only", "-r", "-z", full)
                                if changed.returncode:
                                    result["status"] = "unverifiable"
                                    result["evidence"] = "Unable to inspect commit changes."
                                else:
                                    paths = changed.stdout.decode("utf-8", "replace").split("\0")
                                    result["status"] = "verified" if path in paths else "contradicted"
                                    result["evidence"] += "; path " + path + (" changed" if path in paths else " not changed")
            elif kind == "COMPLETE":
                result["scope"] = "Document consistency only; not independent proof that all work is complete."
                if value.casefold() not in {"yes", "true", "si", "sì"}:
                    result["evidence"] = "Supported positive claim: COMPLETE: yes"
                else:
                    refs = [x["line"] for x in report["tasks"] if x["status"] == "open"]
                    refs += [x["line"] for x in report["notes"] if x["kind"] == "blocker"]
                    result["status"] = "contradicted" if refs else "unverifiable"
                    result["evidence"] = ("Open tasks or blockers at source lines: " + ", ".join(map(str, sorted(refs)))
                                          if refs else "No explicit conflict found; completion remains unproven.")
            else:
                result["scope"] = "Test execution is outside this verifier."
                result["evidence"] = "Reported test outcome is not independently verified. No command executed."
        except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
            result["status"] = "unverifiable"
            result["evidence"] = "Evidence unavailable: " + type(exc).__name__
        checks.append(result)
    report["verification"] = dict(checked_at=datetime.now(timezone.utc).isoformat(), checks=checks,
        summary={s: sum(c["status"] == s for c in checks) for s in ("verified", "contradicted", "unverifiable")})
    return report

def render_verification(report):
    rows = ["# Handoff evidence report", "", "Checks are scoped observations, not certification of project completion.", ""]
    checks = report["verification"]["checks"]
    if not checks:
        rows.append("No explicit FILE, COMMIT, COMPLETE or TESTS claims found. Nothing verified.")
    for c in checks:
        rows += [f"## {c['status'].upper()} — {c['kind']} ({report['source']}:{c['line']})",
                 "", c["claim"], "", "Evidence: " + c["evidence"], "", "Scope: " + c["scope"], ""]
    return "\n".join(rows) + "\n"
