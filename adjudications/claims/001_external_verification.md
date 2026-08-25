# Adjudication 001 — external verification

**Module:** Adjudications/ExternalVerification.lean
**Status:** exploratory (back-translation round pending)
**Date:** 2026-08-25

## The prose claim

BLUEPRINT.md § 1:

> Quality therefore cannot be secured at the point of generation. It
> has to be secured by the structure around it.

## The formal skeleton

Two conclusions, both kernel-checked from the single premise P1:

- `no_internal_only_sound` — any acceptance policy that admits
  whatever feels right admits an incorrect claim. This is the
  "cannot be secured at the point of generation" half.
- `sound_overrules_somewhere` — any policy that admits only correct
  claims must reject something that feels right. This is the
  "structure around it" half: a gate worth the name can fire against
  the generator's own signal.

The pinned axiom lists (the `#guard_msgs` blocks in the module) are
the mechanically generated version of the ledger below: three opaque
atoms and one premise, and the build fails if a proof ever starts
depending on more.

## The ledger

### Axiom: Adjudication001.Claim

Opaque atom — the space of claims a generator can produce. Vocabulary
only; carries no load beyond existence.

### Axiom: Adjudication001.Correct

Opaque atom — correctness of a claim. The kernel is given no theory
of it; every dispute about what "correct" means lives here, in one
inspectable place, and moves nothing about the two conclusions.

### Axiom: Adjudication001.FeelsRight

Opaque atom — the generator's internal signal: fluency, coherence,
confidence. Same discipline as `Correct`.

### Axiom: Adjudication001.P1

The one load-bearing premise: **some claim feels right and is
incorrect.**

- **Budget:** total — both conclusions stand on P1 alone, so the
  whole adjudication is exactly as strong as this leaf. It needs only
  one witness, ever, in the life of one generator.
- **Discharge route:** empirical, and already witnessed. Any dated
  instance of a confident claim later corrected discharges it;
  the provenance program logged several in one week (a section
  declared absent that was present; a bound mispriced by two orders;
  a stated hypothesis found unsatisfiable — see the Primebeat
  notebook's correction entries).
- **Satisfiability:** the model section realizes {Claim, Correct,
  FeelsRight, P1} on `Bool` with zero axioms, so the premise set has
  a model and the conclusions are non-vacuous.

## Considered and rejected at sketch time

**P2-naive: "whatever passes the gate is correct"**
(`PassesGate c → Correct c`). Rejected before entering the file: its
discharge cannot be sketched. A gate checks what was stated —
consistency, validity, reproducibility — and a gate that admitted
only correct claims would need to decide correctness, which is the
very thing at issue. Stating P2-naive would have made the argument
stronger and the ledger false. The honest version of the gate's power
is already inside `Sound` as a definition, where it costs no axiom.

## Verification

```text
cd adjudications && lake build      # kernel + pins, must be green
python3 ../utilities/adjudicate.py  # ledger cross-check, must be green
```

## Back-translation round

Pending. Per the operator's guidance the adversarial pass is used
sparingly — one decorrelated reader, briefed with this file's module
path only, asked to render the formal statements back into prose;
the diff against § "The prose claim" is the fidelity check. To be
run before this adjudication is cited anywhere outward-facing.
