# NOTEPAD — the_container

One-line index of threads. Newest at top. Append-only by the
generator; status transitions ([open] → [paused] / [closed] /
[blocked]) are the operator's call.

Format (strict, for grep):

```text
- [STATUS] YYYY-MM-DD  entry N: terse one-line description
```

STATUS is one of: [open], [paused], [closed], [blocked]
"entry N:" points at the matching entry in lab_notebook.md. A
description that mentions an entry without that pointer format fails
the gate — the pointer is how references stay checkable.

Common greps:

```text
grep '\[open\]'                  # active threads only
grep '\[open\]\|\[paused\]'      # everything not closed
grep 'entry 1'                   # all lines pointing at entry 1
```

## Threads

- [open]   2026-08-25  entry 2: run adjudication 001's back-translation round — decorrelated reader, module path only, diff against the quoted claim
- [open]   2026-08-25  entry 1: discharge the domain-agnostic leaf — instantiate the container on one project outside formal research
