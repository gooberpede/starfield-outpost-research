# State, Relationship, and Representation Register

## SOR-ST-0026 — Native stored terrain workshop center/radius and selected-grid result

[EXP0021 / EV0029](experiments/durable-position-engine-oracle.md): terrain singleton
145fd9c30→+130 owner stores native center at+90/+98 and radius+9c, with raw
activation/dirty flags e8/e9/ea. Producer1421b2570 and bounds consumer1407a6540
are statically mapped. RUNTIME-DERIVED/TRANSIENT; persistence not established.
Reset can zero radius while leaving center; identical brackets do not establish
freshness or active identity. Separate140ad0b90 stack hierarchy is computed native
coverage state with selected base/translation, not a serialized ID. Observer0.1.1
and disposable trace qualify acquisition only, no new live observations. No
change to ST0021/0025 persisted-vector/world classifications; review required.

## SOR-ST-0025 — Persisted world descriptor, component link and selected saved frame

[EXP0020](experiments/activated-overlay-static-exhaustion.md): unit3 generated-world descriptors persist body/key/legacy ID, distinct from the leading active-context key/checksum reuse discriminator. Packed key encodes X16/Y16/tag3/index6/system18; reserved bits retained, tags2/3 reversed before native hierarchical lookup. Unit6 world component persists linked/system/index/secondary/flags/signed bounds, distinct from galaxy site30-byte entries and reconstructed activated edge. Unique selected parent→secondary descriptor joins supply saved origins. Frame20 distinguishes studied source-origin-relative/site-relative XYZ; native ref+d3 mask02 and future runtime validity/height remain distinct domains. STRONG scoped interpretation proposed, REVIEW-REQUIRED, raw LOCAL-ONLY. Arbitrary future manager aliases/epoch are not persisted origins.

## SOR-ST-0024 — Active pair, reconstructed overlay payload and frame epoch

[SOR-EXP-0019](experiments/activated-overlay-and-grid-geometry.md#activated-overlay-reconstruction-map),2026-10-10. Terrain+b0 (mode3:+1a8) supplies active angle pair; all9 mode2 captures project10464,21120, agreeing with separate+c8 origin. ActivatedOverlayProperty shifts+8/+c, bounds+10..1c, pair+20/+28, height+30, flags+34/+35 are typed constructed runtime state; BGSWorldSpaceOverlay_Component BNAM/body identifiers are DEFINITION-DERIVED. Rebase uses terrain+1ec/+1f0 and changes shifts/bounds together. Payload save persistence UNCLASSIFIED; selected saved-frame join/epoch OPEN. Scoped STRONG semantics proposed, REVIEW-REQUIRED. Persisted reference XYZ/Workshop compensation/site associations retain separate evidence; no automatic old-state promotion.

## SOR-ST-0023 — Parent reference transforms, overlay translation and compensated center

2026-10-10, [SOR-EXP-0018 / SOR-EV-0026](experiments/durable-outpost-center-and-object-transforms.md). Persisted case5 XYZ/conditional rotations and Workshop compensation are separate from reconstructed ActivatedOverlayProperty selection. Typed payload+8/+0xc int32 shifts times100 and+0x30 floatZ are valid only with+0x35 clear; edge+0x20 is payload origin. Parent/world keys and inclusive cell bounds select the map. Captured terrain mode2 origin+c8 is10464,21120 in nine checkpoints. Stored center and general loaded center cannot universally be equated without that selection. Scoped STRONG interpretation proposed for tested transforms; continuous embedding OPEN; OBSERVED-INTERNAL only, REVIEW-REQUIRED. No old state reclassification.

## SOR-EXP-0017 supplement to SOR-ST-0021 — Proposed scoped persistence/semantics update

[SOR-F-0021 / SOR-EV-0025](experiments/workshop-origin-beacon-relocation-persistence.md) supersedes the earlier unresolved interpretation **for this sampled modern branch**, preserving the original entry below. Concrete Workshop::ExtraData type 0xbc, allocated 0xa0, vtable RVA 0x4c24e60; +0x60 is three float32 values, typed relocation accumulation/current-XYZ compensation with reset paths. **PERSISTED** directly in four framed Save25/26 Workshop prefixes (12 bytes; see decoded offsets), confirmed by native saver/loader and matched captured fields across pointer reacquisition. Scoped STRONG original-center/persistence semantics proposed pending critical review. Does not establish universal load authority, immutable birth origin, historical grammar, exhaustive writes or safe integration. Raw evidence LOCAL-ONLY; authored REVIEW-REQUIRED.

## SOR-ST-0022 — Radius property, compensated descriptor and terrain coverage

[SOR-F-0022 / SOR-EV-0025](experiments/workshop-origin-beacon-relocation-persistence.md). Ordinary ACTI property OutpostBuildAreaRadius 150.0 is DEFINITION-DERIVED; fItemPlacementRadius:Workshop native default 71.40000152587890625 is a separate configurable fallback. Descriptor center +0x00, frame index +0x0c, radius +0x28 and separate heights feed horizontal circle or region/volume paths. Runtime effective values unobserved; persistence UNCLASSIFIED for modifications/overrides. Terrain/overlay coverage consumes compensated center plus frame translation and quantizes; it does not locate the moved beacon continuously. Native-unit compatibility supported; metres, full permission authority and integration unvalidated. REVIEW-REQUIRED.

## SOR-ST-0021 — Observed workshop relocation-offset candidate

[SOR-EV-0024 / SOR-H-0010](audits/beacon-observer-initial-live-results.md), pinned1.16.244/observer0.1.0. In-memory ExtraWorkshop-candidate+0x60 holds three float32 values matching original beaconXYZ minus current beaconXYZ for one move and controls; bit-identical after manual Save26/reload with changed workshop pointer. Reference transform at+0x8c and this offset are distinct fields. Runtime byte relation OBSERVED-INTERNAL; authoritative boundary-center/radius semantics PROVISIONAL. Persistence class UNCLASSIFIED: post-load survival alone does not prove direct serialization. No serialized offset/native consumer/writer/safe integration established. Raw byte locators and exact arithmetic in report; REVIEW-REQUIRED.

## SOR-ST-0020 — Derived terrain indices and runtime frame inputs

[SOR-EXP-0015](experiments/exact-beacon-planetary-coordinates.md), SOR-F-0020/H-0009/EV-0021. Qualified saved site/XYZ/initial flags PERSISTED. Recovered grid indices/common-origin candidates are DERIVED, not new wire fields. Native manager+50 R, origin+0xc8/+0x1c0, activated-overlay shift+8/+c/+30 and cached ExtraData0x81 pair/body OBSERVED-INTERNAL; persistence/authority UNCLASSIFIED without wire linkage. Pair and fractional XYZ travel separately; active-world angle consumer quantizes, other-world/cached branches can supply anchors. Exact continuous embedding/post-load authority/integration unvalidated. REVIEW-REQUIRED, prior records retained.


## SOR-ST-0018 — Alternate placement prefix and omitted flag state

[SOR-EXP-0010 / SOR-EV-0016](experiments/active-outpost-membership-completion.md), SOR-F-0015. Case-6 conditional REFR initial data consumes cell and placement-parent queue entries, transform and two signed int16 indices, then general self reference. HIST-0016 change flags `0x92018200` omit saved flags: disabled/deleted are UNKNOWN/inherited, not stored false. Ordered queued refs and token-domain distinctions remain PERSISTED structural evidence; final loaded identity and ownership are MIXED/unvalidated. Installed template/base relationships are STATIC; R1 adjacency interpretation and conditional plugin mapping remain INFERRED. ExtraPromotedRef type0x84, ExtraOwnership type0x1f and ExtraWorkshop type0xbc must remain distinct. Nonempty type0x80 / unknown ExtraFlags buffer version stop decoding. No complete player-membership predicate or negative proof; REVIEW-REQUIRED.

## SOR-ST-0017 — Framed change records and conditional beacon initial data

[SOR-EXP-0009](experiments/active-outpost-identification.md), SOR-F-0014 / SOR-EV-0015. R3 tag/optional type/token/change flags/counts, ordered three-byte reference queue, uint16 string queue and body are PERSISTED / PROVEN within exact sampled closure. Save tokens require tagged resolution and load remapping; they are not runtime pointers or stable logical IDs. Case-5 parent/base/self consumption and saved form/auxiliary flags have STATIC loader support; actual inherited form types and alternate initial-data base resolution remain UNKNOWN. Saved disabled flag maps conditionally to runtime IsDisabled, while active-player membership is unresolved. Almanac's runtime workshop registry is MIXED/reconstructed evidence: global handle list, keywords, parent condition and ExtraWorkshop predicates are observed statically, full serializer/reconstruction equivalence UNKNOWN. Version-dependent ExtraWorkshop load branches prohibit transferring raw payload offsets without validation. REVIEW-REQUIRED, OBSERVED-INTERNAL only; no callable interface or zero-active proof. Earlier SOR-ST-0010 window bounds are superseded only where the new framing explicitly validates them.

## SOR-ST-0015 — Bounded beacon-reference and keyed relationship collection

SOR-EXP-0006 / SOR-EV-0012 / SOR-F-0012. [Exact grammar and all-corpus counterexamples](experiments/mature-save-outpost-validation.md). Observed 0x79 / uint32-length envelope in directory R2, beacon count/references then keyed counted reference groups; 9/12/19/1588-byte payloads consume exactly. Bytes PERSISTED in inspected saves, SAVE / PROVEN structural observation; name/relationship semantic association INFERRED, proposed STRONG pending review. Mature 17 references match JSON active names; all-known-active membership is not proven. S1/S2/S7 beacon candidates remain outside the collection. Inclusion trigger, logical owner, zero-key purpose, complete identity resolution and load authority UNKNOWN. SOR-ST-0011 output-link association remains proposed STRONG; framing support does not determine direction. REVIEW-REQUIRED.

## SOR-ST-0016 — Member-associated cargo-marker windows and reciprocal pad references

SOR-EXP-0006 / SOR-EV-0012 / SOR-F-0012; extends static SOR-ST-0003/0004 without claiming runtime validation. 61 observed marker-like windows use repeated three-byte tokens and regular/fueled base-like anchors; 53 contain one member-beacon pattern within 128 bytes. Save-derived 655cc8/dynamic-token occurrences produce 24 nonself reciprocal pairs; three self repeats retained separately. Bytes PERSISTED in SOR-SAMPLE-0029; semantic marker type, association and cargo topology proposed STRONG pending critical review. Matching 17 JSON names/counts/types/full multigraph does not map app UUIDs or resolve complete record ends, stable runtime identities, directional cargo, inventories, timing, owner/consumer or authoritative restoration. Eight unassociated windows remain unresolved. OBSERVED-INTERNAL research, no safe integration. REVIEW-REQUIRED.

## SOR-ST-0014 — Shared name/animation collection and beacon index correspondence

SOR-EXP-0005 / SOR-EV-0011 / SOR-F-0011. [Bounded containment](experiments/outpost-save-structural-containment.md). OBSERVED counted uint16-length string collection reached by an early logical uint32 pointer; uint16 index triples within SOR-ST-0010's beacon window match SOR-ST-0012's name and two following beacon animation entries across 20 beacon-bearing labels. Bytes PERSISTED; reference interpretation INFERRED/STRONG proposed for review. Collection is shared, not an exclusive outpost header. Parent logical owner, consumers, load authority, full object record boundaries and stable game identity UNKNOWN. Separate from three-byte candidate tokens. Existing semantic candidates are unchanged; SOR-ST-0011 remains a relationship/collection region with unresolved internal schema. Publication REVIEW-REQUIRED.

## SOR-ST-0011 follow-up — Link-only removal/recreation

SOR-EXP-0004 / SOR-EV-0010 / SOR-F-0010: [bounded validation](experiments/output-link-validation-L0-L2C.md) preserves the failed original literal test across reload and observes a corresponding remapped/reordered relationship payload. Endpoint-pair entry present in L0/L0C, absent L1/L1C, restored L2/L2C; payload length 19/19/12/12/19/19. SOR-ST-0010's four candidate object windows remain, with new-session tokens stable throughout. Bytes PERSISTED; semantic association with output-link state is proposed STRONG pending review, not automatically promoted. Separate list/relationship region best fits the observed placement; logical owner, count encoding, mirroring, direction, authoritative post-load consumer and runtime identity mapping remain unresolved. The historical provisional records below remain intact. Publication REVIEW-REQUIRED.

## SOR-ST-0010–0013 — Manual-corpus saved candidates

SOR-ST-0013 offline correction: [comparison with verified A0/A0C live coordinates](experiments/manual-save-corpus-S0-S7C.md#offline-comparison-with-earlier-exp0002-live-player-coordinates) gives candidate distances 6.830539 / 8.997486 / 26.000118 without physical units. This strengthens only SOR-H-0004's provisional same/related local-frame interpretation. Frame origin, units, axes, reference ownership, body-relative meaning and latitude/longitude conversion remain UNKNOWN; no authoritative object-transform or cross-session identity mapping established.

SOR-EXP-0003 / SOR-EV-0009 / SOR-F-0009; SOR-SAMPLE-0006–0022. [Exact signatures, offsets and lifecycles](experiments/manual-save-corpus-S0-S7C.md), [ledger](experiments/manual-save-corpus/candidates.csv). All SAVE byte observations; semantic assignments PROVISIONAL, publication REVIEW-REQUIRED. No runtime identity mapping or safe integration point.

| ID | Candidate | Observed lifecycle | Persistence/authority limit |
|---|---|---|---|
| SOR-ST-0010 | B/T/E/P object-window family | B appears S1; T S2; E/P S3; E disappears S7, others persist | Bytes PERSISTED in these samples; roles inferred; full record bounds, ownership and reload authority UNKNOWN |
| SOR-ST-0011 | B/T/E relationship motif | Absent through S3C; present S4–S6C; absent S7 onward | Bytes PERSISTED; output-link interpretation inferred, endpoint direction/authority UNKNOWN |
| SOR-ST-0012 | Outpost name string neighborhood | Kreet Outpost 1 S1–S4C, SOR-001 S5 onward | Text PERSISTED; string-table reference to B and authoritative post-load consumer UNKNOWN |
| SOR-ST-0013 | P/B position candidates and location labels | P tuple changes only at S6; B tuple stable through actor/solar movement; header Kreet label | Bytes PERSISTED; XYZ interpretation inferred; units, frame, body mapping, latitude/longitude UNKNOWN; Narion only a script-name lead |

## SOR-ST-0009 — Candidate save-manager coordination state

SOR-ENV-0003 / SOR-EV-0005 / SOR-F-0007. Static global `0x145e6d6e8` (RVA05e6d6e8) supplies the manager to the UI new-slot call. Request reads manager-relative+50; finalization setup exchanges+8c to1 and completion path clears+8c then wakes waiters. These are instruction operands, not a declared native layout or save offsets. Live object identity, lifetime, status enumeration, authority, complete synchronization, persistence and serialized representation are UNKNOWN; persistence UNCLASSIFIED. PROVISIONAL busy/completion interpretation, OBSERVED-INTERNAL, REVIEW-REQUIRED. [Detailed map](experiments/SOR-EXP-0002A-native-save-thread-mapping.md) preserves alternative/error/backend paths. No field was semantically validated live.

Concrete candidates below are supported by static evidence only. No saved record or cross-domain identity mapping is established. Evidence/entry hashes and native operand domains: [SOR-EV-0001](experiments/evidence/initial-reconnaissance/README.md). All publication classification REVIEW-REQUIRED.

| ID | Subsystem / concept | Runtime representation | Saved representation / offset domain | Definition dependencies | Persistence class | Lifecycle / authority | Build and sample scope | Confidence / evidence |
|---|---|---|---|---|---|---|---|---|
| SOR-ST-0001 | Member-to-workshop query relation | GetWorkshop callback reads source-object operand +0xc8 and global key; full runtime structure UNKNOWN | UNKNOWN | Beacon ACTI 002C60E9; WorkshopKeyword 00054BA7 are separate definition facts, not resolved callback-global proof | UNCLASSIFIED | Authority/creation/cleanup UNKNOWN | SOR-ENV-0001, no save sample | SOR-F-0003, SOR-H-0001; STATIC/provisional model |
| SOR-ST-0002 | Storage capacity/filter definition | Runtime value after modifiers UNKNOWN | UNKNOWN | Starfield.esm CONT 0023AED9: CarryWeight 000002DC default 75; OutpostBuildContainer 0000F65A default 1; filter FLST 0029954D | DEFINITION-DERIVED for recorded defaults only | Native enforcement and runtime overrides UNKNOWN | SOR-ENV-0001, focused xEdit sample | PROVEN STATIC xEdit observation; SOR-F-0004 |
| SOR-ST-0003 | Cargo endpoint relationships | Script keyword-linked reference candidates and quest/ship properties; live identities UNKNOWN | UNKNOWN | LinkOutpostCargoIncoming 002A6C46, Outgoing 002A6C45, Active 00255CC8; QUST 002A6C44 | UNCLASSIFIED | Script create/clear/transfer paths identified; native authority UNKNOWN | SOR-ENV-0001 | PROVEN STATIC names/source; relationship semantics unvalidated |
| SOR-ST-0004 | Cargo animation state | ActorValue OutpostCargoLinkAnimState 00333D22, source SetAnimationState/OnLoad consumers | UNKNOWN | ACTI 002A6C3F/00219523 marker script; AV definition independently inventoried | UNCLASSIFIED | Source-level read/write and animation reconstruction; saved authority UNKNOWN | SOR-ENV-0001 | SOR-F-0002, SOR-H-0002; STATIC |
| SOR-ST-0005 | Selected manufacturing output | Runtime product/rate UNKNOWN | UNKNOWN | CONT 0027319F has ResMfg_Tier01_AdaptiveFrameAV 00245794 default 1 and PowerRequired 00000330 default 5 | DEFINITION-DERIVED for recorded defaults only | No rate/scheduler/delta-time semantics inferred from values | SOR-ENV-0001 | PROVEN STATIC xEdit observation; SOR-EV-0001 |
| SOR-ST-0006 | Crew association | GetWorkshop/AssignCrew path in OutpostActorScript; crew station removal callback | UNKNOWN | AssignAsCrewOnCreation, CrewSlotCost, CrewReassignDisabled source properties; actual robot record values UNKNOWN | UNCLASSIFIED | Script condition/assignment paths only; modifier application/persistence UNKNOWN | SOR-ENV-0001 | STATIC SOR-S-0104; runtime question OPEN |

Use `SOR-ST-` IDs. Unknown columns must say `UNKNOWN`, not be silently inferred. Record owning object, identity, lifetime, creation/update/consumption, relationships, and whether an interpretation is structural or semantic. Link detailed evidence rather than putting guessed layouts into this table.

## SOR-ST-0007 — Coordinate-name binding candidate

SOR-ENV-0002; STATIC evidence SOR-F-0005 / SOR-EV-0002. Starfield function 0x14167f7e0 passes object-relative addresses +0x68/+0x88 with latitude/longitude names. This does not define raw numeric fields; owning type, object lifetime, body/outpost link, units, authority, runtime acquisition and saved representation are UNKNOWN. Persistence UNCLASSIFIED; UI/property-binding interpretation PROVISIONAL. Keep reference transform, cell/worldspace, body-relative and map/lat-long domains separate. REVIEW-REQUIRED. No field read live or safe integration established.

Persistence classes and integration statuses are defined in [EVIDENCE_STANDARD.md](EVIDENCE_STANDARD.md). An in-memory field is not proof of a serialized field; a stored value may be replaced or recalculated during load. Record mappings between runtime pointers, handles, FormIDs, saved identifiers, and logical entities only once demonstrated.

## SOR-ST-0008 — Candidate native checkpoint byte views

SOR-ENV-0002 / SOR-F-0006 / SOR-EV-0002. Fresh runtime reference FormID/pointer, stored base/parent, raw transform and candidate identifier are separate output fields. Native operand table and consulted type leads in STATIC-CONTRACT.md. Owning engine lifetime, resolved handles, loaded-3D, coordinate units/frame and saved authority UNKNOWN. Repeated reads do not provide atomicity or ownership. No live value acquired; persistence UNCLASSIFIED, not PERSISTED. Selection is limited to two candidate cell views and exact beacon/storage roles, not exhaustive outpost membership. REVIEW-REQUIRED.

## Historical triage follow-up — SOR-ST-0013 / SOR-ST-0015–0016

[SOR-EXP-0007 / SOR-EV-0013](experiments/historical-save-inventory-triage.md) extends observational coverage to 275 fully inspected historical saves, with three resource-limited metadata-only inputs. Selected counts and provisional absence candidates do not establish a universal active index or residual-state exclusion. Name-associated float tuples extend SOR-ST-0013 as PROVISIONAL local-coordinate candidates; no engine body ID, planetary frame, complete record bounds or load authority is recovered. SOR-ST-0015–0016 ownership, inclusion and runtime cargo semantics remain unresolved; no semantic promotion or new safe integration point.

## SOR-EXP-0011 scoped detector view of SOR-ST-0017–0018

[Ordinary beacon detection](experiments/ordinary-outpost-beacon-detection.md) adds a research view of already identified PERSISTED token/prefix/flag evidence, not a new serialized field. Case-5 inline ordinary identity and saved disabled-clear/set/omitted/unresolved classes are separate from registration/player ownership. Logical record bounds, queue locations and compressed-stream spans are explicitly different address domains. R1 template adjacency is still a lead; loaded identity and omitted-state reconstruction remain unvalidated. No prior state classification is promoted. REVIEW-REQUIRED; no integration interface.

## SOR-ST-0019 — Saved overlay/body associations and surface-anchor pair

[SOR-EXP-0012](experiments/save-capacity-and-planetary-location.md), SOR-F-0017 / SOR-H-0008. SAVE bytes PERSISTED within sampled serialization; authority after load, engine owner/lifecycle and runtime identity mapping UNKNOWN. Case-5 beacon parent token links into a bounded R1 unit 6 through four-byte little-endian tagged saved identity; one structure carries system/body index/source-world token, another direct PNDT token and repeated overlay key around two doubles. Two structures agree for S1/S1C/L2C and 17 mature clear records; cache-only evidence is weaker for two set records. Parent, source world, PNDT FormID, body index, system key and STDT FormID are distinct. Surface frame/units, exact anchor and local-to-global transform UNKNOWN. Proposed scoped STRONG body association; PROVISIONAL surface interpretation; OBSERVED-INTERNAL only, no validated integration or live mutation authority.

### SOR-EXP-0013 follow-up, proposed for review

[Surface-anchor research](experiments/planetary-surface-anchor-semantics.md) adds STRONG proposed longitude-first/latitude-second radian semantics within sampled SOR-ST-0019 pairs. PERSISTED describes observed save bytes; installed PNDT fixed-world angles are separately DEFINITION-DERIVED, while analytical unit vectors/degrees are derived research views. Native CTPlanetOverlayData creation couples pair/world identity and can adjust a selected point through terrain coordinates. Full generic wire mapping, authoritative restoration and exact local beacon position remain UNKNOWN. Engine +Z/+X/+Y convention does not clear Earth/compass/texture orientation. No earlier classification is silently replaced; OBSERVED-INTERNAL, REVIEW-REQUIRED.

### SOR-EXP-0014 follow-up to SOR-ST-0013 / SOR-ST-0019

[Save25 comparison](experiments/two-outpost-site-anchors-and-beacon-coordinates.md) supplies two structurally owned case-5 local XYZ tuples and distinct parent-keyed planetary pairs. Bytes are PERSISTED in this sample; exact runtime owner/frame/authority remains UNKNOWN. Same source-world token is a cache lead, not proven same loaded cell/frame. Shape 0 omits rotation floats; reconstruction is UNKNOWN. Old cache-window predicate admits an unrelated/ambiguous Uranus-shaped match for SOR-003; direct repeated-key PNDT evidence separately supports Kreet. Native `14077fc20/14078d370` shows grid-origin/resolution and sub-grid residual stages. These in-memory inputs are not assigned guessed wire offsets. Precise beacon conversion and all integration status remain unvalidated; REVIEW-REQUIRED, no historical classification silently changed.
