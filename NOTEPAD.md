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

- [open]   2026-08-27  entry 7: § 6's three recommendations were tested by construction — two died, the shipped set differs, and the best gate (label-parity) was one § 6 never proposed; blueprint amended in place so the delta has provenance
- [open]   2026-08-27  entry 7: selection rule found by building — gates that scan MUTABLE state ship, gates that scan the APPEND-ONLY record cannot ever be silent when clean; § 6 had not stated it
- [open]   2026-08-27  entry 5: build the three gates § 6 scored and kept — flag-from-or-chain, numbers-in-prose over the record, throwaway-invocation warning; blueprint recommends them, container does not yet implement them
- [open]   2026-08-27  entry 6: A14 throwaway-invocation warning is unscoreable — no corpus of past invocations exists; recording them for a period is its own slice before it can ship
- [open]   2026-08-25  entry 2: run adjudication 001's back-translation round — decorrelated reader, module path only, diff against the quoted claim
- [open]   2026-08-25  entry 1: discharge the domain-agnostic leaf — instantiate the container on one project outside formal research

