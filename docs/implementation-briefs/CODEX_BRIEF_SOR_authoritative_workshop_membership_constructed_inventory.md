# Codex research and implementation brief — Authoritative Workshop membership and exhaustive constructed-object inventory

**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)  
**Starting state:** Continue from the latest committed and synced research, including the durable-position consolidation and extractor/resource association work.  
**Authorization:** Offline research, read-only analysis of existing saves/game definitions, implementation, disposable testing, documentation, independent review. **No Starfield launch or attachment, save alteration, deployment, staging, commit, or push.**  
**Deliverable status:** REVIEW-REQUIRED until maintainer approval.

## 1. Purpose and acceptance contract

Recover **which player-constructed object instances belong to which ordinary outpost/Workshop** in saved Starfield data, and produce an **exhaustive, one-row-per-instance inventory within a precisely stated supported representation**. Do not make object-category knowledge a prerequisite for detecting membership. This is a foundation for later analysis of extractors, storage, power, greenhouses, animal husbandry, manufacturing, robots, crew, cargo links, furnishings and decoration.

The work is **not** a cargo-link, power-link, output-link, inventory-contents, production-rate or planetary-coordinate reconstruction. These can be future studies. Categorization and filtering are not required for inventory completeness.

**Required final outcome:** (A) a deterministic, supported owner-to-instance inventory with independent evidence, coverage/ambiguity accounting and reproducible tests; or (B) a completed evidence-bounded negative investigation establishing precisely which membership/population relationships cannot be recovered from authorized data and what is needed to finish them. An unsupported partial inventory, a list of promising fields or an untested association heuristic is **INCOMPLETE — CONTINUE**, not a final deliverable. A scoped positive result may coexist with documented unresolved populations; do not claim universal completeness without evidence.

## 2. What counts as an instance

Include every **player-constructed outpost object** recognized under the recovered representation: extractors, generators, industrial builders/fabricators, greenhouse and husbandry buildings, habs, floors, walls, landing pads, cargo-link equipment, storage, furniture, lighting, decorations, displays, and unfamiliar or uncategorized constructions. Preserve **each physical instance** separately even when several share a base object: twelve chairs produce twelve rows.

**Containers are in scope as constructed instances**, including conventional storage units, chests, containers used in production/logistics, weapon racks, mannequins, armor/weapon displays, cases and other constructed display fixtures. Include empty containers and displays. **Their contents are out of scope**: no obligation to recover item stacks, quantities, mounted-equipment links, modifications, transfer behavior or contents ownership. Preserve raw inventory/display relation tokens if encountered naturally and cheap to record, but do not turn stored/displayed item references into extra constructed-object rows unless independently proven constructed themselves.

Distinguish the ordinary placed reference from other save records that mention its base definition, relationships, inventories or recipe. Revisit the **17 additional Save52 extractor-base mentions outside the recognized base slot** as potential negative controls/representation leads; do not assert that they are extra extractors or fabricators without evidence.

Retain disabled/deleted/otherwise inactive instance evidence with precise state and provenance, without silently suppressing records or inventing `IsDeleted` semantics. Ordinary player Workshop objects should not be confused with procedurally generated terrain pack-ins, static POIs, loose loot, NPCs or ships unless a native/saved construction relationship supports membership. Do not use geometric proximity as a substitute for authoritative ownership.

## 3. Ownership investigation

Trace saved identity domains and actual ownership paths from constructed references to their Workshop/beacon: direct owner, intermediate relationship, extra data, workshop object handles, ownership tables, serialization units or other mechanisms as supported by evidence. Reuse established ordinary beacon and planetary identity models, the bounded relationship/reference readers, controlled-save differential methods and Save52 extractor associations.

Explicitly distinguish saved reference identifiers, base FormIDs, plugin identity domains (full/medium/small), dynamic handles, Workshop IDs, beacon records, runtime pointers and historical/deleted identities. Specify the **authoritative evidence path** for assigning an instance to one Workshop; report secondary contextual evidence as such. Handle two outposts in the same continuous landing area (SOR-002/SOR-003) without a nearest-beacon shortcut. A null/ambiguous/conflicting owner must produce an **unresolved** entry with reason and relevant raw provenance, not a guessed assignment or silent omission.

If there are multiple constructed-reference encodings, investigate and characterize them. Do not restrict the claimed complete inventory to a small handpicked set of recognizable classes. Preserve negative controls that distinguish player construction from base-object mentions and nonconstructed references.

## 4. Evidence and validation

Start with existing controlled construction/deletion checkpoints (including the extractor/solar/storage/link observations) and validate transition-by-transition: absent before creation, present after construction, retained across unrelated edits, and deleted/disabled state represented accurately. Use distinct controls for non-extractor object types where existing corpus supports them; do not infer general coverage solely from the iron extractor case.

Apply to mature **Save52**: retain the 17 active outposts and two historically removed/disabled beacon records as distinct owners/history; do not reassign their structures to an active outpost. Supply per-outpost inventory counts, a full instance export and an explicit unresolved/possible-missed population. Distinguish what has been independently checked against previously maintained network JSON (which may corroborate selected known objects, not establish every chair or decoration).

Include positive and adversarial tests for collisions across identity domains, duplicated base definitions, unrelated reference mentions, mixed record types, truncation, disabled flags, historical outposts, missing owner edges, ambiguous ownership and unknown base objects. Preserve all protected save originals, frozen predictions and earlier research/evidence. **No arbitrary count, processing-duration or output-size quotas**; retain the 40,000,000,000-byte free-space guard on both C: and D: for substantial analysis. Fail safely on actual integrity/resource failures.

A reviewer should independently challenge **completeness of the detected population**, not just correctness of assigned rows: false negatives matter as much as false positives. Document confidence, coverage and application readiness separately.

## 5. Outputs

Deliver within the repository, with locations following its existing conventions:

1. **Deterministic offline inventory CLI/library** that accepts qualified save inputs and game-definition context where required. Output one row per constructed instance, with stable ordering and schema/version documentation; provide CSV and/or JSON as justified. Preserve raw instance reference, base identity and plugin provenance, Workshop/beacon identity if established, record type, display/Editor name if resolvable, state flags, saved-record source offsets, optional raw position, and association status/reason. Unknown display names must not suppress rows.
2. **Machine-readable ownership ledger** and unresolved population, including competing ownership evidence where applicable, not just summarized totals.
3. **Save52 per-Workshop summary**, inclusive of inactive/historical owners as distinct entries, with clear counts and coverage limitations. Large furniture/decorative inventories must remain intact in the machine-readable output, not condensed to category counts.
4. **Scientific report and dependency map**, demonstrating the ownership mechanism and construction-instance detector, counterexamples and exact boundaries of supported representations; differentiate authoritative joins, corroboration and inference.
5. **Executable validation/tests and reproducibility receipt** spanning controlled checkpoints and mature saves, including independence of expected results and unchanged protected inputs.
6. **Capability/backlog note** for contents/display associations and future categorization/filtering; do not implement content extraction or unrelated functional links.
7. **Independent review and acceptance matrix**, plus complete/task-only review diffs under `.local-work/diffs/`, `git status --short`, manifest and exclusions. Do not stage merely to generate a diff; include untracked authored text in `-complete.diff`.

Large raw/private save exports, proprietary binaries and bulk generated evidence stay in ignored local storage; commit only suitable authored source, documentation, fixtures permitted by project policy and lightweight reference summaries. Record exact local evidence paths/hashes in review receipts without embedding private raw data.

## 6. Execution and agents

Follow `WORKFLOW.md` and the Research Execution and Completion Protocol. The primary agent owns the complete assignment, investigates failures, corrects code and reruns tests **within this task**. Preserve negative evidence; do not use a missing record type or failing test as an automatic handoff. Complete scientific analysis and review before final submission.

Use **one independent reviewer**, and optionally **one specialist researcher**, maximum **two active sub-agents simultaneously** (excluding primary). Suggested specialist responsibility: independently audit Workshop-ownership serialization paths and search for constructed-instance populations omitted by the main detector, especially furniture, containers/displays, inactive references and multiple encoding forms. The reviewer challenges evidence, independence of controls, systematic omissions, semantic claims and any proposed terminal evidence boundary. Reviewer verdict ACCEPT / REWORK / ESCALATE; REWORK must return to the same assignment.

The specialist's distinct contributions, corrections and counterexamples should be recorded briefly. No need to continue assessing whether the reviewer role is generally worthwhile unless workflow regression appears.

## 7. Authority boundaries and closing requirements

Entire assignment **offline and read-only against protected game inputs**. Do not launch Starfield, install/alter SFSE plugins, attach a debugger, create or alter saves, inject native calls, or touch Vortex deployment. Do not reopen native Z or terrain-procgen investigations. Do not stage, commit or push.

A negative result must be properly completed and independently reviewed: show which candidate mechanisms and alternative encodings were pursued, decisive counterexamples, exact missing evidence, and what later acquisition would discriminate them. No generalized 'more research required' conclusion.

The final response must provide a concise scientific conclusion, coverage/exception counts, actual test results, reviewer disposition, exact artifacts and patch paths, protected-input preservation, and a suggested commit message. **Do not present an inventory as exhaustive for Save52 or for all player constructions unless the population-detection completeness claim is supported.**

Suggested subject upon acceptance: `research: reconstruct Workshop ownership and constructed-object inventory`.
