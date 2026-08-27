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

    def git_no_hookspath(t):
        subprocess.run(["git", "init", "-q"], cwd=t, check=True)
    expect("git repo, hooksPath unset -> red", "gate.py",
           git_no_hookspath, True)

    def git_with_hookspath(t):
        subprocess.run(["git", "init", "-q"], cwd=t, check=True)
        subprocess.run(["git", "config", "core.hooksPath",
                        "utilities/hooks"], cwd=t, check=True)
    expect("git repo, hooksPath set -> green", "gate.py",
           git_with_hookspath, False)

    # -- BLUEPRINT § 6 subgate scenarios (entry 6) ------------------
    # Each of the three must fire on the defect it was scored against,
    # and each must stay silent on a tree with nothing of its kind.
    def flag_from_or(t):
        (t / "utilities" / "sample_run.py").write_text(
            "import argparse\n"
            "args = argparse.Namespace(ceiling_pow=40)\n"
            "gate_b_ok = (args.ceiling_pow != 40 or args.x0 != 1000.0)\n")
    expect("verdict flag from an `or` chain -> red", "gate.py",
           flag_from_or, True)

    def flag_from_and(t):
        (t / "utilities" / "sample_run.py").write_text(
            "import argparse\n"
            "args = argparse.Namespace(ceiling_pow=40)\n"
            "gate_b_ok = (args.ceiling_pow == 40 and args.x0 == 1000.0)\n")
    expect("same flag from an `and` chain -> green", "gate.py",
           flag_from_and, False)

    def labels_not_in_script(t):
        (t / "preregs").mkdir(exist_ok=True)
        (t / "preregs" / "demo_v1_20260827.md").write_text(
            "# Prereg — demo\n\n## Decision rule\n\n"
            "1. `compromised` — integrity failed.\n"
            "2. `supported` — H1 conditions.\n"
            "3. `inconclusive` — anything else.\n\n"
            "| script | `demo_run.py` |\n")
        (t / "demo_run.py").write_text(
            'print("the rule lives in prose only")\n')
    expect("prereg labels absent from its script -> red", "gate.py",
           labels_not_in_script, True)

    def labels_in_script(t):
        labels_not_in_script(t)
        (t / "demo_run.py").write_text(
            'labels = [("compromised", lambda r: r.bad),\n'
            '          ("supported", lambda r: r.h1),\n'
            '          ("inconclusive", lambda r: True)]\n'
            'fired = [n for n, p in labels if p(result)]\n'
            'assert len(fired) == 1, f"RULE DOES NOT PARTITION: {fired}"\n')
    expect("prereg labels present as a predicate table -> green",
           "gate.py", labels_in_script, False)

    def unresolvable_script(t):
        (t / "preregs").mkdir(exist_ok=True)
        (t / "preregs" / "demo_v1_20260827.md").write_text(
            "# Prereg — demo\n\n## Decision rule\n\n"
            "1. `compromised` — integrity failed.\n\n"
            "| script | `no_such_script.py` |\n")
    expect("prereg names a script that does not resolve -> red",
           "gate.py", unresolvable_script, True)

    def sidecar_no_preimage(t):
        subprocess.run(["git", "init", "-q"], cwd=t, check=True)
        subprocess.run(["git", "config", "core.hooksPath",
                        "utilities/hooks"], cwd=t, check=True)
        (t / "preregs").mkdir(exist_ok=True)
        (t / "preregs" / "demo_v1_20260827.md").write_text("locked text\n")
        (t / "preregs" / "demo_v1_20260827.sha256").write_text("0" * 64 + "\n")
    expect("sidecar with no recoverable pre-image -> red", "gate.py",
           sidecar_no_preimage, True)

    def sidecar_matches_worktree(t):
        import hashlib
        subprocess.run(["git", "init", "-q"], cwd=t, check=True)
        subprocess.run(["git", "config", "core.hooksPath",
                        "utilities/hooks"], cwd=t, check=True)
        (t / "preregs").mkdir(exist_ok=True)
        body = b"locked text\n"
        (t / "preregs" / "demo_v1_20260827.md").write_bytes(body)
        (t / "preregs" / "demo_v1_20260827.sha256").write_text(
            hashlib.sha256(body).hexdigest() + "\n")
    expect("sidecar pinning the current text -> green", "gate.py",
           sidecar_matches_worktree, False)

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
