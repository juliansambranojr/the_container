#!/usr/bin/env python3
"""The adjudications gate. Exit 0 green; exit 1 with one line per
failure. Format: adjudications/FORMAT.md.

Checks:
  1. `lake build` in adjudications/ is green, and no declaration in
     the build uses `sorry` — an unfinished proof is the first thing
     this gate exists to catch, so `sorryAx` is red anywhere,
     including inside an honestly-written pin.
  2. Every module a ledger names is in the root file's import
     closure. `lake build` compiles only what the root imports; a
     module missing its import line was never seen by the kernel, so
     certifying it would be a lie.
  3. Theorem/pin parity per module: every `theorem` carries a
     `#print axioms` pin. An unpinned theorem could smuggle an axiom
     past the ledger.
  4. Every `axiom` declared in a module appears in some pinned list
     (matched by name suffix, since pins carry namespaced names).
  5. Every pinned non-core axiom has a `### Axiom:` section in the
     ledger; every ledgered axiom exists in some pin; every ledger's
     module exists; no orphan modules.

Parsing notes, paid for upstream: declaration counting runs on
comment-stripped source, because docstrings here talk about theorems
and pins; pinned lists are read from `#guard_msgs` docstrings, which
check 1 has just certified against the compiler; fenced blocks in
ledgers are skipped; patterns use [0-9]+.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ADJ = ROOT / "adjudications"
CORE_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

MODULE_RE = re.compile(r"^\*\*Module:\*\* +(\S+\.lean)$", re.M)
IMPORT_RE = re.compile(r"^import +([A-Za-z0-9_.]+)", re.M)
PIN_RE = re.compile(
    r"/--\s*\ninfo: '[^']+' depends on axioms: \[([^\]]+)\]\s*\n-/"
    r"|/-- info: '[^']+' depends on axioms: \[([^\]]+)\] -/")
LEDGER_AXIOM_RE = re.compile(r"^### Axiom: +(\S+)$", re.M)
THEOREM_RE = re.compile(r"^theorem +", re.M)
AXIOM_DECL_RE = re.compile(r"^axiom +([A-Za-z0-9_']+)", re.M)
PRINT_RE = re.compile(r"^#print axioms +", re.M)


def strip_lean_comments(text):
    """Remove /- ... -/ blocks (nesting-aware) and -- line comments,
    so prose about theorems never counts as a theorem."""
    out, i, depth = [], 0, 0
    n = len(text)
    while i < n:
        if text.startswith("/-", i):
            depth += 1
            i += 2
        elif depth and text.startswith("-/", i):
            depth -= 1
            i += 2
        elif depth:
            i += 1
        elif text.startswith("--", i):
            j = text.find("\n", i)
            i = n if j == -1 else j
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def pinned_axioms(lean_text):
    axioms = set()
    for m in PIN_RE.finditer(lean_text):
        body = m.group(1) or m.group(2)
        for name in body.replace("\n", " ").split(","):
            name = name.strip()
            if name:
                axioms.add(name)
    return axioms


def main():
    fails = []

    try:
        build = subprocess.run(
            ["lake", "build"], cwd=ADJ, capture_output=True, text=True)
    except FileNotFoundError:
        print("ADJUDICATE RED  `lake` not found. The adjudications gate "
              "needs Lean 4 via elan (https://github.com/leanprover/elan); "
              "after installing, ensure ~/.elan/bin is on PATH. The "
              "adjudications layer is optional — the main gate.py runs "
              "without it.")
        sys.exit(1)
    build_out = build.stdout + build.stderr
    if build.returncode != 0:
        fails.append("lake build failed:")
        fails.extend(f"  {line}"
                     for line in build_out.strip().splitlines()[-6:])
        for f in fails:
            print(f"ADJUDICATE RED  {f}")
        sys.exit(1)
    if "sorry" in build_out:
        fails.append("build output mentions `sorry` — an unfinished proof "
                     "is never green")

    root_lean = ADJ / "Adjudications.lean"
    imports = (set(IMPORT_RE.findall(root_lean.read_text()))
               if root_lean.is_file() else set())
    if not imports:
        fails.append("Adjudications.lean: no imports found — nothing is "
                     "being built")

    ledgers = sorted((ADJ / "claims").glob("*.md"))
    if not ledgers:
        fails.append("no ledgers in adjudications/claims/")
    referenced = set()
    for ledger in ledgers:
        text = ledger.read_text()
        mods = MODULE_RE.findall(text)
        if len(mods) != 1:
            fails.append(f"{ledger.name}: expected exactly one "
                         f"'**Module:**' line, found {len(mods)}")
            continue
        mod = ADJ / mods[0]
        referenced.add(mod.resolve())
        if not mod.is_file():
            fails.append(f"{ledger.name}: module {mods[0]} does not exist")
            continue
        mod_name = mods[0][:-len(".lean")].replace("/", ".")
        if mod_name not in imports:
            fails.append(f"{ledger.name}: module {mod_name} is not "
                         f"imported by Adjudications.lean — the kernel "
                         f"never built it; add `import {mod_name}`")
            continue
        raw = mod.read_text()
        stripped = strip_lean_comments(raw)
        n_theorems = len(THEOREM_RE.findall(stripped))
        n_pins = len(PRINT_RE.findall(stripped))
        if n_theorems != n_pins:
            fails.append(f"{mods[0]}: {n_theorems} theorems but {n_pins} "
                         f"'#print axioms' pins — every theorem must be "
                         f"pinned, or an axiom can slip past the ledger")
        pinned = pinned_axioms(raw)
        if "sorryAx" in pinned:
            fails.append(f"{mods[0]}: a pin contains sorryAx — an "
                         f"unfinished proof is never green")
        pinned_suffixes = {name.split(".")[-1] for name in pinned}
        for decl in AXIOM_DECL_RE.findall(stripped):
            if decl not in pinned_suffixes:
                fails.append(f"{mods[0]}: declared axiom {decl} appears in "
                             f"no pinned list — it is invisible to the "
                             f"ledger check")
        if not pinned and n_theorems > 0:
            fails.append(f"{mods[0]}: no pinned axiom lists found")
        documented = set(LEDGER_AXIOM_RE.findall(text))
        for ax in sorted(pinned - CORE_AXIOMS - {"sorryAx"}):
            if ax not in documented:
                fails.append(f"{ledger.name}: pinned axiom {ax} has no "
                             f"'### Axiom:' ledger section")
        for ax in sorted(documented - pinned):
            fails.append(f"{ledger.name}: ledger documents {ax}, which "
                         f"no pin in {mods[0]} contains")

    for mod in sorted((ADJ / "Adjudications").glob("*.lean")):
        if mod.resolve() not in referenced:
            fails.append(f"orphan module: {mod.name} is reachable from "
                         f"no ledger in claims/")

    if fails:
        for f in fails:
            print(f"ADJUDICATE RED  {f}")
        sys.exit(1)
    print(f"ADJUDICATE GREEN  build ok, no sorry, {len(ledgers)} "
          f"adjudication(s) all imported, theorem/pin parity holds, "
          f"every pinned axiom carries a ledger line.")
    sys.exit(0)


if __name__ == "__main__":
    main()
