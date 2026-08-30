#!/usr/bin/env python3
"""Gate: every `theorem` in a Lean module carries a `#print axioms` pin.

A pinned theorem has its axiom dependencies frozen in a `#guard_msgs`
docstring, so the day someone's edit pulls in a new axiom — or a
`sorry` — the build breaks. An unpinned theorem has no such tripwire:
its dependency set can change under any refactor and the build stays
green, which is the appearance of coverage without the coverage
(BLUEPRINT § 6). Counting is the whole check. Parity is decidable from
the source text; whether a given pin is the *right* pin is not, and
this gate does not pretend otherwise.

This is `adjudicate.py`'s check 3 lifted out of that gate and pointed
at arbitrary trees. The counting convention is copied from it verbatim,
deliberately — a second convention would make the two disagree on the
same file:

    strip comments (nesting-aware /- -/ and -- ), then count
    `^theorem ` against `^#print axioms `

Comment-stripping is load-bearing and was paid for upstream: modules
here have docstrings that talk about theorems and pins, and
`EulerFactorChain.lean:122` opens a prose line with the word `lemma`.
A raw grep counts those.

WHAT THE CONVENTION DOES NOT COUNT, stated rather than resolved: the
regex is anchored bare at column zero, so `private theorem`,
`protected theorem`, `@[simp] theorem`, `lemma`, `example` and
continuation lines of a multi-line signature are all invisible to it.
On the trees measured 2026-08-29 that is one real declaration —
`Primebeat_081426/lean/Chain.lean:474  private theorem sq_rpow_half` —
and it is why this gate reports an UNCOUNTED tally instead of widening
the pattern. Widening is a convention change, and a convention change
belongs to the operator, not to this file. The tally appears in
`--report` and, when nonzero, on the green line.

Vendored trees are skipped (SKIP_DIRS, same list as check_flag_or.py).
`Primebeat_081426/lean/.lake/packages/mathlib` alone carries ~118k
`theorem` lines and zero pins; scanning it would drown the gate in a
finding about somebody else's repository.

MEASURED 2026-08-29, --report over three trees:

    the_container/adjudications            3 theorems    3 pins    +0
    Primebeat_081426/lean_stage3/Stage3  269          129        -140
    Primebeat_081426/lean                311          311          +0

Stage3 is the finding: 7 of its 15 modules are short, LineBound.lean
alone by 60. lean/ is at parity across all 25 modules.

Degrades to silence: a path with no .lean files outside SKIP_DIRS
contributes nothing and is reported as empty rather than as a failure.

Usage:
    check_pin_parity.py [DIR ...]     gate  — silent-ish when clean, 1 on drift
    check_pin_parity.py --report [DIR ...]  survey — full table, always 0

Default DIR is the container's own adjudications/.
"""
import argparse
import pathlib
import re
import sys

SKIP_DIRS = {".git", ".venv", "venv", "site-packages", "node_modules",
             "__pycache__", "build", "dist", ".lake", ".mypy_cache"}

THEOREM_RE = re.compile(r"^theorem +", re.M)
PRINT_RE = re.compile(r"^#print axioms +", re.M)

# Declarations the convention above leaves out. Counted only to be
# reported, never to change a verdict.
UNCOUNTED_RE = re.compile(
    r"^(?:(?:private|protected|noncomputable|@\[[^\]]*\]) +)+theorem +"
    r"|^(?:(?:private|protected|noncomputable|@\[[^\]]*\]) +)*lemma +",
    re.M)


def strip_lean_comments(text):
    """Remove /- ... -/ blocks (nesting-aware) and -- line comments,
    so prose about theorems never counts as a theorem. Copied from
    utilities/adjudicate.py."""
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


def lean_files(root):
    root = pathlib.Path(root)
    if root.is_file():
        return [root] if root.suffix == ".lean" else []
    return sorted(f for f in root.rglob("*.lean")
                  if not SKIP_DIRS & set(f.parts))


def scan(root):
    """[(display_path, n_theorems, n_pins, n_uncounted)] for one tree."""
    root = pathlib.Path(root)
    base = root.parent if root.is_file() else root
    rows = []
    for f in lean_files(root):
        stripped = strip_lean_comments(
            f.read_text(encoding="utf-8", errors="replace"))
        rows.append((str(f.relative_to(base)),
                     len(THEOREM_RE.findall(stripped)),
                     len(PRINT_RE.findall(stripped)),
                     len(UNCOUNTED_RE.findall(stripped))))
    return rows


def table(rows):
    w = max([len(r[0]) for r in rows] + [4])
    out = [f"{'file'.ljust(w)}  theorems  pins  delta  uncounted",
           f"{'-' * w}  --------  ----  -----  ---------"]
    for name, t, p, u in rows:
        out.append(f"{name.ljust(w)}  {t:8d}  {p:4d}  {p - t:+5d}  "
                   f"{u:9d}")
    tt, tp, tu = (sum(r[i] for r in rows) for i in (1, 2, 3))
    out.append(f"{'-' * w}  --------  ----  -----  ---------")
    out.append(f"{'TOTAL'.ljust(w)}  {tt:8d}  {tp:4d}  {tp - tt:+5d}  "
               f"{tu:9d}")
    return out


def main():
    ap = argparse.ArgumentParser(
        description="theorem/#print-axioms parity in Lean sources")
    ap.add_argument("dirs", nargs="*", help="directories (or .lean files)")
    ap.add_argument("--report", action="store_true",
                    help="print the full table and always exit 0")
    args = ap.parse_args()

    default = pathlib.Path(__file__).resolve().parent.parent / "adjudications"
    targets = [pathlib.Path(d) for d in args.dirs] or [default]

    files, mismatches, uncounted = 0, [], 0
    for t in targets:
        if not t.exists():
            print(f"PIN-PARITY RED  {t}: no such path")
            sys.exit(1)
        rows = scan(t)
        files += len(rows)
        uncounted += sum(r[3] for r in rows)
        mismatches += [(t, r) for r in rows if r[1] != r[2]]
        if args.report:
            print(f"\n{t}")
            if not rows:
                print("  (no .lean files outside SKIP_DIRS)")
            else:
                for line in table(rows):
                    print(f"  {line}")

    if args.report:
        sys.exit(0)

    if mismatches:
        for t, (name, th, pin, _) in mismatches:
            print(f"PIN-PARITY RED  {pathlib.Path(t) / name}: {th} theorems "
                  f"but {pin} '#print axioms' pins ({pin - th:+d}) — an "
                  f"unpinned theorem's axiom dependencies can change without "
                  f"breaking the build")
        sys.exit(1)

    note = (f"; {uncounted} declaration(s) outside the counted convention, "
            f"see --report" if uncounted else "")
    print(f"PIN-PARITY GREEN  {files} module(s), theorem/pin parity holds"
          f"{note}.")
    sys.exit(0)


if __name__ == "__main__":
    main()
