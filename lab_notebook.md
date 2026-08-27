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

## Entry 6 — 2026-08-27 — instrument — the § 6 gates, designed independently and scored on a real corpus

**What was asked.** Build the gates § 6 recommends — but not by
treating its three as a shopping list. § 6's own rule is that a
proposed gate is prototyped against the real corpus and scored before
adoption, so the method was applied to § 6 itself: design candidates
independently from the §§ 5.1–5.9 failure classes, produce at least one
§ 6 does not propose, score everything, keep only what earns a place.

**The corpus.** The container has no preregs, so scoring ran read-only
against `/Users/juliansambrano/GitHub/Primebeat_081426`: 9 preregs, 221
first-party Python files, 175 entries in `notes/lab_notebook_2.md`, 147
`results/*.json`. Nothing there was created, edited, or committed.
Sixteen candidates were written down before any scoring
(A1–A16); the measured table:

| candidate | fires | true positives | verdict |
|---|---|---|---|
| A3 label-parity, prereg → script | 1 | 1 | **kept** |
| A10 flag-from-or-chain | 1 | 1 | **kept** |
| A13 sidecar pre-image | 8 | 8 | **kept** |
| A1 named script resolves | 0 | 0 | folded into A3 |
| A2 partition assertion in script | 9 of 9 preregs | n/a | killed — fires on everything |
| A16 numbers-in-prose over the record | 104 / 40 entries | 1 | killed — 1% precision |
| A16d narrowed to comparison claims | 25 / 175 entries | 1 | killed — 4% precision |
| A12 boolean-with-margin, artifact form | 800 across 47 files | 0 | killed |
| A12 boolean-with-margin, source form | 13 | 0 | killed |
| A15 sliced-extremum in source | 6 | 0 | killed — confirms § 6 |
| A11 verdict literal on a config branch | 0 | 0 | killed — no signal |
| A9 extrapolation names its points | 3 | 2 | killed — see below |
| A5 blind claim without a mechanism | 3 of 9 | 0 | killed |
| A6 null as preserves/destroys | 5 of 9 | 0 | killed |
| A14 throwaway-invocation warning | unscoreable | — | see below |
| A8 comparison-set contamination | not proposed | — | not mechanically checkable |

**The candidate § 6 does not propose, and it is the sharpest one.**
A3 asks whether the verdict labels a prereg declares appear anywhere in
the script the prereg names. It does not parse the prose rule; it asks
the one question a tool can settle. A label the script has never heard
of cannot have been computed by it, so the exactly-one-fires assertion
cannot exist either — § 5.1's root cause made decidable. One fire on the
corpus, and it is the ground-truth defect:
`preregs/multibase_synthesis_v1_20260827.md:48` → `O95_multibase_synthesis.py`
missing `joint_attributes`, `misattributed`, `inconclusive`. Zero false
positives.

**The extractor lied twice before it told the truth.** A3's first pass
reported 1 fire and looked finished. Checking the *silent* prereg found
the extractor was undefined on it — labels are sometimes bolded, and the
script is sometimes named in prose rather than in the locked table. The
second pass reported 2 fires; the new one was false, because Python
3.12+ emits `FSTRING_MIDDLE` rather than `STRING` and the matcher could
not see labels written as f-string prefixes. Both bugs were found by
interrogating the cases where nothing happened, never by reading the
fires. A fire count is not evidence that a checker is defined.

**Why numbers-in-prose died, and what it teaches.** § 6 recommends it
and says it would have caught § 5.9's error four entries before a human
did. Measured on the record, it does not. Three findings, in order of
weight. Entry 215 of the source notebook — where the bad number sits —
names no artifact at all, because that record's convention separates the
run entry (which names the artifact) from the reading entry (which
states the numbers), so the check is undefined exactly where the defect
is. Pooling artifacts transitively through `refs:` makes it fire on the
defect at a 38% false-positive rate. Narrowing to comparison claims
brings it to 25 fires across 175 entries, of which 1 is the defect.

The reason is structural, not tunable. The claimed `2.85` is
`3.719 / 1.305` — a ratio, and a ratio is by construction absent from
the artifact. The existing checker in the source program says so in its
own docstring: statements derived from other statements are skipped
because their numbers are computed, not printed. The defect is not that
`2.85` is missing from the artifact. The defect is that it was computed
from row 8 of a 17-row table when the true next-highest is 3.0315, which
makes the real margin 1.227. **Absence-from-artifact is not the
signature of a slice-extremum error**, and no threshold on that check
turns it into one.

**The general rule the scoring produced.** Every candidate that survived
scans *mutable* state — source files, prereg-to-script links, sidecars
against git. Every candidate that died scans the *append-only record*.
A record-scanning gate cannot be silent when clean, because a true
positive in a historical entry is a permanent fire: the record is
append-only, so the noise never goes away and the gate is baselined into
inertness within a session. That, and not precision alone, is what
disqualifies A16 and A9. A9 is the instructive one — it fires 3 times in
the whole corpus and 2 of those are the real § 5.6 two-point
extrapolation, which reads like a keeper until you notice it will fire
on that same corrected entry on every commit forever.

**A14 could not be scored, and shipping it unscored would break § 6's
own rule.** The throwaway-invocation warning intercepts ad-hoc commands
that read an artifact and slice it. There is no corpus of past
invocations anywhere in the tree — the § 5.9 defect never entered a
file, which is precisely why § 6 wants it intercepted at the invocation
layer. So its precision and coverage are unmeasured and unmeasurable
from the artifacts that exist. It is not shipped. Building it requires
first recording invocations for a period, which is a separate slice with
its own cost.

**An inconsistency in § 6 worth recording.** Its table scores "sidecar
verified at its locking commit" as *the only one that found something
real*, and then its recommended three do not include it. Scored here, it
is the highest-yield candidate of all sixteen: 8 fires, 8 true
positives, 0 false positives, reproducing the known 8-of-9 exactly and
staying silent on `multibase_synthesis_v1_20260827.md`, the one locked
under lock-commit-then-run. It is shipped.

**What shipped.** `utilities/check_flag_or.py` (§ 5.7),
`utilities/check_rule_labels.py` (§ 5.1),
`utilities/check_sidecar_preimage.py` (§ 9), each exposing `check(root)`
and each runnable alone. `utilities/gate.py` aggregates all three, so a
clone gets them from the one gate command with no extra wiring, and
`utilities/hooks/pre-commit` needs no change. Each names the Primebeat
corpus and its measured numbers in its own docstring, so the next reader
finds the scoring where the gate is, not in a summary.

**Cost, measured.** Clean run of the whole gate on this tree: 0.03–0.05 s,
110 characters, one line — about 28 tokens per invocation, so roughly
560 tokens across a 20-commit session. Firing on the pathological corpus
with all defects present: 1.2 s and about 700 tokens. § 6's rejected
prototype was ~55k tokens of noise per session; this is three orders
below that, and the clean case is a single line.

**Degradation in a corpus-free clone.** `check_rule_labels` returns
early with no `preregs/`; `check_sidecar_preimage` returns early with no
sidecars, and reports without a history claim when there is no git;
`check_flag_or` walks zero files once vendored trees are skipped. All
three return `[]` rather than erroring, which is why the container's own
gate is green with none of them having anything to check. One leak was
found and closed: `ast.parse` re-emits a scanned file's `SyntaxWarning`
onto stderr, which would have broken silence on a foreign corpus.

**Verified in both directions.** Seven new scenarios in
`utilities/break_tests.py` — `or`-chain red and `and`-chain green,
labels-absent red and labels-present-as-a-predicate-table green,
unresolvable script red, sidecar-without-pre-image red and
sidecar-pinning-current-text green. 22 scenarios behave, 0 skipped;
`gate.py` green on the intact tree.

**Not mechanically checkable, and this list is a deliverable.** § 5.5
(comparison-set contamination) needs to know whether a control sits on a
real feature — domain semantics, no syntax. § 5.2 (power before lock)
can only be checked as section-presence, which measures compliance
theatre rather than power. § 5.3 (blind arm) and § 5.4 (null carries the
transfer function) fire on 3 of 9 and 5 of 9 preregs respectively with 0
true positives — they detect vocabulary, not mechanism. § 5.6 is
checkable but only over the record, so it inherits the append-only
problem. Of the nine failure classes, three now have a running gate;
§ 5.9 has a design that cannot yet be scored; the remaining five stay
prose, and § 1.1 says plainly to expect prose to fail sometimes.

No outcome marked; transitions are the operator's.

---

## Entry 7 — 2026-08-27 — correction — BLUEPRINT § 6 amended after its recommendations were built

**What happened.** Entry 6 built the § 6 gates under an instruction to
derive candidates independently *before* reading § 6's three, and to
score everything against a real corpus. Sixteen candidates, thirteen
dead, and the three that shipped are **not** the three § 6 recommended.
The operator authorised amending BLUEPRINT — a commitment file the
builder correctly left alone — so the delta is recorded rather than
silently absorbed.

**Amended, in § 6.1 and § 12.** § 6.1 now carries: the shipped set with
each gate's measured firing on its ground-truth defect; the two
recommendations that died and why; the inconsistency the builder caught
in § 6's own table; and the selection rule that only became visible by
building.

**The inconsistency, recorded where it occurred.** § 6's scoring table
called the sidecar pre-image check "the only one that found something
real" and then omitted it from the recommended three. Scored, it was
the highest-yield of all sixteen — 8 fires, 8 true positives. The
builder caught the contradiction between a document's table and its own
recommendation, which is § 5.7's failure mode (a displayed verdict
disagreeing with its displayed numbers) appearing in prose rather than
in code.

**The candidate § 6 never proposed, and it is the best one.**
Label-parity: every verdict label a prereg names must appear in the
script it names. It sidesteps what killed every text-parsing
candidate — instead of reading a prose rule, it asks whether the rule's
labels are in the code at all. A label the script has never heard of
cannot have been computed, so the exactly-one-fires assertion cannot
exist. § 5.1's root cause, reduced to a decidable question. 1 fire, the
real defect, 0 false positives, 0 undefined.

**The selection rule found by building, not by reasoning.** Every gate
that shipped scans **mutable** state — source, links, sidecars against
git. Every one that died scans the **append-only record**. A
record-scanning gate can never be silent when clean: a true positive in
a historical entry fires forever and the entry cannot be edited to fix
it. That is sharper than precision alone and was invisible until
sixteen candidates were scored. § 6 had not stated it.

**A defect of mine, fixed.** The entry-5 NOTEPAD line was appended
inside the header's format-example fence rather than under `## Threads`,
because the insertion matched the first line beginning `- [` — which
was the example. The gate skips fences, so it passed silently. This is
the documented hazard of files that contain examples of themselves,
committed by the same generator that documents it. Moved; gate still
green.

**Status.** Gate green: contract, 6 required files, 7 entries, NOTEPAD
consistent, 3 § 6 checks quiet. Cost measured at 0.03–0.05 s and ~28
tokens clean. The method survived its own first application, which is
the only reason to trust § 6 at all: had its three been adopted as
written, two would have been noise and the best available check would
have been left on the table.
