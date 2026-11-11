# D5AD active investigation ledger

2026-11-02, Australia/Sydney. Original contract: [D5AD brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AD_initialization_save_load_reconstruction.md`).

Frozen controlling question: When Starfield starts and loads the exact protected Save52 in the Lodge, how is the resource-generation state that later destination streaming uses established?

Baseline HEAD: `890440d14476be02b6ff715bbfed4cb873f37611`. Initial index and tracked tree are clean; the supplied brief alone is untracked and predates task edits. Authorized scope is offline only, with no game, deployment, original-save writes, database edits or Git integration. Actual Ghidra temporary-file housekeeping and procedural deviations are disclosed below. Raw inputs and receipts remain LOCAL-ONLY. D5R remains OPEN.

| Branch | Question | Disposition | Evidence / next action |
|---|---|---|---|
| L01 | Q1 source-to-ready inputs | OPEN | Reconcile D5V/W/Z, then trace concrete loaders and deferred guards. |
| L02 | Q2 actual Save52 ordering | OPEN | Reconcile B1/B2 checkpoints and D5AC reset triads against primary records. |
| L03 | Q3 saved/reconstructed state | OPEN | Reverify protected copy, native global-type-3 readers/writers and landscape/world dependencies. |
| L04 | Q4 Lodge handoff | OPEN | Join L01–L03 without promoting possible requests to observations. |
| L05 | AC01 provenance | OPEN | Fresh identity, tool, protected-copy and disk receipts pending. |

Initial checkpoint: brief and governance read; historical D5Z result separates transient visited storage from serialized world inputs. No D5AD scientific conclusion or checklist tick yet.

## Primary-evidence checkpoint

Fresh baseline receipt `.local-work/d5ad/baseline02.json` authenticates 54 inputs,
including the installed executable/ESM/PlanetData, existing database roster,
protected research copy and B2 records/notes. Save52 retains SHA-256
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
The receipt's status is its capture-time status after early task files existed;
the initial clean tracked/index and sole untracked supplied brief were observed
before these edits. Both caller-available drive floors pass. The Python app
execution alias cannot run; the installed CPython 3.14 executable works. Early
database hashing appeared stalled; explicit chunk reads reproduced its expected
hash, and the original baseline worker later completed. No cause is assigned.

| Branch | Question | Current result / counterexample | Disposition and next action |
|---|---|---|---|
| L06 | Q2/Q4 Lodge checkpoint | Fresh raw/ACK audit finds 383 source births and 383 publications before acknowledged record 876, plus one empty reset and Grid fences. Zero provider calls in that prefix. | RESOLVED at recorded-boundary scope; inspect body/Grid identity limits before interpreting Lodge demand. |
| L07 | Q2 reset after checkpoint | Actual second triad 881/882/883 follows prefix QPC; 47 Grid clears precede provider 2470 and change observer epoch without clearing visited. | RESOLVED at recorded-boundary scope; caller and visual-load clock remain OPEN. |
| L08 | Q3 opaque type-3 tail | Read-only selected-block and full-stream oracles agree: two empty auxiliary lists and 88 typed rows exhaust the remaining 892 bytes. | Native typed writer/deferred-reader validation ongoing; no semantic name assigned to opaque u32 values. |
| L09 | Q1 raster prerequisite | Fresh native trace shows generator acquisition, pending-state handling and a synchronous map-load opportunity before sampling. | OPEN: finish upstream DB/definition loaders and failure paths; resident raster at Lodge is not necessary for every later construction. |
| L10 | Q2 completion phases | Recovered LoadGame instruction sites establish synchronous revert/load/init/finish order; type-3 finish waits on a selected service. | OPEN: characterize actual Save52 branch evidence and prove the limits of extending that wait to all resource inputs. |
| L11 | AC06 invalid control | First chronology assertion wrongly rejected source birth/publication in the Lodge prefix and failed before output creation. | DISPROVED assumption, preserved failure in test history. Corrected detector permits metadata and independently rejects provider activity. No scientific absence claim from the failed method. |

The frozen Q1–Q4 remain open. These positive boundaries do not close actual
startup construction, all readiness chains or full historical Save52 ordering.

## Independent challenge and additional upstream work

The early independent reviewer returns REWORK while mandatory offline avenues
remain. Four invalid reset-witness mutations were accepted by the first audit
despite the actual raw triads being valid. The corrected method explicitly
matches receiver, thread, epoch, status, hazards, empty operands and native QPC
for both B1/B2 triads; nine adverse cases pass in `chronology06`. This preserves
the method failure without changing original recorded evidence.

| Branch | Current evidence / counterexample | Disposition and next action |
|---|---|---|
| L12: finish phase | Fresh native export13 proves `0x142406950` publishes a component command; its body does not wait. | Earlier service-wait interpretation is superseded for D5AD; trace command callback `0x142417130` before claiming completion coverage. Historical D5Z wording is retained. |
| L13: actual saved destination | Native dispatcher case 9, not the initially assumed case 7, calls `0x141829ec0`. New read-only decoding identifies saved Lodge interior CELL and Jemison context with alternate-reference flag zero. | Resolve native success path from these actual inputs and state the remaining live/global guards. Unit 7 is a negative grammar control. |
| L14: startup construction | Reviewer identifies sole ordinary bootstrap caller `0x14189a69e`; export13 follows it into the tested missing-singleton constructor branch. | Follow singleton writers and normal initialization progression rather than treating the absent constructor timestamp as proof of unknowability. |
| L15: definition readiness | Generic `0x140594980` dispatches typed loader at vtable `+0x88`; PE/RTTI independently binds IRES and RSGD loader/postlink tables. Console ReloadFile callers are positively distinguished from normal workers. | Follow normal startup/load ingress and postlink completion. Console source is not ordinary startup evidence. |
| L16: original database housekeeping | Read-only Ghidra removed a temporary presave file; all 15 pinned core files still match. Disposable copy under dot-prefixed workspace was rejected; verified tools-root copy works. | Root also mistakenly used the legacy original-project launcher for export13 after announcing the move. Its log has no additional presave-removal line, and its core postcheck passes. Deviation is retained; no manual original cleanup. Later exports use the copy-specific launcher. |

Q1–Q4 are still judged against their original breadth. No terminal barrier has
yet been accepted; additional native/save work directly addresses the reviewer's
highest-value omitted avenues.

Procedural deviation: root restarted the independent reviewer before the save
specialist finished. The live agent inventory briefly showed three active
sub-agents, exceeding the brief's maximum of two. Root immediately interrupted
the reviewer and continued with two specialists. This is a failed concurrency
constraint, not a revised limit or a scientific counterexample. No full original
procedural-conformance claim is made; the final review must retain this event.

## Third science challenge

The reviewer accepts the startup/admission edge as concretely constrained by
the event wait and ordinary manual-load dispatch; no invented total timestamp
trace is required. It identifies a further material Q3 lead:
`SurfaceTreePatternSwapInfo_Component` could affect the reused surface hierarchy
if consumed. The earlier capability wording exceeded the evidence; the final
factory result does not demonstrate that mutation.
The existing surface-tree seed/reuse account does not classify that component's
save/reconstruction provenance. L17 remains OPEN while the save specialist
traces its producers and persistence boundary. The reviewer is interrupted
before restarting that specialist, preserving the two-active-subagent limit.
Q1's ordinary definition-ingress edge remains active as L15; generic typed
loaders and postlink joins alone are not substituted for that missing edge.

L15 closes at question-level science review. The concrete subclass is
TESPackedFile, not the stub TESFile base: startup enumeration constructs it,
inserts it into the same handler list consumed by definition loading, and its
open method supplies explicit success/failure paths before typed dispatch.
The reviewer independently authenticates all 216 windows across 41 inputs and
judges Q1 COMPLETE for the original qualified ordinary contract. Its full
return is retained at `.local-work/d5ad/review04-q1-return.md`. Exact-final
integration/editorial review is still pending; L17 remains actively open.

L18 follows a concrete alternative serializer: global type 7 dispatches to
`0x1418b22c0`, paired with writer `0x1418b1eb0` in `0x141824a60` case 7.
The nearby earlier surface-tree creation route makes this a material persistence
lead. Using type 7 as a negative destination grammar control does not classify
its actual contents. The save specialist pursues this edge alongside the BFCB
component factory and SFTR changeform virtuals; base-form flags alone cannot
exclude a separate global serializer.

L18 is positively material: type 7 restores a distinct PCM manager seed and
two content maps. The sampled payload is nonempty, 335,338 bytes, with 478
outer entries. Fresh controlled-copy/independent selected-block decoding agrees.
The specialist now follows BlockContent and placement serializers and the
actual Save52 entries. The earlier three-seed account is therefore incomplete
as a full state inventory; no Q3 closure is claimed from the type-3 tail alone.

## Final branch reconciliation

The independent reviewer finds all four scientific questions complete and
accepts the three checklist ticks under the original qualified contracts.
The closing delta return and final manifest bind the integrated delivery
snapshot; no procedural exception is self-approved.

| Ledger branches | Final scientific outcome | Exact result / retained boundary |
|---|---|---|
| L01/L09/L15 | COMPLETE: Q1 | Concrete ordinary plugin class/open/load/postlink/module chain, component/source producers, PCM preparation and deferred raster guards. Entry-state/default controls challenge unsupported readiness assumptions. |
| L02/L10/L12/L13/L14 | COMPLETE: Q2 | Startup admission, actual Save52 Lodge operands, sequential restoration, corrected queued type-3 finish and observed reset/source boundaries form the specific-load partial order. L10's early wait interpretation is superseded by L12. |
| L03/L08/L17/L18 | COMPLETE: Q3 | Full sampled type-3 and type-7 framing, state lifecycle, independent PNDT joins, SFTR factory/changeform boundary and PCM consumers/revert/finish are traced. The earlier three-seed account is superseded by explicit persisted PCM seed/content. |
| L04/L06/L07 | COMPLETE: Q4 | Lodge metadata and separately derived ProcGen emptiness join restored PCM/context state and later destination preparation. Historical reset callers, per-row resolution/refresh and deferred completion clocks remain unrecorded, not falsely observed. |
| L11 | DISPROVED method assumption; corrected | Metadata construction is allowed before Lodge. Corrected reset matching rejects the four formerly accepted corruptions alongside five other adverse cases. |
| L05/L16 and concurrency deviation | Scientific preservation PASS; full procedural conformance FAIL | Final 84 selected original/copy inputs and unchanged HEAD/index pass. Original Ghidra housekeeping/legacy use and three-active-specialist interval remain execution-history facts requiring maintainer disposition. |

The PCM follow-up follows saved placement state through game-day/flag retention,
residual generation, preparation records and ready request publication. It also
distinguishes content replay/world activation, revert map clearing and deferred
finish-ID cleanup. Registry name lookup/insertion share the same interned key
namespace; the direct alias/shutdown census closes the concrete alternative
population lead. These resolved branches answer the original scope rather than
discarding it after an adequate-looking type-3 report.

Final preservation is in `.local-work/d5ad/verification.json`. Promoted PCM and
registry methods preserve frozen local originals; current output agrees with
the historical state/rows, with explicit LF normalization where required.
The first preservation/promotion comparison refusals and provisional matrix
encoding damage are retained and explained in the methods record. None is
relabeled as successful evidence. Final editorial, inclusion and exact patch
checks bind the closing review snapshot. D5R remains OPEN; publication ON HOLD.
