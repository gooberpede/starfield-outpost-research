# State, Relationship, and Representation Register

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
