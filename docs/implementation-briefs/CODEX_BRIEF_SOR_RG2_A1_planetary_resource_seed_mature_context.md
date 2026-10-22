# Codex research brief — RG2-A1: Planetary Resource Seeds and Mature Source-Context Reconstruction

**Project:** `D:\Projects\starfield-outpost-research`  
**Type:** bounded offline native/definition/save reconstruction, with original analytical checks  
**Status:** proposed for maintainer invocation; no execution or publication authority is conferred merely by storing this document  
**Game baseline:** one investigated retail executable, **Starfield 1.16.244.0**. Historical save-header versions are evidence provenance, not additional researched executable builds.

## 1. Research question and required result

Explain how Starfield derives or retrieves the deterministic inputs that generate inorganic resource vein geometry for an ordinary planetary outpost, and use that explanation to remove, if evidence permits, the source-context gap between the qualified Kreet cases and active mature Save52 outposts.

**Do not assume** that a seed must reside in a saved game, that Creation Kit's **Planet Resource Seed** directly seeds vein geometry, or that the game uses a resource overlay. Trace each actual native consumer and producer. A stable geometry may be regenerated from installed planetary data, effective settings, spatial identities and derived per-source seeds. The goal is a causal model and usable inputs, **not** an exhaustive proof against speculative other seeds or a complete terrain renderer.

This is a substantive attempt to produce **frozen mature vein predictions** where inputs can be qualified, not an investigation that stops after cataloguing obstacles. A concrete, evidenced missing dependency is an acceptable qualified limit only after serious bounded attempts to resolve it through existing offline material.

## 2. Required sources and prior-art review

Read the current project governance and baseline first: `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, and publication/third-party policies. Read at minimum:

- `docs/experiments/resource-geometry/` (RG1: `report.md`, `native.md`, `evaluator.md`, `validation.md`, relevant functions/source pins/receipts, code under `research/resource-geometry/`);
- `docs/experiments/resource-geometry-live-prep/` (RG2-A: `report.md`, `prediction-contract.md`, `cases.csv`, `case-selection.md`, `predictions-v1.json`, `freeze-v1.json`, source and review records);
- `docs/experiments/native-availability-map/` (`region-dependencies.md`, minimum inputs, native source maps, uncertainties and review);
- earlier planetary/resource-selection, biome, geographic-frame and saved Workshop/disabled-state research, including the original Kreet owner-key capture and its hash/epoch provenance.

**Sibling project prior research:** inspect maintainer-owned `starfield-resource-research`, locally if present and via `https://github.com/gooberpede/starfield-resource-research` as appropriate. Search specifically for PNDT/RSCS, per-biome selection, resource seed, Kreet, CRC/MT, generator context and the Creation Kit Resources tab. Consult `starfield-resource-reproducer` only where genuinely relevant to selection/seed rules; **do not equate its validated resource-set algorithm with spatial vein generation**. Record exact repo/commit/file anchors and what each establishes. Prefer the locally pinned work where versions differ. Prior work is evidence to evaluate, not an authority to silently import assumptions.

Respect authorship and third-party permissions: maintain provenance and attribution for any consulted external source, check permission before incorporating code or substantive copied material, retain only original analytical explanations and bounded attributable excerpts where permitted. Do not copy proprietary executables/ESMs/BA2s, Ghidra databases, decompiled C/ASM, raw disassembly dumps, or third-party datasets into Git. No generalized third-party reuse authorization follows from reading a public repo.

## 3. Seed lineage: Creation Kit to generation

Use the maintainer's Creation Kit screenshot as a concrete lead: Kreet's Resources tab shows **Planet Resource Seed `-1452258485`**. Treat the screenshot as an observed UI value, **not** established storage location, unsigned/signed representation, scope, or vein-generator seed.

Trace, as far as existing installed/static evidence permits:

1. Which installed record field(s), settings, initialization and UI plumbing produce the displayed seed; how the signed UI value corresponds to any underlying byte representation; and whether Apply/Apply Random imply mutation paths (do not invoke them).
2. Actual native consumers of planetary resource-selection inputs (including PNDT/RSCS and BIOM/per-biome inputs), with separation between *which resource is eligible/selected* and *where its vein paths are generated*.
3. RG1's surface-pattern seed, its default `0x20201215`, body/system selection, CRC/MT input path and effective override/configuration boundaries.
4. RG1's **per-vein CRC/MT seed contract**: packed cell/source key and procedural-manager `+0x80` owner value, derivation of that owner value and the spatial source identity/frame; explain which are installed, serialized, derived, cache-held or transient.
5. How resource ordering, masks/weight, atmosphere and selected family/RSGD affect sequence consumption and resulting geometry. Do not invent unobserved environment overrides.

Provide an **operand-provenance table** with input, exact producer, consumer, domain/type, baseline/source pin, current coverage and how to obtain it for an arbitrary qualified planetary body. Where negative claims are made, state the inspected path and bounds.

## 4. Symmetric Kreet versus mature reconstruction

Construct a side-by-side dependency matrix for:

- Kreet `SOR-002` (Save25), `SOR-003` (same Kreet save), and Save39;
- **active** Save52/HIST-0267 `Feynman V Cu Co Ni IL` (mixed-biome) and `Carinae III-a Rc Fe` (single-biome).

**Exclude `Feynman V Cu IL F`: it is a deleted outpost, not a validation candidate.** Remove it as RG2 reserve R2 in prospective documentation and any candidate-selection output, preserving the historical RG2-A record and prior frozen predictions. Apply established disabled/deleted state and Workshop membership evidence to *all* candidate searches; a surviving reference, name, or coincident descriptor is not proof of an active outpost. Do not study deleted outposts as a separate subsystem.

For Kreet, trace exact earlier evidence for owner suffix **`259487`** (including whether it came from an actual live manager field), associated frame, capture version/hash and observation epoch. Do not generalize `259487` as a planet-record identity merely because it happens to agree in Kreet. Determine whether the same producer/lookup can be reconstructed from definitions or saved identities for Feynman/Carinae.

For the mature cases, reuse exact saved Workshop→parent→secondary→descriptor joins and investigate:

- The specific actual generator owner/context identity and any encoded manager suffix;
- Source-native origin versus saved site origin and the candidate translations (Feynman `(-2800,-200)`, Carinae `(-900,-800)` native units);
- Effective resource/per-biome family, mask, atmosphere and registration order;
- Differences arising from transient loaded context versus available installed or saved data.

Trace the *input acquisition path* rather than merely fitting a translation to a desired resource list. Compare competing candidate frame/owner hypotheses against independent records/call sites. Explicitly separate a derived candidate from a qualified generator input. Preserve fixed RG2-A Kreet prediction v1; corrected science requires new, versioned predictions and rationale.

## 5. Evaluator and verification deliverables

If actual mature input sets are established, use the existing original RG1 evaluator to generate complete relevant ordered sources and vein geometries for the two active mature sites. Make input provenance machine-readable, freeze spatial predictions **before any subsequent live observation**, and include interior/exterior, positive/negative and edge-discriminating samples with uncertainty flags. Reuse the certified nominal 150-unit intersection logic; do not treat UI resource totals, named extractor installations or the nominal biome set as direct geometry oracles. Additional tests for new source/weight branches should be independent of the primary path where feasible.

If an input remains unresolved, document *what was tried*, specific source/call evidence, which input is still unknown, alternatives rejected by concrete counterexamples, and the **smallest discriminating next observation**. Do not silently generate fictional mature predictions; an `UNKNOWN` result is better. Don't halt simply because the first archived path lacks a field when further in-scope static avenues exist.

Produce clear answer-first prose and original, accurately scoped pseudocode where it improves the seed-generation explanation. New text must conform to B2 native address/offset/identifier conventions; the earlier noted editorial defects in `region-dependencies.md` are **separate release-readiness work**, not authority to rewrite that historical report.

## 6. Execution authority and safety

**Offline only.** Authorized: read existing research, user-owned sibling repo/public GitHub research with provenance, installed data and previously authorized local analysis sources; bounded static/native/definition/save inspection; original offline scripts and deterministic/synthetic tests; write research artifacts, code where necessary, review receipts and diffs in project-designated locations. Read protected inputs without modifying their bytes or provenance.

**Not authorized:** launching Starfield or Creation Kit, debugger or process attachment, SFSE deployment/live observation, new manual saves or game actions, mutation of original saves/installed game/third-party data/Ghidra project state, unreviewed external downloads, publication, Git stage/commit/push, evidence release, or B6 execution. Existing observer NO-GO decisions remain binding. No deletion or bulk `.local-work` cleanup. Observe active disk-space/output/integrity safeguards and sandbox/review-scratch lifecycle controls from project policy.

## 7. Frozen assignment completion contract — AC1–AC8

**Task type:** bounded scientific reconstruction and offline validation; not live validation or an implementation for a particular mod.

| Criterion | Mandatory acceptance and evidence |
|---|---|
| **AC1 — Authority and integrity** | Identify the exact baseline, starting HEAD/index, permitted files/source pins and protected evidence; show no unauthorized operations or input changes. |
| **AC2 — Relevant prior research and permissions** | Search project and sibling research, record exact source provenance/usefulness, attribution/reuse decisions and substantive leads/counterexamples. |
| **AC3 — Creation Kit seed provenance** | Trace the observed Kreet Planet Resource Seed value through supported record/UI/native path(s), distinguish seed domains and signed/unsigned presentation; bounded unknowns are explicit. |
| **AC4 — Complete scoped generation operand model** | Connect surface selection and vein CRC/MT seed inputs to actual producers/consumers, document storage/derivation/lifetime and testable generator-owner/source-frame claims. |
| **AC5 — Active-site symmetry and correction** | Verify active membership, exclude deleted Feynman reserve from prospective population, establish side-by-side Kreet/Save52 inputs with exact references and genuine missing edges. |
| **AC6 — Mature reconstruction and predictions** | Substantive bounded attempt for both active mature cases; qualified inputs yield original evaluator predictions and spatial tests, otherwise evidence-backed `UNKNOWN` with exact smallest blocker, not an unexamined stop. |
| **AC7 — Durable scientific report** | Answer-first model, numeric/source evidence, confidence and coverage, corrections/counterexamples, concise predictions or narrow follow-up, plus explicit RG1/RG2-A/B6 boundaries. |
| **AC8 — Independent review and delivery** | Independent adversarial review of actual tree/evidence against all AC1–AC8, defects remediated under the same brief, relevant deterministic checks, protected hashes, complete/task-only exact forward/reverse patches, change inventory and final reviewer verdict. |

**Negative/qualified closure:** scoped negative results require real inspected path coverage and discriminating controls, not inability to find a keyword, guessed alternate seed, or imagined runtime state. A true inaccessible required input or live-only measurement is an escalation with its exact dependency and preservation evidence. No retroactive weakening of ACs; material acceptance changes require maintainer approval.

**Continuation:** fix in-scope failures, perform warranted offline analysis/refactoring, rerun regressions, retain earlier failed review artifacts and acquire a genuinely independent final review. Avoid needlessly proliferating experiment scaffolding or broadening into all terrain procgen.

## 8. Deliverables and return format

Proposed location: `docs/experiments/resource-geometry-mature-context/` for `report.md`, `seed-lineage.md`, `kreet-mature-comparison.md`, `active-candidates.md`, `validation.md`, `review.md` and source references. Put minimal original code/tests under `research/resource-geometry/` or a clearly named sibling location only when needed. Include any new frozen prediction tables/JSON with versioned hashes; retain v1 unchanged. Add only proportionate navigation links in current reader indexes.

Return a concise implementation summary: scientific conclusion, AC1–AC8 matrix, verified inputs, new/changed files, permissions and third-party-use ledger, uncertainty and actual next dependency, tests/failures and independent decision. Supply **complete** and **task-only** diff paths, patch byte identities and inclusion/exclusion inventories. Do not stage, commit, push or propose public-release approval as a consequence of the research review.
