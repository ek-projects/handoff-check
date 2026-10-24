import unittest
import tempfile
import subprocess
import sys
from pathlib import Path
from handoffcheck.verify import verify

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "real.txt").write_text("evidence")
    def checks(self, text):
        return verify(text, self.root)["verification"]["checks"]
    def test_file_presence_and_absence(self):
        self.assertEqual([c["status"] for c in self.checks("FILE: real.txt\nFILE: missing.txt")],
                         ["verified", "contradicted"])
    def test_escape_and_symlink(self):
        (self.root / "outside").symlink_to(self.root.parent)
        for path in ("../secret", "/etc/passwd", "outside/secret"):
            self.assertEqual(self.checks("FILE: " + path)[0]["status"], "unverifiable")
    def test_completion_never_inferred(self):
        self.assertEqual(self.checks("COMPLETE: yes")[0]["status"], "unverifiable")
        c = self.checks("COMPLETE: yes\n- [ ] pending\nBLOCCO: unresolved")[0]
        self.assertEqual(c["status"], "contradicted")
        self.assertIn("2, 3", c["evidence"])
    def test_test_claim_never_executed(self):
        self.assertEqual(self.checks("TESTS: touch PWNED")[0]["status"], "unverifiable")
        self.assertFalse((self.root / "PWNED").exists())
    def test_fenced_claims_ignored(self):
        self.assertEqual(self.checks("````md\nFILE: missing\n~~~\nFILE: missing\n````"), [])
    def test_git_commit_and_changed_path(self):
        def git(*args):
            return subprocess.check_output(["git", "-C", str(self.root), *args], stderr=subprocess.DEVNULL).decode().strip()
        git("init")
        git("add", "real.txt")
        git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "Fixture")
        sha = git("rev-parse", "HEAD")
        cases = self.checks(f"COMMIT: {sha} | real.txt\nCOMMIT: {sha} | other.txt\nCOMMIT: {'0'*40}\nCOMMIT: --help")
        self.assertEqual([c["status"] for c in cases], ["verified", "contradicted", "contradicted", "unverifiable"])
    def test_non_repository_is_unknown(self):
        self.assertEqual(self.checks("COMMIT: abcdef0")[0]["status"], "unverifiable")
    def test_cli_strict_and_nonoverwrite(self):
        source = self.root / "handoff.md"
        source.write_text("FILE: missing")
        output = self.root / "report.md"
        output.write_text("keep")
        def run(*args):
            return subprocess.run([sys.executable, "-m", "handoffcheck", str(source), *args],
                                  capture_output=True, text=True)
        self.assertEqual(run("--root", str(self.root), "--strict").returncode, 1)
        self.assertEqual(run("-o", str(output)).returncode, 2)
        self.assertEqual(output.read_text(), "keep")
        source.write_text("FILE: real.txt")
        self.assertEqual(run("--root", str(self.root), "--strict").returncode, 0)
        source.write_text("Nothing explicit")
        self.assertEqual(run("--root", str(self.root), "--strict").returncode, 1)
