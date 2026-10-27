# Codex research brief — SOR RG2-D5J
## Terran Armada faction-outpost reconnaissance for independent resource validation

**Status:** Issued for offline investigation only. **No retail Starfield launch/attachment, quest progression, Creation Kit modification, plugin deployment, save modification, new native instrumentation, staging, commit, push, publication, or archival migration.**

**Repository:** `D:\Projects\starfield-outpost-research` (`main`). Follow `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/PROVENANCE.md`, and the completion-contract and independent-review templates. Existing stricter protections prevail. This is a bounded reconnaissance, not another infrastructure project.

### Motivation and question

Our standalone ordinary-resource generator reproduces **ten exact native region controls** at original Feynman V, Carinae III-a and Archimedes III, plus **three** source-bound native region matches at the second Feynman V under frozen mask 3. D5H/D5I classify **19 conditionally mask-invariant and six conditionally mask-variable** source projections; the six variable sources have viable alternative first-construction paths but unknown historical winning queries. A useful prospective validation must obtain independently controlled location and Workshop observations. Eyeballing a landing point on the planetary globe or hand-placing an outpost beacon is not sufficiently precise, and building an exact beacon-placement harness could require extensive terrain-site legality and Workshop initialization research.

**Research question:** Do the three reported Terran Armada faction construction quests provide pre-existing, accurately locatable, fully functional Workshops that can act as independent prospective resource-presence and/or native-vein-geometry controls **without** programmatically placing a new outpost? If not, what exactly prevents their use? Secondary: do installed records reveal an existing Bethesda-supported fixed/dynamic Workshop construction route worth investigating later?

### Unverified leads — discover, don't assume

Investigate the reported quest/faction/location leads **as claims to verify from installed definitions**, not authoritative identifiers:

| Reported quest | Faction | Reported location |
|---|---|---|
| Favors for Favors | Ryujin | Neméria IV-a |
| Give and Take | Freestar Collective | Alpha Ternion III |
| Quid Pro Quo | United Colonies | Strix I |

Names, planet names, quest stage relationships and even the number of relevant Workshops must be checked against the **actual installed Terran Armada content and effective load-order context**. If the local installation differs, document the discrepancy rather than fitting records to the lead. X-Tech extractor quest success does **not** establish ordinary mineral presence, since X-Tech extraction may use special rules. Do not treat marketing/guide text, screenshots, or an extractor's operation as proof of native ordinary-source geometry or Workshop admission.

### Research tracks and evidence boundaries

**Track A — Content/identity discovery.** Identify the installed DLC/plugin(s), versions and immutable hashes; identify relevant QUST, scene, alias, script, property, reference, location, cell/worldspace, planet/body, Workshop, beacon, ownership/faction and extractor records. Use existing xEdit/BA2/ESM readers and read-only Creation Kit/Ghidra facilities where sufficient. Do not export unbounded proprietary content or commit raw installed records. Record exact FormIDs with file/override provenance (be mindful of light-plugin addressing and form resolution), script/module identity, relevant conditions and stage-specific enabling. Distinguish reported quest labels from actual installed editor IDs.

**Track B — How the outposts exist.** For each site, trace whether it is (a) a preplaced Workshop/reference activated by a quest, (b) dynamically created/registered on quest progress, (c) a hybrid, or (d) presently unresolved. Find the decisive placement and initialization edges, rather than infer dynamic creation merely because the beacon is absent before a quest stage. Inspect reference transforms, enable parents, persistent aliases, scripting and native calls where justified. If a Workshop is dynamically created, identify the actual invocation and required prerequisites without implementing or running it.

**Track C — Geospatial identity and repeatability.** Determine whether the site possesses a qualified stable landing target, planetary source/chart/frame, Workshop/beacon world coordinates and resource-evaluation radius/orientation. Show the full native/installed transform chain needed to compare the Workshop footprint to our offline source geometry. If coordinates cannot be recovered uniquely, say which transformation, initialization operand or runtime value is missing. Distinguish authored placement from runtime object position and distinguish a POI anchor from the actual Workshop center. Do not use a manually eyeballed or approximate site position as an exact test input.

**Track D — Ordinary resource-evaluation equivalence.** Establish whether the faction Workshop uses the same native Workshop area callback and accepted-resource/operation-vector path as an ordinary player outpost, or identify divergences: ownership, quest flags, placement bypasses, source generation, unusual extractors and special resource admission. Inspect relevant X-Tech extractor conditions separately and **never** treat a successful X-Tech installation as ordinary vein evidence. Identify what ground truth can be obtained without creating a new outpost: native source populations; a Workshop-bound ordinary-resource accept/transfer; extractor-catalogue positives; and the scope/limits of each. A preplaced quest Workshop need not imply all native fields are available offline.

**Track E — Feasibility and next-step design.** Give each candidate a decision: `READY_FOR_OFFLINE_PREDICTION_FREEZE`, `PROMISING_NEEDS_EXACT_OPERAND`, `SPECIALIZED_NOT_COMPARABLE`, or `UNRESOLVED`, with explicit conditions. Distinguish source-geometry validation (can occur without a Workshop) from complete footprint/admission validation (requires functional Workshop evidence). Recommend the **least intrusive** prospective test if one or more candidates qualifies, with offline prediction freeze *before* consumer/geometry ground truth is examined. If all fail, state whether a fixed ordinary POI or an already existing conventional outpost is the more economical alternative. Design only; **no live run authorization or full debugger engineering**.

### Method and discipline

1. Start with a concise plan, actual repo/head/index, current effective preservation baseline, disk guards (at least 40,000,000,000 bytes available on **both** C: and D: where applicable), available installed Terran Armada assets, tools and source hashes. If the DLC is absent or inaccessible, do not invent record contents: perform other bounded, independent offline checks and give the exact missing dependency.
2. Use the **active archive-backed** historical evidence model; do not reinstate the obsolete 93,334 loose-file hash routine. Verify only relevant scientific inputs and critical protected sources. Preserve existing accepted archive state and all saves. Avoid new giant per-receipt inventories, bulk exports and repeated full analyses merely to collect more documentation.
3. Build a **compact comparative table**, one row per real candidate Workshop (not forced to exactly three), with installed identities, placement mechanism, fixed/variable state, exact-coordinate status, standard Workshop admission evidence, ordinary-resource/geometry oracle, missing operands, scientific value and explicit qualifiers.
4. Prefer targeted static reads and already-owned tools to a new framework; document true negative findings (for example a scripted preplaced alias or X-Tech-only resource route). Trace alternate explanations as far as necessary to decide each candidate. Do not weaken conclusions when exact proof is unavailable, but do not expand into all of terrain procgen or Workshop placement legality.
5. Keep `PROVEN/STATIC`, `INSTALLED`, `DERIVED`, `SOURCE-REPORTED`, `CONDITIONAL`, `UNKNOWN` separate. An installed route does not establish runtime quest-state behavior. A fixed quest location does not prove ordinary resources are fixed across different source-generation histories.
6. Freeze legacy geometry generator, D2–D5I outputs and Save52 classifications. Ten original native geometry controls and three D5B conditional matches are preserved, not implied to be rerun. No test-site predictions may be fitted using known Workshop resources.

### Frozen completion contract / AC1–AC8

**Type:** Bounded offline research/reconnaissance, with a supported positive or bounded negative result. Complete genuinely in-scope alternative traces; an unproductive initial search alone is not an acceptable negative conclusion. The maintainer alone can amend criteria or authorize later live/destructive actions.

| AC | Mandatory acceptance requirement |
|---|---|
| **AC1 — Authority and preservation** | Verify baseline/installed identities and applicable protected inputs; offline/read-only game research only. No live target, save/content mutation, archival changes, staging or commit/push. Existing free-space safeguards upheld. |
| **AC2 — Exhaustive lead accounting** | Investigate all three reported quest/faction/location leads; record actual installed identities, discrepancies and negative/absent evidence. Discover multiple Workshops per lead if indicated. |
| **AC3 — Placement/initialization classification** | For every located candidate, substantiate preplaced, dynamically created, hybrid or unresolved status with exact installed/native/script evidence, not guesswork. |
| **AC4 — Precision and repeatability** | Evaluate each site's stable landing/POI authority and exact Workshop/planetary-frame coordinate derivation; explicitly label missing operands and no-eyeballing constraint. |
| **AC5 — Valid resource oracle** | Determine whether an ordinary Workshop resource evaluation and/or native source-geometry oracle exists; distinguish X-Tech-special mechanisms, catalogue positives, region geometry and complete accepted-resource inventory. |
| **AC6 — Actionable comparison** | Publish a compact candidate matrix and a reasoned best/no suitable control recommendation, with a bounded prospective freeze-and-observe design or concrete obstacle. No new general-purpose placement harness. |
| **AC7 — Durable, proportionate evidence** | Concise report, precise primary-source ledger, method/reproduction notes, scoped tests/sanity checks and limitations. Changed prose receives automatic screening and **manual** editorial finalization. No unnecessary giant receipts. |
| **AC8 — Independent acceptance and exact delivery** | Independent scientific/engineering/editorial reviewer challenges each AC, the installed identity joins, fixture consistency and unsupported positive claims; fix REWORK within scope. Preserve exact final reviewed snapshot, complete and task-only diffs, changed-file inventory, exclusions, exact SHA-256, status and final closure delta if needed. |

**Negative completion:** If none of the three leads supplies an independently locatable ordinary-Workshop validation control, deliver the evidence-backed reasons for each, the smallest potential remedy, and the next lowest-cost alternative; this is a legitimate completed negative result, subject to the same ACs. Do not force a positive result or require a live experiment to close this offline brief.

### Expected tracked deliverables

Choose a concise new folder such as `docs/experiments/terran-armada-outpost-recon/` with `report.md`, `candidates.csv` (or equivalent table), `sources.csv`, `methods.md`, `review.md`, optionally short native/script findings and proposed **unapproved** experiment design. Update relevant navigation; store the supplied brief unchanged in `docs/implementation-briefs/` and only add task-scoped helper code if necessary. Protected installed content, raw scripts/BA2 extracts, corpus, saves and large receipts remain local-only. Cite exact source identities and source line/instruction/record fields for material assertions.

### Delivery and decisions

Report the eight criteria PASS/FAIL/NOT TESTED with evidence, scientific conclusion and qualifications, independent verdict, remaining unknowns, actual execution and preservation outcome. Include original brief and all authored untracked text in **complete** diff; exclude pre-existing supplied brief from **task-only** diff if appropriate; forward/reverse reconstruct both against real baseline. Do not stage, commit, push, open a PR or grant publication status. B6 remains on hold.

**Most important boundary:** The goal is to find a reliable Bethesda-authored ground-truth location that avoids precise manual landing and beacon-placement problems. It is **not** to solve all terrain site legality, rebuild Workshop creation, or assume that a faction's X-Tech extractor proves ordinary resource availability.
