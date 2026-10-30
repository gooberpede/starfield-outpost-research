# RG2-D5W — Normal Resource-Generation Operating Contract and Outcome Preference

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)

**Assignment:** Offline-first, question-led research into the normal operating behaviour of Starfield's resource-generation system. Follow material authorized dependencies across subsystems; allow narrowly triggered read-only save analysis. **No retail game launch, SFSE modification/deployment, Vortex operation, save modification, publication or repository integration.**

**Status:** Implementation/research brief; freeze D5W-Q1–Q4 and D5W-AC1–AC11 before investigation. D5P retail remains **NO-GO**; B6/publication **ON HOLD**.

## 1. Scientific purpose and non-assumptions

**Controlling objective:** Determine what resource-generation behaviour Starfield's ordinary initialization, scheduling, generation and retention architecture **guarantees, structurally favours, permits as an alternative, and treats as exceptional**; establish the level of stability actually supported for source geometry, outpost-wide resource identities and extractor availability. If one outcome is privileged, explain **the mechanism** rather than guessing which mask the developers wanted.

This is an operational-contract investigation, **not** an attempt to reconstruct developers' thoughts and **not** a bug-cause investigation. The maintainer reports that ordinary repeated visits generally show stable resource presence, and an intermittent missing/swapped-resource bug exists. Neither observation privileges mask variability, worker scheduling, caching, consumer filtering or any candidate bug cause. A cache can preserve either of two generated outcomes; repeated visits to one retained population are **not independent generation trials**. The manually inspected Feynman V Cu IL F outpost qualitatively matches Mask 3, but **must not** be used to nominate Mask 3 as canonical in advance.

Freeze the following questions:

- **D5W-Q1 — Normal-path preference:** Under an explicitly specified ordinary, successful initialization/arrival state, what native request, dependency, service-pump, publication, worker-claim and source-map-miss rules determine—or structurally favour—the first constructing query? Is there a guaranteed winner, a conditional preference, or only several permitted winners?
- **D5W-Q2 — Outcome authority:** Does the architecture establish an authoritative source-level population, sampling location, query, mask or outcome? Distinguish a canonical native rule from incidental first-writer authority and from a typical but unenforced execution preference. Do not presume one mask per outpost or one result per source.
- **D5W-Q3 — Stability levels:** What does normal operation guarantee or favour for (a) outpost-wide resource identities, (b) exact native deposit geometry, and (c) extractor-specific availability at fixed coordinates? When can each remain stable while another varies? Distinguish initial construction, process-local retention, regeneration after invalidation and fresh loading episodes.
- **D5W-Q4 — Competing-design discrimination:** Which of these hypotheses best fits **independent native architectural evidence**: a canonical source result; multiple intentionally permitted first-construction outcomes with stable retention; a higher-level selection policy with admitted exceptional interleavings; or another supported operational model? Specify the evidence that confirms, contradicts or cannot distinguish each. A verified violated invariant is distinct from surprise, rarity or a known gameplay symptom.

Question completeness is not measured by the number of documents or tests. No shift to a narrower question, no “could not find” closure, and no declaration of a developer's intent from visual plausibility alone.

## 2. Required baseline and preservation

Read the **current** `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/SAVE_PROTECTION.md`, current research state/decisions, and the relevant D5Q–D5V and D5V-C1 documentation, source/claim ledgers and original receipts. Apply the strengthened controlling-question and dependency-ledger governance, including exact independent completeness review.

Primary prior findings to preserve and challenge only with actual counterevidence:

- D5Q: source provider receives original Int2 and manager; raster low nibble is a **numeric rarity control**, not a per-resource bitset; source map, visited guard and geometry copying have separate semantics.
- D5S: distinct native-feasible first-winner continuations and different surviving ordinary geometry; a bounded source-lifetime protection gap. Feasibility does **not** give retail frequency.
- D5T: precisely two ordinary source outcomes for Feynman V outpost 2 within the frozen scope.
- D5U: qualified three-outcome counterexample at source U26, which is **not an associated outpost**; source masks and whole-outpost outcomes are not interchangeable.
- D5U-C1: historical-frame source joins and seven outpost composites; manually compared Feynman V Cu Co Ni IL resources match qualitatively, and Feynman V Cu IL F matches Mask 3 qualitatively.
- D5V and D5V-C1: population retention/invalidation, distinct area and point consumers, native-coordinate presentation with **absolute** descriptor-frame axes, verified native outpost centres/150-unit circles, and full-extent companion views. These do **not** identify a bug cause.

Verify exact installed executable/data/Ghidra identities before using pinned addresses. Prior Starfield 1.16.244.0 hashes: EXE `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; ESM `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`; PlanetData `2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5`. Native addresses are preferred static VAs based at `0x140000000`, not relocated addresses. Verify provenance rather than silently porting.

## 3. Q1: Ordinary execution and critical paths

Begin from D5S's proven competing winners and D5R's request graph, **not** a presumed Mask 3 winner. For Feynman V Cu IL F (primary case), trace both paths and their relevant siblings backward through complete ordinary focus/landscape initialization, root derivation, cell/rectangle registration, density/layer dependencies, asynchronous file readiness, JobSite/service-pump publication, actual worker claims, source selection, visited/map barriers and the first exclusive constructing miss.

For each competing path document:

1. Original Int2, source identity, effective descriptors and cold/warm state assumptions.
2. Mandatory predecessors, ready conditions, synchronous versus asynchronous stages, locks and queues; whether work can be claimed while registrations are still in progress.
3. Any native priority, FIFO, ordering, inline-execution, cancellation, reuse or canonicalization rule, including the *scope* of its guarantee. Do not infer fairness, scheduling probabilities or preference from iteration order alone.
4. The minimum relative ordering/interleaving for that winner; identify which conditions are normal-state, exception-state or unresolved **with evidence**.
5. Any decisive additional upstream producer/consumer or scheduling path. Follow material authorized dependencies until resolved or proven blocked, rather than deferring them as a new project.

Produce **paired critical-path diagrams** marking happens-before constraints, concurrency windows, source-map arbitration and each inferred preference distinctly. Where a preference is structurally suggested but not guaranteed, identify the exact missing latency or scheduling assumptions; do not manufacture numerical probabilities. Quantitative claims require measured, independently justified timing distributions or an explicit probability model with validated premises. Repeated visits to one retained population are not a sampling design.

## 4. Q2: Authority and intended operating contract

Test competing design explanations rather than treating one central or common-looking mask as authoritative:

- A canonical query/sampling position generated from source anchor, nominal source footprint, outpost centre or a deterministic canonicalization operation.
- Higher-level request/streaming policy that selects or strongly favours a particular constructor.
- Deliberately permitted query-dependent generation with first-writer retention and stable subsequent reuse.
- An architectural invariant contradicted by a native-feasible continuation (conditional defect **only if** the invariant itself is independently established).

Investigate raster boundaries, source padding, nominal footprint, ordinary resource/rarity data, source selection and generator query conversion **as discriminators**, not proof-by-geometry. For each proposed canonical location, prove the native code actually chooses/uses it authoritatively or classify it as a hypothesis. Establish whether the source map/visited guard is simply a performance and stability mechanism or enforces a particular result; do not infer intent from existence of a cache.

Use controls: (i) Feynman V Cu IL F as primary two-outcome/manual-match case, (ii) Feynman V Cu Co Ni IL as multi-source outpost check, (iii) a previously qualified singleton source, and (iv) U26 as a three-outcome *source-only* adversarial example. Add further existing-data examples only if needed to discriminate hypotheses. Preserve the difference between source-level mask, source geometry, jointly admissible multi-source construction and outpost-wide availability.

Evidence hierarchy in the report:

- **EXPLICIT DESIGN EVIDENCE:** verifiable developer/technical statements with exact source and applicability.
- **INFERRED OPERATIONAL CONTRACT:** independent native architecture and controls that justify an invariant or favoured path.
- **PERMITTED/EXECUTED BEHAVIOUR:** compiled feasibility or controlled native execution without corresponding intent proof.
- **UNKNOWN:** unresolved alternatives with exact discriminator; not equivalent to absence of a rule.

Direct external sources may be consulted **read-only**, with the repository's source-permission/provenance gates. Do not incorporate third-party implementation, open issues/contact developers, or disclose private research without separate authorization. Direct developer documentation is helpful but not a mandatory prerequisite to inferring a qualified operational contract.

## 5. Q3: Three stability targets, no bug assumption

Construct a state/consumer matrix separating:

| Stability target | Required discriminator |
|---|---|
| Outpost-wide resource identity set | Native area test, radius, transforms, source population/consumer state; can different valid geometries yield the same resource names? |
| Exact resource-deposit geometry | Native input/winner dependence, retained state, invalidation and fresh generation; can identical names hide different geometry? |
| Extractor availability at fixed placement | Native point/footprint tests, accepted resource definitions, placement/Workshop state; can area results remain equal while a fixed extractor point changes? |

Trace normal persistence across **same retained episode**, **new generation after qualified invalidation** and **fresh loading episode**, treating them as distinct scientific circumstances. Do not assume save-serialized geometry; consult a protected save read-only only if a specific indispensable input with a plausible persisted producer has been evidenced and offline/static alternatives have been checked. A game-architecture claim that one behaviour is favoured must say under which state contract it holds. A statement that something *could* vary is not evidence that it *does* vary in retail.

The missing/swapped-resource bug is a known gameplay report but **not a privileged hypothesis or target**. Do not attribute it to multiple masks, cached state or consumer differences without independent causal evidence. No bug remediation is authorized.

## 6. Q4: Discrimination, counterexamples and stopping rules

Maintain an explicit competing-hypotheses matrix, each with positive evidence, negative evidence, strongest counterexample, discriminating next test, and current disposition. Investigate structural preference even if not perfect: one branch's prerequisite chain may favour it over another, but label *potential preference* versus a demonstrated ordering guarantee. Do not call an alternate path pathological merely because it differs from the operator's Mask 3 observation.

Completion must establish one or more **appropriately bounded operational conclusions**: canonical rule, architecture-backed conditional preference, genuinely permitted alternatives without an identified preference, or a demonstrated inconsistency with an independently established invariant. These may coexist at different levels of stability. The research is **not COMPLETE** if material authorized checks remain that could distinguish these models.

If a decisive property depends irreducibly on runtime timing, establish the precise missing signal, why static/native controlled methods cannot supply it, and the **smallest discriminating experiment**, with a proposed operator-only method; this is BLOCKED/ESCALATE for that controlling question, not automatic approval to launch Starfield or repair the D5P observer. Distinguish what a hypothetical fresh independent generation episode would measure from repeated visits to one retained population.

## 7. Maps and explanatory figures — native coordinates mandatory

Visualizations are required whenever spatial or causal relationships materially support a claim. Produce at minimum:

1. **Absolute native-coordinate sampling maps** for the primary case, showing source nominal footprint and padded query support, raster mask regions, proven winning queries, unproven candidates, and each hypothesized/established canonical sampling point with visibly different styles.
2. **Outpost-level spatial comparisons** for the two Feynman V reference outposts, using validated **absolute native descriptor-frame X/Y axes**, their verified centres and beacons where established, full **150-native-unit boundary circles**, all relevant contributing resource sources and resource colors sourced from IRES. Provide full-extent companion views where geometry extends beyond the detail view.
3. **Critical-path diagrams** comparing candidate winning requests, barriers, work queues and opportunities for overtaking; distinguish proved ordering from assumed or unmeasured timing.
4. **A compact stability matrix/diagram** separating the three player-facing stability targets and the relevant lifecycle transitions.

Do not silently translate the scientific coordinate origin to `(0,0)` at the outpost. Renderer pixel coordinates and viewport translations are permitted, but labels/axes and plotted native geometry must refer to the actual native domain. Do not equate source-relative, body-face and descriptor-frame coordinates without an explicit validated transformation. SVG maps are research artifacts derived from machine-readable evidence and accompanied by source/transform metadata and fidelity limitations. Use actual deposit geometry rather than bounding boxes where qualified; disclose approximated continuous edges and unmeasured retail overlays. Preserve existing accepted figures; new maps must not retrospectively rewrite their native scientific inputs.

## 8. Execution, investigation ledger and independent challenge

Begin with a frozen question/acceptance register and create a durable **active investigation ledger** near the start, with stable IDs for each material native path, hypothesis, evidence pointer, failure, dependency, attempted discriminator and next action. Checkpoint meaningful updates during investigation; preserve genuine failures and rejected models without inventing chronology.

Reuse existing read-only Ghidra exports, static archives, qualified native fixture methods and previously verified geometry/consumer outputs proportionately. Disposable native execution is permitted in isolated processes if needed and scoped safely; do not operate installed Starfield itself. Enforce source/permission guards and 40,000,000,000-byte free-space floors on C: and D: where applicable. Maintain original evidence hashes and protected originals. No destructive reanalysis or Ghidra database mutation; keep proprietary dumps and source assets local-only.

Independent **scientific/completeness**, **engineering/evidence** and **editorial** reviewers must receive the original contract, active ledger, full evidence and changed tree, not just a summary. The completeness reviewer must challenge whether the paths supporting one 'normal' outcome were selected retrospectively, whether a timing/preference assertion lacks proof, and which highest-value authorized avenue remains. Reviewer REWORK returns the **same assignment** for correction, not a new brief. Material unresolved authorization blockers receive ESCALATE with a narrow request. Do not redefine criteria or demote unanswered controlling questions to optional recommendations.

## 9. Deliverables

Place focused authored work under `docs/experiments/resource-retained-population/` using existing conventions:

- `d5w-report.md`: answer each controlling question; classification of canonical/favoured/permitted/exceptional; confidence, native/retail limits, counterexamples and possible operational contract.
- `d5w-normal-path-model.md`: both candidate critical paths, state assumptions, ordering guarantees, life-cycle relationships and precise outstanding discriminators.
- `d5w-hypotheses.csv` or equivalent: positive/negative evidence, branch dispositions, controls, question linkage.
- `d5w-investigation-ledger.md`: active branch and dependency accounting, preserved failures/checkpoints.
- `d5w-sources.csv` and `d5w-review.md`: evidence provenance and exact independent review/dispositions.
- `d5w/README.md`, reproducible SVGs/diagrams and machine-readable plotting data for the required figures, or equivalent established directory layout.
- Source hashes, method/test receipts and a final delivery manifest, complete/task-only diffs, status/inclusion/exclusion inventory, exact reviewed-snapshot identity and proportionate editorial validation.

Avoid creating redundant records or rerunning full geometry populations where existing accepted controls suffice. Do not stage, commit, push, make a PR, or publish. A fresh retail run card may be proposed only upon an evidenced indispensable discriminator; it remains **NOT AUTHORIZED**.

## 10. Frozen acceptance criteria

| ID | Mandatory outcome |
|---|---|
| **D5W-AC1 — Authority and provenance** | Verify current source/binary/data/Ghidra identity and protection; no live game, SFSE/Vortex, protected save mutation, third-party reuse or publication outside existing grants; record exclusions. |
| **D5W-AC2 — Controlling questions and ledger** | Freeze Q1–Q4, success/negative conditions and parent relationship; actively log significant branches, failed assumptions and dependencies. No silent scope narrowing. |
| **D5W-AC3 — Normal initialization and critical paths** | Trace the material ordinary ingress and both target winner paths through native dispatch and first constructing miss, with verified synchronization/priority boundaries. Discriminate guarantees from plausible preference. |
| **D5W-AC4 — Outcome-authority test** | Seek and test canonical source/winner/selection rules and alternative first-writer contracts; apply independent controls and reject unsupported claims of one intended mask. |
| **D5W-AC5 — Three-level stability** | Explain what is guaranteed, favoured or conditionally stable for area resource identities, surviving geometry and fixed-location extractor availability, across retained and fresh-generation episodes. |
| **D5W-AC6 — Competing design hypotheses** | Compare models with explicit falsifiers, counterexamples and supported dispositions; do not assume the missing/swapped-resource bug's cause. Follow material authorized leads or prove a terminal barrier. |
| **D5W-AC7 — Native-coordinate visualizations** | Provide required maps, outpost overlays, full-extent views, path and stability diagrams; native-coordinate axes, IRES provenance and validated transformations, with uncertainty legible in the figures. |
| **D5W-AC8 — Conditional persistence/source gates** | Examine save state only on a demonstrated indispensable-input trigger; evaluate external developer evidence under provenance and permission controls without making it required. |
| **D5W-AC9 — Outcome/exit integrity** | COMPLETE only for answered controlling questions under original scope; otherwise INCOMPLETE/REWORK if authorized avenues remain or BLOCKED/ESCALATE with exact proof, alternatives and minimal next action. |
| **D5W-AC10 — Independent completeness review** | Independent scientific, engineering and editorial reviews challenge primary evidence and omitted authorized avenues; exact-snapshot disposition, remediate REWORK under same task. |
| **D5W-AC11 — Durable delivery** | Reproducible outputs, source ledger, complete/task-only diff manifests, status, editorial/manual checks, exclusions and reviewed identities; no integration or publication. |

## 11. Specific scientific cautions

- An outcome repeatedly returned by **one retained population** is not evidence of its probability across independent initial constructions.
- Native-feasible alternatives do not establish retail occurrence rates, bugs or lack of developer care.
- A nominal centre, source anchor, outpost beacon and raster sample may coincide in a particular case; never assume interchangeability without native proof.
- A numeric rarity mask is **not** a resource-membership bitset.
- Multiple outcomes at one source do not imply arbitrary combinations across multiple sources at an outpost.
- A stable outpost-wide resource list can coexist with different deposit geometry and fixed-extractor availability.
- A partial/negative research finding cannot be promoted into assignment COMPLETE while a required controlling question remains unanswered and authorized avenues are available.

**No D5W finding by itself authorizes a retail experiment, D5P observer repair, bug diagnosis, repository integration or B6 publication.**
