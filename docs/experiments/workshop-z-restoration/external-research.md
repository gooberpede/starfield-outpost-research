# Independent public research: Workshop Z restoration

2026-10-13, Australia/Sydney. Specialist contribution under the
[authorized brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_native_workshop_Z_restoration_external_research.md`).
Authored interpretation REVIEW-REQUIRED. Consultation only: no outside code,
tests, diagrams, dependencies or bulk source text incorporated; no tools installed
or executed from consulted projects, and no external contact or uploads.

| Element | Result |
|---|---|
| Question | Does public primary research provide a Starfield-specific saved-reference to loaded-reference Z contract or independently falsify competing explanations? |
| Answer | Public sources corroborate the distinction between raw reference position and loaded/parent state, but supply no validated restoration formula for these two Workshops. They expose concrete metadata disagreements and an explicitly uncertain terrain scale, preventing attractive but unjustified shortcuts. |
| Confidence | SOURCE-REPORTED for public declarations; project-derived falsifications below inherit the cited existing report's scope. No new native validation. |
| Coverage | SFSE reference declarations, archived and successor CommonLibSF reference/world/cell declarations and wrappers, xEdit Starfield placed-reference definitions, fo76utils Starfield BTD decoding, and focused public restoration/height searches. No claim of exhaustive internet coverage. |
| Evidence | [Consultation ledger](external-sources.csv), exact file/symbol/line anchors below, [existing Z/frame report](../ship-relocation-050/z-frame-followup.md), [prior save/frame trace](../static-exhaustion/call-and-dataflow.md). |
| Limits | Public declarations are not validation on retail 1.16.244.0; moving branch tips are explicitly unpinned. Selected edge, flag, height and update-history operands remain absent from the existing capture. |
| Next step | Use the pinned native writer/selector investigation to evaluate the branches below. A future simultaneous reference/frame/edge observation is design-only under this brief. |

## Lead matrix: external claims versus local evidence

All consultations occurred on 2026-10-13. Branch and line references identify the
read surfaces, not immutable revisions. Attempts to obtain commit metadata through
GitHub's API were unavailable to the browser tool; a read-only shell request was
socket-denied. No permission escalation, clone, mirror or retry workaround was
used. Consequently unobserved commit hashes remain UNKNOWN.

| Lead | Primary author/project and supporting surface | Actual public finding | Local evaluation and effect |
|---|---|---|---|
| EXT-Z-01 | Starfield-Reverse-Engineering/CommonLibSF, archived 2025-09-16; [TESObjectREFR.h](https://github.com/Starfield-Reverse-Engineering/CommonLibSF/blob/main/include/RE/T/TESObjectREFR.h), `OBJ_REFR`, accessors and final member block | Declares `data` at +80, position inside it at +0c, parentCell +b0, generic flags +d3; position accessors return the location field. No bit 02 meaning is supplied. | Agrees with project +8c/+90/+94 position observations. No height normalization occurs in the accessor. This is layout corroboration, not an independent proof of the native writer or sampled branch. |
| EXT-Z-02 | libxse/CommonLibSF successor; [TESObjectREFR.h](https://raw.githubusercontent.com/libxse/commonlibsf/main/include/RE/T/TESObjectREFR.h), lines 109–130,150–153,318,367–395; [implementation](https://raw.githubusercontent.com/libxse/commonlibsf/main/src/RE/T/TESObjectREFR.cpp), lines 53–58; [IDs](https://raw.githubusercontent.com/libxse/commonlibsf/main/include/RE/IDs.h), lines 2423–2432 | Retains the generic +d3 byte; names editor-location variants and SetParentCell slot 10C. GetParentWorldSpace calls a relocated native operation, with public ID63417. | Useful semantic search handles. Neither ID nor slot is a verified 1.16.244.0 address. Do not replace the pinned fallback getter with a direct parentCell read or equate editor, current and saved positions. No exact Z formula added. |
| EXT-Z-03 | Ian Patterson/SFSE contributors; [GameReferences.h](https://raw.githubusercontent.com/ianpatt/sfse/master/sfse/GameReferences.h), lines 223–249 | Member comments disagree with static assertions: parentCell comment +a8 versus assertion +b0; data +78 versus assertion +80. A function at RVA 02116840 is labelled IsInSpaceship. | Concrete metadata counterexample. The project independently inspected static VA 142116840, preferred base 140000000, as the cell/fallback path. Source aliases/comments cannot override instructions. The discrepancy does not identify an observer defect or a restoration cause. |
| EXT-Z-04 | TES5Edit/xEdit contributors; [wbDefinitionsSF1.pas](https://raw.githubusercontent.com/TES5Edit/TES5Edit/dev-4.1.6/Core/wbDefinitionsSF1.pas), lines 8216–8321 and 8723 | Defines placed REFR plugin records, base-dependent record flags and DATA position/rotation. Some flags describe ground/settling behavior. | Plugin headers are a different domain from saved frame byte and runtime +d3. No mapping in this inspected definition connects those flags to +d3 bit 02 or supplies a save-loader Z rule. Adds a necessary domain exclusion. |
| EXT-Z-05 | libxse/CommonLibSF; [TESWorldSpace.h](https://raw.githubusercontent.com/libxse/commonlibsf/main/include/RE/T/TESWorldSpace.h), lines 105–135; [TESObjectCELL.h](https://raw.githubusercontent.com/libxse/commonlibsf/main/include/RE/T/TESObjectCELL.h), lines 144–145 | Names default land/water heights, leaves world+310/+388 unknown, and annotates cellWorldspace at +118. | These declarations do not recover selected edge+30. The project uses its independently established cell+110 relation; incompatible annotations are unvalidated leads, not replacements. A default world height is not established as the per-reference restoration height. |
| EXT-Z-06 | fo76utils contributors; [btdfile.cpp](https://github.com/fo76utils/fo76utils/blob/main/src/btdfile.cpp), BTDFile constructor; [20230903 release](https://github.com/fo76utils/fo76utils/releases/tag/fo76utils-20230903), displayed short revision 200ea19 | Detects Starfield BTD through zero cell extents; scales min/max heights by 8 while explicitly marking Z scale as potentially incorrect. The release states Starfield terrain-file support. | Concrete reason to reject treating a public decoder's output as native ground truth. A BTD asset sample needs the actual selected asset, orientation, scale, interpolation and runtime edge-height join. No decoder execution or adoption. |

## Competing hypotheses and falsification status

These are specialist challenges to the existing project evidence, not newly
discovered external semantics. Numeric values and native addresses below come
from the two linked project reports, not from public declarations.

| Hypothesis | Test or counterexample | Disposition |
|---|---|---|
| One common additive Z shift explains both Workshops | Existing exact differences have opposite signs: SOR-002 requires +14.709359169006348; SOR-003 requires -22.37442398071289. | DISPROVED for the two captured geometries. Per-site transforms survive. |
| The third observer translation word is Z | Native construction initializes eight bytes only; the copied third word matches adjacent candidate-pointer low bits. | DISPROVED for these captures. No restoration inference can revive it. |
| Workshop compensation causes the discrepancy | In all 40 observations reference position equals center output and captured +60 vector is zero. | DISPROVED in these observations. Save26 moved-beacon compensation/invariance remains a separate earlier control. |
| Correct source world/packed XY key proves full XYZ equivalence | Prior trace includes independent 3D selected-edge/height conditions; query source identity is not reference parent identity. | UNSUPPORTED implication, contradicted as a sufficient inference by the established separate dataflow. |
| +d3 bit 02 means Havok settling because public flags mention ground | No inspected source connects plugin record flags to that runtime byte. | UNSUPPORTED domain substitution. Requires the pinned bit-level writers/readers. |
| Native Z is simply global planetary elevation or ground clearance | Neither public location accessors nor project grid code defines that semantic frame. | UNSUPPORTED. Negative native Z alone is not a contradiction or a datum. |
| A universal inherited Fallout/Skyrim or BTD 8× height rule resolves Z | Public terrain implementation itself marks the scale uncertain; no selected runtime sample/asset join is supplied. | UNSUPPORTED, not numerically disproved for every possible height source. |
| A model fitted to the two required differences validates restoration | Such constants are calculated from outputs, without an independently observed producer. | INVALID validation method; do not implement as causal model. |

## Native symbols and relationships worth checking

The public names are search leads; the following addresses are project static
VAs for pinned retail 1.16.244.0 at preferred image base 140000000. No current public
Address Library ID is transferred into that address domain.

1. Verify editor-location accessors and SetParentCell slot 10C only if they reach
   the actual reference position writer. The authoritative question is which
   writes affect +94 before the observed Workshop call, including post-load ones.
2. Follow the established writer chain: 141835450 saved frame/XYZ,
   141835c20/141835610 read, 141833b20 created-reference restoration,
   140ad3ed0 translation, 1405a0520 construction, and ordinary conversion
   140b734c0→140b73310. Establish bit 02 state changes and arithmetic order;
   declarations cannot select a live branch.
3. Distinguish world default land/water values from the actual
   140ada3a0 selected record+30. Trace 140acf480's producer and its call-site
   arguments, component ownership and activation epoch before broad asset work.
4. Keep reference own-parent fallback 142116840 distinct from the enclosing
   query-world key. Its actual returned cell/world must be joined to the same
   reference invocation; do not borrow marker cell views.
5. If an asset-dependent height path survives, require selected BTD identity,
   transformed XY, runtime scale/origin, sample indices/interpolation and output
   join before fixed POI terrain comparisons. Static terrain-image similarity
   cannot establish the reference restoration mechanism.

## Contribution and provenance outcome

The external pass changed the reconstruction's safeguards and lead ranking:
generic accessors do not perform a hidden Z conversion; +d3 has no public bit
name in inspected declarations; contradictory offset comments demonstrate why
layout names must be independently checked; plugin flag domains and uncertain
BTD scaling cannot supply missing runtime operands. It supplied concrete
editor/parent writer leads without substituting them for native validation.
It did not discover a numeric reconciliation, prove the selected live path, or
resolve the missing event operands. No specialist effectiveness rerun was done.

Credit additions required centrally: Ian Patterson/SFSE contributors;
Starfield-Reverse-Engineering and libxse/CommonLibSF contributors;
TES5Edit/xEdit contributors; fo76utils contributors. Existing source records
SOR-S-0103/0108/0116/0118 and related SFSE provenance may be extended where
appropriate; the primary agent owns stable-ID allocation for new consultations.
Research consultation grants no implementation reuse permission. The authored
summaries here are short paraphrases of findings; no outside source file is
vendored or redistributed. Full code reuse would retain the repository's separate
rights-holder and exact-use user-authorization gates.
