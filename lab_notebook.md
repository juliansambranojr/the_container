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

## Entry 4 — 2026-08-25 — instrument — the gate detects its own bypass

**The hole.** Git never runs hooks from a tracked directory: a fresh
clone carried `utilities/hooks/pre-commit` and did nothing with it,
so every commit on that clone was ungated, silently, until the
one-time `git config core.hooksPath utilities/hooks` was run. That
knowledge lived in a quickstart step and a comment inside the hook
file — prose, guarding the one path where prose is worthless. The
operator asked whether the hooks were explicit; they were three
scattered one-liners.

**The repair, commit c7d6030.** The record gate now checks, whenever
a `.git` directory exists, that `core.hooksPath` is set — red with
the one-line fix in the message when it is unset, skipped entirely
before git init so the § 7.2 seed workflow stays clean. A clone that
skips the config now learns it on the first gate run. The hook
header and the README also state the cost profile plainly: what runs
on every commit (both gates, about a second once Lean is warm,
adjudications skipped with a notice when Lean is absent) and what
deliberately stays out (the break-test suite, which copies the tree
and rebuilds Lean per scenario; it runs by hand after any change to
the gates).

**Verification.** Two new break scenarios: git repo with hooksPath
unset fires red; with it set, green. Fifteen scenarios behave, zero
skipped; both gates green on the intact tree.

No outcome marked; transitions are the operator's.

---

## Entry 5 — 2026-08-27 — setup — BLUEPRINT second draft: execute over read

**What changed.** `BLUEPRINT.md` rewritten from 469 to 544 lines. The
first draft was written after the container had worked; this one after
it broke repeatedly in one week of hard use in Primebeat_081426. The
first draft is in git history at `367abac`.

**The finding that forced it.** The source program's governing
documents already contained the exhaustiveness rule that a prereg then
violated — with a worked example, in the layer read at the start of
every session, and with two earlier preregs in the same directory
applying it correctly days before. The defect happened anyway, drafted
by a generator that had all of it available.

So the first draft's implicit assumption — that a rule written where
the generator reads is a rule — is false. Under context pressure a
generator regenerates structure from priors rather than loading it, and
the regenerated version is fluent and subtly wrong. That is `drift`,
and prose does not prevent it. The new § 1.1 states the constraint that
follows: **prefer a mechanism that executes over one that must be
read**, and §§ 5 and 6 are derived from it.

**What is new.** § 5.1 makes a decision rule a predicate table in code
with an exactly-one-fires assertion, and names the residue branch —
because a prose rule was evaluated by hand, returned a plausible label,
and a perturbation later found the observed configuration matched no
branch at all. § 5.4 adds that a null must carry the pipeline's own
transfer function, not merely pass through the pipeline. §§ 5.5–5.9 add
comparison-set contamination, extrapolation honesty, gates whose
displayed verdict contradicts their displayed numbers,
git-before-mitigation, and whole-table reads. § 7 records that a
perturbation must attack the *concession* as well as the claim. § 9
gains the corollary that a prereg must be committed before it is run,
or its hash pins text that exists nowhere.

**§ 6 is the section with teeth, and it is empirical.** After the bad
week the generator proposed eight gates, all plausible. A perturbation
prototyped each against the real nine-prereg corpus and scored it: six
died. The table is in the blueprint with the measured numbers, and the
rule it establishes is that **a proposed gate is scored against the
real corpus before adoption** — with the token arithmetic showing why
(~1000 tokens per edit at ~90% false positives ≈ 55k tokens of noise
per session, and a noisy gate gets baselined into inertness, which is
worse than no gate).

**What was deliberately preserved.** The thesis, the four properties,
the full vocabulary (operator, leaf, budget, discharge sketch,
consensus price, slice, perturbation, stigmergy, drift), the separation
of powers, the ratchet. Those held under every load applied, and
replacing working vocabulary would have been exactly the unforced churn
the blueprint elsewhere warns against.

**Status.** Gate green. The three surviving gates in § 6 are
*recommended*, not built — the container does not yet implement them,
and the blueprint says so rather than claiming coverage it lacks. That
is the next slice.
