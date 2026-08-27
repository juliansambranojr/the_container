# The Container

A blueprint for durable work with a fluent generator. Domain-agnostic,
tool-agnostic, evergreen. It was built once, under load, for a research
program in analytic number theory; it is written down here so that any
idea can move in.

This is the second draft. The first is in git history; it was written
after the container had worked, and this one is written after it broke,
repeatedly, in a single week. § 12 records exactly what changed.

---

## 1 · Thesis

A fluent generator — a language model, or any collaborator who produces
faster than they verify — fails in a specific way: its errors arrive
with the same confidence, the same coherence, and the same feel as its
successes. From the inside, generating something right and generating
something wrong are one experience. Quality therefore cannot be secured
at the point of generation. It has to be secured by the structure
around it.

The container is that structure. Four load-bearing properties:

1. **State lives in files**, outside every head and every context
   window, in plain text any future reader can open.
2. **Claims enter the record only through gates** — mechanical checks
   that can fail, and that fail loudly.
3. **The powers are separated.** Generating, checking, adversarial
   reading, and deciding are held by different parties, because the
   generator's characteristic error is invisible to the generator.
4. **Progress is a ratchet.** Every green state is committed before the
   next risk is taken, so ground gained is never lost — to a crash, a
   context wipe, a bad afternoon, or a wrong turn.

Inside this container the generator can be pushed hard — fast,
believing, ambitious — because velocity has stopped being the thing
that safeguards truth. The gates safeguard truth. Belief supplies the
pressure; the gates supply the direction; the pairing is the engine.

The inversion at the core: the default workflow is a generation engine
with optional verification. The container is a verification engine with
generation as its fuel.

### 1.1 · The correction that produced this draft

The first draft assumed that a rule, written down in a place the
generator reads, is a rule. It is not.

The source program's governing documents contained the exhaustiveness
rule — the one broken in § 5.1 — with a worked example, in the layer
read at the start of every session. Two earlier protocols in the same
directory had applied it correctly, days before. The defect happened
anyway, in a protocol drafted by a generator with all of it available.

**A rule that must be read to be obeyed will eventually not be read.**
Under context pressure a generator regenerates structure from priors
instead of loading it, and the regenerated version is fluent, plausible,
and subtly wrong. That is `drift`, and no amount of writing prevents it.

So the container's central design constraint is now:

> Prefer a mechanism that **executes** over a mechanism that must be
> **read**. When a rule can be made to run, make it run. When it cannot,
> write it down — and expect it to fail sometimes.

Sections 5 and 6 follow from that sentence.

---

## 2 · Definitions

**Operator.** The human owner of the work. Holds synthesis, verdicts,
scope, and every outward-facing action.

**Generator.** The fluent producer — an AI model, or any collaborator
whose output rate exceeds their verification rate. Interchangeable by
design: if the generator is swapped, the container still works.

**Gate.** A mechanical check that can fail: a compiler, a proof kernel,
a test suite, a reference checker, a value checker, a decision rule's
partition assertion. Gates fire in both directions — a gate that can
only pass is decoration.

**Green state.** The condition in which every gate passes. The unit of
progress; the only state worth committing.

**Ratchet commit.** A commit of a green state, made before the next risk
is taken. The sequence of ratchet commits is a floor that only rises.

**Commitment files.** The small set of files carrying the working
contract: identity and rules; the current state of the world; the
references; the index of open threads. Reading them is how any instance
— fresh, resumed, or replaced — recovers orientation.

**Record (notebook).** The append-only, dated log of what happened.
Entries are appended by anyone; outcome markings and status transitions
belong to the operator.

**Index.** A greppable one-line-per-thread pointer into the record, each
line carrying a status.

**Leaf.** A named open assumption the current work stands on. Every leaf
carries two things at birth: a budget and a discharge sketch.

**Budget.** The measured tolerance of the downstream consumer: how
wrong, how crude, how large can this piece be before the thing that uses
it stops working? Measured by running the consumer, never estimated from
prestige.

**Discharge sketch.** A concrete sketch of how a leaf would ever be
proved or verified, produced the moment the leaf is named. A leaf whose
discharge cannot be sketched is usually a defect in the leaf — and this
is the cheapest place to find it.

**Consensus price.** The difficulty a task inherits from its reputation.
A consensus price is an echo; a budget is a measurement.

**Slice.** A unit of work no larger than one green build. Slicing is
what makes belief safe.

**Prereg (locked protocol).** For empirical claims: the test written
before the run — parameters locked, a decision rule implemented as a
predicate table (§ 5.1), results hashed against a sidecar. Output
produced under a locked prereg can carry a verdict; everything else is
exploratory and is labelled so.

**Predicate table.** A decision rule expressed as `(label, predicate)`
pairs in executable code, with an assertion that exactly one fires.

**Residue branch.** The one label whose predicate is unconditionally
true — it owns every outcome the others do not. Not a failure label; it
routes to a stated next step.

**Verdict.** The operator's recorded judgment on a preregistered result.
Generators report what the decision rule mechanically returned; the
verdict line is the operator's to write.

**Blind arm.** The part of the data nobody has looked at, stated as a
mechanism rather than an assurance (§ 5.3).

**Perturbation.** A deliberately decorrelated pass — an adversarial
reader with no stake in the author's framing, briefed from files rather
than from the author's summary. Scheduled by the operator, especially at
the moments the work feels most obviously right.

**Stigmergy.** Coordination through the shared artifact rather than
through memory: each actor reads the tree, acts, and writes back to the
tree, so the environment itself carries the plan.

**Drift.** Generating from priors and recency while believing you are
generating from the sources. The symptom: hours of iteration arriving
back at what the documents already said.

---

## 3 · Why — the failure modes each part answers

| failure mode | what it looks like | the part that answers it |
|---|---|---|
| confident error | wrong output indistinguishable from right | gates |
| drift | regenerating structure from priors | commitment files, read not recalled |
| context loss | the thread dies with the window | record + ratchet commits |
| self-agreement | a conclusion reviewed by its author | perturbation |
| rationalized result | the rule bent to fit the data | prereg, fixed before the run |
| unanswerable outcome | a result no label covers | predicate table + residue branch |
| manufactured signal | the pipeline producing its own finding | null through the identical pipeline |
| consensus pricing | "that's out of scope" without measurement | budget |
| silent clobber | a re-run destroying its predecessor | invocation-layer interception |
| unverifiable provenance | an artifact with no invocation behind it | manifests |

---

## 4 · The parts

| part | holds | fails loudly when |
|---|---|---|
| commitment files | the working contract | orientation is taken from a summary |
| record | dated entries, one per event | an entry cites something nonexistent |
| index | one line per open thread | a thread goes stale unreviewed |
| preregs | fixed-before-run protocols + sidecars | a hash does not match its text |
| gates | executable checks | a claim enters unchecked |
| artifacts | run outputs, immutable | a run overwrites a prior one |
| manifests | what invoked what, with hashes | an artifact has no invocation behind it |
| adjudications | claims verified outside the system | an internal-only check is called sound |

Nothing here is domain-specific. The record is markdown, the gates are
scripts, the artifacts are whatever the work produces.

---

## 5 · The scaffold

Each item below exists because it failed. The citations are to runs, not
to opinions.

### 5.1 · Decision rules execute; they do not persuade

A prereg's decision rule is a list of `(label, predicate)` implemented
**in the script the prereg names**, and the run asserts that **exactly
one predicate fires**.

```
labels = [
    ("compromised",  lambda r: <integrity conditions>),
    ("supported",    lambda r: <H1 conditions>),
    ("refuted",      lambda r: <H0 conditions>),
    ("inconclusive", lambda r: True),          # the residue branch
]
fired = [name for name, p in labels if p(result)]
assert len(fired) == 1, f"RULE DOES NOT PARTITION: {fired}"
```

**Why.** A prereg whose rule lived only as prose was evaluated by hand
and returned a plausible label. A perturbation later found the observed
configuration matched *no* branch: one label failed on its second
clause, the next failed on both of its clauses, and only a fourth
label's silent gate caught the run. Move the measurement 25% in the
direction it was already moving, and no label in the protocol would have
applied. Three days and two further runs passed without anyone noticing,
because English does not assert.

Prose rules also cannot be checked for exhaustiveness by any tool. A
text checker for "the final rule must be unconditional" was prototyped
against nine real preregs: **1 true positive, 1 false positive,
undefined on 4**. It cannot distinguish "no case clears the threshold"
— a legitimate residue phrased positively — from "the gate failed." The
predicate table makes the question decidable because the assertion runs.

### 5.2 · Power is measured before the prereg is locked

Before locking, simulate. Plant the effect at several sizes, plant its
absence, push both through the identical pipeline, report the rate at
which each is labelled correctly.

Three outcomes, all useful: the design has power and is worth locking;
the design has no power at the available data size, and the honest
deliverable is the size at which it would; or the statistic is
degenerate — returning the same value under both plants — which kills
the design before it costs a prereg.

In the source program this killed one design outright, sized a second
that then worked, and twice identified *which variant* of a statistic
was constant by construction, so the informative variant got locked.

### 5.3 · The blind arm is a mechanism, not an assurance

"We have not looked" is unverifiable and, from a generator, worthless.
State it as something checkable:

- the code drops the values before any statistic is computed;
- the analysis mode refuses to run without an explicit confirmation
  flag, and the refusal is exercised;
- the design work computed no value at any measured site, and the commit
  history shows it.

### 5.4 · Nulls carry the instrument, including its transfer function

A null must pass through the **identical** pipeline as the observation.
That is standard and insufficient.

**The pipeline's own shape must be in the null.** An instrument that
differences consecutive blocks imposes a gain suppressing low
frequencies; a null placing outcomes uniformly across the full band
models a freedom the instrument does not have and reports significance
that is partly geometry. Here that inflated a p-value roughly fourfold,
and a perturbation found it, not the pipeline.

Two rules follow. A null must be describable as *what it preserves and
what it destroys* — if that sentence cannot be written, the null is not
understood. And validate a proposed null by pushing structureless input
through it: if it returns "significant" on noise, it is manufacturing
the finding. That check has fired here twice, once turning
Poisson-placed input into a statistic sitting on the celebrated value it
was being compared against.

### 5.5 · Comparisons need their comparison sets audited

When a statistic ranks one target against others, verify the comparison
set is not contaminated by something unrelated to the hypothesis.

Here, one target's strongest "control" sat within a resolution element
of a genuine feature — so that target was asked to out-read real signal
while its rivals were compared against quiet regions. Cleaning the sets
inverted the ordering the conclusion rested on.

Also ask whether the coordinate system privileges one target by
construction. There, the sampling lattice was *defined from* the first
target, placing it at rational points of every sub-instrument while
rivals sat at generic points. Dropping one sub-instrument moved two
targets by +15% and −16% and flipped the ranking.

### 5.6 · Extrapolations name their branch, their points, and their independence

An extrapolation states how many points it rests on, whether those
points are independent, which model produced it, and the interval.

A two-point extrapolation was published here as "roughly 2^52." The
points were **nested** — 89% of the second was the first — the observed
gain sat one standard deviation above the trivial floor, and the implied
exponent interval spanned `[−0.46, 1.55]`. Under the other branch of the
same paragraph the answer was past 2^64. The honest form names both
branches, or says the slope is unmeasured.

### 5.7 · A gate's displayed verdict derives from its displayed numbers

A gate printed `PASS ... union 224 (design 199)` — a pass label beside
the numbers contradicting it — because its flag short-circuited to true
whenever the configuration was off-design.

Two consequences. A gate that does not apply prints `N/A` with the
reason, never `PASS`. And any boolean the record reports carries the
margin that decided it: a "dominates" flag separating values by 1e-7 is
float jitter wearing a verdict's clothes.

### 5.8 · Check version control before building a mitigation

An artifact recorded the hash of the script that produced it; the script
was later edited; the mismatch was read as a provenance loss and an
elaborate reproduction check was built to mitigate it. The original
bytes were in git the whole time, at a commit the record already cited.
One command settled it.

General form: before building a mitigation, establish that the thing
being mitigated is actually lost.

### 5.9 · Read the whole table

A maximum was reported from a six-row view of a seventeen-row table. The
number was wrong by a factor of 2.3 and stood for four entries before a
perturbation caught it.

Slicing a result and reporting an extremum of the slice is a distinct,
recurring failure. Count the rows before trusting an extremum — and note
this one happens in throwaway invocations, outside any file a linter
scans, which is why § 6 intercepts it where it occurs.

---

## 6 · Gates: what earns a place

**A proposed gate is prototyped against the real corpus and scored
before adoption.** Precision and coverage, measured, on the actual
files. Not optional, and cheap.

The evidence is eight checks proposed here after a bad week — all
plausible, six dead on contact with the corpus:

| proposed check | measured |
|---|---|
| final rule must be unconditional | 1 true positive, 1 false positive, undefined on 4 of 9 |
| rule thresholds appear in the locked table | fired on 8 of 9 — passing only the broken file |
| labels agree across sections | 8 fires, 0 true positives, impossible by construction |
| required sections present | 3 fires, all false, one on the reference exemplar |
| verdict authored by a human | unimplementable — every commit has one author |
| sliced-extremum source linter | 7 hits, 0 the defect; the defect never entered the repo |
| short-circuit gate linter | 0 hits; the real defect is an `or` in an assignment |
| sidecar verified at its locking commit | the only one that found something real |

A gate's cost is paid on every invocation, forever. That prototype would
have emitted ~1000 tokens per edit at a ~90% false-positive rate —
roughly 55k tokens of noise per working session, on machinery whose
entire value is silence when nothing is wrong. **A noisy gate gets
baselined into inertness, which is worse than no gate**, because it
leaves the appearance of coverage.

Three survived scoring, and are the recommended starting set:

1. **Flag-from-or-chain.** One grep: a boolean reporting a check's
   verdict must not be assigned from a short-circuiting `or`. Measured:
   1 hit, the real defect, 0 false positives.
2. **Numbers-in-prose.** Every number stated in the record appears in
   the artifact its source line names, within rounding. Extend an
   existing checker's scan set to cover the record and the preregs
   rather than building a second checker. Measured: this would have
   caught § 5.9's error four entries before a human did.
3. **Throwaway-invocation warning.** When an ad-hoc command both reads
   a result artifact and slices it, warn. Catches § 5.9 where it
   happens.

Behind all three: **intercept at the invocation layer, not at the call
sites.** One implementation covers every script including the ones
nobody has touched — the alternative here was seventy-five edits across
three call-site shapes, each owing a re-run.

---

## 7 · The powers, separated

Four roles. One party may hold several, but never *generate* and
*adjudicate* the same claim.

**Generator.** Produces work, at speed, believing it.

**Gates.** Mechanical, automatic, no discretion, no appeals except by
fixing the thing in the open.

**Perturbation.** Reads to break. Three findings from running this hard:

- *Spawn it when you agree with yourself.* A conclusion that survives
  its own author's review is the least-tested kind.
- *It must attack the concession too.* When a generator is challenged
  and concedes, the concession is a claim produced in one move, aimed at
  the challenger. Here a generator conceded within a single message and
  two of its four stated grounds were falsified by entries it had
  written the previous day. Agreeing quickly with whoever pushed is the
  same defect as agreeing with yourself, and harder to see because it
  looks like rigor.
- *One that measures beats one that argues.* The strongest audit
  produced here prototyped every proposed check against the real corpus
  and scored it; six of eight died on the numbers. A report reasoning
  about a check is worth less than one that runs it.

**Operator.** Owns verdicts, status transitions, scope, and every
outward-facing action. The generator computes the mechanical output and
recommends; it does not stamp.

---

## 8 · The loop

1. **Orient.** Read the commitment files. Not a summary of them.
2. **Scope, audited.** One party proposes; a second, with no stake,
   audits and returns a recommendation; the operator approves. Both
   instruments built this way here caught a fatal flaw *before* code
   was written — one a formula index that would have measured the wrong
   objects and reported them under the right names.
3. **Power first.** § 5.2.
4. **Lock.** Predicate table in the script; hash the text; commit the
   locked text *before* running (§ 9's corollary); state the blind arm
   mechanically.
5. **Run through the invocation layer**, so the artifact carries a
   manifest and the prior version is archived.
6. **Report the mechanical output.** Not the verdict.
7. **Perturb.** § 7.
8. **Record.** Run and reading as separate entries: what happened, then
   what it means. Corrections go in new entries, visible as corrections,
   never by editing the old one.
9. **Ratchet.** Gates green, commit, push.

---

## 9 · Where things live

Three layers, in order of authority. **Anything load-bearing lives in
layer 1**, because 2 and 3 do not survive a change of tool.

1. **Plain files in the work tree** — rules, preregs, record, gates.
   Readable and runnable by anything. The system of record.
2. **Tool-specific configuration** — hooks, settings. Convenience that
   enforces layer 1.
3. **Assistant-specific accelerators** — skills, memory. Forfeit on a
   swap; may point at layer 1, must never be its only home.

A proposal here failed this test by putting work-tree paths into an
assistant skill *and* duplicating the discipline into a new tree
document. Two homes, no rule for which wins, guaranteed drift. Before
writing a new governing document, check whether the authoritative home
already exists — usually the spec you are about to duplicate, plus the
dated entry that taught the lesson.

**Corollary, learned expensively.** A prereg's hash must stay verifiable
after the fact. If the text is mutated after locking — to fill a run
record — the sidecar pins text that then exists nowhere, unless the
locking commit was made *before* the mutation. Eight of nine preregs in
the source program have no recoverable pre-image for exactly this
reason. Lock, commit, *then* run.

---

## 10 · Starting kit

The minimum that is still a container:

- a record file, dated entries, append-only;
- an index of open threads, one line each;
- one gate that can fail, wired to run automatically;
- a prereg with a predicate-table rule, for the first claim that
  matters;
- version control, committed at every green state.

A morning of work. Everything else here is what you add when a specific
failure teaches you to — and the order in which failures arrive is the
order in which to add.

**Move in when** a wrong claim would cost more than the gates cost, and
the work outlives one sitting. **Do not move in** for a one-afternoon
question with no downstream consumer.

---

## 11 · What the container refuses

- **A verdict from the generator.** It computes, recommends, stops.
- **A gate with an appeals process.** Fix the thing or fix the gate, in
  the open.
- **A claim whose provenance is a summary.** Open the source.
- **A correction folded into the original.** New entry, visible.
- **A rule left in prose when it could execute.**
- **A check adopted because it sounds right.** Score it first.
- **A negative asserted without measurement.** "That says nothing about
  X" is a claim, and it needs the same evidence as any other.

---

## 12 · What changed from the first draft

The first draft was written after the container had worked. This one
after it broke, several times, in one week.

**Added:** § 1.1 (documentation's track record, and the
execute-over-read constraint that follows); § 5.1 (executable decision
rules and the residue branch); § 5.4's transfer-function requirement;
§§ 5.5–5.9 (comparison contamination, extrapolation honesty, gates that
contradict their own numbers, git-before-mitigation, whole-table reads);
§ 6 entire (scoring a gate before adopting it, with the eight-check
table and the token arithmetic); § 7's findings on concessions and on
measuring adversaries; § 9's corollary on hash pre-images; § 11's last
refusal.

**Unchanged:** the thesis, the four properties, the vocabulary, the
separation of powers, the ratchet. Those held under every load applied.

---

## 13 · Provenance

Built and stress-tested in Primebeat_081426
(<https://github.com/juliansambranojr/Primebeat_081426>), a measurement
bench and Lean 4 formalization program. Its record is public, including
the corrections — which is the point: the notebook shows the container
operating, failing, and being repaired. A container whose record shows
no failures is a container nobody ran hard.

Two things there are load-bearing for this document. The dated
correction entries are the empirical witness discharging the single
premise of this repository's own adjudication — *some claim feels right
and is incorrect* — so the argument here does not rest on assertion. And
the week that produced this draft is itself the evidence for § 6: a
generator proposed eight sensible-sounding gates, a perturbation ran
them against the real corpus, and six died.

The method is the container. The ideas are yours.
