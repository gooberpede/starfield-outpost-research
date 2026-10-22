# Codex research brief — RG2-C1B: Native UI Resource Oracle Qualification

**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)  
**Authority:** offline research, static analysis and disposable/synthetic prototype qualification **only**. No live Starfield execution, process attachment, plugin deployment, game launch, game save creation, or changes to protected files under this brief. A future separately approved live task may use a disposable session, including tolerable post-capture instability.  
**Release:** B6 remains on hold. No staging, committing, pushing, publishing or cleanup.  
**Baseline:** committed/synced RG2-C1A and preceding RG1, RG2-A/A1/F1, RG2-C1, D1 results. Verify HEAD, working-tree/index state and pinned binaries before starting; do not assume an unqualified target version.

## 1. Objective and decisive question

Qualify a **native resource-list oracle** capable of obtaining previously unavailable, identity-bound information about which resources Starfield actually associates with an outpost and **which underlying population supplies each identity**. Prefer a narrow capture of resource-list inputs and output over full vein-geometry capture if scientifically discriminating.

Test whether `FUN_141578500` (static VA `0x141578500`, RVA `0x01578500` on pinned Starfield.exe 1.16.244.0) is relevant to the *extractor build catalogue* shown by the player, as opposed to an adjacent available-resource UI. **Do not assume equivalence.** Trace the actual dataflow and distinguish:

1. spatial area resources from `FUN_1421e07d0` → `FUN_1421e0f50`;
2. atmosphere-derived resources (`FUN_14076bd20` / related helper);
3. biome-derived resources (`FUN_14078ee90`, including Water special handling);
4. the three-population UI union / typed-row builder `FUN_141578500`;
5. extractor catalogue eligibility/filtering and item display;
6. selected extractor's placement/admission gate `FUN_1421f68f0` and any distinct location/footprint conditions;
7. cached/retained state and skipped refreshes.

The existing static UI resource-list contract is evidence for a **three-population UI list**, not yet proof that this function feeds the pictured **extractor catalogue**. A negative trace is an informative result; identify the actual catalogue producer/consumer when evidence permits, otherwise give a bounded unresolved edge and a capture route that still produces useful new native information.

## 2. Prior evidence, locations and constraints

Read current repo versions of `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md` and linked research. Mandatory starting points:

- `docs/experiments/native-availability-map/output-contract.md` and `region-lifecycle.md` — three operation-owned populations, previously observed UI folds, refresh/retention distinction, native addresses and limitations.
- `docs/experiments/resource-geometry-observation/native-contract.md`, `report.md`, `cases.md`, `acquisition.md` — observation designs and geometry consumer boundaries.
- `docs/experiments/resource-region-acquisition/report.md`, `plan.md`, `native.md` and `verification.md` — RG2-C1A method comparison, mitigations and scientific shortfall of a repeat-video experiment.
- `docs/experiments/resource-geometry-mature-context/f1-reconciliation.md`, `f1-water.md`, `seed-lineage.md` — actual contradictions, Water bypass and Copper positive control.
- `docs/experiments/disappearing-deposits/report.md` — optional stability case, no established incident mechanism.
- Original source/native registers and protected evidence receipts from these reports; inspect existing local exports and implementations rather than asserting new offsets. Reuse evidence from maintainer-owned `starfield-resource-research` only when directly relevant, preserving provenance and permissions.

All native claims are scoped to the binary version/hash they were obtained from. `FUN_` labels are Ghidra analysis labels; use measured module base plus RVA for any eventual ASLR-adjusted live VA. Do not conflate static VAs, runtime pointers, saved tokens, FormIDs, handles, object member offsets or stream offsets.

## 3. Diagnostic cases and success measurements

**P1: Save52 Feynman V `Cu Co Ni IL`, Ionic Liquids.** Native oracle must distinguish spatial inclusion from atmosphere/biome inclusion, retained rows and catalogue filtering. Existing screenshot and saved extractor establish observed gameplay presence, not native origin or geometry.  
**P2: Same Workshop, Copper.** Positive control: frozen conditional singleton disk contains saved extractor; use without tuning prediction or assuming geometrical equivalence.  
**P3: Save52 Carinae III-a `Rc Fe`, Iron.** Independent resource-list contradiction.  
**R1 (optional): Feynman VIII-b Au/Sb/Cu.** Potential source/population stability diagnostic only. Do not chase or presume reproduction of historical substitution. Preserve correction that other Feynman V `Cu IL F` outpost is **active**, but it is not mandatory for this test.

State exact independently confirmed Workshop/beacon/extractor identity joins and distinguish saved historical state from currently loaded runtime state. Frozen v1/v2 geometry predictions must remain untouched; no counterfactual parameter-fitting.

## 4. Required offline research and acquisition engineering

**A. Follow the native UI dataflow.** Build an evidence-pinned graph from each resource-population writer, update/refresh condition and retained storage to `FUN_141578500`, then trace *specifically* to the extractor build menu/catalogue. Locate catalogue resource-filter decisions, item list construction and refresh triggers if supported. Distinguish what is definitely observed/static from unknown linking edges. A menu row is not proof of local placement or extraction; identify the point where this distinction arises.

**B. Choose a minimal observation.** Prefer one naturally executing boundary that provides: case/outpost association, three population identities with source tags, freshness/retention indicator, final merged resource identities and, where provable, catalogue results. Name precisely which information the observed path can and cannot supply. If the output/typed rows are not the catalogue's feed, provide a parallel minimal catalogue observer or a defensible native spatial-list probe. An oracle returning only the already visible names without **native population provenance or context** is insufficient.

**C. Design a real collection route, not another unexecuted feasibility objection.** Compare reasonable offline-implementable acquisition architectures (e.g. narrow debugger probe, new bounded instrument/plugin, native one-shot snapshot, available existing observer components under requalification). Make an engineering recommendation with an ordered route, exact interception/read points, fields, copying strategy, required dependencies, acquisition trigger, expected evidence format and reproducibility instructions. A rejected method must include a concrete mitigating design or a reason to prefer the chosen one. The older observer remains NO-GO **as-is**, but prior components may be reused after explicit requalification.

**D. Prototype what can be tested offline.** Where feasible, implement a disposable synthetic/harness prototype demonstrating identity serialization, bounded record copying, resource-population tags, loss detection, durable write/flush and interpretation. Do not falsely claim synthetic success qualifies retail object lifetime, concurrency or actual UI ancestry. No live Starfield testing under C1B.

**E. Design the first *scientifically discriminating* live experiment** for a later separately approved brief. Expected ordinary successful run must reveal new, previously unavailable native information (e.g. IL membership in actual spatial collection, freshness, Workshop-bound native origin, catalogue filter input), not merely produce another recording of stable IL visibility. Specify exact steps, minimal permissions, receipt checks, stop/abort criteria, result classifications and escalation to the area callback if needed. The plan may permit a game crash **after** complete/durable receipt; failure before useful receipt does not count as success.

## 5. Safety and authority policy to reflect

The maintainer explicitly permits **destructive or unstable disposable observers** if they reliably return meaningful data first. Clean retirement and post-capture playability are *desirable*, not absolute success conditions. The priorities are:

1. **Never damage or overwrite original/protected saves or research inputs.** Specify a genuinely isolated live save environment for any later capture (save-path/autosave/cloud-sync checks; read-only master copies, verified hashes, disposable writes; explicit abort if separation fails). This brief does not authorize doing it live.
2. **Obtain authentic, correctly identified, durable observations before destabilization.** Flush/acknowledge, validate framing/checksums and record `LOSS`/partial results honestly. Crashing after secure capture may be allowed; crashing before receipt is a failed acquisition.
3. **Keep the risk domain bounded.** No uncontrolled system effects, privileged modification, unguarded reads of freed memory, corrupting shared project files or relying on speculative pointer ownership as fact.
4. **No false safety claims.** Distinguish theoretical path, offline prototype, qualified live method and successful actual capture. Disposition may remain `CONDITIONAL-WITH-MITIGATION`, but the recommendation must be actionable.

Explicitly identify which previous C1/C1A gates are relaxed by disposable-session tolerance, and which remain mandatory for evidence correctness and preservation.

## 6. Scientific result contract

Provide a decision table for normal possible oracle receipts, at minimum:

- IL/Iron in native **spatial** population, correct identity and fresh state → strong evidence model input/source/region discrepancy; escalate to region geometry only if needed.
- IL/Iron absent spatially but present in **biome/atmosphere** population → investigate resource admission/list semantics rather than infer missing vein.
- IL/Iron absent from all three but appears in catalogue → catalogue source/filtering/retention or an untraced fourth route; demonstrate rather than assume.
- Spatial membership only from retained state / no area refresh → cannot claim contemporary generated geometry; target refresh provenance.
- Spatial inputs and catalogue provenance unbound → mark `UNKNOWN`, not `ABSENT` or successful validation.

Keep source identity, temporal freshness, population ancestry and actual downstream consumer outcome separate. A native resource identity list is a *resource oracle*, not a geometric-region oracle, and cannot by itself settle the geometry algorithm. Describe its highest-value next escalation.

## 7. Durable deliverables

Create a dedicated directory `docs/experiments/resource-ui-oracle/` with at least:

- `report.md`: research answer, evidence-backed findings, residual uncertainty, actionable selected acquisition method and next step.
- `dataflow.md`: function/branch/source evidence map, provenance of three populations, native UI-to-catalogue link status, semantic distinctions.
- `capture-contract.md`: minimum fields, ownership/coherence assumptions, negative/retained/partial outcomes, receipt schema and attribution rules.
- `methods.md`: comparison, selected engineering architecture, risks and concrete mitigations, offline prototype results if any.
- `pilot-plan.md`: separately-authorized future live procedure, save isolation and evidence integrity, stop conditions and decision table.
- `review.md`: frozen AC1–AC8 matrix, independent findings, corrections and final disposition.

Update existing index/navigation/state/register documents *only where the project rules require*, and avoid redundant or misleading claims that native capture has occurred. Retain prior snapshots and result limitations; do not overwrite RG2-C1A's recommendation or frozen predictions. Register any created code, tests, licenses/provenance and protected-source hash pins according to existing conventions. Documentation and software must not embed proprietary native exports, copyrighted decompilations, private saves or screenshots without the established approvals.

## 8. Frozen acceptance criteria

**AC1 — Scope, authority and preservation:** Verified baseline and protected hashes; strictly offline work; no game launch/attach, save writes, original-file modification, staging, commit, push or publication.

**AC2 — Existing-evidence and source diligence:** Trace inherited research with exact versioned evidence, address-domain discipline, existing capture outcomes and maintainer-owned prior research where relevant; no fabricated joins or repurposed old observer.

**AC3 — Catalogue lineage:** Establish or explicitly bound the UI-union-to-extractor-catalogue relationship using native evidence; account for distinct resource populations, refresh/retention and construction/placement gating.

**AC4 — Native oracle specification:** Concrete minimum capture contract that yields correctly identified **new native information**, especially population ancestry and fresh/retained state, with explicit limits and missing-data handling.

**AC5 — Actionable engineering route:** Deliver **at least one technically specified acquisition architecture** capable in principle of obtaining AC4's new evidence. Every material unresolved feasibility/risk issue has an actionable mitigation or qualification test, objective outcome and fallback. All-NO-GO without a constructive route fails. A repeated screenshot or UI video alone cannot satisfy AC4/AC5. Report conditional status honestly.

**AC6 — Executable-in-principle first pilot:** Single bounded later-authorized experiment for P1+P2, escalation to P3 if warranted, optional R1 only if informative; save isolation, exact triggers, expected receipt, durable export, scientific discriminator, pass/fail and abort conditions. Expected normal outcome must add information.

**AC7 — Durable evidence and reproducibility:** Complete documents/source pins, bounded offline validations and accurate confidence; no mutated frozen predictions or invented live results.

**AC8 — Independent critical review and exact delivery:** Independent reviewer checks AC1–AC7 and explicitly challenges claimed catalogue lineage, scientific information gain, mitigation credibility and safe save handling. Correct identified defects, preserve review history, then regenerate and verify complete and task-only forward/reverse exact patches, manifests, protected-input/HEAD/index preservation. Provide final local review receipt and exact paths/hashes; no commit.

## 9. Delivery / decision rules

Before finishing, explain clearly **what the proposed capture tells us that the user's existing IL screenshots and saved extractors cannot tell us**. If catalogue lineage cannot be proven offline, identify the smallest experimentally discriminating unresolved edge, specify exactly how to observe it, and retain `UNKNOWN`; do not manufacture an affirmative link. A conditional instrument must still have a concrete build/qualification trajectory.

Deliver the above documentation, source/test changes if genuinely justified, independent review, final file manifest, complete and task-only diffs, measured hashes, and brief status summary. Request separate maintainer authority before any live pilot. No further planning/permission round is needed merely to perform this **offline** assignment.
