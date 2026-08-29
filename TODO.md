# TODO — the_container

Working specifications for container improvements not yet built.

**Why this file exists, and why it is not a second home.** `NOTEPAD.md`
is the index: one line per thread, pointer-only, and a specification
cannot be hashed out in it. `lab_notebook.md` is the append-only record:
corrections go in new entries and the original is never edited, so an
evolving spec cannot live there either. This file is mutable by design
and holds only work *not yet built*. When an item ships, it leaves here
and enters the record as a dated entry; this file is never the authority
on anything that exists.

Items are numbered for citation. Open decisions are marked
**OPERATOR** — the generator drafts, the operator decides.

---

## 1 · Mechanism glossary — fuller entries with examples

**Status:** open, unstarted.

**What.** A per-mechanism entry deeper than `BLUEPRINT.md` § 2's
one-paragraph definitions: what the mechanism is, what makes it more
than the obvious thing, what its promise precisely is, where the word
came from, and a worked instance with a file citation.

**Why § 2 is not already this.** § 2's definitions are sufficient to
*use* a mechanism you already understand. They are not sufficient to do
the two things the operator actually needs. First, to **recognize a new
instance** of a known mechanism when it appears in an unfamiliar domain
wearing a local name. Second, to **articulate the differentiation**
between two mechanisms that feel alike — the case that prompted this
item was gate versus pin, which § 2 cannot separate because it defines
only one of them.

**The exemplar.** `sidecar`, worked 2026-08-29 in conversation, is the
shape to copy:

1. **What it is, mechanically.** The file, its name, its contents.
   (`preregs/<basename>.sha256`, holding the SHA-256 of the locked text.)
2. **Two or three properties that make it more than the obvious
   thing**, each with a `file:line` citation to a real spec.
   (It *is* the lock status — `preregs/FORMAT.md:37`. It pins text the
   file itself will destroy — `:44`. So verification is a search, not a
   comparison — `:54`.)
3. **The promise, stated precisely.** What this mechanism guarantees
   that nothing else does. (No parameter, hypothesis, or decision-rule
   text drifted between locking and computing. Git already dates the
   changes; the sidecar proves the text you are reading is the text
   that was run against.)
4. **Root and specialization.** Where the word comes from in general
   use, and how this use narrows it. (A sidecar in computing is any
   file riding alongside another carrying metadata — XMP beside a RAW,
   `.asc` beside a release. Here the metadata is a hash and the hash is
   a commitment. Root intact, meaning narrowed.)
5. **The inheritance test.** *X is a ⟨mechanism⟩* — completed for this
   term. (*A sidecar is a pin.*)
6. **A live finding, where one exists.** Not decoration; it is the
   evidence the entry is describing something real and not a plan.

**The inheritance test, stated once for the whole glossary.** For any
term in any project built on this container, it should be possible to
say *"X is a ⟨mechanism⟩"* and have it be true. *hEF is a leaf.
check_refs is a gate. Crude-explicit is a budget honored. A sidecar is a
pin.* When the sentence will not complete, one of two things happened:
a genuinely new mechanism was found and belongs upstream in § 2, or the
work drifted into inventing a second name for something § 2 already has.
This is what lets domain vocabulary travel — the local meaning can move
as far as the domain requires, provided the root stays sayable.

### 1.1 · Decisions the operator owes before drafting

- **OPERATOR — home.** Does the glossary (a) replace § 2, (b) live as a
  separate file that § 2 points into, or (c) extend only the entries
  that need it, in place? Bears on § 9: a second home with no rule for
  which wins is guaranteed drift.
- **OPERATOR — scope.** Which mechanisms get the full treatment first?
  All twenty-one of § 2 is a large document that will rot; the ones
  that are confusable with each other is a small one that earns its
  keep.
- **OPERATOR — citation source.** The exemplar cites Primebeat files.
  A domain-agnostic document citing one program's paths is a coupling.
  Options: cite them as provenance and mark them so; carry an abstract
  instance and a concrete one; or keep citations out and lose the
  evidence.

### 1.2 · Candidate entries

Present in § 2, confusable, likely worth the full treatment:
gate · pin *(not yet defined — see below)* · leaf · budget ·
discharge sketch · slice · green state · ratchet commit · blind arm ·
prereg · predicate table · residue branch · verdict · perturbation ·
drift.

Proposed 2026-08-29, **unscored**, listed here so the proposal is
visible rather than adopted. § 6.1's rule applies: score before
adopting, including when the proposal is in this repository.

- **pin** — record what a claim depends on, mechanically, so a change
  in the dependency makes the claim fail loudly rather than quietly.
  Already operating under three names — `#print axioms` freezing a
  theorem's axiom set, the sidecar freezing a prereg's text, a
  dependency revision freezing an upstream. Unifying them would
  transfer § 9's lock-commit-then-run rule to every pin for free.
  *Evidence it prevents a real failure: none measured yet.*
- **weld** — composition across two systems that cannot be
  mechanically linked, with the interface stated and every crossing
  claim marked. Already has a gate and a rule in the source program.
  Strongest of the unscored four.
- **stable/mutable split** — the decision procedure that prevents
  drift, as distinct from drift itself: classify every fact before
  using it, because a recalled fact and a read one feel identical from
  inside the generation. § 3, § 8 and § 11 carry the imperative; none
  carries the procedure. Has a documented failure behind it.
- **scratch artifact** — write the shape as checkable obligations
  before the content exists, declare the incompleteness in the header,
  exclude it from every completeness claim, delete each obligation when
  the real thing lands. One recorded failure so far (a superseded
  obligation left in place).
- **paid-once record** — accumulated environment friction as a
  first-class lookup artifact, distinct from the dated record.
  Probably a § 4 part rather than a § 2 definition.

### 1.3 · Defect to repair while in the file

`BLUEPRINT.md:512` states "Eight of nine preregs in the source program
have no recoverable pre-image." The source program states four of nine
(`preregs/FORMAT.md:59`, audited entry 220), and ground truth on
2026-08-29 is eleven preregs, eleven sidecars, four baselined —
**seven of eleven verify**. The container's figure is wrong by roughly
a factor of two in the alarming direction, most likely frozen from an
audit taken before `check_sidecar.py` learned to search git blobs. It
sits in § 9, the section about hash pre-images.

---

## 2 · The itch protocol — capture at friction, discharge at a boundary

**Status:** open, unstarted. **Operator's framing, 2026-08-29.**

**The observation.** A trap noticed mid-work is an itch. You can ignore
it for a while, but eventually you have to scratch it — fix the thing —
and then apply ointment, the script or rule that stops it recurring.
Both are necessary. Neither is the hard part.

**The hard part is timing.** Fixing scaffold while executing a test
deviates the work from project to scaffold. Those are the same thing,
but moving between them costs a context switch for the model *and* the
operator. Pay that cost at the wrong moment and the exploration loses
its thread; refuse to pay it at all and the trap recurs forever.

**The protocol, therefore, is two-phase and the phases are separated in
time:**

- **At friction — capture only.** Name it, flag it, one line, keep
  working. Cheap by construction: no fix, no script, no design. The
  cost of capture must stay below the cost of the context switch, or
  the generator will skip it under load.
- **At a boundary — scratch and apply ointment.** Fix the thing, then
  build the rule or script that prevents recurrence. The context switch
  is paid once, deliberately, at a moment already dedicated to looking
  up rather than forward.

**The boundaries already exist in practice** and should be named rather
than invented: an operator asking what is open; the pre-compaction
ratchet; end of session; the index sweep. Each is already a moment when
attention has left the work and moved to the record.

**What this adds that the container lacks.** § 8's loop has no sweep
step. The ratchet preserves green states; nothing schedules remediation.
Traps therefore accumulate with no defined moment of discharge, which is
exactly what happened in the source program — the same trap
(`Iio_mem_nhds` is a membership, not an `Eventually`) bit twice in one
session because the first bite was never written down.

### 2.1 · Open questions

- **OPERATOR — naming.** "Itch protocol" is the operator's metaphor and
  is good; whether the mechanism ships under that name or a plainer one
  (deferred remediation) is a call, and the metaphor's advantage is that
  it carries the two-phase structure inside it.
- Does capture write to the paid-once record, to NOTEPAD as an `[open]`
  line, or to a third lightweight place? NOTEPAD costs an entry pointer,
  which may exceed the capture budget.
- Is the boundary set enumerable, or is it "whenever the operator asks"?
  An enumerable set can be checked; a discretionary one cannot.

---

## 3 · Trap graduation — the paid-once record is a pipeline, not a home

**Status:** open, unstarted. **Operator's framing, 2026-08-29.**

**The observation.** The trap ledger works, and it also accumulates
things that should not stay prose. Some traps are inert facts (a lemma
was renamed; nothing can automate that). Others are checkable and should
become gates. Others are procedural and should become workflow steps
that fire automatically, so the generator never has to remember them.

**So each trap carries a disposition,** assigned when it is recorded:

- **inert** — a fact to be read. Stays prose forever, legitimately.
- **gate candidate** — mechanically checkable. Enters § 6's pipeline
  and gets scored against the real corpus before adoption. Most will
  die; that is the point.
- **workflow step** — not a check but an action that belongs at a
  known stage of the loop. Fires from the chart (item 4) rather than
  from memory.

**Why the disposition matters.** Without it, the ledger's length is
ambiguous: a long ledger might mean a well-documented environment or a
large pile of unautomated debt, and nothing distinguishes them. With
dispositions, the count of ungraduated `gate candidate` entries *is*
the debt, and it is visible.

**Prior art in the tree.** § 6 already defines the scoring pipeline a
gate candidate must pass. This item connects the ledger's front end to
it; it does not propose new adoption criteria.

---

## 4 · Workflow chart with dependencies — the loop as something that fires

**Status:** open, unstarted. **Operator's framing, 2026-08-29.**

**The ask.** A chart of stages with their dependencies, so that skills
and checks fire at the stage that needs them and the generator executes
and backfills rather than reasoning about which step comes next.

**Why this is the document's own trajectory rather than an addition.**
§ 1.1 records the correction that produced the second draft: *a rule,
written down in a place the generator reads, is not a rule.* § 5.1
applied that to decision rules — prose that could not assert became a
predicate table that does. § 8's loop is still prose: nine numbered
steps a generator must read, interpret, and remember to apply. It is the
largest remaining piece of the method that is read rather than executed.

**What the chart needs to carry per stage**, at minimum: the stage's
preconditions (what must be green before it may start), what fires
automatically at it, what the generator must produce, and what may not
happen before it. The lock-commit-then-run corollary in § 9 is exactly
a dependency edge and is currently enforced by a human remembering it.

### 4.1 · Open questions

- **OPERATOR — form.** A markdown table, a diagram, or a machine-readable
  file that a hook consumes? Only the third can fail loudly, and § 1.1
  argues that the difference matters more than it appears.
- Does the chart replace § 8 or annotate it?
- Which stages already have automatic firing (the pre-commit hook, the
  invocation layer) and which are still discretionary? Enumerate before
  designing; the answer sizes the work.

---

## 5 · Port theorem/pin parity to the sibling package

**Status:** open, ready — this one is not a candidate needing a score.

**The finding, 2026-08-29.** The container's adjudicate gate already
prints `theorem/pin parity holds`. The mechanism exists here, running,
proven. It is simply not applied to `Primebeat_081426/lean_stage3`,
where an audit the same day found five modules drifted: `PerronKernel`
at 31 theorems against 5 pins, `ContourShift` 30/15, `EdgeBound` 15/5,
`ZetaGrowth` 18/8, `VonKochScaffold` 21/2, plus `LineBound` 70/10 which
predates and is already flagged in that program's roadmap.

**Why it is not a § 6 candidate.** § 6 requires scoring before adoption
because a proposed gate is a guess. This one is running in this
repository, and by § 6.1's selection rule it is the surviving kind: it
scans **mutable** source, so it goes silent when the tree is clean.

**Why it is a container item and not only a Primebeat item.** The check
is currently welded into one repository's adjudicate gate. Extracting it
as a portable utility is the container's work; applying it to the
sibling package is the test case. That split is the three-body design
(entry 9) in miniature.

---

## 6 · The itch ticker — accumulation without the model keeping score

**Status:** open, specified, **not prototyped**. Sub-item of § 2.

**The ask, 2026-08-29.** Accumulate open problems without relying on the
generator to remember them, and surface the *score* of what has not been
checked — the way a stale credential produces a system reminder: enough
to land, not enough to derail momentum.

**The inversion that makes it work.** If the generator writes the itch
lines, the file is only as good as the generator's attention and nothing
has changed. So **detectors append, the model does not.** A check runs,
finds drift, and writes its own line. The model never has to notice.
Manual capture stays available for traps no detector can see, but it is
the minority path, not the mechanism.

**Two sources, different reliability:**

- **Detected** — a non-blocking check finds a condition and records it.
  Machine-owned end to end. Pin parity is the worked example: it drifted
  across five modules of the sibling package for weeks and no human or
  model noticed.
- **Captured** — the generator hits a trap and writes one line. Cheap by
  construction (§ 2's capture budget). Still model-dependent, and known
  to be.

**Firing on age, not existence.** This is the velocity answer. An itch
recorded ten minutes ago earns silence; one carried across sessions
earns a line. The ticker is therefore quiet during flow and audible at
the boundary — § 2's timing rule expressed as a threshold rather than a
habit. Output is a **count, not a list**: `3 itches, 1 due` is under ten
tokens. The list renders only at discharge, when the operator asks.

**Why this is not NOTEPAD.** Different ownership and lifecycle.
`NOTEPAD.md` is human-owned, entry-pointed, and its status transitions
belong to the operator alone. An itch record is machine-owned, has no
entry pointer, and is **self-healing** — when the drift is repaired the
detector stops reporting it and the line clears without anyone
transitioning it. An operator-owned index and a machine-owned debt
register are not the same artifact, so this is a new part rather than a
second home (§ 9).

**Idempotency is a hard requirement.** A detector that runs fifty times
must not write fifty lines. The record is keyed on
`(detector, subject)` and updated in place, which makes it a *state*
file rather than an append-only one — the third such shape in the tree,
alongside the append-only record and the pointer-only index.

### 6.1 · Shape

- an itch record, keyed, one line per open item, carrying first-seen
  date and source (`detected:<check>` or `captured`);
- one or more non-blocking detectors that write to it and clear from it;
- a ticker that reads it and emits a one-line score, silent unless
  something is past the age threshold;
- wired into the existing hook, which already runs on Edit/Write and
  whose clean cost § 6 measured at ~28 tokens.

### 6.2 · Scoring plan, before any wiring

§ 6 requires a proposed check to be scored against the real corpus
before adoption, and § 11 refuses a check adopted because it sounds
right. This one is a notifier rather than a gate, but the failure mode
§ 6 identified applies with full force: **a ticker that fires every
session becomes wallpaper in about a week**, and wallpaper is worse than
nothing because it leaves the appearance of coverage.

What must be measured before wiring:

- **The age threshold, measured not guessed.** Replay the source
  program's history: at what age would a real itch have fired, and how
  many sessions would have seen a line? Target: silent in the large
  majority of sessions.
- **Token cost clean and firing**, against § 6's measured baseline.
- **False-positive rate of each detector**, on the real tree.
- **Self-healing verified** — repair the drift, confirm the line clears
  with no human action. An itch that needs manual closing is a NOTEPAD
  line wearing the wrong clothes.

**OPERATOR — prototype?** Building it is what scoring requires; wiring
it is what needs the operator's approval afterward. Per the
audit-before-execute split, this item stops here until you say build.

---

## 7 · (next item)

To be added.
