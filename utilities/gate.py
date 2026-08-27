#!/usr/bin/env python3
"""The container's gate. Exit 0 when the record is self-consistent;
exit 1 with one line per failure.

Checks:
  1. The required files exist and are non-empty. The contract file is
     any one of AGENT.md / CLAUDE.md / CONTRACT.md (BLUEPRINT § 4.1
     invites renaming it for whatever generator you use).
  2. lab_notebook.md entries: header format, sequential numbering
     from 1, a real calendar date, and a type parsed from the
     contract file's own vocabulary block — one source, no hardcoded
     copy to drift from it.
  3. NOTEPAD.md thread lines: strict format, a valid status, every
     "entry N:" pointer resolving to an entry that exists — and any
     description that mentions "entry N" WITHOUT the pointer format
     is red, because a one-character typo must never silently defeat
     the dangling-reference check.
  4. A code fence left open at end of file is red: an unclosed fence
     hides everything after it from this parser.
  5. In a git repository, core.hooksPath must be set. Git never runs
     hooks from a tracked directory, so a fresh clone has the
     pre-commit hook file and does nothing with it — commits would
     sail through ungated, silently. The gate detects its own
     bypass. Skipped before git init, so the seed workflow is clean.
  6. The BLUEPRINT § 6 checks, each scored against the Primebeat_081426
     corpus before adoption and each silent on a tree that has nothing
     of its kind to check (entry 6):
       check_flag_or.py           § 5.7  verdict flag from an `or` chain
       check_rule_labels.py       § 5.1  prereg labels absent from its script
       check_sidecar_preimage.py  § 9    sidecar with no recoverable pre-image

Hazards this parser is built around, all paid for upstream: several
files in this tree contain examples of themselves, so the notebook
scan SKIPS fenced blocks and the NOTEPAD scan reads ONLY the section
after "## Threads". Patterns use [0-9]+ and matches are counted.
"""
import datetime
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_flag_or          # noqa: E402
import check_rule_labels      # noqa: E402
import check_sidecar_preimage  # noqa: E402

# BLUEPRINT § 6: each scored on a real corpus before adoption, each
# returning [] on a tree with nothing of its kind to check.
SUBGATES = (check_flag_or, check_rule_labels, check_sidecar_preimage)

ROOT = pathlib.Path(__file__).resolve().parent.parent

CONTRACT_NAMES = ["AGENT.md", "CLAUDE.md", "CONTRACT.md"]
REQUIRED = ["BLUEPRINT.md", "CONTEXT.md", "REFERENCES.md",
            "NOTEPAD.md", "README.md", "lab_notebook.md"]

STATUSES = {"open", "paused", "closed", "blocked"}

ENTRY_RE = re.compile(
    r"^## Entry ([0-9]+) — ([0-9]{4}-[0-9]{2}-[0-9]{2}) — ([a-z]+) — (.+)$")
THREAD_RE = re.compile(
    r"^- \[([a-z]+)\] +([0-9]{4}-[0-9]{2}-[0-9]{2}) +(?:entry ([0-9]+): )?(.+)$")
STRAY_ENTRY_RE = re.compile(r"\bentry [0-9]+")


def unfenced_lines(text):
    """Return (lines outside ``` fences, fence_open_at_eof). Files
    here contain examples of themselves; a fenced template must never
    parse as content — and an unclosed fence must never hide real
    content."""
    out, fenced = [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return out, fenced


def valid_date(s):
    try:
        datetime.date.fromisoformat(s)
        return True
    except ValueError:
        return False


def parse_types(contract_text):
    """Parse the entry-type vocabulary from the contract file: the
    fenced block following the '`type` is one of:' line. First word
    of each line in the fence is a type."""
    lines = contract_text.splitlines()
    for i, line in enumerate(lines):
        if "`type` is one of:" not in line:
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip().startswith("```"):
            j += 1
        types = set()
        k = j + 1
        while k < len(lines) and not lines[k].strip().startswith("```"):
            words = lines[k].split()
            if words:
                types.add(words[0])
            k += 1
        return types
    return set()


def hooks_bypass():
    """Return a failure string when this is a git repo whose hooks
    are silently inactive; None otherwise (including pre-git-init)."""
    if not (ROOT / ".git").exists():
        return None
    try:
        r = subprocess.run(["git", "-C", str(ROOT), "config",
                            "core.hooksPath"],
                           capture_output=True, text=True)
    except FileNotFoundError:
        return None
    if r.returncode != 0 or not r.stdout.strip():
        return ("git repository with core.hooksPath unset — git never "
                "runs hooks from a tracked directory, so commits on this "
                "clone are ungated; run: "
                "git config core.hooksPath utilities/hooks")
    return None


def main():
    fails = []

    bypass = hooks_bypass()
    if bypass:
        fails.append(bypass)

    contracts = [n for n in CONTRACT_NAMES
                 if (ROOT / n).is_file() and (ROOT / n).stat().st_size > 0]
    if not contracts:
        fails.append("no contract file: need one non-empty "
                     "AGENT.md, CLAUDE.md, or CONTRACT.md")
        types = set()
    else:
        types = parse_types((ROOT / contracts[0]).read_text())
        if not types:
            fails.append(f"{contracts[0]}: could not parse the entry-type "
                         f"vocabulary (the fence after '`type` is one of:')")

    for name in REQUIRED:
        p = ROOT / name
        if not p.is_file():
            fails.append(f"missing required file: {name}")
        elif p.stat().st_size == 0:
            fails.append(f"empty required file: {name}")

    entries = set()
    nb = ROOT / "lab_notebook.md"
    if nb.is_file():
        nb_lines, nb_open = unfenced_lines(nb.read_text())
        if nb_open:
            fails.append("notebook: a code fence is left open at end of "
                         "file — everything after it is hidden from this "
                         "gate; close the fence")
        expected = 1
        for line in nb_lines:
            if not line.startswith("## "):
                continue
            m = ENTRY_RE.match(line)
            if not m:
                fails.append(f"notebook: malformed entry header: {line!r}")
                continue
            n, date, typ, _title = m.groups()
            n = int(n)
            if n != expected:
                fails.append(f"notebook: entry {n} follows entry "
                             f"{expected - 1}; numbering must be sequential")
            expected = n + 1
            if not valid_date(date):
                fails.append(f"notebook: entry {n}: invalid date {date}")
            if types and typ not in types:
                fails.append(f"notebook: entry {n}: type {typ!r} outside "
                             f"the contract file's vocabulary")
            entries.add(n)
        if not entries:
            fails.append("notebook: no entries found")

    np_ = ROOT / "NOTEPAD.md"
    if np_.is_file():
        text = np_.read_text()
        marker = "## Threads"
        if marker not in text:
            fails.append("NOTEPAD: missing '## Threads' section")
        else:
            body_lines, np_open = unfenced_lines(text.split(marker, 1)[1])
            if np_open:
                fails.append("NOTEPAD: a code fence is left open at end "
                             "of file; close the fence")
            for line in body_lines:
                if not line.startswith("- "):
                    continue
                m = THREAD_RE.match(line)
                if not m:
                    fails.append(f"NOTEPAD: malformed thread line: {line!r}")
                    continue
                status, date, ref, desc = m.groups()
                if status not in STATUSES:
                    fails.append(f"NOTEPAD: unknown status [{status}]")
                if not valid_date(date):
                    fails.append(f"NOTEPAD: invalid date {date}")
                if ref is not None and int(ref) not in entries:
                    fails.append(f"NOTEPAD: line references entry {ref}, "
                                 f"which the notebook does not contain")
                if ref is None and STRAY_ENTRY_RE.search(desc):
                    fails.append(
                        f"NOTEPAD: description mentions an entry without "
                        f"the 'entry N: ' pointer format, so the reference "
                        f"is unchecked: {line!r}")

    for mod in SUBGATES:
        fails.extend(mod.check(ROOT))

    if fails:
        for f in fails:
            print(f"GATE RED  {f}")
        sys.exit(1)
    print(f"GATE GREEN  contract {contracts[0]}, "
          f"{len(REQUIRED)} required files, {len(entries)} notebook "
          f"entries, NOTEPAD consistent, {len(SUBGATES)} § 6 checks quiet.")
    sys.exit(0)


if __name__ == "__main__":
    main()
