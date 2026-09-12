"""ECBS5293 pre-course setup check.

Run with:  uv run python check.py
Prints a report; the last line is ALL CHECKS PASSED or FIX THESE FIRST.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys

problems: list[str] = []


def line(label: str, value: str, ok: bool, fix: str = "") -> None:
    print(f"  [{'ok' if ok else '!!'}] {label:<28} {value}")
    if not ok:
        problems.append(f"{label}: {fix or value}")


def version(cmd: list[str]) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return (r.stdout or r.stderr).strip().splitlines()[0]
    except Exception as e:  # noqa: BLE001
        return f"error: {e}"


def semver(text: str) -> tuple[int, ...]:
    import re

    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", text)
    return tuple(int(x) for x in m.groups(default="0")) if m else (0,)


print(f"ECBS5293 setup check · {platform.system()} {platform.release()} · {platform.machine()}\n")

# Python that uv run picked
exe = sys.executable
py_note = "" if sys.version_info >= (3, 13) else " (works for this course, but below the 3.13 program standard)"
line("python (this one)", f"{platform.python_version()}{py_note}  {exe}", sys.version_info >= (3, 10),
     "the program standard is 3.13 and this repo pins it — `uv sync` should have fetched it; re-run with `uv run python check.py`")
line("not the Store stub", "ok" if "WindowsApps" not in exe else exe, "WindowsApps" not in exe,
     "disable the Microsoft Store python alias (Settings → Apps → App execution aliases)")
line("inside a project env", "yes" if ".venv" in exe.replace("\\", "/") else exe, ".venv" in exe.replace("\\", "/"),
     "run this with `uv run python check.py` from inside the cloned folder")

# pandas importable from THIS interpreter
try:
    import pandas as pd  # noqa: F401

    line("import pandas", pd.__version__, True)
except Exception as e:  # noqa: BLE001
    line("import pandas", str(e), False, "run `uv sync` in this folder, then re-run")

# ipykernel: without it VS Code can list this environment but cannot run a cell on it
try:
    import ipykernel  # noqa: F401

    line("import ipykernel", ipykernel.__version__, True)
except Exception as e:  # noqa: BLE001
    line("import ipykernel", str(e), False, "run `uv sync` in this folder, then re-run")

# tools on PATH
for tool, flag, minimum, fix in (
    ("git", "--version", (2, 23), "install Git >= 2.23 (Git for Windows on Windows)"),
    ("uv", "--version", (0, 4), "install uv: https://docs.astral.sh/uv/"),
):
    w = shutil.which(tool)
    v = version([tool, flag]) if w else "not on PATH"
    line(tool, v, bool(w) and semver(v) >= minimum, fix)

# git identity — without it, the first commit in Homework 2 fails
for key in ("user.name", "user.email"):
    v = version(["git", "config", "--global", key])
    ok = bool(v.strip()) and not v.startswith("error") and not v.startswith("exit")
    line(f"git {key}", v.strip() if ok else "(unset)", ok,
         f'run: git config --global {key} "YOUR {"NAME" if key == "user.name" else "EMAIL"}"')

# shell
shell = os.environ.get("SHELL", "") or os.environ.get("ComSpec", "")
if platform.system() == "Windows":
    in_git_bash = "MSYSTEM" in os.environ or "bash" in shell.lower()
    line("shell is Git Bash", os.environ.get("MSYSTEM", shell or "unknown"), in_git_bash,
         "open Git Bash (not PowerShell/cmd) and re-run — in VS Code: Command Palette → "
         "'Terminal: Select Default Profile' → Git Bash, then open a new terminal")
    crlf = version(["git", "config", "--global", "core.autocrlf"])
    line("core.autocrlf = input", crlf or "(unset)", crlf.strip() == "input",
         "run: git config --global core.autocrlf input")
else:
    line("shell", shell or "unknown", True)

print()
if problems:
    print("FIX THESE FIRST")
    for p in problems:
        print(f"  - {p}")
    sys.exit(1)
print("ALL CHECKS PASSED — this is half of the submission.")
print("\nNow the half this script cannot check: open this folder in VS Code, open check_notebook.ipynb,")
print("pick the .venv kernel, Run All, and screenshot its three outputs (README §3).")
