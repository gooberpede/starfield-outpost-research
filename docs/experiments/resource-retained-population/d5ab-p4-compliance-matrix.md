# P4 audit of the unchanged D5AB contract

2026-11-01, Australia/Sydney. All five AB questions COMPLETE and all twelve
AB criteria PASS for offline readiness. Independent Review02 ACCEPT is recorded in [review](d5ab-p4-review.md). D5R OPEN; B1 PARTIAL NATIVE
COVERAGE; historical D5AA gap unresolved; B2 NOT AUTHORIZED.

The [original brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_observer_remediation_live_readiness.md)
retains the full normative requirements. These summaries neither amend them nor
upgrade historical handoff verdicts. All results concern offline readiness.

## Evidence key and applicability

Paths below are repository-relative, usually ignored/local. `V` means bytes and
source identities checked in P4; `R` means earlier execution receipts revalidated
for unchanged inputs; `N` means new P4 execution. No `R` result is described as
rerun. The [manifest](d5ab-p4-package-manifest.md) binds exact final versions.

| Key | Primary evidence and scope |
|---|---|
| P | `.local-work/d5ab/p4-provenance01/receipt.json`; V. Twenty-one Final04 build inputs, compiled outputs, identical Repro02 DLL, fifteen suite receipts, seventeen P1 exports and 826 historical preservation records. |
| L | [P1 L01-L21 matrix](d5ab-p1-source-identity-lifetime.md), exact primary export locators in [sources](d5ab-p1-sources.csv); V/R. Constructor-private initialized semantic scalars, full ordinary alias/owner graph and fences; no post-selection observer dereference or raw-padding identity. |
| N | `.local-work/d5ab/p3-native-controls-final02/receipt.json`; R, 257 checks over Final04's compiled native hosts. Corresponding `p3-positive-no-bypass`, `p3-positive-bypass`, `p3-skipped-store`, `p3-store-access-fault`, `p3-competing-map`, `p3-real-reuse`, `p3-detached-retirement` and owner/reset cases under `.local-work/d5x/p3-native-final04/`. |
| A | `.local-work/d5ab/p3-bridge-abi03/receipt.json`; R, thirteen exact-object checks. `.local-work/d5ab/p3-original-instructions01/receipt.json`; R, eleven original-instruction controls. Final04/Repro02 include 226 actual `RtlVirtualUnwind` contexts. |
| C | `.local-work/d5ab/p3-reader-final02/receipt.json`; R, 133 consumer checks. `.local-work/d5ab/p3-reader-legacy-final02/receipt.json`; R, 316 checks including historical schema-2/3 equality; `.local-work/d5ab/p3-legacy-semantics02/receipt.json`, 54 explicit semantic controls. |
| T | `.local-work/d5ab/p3-capacity-final02/receipt.json`, nine complete-producer combinations; `.local-work/d5ab/p3-queue01/receipt.json`, nine compiled queue runs; `.local-work/d5ab/p3-transport-audit02/receipt.json`, 88 sessions. V/R. |
| W | `.local-work/d5ab/p3-controller-final02/receipt.json`, 26 actual-worker cases; sharing control `.local-work/d5ab/p3-sharing-final02/receipt.json`. R. P4 adds the separately pinned retail adapter; P2 remains disposable-only. |
| O | `.local-work/d5ab/p4-controller-final03/receipt.json`, `p4-admission-final04/receipt.json` and `p4-procedures-final03/receipt.json` below the same local receipt root; N. Exact hashes in [manifest](d5ab-p4-package-manifest.md). Includes actual-worker controls, synthetic retail validation, lightweight protection and native-capture archive reconstruction. |
| F | `.local-work/d5p/d5ab-p4-offline-pre01/protection.json` and `.local-work/d5ab/p4-full-preflight04/receipt.json`; N. Final Accounting02 verifies equality and final correspondence. Full protected input/backup/restoration-copy procedures; never a live GO. |

Native hosts execute the actual DLL, bridges, recorder and controlled original
instruction excerpts. Their provider/map/generator/geometry/allocator policy is
host code. Static engine evidence supplies the corresponding pinned native
contracts. Empty/partial host output distinguishes geometry from a sample/store;
it is not execution of the complete retail generator.

## Five original questions

| Question / original requirement | Code or native boundary; positive evidence | Adverse control and uncertainty | Current result / independent gate |
|---|---|---|---|
| AB-Q1: safe positive source identity including visited bypass | `observer.h` birth/selected/visited captures, `reduce_v4.py` identity joins; L/N/A/P. Actual initialized birth/publication and positive same-allocation bypass. | N detached retirement, actual ABA, token collision, unknown birth/publication; C missing/late/tied events. Ordinary pinned graph only, not arbitrary corruption or a native source lease. | COMPLETE within offline readiness; independent Review02 ACCEPT. |
| AB-Q2: distinguish every visited transition through actual store | `bridges.asm` reserve/store; preferred static token-store VA `0x14079ff60` and publication-store VA `0x14098317e` (hook windows begin at `0x14079ff59` and `0x140983177`); N/A/P. Actual MOV precedes Stored callback; destination/token memory independently checked. | Native failure sentinel `0xffffffff`, reserve throw, skipped store, access fault before callback, retirement/reset interruption. A reserve or later bypass is never a substitute for the store. | COMPLETE within offline readiness; independent Review02 ACCEPT. |
| AB-Q3: reliable required-category transport with safeguards | `transport.cpp`, measured 32,768-cell candidate; T/W/O. Representative 21,061 and burst 12,018 actual producer records retained with zero loss; all seventeen categories. | Smaller capacities, hot retry overload, delayed publication, writer/ACK/worker/disk faults. Finite envelopes only; sampled telemetry can be inconsistent and must refuse qualification. | COMPLETE within offline readiness; independent Review02 ACCEPT. |
| AB-Q4: defensible chronology or explicit refusal | Versioned reader/reducer; N/C/P. First construction with or without later bypass, separately verified subsequent bypass and reset-scoped recovery. | Missing/duplicate/cross-thread/tied/late boundaries, wrong owner/query/epoch, loss and contradictory counters. Queue admission and operator checkpoints do not establish native causality. | COMPLETE within offline readiness; independent Review02 ACCEPT. |
| AB-Q5: identity-bound independently reviewed B2 readiness | P/O/F plus frozen package/plan and [B2 card](run-card-d5x-b2.md). Exactly one proposed process/load/direct travel. | Current retail loader/admission/target occurrence untested; no promise of a new target birth or mask. Full fresh preflight and separate maintainer GO still required later. | COMPLETE within offline readiness; independent Review02 ACCEPT. |

## Twelve original acceptance criteria

| Criterion / original requirement | Final-candidate evidence and actually executed layer | Decisive positive / adverse controls; residual coverage | Current PASS / FAIL / NOT TESTED; review disposition |
|---|---|---|---|
| AB-AC01: policies, pins, inputs, permission boundaries | P/F; P4 baseline `.local-work/d5ab/p4/baseline.json`, governing brief and active ledger. | Actual exact hashes and offline writes; no retail/deployment/save-original/Git integration action. Historical missing refusal transcripts remain UNKNOWN. | PASS for recorded current scope; independent Review02 ACCEPT. |
| AB-AC02: unchanged five questions, active ledger, D5R OPEN | [Active P4 ledger](d5ab-p4-investigation-ledger.md) and original AB ledger/brief. | Ledger created before implementation and updated as failures/corrections arose. No narrower parent question. | PASS; independent Review02 ACCEPT. |
| AB-AC03: positive visited-bypass identity and native lifetime | L/N/A/C/P; private birth semantic definition, publication, full prefix/native order and equal producer epoch. | Positive bypass; inaccessible selected source at lookup, detached retirement, ABA/collision/alias and missing witnesses refuse false identity. Native graph coverage is scoped, not universal. | PASS intrinsic offline evidence; independent Review02 ACCEPT. |
| AB-AC04: real successful append versus attempt/failure | N/A/C/P; actual reserve return and executed token-store bridge; independent host memory oracle. | Positive store, sentinel, exception, skip, inaccessible destination, wrong token/count/source/epoch and native-order counterexamples. | PASS intrinsic offline evidence; independent Review02 ACCEPT. |
| AB-AC05: full essential event/lifecycle visibility | L/N/C/P; eighteen guarded sites, seventeen unfiltered categories; static original-query-to-consumed-sample def-use. | Non-target events/global resets retained. Missing sample/prerequisites, empty/partial output, retirement/owner replacement and lost fences refuse overclaims. Native loading/visual-arrival instants are not newly instrumented. | PASS at original offline mechanism scope; independent Review02 ACCEPT. |
| AB-AC06: measured queue/writer comparisons and safeguards | T/W/O; compiled 1,024/8,192/32,768 capacities, real phase/high-water/working-set measurements. | Zero drops in declared candidate lossless envelopes; deliberate hot/capacity overload counted. Durable admitted bytes remain distinct from coherent telemetry/native completeness. | PASS for exact complete operational bundle and finite envelopes; independent Review02 ACCEPT. |
| AB-AC07: concurrency/fault/wrap/STOP/lifetime tests | N/A/C/T/W/O; independent host state/operand/sequence oracles. | Real exceptions/unwind, same-address reallocation, competing map, worker death/stall, stale/foreign STOP, delayed ACK, raw/ACK faults. Synthetic schedules are labeled separately. | PASS: final 28 controls and independent four-case isolated dry run; independent Review02 ACCEPT. |
| AB-AC08: versioned schema/reducer and original counterexamples | C/N/P; exact schema-4 producer/consumer; original schema-2 B1 and schema-3 comparisons unchanged. | Positive first chain without mandatory bypass; malformed/omitted/damaged/lost histories refuse; conditional partial evidence survives. Actual overloaded flush tuple preserved. | PASS intrinsic offline evidence; independent Review02 ACCEPT. |
| AB-AC09: reviewed card and protected identity-bound operations | O/F plus [card](run-card-d5x-b2.md), hash-bound preflight/admission/control/postflight/archive. | Independent backups/restoration COPY, both caller-available disk floors, emergency STOP, ownership and partial archival; no quota or implicit live authority. | PASS: final plan-bound rehearsal and protected equality, independent operational controls and card challenge; independent Review02 ACCEPT. |
| AB-AC10: accurate docs/preservation/checklist/manifests | P/F and final delivery inclusion/exclusion inventory. | Historical B1/D5AA/checklist unchanged; binaries/native/private/raw excluded from Git. Owned source and existing approved SFSE notice basis only. | PASS; independent exact inclusion/exclusion/delivery verification accepted. |
| AB-AC11: independent full engineering/scientific-readiness challenge | [Review](d5ab-p4-review.md), actual independent return and exact file hashes. | Reviewer reads source/native/primary failures and challenges all original questions/criteria and operational counterexamples. Specialist cannot accept its implementation. | PASS; independent Review02 ACCEPT. |
| AB-AC12: full exact-final editorial review and verified diffs | Final screen/manual inventory, independent prose review, complete/task-only patches and forward/reverse exact-byte checks. | Supplied brief separate from task-authored paths; untracked text included without staging. Later substantive changes require delta review. | PASS; exact-final prose, screen/manual coverage and both patches independently accepted; closing metadata delta verified. |

## Telemetry anomaly and claim limits

The actual overloaded Final04 `stop-under-production/flush.jsonl` line three
has incompatible sampled generation/cause totals. T authenticates 65,553 frames
and the durable ACK prefixes while C reports
`LOSS_TELEMETRY_INCOMPLETE_OR_CONTRADICTORY` and refuses whole-session and
reset-scoped scientific qualification. The retained challenge ACK itself is
coherent at one flushed record; metadata-only health cannot detect a contradiction
confined to another flush record. P4 tests the exact inconsistent tuple through
controlled current-worker telemetry and preserves that distinction.

Confidence in scoped native/offline witness logic is high; coverage is not retail
behavior, universal zero loss, source frequency, complete generated geometry or
save persistence. Streaming archival is qualified. The reader materializes raw
bytes/events; universal reduction memory bounds are not claimed. A resource
failure retains original evidence and a partial result rather than a false PASS.
