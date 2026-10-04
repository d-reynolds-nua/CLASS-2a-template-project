# CLASS-2a Template Project

## 1. What this is

This repository is the starting-point template for the CLASS-2a project: a
real-time, audio-driven interactive visualisation. You **fork** this
repository and build your entire project on top of it — it is not a
reference implementation to copy from, and you are not expected to build
it from scratch. The uninteresting/boilerplate parts (window setup, the
render loop, project structure) are solved for you; the parts that are the
actual point of the unit are left as stubs for you to implement across the
workshops.

This README is written to stand on its own — it does not assume you
remember anything from a lecture or workshop. If you're working from home,
outside lab hours, with nobody to ask, everything you need to get set up
should be here.

## 2. Fork and clone

**Fork this repository first**, using GitHub's "Fork" button (top-right of
the repository page on github.com). This creates a copy of it under your
own GitHub account.

**Clone your own fork — not this template.** You need your own remote to
push commits to, and later to export your submission via `git archive`.
Cloning the original template directly won't let you push anything.

Once forked, get the clone URL from **your fork's** GitHub page (the green
"Code" button → HTTPS tab), then:

**Windows 11** (PowerShell or Git Bash):
```powershell
git clone https://github.com/<your-username>/<your-fork-name>.git
cd <your-fork-name>
```

**macOS** (Terminal):
```bash
git clone https://github.com/<your-username>/<your-fork-name>.git
cd <your-fork-name>
```

**Arch Linux** (any terminal):
```bash
git clone https://github.com/<your-username>/<your-fork-name>.git
cd <your-fork-name>
```

The command itself is identical everywhere — the differences between
platforms in this project are all in *installing tools*, not in git usage
itself (covered below, and in §11).

On the **NUA lab machines**, git should already be installed — if `git` is
not recognised as a command, don't try to install it yourself (you don't
have admin rights on lab machines); contact Danny or Jawwad instead. On your
**own machine**, if you don't already have git, install it from
[git-scm.com](https://git-scm.com/downloads) (Windows/Mac) or via your
package manager (`sudo pacman -S git` on Arch).

## 3. GitHub authentication

You have an NUA-issued GitHub account, but you almost certainly don't have
an SSH key or a Personal Access Token (PAT) set up yet. This project uses
**HTTPS + a Personal Access Token** for authentication — not SSH keys, and
not GitHub Desktop. HTTPS+PAT needs no key-generation step, and a single
CLI workflow is far easier to support consistently across Windows/Mac/Arch
than a GUI app whose stored login may need re-establishing after a lab
machine wipe (see §6).

**You will need to do this more than once** — lab machine state doesn't
persist (§6), so a cached credential there can disappear. Don't treat this
as one-time setup.

### Generating a PAT

1. On GitHub, go to **Settings → Developer settings → Personal access
   tokens → Fine-grained tokens** (or "Tokens (classic)" if you prefer —
   either works for this).
2. Generate a new token, scoped to at least read/write access on your fork.
3. **Copy the token immediately** — GitHub only shows it once. Treat it
   like a password; don't commit it anywhere or paste it into chat/files
   in the repo.

### Using it with git

The first time you `git clone` (over HTTPS) or `git push` and are prompted
for credentials, enter your GitHub **username**, and for the password,
paste your **PAT** (not your actual GitHub password — that won't work).

### Caching your credential per OS

So you're not retyping the token every single push:

- **Windows:** modern Git for Windows installs come with Git Credential
  Manager already enabled — it should just work after the first successful
  authentication. If not, run:
  ```powershell
  git config --global credential.helper manager
  ```
- **macOS:**
  ```bash
  git config --global credential.helper osxkeychain
  ```
- **Arch Linux:** the simplest option with nothing extra to build is an
  in-memory cache:
  ```bash
  git config --global credential.helper 'cache --timeout=3600'
  ```
  If you want it to persist across reboots, `libsecret` is the more
  proper option, but it requires building git's `credential-libsecret`
  helper yourself (check the AUR for a prebuilt package first) — the
  cache helper above is a perfectly reasonable default if you'd rather
  not bother.

## 4. Setup

From inside your cloned fork:

```bash
uv sync
uv run python main.py
```

That's it — `uv sync` reads `pyproject.toml`, creates a `.venv`, and
installs every dependency the project needs. `uv run python main.py`
launches the project inside that environment without you needing to
manually activate anything.

(If you don't have `uv` installed yet, see
[the official install instructions](https://docs.astral.sh/uv/getting-started/installation/)
— on a lab machine, check with Danny or Jawwad first if it isn't already
present, since you won't have admin rights to install it yourself.)

**On a fresh, unmodified clone, `uv run python main.py` opens a blank
window.** The terminal prints one line saying the audio pipeline isn't
implemented yet and a blank feature source is being used instead — that's
expected, see §8. Closing the window or pressing Esc exits cleanly.

## 5. Windows lab troubleshooting note

If `uv sync` fails with an error mentioning a missing compiler or build
toolchain, this most likely means the Python version on that machine falls
outside the range this project supports (see `pyproject.toml`'s
`requires-python`). **Don't attempt to fix a missing build toolchain
yourself** — you don't have admin rights to install one on a lab machine
anyway. Contact Danny or Jawwad instead.

## 6. Working across lab and home machines

**Lab machine local state is not persistent and gets wiped
unpredictably.** Anything you haven't committed and pushed to your fork
can be lost without warning. Commit and push *frequently* — don't treat a
lab machine's disk as storage for work in progress.

Working on a **home machine** follows exactly the same steps as a lab
machine — fork, clone, authenticate, `uv sync`, run. It's not a special
case. The one thing that *is* different: don't assume anything is already
installed on your home machine just because it's present in the lab. Git,
`uv`, VSCode, a working Python installation — check for all of them
yourself and install what's missing (§2, §4, §11).

## 7. Project structure overview

```
main.py              # wires the pipeline and your chosen engine together
audio/
├── pipeline.py       # AudioPipeline — loads audio, extracts features
└── track.wav         # placeholder audio — replace with your own (§10)
engines/
├── base_engine.py    # shared engine interface + the run loop itself
├── pygame_engine.py  # PyGame engine stub
├── pyglet_engine.py  # Pyglet engine stub
└── modern_gl_engine.py  # ModernGL engine stub
```

## 8. What's implemented vs what you must implement

**Implemented for you:**
- All three engine stubs (`pygame_engine.py`, `pyglet_engine.py`,
  `modern_gl_engine.py`) open a window at a stable frame rate and close
  cleanly on window-close or Esc. They do nothing else — no drawing beyond
  a blank background.
- `engines/base_engine.py`'s `run()` method — the loop/timing mechanism
  every engine shares. You shouldn't need to touch this.

**Left for you to implement:**
- `AudioPipeline.load()` and `AudioPipeline.get_features()` in
  `audio/pipeline.py` — both currently `raise NotImplementedError`. These
  are your first tasks. They're intentionally left for you, not missing by
  accident.

Until they're implemented, `main.py` falls back to a blank feature source,
which is why a fresh clone opens an empty window and prints a "not
implemented yet" message rather than crashing. That message is telling you
where to start.

## 9. How to switch engines

Near the top of `main.py`:

```python
ENGINE: type[BaseEngine] = PygameEngine
```

Change this to `PygletEngine` or `ModernGLEngine` to switch tiers. This is
a **one-time project decision**, not something to toggle per run — commit
to one engine and build on it. Your choice should be visible in your
fork's commit history, not switched back and forth.

## 10. Where your audio file goes

Put your chosen audio file in the `audio/` directory, and update
`AUDIO_FILE` in `main.py` to point at it. The placeholder `track.wav`
shipped with this template is not meant to be your project's actual audio
— replace it with the file you're actually working with.

Your chosen audio file must be included in your final submission (it's
part of what `git archive` exports), so make sure it's committed to your
fork like any other project file.

## 11. VSCode setup

1. Install the **Python extension** for VSCode (Extensions panel, search
   "Python", the one published by Microsoft).
2. Open your cloned fork as a **folder** in VSCode (File → Open Folder),
   not as a single file.
3. Select the `uv`-managed virtual environment as your interpreter:
   Command Palette (Ctrl+Shift+P / Cmd+Shift+P) → "Python: Select
   Interpreter" → choose the one inside your project's `.venv` folder.
   This matters for IntelliSense and debugging to work correctly against
   the packages `uv sync` actually installed.
4. Run the project via the **integrated terminal** (`` Ctrl+` ``), using
   `uv run python main.py` — not VSCode's built-in Run button, which may
   not respect the `uv`-managed environment without extra configuration.

On the NUA lab machines, VSCode is likely already installed — if it isn't,
check with Danny or Jawwad rather than trying to install it yourself (no admin
rights). On your own machine, install it from
[code.visualstudio.com](https://code.visualstudio.com/).
