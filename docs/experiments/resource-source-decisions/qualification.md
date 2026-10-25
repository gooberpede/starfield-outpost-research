# D5E qualification and preservation record

[Report](report.md), [native contract](native.md),
[helper effects and commands](../../../research/resource-source-decisions/README.md).
The final exact-snapshot matrix and independent disposition are recorded in
[review](review.md). Raw commands, logs, receipts, assertions and failed attempts
remain under `.local-work/resource-source-decisions/`.

## Real disposable Windows matrix

Every scenario creates and attaches a separately hash-pinned disposable Windows
process. Four real hardware execution breakpoints, stopped-thread CONTEXT reads,
ReadProcessMemory, instruction guards, durable SRO1/readback ACKs and target exit
checks run through the inherited Windows design. This is not solely parser
qualification. Synthetic fields/epochs and explicit branch controls remain
synthetic; they do not independently establish retail field semantics.

The exact final build is `build09`; the complete default qualification output is
`qualification06`. All 22 scenarios PASS, with 2,362 durable receipts and 147
ordered selected-source decisions across the matrix. Both busy scenarios retain
all 44 expected selected-source decisions. The shared healthy pump and all three
failure pumps also PASS. These are actual Windows results, separate from the
fourteen invented-byte native reducer checks and unexecuted retail adapter.

| Required case | Reproducible fixture/configuration and expected observation |
|---|---|
| 1. Miss 0, repeated hit, bypass | Every normal scenario begins with MAP_MISS/A using query (37536,20928), mask 0 and actual retained allocation/insertion/completion, then MAP_HIT/B and VISITED_BYPASS/B. |
| 2. Separate lifetime, mask 3 | `reuse`, `reset`, `replacement`: change source epoch, manager epoch or manager identity respectively, preserve mask 0 and 3 as separate A results with unequal lifetime tuples. |
| 3. Busy unrelated sources | `interleave`, `threads`: four workers, 80 requests each, distinct unrelated sources and ten same-selected-pointer hits per worker. Initial three decisions plus forty worker hits plus final hit yield 44 selected decisions. No phase switch. |
| 4. Concurrency/nesting/lock order | The busy cases contend on an actual target mutex; unrelated misses can nest probe sequences without recursive lock acquisition. `nested` supplies an independent child invocation/parent. Encounter order is separate from completion order. |
| 5. Reuse without history/completeness | `bypass-incomplete`, `hit-unknown`: explicit B remains useful without a complete current population or observed historical constructor; first-ever stays UNKNOWN. |
| 6. Recycling/reset/stale | `reuse`, `reset`, `replacement`, `stale`: same-address source reuse changes an explicit fixture epoch; stale zero-epoch case is C. These are oracle witnesses, not a demonstration that native ABA is detectable. |
| 7. Incomplete/corrupt operands | `partial`, `failed-insert`, `invalid`, `misleading`, `corruption`: C for incomplete/failed construction, rejected invalid cross-process read or unrelated geography, modified SRO1 bytes refused by independent decoder. |
| 8. Slot/arm/gap/ACK/teardown | `slot-pressure`, `lost-slot`, `bad-ack`, `lost-sequence`, `stop`, `interrupted-teardown`: actual foreign/lost DR state, refused ACK, replay sequence loss, stop at durably persisted capture 4 and target death before ACK. Explicit GAP/terminal state, no later sampling/rearming and target absence are checked. Replay corruption/sequence mutations are offline derivatives of real captures. |
| 9. First construction then reuse | Normal first three requests share one fixture manager/source lifetime. Only the first constructs; the next hits and then bypasses. |
| 10. Pre-load arm and busy interval | Gate remains blocked until all-thread readback and durable ARM_ACK. Busy cases preserve all expected same-source decisions after that barrier; new threads arm before continuation. This qualifies the fixture barrier, not game load timing. |

The shared future native transport pump is additionally executed with a disposable
target in four cases: healthy basic acquisition, pre-arm STOP, idle collector
exception and idle control-pipe EOF. Pre-arm STOP must not publish READY or
release the fixture gate. Collector failure preserves a GAP receipt and retires
the controller; closed pipe triggers controller cleanup. The healthy pump checks
normal controller completion, while the three failure pumps and separate basic
test explicitly check target absence. No retail path is executed. There is no
arbitrary scientific duration/event cutoff; fixture startup and failed-process recovery have bounded
engineering waits because no operator/gameplay is involved.

The separate `native-tests02.json` records fourteen offline tests using invented
bytes: C-only miss, session/coverage binding, missing/duplicate/wrong-image/
synthetic session refusals, missing source/capacity/manager/query fields, sequence
loss, mask-only D, wrong instruction and refusal to use fixture epochs for native
input. These do not qualify cross-process native ABI reads. `event.schema.json`
is parsed, not validated by a newly installed external schema library.

## Preserved failures and corrections

- The WindowsApps Python alias could not execute. The installed CPython 3.14
  executable was used directly; no installation or settings change was made.
- `qualification01` exposed no-hit startup despite arm readback and then an
  overly brittle qualification assertion. The gated-main attachment sequence
  replaces create-under-debug startup; missing outcomes are reported, not indexed
  blindly. This is engineering failure, not scientific absence evidence.
- `qualification02` exposed the startup check rejecting already-owned slots.
  Exact owned-state reconciliation corrected it without admitting foreign slots.
- `qualification03` passed the earlier seventeen-case matrix, but is superseded:
  the final matrix adds stronger lifetime, stop, slot and transport-failure cases.
- Preliminary independent review required native session binding, named missing
  operands/coverage, unconditional STOP evidence, collector-failure cleanup and
  pre-arm cancellation. Corrections and actual returns are retained locally.
- `qualification04` retained an interrupted-teardown result lacking explicit GAP
  and a shared-pump import collision caused by an inherited module's search-path
  change. Unexpected target exits now emit GAP; the pump loads owned modules by
  exact path. `qualification05` is a focused real rerun of basic/stop/interrupted
  teardown plus all four pump paths; it passed. It does not replace the final
  complete default matrix.
- An optional Windows CIM process-I/O diagnostic was denied. No elevation or
  workaround was attempted; it is not needed for qualification or preservation.

Each attempt retains its build/source hashes, raw rows and stderr. Failed and
superseded outputs are never overwritten. The final build binds every quoted
transitive include, the installed compiler/linker hashes and compiler-version log.

## Preservation and regression scope

The unchanged owned D5D `audit.py` is invoked in-process with only its output
root changed to this task's ignored directory. The baseline records HEAD/index
and initial status containing only the supplied D5E brief. Before-audit verifies
78,435 inherited pins, including existing D5B captures/receipts, native exports,
frozen evidence and all fifteen analysis-project files; the after-audit compares
exactly that map. The original 12,974-row protected-save/content manifest is read
under current SAVE_PROTECTION: qualified active transients are diagnostic, while
designated/manual/quicksaves, backups and historical evidence remain strict.
Both full audits PASS with equal 78,435-pin maps, unchanged HEAD/index and zero
protected changes. Protected receipts are byte-identical, with 173 qualified
active-transient exclusions. The actual executable file version is 1.16.244.0;
final Starfield and fixture process counts are zero. No original is modified.

`verification01.json` rehashes 405 inherited source pins. Ten exact native
geometry controls across twenty normalized/expanded comparison rows, plus the
frozen conditional-result digest, are checked for integrity **without rerunning
geometry or changing the predictor**. Original Feynman V contributes four,
Carinae three and Archimedes three. D2–D5D outcomes, D5A alternatives, D5B current
geometry and all seven indeterminate associations remain unchanged. This is not
a new native geometry, retail safety or historical construction validation.

Scientific result: explicit static decision/query/mask boundaries and tested
synthetic acquisition; the selected retail history remains OPEN. Engineering:
only executed Windows/offline scope is qualified. Target outcome: disposable
processes exit normally or are intentionally terminated/crashed; target absence
is checked. Authority: Phase A only, no retail/deployment/save modification or
Git publication action. Rights: raw native/private evidence LOCAL-ONLY, authored
work REVIEW-REQUIRED; B6/publication stays on hold.

`final-checks01.json` additionally verifies all 83 build-manifest pins and 76
per-use source pins, independently redecodes all 2,362 matrix receipts and
reproduces all 22 stored reductions after target exit. The independent reviewer
also checks the twelve pump receipts, for 2,374 receipt files in total. Hash
checks and synthetic passes remain separate from native semantic validation.
