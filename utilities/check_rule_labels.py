#!/usr/bin/env python3
"""Gate: every verdict label a prereg names must exist in the script it names.

BLUEPRINT § 5.1 — a prereg's decision rule is a list of (label, predicate)
implemented IN THE SCRIPT THE PREREG NAMES. A rule that lives only as
prose is evaluated by hand and returns a plausible label; English does
not assert, so no run can discover that the observed configuration
matched no branch.

This gate does not try to read the prose rule. It asks the one question
a tool can settle: are the rule's labels present in the code at all? A
label the script has never heard of cannot have been computed by it, so
the exactly-one-fires assertion cannot exist either. That is the root
cause of § 5.1 reduced to a decidable question.

Also fires when a prereg names a script that does not resolve.

SCORED ON: /Users/juliansambrano/GitHub/Primebeat_081426 (2026-08-27),
9 preregs, 42 labels, 9 named scripts. 1 fire — the ground-truth defect:

    preregs/multibase_synthesis_v1_20260827.md -> O95_multibase_synthesis.py
    missing ['joint_attributes', 'misattributed', 'inconclusive']

0 false positives, 0 undefined. Two extractor bugs were found and fixed
by checking the silent cases rather than trusting the fire count:
labels are sometimes bolded (**`compromised`**), and the script is
sometimes named in prose rather than in the locked-parameter table —
both produced a silently-undefined prereg on the first pass, which is
the pathology § 6 killed other candidates for.

Matching is over the whole source rather than tokenized string literals:
Python 3.12+ emits FSTRING_MIDDLE instead of STRING, so a tokenizing
matcher silently missed labels written as f-string prefixes
(O48_small_angle_cross_base.py) and produced a false positive. Both
strategies score identically on the corpus; the whole-source one has no
version dependence. A label mentioned only in a comment would be a
false negative, which is the cheap direction to be wrong in.

CANDIDATES SCORED AND KILLED alongside this one, on the same corpus:
  - "the named script contains an exactly-one-fires assertion":
    9 fires of 9 preregs. Fires on everything, so it is a demand for a
    refactor rather than a defect detector, and would be baselined into
    inertness on first contact (§ 6).

Degrades to silence: no preregs/ directory, or no *.md in it, returns [].
"""
import pathlib
import re
import sys

PY_NAME = re.compile(r"`([A-Za-z0-9_][A-Za-z0-9_\-]*\.py)")
# labels are list or numbered items whose first token is a backticked
# lower_snake word, optionally wrapped in bold
LABEL = re.compile(r"^(?:- |[0-9]+\. )\*{0,2}`([a-z][a-z0-9_]*)`")
HEADING = re.compile(r"^## ")


def rule_labels(text):
    """Labels declared in the '## Decision rule...' section."""
    out, in_rule = [], False
    for line in text.splitlines():
        if HEADING.match(line):
            in_rule = line.lower().startswith("## decision rule")
            continue
        if in_rule:
            m = LABEL.match(line)
            if m:
                out.append(m.group(1))
    return out


def named_scripts(text):
    """Scripts the prereg names. Tier 1 is the locked-parameter table
    or an analyzer line; tier 2 is any backticked .py anywhere, so the
    check is never silently undefined on a prereg that names its script
    in prose."""
    tier1, tier2, line_of = [], [], {}
    for i, line in enumerate(text.splitlines(), 1):
        low = line.lower().lstrip()
        hits = [m.group(1) for m in PY_NAME.finditer(line)]
        for h in hits:
            line_of.setdefault(h, i)
        if (low.startswith("| script") or low.startswith("- analyzer:")
                or low.startswith("- script:")):
            tier1 += hits
        tier2 += hits
    chosen = tier1 or tier2
    seen, out = set(), []
    for s in chosen:
        if s not in seen:
            seen.add(s)
            out.append((s, line_of[s]))
    return out


def resolve(root, name):
    p = root / name
    if p.is_file():
        return p
    hits = [q for q in root.rglob(name)
            if q.is_file() and ".git" not in q.parts]
    return hits[0] if len(hits) == 1 else None


def check(root):
    root = pathlib.Path(root)
    pdir = root / "preregs"
    if not pdir.is_dir():
        return []
    fails = []
    for p in sorted(pdir.glob("*.md")):
        if p.name == "FORMAT.md":
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        labels = rule_labels(text)
        scripts = named_scripts(text)
        rel = p.relative_to(root)
        for name, lineno in scripts:
            target = resolve(root, name)
            if target is None:
                fails.append(
                    f"{rel}:{lineno}: names script {name!r}, which does not "
                    f"resolve in this tree")
                continue
            if not labels:
                continue
            src = target.read_text(encoding="utf-8", errors="replace")
            missing = [l for l in labels
                       if not re.search(r"\b" + re.escape(l) + r"\b", src)]
            if missing:
                fails.append(
                    f"{rel}:{lineno}: verdict labels {missing} appear nowhere "
                    f"in {name} — the decision rule is prose the script never "
                    f"evaluates, so no run can assert that exactly one branch "
                    f"fires (BLUEPRINT § 5.1)")
    return fails


if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve().parent.parent
    out = check(root)
    for line in out:
        print(f"GATE RED  {line}")
    sys.exit(1 if out else 0)
