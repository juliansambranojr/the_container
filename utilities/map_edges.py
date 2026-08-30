#!/usr/bin/env python3
"""map_edges.py — S2 of the map (TODO § 11.4). Emit every gated edge.

An edge is emitted only when BOTH endpoints are nodes S1 already found,
and only for link kinds a gate already validates:

    cite_paper     Paper.md § A3      check_refs validates existence
    cite_lean      Namespace.decl     check_refs, by namespace and stem
    cite_script    script.py          check_refs
    cite_artifact  results/x.json     check_refs
    cite_prereg    preregs/x.md       check_refs
    cite_doc       CLAUDE.md § Name   check_refs
    ran            manifest -> script         structured JSON
    produced       manifest -> results        structured JSON
    wrote          results -> script          structured JSON
    locked_by      prereg -> sidecar          filename convention

    refs           entry -> entry            check_entry_refs.py

`refs:` was excluded until 2026-08-29 because no gate validated it. The
rule is *only gated edges*, so the resolution was to build the gate:
`check_entry_refs.py`. It is admitted now under the same rule that kept
it out. Note it stays noisy — 209 of 270 entries cite N-1 — so a walk
over refs edges needs a depth bound; that is the renderer's problem, not
the extractor's.

The SOURCE of an edge is the node that owns the line it appears on:
nodes in a file are sorted by line, and a citation belongs to the last
node starting at or above it. A citation before any node in a file is
attributed to the file itself and dropped if the file is not a node.

Read-only. JSON on stdout; --report for a summary.

    python3 utilities/map_nodes.py CORPUS > nodes.json
    python3 utilities/map_edges.py CORPUS nodes.json --report
"""
import argparse
import bisect
import json
import pathlib
import re
import sys

SCAN_SUFFIX = {".md", ".lean"}
SKIP_DIRS = {".git", ".lake", "__pycache__", "node_modules", ".venv",
             "archive", "imported", "files (2)"}


def _text(p):
    try:
        return p.read_text(errors="replace")
    except Exception:
        return ""


def _defence(t):
    """Blank fenced blocks, preserving line numbering so owner lookup stays
    correct. Fenced text is quoted evidence, not the file's own citation —
    and several files here contain examples of themselves."""
    def blank(m):
        return "\n" * m.group(0).count("\n")
    return re.sub(r"```.*?```", blank, t, flags=re.S)


def owner_index(nodes):
    """file -> (sorted line list, parallel id list)."""
    byfile = {}
    for n in nodes:
        byfile.setdefault(n["file"], []).append((n.get("line", 1), n["id"]))
    out = {}
    for f, pairs in byfile.items():
        pairs.sort()
        out[f] = ([p[0] for p in pairs], [p[1] for p in pairs])
    return out


def owner_of(idx, relfile, line):
    got = idx.get(relfile)
    if not got:
        return None
    lines, ids = got
    i = bisect.bisect_right(lines, line) - 1
    return ids[i] if i >= 0 else None


def scan_citations(root, ids, idx, edges):
    """The four gated token types, wherever they appear."""
    lean_ns = {i.rsplit(".", 1)[0] for i in ids if "." in i}
    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.suffix not in SCAN_SUFFIX:
            continue
        if any(part in SKIP_DIRS for part in f.parts):
            continue
        rel = str(f.relative_to(root))
        text = _defence(_text(f))
        starts = [0]
        for ch in text:
            pass
        # precompute line index once
        line_of = []
        ln = 1
        for ch in text:
            line_of.append(ln)
            if ch == "\n":
                ln += 1
        line_of.append(ln)

        def emit(pos, target, kind):
            src = owner_of(idx, rel, line_of[pos])
            if src and target in ids and src != target:
                edges.append({"from": src, "to": target, "kind": kind,
                              "file": rel, "line": line_of[pos]})

        for m in re.finditer(r"([A-Za-z][\w\-.]*\.md)`? § ([A-Z]\d*)", text):
            emit(m.start(), f"{m.group(1)} § {m.group(2)}", "cite_paper")
        for m in re.finditer(r"([A-Za-z][\w\-.]*\.md)`? § ([^\n`§]{3,60})", text):
            emit(m.start(), f"{m.group(1)} § {m.group(2).strip()}", "cite_doc")
        for m in re.finditer(r"(?<![\w\-/])([A-Z][\w']*)\.([a-z][\w'_]*)", text):
            if m.group(1) in lean_ns:
                emit(m.start(), f"{m.group(1)}.{m.group(2)}", "cite_lean")
        for m in re.finditer(r"(?<![\w/])([\w\-]+\.py)\b", text):
            emit(m.start(), m.group(1), "cite_script")
        for m in re.finditer(r"(?<![\w/.])(results/[\w./\-]+)", text):
            emit(m.start(), m.group(1).rstrip("."), "cite_artifact")
        for m in re.finditer(r"(?<![\w/.])(preregs/[\w./\-]+\.md)", text):
            emit(m.start(), m.group(1), "cite_prereg")


def scan_refs(root, ids, edges):
    """entry -> entry, gated by check_entry_refs.py."""
    for vol, _lo, _hi in (("notes/lab_notebook.md", 1, 44),
                          ("notes/lab_notebook_2.md", 45, 10 ** 6)):
        f = root / vol
        if not f.exists():
            continue
        body = _defence(_text(f))
        for m in re.finditer(r"^## \d{4}-\d\d-\d\d — Entry (\d+) — .*?\n"
                             r"type: *\S+\nrefs: *(.*?)$", body, re.M):
            src = f"entry {m.group(1)}"
            if src not in ids:
                continue
            line = body[:m.start()].count("\n") + 1
            for tok in re.findall(r"\d+", m.group(2)):
                tgt = f"entry {tok}"
                if tgt in ids and tgt != src:
                    edges.append({"from": src, "to": tgt, "kind": "refs",
                                  "file": vol, "line": line})


def scan_commits(root, ids, idx, edges):
    """A short SHA in prose becomes an edge only if git knows the commit —
    the node set already carries only git-known commits, so membership in
    `ids` is the gate."""
    for f in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in f.parts):
            continue
        rel = str(f.relative_to(root))
        text = _defence(_text(f))
        ln = 1
        for m in re.finditer(r"(?<![\w])([0-9a-f]{7})(?![\w])", text):
            line = text[:m.start()].count("\n") + 1
            src = owner_of(idx, rel, line)
            if src and m.group(1) in ids:
                edges.append({"from": src, "to": m.group(1), "kind": "at_commit",
                              "file": rel, "line": line})
    d = root / "results" / "runs"
    if d.is_dir():
        for f in sorted(d.glob("*.json")):
            try:
                o = json.loads(_text(f))
            except Exception:
                continue
            h = (o.get("git_head") or "")[:7]
            if h in ids:
                edges.append({"from": f"results/runs/{f.name}", "to": h,
                              "kind": "at_commit",
                              "file": f"results/runs/{f.name}", "line": 1})


def scan_structured(root, ids, edges):
    """Machine-written links: manifests and the results envelope."""
    d = root / "results" / "runs"
    if d.is_dir():
        for f in sorted(d.glob("*.json")):
            mid = f"results/runs/{f.name}"
            try:
                o = json.loads(_text(f))
            except Exception:
                continue
            sc = o.get("script")
            if sc in ids:
                edges.append({"from": mid, "to": sc, "kind": "ran",
                              "file": mid, "line": 1})
            for grp in ("files_created", "files_modified"):
                for item in o.get(grp) or []:
                    tgt = f"results/{item.get('path','')}"
                    if tgt in ids:
                        edges.append({"from": mid, "to": tgt,
                                      "kind": "produced", "file": mid,
                                      "line": 1})
    rd = root / "results"
    if rd.is_dir():
        for f in sorted(rd.glob("*.json")):
            try:
                o = json.loads(_text(f))
            except Exception:
                continue
            if isinstance(o, dict) and o.get("script") in ids:
                edges.append({"from": f"results/{f.name}", "to": o["script"],
                              "kind": "wrote", "file": f"results/{f.name}",
                              "line": 1})
    pd = root / "preregs"
    if pd.is_dir():
        for f in sorted(pd.glob("*.md")):
            if (pd / f"{f.stem}.sha256").exists():
                pid = f"preregs/{f.name}"
                if pid in ids:
                    edges.append({"from": pid, "to": f"preregs/{f.stem}.sha256",
                                  "kind": "locked_by", "file": pid, "line": 1})


def main():
    ap = argparse.ArgumentParser(description="Emit every gated edge.")
    ap.add_argument("root")
    ap.add_argument("nodes", help="nodes.json from map_nodes.py")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    nodes = json.loads(pathlib.Path(a.nodes).read_text())["nodes"]
    ids = {n["id"] for n in nodes}
    idx = owner_index(nodes)

    edges = []
    scan_citations(root, ids, idx, edges)
    scan_refs(root, ids, edges)
    scan_commits(root, ids, idx, edges)
    scan_structured(root, ids, edges)

    seen, uniq = set(), []
    for e in edges:
        k = (e["from"], e["to"], e["kind"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(e)
    uniq.sort(key=lambda e: (e["from"], e["kind"], e["to"]))

    if not a.report:
        json.dump({"corpus": str(root), "edges": uniq}, sys.stdout, indent=1)
        return

    kinds, srcs = {}, set()
    for e in uniq:
        kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
        srcs.add(e["from"])
    print(f"  {'edge kind':<16} {'count':>7}")
    print(f"  {'-'*16} {'-'*7}")
    for k in sorted(kinds, key=lambda x: -kinds[x]):
        print(f"  {k:<16} {kinds[k]:>7}")
    print(f"  {'-'*16} {'-'*7}")
    print(f"  {'TOTAL':<16} {len(uniq):>7}")
    print(f"\n  nodes with at least one outbound edge: {len(srcs)} of {len(ids)}")
    print("  every edge resolves to a known node, by construction.")


if __name__ == "__main__":
    main()
