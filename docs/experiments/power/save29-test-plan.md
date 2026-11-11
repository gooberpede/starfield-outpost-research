# Save29: accepted reload result and mechanism test plan

**Prospective Save29 supersession, 2026-10-17:**
[Offline allocation-authority adjudication](save29-authority.md) selects
**C / STRONG** within ordinary Save29 conditions, from a grounded beacon CB
order and root-independent single-generator selection. Earlier mechanism-OPEN
language and temporal-capture recommendations below are retained history,
superseded for this bounded question. Reload PASS and writer NO-GO are unchanged;
historical instruction execution/general prediction remain unproved. No new live
or writer work follows; [review](save29-authority-review.md) controls disposition.

2026-10-17. SOR-EXP-0041 / SOR-EV-0049 continuation.
[Authorized planning brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_P1_Save29_restoration_vs_recalculation_test_plan.md`).

| Item | Response |
|---|---|
| Agreed Save29 test | **PASS  -  repeated-load allocation is consistent in this controlled configuration.** Before saving and after each of three desktop exits/fresh loads of the same Save29, the user found #1 powered and #2 unpowered, immediately and again several seconds later. One solar array supplies 6, two small Iron extractors demand 5 each; the UI reports 10 needed / 6 total. This empirical question is settled for project purposes. |
| R vs C | Saved bits are independently decoded as one on / one off. Subsequent user console XYZ readings link #1 to saved `ff022917` and #2 to saved `ff02294d` at displayed precision. The saved pair agrees with the previously reported live pair; restoration and recomputation to the same set remain observationally equivalent. Actual writer execution on the three historical loads was not captured. |
| Recommended decisive next experiment | **Propose one fresh-process temporal capture of unchanged Save29**, after a separate instrumentation qualification and live brief. Identify both references independently, observe restoration before the first applicable allocation, capture actual calculation/result application and every effective powered-bit transition through the agreed observation endpoint. A surviving allocation-caused transition decisively falsifies R. If computation agrees with restored bits, report equivalence and stop; only then consider a separately approved protected-copy bit-conflict experiment. There is no demonstrated decisive ordinary-UI-only player protocol for this baseline. |
| Predicted outcomes | The preregistered table below separates decisive transitions, matching computation, absent computation and inadequate coverage. |
| Permissions | This assignment permits documentation, protected backup/hash and bounded offline reading only. The user may supply already-held reference-identification evidence or clarify the completed test now. No additional research gameplay/save generation is authorized here. New gameplay, observer engineering/deployment/live capture or copy perturbation requires its own scoped approved brief; the latter examples are assessed proposals, not actions. |

## Preregistered outcome rules

R means restoration survives to the endpoint **without a superseding allocation**;
C means an actual load/activation allocation result supersedes restoration before
that endpoint. Both allow an initial restoration. Hybrid/conditional paths are
explicit alternatives. These definitions and the following acceptance rules must
be frozen in the approved live card before testing. No result changes the Save29
repeatability PASS.

| Observed result, with qualified identity/coverage | R | C / other conclusion |
|---|---|---|
| Restored bit changes through an identified allocation writer; its result survives to endpoint | Falsified for that consumer/load | C supported for that consumer/load; both consumers require both identities and histories. Does not explain root choice |
| Applicable allocation executes, computes the same set, and makes no effective bit change | Strict absence-of-computation model falsified, but R's surviving-state authority remains unresolved | Computation occurred; counterfactual authority is **not distinguished**. A setter hit or same-value store alone is insufficient |
| Restoration persists and a complete qualified history excludes applicable allocation/result application through endpoint | R supported **only for that captured interval/path** | C falsified within that interval; no claim about all later play or other attach paths |
| Different consumers/epochs have different provenance, or a later writer undoes an earlier change | Pure R does not explain changed consumer | Hybrid or superseding writer; identify terminal effective update, do not force C for both |
| UI matches save, callback merely reachable, polling sees no change, missing start, dropped events or unknown writer | Undecided | Undecided; negative detector output is not absence proof |
| Validated conflict copy restores reversed bits, then allocation changes them to its independently observed different result and retains it | Falsified on the copy | C supported on that perturbed path; transfer to untouched Save29 remains conditional |
| Validated conflict copy preserves reversed bits despite a separately established contrasting C prediction and complete coverage | R supported on the copy | That specified C prediction falsified; check no-op/difference-set and selective application alternatives |

## Evidence: completed player trial and independent offline inspection

The brief is the durable source for the user's three runs, desktop restarts,
immediate/repeated inspection and identification of foreground screenshot #2 as
extractor #1. No trial timestamps, recordings or instrumentation were supplied;
several seconds is the reported wait, not retrospectively an imposed timer.
The supplied images were visually inspected in this conversation: `1716740_64.jpg`
shows the selected Iron extractor's Power 5 row red; `1716740_65.jpg` shows it
normal. Both show Needed Pwr 10, Total Pwr 6 and Production 1.66/MIN. They support
the displayed configuration, not three runs or a native getter result. File
SHA-256 values respectively:
`dddcc92b449904306d6acd0a33011ebe0361053d961a3dc0780909e2522814dc`,
`6dd98183b64ffaaffdb6b050fc3ff5c7c67e76f4e1f1573537bf28cd9d474bef`.
Raw images remain local under `.local-work/screengrabs/`.

Original `Save29_D6036588M417474696C61204B6972616C79_000216_20261017043132_3_0_4.sfs`
in the user's Saves directory: **2,085,680 bytes**, SHA-256
`ab28c98940b019320cda4d6a0db54c9d88b721a18fba4c6a701fbed0966b42fe`.
A new exclusive byte copy under `.local-work/p1-save29/protected/` matches.
Only that copy was decoded; original Save3/Save29 remain unchanged by hash.
Decoded stream: 5,539,576 bytes, SHA-256
`b236f22dd601b2dab59d5640967b12ab1f4dd5b3e4aac58cfae593bf43989579`.
Offsets below are **decimal decoded-stream offsets**, half-open ranges, not
compressed-file offsets or runtime addresses. ExtraFlags words/mask are hex;
the tag occupies the first byte and the following four bytes are little endian.

| Saved dynamic reference | Base / role | Record range | Extra9C range / word / powered mask 40 |
|---|---|---|---|
| `ff022841` | `002031e1`, OutpostPowerSolarArray03 | [1300005,1300509) | [1300167,1300172), `840`, set |
| `ff022917` | `0005ef19`, OutpostHarvesterSolid_Iron_01 | [1300577,1301023) | [1300659,1300664), `840`, set |
| `ff02294d` | `0005ef19`, OutpostHarvesterSolid_Iron_01 | [1301249,1301671) | [1301324,1301329), `800`, clear |

All three positively identified rows have decoded disabled/deleted false,
forward owner keyword `00054ba6` to `DYNAMIC:ff022778`, and one CB word-1 edge
to that beacon candidate. This is a simple membership subset, not explicit
word-3 wiring or an exhaustive network census. Extra counts close for these
rows; counted extras end before whole-record end, which is not interpreted as
unparsed power state. The existing positive-subset reader reports 71 prefix
queue bounds, 21 record-boundary and 76 self-reference gaps elsewhere. These
are retained coverage limits, not absent devices or a complete graph proof.

**Historical gap at review02, resolved below by subsequent console positions:**
no unambiguous #1/#2 reference join had yet been supplied. Saved powered values must
not themselves be used to assign #1=`ff022917`: that would assume the match
being tested. Saved XYZ for these extractors are respectively
(105.2583999633789,282.58807373046875,16.822933197021484) and
(87.36466979980469,269.6070556640625,14.886632919311523), but the screenshots
lack reference IDs or a calibrated camera/position join. Minimum missing
mapping: a positively selected per-extractor FormID captured beside its visible
identity, or a qualified same-epoch reference/position selection capture.
Runtime pointers/handles must be reacquired and joined to remapped FormIDs.
Thus Save29 has **no demonstrated saved/live disagreement**; its one-on/one-off
pair is compatible with the report, not by itself discriminating.


### Subsequent user console identity evidence

The user confirmed the initial selections were from the same Save29: #1
`CONT FF019DA1`, powered; #2 `CONT FF019DA6`, unpowered. After exiting,
restarting and reloading Save29, the user supplied these new selections and
`getpos` results. This is a user transcription, not an instrumented capture.

| User object | New live RefID | Reported XYZ | Corresponding saved identity / XYZ rounded to console precision |
|---|---|---|---|
| #1 | `FF019CAA` | (105.26,282.59,16.82) | `ff022917`: (105.26,282.59,16.82) |
| #2 | `FF019CAF` | (87.36,269.61,14.89) | `ff02294d`: (87.36,269.61,14.89) |

Each triple matches only its corresponding member of the two saved Iron
extractor candidates. This closes the practical #1/#2 correspondence gap
within this controlled pair independently of powered status, with console
precision and user-reported selection provenance explicit. It is not a global
position-uniqueness proof or a captured engine remapping table. Prior live IDs
are retained as session-specific observations, not stable save keys. The owned
`outpost_membership.token_value` explicitly returns the saved identity domain
before engine remapping; numeric saved/live equality was never required.

The mapped saved bits (#1 on, #2 off) therefore agree with the earlier reported
live allocation. **R versus C remains OPEN**: both can produce that agreement.
The latest message supplies positions and changed IDs, not a new pair of power
readings; it is not counted as a fourth repeatability trial. Exact comparison
receipt: `.local-work/p1-save29/position-join01.json`. No game/process access,
save generation or original modification was performed by the agent.

The local reader `read_save29.py` adapts project-owned
[saved_instances.py](../../../research/p1-power/saved_instances.py), changing
only root/output and explicit source-receipt selection. It uses existing strict
stream decoder, record framer, token/plugin resolver, reference prefix and
counted-extra reader, with the same P1/E2 definition caches. CPython 3.14.3,
`-B`, stdlib/project code only; C:/D: 40 GB free-space guards retained. It writes
exclusive local JSON and disposable decoded scratch; scratch is removed on
exit. No target, config, database or original-save writes. The initial local
filename `inspect.py` shadowed Python's stdlib and failed before decoding;
renamed to `read_save29.py`, then the unchanged inspection criteria passed.
Exact tools/caches/native inputs and images are pinned in
`.local-work/p1-save29/evidence-pins.json`; raw receipt is
`inspection/inspection01.json`. No new third-party source or implementation.

## Minimal technical basis

Reuse the [accepted load mapping](load-determinism.md),
[allocation follow-up](followup.md) and [native contracts](native.md), rather
than initiating more native mapping. Retail 1.16.244.0 preferred image base
`0x140000000`, executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
ESM SHA-256 `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Installed files were freshly hash-checked; the historical player's module/profile
was not captured. All prospective runtime sites require actual module relocation
and byte-guard verification for the approved build.

| Site (RVA, hex) | Reused evidence and implication for design |
|---|---|
| Extra9C loader `00545e40` | Prior L002 export retains powered mask under `7ffffffd`. Capture the selected reference after restoration and before its first applicable calculation, not merely at UI entry |
| Loaded-event sink `021f0340` -> scheduling `0066f880` / worker `0066fa50` | Prior L003/L004 and P1 p008 identify load-triggered per-reference allocation. Entry alone is insufficient; correlate enqueue, execution, root and result application across threads |
| Allocator `0066b100`; setter `0066abc0` | Prior p007/p008 plus L001 call census. Worker compares old/new sets and sets only differences. Fresh examination of p008's calls at preferred VAs `14066fbd6` and `14066fcd6` confirms clear/set application, not an unconditional rewrite of both extractors |
| Getter `00531b10`, IsPowered wrapper `00c05630` | Extra list reference +`c8`, Extra9C +`18`, mask `40`. A qualified current read does not capture earlier epochs; null/failure is not false power |

This review adds Save29 saved observations and experiment logic, not a new
native lifecycle discovery. The allocation core uses graph/current inputs;
old/new difference application uses the previous powered set. Consequently
changing saved bits might change application behavior: it cannot be assumed
irrelevant to C without validation. The root/order explanation is a separate
question from whether recalculation changes final bits.

## Ranked experiment matrix and player protocol

Rank is by useful discrimination per intervention, with guaranteed separation
conditional on listed coverage and input assumptions. **All are unperformed.**
Common protection: preserve hash-bound original Save3 and Save29 and the evidence
backup; never overwrite them. Any future generated save gets a distinct slot
and archive. Hold build/profile, reference identity, generator output 6, demand
5+5, ordered graph/owner data, activation, crew/modifiers, loading state and
fuel context fixed unless explicitly the variable. Solar has no fuel experiment
here; do not introduce a fueled generator. Record actual effective values,
not just the 6/10 HUD cache. Fresh process means normal desktop exit followed by
loading the designated same hash-bound input; do not kill the game.

| Rank / candidate | Changed variable; controls and observations | Predictions, falsifiers and unresolved outcomes | Stop / effort / risk boundary |
|---|---|---|---|
| 1. Temporal unchanged-load history (T) | No intentional gameplay variable; observe initial restoration, actual allocator results and effective writes for both identified consumers. Uninstrumented three-load result is the historical control; qualify detector on disposable fixtures first | R predicts no superseding applicable result; C predicts applicable computation/application before endpoint. Effective surviving transition falsifies R; complete exclusion falsifies interval C. Matching computation leaves authority equivalent | One complete load is enough for a decisive transition. Stop scientific acquisition at completed endpoint/evidence persistence; gaps mean inconclusive, not retry automatically. Highest relevant evidence, engineering effort medium/high, instrument affects timing |
| 2. Protected-copy saved-bit conflict (P) | Reverse only the two powered bits in an isolated derivative, preserving all other decoded bytes, graph/order, identities and inputs. Original-copy control + independent parser/compression validation, then T on copy | R predicts reversed saved pair survives; independently fixed C prediction must differ. Observed restored reversal followed by allocation correction falsifies R on copy. Survival only falsifies that contrasting C after complete coverage; matching/adaptive C is inconclusive | Separate save-editor/engineering and live briefs. Highest causal separation if validated, highest intervention risk/effort; stop on any unexpected difference, corruption or restoration rejection |
| 3. Legitimate contrasting save / reversible network cycle (G) | Player can propose disconnect/reconnect or generator toggle in a new branch, restoring exactly the original graph before a new slot. Inspect flags/order/effective inputs first; do not assume reversal can be produced | Ordinary gameplay generally changes graph, callbacks and saved bits together. R predicts that branch's saved pair; C may predict the same pair. Admit as decisive only if a separately supported C result differs while relevant inputs are fixed. Otherwise mere repeatability/control | Low tooling, gameplay changes and save generation need new brief. Stop after one verified contrast attempt; no endless toggling. Not recommended as a decisive first trial |
| 4. UI after load, then deliberate refresh | One approved normal in-game trigger after baseline; capture same identities before/after and log intervention time. Keep input differences explicit | A later change proves state can be updated by that action, not that load recomputed. No change fits R and C. Observing a delayed natural transition rejects strict persistence only if attribution/identity is established | Low effort, limited inferential value, gameplay approval required. One trigger/control; no redundant unchanged reload series |

**Smallest player-executable candidate, T:** after separate qualification and
approval, the player starts the approved capture before one normal fresh-process
Save29 load, positively identifies #1 and #2 by selection, and performs no
construction, switching, travel, waiting/sleep, save or console mutation. Inspect
each as soon as UI permits; record monotonic timestamps. Continue normal simulation
for at least ten seconds after the last observed applicable update, then inspect
both again; retain continuous history through that second inspection. The ten
seconds is a prospective observation endpoint, not a proof of engine quiescence
or a hard session deadline. If updates continue, extend the observation interval;
if dependencies remain unresolved, label it unsettled rather than claiming a
final writer. Record operational settled status separately from proof of job
completion. Exit normally after evidence is flushed and observer retired under
the approved card; postflight hashes protect source saves and report incidental
exit saves. A complete, attributable surviving transition is sufficient to stop;
no extra reload count is required. A result for one consumer is not silently
extended to both or to all attach paths.

T requires a newly qualified, narrowly filtered observer: loader-completion/early
reference snapshots; actual load event/queued-job correlation; allocator computed
set; difference-application entry/exit; all effective mask-40 writes and late
writers for these identities through the endpoint. Establish lifetime safety,
coverage of direct/generic stores, event ordering across threads, bounded owned
buffers, lost-event detection, durable flushing, shutdown and protected-input
checks offline before a live brief. Do not claim completeness from the mapped
setter census alone. Hooks or execution breakpoints alter execution and require
explicit disclosure and approval. The external debugger acquisition route was
[abandoned for safety reasons](../event-latency/thread-control-final-report.md);
this plan does not reopen it. Existing position/resource observers capture other
fields and epochs; none of the reviewed P1 evidence qualifies the required
power history. Reusing their transport is not power-observer qualification.
Calling IsPowered after load, or polling memory, cannot exclude an intervening
recalculation or prove a pre-recalculation capture. No observer is built here.

Escalate **only if T is equivalent or incomplete**. Repair an actual coverage gap
within its separately authorized engineering scope before interpreting absence.
If complete T shows matching computation, consider P only when the causal
question warrants save perturbation. Pre-register the differing C result from
qualified graph/current inputs or a bounded matched control, not from a preferred
winner inferred after seeing the copy. Validate that the perturbation is actually
restored and that C's effective operands remain unchanged; selective old-set
application, alternate consumers and reload remapping are confounders. Require
byte-exact decoded comparison outside the two mask bits, valid framing/checksums,
copy/original clear separation, and an explicit no-write-to-original policy.
Never load a hand-edited save merely because it passes a parser. If prediction
independence cannot be established, P is not admitted as a decisive test. No
unconditional proof is promised by either proposal.

## Acceptance and handoff contract

Planning mandatory criteria: accepted player PASS preserved; save availability,
backup/hash and selected powered bits established or precise gaps reported;
independent identity join not invented; R/C/hybrid contrasting predictions,
controls, restart/endpoint, falsifiers, failure/stop conditions and authority
specified; candidates ranked and smallest protocol/escalation stated; narrow
native basis and getter limitations; durable minimal state updates; verified
review patches and independent audit. All executed checks are offline; proposed
live acceptance is NOT TESTED. Raw evidence LOCAL-ONLY; authored interpretation
REVIEW-REQUIRED. See [review ledger](save29-review.md) for actual check limits,
patch manifests and independent disposition. Integration/publication remains
subject to maintainer review. Suggested subject:
`docs(power): record Save29 reload pass and plan causal tests`.
