#!/usr/bin/env python3
"""map_query.py — S3 of the map (TODO § 11.4). Ask the map a question.

The map's reader is a model with no session context, not a person at a
search bar: 5,876 corpus queries over two weeks in the source program
were issued by a generator on the operator's behalf, and the operator
issued none directly. So this answers the questions that reader actually
has — *what is this, what does it rest on, what points at it, is it
checked* — and it answers them by name, because a name is what a reader
arrives holding.

    map_query.py NODES EDGES --find hEF          # locate, by substring
    map_query.py NODES EDGES --node "entry 271"  # one node's neighborhood
    map_query.py NODES EDGES --node Glue.stmtEF_poly --depth 2
    map_query.py NODES EDGES --flagged           # everything non-conforming

A substring naming nothing says so. It does not guess a nearest match,
because a confident wrong answer is the failure this whole tree exists
to prevent.

DEPTH IS BOUNDED AND DEFAULTS TO 1. Unbounded traversal over `refs:`
returns the prefix of the notebook — entry 271's full closure is 166
entries, 62% of the corpus — because 209 of 270 entries cite N-1. The
bound is the fix; the edges are not the problem.
"""
import argparse
import json
import pathlib
import sys


def load(np, ep):
    nodes = json.loads(pathlib.Path(np).read_text())["nodes"]
    edges = json.loads(pathlib.Path(ep).read_text())["edges"]
    N = {n["id"]: n for n in nodes}
    out, inb = {}, {}
    for e in edges:
        out.setdefault(e["from"], []).append(e)
        inb.setdefault(e["to"], []).append(e)
    return N, out, inb


def line(N, nid, prefix=""):
    n = N[nid]
    flags = ("  ⚠ " + ", ".join(n["flags"])) if n["flags"] else ""
    where = f"{n['file']}:{n['line']}" if n.get("line", 1) != 1 else n["file"]
    return f"{prefix}{nid}  [{n['kind']}]  {where}{flags}"


def show(N, out, inb, nid, depth):
    if nid not in N:
        print(f"no node with id {nid!r}")
        return 1
    n = N[nid]
    print(line(N, nid))
    if n.get("title"):
        print(f"    {n['title'][:100]}")
    if n["flags"]:
        print(f"    NOT CONFORMING: {', '.join(n['flags'])}")

    seen = {nid}
    frontier = [(nid, 0)]
    while frontier:
        cur, d = frontier.pop(0)
        if d >= depth:
            continue
        for e in sorted(out.get(cur, []), key=lambda x: (x["kind"], x["to"])):
            pad = "    " * (d + 1)
            mark = "" if e["to"] in seen else ""
            print(f"{pad}--{e['kind']:<12}-> {line(N, e['to'])}{mark}")
            if e["to"] not in seen:
                seen.add(e["to"])
                frontier.append((e["to"], d + 1))

    back = inb.get(nid, [])
    if back:
        print(f"\n    {len(back)} inbound:")
        for e in sorted(back, key=lambda x: (x["kind"], x["from"]))[:20]:
            print(f"      {line(N, e['from'])}  --{e['kind']}->")
        if len(back) > 20:
            print(f"      … {len(back) - 20} more")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Ask the map a question.")
    ap.add_argument("nodes")
    ap.add_argument("edges")
    ap.add_argument("--node")
    ap.add_argument("--find")
    ap.add_argument("--flagged", action="store_true")
    ap.add_argument("--depth", type=int, default=1)
    a = ap.parse_args()
    N, out, inb = load(a.nodes, a.edges)

    if a.find:
        q = a.find.lower()
        hits = [n for n in N.values()
                if q in n["id"].lower() or q in (n.get("title") or "").lower()]
        if not hits:
            print(f"nothing in {len(N)} nodes matches {a.find!r}")
            return 1
        for n in sorted(hits, key=lambda x: (x["kind"], x["id"]))[:40]:
            print(line(N, n["id"]))
            if n.get("title"):
                print(f"    {n['title'][:96]}")
        if len(hits) > 40:
            print(f"… {len(hits) - 40} more")
        return 0

    if a.flagged:
        bad = [n for n in N.values() if n["flags"]]
        by = {}
        for n in bad:
            for f in n["flags"]:
                by.setdefault(f, []).append(n["id"])
        for f in sorted(by, key=lambda x: -len(by[x])):
            print(f"{f}  ({len(by[f])})")
            for i in by[f][:6]:
                print(f"    {i}")
            if len(by[f]) > 6:
                print(f"    … {len(by[f]) - 6} more")
        print(f"\n{len(bad)} of {len(N)} nodes carry at least one flag.")
        return 0

    if a.node:
        return show(N, out, inb, a.node, max(1, a.depth))

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
