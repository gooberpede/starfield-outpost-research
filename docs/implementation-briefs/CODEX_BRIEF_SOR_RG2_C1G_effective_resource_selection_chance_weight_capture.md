# Codex implementation brief — RG2-C1G Phase A
## Effective resource-selection and chance-weight acquisition

**Project:** `D:\Projects\starfield-outpost-research` (`starfield-outpost-research`)
**Status:** Authorized **Phase A only**: bounded offline native research, implementation, synthetic qualification, documentation and approval-ready run card. **No Starfield launch, attachment, live trace, cache intervention, or save modification is authorized by this brief.** Phase B requires the maintainer's separate explicit approval **after reviewing Phase A and the completed run card**.
**Research target:** P3, Save52, Feynman V `Cu Co Ni IL`; Ionic Liquids (`Starfield.esm:0057d4`) primary, Copper (`Starfield.esm:0057cf`) invariant control. Carinae III-a Iron is a later independent test, not an automatic substitution.
**Pinned target:** `Starfield.exe` 1.16.244.0, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; treat native addresses as preferred static VAs unless verified against a measured runtime base.

## 1. Motivation and frozen evidence

RG2-C1D acquired a P3-bound native spatial transfer containing Ionic Liquids and Copper. RG2-C1E Phase B captured an accepted three-point Ionic Liquids region absent from frozen RG1/RG2 conditional predictions, while Copper's singleton and two other accepted paths matched exactly. RG2-C1F reproduced the **exact** native Ionic Liquids points, widths and bound with the existing offline generator when a candidate source/cell's **chance-admission test** was allowed through. The frozen inactive exotic weight prevented that attempt, and the three tested alternative weighting configurations each lost the Copper control. **No historical cause was proved** and no variant was adopted.

The relevant conditional candidate is source `0:25116:32448:00257f38`, cell `(10,1)`; the frozen draw×100 is approximately `0.49152764678001404`, frozen weight×RSGD chance approximately `0.14999999105930328`. Higher admission can reproduce the native IL path but may admit an additional IL region at `(11,1)` and alter Copper competition. These are **offline hypotheses**; do not equate exact output coincidence to an observed historical generator call.

Creation Kit screenshots supplied by the maintainer show applicable RSGD **Generation Data (Cell)** Exotic `Chance to Appear` = **15.0000** for selected `CanyonsDefaultRes`, `FrozenBarrenDefaultRes03` and `DesertRocksDefaultRes` resource entries. These are record-level corroboration, **not proof of which RSGD or effective multiplier the native generator selected**. The known default exotic inactive multiplier `0.01` was traced to native initialization, not directly to RSGD DNAM. Explicitly separate RSGD chance, active/inactive rarity mask, effective runtime multiplier, resource attempt order and prior region competition.

Use existing durable research and exact local primary records rather than duplicating broad exploration:
- `docs/experiments/resource-generation-ancestry/{report,ancestry,results,next-run-card,review}.md`
- `docs/experiments/resource-region-ancestry/{phase-b,phase-b-review,run-card}.md`
- `docs/experiments/resource-oracle-retail/{report,implementation,run-card,review}.md`
- `docs/experiments/resource-geometry/{native,evaluator}.md`
- `docs/experiments/resource-geometry-mature-context/` and `docs/experiments/resource-geometry-live-prep/`
- `docs/experiments/native-availability-map/`, `docs/experiments/disappearing-deposits/`, and existing implementation/source registries.
- `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`.

Other relevant maintainer research in `starfield-resource-research` may be read locally or via the connected GitHub repository, with documented provenance and permissions. No externally sourced code or private/proprietary evidence is to be incorporated into versioned deliverables without the existing clearance rules.

## 2. Primary assignment: a working, qualified generator-operand collector

Extend the **existing RG2-C1D/C1E retail debugger controller and evidence/receipt formats**, not an unproven new observer. Offline implementation should target the actual native lineage that selects resources and supplies their chance multipliers, especially `FUN_14079b520` and the established `0x14079bdad–0x14079be20` ordinary weight/mask selection, together with justified nearby producer/cell sites. The precise instruction stop(s), register assumptions and callback ancestry must be revalidated against pinned native evidence and instrumented fixtures. Do **not** presume the published `XMM3` state applies at every callsite or survives intervening instructions.

Specify and, to the degree Phase A permits, implement a receipt capable of capturing **actual observed**:
1. Session and measured image identity; thread/call ancestry, entry and terminal, source/population correlation, sample completeness/loss and time/order.
2. Actual generating manager and **source identity**, selected source frame/anchor, owner key and source descriptor—not merely a consumption-time source ordinal or reused pointer.
3. Effective BIOM, selected RSGD, family, IRES identity and rarity; provenance for current/alternate descriptor and any relevant atmosphere or component choice.
4. **Ordinary rarity mask**, mask-selection branch, settings source/address, actual inactive or active multiplier, native `Chance to Appear` block and multiplication operands (binary32 bits where relevant). Record branch selection independently of the final scalar.
5. If observation at the generation-cell boundary is feasible: cell `(x,y)`, packed key, seed/draw, attempted chance threshold, admission/rejection, actual resource generation order and necessary predecessor/competition context. Distinguish planned from actually instrumented fields.
6. Correlation to the previously captured P3 IL three-point region and Copper singleton, or explicitly mark historical-generation ancestry **UNKNOWN** where not established.

Preserve signed/raw values, field domains, offsets, exact register and return-site semantics, and observed vs derived status. A pointer match, matching geometry or matching FormID cannot by itself prove a shared generation epoch. Receipts must distinguish genuinely absent data, unobserved events, and evidence lost on a crash.

## 3. Source and settings provenance (bounded offline work)

Trace where the inactive rarity multipliers are initialized, read, selected and potentially written/overridden **in the relevant path only**. Identify executable defaults versus effective runtime setting values, and whether the relevant value can be set via INI/GMST/plugin/ESM or other state **only where demonstrated by native consumers/writers**. Don't assert an override exists or is impossible based on default initialization alone. Pin exact native export and installed-definition evidence. Distinguish upper RSGD biome-generation probabilities from lower cell-generation parameters. The real question is which **effective setting branch and selected source** the game uses, not whether the Creation Kit displays 15%.

Do not generalize to a complete engine settings audit or reopen all planet generation research.

## 4. Controls, counterfactual policy, and scientific comparison

- Keep original RG1/RG2 frozen predictions, 967 C1E raw receipts and C1F result sets intact. Preserve exact source/capture hashes before and after investigation.
- Carry forward **Copper as a mandatory exact control**; include the two additional matching IRES paths (`0057ce`, `0057cb`) wherever comparisons apply.
- Compare native and offline **at the first supported diverging stage**: selected BIOM/RSGD/family → mask/active branch → effective scalar → chance test → path construction → competition → accepted cached region.
- Evidence-constrained counterfactuals may vary documented alternative branches only. Do **not** search arbitrary seed/weight intervals or tune to make IL and Copper match, then present it as validation.
- Any proposed explanation must confront why the extra admitted IL path can suppress Copper. Keep distinct: same consumption-time slot, generating source and cache/generation epoch.
- If newly generated conditions cannot be joined to Save52's **historical** cached regions, label them new-epoch evidence; no silent historical attribution.

## 5. Engineering qualification — Phase A only

Implement real controller changes and reproducible **disposable synthetic Windows debug fixtures**, not merely prose. Test the actual chosen execution-breakpoint sites/operand-copying assumptions using synthetic source-shaped invocations, including at least: active vs inactive ordinary mask, alternative selected descriptor, different resource rarity, multiple cells, admitted/rejected attempts, wrong source/workshop, thread/nested invocation, incomplete register or pointer read, buffer overflow/copy budget, no breakpoint hit, and durable receipt/ACK before controlled termination. Re-run applicable existing C1C/C1D/C1E suites.

Offline/static tests may inspect the pinned EXE and local native exports read-only using established tools; no game process attachment. Synthetic debug targets can crash or be disposed after durable data capture. Verify complete writes, independent parse/readback and loss reporting. Document actual calls/commands, compiler/tool versions, expected/observed counts, negative tests and remaining retail-specific uncertainties.

## 6. Mandatory run card — do not execute without approval

If live acquisition is desirable, prepare a **complete, reviewable Phase B run card** with:
- Exact pinned build/installed definitions, controller binary hash, guarded stop addresses/bytes, register/struct checks and source/Workshop identity criteria.
- An explicit **natural generation trigger strategy** (and likelihood of no generation event). Existing geometry may already be cached. Do not force resets, cache misses or save edits without separately approved authority.
- First case and discriminators: P3 Ionic Liquids at source/cell if naturally observed, Copper control and relevant skipped attempt/competition information; explain which observations could be obtained in a *new* epoch and what would remain historical UNKNOWN.
- Minimal exact operator sequence, Steam/user-token handling, fresh run/receipt paths, named limits, no-autoretry rule, fail-closed/abort criteria, stop-after-evidence policy, and a qualified fallback for no natural generation (e.g., a separately proposed controlled-save or newly generated source case), without automatically switching to Carinae.
- **Save standard:** preflight SHA-256 of live saves and independently recoverable backups outside sync/write paths; verified restoration rehearsal; explicit Steam Cloud status; postflight inventories/hashes, preserve changed files before any restoration, restore from verified backup if needed and verify restored hash. Backed-up live saves may incur bounded risk, sole recoverable copy may not.
- Evidence and experiment integrity: durable acknowledgement and independent readback before intentional game termination; crashes after completed receipts are acceptable, incomplete captures are not promoted to facts. Game playability/clean debugger retirement after successful evidence collection is not mandatory.
- Precise statement that **Phase A and its independent ACCEPT do not authorize Phase B**. Present the run card to the maintainer and assistant for explicit approval **before** launching or attaching to Starfield.

The previous rejected observer stays NO-GO. A major architecture change, injection or executable patching requires separate approval; the current synthetic hardware-breakpoint collector is the starting point. B6/release-publication activity remains on hold.

## 7. Frozen acceptance criteria (AC1–AC8)

**AC1 — Authority, baseline and preservation.** Confirm correct branch/repo, initial HEAD/index, executable/definition pins and protected-input hashes. No retail launch/attachment, save modifications, unauthorized third-party incorporation, staging, commit, push or publication.

**AC2 — Native operand lineage.** Precisely map relevant mask/weight/descriptor selection and the candidate cell-generation call with cited native windows and truthful STATIC/OBSERVED/DERIVED/UNKNOWN distinctions.

**AC3 — Implemented collector.** Deliver functioning Phase A controller extension that captures the defined generator-selection operands from disposable synthetic native memory using real Windows debugging; no documentation-only implementation claim.

**AC4 — Controls and scientific discrimination.** Define exact IL chance-gate and Copper competition questions, preserve all four native paths/frozen baseline, and provide unfitted comparison rules for any later evidence.

**AC5 — Test qualification and durable evidence.** Pass reproducible positive and adverse synthetic qualification, including event identity, no-hit/partial states, bounds, loss, acknowledgement and crash/termination cases; confirm backward compatibility or document justified migration.

**AC6 — Constructive live plan.** Deliver one actionable, bounded Phase B run card with objectively testable preflight, a natural-trigger and no-hit contingency, save-backup/postflight controls, scientific expected results and explicit independent approval barrier. An all-NO-GO result without concrete mitigation fails; a method that only reconfirms screenshots is insufficient.

**AC7 — Durable analysis and provenance.** Write concise report, native operand/setting provenance, implementation notes, replay/fixture evidence, exact unknowns, source ledger and proposal; maintain navigation and provenance records as appropriate, no altered historical predictions.

**AC8 — Independent review and complete delivery.** Obtain a distinct independent critical reviewer examining native interpretation, actual tests, instrument safety/evidence validity, scope, reproducibility and the exact final worktree. Resolve defects, retain outcomes. Produce exact verified **complete** and **task-only** unified diffs, path/hash manifests and protected-input audit; check apply/reverse in disposable scratch. Do not stage/commit/push. The maintainer will review the diff before committing, and separately review/approve any retail test.

## 8. Return contract

Return: (a) concise finding and limitations, (b) exact created/changed path manifest, (c) implemented controller + synthetic test results, (d) independent final review and AC matrix, (e) approval-ready run card **not executed**, (f) verified complete/task-only patch locations and SHA-256, (g) initial/final HEAD/index and protected-input preservation status, (h) blockers, next discriminator and recommended commit message.

**Mandatory stopping point:** Complete Phase A and return for review. **Do not conduct a Starfield live test on the strength of this brief or an independent reviewer ACCEPT.**
