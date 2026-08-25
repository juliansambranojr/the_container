# the_container

A template for durable work with a fluent generator — an AI model, or
any collaborator who produces faster than they verify. The method is
described in [BLUEPRINT.md](BLUEPRINT.md); this repository is the
method's own starting kit, ready to copy.

The core inversion: the default workflow is a generation engine with
optional verification. The container is a verification engine with
generation as its fuel. State lives in files. Claims enter the record
through gates. The powers are separated. Progress is a ratchet.

## What's in the box

```text
BLUEPRINT.md       the method — thesis, parts, definitions, workflow
AGENT.md           the working contract for whatever model you use
CONTEXT.md         the state of the world, one entry per artifact
REFERENCES.md      every cited document and dependency, with paths
NOTEPAD.md         one status-tagged line per open thread
lab_notebook.md    the dated, append-only record
utilities/gate.py  the mechanical gate — exits 0 when the record
                   is self-consistent, 1 with a reason when it fails
adjudications/     kernel adjudication of argument-shaped claims:
                   premises as named axioms, conclusions as theorems,
                   pinned axiom lists, one ledger per claim
                   (format: adjudications/FORMAT.md; gate:
                   utilities/adjudicate.py, needs Lean 4 via elan)
results/           run artifacts land here
```

## When to move in, and the smallest start

The container becomes useful at the first claim you would mind
losing — before that, explore freely without it (BLUEPRINT § 7.1).
And the true minimum is smaller than this repo: a git repository,
one notebook whose entry 1 names the idea, its assumptions, and the
smallest artifact that would prove it wrong, and the commit habit
(§ 7.2). The full kit below is what that seed grows into.

## Quickstart

1. Copy this folder (or use it as a template repository) and rename it
   for your project.
2. Open `AGENT.md` and fill in the permissions section for your
   domain. Point your model at it — the file is the contract, and any
   model that can read a file can honor it. Rename it `CLAUDE.md` or
   `CONTRACT.md` if your tooling prefers; the gate accepts all three.
3. Replace `lab_notebook.md` entry 1 with your own: what the project
   is, and the smallest artifact that would falsify its central claim.
   If you cannot name that artifact, that is your first open thread.
4. Name your leaves — every assumption the idea stands on — each with
   a measured budget and a sketched discharge (BLUEPRINT § 3 defines
   these; § 7 walks the setup).
5. Build the strongest gate your domain admits (BLUEPRINT § 8 maps
   common domains) and add it beside `utilities/gate.py`.
6. `git init`, then `git config core.hooksPath utilities/hooks` so
   the gates run before every commit. Commit the green state, add a
   remote, push. That is ratchet zero. Start the loop (BLUEPRINT § 5).

## What to keep, what to replace

This repo practices its own method, so it ships with its own state.
When you instantiate:

**Keep:** `BLUEPRINT.md`, `AGENT.md` (edit permissions), `LICENSE`,
`utilities/`, `adjudications/FORMAT.md`, `.gitignore`.

**Replace with your own:** `lab_notebook.md` (entries 1–2 are the
container's — replace both), `NOTEPAD.md`'s thread lines (both are
the container's), the body of `CONTEXT.md` and `REFERENCES.md`, and
this README.

**Your choice:** `adjudications/` beyond FORMAT.md — claim 001 and
its module are the container adjudicating its own thesis; keep them
as a worked example or delete the pair (ledger and module together,
plus the import line in `Adjudications.lean`). The whole
adjudications layer is optional; without Lean installed,
`adjudicate.py` says so and `gate.py` runs fine alone. To use it,
install Lean 4 via elan (<https://github.com/leanprover/elan>).

## The gate

```bash
python3 utilities/gate.py
```

Checks that the commitment files exist and are non-empty, that
notebook entries are sequentially numbered, dated, and typed from the
contract file's vocabulary, and that every NOTEPAD thread line is
well-formed and points at an entry that exists.

The pre-commit hook at `utilities/hooks/pre-commit` runs both gates
on every commit (the adjudications gate takes about a second once
Lean has built, and is skipped with a notice when Lean is absent).
One thing git will never do for you: hooks in a tracked directory do
not activate on clone. That is why quickstart step 6's
`git config core.hooksPath utilities/hooks` exists — and why gate.py
goes red on any clone where it hasn't been run: an ungated commit
path is not allowed to stay silent. `utilities/break_tests.py` is
deliberately outside the hook (it copies the tree and rebuilds Lean
per scenario); run it by hand after any change to the gates.

## Model-agnostic by construction

Nothing here depends on which generator you use. The contract file is
named `AGENT.md`; the substrate is plain text under version control;
the test is in BLUEPRINT § 7 — swap the generator entirely, different
model or different person, and the workflow keeps working from the
tree alone.

## Provenance

Built and stress-tested in
[Primebeat_081426](https://github.com/juliansambranojr/Primebeat_081426),
a measurement bench and Lean 4 formalization program whose notebook
shows the container operating, corrections included.

The method is the container. The ideas are yours.
