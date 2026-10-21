# Prior art, source reports and permission decisions

SOR-EXP-0063. Read-only public consultation, **2026-10-21 Australia/Sydney**.
This is a bounded relevance pass, not an absence proof or exhaustive literature
review. No external repository was forked/copied, package installed, implementation
executed or source adapted. Search results were leads; the first-party author
pages/README descriptions below supply the cited claims. Versions not available
from those pages are UNKNOWN rather than inferred from crawl times.

| Key / author / version/date | Exact source and evidence type | Relevance and separation from RG1 |
|---|---|---|
| RG1-PA01 / DownfallNemesis, credits ZeeOgre and ProbeTech / 1.0, 2025-05-09 | [Overlay ProcGen Masks](https://www.nexusmods.com/starfield/mods/13830), author tutorial and permission panel | Source reports black/white masks controlling allowed procedural content in custom overlays. It describes object generation/removal and worldspace-named DDS masks, not per-IRES vein boundaries or deterministic vein membership. No semantic equivalence to the native point path demonstrated. |
| RG1-PA02 / Mesmacat / posted 2025-01-02; page displays updated Apr 7 without a year | [CK outposts and POIs guide](https://steamcommunity.com/sharedfiles/filedetails/?id=3385012985), author documentation | Worldspace/landscape cutting, overlays and planet assignment. An overlay is not evidence of an inorganic vein mask. Used to distinguish CK terms, not as a generator specification. |
| RG1-PA03 / Jaheay / current README, revision UNKNOWN | [starfield-outpost-data](https://github.com/Jaheay/starfield-outpost-data), implementation project README/file inventory | Describes planet and biome resource combinations, scraping and outpost optimization. The inspected description supplies catalogue/eligibility data, not local contour generation. Code and datasets were not incorporated or executed. |
| RG1-PA04 / Aldruun / README version/date UNKNOWN | [Starfield-Planet-Resource-Checker](https://github.com/Aldruun/Starfield-Planet-Resource-Checker), author repository description | Planet combinations in a WPF tool; no local vein geometry contract in the inspected description. No binary downloaded/executed. |
| RG1-PA05 / deveris256 / README revision/date UNKNOWN | [SF_Planet_Experiments](https://github.com/deveris256/SF_Planet_Experiments), author experimental Blender-addon repository | A planetary experiment/biome-map lead; inspected landing page does not establish a vein spatial oracle. No addon/code/data was executed, copied or adapted. Its complete implementation has not been audited for all geometry capabilities. |
| RG1-PA06 / gooberpede / reproducer local HEAD `a8ff1c788bca415f571f06769ab3e712fa674f75`, research HEAD `a23e1c337bc369232d6ce463552a53617bb918e2` | [resource reproducer](https://github.com/gooberpede/starfield-resource-reproducer), [research](https://github.com/gooberpede/starfield-resource-research), local README and public landing pages | Maintainer-owned baseline reproduces planetary/per-biome membership; reproducer explicitly excludes resource-vein geometry. Its 1,444-body validation is not RG1 spatial validation. Existing project's MT method already records this lineage; RG1 adds conditional spatial generation. |
| RG1-PA07 / Constellation-VASCO / 2023-11-29, reported build 1.8.86.0 | [SFCP issue 703](https://github.com/Starfield-Community-Patch/Starfield-Community-Patch/issues/703), original incident report | Reports changed/disappearing deposits with working extractors. A lifecycle counterexample lead, not proof of a cache mechanism or a geometry dataset. Not newly reproduced; current RG1 build and acquisition differ. |

Queries included `Starfield resource vein procedural generation RSGD resource map
overlay Creation Kit`, `github Starfield inorganic resource veins map generation`,
`site.ck.uesp.net Starfield ResourceGenerationData` and `Starfield
ResourceGenerationData DNAM veins Github`. No decisive CK vein-generation
specification was recovered by this search; that does not prove none exists.
No Reddit/forum conjecture or scraper-derived map was adopted as native evidence.

## Rights and attribution are separate

PA01's permission panel restricts upload/modification/asset use, while its prose
also has a broad content-use statement. That ambiguity was **not resolved into
permission**; nothing was reused. PA02 has no established incorporation grant.
PA03 advertises MIT, but its data includes separate source ownership, and user
acceptance for any incorporation is absent. PA04/05 terms were not relied upon;
licence/rights scope remains unreviewed. PA07 is consultation/credit only, with
no issue reply/contact or copied substantial text. None needs a reuse approval
for the read-only relevance summaries actually performed.

PA06 maintainer-authored material has standing inspection/reuse authority
[SOR-P-0002](../../PERMISSIONS.md#sor-p-0002--standing-maintainer-owned-material-grant).
It does not clear embedded third-party data or native exports. No new sibling
implementation was copied. Immediate original method lineage is recorded in
[sources.csv](sources.csv): existing project CRC/MT, binary32 strip construction,
scalar polynomial study and review-export method. Bethesda installed executable
and ESM are lawful local analytical inputs; their bulk payloads stay local. Only
original explanatory prose, bounded numerical facts and authored source appear
in the review diff. No classification or redistribution approval is inferred.

The new causal/generation and exact geometric conclusions are project-original
STATIC/mathematical work. Public sources above contribute terminology,
alternative hypotheses, limits and incident leads; they do not validate RG1.
Credits are recorded here at use, in [SOURCES](../../SOURCES.md) and
[CREDITS](../../../CREDITS.md).


Continuation reuse: SOR-P-0002 also covers execution of the maintainer-authored
sibling domain/generation/PRNG modules for installed-field planetary selection and
the independent explicit-MT arithmetic check. No third-party module or catalogue
CSV is used. Exact current module hashes/revision and method receipts are in the
source ledger. Owned B1 map parser/orientation and exact patch methods are credited;
the new source-context/geometry methods remain original source-informed work.
