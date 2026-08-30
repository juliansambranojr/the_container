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

# No domain constants. Everything comes from the descriptor.


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


def _globs(root, spec):
    pats = spec.get("glob")
    pats = [pats] if isinstance(pats, str) else (pats or [])
    out = []
    for p in pats:
        out.extend(sorted(root.glob(p)))
    ex = set(spec.get("exclude_basenames") or [])
    return [f for f in out if f.name not in ex]


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


def scan_citations(root, d, ids, idx, edges):
    """Every link pattern the descriptor declares. A pattern cannot invent a
    node: an edge is emitted only when its target is already in `ids`."""
    scan = d.get("scan") or {}
    suffixes = set(scan.get("suffixes") or [".md"])
    skip = set(scan.get("skip_dirs") or [])
    pats = d.get("link_patterns") or []
    ns_of = {i.rsplit(".", 1)[0] for i in ids if "." in i}

    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.suffix not in suffixes:
            continue
        if any(part in skip for part in f.parts):
            continue
        rel = str(f.relative_to(root))
        text = _defence(_text(f))
        line_of = []
        ln = 1
        for ch in text:
            line_of.append(ln)
            if ch == "\n":
                ln += 1
        line_of.append(ln)

        for spec in pats:
            fmt = spec.get("target_format", "{1}")
            for m in re.finditer(spec["re"], text):
                tgt = fmt
                for gi in range(1, (m.lastindex or 0) + 1):
                    tgt = tgt.replace("{%d}" % gi, m.group(gi) or "")
                if spec.get("strip_target"):
                    tgt = tgt.strip()
                if spec.get("rstrip_dots"):
                    tgt = tgt.rstrip(".")
                # a namespaced code citation is only real if the namespace is
                # one the corpus actually declares
                if spec.get("require_namespace_group"):
                    if m.group(spec["require_namespace_group"]) not in ns_of:
                        continue
                if tgt not in ids:
                    continue
                src = owner_of(idx, rel, line_of[m.start()])
                if src and src != tgt:
                    edges.append({"from": src, "to": tgt, "kind": spec["kind"],
                                  "file": rel, "line": line_of[m.start()]})


def scan_refs(root, d, ids, edges):
    """record -> record, gated by check_entry_refs.py."""
    spec = d.get("record") or {}
    if not spec.get("refs_are_ids"):
        return
    fmt = spec.get("id_format", "entry {id}")
    gi = spec.get("field_refs_group", 5)
    for vol in spec.get("volumes") or []:
        f = root / vol["file"]
        if not f.exists():
            continue
        body = _defence(_text(f))
        for m in re.finditer(spec["entry_re"], body, re.M):
            src = fmt.format(id=m.group(2))
            if src not in ids:
                continue
            if src not in ids:
                continue
            line = body[:m.start()].count("\n") + 1
            for tok in re.findall(r"\d+", m.group(gi) or ""):
                tgt = fmt.format(id=tok)
                if tgt in ids and tgt != src:
                    edges.append({"from": src, "to": tgt, "kind": "refs",
                                  "file": vol["file"], "line": line})


def scan_commits(root, d, ids, idx, edges):
    """A short SHA in prose becomes an edge only if git knows the commit —
    the node set already carries only git-known commits, so membership in
    `ids` is the gate."""
    scan = d.get("scan") or {}
    skip = set(scan.get("skip_dirs") or [])
    n = ((d.get("commits") or {}).get("short_len") or 7)
    for f in sorted(root.rglob("*.md")):
        if any(part in skip for part in f.parts):
            continue
        rel = str(f.relative_to(root))
        text = _defence(_text(f))
        ln = 1
        for m in re.finditer(r"(?<![\w])([0-9a-f]{%d})(?![\w])" % n, text):
            line = text[:m.start()].count("\n") + 1
            src = owner_of(idx, rel, line)
            if src and m.group(1) in ids:
                edges.append({"from": src, "to": m.group(1), "kind": "at_commit",
                              "file": rel, "line": line})
    st = d.get("structured_links") or {}
    md = root / (st.get("manifest_dir") or "")
    key = st.get("manifest_commit_key")
    if key and md.is_dir():
        for f in sorted(md.glob("*.json")):
            try:
                o = json.loads(_text(f))
            except Exception:
                continue
            h = (o.get(key) or "")[:n]
            mid = st["manifest_dir"] + "/" + f.name
            if h in ids and mid in ids:
                edges.append({"from": mid, "to": h, "kind": "at_commit",
                              "file": mid, "line": 1})


def scan_structured(root, d, ids, edges):
    """Machine-written links, declared in the descriptor."""
    st = d.get("structured_links") or {}
    md = root / (st.get("manifest_dir") or "")
    if st.get("manifest_dir") and md.is_dir():
        for f in sorted(md.glob("*.json")):
            mid = st["manifest_dir"] + "/" + f.name
            try:
                o = json.loads(_text(f))
            except Exception:
                continue
            sc = o.get(st.get("manifest_script_key") or "")
            if sc in ids:
                edges.append({"from": mid, "to": sc, "kind": "ran",
                              "file": mid, "line": 1})
            for grp in st.get("manifest_file_keys") or []:
                for item in o.get(grp) or []:
                    tgt = (st.get("manifest_file_prefix") or "") + item.get("path", "")
                    if tgt in ids:
                        edges.append({"from": mid, "to": tgt, "kind": "produced",
                                      "file": mid, "line": 1})
    ad = root / (st.get("artifact_dir") or "")
    akey = st.get("artifact_script_key")
    if akey and st.get("artifact_dir") and ad.is_dir():
        for f in sorted(ad.glob("*.json")):
            try:
                o = json.loads(_text(f))
            except Exception:
                continue
            if isinstance(o, dict) and o.get(akey) in ids:
                rel = st["artifact_dir"] + "/" + f.name
                edges.append({"from": rel, "to": o[akey], "kind": "wrote",
                              "file": rel, "line": 1})
    for spec in d.get("collections") or []:
        if not spec.get("lock_sibling_suffix"):
            continue
        for f in _globs(root, spec):
            sib = f.with_suffix(spec["lock_sibling_suffix"])
            if sib.exists():
                a_, b_ = str(f.relative_to(root)), str(sib.relative_to(root))
                if a_ in ids and b_ in ids:
                    edges.append({"from": a_, "to": b_, "kind": "locked_by",
                                  "file": a_, "line": 1})


def main():
    ap = argparse.ArgumentParser(description="Emit every gated edge.")
    ap.add_argument("root")
    ap.add_argument("descriptor")
    ap.add_argument("nodes", help="nodes.json from map_nodes.py")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    d = json.loads(pathlib.Path(a.descriptor).read_text())
    nodes = json.loads(pathlib.Path(a.nodes).read_text())["nodes"]
    ids = {n["id"] for n in nodes}
    idx = owner_index(nodes)

    edges = []
    scan_citations(root, d, ids, idx, edges)
    scan_refs(root, d, ids, edges)
    scan_commits(root, d, ids, idx, edges)
    scan_structured(root, d, ids, edges)

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
