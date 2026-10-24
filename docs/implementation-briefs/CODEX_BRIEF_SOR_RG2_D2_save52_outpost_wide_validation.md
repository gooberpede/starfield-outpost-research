# Codex Research Brief — RG2-D2: Save52 Outpost-Wide Resource Prediction Validation

**Project:** `D:\Projects\starfield-outpost-research\` / `gooberpede/starfield-outpost-research`  
**Status:** Implementation and offline research authorized; live testing **not** authorized  
**Starting point:** Committed RG2-D1 standalone geometry reproducer and normalized local corpus, with seven exact native-region controls at Feynman V and Carinae III-a.  
**Primary question:** How well does the current independently specified offline resource-geometry predictor generalize to the other active ordinary outposts in Save52, without being given their known extractor resources or being adjusted case by case?

## 1. Authority, scope, and mandatory project standards

Read and follow `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md`, and the independent-reviewer procedure before work. Freeze the AC1–AC8 below at intake; do not reinterpret them to accommodate outcomes. Apply the full final editorial screening, manual reading, and independent verification to the exact submitted snapshot.

Use the committed RG2-D1 algorithm, predictor, builder, schema, isolation tests, reference corpus and existing native results as the baseline. Relevant predecessors: RG2-C1E, C1G, C1H, C2A–C2D and D1. Reuse established Save52 workshop, disabled-state, geographic-coordinate, extractor-owner and resource-identity readers rather than creating weaker alternatives.

**Permitted:** Read-only Save52 decoding and previously authorized local installed data; local-only corpus extension for additional planetary definitions; analytical/test code; offline evaluation, strict isolated predictor runs and independent review. **Not permitted:** Launching or attaching to Starfield, live captures, changes to saves or installed game data, forced regeneration, repository staging/commit/push, publication, or integrating with the Outpost Tracker. Additional live observations require a separate reviewed run card and explicit maintainer approval.

Preserve frozen RG2-D1 predictions, native receipts, input hashes and original save evidence. Do not alter the common generator or numerical semantics merely to improve validation outcomes. Generated ESM-derived corpus payloads, primary save bytes, native receipts and proprietary exports remain ignored/local-only. Tracked algorithm/specification, code, reporting and limited authored aggregate results retain existing publication review restrictions. Keep B6 on hold.

## 2. Population: enumerate all Save52 ordinary outposts

Use **Save52 / HIST-0267** by verified identity/hash, not an interchangeable filename or unverified similarly named save. Recover the full saved ordinary-beacon population using the established parsing, saved Workshop joins and disabled-state logic. Do not treat a surviving deleted/disabled reference as an eligible active outpost. Check supported active ownership/membership rules; where active state or membership cannot be qualified, explicitly flag the case instead of silently including/excluding it. The second Feynman V `Cu IL F` outpost is **not deleted** and must not be excluded merely on an old mistaken assertion; apply actual saved-state evidence.

Create a frozen case inventory with stable saved identifiers, original human-readable outpost names for navigation, planet/body identity, supported spatial frame, biome/terrain metadata, location and footprint inputs, eligibility decision and reason. Record protected source references locally and avoid committing sensitive raw details unnecessarily. Distinguish active, disabled, unsupported and identity-indeterminate counts.

Retain **Feynman V Cu Co Ni IL** and **Carinae III-a Rc Fe** as *development/known-native regression controls*, excluded from the numerical held-out score. The primary study population is all other eligible Save52 ordinary outposts, not a convenient manually selected subset.

## 3. Blind evaluation — strict order of operations

The study must enforce a real independence boundary:

1. **Freeze inputs and predictor baseline.** Record exact committed source, executable reference, installed-definition hashes, input schema and version of each corpus extraction route. Record the case inventory and deterministic prediction requests. Existing saved extractor records may be used to establish identity/footprint only insofar as unavoidable; their resource labels and historical outcomes must not influence resource selection, source enumeration, inclusion in the predictor request or prediction generation.
2. **Extend local reference coverage if needed**, using the existing field-level corpus builder and only data/derivations required by the documented algorithm. Record every added field, source record, unsupported path and rationale. Never use installed-extractor/resource witness lists to choose corpus content or predictor targets. The local generated corpus remains untracked. Freeze a version/hash of the entire resulting corpus **before** comparing predicted resource memberships with saved extractor labels.
3. **Produce predictions for every eligible case with supported input** using the unchanged RG2-D1 generation and availability algorithm. Derive selected SFTR/SFPT, sources, effective BIOM/RSGD, settings and competing regions without feeding known source anchors, runtime captures, extractor resource identities or expected answers. Emit full predicted resource identities, status, relevant contributing regions and coverage/unknown codes. Preserve fixed, immutable local predictions and their hashes.
4. **Only after the preceding freeze**, open/join historical Save52 direct-owner extractor/resource associations and any independently documented gameplay/native observations. Preserve exact identity qualifications and provenance. Record comparison as a second stage, with a verifiable audit trail showing when prediction was finalized relative to answer evidence access. A single script that loads all resource answers before running the predictor is not an acceptable blind test; use process/file or permission boundaries where practical.
5. Investigate failures *after* the blind comparison in separately labelled diagnostics. Never replace the blind first-pass record. Any evidence-supported model revision must be versioned and rerun across the complete case set and the seven established native controls, with the original results retained.

Do not conceal resource labels through superficial variable renaming while using them indirectly to choose inputs. The independent reviewer must challenge leakage, predictor reads outside the portable corpus and sampling bias.

## 4. Evidence interpretation and outcome taxonomy

Compare **ordinary localized inorganic vein availability** first. Keep atmosphere, Water/Everywhere, biome-admission bypass and special extractor eligibility branches out of the ordinary-vein score; label them separately if encountered. Derive membership by spatial intersection of generated regions with the qualified native query/footprint, not merely from PNDT planet resource availability.

- **Positive correspondence:** a supported predicted ordinary resource agrees with a positively qualified saved extractor resource association. This is historical saved-state corroboration, not proof of contemporary native geometry or throughput.
- **Potential false negative:** a positively joined historical extractor resource is absent from a supported ordinary prediction. Preserve source and case identities, date/epoch uncertainty, and investigate as a counterexample rather than immediately calling the generator wrong. A surviving extractor can outlive a vein change.
- **Unverified extra prediction:** predicted resource with no saved extractor. **Never** count as a false positive or evidence of actual absence; players do not necessarily build all available extractors.
- **Unsupported/indeterminate:** missing geographic context, invalid seam, unresolved tree/source, ambiguity, unsupported record, uncertain activity/ownership or other precise blocker. Do not collapse unknown to absent.
- **Alternative admission:** a resource/extractor whose eligibility is known to bypass ordinary finite veins. Exclude from vein mismatch scoring and explain the separate mechanism.

Keep separate denominators for: (a) outpost-population coverage, (b) predictor support, (c) positively established extractor-resource validation coverage, and (d) corroborated correctness within that positively evidenced subset. Report false-negative candidates by reason and scope; do not invent whole-population accuracy, specificity, false-positive rate, exhaustive source coverage or completeness from positive-only evidence.

Where practical, classify a case with partial resource-family support at resource granularity rather than forcing all-or-nothing outpost status. Establish actual supported geographic chart/interior versus seam status before advancing an exact comparison.

## 5. Analysis and substantive stopping rule

Prioritize scientifically informative discrepancies and **coverage class failures** over performance optimization. For each candidate false negative, perform bounded source-tree, definition, mask, coordinate, geometry, cache-history and extractor-identity diagnostics, proceeding by information gain. Do not run broad seed-fitting, arbitrarily shift geometry, alter source selection to fit saved hardware, or issue site-specific exception patches.

The work is successful if it produces a genuine frozen Save52-wide evaluation, defensible coverage accounting and prioritized counterexamples/unsupported classes, even if some outposts cannot yet be predicted. Do not promise perfect planet-wide coverage or demand an impossibility proof. A scientifically important negative result should identify the earliest relevant failing stage and the next falsifiable discriminator.

If additional live evidence is warranted, produce a **separate prospective run card** (target/identity, exact unresolved observation, selected acquisition point, natural trigger, controls, save pre/postflight, transient-save handling, durable receipt and stopping/abort conditions), and seek approval. Do not execute it.

## 6. Deliverables

Track authored research and reusable original code appropriately, but not extracted/proprietary corpus payloads:

- A durable `docs/experiments/...` report with population table, coverage denominators, independent test chronology, outcomes, unresolved source/terrain classes, prioritized counterexamples, limitations and evidence references.
- Frozen case inventory and comparison tables with consistent IDs and sufficient provenance, sanitized for research/publication review; detailed sensitive/raw local files remain ignored.
- Versioned local first-pass request/prediction/corpus manifests with byte hashes and explicit access/freeze chronology; preserve immutable original results.
- Corpus-dependency changes and coverage measurements (what additional data was necessary and approximate incremental bytes), without turning this into a size/performance optimization assignment.
- Existing seven native geometry controls rerun or independently verified from protected fixtures; baseline no-change demonstrated. Review records and commands sufficient for independent offline reproduction by an authorized local researcher.
- Updated research navigation/state/source ledger only as needed; no premature promotion to universal correctness or publication clearance.
- If needed, a separate *unexecuted* live run card for highest-value unresolved evidence.
- Complete and task-only unified diffs, manifests including untracked textual artifacts, before/after protected-input checks and verified forward/reverse patch applicability. No staging, commit, push or release.

## 7. Frozen acceptance criteria

**AC1 — Authority, inputs and preservation.** Correct hashed Save52/pinned installed build, permissions and protected-input handling; no unauthorized game or repository operations; transient exitsaves/autosaves excluded from active integrity gates according to the accepted policy while designated/manual/quicksaves remain protected. Original corpus and native controls unchanged.

**AC2 — Complete eligible case inventory.** Every saved ordinary outpost is accounted for with qualified state/ownership, stable identity and explicit active, disabled or unknown status; two known validation sites remain separate controls; no old false deletion assertion is reused.

**AC3 — Blind prediction contract.** Freeze input corpus and first-pass results before reading comparator resource labels; enforce independence from native expected geometry and saved extractor identities in prediction; retain timestamps/hashes and audit the no-leakage mechanism.

**AC4 — Portable corpus coverage.** Extend field-level local corpus only when required; standalone inference reads no installed ESM/EXE, raw saves, caches, expected labels or native captures. Unsupported domains fail explicitly rather than silently defaulting.

**AC5 — Scientifically valid comparison.** Correct positive/possible-false-negative/unverified-extra/alternative-admission/unsupported classifications; extractor records do not become a complete availability oracle; separate predictor coverage, validation coverage and corroborated agreement denominators.

**AC6 — Material generalization findings.** Produce a comprehensive held-out Save52 assessment with independently prioritized counterexamples/coverage gaps and bounded diagnostics. No site-by-site fitting; all seven Feynman/Carinae native-region controls remain exact.

**AC7 — Durable technical and editorial record.** Reproducible commands, hash-bound manifests, clearly versioned results, consistent terminology/hex offsets/numeric domains, no fused prose; automated editorial scan and manual finalization of *all changed authored text*.

**AC8 — Independent acceptance and exact delivery.** Independent reviewer critically checks actual source/fixture evidence, blind freeze and leakage prevention, population accounting, scientific qualifiers, full edited prose and complete/task-only exact patch packages. REWORK if a material requirement fails; make no unsupported ACCEPT claims. Supply review disposition and verification evidence before return.

## 8. Handoff instructions

Return a concise summary of: eligible active/unknown/disabled outposts; successfully predicted outposts; supported positive extractor-resource associations; potential false negatives; other unsupported classes; native regression results; scientific findings; independent disposition; exact patches and manifest; and proposed next discriminator. Explicitly distinguish **NO LIVE TEST PERFORMED** from a planned run card. Suggested commit message after maintainer approval: `feat(research): validate standalone resource predictor against Save52 outposts`.

**B6 publication verification remains on hold.**
