#!/usr/bin/env python3
"""map_nodes.py — S1 of the map (TODO § 11.4). Emit every addressable node.

A node is anything the corpus can already point at with a stable
identifier that a gate checks: a notebook entry, a Lean declaration, a
paper statement or section, a named section of a root document, a
script, a results artifact, a prereg, a run manifest.

Read-only. Emits JSON on stdout, a table with --report.

Every node carries CONFORMANCE FLAGS — the ways it falls short of its
own format spec. They are the point, not a diagnostic: TODO § 11.4's S5
renders a node as non-conforming rather than skipping it, so gaps appear
in the map itself and nothing separate has to hunt them.

Acceptance (TODO § 11.5): counts match the measurements in § 11.2, and
two runs produce byte-identical output.

    python3 utilities/map_nodes.py /path/to/corpus --report
    python3 utilities/map_nodes.py /path/to/corpus > nodes.json
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

SKIP_DIRS = {".git", ".lake", "__pycache__", "node_modules", ".venv"}


def _text(p):
    try:
        return p.read_text(errors="replace")
    except Exception:
        return ""


def _defence(t):
    """Drop fenced blocks. Several files in this corpus contain examples of
    themselves; a naive scan reports the template as content."""
    return re.sub(r"```.*?```", "", t, flags=re.S)


def entries(root, nodes):
    for vol, lo, hi in (("notes/lab_notebook.md", 1, 44),
                        ("notes/lab_notebook_2.md", 45, 10 ** 6)):
        f = root / vol
        if not f.exists():
            continue
        body = _defence(_text(f))
        for m in re.finditer(
                r"^## (\d{4}-\d\d-\d\d) — Entry (\d+) — (.*?)\n"
                r"type: *(\S+)\nrefs: *(.*?)$", body, re.M):
            date, num, title, typ, refs = m.groups()
            flags = []
            if not (lo <= int(num) <= hi):
                flags.append("outside_volume")
            if not refs.strip():
                flags.append("no_refs")
            nodes.append({"id": f"entry {num}", "kind": "entry",
                          "file": vol, "line": body[:m.start()].count("\n") + 1,
                          "title": title.strip(),
                          "type": typ, "date": date, "flags": flags})


def lean(root, nodes):
    for sub in ("lean", "lean_stage3/Stage3"):
        d = root / sub
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.lean")):
            src = _text(f)
            m = re.search(r"^namespace ([A-Za-z_][\w'.]*)", src, re.M)
            ns = m.group(1) if m else f.stem
            # lean/ writes pins namespace-qualified (`#print axioms
            # Chain.foo`); lean_stage3/ writes them bare. Two conventions
            # for one thing — accept both, and record the divergence as a
            # finding rather than picking a side.
            raw = re.findall(r"^#print axioms +([A-Za-z_][\w'.]*)", src, re.M)
            pins = set(raw) | {r.rsplit(".", 1)[-1] for r in raw}
            for tm in re.finditer(r"^theorem +([A-Za-z_][\w']*)", src, re.M):
                name = tm.group(1)
                nodes.append({"id": f"{ns}.{name}", "kind": "lean_decl",
                              "file": f"{sub}/{f.name}",
                              "line": src[:tm.start()].count("\n") + 1,
                              "title": name,
                              "flags": [] if name in pins else ["no_axiom_pin"]})


def papers(root, nodes):
    d = root / "papers"
    if not d.is_dir():
        return
    for f in sorted(d.glob("*.md")):
        if f.name == "FORMAT.md":
            continue
        t = _text(f)
        lines = t.split("\n")
        for m in re.finditer(r"^#{2,4} ([A-Z]\d*)\s*·\s*(.+)$", t, re.M):
            nodes.append({"id": f"{f.name} § {m.group(1)}", "kind": "paper_section",
                          "file": f"papers/{f.name}",
                          "line": t[:m.start()].count("\n") + 1,
                          "title": m.group(2).strip(), "flags": []})
        for i, line in enumerate(lines):
            sm = re.match(r"^\*\*([A-Z]\d+[′″‴]?)\.\*\*\s*(.*)", line)
            if not sm:
                continue
            # a source line is a backtick span standing alone; FORMAT.md
            # permits it to run over several lines, so accept a run whose
            # first line opens with a backtick and carries no prose before it
            has_src = False
            for j in range(i + 1, min(i + 30, len(lines))):
                nxt = lines[j]
                if re.match(r"^\*\*[A-Z]\d+[′″‴]?\.\*\*", nxt):
                    break
                if re.match(r"^\s*`", nxt):
                    has_src = True
                    break
            nodes.append({"id": f"{f.name} § {sm.group(1)}", "kind": "paper_statement",
                          "file": f"papers/{f.name}", "line": i + 1,
                          "title": sm.group(2).strip()[:120],
                          "flags": [] if has_src else ["no_source_line"]})


def doc_sections(root, nodes):
    for f in sorted(root.glob("*.md")):
        for m in re.finditer(r"^#{2,3} (.+)$", _text(f), re.M):
            nodes.append({"id": f"{f.name} § {m.group(1).strip()}",
                          "kind": "doc_section", "file": f.name,
                          "line": _text(f)[:m.start()].count("\n") + 1,
                          "title": m.group(1).strip(), "flags": []})


def scripts(root, nodes):
    for f in sorted(root.glob("*.py")):
        nodes.append({"id": f.name, "kind": "script", "file": f.name,
                      "line": 1, "title": f.stem, "flags": []})


def results(root, nodes, cited):
    d = root / "results"
    if not d.is_dir():
        return
    for f in sorted(d.glob("*.json")):
        rel = f"results/{f.name}"
        flags = []
        try:
            o = json.loads(_text(f))
        except Exception:
            o = None
            flags.append("unparseable")
        if isinstance(o, dict):
            for k in ("schema_version", "script", "summary"):
                if k not in o:
                    flags.append(f"no_{k}")
        if rel not in cited:
            flags.append("uncited")
        nodes.append({"id": rel, "kind": "results", "file": rel,
                      "line": 1, "title": f.stem, "flags": flags})


def preregs(root, nodes):
    d = root / "preregs"
    if not d.is_dir():
        return
    for f in sorted(d.glob("*.md")):
        if f.name == "FORMAT.md":
            continue
        t = _text(f)
        flags = []
        if not (d / f"{f.stem}.sha256").exists():
            flags.append("no_sidecar_unlocked")
        elif not re.search(r"^-? *verdict: *\S", t, re.M):
            flags.append("locked_no_verdict")
        nodes.append({"id": f"preregs/{f.name}", "kind": "prereg",
                      "file": f"preregs/{f.name}", "line": 1, "title": f.stem,
                      "flags": flags})


def manifests(root, nodes):
    d = root / "results" / "runs"
    if not d.is_dir():
        return
    for f in sorted(d.glob("*.json")):
        nodes.append({"id": f"results/runs/{f.name}", "kind": "manifest",
                      "file": f"results/runs/{f.name}", "line": 1, "title": f.stem,
                      "flags": []})


def commits(root, nodes):
    """A commit is a node only if git knows it. Git is the gate — a 7-hex
    token in prose that no commit matches is not admitted."""
    try:
        log = subprocess.run(["git", "-C", str(root), "log",
                              "--format=%h\t%ad\t%s", "--date=short"],
                             capture_output=True, text=True, timeout=60)
    except Exception:
        return
    if log.returncode != 0:
        return
    for line in log.stdout.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        sha, date, subj = parts
        nodes.append({"id": sha, "kind": "commit", "file": ".git",
                      "line": 1, "title": subj[:120], "date": date,
                      "flags": []})


def cited_paths(root):
    """Which results paths any notebook entry names. Used only for the
    `uncited` flag; the edge itself is S2's job."""
    out = set()
    for vol in ("notes/lab_notebook.md", "notes/lab_notebook_2.md"):
        f = root / vol
        if f.exists():
            out |= set(re.findall(r"results/[\w./\-]+", _text(f)))
    return out


def main():
    ap = argparse.ArgumentParser(description="Emit every addressable node.")
    ap.add_argument("root")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    if not root.is_dir():
        sys.exit(f"map_nodes: no such corpus: {root}")

    nodes = []
    entries(root, nodes)
    lean(root, nodes)
    papers(root, nodes)
    doc_sections(root, nodes)
    scripts(root, nodes)
    results(root, nodes, cited_paths(root))
    preregs(root, nodes)
    manifests(root, nodes)
    commits(root, nodes)
    nodes.sort(key=lambda n: (n["kind"], n["id"]))

    if not a.report:
        json.dump({"corpus": str(root), "nodes": nodes}, sys.stdout, indent=1)
        return

    by_kind, flagged = {}, {}
    for n in nodes:
        by_kind[n["kind"]] = by_kind.get(n["kind"], 0) + 1
        for fl in n["flags"]:
            flagged[fl] = flagged.get(fl, 0) + 1
    print(f"  {'kind':<18} {'count':>6}")
    print(f"  {'-'*18} {'-'*6}")
    for k in sorted(by_kind):
        print(f"  {k:<18} {by_kind[k]:>6}")
    print(f"  {'-'*18} {'-'*6}")
    print(f"  {'TOTAL':<18} {len(nodes):>6}\n")
    print(f"  {'conformance flag':<22} {'count':>6}")
    print(f"  {'-'*22} {'-'*6}")
    for k in sorted(flagged, key=lambda x: -flagged[x]):
        print(f"  {k:<22} {flagged[k]:>6}")


if __name__ == "__main__":
    main()
