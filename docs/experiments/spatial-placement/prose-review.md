# Contextual prose correction

2026-10-19. The maintainer requested an occurrence-by-occurrence review of
uncommitted documentation for missing spaces between words and numbers or
identifiers, with independent challenge and no commit or push.

The review covered the eight modified documentation indexes and all newly
authored Markdown in the L3 package. The supplied implementation brief remains
unchanged. Each correction was selected in context; no blanket replacement
rule was applied. A discovery-only character-pair scan supplemented reading.
Its first console run stopped on a Unicode arrow because of Windows console
encoding; rerunning with explicit UTF-8 output completed the discovery pass.

Corrections separate ordinary prose from values and references: radius 150,
retail 1.16.244.0, beacon ff029ab6 and solar ff03aaa6, for example. Save33,
Save35, other Save labels, research IDs, filenames, hashes, function addresses,
export labels and the literal display label KREET OUTPOST1 remain intact.

The [native descriptor explanation](native.md) now lists memory offsets in a
table and spells out integer mode values. Hexadecimal memory/vtable offsets,
status codes, form types and masks have explicit `0x` notation. Change-state
bit 24 is distinguished from mask `0x01000000`; the reference flag uses mask
`0x04` at offset `0xd3`. These clarify the existing observations and do not
promote confidence, extend coverage or supply missing screenshot identities.

The historical [research acceptance](review.md) and its ignored evidence
receipts remain preserved. That acceptance applies to its original bytes;
the present prose correction requires its own actual independent decision.

Local review artifacts are retained under `.local-work/l3-prose-spacing/`:
`baseline.json`, exact before-text copies, `approved-edits.json`,
`scope-check.json` and `package-review01.json`. The package identifies complete
and task-only patches under `.local-work/diffs/`, their hashes, file inventory,
encoding/link/whitespace checks and disposable forward/reverse byte checks.
The task-only patch starts at the maintainer's correction request; the complete
patch starts at HEAD and includes the unchanged supplied brief.

The independent reviewer must challenge the edits against the before-text and
current native evidence where notation is ambiguous. Its actual decision is
retained locally as `independent-review01.md`; ACCEPT applies only to the
unchanged reviewed manifest. Any REWORK requires correction and another review.
This record does not preassign the outcome or authorize integration/publication.

CSV evidence ledgers, executable research code and original local research
receipts are outside this text correction. No game, debugger, Ghidra worker,
save mutation, staging, commit, push or network action is part of this task.
