"""Record real CLI results from a temporary synthetic repository."""
import tkinter as tk
import tempfile, subprocess, sys, json
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
tmp=tempfile.TemporaryDirectory(prefix="handoff-video-")
repo=Path(tmp.name)
def git(*args):
    return subprocess.check_output(["git","-C",str(repo),*args],stderr=subprocess.DEVNULL).decode().strip()
git("init")
(repo/"app.py").write_text("print('demo')\n")
git("add","app.py")
git("-c","user.name=Demo","-c","user.email=demo@example.invalid","commit","-m","Synthetic fixture")
sha=git("rev-parse","HEAD")
source=repo/"handoff.md"
before=f"COMPLETE: yes\nFILE: app.py\nFILE: release.txt\nCOMMIT: {sha} | app.py\n- [ ] Prepare release\n"
source.write_text(before)
root=tk.Tk()
root.geometry("1280x720+0+0")
root.attributes("-fullscreen",True)
root.configure(bg="#101827")
tk.Label(root,text="HANDOFF CHECK  /  Evidence, not confidence",font=("DejaVu Sans",26,"bold"),fg="white",bg="#101827",pady=24).pack()
caption=tk.Label(root,font=("DejaVu Sans",17),fg="#78c7ff",bg="#101827",pady=16)
caption.pack()
body=tk.Text(root,font=("DejaVu Sans Mono",15),bg="#101827",fg="#e5f0ff",wrap="word",borderwidth=0,padx=38,pady=20)
body.pack(fill="both",expand=True)
tk.Label(root,text="Actual CLI execution • Synthetic repository • No handoff commands executed",font=("DejaVu Sans",13),fg="#8da4bf",bg="#101827",pady=18).pack()
def show(title,text):
    caption.config(text=title)
    body.delete("1.0","end")
    body.insert("end",text)
def check():
    p=subprocess.run([sys.executable,"-m","handoffcheck",str(source),"--root",str(repo),"--strict","--format","json"],cwd=BASE,capture_output=True,text=True,timeout=15)
    data=json.loads(p.stdout)
    lines=["$ python3 -m handoffcheck handoff.md --root REPO --strict",""]
    for c in data["verification"]["checks"]:
        lines += [c["status"].upper()+"  "+c["kind"]+"  [source line "+str(c["line"])+"]",c["evidence"],""]
    lines += ["Actual process exit code: "+str(p.returncode)]
    return "\n".join(lines)
def fix():
    (repo/"release.txt").write_text("Local demo release")
    source.write_text(f"FILE: app.py\nFILE: release.txt\nCOMMIT: {sha} | app.py\n- [x] Prepare local release\n")
    show("3 / 5 — Fix the file; remove the unsupported global completion claim",check())
def tests():
    p=subprocess.run([sys.executable,"-m","unittest","discover","-s","tests"],cwd=BASE,capture_output=True,text=True,timeout=15)
    show("4 / 5 — Run the real regression suite","$ python3 -m unittest discover -s tests\n\n"+p.stdout+p.stderr+"\nActual exit code: "+str(p.returncode))
show("1 / 5 — An agent says the work is complete. Is the evidence there?",before)
root.after(15000,lambda:show("2 / 5 — Verify claims against real local files and Git",check()))
root.after(40000,fix)
root.after(63000,tests)
root.after(80000,lambda:show("5 / 5 — Know exactly what was checked","VERIFIED: specific local evidence exists now.\n\nCONTRADICTED: local evidence conflicts with the claim.\n\nUNVERIFIABLE: insufficient evidence; never assume success.\n\nFile presence is not correctness.\nA commit is not a deployment.\nClaimed test results are not independently verified.\n\nPython standard library • Git • MIT license"))
root.after(95500,root.destroy)
root.mainloop()
tmp.cleanup()
