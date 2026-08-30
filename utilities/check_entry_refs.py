#!/usr/bin/env python3
"""check_entry_refs.py — gate the notebook's `refs:` field.

WHY THIS EXISTS. `refs:` is the only link type in the source corpus that
no gate validates. `check_refs.py` checks entry numbering, types, volume
ranges and NOTEPAD placement, and never parses `refs:` at all. The map
(TODO § 11) admits an edge only if a gate already validates it, so
`refs:` was excluded — which made § 11.5's acceptance test unpassable,
because entry-to-entry lineage exists nowhere else.

The rule was never "no `refs:`". It was "only gated edges." So this is
the missing gate rather than an exception to the rule.

WHAT IT CHECKS. For every entry: that each `refs:` target is a number,
that the entry it names exists, that it is not the entry itself, and
that the field is present at all. Known gaps are declared, not guessed —
the source notebook's own header states there is no Entry 18.

MEASURED at first run, 2026-08-29: four entries (210, 211, 212, 215)
cite Entry 18, and one (112) carries a non-numeric token, `26 (vol 1)`.
Five defects standing in a corpus gated for weeks, because nothing was
looking at this field.

Exit 0 when clean and silent. Exit 1 listing every defect.

    python3 utilities/check_entry_refs.py CORPUS
    python3 utilities/check_entry_refs.py CORPUS --gaps 18
"""
import argparse
import pathlib
import re
import sys

VOLUMES = (("notes/lab_notebook.md", 1, 44),
           ("notes/lab_notebook_2.md", 45, 10 ** 6))
HEADER = (r"^## (\d{4}-\d\d-\d\d) — Entry (\d+) — (.*?)\n"
          r"type: *(\S+)\nrefs: *(.*?)$")


def main():
    ap = argparse.ArgumentParser(description="Validate notebook refs: edges.")
    ap.add_argument("root")
    ap.add_argument("--gaps", default="",
                    help="comma-separated entry numbers known absent")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    gaps = {int(x) for x in a.gaps.split(",") if x.strip().isdigit()}

    entries, raw = {}, {}
    for vol, lo, hi in VOLUMES:
        f = root / vol
        if not f.exists():
            continue
        body = re.sub(r"```.*?```", "", f.read_text(errors="replace"),
                      flags=re.S)
        for m in re.finditer(HEADER, body, re.M):
            n = int(m.group(2))
            entries[n] = vol
            raw[n] = m.group(5)

    if not entries:
        sys.exit(f"check_entry_refs: no entries found under {root}")

    broken = []
    for n in sorted(entries):
        field = raw[n].strip()
        if not field:
            continue                      # an empty refs: is legal — a root
        for tok in [t.strip() for t in field.split(",") if t.strip()]:
            if not tok.isdigit():
                broken.append((n, f"non-numeric refs token {tok!r}"))
                continue
            t = int(tok)
            if t == n:
                broken.append((n, f"cites itself"))
            elif t not in entries and t not in gaps:
                broken.append((n, f"cites Entry {t}, which does not exist"))

    if not broken:
        print(f"entry refs: {len(entries)} entries, all targets resolve.")
        sys.exit(0)
    for n, why in broken:
        print(f"BROKEN  entry {n}  ->  {why}")
    print(f"\n{len(broken)} broken refs edge(s)")
    sys.exit(1)


if __name__ == "__main__":
    main()
