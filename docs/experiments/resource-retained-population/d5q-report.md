# D5Q offline construction and retained-population mapping

2026-10-29, Australia/Sydney. [Call/data map](d5q-call-dataflow-map.md),
[source ledger](d5q-sources.csv), [frozen criteria and review](d5q-review.md),
[invoked brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5Q_resource_construction_call_dataflow_mapping.md`).

**Native instructions join the request's cell enumeration to its selected
source, original-query mask sample, geometry attempts and source-map retention.
This supports an invocation-selection provenance route with a smaller storage
scope than a full ordinary-Grid scan. It does not qualify an observer, prove
continuous source lifetime, or identify Save52's historical first construction.**

| Element | Supported account |
|---|---|
| Question | How do compiled request, selection, mask, construction, ownership and reuse boundaries connect, and what would an invocation-selected witness establish? |
| Best-supported answer | Each nonnull cell contributor is copied into the provider's source slot. An unvisited pointer-map miss inserts a wrapper and synchronously calls generation. The original caller query, converted with current manager context, supplies the ordinary raster sample. Actual geometry copy and final retained ownership need separate witnesses. |
| Confidence | ESTABLISHED (static) for the instruction/call relationships in the map. The future observation strategy is INFERRED; historical query, source lifetime and full chain remain UNRESOLVED. These are proposed research accounts pending maintainer review. |
| Coverage | Pinned 1.16.244.0 ordinary cell/index/provider paths, two direct provider callers, ordinary/Special sampling distinction, region-copy ownership and known invalidators. Fresh export contains 22 explicitly requested function bodies; existing D5D/D5H/D5I/D5L/R3 evidence supplies bounded upstream and lifecycle context. |
| Completeness | The map accounts for the required boundaries and explicitly identified gaps. It is not a whole-engine caller/writer census, recovered source architecture, full population census, universal allocation contract or persistence model. |
| Evidence | Q01–Q19 in the claim ledger, exact export hashes and address windows, fresh installed/database pins, direct CALL and vtable backing-byte checks in local verification receipts. Existing executed fixture/live observations retain their original evidence envelopes. |
| Limits | Raw chunk payload does not retain sources. Dynamic emitter/type, concurrent cell/source mutation, manager stability and continuity to later retrieval require qualification. Static possible paths do not select the actual historical path. |
| Next step | First resolve relevant cell/source writers and synchronization against a retained Grid. A future observer could then be designed around a qualified natural selection witness; it needs a separate implementation/live brief. |

## Methods and provenance

D5Q-AC1–AC8 were frozen from the supplied brief before substantive analysis;
the original brief is retained unchanged. Starting branch is `main`, HEAD
`7c8a184dd2aeb2f065969880b0d3209c7921c69e`; only that supplied brief was
untracked. The local initial receipt records the Git index hash and status.
Installed EXE, main ESM, PlanetData and SFSE match R1's durable installed pins.
The EXE matches the brief's SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
All map addresses are preferred static VAs at image base `0x140000000`.

The 15 existing database files match R3's post-export record before and after
fresh extraction. The existing project is
`D:/ReverseEngineering/Starfield/GhidraProject/Starfield`, program
`Starfield.exe`. Installed Ghidra 12.1.2 and JDK 21 run only the established
`-readOnly -noanalysis` procedure. No reanalysis, symbol/type/comment edit or
database-content rewrite occurred. Four selected inherited native exports were
rehash-verified and read; the fresh export independently revisits provider,
both caller boundaries, emitters, chunk append/cleanup, conversion, sampler,
component search, resource traversal and region-copy/retrieval operations.

The command and local original reader are retained under
`.local-work/d5q/export01/`; `native.tsv` is proprietary LOCAL-ONLY evidence.
The reader adapts this repository's `ExploreD5L.java`, omitting automatic vtable
walks and accepting only the 22 explicit function requests. One request is an
interior address `0x14079c4a0`; Ghidra resolves its containing function to
`0x14079c470`, which is the entry used in the map. This is an explicit locator
correction, not an extra function or an inferred declaration.

Focused methods, all CPython stdlib or the existing approved local toolchain:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B .local-work/d5q/setup.py
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B .local-work/d5q/export.py
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B .local-work/d5q/verify.py
```

These commands document the executed local methods, not a portable public
checkout recipe. `setup.py` hashes explicit installed/database/export inputs,
records disk/HEAD/index/status and splits existing native exports into disposable
reading derivatives. `export.py` reuses that setup, emits the task-owned Java
reader, caches, command and logs, then compares database bytes. Its fixed
`export01` directory refuses overwrite; reproduction needs a fresh task label
and corresponding output paths. `verify.py` checks ledger windows and PE-backed
direct CALL/vtable arithmetic, writes checks/claim ledger and rechecks protected
pins. No script reads or writes saves or invokes game functions. Initial setup
was run twice during preparation; the second receipt preceded authored changes,
with the same HEAD/index/input identities and a fresh disk observation. No
historical evidence was replaced. Exact methods and outputs are hashed locally.

The initial ledger checks rejected two incorrect export locators: spatial lookup
was present in the inherited R3 export rather than the fresh explicit set, and
reset was in `native-full.tsv` rather than `native-owner-copy04.tsv`. Correcting
those source paths makes the focused checks pass; no evidence bytes or semantic
claim changed. The failed first verifier source and failure notes are preserved
locally. A passing hash or locator check is not proof of the interpretation.

Independent technical review then found a partial-range defect: the Q17 row
advertised standalone retirement through `0x140982c32` in R3's export, whose
relevant body actually ended at `0x140982b6c`. The original verifier accepted any
instructions inside a range. The corrected ledger splits Grid clear from
standalone retirement, cites the latter's actual owner-copy export, and the
verifier now requires both advertised endpoints. It also reproduces the missing
retirement endpoint in the rejected source. The review01 failure and pre-correction
verifier remain retained; scientific interpretations did not change.

Primary disassembly, native definitions and proprietary installed bytes belong
to Bethesda. Existing project research and exporter/package methods are reused
under SOR-P-0002 at the starting HEAD, with exact paths/hashes in the ledger.
Prior D5A–D5I and D5L–D5P/R1–R3 reports, native ledgers and review qualifications
remain controlling for inherited results. No new third-party implementation,
dependency, licence basis, contact or disclosure was introduced. Authored
synthesis is REVIEW-REQUIRED; raw/static/runtime evidence remains LOCAL-ONLY.

## What the mapping resolves

The selection route is concrete. The provider retains its Grid, looks up one
cell with the original Int2, enumerates that cell through virtual `+0x10`,
and processes entries in the materialized list. Fill, edge and corner emitters
append up to one, two or four nonnull contributor pointers in slot order. No
resource-eligibility predicate occurs in these emitters. Selection at
`0x14079fa90..0x14079fa93` means a candidate for this provider iteration;
later BIOM/visited/map/generator gates determine what happens to it.

The chunk representation is now explicit: 32 eight-byte entries and one
next-link in a `0x108`-byte allocation; caller-side endpoint/cursor iteration;
allocator-backed cleanup after the loop. Count is published before slot fill.
The provider reads the list after synchronous materialization returns, so this
is not evidence of the same interleaving demonstrated against the mutable Grid
vector. Nevertheless, no per-source reference is acquired by append or selection.
Caller ownership of chunks and source lifetime are different obligations.

Backward tracing from ordinary sampler `0x142339340` reaches the original
provider Int2 and selected manager descriptor, independently of the source-local
origin. Forward tracing reaches wrapper insertion, ordered resources and cell
attempts, actual destination copy, retained wrapper/collection and later lookup.
Mask determination and mask representation remain separate: the low nibble
comes from a raster byte, and the ordinary branch compares it numerically with
rarity. The Special branch separately uses zero/nonzero high-nibble behavior.
No individual bit-to-resource mapping is proposed.

The forward path retains adverse evidence: BIOM/component/readiness failure,
visited bypass, source hit, failed region append and partial point copy. Insertion
precedes generation; visited append follows synchronous return without proving
complete geometry. A valid copied region may be witnessed without proving the
entire intended population succeeded. A resource lookup shares a holder; a source
hit bypasses sampling. Those static reuse rules allow first-request dependence
under D5H/D5I's common-state premises, but do not reconstruct an actual first query.

## Comparison for future SFSE research

| Route | Useful evidence | Remaining qualification |
|---|---|---|
| Invocation-selected provenance | Directly identifies the source used by this provider iteration. Avoids claiming complete membership from scanning an unrelated mutable source-vector allocation. Small ordinary cell emitter output is traceable. | Dynamic cell/type, retained/current Grid relationship, source lifetime, invocation correlation, actual mask/copy/final owner and later reuse/Workshop ancestry. No safe detour or helper call is established. |
| Writer-qualified ordinary Grid | Could establish membership in the specific retained vector under a demonstrated coherent ownership protocol. | Relevant writers, growth/free ordering, independent suballocation extent, count-before-fill and all relevant source-retirement boundaries. Equal/readable headers do not suffice. |
| Unqualified larger/fixed scan | R3's altered-source fixtures show why increasing/removing the old bound can pass a logical allocation alias or read stale storage. | Rejected as a production solution. The counterfactual remains experimental, and production is unchanged. |

Neither remaining route is disproved. Cell-selection provenance solves a narrower
question than complete Grid membership. It must not silently be substituted for
the schema-2 zero-status qualification contract. A future diagnostic-only or
selection-based contract would need explicit versioning, independent qualification
and separate authority; D5Q changes no observer, schema, DLL or reader.

## Historical and safety boundaries

Existing D5B is a qualified contemporary consumer witness with historical
construction unknown. D5H/D5I supply conditional static first-successful-miss
alternatives; they do not record which happened. R2's 9,736 admitted records and
6,101 first-failure reason-24 demands never reached later membership predicates.
R3's 41 cases per unchanged/counterfactual build, 25 unchanged-DLL regressions
and allocator/race counterexamples are inherited executed disposable evidence,
not fresh tests here. D5P's original 319 context failures remain historically
unexplained. No existing execution envelope closes Q19's full historical chain.

The construction-to-reuse hypothesis is therefore still UNRESOLVED for Save52.
Source pointer equality, geographic/geometry equality and successful hash checks
cannot establish historical ownership. Persistence and post-load authority remain
UNCLASSIFIED by this assignment; no save serialization path was investigated anew.

Both caller-available disk floors exceeded 40,000,000,000 bytes before export
and at verification. No game/SFSE/Steam launch, game debugger attachment, Vortex
operation, installation, production build/edit, native invocation, game/config
write, save mutation, staging, commit or push occurred. Whole-save/backups audits
were not run because no save operation was in scope; no whole-save equality claim
is made. Relevant installed, analysis and selected primary evidence identities
were checked proportionately. Target survival/restoration is not applicable.

Independent review and delivery checks are recorded in the review document.
Acceptance concerns this evidence-linked account, not observer readiness,
integration, retail GO or publication. D5P/R3 retail NO-GO and B6/publication
ON HOLD remain unchanged.
