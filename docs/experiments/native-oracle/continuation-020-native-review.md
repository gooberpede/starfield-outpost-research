# Native-oracle 0.2.0 specialist static review

2026-10-12, Australia/Sydney. Governing authority: [continuation brief](../../implementation-briefs/CODEX_BRIEF_SOR_native_oracle_reachability_continuation.md). Specialist research, not the independent implementation acceptance review. **Recommendation: retain the minimal Q/E additions and the conditional one-new-Kreet-landing N1 scenario. Native reachability remains NOT TESTED for 0.2.0.** No static implementation defect explaining attempt01's empty callback set was established.

## Independently inspected evidence

The specialist read the primary instruction exports below, rather than treating prior agent summaries as evidence. Paths are repository-relative, ignored LOCAL-ONLY exports; hashes identify the inputs, not semantic truth. Retained native exports and proprietary PE bytes are not incorporated into this authored report.

| Primary export under `.local-work/recon/` | SHA-256 | Decisive locations |
|---|---|---|
| engine-oracle-01.tsv | 33c4508537b7993cc6942a3ecc8bc8b8bd77812a5d3bb9c7b104efa5ac35cfad | AD0B90 callback gates, center/grid CALLs, private scratch and output consumption; lines6–195. |
| engine-oracle-02.tsv | 13739f8755ec6a4f164a7f1759c2d19197c29eb7f81428cb5714a6b2731e42b8 | AD8EC0 thunk lines6–15; vtable references45–46; query instructions48–213. |
| engine-oracle-04.tsv | a1294f6a39e711622e3dbb55cf74ffaa09c251aa37022ebfacdeb698703fe762 | AD92E0 constructs Q context32–40; invokes Q69, consumes EAX70–71; upstream callers195–198. |
| exp0002-selection-sites.tsv | 1f2d830b761dcd72ce719f22509f3670e1acb41b3106b9c74347675e833225f9 | B1E190 reference filtering and indirect dispatch827–917. |
| durable-center-04.tsv | 8a8cd7abff1a44c44d33f7f9f39e97d8503906cff73e645b58b6ff661e56636f | Existing-reference CALL1994 and fallback CALL2038; corresponding decompilation2212–2245. |
| static-exhaustion-04.tsv | b43b4ab1f67c6db02a2c82acef192550115c8109336cd7b236f14abeee7886e8 | Candidate search77E350 starts1115; natural AD92E0 CALL1412, with preceding eligibility/context instructions. |
| exact-beacon-05.tsv | ab80b3416b477d10123d008a8febd09ae5ccc987f55643108c82a8873509a1c7 | Terrain-placement caller78B030 invokes77FC20 at78B877, line1695. |

Fresh read-only SHA-256 on the installed `C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe` agrees with all inspected export headers: `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. Preferred image base is0x140000000. Prior independent PE reads in this specialist session verified the center/grid complete CALLs and callback vtable. The retained [proposal](revised-acquisition-plan-01.md) contains the separate Q/E PE-byte receipt; this review independently rechecked their instruction contracts in primary exports, not a new Q/E byte receipt.

A fresh direct PE read using PowerShell/.NET FileStream inspected RVA00B1E190–00B1E38F at file offset00B1D790. Manual decoding, checked against the exported dispatch windows, confirms the consumed E arguments and return below. This is a bounded inspection, not a generic disassembler or whole-image control-flow proof. No external analysis tool or third-party implementation was executed, downloaded or adapted.

## Native ABI and stage linkage

All instruction addresses in this section are static VAs; subtract0x140000000 for their RVAs. Runtime addresses require the observed loaded base. Member offsets are runtime structure offsets, not save offsets.

**Q:** Complete CALL140AD93FA targets140AD08D0. RCX supplies the five-pointer query context; RDX supplies a candidate descriptor. The inspected query consumes these two arguments; no additional register/stack argument was identified. Context construction is explicit at140AD9345–140AD9374. The query exit140AD0B74–140AD0B7C loads context+8's output-byte pointer, zeros EAX, compares the byte and SETNZ AL. Thus EAX is0/1. Caller140AD93FF compares full EAX with1. Preserve the consumed uint32 result; an inferred AL-only return contract is insufficient.

**E:** Complete CALL140AD0AB5 targets140B1E190. Natural caller sets RCX to resolved form+0xD8's collection, RDX to the stack callback object, and R8D to0. Fresh PE prologue140B1E1A4/1A8/1AB consumes R8B/RDX/RCX into R15D/R13/RBP. No consumed R9 or stack argument was identified in the inspected function. Epilogue140B1E370 returns EAX=R14D, initially1 and subsequently assigned the callback's EAX. Preserve uint32 return even though this exact caller overwrites RAX immediately afterward.

**C:** Enumeration dispatch140B1E2C0 and140B1E33C loads the callback object's actual vtable and calls slot+0x10, forwarding the object and reference-slot pointer. The option-zero caller follows the latter collection branch. Both original callback slots at static144B916F0/144B916F8 identify140AD8EC0. Thunk140AD8EC0 dereferences RDX, loads RCX from object+8 and tail-jumps140AD0B90. Query140AD0A9D constructs the object with the exact144B916E8 table. This inspected path supports the selected slot contract; it does not demonstrate an alternate copied table or devirtualized bypass. It is not a whole-game absence claim.

Q→E→C must be linked by actual nested invocation/thread identity. Independent or incomplete scopes cannot establish qualified zero-child branch results. The center channel is the callback's CALL140AD0C36, not all seven known callers of helper140F4AB80. Therefore zero center records cannot exclude fresh centers in separate descriptor/border/clamp/publication consumers.

## Gate and oracle limits

Q requires candidate resolution, non-null overlay resolution and active landscape, then compares candidate/source native hierarchy fields and tests overlay+0x20 bit0 before E. Evidence: engine-oracle-02.tsv76,82,95–127. E filters collection population, reference flags and non-null bases before C; the optional nonzero-R8B path has additional cell filtering. Native C itself checks base/type/Workshop eligibility before center/grid.

A complete Q with no E isolates pre-enumeration traversal but does not identify a particular failed predicate. E with no C does not prove an empty collection or absence of outposts. Optional raw snapshots do not turn earlier sampled flags into proof of a later native branch decision. Exact gate diagnosis would require additional reviewed natural helper-result observations; these are outside the minimal Q/E patch set.

The selected hierarchy is callback-private scratch at RBP-9. Center RBP-49 is later overwritten by projection, and floor storage RBP+6F is later reused. External candidate/source buffers are inputs; a vtable-only postcallback wrapper cannot recover or relabel them as the selected native output. Retaining the center/grid CALL wrappers is therefore justified.

## Trigger recommendation and N1 consistency

The [architecture](continuation-020-architecture.md) and [current card](continuation-020-run-card.md) correctly distinguish existing Save25/26 controls from an established Q-positive trigger. Primary data flow links terrain placement78B030→77FC20 at78B877, then existing-reference search77F900 at7801B3. Only a null existing-search result reaches fallback780264→77E350. Candidate processing then invokesAD92E0, whose140AD93FA CALL is Q. Native request-mode and eligibility branches remain relevant: ordinary travel does not prove every link executes.

Conditional N1 is a defensible accessible opportunity: from a controlled Save26 descendant on Kreet, use ordinary ship/orbit/map controls to select one genuinely new landable point distinct from existing outpost/Landing Area and POI/quest markers, land once, settle and preserve a new checkpoint. This tests a different request condition from the earlier successful existing-site revisits. It does not guarantee bypass of existing-reference search or positive Q/E/C. A virgin location can supply candidate-query diagnostics while containing no Workshop reference eligible for C. New beacon preview alone has no established linkage to this graph.

The current N1 card is consistent with these limits: explicit combined approval, one agreed new point, new manual baseline/landed slots, filename/hash/parent mapping, incidental autosave preservation, no original overwrite, no new beacon, no second landing/reload and no automatic Save52 fallback. No extra outpost slot or specialized unlock is needed by this landing-only design. The low-level eight-outpost limit therefore causes no construction requirement. New-site evidence remains a diagnostic holdout, not an addition to the frozen23 prediction corpus.

If Q/E/C remain absent under healthy qualified capture, preserve that scoped negative. Do not improvise new placement or travel. A populated-beacon scenario or mature Save52 lineage would need explicit specific approval, capacity/accessibility checks and independently frozen expectations before any new scientific comparison. It is not required for this minimal N1 diagnostic trial.

This static assessment does not certify the card's release-lock placeholders, binaries, fixture results, startup compatibility, instrumentation overhead or complete engineering acceptance; those belong to the implementer and independent reviewer. Neither overlays nor unfamiliar module names establish a conflict. Actual owned-site guards and specific interference evidence remain necessary.

## Outcome and authority

Static Q/E contracts and bounded gate/trigger rationale: supported within the inspected paths. Actual0.2.0 game reachability, same-frame native equivalence and N1 runtime feasibility: **NOT TESTED**. The recommendation preserves uncertainty while supplying a materially different natural candidate-processing opportunity and diagnostic stage separation.

Only this authored report was created by the specialist. No source code reuse, native tool execution, game launch/attachment, deployment, configuration/overlay change, save creation/modification, Ghidra/database mutation, staging, commit or push occurred. Original exports, game bytes, protected saves and frozen predictions were read or left untouched.
