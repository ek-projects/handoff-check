"""Reproducible real CLI demonstration in an isolated temporary repository."""
import subprocess, sys, tempfile
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent
def main():
    with tempfile.TemporaryDirectory(prefix="handoff-demo-") as td:
        root=Path(td)
        def git(*args):
            return subprocess.check_output(["git","-C",td,*args],stderr=subprocess.DEVNULL).decode().strip()
        git("init")
        (root/"app.py").write_text("print('hello')\n")
        git("add","app.py")
        git("-c","user.name=Demo","-c","user.email=demo@example.invalid","commit","-m","Synthetic fixture")
        sha=git("rev-parse","HEAD")
        source=root/"handoff.md"
        for title, contents in [
            ("BEFORE: confident handoff, missing evidence",f"COMPLETE: yes\nFILE: app.py\nFILE: release.txt\nCOMMIT: {sha} | app.py\n- [ ] Publish release\n"),
            ("AFTER: corrected file and explicit scope",f"FILE: app.py\nFILE: release.txt\nCOMMIT: {sha} | app.py\n- [x] Prepare local release file\n")]:
            if title.startswith("AFTER"):
                (root/"release.txt").write_text("Synthetic local release\n")
            source.write_text(contents)
            print("\n"+title+"\n"+contents,flush=True)
            result=subprocess.run([sys.executable,"-m","handoffcheck",str(source),"--root",td,"--strict"],cwd=BASE)
            print("Actual exit code:",result.returncode,flush=True)
if __name__=="__main__": main()
