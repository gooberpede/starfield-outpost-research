# D5AC source and native evidence locator

All primary paths below are relative to the repository root and remain local
where marked. This is source-informed owned research under SOR-P-0002, reusing
D5V/W/Z and D5AB P1/P3/B2 methods. No new third-party implementation or licence
basis is introduced. [Report](d5ac-report.md), [tests](d5ac-tests.md).

## Version and attempt pins

Starfield 1.16.244.0 executable SHA-256 is
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Native locations use preferred static image base `0x140000000`; actual B2 module
base is recorded in its identity file. The observer DLL is
`9d2f0bab159f3ec23186426fb4833eb645578d2a43612bb2e8def6b1af455dcc`.
No installed executable or database is reanalysed or changed. Existing exports
suffice; their hashes, source pins and recorded original database provenance are
preserved rather than claiming a fresh Ghidra baseline.

The exact session root is
`.local-work/d5x/live/session-5ed302aea9da7dc2261163b3dd1816e670a3c2f39891f1ec8d20094afa72b3a1/`.
Its `identity.json` SHA-256 is
`60ab253002916e04cdce854345dfde49bb539dddea4dcf40f5f690704360beef`.
Schema is `sor-d5x/4`, PID 47984, creation FILETIME 134379890667956618,
QPC frequency 10,000,000 Hz. Raw SHA and frame sizes are in the report.
`ready.json`, `flush.jsonl`, `terminal.json` and the original B2 reader result
bind operating and durable-accounting identities. Exact per-file hashes are in
the local preservation/delivery manifests.

Attempt 001 is the distinct session ending `987ad`, PID 45524, one frame with
no terminal. Its [timestamp amendment](d5ab-b2-timestamp-amendment.md) and
[live ledger](d5ab-b2-live-ledger.md) preserve explicit retry authority. The
attempt-002 notes retain the original card, corrected package plan, phase ACKs,
postflight and reader. Archive hashes remain
`bed491d01a742ec4f8c3773ee76926d120cd613c7ea9934b68a1d7a4c2eef6f2`
for attempt 001 and
`f472f69b85e37a4715c1d713e91387e80d20d3518fc66a5b42b9709e0e733d88`
for attempt 002, at `.local-work/d5ab/B2-APPROVED-00N-archive/capture.zip`.
Current rehashing authenticates archive identity; the original B2 all-member
stream verification remains historical, not a newly executed archive test.

## Owned source and primary native graph

| Primary input | SHA-256 | Exact locator / use |
|---|---|---|
| `runtime/construction-winner/observer.h` | `bb5cccce9bd6fd390ee8a892f3403dc854d5ed0e7c9d89e31bd6592fb5dc8cd5` | Lines 45–78: loss, increment, emit and QPC-before-admission. Lines 91–152: inherited context and current lookup epoch. Lines 189–204: all fence/Cold rules. |
| `runtime/construction-winner/transport.h` | `deaf3ca0a70247c32efcd4644dbc4b1521a58e15b18985a0928605e94bea9f92` | Lines 23–25, 50–51: installed-site/fence-template binding. |
| `runtime/construction-winner/reduce_v4.py` | `f3a7e533210f0df9aac166aab49e7c728b830ff392488fa7b970eac8e9366419` | Exact reset triad at lines 65–88; allocation/lookup qualification thereafter; append and prior-decision checks in the final chain loop. |
| `runtime/construction-winner/read_capture.py` | `645b028a18ff2a2033d68719fe75ac6e9abd81d5f7bd4ccc25deacf9ce758ede` | `decode`, `reduce`, `inspect`: schema, sample-prefix and enclosing frame/ACK/terminal qualification. |
| LOCAL-ONLY `.local-work/d5z-visited/export02/native.tsv` | `869f0968f70236f336f99fa938282d3737ba208758298e1dc78f006fbed169e7` | Lines 2–253: constructor, empty map `0x14079d6f1..0x14079d720`, visited/lock `0x14079d722..0x14079d733`. Lines 303–387: destructor. Lines 870–957: reset map clear `0x14079de8d`, visited free/zero `0x14079de9e..0x14079deb8`, protected unlock `0x14079dec4`. |
| LOCAL-ONLY `.local-work/d5ab/p1-export01/native.tsv` | `27fe3e554236d1d03acddee2b26df26bcc0c976b1510fb60b54154fce29656a6` | Lines 763–855: standalone retirement, erase/unlock/free. Lines 856–1061: Grid clear, lookup `0x140982a24`, optional erase `0x140982a36`, free `0x140982af8`; no visited clear. Source constructor/publication and original P1 owner graph are in the same export and linked matrix below. |
| LOCAL-ONLY `.local-work/d5w/functions/14079f860.txt` | `672846097b588ed3b4d02a68deddb0f480aaa6853dbc357993933d85b4d1c06a` | Lines 220–263: visited scan, shared unlock, exclusive acquire `0x14079fcb3`, pointer lookup `0x14079fccb`. Lines 334–359: insertion call and key/wrapper stores. Lines 408–446: generator/reserve/store/exclusive unlock. |
| LOCAL-ONLY `.local-work/d5z-visited/closure.md` | `4e2ec44cbb9ab3c153c5399251183c9d3e465c8cbb5f30bf9e444370ffb0add3` | Representation and mutation proof; ordinary visited writer/alias/load closure. This synthesis is supported by its native exports and source ledger, not treated as raw observation. |

The [P1 source/lifetime matrix](d5ab-p1-source-identity-lifetime.md), especially
L01–L08 and L12–L18, supplies geographic publication, free, reset/owner and alias
premises. [D5V lifecycle](d5v-lifecycle-consumer-map.md) supplies holder insertion,
map retention/removal and lock scope; [D5Z](d5z-report.md) supplies constructor,
visited writers and complementary load clears. [D5AA ingress](d5aa-gameplay-transition-map.md)
is conditional gameplay context, not a recorded B2 caller trace. The source
graph is qualified ordinary compiled receivers and aliases; arbitrary injected
writers, corrupt objects and substituted vtables remain excluded.

## Reproduction outputs and preservation

The two new scripts are offline analysis only. Their docstrings state reads,
writes, dependencies and target/database effects. Exact script/interpreter and
input/output hashes, duplicate-output comparisons, unchanged production-source
pins, local primary/export/archive preservation and HEAD/index checks belong in
`.local-work/d5ac/verification.json` and the exact delivery manifest.
Event tables contain runtime pointer operands; they are excluded from Git along
with raw frames, archives, native listings and all existing analysis databases.
No new external source is consulted, reused or contacted.
