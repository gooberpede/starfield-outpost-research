# Codex research brief — C1: Cargo-link configuration, management interface and save/runtime correspondence

**Project:** `starfield-outpost-research`  
**Type:** Bounded offline native/definition/save investigation and independent review  
**Phase:** C1 of cargo-link research (C2 freight/ship lifecycle; C3 remote operation/inter-system fuel)  
**Authority:** Offline/read-only research and authored documentation/evidence utilities within repository conventions only. **No Starfield launch, live observation, process attachment, instrumentation engineering/deployment, save mutation, original asset modification, staging, commit, push or publication.** Do not infer that mentioning a later test authorizes it.

## 1. Objective and accepted context

Explain how an outpost cargo link is **configured, represented, displayed and persisted**. Investigate both the live-runtime *machinery* that populates the cargo-link management interface and the matching structures in existing saves. The principal concrete case is the user's Save52 screenshot from the ordinary, **same-system** cargo pad at **“Feynman I Li Cu xF4”**, linked to **“Feynman VII-b Nd Al He3”**, both in Feynman (displayed **0 LY**). The screenshot shows a selected/linked destination, **Cargo Ship 0/300**, empty **Outgoing Resources** and **Build Resources Needed** panels on both sides, and a list headed **Available Outposts**. The user reports Isotopic Coolant may be sent from one end and Supercooled Magnets returned; these identities, actual shipments, and exact direction are **user recollection, not verified screenshot contents**. Determine *why* panels can be empty despite an apparently configured operational pair; do not assume a defect or infer that cargo is in transit.

Preserve established S1/S2 results: cargo pads use distinct incoming/outgoing child inventory references; local links and cargo transportation are separate relationships; production can create downstream inventory without a periodic conveyor; save inventories are historical snapshots. Consult `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, current subsystem map/backlog, S1/S2 reports and P1 save identity conventions. Reuse pinned installed retail build/native database, installed scripts/definitions, saved corpus and project-owned readers. Verify all actual paths/hashes/builds before use; preserve source/permission boundaries. Add this brief under `docs/implementation-briefs/` and its index as normal.

**Required executive response:** Begin the research report with an answer-first table: UI field; what it means; exact population source and gates; refresh/update mechanism; saved or transient provenance; Save52 observation/explanation; confidence and remaining consequential limitation. Provide a clear *positive answer* where sufficient native evidence exists; don't bury conclusions under generic qualifications.

## 2. C1 investigation requirements

### A. Configuration, eligibility and pairing

Trace from the actual terminal/menu selection through the relevant native/Scaleform/SWF/script/PEX/definition layers (as evidence permits): how candidate outposts and compatible pads are identified; same-system versus inter-system types; occupied/available endpoints; distance, outpost names/system/location; pairing, removal, and orientation/bidirectionality. Distinguish candidate list eligibility from successful link validation, selected UI row and existing connection. Trace concrete saved identifiers, endpoint links, child pad references and reconstruction/loading of runtime pairing data. Do not equate local output links, Workshop ownership, electrical links and inter-outpost links.

### B. Management interface — every visible field

For **Available Outposts**, row sorting/order, selected item, green arrows/linked indicators, **Outgoing Resources** at each end, **Build Resources Needed** at each end, **Cargo Ship current/300**, and names/distance: identify the UI binding/property/provider, actual inputs/filters, update or invalidation triggers (open, selection, inventory changes, link updates, ship events, periodic refresh) and any caching. Trace displayed “resource” meaning precisely: outbox inventory, planned/assigned exports, ship manifest, recipe/build needs, transport history or another distinct concept. Separate missing data, intentional empty state, wrong endpoint, stale cache and UI bug **only where supported**. If UI resources are packaged/compiled and a source-to-binding step is unavailable, document what was positively traced and the exact gap; do not assert absent behaviour from missing source.

### C. Save52 case study (mandatory)

Locate the correct existing Save52 by verified evidence/identity, not filename guesswork. Ground the **Feynman I** and **Feynman VII-b** endpoints, ordinary pads, terminal/pair relation and child inventories using independently supported saved identities and ownership (not the UI labels alone). Determine what the selected outpost/cargo references actually contain in the saved snapshot, including possible Isotopic Coolant and Supercooled Magnet identities/quantities if supported. If save decoding does not cover a relevant record, investigate the representation and native reader/writer for that *specific* record sufficiently to explain or bound the question. Distinguish what Save52 proves from what could have changed in the running game before the screenshot. Analyze competing, falsifiable explanations of empty **Outgoing Resources** and **Build Resources Needed**; where possible rank them against actual provider code, item data and evidence. Do not simply relabel empty display as empty physical pad cargo.

### D. Runtime/save correspondence and refresh

Create a field-by-field mapping: definition/configuration → serialized representation → loader/reconstruction → current runtime source → UI adapter/binding → displayed text. For each field classify PERSISTED, DEFINITION-DERIVED, RECONSTRUCTED, TRANSIENT or UNKNOWN. Explain refresh while terminal remains open, as far as provable offline, distinguishing event-driven UI invalidation from underlying transport updates. Show any necessary freight-state dependency but stop before investigating ship flight/unloading logic itself unless a bounded trace is indispensable to explain a particular UI field.

### E. C2/C3 boundary and scoped questions

Record, but **defer detailed mechanism research** on departures, ship loading/unloading/round trips, stranded/returned freight, remote saturation, inter-system Helium-3 use, transport simulation while distant/unloaded, and transport recovery. If some cargo UI value depends on these, identify the exact provider/producer boundary and carry forward a concrete question. Preserve the user's earlier hypothesis that cargo seen in an origin incoming bay might be undelivered freight returning from a blocked destination **as an open hypothesis**; don't promote it into a fact. Keep local-output S2 findings intact.

## 3. Backlog additions to preserve durably

Add concise entries in the existing backlog/decision structure without reopening them in C1:

1. **Storage-container side indicator:** percentage, green/yellow/red bar thresholds, refresh triggers, effective occupancy/capacity source, clipping or >100% after overcapacity production. User screenshot from Save52 is a reference, not live instrumentation evidence.
2. **Remote outpost diagnostics feasibility:** query from elsewhere (e.g. Lodge) for Workshop membership, individual production eligibility, power, inventory, capacity, output-link graph and pending work; distinguish snapshot from trend and unresolved reference from stopped/empty.
3. **Remote reference/producer lifecycle:** whether ordinary distant/unloaded states cause failed handle resolution, sentinel/pending bookkeeping, identity reconciliation and actual delivery/catch-up, versus exceptional/deletion cases.
4. **Local stock re-redistribution:** what (if anything) flushes old upstream contents when a downstream container regains free capacity, beyond established link-add and explicit/script triggers.
5. **Deferred chest/display phase:** Shared Outpost Storage cross-outpost access and workbench sourcing; which inventories (including shared storage) contribute to outpost database **Stored Resources** and when that panel refreshes.
6. **Cargo C2 case:** reported outgoing-to-incoming spillover and remote failed delivery/return-freight hypothesis; investigate only when freight transport is in scope.

Avoid duplicate backlog entries where present: amend/clarify existing ones with links and provenance instead.

## 4. Evidentiary and stopping standard

Apply the previously agreed **reasonable engineering confidence / explanatory sufficiency** approach and the repository's confidence vocabulary (`PROVEN`, `STRONG`, `PROVISIONAL`, `OPEN`). A coherent native producer/binding path supported by saved case evidence is sufficient for an ordinary scoped answer; don't demand a live observer to exclude every hypothetical exception. Conversely, do not claim a specific *historical UI session* executed a path without observation. Missing provider code is a **specified evidentiary gap**, not proof of a missing feature or a fabricated explanation. Resolve promising in-scope leads rather than stopping at the first unrecognized UI binding; keep the investigation finite and directly tied to C1 field questions. Do not commission generic SWF tooling, save writers, game-wide inventory extractors, debugger backends or an end-to-end freight simulator.

Any suggested future test must state the exact opposing predictions, smallest observable discriminator, cost/risks and permission boundary. It is not automatically necessary for C1 acceptance. Preserve conflicting observations and source provenance and do not retroactively raise the agreed acceptance threshold.

## 5. Completion contract (frozen for this assignment)

- **Task type / deliverable:** Offline research; indexed C1 answer-first report, detailed UI/configuration native contract, Save52 correspondence, source/function/register/evidence references, deferred-backlog updates, review package.
- **Scope / protections:** Explicit §1–4 only. Read installed definitions, compiled/script/UI assets and protected save *copies*, plus bounded project-owned diagnostic scripts if essential. Originals, analysis DB, saves, game files, config and Git HEAD/index must remain unchanged. Preserve both-drive 40,000,000,000-byte free-space safeguards where relevant; no game, deployment, save editing or external disclosure.
- **Mandatory acceptance:** (1) correct Save52 endpoint and screen provenance; (2) outpost/pad candidate and pair semantics; (3) each visible field's supported provider/meaning/refresh with exact gaps and no invented values; (4) reasoned, evidence-ranked explanation or precise discriminating blocker for empty outgoing/build-needs panels; (5) saved object/pair/inventory-to-runtime/UI correspondence; (6) C2/C3 boundaries and all six backlog topics durably recorded without duplicate scope expansion; (7) primary evidence, regressions/protected hashes, source/version pins and answer-first presentation; (8) independent review ACCEPT and complete verified text patch package. For requirements (3)–(5), a negative/partial result is acceptable **only** after documented bounded investigation of the specific unresolved provider or save representation, with concrete evidence and a useful next discriminator—not a generic “not measured live.”
- **Optional:** An independently verified example from a second known link, if available at low cost. Not required for completion.
- **Negative closure:** Preserve observed non-matches, absent fields within qualified coverage, mismatched list contents and counterexamples. No universal absence claim based on partial UI/source coverage.
- **Continuation authority:** Diagnose/correct/retest in scope and remediate reviewer REWORK without requesting a new brief. No unilateral criteria changes.
- **Exit/escalation:** Stop only at specific missing authority, inaccessible essential source, protected-input/integrity/resource risk, or demonstrated need for disallowed live intervention. Complete independent authorized work and record a precise resume checkpoint. A completed bounded analysis can legitimately report a named scientific unknown; it must not silently treat its incomplete mandated exploration as PASS.
- **Review artifacts:** Mandatory PASS/FAIL/NOT TESTED matrix, evidence pin ledger and exclusions, source hashes, tests/negative cases, independent reviewer verdict (verbatim locally), `git status --short`, task-only and complete diff under `.local-work/diffs/`, manifest, exact forward/reverse reconstruction checks, link/UTF-8/whitespace audit and Conventionally styled suggested commit. Preserve private/proprietary saves/screenshots/native data locally; textual diff may cite paths/hashes, not raw bytes.

**Suggested report structure:** `docs/experiments/cargo-links/configuration-ui/{report.md,native.md,save52.md,review.md,functions.csv,sources.csv}` (adapt to existing project naming conventions). Update `docs/RESEARCH_STATE.md`, `docs/BACKLOG.md`, `docs/DECISIONS.md` if warranted, `docs/subsystems/` and brief index. Avoid inventing stable research IDs; allocate via project convention. No automatic C2/C3 execution.
