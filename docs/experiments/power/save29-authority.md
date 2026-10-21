# Save29 allocation authority: deterministic reconstruction

2026-10-17, Australia/Sydney. SOR-EXP-0041 / SOR-EV-0049 continuation.
[Authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_P1_Save29_offline_allocation_authority.md),
[review and acceptance matrix](save29-authority-review.md).

**C — deterministic reconstruction is the best-supported working explanation,
STRONG within ordinary Save29 loading conditions.** The native load-event path
can independently select extractor #1 ahead of #2 from this save's actual
electrical graph. Saved powered bits are restored first, but the applicable
allocation worker does not preserve a satisfactory old assignment by policy:
it calculates a new set, then writes only differences. The graph predicts the
same pair as the saved bits, so ordinary recalculation need not change either
extractor's bit.

The decisive additional evidence is the beacon's ordered electrical list:
**solar, #1, #2**. All three devices link back only to that beacon. With these
links resolving and ordinary eligibility, each of the four possible object
roots reaches the same sole generator. Consumer assessment starts from that
generator and expands forward through the beacon's list: #1 adds demand 5 and
fits supply 6; #2 raises cumulative demand to 10 and does not fit. This derives
the winner without choosing a favourable notified object, sorting FormIDs, or
using powered status to identify the extractors.

The accepted **three fresh-process reloads remain PASS**: #1 on / #2 off.
Restoration alone is sufficient to reproduce that observation, but it is a
weaker causal explanation once a real load-related, independently selecting
path predicts the same winner. No concrete native rule retaining feasible
prior winners was found in the examined worker/selection paths; H is not
supported merely by difference-only writes.

This is engineering confidence from native causality and saved corroboration,
not a captured instruction history of the three loads. Event admission, handle
resolution and invocation-time effective values were not recorded. **PROVEN
historical execution is not claimed.** A qualified ordinary-load trace showing
no applicable worker, or different effective graph/gates that defeat this
selection, would overturn or narrow C. An applicable calculation choosing #2
while #1 remains powered through a demonstrated retention rule would support H
or R instead.

**Stop here:** close this bounded mechanism assignment for independent review;
defer general power-load prediction. No observer, edited save or new gameplay
is needed to justify this working conclusion. The earlier save-writer **NO-GO**
is unchanged. Authored synthesis is REVIEW-REQUIRED; raw native/save evidence
is LOCAL-ONLY, with publication eligibility separate from confidence.

## Technical appendix: identity, provenance and boundaries

Pinned retail **1.16.244.0**, preferred image base **0x140000000**. All native
locations below are hexadecimal **RVAs**, not runtime pointers or save offsets.
Original names remain `FUN_<preferred VA>`; RVA plus image base gives that VA.
Executable SHA-256:
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Main ESM SHA-256:
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Installed version resources and both hashes were freshly checked; they do not
retroactively pin the user's earlier loaded profile. No override merge or
current effective actor-value measurement is claimed.

Save29 original and existing protected archive each remain 2,085,680 bytes,
SHA-256 `ab28c98940b019320cda4d6a0db54c9d88b721a18fba4c6a701fbed0966b42fe`.
Decoded stream is 5,539,576 bytes, SHA-256
`b236f22dd601b2dab59d5640967b12ab1f4dd5b3e4aac58cfae593bf43989579`.
The [console-position join](save29-test-plan.md#subsequent-user-console-identity-evidence)
independently identifies #1/#2. Saved dynamic identities below precede engine
remapping; historical runtime RefIDs, manager handles and pointers are distinct.

### Evidence locator key

`Pnnn` means `.local-work/p1-power/native/nnn.request.tsv`; `Lnnn` means
`.local-work/p1-load/native/nnn.request.tsv`; `L2-nnn` means the latter task's
`native-r2/nnn.request.tsv`. Each locator denotes its `FUNCTION` block and
complete decompilation, supplemented by the specific instruction sites below.
Instruction exports capped at 600 instructions are not used for absence claims.
Existing [P1](sources.csv), [order](followup-sources.csv) and
[load](load-sources.csv) manifests pin the reused exports. Fresh selected hashes,
local derived receipts and tool hashes are in
`.local-work/p1-authority/evidence-pins.json`; baseline checks are in
`baseline.json` in that directory. No Ghidra session or database writes occurred.

### Grounded saved graph

Offsets are **decimal decoded-stream**, half-open ranges. CB words and flags
are hexadecimal; CB words are little-endian u32s. Identifiers are saved FormIDs.

| Object / base | REFR range | ExtraCB range; ordered targets / words | Extra9C word |
|---|---|---|---|
| Beacon `ff022778` / `002c60e9` | [1298916,1299344) | [1299159,1299173); `ff022841,ff022917,ff02294d` / `1,1,1` | `840` at [1299043,1299048) |
| Solar `ff022841` / `002031e1` | [1300005,1300509) | [1300178,1300184); `ff022778` / `1` | `840` at [1300167,1300172) |
| #1 `ff022917` / `0005ef19` | [1300577,1301023) | [1300678,1300684); `ff022778` / `1` | `840` at [1300659,1300664) |
| #2 `ff02294d` / `0005ef19` | [1301249,1301671) | [1301343,1301349); `ff022778` / `1` | `800` at [1301324,1301329) |

All four counted extra lists close; the selected CB graph is reciprocal with no
outgoing electrical endpoint outside these four. This is a closed saved CB
component, not proof of every future/default/runtime relationship. The record
framer traversed all 20,825 R3 records; that structural coverage is not a complete
outpost census. Counted extras do not exhaust whole records or necessarily the
whole reference queue. Non-CB references are not added as electrical edges.

The original positive-subset reader stopped at beacon ExtraBC. This attempt
uses the already owned `workshop_inventory.linked_prefix` BC consumption grammar
in a local adaptation of `saved_instances.extra_view`. Both parsers agree on
counted-extra end and reference cursor for each selected row. This is a bounded
reader extension, not a new BC semantic discovery; shared grammar is not an
independent oracle for all semantics. `save29-graph01.json` preserves the initial
unsupported-BC result, `graph02` the extension, and `save29-graph03.json` the
cross-check. No byte scanning for an attractive `CB` tag or winner-driven
reference permutation was used.

Fresh main-ESM projection `definitions01.json` identifies beacon ACTI
`OutpostBeaconActivator` at original ESM byte 3761304, solar ACTI
`OutpostPowerSolarArray03` at 3555740 and Iron CONT
`OutpostHarvesterSolid_Iron_01` at 5403487. Solar base PowerGenerated is 6;
extractor base PowerRequired is 5. Beacon has neither property in its PRPS.
Runtime eligibility/effective supply remain scoped assumptions corroborated by
the accepted ordinary setup, rather than inferred from the HUD alone.

## Reachable paths and authority operands

| Entry / trigger and RVAs | Gates / candidate root / coverage | Old versus new operands; consequence | Exact evidence / remaining boundary |
|---|---|---|---|
| REFR extras `00b29990` -> `00521620` -> Extra9C `00545e40` | Selected record's restored extra list; modern four-byte branch | Mask `7ffffffd` retains `40`; establishes initial persisted powered state, no consumer selection | L002; AND at `00545fbd` / `00545ff6`. Does not establish final authority |
| Ownership post-load `00b2bc70` -> `00526bb0` -> `00518750` | Restored forward4C/change `100`; append deduplicated reverse4D entries | Rebuilds ownership indexing, not powered-set arithmetic | L002, existing population evidence; order across references is not canonical |
| FinishLoadGlobalData `01827380`, case `0a` -> `005810b0` | Loaded-cell visitors plus restored handle list; references require parent/context/eligibility, including flag4 test | Emits loaded=true with current reference FormID; no allocation result yet | L2-015/016/017; list events near `005812ca` onward. Actual Save29 list membership/notification epochs unrecorded |
| Cell attach `00b11780` -> `00b02630` | Cell index/current reference, admission `00b40660` and loaded state | Further object-loaded events, not a final power barrier | L2-015/017; no assumed mandatory last refresh |
| Workshop TESObjectLoadedEvent `021f0340` | Suppression byte `05f5e1e8` clear; form-map resolution, virtual `+228`, current reference flag bit index 10 clear, loaded=true, forward owner resolves | Calls `0066f880(notifiedRef,null)` at `021f03d9`; root is each admitted object, not a chosen generator. Missing declared owner goes to cleanup `0187bb60` | L003, L004, L2-020/021; registration/RTTI in load report. These are positive relevant paths, not observed historical hits |
| Scheduler `0066f880` / queued adapter `00677150` -> worker `0066fa50` | Validated reference-manager handle; direct designated-thread execution or service queue; worker re-resolves root | Collects old set with `00671470`, creates empty new set, calls allocator `0066b100` with null override for this event. No old-feasible-set early return | P008 full worker; L001 call census. Queued invocation can see later state; no exact timing assertion |
| Generation `00671f70` / callback `0066bcb0` | Ordered CB walk; eligible positive generator predicate `006697f0`, state exclusion `00669ac0`, special exclusion `0066bad0`, effective contribution `00669880` | Seeds new vector and supply independently of consumer `40` bits; this ordinary component has one solar seed | P010/011/017, P007/009/013; state exclusions include activation/fuel conditions, not a consumer powered preference |
| Allocation `0066b100` -> expansion `006722f0` | Positive supply; valid/nonexcluded nodes; terminal and partition gates; CB FormIDs resolve to live references | New consumer winners from expanding seed vector and cumulative demand, not old-set priority. `VADDSS` `0066b531`, compare `0066b535` | P007 complete decompilation plus `0066b51c..0066b54e`; P011 expansion complete. Successful resolution/ordinary categories are conditions |
| Worker result application `0066fa50` -> setter `0066abc0` | Iterate old-only / new-only pointer-identity sets | Clear old-only at `0066fbd6` with arg1; set new-only at `0066fcd6` with arg0. Intersection unchanged. Setter applies inverse argument to `40` and emits updates | P008/P009. No difference does not mean no independent calculation |
| Owner refresh `0066d4b0` through `006728e0`; caller `00f7c060` | Eligible generators in rebuilt reverse4D | Unions per-generator new sets before differences; root-loop permutation alone does not alter union under fixed inputs | P007, L2-018. Not proved mandatory final load stage; singleton case agrees |

Later AV, activation/open-close and topology paths remain as mapped in
[load-determinism](load-determinism.md) and [followup](followup.md). They can
change inputs; they are not evidence that inputs changed in this trial. The
event's current bit index 10 gate must not be tested by directly copying the serialized
form-flag word: generic flag loader RVA `005dfa40` merges only masks `d12960`
or `30860` into current reference `+20`, neither of which includes `400`.
Exact instructions are `005dfb3b..005dfb4a` and `005dfb94..005dfb9f` in
`.local-work/p1-order/native/006.request.tsv`. This does not measure the current
bit or rename it as a proven disabled-state semantic.
The
examined boundary is the listed restoration/finalization/event/scheduler/core/
difference chain and relevant owner/activation/partition helpers. No executable-
wide callback search or proof of universal nonexecution is claimed.

## Ordering provenance and bounded Save29 derivation

| Candidate ordering source | Actual role in the examined paths | Save29 consequence |
|---|---|---|
| Serialized ExtraCB array | **USED** by loader `0065be30`, enumerators `006779e0` and `006722f0`; forward array order is retained | Beacon's solar/#1/#2 order directly yields #1-before-#2 consumer assessment |
| Notified reference | **USED** as load-event root | All four eligible roots in this connected graph yield the sole solar seed, so no favourable root is selected after seeing the winner |
| Generator collection / setting | **USED**: front insertion/promotion (`00675c50`, `00677c50`) or recursive forward traversal (`00676350`) | Generation visit order differs, but a single eligible generator gives the same seed; consumer expansion is a separate forward append vector |
| Restored global notification list / cell traversal | **USED** by notification producers; saved-list ordering and backward cell-array visitor are concrete | Actual Save29 list was not decoded. Cross-object event order need not be chosen to explain the fixed applicable component result |
| Extra4C / rebuilt Extra4D | **USED** for owner resolution / owner-refresh generator enumeration | No 4D consumer priority or saved 4D array is invented. One eligible generator makes its owner-root order immaterial here |
| Saved FormID magnitude / record offset | **AVAILABLE**, not an explicit priority key in this core | Their correlation with #1 is not the derivation. CB order remains the basis after identity remapping |
| Pointer order / manager handles | **USED** for identity sets / validated lookup, not the consumer vector's numeric priority | No pointer/handle sorting is substituted for saved CB array order |
| Saved consumer `40` bits | **USED** for old-state comparison/application; not selection inputs in this worker/core chain | Reversing only the illustrative old set changes differences to apply, not the computed winner |

Starting at beacon, solar, #1 or #2, both generation modes reach the same solar
seed under fixed admitted links. Stage two assesses solar then beacon, appends
the beacon's targets in stored order, skips the already visited solar, and
assesses #1 then #2. Ordinary consumers can terminate expansion; their sole
outgoing edge is back to the already reached beacon, so this does not change
the consumer sequence. The beacon has no base demand. Supply 6 and binary32
integer demands 5+5 yield cumulative 5 then 10; these exact small integers add
no rounding ambiguity. With an already matching old consumer set `{#1}`, the
consumer symmetric difference is empty. That leaves restored bits unchanged
while the new-set selection is independently determined.

Local `model01.json` checks all four roots in both generation modes, all four
old consumer sets for each, and reversal of the beacon's two consumers (which
selects #2). **This is an illustrative fixed-input projection, not a native
invocation, emulation of all gates, or validated production predictor.** Native
control/operand evidence supports the interpretation; a passing model alone
does not. Missing runnable historical inputs are exact event admissions,
resolved reference lifetimes and invocation-time eligibility/effective values.
Those limit confidence to STRONG, but do not leave two equally supported
ordinary-case mechanisms under this brief's reasonable engineering standard.

## Hypothesis assessment and direct answers

| Hypothesis | Supporting evidence | Concrete conflict / missing link | Rank and burden |
|---|---|---|---|
| C: independent deterministic reconstruction | Real load/attach sink reaches unconditional calculation after root resolution; actual saved CB order selects #1 for every applicable component root; old consumer flags are outside winner arithmetic | Historical event/worker execution and effective inputs not captured; no disagreement with restored flags is expected here | **1, STRONG ordinary-case working explanation.** No requirement to show restoration irrelevant elsewhere |
| R: restoration retains selection authority | Extra9C loader preserves `40`; accepted final pair matches saved flags | Relevant calculation independently selects that pair; no satisfactory-old-set bypass is present in examined worker/core. Requires this applicable computation to be absent/nondecisive in the actual load, without positive evidence for that exception | **2, observation-compatible**, but less causally supported than C. Restoration itself remains established |
| H: conditional retention of satisfactory winners | Difference-only writes preserve intersection; eligibility/scheduler conditions are real | Intersection preservation happens after independent selection, not a prior-winner preference. No concrete old-assignment satisfaction rule established | **3, unsupported as the selection explanation**; conditional execution alone is not this H |

1. **Restored bits suffice to reproduce the observations.** They do not alone
   explain why the positive ordinary load path would leave them authoritative.
2. **Independent ordering and selection are demonstrated on a relevant reachable
   load path**, with actual saved graph provenance. Historical hits are inferred,
   not measured.
3. **Matching recomputation independently determines the pair algorithmically**
   without necessarily changing consumer bits. Historical effective mutation
   remains observationally indistinguishable from restoration on this baseline;
   this does not erase the causal selection contract.
4. **#1 is predictable without choosing a root or sorting identities**, within
   the fixed ordinary graph/eligibility conditions above. This is not a general
   save-to-settled-power predictor.
5. **Use C / STRONG now; close/defer P1 mechanism research.** Reopen for a concrete
   contradictory native/observed path, independently decisive evidence, or a
   material application need. Do not build an observer merely to eliminate
   conceivable unexamined callbacks.

This prospectively supersedes the Save29 mechanism-OPEN disposition and
automatic temporal-capture recommendation in earlier P1 planning documents.
Their evidence and historical uncertainty remain preserved. The accepted reload
PASS and [writer NO-GO](save29-derivatives.md) are unchanged. No general native
function discovery warrants a new function-register row or project-wide policy
decision. Scientific confidence, independent assignment acceptance and maintainer
integration/publication permission remain separate.
