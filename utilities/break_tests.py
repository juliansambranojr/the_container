#!/usr/bin/env python3
"""The gate for the gates. Replays the 2026-08-25 adversarial
review's break scenarios on scratch copies of this tree: each must
turn a gate red; the intact tree must be green. Run after any change
to gate.py or adjudicate.py — a gate that can only pass is
decoration, and this script is how that stays checked.

Slow-ish by design: the adjudication scenarios rebuild Lean in the
scratch copy. Skips those scenarios (loudly) when lake is absent.
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAKE = shutil.which("lake") or (
    str(pathlib.Path.home() / ".elan/bin/lake")
    if (pathlib.Path.home() / ".elan/bin/lake").exists() else None)

results = []


def copy_tree():
    d = pathlib.Path(tempfile.mkdtemp(prefix="container_break_"))
    dst = d / "tree"
    shutil.copytree(ROOT, dst,
                    ignore=shutil.ignore_patterns(".lake", ".git"))
    return dst


def run(gate, cwd):
    import os
    env = dict(os.environ)
    if LAKE:
        env["PATH"] = str(pathlib.Path(LAKE).parent) + ":" + env["PATH"]
    return subprocess.run([sys.executable, f"utilities/{gate}"],
                          cwd=cwd, capture_output=True, text=True, env=env)


def expect(name, gate, mutate, want_red, needs_lake=False):
    if needs_lake and not LAKE:
        results.append((name, None, "SKIPPED (no lake)"))
        return
    tree = copy_tree()
    try:
        mutate(tree)
        r = run(gate, tree)
        got_red = r.returncode != 0
        ok = got_red == want_red
        detail = r.stdout.strip().splitlines()
        results.append((name, ok, detail[-1] if detail else "(no output)"))
    finally:
        shutil.rmtree(tree.parent, ignore_errors=True)


def main():
    # -- gate.py scenarios ------------------------------------------
    def missing_file(t):
        (t / "CONTEXT.md").unlink()
    expect("missing required file -> red", "gate.py", missing_file, True)

    def bad_entry(t):
        with open(t / "lab_notebook.md", "a") as f:
            f.write("\n## Entry 9 — 2026-08-25 — vibes — bad type, bad seq\n")
    expect("broken numbering + bad type -> red", "gate.py", bad_entry, True)

    def dangling_ref(t):
        with open(t / "NOTEPAD.md", "a") as f:
            f.write("- [open]   2026-08-25  entry 99: dangling\n")
    expect("dangling entry reference -> red", "gate.py", dangling_ref, True)

    def typo_pointer(t):
        with open(t / "NOTEPAD.md", "a") as f:
            f.write("- [open]   2026-08-25  entry 99:typo evades check\n")
    expect("pointer typo (entry 99:typo) -> red", "gate.py",
           typo_pointer, True)

    def unclosed_fence(t):
        with open(t / "lab_notebook.md", "a") as f:
            f.write("\n```\n## Entry 99 — 2099-13-45 — vibes — hidden\n")
    expect("unclosed fence hiding content -> red", "gate.py",
           unclosed_fence, True)

    def rename_contract(t):
        (t / "AGENT.md").rename(t / "CLAUDE.md")
    expect("contract renamed CLAUDE.md -> green", "gate.py",
           rename_contract, False)

    def empty_threads(t):
        text = (t / "NOTEPAD.md").read_text()
        (t / "NOTEPAD.md").write_text(
            text.split("## Threads", 1)[0] + "## Threads\n")
    expect("zero-line Threads section -> green", "gate.py",
           empty_threads, False)

    # -- adjudicate.py scenarios ------------------------------------
    def unimported_module(t):
        (t / "adjudications/Adjudications/Bogus.lean").write_text(
            "this does not even parse\n"
            "/-- info: 'Bogus.x' depends on axioms: [Bogus.P9] -/\n")
        (t / "adjudications/claims/002_bogus.md").write_text(
            "# Bogus\n\n**Module:** Adjudications/Bogus.lean\n\n"
            "### Axiom: Bogus.P9\n\nfake.\n")
    expect("unimported module w/ fake pin -> red", "adjudicate.py",
           unimported_module, True, needs_lake=True)

    def sorry_proof(t):
        p = t / "adjudications/Adjudications/ExternalVerification.lean"
        src = p.read_text()
        p.write_text(src.replace(
            "  P1.elim fun c h => ⟨c, h.1, fun hacc => h.2 (hsound c hacc)⟩",
            "  sorry"))
    expect("sorry-backed proof -> red", "adjudicate.py",
           sorry_proof, True, needs_lake=True)

    def smuggled_axiom(t):
        p = t / "adjudications/Adjudications/ExternalVerification.lean"
        src = p.read_text()
        p.write_text(src.replace(
            "end Adjudication001\n\n/-! ## Satisfiability",
            "axiom P_smuggled : ∀ c, Correct c\n"
            "theorem smuggled : ∀ c, Correct c := P_smuggled\n\n"
            "end Adjudication001\n\n/-! ## Satisfiability", 1))
    expect("unpinned theorem + smuggled axiom -> red", "adjudicate.py",
           smuggled_axiom, True, needs_lake=True)

    def orphan_module(t):
        (t / "adjudications/Adjudications/Orphan.lean").write_text(
            "-- unledgered\n")
    expect("orphan module -> red", "adjudicate.py",
           orphan_module, True, needs_lake=True)

    # -- intact tree ------------------------------------------------
    expect("intact tree gate.py -> green", "gate.py", lambda t: None, False)
    expect("intact tree adjudicate.py -> green", "adjudicate.py",
           lambda t: None, False, needs_lake=True)

    bad = 0
    for name, ok, detail in results:
        if ok is None:
            print(f"BREAK SKIP  {name}")
        elif ok:
            print(f"BREAK OK    {name}")
        else:
            bad += 1
            print(f"BREAK FAIL  {name}\n            last: {detail}")
    if bad:
        print(f"\nBREAK TESTS RED  {bad} scenario(s) failed")
        sys.exit(1)
    print(f"\nBREAK TESTS GREEN  {sum(1 for _, ok, _ in results if ok)} "
          f"scenario(s) behaved, "
          f"{sum(1 for _, ok, _ in results if ok is None)} skipped")
    sys.exit(0)


if __name__ == "__main__":
    main()
