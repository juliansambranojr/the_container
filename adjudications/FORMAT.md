# Adjudications — format

How a claim gets kernel-adjudicated in this container, in any domain.
The kernel judges validity; the ledger holds meaning; the adversary
checks the translation between them. BLUEPRINT § 8 places this as the
gate for argument-shaped claims.

## What an adjudication is

One prose claim, one Lean module, one ledger document. The kernel
certifies exactly one thing: the stated conclusions follow from the
named premises, with nothing smuggled. Everything contested — what
the words mean, whether the premises are true — is pushed into a
short, inspectable axiom list, and each axiom carries a budget and a
discharge route.

## The three artifacts

**The module** (`Adjudications/<Name>.lean`):

- Domain concepts declared as opaque atoms (`axiom X : Type`,
  `axiom P : X → Prop`) — the kernel needs no theory of the domain.
- Each premise a named `axiom` with a docstring.
- Each conclusion a `theorem`, proved from the premises.
- A satisfiability section: a concrete model of the axiom shape,
  built with zero axioms, so the conclusions are non-vacuous. An
  axiom set with no sketchable model is a defect in the axioms —
  found here, cheaply, before anyone debates them.
- A `#guard_msgs` pin on `#print axioms` for every conclusion — the
  gate enforces one pin per theorem. The pin is the mechanically
  generated leaf ledger: a proof that starts depending on an
  unstated assumption fails the build.
- An `import Adjudications.<Name>` line added to the root
  `Adjudications.lean`. `lake build` compiles only the root's import
  closure — a module without its import line is never seen by the
  kernel, and the gate rejects its ledger.
- Bare Lean 4, no imports inside the module — the kernel stays small
  enough for anyone to install and audit.
- From claim 002 onward, consider a `structure` bundling the atoms
  and premises instead of global axioms: the satisfiability model
  then becomes a kernel-checked instance rather than a hand-checked
  analogue. Axioms remain acceptable; the ledger discipline is the
  same either way.

**The ledger** (`claims/NNN_<name>.md`):

- Header with `**Module:**` naming its Lean file — the gate uses
  this line to pair the two.
- The prose claim, quoted from its source.
- One `### Axiom: <full.name>` section per pinned axiom: what it
  says, its budget (how much load the conclusions put on it), its
  discharge route (what would establish or refute it).
- A "considered and rejected" section for candidate axioms killed at
  sketch time, so the reader sees what the argument declined to
  assume.

**The back-translation round** (recorded in the ledger): one
decorrelated reader, briefed with the module path only, renders the
formal statements back into prose; the diff against the quoted claim
is the fidelity check. This is the § 2 self-judging answer applied to
translation — the one step the kernel cannot check. Used sparingly,
on the operator's schedule: it is a fidelity instrument, and
overusing it re-prices the work toward consensus caution.

## The gate

`python3 utilities/adjudicate.py` (from the container root):

1. `lake build` in `adjudications/` — kernel and pins, red on any
   failure — and red if any declaration uses `sorry`: an unfinished
   proof is never green, even honestly pinned.
2. Every ledger's module must be in `Adjudications.lean`'s import
   closure, or the kernel never built it.
3. Theorem/pin parity per module — every `theorem` pinned — and
   every declared `axiom` must appear in some pinned list, so
   nothing slips past the ledger unpinned.
4. Every pinned non-core axiom needs a `### Axiom:` ledger section;
   every ledgered axiom must exist in some pin; every ledger's
   module must exist; no orphan modules.

## Status discipline

An adjudication is **exploratory** until its back-translation round
is recorded and the operator has accepted the axiom ledger; only then
may it be cited as adjudicated. The verdict is the operator's, as
everywhere in the container.
