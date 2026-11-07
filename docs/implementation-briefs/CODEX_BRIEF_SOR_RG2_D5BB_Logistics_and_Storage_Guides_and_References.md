# Codex implementation brief — RG2-D5BB

**Title:** Logistics and Storage: Reader Guides and Technical References  
**Project:** `D:\Projects\starfield-outpost-research` / `gooberpede/starfield-outpost-research`  
**Type:** Documentation synthesis and independent review only  
**Authority:** This brief, the accepted D5AY/D5AZ/D5BA documentation pattern, `docs/guides/AUTHORING-STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/VISUALIZATION_STANDARD.md`, `docs/EVIDENCE_STANDARD.md`, and the repository's existing research and publication controls.  
**Working rule:** One concurrent subagent maximum. Do not stage, commit, push, publish, move originals, or modify installed game/save inputs.

## 1. Aim and reader contract

Produce four coherent reader-facing subsystem guides, four technically detailed companion references, and narrowly scoped glossary/navigation/evidence-review updates. The readership understands reverse engineering or Creation Kit modding but has **not** followed the project's investigation chronology. Explain the ordinary mechanisms in an intelligible order rather than retelling S1/S2/C2/C3/SD2/SD3 assignments. Every consequential claim must preserve its build, input, observation, and inference limits, with direct routes to original evidence and reviews.

The D5AY resource-generation pilot and accepted D5AZ/D5BA pages establish the **pattern, not an inflexible document template**. Subjects may differ in length, chart types and explanatory structure. This work documents established research; it does not resolve open scientific questions by hypothesis or new execution.

## 2. Controlling questions and exact deliverables

| Question | Guide | Technical reference | Reader's question |
| --- | --- | --- | --- |
| **Q1: Storage and local output links** | `docs/guides/storage-and-output-links.md` | `docs/reference/storage-and-output-links.md` | Where is outpost stock actually held, what can accept it, how do directed links move or deliver it, and what happens when capacity or eligibility blocks an operation? |
| **Q2: Cargo links and fuel** | `docs/guides/cargo.md` | `docs/reference/cargo.md` | How does a reciprocal pad configuration result in outbound shipment, arrival, unloading, return freight, timed stages and inter-system fueling? |
| **Q3: Shared Outpost Storage** | `docs/guides/shared-storage.md` | `docs/reference/shared-storage.md` | What is the shared backing inventory, which providers can reach it, who can count or spend it, and which saved and live quantities are known? |
| **Q4: Locations Stored Resources** | `docs/guides/stored-resources.md` | `docs/reference/stored-resources.md` | Which object inventories contribute to each outpost's displayed resource totals, how are they grouped and refreshed, and why is that UI not a separate authoritative physical inventory? |

Produce or update as needed:

- `docs/reference/glossary.md`: concrete, noncircular project-wide entries and disambiguations, not a logistics-only glossary.
- `docs/guides/README.md` and `docs/reference/README.md`: add navigable entries for all eight pages, preserving previous routes.
- A bounded **tracked** claim/evidence crosswalk and review/handoff under `docs/audits/logistics-guides-d5bb/` (for example `claims.md` or `claims.csv`, plus `README.md`), with actual source, review, evidence-access and final acceptance status. Name any additional audit files intentionally; avoid gratuitous bulk receipts.
- A complete task-only unified patch plus an optional complete patch including this supplied brief, with manifest and reproducible hashes. Keep local generated outputs inside `.local-work/` unless they are explicitly reader-facing or essential, small tracked evidence.

**Do not** create duplicate physical-inventory concepts simply because multiple UI or consumer systems mention resources. The four Qs define separate contracts and should cross-link where mechanisms overlap.

## 3. Cross-cutting scientific boundaries

### 3.1 State and authority

Every guide and technical reference must distinguish, where applicable:

1. **Definition/configuration:** form properties, capacity fallback, selection, direction permissions and endpoint assignment.
2. **Live eligibility:** actual resolving references, effective properties, registered Workshop ownership, inventories, links, fuel/readiness, current producer/consumer gates.
3. **Scheduling or planning:** source traversal, destination selection, movement requests, producer countdowns, cargo script deadlines and VM/AI stages.
4. **Realized item changes:** actual removal, inventory insertion, shipment holding, recovery or spending; a possible path, requested count, scheduled stage or UI count is not by itself a measured historical transaction.
5. **Persistence/restoration:** which saved identities, stacks, links, flags or timer fields exist; which live graph and handles are reconstructed; what cannot be inferred from a static save or a snapshot from another epoch.

Describe state **by actual writer, owner, consumer and lifetime**. Distinguish native STATIC and saved SAVE mechanisms from directly observed RUNTIME outcomes. Use source-specific qualifications, not a blanket disclaimer or generic confidence inflation.

### 3.2 Inventory, weight and reporting

Never conflate item stack **units**, inventory **weight**, production **rate**, local graph **reachability**, shared source **eligibility**, and UI **aggregates**. A configured link is not evidence of cargo receipt; a registered source is not current stock; a saved inventory is not automatically a settled loaded inventory; a UI screen is neither a warehouse nor an independently serialized universal outpost ledger. Name where a quantity is physically stored and where it is merely computed.

### 3.3 Boundaries shared with existing guides

Reuse the accepted production guides for extractor/fabricator/organic production and the power guide for generator consumption where helpful. Resource-generation contours and placement eligibility remain in the resource-generation/inorganic-production guides. Avoid reprinting extensive primary tables or duplicating mechanisms. Explain the integration at the point it matters, with direct links.

## 4. Q1 — Storage and local output links

**Primary research:** `docs/experiments/storage/report.md`, `native.md`, `saves.md`, `catalogue.csv`, `review.md`; `docs/experiments/local-output-links/report.md`, `native.md`, `lifecycle.md`, `traces.md`, `saves.md`, `review.md`. Reuse E1/E2/E3 and P1 only for cross-boundary authority.

The reader guide should explain ordinary dedicated Solid/Liquid/Gas/Warehouse storage, multi-item matching inventories, effective capacity and item filters; producer output buffers; Transfer Container's separate ship-access role; cargo-pad child containers; and the directed local output-link graph. Show why **existing-stock redistribution** is not the same as **new output creation/delivery**. Explain upstream ingredient access without inventing an independent physical ingredient store in a builder. Explain how remote/unloaded production is natively possible under registered/resolvable conditions, without promising that every distant outpost always runs or catches up.

The technical reference must document the applicable CONT/reference/ONAM and item-keyword criteria, effective rather than only base capacity, incoming/outgoing eligibility, graph membership, reference/stack identities, native selection and mutation paths, saved source links and inventory framing. Include consequential exceptions and mechanisms:

- Ordinary dedicated capacities **75/150/300** by size are **base definition** values in weight units; Transfer Container **200**; ordinary cargo child containers **300** in the qualified templates. Do not generalize capacities or inventory completeness from unsupported extras or modified instances.
- Ordinary decorative chests' effective link prohibitions are real native eligibility gates, not merely absent UI controls. A hypothetical changed definition is a different case.
- Cargo incoming and outgoing compartments are **different child references**, with different local-link directions; their capability to act as local sources is not proof of reverse cross-outpost freight.
- Existing-stock redistribution can traverse/bypass intermediate buffers, split by destination and use current vector order without a guaranteed stable first-link priority. Item-by-item planning does not reserve aggregate multi-item capacity.
- Fresh production may choose one downstream store or own buffer fallback; an already-full check and whole-batch insertion can differ from the weight-limited redistribution path. Do not claim all insertions enforce the same nominal bound.
- Local-link movement is directed. Script refill can seek upstream **sources** while selected item movement still proceeds downstream; reciprocal edges are two directed paths, not spontaneous reversal.
- Graphically unloaded is distinct from unresolved/unregistered; skipped elapsed updates, failed handles, ineligible producers and effective current state have different consequences. Avoid universal retention/debt/catch-up guarantees.

Provide at least one bounded, cited positive example and one counterexample that challenges an intuitive but wrong capacity/direction/remote-production assumption.

## 5. Q2 — Cargo links, returned freight and inter-system fuel

**Primary research:** `docs/experiments/cargo-links/transport/report.md`, `cycle.md`, `timing.md`, `inventory.md`, `lifecycle.md`, `saves.md`, `transit.md`, original and follow-up reviews; `docs/experiments/cargo-links/fuel/report.md`, `native.md`, `stages.md`, `saves.md`, `time.md`, `review.md`. Use S1/S2 for local compartment behavior; use production/power references where these share scheduling/consumer machinery.

Explain reciprocal endpoint configuration versus a currently functioning route. Show the two-ended ordinary ship/hold cycle and where items really go: load from the active endpoint's outgoing child, transport in the shared ship hold, unload into the next endpoint's incoming child, then attempt the opposite leg. Include partial/empty journeys and failure to unload. **Undelivered stock can remain in the shared hold and return into the original endpoint's incoming bay**; explain the actual native/script mechanism, while explicitly declining to certify a particular historical incident from a static snapshot. Do not turn asymmetric endpoint compartments into symmetric instantaneous bidirectional flow.

Document the distinct time domains: cargo stage/script game-time deadlines, wait/sleep VM timer dispatch and rearming, travel/package completion, versus the engine elapsed-time producer scheduler. Qualify defaults and conversions (including ordinary 30/15/30-second script stage defaults) against the exact source and actual invocation gates. Advancing the calendar is not evidence that every missed voyage was replayed. Discuss distant/unloaded routes as conditional on bound/resolvable objects, package work and completion. Include link clearing/retargeting/recovery: the old hold's successful recovery path to home ship and remaining player inventory is **not** an automatic return to the old outgoing bay.

For inter-system fuel, identify the pad marker as a **logical recipe consumer** supplied by upstream inventories through the local graph. The qualified installed ordinary recipe withdraws **five He-3 per accepted fuel-production cycle**, with **108 engine scheduler seconds** base interval before modifiers. This is neither five units per departure nor five units per round trip, and does not imply an independent physical marker inventory. Separate native fuel readiness, charge/evaluation, cycle accumulation, saved state, departure gates and actual removal. Distinguish ordinary unfueled and inter-system configurations without inventing a global guaranteed fuel policy or closed-form voyage schedule.

The technical reference should map native/script ownership and methods, source/receiver and ship hold identities, stage gates, saved compartments and timers, conditional clocks, relevant failure/retry paths, precise citations and a conservation-qualified illustrative round trip. The worked example must be labelled as a model, **not a captured historical voyage**. Preserve the timing follow-up's narrower conclusions and original review history.

## 6. Q3 — Shared Outpost Storage

**Primary research:** `docs/experiments/shared-outpost-storage/report.md`, its native/provider/saves/verification and independent-review documents. Cross-check SD3 but never merge the two systems merely on the phrase “storage.”

Introduce the add-on fixture's definition, construction eligibility and Workshop membership separately from the **actual backing inventory on the player-side object**. Make plain that a visible shared fixture can expose resources via this backing inventory without possessing its own conventional saved item list. Explain the shared provider's sources and substitution, and the different consumers: bench/crafting/research versus construction, and how local Workshop, ship and player sources change the effective candidate vector. Fabricators and cargo use distinct graph/transport mechanisms; do not imply they automatically consume the shared store.

The reference must distinguish the backing reference/owner, registered source vector, counting copies, actual spend requests, forward source ordering, unstable Workshop-member ordering, virtual-removal planning, and absence of a proven globally atomic inventory transaction. Include the useful counterexample: a cargo outgoing compartment may hold items while failing an effective build-container gate, while an ordinary chest may pass that gate despite local-link prohibitions. **Exact saved backing quantities remain unparsed** under the historical evidence: preserve that limit and do not reconstruct totals from unrelated fixture saves. Separate positive membership/definition checks from currently loaded effective sources and spending results. Document add-on/build scope, not an invented general main-game mechanism.

## 7. Q4 — Locations “Stored Resources”

**Primary research:** `docs/experiments/stored-resources/report.md`, `provider.md`, `membership.md`, `aggregation.md`, `icons.md`, `saves.md`, `methods.md`, `review.md`. Reference `docs/experiments/shared-outpost-storage/` solely to explain overlap and divergence.

Explain how the Locations panel binds to a registered, resolvable Workshop/outpost row, traverses eligible member inventories with effective `OutpostBuildContainer` and container gates, substitutes/deduplicates recognized shared backing inventory, converts actual item instances to resource identities, aggregates **stack units** per resource, orders and labels the displayed list, and refreshes as an asynchronous snapshot rather than a live universal inventory ledger.

The guide and reference must explicitly reject misleading simplifications:

- Stored Resources is **not** a separately persisted universal outpost inventory and does **not** automatically include player pockets, all ship cargo or all remote chests.
- Distinguish item base and associated resource FormID; unit sums are not item-weight sums, per-second production, or proof of crafting availability.
- The row and displayed arrays reflect the collection/refresh epoch; screen comparisons at different times cannot establish inventory conservation or an immediate update subscription.
- The SD2 construction/crafting provider shares a membership predicate but adds sources and spending behavior; SD3's screen collector has a different output and scope.
- Historical saved inventory examples and screenshot visibility must retain their original sample/membership and epoch limits; unsupported extras are not presumed empty.

Include a concrete small aggregation walkthrough with sourced/testable item-to-resource mappings, not fabricated screenshot observations. Explain icons only to the degree established by the native/UI evidence and keep presentational concerns subordinate to identity and authority.

## 8. Evidence, diagrams and glossary

Before drafting decisive prose, assemble a **claim-to-evidence crosswalk** for the four Qs: statement, scope/build, evidence type (STATIC/SAVE/RUNTIME/derived), primary path and relevant section, independent review/status, counterexample or negative case, and current publication access tier. Crosslink tracked paths rather than using private `.local-work/` paths as the only public route. If an indispensable historical witness lacks a lawful enduring public route, state **PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING** and identify the dependency; do not package it in D5BB or pretend a hash makes the bytes accessible. Do not require comprehensive inventory of disposable local work.

Use editable Mermaid where it helps readers distinguish: local graph versus physical stores, cargo shipment/lifecycle and timing, shared backing/provider/craft spend, and Locations aggregation/refresh. A figure is **not** an additional scientific claim: label absent branches, frame/units, source evidence and qualitative versus measured quantities. Supplement diagrams with accessible prose/tables. Mermaid rendering should be checked if tooling exists; record an honest limitation if visual preview is unavailable. Do not fabricate illustrations or draw complete game networks from incomplete saved snapshots.

Update the glossary under its accepted **plain-language, concrete, noncircular** contract. Likely useful entries include output link, receiving versus outgoing cargo child, transfer container, source inventory, target inventory, producer output buffer, ship hold, fuel marker, cargo timer, shared backing inventory, provider source vector, virtual removal, item stack, effective capacity, resource aggregation and refresh epoch. Distinguish native type/structure/function, save record, script object, UI label or researcher abstraction; identify provenance and known ownership/lifetime. Avoid repeating existing definitions and avoid terminology that makes UI quantities physical inventories.

## 9. Verification, independent review and reporting

Perform **three reader journeys for each of the four subjects (12 total)** on the exact delivered pages:

1. **Understand:** follow the normal operation from the guide into technical reference, identify a practical consequence and one consequential limit.
2. **Reproduce:** execute a bounded verification from tracked public inputs or a clearly defined conditional regeneration contract; report the command, actual inputs/results and exactly what the result does **not** validate. Do not call a private raw input reproducible because its filename or checksum is known. Where genuinely no portable exact data exists, use a transparently bounded tracked calculation or declare the access limitation rather than synthesize false output.
3. **Challenge:** reach the source report, relevant review and a counterexample/negative case; distinguish historic uncertainty from accepted later qualification.

Run link, case-sensitive relative-path and heading-fragment checks on **all modified pages**. Validate Mermaid syntax and visually inspect rendered diagrams when feasible; record rendering limits. Check numerical claims from tracked sources; check units, counts, native address domains, save identities, stage durations and phrasing. Inspect full final prose for circular definitions, mismatched graph directions, false capacity/consumption authority and misleading static→retail extrapolation. Preserve links and navigation to all previously accepted guides.

Conduct an **independent** final scientific review and independent engineering/evidence and editorial review of the **corrected final snapshot**, not only a draft. The reviewer should challenge the hardest cross-system claims: storage versus output buffer; movement versus production; outgoing/incoming bay versus shared ship hold; accepted cycle versus voyage fuel; shared store versus SD3 display; saved versus effective inventory. Record actual findings, fixes, re-review, limitations and Q/AC disposition. A reviewer-reported ACCEPT is not a substitute for checked evidence, and a review limitation should not be silently called a PASS.

## 10. Acceptance criteria

| ID | Requirement |
| --- | --- |
| **AC01** | All four named guide/reference pairs exist, are coherent standalone reader documents, and use the accepted guide/reference distinction. |
| **AC02** | Q1 accurately distinguishes physical inventories, native capacity/filters, directional graph, existing-stock redistribution, production delivery and conditional remote updates, including exceptions. |
| **AC03** | Q2 faithfully explains endpoint/hold cycling, returned freight, game-time stages, skipped-time limits, recovery and fuel recipe/charge boundaries without claiming guaranteed journeys or per-departure He-3 consumption. |
| **AC04** | Q3 identifies the shared backing inventory, source-provider and spending routes; distinguishes fixture/eligibility/saved identity and documents the unparsed backing-quantity limit. |
| **AC05** | Q4 documents SD3's qualified membership, resource conversion, unit aggregation and refresh authority; explicitly separates it from Shared Outpost Storage and general physical stock. |
| **AC06** | Shared glossary, guide index and reference index are extended correctly with concrete noncircular terminology and working backward navigation. |
| **AC07** | Decisive claims have direct scope/evidence/review/counterexample crosswalks, with genuine public-access classifications and explicit pending indispensable witnesses. |
| **AC08** | Twelve reader journeys, numerical/command examples, links/fragments and diagram sources are checked on the final snapshot; rendering and private-input limits are candidly recorded. |
| **AC09** | Independent scientific, engineering/evidence and editorial review examines final corrected prose; Q1–Q4 and AC01–AC09 receive evidence-based COMPLETE/PASS or explicit REWORK/BLOCKED dispositions; patch and changed-file manifest reconstruct exactly. |

A temporary inability to render Mermaid visually does not automatically fail otherwise valid diagrams, but must remain visible as an unperformed public-presentation check. Do not waive broken links, misleading cross-domain assertions or material missing qualifications as mere cosmetic issues.

## 11. Scope exclusions, preservation and delivery

**In scope:** Documentation synthesis, bounded tracked text/data examples, glossary and navigation maintenance, claim crosswalk, independent review, small audit receipts and patches.

**Out of scope:** Any Starfield gameplay/native debugging, running Ghidra or game observers, rewriting save files, manipulating installed game assets, new research experiments, measurement of actual transfer throughput, generalized logistics simulators, cargo network optimizers, evidence-derivative extraction/packaging, GitHub Release asset creation, broad repository README rewrite, historical experiment/brief/audit relocation, publication status changes, commits/pushes, or approval of legal/privacy/publication clearance.

Preserve historical reports and negative cases at existing paths. Preserve D5AX's three-layer reader architecture and D5AW's publication-independence policy. **Leave implementation briefs and administrative audits loose** for the separately authorized coordinated archival operation near final release. `.local-work/` is disposable post-publication; do not impose a local-corps retention obligation. Keep B4-F1 release assets, D5AS/C19 access preparation, B6 clean-checkout verification and final release authorization separate. Publication remains **NOT READY / NOT CLEARED**.

At completion, report: changed files, Q1–Q4 and AC01–AC09 dispositions; primary claims and important limitations; reviewer findings and corrections; 12 journeys and tests; evidence-access dependencies; exact task-only and complete patch paths/hashes; uncommitted working-tree status; and a suggested commit message (for example `docs(research): add logistics and storage guides and references`). Do not declare success merely because a patch applies or review files exist.
