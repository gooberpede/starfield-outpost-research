# D5Z active investigation ledger

2026-10-31, Australia/Sydney. Controlling authority is the unchanged
[D5Z brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5Z_visited_state_persistence_reset_capacity.md).
Its D5Z-CQ and Q1–Q5 are frozen without amendment: explain visited-state origin,
all relevant mutations/readers, persistence or reconstruction, reset causality,
capacity/failure mechanics and consequences for B1's inherited initial state.
Parent D5R remains OPEN. No new retail operation is authorized.

## Investigation plan and initial branches

Allowed actions: read/hash installed inputs and existing static-analysis state;
export with `-readOnly -noanalysis`; inspect authenticated prior B1 evidence;
write task-owned offline scripts and documentation. Save inspection, if justified,
uses existing controlled copies only. No save/game/configuration/database writes,
attachment, deployment, network disclosure or Git mutation. Outputs are authored
documents and local receipts. Risks are disk use, accidental input mutation and
overclaiming incomplete paths; stop affected work on identity mismatch, either
drive below 40,000,000,000 caller-available bytes, or unauthorized required action.
Keep original evidence unchanged; cleanup does not delete historical inputs.

| Entry | Question / alternative | Action and current disposition |
|---|---|---|
| Z01 | Q1/Q4: dynamic visited storage versus fixed capacity; exceptional writers | OPEN. Trace provider, append, constructor, clear, allocator and aliases in existing native state. Dedicated visited lane started before native investigation. |
| Z02 | Q2/Q3: direct serialization, indirect reconstruction, retained object and reset purposes | OPEN. Trace reset/module dispatch and load/serialization producers in both directions; compare context transition, teardown, pressure and capacity hypotheses. Dedicated reset lane started. |
| Z03 | Q5: reset execution versus qualified cold anchor; target bypass versus identified construction | OPEN. Reauthenticate B1 archive/checkpoints and D5Y conditional attribution; preserve all lost-coverage limits. |
| Z04 | Checklist: operation completeness versus historical occurrence | OPEN. Audit every supplied item, retain player grouping, narrow ticks to supported operations and leave unresolved action mapping unchecked. Source checklist remains unchanged on Desktop. |
| Z05 | Evidence and handoff integrity | OPEN. Capture initial dirty tree before edits, preserve D5Y work, verify pins/disk, create reproducible causal SVGs, checks and both patch coverages; obtain independent final scientific, engineering and editorial review. |

No branch is closed by this plan or by a contributor summary. Subsequent entries
record actual exports, contradictions, failed approaches and remaining edges.

## Evidence checkpoints

| Entry | Actual evidence / correction | Disposition and next action |
|---|---|---|
| Z06 | `.local-work/d5z/initial.json` rehashes installed EXE/ESM/PlanetData and all fifteen existing Ghidra DB/project files; C: 91,144,728,576 and D: 84,632,317,952 caller-available bytes. | Identity PASS. D5Y changes visible during first reading were committed externally before this baseline; HEAD is `87468b70737a01468c3a5c38c5979bb622c30fd0`. This task performs no Git write. The initial snapshot includes this task's newly created ledger and is not an unrelated pre-existing file. |
| Z07 | Fresh unchanged `d5y_forensics.py d5z-recheck01` authenticates 19,780 frames, 39 flush prefixes, all 47 archive members/originals, installed/SFSE/tool/DB pins and unchanged capture bytes. `.local-work/d5y/d5z-recheck01/analysis.json` records exact input hashes. | Q5 retained-evidence baseline resolved; no fresh retail activity. Root-only `d5z_b1.py` extends the reset analysis. |
| Z08 | `.local-work/d5z/b1-01/b1.json` finds two matched reset/empty-state/unlock closeouts: sequences 2/3/4, epoch 2; 115/116/117, epoch 113. First 110 records contain READY and lifecycle events, no admitted provider entry/selection. | Stronger than mere reset-site execution. Does not qualify a later target first miss; 119 conditional target bypasses remain after the first reported loss boundary. Exact historical append/load origin stays OPEN. |
| Z09 | Initial `d5z_b1.py` used an incorrect result-key name, `qualified_chains`, and failed before output creation. The unchanged reader actually returns `chains`; corrected script reports zero chains. | Failed preparation preserved in session record; no scientific result discarded. |
| Z10 | All 31 supplied checklist operations are retained in the five required groups. Broad loading, complete placement and unconditional append wording narrowed; every line separates native explanation from actual B1 evidence. | Checklist draft awaits evidence/independent review. Original Desktop bytes unchanged; no formerly open operation is silently ticked. |
| Z11 | Reset export01 verifies actual ProcGen vtable `0x144b3f3a8`, reset slot `+0x18`; later manager slot `+0x20` is a separate no-op for ProcGen. | Preliminary lane interpretation corrected before report promotion. Forward bootstrap/load, indirect serialization and allocator census continue. |
| Z12 | Visited fresh exports verify allocation minimum 4, dynamic doubling and 32-bit byte products; provider skips token store on append sentinel `0xffffffff`. | Q4 local growth resolved; lower allocator `0x1422c7ad0 → 0x1422c8200 → 0x14186dfc0` introduces a genuine recovery dependency. Follow it before excluding pressure-triggered reset. |
| Z13 | LoadGlobalData type 3 reaches `0x1407896d0`, which reads a saved context u64 and version-gated compatibility u32 and calls reset wrapper under the reload setting. Setting initializer names `bAvoidClearOnReload:Planet`; configured runtime value is not measured. | Positive persistence-to-reset edge. Saved comparison producer and complete type-3 payload followed; no keyword-search absence conclusion. |
| Z14 | `.local-work/d5z/save-03/save-prefix.json` rehashes protected controlled Save52 copy and decodes only grounded global-type-3 prefix/descriptor fields. Independent selected-block decompression matches payload span `0xff5..0x152d`; 88 descriptors, 892 later payload bytes remain. | Q2 save inspection justified by Z13. Temporary decoded mmap removed, source copy hash unchanged. Actual buffer-version provenance remains a required native check. |
| Z15 | Existing typed-world/overlay serialization evidence maps saved context comparison, generated-world descriptors, two overlay-ID lists and typed `PlanetWorldSpaceData` values. Prior shorthand “reset/reuse argument” does not establish ProcGen visited retention: the actual reset thunk ignores that flag. | Preserve earlier notes as historical; new result must state the narrower compatibility effect and fresh source verification. Continue exact tail/alias closure. |
| Z16 | Whole existing-instruction `+0x130` candidate census discovers undefined wrapper `0x14079a310 → 0x1407a5790`, outside the initial local ProcGen method range. | Counterexample to a local-function-range completeness argument. Trace nonlocal rendering/presentation methods and all receiver escapes; do not create Ghidra functions or alter DB state. |
| Z17 | Independent early reviewer reauthenticates every B1 frame/ACK, selected Save52 prefix/envelope, original checklist count and growth/reset instructions. Finds clipped figure labels and ambiguous shared routes. | Counts derive from receipts after correction; regenerate figures with separate reset route and scoped load label. Final snapshot review still pending. |
| Z18 | Planned bounded native control: execute only the pinned `0x1422cc0d0..0x1422cc150` reserve helper in a disposable CPython process, with synthetic true/false allocation callbacks and six fixed count/capacity cases. | Allowed by the brief's isolated-native clause. Reads pinned EXE and owned PE reader; writes only fresh local receipts. No game/DB/save/configuration access or engine allocator call. Risk is a fault in the disposable process; stop on fault, identity/disk mismatch or failed expectation. Flush each case to local JSONL, retain failed prefixes, free the local RX page on normal exit. Successful callbacks do not allocate storage, so this tests helper control flow only, not real OOM, valid full-array growth or retail recovery. |

## Closing dependency dispositions

| Entry | Final evidence / correction | Disposition |
|---|---|---|
| Z19 | `.local-work/d5z/append-01/control.json` and flushed `cases.jsonl` complete all six original-helper cases. Direct-capacity reservation, false init/grow and true synthetic callbacks match the instruction account. | RESOLVED within reserve-helper control scope. No engine allocation or huge-array/wrap execution; old array correctness and retail OOM are not inferred. |
| Z20 | Native header chain `0x141830550 → file+0x110 → global reader+0x28` maps serialized byte `0x14` to the compatibility version predicate. `.local-work/d5z/save-04/save-prefix.json` independently verifies structure version 27 and buffer version 153. | RESOLVED. Save52's modern twelve-byte type-3 prefix is grounded without borrowing the installed build string as save provenance. Earlier save receipts remain unchanged. |
| Z21 | Fourteen complete visited-lane exports, 173 indexed function windows and actual receiver/captured-functor/RTTI binding, plus the reset lane's four complete exports and module census, close ordinary visited writer/reader/clearer and serialization aliases. | RESOLVED at the pinned ordinary receiver scope. The initial local-range approach was insufficient and was expanded; arbitrary substituted/corrupt pointers and injected writers are outside this claim. |
| Z22 | Allocator recovery is followed through actual LoadedCellDB entry/cache release, `0x140596dd0` unload, typed Cell destruction, and the suspected worldspace-removal edge. `0x140bbe590/0x140bbe250` remove cell membership without component destruction/installation or module reset. | RESOLVED scoped negative for a dedicated visited size/pressure reset policy. Generic recovery can service independently eligible engine work, so OOM preceding a later lifecycle reset is not universally excluded. This was the highest-value omitted avenue and was pursued before closure. |
| Z23 | Reset/load dossier `.local-work/d5z-reset-findings.md`, visited closure `.local-work/d5z-visited/closure.md`, source indexes and PE checks bind all actual module slots, direct predicates, saved fields and the two chained-unwind false callback candidates. | RESOLVED native model. Earlier “reset/reuse” shorthand is qualified for ProcGen without altering historical evidence. The final dossier is supporting context; primary exports/bytes control semantics. |
| Z24 | All 31 checklist items retained. Complete definition/data loading is explicitly downgraded, the visited subquestion is resolved inside the broader still-open historical resource-state item, and selected-sequence range is distinguished from paired visited endpoints. | RESOLVED checklist conformance, subject to final exact review. No formerly unchecked player-action mapping is silently marked complete. |
| Z25 | Source-manifest preparation first expected an exit key absent from the corrected reset-export01 postprocessor receipt; corrected to require its explicit preserved encoding-failure record and authenticated complete export. An overstrict exact-phrase checklist check rejected valid native/B1 clauses and was corrected to test their actual distinction. | Delivery-check preparation failures, not failed science. Subsequent source/hash/range/checklist/graph/link checks pass; originals and prior failed preparation diagnostics remain preserved. Final checks/patches will bind the reviewed snapshot. |
| Z26 | Final manual reading removes the B1 method's ambiguous “public-review” wording; `.local-work/d5z/b1-03/b1.json` reproduces the earlier `b1-02` aggregate byte-for-byte after that docstring-only clarification. | RESOLVED editorial qualification; no publication clearance or scientific-result change. Earlier receipt remains preserved. |

## Question gate before independent final disposition

| Question | Proposed status | Closure argument / residual boundary |
|---|---|---|
| Q1 | COMPLETE | Actual owner/receiver roots, local and nonlocal aliases, bound callbacks and helpers account for ordinary count/capacity/data reads/writes/clears. No ordinary alternate membership writer remains. |
| Q2 | COMPLETE | Positive initialization/complementary load clears and separate native writer/restorer paths establish transient visits with restored persistent inputs. Actual historical B1 demands remain unidentifiable in retained evidence. |
| Q3 | COMPLETE | Direct/module caller predicates and recovery-to-lifecycle distinction mapped. No claim that arbitrary queued work or corrupt/plugin state cannot reset. |
| Q4 | COMPLETE | Dynamic storage, exact payload arithmetic, u32 wrap, conditional null/retry and recovery semantics established; no safe maximum or retail exhaustion outcome invented. |
| Q5 | COMPLETE | Conditional post-reset append model explains a valid bypass. B1 certificates/conditional identity/loss coverage cannot identify the historical target append/query/mask. |

These are scientific proposals awaiting independent original-contract review,
not self-acceptance. Final review/engineering/editorial artifacts must pass before
assignment completion is accepted. No material ordinary native/save branch
identified in this investigation remains unexamined. Historical lost target
fields, actual OOM frequency/behavior and nonordinary inputs are explicit limits,
not silently discarded mandatory native dependencies. D5R remains OPEN.

## Independent closure

Scientific/completeness, engineering/evidence and editorial reviewers ACCEPT
the same 23-file `review01` snapshot, delivery SHA-256
`84990f44f5cde1d15f68d6a46de3487a1d9fdb939e4441043493c43b73843e95`.
The preceding proposal/checkpoint language is retained as investigation history;
Q1–Q5 now have accepted COMPLETE scoped answers. The highest-value omitted
pressure/cell/worldspace branch was challenged against primary leaves, not
deferred as optional work. Verbatim returns and final closure identity are
recorded in [the review package](d5z-review.md).

The apparent SVG mutation during engineering review was a default-code-page
diagnostic error: all raw file hashes remained unchanged. No original evidence
or figure was rewritten. The final change is a small self-describing status/
review closure, independently delta-reviewed. D5R and the historical target
winner remain OPEN; no integration, live action or publication is authorized.
