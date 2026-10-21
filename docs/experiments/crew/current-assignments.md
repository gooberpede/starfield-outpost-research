# Current saved crew assignments: CR1 corrective continuation

2026-10-18. SOR-EXP-0047 / SOR-EV-0055, REVIEW-REQUIRED; primary bytes LOCAL-ONLY.
[Rework authority](../../implementation-briefs/CODEX_BRIEF_SOR_CR1_current_crew_assignment_persistence_rework.md).

**Yes: current saved outpost assignments and a saved unassigned roster are now
recoverable in HIST-0255 (earlier mature Save41), with independent assignment
cross-checks in HIST-0021/22/24.** The qualified subset has ten reciprocal
actor4C/outpostE2 rows, three actor4C targets positively in the saved owned-ship
registry, and Barrett/Sam/Andreja explicitly in the saved available roster.
This resolves the missing real-save assignment boundary, including Lin and Heller.
Full post-load/default/VM coherence and complete crew enumeration remain OPEN.
No assignment history is needed.

## Answer and capability boundary

| Required question | Strongest supported result | Coverage / discriminator still missing |
|---|---|---|
| Individual identity | **Demonstrated from real saves.** Named placed and dynamic ACHR identities; Lin/Heller/Sarah and three available named actors join installed NPC bases. | Generic base26f937 is Crew_LvlCrew_Any; nested templates include Engineering/Security definitions. Exact final display name and template-role selection are not reconstructed. |
| Assigned versus unassigned | **Both demonstrated as saved inputs.** Explicit assignments agree with outpost E2 or owned-ship membership; HIST-0255 positively stores three available actors in the independently bounded registry. | Unassigned means the saved available-roster input to the native UNASSIGNED row path. It does not guarantee final loaded coherence or absence of overriding defaults. |
| Outpost versus ship | **Both demonstrated at saved registry level.** Ordinary outpost beacon 2c60e9 joins differ from targets positively in the restored owned-ship array. | The saved ship reference is unique; effective child/base, displayed ship name and loaded UI category remain **not established**. |
| Unique destination | **Demonstrated from real saves.** Exact dynamic saved destination identity and unique R3 record, rather than proximity/name matching. | IDs are save-local; mutable outpost labels and galaxy/body naming are separate decoration. Sarah's exact target and saved ship-registry membership are recovered; effective loaded classification remains unresolved. |
| Saved authority versus reconstruction | **Native-only mapped in part.** E2 actor identities rebuild fresh handles; 4C mode0 targets become handles. Registry fixup and definition/default paths matter. | The saved lists/links are inputs, not an observed post-load census. General default/Extra80 precedence, disagreements, VM ordering and full restored coherence remain OPEN. |

| Import/research state | Required evidence | Supported output |
|---|---|---|
| ASSIGNED_OUTPOST_RECIPROCAL | Typed actor plus actual4C key/mode/target, unique beacon, reciprocal E2 | Positive current saved assignment for the qualified pair. |
| EXPLICIT_ASSIGNED_ELSEWHERE_KIND_UNRESOLVED | Actual4C relationship and unique saved target; effective destination type unqualified | Retain actor/target IDs and report unresolved destination kind; do not guess a label. |
| ASSIGNED_SHIP_REGISTRY_MEMBER | Actual4C target positively in the independently bounded owned-ship array | Saved ship destination input; effective loaded child/name/category remains open. |
| SAVED_UNASSIGNED_ROSTER | Positive, independently bounded available-roster entries in HIST-0255 | Barrett005788, Sam29d488 and Andreja0059a9, count3; final loaded status NOT TESTED. |
| UNKNOWN | Missing record/key, unsupported prefix/version/extra, unresolved identity, or incomplete enumeration | Preserve unknown; do not emit unassigned/false/empty. |
| DESTINATION_UNRESOLVED | Positive relationship with absent/unresolved target record or effective classification | Preserve relationship and failure domain; do not invent an outpost/ship name. |

Recruitment/availability, current assignment, pending travel, physical presence and
effective contribution remain separate. A reciprocal saved assignment proves none
of the last three. CR2/CR3 are unchanged.

## Corpus selection before acquisition

`.local-work/cr1-current/selection.json` freezes selection from the existing
278-save inventory **before** the new record search. Select every candidate with
header level candidate at least 290, parsed header playtime earlier than Save52's
58d7h43m, and declared decoded size at most 64 MiB. This yields 203 originals,
including rich outpost and ship-location profiles and no-beacon comparison profiles.
Playtime/level are selection strata, not verified gameplay chronology, shared
universe identity or proof of crew. Original filenames, paths, contextual header
locations, hashes and exact selection rationale remain in the local receipts.
[Safe corpus ledger](current-corpus.csv) retains immutable HIST IDs and hashes.

The search closes R3 framing for106 inputs, totalling15,199,099 records. The other
97 fail the existing plugin/header qualification with UNQUALIFIED_SAVE_HEADER_BUILD;
they are untested semantically, not negative crew samples. Across supported inputs,
953 ordinary beacon counted-extra prefixes close;287 explicitly contain E2,
including empty lists. **23 saves contain nonempty beacon E2**;59 selected records
queue the assignment key. These are search leads, not59 qualified assignment rows
or 23 independent controlled repetitions. All 203 originals match before/after hashes.

HIST-0021/22/24 were selected for detailed reads after positive detection. Their
headers describe mature level317/318 profiles, playtimes55d0h24m/55d7h7m/55d14h22m
and player location Starbug. Those labels do not identify each actor's destination.
The native-backed, typed witness reads qualify the actual joins below. Other E2
hits remain leads; unsupported selected records are not silently counted as beacons.

Save52 is a comparison only. The original54 closed beacon extras without E2 in
Save52/HIST-0036/HIST-0077 remain exactly the historical search result in [saves](saves.md).
They do not contradict the earlier mature positives and never qualify an individual
unassigned actor. HIST-0036 actor reinspection also preserves incomplete/default
branches instead of deriving unassignment from missing4C.

## Real saved witnesses and controls

All offsets are **decimal decoded logical-stream offsets**, not original compressed
offsets, runtime addresses or record-relative offsets. Exact source hashes, record
offsets, keyword/target queue byte offsets, mode byte offsets and destination E2
locators are in [current-witnesses.csv](current-witnesses.csv). Raw receipts are
`.local-work/cr1-current/HIST-0021-witness05.json`, `HIST-0022-witness05.json`
and `HIST-0024-witness05.json`; principal `HIST-0255-witness06.json` and
`HIST-0255-registry-boundary01.json`.

| Save / actor | Saved actor/base identity | Current saved assignment | Exact evidence / independent corroboration | Limit |
|---|---|---|---|---|
| HIST-0255 / Lin005639 | Static ACHR005639 → NPC005638 | Outpost ff047885 | Actor4C mode at 9729048; destination E2 at 6919420 lists Lin and Heller among 4 members. | Current saved membership; arrival/effect unknown. |
| HIST-0255 / Heller00563c | Static ACHR00563c → NPC00563a | Same outpost ff047885 | Actor4C mode at 9731318; independently decoded E2 includes Heller. | Base identity corroborated by installed NAME, not inferred from location. |
| HIST-0255 / Sarah005986 | Static ACHR005986 → NPC005983 | Saved owned-ship reference ff02a419 | Actor4C mode at 9750456; unique target positively occurs in the independently bounded owned-ship array. | Effective loaded ship child/base/name remains unqualified. |
| HIST-0021 / ff04e381 | Typed ACHR, dynamic ff04e381; initial NPC26f937; nested Engineering template associations | Outpost ff02a587, ordinary beacon 2c60e9 | Actor record9769132;4C mode0 at 9770766; destination E2 at 4211213 explicitly lists ff04e381. Actor and destination identities come from different records. | Generic template association is not an imported effective perk/name. |
| HIST-0022 / ff05102a | Typed ACHR, initial NPC26f937 | Outpost ff02b720 | Actor11332833;4C mode11334468; E2 at 4632748 contains this actor. | Independent save reproduces grammar, not a controlled intervention. |
| HIST-0024 / ff03f5ac | Typed ACHR, initial NPC26f937; nested Security Chief associations | Outpost ff02e122 | Actor10599609;4C mode10601277; E2 at 4666649 contains both listed actors. | Two members, not two slot-cost observations. |
| HIST-0024 / ff058402 | Typed ACHR, initial NPC26f937; nested Engineering associations | Same outpost ff02e122 | Actor11352510;4C mode11354143; same E2 independently contains ff058402. | No claim of physical arrival or bonus. |
| HIST-0024 / Sarah005986 | Static ACHR005986 → installed NPC005983; NAME original ESM offset 361113343 | Explicitly assigned elsewhere, target ff057a47 | Actor7919769;actual4C CrewAssignment mode0 at 7924285; target record2878750 initial base GBFM0b136e (LvlShip_CrimsonFleet_Combat). | New registry boundary positively classifies this as a saved owned-ship target. Effective child/category and reciprocal ship E2 remain unqualified; not final loaded getter authority. |

The distinct-target Sarah row is a positive assigned-elsewhere control.
HIST-0255 supplies a separate **positive saved unassigned-roster control** below. Empty E2 at HIST-0021 beacon ff01993e, offset 3360850, explicitly
stores count0; the nonempty beacon's count1 and HIST-0024's count2 cross-check count
and queue consumption. Empty membership qualifies that serialized owner list only.
It is not proof that any named actor is unassigned or that every destination is empty.

## Producer, wire, loader, fixup and consumer

Native addresses below are hexadecimal **static VA**, image base140000000,
pinned retail 1.16.244.0 / EXE SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Installed ESM SHA256 remains
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Fresh baseline rehashes verify both and the protected Ghidra database. Exact new
exports/functions and source/tool pins are in [current-sources.csv](current-sources.csv); [function lines](current-functions.csv).

| Stage | Actual representation and location | Consequence |
|---|---|---|
| Assignment writer | Existing1404076b0 removes old owner membership, appends actor handle to destination E2, and writes actor keyed relationship through140ba0d40. Removal140407a10 clears/removes. | A current owner relationship, not an arrival flag or skill grant. |
| Destination serializer | **14051ea30 caseE2**, export005 lines2544 onward. Calls14040a0d0 on +18 count/+20 array to prune unresolved handles, writes compact count with141868770, then140306db0 emits each resolving actor's **FormID through the saved identity encoder**. | Actual writer found. Runtime pointer/capacity/handle words are not the wire schema. Empty E2 and omitted E2 are different states; outer change masks/presence bits control serialization. |
| Actual E2 wire | One extra tagE2, compact count (low 2 bits width, value shifted 2), members consume reference-queue entries; count body occupies bytes even when identities are out of line. | Real count 0/1/2 and reciprocal pairs above; the extra can be on an ordinary beacon. Not every assignment requires a sampled beacon extra. |
| E2 loader | 140521620 caseE2 →140408a50(owner,true) →1404089e0; compact count then140306e40 reads/remaps identity, resolves Actor and obtains a fresh handle, or invalid sentinel. | No call to ordinary capacity admission during this reader. The owner's runtime +28 identity comes from owner context, not a second saved destination field in E2. |
| Actor save/load | Actor private header precedes TESForm flags/common REFR extras. Actual141917e40 reads u32 mask,u32 field,optional u32(mask1),optional byte(mask2),u32,byte **before140b29990**. | Omitting this header caused the earlier false prefixes; correct initial case6 for static changed actors also differs from dynamic case5. |
| Actor explicit4C | Writer14051ea30 case4C delegates linked-reference save; reader140521620→140547c90→140562ef0. Counted key, one mode byte, target consume explicit queued identities. | Witnesses decode CrewAssignment26beac, mode0 and target; no queue-adjacency heuristic makes the claim. Mode1 stores a FormID representation and is not silently treated as mode0. |
| Generic branch | Extra2B has source NPC,15-bit template mask/selected references, created-NPC identity, change mask and nested NPC self. Only **zero nested NPC change mask** is supported in the new aid. | Template identities and created NPC differ from placed/dynamic ACHR identity. Nonzero nested changes fail closed; no universal actor/NPC decoder. |
| Unassigned registry serializer | **14130ce90 is also the actual writer**, not merely a pruning helper as described in the initial CR1 discussion. It copies ship/available handle arrays, prunes unresolved entries in those temporary copies, writes scalar identities and u32-counted identity arrays. Caller14130fba0 enumerates ShipManagementComponent entries. | Does not prove mutation of the original runtime arrays. Real per-entry available-roster locators are now qualified by the independent boundary below; final loaded coherence remains separate. |
| Enclosing registry stream | 141825820 type6→141822570→14130fba0; actual R1 global **unit6** is framed in HIST-0024 at 1438888..1738495 (end exclusive), units24.json. | Actual block boundary now independently identified by the preceding world-component zero terminator and native successor order; interior Player-token search alone remains rejected as proof. |
| Registry loader/fixup | 14130d540 reads scalar identities into +38/+3c and arrays +40/+58. 14130d650, called by1418234e0, resolves/remaps these into runtime ship +8/+10 and available-actor +20/+28 arrays, retaining qualifying resolved types. | The independently qualified HIST-0255 block now supplies three real available actors. Unresolved/pruned entries must not become known unassigned actors. |
| Crew screen reader | Existing14153cfe0 walks restored available handles, owned ship handles and registered Workshop handles;14153d170 uses destination E2.14153e4f0 fills assigned row or UNASSIGNED when no AssignmentInfo was supplied. | UI authority is consumer-specific: destination E2 supplies assigned rows; registry supplies unassigned rows. An optional selected candidate can also have no AssignmentInfo. The label alone is not a global saved-status oracle. |

Actor getter140517d60 can consult Extra80/default context before direct4C;
140547d80 distinguishes raw identity/handle representation. Save restoration and
ordinary assignment are different paths. No inspected reader establishes a universal
repair rule for disagreeing E2/4C/registry/VM state. Therefore retain both saved
relationships and disagreement flags in research rather than choosing a fabricated
single authoritative field. No runtime experiment or reload was performed.

## Validation, failures and remaining work

The final fresh finite verifier records144 PASS (initial narrower run44 PASS); the original CR1 verifier rerun records
95 PASS. Existing inventory/population/framing/streaming regressions record68 PASS;
the corrected text-validation command records7 PASS. These are integrity/format
and scoped join tests, not runtime or whole-corpus semantic validation. Truncation,
wrong type/version, short reference queue and nonzero nested NPC changes fail closed.

Preserved failures: witness01 uses the incomplete common prefix; witness02/03 add
the Actor header but stop on unsupported generic2B; witness04's scoped56 skip missed
the second trailing byte and stops at type00; witness05 corrects it from actual
writer bytes. No rejected interpretation becomes absence. Initial regression
discovery looked in the wrong directory and ran zero text tests (exit5); the correct
research/s1-storage invocation passes7. The old verifier first rejected a hyphenated
run label; rerunning its documented alphanumeric form passes95. All failed receipts
and commands remain local. Earlier CR1 PEX/save failures and reviews are retained.

General component/version coverage, ship child/base resolution,
default/Extra80 effects, complete saved population and post-load disagreement repair
remain OPEN. These do not erase demonstrated outpost assignments. A new player-only
save pair is **not required to prove the positive examples already recovered**. If
future work requires a loaded coherence oracle, the minimal proposal is the same
named actor visibly unassigned, then assigned to a uniquely identified outpost in
two retained original saves; document both Crew rows and destination. Do not execute
this proposal under offline authority. No historical timeline reconstruction follows.


## Independent registry boundary and positive unassigned input

This follow-up completes the in-scope unit6 lead instead of stopping at the first
Player-token pattern. All 106 qualified originals were searched with the native-shaped
registry grammar; only HIST-0255 yielded a nonempty candidate available list. The
initial candidates and rejected Player-token occurrences remain in `registry/` and
`registry-candidates01.json`; candidate uniqueness alone was not accepted.

The qualifying route uses **different data**: fresh PNDT GNAM system/body keys,
ordinary beacons' independently decoded parent tokens, and the owned
saved_world_components.py method. Pinned existing native export
`.local-work/recon/static-exhaustion-38.tsv` (SHA256
`0d36a0eaae58a1709a5f221ed90f7982aa86d7b7c4b87df1a4ab375548f87ee4`)
shows140ad5f20's37-byte world rows and terminal u32 zero. New native004 shows
141822570 calling that writer **immediately before14130fba0**. The unique maximal
run matches all independent beacon parents and installed system/body keys, closes
with zero, and supplies the successor boundary without searching for the Player ID.
This corroborates the scoped boundary, not every earlier unit6 component.

| Save | World rows / independent beacon parents | ShipManagement block, end exclusive | Explicit available count |
|---|---|---|---|
| HIST-0021 | 422 /12 | 1501085..1501131 | 0 |
| HIST-0022 | 450 /13 | 1597697..1597743 | 0 |
| HIST-0024 | 436 /15 | 1629617..1629663 | 0 |
| HIST-0255, principal positive | 563 /17 | 2195684..2195742 | **3 at 2195726** |

Each block begins u32 outer count1, encoded u32 Player identity000014, u16 index0,
then the exact native scalar/u32-counted ship-array/scalar/u32-counted actor-array
sequence. `14186b940→14186bd40` writes saved form tokens as little-endian u32 here,
**not** R3's three-byte queue entries. The scalar fields remain unnamed; do not
mistake the second scalar's outpost value for a proven home-ship field. Every block
has five saved ship identities including 03f7e8; explicit assigned targets independently
join this array. Loader14130d540 and post-load14130d650 map the second array to the
runtime +20/+28 population consumed by14153cfe0 without AssignmentInfo. Ordinary
insertion1404076b0 removes the actor from availability via14130cbf0 before assignment.

HIST-0255 original name is retained locally as Save41, header48d6h19m, level309,
Jemison/The Lodge; SHA256
`635c07a4914c3313bbf12f031523f707183e4757324ce070f361bec0edfe10b4`.
[Positive roster rows](current-roster.csv) give the three exact u32 token offsets:
2195730 Barrett005788 → NPC005787;2195734 Sam Coe29d488 → NPC005999;
2195738 Andreja0059a9 → NPC0059a7. Fresh installed ACHR NAME/NPC EDID reads and actual
saved typed ACHR records independently qualify identity. This is positive roster
membership, not an inference from missing CrewAssignment fields. The other three
whole available arrays explicitly store zero; that qualifies these arrays only,
not absence of all recruited actors or all default/reconstructed state.

The final verifier rereads these four blocks from protected originals, checks world
boundary/count/parent correspondence, all three real actor types, exact roster
entries, Sarah's target in owned ships and rejection of truncated blocks. Its first
expanded run incorrectly required mode0 on an unrelated available actor's non-crew
4C entry; that test assumption was corrected to apply only to CrewAssignment. The
successful144-check run preserves modes on all other keys and makes no loaded-state
claim. New reader branches33/80/1D permit named-actor prefix evidence; unsupported
leading9C and nonzero nested NPC changes remain explicit gaps in the saved census.
