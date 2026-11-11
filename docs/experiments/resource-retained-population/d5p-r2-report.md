# D5P-R2 diagnostic preparation

2026-10-29, Australia/Sydney. [Brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5P_R2_retail_context_diagnostic_preparation.md`),
[pre-implementation adequacy decision](d5p-r2-decision.md),
[source ledger](d5p-r2-sources.csv), [review](d5p-r2-review.md),
[proposed card](run-card-d5p-r2.md).

**Unchanged R1 can discriminate the next recorded validator failure. No new
observer binary, native hook, selectable profile or schema is necessary.**
The new offline decoder explicitly distinguishes reached/read-valid operands
from unavailable values and leaves deeper ambiguities unresolved. The original
retail failure remains UNKNOWN. The retained-population hypothesis remains
UNRESOLVED; D5P Phase B FAILED and R1-AC3 UNVALIDATED are unchanged.

| Element | Supported answer |
|---|---|
| Question | Can the existing candidate identify why an admitted retail source-demand context is rejected? |
| Best-supported answer | Yes for its first failed validator predicate and safely retained operands; not every underlying native cause. |
| Basis/confidence | PROVEN / RUNTIME for enumerated disposable controls and emitted bytes; STATIC for unexecuted composite routes and retail ABI evidence. Diagnostic readiness is proposed pending independent review. |
| Coverage | Exact R1 build04, schema 2; 27 newly executed DLL cases, 25 standalone production-validator records, four damaged diagnostic-stream controls. No retail execution. |
| Completeness | Complete only for enumerated controls. Reasons 9, 10, 13 and 25 have primitive/read-source checks but no deterministic composite execution. Final-state lifetime subcauses, all alternate objects, natural CAS exhaustion and general unwind behavior remain unvalidated. |
| Publication | Authored text/code REVIEW-REQUIRED; raw/native/binary/private receipts LOCAL-ONLY. No B6/publication clearance. |

## Adequacy and minimal differences

The decision was written before any R2 code. An independent initial source
assessment concurred with REUSE UNCHANGED and identified the same validity,
later-hook overwrite and lifetime limits. The actual preliminary return is
retained under `.local-work/d5p-r2/`; final review is separate. The matrix defines
all reasons 1–26, actual short-circuit order, field offsets and unavailable data.

Production `runtime/retained-population/` sources and existing DLL are unchanged
from HEAD `8bb992737eba06833a4080f9338f46dd634654b2` / `main`. R1 version `0.2.0`,
eleven hooks and full scientific acquisition remain available. Diagnostic use
selects the same full behavior; its explicit card/reader label is not a runtime
profile switch. There is no honest overhead/volume comparison between different
profiles because there is only one binary/profile.

[The new decoder](../../../research/resource-retained-population/d5p_r2_diagnostics.py)
authenticates original single-file evidence with the unchanged independent R1
reader before interpreting only acknowledged demand records. It derives operand
validity from reached predicates. It refuses a changing capture or segmented
derivative rather than inventing continuity; original R1 segmented reduction
remains supported separately. Unknown/contradictory fields and noncomposite
primitive checks receive explicit UNRESOLVED labels. No mask/owner/source filter
is introduced. Successfully reading a null pointer differs from failing its slot
read. Later lookup fallback with invocation 0 is never joined to a demand.

Type expected RVAs remain available; absolute VAs require independently recorded
module-base metadata. R1 does not store that base. Reason 23 identifies the
lifetime predicate but cannot distinguish final hazard, epoch change or broken
recorder from stored starting samples alone. The generator fifth argument is a
definition operand captured at completion, not a Grid identity or demand-time
validator operand. Existing getter/forwarding evidence supports that distinction
statically; it does not establish definition semantics dynamically.

## Actual native qualification

Reproduce into a **fresh** ignored child with installed CPython/MSVC/SDK:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-retained-population/d5p_r2_qualify.py new-qualification-label
```

The runner reads existing R1 build04 and installed pins, executes the original
`sor-d5p-fixture.exe` against the original DLL, then compiles a separate disposable
[context harness](../../../research/resource-retained-population/d5p-r2-context.cpp)
including unchanged `observer.h`. It never rebuilds or replaces the DLL. Reads,
writes, prerequisites and target effects are stated in each script's header.
Source/build/raw outputs remain in `.local-work/d5p-r2/qualification01/`.

| Control | Observed result and qualification |
|---|---|
| Unchanged DLL context suite | 16 acknowledged records; reasons 0, 5, 7, 8, 12, 14, 15, 16, 19, 21, 22, 23, 24, 26. Two valid ordinary/non-target contexts survive; the standalone cross-page primitive record is not a composite invocation. |
| Expanded actual production validator | 25 native records; the oracle records reasons `[0,1,2,3,4,5,6,7,8,11,12,14,15,16,17,18,20,19,24,21,22,26,23,23,0]`. Each reason is independently checked against emitted bytes and read-validity decoding. |
| Read controls | All 18 read-reason labels execute the actual failing read primitive. Composite 9/10/13/25 remain statically inspected only: earlier reads and these small offsets share protected pages, so the harness does not claim realistic isolated composite coverage. Cross-page request 16 returns **0** bytes; no positive partial-copy payload is claimed. |
| First failure and extent | Malformed 2/1 extent yields 19; structurally admissible 257/257 yields 24 before a member-pointer read. Expected/observed type operands, different manager ProcGen, missing member and retained/current Grid mismatch decode separately. |
| Deliberate ambiguity | Starting hazard and broken-recorder controls both emit reason 23; decoder reports the same unresolved subcause family. It does not infer a final state from starting samples. |
| Nested/concurrent/address reuse | Original DLL nested and concurrent controls retain correlation; 33 concurrent reuse chains. ABA/reset block old joins. Native-shaped context changes are observations, not geographic target certification. |
| Forced losses and recovery | Capacity and retry-exhaustion: exactly 1/37 losses, continuing acquisition. Cross-loss/lost-fence/in-flight-loss controls yield zero cross-gap chains; fresh post-gap reconstruction yields one. Retry injection manipulates a disposable queue ticket; natural CAS exhaustion is not reproduced. |
| Unpaced actual hooks | Eight producers for the fixture's requested 250 ms interval: 2,122 acknowledged records, 91,085 capacity drops, 506 qualified intact-epoch chains; scheduled STOP succeeds. Final recovery remains recorded. |
| Unpaced transport | Eight producers: 2,807 acknowledged records, 3,849,521 drops; later fresh chain survives. High loss is preserved, not renamed complete coverage. |
| Fault/crash/worker controls | Late disk/write/raw-flush/ACK-write/ACK-flush failures preserve the earlier nine-record prefix; no unconfirmed tail qualifies. Actual before-drain/after-ACK exits, worker STOP and hook-guard failure remain distinct. |
| Diagnostic damage oracle | Torn tail retains 16 acknowledged diagnostics; first-frame corruption and torn ACK yield zero qualified diagnostics; wrong DLL refuses. Original evidence remains intact. Prior R1 corruption/segmentation controls remain a separately pinned regression baseline, not newly rerun segment tests. |

The separate harness writes raw Event bytes, not counterfeit plugin identities or
durability receipts. Its native oracle and file hashes establish those source-path
tests. Independently authenticated diagnostic records come from the unchanged
DLL's own recorder/CRC/ACK path. This distinction prevents standalone source
testing from masquerading as qualification of newly built plugin bytes.

Measured 64-call means: small ordinary hit **4.642188 microseconds** observed vs
**0.053125 microseconds** resident bypass; bound-shaped 256-member/256-source/
256-resource/64-point model **95.203125 microseconds** vs **0.062500 microseconds**.
Both timing cases retain 137 acknowledged records, no drops and 65 chains.
These are means, not upper latency bounds; malformed duplicate rows and retail
scheduling are not certified. Full-profile geometry traffic remains enabled.
No new hot-path work, unbounded queue or arbitrary acquisition quota was added.

## Original chronology and proposed diagnostic readiness

Primary Phase B demand sequences **106–1472** contain all 319 invalid contexts.
Fresh pre-load ACKs authenticate only startup. The original arrival-health receipt
reports terminal already present. READY/ACK/terminal file timestamps describe
filesystem receipt boundaries, not event times or operator milestones; no clock
correlation locates the first failure within load/travel/arrival. The card retains
Save52 load plus original travel to second Feynman V and a manual arrival endpoint.
No alternate source, replay or earlier endpoint is inferred.

The candidate is proposed for **separate retail GO consideration for first-failure
diagnosis only**. The card defines manual schema-2 identity/nonce/ACK validation,
read-only module-base capture, operator-owned Vortex/SFSE steps, protection and
disk guards, diagnostic sufficiency and thirteen-or-current-version postflight.
Schema-1 operation helpers remain intentionally unsuitable. The manual procedure
is reviewed preparation; actual retail READY/nonce admission is NOT TESTED.
Loaded/active, predicates exercised, discriminating durable record and full
scientific-chain qualification are separate outcomes.

R1 did not issue a deployment ZIP. The R2 distribution wrapper, if independently
accepted, contains its exact unchanged DLL and existing approved licence notices.
It introduces no dependency or new third-party implementation. The package
manifest separately pins wrapper bytes, reader/card, old build and current test
receipts. It is explicitly not a new observer build or retail GO.

The single proposed ZIP has SHA-256
`391b23f9cb3ec86e82da2d37886bdb3b9fd3b8566b0a1bfdc706f4f4083a2bb0`.
The unchanged DLL remains
`503464d3670ff00422303c10652b036cd0bc891d3f8f7cba9a22d9d396fb5667`.

## Preservation and delivery

All 59 local evidence rows selected from the original Phase B/R1 ledgers
authenticate, including the prior sealed archive and native exports. Installed
EXE/ESM/PlanetData/SFSE identities and all eleven 32-byte site guards match.
The qualification runner verifies original production sources and installed pins
again after tests, together with unchanged HEAD/index. Both disk floors pass.
No game, Steam or SFSE launch, debugger, deployment, Vortex action, protected-save
operation, configuration write, staging, commit, push or publication occurred.
No new save equality audit is claimed; unchanged content of untouched saves is
not established by source/build checks. Future preflight remains mandatory.

Final package/DLL/ZIP hashes, exact changed-file/status/exclusion manifests,
source/tool/evidence ledger, screen/manual editorial record, actual reviewer
returns and verified complete/task-only patches belong to the external
`.local-work/d5p-r2/final-delivery.json` binding. This avoids a self-referential
report hash. Final independent review controls disposition. No accepted offline
preparation resolves the original retained-population hypothesis.
