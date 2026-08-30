#!/usr/bin/env python3
"""Walk a lab notebook's `refs:` edges backwards — one entry's whole history.

The record already carries the graph. Every entry declares a `refs:` line, so
`entry N -> the entries it stands on` is specified in plain text today; nothing
renders it. Rendering all of it at once is a hairball. This renders one node's
ancestry instead — the transitive closure of its refs, as an indented tree:

    Entry 271 (formalization, 2026-08-28) — <title>
      Entry 269 (run, 2026-08-28) — <title>
        Entry 267 ...

    python3 utilities/ancestry.py notes/lab_notebook.md notes/lab_notebook_2.md --entry 271
    python3 utilities/ancestry.py notes/*.md --stats

An entry reachable by several paths is expanded once; later arrivals print as
`[re-converges — expanded under Entry M]`, so the shape of the convergence is
visible without the subtree being repeated.

  --stats   totals, edges, roots (cite nothing), leaves (nothing cites them),
            max depth, and DEFECTS: refs pointing at entries that do not
            exist, self-references, cycles, malformed refs tokens, headers
            missing their type/refs fields, duplicate entry numbers.

READ-ONLY. Nothing is written anywhere; the record stays the authority and
this is a view of it.

Two parse hazards, both live in this corpus, both handled rather than assumed
away. Fenced code blocks are skipped, because notes files contain examples of
themselves and a `## YYYY-MM-DD — Entry N` inside a fence is a template, not an
entry. And `type:`/`refs:` are read as the entry header's own next two fields,
not by a document-wide grep, so a stray `refs:` in a body cannot be adopted by
the entry above it. Both parses report their counts under --stats; if the
header count and the field count disagree, that is printed as a defect rather
than silently reconciled.
"""
import argparse
import pathlib
import re
import sys

HEADER = re.compile(r"^## (\d{4}-\d{2}-\d{2}) — Entry (\d+) — (.*)$")
FENCE = re.compile(r"^\s*(```|~~~)")
FIELD = re.compile(r"^(type|refs):\s*(.*)$")
NUM = re.compile(r"\d+")


class Entry:
    __slots__ = ("num", "date", "title", "type", "refs", "src", "line", "raw_refs")

    def __init__(self, num, date, title, src, line):
        self.num, self.date, self.title = num, date, title
        self.src, self.line = src, line
        self.type, self.raw_refs, self.refs = "", "", []

    def label(self):
        return f"Entry {self.num} ({self.type or '?'}, {self.date}) — {self.title}"


def parse(paths):
    """{num: Entry}, plus a list of parse defects. Fences are skipped."""
    entries, defects, header_count = {}, [], 0
    for path in paths:
        p = pathlib.Path(path)
        if not p.is_file():
            defects.append(f"file not found: {path}")
            continue
        lines = p.read_text(encoding="utf-8").splitlines()
        in_fence, fence_tok = False, ""
        i = 0
        while i < len(lines):
            line = lines[i]
            m_fence = FENCE.match(line)
            if m_fence:
                tok = m_fence.group(1)
                if not in_fence:
                    in_fence, fence_tok = True, tok
                elif tok == fence_tok:
                    in_fence = False
                i += 1
                continue
            if in_fence:
                i += 1
                continue
            m = HEADER.match(line)
            if not m:
                i += 1
                continue
            header_count += 1
            date, num, title = m.group(1), int(m.group(2)), m.group(3).strip()
            e = Entry(num, date, title, p.name, i + 1)
            # the header's own fields: the next lines, before the blank that
            # ends the header block. A document-wide grep would let a body
            # line masquerade as a field.
            j, got = i + 1, set()
            while j < len(lines) and lines[j].strip():
                mf = FIELD.match(lines[j])
                if not mf:
                    break
                key, val = mf.group(1), mf.group(2).strip()
                got.add(key)
                if key == "type":
                    e.type = val
                else:
                    e.raw_refs = val
                    for tok in [t.strip() for t in val.split(",") if t.strip()]:
                        nums = NUM.findall(tok)
                        if len(nums) == 1 and nums[0] == tok:
                            e.refs.append(int(nums[0]))
                        elif len(nums) == 1:
                            e.refs.append(int(nums[0]))
                            defects.append(
                                f"malformed refs token in Entry {num} "
                                f"({p.name}:{j + 1}): {tok!r} — read as {nums[0]}")
                        else:
                            defects.append(
                                f"unreadable refs token in Entry {num} "
                                f"({p.name}:{j + 1}): {tok!r} — SKIPPED")
                j += 1
            for k in ("type", "refs"):
                if k not in got:
                    defects.append(
                        f"Entry {num} ({p.name}:{i + 1}) has no `{k}:` field")
            if num in entries:
                prev = entries[num]
                defects.append(
                    f"duplicate entry number {num}: {prev.src}:{prev.line} "
                    f"and {p.name}:{i + 1}")
            else:
                entries[num] = e
            i = j
    return entries, defects, header_count


def graph_defects(entries):
    """Dangling refs, self-references, cycles."""
    out = []
    for n in sorted(entries):
        e = entries[n]
        for r in e.refs:
            if r == n:
                out.append(f"self-reference: Entry {n} refs itself")
            elif r not in entries:
                out.append(f"dangling ref: Entry {n} refs Entry {r}, which does not exist")
    # cycles, over edges that resolve
    WHITE, GREY, BLACK = 0, 1, 2
    color, stack, found = {n: WHITE for n in entries}, [], []

    def visit(n):
        color[n] = GREY
        stack.append(n)
        for r in entries[n].refs:
            if r not in entries or r == n:
                continue
            if color[r] == GREY:
                cyc = stack[stack.index(r):] + [r]
                found.append("cycle: " + " -> ".join(f"Entry {x}" for x in cyc))
            elif color[r] == WHITE:
                visit(r)
        stack.pop()
        color[n] = BLACK

    sys.setrecursionlimit(10000)
    for n in sorted(entries):
        if color[n] == WHITE:
            visit(n)
    return out + found


def ancestry(entries, root, out):
    """Indented tree of root's transitive refs. Repeats are noted, not expanded."""
    if root not in entries:
        out.append(f"Entry {root} does not exist in the files given.")
        return
    expanded = {}

    def walk(n, depth, path):
        pad = "  " * depth
        e = entries[n]
        if n in path:
            out.append(f"{pad}{e.label()}  [CYCLE — already on this path]")
            return
        if n in expanded:
            under = expanded[n]
            note = ("[re-converges — expanded above at top level]" if under is None
                    else f"[re-converges — expanded under Entry {under}]")
            out.append(f"{pad}{e.label()}  {note}")
            return
        expanded[n] = path[-1] if path else None
        out.append(f"{pad}{e.label()}")
        for r in e.refs:
            if r not in entries:
                out.append(f"{pad}  Entry {r}  [DANGLING — no such entry]")
                continue
            walk(r, depth + 1, path + [n])

    walk(root, 0, [])
    out.append("")
    out.append(f"{len(expanded)} distinct entries in the ancestry of Entry {root} "
               f"(including itself).")


def stats(entries, defects, header_count, out):
    edges = sum(len(e.refs) for e in entries.values())
    cited = set()
    for e in entries.values():
        cited.update(r for r in e.refs if r in entries)
    roots = [n for n, e in sorted(entries.items()) if not e.refs]
    leaves = [n for n in sorted(entries) if n not in cited]

    # longest ancestry chain, memoised over the resolving edges
    depth, onstack = {}, set()

    def d(n):
        if n in depth:
            return depth[n]
        if n in onstack:
            return 0
        onstack.add(n)
        best = 0
        for r in entries[n].refs:
            if r in entries and r != n:
                best = max(best, 1 + d(r))
        onstack.discard(n)
        depth[n] = best
        return best

    sys.setrecursionlimit(10000)
    deepest = max(entries, key=d) if entries else None

    nums = sorted(entries)
    gaps = sorted(set(range(nums[0], nums[-1] + 1)) - set(nums)) if nums else []

    out.append(f"headers matched      {header_count}")
    out.append(f"entries parsed       {len(entries)}")
    out.append(f"number range         {nums[0]}–{nums[-1]}" if nums else "number range  —")
    out.append(f"gaps in numbering    {gaps if gaps else 'none'}")
    out.append(f"edges (refs)         {edges}")
    out.append(f"roots (cite nothing) {len(roots)}: {roots}")
    out.append(f"leaves (uncited)     {len(leaves)}: {leaves}")
    out.append(f"max depth            {d(deepest)} (deepest: Entry {deepest})")
    out.append("")
    by_type = {}
    for e in entries.values():
        by_type[e.type] = by_type.get(e.type, 0) + 1
    out.append("types                " + ", ".join(
        f"{k}={v}" for k, v in sorted(by_type.items())))
    out.append("")
    all_defects = defects + graph_defects(entries)
    if all_defects:
        out.append(f"DEFECTS ({len(all_defects)})")
        for x in all_defects:
            out.append(f"  {x}")
    else:
        out.append("DEFECTS  none")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+", help="notebook markdown file(s)")
    ap.add_argument("--entry", type=int, help="print this entry's ancestry")
    ap.add_argument("--stats", action="store_true", help="graph statistics and defects")
    a = ap.parse_args()
    if a.entry is None and not a.stats:
        ap.error("give --entry N, --stats, or both")

    entries, defects, header_count = parse(a.files)
    out = []
    if a.stats:
        stats(entries, defects, header_count, out)
    if a.entry is not None:
        if a.stats:
            out.append("")
        ancestry(entries, a.entry, out)
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
