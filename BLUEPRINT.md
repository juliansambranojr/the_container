# The Container

A blueprint for durable work with a fluent generator. Domain-agnostic,
tool-agnostic, evergreen. It was built once, under load, for a research
program in analytic number theory; it is written down here so that any
idea can move in.

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
4. **Progress is a ratchet.** Every verified state is committed before
   the next risk is taken, so ground gained is never lost — to a crash,
   a context wipe, a bad afternoon, or a wrong turn.

Inside this container the generator can be pushed hard — fast,
believing, ambitious — because velocity has stopped being the thing
that safeguards truth. The gates safeguard truth. Belief supplies the
pressure; the gates supply the direction; the pairing is the engine.

The inversion at the core: the default workflow is a generation engine
with optional verification. The container is a verification engine
with generation as its fuel.

---

## 2 · Why — the failure modes each part answers

Every part of the container exists because a specific failure occurred
without it. The failures are properties of fluent generation itself,
so they will recur in any domain.

**Coherent-and-wrong.** The generator produces a reference, a value, a
claim that reads correctly and is false — and nothing about the
experience of producing it signals the error. *Answer: gates. A claim
is checked by a mechanism that cannot be charmed.*

**Self-judging.** Asked to evaluate its own output, a generator
consults the same instincts that produced the output; an LLM judge
parrots the preferences of its training. Agreement with yourself is
the weakest evidence there is. *Answer: separation of powers, and an
adversary decorrelated from the author.*

**Consensus pricing.** The generator prices difficulty from the
literature it absorbed — "that is known to be hard" — when difficulty
is a property of the claim at the precision the consumer needs, and
the consumer's tolerance is routinely 10–700× cruder than the
literature's standard. Whole programs die at this mispricing. *Answer:
measure the budget before pricing the scope.*

**Flow cuts corners.** Deep in a productive run, the path looks so
clear that steps get skipped — and the skipped step is where the
defect sits. The pattern folds in on itself; attention needs outside
contrast to stay sharp. *Answer: scheduled perturbation — the
adversarial round fires precisely when a conclusion has survived its
author's own review.*

**Context evaporates.** Sessions end, windows compact, instances die,
people forget. Work whose state lives in a head or a chat log loses
ground at every boundary. *Answer: stigmergy — the state lives in the
tree, and any fresh instance re-orients by reading files.*

**Unlogged results.** A result that produced no dated entry does not
exist a month later. The judgment of what deserves logging drifts if
it is left to the generator's mood. *Answer: after anything a later
reader would want dated, offering the log is mandatory; deciding is
the operator's.*

**Silent scope narrowing.** Given "check all of X," a generator checks
most of X and reports done. Compressed scope is a decision taken away
from the operator. *Answer: scope is part of the ask; narrowing
requires asking first.*

**Hedge-dressing.** Corrections smuggled inside new claims ("it is A,
not B" — where B was the generator's own earlier assertion), and
disclaimers appended after deliveries they could not have informed.
Both read as rigor while hiding a retraction. *Answer: say what is;
corrections stand as their own plainly-visible sentences.*

---

## 3 · Definitions

**Operator.** The human owner of the work. Holds synthesis, verdicts,
scope, and every outward-facing action.

**Generator.** The fluent producer — an AI model, or any collaborator
whose output rate exceeds their verification rate. Interchangeable by
design: if the generator is swapped, the container still works.

**Gate.** A mechanical check that can fail: a compiler, a proof
kernel, a test suite, a reference checker, a value checker, a locked
decision rule. Gates fire in both directions — a gate that can only
pass is decoration.

**Green state.** The condition in which every gate passes. The unit of
progress; the only state worth committing.

**Ratchet commit.** A commit of a green state, made before the next
risk is taken. The sequence of ratchet commits is a floor that only
rises.

**Commitment files.** The small set of files that carry the working
contract: identity and rules; the current state of the world; the
references; the index of open threads. Reading them is how any
instance — fresh, resumed, or replaced — recovers full orientation.

**Record (notebook).** The append-only, dated log of what happened:
runs, results, corrections, decisions. Entries are appended by anyone;
outcome markings and status transitions belong to the operator.

**Index.** A greppable one-line-per-thread pointer into the record,
each line carrying a status. The cheapest possible map of what is
open.

**Leaf.** A named open assumption the current work stands on. Every
leaf carries two things at birth: a budget and a discharge sketch.

**Budget.** The measured tolerance of the downstream consumer: how
wrong, how crude, how large can this piece be before the thing that
uses it stops working? Measured by running the consumer, never
estimated from prestige.

**Discharge sketch.** A concrete sketch of how a leaf would ever be
proved or verified, produced the moment the leaf is named. A leaf
whose discharge cannot be sketched is usually a defect in the leaf —
and this is the cheapest place to find it.

**Consensus price.** The difficulty a task inherits from its
reputation. A consensus price is an echo; a budget is a measurement.

**Slice.** A unit of work no larger than one green build. Slicing is
what makes belief safe.

**Prereg (locked protocol).** For empirical claims: the test written
before the run — parameters locked, a decision rule that can fire in
both directions, results hashed against a sidecar. Output produced
under a locked prereg can carry a verdict; everything else is
exploratory and is labelled so.

**Verdict.** The operator's recorded judgment on a preregistered
result. Generators may report what the decision rule mechanically
returned; the verdict line is the operator's to write.

**Perturbation.** A deliberately decorrelated pass — an adversarial
reader with no stake in the author's framing, briefed from files
rather than from the author's summary. Scheduled by the operator,
especially at the moments the work feels most obviously right.

**Stigmergy.** Coordination through the shared artifact rather than
through memory: each actor reads the tree, acts, and writes back to
the tree, so the environment itself carries the plan.

**Drift.** Generating from priors and recency while believing you are
generating from the sources. The symptom: hours of iteration arriving
back at what the documents already said.

---

## 4 · The parts

### 4.1 The substrate — state in the tree

A flat directory of plain-text files under version control. Four
commitment files at the root:

```text
CLAUDE.md      identity, rules, permissions — the working contract
               (name the file for whatever generator you use;
               the contract is what matters)
CONTEXT.md     the blueprint of the work: what exists, what each
               piece does, the current state of the world
REFERENCES.md  every cited document, dependency, and constant,
               with paths
NOTEPAD.md     the index: one status-tagged line per open thread,
               pointing into the notebook by entry number
```

Alongside them: the notebook (`lab_notebook.md`), the artifacts
(results, papers, proofs, code), and the gates (`utilities/`).

Two disciplines keep the substrate load-bearing. **Orient on entry:**
any instance, on arrival or after any context loss, reads the
commitment files before doing substantive work — prior summaries are
never trusted alone. **Ratchet before loss:** before any planned
context boundary, the commitment files are brought to current truth
and the tree is committed and pushed. The remote copy is the durable
fallback; if memory is forfeit, the freshly-synced commit is what the
next instance reads.

### 4.2 The gates

Every domain gets the strongest gate it admits (§ 8 maps common
domains). Whatever the gate, three rules hold:

- A claim enters the record only through a gate. Output produced
  outside the gates is exploratory and is labelled so.
- Gates are mechanical. A gate that requires judgment to interpret has
  the judgment moved into it (a locked threshold, a pinned expected
  output) or is demoted to advice.
- When a gate is red, the state is red. There is no "basically green."

### 4.3 The ledger of leaves

The work at any moment stands on a short, explicit list of named open
assumptions. Each carries its budget (measured) and its discharge
sketch (written at naming time). The ledger is small on purpose: if it
grows, the work has outrun its verification and the next slices are
discharges. Twice-proven pattern: sketching the discharge of a
freshly-named leaf exposes that the leaf, as stated, is unsatisfiable
— the cheapest possible time to learn it.

### 4.4 The adversarial round

A second reader, decorrelated from the author: fresh context, briefed
by file paths rather than by the author's summary, instructed to
break the thing. Fired at three moments — when a scope call says
"impossible," when an audit conclusion survives the author's own
review, and before anything outward-facing ships. Two-round form for
big claims: one round to break the proposal, a separate round to break
the repair. The retraction rate of the adversary's own findings is
part of the signal; an adversary that retracts none of its findings
was not pushed to attack itself.

The round is scheduled, never ambient: an adversary run on everything
re-prices the trajectory toward consensus caution — the same drift
§ 2 names, entering from the other side. It refines; the operator
rations it.

### 4.5 The ratchet

Slice → green → commit → next risk. Commits are small, frequent, and
always of green states. Corrections are logged plainly where they are
visible as corrections. The floor never goes down.

---

## 5 · The workflow — one loop

```text
0. ORIENT     read the commitment files; trust nothing remembered
1. PRICE      before scoping, measure the budget: how crude can this
              be before the downstream consumer breaks?
2. SLICE      cut the work into pieces no larger than one green build
3. GROUND     read the source before writing the claim; cite it or
              do not claim it
4. GENERATE   build the slice
5. GATE       run every check; red means stop and fix
6. LOG        offer the entry; the operator decides; date everything
7. RATCHET    commit the green state; push
8. PERTURB    when a conclusion survives your own review, spawn the
              adversary; repair; gate again
9. REPEAT     next slice — or, at any context boundary, ratchet the
              commitment files and re-enter at 0
```

Notes on the loop:

- Step 1 is where most "impossible" work becomes possible. Run the
  consumer at deliberately degraded inputs and find where it breaks;
  the distance between that break point and the literature's standard
  is the room you have.
- Step 3 has a hard trigger list: any foundational question — "is X
  the right tool," "what does the spec say," "what is the deliverable"
  — blocks generation until the source is open. A reference that could
  have been different last week is opened, never recalled.
- Step 6 exists because the record is part of the work. "That's a
  result — log it?" costs one line; the missing dated entry costs the
  history.
- Step 8 is scheduled by the operator, and the trigger is confidence
  itself: the moment the path looks clearest is the moment the
  adversary earns its keep.

---

## 6 · The roles — separation of powers

Four powers, four holders. Collapsing any two recreates a failure
mode from § 2.

**The generator generates.** Fast, believing, inside the rules. It
appends entries, opens index lines, reports what decision rules
mechanically returned. Where the work is finite and inside known
rules, it decides and executes; escalation is reserved for genuine
synthesis moments.

**The gates judge validity.** Mechanically, incorruptibly, without
fatigue. What the kernel or the test suite accepts is valid; meaning
is a separate question and belongs to the parties below.

**The adversary judges the framing.** It attacks the author's model
of the work — the part gates cannot see, because gates only check
what was stated, and the characteristic defect is in what was stated.

**The operator judges meaning.** Synthesis, verdicts, status
transitions, scope changes, and every outward-facing action —
publishing, posting, flipping visibility — happen on the operator's
explicit word, at that moment. The operator also supplies belief:
"it's possible — let's go" is an instruction to measure and slice,
and the operator's willingness to say it against consensus pricing is
half the engine.

---

## 7 · The starting kit — when to move in, and how

### 7.1 When to move in

Exploration precedes the container. The idea, the sketches, the first
wild claims — those happen in chat, on walks, in whatever medium
generates best, and a container built during that phase adjudicates
claims that do not exist yet. Gates on brainstorming kill the
generativity, the same way an ambient adversary re-prices a
trajectory toward caution (§ 4.4).

The entry criterion: **the container becomes useful at the first
claim you would mind losing.** Concrete signs the moment has come:

- you catch yourself repeating a claim as if it were established;
- you are building B on top of claim A;
- you are about to tell someone;
- you can no longer reconstruct why you believed something last week
  — state has to leave your head now.

The check then runs inward before outward. Inward is the argument
layer: do the premises cohere, is the assumption set satisfiable,
what does the conclusion actually stand on (§ 8's adjudication gate).
Outward is the world layer: budgets, preregistered measurements,
evidence. An idea that has passed neither is exploration; label it
so and enjoy it.

### 7.2 The seed — the minimum instantiation

Four things, roughly twenty minutes:

1. A git repository. That is the ratchet; without it nothing else
   survives.
2. One notebook file whose entry 1 answers three questions: what is
   the idea; what does it stand on (the leaves, each with one line on
   how it would ever be checked); what is the smallest artifact that
   would prove it wrong.
3. The falsifying-artifact question is the day-one gate. A script
   comes later, when there is something mechanical to check.
4. The commit habit: green, commit, next risk.

Everything else grows on demand, each piece arriving when its absence
first hurts. CONTEXT, REFERENCES, and NOTEPAD start as three sections
of the notebook and split into files when they get too big to skim.
The contract file joins the day a generator does — it is the contract
with the generator, and a solo explorer needs no contract with
themselves yet. The adjudication layer joins when an argument gets
long enough that its validity can no longer be held by eye.

### 7.3 The full kit

Under an hour, any domain:

1. `mkdir` the project; `git init`; add a remote.
2. Write the four commitment files. CLAUDE.md (or AGENT.md, or
   CONTRACT.md) carries the rules from this blueprint plus your
   domain's specifics; CONTEXT.md starts nearly empty and grows one
   entry per artifact; REFERENCES.md lists what you already cite;
   NOTEPAD.md starts with its format comment and zero lines.
3. Create `lab_notebook.md` with a dated entry 1: what this project
   is, and what the smallest artifact is that would falsify its
   central claim. If you cannot name that artifact, that is the first
   open thread.
4. Build one gate — the strongest your domain admits — and a script
   that runs it. Wire it to run before every commit.
5. Name your leaves: every assumption the idea stands on. Give each
   its budget (measure it — build the crudest version and see if the
   idea survives) and its discharge sketch (write, today, how it
   would ever be verified).
6. Start the loop at step 1.

The kit is deliberately poor: files, git, one checker. Anything
fancier is convenience, and convenience must never become the system
of record. The test of the substrate: swap the generator entirely —
different model, different person — and the workflow keeps working
from the tree alone.

---

## 8 · Adapting the gates by domain

The container is invariant; only the gates change. The question in
every domain is the same: *what is the strongest mechanical check this
kind of claim admits?*

```text
formal math        proof kernel (Lean, Coq, Isabelle); axiom pins so
                   a proof that starts assuming more fails the build
software           compiler + test suite + CI; the regression test IS
                   the notebook entry's teeth
empirical claims   prereg with locked parameters, a decision rule
                   that can fire both ways, hashed result artifacts
data analysis      pinned inputs (checksums), deterministic reruns,
                   a sanity gate against a known-exact case
writing/argument   reference checker (every citation resolves and is
                   opened), value checker (every number traces to an
                   artifact), the falsifying-artifact question
design/craft       a locked acceptance checklist written before the
                   build; a second decorrelated reviewer against it
strategy/decisions the discharge sketch itself: state what evidence
                   would change the call, and the date to re-check
```

Where a domain seems to admit no gate, the leaf ledger is the gate:
force every claim to name what it stands on, budget it, and sketch its
discharge. A field with no mechanical checks still has satisfiability
— and unsatisfiable assumptions are found by sketching, in any field.

---

## 9 · What the container refuses

- **Verification by vibe.** "It looks right" enters nothing into the
  record.
- **The generator as judge of its own work.** Ever. The adversary is
  briefed from files, never from the author's summary.
- **Consensus pricing without a budget run.** "Too hard" is accepted
  only with the measurement attached.
- **Big-bang slices.** A slice that cannot reach green in one sitting
  is two slices.
- **Silent corrections.** A walked-back claim gets its own sentence,
  dated, visible as a correction.
- **Scope compression.** "All" means all; narrowing is asked for,
  never assumed.
- **Memory as a system of record.** Anything load-bearing that exists
  only in a head, a chat log, or a model's memory is already lost.
- **Outward actions on standing permission.** Publishing, posting,
  and visibility changes take the operator's explicit word at that
  moment.
- **Verdicts from anyone but the operator.** Mechanical outputs are
  reported; verdicts are written by the human whose name is on the
  work.

---

## 10 · Provenance

This container was built and stress-tested in Primebeat_081426
(<https://github.com/juliansambranojr/Primebeat_081426>), where it
carried a measurement bench and a Lean 4 formalization program —
including a day on which the same generator priced a theorem "months,
minimum" at breakfast and delivered its first half, kernel-checked,
by midnight. The delta was zero capability and one method: the budget
was measured, the work was sliced, the adversary was scheduled, and
the floor only rose. The notebook there is part of the publication;
it shows the container operating, corrections included.

The method is the container. The ideas are yours.
