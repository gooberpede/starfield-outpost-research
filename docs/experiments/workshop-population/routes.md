# Offline mechanism audit and corrections

Pinned Starfield1.16.244.0 executable SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Native addresses below are static VAs, image base140000000. Save offsets in
receipts are decoded logical-stream offsets; ESM offsets are original-file or
explicit decoded-subrecord offsets. None are runtime pointers or interchangeable
with handles, FormIDs, alias IDs or resource triples.

| Route | Completed observation / conclusion | Local primary evidence |
|---|---|---|
| Extra80 | TESQuest+aliasID, notPKIN/groupID.14053d4e0 casts toTESQuest;140cf72d0 indexes quest+90.140517c00 resolves ALLA keyword/targetalias through140500ba0 cache and bound aliases. All cache producers/consumers and four sentinel aliases audited. | specialist/native01–20; final-report.md |
| Installed alias defaults | All38ESMs/all2675QUST variants:31411aliases,2643ALLA pairs, zero054ba6/191/192 keys. Positive other keys across9plugins. Override selection cannot introduce an absent key. This excludes the recovered alias route for these keys, not arbitrary mods. | specialist/alla-global01.json; probe07.py |
| Static XLKR | All6,935,033REFR/ACHR variants:428WorkshopItem defaults,12target refs, all target base024dc7 OutpostPlayerHouseActivator, none ordinary2c60e9. All source and targetNAME fields retained. | default-links-01.json; default-catalog01.json; default-bases01.json |
| Base overrides | All19129nonactorflag80 references audited; no ordinary-beacon base override. Four changed static default-owner refs lackflag80. Noninline sources are not excluded merely because inline base is absent. | base-overrides01.json; typed-full03 |
| Explicit4C | Full205557R3 necessary-condition queue census finds8628WorkshopItem leads, exactly old members, no additional serialized-key leads. All actualREFR4A. Absence excludes that saved edge only. | typed-census01.json; typed-full03 |
| Reverse4D | Save mask zero versus4C100; no4Dloader branch. Every identified518750 insertion path derives from forward4C, including postload/clone/queued paths. No independently persisted reverse membership table in this route. | specialist/reverse-report.md; native21–26 |
| Optional header byte | BUFFER VERSION override, not form type.14185dff0/14185e180 and141863e00→14186d830 propagate it toLoadBuffer. Old framing remains usable; its explicit_type label and semantic decoy test are superseded. | specialist/header-type-table03.json; native13–19 |
| Actual form types | Ordered footer runs at directory+2c map through59bytes at144a53290. Repeated indices and run order preserved; all counts close. Save52:155540REFR,8381ACHR,23844nonreference-family records. | workshop_population.py; typed-full03 |
| Alternative prefixes | Cases0/4/5/6/7 parse all181713reference-family records with zero prefix errors. Unknown extra suffixes remain unknown. FD has a zero-length body, not an unparsedDA barrier. | typed-full03; reviewer-class-check06/07 |
| Registration | Setter100 reaches ChangedFormMap only when manager/form/TLS/cell gates admit it. Ordinary clone helper restores a temporarily introduced TLSbit0; inherited suppression remains. Type5 restoration can suppress AddChange. No universal constructed→R3 theorem. | specialist/change-registration-report.md; native27–30,51–61 |
| Global envelopes |17R1+21R2+9R4=47units close exactly.0/2 are out-of-line pointers; strings precede length where maskC;1009 follows native unknown-mask zero, explicitly retained. | global-census01.json; workshop_global_units.py |
| Type2 | Full306809 saved IDs mapped to BSResource::ID triples. Triple words are not component type IDs. All848positive roots and ten selected missingDA groups present; mapping itself creates no placed-reference owner authority. | type2-probe01.json; native31/32/39/41 |
| Type5 | Full3708entries/183318identity pairs; kind4three extra IDs. All352unique static CELL/WRLD sources independently typed; native clone dispatch examined. None8628direct members/19beacons/848roots/ten selected groups occurs. One other dynamicDA group belongs to a kind4ship mapping. | reviewer-type5-complete14/source15/member-crosscheck16 |
| Type4 | Both full bodies close: S159template entries/734typed IDs; Save52371templates+1custom/4432IDs. Zero typed joins to31groups/17missing/64parents/19beacons/848roots/8628members. Generic templates include nonship definitions: no ships-only claim. Selector requires existing owner/+230; custom source cloning separately traced. | specialist/type4-census01/context01; type4-consumers-report.md; native77–80 |
| Type6 | All43sections close exactly, S1297569 andSave521451260 end offsets. Includes cell/world clones, activities, colors, blobs, CalculatedPackinData, effects and final version-gated tables. Component storageID is FOUR bytes, with native low24-bit token resolution. | components01; type6-walk14; workshop_components.py; native37–78 |
| Activity reconstruction | All30name→factory→runtime+70/+90 paths mapped. StarbornManager-zero format reads derived payload before common counter/status. Save52 has9BuildWorkshop activities, both identity arrays empty; counters are not one-row physical identities. | specialist/activity-dispatch01/activity-report.md; activity-census01.json |
| Historical witnesses | Existing protected historical saves are searched for exact target/source/owner fingerprints; repeatedFFIDs alone cannot prove continuity across resets/characters. | specialist historical-target receipts; final review |
| Historical cohort closure | All261available originals examined.165modern typed/96older framing-only. Only two complete current fingerprint witnesses, both171/171full resource triples; neither supplies missing roots. All96older resource arrays/ID runs close with6031numeric matches but zero full current triples. | specialist/historical-witness14; historical-resource15; historical-old-resource17; historical-report16.md |
| Replacement alternatives |88nonmember191REFRs:8enabled ship-source cases,80disabled sources→8wall targets→two missing Hab canonical groups. ExactPKIN/CELL/template ancestry and native dummy selector prevent eight false added roots. | reviewer-relations21; reviewer-ancestry22; canonical-candidates01 |
| Papyrus owner/history | Actual directFF writer and handle-kind domains qualified;54940bound/44unbound headers strictly decoded. All19beacon bindings retained. No ordinary handle for17missing groups/8extra targets; variables resolve through those same object/handle maps. EntireVM tail not decoded, and no physical-nonexistence/deletion claim. | specialist/native81–99; papyrus-bindings20; papyrus-report21.md |
| Non-reference/location route | All 23,844 non-reference R3 queues tested; all 2,201 actual BGSLocation records close. Nineteen target locations retain 424 LCRT/reference pairs. Exact WRLD XLCN + type5 cloned-location joins associate the two Hab worlds with historical beacons. Location registration and Workshop owner assignment are separate native writes. The indirect 142121570 selector requests ShipFastTravelMarkerRefTypeDO, not OutpostBeacon_RefType; context is not authoritative ownership or construction origin. | nonref-targets01; specialist/location-census24/location-target25; reviewer-hab-world-source28; native100–116 and final location report |

All rejected interpretations remain in earlier receipts. Type6-walk01–13 retain
failed boundaries, including a guessed version byte, three-byte storage IDs,
uniform activity payloads and an incorrectly described virtual reset. Strict
native leaf decoding replaced those guesses. No failed partial parse is used
as a terminal negative. Exact native evidence and raw decompilation stay local.

Dependency: installed default key → explicit/alias lookup → forward4C → derived
reverse4D → foundation192 and replacement191/groupDA → native single/compound
representative. Separately, resource identities → type5/static sources → type4/6
restoration → final loaded references. No geometric nearest-beacon shortcut,
class-name exclusion or recipe-only detector is used as ownership authority.
