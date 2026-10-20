# Codex research brief — LO1: Locations → Outpost field lineage and remaining calculations

**Project:** `D:\Projects\starfield-outpost-research`  
**Assignment:** LO1 — bounded offline research and documentation  
**Authority:** User-approved research brief; **not** approval to run the game, attach to processes, modify saves, publish evidence, or stage/commit/push  
**Status:** Proposed brief for execution, subject to applicable repository controls

## 1. Research objective

Explain the information architecture of **Locations → Outpost**: how each informational value and graphic is calculated or obtained, how it travels through native providers/payloads to the compiled screen, and which update events replace or refresh it. **Consolidate previously accepted findings without re-verifying their underlying computations.** Investigate only the screen-specific presentation routes and genuinely unresolved calculations or field meanings.

This is foundational research into Starfield's machinery, not a mod implementation, exhaustive catalogue, UI redesign or full Scaleform reference. Clearly distinguish the **Locations → Outpost** subview from the separately investigated Database/Almanac Outpost page and from the Build Mode footer. Use installed definitions, compiled interface/native mapping, qualified local evidence and previously accepted results. Do not infer one screen's source solely from a similar-looking field on another screen.

Read and follow `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/PERMISSIONS.md`, `docs/PROVENANCE.md`, `docs/PUBLICATION.md`, third-party rules and reviewer procedures before executing. Preserve current project classifications and evidence identity. The governing audit is `docs/audits/outpost-coverage-2026-10/build-mode-and-locations.md`; its **TRACED / PARTIAL / UNTRACED** categories are starting leads, not new truths. Check subsequent accepted BM1/BM2 and SD3 work before allocating investigation.

## 2. Explicit exclusions and reuse

**Do not re-investigate:** E1–E3 producer arithmetic, BM2 production stacking; P1 power flow; L1 construction limits, L2 budget accounting or L3 spatial restrictions; CR1 crew assignment; C1–C3 cargo logistics; SD1/SD2 inventory mechanics; SD3 Stored Resources aggregation, icon sources and snapshot collection; BM1 component CHANGE. Reuse their already reviewed results and cite exact documents/functions. A *different screen-specific calculation or binding* is a valid new LO1 question; the previously mapped general mechanism is not.

**Do not study:** general menu navigation, paging, sort controls, animations, input mappings, graphics rendering, arbitrary live refresh experiments, full active-player-outpost importer membership, screenshot recreation, or arbitrary other Database screens. No unrelated systems, generalized reverse-engineering infrastructure, game or save manipulation. If a screen graphics path selects an asset, identify the actual selector, data and asset provenance without dissecting the renderer.

## 3. Required field scope

Create one authoritative field-lineage table including **every informational field visible in the supplied Locations → Outpost screenshot** and any associated nondecorative label/graphic. At minimum:

1. Selected outpost/list name and detail name; rename/update source.
2. Planet/subtitle, system designation and their actual localized metadata paths.
3. **OUTPOSTS BUILT** numerator and denominator: count population/predicate, relevant player allowance, any resolved registry and exceptional inclusion limits. Trace this *screen's* count without reopening global saved active-membership completeness.
4. **Cargo Links**: precise counted entity and native producer of the summary integer; distinguish built pads, routes, operational links and freight. Reuse C1/L1 but do not equate their predicates without proof.
5. **Crew**: exact counted entity and producer of the summary integer; distinguish assigned people, capacity, present actors and robot contributions where relevant. Reuse CR1/R1.
6. Needed Power / Total Power: source status lanes and screen bindings; only follow an untraced display conversion, not P1's graph.
7. Production: reuse E1/BM2 nominal aggregate and Locations rounding, verify/document its already-established presentation path by citation, **no new arithmetic or realized-throughput work**.
8. Stored Resources and resource icons: reuse SD3 source, per-outpost array/selection, resource unit aggregation, icon mapping and refresh; **no new inclusion census**.
9. Build Limit indicator: trace *this screen's* payload binding and frame/ratio presentation as needed; reuse L2 scalar accounting.
10. Faction label and emblem: actual governing source/selection, context (body/system/territory), missing/default/override behavior and asset lookup; do not assume jurisdiction from the visible text.
11. System level: which installed/effective level datum, default/override logic, provider field and formatting; avoid inferring a level from the screenshot.
12. Selected planet image, starfield/upper image, orbital/system diagram and selected-body marker/highlight: source records, identifiers, asset selectors and mapping to the selected entry, insofar as these convey information. Exclude internal drawing/animation architecture.

Use **SOURCE → CALCULATION/COUNT PREDICATE → NATIVE PROVIDER/PAYLOAD FIELD → COMPILED UI CONSUMER → DISPLAY** and note cached/derived/live and refresh semantics. Include resolved version/pin for new native claims, and record whether lineage is fully traced, inherited from accepted work, or genuinely partial. Do not confuse copied payload offset with a proven semantic counting predicate.

## 4. Actual novel research priorities

A. **Cargo and crew counting:** Starting from the known common summary lanes (`+0x88` cargo, `+0x8c` crew) trace upstream producer and counted population. Document event/update source and relevant zero/absent cases. Use saved contrasts if already available; avoid broad new sample acquisition.

B. **Outposts Built:** Trace numerator's registry filters and denominator's player-capability path through final UI binder. State clearly any incompleteness relative to the general saved-beacon corpus and exceptional membership. Do not claim exact active population beyond the native screen selection rule.

C. **Faction, system level, visuals:** Trace previously unmapped data and asset selectors. For images/diagrams distinguish static art, calculated layout and metadata lookup, and record an explicit technical limit if visuals are assembled by opaque UI routines.

D. **Residual bindings:** Finish specific name, planet/system caption, Build Limit bar or other fields where the underlying computation is accepted but the particular Locations payload/consumer isn't. Keep these follow-ups narrow.

E. **Provider lifecycle:** Summarize Locations entry, collection, outpost selection and any known refresh/invalidation triggers. Separate *source state updated*, *provider snapshot refreshed* and *selected entry repainted*. Reuse SD3's existing trace; new evidence only for gaps, not a fresh UI-runtime study.

For each novel claim use decisive native, compiled UI, installed-record or existing save evidence. A screen caption by itself never establishes the semantic source. If the source has no demonstrable additional calculation, say so.

## 5. Research process and evidence

1. Freeze the original eight acceptance criteria below before starting. Document installed game/build, tools, source hashes/identity and approved evidence inputs. Inspect repo state and retain baseline HEAD/index/status.
2. Start with a **reuse ledger**: list every field and the accepted documents/pins that already explain its source/calculation or presentation; identify *only* missing edges. Do not rerun previous analyses as a condition of reuse. Recheck a pin only when a material version mismatch or contradiction is demonstrated.
3. Trace missing edges top-down from actual Locations UI consumers and bottom-up from provider/calculation as needed; use the smallest discriminating local analyses. Preserve alternative interpretations where real evidence supports them, and avoid hypothetical “maybe” branches with no counterexample.
4. Use existing historical saves only as optional field-semantic corroboration where they can discriminate competing counts, identities or snapshots. Preserve source hashes and reject chronology-free equivalences. No requirement for fresh user saves or live screenshots.
5. Give a concise answer-first report that separates **established, bounded/static inference, measured SAVE and unknown**. Describe what information *cannot* be inferred from screenshot or stored save alone.
6. Update the new experiment/audit documents, appropriate research indexes and backlog pointers. Do not silently reclassify/rewrite prior findings or alter historic reports to match new conclusions.

## 6. Deliverables

Suggested location `docs/experiments/locations-outpost/` (adjust to repo conventions):

- `report.md`: answer-first summary, new discoveries, limits, no duplicated whole-subsystem reports.
- `field-lineage.md` or `field-lineage.csv`: full screen field-by-field table of source, actual formula/predicate, payload/UI binding, refresh and provenance/status.
- `native-and-ui.md`: bounded newly traced function/call/data paths, version-pinned native offsets, compiled interface symbols and essential record/asset joins.
- `reuse-and-gaps.md`: accepted findings reused without re-verification, precise new work and explicitly open paths.
- `review.md`: frozen criteria, validation, independent review, corrections, evidence and packaging receipts.
- Appropriate source/function/asset registers or compact reproducible verification scripts **only where genuinely useful**. Keep local game binaries, compiled assets, save extracts, Ghidra projects and raw screenshots outside publication candidates.

Cross-link the output from existing indexes and `docs/RESEARCH_STATE.md`/`docs/BACKLOG.md` using relative repository links when suitable; do not initiate project-wide cleanup.

## 7. Frozen completion contract — AC1–AC8

**Task type:** Bounded offline research, cross-subsystem consolidation, documentation.

**AC1 — Evidence and authority.** Identify/preserve primary installed and historical sources, game versions and required hashes; verify applicable permission/integrity gates; no unapproved live/save/repository integration actions.

**AC2 — Complete informational-field inventory.** Every informational field and meaningful graphic of Locations → Outpost has a documented source/calculation/presentation/refresh status, including the listed fields. Excluded navigation and animation are explicitly bounded.

**AC3 — Faithful consolidation.** Existing accepted mechanisms (P1/E1/BM2/L2/CR1/C1–C3/SD3 etc.) reused by correct citations with no compulsory repeat verification or unwarranted promotion. Distinguish shared providers from screen-specific adapters.

**AC4 — Count and allowance semantics.** Cargo Links, Crew and Outposts Built numerator/denominator receive bounded causal upstream counting/eligibility evidence, or a concrete, evidenced missing edge and the strongest warranted scoped result. Merely naming offsets is not completion of their semantic trace.

**AC5 — Previously unmapped metadata and assets.** Faction, level and selected-body imagery/system diagram receive actual source/selection/data-to-interface tracing, including what is and is not computed, with scoped negative findings permitted where supported.

**AC6 — Field delivery and refresh.** Identify Locations provider payload and compiled consumer for each field to the extent supported; distinguish initial collection, selection repaint and refresh/invalidation. No invented live timing guarantees.

**AC7 — Durable causal report.** Produce reproducible field lineage and concise answer-first results, source/asset pins, reuse ledger, precise confidence/coverage and unresolved material gaps. All links resolvable or explicitly declared local-only; no false exhaustive reach claims. Run malformed prose, markdown/link and source-reference checks.

**AC8 — Independent review and integration package.** Follow the project's independent reviewer contract against this unmodified brief and primary evidence. Return AC1–AC8 PASS/FAIL/NOT TESTED with reasons and paths; retain initial failures and corrections; supply exact complete and task-only diffs (including untracked text), verified forward/reverse applicability/reconstruction, baseline and final status/HEAD/index, change inclusion/exclusion manifest, integrity/check receipts and reviewer ACCEPT/REWORK/ESCALATE. No stage, commit or push.

**Optional:** independent same-state live refresh observations, exotic override populations and exhaustive UI-asset variants, expressly not required and not authorized under this brief.

**Scoped negative closure:** A grounded analysis finding no additional screen-specific calculation can complete a field if the actual inherited provider/binder is established. A properly bounded unknown or unimplemented pathway may be reported where concrete constraints/evidence justify it; do not call an unsearched likely producer absent or a known mandatory gap PASS merely by relabelling. Distinguish scientific completion from deployment/release qualification.

**Continuation:** Diagnose/fix in-scope failures and rerun affected checks under the same assignment. Do not shift ACs without maintainer approval; preserve counterexamples and unsuccessful methods. No arbitrary deadline or verification-count quota, and no refactoring unrelated tooling to pad coverage.

**Escalation/stop:** Halt the affected operation on protected-input mutation/hash discrepancy, failed disk/free-space or STOP guards, required external permission, inaccessible essential evidence after bounded checks, or genuine tool/resource exhaustion. Preserve receipts and state, request narrow authority/input, and continue independent safe work. Preserve project C:/D: disk guards and workspace integrity controls where applicable. No game launch/attachment, save modification, network publication, copying restricted game assets into tracked files, or git staging/commit/push.

**Independent disposition:** Only reviewer ACCEPT after these frozen criteria, followed by maintainer critical diff review, permits a recommendation to integrate. Reviewer approval does not itself authorize any integration or publication.

## 8. Requested return

Provide a concise findings summary emphasizing the newly resolved counting and metadata questions; a list of remaining material limitations; the frozen AC matrix and independent review verdict; check and preservation receipts; complete/task-only verified patch paths; final status; and a suggested commit message. **Return for maintainer review.**
