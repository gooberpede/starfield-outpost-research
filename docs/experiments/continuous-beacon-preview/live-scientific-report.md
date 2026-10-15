# SOR-EXP-0035 — Save3 continuous unplaced-preview result

2026-10-15, Australia/Sydney. SOR-EV-0043 / proposed SOR-F-0034.
[Authority and actual procedure](live-attempt-01.md), [native contract](native.md),
[offline engineering acceptance](validation.md), [review](review.md).

| Element | Best-supported scoped answer |
|---|---|
| Answer | Continuous native preview evaluations and independently constructed UI rows recover Iron + Helium-3, Iron + Alkanes + Helium-3, then Iron + Helium-3, agreeing with the operator's A/B/C displayed lists. |
| Confidence | Direct native argument/population/row observations and transport integrity are proven within this sampled session. Displayed agreement is a scoped STRONG result based on independent operator testimony; exact rendering time and unique asynchronous ancestry are unresolved. |
| Coverage | Approved 0.7.0, retail 1.16.244.0, protected Attila Kiraly Save3 on Kreet; 35,573 preview evaluations plus one initialization evaluation, 346 complete UI updates, 611,926 verified records. |
| Completeness | Every recorded evaluation and UI update decodes completely with status zero; this does not establish coverage of unhooked engine paths, other sites/builds, all geography or deterministic input reconstruction. |
| Result | Milestone A PASS within the observed phase/set scope; independent ACCEPT, awaiting maintainer critical review. Milestone B NOT TESTED and remains separate. |
| Protection | Normal exit and observer removal verified; all 6,847 protected content pins match. No construction, manual checkpoint, console, debugger or instrument change was requested/performed. |

## Phase agreement and timing

Markers record receipt of operator reports, not exact render timestamps. CPython
`perf_counter_ns()` uses the Windows performance counter; dividing by 100 maps
receipt values into the captured 10,000,000-Hz QPC domain. UTC receipt times below
are distinct from native invocation intervals. Entire constant-population runs
containing each report were examined, including every completed UI callback in
those runs. No nearest-event rule chooses a producer ancestor or a render event.

| Phase | Report receipt, Sydney | Operator labels | Complete preview evaluations in containing stable run | UI updates in that run | Native row identities |
|---|---|---|---:|---:|---|
| A | 10:52:35.076 | Iron, Helium-3 | 18,397 | 3 | `0057c7`, `0057f5` |
| B | 10:57:44.135 | Iron, Alkanes, Helium-3 | 3,964 | 10 | `0057c7`, `0057c9`, `0057f5` |
| C | 10:59:15.042 | Iron, Helium-3 | 2,271 | 2 | `0057c7`, `0057f5` |

All IDs here are runtime FormIDs independently resolved to `Starfield.esm`
definition identities in this installed plugin context. They are not save tokens,
pointers or file offsets. Hash-bracketed installed ESM scans resolve Iron to
`ResInorgCommonIron`, Alkanes to `ResInorgUncommonAlkanes_G`, and Helium-3 to
`ResInorgCommonHelium3_G`. Exact file offsets, record types and source hashes
remain in private definition receipts; [source ledger](sources.csv) pins them.

The stable-run boundaries are native population changes, not asserted times when
the operator started or finished moving. A contains invocations 13258–31672
(QPC 892264951470–895270987991), B 31673–35706
(895271096503–896273388037), and C 35707–37989
(896273514997–896861738504). Counts exclude child invocations. Initial exploration
also includes three earlier preview runs with 10,602 / 86 / 253 evaluations and
315 / 2 / 14 UI updates; no operator label report was supplied for those runs.
They are retained without manufacturing additional displayed phases.

The short live tail inspections had no callbacks because they sampled stationary
cached windows. Complete-session decoding finds earlier callbacks in every A/B/C
stable run, resolving that inspection limitation. UI rows remain a native
data-model channel; independent displayed lists come from the operator. No
screenshot or direct Flash render observation was acquired.

## Actual argument, source populations and native rows

All 35,573 preview calls are observed at RVA `0x21b42e3` with evaluation-time
indexed descriptor, held placement reference and raw populations. Sampled
A/B/C proposed XYZ are approximately (264.799866,379.944519,22.629501),
(348.092224,376.197388,21.243870), and
(264.798340,379.944580,22.629593), respectively. Frame 0 and the captured domain
remain consistent in these samples. These are native indexed coordinates; no
new world/geographic conversion or global site equivalence is claimed.

The held reference has base `Starfield.esm:015804`, STAT
`OutpostGroupPackinDummy`, rather than the placed ordinary-beacon base. It is the
actual preview placement context captured from the held native reference. Its
full lifecycle relationship to a placed beacon is unresolved; it was not
substituted with player position. Player stationarity was neither required nor
independently measured. The operator explicitly reports moving the proposed
beacon without placing it.

The generated population changes between Iron alone and Iron + Alkanes;
atmosphere remains Helium-3 throughout. The third unfiltered biome population
contains Iron and Lead (`Starfield.esm:0057c1`, `ResInorgCommonLead`). Its presence
does not add Lead to the displayed list: the native third-source branch admits
selected water only. No selected special append contributes a row in this
session. Lead is not classified as a UI false negative or extractor result.

For all 346 UI callbacks, exact common-consumer inputs are independently folded
by pointer identity in first-occurrence order, then actual selected append inputs
are considered. Final row census and completed constructor operands associate
identities with committed row ordinals. All 346 input-versus-row reconciliations
AGREE; all rows resolve, with no missing ordinals or reported overlap/instability.
There are 339 three-row and seven two-row updates: one initial set, five changed
sets and 340 unchanged redeliveries. This is an identity-based reconciliation,
not a comparison of display-field bytes mistaken for FormIDs.

Refresh is distinct from set change: 346 evaluations return refresh predicate 1,
of which five change the recorded populations and 341 do not (including initial
delivery); 35,228 return zero with unchanged populations. Thus the acquisition
retains repeated evaluations, and a native refresh does not imply a new set.
Measured source-change→first same-set UI callback intervals are available in raw
QPC evidence; they are not rendering latency or proof of a unique producer cause.
Queue-allocation correspondence has one candidate per UI command here, while
source-content producer correspondence ranges from one to 18,487 candidates.
Even a single content candidate does not prove a snapshot-free causal edge.

## Transport, cleanup and save protection

User cancellation and explicit STOP ended acquisition. Actual retirement at
11:00:05.530 Sydney reports admitted/written/durable 611,926, zero failures and
zero active calls. The approved complete WAL inspector independently verifies
every record's ordering, length and SHA256, pairs all invocations, checks the
terminal counts and reports `RETIRED_INTEGRITY_OK`, errors empty. Raw length is
2,036,489,728 bytes. No output-size, time or event quota ended this run.

After operator normal exit, process PID/creation metadata reports EXITED; a
complete Toolhelp process inventory also finds no Starfield/SFSE match. The
runtime-required DLL is absent. `PASS_TRANSPORT_POSTFLIGHT` checks all 6,847
protected inputs, frozen observer sources and approved build prerequisites;
`SEALED_INVENTORY` hashes the retired session files. Observed C:/D: free space
always exceeds the 40,000,000,000-byte floors. The ten approved CALL replacements
remained resident/inert until normal exit; this was disclosed instrumentation
that could affect timing. No hot-unpatch, unload, forced termination, save
restoration, additional instrumentation or game-configuration edit was performed.

The pre/post active save inventory remains 261 files. Normal exit produced one
new Attila Kiraly ExitSave and removed the preceding active ExitSave; original
Save3 remains 2,096,496 bytes with SHA256
`d06123ee32bd5b3e244650852fac9714697a19fd6243384966414d1d1f4ffbfe`.
131 existing files have metadata-only timestamp changes; all retain identical
lengths/content hashes. Their cause is not directly observed, including whether
Steam synchronization explains them. There are zero modified-content existing
saves. No original was overwritten or restored by Codex. New ExitSave contents
were not used as a semantic oracle.

Private receipts are under
`.local-work/continuous-beacon-preview/run-20261014T233433728771Z/`; raw session
is `.local-work/continuous-beacon-preview/live/session-24552-88395531`.
Approved `operate.py postflight`/`seal` and `inspect_resources.py` were unchanged.
Original read-only private summarizers read their output, markers and installed
definitions, and write exclusive local derivatives; they do not access target
memory, edit saves or use new dependencies. Postflight SHA256
`5c6a3e25d9e30d8ded42219e762d551d5398c598914c546af81bc6dca40f061e`;
session seal SHA256
`5836da47413f5223f57116070652674dcd3a81de653d58a40d5670e839d7231b`.

## Acceptance and remaining limits

| Criterion | Actual result |
|---|---|
| Exact approved deployment/preflight/READY/ACK/native guards | PASS; pinned card and unchanged 0.7.0, operator-deployed and operator-launched |
| Every recorded argument/population evaluation retained and decoded | PASS within ten-hook coverage; 35,574 complete evaluations, status zero |
| Independent complete native UI row/input reconciliation | PASS; 346/346 AGREE, no unknown rows |
| Display agreement in observed A/B/C set conditions | PASS scoped milestone A; operator testimony, native constant-population intervals and UI rows agree |
| Repeated/cached and changed/equivalent sets | PASS sampled; five changes, repeated identical evaluations and repeated UI deliveries |
| STOP/drain/normal exit/removal/protected postflight/seal | PASS actual, no recorder failure or corrupt tail |
| Exact rendering time / unique producer→UI ancestry | UNRESOLVED; no render capture or evaluation snapshot in queue |
| Complete deterministic offline reconstruction, milestone B | NOT TESTED; runtime argument/populations do not supply all generation inputs |
| Persistence, established-outpost equality, extractor footprint, other builds | NOT TESTED; outside this live question |
| Independent scientific review and exact cumulative/task-only package | PASS independent ACCEPT; full raw replay, separate struct-based UI reconciliation, sealed files, phase intervals and exact patches checked; [review](review.md) retains scope/limits |

Publication eligibility remains REVIEW-REQUIRED for authored summaries/source;
raw/proprietary/save/build/bulk derivatives remain LOCAL-ONLY. No staging, commit,
push, PR, release or disclosure follows from this result. The earlier offline
NOT TESTED classifications remain valid historical statements and are superseded
only for the explicitly measured live scope above.
