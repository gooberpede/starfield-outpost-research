# Codex Research Brief — Extractor/Resource Association and Completion-Protocol Trial

**Project:** `D:\Projects\starfield-outpost-research`  
**Status:** Implementation/research assignment; offline and read-only with respect to game state  
**Purpose:** First substantive trial of the newly committed Research Execution and Completion Protocol.  
**Authority:** Research existing approved saves and local reference/source data; implement offline analysis tooling and tests. No Starfield launch, debugger attachment, SFSE deployment, game configuration change, new controlled save, staging, commit or push without separate authorization.

## 1. Research question and successful outcome

Recover and test a deterministic method to identify **placed outpost extractor instances** in Starfield saves, associate each instance with the **resource it produces**, and report the evidence and coverage of that association. Use both the controlled save series and the mature saved networks already available in the repository/local research archive. This is not a general outpost-production simulation task.

The outcome may be positive or negative. A **scientifically completed negative finding** is acceptable if a clearly specified candidate identification/association rule is rigorously falsified. **Stopping after finding ambiguous records, a failing regression, or a promising unresolved alternative is not an acceptable result.** Continue investigating and testing authorized approaches within this same assignment. Do not confuse a scoped negative finding with proof that resource association is impossible by all methods.

## 2. Freeze a concrete completion contract before implementation

Inventory the accessible controlled and mature saves, existing parse/extractor libraries, ESM/record metadata, independent outpost observations, and known resource dictionaries. Preserve original saves and existing frozen inputs byte-for-byte. State the exact available corpus and evidence gaps; do not invent the presence of X-Tech or other objects. Identify known-positive and known-negative controls before choosing an association rule. At minimum, examine the controlled sequence containing extractor construction and extractor deletion and the mature Save52 outpost corpus. Use other relevant controlled saves when available and justified.

Before implementation, record in the task's durable completion contract:

1. The unit of observation: extractor instance/reference, base/form identity, containing outpost/workshop, produced resource, source save and confidence/evidence provenance.
2. Mandatory positive and negative corpus cases; exact expected observable differences where already independently known.
3. The intended independent checks (e.g. save diff, object base/reference relationship, ESM/industrial resource records, outpost/context relationships), and limits on using one inference as its own oracle.
4. Acceptance conditions for a deterministic offline tool and human-readable result inventory; expected handling of unknown/unresolved objects without fabrication.
5. An explicit negative-hypothesis standard and the reviewer gate. Do **not** alter acceptance thresholds after seeing results merely to convert failure into PASS. New material risks may be escalated with supporting evidence.

Do not set an arbitrary small limit on record scanning, saved sections, or research iterations. Enforce the established 40,000,000,000-byte available-space guard on both C: and D: for any new sizeable writing/capture operation.

## 3. Mandatory investigation

### A. Identify extractor instances

- Start from controlled-save differences for construction and deletion, respecting existing save decoder boundaries and established record associations; compare against independent observations rather than guessing solely from strings.
- Discriminate placed extractor references from build-menu definitions, inventory items, resource deposits, storage, machinery and deleted/historical objects.
- Resolve plugin-qualified forms and references using the established repository conventions; respect load-order/light-plugin and DLC distinctions. Avoid bare FormID assumptions when the full identity is available.
- Account explicitly for disabled, removed, or historical references using the project's existing rules. Do not silently discard a case simply because it is inconvenient.
- Extend the identified rule to the mature save population and record both successes and challenging counterexamples.

### B. Establish produced-resource association

- Investigate whether resource identity is carried directly on the placed reference, in its base/object definition, in production/activation components, keyword/linked forms or other documented relationships. Distinguish actual native/serialized evidence from heuristic class/name matching.
- Cross-check associations with independent source records, controlled changes, and known mature-network observations where available. Do not use manually maintained network labels as proof of resource production; labels may aid lookup only.
- Produce a deterministic extractor-to-resource inventory with per-case provenance; never silently classify an unknown object as a familiar extractor/resource.
- Clearly separate **resource produced**, **deposit/site eligibility**, **power requirement**, **production rate** and **connected output storage**. The latter four are outside the mandatory detailed reconstruction; record encountered leads for future tasks without allowing them to derail this one.

### C. X-Tech exception — bounded but explicit

X-Tech resource was introduced with Free Lanes; the special X-Tech extractor is a Terran Armada feature. Reference information indicates an X-Tech Power Core build requirement, and that dismantling does not return the core. The special extractor may not obey normal deposit placement rules. Verify these points from available authoritative game records or mark external documentation as such. Starting sources to check (not an engine oracle):

- Bethesda overview: https://bethesda.net/en-US/news/starfield-free-lanes-terran-armada
- INARA extractor: https://inara.cz/starfield/outpost-module/4714/
- INARA core: https://inara.cz/starfield/item/4719/

Inspect available DLC/ESM records and save corpus for the relevant resource and extractor definition, checking content availability and provenance. **Do not assume any current save contains a placed X-Tech extractor.** If no such instance is present, record its static/form association if demonstrated, report `NOT_OBSERVED_IN_SAVE_CORPUS` for runtime placement, and make the placement-instance validation a future coverage gap—**not** an excuse to leave ordinary extractor association unfinished. Do not request creation of a new live X-Tech outpost as part of this assignment. Do not force ordinary deposit/rarity-family rules onto X-Tech.

## 4. Deliverables and tests

Produce:

1. A durable research report showing method, observations, evidence references, counterexamples, supported claims, explicit coverage limits and next-domain leads.
2. A deterministic offline implementation (or carefully documented, defensible negative outcome if the proposed mapping mechanism is falsified and no authorized independent recovery route remains viable) integrated with the repository's established tooling rather than an unnecessary duplicate save parser.
3. Machine-readable inventory and comparison outputs suitable for regression tests, including provenance and explicit unknowns; keep proprietary saved data and bulk raw artifacts in ignored local work areas, not Git.
4. Reproducible positive and negative tests for controlled corpus and a mature-save validation inventory; regressions must cover creation/deletion and incorrect lookalike identification.
5. A frozen acceptance matrix with `PASS / FAIL / NOT_TESTED` and evidence pointers; failures are not averaged away.
6. A workflow-trial report explicitly evaluating whether the implementer/reviewer/rework loop complied with the new standing instructions, including any actual reviewer challenges and corrections.
7. Complete and task-only diffs under `.local-work/diffs/`, including newly created text files, plus Git status, exclusions, patch-check receipts and a concise review package.

The result need not reconstruct deposits, power consumption, extractor production rates, storage output or X-Tech build eligibility in full. Those are distinct later research domains. However, it must not conflate them with the narrower association claim.

## 5. Mandatory independent review **before final handoff**

Follow the committed Research Execution and Completion Protocol and its current agent capability check. Spawn a fresh, read-mostly independent reviewer when supported; otherwise use its documented real fallback, reporting what actually occurred. Give the reviewer the *original frozen contract*, changed code, raw/primary evidence or reproducible derivations, full failed-test history and both diffs—not merely an implementer summary.

Reviewer must:

- Attempt to falsify the extractor identification and produced-resource claims; check that controlled-save expectations are independently sourced.
- Verify the deleted-extractor control, mature-save coverage and no-false-positive/lookalike handling.
- Check X-Tech is neither omitted invisibly nor treated as proven placed when no such object is observed.
- Challenge unsupported universality and inadequate coverage without manufacturing a new acceptance threshold after completion.
- Distinguish a completed falsification of a specific association hypothesis from an unfinished investigation.
- Return **ACCEPT, REWORK or ESCALATE**, with concrete references.

A `REWORK` decision must return to the **same assignment** for additional diagnosis, correction and testing. Re-run reviewer evaluation after substantive rework. Do not hand off 5/6 tests, an unresolved ambiguous association or a request for an ordinary follow-up brief as a completed task. Preserve failing evidence. A genuine external-authority, safety or resource limitation may be escalated with the exact blocker and minimum required operator action; never claim it is a passing result.

## 6. Quality, safety and scope

- Scientific completeness, instrumentation/process health and save integrity are distinct statuses. Strong **scoped** findings are useful; do not demand impossible universal proof. Equally, a narrow scoped finding is not a full-population result.
- Do not stage/copy proprietary raw saves, dumps, game assets, third-party code, local system inventories or secrets into tracked files or deliverable ZIPs. Preserve hashes and durable local pointers as appropriate. Honor existing source/license/provenance policy for maintainer-owned and third-party work.
- Treat existing game/save data as read-only. No native code execution in the game, SFSE or debugger work. Do not modify source game binaries or frozen evidence to make tests pass.
- Avoid task sprawl. Extractor/resource association is the goal; X-Tech placement eligibility, greenhouse/animal production, power, crew, robots and cargo-link algorithms are future research, not current acceptance gates.
- No staging, commit or push. No live Starfield launch, save generation, deployment, system changes or expanded permissions without the maintainer's explicit authorization.

## 7. Final handoff rule

Return only once the original acceptance contract has been completed and independently reviewed, or a **genuine, evidenced authority/safety/resource blocker** prevents authorized continuation. A valid completed negative outcome must state precisely which hypothesis and scope were disproved, all attempted authorized alternatives and what remains unknown. The reviewer must concur before treating a feasibility abandonment as COMPLETE.

The final report should identify **COMPLETE — PASS**, **COMPLETE — NEGATIVE FINDING** (appropriately scoped) or **ESCALATE — AUTHORITY REQUIRED**; never label incomplete implementation as COMPLETE. If a blocker is raised, provide a self-contained resume path rather than an unrequested fresh research brief. This assignment is the substantive test of our new workflow—not an opportunity to produce another polished intermediate report.
