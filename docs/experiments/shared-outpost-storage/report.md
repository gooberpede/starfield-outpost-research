# SD2: Shared Outpost Storage and ingredient access

2026-10-19, Australia/Sydney. SOR-EXP-0056 / SOR-EV-0064.
[Frozen plan](plan.md), [original brief](../../implementation-briefs/CODEX_BRIEF_SOR_SD2_shared_storage_crafting_access.md),
[prerequisites](prerequisites.md), [shared inventory](shared-inventory.md),
[source–consumer matrix](consumers.md), [saves](saves.md), [methods](methods.md),
[independent review/package](review.md). Authored interpretation REVIEW-REQUIRED;
raw installed/save/native material LOCAL-ONLY. No integration/publication follows.

**Best-supported answer:** recognized Shared Outpost Storage fixtures expose
**one player-held backing inventory**. Native menus and ingredient providers
substitute that reference, deduplicate it and mutate it through ordinary inventory
operations. There is no need to synchronize separate per-outpost item stacks.
Crafting/research still require the appropriate source context; the existence
of a remote fixture alone is not an ingredient-provider entry at every bench.

| Question | Answer / strongest basis | Tested coverage and meaningful limit | Most useful next step |
|---|---|---|---|
| Construction requirements | Two rank-4 perk equalities, a location/parent keyword exclusion and selected-outpost quota 1; STRONG STATIC | Pinned installed add-on recipe/controls and native menu/admission paths; exact live wording and successful build unmeasured | Independent review of definition-to-provider chain |
| Identity and membership | Keyword capability plus ordinary WorkshopItem membership; STRONG STATIC + SAVE | 1,499 inline-base records across 124 supported historical saves; three fresh sets of beacon-owner joins; default/unsupported cases bounded | Retain actual membership separately from present eligibility |
| Authoritative contents | One backing reference at player+1008; special direct access and ingredient substitution; STRONG STATIC | Constructor, menu, count/spend and separate player writer/loader paths; physical fixture records lack their own inventory-change branch | Field-anchored decode of the backing player's saved item segment |
| Craft/research | Real shared provider builds bench/link/selected-ship/local-Workshop/player vector and a counting copy; STRONG STATIC | Actual menu callbacks and Research AddMaterial path; source and recipe predicates, no measured craft | Controlled split-source craft only if realized priority is needed |
| Construction versus other consumers | Separate construction vector shares local eligibility/substitution; fabricators/freight use their own graph/reference mechanisms; STRONG STATIC | Actual spending calls, SD1/S1/S2/E3/C2/DA1 reuse with original bounds; repair has no ingredient spend in mapped route | No SD3 screen inference |
| Depletion priority | Forward source order and bounded sequential requests; STATIC | Actual min/remaining and virtual-removal loops; Workshop-member order unstable/unqualified, no atomic global transaction or observed conservation | Record before/after actual source inventories in a future controlled test |
| Saved/load correspondence | Positive fixtures/owners and decisive native backing serialization; STRONG for these scoped joins | 255 original hashes verified; 147 supported, 108 unsupported, 23 missing. **Exact saved backing quantities remain unparsed**; actual settled load unknown | Continue field-specific offline PlayerCharacter decoding before claiming saved totals |

Installed retail EXE identity is freshly equal to 1.16.244.0 / SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Main ESM SHA-256 is
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Add-on/reader/source receipts and all exact native locators are in
[sources.csv](sources.csv) / [functions.csv](functions.csv). This is installed
definition analysis, not a complete winning-load-order or live module baseline.

The most useful negative contrasts are causal: a cargo outgoing compartment can
hold stock and participate in freight/local links yet fail the ingredient
provider's effective build-container AV gate; an ordinary constructed chest can
pass that gate while both its local-link directions are prohibited. A shared
fixture with no physical inventory-change branch can still expose a populated
backing inventory. Visibility, source eligibility and actual mutation therefore
need independent descriptions; unsupported matrix cells stay qualified.

Confidence, coverage and assignment completion are separate. The frozen
eight-criterion matrix and actual reviewer disposition in review.md control
acceptance. No new RUNTIME observation, gameplay success, current totals,
cross-version layout guarantee, safe mod integration point or SD3 Stored
Resources result is claimed. No game, save/configuration/database modification,
staging, commit, push, account operation or disclosure occurred.
