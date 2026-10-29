# D5P-R1 offline result — resilient recorder, retail NO-GO

2026-10-29, Australia/Sydney. [Brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5P_R1_observer_resilience_context_repair.md),
[pre-repair diagnosis](d5p-r1-diagnosis.md), [design/schema](d5p-r1-design.md),
[review](d5p-r1-review.md), [source ledger](d5p-r1-sources.csv),
[held operation plan](run-card-d5p-r1.md).

**Ordinary drops no longer retire the recorder. The final compiled observer
recovers after capacity and bounded-retry losses, preserves later witnessed
chains, and rejects joins crossing loss. The original retail context failure
cannot be identified from the retained operands. Retail remains NO-GO; no R1
deployment ZIP or executable retail card is issued.**

| Element | Scoped result |
|---|---|
| Question | Can the existing eleven-hook observer diagnose invalid context and survive ordinary observation loss without false causal chains? |
| Answer | The recorder and ordinary-context diagnostics are corrected and exercised in disposable Windows processes. The original failed type/Grid/extent/membership predicate remains UNKNOWN. |
| Confidence/basis | PROVEN / RUNTIME for the enumerated disposable controls and authenticated records; STATIC for pinned native ABI/layout inspection. No retail reliability or selected-source finding. |
| Coverage | Final build04: 57 native process cases, 56 reader oracles, 10 damage controls and a valid segmented-derivative reconstruction. Exactly 15,228 acknowledged records across the native case receipts. |
| Completeness | Complete only for those declared checks. Historical context operands, alternate runtime contexts, general trampoline unwinding, all aliases and actual retail burst timing remain unvalidated. |
| Publication | Authored changes REVIEW-REQUIRED. Native/raw/binary/private receipts LOCAL-ONLY. B6/publication remain on hold. |

## Corrections and actual qualification

The plugin remains eleven hooks. Version 0.2.0/schema 2 adds stable first-failure
context reasons and bounded read/operand diagnostics. It distinguishes the
provider's retained Grid from the current manager Grid and separates unsupported
observer extent from malformed native extent. No predicate is loosened to make
the selected source appear. The generator's inherited `grid` parameter alias was
corrected to `definition` after native inspection; the argument is forwarded
unchanged. The fixture original ignores it, so definition semantics are not
claimed as dynamically validated.

Ordinary admission losses have separate capacity and retry-exhaustion counters.
They advance conservative global continuity and continue acquisition. Bounded
worker batches retain raw-flush/ACK-flush barriers, disk guards, nonce/STOP and
resident fail-safe behavior. The reader separates session completion, authentic
prefixes, provisional tails, contradictory geometry and qualified causal chains.
CRC-valid observations after corruption or a missing segment survive as orphans;
they cannot bridge the damage. A known failed ACK flush cannot promote its tail.

Build and repeat all native controls using installed CPython/MSVC/MASM/SDK:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B runtime/retained-population/build.py r1-reproduction
```

The directory name must be fresh. The script reads pinned installed inputs,
writes only its exclusive ignored build, and runs disposable hosts. It does not
launch Starfield, deploy through Vortex or operate on protected saves. Individual
control invocation is the built `sor-d5p-fixture.exe`, exact DLL path, fresh
output folder and scenario name. All commands, source copies, generated guards,
logs, raw records and expectations are retained in
`.local-work/d5p/r1-build04/`; `qualify.py` contains the executable oracles.

| Native control | Final observed outcome |
|---|---|
| Context reasons | 16 records: two valid ordinary/non-target contexts and 14 failures, covering read/partial-read, manager/type/Grid/membership, lifetime, retained-Grid mismatch and valid 257-member unsupported extent. |
| One/many capacity losses | Exactly 1 / 37 losses. Later authentic chains survive; the one-loss concurrent case has 1,097 records and 33 chains. Nested generation survives the many-loss case. |
| One/many retry exhaustion | Exactly 1 / 37 forced exhaustion losses, then authentic fresh chains. Injection temporarily changes a queue ticket to force 32 bounded positive-ticket retries. It does not reproduce natural CAS exhaustion or establish the historical cause. |
| In-flight loss | One exhaustion during an intercepted copy; nine admitted records include later completion/lookup, zero construction witnesses or complete chains. |
| Cross-loss / lost lifetime record | Each retains 1,033 records and zero cross-gap chains. A fresh post-gap reconstruction plus reuse produces one new chain in 1,040 records. |
| Unpaced transport | Eight producers, requested 250 ms production interval; 3,082 acknowledged records, 4,370,963 capacity losses, queue peak 1,024, later qualified chain and normal scheduled STOP. |
| Unpaced actual hooks | Eight producers repeatedly execute the patched provider without pacing; 2,058 acknowledged records, 101,817 capacity losses, queue peak 1,024 and 506 qualified chains within intact epochs. The final recovered construction/reuse survives to STOP. |
| Early/late output faults | Disk, raw write/flush and ACK write/flush faults are distinct. Each late fault preserves the earlier nine-record acknowledged chain; unconfirmed new tails never become qualified. No output recovery is claimed after fatal failure. |
| Lifetime/scientific regressions | Reset, destruction, erase, Grid clear, retirement and ABA reject old joins. Partial/failed append, contradictory geometry, owner/mode/descriptor changes, nested requests and concurrent misses retain their expected distinctions. |
| Crash/damage/segments | Actual crashes before drain and after ACK, missing terminal, torn header/payload/ACK, corruption, wrong identities and negative ACK count are discriminated. Three hash-bound offline parts reconstruct the original chain; corrupting the middle part leaves only authenticated later orphans. |

Context reasons 1–4, 6, 9–11, 13, 17–18, 20 and 25 are implemented first-failure
routes but were not individually forced through the full composite native
context check. Their source mapping was inspected; that is not an executable
test of every read failure. Neither the 319 historical failures nor a genuine
natural CAS retry-exhaustion event was reproduced.

For 64 unpaced hit calls, the small one-slot/two-point model averages 4.721875 µs
with observation versus 0.056250 µs with resident bypass. A valid bound-shaped
model with 256 members, 256 source slots, 256 resource slots and 64 points averages
99.189063 µs versus 0.056250 µs. These are measured means, not maximum latency or
retail safety guarantees. Malformed duplicate matching rows can require more
bounded traversal than that model. Flush stalls and hook work are distinct.

Filesystem creation timestamps give READY-to-terminal diagnostic intervals of
0.7661026 s for transport stress and 0.8899571 s for hook stress: approximately
4,022 / 2,311 post-READY acknowledged records per second. These wall-clock file
metadata intervals include setup/drain/STOP overhead; they are not QPC producer
durations. Historical captures have no event clock, so no exact comparative
retail burst-rate claim is supported. Native QPC timing and output write/flush
latency aggregates remain in the actual receipts.

## Preserved evidence and scientific impact

All 44 original local entries in the Phase B source ledger authenticate, including
the sealed archive; existing native exports remain pinned. The original 1,592
primary records still authenticate and provide zero selected-source chains.
All 319 demand records reached the copied owner/mode/descriptor stage before
failing later qualification. They cannot distinguish ProcGen type/read, Grid
type/read/extent or membership failure because those operands were not saved.
Static code and new synthetic contexts cannot reconstruct that missing state.

The historical unqualified stages remain explicit: 319 source demands, eleven
map lookups, seven query/mask pairs, 1,137 temporary/copy observations and six
completion snapshots. Four raw differing lookup outputs remain unqualified
reuse candidates. These observations do not establish retention, selected-source
mask, uninterrupted lifetime, absence or first construction. D5P Phase B stays
FAILED / UNRESOLVED. Accepted D5H/D5I conditional masks, geometry and persistence
findings are unchanged.

Build01 used a transitional schema and its original green receipt is retained.
Build02 failed a missing-reuse fixture oracle; that failure is not green evidence.
Build03 passed; independent native reruns covered loss, an ACK-flush fault and STOP.
Build04 incorporates engineering review's late-fault, definition-alias and latency
controls and passes the final suite. No failed development result is erased.

The final DLL SHA-256 is
`503464d3670ff00422303c10652b036cd0bc891d3f8f7cba9a22d9d396fb5667`.
A second compilation with `/Brepro` produces identical DLL bytes and unchanged
inputs; `.local-work/d5p-r1/reproducibility.json` binds the comparison and log.
This establishes same-machine reproducibility, not another compiler/SDK result.

## Protection and remaining decision

No game/Steam/SFSE launch, debugger attachment, deployment, Vortex change, save
operation, configuration write, staging, commit, push or publication occurred.
Only disposable native processes and task-owned outputs were written. Both disk
floors and the active archive-backed baseline were checked. Installed build pins
were hashed before/after compilation; original local evidence is rechecked for
delivery. No new protected-save rehearsal copy or full live-save audit was run;
unchanged original saves are not claimed on the basis of a new save audit.

The missing capability is the original failed predicate and its runtime operands,
or separately authorized new context evidence sufficient to validate that native
contract. The inspected code, ordinary fixtures and archived records exhaust the
available discriminator; weakening type/membership guards would fabricate proof.
General unwind/retail latency also remains unvalidated. The held plan therefore
cannot advance to installation or another trial. Independent review and exact
delivery determine acceptance of this bounded offline result, not retail GO.
