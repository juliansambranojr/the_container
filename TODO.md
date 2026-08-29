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
  Machine-owned end to end. Two known candidates: **pin parity**, which
  drifted across five modules of the sibling package for weeks with no
  human or model noticing; and **unrecorded run** — a results artifact
  exists and no record entry cites it — which is the backstop for
  § 7.7's silent-miss failure. Two detectors is the minimum that makes
  the ticker worth building over a plain gate.
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

## 7 · Structured emission — synthesize once, render twice, file by parser

**Status:** open, specified. **Operator's framing, 2026-08-29.**

**The ask.** The generator emits one structured response that a parser
routes to its destinations — record entry, index line, trap record,
open items — instead of writing each by hand. Revisions and reframes
arrive in an append format that parses the same way. An explicit
off-record channel keeps adjacent or benign dialogue out of the record
without suppressing it.

**Prior art, and how it differs.** `Primebeat_081426/utilities/
extract_run.py` already stages a record entry from the transcript window
around a run, leaves `type:` for a human to choose from the documented
vocabulary, and refuses `--append` until it is chosen. It works in the
opposite direction: it **reconstructs after the fact**, so it must infer
what happened. This item has the generator **emit while it still knows**.

They compose rather than compete. Emission is the primary path;
extraction is the recovery path for a session where nothing was emitted.
Building the emitter does not obsolete the extractor.

### 7.1 · The refinement: the saving is in synthesis, not in text

The operator's reasoning is that answering *and* writing the entry costs
twice the thinking. The cost is real, and it sits in the **synthesis** —
deciding what happened and what mattered — not in the rendering.

An entry and a reply have different readers. The entry is for a stranger
six months out with no shared context; the reply is for the operator now,
with all of it. Collapsing them into one text produces either entries
that read like chat (context-dependent, opaque later) or chat that reads
like a filing.

**So the format carries the synthesis once and permits two renderings.**
The generator decides what happened a single time; the parser and the
reply draw from the same decided content in different shapes. This
preserves the saving without flattening two audiences into one — and it
removes the failure where the chat summary and the entry quietly
disagree, because they can no longer be independently authored.

### 7.2 · Hard constraints

- **The parser refuses verdicts and status transitions.** Entries and
  `[open]` lines are generator-writable and always have been. Verdict
  lines and `[open] → [closed]/[paused]/[blocked]` are the operator's
  alone (§ 7, § 11). A parser able to write those has moved a power
  across the line the container is built on. This is a constraint on
  the implementation, not a preference.
- **Malformed blocks fail loudly.** A block that does not parse must
  error, never drop silently. Otherwise "I filed it" and "it was filed"
  diverge, which is precisely the failure the record exists to prevent.
- **Type is never guessed.** The extractor's existing rule holds: the
  vocabulary is fixed, and an entry fitting no type is flagged to the
  operator, not assigned one.

### 7.3 · Marker visibility

**OPERATOR — decide.** The proposal allows silent markers, so the reply
reads as ordinary prose while remaining parseable.

*Recommendation: visible markers.* Invisible machine-executed state
contradicts the method's first property — state lives in plain files,
legible where it acts. A misfiring silent marker fails silently: text
routes to the wrong destination or nowhere, and the discovery comes
months later when the record is missing something the operator is
certain was filed. A visible delimiter costs little to read and makes
misfires obvious at the moment they happen.

### 7.4 · Off-record

Worth stating plainly: this creates no hiding place, because **nothing
is filed today until the operator says so.** What changes is *when the
writing happens* — synthesis is emitted and parked while it is fresh,
then filed on the operator's word rather than reconstructed later.

The rule that keeps it honest: on-record is marked, off-record is the
default, and the generator never moves something already emitted as
on-record into off-record.

### 7.5 · Synthesis on arrival

**The operator's second idea, and it is separable from the rest.**
Entries accumulate along a line of work. When that work **lands** — a
theorem proved, a script shipped, a mechanism named — a synthesis entry
compresses the chain and points at the final object. Navigation is then
by object; provenance stays recoverable by following the chain back.

This already happens informally in the source program (an entry closing
an arc narrates the entries behind it) but it is prose, so the chain is
not machine-navigable. Making it a field in the entry header —
`synthesizes: 257–271`, or similar — is cheap and makes the compression
checkable: every entry in a synthesized range should be reachable, and a
synthesis naming a range with a gap is a defect a gate could catch.

**Constraint:** synthesis compresses navigation, never the record.
Superseded entries are never edited or removed (§ 11). The chain stays;
only the entry point moves.

### 7.6 · Open questions

- Which destinations does the format cover in v1? Record entry and index
  line are the minimum; trap record and open items may follow once § 3
  and § 6 settle their shapes.
- ~~Does the parser run as a hook, a command, or both?~~ **Resolved
  2026-08-29: a skill, triggered by the task** — see § 7.7. A hook files
  without asking (conflicts with § 7.4); a typed command reintroduces
  the friction the item exists to remove. A task-triggered skill fires
  when the work reaches a filing moment, which is the operator's word
  expressed as a task.
- Does the append format revise an entry, or does it always create a new
  one? § 11 refuses corrections folded into originals, which suggests
  new-entry-always — but a reframe arriving two minutes later is not a
  correction, and the boundary needs stating.

### 7.7 · The skill is layer 3 and must stay thin

**Operator's decision, 2026-08-29: the parser is invoked by a skill,
triggered by the task.**

**The constraint this inherits.** § 9 places assistant skills in layer 3
— "forfeit on a swap; may point at layer 1, must never be its only
home" — and records a proposal that failed exactly this test by putting
work-tree paths into a skill *and* duplicating the discipline into a new
tree document: two homes, no rule for which wins, guaranteed drift.

**So the split is fixed:**

- **Format spec — layer 1.** A plain file in the tree. The authority.
- **Parser — layer 1.** A script in `utilities/`. Runnable by hand.
- **Skill — layer 3.** A thin pointer: read the spec, emit in that
  shape, call the parser. **It defines nothing.** Its whole content is
  the trigger conditions and two paths.

A model swap then costs the auto-triggering and nothing else. A
different generator reads the spec and files by hand, which is exactly
today's behavior.

**Trigger conditions belong in the skill description**, and they need
enumerating rather than gesturing, because the description is what
determines when a model invokes it. Candidates: a run completes; a
theorem, script, or mechanism lands; the operator says to log it; a
correction or reframe arrives; the operator asks what is open.

**The silent-miss failure.** A skill fires at the generator's
discretion. If it is not invoked, nothing is filed **and nobody
notices** — the same class as a generator forgetting to offer the log,
which is a documented failure in the source program's own rules.
Discretion cannot be the only safeguard for a mechanism whose purpose is
to survive the generator's attention.

**Two backstops, covering two different failures.** Neither subsumes the
other, and the distinction is the whole design:

- **Filed by the wrong path** — the generator writes to a destination
  the skill owns without invoking the skill. There *is* a write to
  intercept. Covered by § 7.8.
- **Not filed at all** — the work finishes and no write is attempted.
  There is nothing to intercept. Covered by a detector for an
  **unrecorded run**: a results artifact exists and no record entry
  cites it. Mechanically checkable, needs no judgment, and it is the
  natural second detector for § 6's ticker. Filed there as well.

### 7.8 · Interception at the skill's first owned action

**Operator's design, 2026-08-29.** The guard fires at the first action
the skill owns. If the skill's job includes writing an index line and
the generator reaches for the index without having invoked the skill,
the hook returns it to the skill. If the skill was already invoked, the
write passes through — an iron gate, closed only against the wrong path.

**This is not a new principle.** § 6 closes with "intercept at the
invocation layer, not at the call sites," and the source program already
ships the pattern: `utilities/hooks/check_direct_run.py` is a PreToolUse
hook whose Check 1 **blocks a measurement script invoked directly** and
routes it through `utilities/run.py`, because direct runs overwrote
their own prior results three times and left artifacts with no dated
record. Same shape, different surface.

**Why it beats a post-hoc detector for the case it covers.** It fires at
the moment of the mistake, while the generator is already in the right
context, so the correction costs almost nothing. And it accumulates no
debt: the itch is prevented rather than recorded for later discharge.

**The flag lifecycle is the crux, and a naive version goes inert.** The
hook must know whether a skill invocation is live. A session-scoped
set-once flag fails: after the first filing the gate passes everything
for the rest of the session. The working version is a flag meaning **an
invocation is in flight** — set when the skill fires, cleared by the
parser on a successful file. Writes to owned destinations are permitted
only while one is in flight, so every filing moment needs its own
invocation and the gate stays live all session.

**It must guard every owned destination, not only the first.** A guard
on the index alone is walked around by writing the record directly. The
set is enumerable and must be enumerated.

**Entry 4's lesson applies recursively.** That entry's finding was that
a guard depending on an unperformed setup step is not a guard: a fresh
clone carried `pre-commit` in a tracked directory and silently gated
nothing until `core.hooksPath` was set, and the repair was to make the
gate detect its own unconfigured state. This interception is itself a
setup step — settings present, hook wired, flag path writable — so it
needs the same liveness check, or a clone ships an interception that
silently does not intercept.

**No generator-invocable escape. The operator is the gate.**
*Operator's decision, 2026-08-29.* An override the generator can invoke
is the generator adjudicating its own exception — the thing § 7 forbids
by construction, and the concession finding directly beneath it says why
it would not hold: given an override, a generator produces
justifications for using it, and from the inside those justifications
are indistinguishable from reasoning. The escape would become the path.

**Instead the write is parked, not blocked and not allowed.** The gate
is a queue. A direct write to an owned destination is diverted to a
staging area, the generator is told in one line that it was parked, and
the work continues. The operator reviews and approves at a boundary —
the same boundaries § 2 already names. Velocity is preserved because
nothing stops; authority is preserved because nothing lands unapproved.

**This unifies three items that were separately underspecified:**

- a staged write has a first-seen date and accumulates, so it is an
  **itch source** — § 6's ticker surfaces it as a count with the same
  age gate, no new machinery;
- a staged write is already in **§ 7's parseable format**, so approval
  is running the parser over the queue rather than a bespoke flow;
- § 7.8's interception now has a defined destination for what it
  catches, instead of a decision it cannot make.

**The queue state is binary: open or closed.** *Operator's decision,
2026-08-29.* While a staged write is **open** it is live, held in
scratch, and available; when the operator decides it is **closed**.
This inherits NOTEPAD's existing status vocabulary rather than inventing
a second word for a state the system already names, and it is cleaner
than a parked/filed pair, which conflates two axes — queue state and
outcome. Open/closed is queue state alone; **the record itself is the
authority on what landed**.

The safety property survives the change: **open** unambiguously means
not yet in the record, so a generator reporting honestly cannot claim
an open write was filed. That divergence — "I filed it" against "it was
filed" — is precisely the failure the record exists to prevent (§ 7.2).

**No silent expiry.** A staged write dropped without a decision is worse
than one refused, because the generator believes it landed. The queue
only shrinks by an operator decision, and an old entry in it is debt to
be surfaced, never garbage to be collected.

---

## 8 · The starting kit ships no tool-call interception

**Status:** open. **Found 2026-08-29 while specifying § 7.8.**

**The finding.** This repository has **no `.claude/settings.json`**. The
source program has one, wiring two surfaces: `PostToolUse` on
`Edit|Write|MultiEdit|NotebookEdit` running the record gate, and
`PreToolUse` on `Bash` running `check_direct_run.py`.

So the invocation-layer interception that § 6 names as the principle —
"intercept at the invocation layer, not at the call sites" — exists in
the test case and **not in the prototype it was extracted from**. A
project copying this tree gets the pre-commit hook, the gates, and the
record, and gets no tool-call interception at all.

**Why it matters beyond tidiness.** § 10's starting kit is the claim
about what a minimal container is. If the interception surface is
load-bearing enough that § 6 closes on it and § 7.8 depends on it, then
either it belongs in the kit or § 10 should say plainly that it is a
later addition and why. Right now it is neither: absent from the kit and
absent from the discussion.

**OPERATOR — decide.** Ship a settings file in the kit (and accept that
it is tool-specific, which § 9 places in layer 2), or document the
omission in § 10 with the reason. The second is defensible — layer 2 is
explicitly convenience that enforces layer 1 — but it should be a
recorded choice rather than a gap.

---

## 9 · The record as a navigable graph — a node that opens to its history

**Status:** open. **Operator's framing, 2026-08-29.** Related: § 7.5.

**The ask.** Thread the record by stacking entries along a line of work,
close the thread with the artifact or mechanism that names the closure,
and let that closure open as a node expanding to its history.

**Two findings that shrink the estimate.**

*The edges already exist, at full density.* The source program's record
carries **227 entries and 227 `refs:` fields** — every entry declares
its ancestry. The graph is complete and specified in plain text today.
This is not a format change plus a backfill.

*The generated-view pattern is already proven in the tree.*
`utilities/theorem_index.py` states it in its own docstring —
"GENERATED, not written" — reading Lean source and emitting a table of
every theorem with its claim, its axiom cost, and **what cites it**. An
artifact-node index with provenance edges, produced from layer-1 source,
never hand-maintained. The precedent holds.

### 9.1 · The reframe: ancestry on demand, not a picture

A rendering of 227 connected nodes is a hairball nobody reads. What the
ask describes functionally is **a node that opens to its history** —
an ancestry query on a DAG, not a visualization of the whole thing.
Given a closure node, walk its edges back and stop:

```text
hEF → 271 → 269 → 267 → 264 → 262 → 257 → 130
```

That is cheap, it matches how the corpus is actually used (the operator
refers to the object, not to the entry range), and it does not require
the whole graph to be legible at once.

### 9.2 · The real work is edge typing

Every edge today is an undifferentiated `refs:`. These have genuinely
different meanings when tracing why a decision was made:

- **builds-on** — this entry stands on that one
- **synthesizes** — this entry closes a chain (§ 7.5's field)
- **corrects** — this entry says an earlier one was wrong; § 11 requires
  corrections as new entries, so this edge is the only machine-visible
  trace of a retraction
- **discharges** — this entry closed a named leaf

An untyped graph flattens a retraction into a citation, which is the one
distinction the record most needs to preserve.

### 9.3 · Hard constraint

**The graph is a view. The record stays the authority.** Append-only,
plain text, corrections as new entries (§ 9, § 11). Nothing is navigable
that is not first readable by a stranger with `cat`. A generated view
cannot rot, because it is regenerated; a hand-maintained one becomes a
second home with no rule for which wins.

### 9.4 · The cheap first slice

**Render untyped ancestry from the 227 refs that already exist**, use
it, and measure whether it is useful *before* paying for typing. If it
is navigable untyped, typing improves it. If it is noise untyped, typing
will probably not save it. No format change, no backfill, one script.

**OPERATOR — decide after the slice**, not before: whether typed edges
earn their cost, and whether closure nodes are enumerated by hand or
detected (an entry that discharges a leaf, ships a script, or pins a
theorem is a candidate closure by its own content).

### 9.5 · The map as an audit instrument, not only navigation

**Operator's framing, 2026-08-29.** Every edge from an open or closed
node is traceable by both parties, so each can catch what the other
missed. The value is not that the operator can find an entry; it is that
**both look at the same surface instead of at two memories.**

**The existing tool names this gap in its own docstring.** The source
program's `utilities/check_refs.py` validates four token types — paper
sections, Lean declarations, scripts, results paths — and then says:
*"It checks that a target EXISTS. It cannot check that the target says
what the citing line claims,"* citing the miss that proves it (entry 88:
a section about RH cited for a claim about analytic continuation).
Existence held; meaning did not.

It already ships `--audit`, which *"pair[s] every cross-document `§`
citation with the text it points at, for review. Reads nothing about
meaning; the judgement is a person's."* **That is the traversal, already
implemented, emitted as a list** — which is the form the operator is
saying does not work. The map is the rendering, not a new capability.

**The class of defect only a map surfaces: linked claims that disagree.**
`BLUEPRINT.md:512` and the source program's `preregs/FORMAT.md:59` state
different counts for the same fact (§ 1.3). That is the entry-88 shape,
and it was found because a file happened to be opened. Adjacent in a
view, the two claims disagree on sight. No gate catches it — judging it
requires reading meaning. No list surfaces it — you would have to
suspect it before going to look.

### 9.6 · Link records, not filesystem symlinks

**Engineering constraint.** The ask names symlinks to results,
references, web pages, and commits. Real filesystem symlinks are fragile
in a tracked tree: they break across clones on some platforms, can point
outside the repository, and some tooling mishandles them.

The portable form is a **link record** — a path, commit SHA, or URL
written in text and validated by the gate that already exists. Same
navigability, survives a clone, stays layer 1. `check_refs.py` already
validates three of the four kinds; commit SHAs and URLs are the
additions, and a SHA is checkable against git while a URL is not
(record it, do not pretend it is gated).

### 9.7 · What the node carries

A closure node is a hub, not a text entry. Minimum contents:

- the artifact it names (theorem, script, mechanism, paper);
- its ancestry, by typed edge (§ 9.2);
- link records to results, references, commits, external sources;
- open/closed state, inherited from the index rather than restated —
  **one authority per fact** (§ 9).

---

## 10 · (next item)

To be added.
