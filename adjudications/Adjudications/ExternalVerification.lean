/-
Adjudication 001 — external verification.

Prose claim (BLUEPRINT.md § 1): "Quality therefore cannot be secured at
the point of generation. It has to be secured by the structure around
it."

The domain atoms below are OPAQUE — the kernel is given no theory of
claims, correctness, or feeling; it is asked only whether the
conclusions follow from the named premises. The full ledger for every
axiom (budget, discharge route, and the candidate axiom REJECTED at
sketch time) is claims/001_external_verification.md. The kernel
adjudicates validity; the ledger holds meaning; the pairing is the
method.

No imports: bare Lean 4, core kernel only.
-/

namespace Adjudication001

/-- Atom: the space of claims a generator can produce. Opaque. -/
axiom Claim : Type

/-- Atom: `Correct c` — the claim is correct. Opaque. -/
axiom Correct : Claim → Prop

/-- Atom: `FeelsRight c` — the generator's internal signal endorses
the claim: it is fluent, coherent, confident. Opaque. -/
axiom FeelsRight : Claim → Prop

/-- **P1 — fluency.** Some claim feels right and is incorrect. The
single premise of this adjudication; its ledger line carries the
empirical discharge. -/
axiom P1 : ∃ c, FeelsRight c ∧ ¬ Correct c

/-- An acceptance policy is **sound** when everything it admits is
correct. -/
def Sound (accept : Claim → Prop) : Prop :=
  ∀ c, accept c → Correct c

/-- A policy is **internal-only** when the felt signal alone drives
admission: whatever feels right gets in. -/
def InternalOnly (accept : Claim → Prop) : Prop :=
  ∀ c, FeelsRight c → accept c

/-- **The thesis, negative half:** no internal-only policy is sound.
Verification at the point of generation — admitting what feels right —
admits an incorrect claim, by P1 alone. -/
theorem no_internal_only_sound (accept : Claim → Prop)
    (hint : InternalOnly accept) : ¬ Sound accept :=
  fun hsound => P1.elim fun c h => h.2 (hsound c (hint c h.1))

/-- **The thesis, positive half:** every sound policy overrules the
felt signal somewhere. A gate worth the name must be able to fire
against what feels right — by P1 alone. -/
theorem sound_overrules_somewhere (accept : Claim → Prop)
    (hsound : Sound accept) : ∃ c, FeelsRight c ∧ ¬ accept c :=
  P1.elim fun c h => ⟨c, h.1, fun hacc => h.2 (hsound c hacc)⟩

end Adjudication001

/-! ## Satisfiability witness

The axioms must have a model, or the theorems above are vacuous — the
lesson paid for twice upstream (unsatisfiable stated assumptions,
found at sketch time). The shape of {Claim, Correct, FeelsRight, P1}
is realized on `Bool`: every claim feels right, only `true` is
correct, and `false` witnesses P1. This section uses zero axioms. -/

namespace Adjudication001.Model

theorem model_P1 : ∃ c : Bool, True ∧ ¬ (c = true) :=
  ⟨false, trivial, by decide⟩

end Adjudication001.Model

/-! ## Axiom check

Each `#guard_msgs` block pins the exact axiom list of one conclusion:
if a proof ever starts depending on anything beyond the pinned
premises, the docstring stops matching the compiler and `lake build`
fails. The pin IS the mechanically-generated leaf ledger. -/

/--
info: 'Adjudication001.no_internal_only_sound' depends on axioms: [Adjudication001.Claim,
 Adjudication001.Correct,
 Adjudication001.FeelsRight,
 Adjudication001.P1]
-/
#guard_msgs in
#print axioms Adjudication001.no_internal_only_sound

/--
info: 'Adjudication001.sound_overrules_somewhere' depends on axioms: [Adjudication001.Claim,
 Adjudication001.Correct,
 Adjudication001.FeelsRight,
 Adjudication001.P1]
-/
#guard_msgs in
#print axioms Adjudication001.sound_overrules_somewhere

/-- info: 'Adjudication001.Model.model_P1' does not depend on any axioms -/
#guard_msgs in
#print axioms Adjudication001.Model.model_P1
