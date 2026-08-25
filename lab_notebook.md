# Lab notebook — the_container

The dated, append-only record. Entry header format and the type
vocabulary are defined in `AGENT.md`. Outcome markings are the
operator's.

## Entry 1 — 2026-08-25 — setup — the container, instantiated on itself

**What this project is.** A domain-agnostic template for the method
described in `BLUEPRINT.md`: durable work with a fluent generator,
secured by state-in-files, mechanical gates, separated powers, and
ratchet commits. This tree is the starting kit made real — commitment
files, notebook, index, and one working gate — ready to be copied
into any project.

**Central claim.** The container works independently of domain and of
generator: copy the tree, adapt the permissions and the gate, and the
workflow holds whether the generator is this model, a different
model, or a person.

**Smallest falsifying artifact.** A fresh instance — different model
or different person — handed only this tree, that fails to
reconstruct the operating contract and continue the loop. The
auditability test from the blueprint: the commitment files alone must
recover full orientation. If they do not, the substrate has hidden
state and the central claim is false.

**Leaf ledger at birth.**

- *Leaf: domain-agnosticism.* The method has operated in exactly one
  domain (formal mathematics with a numerical bench). Budget: one
  honest instantiation in a domain without a proof kernel — writing,
  strategy, design — surviving to its tenth ratchet commit without
  the gates being abandoned. Discharge sketch: run the § 7 starting
  kit on such a project; the § 8 table names the gate to build; the
  tenth green commit discharges the leaf, and an abandoned gate
  refutes it.

**Provenance.** Method built in Primebeat_081426 (see
`REFERENCES.md`); blueprint written 2026-08-25; structure scaffolded
the same day. Gate `utilities/gate.py` green at scaffold time.

## Entry 2 — 2026-08-25 — instrument — kernel adjudication for argument-shaped claims

**What was built.** `adjudications/` — the § 8 gate for domains
without a native mechanical check, proof of concept included. Bare
Lean 4 (v4.32.2, zero dependencies): domain concepts as opaque atoms,
premises as named axioms, conclusions as theorems, a zero-axiom
satisfiability model, `#guard_msgs` pins on every conclusion's axiom
list. `utilities/adjudicate.py` couples kernel to ledger: build
green, every pinned axiom documented with budget and discharge route,
no orphan modules. `FORMAT.md` fixes the recipe for claim 002 onward.

**Adjudication 001.** The blueprint's own § 1 thesis. From the single
premise P1 — some claim feels right and is incorrect — the kernel
checks both halves: an internal-only acceptance policy admits an
incorrect claim, and any sound policy must reject something that
feels right. Budget on P1 is total and its discharge is empirical,
already witnessed by dated corrections in the provenance program's
notebook. One candidate axiom ("whatever passes the gate is correct")
was rejected at sketch time as undischargeable.

**The pin fired during construction.** The hand-written axiom list
mismatched the compiler's and the build failed until the pin carried
the truth — the full atom vocabulary plus P1. The instrument caught
its author on first contact.

**Both gates verified in both directions.** Green on this tree; red
on scratch copies broken deliberately (missing ledger section, orphan
module; and for gate.py: missing commitment file, broken numbering,
bad type, dangling entry reference, bad status).

**Status.** 001 is exploratory until its back-translation round is
recorded and the operator accepts the ledger. The blueprint § 4.4
gained the operator's rationing rule: the adversarial round is
scheduled, never ambient — overuse re-prices the trajectory toward
consensus caution.

## Entry 3 — 2026-08-25 — audit — the adversarial review, and what it broke

**The review.** Before ratchet zero, on the operator's instruction, a
decorrelated reader was briefed with file paths only and told to
break the repository: legibility for a stranger, and the build.
It ran its own break-tests on scratch copies, attacked its own
findings before reporting, retracted 5, and returned 12. Its summary
line was the finding that mattered: the prose describing the gates
was stronger than the gates — in a repository whose thesis is that
prose confidence is worthless.

**The sharpest findings.** Three ways to pass the adjudication gate
falsely: a module never imported into the root file is never
compiled, so a fabricated pin with a matching ledger certified
GREEN; an unpinned theorem could smuggle any axiom past the ledger;
and `sorryAx` sat in the core-axiom allowlist, so an unfinished
proof, honestly pinned, passed. Beyond those: the record gate
contradicted the blueprint twice (contract filename hardcoded, empty
thread section rejected — following § 7's own instantiation steps
produced a red gate), a one-character pointer typo silently defeated
the dangling-reference check, an unclosed code fence hid everything
after it, no license on a repository whose pitch is "copy this
folder," and the quickstart left an adopter shipping the template's
own state.

**The repairs, all landed before ratchet zero.** The adjudication
gate now requires import-closure membership, theorem/pin parity,
declared-axiom coverage, and rejects `sorry` everywhere. The record
gate accepts three contract filenames, allows an empty thread
section, parses the type vocabulary from the contract file itself,
and reds on unclosed fences and unpointed entry mentions. LICENSE
(Apache-2.0), the keep/replace checklist, the elan pointer, and the
pre-commit hook shipped. The review's break scenarios became the
permanent regression suite — 13 scenarios, replayed on scratch
copies, each required to fire; the gates now gate the gates.

**Correction.** Entry 2 said the kernel checks "both halves" of the
§ 1 thesis. Overstated: the kernel checks two theorems over the
thesis's skeleton, and the positive half of the prose is stronger
than `sound_overrules_somewhere`, which a reject-everything policy
satisfies vacuously. The ledger stated this correctly; the entry's
summary sentence inflated it. This entry is the correction.

**What the audit demonstrated about the method.** The pin fired on
its author during construction (entry 2); the review fired on the
gates before they could certify anyone else. Both catches are the
container behaving as specified — the characteristic error is
invisible to its author, and only decorrelated mechanism finds it.

No outcome marked; transitions are the operator's.
