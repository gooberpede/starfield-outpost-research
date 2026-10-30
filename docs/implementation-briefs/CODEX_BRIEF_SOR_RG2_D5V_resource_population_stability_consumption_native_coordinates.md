# RG2-D5V — Resource Population Stability, Regeneration and Gameplay Consumption

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)  
**Assignment:** Offline-first scientific investigation, including conditional read-only save examination; no retail game operation or plugin changes.  
**Status:** Proposed implementation/research brief. Freeze D5V-AC1–AC11 and the controlling questions before work.  
**D5P observer:** Retail NO-GO. **B6/publication:** ON HOLD.

## 1. Controlling scientific purpose

Determine **how Starfield ordinarily creates, preserves, invalidates, regenerates and exposes resource populations at existing outposts**, and why player-visible resource availability is usually stable despite the native generation alternatives demonstrated by D5S/D5T/D5U. Establish the actual relationships among native generation, retained source populations, landscape lifecycle, Workshop/resource consumers and persisted outpost state. Explain *normal mechanisms*, not a presumed defect.

The maintainer reports an intermittent missing/swapped-resource gameplay bug. **That report is background context, not a hypothesis privileged above alternatives or a reason to bias this investigation towards mask variability, scheduling, cache failure or any other proposed fault.** Do not diagnose or reproduce the bug as part of D5V merely because it exists. A native mechanism's ability to vary is not evidence that it causes the reported bug. Report any independently evidenced defect neutrally, but do not substitute bug hunting for the controlling questions.

Freeze stable question IDs:

- **D5V-Q1 — Population lifecycle:** When is construction executed, when is a previously constructed population reused, and which specific lifecycle operations can invalidate it or require regeneration during common arrival, departure, streaming, loading and Workshop activity?
- **D5V-Q2 — Gameplay consumption:** By what actual native data and control paths do generated resource regions become resource queries, outpost resource availability and extractor/Workshop decisions? Can a changed gameplay observation arise without a changed generated population, as a matter of native semantics? Do not assert that it does occur without evidence.
- **D5V-Q3 — Stability mechanisms:** Under documented ordinary action/state contracts, what determines stability of the player-visible population, including any constraints on query-winner selection, caching, lifetime, persisted state, or consumer behaviour? Distinguish guaranteed invariance, conditional stability, and possibilities that require unobserved timing.
- **D5V-Q4 — Native spatial provenance and visualization:** Establish and document the native coordinate domains, transforms and ownership of the geometry, outpost centre/beacon, 150-native-unit build radius, source frames, Workshop queries and consumer outputs. Produce scientifically traceable visual comparisons using the **actual native coordinate system(s)**, not a plausible but unverified coordinate grid grafted onto results.

These are controlling questions, not headings for a bounded literature review. Each must end **COMPLETE, INCOMPLETE or BLOCKED** under current governance. No narrowing, silent omission or overall ACCEPT while a mandatory question remains incomplete/blocked.

## 2. Baseline and mandatory reading

Read current `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/SAVE_PROTECTION.md`, active `RESEARCH_STATE.md` and project decisions. Apply the 2026-10-30 controlling-question governance reinforcement.

Start with actual committed D5Q–D5U and D5U-C1 documents, geometry and map generators; D5C cache/visited lifetime research; earlier SOR-002/003 outpost/native-centre work; Workshop resident/extractor/resource consumer research; and the separately recorded operator checks: **Feynman V Cu Co Ni IL** qualitatively matches all four resources with minor shape differences, and **Feynman V Cu IL F** qualitatively matches the Mask 3 alternative rather than Mask 0. They are operator-reported observations, not independent native proof.

Verify rather than assume the installed binary/data/Ghidra pins. Prior pinned Starfield 1.16.244.0 executable SHA-256 is `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; ESM `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`; PlanetData `2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5`. Native VAs in older documents are preferred static VAs based at `0x140000000`, not relocated addresses. Never transfer a pinned layout without verification.

Preserve the established findings: D5Q maps provider/cell selection/mask and map hit/miss; D5S proves two native-feasible query winners with distinct controlled ordinary geometry and a bounded source-lifetime gap; D5T proves two ordinary outcomes at second Feynman V in its fixed domain; D5U establishes a three-outcome counterexample in a different qualified domain; D5U-C1 distinguishes historical-frame outpost composites from prospective normalized source geometry. **None of these alone proves that gameplay changes populations, why they normally persist, or the cause of the missing/swapped-resource bug.**

## 3. Q1 — Native population and landscape lifecycle

Trace the concrete native path, with exact call, field, ownership and side-effect evidence, for these ordinary action/state classes insofar as each can affect population construction or validity:

- First demand after a cold manager/index initialization; initial arrival and required streaming prerequisites.
- Subsequent spatial demands against visited/source-map state, including bypass, lookup hit and fresh miss; establish which paths execute the generator, not a complete historical cache-hit byte-continuity proof.
- Landscape focus/region shifts, cell/source retirement, Grid clear, ProcGen reset/destruction, worldspace changes and manager replacement.
- Exiting/re-entering an area and loading/reloading existing outpost state, including which lifecycle state is reconstructed versus retained in process.
- Actual Workshop/outpost events only where they intersect construction, invalidation or consumer availability.

Do not confuse a source-vector membership, source-map wrapper allocation, visited marker, successful region copy, aggregate result or Workshop availability flag. Distinguish state persistence in **process memory** from serialization in a save. For each transition state whether it **can** cause new generation, **must** cause it subject to predicates, or merely permits it; document the precise source of that characterization. Prove or bound any claim of a stable population across a normal activity sequence. Full cache-hit content identity and first-ever Save52 query tracing are **not standalone acceptance requirements**; investigate only if indispensable to Q1–Q3.

## 4. Q2 — Generated geometry to gameplay resource availability

Trace source/collection/region ownership from native copied geometry into the actual downstream spatial query and Workshop consumers, including extractor-location checks where evidenced. Locate native functions and inputs/outputs for:

1. retrieving/interpreting generated resource regions at a queried location;
2. resolving which resource(s) a position is considered to occupy, including spatial predicates, overlaps, priority and any filtering;
3. aggregating or exposing resource availability for an outpost and supporting extractor decisions;
4. relevant caching, query-result state, UI-facing or saved Workshop state only where causally connected.

Use the existing D5Q Workshop resident scan and prior SOR-002/003 consumer evidence as starting points, not as proof of a complete dataflow. Show where geometry can be unchanged yet a consumer could return a different result **if** the code and inputs allow it. Conversely, establish conditions under which consumer results are deterministic. A mere speculative list of bugs is not completion. Do not presume that resources visible in the scanner, selectable in Workshop and usable by an extractor use identical predicates.

## 5. Q3 — Ordinary stability versus admitted alternatives

Separate at least four distinct mechanisms: (a) construction-query winner selection, (b) generation outcome for specified effective inputs, (c) in-process retained population reuse/invalidation, and (d) downstream interpretation by the gameplay consumer. Identify the actual protection/stability contract for each and how the contracts compose in ordinary arrival/return/reload scenarios.

Use the two manually checked Feynman V outposts as focused reference cases and other recorded outposts only as needed to discriminate competing mechanisms. A complete answer need not establish the **frequency** of alternative outcomes in retail if frequency is not derivable offline; it must not present possibility as observation. Investigate the provenance of any state indispensable to Q3. If a value cannot be recovered from executable/static data and has a reasoned potential serialized producer, perform a **targeted read-only** examination of approved save evidence/copies under `SAVE_PROTECTION.md`; do not begin broad save archaeology. Persisted centre/outpost state is not by itself evidence of persisted resource geometry.

If offline work cannot distinguish two live-only mechanisms, document the precise discriminating measurement and why authorized alternatives cannot answer it. This is a candidate **BLOCKED/ESCALATE**, not a licence for unapproved live work or an ACCEPT for an unanswered question.

## 6. Q4 — Native spatial coordinate contract and plots

**Mandatory: establish coordinate provenance before altering or creating a spatial plot.** Native data may legitimately use several coordinate domains; do not assert that one universal 2D plane applies to all operations. For each displayed layer record:

- native producing function/structure and coordinate domain (e.g. source-local Int2, native region geometry, world/native outpost centre, terrain or Workshop query);
- axis definition, origin, units and orientation, including handedness/vertical axis if relevant;
- scale, offsets, signedness, numeric precision, rounding and any projection or frame conversion;
- original native values and exact transform to plotting coordinates, with round-trip/control checks where mathematically meaningful;
- what constitutes a *native* coordinate versus a deliberate **display-space transform** (translation, Y inversion, clipping, viewport scaling); never label display coordinates native;
- explicit distinction among source anchor, outpost native centre and beacon; prove equality before co-locating them.

An SVG may translate/scale native coordinates for presentation; this is acceptable **only when the transform is explicit, reversible as appropriate and independently validated**. If two native domains cannot be joined, do not superimpose them. Preserve existing correct D5U-C1 maps and correct their labels/transforms where evidence warrants, without reinterpreting historic evidence retrospectively.

For every genuine **outpost** map show the verified native centre and the full **150-native-unit radius** circle in the correct frame. Mark beacon separately where appropriate. Preserve consistent IRES-derived resource colors and accurate resource-deposit shapes, with the prior documented marginal-boundary approximation disclosed. Never substitute a source-only map for an outpost map; U26 remains a source-only example. Clearly label each image as observed/manual, historical-frame reconstruction, prospective native model, or conditional alternative; distinguish overlaid observations from model geometry.

**Visualization deliverables:** at minimum one native-coordinate-domain and transformation diagram, one outpost-centred lifecycle/consumer comparison for each of the two Feynman V reference outposts where supported, and a diagram/figure of lifecycle state transitions and consumer boundaries. Prefer reproducible SVG plus machine-readable backing data. Add further comparison or before/after maps when necessary for a scientific claim, not merely to decorate the report. If a spatial claim cannot be plotted because a coordinate join is genuinely unavailable, record exact missing edge, attempted alternatives and the BLOCKED consequence under Q4; do not quietly omit a mandatory layer. Validate diagram semantics and legibility independently, including rendered previews and frame/scale/center checks.

## 7. Method, continuation and review

Create an **active investigation ledger near task start**, with D5V-Q1–Q4, required dependencies, evidence and candidate explanations, negatives, paths searched, next concrete actions and branch dispositions. Follow all material authorized upstream/downstream dependencies across landscape, ProcGen, save and Workshop code until answered or a demonstrated terminal blocker; a subsystem boundary or an inconvenient static path is not grounds to close. The reviewer must identify the highest-value omitted authorized lead, if any.

Permitted: read-only Ghidra exports on pinned existing state; existing game data and controlled historical evidence; bounded original native methods in **disposable** offline processes; new task-owned parsers, controls, visualizers, and reproducible tests under ignored scratch. Reuse existing qualified components; if a new method cannot answer a key question, diagnose and revise it in the same assignment. No installed game invocation, attaching, breakpoints, SFSE plugin changes/deployment, Vortex operations, save edits, gameplay actions, Ghidra database edits, external communication, staging, commit, push or publication. Preserve the 40,000,000,000-byte free-space guard separately on C: and D: when applicable. Raw native/save evidence and proprietary artifacts remain local-only; no unapproved redistribution.

Separate findings as **ESTABLISHED (static)**, **ESTABLISHED (executed)** with its fixture coverage, **OPERATOR OBSERVED**, **INFERRED**, or **UNRESOLVED**. Include falsifiers, control cases and explicit evidence provenance. Verify geometry/consumer agreement with actual native predicates, not visually plausible shapes alone. Preserve differences between negative evidence, lack of evidence and invalid/incomplete capture.

The **independent scientific/completeness reviewer** must inspect the frozen controlling questions, active ledger, native evidence windows, alternative mechanisms and counterexamples. It must reject an unanswered material question where plausible authorized investigation remains. A distinct engineering/evidence reviewer verifies methods and transformations; an editorial reviewer checks authored prose, maps/legends and scientific qualifications. Apply actual exact-snapshot and delta review, not merely a self-reported successful check.

## 8. Completion and escalation contract

Use the 2026-10-30 governance rules without relaxing them:

- **COMPLETE:** Each controlling question has a supported answer at its frozen generality, including an adequately controlled scoped negative conclusion when appropriate; all mandatory deliverables and independent reviews pass.
- **INCOMPLETE / REWORK:** Any material question remains unanswered with further authorized work available; labels, diagrams, partial findings or passing infrastructure tests do not close it. Continue under this brief.
- **BLOCKED / ESCALATE:** An indispensable edge, input, capability or unauthorized action is proven necessary and inaccessible despite documented authorized alternatives. Name its exact site/value, attempted evidence paths, why alternatives cannot resolve it, impact on each question and minimal requested action plus reproducible resume checkpoint. BLOCKED is not COMPLETE.

Do not re-scope the assignment into a missing/swapped-resource bug investigation. Do not imply the native scheduling alternatives caused the reported bug. A separately scoped and explicitly approved bug investigation may follow only when useful, not as a substitute for the normal-system scientific account.

## 9. Deliverables

Follow actual repository conventions; do not create redundant document frameworks:

- `docs/experiments/resource-retained-population/d5v-report.md`: direct Q1–Q4 answers first; lifecycle and consumption explanation; stability analysis; evidence strength and gaps; no bug attribution without proof.
- `docs/experiments/resource-retained-population/d5v-lifecycle-consumer-map.md`: evidence-linked native call/data/ownership map and action/state transition matrix.
- `docs/experiments/resource-retained-population/d5v-coordinate-contract.md`: native coordinate taxonomy, precise transforms and independent join verification for plotted layers.
- `docs/experiments/resource-retained-population/d5v-investigation-ledger.md` and `d5v-sources.csv`: active history, alternatives/counterexamples, traceability and terminal dispositions.
- Task-owned machine-readable spatial exports plus SVGs and a small linked gallery/readme under an appropriate `d5v/` directory. Clearly identify whether existing D5U-C1 maps are reused, corrected or supplemented, preserving historical originals.
- `d5v-review.md`: original frozen criteria, independent scientific/completeness, engineering and editorial review, separate science/engineering/authority outcomes, actual receipt and snapshot limits.
- Exact-hash final delivery manifest and **complete and task-only diffs**, with verified inclusion/exclusion inventory, untracked paths, `git status --short`, whitespace/link/patch byte checks and unchanged HEAD/index. No staging, commit or push.

## 10. Frozen acceptance criteria

| ID | Required result |
|---|---|
| **D5V-AC1 — Authority and provenance** | Verify exact installed/native/data/analysis identities and protection boundaries; strictly offline. No unapproved target, save, repository or publication actions. |
| **D5V-AC2 — Controlling questions and ledger** | Freeze D5V-Q1–Q4 and original generality, establish active investigation ledger early, pursue and close/disposition each material discovered branch without silent narrowing. |
| **D5V-AC3 — Construction and regeneration lifecycle** | Establish concrete generation/retention/invalidation/reconstruction paths for relevant ordinary actions/states, precise predicates and implications; no hand-waving about generic caches. |
| **D5V-AC4 — Native gameplay-consumer paths** | Map actual native geometry-to-query-to-Workshop/extractor resource decisions and identify whether/where consumer outputs can differ independently of geometry, with evidence and counterexamples. |
| **D5V-AC5 — Normal population stability** | Explain supported stability/invariance mechanisms and conditions and how they constrain alternatives; distinguish guaranteed, conditional and merely feasible changes; do not conflate bug observations with causes. |
| **D5V-AC6 — Native coordinate provenance** | Prove and document native coordinate domains, origin/scale/orientation/precision and each cross-frame transform; independently verify outpost-centre/beacon/boundary joins, distinguishing native data from display transformation. |
| **D5V-AC7 — Scientific visualizations** | Produce reproducible, legible SVG/geometry-backed native-coordinate/lifecycle/consumer maps for supported Feynman V reference cases with 150-unit circles, honest spatial provenance, resource colors, labels and approximation limits. |
| **D5V-AC8 — Conditional save-state gate** | Pursue targeted read-only save research only for a specifically identified missing indispensable input with supported serialized provenance; otherwise document non-trigger. No save mutation. |
| **D5V-AC9 — Discrimination, negative controls and continuation** | Test plausible competing explanations; preserve non-supporting evidence; follow authorized leads. COMPLETE requires original-question proof, otherwise INCOMPLETE/REWORK or evidenced BLOCKED/ESCALATE. |
| **D5V-AC10 — Independent adversarial review** | Separate reviewer challenges omissions, native edge semantics, coordinate joins and bug-neutrality; engineering and editorial reviewers inspect primary evidence and exact outputs; no accept-by-documentation. |
| **D5V-AC11 — Durable final delivery** | Exact maps/exports, report/ledgers, reproducibility, full criteria matrix, source/licensing protections, review records and verified complete/task-only diff package; no stage/commit/push. |

**No result from this offline assignment authorizes a retail session, SFSE repair, publication, or a new bug-focused scope.**
