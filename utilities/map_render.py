#!/usr/bin/env python3
"""map_render.py — S4 of the map (TODO § 11.4). Markdown you can walk.

One file per node, `[[wikilinks]]` between them, YAML frontmatter. That
format was chosen because the operator asked from the outset for three
things — a search bar like Google, a mind map, and Google-Maps walking —
and it is the one format delivering all three through renderers that
already exist and are free:

    Obsidian   open the output folder. Search box, local and global
               graph view, backlinks panel. Offline, no build step.
    Quartz     markdown in, browsable website out, with a search bar and
               a graph. A stranger installs nothing.

One file per node is not a preference. Backlink panels and graph views
exist *because* each note is a node; one file per type yields a table.

The source stays plain markdown — layer 1, portable, readable with
`cat`. The renderer is layer 2 and disposable.

SLUGS. Node ids are not legal filenames (`Paper.md § A3`,
`results/x.json`, `Glue.stmtEF_poly`). Each file takes a deterministic
slug with the true id in frontmatter, and every link uses the same slug.
Collisions are resolved by suffix and reported, never silently merged —
two nodes sharing a file would be a map that lies.

    python3 utilities/map_render.py NODES EDGES --out map/
"""
import argparse
import json
import pathlib
import re
import shutil
import sys

KIND_ORDER = ["entry", "lean_decl", "paper_statement", "paper_section",
              "doc_section", "results", "prereg", "manifest", "script",
              "commit"]


def slugify(nid, kind):
    s = f"{kind}--{nid}"
    s = s.replace("§", "-").replace("/", "-").replace(".", "-")
    s = re.sub(r"[^A-Za-z0-9_\- ]", "", s)
    s = re.sub(r"[\s\-]+", "-", s).strip("-")
    return s[:120]


def build_slugs(nodes):
    slugs, used, collisions = {}, {}, []
    for n in nodes:
        base = slugify(n["id"], n["kind"])
        s = base
        if base in used:
            i = 2
            while f"{base}-{i}" in used:
                i += 1
            s = f"{base}-{i}"
            collisions.append((used[base], n["id"], s))
        used[s] = n["id"]
        slugs[n["id"]] = s
    return slugs, collisions


def yaml_escape(v):
    return '"' + str(v).replace('\\', '\\\\').replace('"', '\\"') + '"'


def render(n, slugs, out_edges, in_edges, N):
    fm = [
        "---",
        f"id: {yaml_escape(n['id'])}",
        f"kind: {n['kind']}",
        f"source: {yaml_escape(n['file'])}",
        f"line: {n.get('line', 1)}",
    ]
    if n.get("date"):
        fm.append(f"date: {n['date']}")
    fm.append("conforming: " + ("true" if not n["flags"] else "false"))
    if n["flags"]:
        fm.append("flags: [" + ", ".join(n["flags"]) + "]")
    fm.append("---")

    body = [f"# {n['id']}", ""]
    if n.get("title"):
        body += [n["title"], ""]
    body += [f"`{n['file']}`" + (f" line {n['line']}" if n.get("line", 1) != 1 else ""), ""]

    if n["flags"]:
        body += ["> **Not conforming.** " + ", ".join(n["flags"]),
                 ">",
                 "> Shown rather than skipped — a gap in the corpus is a gap"
                 " you can see here.", ""]

    oe = out_edges.get(n["id"], [])
    if oe:
        body += ["## Points at", ""]
        for kind in sorted({e["kind"] for e in oe}):
            body.append(f"**{kind}**")
            for e in sorted([x for x in oe if x["kind"] == kind],
                            key=lambda x: x["to"]):
                t = N[e["to"]]
                mark = " ⚠" if t["flags"] else ""
                body.append(f"- [[{slugs[e['to']]}|{e['to']}]]{mark}")
            body.append("")

    ie = in_edges.get(n["id"], [])
    if ie:
        body += [f"## Pointed at by ({len(ie)})", ""]
        for e in sorted(ie, key=lambda x: (x["kind"], x["from"]))[:60]:
            body.append(f"- [[{slugs[e['from']]}|{e['from']}]] — *{e['kind']}*")
        if len(ie) > 60:
            body.append(f"- … {len(ie) - 60} more")
        body.append("")

    if not oe and not ie:
        body += ["*No gated links. This node is isolated in the map — which"
                 " is itself a finding.*", ""]

    return "\n".join(fm) + "\n\n" + "\n".join(body)


def main():
    ap = argparse.ArgumentParser(description="Render the map as walkable markdown.")
    ap.add_argument("nodes")
    ap.add_argument("edges")
    ap.add_argument("--out", default="map")
    a = ap.parse_args()

    nodes = json.loads(pathlib.Path(a.nodes).read_text())["nodes"]
    edges = json.loads(pathlib.Path(a.edges).read_text())["edges"]
    N = {n["id"]: n for n in nodes}
    slugs, collisions = build_slugs(nodes)

    out_edges, in_edges = {}, {}
    for e in edges:
        out_edges.setdefault(e["from"], []).append(e)
        in_edges.setdefault(e["to"], []).append(e)

    out = pathlib.Path(a.out)
    if out.exists():
        shutil.rmtree(out)          # regenerate wholesale; it is a view
    out.mkdir(parents=True)

    for n in nodes:
        (out / f"{slugs[n['id']]}.md").write_text(
            render(n, slugs, out_edges, in_edges, N))

    # entry points, one per kind, so a reader has somewhere to land
    by_kind = {}
    for n in nodes:
        by_kind.setdefault(n["kind"], []).append(n)
    idx = ["---", "id: \"INDEX\"", "kind: index", "---", "",
           "# The map", "",
           f"{len(nodes)} nodes, {len(edges)} edges. Generated — never",
           "edited by hand. Rebuild and it cannot go stale.", "",
           "Open this folder in Obsidian for search, graph view and",
           "backlinks; or publish it with Quartz so a stranger installs",
           "nothing.", ""]
    for k in KIND_ORDER + [k for k in sorted(by_kind) if k not in KIND_ORDER]:
        if k not in by_kind:
            continue
        ns = by_kind[k]
        bad = sum(1 for x in ns if x["flags"])
        idx.append(f"## {k} ({len(ns)})" + (f" — {bad} not conforming" if bad else ""))
        idx.append("")
        for n in sorted(ns, key=lambda x: x["id"])[:400]:
            mark = " ⚠" if n["flags"] else ""
            idx.append(f"- [[{slugs[n['id']]}|{n['id']}]]{mark}")
        if len(ns) > 400:
            idx.append(f"- … {len(ns) - 400} more")
        idx.append("")
    (out / "INDEX.md").write_text("\n".join(idx))

    print(f"map_render: {len(nodes)} node files + INDEX.md -> {out}/")
    if collisions:
        print(f"  {len(collisions)} slug collision(s), resolved by suffix:")
        for a_, b_, s in collisions[:10]:
            print(f"    {a_!r} and {b_!r} -> {s}")
    else:
        print("  no slug collisions")


if __name__ == "__main__":
    main()
