# Codex implementation brief — RG2-D5BC

**Title:** Remaining Subsystem Guides and Technical References; 18-Subject Collection Consistency Check  
**Project:** `D:\Projects\starfield-outpost-research` / `gooberpede/starfield-outpost-research`  
**Type:** Bounded documentation synthesis, integration and independent review only  
**Authority:** This brief; accepted D5AY, D5AZ, D5BA and D5BB authoring/review pattern; `docs/guides/AUTHORING-STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/VISUALIZATION_STANDARD.md`, `docs/EVIDENCE_STANDARD.md`, existing source/review registers and publication governance.  
**Working rule:** **One concurrent subagent maximum.** No staging, commit, push, publication, original-file relocation, installed-game changes or save modifications.

## 1. Objective and reader contract

Complete the planned **18-subject** guide/reference collection by authoring the five remaining subsystem pairs and conducting a **bounded collection-wide consistency and navigation check** against the 13 previously accepted pairs. These are two related deliverables within one assignment: (1) five independently reviewable subject syntheses and (2) a precise, non-destructive check that the whole collection is navigable, internally consistent and properly qualified.

Write for technically experienced readers acquainted with reverse engineering or Creation Kit modding but unfamiliar with this investigation's chronology. Explain the useful mechanism and gameplay implications first; place exact native/save contracts and evidence challenges in companion references. Organize by what the system does, **not** by the order in which CR/DA/SD/RC investigations were performed. D5AY is a pattern, **not** a mandate for identical lengths, sections or diagram counts. The access/save-framing subject may reasonably be more technical than an ordinary gameplay guide.

This assignment **does not** re-open scientific investigations, independently revalidate inaccessible raw witnesses, produce a save importer or integration API, or rewrite the already accepted 13 subjects. Preserve original historical claims and their contemporary scope/status; reconcile current-facing statements using the best subsequently reviewed evidence without silently rewriting history.

## 2. Controlling questions and required documents

| Question | Reader guide | Technical reference | Principal reader question |
| --- | --- | --- | --- |
| **Q1 — Crew and robots** | `docs/guides/crew-and-robots.md` | `docs/reference/crew-and-robots.md` | How are people and constructed robots counted, assigned, restored and made eligible to contribute to an outpost, and what distinguishes a displayed skill from a real effect? |
| **Q2 — Outpost defense** | `docs/guides/defense.md` | `docs/reference/defense.md` | What starts or prevents an attack, what defenses actually affect, and how do damage, destruction, Integrity and repair differ? |
| **Q3 — Containers and displays** | `docs/guides/containers-and-displays.md` | `docs/reference/containers-and-displays.md` | Where do stored and displayed items reside, which object owns each item or visible reference, and what does save restoration prove? |
| **Q4 — Locations UI** | `docs/guides/locations-ui.md` | `docs/reference/locations-ui.md` | Where do the outpost panel's identities, counts, faction/level values and visual representations come from, and when are they current? |
| **Q5 — Access and save framing** | `docs/guides/access-and-save-framing.md` | `docs/reference/access-and-save-framing.md` | Which definition, script, saved, native and current-state information channels are known, how should they be interpreted, and which interfaces are actually validated? |

Also deliver:

- Updates to `docs/reference/glossary.md`, only for new or materially clarified terms, preserving canonical, **concrete, plain-language, noncircular** definitions and important historical aliases.
- Bounded entries and cross-links in `docs/guides/README.md` and `docs/reference/README.md`, retaining all 13 existing pair routes. Update small stale *cross-references* in previously accepted guide/reference pages only when demonstrably necessary; avoid broad prose revisions.
- A **tracked, compact** D5BC claim-to-evidence crosswalk, collection-consistency record and final review/handoff under `docs/audits/remaining-guides-d5bc/` (e.g. `claims.md`, `collection-check.md`, `README.md`). Exact names may vary; state chosen paths and maintain clear separation between author evidence and reviewer judgement.
- One task-only unified diff, optionally one complete diff including this supplied brief, complete changed-file manifest and reproducible patch hashes. Working receipts/intermediate exports belong in `.local-work/` unless indispensable, small, lawful, reader-facing tracked assets have been specifically identified.

**Q1–Q5** are separately adjudicated; the **collection-wide check** is a cross-cutting acceptance gate, **not** a sixth scientific investigation.

## 3. Scientific and documentary requirements common to all five

For every consequential claim, distinguish **definition/configuration**, **saved snapshot or serialized identity**, **runtime resolution/ownership**, **current eligibility**, **actual event/effect**, and **derived UI/reporting**. Not every system has each stage, and a diagram must not invent a universal state machine. For each native interface identify object/function/record class, owner, writer and reader, identity/address frame, lifetime and supported path, where established. Definitions, declarations, and static causal paths are not direct observations of particular game sessions.

Create the claim/evidence crosswalk **before** final explanation: bounded claim, pinned version/sample and prerequisites, STATIC/SAVE/RUNTIME/derived evidence type, exact original report/section, source review and later correction, negative case/counterexample, and public access class. Explain cases where later work supersedes *current interpretation* while preserving original documents. Do not elevate proposed claims to proven runtime results because a reviewer accepted a *bounded* static mapping. Preserve original historical uncertainties and negative cases.

The installed retail build researched in most cited native work is **Starfield 1.16.244.0**; use actual pinned builds and source hashes where relevant, rather than implying all load orders, DLC, other versions, or active overrides are identical. Keep FormIDs, dynamic saved IDs, native pointers, handles, editor IDs and reference identities separate. Mark RVA versus preferred static VA versus runtime VA; saved-stream offsets use an entirely different byte domain. Explain difference between saved conditions and effective values reconstructed after load.

A public-facing reference to a private `.local-work/` path or hash is **not evidence access**. A reproducible derivative/calc from tracked inputs is narrower than a replay of the protected original. If an indispensable witness has no durable lawful public access route, record **PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING**. Do not extract/package original saves, decompilation, screenshot or proprietary source material as part of D5BC. Existing B4-F1 release asset decisions, D5AS/C19 evidence work and B6 rights/clean-checkout gates remain separate.

## 4. Q1 — Crew assignment, effective skills and constructed robots

**Primary research:** `docs/experiments/crew-lifecycle/report.md`, `native.md`, `persistence.md`, `examples.md`, `review.md`; `docs/experiments/crew-skills/report.md` and its technical/evidence/review pages; `docs/experiments/robots/report.md`, `catalogue.csv`, `limits.md`, `effects.md`, `lifecycle.md`, `persistence.md`, `review.md`. Reuse `docs/experiments/workshop-population/`, existing `docs/guides/identity.md`, `docs/guides/power.md` and the production guides where their authority matters.

Guide narrative: assignment and crew limits; differences between human staff and built robots; crew skill possession, applicability, lifecycle and eligibility; timing/power outcomes; saved assignment versus currently contributing actor. Explain why a crew roster or visible skill is not itself proof of effective bonuses, and why physical arrival is not a universal activation switch. Show player-facing examples with explicit limits.

Technical reference must clearly separate:

- Human crew-station/capacity checks, membership/assignment and registered actor handles versus constructed **robot quota** and automatic assignment; robot count is not human slot cost.
- The **eight** ordinary direct constructed robot variants (Garden, Sanitation, Model A01/A02/A03, Security minibot, Model S01, Model A04). Earlier five-variant CR2 coverage was a positive *perk-bearing subset*, corrected/extended by R1, **not** the complete ordinary construction catalogue. Five process-perk robots and three without demonstrated ordinary A1/DB bonus must not be treated as eight equal production boosters.
- Robot construction threshold **three**, ordinarily **six** with the qualified Management perk increase, as scoped construction-limit results, not universal simultaneous active-actor guarantees.
- Crew possession/registered rank, effective active entry buckets, assignment environment, eligible life/Health state, consumer-specific filters and actual A1 timing or generator-power contribution. Distinguish ordinary human Outpost Management and Engineering from unrelated ship skills, including **ship** versus **outpost** Aneutronic Fusion; the Model A03 outpost power route is a special positive case.
- Current modifier query and due-cycle timer reset: changing assignment does not retroactively recompute already processed production, and a retained countdown may continue until its next due reset. Arrival/loaded 3D not explicitly tested by these consumers is not a promise every unloaded actor always participates; resolution, bucket readiness and process transitions matter.
- Saved owner/assignment/actor/template and rank evidence versus reconstructed handles/active entries after load; no inference of perpetual skill operation from a saved assignment alone.

Include a concrete example of a positive perk effect and a contrasted noncontributing case, plus a challenge path to CR3/R1 review/counterexample.

## 5. Q2 — Attack opportunities, defense and Integrity

**Primary research:** `docs/experiments/outpost-defense/report.md`, `attacks.md`, `defenses.md`, `integrity.md`, and relevant saved/state/review pages. Reuse accepted crew/robot, construction, identity and power pages strictly where needed.

Guide should distinguish the **opportunity for an attack check** from an attack actually starting; the ordinary versus Armillary/Starborn path; same-planet eligibility and environmental/spawn constraints; behavior while player/outpost objects are unloaded; physical combat versus attack-selection scoring; partial damage, destroyed state and repair. Avoid presenting a random check window as observed raid periodicity.

Technical reference should document exact bounded shipped script/native predicates and evidence:

- Beacon load and qualifying resource-object placement can arm a **one-shot random 12–48-second opportunity timer**. The callback has planet, permission, cooldown, resource and cargo-link logic; this is **not** a guaranteed attack every 12–48 seconds. Define timer's domain and qualifying triggers, not a universal player-visit rule.
- The special Armillary/MQ condition and separate **50% roll per eligible check** do not establish a measured encounter rate or rewrite the ordinary seven-day cooldown rules. Distinguish Starborn initiation from the ordinary selector.
- Mapped attack selection does **not** read a universal defense score from turrets, crew or robots. Real combat can change surviving attackers and thus outcomes; absence in the *mapped selector* does not prove that all defenses are irrelevant.
- Build-mode **Integrity** reflects current effective Health relative to permanent/base Health under the qualified object-type paths, with a hidden sentinel on invalid denominator; distinguish actor-turret and destructible-object Health, retained damage modifiers, destroyed state, disabled/deleted flags, repair effects and what persists.
- A saved damaged object does not prove the cause, time, attack frequency or later repair; no live frequency/attack resolution or fully universal post-load behavior is implied.

Present at least one attack-path decision table and an example contrasting physical damage with the displayed Integrity condition. Keep unqualified object classes and historical events visible.

## 6. Q3 — Ordinary containers, display slots and mannequins

**Primary research:** `docs/experiments/containers-displays/report.md`, `definitions.csv`, `native.md`, `saves.md`, `review.md`, plus selected ordinary fixture/assembly and Item residence records. Link to `docs/guides/storage-and-output-links.md`, `docs/reference/storage-and-output-links.md`, and `docs/guides/shared-storage.md` for **other** inventory domains.

Guide should make the physical residence model intuitive: ordinary decorative chest contents reside as item stacks in the fixture; display cases can turn admitted inventory items into separately represented world references and slot lists; mannequins are actor-based equipment/inventory systems. Distinguish displayed appearance from actual item ownership or right to take, and saved state from visually proven restored display.

Technical reference must document:

- Construction/definition classification and exclusions: recipe/leaf rows versus unique definitions, ordinary decorative chest forms versus display pack-in children, mannequin NPCs and comparison-only objects. Do not promote cut/test/mission/installed add-on variants into universal ordinary gameplay support.
- Capacity and inventory admission (effective versus base), prohibition of ordinary local output links for qualifying decorative chests, and distinctions from industrial storage.
- Container inventory stacks, display-generated item references and slot lists, mannequin actor inventory/equipment, Workshop membership, fixture ownership and item permissions as **separate relationship/identity channels**.
- Native display admission/removal, save writer and loader/fixup chains and supported saved joins; current equipped/visually restored state only where supported. Record unsupported actor tails, stack extras and render-reload behavior instead of inferring empty stock or complete visual reconstruction.
- A negative case (e.g. cosmetic/visible equivalence or saved join does not prove a successful live deposit/theft/repair/reload) and the original review route.

Use diagrams/tables only where they illuminate the different residence/ownership paths. No 3D rendering or new gameplay testing.

## 7. Q4 — Locations outpost panel, excluding Stored Resources repetition

**Primary research:** `docs/experiments/locations-outpost/report.md`, `field-lineage.md`, `native-and-ui.md`, `reuse-and-gaps.md`, `methods.md`, `review.md`; earlier Workshop registry/Workshop population/Locations field provenance. Link directly to the accepted `docs/guides/stored-resources.md` and `docs/reference/stored-resources.md` rather than reproducing its inventory aggregation in depth.

The guide should explain which outposts appear, how selection and presentation work, what Cargo Links, Crew and Outposts Built count, how faction and level are resolved, and what system/planet/star/marker imagery actually depicts. Emphasize that the panel combines **different producer paths and refresh epochs**: it is **not** an atomic, continuously live snapshot of the whole outpost.

Technical reference should preserve:

- Registered/resolvable Workshop collection, default-keyword exclusions, selected EntryObject and body/system metadata, versus a universal active-player/save outpost census.
- Cargo Links count from qualifying resolved, non-disabled, active local endpoint memberships; not link-pair count, pad quota or guaranteed operating route.
- Crew badge as assignment-handle list length, not a resolved at-display actor census, capacity or active skill contribution; robots are not universally excluded.
- Outposts Built numerator from relevant collected entry count and denominator from the player's **base** OutpostMaxDeployed value, distinct from placement's effective remaining capacity.
- Faction from location/system owner resolution and emblem categorization; level from system-location data, **not** the player's own level or an unqualified outpost-combat difficulty.
- System/body markers and schematic orbital images versus true surface/beacon-coordinate photography. Selection can repaint copied values while separately requesting body metadata; a plausible screen does not certify a single refresh epoch.

Include a bounded field-lineage table with source owner, identity, refresh, UI consumer and evidence tier, and at least one failure/negative interpretation challenge.

## 8. Q5 — Capability access, save framing and integration limits

**Primary research:** `docs/audits/outpost-rc1-2026-10/report.md`, `capability-access.md`, `gap-reconciliation.md`, `papyrus-interfaces.md`, `review.md`; existing `save-analysis/`, `docs/EVIDENCE_STANDARD.md`, `docs/PROVENANCE.md`, `docs/function-register.md`, `docs/state-register.md` and pertinent accepted subsystem reference pages. Do not create a second competing register or rewrite established save-analysis tools.

Unlike the gameplay guides, organize this guide around:

1. **What information exists and where?** Definition records/ESM/CK, Papyrus declarations and shipped scripts, saved file framing/identities, native runtime structures and exposed consumers, UI projections and independent research instruments.
2. **What can be reconstructed under what conditions?** File/version and byte domains, FormID/reference/handle/pointer conversion, saved extras, source framing, parser coverage and unsupported branches, reconstructed objects/owners, current effective state and its observation limits.
3. **What is actually supported for access or modification?** Interface declarations, observed call paths, known preconditions, risk and authority; distinguish discovery of a function or declaration from a validated external, safe, callable API.

The technical reference should present a **capability/access matrix**, using RC1's actual categories and statuses, not hypothetical integration APIs. Include exact existing technical registries and original per-subsystem evidence links without copying hundreds of function addresses. State where read-only offline reconstruction is possible, where original protected data is required, where current runtime access is merely a candidate, where unsupported record forms/tails remain, and which methods have not been validated at all. Do not infer impossibility from a missing known interface, or safety from a native call observed internally. A save serializer/writer path found in disassembly does not authorize save editing.

Preserve RC1's original reconciliation and gap results, including that an old open question may be retired, conditionally answered or still a real dependency. Explain scientific completeness versus practical tool readiness and publication eligibility. Do not implement an importer, PEX/native bridge, script, mod, observer, or caller prototype.

## 9. Visuals, glossary and evidence access

Each pair should have an appropriate explanatory visual **when it adds genuine value**: actor assignment and consumer eligibility, attack check versus damage, item residence/slot/actor ownership, Locations field/refresh lineage, and access channels/save reconstruction are possible candidates. Use editable Mermaid with captions, branch limitations and linked evidence. Quantitative figures need sourced counts, unit/denominator/frame labels and distinguish measured/derived/illustrative quantities. Provide prose/table alternatives. Test rendered appearance if available; accurately record inability if not. Do not require a fixed count or invent data to fill an illustration.

Extend `docs/reference/glossary.md` only as needed. Entries must **identify the concrete thing** (native structure, engine operation, save record, Papyrus interface, actor perk, UI-derived count or researcher term), describe what it actually does, avoid self-reference/unexplained synonyms, resolve confusing names and cite source-appropriate authority. Examples worth considering: CrewExtraData, skill rank versus active entry, robot construction quota, defense attack-opportunity timer, Integrity, display slot/item reference, mannequin actor equipment, Locations entry/refresh epoch, saved record framing, capability surface, native function declaration, static VA/RVA. Reuse existing canonical entries rather than duplicating them.

## 10. Final 18-subject collection consistency check

**Required and bounded.** Inventory the collection from the D5AX proposed 18 guide/reference stems, reconciled with the accepted D5AY/D5AZ/D5BA/D5BB documents. There should be **18 current guide entry points and 18 corresponding reference entry points**, not a claim of 18 newly created pairs. The target stems are:

| Previously accepted (13) | New D5BC (5) |
| --- | --- |
| `resource-generation` | `crew-and-robots` |
| `identity` | `defense` |
| `position` | `containers-and-displays` |
| `nominal-biomes` | `locations-ui` |
| `construction` | `access-and-save-framing` |
| `inorganic-production` | |
| `organic-production` | |
| `fabrication` | |
| `power` | |
| `storage-and-output-links` | |
| `cargo` | |
| `shared-storage` | |
| `stored-resources` | |

Run and **record** these checks:

1. **Coverage and navigation:** all 18 pairs exist; both indexes have discoverable entries; every guide reaches its own reference and the authoritative original report/review. Confirm from existing root navigation that intended entry points are reachable (without undertaking a broad root README rewrite); test case-sensitive links/heading anchors throughout the current guide/reference collection and changed audit/index pages.
2. **Terminology:** compare glossary and the 18 pairs for consequential overloaded terms—Workshop owner, active, registered, eligible, constructed, persisted/restored, producer, source, resource, inventory, capacity, shipped, assigned, power, refresh and similar terms. Record and resolve demonstrated semantic collisions, not stylistic synonyms.
3. **Cross-subsystem authority:** inspect the actual handoffs: resource geometry→extractor eligibility/producer; identity→crew/robots/defense/Locations; construction→robot/turret quotas; production/power→crew effects; producer→storage/local link; storage→cargo/shared/Stored Resources; save framing→all reconstructed claims. Ensure distinct state, identity, writer, consumer, clock and evidence domains are not conflated. Explicitly cross-check UI cached counts versus native effective or physical state.
4. **Reader independence:** choose a small representative route across multiple subsystems that begins at an ordinary question, follows dependencies through guides/references and ends at accepted original evidence/counterexamples without requiring knowledge of brief IDs or private local file paths. Record where it fails and repair links/small explanatory transitions.
5. **Publication dependency inventory:** list only **claim-relevant indispensable** evidence routes still pending for the newly created pages and material collection-wide inconsistencies. Carry forward existing D5AS/C19/B4-F1 and historical-save access dependencies by reference; do not launch an exhaustive local-corpus inventory, asset packaging or new publication scope audit.

**Change authority:** Fix broken cross-references, missing index entries and small unambiguous terminology/navigation errors in previously accepted pages. For a substantive science disagreement, record exact conflicting claims and original evidence/reviews, mark it for maintainer decision, and **do not silently revise the accepted mechanism** or stage a wholesale rewrite. The collection consistency verdict must distinguish *mechanical coverage*, *semantic consistency*, *provisional evidence-access issues*, and *out-of-scope open scientific questions*. Keep a concise, actionable findings table (issue, cited pages, severity, action taken/deferred, reason), including explicit NONE where a class is clean.

This is an integration check, **not** a substitute for later B6 exact-tree, public-rights, real asset-hosting or clean-checkout validation. In particular, do not claim all first-release evidence accessible just because the links resolve to a tracked report.

## 11. Verification and independent review

Perform **three reader journeys per new pair (15 total)** on the **final corrected pages**:

1. **Understand:** follow the ordinary mechanism and explain one practical consequence plus one meaningful limitation.
2. **Reproduce:** run a bounded check from tracked inputs using a documented command, or expressly conditional reproducible public-source contract if genuinely lawful/portable; state the data and result, as well as what it does not establish. For topics without a defensible portable numeric example, use a transparent tracked text/relationship/definition check rather than fabricating an experiment or claiming private bytes were replayed.
3. **Challenge:** reach original report, review and a negative case or later refinement; preserve source-scope and evidence-access limits.

Additionally carry out the **collection-level** checks in §10. Verify every changed link/anchor, plus the 18-pair entry/link paths. Check exact static/saved counts, identities, address domains and denominators in the five new references against tracked original work. Validate Mermaid sources and rendering where feasible. Review the full final prose for circular glossary definitions, omitted negative cases, fabricated current-state authority and misleading interface or persistence guarantees.

Require **independent final scientific, engineering/evidence and editorial review** of the corrected snapshot. Evaluate Q1–Q5 **individually**. The reviewer must specifically challenge: robot catalogue versus effect-bearing subset; assigned versus active crew; attack opportunity versus attack occurrence; saved damage versus observed attack; inventory versus display reference versus actor equipment; Locations badges versus real operational state; and declared/read native interfaces versus approved mod access. Inspect the collection-consistency record and independently sample consequential cross-subsystem comparisons. Record first-review failures and subsequent fixes without erasing review history. Do not equate an inaccessible receipt, textual self-attestation or a patch applying with direct independent verification.

## 12. Acceptance criteria

| ID | Requirement |
| --- | --- |
| **AC01** | All five exact guide/reference pairs exist as coherent, distinct reader products; originals and prior accepted documentation remain preserved. |
| **AC02** | Crew/robot documentation correctly separates quotas, human slots, eight robot variants, ownership, assignment, possessed skills, active consumers, output effects and restoration qualifications. |
| **AC03** | Defense documentation distinguishes eligible attack checks, separate Armillary path, actual combat, Integrity, damage, destroyed state and repair without claiming measured attack frequency. |
| **AC04** | Containers/displays documentation accurately separates chest stacks, displayed item references, mannequins, membership/ownership and qualified persistence/visual-restoration limits. |
| **AC05** | Locations UI documentation covers supported field lineage, registry/badge meanings, faction/level and graphical elements; distinguishes non-atomic presentation from current operating state and links rather than duplicates Stored Resources. |
| **AC06** | Access/save-framing guide and reference accurately classify definitions, serialization and runtime identity, evidence coverage and interfaces without presenting unvalidated declarations as safe callable APIs. |
| **AC07** | New pages have direct claim/scope/evidence/review/counterexample routes and genuinely classified publication-access dependencies; no local-only file is misrepresented as publicly available. |
| **AC08** | Glossary and both indexes are correctly extended, with concrete, noncircular definitions and working cross-subsystem links; diagrams/figures are evidence-backed and their rendering limits stated. |
| **AC09** | Fifteen new-pair reader journeys, bounded verification examples, links/anchors, hashes/manifest and final-snapshot independent scientific/engineering/editorial review are completed or explicitly blocked with evidence-based dispositions. |
| **AC10 — COLLECTION** | **All 18 pairs** are accounted for and checked for navigation, meaningful terminology conflicts, cross-subsystem identity/state authority and representative independent reader routes. Findings/corrections/deferred science and evidence-access issues are recorded. No unapproved broad rewrite or unsupported release-readiness assertion occurs. |

Report Q1–Q5 as **COMPLETE**, **REWORK** or **BLOCKED** separately, AC01–AC10 as supported **PASS**, **REWORK** or **BLOCKED**, and a separately reasoned **collection consistency** result. A temporary absence of a Mermaid renderer is a documented presentation limit, not an automatic scientific failure; broken links and significant false claims remain failures. A scope-limited pending raw-evidence access dependency need not block a scientifically sound guide **if** transparently classified and not misrepresented as a completed release gate.

## 13. Exclusions, preservation and delivery contract

**Allowed:** Documentation synthesis; tracked crosswalk and review records; modest reproducible examples; glossary/index integration; small demonstrable consistency fixes; independent final review; task-only/complete patches and hashes.

**Not authorized:** New gameplay sessions, native traces/debugging/Ghidra work, running observers, save edits, Papyrus execution, mod changes, data extraction from protected original witnesses, importer/API development, broad revalidation of past research, speculative scientific closure, speculative rewriting of 13 accepted subjects, whole-repository redesign, image/diagram inventions unsupported by evidence, root README restructuring, historical experiment/brief/audit relocation, archival ZIP operation, evidence derivative packaging, new release assets, rights/privacy clearance, changes to `docs/PUBLICATION.md` readiness, staging/commits/pushes/publication.

Preserve the three-layer reader architecture (guides, reference, historical experiments) and original evidence/review paths. Leave **implementation briefs and administrative audits loose** for the separately authorized coordinated archive operation near release. `.local-work/` remains disposable after publication: indispensable public evidence needs a tracked path, separately approved future hosted asset or a genuinely reproducible lawful public method; no promise to retain private working storage. Existing B4-F1 asset selection, D5AS/C19 access route, B6 final clean-checkout/rights/historical disclosure review and final release authorization remain open. Publication is **NOT READY / NOT CLEARED**.

At handoff report: exact changed files, Q1–Q5/AC01–AC10 decisions, five substantive mechanisms/limits, 15 reader journeys and collection consistency checks, identified and corrected contradictions, independent review and unresolved findings, claim-specific publication dependencies, diagram-render limits, manifest and task-only/complete patch **paths and SHA-256**, exact uncommitted worktree/index/HEAD status, and a suggested commit message such as:

`docs(research): complete subsystem guides and cross-system consistency review`

A passing patch reconstruction or assertion of independent acceptance alone is not a completion criterion.
