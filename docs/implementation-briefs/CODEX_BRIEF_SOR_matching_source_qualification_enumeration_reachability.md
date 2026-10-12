# Codex research brief — SOR: Matching-Source Qualification and Native Enumeration Reachability

**Assignment:** Offline research and deterministic analysis, continuing the committed and synced `starfield-outpost-research` repository.

**Authority:** This brief authorizes analysis of existing project sources, disassembly, save files, previously captured native evidence, and disposable offline tests. It does **not** authorize a Starfield launch, process attachment, SFSE deployment, modifying the 0.3.0 observer, memory patching, new native call injection, save mutation, staging, commit or push.

## 1. Research purpose

Our objective remains independent validation of the durable outpost-position algorithm. The latest 0.3.0 experiment provided 18 complete native candidate-query/helper chains but no enumeration (`E`), callback, center or grid observation. Subsequent offline reconciliation supports hierarchy mismatches as the reason all 18 chains bypassed the instrumented E boundary: 15 first mismatched at hierarchy `+0x0`, three at `+0x4`. Candidates **15 and 16** have overlay bit 0 set consistently in their recorded helper samples; that is a lead, not proof of eligibility. Q return value `1` means **continue scanning**, not successful enumeration or native positioning.

The immediate research question is: **Can ordinary, naturally occurring gameplay construct or select a source hierarchy that matches candidate 15 or 16 and actually reaches the required native enumeration path?** Also ask whether reaching E is genuinely required to obtain an independently attributable native positioning output, or whether a better-supported natural path exists.

The counterfactual source key `0x02b20e79528028e0` is a derived diagnostic vector, **not** an established landing site, approved game input or license to inject/manipulate state.

## 2. Begin with existing evidence; preserve its identity

Read `WORKFLOW.md`, the current Research Execution and Completion Protocol, relevant `AGENTS.md`, the latest committed research state, and at minimum:

- `docs/experiments/q-branch-030/captured-chain-analysis.md` and the associated reviewer record and raw-evidence index;
- Q-to-E control-flow and prior 0.2.0/0.3.0 experimental reports;
- source-key/hierarchy/terrain-frame static-analysis maps, deterministic model and all 23 frozen position predictions;
- controlled Save25–Save28 and mature corpus references where relevant, including provenance and integrity manifests.

Use the actual repository's names/locations when they differ from the shorthand above. Do not infer semantic identity merely from matching angular values or matching byte sequences. Retain original capture bytes and hashes; produce derivatives separately. No raw `.sfs`, game binaries, dumps, private configurations or sensitive evidence in patches or review ZIPs.

## 3. Primary investigation — both candidates

Investigate **candidate 15 and candidate 16 individually**, without treating either as settled by the other's apparent attractiveness. Deliver a directly evidenced comparison addressing:

1. **Candidate identity:** tie each Q invocation to raw descriptor, packed dynamic key, angles, observed helper values, native hierarchy A and overlay flag state. Determine whether there is a defensible reference/site/body/save-record identity join; explicitly distinguish exact joins, bounded correspondences and coincidences. Explain any changing runtime keys across sessions.
2. **Source-key origin:** trace the native producer(s) and callers of Q's packed source key, including the originating gameplay/terrain selection state, hierarchy unpack/pack/transformation, axis reflection, rounding and other branch-relevant operations. Follow upstream dependencies as far as necessary; do not stop at the first unnamed helper.
3. **Matching conditions:** recover the complete relevant equality and eligibility predicates for the Q-to-E route. Reconcile what is directly captured, statically established, derivable under stated preconditions, or missing. Consider bit 0 set for candidates 15/16 without assuming its full semantics or atomicity.
4. **Existing-reference bypass:** determine when a known site/reference is resolved before Q, potentially preventing the very Q invocation intended by a proposed revisit. Follow downstream caller handling of Q return `1`, as well as alternatives that produce grid/position outputs without E.
5. **Natural trigger feasibility:** identify what an operator could actually do with an existing Save27/28, another controlled Kreet save, or a separate save lineage to generate compatible source state. Distinguish a game-selectable landing/site context from a mathematically constructed key. Consider travel, new landing and outpost construction only when source-supported, not because they are convenient experimental motions.

Do not impose a gratuitous geographic distance rule, assume a 2D angular coordinate uniquely determines a terrain hierarchy, or conflate saved site anchors, beacon positions and durable workshop centers.

## 4. Deterministic offline verification

Implement or extend **small reproducible offline tools/tests as needed** to substantiate key derivations. At minimum:

- Reproduce the observed A/B hierarchy comparisons for all 18 previously acquired chains, retaining their identifiers and exact recorded operands.
- Explicitly test source-key packing/unpacking and tag/axis transformation around candidates 15/16, including reflected-axis and boundary counterexamples from prior research.
- Validate any proposed native path/predicate against actual recovered instruction sequences, not a model of its own assumptions.
- If a proposed matching source is derived, show exact key/hierarchy values and all unverified assumptions, and differentiate it from a naturally selectable source.
- Preserve all 23 frozen predictions byte-for-byte; do not change tolerances or controls to manufacture agreement.
- Inventory input/output hashes and ensure the protected saves, previous observer/analysis packages and evidence remain unchanged. Apply the standing 40,000,000,000-byte free-space guard on C: and D: to substantial local processing.

Use evidence-driven coverage (including negative controls) rather than an arbitrary number of repeat tests. Investigate discrepancies and fix in-scope problems within this assignment.

## 5. Evidence ledger and decision-ready experiment design

For each candidate, provide a compact evidence matrix separating:

- saved/native identity and supporting primary reference;
- actual captured source/candidate values versus constructed counterfactuals;
- necessary and sufficient predicates to enter E as far as established;
- ordinary gameplay action and the code-supported link to source production;
- chance of direct existing-reference bypass;
- remaining missing information and a precise observation that would discriminate possibilities;
- scientific value for full native position equivalence, not merely E reachability.

Rank concrete options as **ESTABLISHED**, **PLAUSIBLE WITH NAMED GAP**, or **UNSUPPORTED**; do not elevate a candidate because it looks geometrically close. Recommend **at most one** subsequent live scenario, if justified. If a new controlled save would be useful, specify exact starting lineage, attainable prerequisites, operator steps, checkpoint names/conditions and protected-save handling. Do not assume a level 3–4 Kreet character can reach high-level systems, or that console commands are permissible; operator feasibility and live actions require later explicit approval.

Assess whether E is truly on the shortest route to an identity-bound native terrain/grid output. If a distinct natural operation is demonstrably more direct, report it with its instruction-level provenance and constraints. This is a secondary comparison, not permission to abandon the primary two-candidate analysis.

## 6. Completion contract — outcomes and escalation

This is an **offline research assignment**, not an instrumentation implementation brief. Acceptable final scientific dispositions are:

**A — QUALIFIED MATCHING-SOURCE SCENARIO.** A specific, feasible *proposed* natural gameplay sequence is supported by reconstructed source production and relevant predicates for candidate 15 or 16 (or a demonstrably better native path), with remaining uncertainty and bypass risks explicit. This does not constitute authority to perform it or proof that it will hit E.

**B — COMPLETED NEGATIVE FINDING.** The authorized static, save and existing-runtime evidence has been thoroughly pursued and demonstrates why no qualifying natural trigger for either candidate can presently be supported within the investigated domain. Provide actual rejected leads/counterexamples, exact limiting dependencies and the shortest defensible alternative. Do **not** convert a difficult unknown into an unsupported impossibility claim.

A partial analysis, uninvestigated helper, unresolved in-scope test failure or speculative run card is **INCOMPLETE — CONTINUE**, not a completed result. The implementer owns in-scope corrections, retries and requalification. If a genuinely indispensable new live observation or permission is required, state exactly why existing authorized evidence cannot provide it, with a decision-ready proposal; use **ESCALATE** only for that real authority boundary, not as a substitute for offline investigation. Negative findings can be full scientific successes.

## 7. Agents and independent review

Follow the established Research Execution and Completion Protocol. Primary Codex owns integration and completeness. Use **at most two active sub-agents simultaneously**: a specialist, when productive, may independently trace source-key production/native conditions; a separate reviewer independently audits claims, raw-to-derived joins, alternative paths and all mandatory criteria. The reviewer should actively challenge premature termination and false identity/branch inferences, demand **REWORK** under the same assignment for in-scope defects, and use **ESCALATE** only for legitimate authority/safety barriers. Reviewer approval does not authorize runtime actions.

Reviewer must assess both positive and negative proposed endings, including whether a matching-source trigger would bypass Q through pre-existing references and whether pursuing E actually advances native equivalence. Record reviewer objections, implementer corrections and evidence-based adjudication.

## 8. Deliverables and review packaging

Return together:

1. Durable research report covering both candidates and native source-key/caller/control-flow reconstruction, with precise source/evidence references and confidence/coverage boundaries.
2. Per-candidate identity, predicate and acquisition feasibility ledger, plus executable offline verification tools/tests and receipts where appropriate.
3. Ranked, **decision-ready** next-acquisition assessment (at most one proposed natural live scenario), explicitly separating authorizations needed from what has already been established.
4. Acceptance matrix against this brief, independent reviewer verdict and rework history.
5. `-task-only.diff` and `-complete.diff` under `.local-work/diffs/`, `git status --short`, changed-file/omission manifests, reproducibility checks and hashes. Include new untracked **text** files in diffs. Preserve raw/private artifacts under ignored local work paths.

Do not stage, commit, push or conduct live work. Keep existing baselines, observer 0.3.0 and committed captured evidence intact. The maintainer will critically review the result and independently decide whether any next experiment should be authorized.

**Success principle:** Explain the actual native conditions and their practical reachability—or establish a well-supported scoped negative result. A further list of things Codex has not yet investigated is not completion.
