# SOR-EV-0024 — Initial beacon move/save/reload live results

2026-10-10, Australia/Sydney. SOR-EXP-0016 / SOR-D-0035 / SOR-H-0010. Authored results REVIEW-REQUIRED; raw captures, saves, logs, pointers and full manifests LOCAL-ONLY. [Operator/session chronology](../experiments/beacon-observer/initial-live-session.md), [approved card](../experiments/beacon-observer/Save25-operator-run-card.md), [installed preflight](beacon-observer-post-deployment-preflight.md), [implementation/provenance](live-beacon-observer.md).

**Moving SOR-003 changed one captured beacon transform; its new XYZ survived manual Save26/reload, while SOR-002's XYZ stayed unchanged. A workshop float triple changed from zero to the original-minus-current beacon displacement and survived reload.** The operator observed no boundary shift after moving or reloading. This is useful scoped live evidence of an original-location offset candidate; boundary-center authority and exact continuous planetary coordinates remain unresolved. One deliberate displacement, one manual reload and one fast-travel comparison were tested. No universal behavior or safe integration point is claimed.

## Direct runtime observations and interpretation

All offsets here are **in-memory member byte offsets**, not save-file offsets. FormIDs identify captured references within this exact sample/session; pointers/handles are separate domains. Source game SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`, Steam1.16.244.0; SFSE 0.2.21 hash `28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b`; approved observer 0.1.0 DLL hash `0e910a3ec6362adf050add3a9cd754246ac12f25e5ae55426d1c44ed93848a31`. Fresh READY matched PID 17596/process creation and module identities; SFSE log confirmed plugin loaded. Observer worker used guarded non-atomic reads, with no engine calls, hook, breakpoint or memory mutation. Gameplay, save, reload, travel and exit were operator-controlled.

| Captured reference | Before move, XYZ float32 displayed | After move, save, reload and travel |
|---|---|---|
| SOR-003-associated `FF01AB8F` | `(356.820404,2459.05859,-31.8908424)` | `(337.853455,2406.4187,-35.214077)` |
| SOR-002-associated `FF01AB50` | `(122.700455,273.046234,18.3525066)` | Bit-identical throughout |
| Additional base-defined candidate `0029A8C8` | `(0,0,0)` | Bit-identical; interior branch unsupported |

Selective response to the operator's move and proximity before/after fast travel support the SOR-003/SOR-002 associations within this run. The additional candidate is retained, not mistaken for a third player-controlled outpost or discarded to force a count. Ordinary-base selection is not exhaustive membership/ownership identification. Repeated identity and handle-slot association passed for all three beacon candidates; player association was false and was retained as a diagnostic. Fresh roots were reacquired after reload even though reference pointers/handles happened to remain unchanged; both workshop-extra pointers changed on reload.

The moved beacon's exact XYZ bytes are `0369b243f0b019457220ffc1` before and `3eeda843b366164537db0cc2` after. Displacement magnitude is approximately 56.0513 local units. The operator selected a depression described as about 46 m away; neither its achieved distance nor a unit conversion was measured. These numbers are not treated as equal or as planetary distances.

For the SOR-003-associated captured ExtraWorkshop candidate (type 0xbc), the 12 bytes at **+0x60** are zero through `premove-003`, then become:

```text
50bc9741408f5242e0af5440
float32 LE: (18.966949462890625, 52.639892578125, 3.3232345581054688)
```

Across all nine snapshots, independently decoding the preserved reference/workshop raw bytes shows:

```text
workshop[+0x60:+0x6c] == float32(original_beacon_XYZ - current_beacon_XYZ)
float32(current_beacon_XYZ + workshop_tuple) == original_beacon_XYZ bits
```

The control beacon's tuple remains zero. The moved tuple is bit-identical after save, reload, reload control, SOR-002 visit and visit control, including after the workshop object's runtime pointer changes. During the premove→moved transition, the only changed bytes in its captured 0xa0-byte workshop prefix are +0x60–+0x6b; the captured 192-byte workshop table is unchanged across that move. Other bytes/tables change around reload, and earlier build-UI inspection changes +0x90–+0x93. These counterexamples prevent treating the entire object/table as invariant or labeling every changed byte a move field.

**Interpretation, SOR-H-0010:** the tuple may compensate for beacon relocation to retain an original workshop location. Exact arithmetic is directly supported here; boundary-center semantics remain PROVISIONAL. Alternatives include a relative transform/repositioning cache used for another workshop purpose. No consuming native function, writer/lifecycle, radius field or serialized offset is identified. Survival through load is POST-LOAD OBSERVED, not proof that these exact bytes were serialized rather than reconstructed. The operator's no-boundary-shift observation is consistent supporting evidence without a measured center/radius or landmark geometry. A second independent displacement or static consumer mapping would distinguish broader interpretations, but neither is automatically authorized by this handoff.

## Terrain/frame coverage and unresolved primary objective

Both sites capture terrain mode 2, selected origin+c8, coarse indices `(54,110)`, sub `(8,0)`, fine `(0,0)`, grid resolution 256 and block+merge 12; candidate axis steps are 49152. Decoded origin bytes and grid fields match across the two sites and controls. The terrain raw prefix nevertheless changes at +0x190/+0x194/+0x198/+0x19c on travel, and active/world prefixes change during no-action controls too. Equal decoded origins do not mean all frame state is equal. Two additional raw sections at SOR-002 concern linked extra data; no guessed semantics assigned.

No ExtraData0x81 cached-pair section was emitted for either player-placed beacon in these snapshots. This describes collector output, not proof that no planetary cache exists anywhere. Native residual conversion, alternate-overlay authority and continuous body embedding are still open. This run delivers rich raw evidence and a reproducible original-location-offset lead; it does not solve exact planetary beacon coordinates. The previously validated discrete 49152 projection is preserved without extending its claim.

## Acquisition completeness, machine safety and target survival

| Checkpoint | Elapsed ms | Verified raw sections | Journal rows |
|---|---:|---:|---:|
| baseline-003 | 40,344 | 581 | 591 |
| control-003 | 38,328 | 581 | 591 |
| premove-003 | 40,938 | 581 | 591 |
| moved-003 | 38,922 | 581 | 591 |
| saved-003 | 39,157 | 581 | 591 |
| reloaded-003 | 39,782 | 581 | 591 |
| reload-control-003 | 39,515 | 581 | 591 |
| visit-002 | 41,578 | 583 | 593 |
| control-002 | 40,141 | 583 | 593 |

All nine have durable CAPTURE_PARTIAL markers and final metrics; **5,233 raw sections / 5,323 snapshot journal rows** pass unchanged offline inspector checks, including every referenced raw length/hash. No truncated tails, observer failure marker, rejected request or quota/time-based abort. Partial flags are the additional candidate's unsupported interior world branch and intentionally unsupported native calls. Complete journal persistence is distinct from incomplete semantic/collector coverage. Full session inventory is 303,692,684 bytes, including startup/control/retirement files; each checkpoint is about 33.74 MB. Measured working sets are whole Starfield-process costs, not observer memory attribution. Duration range 38.328–41.578 s applies to this run, not a guaranteed timeout/performance promise.

The initial launch lacked SFSE because, according to the operator, Vortex retained Starfield.exe as launch target after re-enabling SFSE. It produced no science capture. Correct SFSE startup succeeded; the operator's60-second startup instruction was adopted, with further time allowed for progress. STOP was sent only after final capture metrics; retirement persisted at 01:37:54.483 UTC (12:37:54 AEDT). Game survived all captures and operator reports normal exit, Steam sync complete and observer disabled. Independent process check confirms game/loader absence; actual deployed plugin directory contains only the Vortex marker. Removing disabled deployed files is operator/Vortex cleanup, not failed preservation. Codex made no deployment/configuration or approved implementation changes.

## Save archival and preservation

Original/frozen Save25 SOR-SAMPLE-0030 remain 2,403,744 bytes, hash `d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5`. New **SOR-SAMPLE-0031 / Save26**:

```text
Save26_D6036588M417474696C61204B6972616C79_000241_20261010012454_4_0_4.sfs
2,409,024 bytes
SHA-256 2b4781e75226f2ff7c6aa47470fb47ff179c1754461aa208c46716d7c3935104
```

Exact new-file identity was selected by before/after directory comparison, not a Save26 glob. An exclusive local archive copy under `.local-work/savegames/beacon-observer/initial-01/` matches the source hash after exit. Operator said time “12:54”; filename/mtime show 12:24:54 AEDT, preserved as separate observations. Save26 was not decompressed, edited or parsed for a serialized workshop-field claim in this pass.

Final hashes confirm pinned game/SFSE/loader, package, selected DLL, all 12 build-manifest source files and both protected Save25 files unchanged. Deployed observer DLL/config are absent after Vortex disabling, not silently replaced. Final available bytes C: 89,613,336,576; D: 139,867,746,304, both above 40,000,000,000. Disk guard was active in unchanged observer; no real low-space event was induced.

## Review package and limits

Local session: `.local-work/beacon-observer-live/session-17596-91165828/`. Local review: `.local-work/beacon-observer-live-review/initial-01/`, containing READY/process/prelaunch/exit receipts, per-snapshot inspector outputs, `final-summary.json`, `session-file-manifest.json`, `root-byte-comparisons.json`, `workshop-60-comparison.json`, `workshop-offset-arithmetic.json`, new-save selection/manifest and copied fresh SFSE logs. Original local `finalize.py` documents reads/writes/dependencies: reads immutable captured files, approved sources/build identities and exact saves; exclusively copies Save26/logs and writes local receipts; stdlib only, no process/game/config mutation. Byte comparisons match attributed root names between snapshots and exclude repeated `.node` roots from the unique-root map; they are not whole-graph semantic comparison. Arithmetic decodes `<3f` at reference+0x8c/workshop+0x60 and rounds each difference/sum with `struct.pack('<3f', ...)`, comparing original bytes.

Authored changes are this report, session ledger, card approval annotation and additive decisions/state/hypothesis/provenance/evidence/subsystem links. Earlier preflight/offline statements remain historical. No new dependency/reuse, debugger/Ghidra work, native save call, save edit, external disclosure, staging, commit or push. Publication eligibility remains independent and no raw material is cleared. Await critical review; deeper static/save analysis or a further experiment is proposed only.
