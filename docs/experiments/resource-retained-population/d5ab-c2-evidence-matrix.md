# C2 primary-evidence matrix

2026-11-01, Australia/Sydney. [Audit](d5ab-c2-audit.md),
[original contract accounting](d5ab-c2-decision.md). PROVEN and DISPROVEN below
apply only to the proposition in that row. UNRESOLVED preserves a parent proof
obligation. No row upgrades an original D5AB criterion.

## Evidence locator and access key

All paths are repository-relative. `V` means bytes directly accessed in C2;
`R` means the historical execution outcome is receipt-reported, not rerun.
Line numbers are one-based in the original retained file; static locations use
preferred image base `0x140000000` and the executable pin in the audit. Source
line ranges refer to frozen current source unless a build copy is explicitly named.
Symbols are exact additional locators. No source/runtime address equivalence is assumed.

| Alias | Exact retained primary path / version | Access and boundary |
|---|---|---|
| E1/E2/E3/E4 | `.local-work/d5ab/lifetime-export01/native.tsv` through `lifetime-export04/native.tsv` | V; export hashes respectively `5cf9dd4007d733c2b5a901cfff62507b129bea90f9d03985dd9a311cdf8fbe97`, `dbb4581c69cfd848814a38616031e3013bb117abc6b354a205362007682a5c5c`, E3 has no preservation receipt, E4 `0b11b5edf86b8cb18ab23a547681ebdbde6791a6d46004c94b5ef54ebf1a0b68`. E3 is 2,110 bytes and incomplete. |
| P | `.local-work/d5w/functions/14079f860.txt` | V; provider assembly/decompile, hash `672846097b588ed3b4d02a68deddb0f480aaa6853dbc357993933d85b4d1c06a`. |
| N | `.local-work/d5ab/native-sites01/sites.json` | V; eighteen site guards/lengths/targets, existing export only. |
| O/A/T/H | `runtime/construction-winner/observer.h`, `bridges.asm`, `transport.cpp`, `worker_health.py` | V; Freeze01 versions; full hashes in C1 inventory and C2 local preservation manifest. |
| RR/RC | `runtime/construction-winner/reduce_v3.py`, `read_capture.py` | V; current hashes in audit. |
| B | `.local-work/d5x/d5ab-build08/build.json` and its `sources/`, `package-runtime/`, per-case directories | V/R; 697 output hashes verified, all match. Native source matches current; packaged reducer differs. |
| F | `.local-work/d5ab/controls-final02/receipt.json` | V/R; current reader/reducer interpret B sessions; explicit test constants in `research/resource-retained-population/d5ab_qualify.py` (Q). |
| K | `.local-work/d5ab/queue-final32000-02/receipt.json`, `queue_stress.generated.cpp`, nine capacity-repeat stdout files | V/R; generated source transform and input hashes checked. |
| U | `.local-work/d5ab/append-native01/control.json` | V/R; six reserve-helper cases; substitutions explicit. |
| W | `.local-work/d5ab/worker-health02/receipt.json` | V/R; nine own-thread cases. |
| D | `.local-work/d5s/export42/native.tsv` lines 941–1067; `.local-work/d5s/export24/native.tsv` lines 4554–4887 | V; preparation-node destructor/worker and reader-owning layer invocation; pins in `d5s-sources.csv`. |

Additional C1 candidates directly inspected: `.local-work/d5ab/initial.json`,
`handoff-freeze01.json`, `lifetime-followup-entries.json`,
`handoff-independent-review01.md`, `handoff-final-editorial-screen.json`,
`fixture-error-screenshot.json` (metadata only), `unwind-probe01.json`;
`.local-work/review-deliveries/d5ab-bounded-handoff-01.json` and both named patches;
`.local-work/d5p/d5ab-offline-preflight01/protection.json`;
`.local-work/d5v/functions/140982d90.txt`, `140982b70.txt`, `1409829b0.txt`;
`.local-work/d5z-visited/export01/native.tsv`; E1–E4 command/log/preservation records
where present; B representative `terminal.json`/`fixture.json` and raw frames.
Preservation receipts authenticate past export bytes; C2 did not reopen the database.
Source/hash checks cover every `d5ab-sources.csv` row; historical index mismatches
are version distinctions, not silent replacements. The detached-retirement receipt is `.local-work/d5s/native-retirement04.json`,
SHA-256 `184f26a2de58235c37e482a19c49b6b6e6ce82dfca57420f81102a75ec338695`;
its driver is `.local-work/d5s/native_retirement.py`, hash
`5604c6e1227cbb2f5215f44ce6b890386c5d33967c3423f8f93320f68613f9cb`.
Its shift-38 callback replaces terminal source retirement/free. The static E1 free
is a separate proof edge. B1 metrics are directly retained in
`.local-work/d5x/live/session-ceb439b14ddc4db8b734526a124f1e879b64cd457774a87a6a67852fd4489894/terminal.json`;
`d5y/writer-progress.csv` and `d5aa/capacity-sensitivity.csv` are the existing
phase/loss and admitted-input-only replay derivatives. Their sampled/model limits
are preserved. C2 frame checks on seven existing B sessions are in
`.local-work/d5ab-c2/frame-inspection.json`; no reducer code was imported.
Original refusal messages and
preliminary reviewer transcript have no supplied primary path. Their absence
limits historical operation adjudication, not this edge audit.

## G1/G2 — provenance claims

| ID / C1 | Material claim | Exact primary locator; access | Finding / classification | Limit | Next discriminating action / D5AB mapping |
|---|---|---|---|---|---|
| G01 / G1 | D5AB checkpoint and current baseline are distinguishable. | Git `623b49c`, `1830061`; initial and Freeze01 receipts; V | PROVEN: historical precommit state and committed source are separately pinned. | No exhaustive operation transcript. | Retain operation claims as reported where no primary log exists; AC01/02. |
| G02 / G2 | S002 identifies current final observer. | S002; Build05 source copy and Build05 `build.json/inputs`; B `inputs`; V | DISPROVEN: exact S002 hash matches Build05; frozen final hash matches Build08/current. | Why index stayed intermediate is unknown. | Use exact-version manifest in later qualification; AC10/12. |
| G03 / G2/R3 | B and F test one identical combined package. | B `inputs`, packaged RR; F `reader_sha256/reducer_sha256/build_sha256`; V/R | DISPROVEN: F uses later RR on B captures. | Native code itself matches final freeze. | Manifest compiled versus interpreted versions; package/regression qualification after approval; AC07/08/09. |
| G04 / G1/G2 | Export03 is complete/preserved. | E3 EOF; missing `lifetime-export03/preservation.json`; E4 preservation; V | DISPROVEN: only two complete helpers; no preservation receipt. | E4 independently supplies more records. | Keep E3 partial; request only an indispensable missing record if needed; AC01/03/10. |
| G05 / G2 | Historical bounded review accepted engineering. | `handoff-independent-review01.md`, original review scope; V | DISPROVEN: source inspection excluded. | Earlier objections available only as summaries. | Exact source/control review under later full readiness scope; AC11/12. |

## L1/L2 — native edges, witnesses and competing routes

| ID / C1 | Material edge or claim | Exact primary locator; access | Finding / classification | Observer witness/fence and coverage limit | Next discriminating action / D5AB mapping |
|---|---|---|---|---|---|
| L01 / L1 | Constructor dedup and allocation. | E2 lines 301–739; static VAs `0x140982dc1`, `0x140982e21`–`0x140982e39`, `0x140983001`; V | PROVEN: locked route can return existing anchor allocation or allocate 0x1a0 bytes. | Birth bridge only on new initialized allocation; no birth on dedup. | Trace each constructor caller's publication/ownership contract; Q1/AC03/05. |
| L02 / L1 | Content identity and token initialization. | E2 `0x140982f59`–`0x140982ff9`, `0x14098301b`–`0x1409830c9`; O 118–123; A `birth_bridge`; V | PROVEN: semantic identity fields and token initialized before birth copy; selected raw padding remains UNRESOLVED. | Dimensions are later written at `0x140983130/0x14098313c` and excluded by RR. RR includes raw padding `+0x39..+0x3b`, whose initialization/stability is unproved. Token is not an injective key or lease. | Test same token/different allocation and source definition, retain collision refusal; Q1/AC03/08. |
| L03 / L1 | Birth implies publication. | E2 `0x14098316c`–`0x14098317e`, return `0x1409831c5`; A `published_bridge`; V | DISPROVEN: reserve sentinel skips publication while R14 may remain nonnull. | Publication callback follows actual array store; no source key captured there. | Explicit unpublished/dedup controls and exception cleanup association; Q1/AC03/05. |
| L04 / L2 | String-operation failure has fully mapped cleanup. | E2 `0x1409830d9`; E4 pseudo records `0x143784550`–`0x14378457e`; `unwind-probe01.json` constructor flags 2; V | UNRESOLVED: retained metadata/partial cleanup does not establish every exceptional deallocation edge or whether source memory is freed. | No separately proven complete cleanup fence. | First reconcile retained unwind/pseudo fragments; if insufficient, acquire only constructor handler/cleanup target and its source alias under new native authority; Q1/AC03/07. |
| L05 / L1 | Source array publication and later cell population. | E2 constructor store; E1 `0x140849bf2`, `0x1407855dc`, `0x140786382`; E1 lines 1209–2255; retained `.local-work/d5w/functions/1409832e0.txt` (population body); V | PROVEN for three constructor callers and retained population/cursor routes; complete alias census UNRESOLVED. | Birth Grid holder differs from ProcGen owner; no equivalence inferred. | Account for each returned pointer's cell insertion and removal, including unpublished return; Q1/AC03/05. |
| L06 / L1 | Later identity writes covered. | E1 `0x1407855e9` writes `+0x178`; constructor prefix writes above; O/RR definition selection; V | UNRESOLVED for complete writer census. Known later `+0x178` write is outside the copy; known `+0x18/+0x1c` writes are inside the copy but outside RR identity definition. | No proof all aliases of selected identity bytes are immutable; dimensions are not claimed immutable; selected padding `+0x39..+0x3b` needs initialization/stability or explicit semantic exclusion. Size scan is not writer scan. | Prove immutability of selected identity bytes from retained aliases or acquire the specific absent writer/alias record; Q1/AC03. |
| L07 / L2 | Bulk source destruction route. | E1 lines 2394–2599, `0x140982a36`, unlock sequence, `0x140982af8`; N site 10; V | PROVEN: map erase, unlock, resource release, source free. | Fence 3 at bulk clear covers this route including Grid destructors calling it. | Challenge lost begin/end, exception, reuse and overlapping publication; Q1/AC03/05/07. |
| L08 / L2 | Standalone retirement route. | E1 lines 3681 onward, `0x140982bbc`, `0x140982bc9`, `0x140982c32`; N site 11; V | PROVEN: map erase/unlock precede source free. | Fence 4 covers whole hooked function, not only map lock. | Distinguish this positive coverage from alternate-free completeness; Q1/AC03/05. |
| L09 / L2 | Grid destructor alternatives. | E1 lines 2256–2393; `0x1409828ff`, `0x14098719f` call `0x140982930`, then `0x140982947` bulk clear; V | PROVEN: two wrappers reach fenced clear before freeing Grid storage. | Grid object is not each source allocation. | Validate indirect/vtable caller coverage and abnormal paths; Q1/AC03/05. |
| L10 / L2 | Movement retires retained Grid's source. | E4 lines 92–614, `0x14098706d`; E1 lines 2695–2905, `0x140988175`, predicate `0x1409870b7`; D5S model lines 94–118; retirement04 `ordinary_shift_series`; V/R | PROVEN STATIC route; Grid-retention-only source protection DISPROVEN. | Retirement fence can invalidate observer join; static schedule is not retail execution. | Integrated detached-source retirement/reuse oracle; Q1/AC03/07. |
| L11 / L2 | Layer reader protects detached density. | D: `0x1407b5235`/`0x1407b526a`; preparation destructor `0x1407b1a19`; D5S retained detached-route records identified in source ledger; V | DISPROVEN: reader ownership belongs to specific paths; destroyed prep reader cannot protect detached continuation. | Generation triple excludes stale generation, not concurrent source retirement. | Do not borrow ownership; establish actual reader/owner for each provider route; Q1/AC03. |
| L12 / L2 | Selected/visited source copy is safe because no source is read there. | O 104–115; A `selected_bridge`/`visited_bridge`; P `0x14079fc37` token read and `0x14079fca3`; V | PROVEN narrow no-dereference behavior of callbacks; end-to-end lifetime UNRESOLVED. | RDI already consumed by engine; native read can itself race. | Qualify birth-to-consumption continuity and known fences; Q1/AC03. |
| L13 / L2 | ProcGen lock alone owns source during lookup copy. | P `0x14079fcb3`, `0x14079fccb`; E1 retirement unlock/free; O 145–157; V | UNRESOLVED: lock serializes map, not proven raw-source lease. | ReadProcessMemory returns bytes/failure; stable epoch checks only observed hazards. | Establish owner/reader that prevents source free across lookup copy, or relocate copy under proven ownership; Q1/AC03/05. |
| L14 / L2 | Map erase, reset and ProcGen destruction are covered. | E1 lines 3368–3680; N sites 7–9/12; O `fence_hook/cold_hook`; V | PROVEN for named entries and protected empty-state site. | Global invalidation is conservative; broad reset does not itself free geographic source. Owner replacement/missed paths remain UNRESOLVED. | Map replacement/context installation to owner epochs; test mismatched owner with equal pointer/token; Q1/AC03/05/08. |
| L15 / L1/L2 | Pointer/token/allocation/key equivalence and ABA are established. | RR `identity/definition/before`; F rebirth/collision/lifetime controls; V/R | DISPROVEN as general equivalence; conditional joins exist. | Observer allocation ID is event token; no native lease. Unseen free/rebirth defeats evidence completeness. | Independent actual reuse, equal-token distinct-owner and missed-invalidation controls after native coverage; Q1/AC03/07/08. |
| L16 / L1 | Old-before-arming and unpublished sources qualify. | RR `identity`, `pubs`; F `unknown-birth`, `constructor-not-published`; V/R | DISPROVEN: omitted birth or publication refuses identity. | Conservative rejection can miss valid native sources; it does not satisfy positive bypass criterion alone. | Retain refusal; obtain a qualified new lifecycle in a separately authorized episode; Q1/AC03/09. |
| L17 / L1/L2 | Every size-census candidate is a source writer/free. | E1 lines 2–769; E2 lines 740–5814; E4 constructors; V | DISPROVEN: numerous different constructor families. Complete alternate-source-path coverage UNRESOLVED. | Followup entries enumerate inspected candidates, not a whole-program proof. | Use family census below; do not add hooks for unrelated same-size objects; Q1/AC03/05. |

### Allocation-size candidate census

E1's `%1a0` scan is a heuristic, not exhaustive alias analysis. E2's followup list
is fully present as function records (including constructor/destructor duplicates).
The local `function-census.json` retains exact per-function line intervals.

| Retained family | Primary discrimination | Disposition and consequence |
|---|---|---|
| `0x140982d90`, `0x1409829b0`, `0x140982b70` | E2 first 739 lines, geographic prefix and known Grid ownership. | Relevant allocation and two known free routes; no alternate-route completeness claim. |
| `0x1404196c0`, `0x140d89b50`, `0x140d89cb0`, `0x140d8a380` | E1 size-scan contexts call `0x140d89a80` or different allocators. | Not demonstrated source aliases. Context-only evidence cannot fully classify their object type; no source edge inferred. If alias evidence connects them, acquire the specific constructor/consumer before adding coverage. |
| `0x141047e60/0x141048110`, `0x141086510/0x1410865c0/0x141086830`, `0x1410b7350/0x1410b7570`, `0x141c2c660/0x141c2cbb0/0x141c2d720/0x141c2ea10/0x141c2ec50/0x141c2edf0/0x141c2eff0` | E2 lines 740–2737; allocations call `0x141c30400`, frees call `0x141c30520`. E4 lines 1171–end show constructor writing owner `+0x160`, counter `+0x158`, linked collection `+0x170`. | Different demonstrated layout/constructor family; not evidence of geographic-source free. Indirect aliases outside retained corpus remain unknown. |
| `0x1413499b0` | E2 lines 1514–1575; VehicleInfo/UIDataShuttle vtables. | Different named family within export. |
| `0x141c8e340/0x141c8f120/0x141c91ea0` | E2 lines 2738–3338; E4 lines 763–878 constructor `0x141c8eb10`, CombatPath/CombatCoveredPath vtables. | Different pathfinding family. |
| `0x142588a00/0x14258e650` | E2 lines 3339–3460; destructor helpers and Particles::Intrinsics::Input vtable. | Different/partially typed families; no geographic-source alias established. |
| `0x142904e10/0x142904fc0/0x142905a90` | E2 lines 3461–5439; construction calls `0x14241ebc0`; E4 lines 879–1040 zeroing layout. | Separate demonstrated construction path; no geographic-source constructor/token initialization. |
| `0x142c497e0/0x142c6dd00` | E2 lines 5440–5560; E4 lines 1041–1170; ViewAllEntry/UI_listEntry family. | Separate UI construction/destruction; no source alias established. |
| `0x142d5daa0` | E2 lines 5561–5594; E4 lines 615–762 destructor `0x142d5d760`. | Different multi-subobject teardown; no geographic-source alias established. |
| `0x1437bc3c0`, `0x1437bd170`, `0x143810a30`, `0x143810a50`, `0x143810a90`, `0x143810af0`, `0x143812b90`, `0x143812da0`, `0x14385f220`, `0x14385f250` | E2 lines 5595–5814; cleanup funclets free stack-owned slots with size 0x1a0. | Pointer origin/type is not established by these short funclets. Retain as unresolved alias/exception candidates; a reference to the same size is insufficient to classify either safe coverage or an actual missed source free. |
| E3 helpers and E4 pseudo cleanup | `0x1402b6280` releases a lock; `0x1402c5b40` installs allocator-functor vtable; pseudo `0x143784550` onward. | Helpers do not prove all exceptional source cleanup; L04 remains open. |

### Raw aliases and cell publication

| ID / C1 | Exact primary edge; access | Finding / classification | Missing obligation / next action / original mapping |
|---|---|---|---|
| L18 / L1/L2 | E1 lines 3159-3367: `0x140988240/330/760` read cell slots `+0x18/+0x20/+0x28/+0x30`; `0x140988ab0` copies `*param_2` into cursor chunk. V. | PROVEN raw pointer propagation into cursor, not a birth, refcount increment or source lease. | Establish writer/removal ownership for each cell variant and cursor lifetime; do not infer source retention from copied pointer. Q1/AC03/05. |
| L19 / L2 | E1 lines 2906-3158: `0x140988090` invokes each pointee's virtual destructor and frees pointer-array backing. V. | PROVEN virtual destruction/backing cleanup; concrete pointee-vtable ownership UNRESOLVED in this record. | Bind actual collection element vtable/owner before classifying source versus cell destruction. Existing bulk-clear fence covers its observed Grid-destructor call chain, not every potential indirect caller. Q1/AC03/05. |
| L20 / L1 | E1 caller `0x140849d49` invokes `0x1409832e0`; its body is already retained in `.local-work/d5w/functions/1409832e0.txt`, full function record, and `.local-work/d5v/export04/native.tsv` from line 1865. V. | PROVEN population route: walks Grid source array; allocates/replaces fill cells, calls virtual insertion with source pointer, and dispatches edge/corner helpers. | Body was located during review, so no new export of it is needed. Virtual insertions and replacement destructors need ownership classification; retain raw-alias limits. Q1/AC03/05. |
| L21 / L1/L2 | `.local-work/d5w/functions/140985870.txt`, full function `0x140985870`; P call `0x14079f92c`. V. | PROVEN cell lookup by origin-adjusted coordinates from Grid `+0x20`; no source lease obtained in that function. | Connect cell vtable enumeration L18 to source lifetime; Grid retention alone still fails D5S. Q1/AC03/05. |

The population body is available and was examined. Its direct fill path initializes
GridFillCell and calls virtual `+8` with the raw source. Existing edge/corner bodies
`140985900.txt` and `140985c50.txt` allocate/replace Grid edge/corner cells and
forward the source to virtual insertion; replacement destructor targets require
actual vtable binding. Direct retained insertion bodies `140988220.txt`, `1409884e0.txt` and
`140988670.txt` show fill/edge/corner source pointer stores into initially empty
slots and same-pointer comparisons, without source refcount increments. This
positively explains how L18 obtains aliases; it supplies no lease. The alternate
auxiliary call `0x1409865e0` has no function record in the targeted d5v/d5w/d5s
native.tsv/text search; only its callsites were found. Its body/ownership is a
specific residual acquisition candidate, after checking any additionally supplied
retained export. No absent file is
mistaken for absent native behavior. L20's available body does not settle complete
publication/writer coverage.

### Every retained size-scan literal

All 59 E1 `CANDIDATE` records are accounted for below. E1 line spans include the
candidate and its retained context only. Family evidence above supplements these
slices; a context-only UNRESOLVED row does not assert a source alias or a missed
free. Every row maps to Q1/AC03/05 via L17; actions remain P1 proposals.

| Candidate function | E1 lines | Direct context / disposition | Exact next discriminator |
|---|---|---|---|
| `0x1404196c0` | 2-14 | Different constructor/helper context above; source relation UNRESOLVED. | Bind `0x140d89a80` or helper object owner before excluding alias. |
| `0x1409829b0` | 15-27 | Bulk geographic-source free; L07. | Retain mapped fence/witness and challenge aliases/exceptional paths. |
| `0x140982b70` | 28-40 | Standalone geographic-source free; L08. | Retain mapped fence/witness and challenge aliases/exceptional paths. |
| `0x140982d90` | 41-53 | Geographic-source allocation; L01-L03. | Retain mapped fence/witness and challenge aliases/exceptional paths. |
| `0x140d89b50` | 54-66 | Different constructor/helper context above; source relation UNRESOLVED. | Bind `0x140d89a80` or helper object owner before excluding alias. |
| `0x140d89cb0` | 67-79 | Different constructor/helper context above; source relation UNRESOLVED. | Bind `0x140d89a80` or helper object owner before excluding alias. |
| `0x140d8a380` | 80-92 | Different constructor/helper context above; source relation UNRESOLVED. | Bind `0x140d89a80` or helper object owner before excluding alias. |
| `0x141047e60` | 93-105 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x141048110` | 106-118 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x141086510` | 119-131 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x1410865c0` | 132-144 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x141086830` | 145-157 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x1410b7350` | 158-170 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x1410b7570` | 171-183 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x1413499b0` | 184-196 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x14138df40` | 197-209 | Call `0x1402b56d0` with size; pointer origin UNRESOLVED. | Parent object constructor/returned pointer ownership at this function. |
| `0x141392400` | 210-222 | Virtual `+0x50` call then constructor `0x14138d830`; source relation UNRESOLVED. | Identify virtual allocator receiver and constructed type. |
| `0x141c2c660` | 223-235 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x141c2c840` | 236-248 | Allocation then `0x141c30400`; demonstrated separate constructor family. | Use E4 constructor layout; no source hook justified by size. |
| `0x141c2cbb0` | 249-261 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x141c2d720` | 262-274 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x141c2ea10` | 275-287 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x141c2ec50` | 288-300 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x141c2edf0` | 301-313 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x141c2eff0` | 314-326 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x141c8e340` | 327-339 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x141c8f120` | 340-352 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x141c91ea0` | 353-365 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x141ebabb0` | 366-378 | Call `0x1402b56d0` with RBX; pointer origin UNRESOLVED. | Bind RBX object constructor and destruction owner. |
| `0x141ebbfd0` | 379-391 | Virtual `+0x50` call then `0x141ebaa30`; type UNRESOLVED. | Bind receiver and constructor output aliases. |
| `0x142588a00` | 392-404 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x14258e650` | 405-417 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x142885d90` | 418-430 | `0x1422cb570` allocation, linked interior pointer `+0x18` to `+0x20`; different visible initialization but full type UNRESOLVED. | Identify consumer/owner; do not infer geographic-source exclusion from partial layout. |
| `0x142903560` | 431-443 | Allocation copies object from owner `+0x378`; consistent separate copy family, source alias UNRESOLVED. | Bind original object type/copy consumer; size alone insufficient. |
| `0x142904e10` | 444-456 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x142904fc0` | 457-469 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x142905a90` | 470-482 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x142be2180` | 483-495 | Allocate aligned 4 then zero 0x1a0 bytes; type UNRESOLVED. | Identify initialization/consumer after zeroing. |
| `0x142c092a0` | 496-508 | `0x1402b56d0` size call; source relation UNRESOLVED. | Bind object pointer and constructor `0x142c09240` family if applicable. |
| `0x142c09340` | 509-521 | Allocate then `0x142c09240`; source relation UNRESOLVED. | Read constructor/owner and returned-pointer consumers. |
| `0x142c09450` | 522-534 | Allocate then `0x142c09240`; source relation UNRESOLVED. | Read constructor/owner and returned-pointer consumers. |
| `0x142c09730` | 535-547 | Allocate, `0x142bff8a0`, vtable `0x144ef9228`; source relation UNRESOLVED. | Bind vtable methods/type and owner aliases. |
| `0x142c09870` | 548-560 | Allocate, `0x142bff8a0`, vtable `0x144ef9228`; source relation UNRESOLVED. | Bind vtable methods/type and owner aliases. |
| `0x142c497e0` | 561-573 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x142c6dd00` | 574-586 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x142d5daa0` | 587-599 | Inspected E2/E4 family above; no geographic-source alias established. | Use family constructor/free evidence; retain indirect-alias coverage limit. |
| `0x142e30030` | 600-612 | Virtual `+8` call with size, then more virtual consumers; type UNRESOLVED. | Identify allocator receiver and output ownership. |
| `0x142f475f0` | 613-625 | `0x142e90140` called with size; pointer/count stored at owner `+0x20/+0x28`; type UNRESOLVED. | Bind helper return and owner field consumers. |
| `0x14366efd0` | 626-638 | Immediate 0x1a0 followed by scalar copies; no allocator call in retained slice. UNRESOLVED context only. | Inspect surrounding existing function context to establish literal role before treating as allocation/free. |
| `0x1437bc3c0` | 639-651 | 0x1a0 free from parent stack slot; source type UNRESOLVED. | Map funclet stack slot to parent allocation/unwind scope. |
| `0x1437bd170` | 652-664 | 0x1a0 free from parent stack slot; source type UNRESOLVED. | Map funclet stack slot to parent allocation/unwind scope. |
| `0x143810a30` | 665-677 | 0x1a0 free from parent stack slot; source type UNRESOLVED. | Map funclet stack slot to parent allocation/unwind scope. |
| `0x143810a50` | 678-690 | 0x1a0 free from parent stack slot; source type UNRESOLVED. | Map funclet stack slot to parent allocation/unwind scope. |
| `0x143810a90` | 691-703 | 0x1a0 free from parent stack slot; source type UNRESOLVED. | Map funclet stack slot to parent allocation/unwind scope. |
| `0x143810af0` | 704-716 | 0x1a0 free from parent stack slot; source type UNRESOLVED. | Map funclet stack slot to parent allocation/unwind scope. |
| `0x143812b90` | 717-729 | 0x1a0 free from parent stack slot; source type UNRESOLVED. | Map funclet stack slot to parent allocation/unwind scope. |
| `0x143812da0` | 730-742 | 0x1a0 free from parent stack slot; source type UNRESOLVED. | Map funclet stack slot to parent allocation/unwind scope. |
| `0x14385f220` | 743-755 | 0x1a0 free from parent stack slot; source type UNRESOLVED. | Map funclet stack slot to parent allocation/unwind scope. |
| `0x14385f250` | 756-768 | 0x1a0 free from parent stack slot; source type UNRESOLVED. | Map funclet stack slot to parent allocation/unwind scope. |

## S1/T1/R1 — store, transport and interpretation

| ID / C1 | Material claim | Exact primary locator; access | Finding / classification | Limitation | Next discriminating action / D5AB mapping |
|---|---|---|---|---|---|
| S01 / S1 | Reserve attempt implies insertion. | P `0x14079ff3e`–`0x14079ff60`; U six `cases`; O `reserve_hook`; V/R | DISPROVEN: sentinel bypasses write; count/index helper tests do not write token storage. | Substituted allocation callbacks. | Preserve reserve-fail/exception/skip distinctions; Q2/AC04. |
| S02 / S1 | Stored event follows executed write. | A `stored_bridge`; O `stored_capture`; N site 17; V | PROVEN STATIC: displaced write executes before callback; failure branch does not enter it. | ABI/async unwind and source lifetime not completely qualified; event loss still possible. | Independent bridge fault-before/after-write, reserve throw and reset/retire interleavings; Q2/AC04/07. |
| S03 / S1 | Reserve/store same source, epoch and destination. | RR append checks; F wrong address/token/frame/thread/count/epoch controls; V/R | PROVEN conditional model refusals; full native claim UNRESOLVED. | Fixture reserve sets a 256-slot synthetic array; no retail allocator/OOM oracle. | Integrated actual-source/epoch adverse schedules after L coverage; Q2/AC04/07/08. |
| T01 / T1 | Tested capacity is justified by actual queue measurements. | K `results`, generated lines for four producers/8,000 each; stress source; V/R | PROVEN for retained bounded held bursts and exact ID/count oracles. | Concurrent overload loses at all capacities; high-water is lower bound. | Extend qualified workload rationale using measured concurrency/flush distributions; Q3/AC06. |
| T02 / T1 | Representative source/writer workload is retail-complete. | B representative raw frames, terminal/fixture; fixture.cpp `representative`; V/R | DISPROVEN as a guarantee: modeled four-producer workload, 500 calls each, plus fences. | Seventeen kinds do not establish every native path or demand tail. | Source-aware workload envelope and repeated native integration controls under new authority; Q3/AC05/06/07. |
| T03 / T1 | Queue publication and loss accounting cover bounded cases. | O `emit/pop/lose`; queue_stress.cpp independent offered IDs/set/count; K stdout; V/R | PROVEN scoped invariant checks: reserved head refuses consumption, wrap, exact admissions plus losses, retry and recursion controls. | Forced retry substitutes exhaustion; loss-bound uncertainty is explicit; no universal concurrency proof. | Independent delayed publication/STOP/fault schedules and counter-edge review; Q3/AC06/07. |
| T04 / T1 | Writer preserves failure metrics and flush ordering. | T `drain/metrics/worker_body`; RC `inspect`; B I/O and ACK cases; V/R | PROVEN source ordering/raw-before-ACK and bounded fault outcomes. | Cumulative sampled telemetry is not event-time loss reconstruction; best-effort exception closeout can fail. | Cross-check actual worker death, ACK-only loss and terminal-write failure with controller; Q3/AC06/07. |
| T05 / T1 | Worker liveness and controller integration are qualified. | H `qualify/watch/verify_ack`; W cases; T worker creation fields; V/R | DISPROVEN as integrated claim: own-thread tests never exercise watch; watch never verifies fresh ACK or owns STOP. | STOP-file existence alone is weak exit classification; no controller failure oracle. | Ordinary protocol state-machine tests plus separately authorized real-recorder fixture; Q3/Q5/AC07/09. |
| T06 / T1 | Original safeguards survive automatically. | plugin.cpp Load; T `disk/guards/worker_body`; transport.h; proposed B2 card; V | UNRESOLVED as full operational claim. Source retains both-drive floor, guards, sole-thread admission and resident inert shutdown. | Protection01 is historical, not current preflight; no accepted controller/card bundle. | Explicit safeguard parity and authenticated control integration; Q5/AC09/10. |
| R01 / R1 | Every retained control is bound to its actual consumer. | B/F/Q, full case index below; V/R | PROVEN byte/version correspondence and reported outcomes; no C2 test rerun. | Native fixture semantics are not retail semantics. | Final manifest and independent oracle review; Q4/AC07/08. |
| R02 / R1 | Damaged/truncated/loss evidence can still imply firstness. | RC `inspect`, RR loss/fence checks; F eight damaged controls, semantic losses; V/R | DISPROVEN in tested examples: refusals or qualified earlier prefix only. | Broad absence/completeness depends on native event coverage. | Integrated ACK/terminal/raw faults, omitted lifecycle and reordered cross-thread schedules; Q4/AC07/08. |
| R03 / R1 | Old-before-arming selection can be recovered by pointer/key. | RR birth/publication requirement; F unknown-birth/prior-unknown; V/R | DISPROVEN under implemented qualification. | Geographic compatibility is weaker evidence. | Preserve conservative refusal and test equal pointer under new owner/epoch; Q4/AC03/08. |
| R04 / R1 | Mask zero or append proves empty/partial geometry. | fixture.cpp native_generate/native_sample; Q mask cases; V/R | DISPROVEN inference: fixtures supply sample result, not real generated geometry. | Prerequisite skip is modeled, not all real generator exits. | Geometry/prerequisite-specific independent fixture/native-path oracle; Q2/Q4/AC04/07/08. |
| R05 / R1 | B1 interpretation recovers missing target arrivals/append. | F `compatibility`; schema dispatch RC; retained B1 event hash in Q; V/R | DISPROVEN: 19,780 durable records, zero qualified chains, schema 2 unchanged. | 9,957 missing admissions and missing fields remain unavailable. | Only additional contemporaneous evidence could revise historical result; future B2 is a new episode; Q4/Q5/AC08/09. |

## Exact residual evidence obligations

These unresolved edges are audit findings, not permission to acquire new records.
The strongest retained routes and the exact absent discriminator are named here
so that P1 is not a generic request for more native analysis.

| Edge rows | Checked existing route / absent discriminator | Smallest acquisition or test and why alternatives do not close it |
|---|---|---|
| L04 | E2 constructor flags 2 and E4 pseudo cleanup `0x143784550/560/570`; last fragment ends after loading stack `+0x210`. | Full retained handler/cleanup control flow and unwind-to-parent map for `0x140982d90`, including pointer origin and free target after that fragment. Lock-release helpers alone do not show source cleanup. If no such retained record exists, separately approve only this export from existing analysis state. |
| L05/L06 | Three constructor callers and selected prefix initialization; post-birth writes `+0x18/+0x1c` and caller write `+0x178` are known. | Establish all aliases/writers of RR-selected bytes (including raw padding `+0x39..+0x3b`) `[0,4)`, `[0x38,0x64)`, `[0x68,0x70)`, plus returned-pointer cell publication/retirement. No selected-byte alternate writer is established in this corpus; the missing evidence is alias/writer coverage, not a proven hidden write. A token match or size search cannot supply it. |
| L13 | ProcGen lock acquisition plus later unlock-before-free; detached route lacks source lease. | Show the actual native owner/reader or lifetime protection spanning selected source through lookup copy on each qualifying route. If none spans it, identify a specific already-consumed protected operand site with independently proved association. Callback read success or epoch equality alone cannot distinguish freed/reused memory. |
| L14/L15 | Named reset/destruction/erase/bulk/retire fences and reducer observed-span refusal. | Bind owner/context replacement and pointer reuse to the same continuity domain; independent controls must replace owner with equal pointer/token and omit/loss an invalidation. Global known-entry fences suffice only if path coverage is demonstrated. |
| L17 | Ten short 0x1a0 free funclets and four context-only candidates enumerated above. | Map each funclet's stack pointer to parent allocation/unwind scope using retained metadata, then either prove unrelated or map to an existing fence. Unavailable parent/pointer-origin records need a named existing-state export; no new hook is justified by size alone. |
| S02/S03 | Native store/sentinel plus modeled reserve and current mismatch refusals. | Execute separately approved fault/throw/reset/retire schedules around actual reserve return/write with source ownership qualified. A later bypass cannot prove a successful write. |
| T05/T06 | WorkerLease and standalone thread tests; native worker closeout and proposed card. | Pure controller tests can establish control ownership independently; real recorder-worker death, controller death, stale ACK/STOP and active-producer shutdown still need a separately approved native integration fixture. |
| R02/R04 | Explicit mutation oracles and fixture sample constants. | Separate actual geometry/prerequisite/output oracle, competing native lock-wait outcome and cross-thread ordering/loss schedules; event renumbering and mask zero cannot stand in for these. |

## Full retained control index

The following tables bind every existing case to the code it actually exercised.
`B/F` means native-shaped Build08 fixture source plus current RC/RR interpretation
in Final02, not a rebuilt native suite. `F-model` means Q's mutated event dictionaries
using current RR. `F-damage` means copied synthetic sessions read by current RC/RR.
All results are historical receipt outcomes, directly read, not reproduced in C2.
Original mappings are Q1/AC03 for identity cases, Q2/AC04 for append cases,
Q3/AC06/07 for transport cases and Q4/AC08 for all chronology cases; no case alone
passes its mapped full criterion. The indexed case name is the exact JSON-array
locator in B/F and the fixture/Q branch name. New integrated controls remain in
the decision regardless of a historical matching expected count.

| Native case | Source / interpretation | Expected exit / actual | F chains / complete session |
|---|---|---|---|
| `normal` | B/F | 0 / 0 | 1 / True |
| `mask-zero` | B/F | 0 / 0 | 1 / True |
| `conflicting-mask` | B/F | 0 / 0 | 0 / True |
| `unexpected-mask` | B/F | 0 / 0 | 0 / True |
| `descriptor-change` | B/F | 0 / 0 | 1 / True |
| `temporary-descriptor` | B/F | 0 / 0 | 0 / True |
| `unrelated-conversion` | B/F | 0 / 0 | 0 / True |
| `post-reset-old-provider` | B/F | 0 / 0 | 0 / True |
| `schedule-old-first` | B/F | 0 / 0 | 0 / True |
| `schedule-fresh-first` | B/F | 0 / 0 | 1 / True |
| `reset-closeout` | B/F | 0 / 0 | 0 / True |
| `edge` | B/F | 0 / 0 | 0 / True |
| `corner` | B/F | 0 / 0 | 0 / True |
| `null-cell` | B/F | 0 / 0 | 0 / True |
| `overlap-reset` | B/F | 0 / 0 | 0 / True |
| `orphan-sample` | B/F | 0 / 0 | 0 / True |
| `bad-read` | B/F | 0 / 0 | 0 / True |
| `bad-source` | B/F | 0 / 0 | 0 / True |
| `bad-descriptor` | B/F | 0 / 0 | 0 / True |
| `source-absent` | B/F | 0 / 0 | 0 / True |
| `selection-only` | B/F | 0 / 0 | 0 / True |
| `visited` | B/F | 0 / 0 | 0 / True |
| `map-hit` | B/F | 0 / 0 | 0 / True |
| `skip-sample` | B/F | 0 / 0 | 0 / True |
| `nested` | B/F | 0 / 0 | 1 / True |
| `interrupt` | B/F | 0 / 0 | 0 / True |
| `in-flight-loss` | B/F | 0 / 0 | 0 / True |
| `missing-lookup` | B/F | 0 / 0 | 0 / True |
| `missing-descriptor` | B/F | 0 / 0 | 0 / True |
| `missing-generator` | B/F | 0 / 0 | 0 / True |
| `missing-sample` | B/F | 0 / 0 | 0 / True |
| `prior-unknown` | B/F | 0 / 0 | 0 / True |
| `ready-only` | B/F | 0 / 0 | 0 / True |
| `descriptor-collision` | B/F | 0 / 0 | 0 / True |
| `reused-pointer` | B/F | 0 / 0 | 1 / True |
| `reset` | B/F | 0 / 0 | 2 / True |
| `clear` | B/F | 0 / 0 | 1 / True |
| `destroy` | B/F | 0 / 0 | 1 / True |
| `erase` | B/F | 0 / 0 | 1 / True |
| `concurrent` | B/F | 0 / 0 | 1 / True |
| `competing` | B/F | 0 / 0 | 1 / True |
| `loss-one` | B/F | 0 / 0 | 1 / True |
| `loss-many` | B/F | 0 / 0 | 1 / True |
| `saturation` | B/F | 0 / 0 | 1 / True |
| `timing` | B/F | 0 / 0 | 1 / True |
| `stop-under-production` | B/F | 0 / 0 | 1 / True |
| `representative` | B/F | 0 / 0 | 1 / True |
| `burst` | B/F | 0 / 0 | 1 / True |
| `reserve-fail` | B/F | 0 / 0 | 0 / True |
| `unknown-birth` | B/F | 0 / 0 | 0 / True |
| `later-bypass` | B/F | 0 / 0 | 1 / True |
| `write-fault` | B/F | 0 / 0 | 1 / False |
| `flush-fault` | B/F | 0 / 0 | 1 / False |
| `ack-fault` | B/F | 0 / 0 | 1 / False |
| `disk-fault` | B/F | 0 / 0 | 1 / False |
| `ack-write-fault` | B/F | 0 / 0 | 1 / False |
| `crash-before` | B/F | 71 / 71 | 0 / False |
| `crash-after` | B/F | 72 / 72 | 1 / False |
| `crash-sample` | B/F | 73 / 73 | 0 / False |
| `sequence-wrap` | B/F | 0 / 0 | 1 / True |
| `guard-mismatch` | B/F | 0 / 0 | N/A / N/A |

| Semantic case | Source | Expected / actual chains |
|---|---|---|
| `interleaved-unknown-selection` | F-model; Q mutation / explicit constant | 0 / 0 |
| `same-pointer-rebirth-after-entry` | F-model; Q mutation / explicit constant | 0 / 0 |
| `same-thread-equal-birth-publication-ticks` | F-model; Q mutation / explicit constant | 1 / 1 |
| `same-thread-publication-equals-entry-ticks` | F-model; Q mutation / explicit constant | 1 / 1 |
| `cross-thread-ambiguous-birth-order` | F-model; Q mutation / explicit constant | 0 / 0 |
| `unmatched-lifecycle-before-birth` | F-model; Q mutation / explicit constant | 0 / 0 |
| `unmatched-lifecycle-contradicts-zero-hazard` | F-model; Q mutation / explicit constant | 0 / 0 |
| `zero-allocation-identity` | F-model; Q mutation / explicit constant | 0 / 0 |
| `cold-loss-generation-mismatch` | F-model; Q mutation / explicit constant | 0 / 0 |
| `positive-no-later-bypass` | F-model; Q mutation / explicit constant | 1 / 1 |
| `direct-mask-zero` | F-model; Q mutation / explicit constant | 1 / 1 |
| `missing-kind-1` | F-model; Q mutation / explicit constant | 0 / 0 |
| `missing-kind-2` | F-model; Q mutation / explicit constant | 0 / 0 |
| `missing-kind-3` | F-model; Q mutation / explicit constant | 0 / 0 |
| `missing-kind-4` | F-model; Q mutation / explicit constant | 0 / 0 |
| `missing-kind-5` | F-model; Q mutation / explicit constant | 0 / 0 |
| `missing-kind-6` | F-model; Q mutation / explicit constant | 0 / 0 |
| `missing-kind-7` | F-model; Q mutation / explicit constant | 0 / 0 |
| `missing-kind-8` | F-model; Q mutation / explicit constant | 0 / 0 |
| `missing-kind-12` | F-model; Q mutation / explicit constant | 0 / 0 |
| `missing-kind-14` | F-model; Q mutation / explicit constant | 0 / 0 |
| `missing-kind-15` | F-model; Q mutation / explicit constant | 0 / 0 |
| `missing-kind-16` | F-model; Q mutation / explicit constant | 0 / 0 |
| `missing-kind-17` | F-model; Q mutation / explicit constant | 0 / 0 |
| `reserve-failure` | F-model; Q mutation / explicit constant | 0 / 0 |
| `count-corrupt` | F-model; Q mutation / explicit constant | 0 / 0 |
| `store-wrong-token` | F-model; Q mutation / explicit constant | 0 / 0 |
| `store-wrong-address` | F-model; Q mutation / explicit constant | 0 / 0 |
| `reset-before-append` | F-model; Q mutation / explicit constant | 0 / 0 |
| `overlapping-epoch` | F-model; Q mutation / explicit constant | 0 / 0 |
| `store-wrong-frame` | F-model; Q mutation / explicit constant | 0 / 0 |
| `store-wrong-thread` | F-model; Q mutation / explicit constant | 0 / 0 |
| `store-invalid-lifetime` | F-model; Q mutation / explicit constant | 0 / 0 |
| `lifetime-loss` | F-model; Q mutation / explicit constant | 0 / 0 |
| `post-sample-loss` | F-model; Q mutation / explicit constant | 0 / 0 |
| `unknown-birth-status` | F-model; Q mutation / explicit constant | 0 / 0 |
| `constructor-not-published` | F-model; Q mutation / explicit constant | 0 / 0 |
| `unvisited-map-hit` | F-model; Q mutation / explicit constant | 0 / 0 |
| `unexpected-mask` | F-model; Q mutation / explicit constant | 0 / 0 |
| `same-key-token-different-ancestry` | F-model; Q mutation / explicit constant | 0 / 0 |
| `complete-non-target-lifecycle` | F-model; Q mutation / explicit constant | 1 / 1 |
| `duplicate-sequence` | F-model; Q mutation / explicit constant | 0 / 0 |
| `missing-admission` | F-model; Q mutation / explicit constant | 0 / 0 |
| `out-of-order-arrival` | F-model; Q mutation / explicit constant | 1 / 1 |
| `loss-before-first-selection` | F-model; Q mutation / explicit constant | 0 / 0 |
| `loss-before-append` | F-model; Q mutation / explicit constant | 0 / 0 |
| `loss-after-append-keeps-earlier-proof` | F-model; Q mutation / explicit constant | 1 / 1 |
| `loss-before-new-empty-boundary` | F-model; Q mutation / explicit constant | 1 / 1 |
| `equal-token-different-source` | F-model; Q mutation / explicit constant | 0 / 0 |
| `different-token-same-geography` | F-model; Q mutation / explicit constant | 0 / 0 |
| `lifecycle-before-visited-1` | F-model; Q mutation / explicit constant | 0 / 0 |
| `lifecycle-before-visited-2` | F-model; Q mutation / explicit constant | 0 / 0 |
| `lifecycle-before-visited-3` | F-model; Q mutation / explicit constant | 0 / 0 |
| `lifecycle-before-visited-4` | F-model; Q mutation / explicit constant | 0 / 0 |

| Damage case | Source | Recorded outcome |
|---|---|---|
| `raw-truncated` | F-damage; Q copied-session mutation | Refused |
| `raw-corrupt` | F-damage; Q copied-session mutation | Refused |
| `ack-truncated` | F-damage; Q copied-session mutation | Refused |
| `ack-corrupt` | F-damage; Q copied-session mutation | Refused |
| `duplicate-frame` | F-damage; Q copied-session mutation | Refused |
| `schema-mismatch` | F-damage; Q copied-session mutation | Refused |
| `stale-identity` | F-damage; Q copied-session mutation | Refused |
| `crash-ack-only-loss` | F-damage; Q copied-session mutation | Refused |

Native success counts depend on the explicit fixture scenario and current interpreter;
for example `reused-pointer` qualifies only a fresh valid chain after modeled
invalidation, not reuse continuity. Expected crash exits 71/72/73 are intentional
controls, not process survival. Build03's earlier invalid-source read at `0x69`
is preserved separately; substituting the already-consumed operand fixes a fixture
premise without proving the game tolerates invalid pointers.

Queue K additionally checks sequential wrap, delayed reserved head, full capacity,
forced retry exhaustion, uncertain loss bounds, eight times 12,000 concurrent
offers, held four times 8,000 offers, recursion, STOP with reserved producer,
source-free visited callback and near-limit disablement. Its nine stdout results
bind capacity/repeat to the generated-source hash in K. U's six cases are
(count, capacity, callback success) = (0,4,false), (3,4,false), (0,0,false),
(0,0,true), (4,4,false), (4,4,true); returned values are 0, 3, `0xffffffff`, 0,
`0xffffffff`, 4. These exercise the original reserve excerpt with substituted
initialize/grow callbacks, not token stores.

W's nine named results are `live-original-worker`, `reject-pid`,
`reject-worker_creation_filetime`, `reject-worker_thread_id`, `reject-nonce`,
`reject-schema`, `reject-reused-tid-creation`, `detect-actual-exit` and
`reject-stale-ack-after-exit`. They exercise current H's WorkerLease/verify_ack
against an owned disposable Python thread. They do not execute watch or a native
recorder/controller. Protection01 verifies historical protected-save/rehearsal-copy
conditions only. Screen01 has an unresolved historical source JOINED_PROSE suspect;
Unwind records limited native metadata, not arbitrary asynchronous bridge unwind.

Direct retained-frame checks distinguish 2,001 reserve events from 1,025 store
events in the representative fixture: each of four local modeled arrays admits
at most 256 stores, plus the baseline store. Zero transport loss does not imply
every modeled reserve succeeded. The seven checked sessions have no CRC-bad
frames; this authenticates framing, not native semantics or retail completeness.
