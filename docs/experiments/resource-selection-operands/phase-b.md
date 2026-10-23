# RG2-C1G Phase B: effective native weight and chance admission

2026-10-23 Australia/Sydney. **The live candidate used exotic inactive weight
0.05, admitted IL cell (10,1), rejected IL (11,1), and admitted Copper (11,1).**
This validates the missing effective-input explanation at the chance stage for
one newly observed generating source. It does not establish the generating
history of C1E's cached regions or their final geometry in this session.

[Historical Phase A](report.md), [unchanged approved card](run-card.md),
[native operand map](native.md), [review/matrix/package](phase-b-review.md),
[exact source pins](phase-b-sources.csv). Primary memory, receipts, saves and
native exports remain LOCAL-ONLY; authored synthesis REVIEW-REQUIRED.

## Authority and execution

The maintainer explicitly approved the completed Phase B card after Phase A,
including independent review and diffs. That subsequent approval supplies live
authority; the original Phase A brief and its ACCEPT supplied none. The local
`phase-b-baseline.json` retains the verbatim instruction and initial clean main
HEAD `bbe1f075e3e7850f6bcfae45e5586819ed0d506b`, index SHA256
`a425a8f5be2df6bafdbe53f5901ecb3a31c38d88511b0a1fabaf59f142b7056e`.
Historical documents, predictions and the approved card are retained unchanged.

Fresh operator confirmations were “Confirmed—Steam Cloud is disabled” through
postflight, then “At main menu; no save loaded”. Ordinary Steam URI dispatch was
2026-10-23T00:58:24.8988313Z; the new pinned Starfield PID 6248 started at
00:58:28.0541564Z. EXE version 1.16.244.0 and all 39 installed definitions, plus configuration,
matched the approved baseline. SESSION measured module base `0x7ff603980000`;
the four guarded RVAs were `0x79b520`, `0x79be20`, `0x79a59e`, `0x79ff1d`.
Preferred static VAs in the card are not runtime pointers. Build05/controller
bytes were unchanged; no plugin, injection, executable patch or cache reset.
Hardware execution breakpoints pause execution and change owned DR/RF state.

One pre-admission wrapper dispatch failed: PowerShell converted the ISO UTC
string to locale text `10/23/2026 00:58:24`, rejected by Python's `fromisoformat`.
This happened before approval consumption, output creation or attachment.
Python JSON/list argument transport corrected the invocation for the same PID;
`timestamp-dispatch-correction01.json` preserves the failure and correction.
There was one Steam launch, one actual attachment, no controller rebuild/retry
and no replacement process. Fresh approval/consumption receipts bind this run.

After all 95 startup thread-arm readbacks, the operator loaded Save52/HIST-0267
(SHA256 `6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`).
The operator reported “After loading Save52, while fast-travelling to P3.” as
the time the game closed. **Build mode was not completed.** Natural generation
during that navigation already met the card's useful-evidence predicate, so
`ACK 1455 STOP` initiated authorized disposal at provider return. No relaunch or
additional action was needed. This is controlled evidence-completion retirement,
not an unexplained crash or a completed build-mode observation.

## Direct observations and scoped comparison

All three observed invocations have manager owner key 385246 (decimal),
corresponding to PNDT FormID `0x0005e0de`.
Identity is PID/TID/thread-lifetime/token, not token alone: each thread's token
was 1. The signed frame fields below describe the anchor X/Y, nominal dimensions
10 × 10, padding 2 × 2 and raw dimensions 14 × 14. These eight signed 32-bit
integers begin at byte offset `0x10` (16 decimal) from the source object's base
address. These are source-grid values, not world positions. Counts, coordinates,
owner keys, capture numbers, thread IDs, lifetimes and tokens are decimal;
FormIDs, RVAs, addresses and numeric bit patterns use the `0x` hexadecimal prefix.
Quoted source identifiers and byte sequences retain their original spelling.

| Entry → return captures | TID / lifetime | Origin | BIOM FormID | Anchor | Ordinary IRES call order |
|---|---|---|---|---|---|
| 1 → 581 | 5076 / 24 | (-3800,-1400) | `0x000fc61c` | (-36,-12) | `0x0083ec`, `0x0057ce`, `0x0057cb` |
| 582 → 1018 | 6292 / 27 | (-6200,1000) | `0x00145440` | (-60,12) | `0x0057d4`, `0x0057d0`, `0x0057cf` |
| 1019 → 1455 | 19416 / 30 | (-3800,-200) | `0x00145440` | (-36,0) | `0x0057d4`, `0x0057d0`, `0x0057cf` |

IRES references are main-file qualified by captured file provenance. The last
source is the card's candidate and has the frozen origin/frame of
`0:25116:32448:00257f38`; that is a conditional correspondence, not an epoch join.
The first corresponds to frozen `0:25116:32436:002c5878`; the middle source lies
outside the frozen six-source footprint and is not assigned a historical source.

For both IL calls, the directly observed low 32 bits of XMM3 are `0x3d4ccccd`
(binary32 0.05000000074505806), agreeing with independently read setting payload
bytes `cd cc 4c 3d` (in memory order). Cell chance is 15.0. Rarity 3 and ordinary mask 8 are observed;
INACTIVE is **DERIVED_STATIC_PREDICATE_NOT_BRANCH_TRACE**, not a direct branch
trace. Copper uses binary32 0.3 and Cell chance 60; IRES `0x0057d0` and
`0x0057ce` use weight 0.2 and Cell chance 45; `0x0057cb` uses weight 0.3 and
Cell chance 60. IRES `0x0083ec`, with rarity 6, uses weight 0 and Cell chance 0
in its ordinary call.

| Candidate comparison | Capture | Observed draw×100 | Threshold bits / value | Observed edge |
|---|---|---|---|---|
| IL (10,1) | 1129 | 0.49152764678001404 | `0x3f400000` / 0.75 | ADMIT |
| IL (11,1) | 1141 | 10.240686416625977 | `0x3f400000` / 0.75 | REJECT |
| Copper (11,1) | 1431 | 10.240686416625977 | `0x41900000` / 18.0 | ADMIT |

Draw bits are respectively `0x3efba983`, `0x4123d9da`, `0x4123d9da`; edge is derived
from captured native CF after the comparison. The selected 560-byte DNAM is
captured in full, SHA256
`5c1b9ddec2b711570b392a60f4f303bbc8599432792a818f8141431a4f24217f`.
It equals definitions in both CanyonsDefaultRes and FrozenBarrenDefaultRes03;
byte equality does not select a unique RSGD. The captured component RSGD pointer
is null in all nine calls. **Effective concrete RSGD identity remains UNKNOWN**;
do not substitute the expected Canyons label. Candidate family root FormID `0x0057cf` is
observed separately. Selected descriptor bits and raw addresses remain in receipts.

The unchanged owned CRC/MT first-gate evaluator reproduces all 1296 joined
ordinary comparisons bit exactly from observed packed keys, owner, chance and
weight. All 864 applicable packed keys match the two frozen source requests.
CRC seed is DERIVED, not directly captured. Phase A's independently reproduced
single definition-backed 0.05 replay matches all four earlier C1E paths and avoids
the extra IL (11,1); that historical conditional result remains intact. The new
observations establish its effective-input premise for this new generation epoch.
They do not add a current final-path/competition oracle: an admitted Copper
attempt alone does not prove its final singleton survives. The earlier endpoint
counterexamples and frozen 156-path predictions are unchanged.

## Integrity, incomplete states and cleanup

1455 durable SRO1 receipts and 1455 accepted ACKs contain three entries, nine
ordinary calls, 1440 chance stops and three returns. All binary framing/digests,
exact SESSION/SAMPLE/END content, ACK hashes and thread sequences pass offline
readback. The EXIT record has code `0xc1c0` and reports `stopped=true`,
`captures=1455`, `open_invocations=0`; the controller exit code is 0, stderr is
empty, and there are no EXCEPTION/LOSS records. There are 1454 verified resumes;
the final acknowledged capture is deliberately not resumed. Maximum copied
bytes per stop (2005) and copy time (16 ms) are observed metrics, not scientific quotas.

**1311 receipts have complete required bindings; 144 do not.** Captures 437–580
in the first invocation have complete read groups and entry/frame association
but no ordinary resource-call join: their observed outer return corresponds to
preferred static VA `0x14079c11c`, rather than the ordinary return at preferred
static VA `0x14079be25`. Actual runtime return addresses use the measured module
base plus the corresponding RVA. They remain raw END `complete=false` and
OUTSIDE_ORDINARY_CALL_CONTRACT diagnostics, excluded from ordinary semantic
comparisons. This is neither silent evidence loss nor proof of their full
nonordinary ancestry. The candidate's required IL/Copper comparisons and terminal
are complete. No incomplete raw receipt was repaired or promoted.

Fresh prelaunch qualification passed 27 cases / 187 synthetic samples using the
approved build. Fresh preflight verified 271 live saves and 271 independently
recoverable master backups, 39 definitions, configuration, the EXE, four guards/call
destinations and a Save52 scratch restoration rehearsal. Actual Documents is
outside OneDrive and has no reparse ancestor. The additionally discovered Steam
userdata namespace had 255 files (254 saves plus metadata), separately inventoried
and copied outside game/sync writes before launch. Both source and backup copies
were independently hashed. Monitoring used lightweight bounded log tails,
stderr and the free-space guard of 40,000,000,000 bytes (40 GB) on each of C:
and D:, with no full live-tree rescans.

After target/controller exit, primary postflight and secondary namespace audit
found no added, missing or changed files in those protected namespaces. No save
restoration or configuration repair was necessary. All 4043 pre-task protected
pins, including earlier C1E evidence, Phase A and frozen predictions, remain
unchanged. The 2914-file closed attempt was losslessly archived, every member
stream-hashed against retained originals; seal and preservation receipts are
listed in [the source ledger](phase-b-sources.csv).

The new [offline analyzer](../../../research/resource-selection-operands/analyze_live.py)
reads closed receipts plus pinned frozen/installed-definition records and writes
one fresh local JSON. It uses the project's existing decoder, selector and
CRC/MT evaluator; no dependency or outside code was added. It is a scoped
positive-run forensic verifier, not a general no-hit/failure verdict tool.
From repository root, with no target process required:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-selection-operands/analyze_live.py --receipts .local-work/resource-selection-operands/retail-attempt01 --output .local-work/resource-selection-operands/pilot-analysis-reproduction.json
```

Evidence integrity and the card's acquisition objective PASS. Target survival:
intentionally disposed after evidence. Save preservation PASS; restoration none.
Scientific coverage: directly observed new-epoch effective operands/chance stage;
historical ancestry, native walk/competition/final cached paths and P3 consumer
join remain UNKNOWN/NOT OBSERVED. No broad persistence conclusion follows.
The next discriminator would join generation output to installed/consumed region
geometry in one epoch under a separately reviewed brief and approval. No further
live work, integration, staging, commit, push, external disclosure or B6/publication
clearance follows from this completed session.
