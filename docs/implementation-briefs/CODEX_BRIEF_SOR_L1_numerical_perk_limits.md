# Codex research brief — L1: Numerical and perk-dependent outpost limits

**Project:** `starfield-outpost-research`  
**Task type:** Bounded offline native/definition/script/save research and documentation, with independent review  
**Research boundary:** L1 numerical and environmental admission only. L2 overall Build Limit meter and L3 spatial placement/territory/collision are separate future investigations.  
**Authority:** Read-only analysis of existing protected sources and saves; author research documents and tightly scoped verification aids. No Starfield launch, instrumentation, save mutation, mod implementation, installation change, staging, commit or push.

## 1. Objective

Explain **how Starfield calculates and enforces numerical construction and outpost-eligibility limits**, not merely what their advertised numbers are. Resolve ordinary installed-main-game behaviour and identify the definitions, actor values, globals, scripts, native callers, checks and failure paths responsible. Distinguish limits on *constructing* something from persistence of already-constructed objects and from a user-interface-only restriction.

L1 encompasses:

1. **Outpost count:** baseline and skill-dependent maximum, global versus other scope, counts of active/deleted/disabled/abandoned outposts, and exact placement/admission gate.
2. **Cargo-link pads:** ordinary and inter-system pads, category/global limits, Outpost Management contributions, precise counting and native/script enforcement (including apparent six-pad maximum).
3. **Turrets:** construction-count limits by turret type/shared categories, relevant perks, and enforcement. Their firing, power, target selection and damage belong to the later turret phase.
4. **Other numerical category limits:** systematic bounded census of construction recipes/categories to locate further ordinary count-restricted objects, including generators, storage, harvesters and relevant special facilities; distinguish a genuinely unlimited ordinary category from one whose check was not identified. **Reuse**, don't repeat, accepted crew-station and robot limit findings.
5. **Planetary Habitation and environment eligibility:** the perk's rank-dependent permission to establish an outpost under gravity, pressure, temperature, atmosphere or other environmental conditions; exact planetary data and conditions consulted, the decision path, and any additional non-spatial prohibition independent of L3 geography.

For each limit, ask what happens if a saved or scripted state exceeds the ordinary permitted count, and whether dropping/altering a perk affects existing structures or only new admissions. Don't assume the game periodically revalidates existing objects.

## 2. Required context and evidence

Read `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, the compact completion template and the relevant earlier reports/registers. Reuse CR1 crew capacity and R1 robot limits without rederiving them. Use C1 cargo-pad/marker and workshop-membership/native construction-root research, planetary/body/PNDT research and the resource-placement findings as appropriate. Inspect the installed ESM, compiled PEX (not just PSC), pinned executable/native analysis, and qualified historical save corpus. Verify actual build/hash/address identity before using locators.

**Do not confuse PNDT keywords used for solar/wind rating with Planetary Habitation's outpost-placement predicates.** Investigate the latter explicitly; if overlap exists, establish it rather than presuppose it.

Select positive and negative saved examples based on their relevance (high/low pad counts, differing outpost counts, outpost environments, actual turret constructions), drawing from the broader indexed corpus. A save's objects/perks can corroborate a runtime-derived limit; an explicit serialized `limit` field is **not** a mandatory expectation. Saved construction roots, references and base-definition counts must be distinguished, especially for PackIns.

## 3. Native enforcement investigation

For each relevant category provide a traceable **definition → modifier → effective limit → current count → admission decision → failure/UI response → update on construction/deletion** chain, with actual record/form IDs, native function RVAs or verified script/bytecode entry points as appropriate.

- Identify *who invokes* the relevant checks on ordinary beacon, pad and turret placement. Separate menu filtering/disabled actions from validation during the actual operation and any script bypasses; state what each trace proves.
- Identify whether limits are per player, outpost/Workshop, pad category, system, planet or another owner, and what native state or saved reference defines that scope.
- Resolve shared-category versus separate-category counting, and how complex PackIns/foundations count relative to one constructed object.
- Identify selected perk ranks, quest stages, globals, actor values, defaults and overrides, including actual installed VMAD property values instead of assuming bundled source defaults.
- Establish refresh/recalculation and decrement/cleanup rules for deletion, disablement, destruction, replacement, perk changes and load, where relevant to numerical admission.
- Explain the actual error/failure response and whether a limit can be reached before visible UI feedback.
- Provide worked examples with native-supported values (e.g., baseline versus advanced skill; mixed regular/inter-system pads; same-category turrets). Mark prediction versus observed sample.

Research may follow narrow dependencies into generic placement code to identify the numerical/environmental **gate**, but must stop before explaining L2 budget accounting or L3 POI zones, clipping, terrain, collision, procedural clutter or beacon-territory geometry. When a failure is attributable to those separate gates, document the dispatch boundary and defer its internals.

## 4. Environment eligibility versus spatial placement

Explicitly distinguish **planet/body admission** (Planetary Habitation, planetary environmental data, hazardous-environment rank conditions) from **local site admission** (POI/settlement exclusion zones, 150-unit radius, boundary clipping, actor/static collisions, flora/rocks, terrain and suppressed scenery).

Map the first end-to-end through the actual beacon placement or location-eligibility consumer. Preserve named L3 questions as future scope rather than claiming their resolution: restricted POIs and cities, intersecting clipped build circles, dynamic actor obstruction, harvestables, pack-in environmental objects, and displaced rocks/trees returning after travel or reload. Likewise **L2** owns the thin overall Build Limit meter, the Fallout 4 triangle/draw-call hypothesis, and any separate complexity budget. Do not import Fallout 4 limits as Starfield facts.

## 5. Required output and reporting standard

Begin with a short plain-language answer giving the base limits, actual skill/perk effects, where enforced, and any material remaining unknown. Follow with a **limits matrix** covering each item above:

`category | scope | base value | perk/definition changes | counted entity | native/script enforcement | UI feedback | persistence inputs | confidence/coverage`.

Provide a compact function/source register, independent real-save corroboration where a suitable case exists, and a worked native explanation for outpost count, cargo pads, turrets and environmental admissibility. For other numerical categories, perform a bounded structured census with positive evidence and defensible absence statements; don't endlessly pursue hypothetical limit types. List specific untouched L2/L3 dependencies, potential corpus gaps and possible future discriminating experiments only when consequential. Existing documented crew/robot numbers should be linked, not rediscovered.

Use **reasonable engineering confidence**. Identified native causal mechanisms plus appropriately qualified evidence suffice for an accepted scoped conclusion. Failure to find an exotic alternative is not a reason to withhold a supported explanation. Conversely, naming a global or perk without tracing its actual check is insufficient. Missing save fields are not failures if the game calculates limits at runtime. Separate task completion, scientific confidence, save/runtime observation, publication and integration permissions.

Update the appropriate `docs/experiments/` research package, `docs/RESEARCH_STATE.md`, `docs/DECISIONS.md`/`docs/BACKLOG.md` and subsystem indexes as justified; preserve historical conclusions and identify any corrections. Record the agreed three-part Limits roadmap (L1 numeric/environmental; L2 build-budget; L3 spatial placement/procgen anomalies) durably. No general-purpose limit calculator, UI mod, save importer or live observer is requested.

## 6. Frozen compact completion contract

- **Task type / deliverable:** Offline native/definition/script/save research; causal numerical/perk/environment eligibility reference, evidence and independent review.
- **Bounds / protected inputs:** Existing installed game/native database and saves are read-only. Preserve EXE/ESM/PEX, source assets, saves, databases, working baseline and Git index/ref; observe C:/D: 40,000,000,000-byte free-space guards and existing identity/integrity practices. No game launch, saves created/edited, live debugging, instrumentation, build/deployment, network incorporation, staging, commit or push.
- **Mandatory acceptance:** (1) Answer-first limits matrix including exact values and authority or explicit evidenced unresolved cases; (2) traced outpost-count admission/skill mechanism; (3) traced regular/inter-system cargo-pad count and modifiers; (4) traced turret construction-count categories/modifiers; (5) bounded census of other numerical limits, with crew/robot reuse; (6) Planetary Habitation environment eligibility chain and explicit separation from L3; (7) save/runtime interpretation, representative corroboration, worked cases, source/function evidence and durable L1/L2/L3 boundaries; (8) executed verification, preserved failures and protected checks, independent reviewer **ACCEPT**, and complete review package.
- **Optional:** additional historical examples or prospective live test proposal if needed for an identified decisive gap, without executing it.
- **Negative result:** An adequately examined native/script path and bounded definition corpus may support a scoped negative. An absence of a particular save field or one uninformative save is not proof of absent gameplay state.
- **Continuation:** Correct diagnostics, rerun checks and complete all in-scope mandatory research without requesting a new brief for routine failed attempts. Mandatory criteria stay frozen unless maintainer-approved amendment is documented.
- **Escalation:** Stop the blocked operation on actual permission, integrity, resource or indispensable-corpus failure; retain precise attempted routes and a narrow proposed resolution. No self-authorized live experiment or scope expansion. No arbitrary hard elapsed-time, volume or operator-delay limits.
- **Review/disposition:** Follow `WORKFLOW.md` and the independent reviewer procedure. Report criterion-by-criterion PASS/FAIL/NOT TESTED and distinct scientific and engineering outcomes. Supply descriptive task-only and full uncommitted Git-style text diffs, including untracked authored text and the supplied brief, status/changed-file/exclusions manifest, exact forward/reverse reconstruction, UTF-8/LF/encoding/link/whitespace checks, source pins/checksums, and locally retained independent verdict. Raw copyrighted native/save/binary material remains LOCAL-ONLY; authored conclusions REVIEW-REQUIRED. Nothing is committed without maintainer review.

Suggested subject: `docs(limits): map numerical construction and environmental eligibility`
