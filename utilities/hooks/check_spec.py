#!/usr/bin/env python3
"""PreToolUse hook: refuse a build artifact that no blueprint names.

WHY. On 2026-08-29 a node/edge extractor was written for a map that had
no blueprint — five revisions and a scored audit, but no plan. The rule
against it was added to the root CLAUDE.md the same night. A rule in a
file the generator reads is not a rule (BLUEPRINT § 1.1); it is a
suggestion the generator can route around while quoting it.

So the check runs at the invocation layer instead. A new executable
under utilities/ must be named somewhere in TODO.md or WORKORDER.md
before it can be created. Naming it is cheap — one line in the item
that calls for it. Not naming it is how code appears for a thing nobody
specced.

WHAT IT DOES NOT DO. It does not block edits to files that already
exist, does not touch anything outside utilities/, and does not judge
whether the spec is any good. It asks the one decidable question:
**does a plan mention this filename.**

Exit 0 = allow. Exit 2 = block, with the reason on stderr.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PLANS = ["TODO.md", "WORKORDER.md", "BLUEPRINT.md"]
WATCHED = "utilities/"
EXTS = {".py", ".sh"}


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)                      # malformed input never blocks work

    tool = payload.get("tool_name", "")
    if tool not in ("Write", "Edit", "MultiEdit"):
        sys.exit(0)

    path = (payload.get("tool_input") or {}).get("file_path", "")
    if not path:
        sys.exit(0)

    try:
        rel = str(pathlib.Path(path).resolve().relative_to(ROOT))
    except ValueError:
        sys.exit(0)                      # outside this repo, not ours to police

    if not rel.startswith(WATCHED) or pathlib.Path(rel).suffix not in EXTS:
        sys.exit(0)
    if (ROOT / rel).exists():
        sys.exit(0)                      # editing an existing tool is fine

    # A declared artifact is named on a `builds:` line, never in free prose.
    # Substring search over prose let `mapgraph.py` through on 2026-08-29
    # because WORKORDER.md named it as the cautionary example — mentioning a
    # failure granted it permission.
    name = pathlib.Path(rel).name
    declared = set()
    for plan in PLANS:
        f = ROOT / plan
        if not f.exists():
            continue
        for line in f.read_text().split("\n"):
            m = re.match(r"\s*builds:\s*(.+)$", line, re.I)
            if m:
                declared.update(t.strip(" `") for t in m.group(1).split(","))
    if name in declared:
        sys.exit(0)

    print(
        f"check_spec: {rel} is new and no plan names it.\n"
        f"  No `builds:` line in {', '.join(PLANS)} declares it.\n"
        f"  Add the filename to the item that calls for it, then write it.\n"
        f"  A tool with no plan is the 2026-08-29 failure: code for a\n"
        f"  thing with five revisions and no blueprint.",
        file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
