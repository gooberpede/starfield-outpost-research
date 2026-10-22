# Codex Research Brief — RG2-C1F: Native Resource-Generation Ancestry and Divergence Analysis

**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)  
**Authority:** Offline research, analysis, bounded read-only tooling and synthetic tests only. **No Starfield launch, debugger attachment, live capture, save creation or modification, instrumentation deployment, staging, commit, push or publication.**  
**Status:** Implementation/research brief for Codex; acceptance and scientific conclusions require independent review.  
**Build:** Starfield.exe `1.16.244.0`, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. Check local authoritative project pins before analysis.  
**Publication:** B6 remains on hold. Existing proprietary/native evidence and first-party saves remain local-only; abide by `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md` and the project completion contract.

## 1. Starting point and objective

RG2-C1D obtained a positively P3-bound spatial transfer payload containing Ionic Liquids (`Starfield.esm:0057d4`) and Copper (`Starfield.esm:0057cf`). RG2-C1E Phase B then obtained exact P3-bound native region observations and a transfer association. **The accepted Ionic Liquids region is a three-point native path absent from the frozen conditional prediction. Copper is an exactly matching singleton; two other accepted regions (`0057ce`, `0057cb`) also match the frozen result.** In the captured consumer traversal, Ionic Liquids and Copper share a source slot/wrapper (invocation-local ordinal 31), while the other two accepted resources use ordinal 54. The observed query XY and nominal radius match the frozen case. These facts do not prove matching *generation* source identities, inputs or cache epochs.

**Research question:** Which earliest independently supportable generation-source, resource-selection, competition, cache-history or generator-arithmetic dependency explains why the observed native Ionic Liquids region differs while the matching control regions remain unchanged? Locate the divergence with the existing offline evidence first. Do not invent unavailable native inputs or fit arbitrary parameters to the observed path.

**Expected result:** Either (A) a qualified offline reproduction or compelling correction with independent input provenance and preserved controls; or (B) a materially narrowed, falsifiable dependency and a concrete minimal next native observation, with a completed proposal/run card for maintainer approval. A generic “runtime context unknown” restatement without discriminating work is not sufficient.

## 2. Primary evidence and relevant earlier research

Read the latest committed versions, links, source manifests and protected local receipts where accessible, beginning with:

- `docs/experiments/resource-region-ancestry/phase-b.md`, `phase-b-review.md`, associated `review.md`, native contract, scripts and *unchanged* raw receipts under `.local-work/`.
- `docs/experiments/resource-oracle-retail/report.md` and the C1D associated-file/source/Workshop identity qualification.
- `docs/experiments/resource-geometry/report.md`, `native.md`, `evaluator.md`, exact prediction products; `docs/experiments/resource-geometry-mature-context/report.md`, `seed-lineage.md`, `f1-reconciliation.md`, frozen v1/v2 predictions and control definitions.
- `docs/experiments/resource-geometry-observation/native-contract.md`, `docs/experiments/native-availability-map/region-lifecycle.md` and source/key maps.
- D1 disappearing-deposits evidence only insofar as it informs concrete cache/source-lifecycle hypotheses. Consult the maintainer-owned `starfield-resource-research` locally or via the existing GitHub repository **only where relevant**, observing provenance and reuse permissions.

Use the source registers' exact native export identities, executable/ESM hashes and local primary evidence. Do not publish protected receipts, full decompilations, proprietary game files, raw saves or sensitive local paths. Never treat a prediction, analyst label, debugger pointer, saved token, native ordinal or hypothetical context as an observed generating identity.

## 3. Work packages

### WP1 — Freeze and independently verify observed-versus-predicted comparison

1. Record exact evidence identifiers, raw capture/analysis digests and the qualified bindings from P3 Workshop → updater/query → accepted callback region → resource identity → completed spatial transfer; retain distinctions between native observation, static source analysis and derived comparison.
2. Reproduce the four exact geometry comparisons independently, using original binary32 values, ordered points/widths, bounds and source/region identities. Do **not** regenerate or edit frozen RG1/RG2 v1/v2 predictions. Report the three matches and Ionic Liquids mismatch explicitly, including any incompleteness from callback short-circuiting.
3. Determine precisely what ordinal-31 wrapper/source equality establishes **at consumption**, and which additional source identity and generation-epoch joins it does not establish. Source map positions, pointer addresses and content hashes are not stable identity/epoch certificates by themselves.

### WP2 — Trace the real backward generation ancestry

Build an evidence-backed dependency graph from the **observed Ionic Liquids accepted region** to the region collection, source wrapper, source-selection and cache construction, and onward to the source provider/generator. Include native addresses and precise operand domains; distinguish directly observed values from reconstructed/candidate values and unknowns. Use the existing static chains such as source provider `14079f860`, generation `14079b520 → 14079c470 → 14079a330`, source owner/key calculation and geographic/source-frame transforms, but verify actual invocation relationships rather than assuming one path universally applies.

Explicitly investigate: source/owner identity, selected source descriptor/anchor/dimensions, local-to-native frame, selected BIOM/per-biome family/RSGD and atmosphere context, effective resource/rarity ordering including ties and special rules, mask/weight/selection branches, packed spatial key/CRC/MT sequence, and prior different-resource geometry/competition state. Identify where native source data or existing receipts support values and where those values could have changed between generation and consumption. Do not infer historical provenance solely from resident geometry.

### WP3 — Divergence localization with controls

Produce a stage-by-stage comparison of **earliest potentially divergent inputs or decisions**, not just a list of hypotheses. For each stage, specify its actual inputs, available evidence, expected effect on Ionic Liquids and on Copper/`0057ce`/`0057cb`, how it could or could not yield a resource-specific divergence, and a falsifier. Prioritize explanations that discriminate the native three-point Ionic Liquids path from the frozen predicted region without breaking the three exact matches.

Pay special attention to the mixed-biome Feynman site, but do not assume mixed-biome selection is the cause; distinguish beacon biome, region source biome, cell/terrain biome and effective generation BIOM/RSGD where supported. Include deterministic generator with *changing effective inputs*, cache reuse/retention and possible lifecycle instability without attempting to reproduce the historical mutation bug.

### WP4 — Evidence-constrained replay

Using the existing evaluator and reproducible analytical helpers, perform only:
- Replay with independently qualified observed/native operands; and
- A small, explicitly enumerated set of alternatives supported by native branches, installed definitions or prior source evidence.

Record each counterfactual's *independent justification before evaluating its fit*, exact differences from baseline, affected generated paths and effects on **all** controls. No arbitrary seed search, optimization over coordinates, unrestricted permutation, hindsight tuning, post-hoc transformations or edits to frozen predictions. A counterfactual match is diagnostic only until the alternative input is independently qualified as actually used by the game. Preserve original outputs and separate provisional conclusions from demonstrated equivalence.

### WP5 — Scientific closure or minimal new acquisition

If a supported explanation is established, document the earliest divergent stage, causal evidence, limitations and cross-control validation; provide a separately versioned correction/proposal only if justified, never silently replace prior results.

If unresolved, provide a **ranked, small set of concrete missing operands/decisions** that would discriminate the remaining hypotheses, ideally a single precisely located native read at source creation or generation. Evaluate whether existing C1D/C1E captures and installed data can supply them without another session. Specify executable observation boundaries, target data types and identities, coherence/lifetime needs, source/epoch correlation, receipt schema, failure status and minimum useful outcome. Draft a bounded implementation and live-run card if needed, **for maintainer review only**. Do not launch Starfield or make the test approval implicit. Feynman P3 remains primary; Carinae Iron is reserved for an evidenced Feynman-specific obstacle or future independent validation.

## 4. Mandatory scientific standards

- The native Ionic Liquids region is evidence of a geometric discrepancy; a catalogue list or saved extractor alone cannot substitute for its generation ancestry.
- Same consumption-time slot/wrapper ≠ same permanent procedural source ≠ same generation context/epoch. Mark the precise strength of every join.
- One accepted region is not necessarily an exhaustive census; skipped candidates are unknown, not absent.
- Preserve namespace/type mapping, actual binary32 and native offsets; distinguish VAs/RVAs, object member offsets, geographic frames, saved identifiers and runtime FormIDs.
- Generator determinism is conditional on complete, stable inputs. Do not assume the engine is bug-free or claim instability without evidence.
- Do not reduce the project to merely the present Feynman case: identify what is generalizable to the resource-geometry model, and which results remain site-specific.
- No destructive edits to primary evidence, installed tools/data, existing scripts, save files, Ghidra project, repository history or frozen models. New derived outputs/scripts must live in appropriately named research directories, with scratch/raw receipts ignored and immutable.

## 5. Frozen acceptance criteria (AC1–AC8)

**AC1 — Authority and integrity.** Verify source/executable/evidence pins and preserve game data, saves/backups, existing native receipts, frozen predictions, HEAD/index and publication restrictions. No live operation, staged change, commit, push or publication.

**AC2 — Native evidence binding.** Independently reproduce P3/IL/Copper/other accepted-region identities, exact geometry comparisons and qualified transfer correspondence; disclose capture incompleteness.

**AC3 — Generation ancestry.** Provide an address-/operand-backed dependency graph from accepted IL geometry through selected cached source toward producer inputs, classifying every join as OBSERVED, STATIC, DERIVED, CANDIDATE or UNKNOWN.

**AC4 — Divergence localization and controls.** Identify the earliest supported stage(s) where IL can diverge while three native control geometries remain exact, with positive/negative evidence, discriminating predictions and falsifiers.

**AC5 — Constrained replay.** Conduct transparent qualified replays or explicitly grounded bounded counterfactuals with all controls and unchanged frozen outputs. No arbitrary fitting or promotion of candidate inputs to observed fact.

**AC6 — Material scientific progress.** Deliver a supported explanation **or** a concretely reduced set of unresolved hypotheses with a specific, independently useful acquisition discriminator. Restating general uncertainty without new elimination, source tracing or operand qualification fails.

**AC7 — Durable delivery.** Create coherent authored report, ancestry/operand ledger, replay results/scripts/tests, limitations and, if necessary, a prospective next run card with objective preflight, sample, evidence and stop criteria. The run card is **not** permission to execute.

**AC8 — Independent critical review and exact delivery.** Obtain an independent reviewer (not merely author self-check) to challenge AC1–AC7, the actual scientific claims, code and counterfactual bias. Remediate defects, preserve review history, provide exact complete and task-only diffs, final changed/untracked-file manifests, source/evidence hashes, forward/reverse patch validation, protected-input checks, tests and final AC matrix. Do not stage/commit/push.

## 6. Required final response to maintainer

Report concise scientific result first; what is proved, disproved, still unknown and why. Link repository-relative authored outputs, state concrete new evidence/discriminators and independent-review disposition, test/preservation results and exact final patch paths/hashes. Include any proposed live card as **approval pending**. Suggest a conventional commit message but perform no Git write operation. Explicitly flag any acceptance criterion not met; never declare an unrun live test successful.

**Reminder:** B6 publication readiness remains on hold. This assignment is an offline investigation of the already observed region—not an automatic authorization for a new live capture.
