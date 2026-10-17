# Codex implementation brief — P1 Save29 controlled save derivatives and preregistered loading tests

**Project:** `starfield-outpost-research`  
**Type:** Bounded offline save-writer feasibility, preparation, independent audit and manual-test planning  
**Authority:** Offline only. No Starfield launch, loading edited saves, runtime instrumentation, original-save edits, staging, commit or push. No automatic installation of generated files into the game's active Saves directory.

## 1. Objective and agreed sequence

Prepare a rigorously controlled, escalating test of whether Starfield restores saved per-extractor powered flags unchanged or corrects/recomputes them after load. The project has already **accepted as PASS** three fresh-process reloads of unmodified Kreet Save29: extractor #1 powered, extractor #2 unpowered, with 6 power supplied and 10 required. Do not reopen that acceptance decision or introduce retrospective criteria.

Prepare, **independently from the same original Save29**, these derivatives, in order:

1. **C — Unchanged repacked control:** identical decoded save content; exercises the writer/container round trip.
2. **R — Reversed allocation:** extractor #1 off, extractor #2 on; validates acceptance of a non-original but nominally feasible powered pair and yields a preliminary behavioural observation.
3. **O — Overpowered allocation:** extractor #1 on, extractor #2 on; deliberately contradicts the 6/10 power budget and tests whether that invalid state survives. Do not add a both-off variant unless a later decision authorizes it.

The *live* gate is sequential: C must load successfully before R; R must load successfully before O. **This brief does not authorize any of those launches or loads.** The intention is to review the produced artifacts and test card first.

## 2. Required baseline and identification

Read `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, the P1 report/review suite, particularly `docs/experiments/power/save29-test-plan.md`, `save29-review.md`, `load-determinism.md`, `saved.md` and `followup.md` where available. Reuse the project-owned strict BCPS/decoded-stream readers and established evidence/version pins; check the actual installed versions, paths and input hashes before use. Do not invent missing writers or presume repacking is possible.

Original input: `Documents/My Games/Starfield/Saves/Save29_D6036588M417474696C61204B6972616C79_000216_20261017043132_3_0_4.sfs` (resolve the actual user-profile path; never search indiscriminately for similar names). Previously recorded SHA-256: `ab28c98940b019320cda4d6a0db54c9d88b721a18fba4c6a701fbed0966b42fe`; size 2,085,680 bytes. Abort on unexpected hash/size until reconciled. Preserve Save3, original Save29 and the existing protected backup.

Saved reference identities (not stable live RefIDs):

| Object | Saved identity | Baseline Extra9C powered bit `0x40` | Saved position / console precision |
|---|---|---|---|
| Solar array | `ff022841` | set | Verify existing report |
| Extractor #1 | `ff022917` | set | `(105.26, 282.59, 16.82)` |
| Extractor #2 | `ff02294d` | clear | `(87.36, 269.61, 14.89)` |

The previous join used user-reported console XYZ and distinct saved positions; live RefIDs changed across sessions. Identify derivatives by **saved record/position**, never historical transient live IDs or inferred powered state. The existing report gives decoded-stream Extra9C locations `1300659..1300664` for #1 and `1301324..1301329` for #2 (decimal, half-open); rederive and verify record boundaries and `0x40` mask before writing. Expected original Extra9C words `0x840` / `0x800` for #1/#2.

## 3. Implementation and scope controls

First assess writer feasibility and container format using existing owned code and recorded sources. If a valid Starfield `.sfs` cannot be safely emitted, **stop with a documented NO-GO** and smallest specific missing prerequisite; do not improvise a format, bypass safeguards or present parser acceptance as game acceptance.

If feasible, implement the minimum **local-only** reproducible writer/validator for these three derivatives. Reuse project components where possible; any new tool must be narrowly scoped, documented and tested. Work on exclusive protected copies or disposable scratch only. Never modify original saves, raw references, game installation or repository Git state. Use distinct non-colliding filenames and a manifest linking every artifact to the baseline hash and its intended two-bit state. Keep generated `.sfs`, decoded binary streams and raw evidence under ignored `.local-work/` only; do not include proprietary binary payloads in textual diffs or commit proposals.

For C require decoded-stream byte-for-byte equality with original. For R and O require **byte equality in the decoded stream outside precisely the designated `0x40` mask positions**; prove the full decoded delta with an independent comparison and verify the intended bits. Preserve all other bits in each Extra9C word, including flags and reference metadata. Each derivative must originate independently from the verified original, not by successive mutation of another derivative.

Validate full BCPS framing, compression/decompression, lengths, integrity fields/checksums if any, save metadata and record/extra boundaries with an independent read-back wherever practical. Prove each derivative can be decoded by the project's strict reader and yields identical non-target entities, graph, ownership, generation/demand inputs and saved settings. Where decoder coverage is incomplete, state the exact blind spots and their consequence; do not claim universal equivalence merely from selected rows. A successful offline decode is **not** proof the retail game accepts the save.

## 4. Preregistered player test card (documentation only)

Produce a short, readable procedure to be reviewed and separately approved before any live test. Require explicit file backup, original-hash confirmation, controlled delivery of one derivative at a time, distinct in-game identification, and a recovery/removal procedure for test saves. Prefer an isolated save location or documented copy-and-restore process; never suggest overwriting Save29. Explain any filename/menu indexing issue and how the player unambiguously selects the intended derivative. No manipulation of the live game from this assignment.

Fixed context: same game executable/profile/mod configuration; one solar array 6 power; two small Iron extractors 5 each; no intentional topology, crew, generator or activation changes. Record whether the file is accepted, any error/corruption warning, whether the intended Kreet outpost and both distinct extractors appear, effective supply/demand, and each extractor's power indicator **immediately after load and again after several seconds**. Exit normally to desktop between trials. Associate live objects by position/scene identification rather than assuming unchanged RefIDs. Retain screenshots/transcriptions and timestamps as available. Do not redefine the accepted historical Save29 result.

Freeze the interpretation matrix **before live tests**:

| Stage | Observation | Permissible inference |
|---|---|---|
| C | Repacked unchanged save rejected | Writer/container or deployment not validated; **STOP**. Cannot blame changed power bits. |
| C | Accepted and baseline Kreet state appears | Writer round-trip demonstrated in this game/profile, not proof that the game processed every field as intended. Continue to R under separate live approval. |
| R | Rejected after C passes | Modified-state handling or edit integrity unresolved; **STOP**, do not proceed to O until investigated. |
| R | #1 off, #2 on | Reversed pair survives to observation endpoint; consistent with restoration, but not proof no recalculation occurred. |
| R | #1 on, #2 off | Reversal did not survive; consistent with recalculation or another load-time correction, but does not identify its writer. |
| R | Both on, both off or unstable | Different behaviour: document without forcing binary restoration/recalculation interpretation. |
| O | Rejected after C/R accepted | Could reflect power-state validation or another edit-specific failure; without further evidence **cannot uniquely attribute** rejection to invalid budget. |
| O | Both powered persist with verified 6/10 and matched objects | Invalid saved state survives through observation endpoint; strongly supports absent effective power-budget correction on that load/path. |
| O | Exactly one powered | Invalid state corrected or superseded; consistent with effective budget enforcement; not proof a particular allocator was invoked. |
| O | Both off, state changes over time or unclear supply/demand | Supersession/instability or invalid control; record specifics and avoid a definitive causal claim. |

Jointly interpret R and O results (including acceptance) after both, rather than interpreting R as a conclusive causal test in isolation. Distinguish **game acceptance**, **restoration of exact edited flags**, **settled visual state**, and **attribution to a native recalculation**. Neither C nor R alone proves later O is valid. No retroactive acceptance changes after observing outcomes. Provide explicit stopping conditions for invalid configuration, save-file damage, inconsistent identities, unexpected changes, or ambiguous UI.

## 5. Independent review, receipts and delivery

Deliver:

1. Brief **GO / NO-GO** feasibility finding in plain English, plus exact writer provenance and serialization assumptions.
2. Three offline derivative saves if feasible, with manifest, SHA-256 values, decoded-delta comparison and distinct labels; otherwise explicit blockers and no fabricated files.
3. A compact player-facing test card with preregistered decision matrix, file-install/cleanup safeguards and sequential approval gates. **Do not execute it.**
4. Minimal durable P1 documentation for method and state, without treating proposed outcomes as findings; update `docs/RESEARCH_STATE.md` / backlog only if appropriate, preserving accepted earlier reports.
5. Focused deterministic tests, independent decode/read-back and zero unintended-delta audit, protected original hashes, plus standard prose/encoding/link checks and version pins.
6. Independent reviewer per `WORKFLOW.md`, explicitly checking mask/offset provenance, original immutability, container legitimacy, scope, test discrimination and honesty of outcome claims.
7. Task-only and complete text diffs (covering new non-ignored tracked/untracked documents), exact forward/reverse application checks, local audit/manifest/independent-review receipts, and a suggested Conventional Commit subject. No binary saves in diffs.

**Authority boundary:** The implementer may develop and validate local offline derivatives, but must **not** copy them into the game's active Saves directory, run Starfield, deploy instrumentation, produce new in-game saves, change original Save29, stage, commit or push. Any subsequent live gameplay/testing requires a separate explicit decision after the reviewed package is available.

## 6. Acceptance criterion

This assignment passes only when the output either (a) provides three verifiably controlled, independently derived `.sfs` candidates and a predeclared safe sequential live-test procedure, or (b) clearly establishes a specific blocker with no misleading claim of readiness. The scientific objective of identifying restoration versus recalculation remains **NOT TESTED** until a separately authorized player experiment; a fully successful writer qualification does not itself settle that question.
