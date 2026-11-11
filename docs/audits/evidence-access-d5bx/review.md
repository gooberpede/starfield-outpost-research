# D5BX review record

**ACCEPT for the D5BX local qualification scope.** Independent review03
marked D5BX-Q1 through D5BX-Q4 COMPLETE and AC01 through AC12 PASS.
See the [original brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BX_Workshop_Root_Projection_and_Cargo_C3_Durable_Access.md)
and the [exact assets and method pins](assets.json).

## Review01

The reviewed delivery manifest SHA-256 was
`e6131d83e92478ace5e106ba329f23d5d37bc6a2e14457f52319a52f96ac5fb3`.
The reviewer marked Q3 COMPLETE and Q1, Q2 and Q4 INCOMPLETE. AC03, AC06–AC09
and AC12 passed for review01. AC01, AC02, AC04, AC05, AC10 and AC11 failed.
The engineering and scientific defects were nine missing canonical DA operands
and incorrect release sequencing. Editorial corrections included the Cargo
comparator key, final receipt bindings and legacy coverage prose in the ZIP.
The [investigation ledger](investigation-ledger.md) records the corrections and
the failed v2 baseline-parser attempt. A single read-only reviewer was active,
and review01 ended before the second review session. No specialist was used.

## Review02

The reviewer accepted engineering and scientific completeness on delivery
manifest SHA-256
`2ab7ed9c3dead25a58017aba771db3a4a737972ba607d0fc3bbc04cf6682b9ab`.
Q1, Q2 and Q3 are COMPLETE. Q4 is COMPLETE at the local qualification tier.
The overall return was editorial REWORK. The final delta distinguishes C2
and C3 marker counts, corrects the ALLA selection description, and records
point-of-use and register attribution. Candidate, reader and primary receipt
bytes carry forward from review02.

| Criterion | Independent review02 result |
| --- | --- |
| AC01 | PASS. Rehashed 13 protected entries and two frozen D5BU receipts. Applied reading, HEAD, tree and index matched. |
| AC02 | PASS. Direct comparison matched all 115 selected typed DA source rows and all 31 ledger counts. |
| AC03 | PASS. Rebuilt ZIP, all member pins and the exact 9,469-byte ledger matched. Archive refusals verified. |
| AC04 | PASS. Full original receipt, 848 roots, all member tuples, roles, owner states and all canonical controls matched. |
| AC05 | PASS. Original replay, normalized supplement, separate source comparison and semantic refusals verified. The historical intake gap remains disclosed. |
| AC06 | PASS. Clean Workshop input and source pins, observed opens and scratch writes matched. |
| AC07 | PASS. Direct comparison found byte equality and all four accepted Cargo path fields. |
| AC08 | PASS. The unchanged Cargo reader reproduced D5BU byte for byte. Changed C3 and wrong CORE witness refused. |
| AC09 | PASS. Twelve Workshop tests, eight adverse processes and an undeclared-read denial support the refusal paths. |
| AC10 | PASS. Local qualification, B6 preflight, later transfer and hosting remain distinct. |
| AC11 | FAIL in review02. Exact patch reconstruction, links and encoding passed. Two editorial corrections required. |
| AC12 | PASS. The distinct reviewer examined the brief, exact source, receipts, adverse effects and changed prose read-only. |

No game or debugger operation was in scope. The outstanding external-access
and B6 actions belong to the subsequent release sequence. Local evidence and
test effects are under ignored `.local-work/d5bx/run01/`. The complete patch
includes the user-supplied brief. The task-only patch covers the implementation
and audit changes.

## Review03 acceptance

The independent reviewer accepted the exact substantive delivery manifest
`delivery-review03.json`, SHA-256
`e3b8a84fc2011f5a25f8d4a7c5a1f4873357a9352ab19af42352315b3cda9dd0`.
Engineering and evidence, scientific completeness, and editorial all received
ACCEPT. Review03 confirmed that only six documents changed from review02.
The candidate, reader, method and primary receipt pins carried forward.

| Frozen question | Accepted result |
| --- | --- |
| D5BX-Q1 | COMPLETE. Full selected source-to-projection parity, including 115 typed DA sources, all 31 group counts and the exact ledger. |
| D5BX-Q2 | COMPLETE. The separate Workshop reader reproduced the full comparison using the staged ZIP, three CORE originals and pinned main ESM. |
| D5BX-Q3 | COMPLETE. The unchanged Cargo reader reproduced the accepted receipt with the exact C3 file and F040. |
| D5BX-Q4 | COMPLETE for local qualification. Exact custody candidates, methods, effects and release handoff are documented. |

AC01–AC10 carry forward as PASS from review02. AC11 passed the manual full
changed-prose check, exact forward reconstruction, reverse applicability, both
file inventories, UTF-8/LF, whitespace and links. The editorial screen reported
zero diagnostics. AC12 passed the separate read-only substantive and delta
reviews. Each review session ended before the next one started.

| Review03 export under `.local-work/diffs/` | SHA-256 |
| --- | --- |
| `d5bx-review03-complete.diff` | `89ff826e079fa0681a43190bdef93ef2d8d3aa975c3d2368c485fb6191072d8b` |
| `d5bx-review03-task-only.diff` | `40faab1c925452fcbe6fd653a25f7b8b6f5129083be51b2b0e7897a9b16ab5ea` |

This transcription is the only post-acceptance authored delta. The final
delivery manifest and exports are named `delivery-final.json`,
`d5bx-final-complete.diff` and `d5bx-final-task-only.diff`. The complete export
contains the supplied unchanged brief. Publication remains NOT READY /
NOT CLEARED. 7B retention, 7C clearance and freeze, independent B6 preflight
and authorized hosting and download verification remain downstream.
