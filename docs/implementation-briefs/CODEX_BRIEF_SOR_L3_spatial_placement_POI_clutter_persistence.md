# Codex research brief — L3: Outpost spatial placement, POI clipping and environmental suppression

**Project:** `starfield-outpost-research`  
**Task:** Bounded offline native/definition/script/UI/save investigation grounded in six new Kreet saves and eleven user screenshots; independent critical review  
**Authority:** Read-only inspection and authored research artifacts. No Starfield launch, new gameplay/save creation, original-save modification, debugger attachment, observer engineering/deployment, staging, commit, push or external publication. A future live experiment requires separate approval.

## 1. Purpose and success condition

Explain how Starfield decides whether an **outpost beacon** or an **ordinary constructed object** can be placed at a proposed position, with particular attention to (a) a valid outpost intersecting a POI exclusion zone, (b) actor and static-object obstruction, and (c) environmental clutter that stops obstructing placement when the candidate is moved deeper into it. Determine which mechanisms persist, which are dynamically recomputed and what could cause suppressed clutter to reappear after leaving and returning.

**An actual causal placement decision matters more than a list of collision or geometry functions.** Trace proposed position/footprint and relevant world/site inputs through validation predicates, classification and precedence, acceptance/rejection and UI error messages. Native-only conclusions must remain distinguishable from directly witnessed screenshots and saved-state observations. The study need not recreate arbitrary terrain, physics or the renderer.

Preserve L1 numerical/environmental admissibility and L2 build-budget findings without reopening them. Earlier position, Workshop ownership, PNDT/resource-region and construction-root reports are reusable inputs, not automatically proven spatial equivalents.

## 2. Freeze and protect the new Kreet evidence first

The following are **six distinct primary save originals**, presently in `Documents/My Games/Starfield/Saves/`. Resolve the actual user-profile path, identify by the entire filename, and **back up, hash and seal before decoding**. Do not assume the filenames' dates prove chronology or that the three saves differ solely by one object.

| Scenario | State | Exact file |
|---|---|---|
| POI | Baseline, no outpost | `Save30_D6036588M417474696C61204B6972616C79_000218_20261019021923_3_0_4.sfs` |
| POI | Beacon only | `Save31_D6036588M417474696C61204B6972616C79_000220_20261019022207_3_0_4.sfs` |
| POI | Beacon + solar power + Iron extractor | `Save33_D6036588M417474696C61204B6972616C79_000221_20261019022719_3_0_4.sfs` |
| Clutter | Baseline, no outpost | `Save34_D6036588M417474696C61204B6972616C79_000215_20261019023113_3_0_4.sfs` |
| Clutter | Beacon only | `Save35_D6036588M417474696C61204B6972616C79_000216_20261019023148_3_0_4.sfs` |
| Clutter | Beacon + solar power + Iron extractor | `Save36_D6036588M417474696C61204B6972616C79_000218_20261019023339_3_0_4.sfs` |

**There is intentionally no Save32**: the player accidentally duplicated Save31 and deleted that redundant save. Do not report missing evidence or try to reconstruct it.

Eleven user-supplied screenshots are the visual witness set; locate originals in the project/operator-accessible evidence location, preserve names, sizes and SHA-256, and copy exclusively to protected/ignored evidence storage if available. If they are *not* accessible locally, report the exact missing inputs and continue independent save/native research; never pretend to have read the screenshot bytes. Filename inventory:

- `identified-poi.jpg` — scanner identifies **Abandoned Industrial Compound** (displayed distance approximately 203 m); location context, not proof of exclusion radius.
- `poi-beacon-inside-exclusion-zone.jpg` — attempted beacon placement rejected, **“Intersects with an existing object”**.
- `poi-clipped-outpost-boundary.jpg`, `poi-clipped-outpost-boundary-above.jpg` — visually clipped build territory, pale yellow boundary very near beacon on POI-facing side.
- `poi-solar-array-inside-exclusion-zone.jpg` — solar placement rejected, **“Area is restricted”**.
- `poi-solar-array-outside-exclusion-zone.jpg` — nearby accepted construction position/control.
- `environmental-clutter-beacon-static-intersection.jpg`, `environmental-clutter-beacon-override.jpg` — obstructing scenery versus accepted/preview-cleared deeper overlap.
- `environmental-clutter-solar-array-static-intersection.jpg`, `environmental-clutter-solar-array-override.jpg` — **“Intersects with an existing object”** at marginal overlap versus permissive deeper overlap, where the large rock fades/disappears.
- `environmental-clutter-extractor-dynamic-intersection.jpg` — attempted extractor placement intersects an animal actor and is rejected.

**Important visual nuance:** The outpost boundary is faint; the unusually short distance from the beacon to the POI-facing boundary demonstrates clipping qualitatively, not a measured radius or polygon. Screenshots document transient placement results; a rejected preview need not have any save representation. Do not manufacture a saved rejected object or promote previewed objects to constructed references.

For each save, preserve pre/post original hashes, immutable protected copy, BCPS framing/build identity, decoded-stream hashes, tool/version/provenance, actual record evidence and an explicit errors/unsupported-representations ledger. Do not overwrite older control saves or mix this corpus with an unrelated Kreet Save3 outpost. Maintain C:/D: 40,000,000,000-byte free-space guards for applicable operations.

## 3. A — POI territory restriction and construction boundary

Investigate separately:

1. **Beacon admission:** Identify the authoritative engine, script or site-validation gates rejecting a proposed beacon inside an established POI/location exclusion. Determine the actual excluded-location data (location, encounter/site bounds, volumes, keywords, radii or other structure) consumed by the check. Distinguish *“Intersects with an existing object”* from territorial restriction rather than assuming both labels identify one predicate.
2. **Territory geometry:** Establish where the nominal outpost build radius originates (the user refers to approximately **150 units**, to be verified), how the buildable territory is represented, and whether POI intersection produces persistent clipping geometry or a dynamically tested excluded region. Reconstruct the overlap decision qualitatively and quantitatively only when the necessary operands are available.
3. **Ordinary placement inside a clipped outpost:** Trace why a valid constructed solar candidate is admitted on one side and rejected with *“Area is restricted”* on the other. Distinguish beacon admission, outpost ownership/range, restricted-site checks and UI rendering of the boundary; determine priority/short-circuiting between rules where supported.
4. **Save correspondence:** Link Save30/31/33 beacon and Workshop position/site data and constructed-object membership to the native placement model. Explicit saved clipping records are not required if the engine recomputes restrictions from world definitions and saved positions.

Use the identified Abandoned Industrial Compound on Kreet as the concrete POI case, but do not presume its visible map-marker distance equals the exclusion radius.

## 4. B — Collision, environmental suppression and restoration

Trace candidate footprint/orientation/bounds, placement physics/overlap query, hit classification and filtering, suppression or disable requests, and final admission to explain the observed apparent **non-monotonic overlap**: marginal intersection fails, yet deeper overlap with some environmental scenery can succeed as that scenery disappears/fades. Verify whether this is genuinely a special suppressible-object rule versus separate hit geometry, collision layers, placement context or preview/cell-state side effects. State the strongest mechanism actually established.

Compare **at least these classes**, using native logic and the available saved/visual examples:

- Dynamic actors (player/animal); why the extractor preview is rejected. Do not investigate animal AI.
- Large static or procedural rocks and shrubs/trees; distinguish placed static references, generated pack-ins, resource/decorative clutter and harvestables where the code provides a meaningful distinction.
- Gas vents/flora/harvestables as separate potential categories **if actual predicates or case evidence support them**; absence of a screenshot is not proof of identical treatment.
- Beacon preview versus ordinary solar/extractor placement; identical error wording does not itself prove identical enforcement logic.

Investigate when clutter is only hidden for placement preview, when it is disabled/removed after confirmed construction, and how it is restored on cell departure/reentry, save/reload or procedural/regeneration work. The reported **rock reappearing and intersecting existing structures** is a user-observed concern from earlier play, *not reproduced by these six saves*. Identify a plausible causal path and a precise discriminator if the current evidence cannot settle it; do not claim it happened during this acquisition.

Avoid reverse engineering complete world generation, mesh collision, actor pathing or renderer visibility. Follow narrow dependencies far enough to explain the placement outcome or specify the actual missing input.

## 5. C — Native/save correspondence and worked comparisons

For each scenario compare baseline → beacon → completed outpost, using the already accepted Workshop construction-root and position provenance. Record positive object identity, owner, saved position/transform, disabled/deleted flags or environmental persistence channels **only where decoded**. Separate actual save changes from pre-existing world/definition state and transient screen feedback. Where possible, use a native-grounded before/after representation showing the exact validator inputs or decision stages.

Produce a matrix for the observed cases:

`candidate | obstructing/restricted context | underlying native predicate | observed UI outcome | saved inputs | transient inputs | confidence / remaining discriminator`.

At least one worked POI/beacon and solar admission/rejection pair, one marginal-versus-deep static overlap pair, and the animal obstruction should be explicitly addressed. An appropriately bounded negative result is acceptable only when the actual relevant native callers/dataflow were examined and the missing discriminator is concrete. A function name or screenshot alone is insufficient explanation.

## 6. Deliverables, interpretation and handoff

Write an answer-first L3 research package under `docs/experiments/` with accessible subsections for territory/POI admission, collision/suppression, lifecycle/persistence, six-save comparisons and the screenshot evidence ledger. Include native locators, type/field provenance, installed build pins, bounded worked examples and an independent review. Update `docs/RESEARCH_STATE.md`, indexes, relevant decision/backlog notes and L3 boundaries where justified; do not silently overwrite earlier L1/L2 or position findings.

Lead with plain-language answers: **Why is beacon placement refused near a POI? Why can a valid outpost have a clipped usable region? Why are some rock overlaps forbidden while deeper overlaps become permitted? How are actors treated? What is saved versus reconstructed?** Give `PROVEN`, `STRONG`, `PROVISIONAL`, or `OPEN` separately by claim, with SAVE / STATIC / user-observed live evidence identified. Prefer explanatory sufficiency at reasonable engineering confidence over impossible universal absence proofs.

Do **not** automatically commission an observer, ask for more player saves, begin a live experiment, implement mods or broadly reopen resource-region reverse engineering. If a specific critical outcome requires live evidence, propose one minimal discriminating test and a separate approval gate; the existing screenshots and six saves remain the authorized baseline.

## 7. Frozen compact completion contract

- **Type/deliverable:** Bounded offline research with answer-first mechanistic explanation of (A) POI/beacon/territory clipping, (B) placement collision and static suppression, (C) save versus transient state, using the newly acquired Kreet evidence.
- **Authority/inputs:** Existing project-owned readers, installed EXE/ESM/PEX, read-only Ghidra/native evidence and existing historical control corpus as needed; six protected new saves, eleven screenshots. No live game, save creation/edits, runtime instrumentation, build/deployment, staging, commit or push.
- **Mandatory acceptance:** (1) Exact six-save identity/backup/hash/seal plus accessible screenshots' inventory/provenance and appropriate missing-evidence disclosure; (2) positive saved baseline/beacon/completed outpost comparisons with unsupported fields marked UNKNOWN; (3) causally traced POI/beacon rejection and nearby accepted control; (4) grounded boundary clipping and inside/outside construction eligibility mechanism; (5) static/clutter suppression explanation addressing marginal versus deeper overlap; (6) actor rejection and category differences, with other environmental classes bounded; (7) persistence/reappearance assessment without misrepresenting absent historical incidents, and answer-first evidence/uncertainty matrices; (8) verification, protected-input integrity, durable docs, independent reviewer ACCEPT and complete exact review package.
- **Optional:** narrow future live discriminator when a consequential question remains genuinely unresolved; never execute without new authority.
- **Negative/blocked outcome:** Preserve examined native/definition routes and counterevidence; one missing visual or save field does not prove absence. A true inaccessible original or unsafe data operation requires precise STOP/ESCALATE on that affected branch; continue independent authorized work.
- **Continuation:** Diagnose/correct/retest within authorization without repeatedly requesting rebriefing. Frozen mandatory criteria change only with explicit maintainer approval; distinguish scientific confidence from assignment completion.
- **Health/protection:** Apply `WORKFLOW.md` and `docs/RESEARCH_EXECUTION_PROTOCOL.md`, both-drive free-space controls, immutable original evidence, identity guards and no arbitrary time/volume cutoff. Do not silently relax protections.
- **Review/package:** Criterion-wise PASS/FAIL/NOT TESTED, evidence pins and actual check receipts; independent reviewer procedure; `git status --short`; `<task>-task-only.diff` plus `<task>-complete.diff` including untracked authored text/unchanged supplied brief as appropriate; path/hash/exclusions inventory; byte-exact forward/reverse reconstruction and UTF-8/LF/encoding/link/whitespace checks. Native/save/screenshot proprietary originals stay local/ignored. Nothing staged/committed/pushed by Codex.

Suggested commit subject: `docs(placement): map Kreet POI clipping and clutter admission`
