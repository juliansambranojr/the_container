# CONTEXT — the_container

The state of the world: what exists in this tree, what each piece
does, and where the work stands. One entry per artifact. Kept current
by the generator; edited structurally only with the operator's
approval.

## Current state of the world

Scaffolded 2026-08-25; adversarially reviewed and repaired the same
day (12 findings, all addressed). The template is complete and
self-hosting: the container's own record is kept by the container's
own rules, and both gates (`utilities/gate.py`,
`utilities/adjudicate.py`) are green. It has been instantiated once —
here. The domain-agnostic claim is a leaf with an open discharge
(entry 1).

Adjudication 001 — two theorems the kernel checks from premise P1,
over the § 1 thesis's skeleton — is exploratory: its back-translation
round is pending (entry 2).

Ratchet zero landed 2026-08-25 on the operator's word: public from
the first commit, at
<https://github.com/juliansambranojr/the_container>.

## Artifacts

### BLUEPRINT.md

The method itself — thesis, failure modes, definitions, parts,
workflow, roles, starting kit, gate adaptations by domain, refusals,
provenance. The canonical document; everything else in the tree
implements it.

### AGENT.md

The working contract for the generator, written model-agnostic. Binds
the blueprint: orientation order, roles, the ten rules, notebook and
NOTEPAD conventions, permissions template. (An earlier version of
this file said "nine rules"; the count was wrong.) The gate accepts
this file renamed to CLAUDE.md or CONTRACT.md.

### README.md

The front door: what the template is, the quickstart, the gate, the
model-agnostic construction test, provenance.

### NOTEPAD.md

The one-line index of open threads. Format is defined in its header;
statuses are the operator's.

### lab_notebook.md

The dated, append-only record. Entry 1 states what this project is,
its central claim, the falsifying artifact, and the leaf ledger.

### utilities/gate.py

The mechanical gate. Checks commitment-file presence, notebook entry
numbering, dating, and type vocabulary, and NOTEPAD line format
including that every referenced entry exists. Parses only the Threads
section of NOTEPAD and skips fenced blocks in the notebook, because
both files contain examples of themselves. Exit 0 green, exit 1 with
reasons.

### adjudications/

Kernel adjudication of argument-shaped claims — the § 8 gate for
domains without a native mechanical check. A bare Lean 4 project
(toolchain v4.32.2, zero dependencies): domain concepts as opaque
atoms, premises as named axioms, conclusions as theorems, a
zero-axiom satisfiability model, and `#guard_msgs` pins that fail the
build if a proof starts depending on an unstated assumption.

- `FORMAT.md` — the recipe: module + ledger + back-translation round,
  and the status discipline (exploratory until the round is recorded
  and the operator accepts the ledger).
- `Adjudications/ExternalVerification.lean` — adjudication 001: the
  skeleton of the blueprint's § 1 thesis. Two theorems from one
  premise (P1: some claim feels right and is incorrect); pins list
  the full atom vocabulary plus P1. The formal conclusions are
  narrower than the prose thesis — the ledger states exactly what is
  proved.
- `claims/001_external_verification.md` — 001's ledger: budgets,
  discharge routes, and one axiom rejected at sketch time
  ("whatever passes the gate is correct" — discharge unsketchable).

### utilities/adjudicate.py

The adjudications gate. Runs `lake build` (kernel + pins) and rejects
any use of `sorry`; requires every ledger's module to be in the root
import closure (lake compiles only what the root imports); enforces
theorem/pin parity and that every declared axiom appears in a pinned
list; cross-checks every pinned non-core axiom against a `### Axiom:`
ledger section; rejects orphan modules. Fails with an install hint
when `lake` is absent. Exit 0 green, exit 1 with reasons. Verified to
fire both directions.

### utilities/hooks/pre-commit

Sample hook running both gates before every commit (adjudicate.py
skipped with a notice when Lean is absent). Enabled per clone with
`git config core.hooksPath utilities/hooks`.

### utilities/break_tests.py

The gate for the gates: replays the adversarial review's break
scenarios on scratch copies of the tree and requires the gates to
fire red on each, and green on the intact tree. Run after any change
to gate.py or adjudicate.py.

### LICENSE

Apache-2.0, matching the provenance repository.

### results/

Run artifacts land here. Empty at scaffold time except its keep file.
