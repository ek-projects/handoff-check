import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from handoffcheck import analyze, render_markdown

class HandoffCheckTests(unittest.TestCase):
    def test_extracts_explicit_evidence_with_lines(self):
        example = "# Delivery\n- [ ] Upload a demo\n- [x] Run tests\nBLOCCO: upload token missing\nVINCOLO: no secrets\nVERIFICA: python -m unittest\n"
        res = analyze(example, "demo.md")
        self.assertEqual(res["summary"], dict(tasks_total=2, open=1, marked_done=1, explicit_blockers=1, constraints=1, verification_notes=1))
        self.assertEqual(res["tasks"][0]["line"], 2)
        self.assertEqual(res["tasks"][0]["section"], "Delivery")
        self.assertIn("demo.md:2", render_markdown(res))

    def test_never_infers_from_prose_or_empty_state(self):
        res = analyze("All tasks complete.\nBLOCCO: nessuno\n## Next\nThis is blocked maybe\n")
        self.assertEqual(res["summary"]["tasks_total"], 0)
        self.assertEqual(res["summary"]["explicit_blockers"], 0)
        self.assertIn("No explicitly marked", render_markdown(res))

    def test_txt_numbered_sections_and_code_fences(self):
        res = analyze("1) WORKFLOW\n- [ ] First\n\x60\x60\x60md\n- [x] fake\n\x60\x60\x60\n- [x] Real\n", "note.txt")
        self.assertEqual([t["line"] for t in res["tasks"]], [2, 6])
        self.assertEqual([t["status"] for t in res["tasks"]], ["open", "done"])
        self.assertEqual(res["tasks"][1]["section"], "WORKFLOW")

    def test_cli_json_and_protection(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/"input.txt"
            path.write_text("- [ ] Check\n", encoding="utf8")
            proc = subprocess.run([sys.executable, "-m", "handoffcheck", str(path), "--format", "json"], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)["summary"]["open"], 1)
            bad = subprocess.run([sys.executable, "-m", "handoffcheck", str(path), "-o", str(path)], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 2)
            self.assertEqual(path.read_text(), "- [ ] Check\n")

if __name__ == "__main__":
    unittest.main()
