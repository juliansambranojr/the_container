# Mechanism glossary — DRAFT

**Not authoritative. Placement undecided.** This is a draft against
TODO item 1, written 2026-08-29. It is not `BLUEPRINT.md § 2`, does not
supersede it, and nothing should cite it. The three operator decisions
in TODO § 1.1 — home, scope, citation source — are open, and this file
exists to make them decidable by example rather than in the abstract.

Citations to `Primebeat_081426` are included and marked. If the abstract
route is chosen they strip out cleanly; adding them later would cost a
re-derivation, so they are here by default.

Six entries. The set is a sample, not a scope decision — § 7 records what
was deferred and why.

---

## gate

**Mechanically.** An executable check that exits zero or nonzero, wired
to run automatically. A compiler, a proof kernel, a test suite, a
reference checker, a decision rule's partition assertion.

**What makes it more than a test.**

1. **It must be able to fail in both directions.** `BLUEPRINT.md:81` —
   "a gate that can only pass is decoration." A check that cannot
   distinguish states is a ritual with an exit code.
2. **It is scored against the real corpus before adoption.** § 6 records
   eight plausible checks proposed after a bad week; **six died on
   contact**. A gate's cost is paid on every invocation forever, and a
   noisy one gets baselined into inertness — worse than no gate, because
   it leaves the appearance of coverage.
3. **The surviving kind scans mutable state.** `BLUEPRINT.md:6.1`, found
   by building rather than by reasoning: every gate that shipped scans
   source, links, or sidecars against git; every one that died scans the
   append-only record. A record-scanning gate can never be silent when
   clean, because a true positive in a historical entry fires forever and
   the entry cannot be edited to fix it.

**The promise.** Not that claims are true. That **an unchecked claim
cannot enter the record silently.** The gate is indifferent to how
confident the claim sounded.

**Root and specialization.** A gate in general use is a barrier
controlling passage. Here what passes is a *claim*, and the gatekeeper is
mechanical rather than a person — which is the whole point, since a
person reviewing fluent output is exactly the thing that fails.

**Inheritance test.** *check_refs is a gate. The pre-commit hook is a
gate. Double-entry bookkeeping is a gate.*

**Live.** Measured cost for the container's full set: 0.03–0.05 s and
~28 tokens when clean, ~700 firing (`BLUEPRINT.md:417`).

---

## pin

**Status: candidate. Unscored.** Proposed 2026-08-29, not present in
§ 2. Listed in TODO § 1.2 with the same caveat. Drafting it is itself a
test — a mechanism that cannot be written crisply is usually not one.

**Mechanically.** A recorded, machine-checkable statement of what a
claim depends on, stored so that a change in the dependency breaks
something loudly.

**What makes it more than a gate — this is the motivating case.**

A gate asks *"is this property true right now?"* A pin asks *"is this
the same thing it was?"* A gate checks a property; a pin freezes a
surface. **A gate can pass on a changed thing.** A pin cannot, because
being unchanged is the entire content of what it asserts.

Three instances already operating under three names:

1. `#print axioms` wrapped in `#guard_msgs` — freezes a theorem's axiom
   dependencies. If a proof starts depending on `sorryAx`, the build
   breaks rather than passing.
2. **A sidecar** — freezes a prereg's locked text as a SHA-256, so no
   parameter or decision-rule text can drift between locking and
   computing.
3. **A dependency revision** — freezes an upstream at a commit, so the
   ground under a formalization does not move underneath it.

**The promise.** A change in what a claim rests on cannot happen
quietly.

**Root and specialization.** To pin is to fix in place so a thing cannot
move. Here what is fixed is a *dependency surface*, and the fixing is a
recorded value — a hash, an axiom list, a revision — rather than a
physical constraint.

**Inheritance test.** *A sidecar is a pin. An axiom pin is a pin. A
lockfile is a pin.*

**Live, and it is the argument for the mechanism.** On 2026-08-29 an
audit found `theorem`/`#print axioms` parity broken in five modules of
`Primebeat_081426/lean_stage3` — `PerronKernel` at 31 theorems against 5
pins. The pins that existed were correct. **Nothing checked whether they
were complete**, so the gap stood for weeks in the file carrying the
central claim.

That is the composition: **a pin freezes, a gate notices.** A missing
pin is invisible without a gate, and a gate has nothing to compare
against without a pin. They are different mechanisms and they need each
other — which is why § 2 defining only one of them left the pair
indistinguishable.

---

## leaf

**Mechanically.** A named open assumption the work stands on, stated as
a proposition rather than prose, carrying two things from birth: a
budget and a discharge sketch (`BLUEPRINT.md:104`).

**What makes it more than a TODO.**

1. **The discharge sketch is required at naming time**, not later.
   `BLUEPRINT.md:112` — and the reason is that it finds defects cheaply:
   "a leaf whose discharge cannot be sketched is usually a defect in the
   leaf." In the source program this exposed two unsatisfiable
   assumptions in a single session, at the cost of ten minutes each.
2. **A leaf is never discharged by argument.** *(Primebeat
   `CLAUDE.md:162`)* — "never call a leaf discharged without a pinned
   theorem." The transition from open to closed is mechanical.
3. **The ledger is countable.** Because leaves are named, "what are we
   assuming" has an answer with a length, rather than being distributed
   through prose where it cannot be audited.

**The promise.** What the work stands on is enumerable. An assumption
cannot hide inside a paragraph.

**Root and specialization.** From the tree — a terminal node with
nothing below it. The specialization is *terminal for now*: a leaf is
where the proof tree stops because nobody has extended it, not because
it cannot be extended. That is what makes a discharge sketch meaningful
rather than wishful.

**Inheritance test.** *hEF was a leaf. StmtArgCrude is a leaf. An
unproven lemma cited as "standard" is an unnamed leaf.*

**Live.** The ledger read `{hEF, StmtArgCrude}` from entry 141 until
2026-08-29, when hEF was discharged by a pinned theorem *(Primebeat
notes entry 271)* and the ledger became `{StmtArgCrude}`. The census had
priced hEF as absent from every proof assistant.

---

## budget

**Mechanically.** The measured tolerance of the downstream consumer:
how wrong, how crude, how large can this piece be before the thing that
uses it stops working. **Obtained by running the consumer**, never
estimated from reputation (`BLUEPRINT.md:107`).

**What makes it more than an estimate.**

1. **It is the instrument that distinguishes a scope call from an
   echo.** `BLUEPRINT.md:117` — a consensus price is the difficulty a
   task inherits from its reputation. A budget is a measurement. Calling
   something out of scope without one is repeating what the field says.
2. **It licenses crude answers.** *(Primebeat `CLAUDE.md:169`)* —
   "constants are chosen for provability, not sharpness. 97 where Rosser
   has 0.137 is a success, because the census re-tabulates and
   survives." Chasing sharpness the consumer does not need is scope
   creep wearing rigor's clothes.
3. **It is measured before the scope call, not after.** The order
   matters: a budget computed to justify a decision already made is not
   a measurement.

**The promise.** "Out of scope" becomes a number rather than a
reputation.

**Root and specialization.** A budget in general use is an allowance you
spend against. Here what is being spent is **wrongness** — how much
error the downstream consumer will absorb before failing.

**Inheritance test.** *Crude-explicit is a budget honored. An error bar
is a budget. A latency SLA is a budget.*

**Live, and it is the clearest instance in the corpus.** The census
priced the explicit-formula leaf at months minimum, echoing the
literature's difficulty for *sharp* constants. The budget — measured
against the consumer, which re-tabulates and survives crude ones — said
the required precision was a different difficulty class. The leaf was
discharged in a night's work *(Primebeat notes entries 257–271)*. The
consensus price was not wrong about sharp constants; it was answering a
question the consumer had not asked.

---

## slice

**Mechanically.** A unit of work no larger than one green build
(`BLUEPRINT.md:120`).

**What makes it more than a task.**

1. **It is sized by verification capacity, not by content.** The cut is
   made where the work can reach a checked state, whatever that work
   happens to contain. A slice is not "a reasonable chunk"; it is
   "as much as can be made green at once."
2. **It is named and priced before it is built**, and it either lands
   pinned or is recorded as still open. A slice that quietly becomes two
   slices has stopped being one.
3. **It is what makes belief safe** — `BLUEPRINT.md:120`, and this is
   the load-bearing relation. Pressure without slicing risks ground;
   slicing without pressure stalls at the consensus price. Neither half
   works alone.

**The promise.** You can be pushed hard without risking ground, because
the largest thing that can go wrong is one build.

**Root and specialization.** A slice is a portion cut from a whole. The
specialization is *where the cut falls* — at the boundary of what can be
verified in one pass, rather than at a natural boundary in the material.

**Inheritance test.** *hEF's four slices were slices. A commit that
builds is a slice. A refactor spanning three days is not.*

**Live.** Across entries 257–271 the majority of large blocks compiled
on their first or second pass. Each had been sized to one build and
scouted for names before it was written.

---

## blind arm

**Mechanically.** A region of the possibility space nobody has examined,
**stated as something checkable rather than asserted**
(`BLUEPRINT.md:140`, § 5.3).

**What makes it more than a promise.**

1. **"We have not looked" is unverifiable, and from a generator it is
   worthless.** § 5.3 gives the mechanical forms instead: code that
   drops the values before any statistic is computed; an analysis mode
   that refuses to run without an explicit confirmation flag, with the
   refusal exercised; commit history showing no value was computed at
   any measured site.
2. **What is blind must be stated precisely, because the sloppy version
   overclaims.** *(Primebeat
   `preregs/floor_reconstruction_v1_20260828.md:83`)* — "x ∈ [512, 2048):
   never computed by any script in this repository. This is the blind
   arm. The zeros file itself is **not** blind (read many times); the
   blindness is in the x-range." A claim that the whole dataset was blind
   would have been false and unfalsifiable at once.
3. **It is what makes a preregistered result more than a prediction.**
   Without it, a locked rule can still be applied to data whose shape is
   already known.

**The promise.** The honesty of a preregistered test does not rest on
anyone's word — not the operator's, and not the generator's.

**Root and specialization.** From clinical trials, where blinding hides
the treatment assignment from the assessor. The specialization: here it
is not a person who is blinded but a **region of the data**, and the
blinding is enforced by code rather than by protocol.

**Inheritance test.** *The floor prereg's x-range was a blind arm. A
held-out test set is a blind arm. A three-body project not yet chosen is
a blind arm.*

**Live.** The floor-reconstruction prereg's blind arm was the x-range,
stated with the non-blind part named alongside it, and the mechanical
form was that no script in the repository had computed on that range —
checkable from the commit history by a stranger.

---

## § 7 · What was deferred, and why

Not a scope decision — a note on what this sample leaves out, so the
operator's choice in TODO § 1.1 is informed rather than inherited.

**Deferred as well covered by § 2 already:** `operator`, `generator`,
`commitment files`, `record`, `index`. Short definitions serve these;
the confusion they cause is low.

**Deferred as needing a decision first:** `verdict` and `perturbation`
both describe *powers*, and § 7 of BLUEPRINT already treats them at
length. Whether a glossary entry duplicates or replaces that is the
home question, unresolved.

**Deferred for lack of live evidence today:** `predicate table`,
`residue branch`, `discharge sketch`, `consensus price`, `drift`,
`stigmergy`. Each is real; none was exercised in a way that would give
the entry a live finding, and an entry without one is a plan rather than
a description.

**Not drafted because unscored:** `weld`, `stable/mutable split`,
`scratch artifact`, `paid-once record` — the four remaining candidates
from TODO § 1.2. `pin` was drafted only because the gate/pin confusion
is the case that motivated the item, and writing it was the test of
whether it is a mechanism at all.
