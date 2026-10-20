# Codex research brief — Kreet Research Lab / Save37–39 coordinate sufficiency

**Project:** `D:\Projects\starfield-outpost-research`  
**Task type:** bounded offline scientific research and documentation  
**Status:** proposed for maintainer invocation; this brief authorizes no live-game action  
**Primary objective:** determine whether existing evidence supports a **locally consistent, repeatable planetary geographic address** for ordinary player outposts, without demanding a continuous physical planetary model or exhaustive native equivalence.

## 1. Research question and success standard

There are two user-defined questions:

1. **Local consistency:** Do geographic addresses of nearby outposts change in the direction and approximate magnitude appropriate to their actual relative placement? Use the new Kreet Research Lab control and the existing SOR-002/SOR-003 relationship. Explicitly account for grid quantization, resolution and site versus beacon coordinates.
2. **Cross-game repeatability:** If an equivalent address is supplied in a fresh character/game on the same planet and game-data version, should it identify the same *geographic site or terrain region*? Distinguish a stable geographic address from selection precision in the landing UI and from incidental procedural clutter.

A satisfactory result may be **planetary terrain cell/region plus a qualified local offset**, rather than floating-point latitude/longitude with unsupported decimal precision. Stable geographic location does not imply continuous spherical geometry. A sound scoped ordinary-case result must not be withheld for unsupported hypothetical coordinate frames, hidden character-dependent transforms or other Russell's-teapot alternatives. Conversely, preserve genuine contradictory observations or actual dependencies that affect the two questions.

**Required output:** (a) an explicit derivation/algorithm with input identities, units, conventions, resolution and measured error/uncertainty, tested on held-out examples where possible; **or** (b) the *smallest concrete missing operand, mapping or observed counterexample* that prevents either conclusion. Report separately what is established for local consistency, stable region identity and finer beacon position. Do not end merely with “more runtime context may exist.”

## 2. Frozen source controls and observations

### New controlled Kreet series

Three originals in `Documents\My Games\Starfield\Saves\`:

- **Save37** — baseline at Kreet Research Lab fast-travel marker: `Save37_D6036588M417474696C61204B6972616C79_000205_20261020002316_3_0_4.sfs`.
- **Save38** — player at intended outpost site, before construction: `Save38_D6036588M417474696C61204B6972616C79_000208_20261020003016_3_0_4.sfs`.
- **Save39** — outpost beacon constructed: `Save39_D6036588M417474696C61204B6972616C79_000209_20261020003045_3_0_4.sfs`.

**User observation:** no movement of the player between Save38 and Save39; all nearby-POI scanner screenshots were taken without moving from this position. The beacon was placed **as close to the player as the game permitted**, making the player-to-beacon separation *small by construction*, **not zero or yet measured**. Recover the actual player and beacon positions and preserve the offset; do not substitute player XYZ for beacon XYZ without testing.

Uploaded copies of these same named saves are available in the current conversation, but Codex should obtain the protected originals at the local path above. Back up, hash (SHA-256), seal and inventory all three before analysis; use immutable working copies, preserve original identity, and stop affected operations on hash/disk-integrity failure. Do not edit originals or infer equality between local originals and uploads without hash comparison.

Seven corresponding screenshots (names beginning `20261020112929`, `...12934`, `...12945`, `...12949`, `...12956`, `...13000`, `...13349`; see original image evidence) show the Kreet surface map, the outpost icon and nearby landmarks. Observed scanner distances from the Save38/39 player position include **Kreet Research Lab 471 m**, **Frontier 512 m**, **Pipeline Terminus 499 m**, **Deserted Biotics Lab 694 m**, and **Abandoned Muybridge Pharmaceutical location 879 m**. These are **scanner target distances**, not proven distances to geographic anchor points. The unlabeled surface-map icons should be matched by identity/orientation only where defensible; do not infer precise distances from pixels. Preserve original screenshot files and hashes if locally available; missing image originals should be recorded, not fabricated.

### Independent installed fixed-worldspace reference

A preceding user-requested read-only Codex check identified the Kreet Research Lab exterior site anchor:

- Kreet PNDT `0003F59F` (`KreetPlanetData`), pre-`BDST` `CNAM` entry;
- Exterior WRLD `00325868` (`LC003KreetBase`), linked to LCTN `00028A08` (`KreetWorldSpaceLocation`);
- Stored latitude **+0.4841205327255354 rad** / **+27.738063301°**;
- Stored longitude **−2.2788728782767467 rad** / **−130.569797972°**;
- First double at decoded PNDT payload offset **38856**, compressed ESM record at file offset **1402105313**;
- Disk order **latitude, longitude, worldspace ID** in this fixed-world format.

Treat this as a reported independent reference requiring verification/pinning against the exact installed ESM build before use; record form identities and hashes. It defines the **exterior worldspace/site anchor**, *not* necessarily the laboratory entrance, survey icon, fast-travel marker, or centre of the compound. Avoid a false metric test that equates those positions.

### Reuse prior coordinate controls and accepted/limited models

Start from `docs/position-model/`, `docs/experiments/exact-beacon-planetary-coordinates.md`, `docs/experiments/exact-beacon/`, `docs/experiments/two-outpost-site-anchors-and-beacon-coordinates.md`, `docs/experiments/two-outpost-anchor/`, `docs/experiments/planetary-surface-anchor-semantics.md`, plus relevant native availability, source-world, Workshop membership and frame reports. Recover the **actual existing identifiers, qualified numerical observations, assumptions and exceptions** for SOR-002/SOR-003. Do not silently promote historical candidate data into established evidence or reopen the dormant observer engineering solely because it exists.

## 3. Investigation sequence

1. **Preservation and source reconciliation.** Verify named files, game/reader/ESM versions, byte hashes, screenshot provenance, existing reference pins and prior confidence statuses. Keep a compact evidence ledger. Review existing findings and choose an initially minimal offline method; do not build a new instrumentation framework.
2. **Controlled save reconstruction.** Compare Save37 → Save38 (player relocation) and Save38 → Save39 (beacon construction) with exact ordinary reference identities, parent/body/worldspace/Workshop membership, relevant site angular anchor, terrain grid coordinates and local XYZ/frame operands. Distinguish true saved change from cross-save churn. Report measured player–beacon offset; the “closest allowed” observation is a control, not equality proof.
3. **Fixed versus dynamic site geography.** Compare the Lab's PNDT/WRLD fixed anchor with the Save39 outpost site anchor. Identify whether the values share an established representation/consumer, what geographic granularity each represents and what valid correspondence exists between marker/fast-travel position and anchor. Do not assume a spherical metre-to-degree conversion from real planetary radius; use qualified installed projection/grid conventions if needed.
4. **Local consistency and held-out checks.** Construct the best supported regional/fine coordinate derivation. Assess expected sign, relative direction, cell changes and magnitude/resolution from Save37–39; test against SOR-002/SOR-003 and any other independent fixed-site controls whose identities and frames are demonstrably comparable. Don't fit one arbitrary transform or constant per case; preserve counterexamples, such as previously reported negative-X/source-frame exceptions, where relevant.
5. **Cross-game stability reasoning.** Follow only the specific installed position/region generation inputs needed to determine whether address identity depends on stable planet/game data or a save-specific/character-specific seed/state. Cite positive dependencies and contrary evidence. A lack of evidence for a hypothetical dependency is **not** proof it exists; likewise no fresh-character observation means actual gameplay repeatability is not directly measured. Distinguish mathematical/model-supported repeatability from live verified placement.
6. **Papyrus location API — bounded trace (mandatory).** Independently determine what `Game.GetPlayer().GetCurrentLocation()` resolves to. Trace `Game.GetPlayer()` and the `Actor`/`ObjectReference` inherited `GetCurrentLocation()` native Papyrus registration/implementation (verify exact signature and dispatch in installed game sources/bindings). Identify whether its return is a `Location`/LCTN object, reference/handle, cell, worldspace or numeric geographic coordinate; where possible map lookup, parent-chain semantics, loaded-cell and location priority/exception cases. Contrast at the Lab, Save38 site and new outpost **only if existing evidence actually supports those states**. Determine whether the returned object can help map an outpost to a planet, POI, biome or site, and explicitly state if it supplies **no longitude/latitude**. Do **not** run Papyrus in the live game, compile/deploy a test plugin or mistake the optional name of a Location for a geographic coordinate. Preserve uncertainty if the exact native implementation isn't reachable offline; supply the narrow next trace.
7. **Synthesis.** Give two prominent answers, **Local consistency** and **Cross-game repeatability**, with separately stated precision, evidence/confidence/coverage and the minimal genuinely unresolved piece. Record whether the original “exact continuous coordinates” objective can be replaced by a sufficient geographic-region-and-offset address.

## 4. Scope and permissions

**Permitted:** read-only offline examination of installed ESM/scripts, existing native Ghidra/source pins, protected save copies, prior documentation and screenshots; non-destructive local analysis scripts/receipts; new scoped report, plan, matrices and review documentation; in-scope verification/corrections. Use existing tools and prior accepted methods when possible. Native analysis is permitted *only to resolve the bounded coordinate dependencies or Papyrus method above*.

**Not permitted:** Starfield launch, debugger attachment, retail memory instrumentation, SFSE/observer build or deployment, live Papyrus invocation, new manual saves, modifying any protected `.sfs`/ESM/BA2/source evidence, general terrain/biome procedural generation reconstruction, speculative exhaustive alternate-frame search, source repository cleanup, changing historical verdicts, license/publication changes, Git add/commit/push or external publication. No biome identification obligation here; capture any specific actionable shared prerequisite for later work.

If a genuinely discriminating live test is needed, deliver the smallest proposed run card and request separate authorization. An observed inability to reconstruct a *fine* continuous offset does not negate an already validated stable **region** address.

## 5. Durable deliverables

Place a concise answer-first report and accompanying focused artifacts under a sensibly named `docs/experiments/` coordinate-sufficiency folder (choose a nonconflicting path, document it). Suggested artifacts:

- `report.md`: two user questions answered directly, derived formula/address or exact blocker; assumptions and counterexamples clearly separated.
- `plan.md`: frozen inputs, controls, competing concrete hypotheses, source/permission guards, stop/escalation conditions.
- `saves.md` / numerical matrix: Save37–39 identities/fields/offsets, SOR-002/SOR-003 control results, error/resolution and held-out outcomes.
- `fixed-poi.md`: Kreet Research Lab anchor verification and relation to physical map/marker.
- `papyrus-current-location.md`: registration, signatures, native call graph, actual return type/semantics, supported uses and limits.
- `evidence.md` or structured ledger: source pins, hashes, tool versions, screenshot mapping, citations and reproducible offline commands.
- `review.md`: all frozen criteria with evidence pointers, independent-review disposition, tests, defects and corrections.

Update only *appropriate new audit/index/backlog cross-references* as necessary; do not retrospectively revise historical evidence or alter accepted status without separate approval. Source and save/native binary extracts remain LOCAL-ONLY; new authored summaries remain REVIEW-REQUIRED pending maintainer review and rights assessment.

## 6. Frozen completion contract / mandatory acceptance

**Task:** bounded discovery/research and documentation; successful negative scoped findings are valid research, while missing required analysis/tests or an unexamined promising in-scope path are not completion.

| ID | Mandatory observable outcome |
|---|---|
| AC1 | Exact Save37/38/39 and screenshots inventoried, originals protected, hashes/source-build and tool version recorded; provenance and deviations explicit. |
| AC2 | Distinct pre/post beacon and player-location controls reconstructed where supported; authoritative membership/identity, player–beacon displacement and site/frame associations traced with stated coverage; no unsupported substitution of player for beacon. |
| AC3 | Lab fixed-worldspace angular anchor independently verified and compared to dynamic outpost site anchor without conflating fixed anchor, POI marker or entrance. |
| AC4 | Best possible **locally consistent geographic address** is explicitly derived and tested against the new case and existing SOR-002/SOR-003 controls, with resolution, meaningful quantitative comparison, actual counterexamples and no case-specific fitting; or a precise evidenced blocker and bounded tests of plausible alternatives. |
| AC5 | Cross-game stability assessed against actual data dependencies; separately classify supported stable region/address versus unmeasured fresh-character recreation and practical landing reproducibility. No speculative universal-proof gate. |
| AC6 | `Game.GetPlayer().GetCurrentLocation()` API traced through available installed Papyrus/native evidence, with exact return category, registration/data flow where attainable, location semantics, whether any geographic coordinates are supplied, and explicit uncertainty/next decisive step if incomplete. |
| AC7 | Answer-first synthesis, auditable numerical/evidence/source registers, scoped conclusion status and minimal remaining dependency; preserve existing findings, scientific counters and the non-continuity premise. |
| AC8 | Full qualified verification and independent reviewer against this original contract; eight-row PASS/FAIL/NOT TESTED matrix, failed cases and fixes preserved, protected hashes and guards checked, status/untracked inclusion manifest, checked links/prose, exact task-only and complete forward/reverse reconstructible patches; no Git staging/commit/push. |

**Negative-result closure:** an evidenced bounded counterexample or precise indispensable missing input may satisfy a scientific negative conclusion without implying universal impossibility. The reviewer must challenge any “unknown” that substitutes for an authorized, promising and unperformed test. Do not extend acceptance criteria mid-run to demand exhaustive hypotheticals; material changes need maintainer approval.

**Continuation authority:** implementer diagnoses and corrects in-scope faults, rechecks evidence and regressions, and resubmits to independent review without requesting another brief for ordinary REWORK. Do not attempt prohibited live actions as “continuation.”

**Exit and escalation:** stop the affected operation for changed protected input, insufficient disk integrity/free-space, inaccessible indispensable local save/ESM after documented searches, unavailable required data for a mandatory result, or missing live authorization; preserve receipts and an exact resume checkpoint. Follow repository `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/templates/completion-contract.md` and applicable safety/rights policies. Preserve both-drive free-space guards and STOP controls. Healthy offline research has no arbitrary time/volume deadline; unjustified tooling sprawl is not a substitute for a causal answer.

**Independent review:** ACCEPT/REWORK/ESCALATE as defined by protocol. Reviewer must independently inspect actual primary evidence and falsifiers, not simply accept implementer's summary; no reviewer self-approval of its edits. Report scientific confidence, method integrity, input preservation, review status and publication eligibility separately.

**Return format:** concise findings and specific uncertainties, complete/task-only diff paths, evidence and verification receipts, independent review decision, commit suggestion. Do **not** stage, commit, push or publish.
