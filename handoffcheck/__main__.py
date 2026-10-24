"""Run: python -m handoffcheck INPUT [--format markdown|json] [--output FILE]."""
import argparse
import json
import sys
from pathlib import Path
from .core import analyze, render_markdown
from .verify import verify, render_verification

MAX_BYTES = 1024 * 1024

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Evidence-linked checklist extraction from TXT/Markdown handoffs")
    p.add_argument("file", type=Path, help="Input .txt or .md (max 1 MiB)")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("-o", "--output", type=Path, help="Write report to a new file (never overwrite source)")
    p.add_argument("--root", type=Path, help="Verify explicit claims against this repository root")
    p.add_argument("--strict", action="store_true", help="Exit 1 if any claim is contradicted or unverifiable; requires --root")
    args = p.parse_args(argv)
    if args.strict and args.root is None:
        p.error("--strict requires --root")
    try:
        path = args.file
        if path.suffix.lower() not in (".txt", ".md", ".markdown"):
            raise ValueError("expected .txt or .md input")
        if path.stat().st_size > MAX_BYTES:
            raise ValueError("input larger than 1 MiB")
        text = path.read_text(encoding="utf-8-sig")
        result = verify(text, args.root, path.name) if args.root else analyze(text, path.name)
        output = (json.dumps(result, ensure_ascii=False, indent=2) + "\n"
                  if args.format == "json" else (render_verification(result) if args.root else render_markdown(result)))
        if args.output:
            if args.output.resolve() == path.resolve():
                raise ValueError("output must not overwrite source")
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(output)
        else:
            sys.stdout.write(output)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"handoffcheck: {exc}", file=sys.stderr)
        return 2
    if args.strict and (not result["verification"]["checks"] or any(c["status"] != "verified" for c in result["verification"]["checks"])):
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
