# D5AV player-action persistence matrix

2026-11-06, Australia/Sydney. [Findings and evidence scope](d5av-report.md) ·
[GC decisions](d5av-cache-decision-matrix.md) · [Evidence ledger](d5av-investigation-ledger.md).
The comparison concerns the geographic source serving Feynman V Cu IL F
where identified, key `0:37536:20928:0029d20e`, body FormID `0x0005e0de`.
Native addresses are preferred static VAs on Starfield 1.16.244.0, image base
`0x140000000`. Source key, process-local allocation ID, runtime pointer, map
slot and visited token represent separate identities.

## Evidence and outcome legend

**STATIC** establishes a compiled branch under its premises. **SAVE** establishes
serialized inputs in the bounded sample. **NATIVE CONTROL** executes selected
original instructions on fixtures. **RETAIL** combines instrumented events with
operator-reported actions where indicated. Emulation is identified separately.

- **Retained / reused** means a qualified interval of continuous ownership with
  actual holder or geometry use. The interval matters.
- **Rebuilt identical / different** requires a new population and a complete,
  source- and frame-qualified output comparison, with the attribution and
  telemetry limitations given in the row.
- **Generated, output unqualified** means construction ran but complete
  comparable output was unavailable. It is distinct from an unqualified attempt
  to attribute a snapshot to its source.
- **Conditional** gives the consequence of a supported native predicate.
  **Unknown** means the actual action-to-predicate or output edge is missing.

## Action-to-transition table

| Player action and context | Evidence and qualified native path | Source, holder, collections and visited state | Lookup, generation and geometry | Player consequence and decisive limit |
| --- | --- | --- | --- | --- |
| 1. Remain at the outpost and move within retained coverage | **Conditional · STATIC.** Focus `0x14078c5f0`, mode 2 and no blocking transition, can remain below the translated X/Y shift threshold. At threshold, the manager-exclusive shift `0x14078ce00` can still preserve source overlap. ProcGen shift slots are no-ops. [D5AH predicates](d5ah-lifecycle-matrix.md#reset-and-return-predicates) | Same published source, map holder and collections survive this branch if no relevant erase, reset or owner change intervenes. Its visited state survives the branch as well. | No new demand can mean no lookup at all. A matching visit bypasses lookup. An unvisited demand that reaches a protected hit skips sampling. A consumer can read the retained map independently. | Under those conditions existing contours persist. A footstep, distance estimate or unchanged list cannot show which branch ran. No matched movement-only retail interval ties this branch to the complete target here. |
| 2. Open and close existing Build Mode at Feynman V without placement or movement | **Retained through the scan · RETAIL + STATIC.** D5AK A0 and A1 separately join completed generation and source/content history to protected resident-map snapshots at existing-outpost scans. The operator reported opening Build Mode. The inspected `0x1421e07d0` refresh reads the map under its shared lock when domain/translated displacement calls for a scan. [D5AK A0/A1](d5ak-a-report.md#source-identity-complete-bytes-and-lifetime-result) · [D5V area path](d5v-lifecycle-consumer-map.md#native-geometry--area-catalogue-and-extractor-decisions) | At each completed native traversal the complete target collections were still resident from that episode's construction. The native scan does not change target ownership or visited state. A reused Workshop list alone carries no contour ownership. | Occupied-slot traversal reads current collections without a provider hit/miss or raster sample in the scan. Existing placement setup is a conditional caller. A reported Pilot03 open/close did not yield an eligible capture before STOP. | Opening Build Mode can expose already-generated geometry. Whether a specific reopen reaches setup, and whether the same population spans the entire open/close action, remain unknown. [Trigger control](d5ar-pilot03-trigger-followup.md) |
| 3. Fast-travel within the same planetary area, then return to the same outpost | **Unknown action mapping · STATIC conditional.** The mapped travel processor can avoid installation on a matching component/context path or reach focus update, installation, or true reset on qualified branches. Preserved overlap under the same owner allows row 1. Overlap loss through `0x140987080` can retire the source. Cell or component changes can take a reset branch even when planet identity is unchanged. [D5AH](d5ah-lifecycle-matrix.md#transition-matrix) | Retention preserves the live tuple. Retirement frees the source and removes its map owner, potentially leaving a collection reference elsewhere and retaining visits. A broad reset clears both stores. | With an equal surviving token, a later source can bypass with no lookup. Otherwise an eligible miss may resample. No source-joined sample or complete comparison for this action. [Bounded travel paths](d5av-report.md#what-actually-survives) | Same area does not guarantee stable deposits. Missing edge is actual owner/component, overlap and first return decision for a named hop. |
| 4. Travel to a different planet and return | **Unknown action mapping · STATIC conditional.** A qualifying component mismatch in `0x14078cf00`, owner installation in `0x140789ce0`, or gated cell transition in `0x14057abc0` can clear ProcGen. The installer can also take false reset for same owner/component. [D5AH exact gates](d5ah-lifecycle-matrix.md#reset-and-return-predicates) | For the target, observe which Grid is cleared or source retired and which ProcGen is reset or replaced. The broader branch empties map and visits. Narrow retirement leaves visits. | Successful return preparation can expose a new source and eligible miss. No independently qualified generic different-planet return cohort. Row 6 supplies one specific itinerary. | A different planet can be part of a rebuilding trip. Destination category alone cannot identify the executed predicate or forecast changed contours. |
| 5. Travel to another star system and return | **Unknown action mapping · STATIC conditional.** Same proven receiver-level alternatives as row 4. The bounded owner/component graph gives no additional verified rule keyed solely to a system change. [D5AH exact gates](d5ah-lifecycle-matrix.md#reset-and-return-predicates) · [D5AD context boundary](d5ad-load-chronology.md#native-dependency-order) | Same conditional lifetime outcomes as row 4. Equality of body/descriptor on return does not prove uninterrupted source ownership. | No separate action-attributed sample or complete comparison here. Even if the named itinerary crosses systems, row 6 isolates no effect of crossing a system boundary. | No distinct player-facing guarantee for intersystem travel. Missing edge is an observed or positively established system-specific selection of a target invalidator. |
| 6. Feynman V Cu IL F → Lodge **exterior fast-travel marker** → Feynman V Cu IL F | **Rebuilt identical · RETAIL + STATIC.** D5AK Episode A recorded installer → true reset → owning Grid clear → exact target erase. ProcGen clear followed. Another installer/true reset and ProcGen clear preceded return generation. [D5AK receiver and sequence proof](d5ak-a-report.md#which-native-path-actually-executed) | A0 allocation 932, A1 allocation 30579, same geographic source. Exact erase ended the old holder and all three recorded collection-content lifetimes. Reset clears visits under the native contract. Both constructors record successful new token stores. | Protected misses at A0/A1, direct `0x3` samples from `[8,3]` and `[-1,11]` respectively. Complete normalized target equality over 5,090 bytes. [Direct events](d5am-retail-events.csv) · [Byte proof](d5ak-a-report.md#source-identity-complete-bytes-and-lifetime-result) | Deposits could look unchanged after real rebuilding. The recorder identifies the nested path, with initiating caller and exact installer operands unknown. Scope is one trip to that exterior marker. |
| 7. Save while the outpost remains loaded, without reloading | **Conditional · STATIC + SAVE.** Audited ordinary global type-3/type-7 writers write context/descriptors and PCM data. Producer/reference writers have separate receivers. [D5AD state matrix](d5ad-save-state-matrix.md#state-classification-and-its-limits) · [D5AH serialization](d5ah-extractor-continuity.md#what-is-serialized-and-reconstructed) | The audited serialization provides no population transition by itself. If runtime owner, source and map remain live through the interval, holder, collections and visits can persist. | Saving alone supplies no target lookup, raster sample or complete before/after measurement. Separate streaming or invalidation could occur during a save. | Saving does not pin deposits for future loads. A save-only retail interval spanning the target's complete lifetime was not isolated. |
| 8. Ordinary full reload within the same running process | **Conditional · STATIC + SAVE.** Drain precedes revert range `(0,17,0)`. With stable `bAvoidClearOnReload` and valid ordinary objects, zero takes type-3 revert reset, nonzero takes type-3 manager-reader reset. Both reset flags clear ProcGen. [D5AD load order](d5ad-load-chronology.md#native-dependency-order) · [D5AH exact gates](d5ah-lifecycle-matrix.md#reset-and-return-predicates) | The manager allocation can survive the reset. Map ownership and visits clear. Old contour references do not become serialized inputs. Source preparation uses restored descriptors and PCM and can finish after the load returns. | Eligible unvisited miss can generate anew. A reset, load completion or source birth supplies no evidence of target sample or complete output. B2 is a fresh startup/load and arrival, with reset caller unknown. | Reload can permit a different result if fresh complete generation occurs. No isolated warm reload binds actual target reset, miss/sample and full output. |
| 9. Exit, restart and load the same unchanged Save52, then visit Feynman V | **Rebuilt identical · RETAIL + STATIC + SAVE** for D5AL A0/B0. **Different complete cold-start populations · RETAIL** for the D5AS class comparison, with construction mechanism conditional at individual D5AS snapshots. Ordinary bootstrap constructs when the singleton is absent. [D5AL](d5al-b-report.md#exact-baseline-and-represented-content) · [D5AS](d5as-series-closeout.md#frozen-roster-and-comparisons) · [D5AD startup](d5ad-load-chronology.md#startup-admission-and-the-save52-branch) | Process exit ends old source/holder/collection and visited lifetimes. D5AL binds distinct process births, new publication and new generation despite the same numeric allocation counter. D5AS binds distinct processes and resident source/frame. The same-Save52 load and visit procedure is operator-reported. Loaded save, route and effective deployment were not independently verified for each run. | D5AL B0 records a miss and direct `0x3` sample with complete equality to A0. D5AS records 2 mask-0-reference, 28 mask-3-reference and 0 other complete qualified results. D5AS captures do not directly observe generating mask, lookup or generator. | D5AL shows equal complete geometry on pinned starting inputs. The D5AS visit procedure yielded different complete geometry classes, with individual effective inputs unverified. Save52 starts inside the Lodge, so this is load **and visit** evidence. It supplies no changed-geometry event within one process and no frequency prediction for a given player. |

## Controls that distinguish the outcomes

The Build Mode scan-boundary result establishes actual completed native
traversal with the complete target resident. The pre-release conjunction
`EDX == 1` and `RDI == R12` at `0x1421e0a79` distinguishes it from a
cached-list bypass or a stopped traversal that reached capacity. Individual
target-region admission and complete action-spanning retention are separate
questions. Pilot03 armed for one established-operation path. The mapped
preview and reference-transition callers are outside that trigger, so the
refusal does not prove no area refresh or target absence.
[D5AI traversal controls](d5ai-source-lifecycle-map.md#area-traversal-completion-two-rejected-oracles-and-the-native-control) ·
[D5AR Pilot03](d5ar-pilot03-trigger-followup.md#what-pilot03-established).

**B2 confirms actual map reuse and separately confirms a generation event
without qualified complete output.** Invocations 3837 and 3844 both see the
same live target unvisited. Invocation 3844 reaches the protected miss at
8091, generates and samples `0x3` at 8093–8094, and stores the token at
8106. Invocation 3837 reaches hit 8339 with the same source pointer and ProcGen.
Later visits bypass before lookup. The continuous allocation and protected
map decision establish holder reuse. B2 did not record complete contours or
an isolated warm player action. [D5AC exact decision order](d5ac-target-lookup-chronology.md)

**An unrelated Grid clear can preserve a target in the same ProcGen map.**
D5AJ attributes nine clear pairs to other owning Grids and qualifies continuous
source/holder history through the complete scan. The erase compares the full
source pointer. Native controls show a collision-chain survivor can move slots
and a collection can outlive the loss of one map ownership edge. An observer
epoch increment alone cannot establish target retirement. [D5AJ typed receivers](d5aj-invalidation-matrix.md#correct-the-receiver-domain-before-scoping-a-fence) ·
[D5AH release controls](d5ah-lifecycle-matrix.md#native-release-addendum)
