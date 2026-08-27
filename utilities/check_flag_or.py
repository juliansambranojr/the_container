#!/usr/bin/env python3
"""Gate: a verdict boolean must not be assigned from a short-circuiting `or`.

BLUEPRINT § 5.7 — a gate printed `PASS` beside the numbers contradicting
it, because its flag short-circuited to true whenever the configuration
was off-design. The shape is an assignment, not a print:

    gate_b_ok = (args.ceiling_pow != 40 or args.x0 != 1000.0
                 or gate_b == GATE_B_EXPECT)

An `or` chain reports true when ANY disjunct holds, so a flag built this
way announces a verdict on the strength of a configuration mismatch. A
gate that does not apply prints `N/A` with the reason; it does not
assign itself a pass.

SCORED ON: /Users/juliansambrano/GitHub/Primebeat_081426 (2026-08-27),
221 first-party Python files. 1 hit — O95_multibase_synthesis.py:1711,
`gate_b_ok`, the real defect — and 0 false positives. Vendored trees
must be excluded: an unfiltered scan also hit
`.venv/.../pip/_internal/network/auth.py:446  password = password or ""`,
a legitimate default-value idiom, which is why SKIP_DIRS exists.

Degrades to silence: a tree with no Python files outside SKIP_DIRS has
nothing to check and returns [].
"""
import ast
import pathlib
import re
import sys
import warnings

SKIP_DIRS = {".git", ".venv", "venv", "site-packages", "node_modules",
             "__pycache__", "build", "dist", ".lake", ".mypy_cache"}

# Names that report a check's verdict. Deliberately narrow: matching
# every boolean would fire on ordinary default-value idioms.
VERDICT_NAME = re.compile(
    r"(?:^|_)(ok|pass|passed|good|valid|holds|dominates?|exceeds?|beats"
    r"|clears?|verdict|green|gate|gates)$"
    r"|^(?:gate|ok|pass|dominat)\w*$", re.IGNORECASE)


def check(root):
    root = pathlib.Path(root)
    fails = []
    for f in sorted(root.rglob("*.py")):
        if SKIP_DIRS & set(f.parts):
            continue
        try:
            with warnings.catch_warnings():
                # the files we scan are not ours to lint; a SyntaxWarning
                # raised while parsing one of them must not reach the
                # gate's output, whose entire value is silence
                warnings.simplefilter("ignore")
                tree = ast.parse(
                    f.read_text(encoding="utf-8", errors="replace"))
        except (SyntaxError, ValueError, OSError):
            continue          # not our gate's business to police syntax
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            if not isinstance(node.value, ast.BoolOp):
                continue
            if not isinstance(node.value.op, ast.Or):
                continue
            for t in node.targets:
                if isinstance(t, ast.Name) and VERDICT_NAME.search(t.id):
                    rel = f.relative_to(root)
                    fails.append(
                        f"{rel}:{node.lineno}: verdict flag {t.id!r} is "
                        f"assigned from a short-circuiting `or` — it reports "
                        f"true whenever any disjunct holds, including an "
                        f"off-design configuration (BLUEPRINT § 5.7). A gate "
                        f"that does not apply prints N/A with the reason.")
    return fails


if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve().parent.parent
    out = check(root)
    for line in out:
        print(f"GATE RED  {line}")
    sys.exit(1 if out else 0)
