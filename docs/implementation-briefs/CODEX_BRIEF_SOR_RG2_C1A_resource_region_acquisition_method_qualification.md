# Codex Research / Engineering Brief — RG2-C1A
## Resource-Region Evidence Acquisition: Method Qualification and Actionable Route

**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)  
**Authority:** This brief authorizes **offline investigation, bounded engineering prototypes and qualification only**. It does **not** authorize launching/controlling Starfield, attaching to a live process, installing hooks, operating Creation Kit, producing saves through gameplay, or making any other live acquisition. Such activities may be designed and explicitly proposed here, but require a separate live-execution approval.  
**Release:** B6 remains on hold. No publication, staging, commits, pushes, or cleanup.  
**Submission workflow:** Codex performs the work, obtains independent critical review of the exact final snapshot, and provides complete and task-only diffs for maintainer review. The maintainer will commit/sync separately.

## 1. Background and scientific target

RG1 and subsequent RG2-A, RG2-A1/F1 reconstructed conditional native inorganic-resource geometry and exposed substantive differences from gameplay at mature outposts. RG2-C1 designed a coherent observation contract, preferentially at `FUN_1421e07d0 → FUN_1421e0f50`, but concluded that safe coherent acquisition is unqualified due to object/owner lifetime, synchronization and source/cache epoch correlation, copying costs and reliable retirement. The old observer remains **NO-GO**.

The objective now is to establish **how to acquire genuinely new evidence**, not to produce another list of reasons that acquisition is difficult. Scientific comparisons should distinguish:

1. Actual generation inputs differ from the frozen offline model.
2. Inputs match but produced paths/regions differ.
3. Inputs and regions match but cached-population selection, spatial consumer or extractor-admission decisions differ.
4. Region population or effective operands change with loading, cache or lifecycle events despite apparently identical saved context.

Do not assume the generator is bug-free or that every relevant input is stable. Conversely, do not attempt to reproduce or determine the root cause of the historical disappearing/mutating-deposit incident.

Read and honor the repository's current `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/PERMISSIONS.md`, `docs/templates/completion-contract.md`, and relevant experiment protocols. Read the latest committed RG2-C1 materials (`docs/experiments/resource-geometry-observation/`), RG1 (`docs/experiments/resource-geometry/`), RG2-A1/F1 (`docs/experiments/resource-geometry-mature-context/`), D1 (`docs/experiments/disappearing-deposits/`), and pertinent native availability/source registers. Cross-project work in maintainer-owned `starfield-resource-research` is allowed read-only where relevant, locally or GitHub, with evidence provenance and source boundaries respected. Do not import third-party code or unpublished/proprietary raw data into authored public-facing material.

## 2. Frozen target cases

- **Primary failure A:** Save52 active **Feynman V Cu Co Ni IL**, Ionic Liquids — saved extractor and gameplay-positive vein, conditional offline negative.
- **Primary failure B:** Save52 active **Carinae III-a Rc Fe**, Iron — saved extractor and gameplay-positive veins, conditional offline negative.
- **Positive control:** Feynman V Copper — frozen predicted singleton disk encompasses the saved extractor; screenshot suggests roughly circular patch. This is a *conditional* agreement, not established native equality.
- **Optional stability comparator:** **Feynman VIII-b Au Sb** (Gold/Antimony/Copper). The D1 historical report is eyewitness evidence of possible mutation, not an independently captured before/after incident. Its inclusion tests the *potential instability of inputs, selection or cache lifecycle*, not reproduction of the bug. Do not require a mutation to occur.

The other Feynman V outpost, **Feynman V Cu IL F**, is **not deleted**; the earlier assertion was retracted. It remains nonmandatory and must not be silently conflated with the primary Feynman site. Use robust Workshop/body/reference identity joins; distinguish save tokens from runtime handles and source pointers.

Preserve all frozen prediction versions, primary saves and research evidence unchanged. Any new scenario/model is separately versioned; do not adjust inputs to fit observed deposits.

## 3. Mandated method comparison

Evaluate three distinct acquisition families seriously, using concrete evidence rather than generic dismissal:

**A. Save-based / controlled-state capture.** Existing and newly produced saves (ordinary or controlled), repeatable reload/travel/build sequences, serialised resource/Workshop/source/extractor and other effective state differences. New saves **may be planned and recommended**, subject to separate gameplay execution authority; no requirement that entire generated region arrays be serialised. Identify exact new observable fields, or say explicitly what cannot be obtained from saves.

**B. Non-invasive live sampling.** In-game scanner/overlay, extractor placement/eligibility and output results, fixed point/area sampling, coordinate registration, screenshot/video and/or game-exposed diagnostics where legitimately available. Define a sufficiently precise operator procedure, positional tolerance and receipt format; separate rendered/UI observations from native-region facts.

**C. Native runtime sampling.** A small, coherent observation on a natural production/consumption path, preferably RG2-C1's region-consumer candidate where warranted. Explicitly assess debugger, plugin/hook, snapshot/quiescence or other technically grounded architectures; do not assume a hook, memory copy or debugger attach is safe. Reuse the prior NO-GO and acquisition-failure record, not its rejected mechanics.

Methods may be combined in a staged campaign. Compare what each actually adds, the questions it discriminates, engineering effort/operator effort, safety, reversibility, failure detection, data volume, coherence and identity/epoch confidence. The objective is **independent new evidence**, not another run of the conditional RG1 evaluator using identical assumptions. A narrow but valid new measurement counts if it rules in/out an important explanation.

## 4. Mandatory constructive-outcome rule (hard gate)

**The investigation MUST conclude with at least one specific, technically actionable method for collecting or sampling new evidence, online or offline.** It may be:

- **QUALIFIED:** feasibility and safety demonstrated to the specified bounds; or
- **CONDITIONAL WITH MITIGATION:** an implementable route whose residual risks and prerequisites are explicit, together with concrete bounded mitigation/qualification steps, objective pass/fail tests and a safe failure response.

**An all-NO-GO conclusion is a failed assignment unless accompanied by at least one such constructive, falsifiable route.** A catalogue of obstacles, vague suggestion to investigate further, unsupported promise that a technique is safe, or speculative future technology does not satisfy this criterion. Codex can reject any individual method and can conclude that no live *execution* is currently safe. It must still propose a viable route to useful acquisition, including the specific engineering work that would make it qualified, or a lower-risk independent sampling alternative.

Do **not** falsify qualifications to meet this gate. If a route is conditional, label it conditional. Identify the smallest viable first receipt and explain exactly why it contains new independent information. If the richest native path proves too risky, fall back to a bounded save/gameplay sampling path with a measurable discrimination goal instead of abandoning all acquisition. A plan incapable of generating any new relevant observation is not viable.

## 5. Native capture qualification — if proposed

Ground the proposed native implementation in actual call sites/structures and source evidence, including:

- selected Workshop/extractor and effective base form, selected source and *actual* cached region population;
- per-use position/radius/upper bound, coordinate frame and transformations;
- owner/packed cell seed and effective BIOM/RSGD/family/weight inputs **where actually observable**;
- ordered geometry or a rigorously bounded subset, actual accept/reject branch and extractor-admission outcome;
- coherent lifecycle/epoch association, cache readiness, invalidation/replacement, and complete versus partial populations;
- object lifetime, concurrency, synchronization or safe-point strategy; snapshot ownership, array bounds, time/copy budget and nonblocking behavior;
- installation, uninstall, detachment and **retirement** guarantees, including prior queued-breakpoint/trap failure modes;
- integrity, hash/identity, truncation/loss signals, tamper-free collection and abort/recovery controls.

Distinguish capture of generation *inputs and constructed geometry* from observation of *already cached geometry* at consumption. A pointer address, equal content hash or successful callback alone does not certify lifetime, epoch or correct resource classification. The plan must not become circular validation against the same inferred source-frame mapping.

For each serious failure mode include **risk → mitigation → bounded verification → objective pass/fail → abort/fallback → residual uncertainty**. Synthetic/disposable offline fixtures may be prototyped and tested now, respecting local permissions. Do not interpret synthetic success as proof of safe deployment in Starfield.

## 6. Required staged procedure and replay decision tree

Deliver a ranked first-experiment proposal with:

- exact case identity, prerequisite state/save and operator/engineer preparations;
- **smallest useful initial observation** (favor an extractor-tied IL or Iron measurement and Copper control, but justify order); instructions sufficient for a future separate execution brief;
- coordinate/identity registration and tolerance, repeatability checks and optional cache/load transitions;
- schema of raw receipts, timestamps/epoch evidence, evidence provenance, loss and negative-result semantics;
- offline comparison against **frozen** RG1/RG2-A1 predictions and precise branching rules for “different inputs / same inputs different regions / matching regions different consumer / unstable epoch / insufficient evidence”;
- clear triggers to escalate from save or manual observation to qualified native sampling, and stop conditions that prevent endless testing;
- optional Feynman VIII-b repeated-observation plan only if it adds relevant evidence without turning into a bug-reproduction hunt.

Specify what a successful *negative observation* means and which missing/context-incoherent receipts must be reported **UNKNOWN** or **NOT TESTED** rather than “no resource.” Include a fallback plan if the preferred acquisition method fails qualification or its first sample is inconclusive.

## 7. Deliverables

Create a durable bounded package under `docs/experiments/` following project conventions, with at minimum:

1. Research report, ranked recommendation and honest qualification status.
2. Method comparison (save / non-invasive / native), including concrete inputs, outputs and discrimination matrix.
3. **Actionable acquisition plan** with exact first experiment, receipts, fallback/escalation and separable execution authority.
4. Native acquisition engineering notes / safety qualification matrix, if native is selected or conditionally proposed; otherwise a documented explanation of why a non-native route meets the hard gate.
5. Input/cache/lifecycle instability considerations scoped to algorithm operands rather than bug reproduction.
6. Verification/test record, provenance/pins, limitations, independent-review finding, navigation/source-register updates as required.

Keep local private evidence, raw saves, executable extracts, debugger databases, proprietary binaries, scratch captures and unapproved third-party materials outside authored public deliverables per existing policy. Supply no invented live measurements. Reuse existing documented fields/code rather than rediscovering unrelated mechanics.

## 8. Frozen acceptance criteria — AC1–AC8

**AC1 — Authority and input integrity.** Offline-only research/prototypes; no live operations, installs or modifications to protected source assets; existing NO-GO enforced. No staging/commit/push/publication. Provenance and input identity recorded.

**AC2 — Bounded prior-work reuse.** Reuse RG2-C1/F1/RG1/D1 and relevant maintainer-owned prior research with explicit attribution; avoid open-ended new reconnaissance and speculative source equivalences.

**AC3 — Serious method alternatives.** Evidence-grounded comparison of save-based, non-invasive live and native sampling, each with independent observation value, scientific discrimination and realistic costs/limitations. No family dismissed solely because it cannot solve all three failure classes by itself.

**AC4 — Concrete safety and mitigation.** Significant risks have paired mitigation, bounded verification, objective pass/fail, abort/fallback and residual risk; previous unsafe observer not resurrected; no circular coherence or false safety proof.

**AC5 — MANDATORY VIABLE ROUTE.** At least one QUALIFIED or explicitly CONDITIONAL-WITH-MITIGATION *actionable evidence acquisition method* that produces new relevant information. Every outstanding blocker on the recommended route has a practical qualification/mitigation plan. Reviewer must **FAIL AC5** if all alternatives are rejected without such a constructive route. No requirement to claim live readiness prematurely.

**AC6 — Specific first experiment and escalation.** Reproducible prospective protocol, identity-bound case, exact receipt and discrimination decision tree; staged order, stop conditions, fallback and optional stability comparator; no bug reproduction requirement.

**AC7 — Durable, reproducible package.** Reports, matrices, native/source pins, measured offline checks, transparent UNKNOWN/NOT TESTED, frozen-prediction integrity, cross-links, and authorized tests/prototype receipts with limitations clearly distinguished.

**AC8 — Independent critical review and delivery.** Independent reviewer assesses the **exact final snapshot**, explicitly challenges AC5 practicality and mitigations, checks AC1–AC7 and historical constraints, requires corrections/re-review as needed. Provide complete and task-only exact diffs, hashes, manifests, forward/reverse patch verification and protected-input checks. Review records must not certify safety beyond evidence.

## 9. Execution and final response contract

Before work, inventory the workspace and report unrelated changes; comply with project workflow. Read the existing completion contract and use its required final delivery fields. Work only within authority. Avoid unnecessary expansion of provenance or automatic cleanup. Exact original source/native address claims must be anchored to retained evidence. Do not modify frozen prior outputs or retroactively change earlier scientific conclusions without versioned correction.

Final response must give: the selected route and status (QUALIFIED / CONDITIONAL-WITH-MITIGATION); its specific initial observation and which hypothesis it can discriminate; principal engineering risks with objective qualification and fallback; exact files and validation performed; independent review AC1–AC8 result; complete/task-only patch paths and hashes; exclusions and assurance no live operation, staging/commit/push. **A generic conclusion of “no safe method exists” without a constructive acquisition plan is explicitly nonconforming.**
