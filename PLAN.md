# python-refresher-2026 — the plan

## What it is

A Python refresher for people who already know the basics, aimed at getting hired,
not at teaching syntax. Every claim in the repo is checked by a test that runs in CI.

## Who it's for

Victor, and students up to masters level. People who can already write Python and want
to be paid for it. **Not beginners** — basics are deliberately out of scope.

## Why it exists

The official tutorial's last chapter is "What Now?", and its closing promise is only
that you'll be able to read and write Python modules. The Language Reference has ten
chapters; none of them are testing, typing, packaging, CI, git, debugging or
concurrency.

That gap — between *knows Python* and *hireable Python developer* — is the entire
subject of this repo.

## How every concept works

Five steps, every time. No exceptions, because the repetition is the point.

1. Victor reads the named documentation section.
2. Victor answers one prediction question **before** running anything.
3. Victor writes the file.
4. Victor runs it and reports what surprised him.
5. Test, then commit.

**Rule on me: six lines of explanation per concept, maximum.** If it runs longer, say
"too long" and it gets cut. This exists because I already burned a session on `.gitignore`
forensics instead of teaching.

**Rule on the repo: if something surprised Victor, it becomes a test.** Not the things
he already knew — only the surprises. That is what makes the repo worth reading.

## Roles

| | Does |
|---|---|
| **Victor** | Creates the folder, initialises git, writes every line under `units/` and `tests/`, commits per unit |
| **Me** | Names the doc section, asks the prediction question, reviews the diff, writes config and prose files only when asked |

I do not write code. If I write anything, it is a correction to something already written
— never a starting point.

## Phase 0 — scaffold

Mechanical. No learning, no concepts. Ends when there is a commit and a public remote.

- [ ] Folder created, `git init`, opened in VS Code
- [ ] `pyproject.toml` via `uv init`
- [ ] Virtual environment created — and *seen* being created
- [ ] `pytest` and `ruff` added
- [ ] `.gitignore` written by hand
- [ ] `README.md`
- [ ] `PLAN.md` (this file)
- [ ] First commit
- [ ] Public GitHub remote
- [ ] CI workflow, badge green

## The units

Fourteen units, three stages, one appendix. One unit = one commit.

### Stage A — working like a professional
*The part every course skips. This stage comes first on purpose.*

| | Unit | What it buys you | Done |
|---|---|---|---|
| A1 | Environments and packaging | A repo someone else can clone and run | ☐ |
| A2 | Testing with pytest | The strongest hireability signal in Python | ☐ |
| A3 | Types and static analysis | Catching bugs before review | ☐ |
| A4 | Lint, format, CI | Working to a team standard, automatically | ☐ |
| A5 | Git for collaboration | Surviving a real pull-request review | ☐ |

### Stage B — the Python that interviews probe

| | Unit | What it buys you | Done |
|---|---|---|---|
| B1 | Execution model — names, objects, mutability, scope | Answering "why did this mutate?" correctly | ☐ |
| B2 | Data structures and cost | Not writing O(n²) by accident | ☐ |
| B3 | Iteration, generators, laziness | Processing data that doesn't fit in memory | ☐ |
| B4 | Functions in depth — closures, decorators, `functools` | Reading any framework's source | ☐ |
| B5 | Errors and context managers | Failures that are diagnosable, not silent | ☐ |
| B6 | OOP and the data model | Designing types people can't misuse | ☐ |
| B7 | Concurrency — choosing a model | Picking from the workload, not preference | ☐ |

### Stage C — the parts nobody teaches

| | Unit | What it buys you | Done |
|---|---|---|---|
| C1 | Debugging and profiling | Finding the bug *and* the bottleneck | ☐ |
| C2 | The standard library 20% | Not reinventing what ships with Python | ☐ |

### Appendix

| | Item | Why | Done |
|---|---|---|---|
| — | The 3.8 → 3.14 delta | Interviews and codebases are on mixed versions | ☐ |

## Per-unit shape

**Two files, not four.** The teaching text lives in the module docstring.

- `units/aNN_topic.py` — runnable *and* importable. Running it prints every demo with
  its result, so a reader can open a single file and see what it does.
- `tests/test_aNN.py` — asserts the claims in that docstring.

No `src/` layout, deliberately. Any reader must be able to open one file and run it
without understanding packaging.

## The skip list

This is a feature, not an omission. It goes in the README.

Syntax basics · `for` and `while` · what a variable is · list methods · f-string syntax ·
"build a to-do app" · OOP taught through animals · notebooks · data science · machine
learning · web frameworks.

**You can find all of it anywhere. That is the point.** The skip list is the positioning.

## Standards, from the first commit

- `uv` with `pyproject.toml`; lockfile committed, virtual environment never
- `ruff` for lint and format, line length 100, target `py314`
- `pytest` for tests
- GitHub Actions on 3.14
- MIT licence
- README: CI badge, the hook, the unit table, the skip list
- **No stubs.** Every unit is complete when committed. A half-built repo is worse than
  no repo — so this is portfolio-grade from commit one, not "finished later".
- Beginner-facing units avoid 3.14-only syntax so students on 3.10+ can follow. 3.14
  features go in callouts and the appendix.

## Boundary

This is a refresher, not a course. It has a deliberate end.

- **One unit in flight at a time.** No parallel units, no starting B3 while A2 is open.
- **If a unit turns out to be already known, skip it and say so in the commit message.**
  "Already knew this" is a legitimate result, not a failure.
- **Measure shipped units, not sessions spent.** The commit history is the evidence.
- When the fourteen units are done, the repo is done. The next thing after it is the
  security work, not a fifteenth unit.
