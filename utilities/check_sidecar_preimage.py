#!/usr/bin/env python3
"""Gate: a locked prereg's sidecar must pin text that still exists.

BLUEPRINT § 9 corollary — a prereg's hash must stay verifiable after the
fact. If the text is mutated after locking (to fill in a Run record) and
the locking commit was not made first, the sidecar pins bytes that exist
nowhere: not in the worktree, not in git. The lock becomes unfalsifiable,
which is the one property it was created to have. Lock, commit, then run.

§ 5.8 is the other half: before building a mitigation, establish that
the thing being mitigated is actually lost. This gate is that one
command. It answers "is the pre-image recoverable?" instead of
assuming it is not.

For each preregs/<name>.sha256 the gate compares the digest against the
current file, and — failing that — against every blob of that path in
git history. It fires only when neither matches.

SCORED ON: /Users/juliansambrano/GitHub/Primebeat_081426 (2026-08-27),
9 preregs with sidecars. 8 fires, all 8 true positives; the ninth,
multibase_synthesis_v1_20260827.md, is recoverable at commit cc74c3c —
the one locked under the lock-commit-then-run discipline. 0 false
positives. Runtime on that corpus: ~1.4 s (22 `git show` calls).

The 8 fires are legacy state in the scoring corpus, not the steady-state
cost. Under the discipline this gate enforces, every prereg is
recoverable from its own locking commit and the gate is silent; it
speaks only when a locked file was mutated without being committed
first, which is the defect.

Degrades to silence: no preregs/ directory, no *.sha256 in it, or no
git repository (a sidecar is then checked against the worktree alone
and unverifiable ones are reported without a history claim).
"""
import hashlib
import pathlib
import subprocess
import sys


def _git(root, *args):
    try:
        r = subprocess.run(["git", "-C", str(root), *args],
                           capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout if r.returncode == 0 else None


def _sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def check(root):
    root = pathlib.Path(root)
    pdir = root / "preregs"
    if not pdir.is_dir():
        return []
    sidecars = sorted(pdir.glob("*.sha256"))
    if not sidecars:
        return []
    has_git = (root / ".git").exists() and _git(root, "rev-parse", "HEAD") is not None
    fails = []
    for side in sidecars:
        want = side.read_text(encoding="utf-8", errors="replace").split()
        want = want[0].strip().lower() if want else ""
        md = side.with_suffix("")
        if md.suffix != ".md":
            md = side.parent / (side.stem + ".md")
        rel_md = md.relative_to(root)
        if not md.is_file():
            fails.append(f"{side.relative_to(root)}: no {rel_md} to verify")
            continue
        if _sha256_bytes(md.read_bytes()) == want:
            continue                      # pins the current text
        if not has_git:
            fails.append(
                f"{rel_md}: sidecar digest {want[:12]}… does not match the "
                f"current file, and there is no git history here to recover "
                f"the pre-image from")
            continue
        log = _git(root, "log", "--all", "--format=%H", "--", str(rel_md))
        found = None
        for commit in (log or "").split():
            blob = subprocess.run(
                ["git", "-C", str(root), "show", f"{commit}:{rel_md}"],
                capture_output=True, timeout=60)
            if blob.returncode == 0 and _sha256_bytes(blob.stdout) == want:
                found = commit
                break
        if found is None:
            fails.append(
                f"{rel_md}: sidecar pins {want[:12]}…, which matches neither "
                f"the current file nor any of its blobs in git history — the "
                f"locked text has no recoverable pre-image, so the lock "
                f"cannot be checked (BLUEPRINT § 9). Lock, commit, then run.")
    return fails


if __name__ == "__main__":
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else \
        pathlib.Path(__file__).resolve().parent.parent
    out = check(root)
    for line in out:
        print(f"GATE RED  {line}")
    sys.exit(1 if out else 0)
