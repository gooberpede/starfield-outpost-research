# C3 completion and independent review package

2026-10-18, Australia/Sydney. SOR-EXP-0046 / SOR-EV-0054.
[Original frozen brief](../../../implementation-briefs/CODEX_BRIEF_SOR_C3_intersystem_cargo_fuel_and_timeskip.md),
[adopted scope](contract.md), [executive answer](report.md),
[finite checks](../../../../research/c3-fuel/README.md).

## Mandatory acceptance matrix

| Original criterion | Implementer result | Evidence and limit |
|---|---|---|
| 1. Actual fuel source, threshold, quantity, withdrawal and modifiers | PASS, scoped STATIC | native.md; installed ingredient five, 108-second base interval; transitive source virtual +458 withdrawal; mode-0 charged bypass versus mode-1 recheck. Current runtime deltas not measured |
| 2. Stage/endpoint asymmetry, four fuel combinations and ordinary control | PASS, shipped PEX / STATIC | stages.md eight endpoint rows plus ordinary control; receipt precedes query; either non-mission side admits reverse freight/next departure; supply during an already admitted leg treated separately |
| 3. Failure, retry, inventories/timers and replenishment | PASS, shipped PEX / STATIC | timer 2 repeats unload, redistribution and query; retained hold, newly available space, independent fuel cycles and either-side recovery; no direct fuel debit by a failed poll |
| 4. Production/storage/one-shot freight through skips and lifecycle | PASS, conditional arithmetic | time.md two reproducible cases, exact cached conversion/quantization, actual elapsed branch rules, capacity qualifications, ordinary distant/wait/travel/reload distinctions. No universal throughput or fast-travel ordering |
| 5. Saved-instance runtime correspondence | PASS, scoped SAVE / STATIC | saves.md and save01.json: four pads/two stocked inter-system ships, role/owner links, transitive source He-3 counts and producer payloads; AV 000338 binding. Specific VM/timer instances and historical epochs explicitly unqualified |
| 6. Separate future reconciliation backlog and boundary correction | PASS, documentation | BACKLOG.md new application preserves UI enhancement and historical C1/C2/S1/S2 entries; conditional consequences, conservation, ordinary-rule/balance distinction and no mod authority |
| 7. Proportional registers/provenance, checks, permissions and preservation | PASS, checked metadata | 23 protected baseline files plus brief/HEAD/index; definitions, script/member reread, native/source ledgers, 68 C3 checks and 68 regression tests; no game/save/config/database/Git mutation |
| 8. Independent ACCEPT, final exact package and prose review | NOT TESTED until final independent receipt | Local final package/seal paths below control acceptance. A preliminary scientific review cannot accept later unreviewed bytes |

## Primary evidence, checks and preserved deviations

`.local-work/c3-fuel/baseline.json` freezes HEAD
`5cdc57aea397da2a76695da7f547a1c033cf9156`, the unchanged supplied brief and
the index. It pins 23 protected EXE/ESM/archive/save/stopped-database files;
C: and D: preflight availability exceeded 40,000,000,000 bytes. Native jobs
001–005 ran in the existing readOnly/noanalysis Ghidra project. The worker was
stopped through its sentinel after acquisition, with no forced termination.
Postflight rereads verify protected inputs, HEAD and index unchanged.

`definitions01.json` binds fresh installed ESM fields; `modifiers01.json`
retains the bounded A1 candidate review and exact field bytes. `scripts01.json`
freshly matches five PEX and five source members and closes the five PEX decodes.
`save01.json` reads the protected original through disposable decoded scratch,
frames 205,557 R3 records and 246 local edges, and qualifies the stated 944-record
selection. Native functions.csv locates positive exports; sources.csv binds raw
local outputs, helpers, reused primary evidence and protected identities.

`verification01.json` records **68 passing finite C3 checks**. The regression
receipt `regressions01.json` records **68 passing tests**: inventory 35, framing
6, streaming 9, extractor identities 11 and authored-text validation 7. Fixed
arithmetic and byte/locator checks do not execute game/VM code or prove a
historical consumption event. No new runtime validation was attempted.

Retained deviations in `errors01.json`: the shell's Python alias was unusable,
so the installed full executable path was used; an initial local helper named
inspect.py shadowed stdlib inspect and was renamed show_native.py; a diagnostic
tried a 16-byte payload format against an actual 17-byte producer payload and
was corrected to `iiBff`; two interior native selectors in job 002 returned
NO_FUNCTION_AT and were corrected to true entries in job 003. None is absence
evidence. The large fresh constructor export retains its cap/incomplete
decompilation; the named charge binding uses the earlier complete primary export
plus fresh helper/setter. Failed attempts are not relabeled passing captures.

An early independent pass identified an endpoint/ship noun ambiguity and
“periodic per-stage fuel accounting” in the new backlog prose. The implementer
corrected both, separating periodic consumption from stage readiness. The
reviewer must inspect the final changed prose in context for missing spaces,
compressed number/unit phrases and grammatical defects, beyond automated checks.

## Exact review artifacts and final disposition

Both coverage patches are retained locally:

- `.local-work/diffs/c3-fuel-final01-task-only.diff`: task-authored changes only.
- `.local-work/diffs/c3-fuel-final01-complete.diff`: every uncommitted text change
  since HEAD, including the unchanged supplied untracked brief.

`.local-work/c3-fuel/package-final01.json` binds the complete/task-only file
inventories, SHA-256 values, patch hashes, exclusions, link/whitespace/encoding
checks and exact forward/reverse reconstruction in disposable .local-work/review-patches trees.
The exporter compares each resulting file byte-for-byte with the actual tree,
verifies reverse applicability against the actual tree and leaves HEAD/index
unchanged. `status-final01.txt` preserves `git status --short`. Ignored raw game,
save/decoded/native data, databases, local tools/receipts and reconstruction trees
are disclosed exclusions; none is cleared for publication by a textual patch.

The independent final response is retained verbatim at
`.local-work/c3-fuel/independent-review-final.md`. The final seal
`.local-work/c3-fuel/final-seal.json` binds that response, exact package/patches,
checks, protected postflight and reviewed authored bytes. Criterion 8 is PASS
**only if** that final response says ACCEPT and the seal confirms the same
snapshot. Otherwise the assignment remains REWORK/NOT REVIEWED as applicable;
the implementer's matrix alone supplies no independent acceptance.

Scientific result: complete bounded ordinary fuel mechanism, STRONG STATIC with
positive SAVE corroboration. Historical epochs/current effective readiness and
specific saved VM/timer correspondence remain unmeasured/unqualified. Engineering
checks are finite evidence/accounting checks, with no native execution. Target
survival is not applicable: no game was launched or touched. Authority compliance
and protected input preservation are checked separately from semantics.
Authored work remains REVIEW-REQUIRED; raw payloads LOCAL-ONLY. Await maintainer
critical integration review; no staging, commit, push or publication follows.

Suggested commit subject:
`docs(research): explain inter-system cargo fuel and time-skip behavior`
