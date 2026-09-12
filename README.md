# ECBS5293 — Pre-course setup check

**Due before Session 1.** This takes ten minutes if your machine is set up and tells you exactly what is missing if it is not. Session 1 cannot be tech support.

## 1. Tools

The **program prep session** installs everything: Python 3.13, `uv`, VS Code, Git, and a GitHub account. If you attended it, skip straight to §2. If you missed it, the course site's *Pre-course setup* page has the per-OS install steps — in short: Git (Git for Windows on Windows, which includes **Git Bash** — the terminal this course uses; not PowerShell, not cmd, not Anaconda Prompt) and `uv`. Python 3.13 arrives by itself: this repo pins it, and `uv sync` fetches it.

You will have a GitHub account from the prep session; this course itself only needs you to *clone* public repositories — you never push to GitHub, and all submissions go through Moodle.

Windows only, before cloning anything: `git config --global core.autocrlf input`

## 2. The check

Open your terminal (macOS Terminal / Git Bash), then:

```bash
git clone https://github.com/earino/ecbs5293-setup-check.git
cd ecbs5293-setup-check
uv sync
uv run python check.py
```

Expected: a short report ending in **`ALL CHECKS PASSED`**. Copy the whole output (or screenshot it). That is half of what you submit; §3 is the other half.

If it ends in `FIX THESE FIRST`, each failing line says what to do. Fix, re-run, submit when it passes. If you are stuck, the "uv install troubleshooting" office-hours slot is in the week before Session 1 — come with the output.

## 3. Run the notebook — the part the script cannot check

Seeing `.venv` in a kernel list does not prove VS Code can *run* a cell on it. So run one.

1. Open **this folder** in VS Code (*File → Open Folder…*, not the notebook file).
2. Open `check_notebook.ipynb`.
3. Click **Select Kernel** (top right) → *Python Environments…* → the entry marked **Recommended** whose path contains **`.venv`**.
4. **Run All.** Three outputs appear: a path containing `.venv`, a pandas version, and this folder.

Screenshot those three outputs. **Submit the screenshot and the §2 report together** to the Moodle "Setup verification" slot.

That folder-then-`.venv`-kernel routine is the *Notebook standard* on the course site's setup page, and it is how every course notebook runs. On Windows, also set VS Code's default terminal to Git Bash: Command Palette → *Terminal: Select Default Profile* → **Git Bash**.

## What this proves

`uv sync` installed this project's packages into an environment of its own; `uv run` found that environment's Python (3.13, the program standard); that Python can import pandas; VS Code can execute a cell on that same environment, which is the workflow Lab 1 starts with; and Git knows who you are, so your first commit in Homework 2 will work. You will learn what each step does in Session 2.

## Windows notes

- **Never type bare `python` in Git Bash.** On some setups it hangs with no error; on others it drops you into Python's `>>>` prompt (type `exit()` to leave). Do not find out which you have: always `python --version`, `python -c "..."`, `python script.py`, or `uv run python …`.
- If the check reports a `WindowsApps` path, that is the Microsoft Store stub, not a real Python: *Settings → Apps → Advanced app settings → App execution aliases*, turn off both `python` entries, re-run.
