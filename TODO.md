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

## 2 · (next item)

To be added.
