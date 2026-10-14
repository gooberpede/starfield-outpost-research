# Offline mechanism audit and corrections

Pinned Starfield 1.16.244.0 executable SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Native addresses below are static VAs, image base 140000000. Save offsets in
receipts are decoded logical-stream offsets; ESM offsets are original-file or
explicit decoded-subrecord offsets. None are runtime pointers or interchangeable
with handles, FormIDs, alias IDs or resource triples.

| Route | Completed observation / conclusion | Local primary evidence |
|---|---|---|
| Extra80 | TESQuest+aliasID, not PKIN/groupID. 14053d4e0 casts to TESQuest; 140cf72d0 indexes quest+90. 140517c00 resolves ALLA keyword/targetalias through 140500ba0 cache and bound aliases. All cache producers/consumers and four sentinel aliases audited. | specialist/native01–20; final-report.md |
| Installed alias defaults | All 38 ESMs/all 2675 QUST variants: 31411 aliases, 2643 ALLA pairs, zero 054ba6/191/192 keys. Positive other keys across 9 plugins. Override selection cannot introduce an absent key. This excludes the recovered alias route for these keys, not arbitrary mods. | specialist/alla-global01.json; probe07.py |
| Static XLKR | All 6,935,033 REFR/ACHR variants: 428 WorkshopItem defaults, 12 target refs, all target base 024dc7 OutpostPlayerHouseActivator, none ordinary 2c60e9. All source and target NAME fields retained. | default-links-01.json; default-catalog01.json; default-bases01.json |
| Base overrides | All 19129 nonactor flag 80 references audited; no ordinary-beacon base override. Four changed static default-owner refs lack flag 80. Noninline sources are not excluded merely because inline base is absent. | base-overrides01.json; typed-full03 |
| Explicit 4C | Full 205557 R3 necessary-condition queue census finds 8628 WorkshopItem leads, exactly old members, no additional serialized-key leads. All actual REFR 4A. Absence excludes that saved edge only. | typed-census01.json; typed-full03 |
| Reverse 4D | Save mask zero versus 4C100; no 4D loader branch. Every identified 518750 insertion path derives from forward 4C, including postload/clone/queued paths. No independently persisted reverse membership table in this route. | specialist/reverse-report.md; native21–26 |
| Optional header byte | BUFFER VERSION override, not form type. 14185dff0/14185e180 and 141863e00→14186d830 propagate it to LoadBuffer. Old framing remains usable; its explicit_type label and semantic decoy test are superseded. | specialist/header-type-table03.json; native13–19 |
| Actual form types | Ordered footer runs at directory+2c map through 59 bytes at 144a53290. Repeated indices and run order preserved; all counts close. Save52: 155540 REFR, 8381 ACHR, 23844 nonreference-family records. | workshop_population.py; typed-full03 |
| Alternative prefixes | Cases 0/4/5/6/7 parse all 181713 reference-family records with zero prefix errors. Unknown extra suffixes remain unknown. FD has a zero-length body, not an unparsed DA barrier. | typed-full03; reviewer-class-check06/07 |
| Registration | Setter 100 reaches ChangedFormMap only when manager/form/TLS/cell gates admit it. Ordinary clone helper restores a temporarily introduced TLSbit0; inherited suppression remains. Type 5 restoration can suppress AddChange. No universal constructed→R3 theorem. | specialist/change-registration-report.md; native27–30,51–61 |
| Global envelopes |17R1+21R2+9R4=47units close exactly. 0/2 are out-of-line pointers; strings precede length where maskC; 1009 follows native unknown-mask zero, explicitly retained. | global-census01.json; workshop_global_units.py |
| Type 2 | Full 306809 saved IDs mapped to BSResource::ID triples. Triple words are not component type IDs. All 848 positive roots and ten selected missing DA groups present; mapping itself creates no placed-reference owner authority. | type2-probe01.json; native31/32/39/41 |
| Type 5 | Full 3708 entries/183318 identity pairs; kind 4 three extra IDs. All 352 unique static CELL/WRLD sources independently typed; native clone dispatch examined. None 8628 direct members/19 beacons/848 roots/ten selected groups occurs. One other dynamic DA group belongs to a kind 4 ship mapping. | reviewer-type5-complete14/source15/member-crosscheck16 |
| Type 4 | Both full bodies close: S1 59 template entries/734 typed IDs; Save52 371 templates+1 custom/4432 IDs. Zero typed joins to 31 groups/17 missing/64 parents/19 beacons/848 roots/8628 members. Generic templates include nonship definitions: no ships-only claim. Selector requires existing owner/+230; custom source cloning separately traced. | specialist/type4-census01/context01; type4-consumers-report.md; native77–80 |
| Type 6 | All 43 sections close exactly, S1 297569 and Save52 1451260 end offsets. Includes cell/world clones, activities, colors, blobs, CalculatedPackinData, effects and final version-gated tables. Component storageID is FOUR bytes, with native low 24-bit token resolution. | components01; type6-walk14; workshop_components.py; native37–78 |
| Activity reconstruction | All 30 name→factory→runtime+70/+90 paths mapped. StarbornManager-zero format reads derived payload before common counter/status. Save52 has 9 BuildWorkshop activities, both identity arrays empty; counters are not one-row physical identities. | specialist/activity-dispatch01/activity-report.md; activity-census01.json |
| Historical witnesses | Existing protected historical saves are searched for exact target/source/owner fingerprints; repeated FFIDs alone cannot prove continuity across resets/characters. | specialist historical-target receipts; final review |
| Historical cohort closure | All 261 available originals examined. 165 modern typed/96 older framing-only. Only two complete current fingerprint witnesses, both 171/171 full resource triples; neither supplies missing roots. All 96 older resource arrays/ID runs close with 6031 numeric matches but zero full current triples. | specialist/historical-witness14; historical-resource15; historical-old-resource17; historical-report16.md |
| Replacement alternatives |88 nonmember 191 REFRs: 8 enabled ship-source cases, 80 disabled sources→8 wall targets→two missing Hab canonical groups. Exact PKIN/CELL/template ancestry and native dummy selector prevent eight false added roots. | reviewer-relations21; reviewer-ancestry22; canonical-candidates01 |
| Papyrus owner/history | Actual direct FF writer and handle-kind domains qualified; 54940 bound/44 unbound headers strictly decoded. All 19 beacon bindings retained. No ordinary handle for 17 missing groups/8 extra targets; variables resolve through those same object/handle maps. Entire VM tail not decoded, and no physical-nonexistence/deletion claim. | specialist/native81–99; papyrus-bindings20; papyrus-report21.md |
| Non-reference/location route | All 23,844 non-reference R3 queues tested; all 2,201 actual BGSLocation records close. Nineteen target locations retain 424 LCRT/reference pairs. Exact WRLD XLCN + type 5 cloned-location joins associate the two Hab worlds with historical beacons. Location registration and Workshop owner assignment are separate native writes. The indirect 142121570 selector requests ShipFastTravelMarkerRefTypeDO, not OutpostBeacon_RefType; context is not authoritative ownership or construction origin. | nonref-targets01; specialist/location-census24/location-target25; reviewer-hab-world-source28; native100–116 and final location report |

All rejected interpretations remain in earlier receipts. Type 6-walk 01–13 retain
failed boundaries, including a guessed version byte, three-byte storage IDs,
uniform activity payloads and an incorrectly described virtual reset. Strict
native leaf decoding replaced those guesses. No failed partial parse is used
as a terminal negative. Exact native evidence and raw decompilation stay local.

Dependency: installed default key → explicit/alias lookup → forward 4C → derived
reverse 4D → foundation 192 and replacement 191/group DA → native single/compound
representative. Separately, resource identities → type 5/static sources → type 4/6
restoration → final loaded references. No geometric nearest-beacon shortcut,
class-name exclusion or recipe-only detector is used as ownership authority.
