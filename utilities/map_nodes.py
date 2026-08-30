#!/usr/bin/env python3
"""map_nodes.py — S1 of the map (TODO § 11.4). Emit every addressable node.

DOMAIN-AGNOSTIC BY CONSTRUCTION. This file names no project, no
directory and no subject. A corpus's shape is declared in a descriptor:
`corpus.example.json` is the annotated template, `corpus.primebeat.json`
a worked one. Point it at another descriptor and it maps another tree.

Declaring the shape IS the standardization. A tool edited per project is
not agnostic; a tool that reads a declaration is.

A node is anything the corpus can already point at with a stable
identifier. Every node carries CONFORMANCE FLAGS — the ways it falls
short of its own declared format. Those are the deliverable, not a
diagnostic: the renderer shows a node AS non-conforming rather than
skipping it, so gaps appear in the map and nothing separate hunts them.

Read-only. JSON on stdout, a table with --report.

    python3 utilities/map_nodes.py CORPUS DESCRIPTOR.json --report
    python3 utilities/map_nodes.py CORPUS DESCRIPTOR.json > nodes.json
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys


def _text(p):
    try:
        return p.read_text(errors="replace")
    except Exception:
        return ""


def _defence(t):
    """Blank fenced blocks, preserving line count. Files documenting their
    own format contain examples of themselves; a naive scan reports the
    template as content."""
    return re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"),
                  t, flags=re.S)


def _lineno(text, pos):
    return text[:pos].count("\n") + 1


def _globs(root, spec):
    pats = spec.get("glob")
    pats = [pats] if isinstance(pats, str) else (pats or [])
    out = []
    for p in pats:
        out.extend(sorted(root.glob(p)))
    ex = set(spec.get("exclude_basenames") or [])
    return [f for f in out if f.name not in ex]


def record(root, d, nodes):
    spec = d.get("record")
    if not spec:
        return
    fmt = spec.get("id_format", "entry {id}")
    for vol in spec.get("volumes") or []:
        f = root / vol["file"]
        if not f.exists():
            continue
        body = _defence(_text(f))
        for m in re.finditer(spec["entry_re"], body, re.M):
            g = m.groups()
            date, ident, title = g[0], g[1], g[2]
            typ = g[spec.get("field_type_group", 4) - 1] if len(g) >= 4 else ""
            refs = g[spec.get("field_refs_group", 5) - 1] if len(g) >= 5 else ""
            flags = []
            if not (vol.get("id_min", 0) <= int(ident) <= vol.get("id_max", 10**9)):
                flags.append("outside_volume")
            if not (refs or "").strip():
                flags.append("no_refs")
            nodes.append({"id": fmt.format(id=ident), "kind": "entry",
                          "file": vol["file"], "line": _lineno(body, m.start()),
                          "title": title.strip(), "type": typ, "date": date,
                          "flags": flags})


def code(root, d, nodes):
    for spec in d.get("code") or []:
        for sub in spec.get("dirs") or []:
            dd = root / sub
            if not dd.is_dir():
                continue
            for f in sorted(dd.glob("*" + spec.get("suffix", ""))):
                src = _text(f)
                ns = f.stem
                if spec.get("namespace_re"):
                    m = re.search(spec["namespace_re"], src, re.M)
                    if m:
                        ns = m.group(1)
                pins = set()
                if spec.get("pin_re"):
                    raw = re.findall(spec["pin_re"], src, re.M)
                    pins = set(raw)
                    if spec.get("pin_accepts_qualified"):
                        pins |= {r.rsplit(".", 1)[-1] for r in raw}
                for tm in re.finditer(spec["decl_re"], src, re.M):
                    name = tm.group(1)
                    flags = []
                    if spec.get("pin_re") and name not in pins:
                        flags.append(spec.get("pin_flag", "no_pin"))
                    nodes.append({"id": ns + "." + name, "kind": spec["kind"],
                                  "file": sub + "/" + f.name,
                                  "line": _lineno(src, tm.start()),
                                  "title": name, "flags": flags})


def documents(root, d, nodes):
    for spec in d.get("documents") or []:
        fmt = spec.get("id_format", "{basename} § {label}")
        for f in _globs(root, spec):
            t = _text(f)
            lines = t.split("\n")
            rel = str(f.relative_to(root))
            for m in re.finditer(spec["label_re"], t, re.M):
                label = m.group(1).strip()
                title = (m.group(2).strip()
                         if m.lastindex and m.lastindex >= 2 else label)
                flags = []
                if spec.get("requires_following_re"):
                    ln = _lineno(t, m.start())
                    ok = False
                    for j in range(ln, min(ln + spec.get("requires_window", 30),
                                           len(lines))):
                        if spec.get("requires_stop_re") and \
                                re.match(spec["requires_stop_re"], lines[j]):
                            break
                        if re.match(spec["requires_following_re"], lines[j]):
                            ok = True
                            break
                    if not ok:
                        flags.append(spec.get("missing_flag", "missing"))
                nodes.append({"id": fmt.format(basename=f.name, label=label),
                              "kind": spec["kind"], "file": rel,
                              "line": _lineno(t, m.start()),
                              "title": title[:120], "flags": flags})


def collections(root, d, nodes, cited):
    for spec in d.get("collections") or []:
        for f in _globs(root, spec):
            rel = str(f.relative_to(root))
            nid = f.name if spec.get("id_is_basename") else rel
            flags = []
            if spec.get("require_keys"):
                try:
                    o = json.loads(_text(f))
                except Exception:
                    o = None
                    flags.append("unparseable")
                if isinstance(o, dict):
                    for k in spec["require_keys"]:
                        if k not in o:
                            flags.append("no_" + k)
            if spec.get("uncited_flag") and rel not in cited:
                flags.append("uncited")
            if spec.get("lock_sibling_suffix"):
                sib = f.with_suffix(spec["lock_sibling_suffix"])
                if not sib.exists():
                    flags.append(spec.get("unlocked_flag", "unlocked"))
                else:
                    if spec.get("stamp_re") and not re.search(
                            spec["stamp_re"], _text(f), re.M):
                        flags.append(spec.get("unstamped_flag", "unstamped"))
                    nodes.append({"id": str(sib.relative_to(root)),
                                  "kind": spec.get("lock_sibling_kind", "lock"),
                                  "file": str(sib.relative_to(root)), "line": 1,
                                  "title": _text(sib).strip()[:16] or "empty",
                                  "flags": [] if _text(sib).strip() else ["empty"]})
            nodes.append({"id": nid, "kind": spec["kind"], "file": rel,
                          "line": 1, "title": f.stem, "flags": flags})


def commits(root, d, nodes):
    spec = d.get("commits") or {}
    if not spec.get("enabled"):
        return
    try:
        log = subprocess.run(["git", "-C", str(root), "log",
                              "--format=%h\t%ad\t%s", "--date=short"],
                             capture_output=True, text=True, timeout=60)
    except Exception:
        return
    if log.returncode != 0:
        return
    for line in log.stdout.strip().split("\n"):
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        sha, date, subj = parts
        nodes.append({"id": sha, "kind": "commit", "file": ".git", "line": 1,
                      "title": subj[:120], "date": date, "flags": []})


def cited_paths(root, d):
    """Which collection paths the record names. Only feeds the uncited flag;
    the edge itself is S2's job."""
    out = set()
    stems = set()
    for spec in d.get("collections") or []:
        pats = spec.get("glob")
        pats = [pats] if isinstance(pats, str) else (pats or [])
        for p in pats:
            stem = p.split("*")[0].rstrip("/")
            if stem:
                stems.add(stem)
    for vol in (d.get("record", {}).get("volumes") or []):
        f = root / vol["file"]
        if not f.exists():
            continue
        t = _text(f)
        for stem in stems:
            out |= set(re.findall(re.escape(stem) + r"/[\w./\-]+", t))
    return out


def main():
    ap = argparse.ArgumentParser(description="Emit every addressable node.")
    ap.add_argument("root")
    ap.add_argument("descriptor")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    if not root.is_dir():
        sys.exit("map_nodes: no such corpus: " + str(root))
    d = json.loads(pathlib.Path(a.descriptor).read_text())

    nodes = []
    record(root, d, nodes)
    code(root, d, nodes)
    documents(root, d, nodes)
    collections(root, d, nodes, cited_paths(root, d))
    commits(root, d, nodes)
    nodes.sort(key=lambda n: (n["kind"], n["id"]))

    if not a.report:
        json.dump({"corpus": str(root), "descriptor": d.get("name"),
                   "nodes": nodes}, sys.stdout, indent=1)
        return

    by_kind, flagged = {}, {}
    for n in nodes:
        by_kind[n["kind"]] = by_kind.get(n["kind"], 0) + 1
        for fl in n["flags"]:
            flagged[fl] = flagged.get(fl, 0) + 1
    print("  corpus: " + str(d.get("name")) + "   nodes: " + str(len(nodes)) + "\n")
    print("  {:<18} {:>6}".format("kind", "count"))
    print("  " + "-" * 18 + " " + "-" * 6)
    for k in sorted(by_kind):
        print("  {:<18} {:>6}".format(k, by_kind[k]))
    print("\n  {:<22} {:>6}".format("conformance flag", "count"))
    print("  " + "-" * 22 + " " + "-" * 6)
    for k in sorted(flagged, key=lambda x: -flagged[x]):
        print("  {:<22} {:>6}".format(k, flagged[k]))


if __name__ == "__main__":
    main()
