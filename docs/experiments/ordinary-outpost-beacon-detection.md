# SOR-EXP-0011 — Scoped ordinary outpost beacon detection

2026-10-09, Australia/Sydney. ANALYZED; critical review required. SOR-EV-0017 / SOR-F-0016 / SOR-D-0028. Authored tools, report and numeric ledgers REVIEW-REQUIRED; original saves, full receipts, donor payload and private oracle LOCAL-ONLY. This handoff grants no integration or publication approval.

## Best-supported answer

The read-only [detector](../../save-analysis/scripts/ordinary_outpost_beacons.py) recognizes the ordinary serialized beacon representation and exposes its saved disabled-state evidence. Save3/S0/S0C yield zero recognized ordinary beacons; S1/S1C each yield one disabled-clear beacon; mature Save52 yields **19 ordinary candidates, 17 disabled-clear and two disabled-set**. A fresh name/token comparison places exactly the 17 clear records in the independently maintained 17-outpost network JSON; both set records fall outside it. Positive ordinary evidence is visible even while authoritative player membership remains INDETERMINATE.

| Dimension | Scoped result |
|---|---|
| Confidence | PROVEN / SAVE for exact decoded bytes, counts and comparisons. Ordinary-beacon identification and the saved-clear/active ordinary association are proposed STRONG within these controls, pending review. STATIC restoration/IsDisabled mapping retains SOR-F-0014's conditions; ownership is unresolved. |
| Tested coverage | Archived pristine/placement/no-action controls, subsequent construction/rename/movement/removal-of-other-object/reload controls, mature network, and bounded historical/donor challenge; exact version ledger linked below. |
| Inferred coverage | Same conditional case-5 identity/prefix in unlabelled historical saves. One-based form-array base representation and omitted flags are synthetic-tested extensions, not independently labelled gameplay examples. |
| Completeness | No complete ordinary-beacon or active-player enumeration claim. Complete sampled R3 framing is a byte-boundary property; it does not resolve omitted/static references, inherited types, content overrides or all base paths. |
| Decisive evidence | [Per-save ledger](ordinary-outpost-beacon-detection/saves.csv), [19 Save52 records](ordinary-outpost-beacon-detection/save52-records.csv), independent 309,057-record arithmetic audit of six primary saves, fresh JSON correspondence after extraction. |
| Limitations | Conditional inherited REFR type; alternate template identity is an R1 adjacency lead; saved flags can be omitted; ownership/registration/load authority and save-era content mapping remain incomplete. |
| Next step | After review of this scoped tool, a separately briefed offline location study should resolve beacon-to-cell/body identity and coordinate frame using existing protected samples. No location decoding or live execution follows here. |

## Authorization, experiment and preservation

The maintainer explicitly invoked [the retained brief](../implementation-briefs/CODEX_BRIEF_SOR_scoped_ordinary_outpost_beacon_detection.md) and requested suggested commit messages without committing/pushing. Allowed operations: original project-authored offline tooling, existing archive/manifest/definition reads, bounded in-memory decompression, synthetic tests, local receipts and durable documentation. No game launch/load, debugger/SFSE, database mutation, network, installation, source-save modification, staging, commit or push.

Plan: freeze a scoped predicate; apply it to raw decoded records without expected counts, names or network labels; compare six primary outcomes; audit their record/flag positions with separate arithmetic; challenge all frozen corpus identities and inspect alternate/decoy cases; return for review. Expected control outcomes are preregistered in the brief, not detector inputs. Previous results were already known, so this is replication/challenge, not blinded discovery.

Inputs are resolved from the same identity manifests as [SOR-EXP-0009](active-outpost-identification.md#inputs-ground-truth-and-preservation). Only verified ignored archived copies are decoded. Original paths are hashed for integrity only. Existing `membership-completion/challenge-final/preservation.json` supplies archive locators; missing copies abort rather than causing analysis of live originals. SHA-256/size are checked against manifests, bytes are checked on read, and all inputs/tools/manifests are rehashed at run completion. No raw/decompressed save is written. Source/oracle preservation receipts stay local.

Safeguards: physical 128 MiB, decoded 64 MiB, 262,144-byte blocks, C/D free space at least 40,000,000,000 bytes, 128 MiB output/run, 32 MiB per receipt and cooperative 1,800-second run bound. A physical/format/decoded bound becomes SCAN_UNSUPPORTED, never a negative detection; identity/resource guard failures abort. Risks are false interpretation of inherited types, unresolved content mapping and private data disclosure. Stop on identity drift, unsafe space, unsupported framing or essential bounds failure; retain partial evidence and original archives. Cleanup removes nothing and performs no target action.

## Exact predicate and saved-state procedure

Reuse [outpost_membership.py](../../save-analysis/scripts/outpost_membership.py), [outpost_record_framing.py](../../save-analysis/scripts/outpost_record_framing.py) and existing bounded BCPS/directory decoding. The old membership API and its INDETERMINATE classification are retained; an optional diagnostics argument adds record indices/queue locations and known-base reference-only leads. No second binary reader or outside parser is introduced.

An ordinary match requires:

1. Exact R3 count/end closure, a dynamic tag-10 saved reference, and no explicit non-REFR type (`0x4a`–`0x55` admitted; inherited type explicitly conditional).
2. The native conditional initial selector chooses case 5: change bit `0x8000` is clear.
3. The second queued reference resolves to saved base identity `0x002C60E9`, previously identified as Starfield.esm ACTI OutpostBeaconActivator. A direct tag-01 value or valid one-based tag-00 form-array entry is admitted. This is a saved identity before load remapping, not a runtime FormID or pointer.
4. The transform-dependent prefix consumes successfully and its following general-self queue entry equals the record token. A base occurrence elsewhere in the queue is insufficient.

The prefix reads shape byte, three LE float32 values, conditional angle floats and conditional packed byte, then consumes the cell/base/self queue entries separately. If change bit 0 is set, it reads LE uint32 form flags and uint16 auxiliary flags at the exact post-transform body cursor. Mask `0x800` yields EXPLICITLY_CLEAR or EXPLICITLY_SET. If bit 0 is absent, the state is OMITTED; an unsuccessful prefix yields UNRESOLVED. Later unsupported extras do not invalidate an already consumed prefix. Saved flag restoration mask `0x00D12960` and named IsDisabled callback are prior STATIC evidence, not a live invocation. Auxiliary flags are retained without inventing membership semantics. IsDeleted is shelved; no investigation or membership test uses it.

The strongest scoped interpretation is a recognized ordinary beacon with explicit disabled-clear/set evidence. Clear state correlates with active ordinary controls and the mature network; set state correlates with the two retained historical-like references excluded from that network. It does not prove every gameplay removal pathway, player ownership or runtime behavior after load. Historical removal of the two extras remains source-reported, not a new controlled removal experiment.

## Primary comparison and independent checks

| Save / source identifier | Independent gameplay oracle | Ordinary | Clear | Set | Omitted/unresolved ordinary |
|---|---|---:|---:|---:|---:|
| Save3 / SOR-SAMPLE-0001 | Pristine, none constructed | 0 | 0 | 0 | 0 |
| S0 / SOR-SAMPLE-0006 | Operator pre-placement | 0 | 0 | 0 | 0 |
| S0C / SOR-SAMPLE-0007 | No-action control | 0 | 0 | 0 | 0 |
| S1 / SOR-SAMPLE-0008 | Operator placed one ordinary beacon | 1 | 1 | 0 | 0 |
| S1C / SOR-SAMPLE-0009 | No-action control | 1 | 1 | 0 | 0 |
| Save52 / HIST-0267 / SOR-SAMPLE-0029 | 17 manually documented outposts | 19 | 17 | 2 | 0 |

All six comparisons pass without fitting expected totals. Primary physical/decoded hashes are in the per-save ledger. An independent arithmetic R3 walker and separate flag-cursor calculation reproduce all candidate tokens, record bounds and raw flag offsets/values across **309,057 records**. Both routes share physical decompression/directory discovery and native format evidence, so independence is implementation-level, not independent engine semantics.

S1 token `822c5d`, logical record `[1295765,1296100)`, body `1295841`, flags `1295855`: form `0x00400409`, aux `0x0040`. S1C record `[1296371,1296706)`, flags `1296461` agrees. Save52's 17 clear candidates carry `0x00400408` / `0x0040`; the two set candidates carry `0x00400C08` / `0x0041`. [Every token, record range, flag position and zero-based JSON outpost index](ordinary-outpost-beacon-detection/save52-records.csv) is recorded without private names or UUIDs.

The independent oracle is the protected manual network JSON already documented in [SOR-EXP-0006](mature-save-outpost-validation.md#authority-plan-inputs-and-provenance). After detection, the preserved mature extraction associates tokens with names; fresh JSON reading verifies the 17 clear-token names equal its 17 unique outpost names, while both set-token names are absent. Its exact hash is rechecked against the earlier source manifest and before/after identities. This is not merely a total-count comparison. Token/name association uses earlier structural research; JSON is independent gameplay documentation, not engine authority, and its later filename date/capture-history uncertainty remains as previously reported. Neither old `active` labels nor JSON enter the detector.

## Exceptions, challenge and support boundaries

Case-6 template-adjacency leads remain unresolved beacon-like candidates with explicit template/base lead IDs, omitted flags and reconstruction gaps. Known inline faction definitions are categorized exceptional/faction; this route is synthetic-tested. The observed HIST faction leads do not have an inline resolved base, so they remain unresolved rather than being overstated as confirmed faction references. Their installed template definitions are recognized; their saved effective identities and quest-control states remain conditional.

Generic changed references are not emitted wholesale. Only a consumed known inline base, an R1 known-template adjacency, or a queued occurrence resolving to a known beacon base produces an inspectable candidate/lead. Other dynamic records are counted as uncovered in coverage. Known-base reference-only records are unresolved, not ordinary matches; explicit non-REFR decoys are also preserved in the rejection ledger. This makes Save52's QUST base/reference decoy visible without calling it a twentieth ordinary beacon.

Challenge measurements and version-specific coverage are recorded in [saves.csv](ordinary-outpost-beacon-detection/saves.csv) and [versions.csv](ordinary-outpost-beacon-detection/versions.csv). Independent gameplay truth is available only for the controlled labels and mature network; all other truth labels are UNVERIFIED. Earlier window/signature classifications are comparison evidence, never truth labels. No invented false-positive/negative rate follows from correlated historical occurrences.

The fresh challenge completes **412 labels / 389 distinct hashes**, with **409 exact R3 closures / 48,863,625 framed records**. It finds **1,804 ordinary record occurrences: 1,717 explicitly clear and 87 explicitly set**, with no ordinary omitted/unresolved flags in this measured corpus. Counts match the previous inline observations on all comparable labels. There are 204 positive labels, 205 scanner-negative labels and three SCAN_UNSUPPORTED labels: HIST-0252/0256/0257 exceed the 64 MiB decoded bound. Repeated/correlated saves are not independent outposts. All three operator-zero and all 20 operator-one controls reproduce their scoped outcomes; the mature comparison passes separately. The remaining 388 labels have UNVERIFIED gameplay truth, including the three unsupported files.

The **151 unresolved leads** are inspected in two bounded groups. Twenty-one select case 6 with OMITTED saved flags: three each in HIST-0016/0058/0100/0143/0189/0250/0251. Their conditional template links comprise seven each to installed FC/RI/UC bases `03038AC8`/`03038AC9`/`03038ACA` under the prior saved-plugin mapping hypothesis. Their effective saved base is not marked resolved. All other **130 reference-only leads carry token `6a6c44`**, previously associated with QUST SQ_OutpostCargoLink, rather than the dynamic ordinary-beacon representation. Save52's instance is at decoded record start **1980560**. No known inline faction match occurs in this corpus; exceptional/faction output is synthetic-tested, while these real faction-template leads remain unresolved. No quest-status investigation follows.

Seven embedded first-header-version strata frame successfully: 1.7.23.0, 1.12.32.0, 1.12.36.0, 1.14.74.0, 1.15.222.0, 1.16.242.0 and 1.16.244.0. The separately sourced **111 launch-era donor saves** (1.7.23.0) all frame and produce zero ordinary/exceptional/unresolved matches; their gameplay truth remains UNVERIFIED. Zero old-version positives in a stratum do not establish semantic positive coverage or absence. The version ledger distinguishes actual ordinary-positive strata from merely compatible framing. Full-run elapsed time is 666.6 seconds; 700 input/tool/manifest paths, including 667 original/archive save paths, have equal before/after identities.

The known counterexamples survive: empty relationship collections in S1/S2/S7 despite ordinary positives reject a collection-only detector; a known base referenced by a QUST record rejects occurrence-only identification; HIST-0016's alternate case-6 path rejects exhaustive inline enumeration. None contradicts the scoped ordinary predicate. No independently established ordinary false positive or false negative is found in the labelled scope.

The two original versions in headers are recorded as embedded fields, not measured originating executable versions. Current installed loader semantics (Starfield 1.16.244.0, SOR-ENV-0001) are not automatically transferred to older engines. Older saves remain eligible structural observations, with their unknown gameplay truth and missing historical ESM/override snapshots explicit.

Full membership/absence would additionally require inherited type and static/default reference enumeration, complete alternate effective-base mapping, content overrides, omitted-state reconstruction, registration/keyword/parent/ExtraWorkshop filters and an independently validated player-control predicate. Quest-status work remains deferred. NO_RECOGNIZED_ORDINARY_BEACONS is a scanner observation only; no result emits NO_ACTIVE_PLAYER_OUTPOSTS. A parser/resource failure instead emits SCAN_UNSUPPORTED.

## Reproduction and handoff

From the repository, using the installed interpreter and fresh run names:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/detect_ordinary_outpost_beacons.py --run review-primary --labels Save3,S0,S0C,S1,S1C,HIST-0267
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/detect_ordinary_outpost_beacons.py --run review-challenge
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B -m unittest discover -s save-analysis/scripts -p 'test_*.py' -v
```

The default definition catalog is the preserved `membership-completion/definitions-01/definitions.json`; `--definitions` and `--archives` allow explicit existing catalog/locator receipts. Missing manifests or archives are a prerequisite failure. The runner covers registered corpus identities; it is a research instrument, not a general save importer. Labels select inputs only.

Machine-readable `results.json` is a list of `{save_id, sample_id, source_sha256, source_bytes, result}`. `result` includes schema `ordinary-outpost-beacons/1.0`, positive/scanner-negative/unsupported headline, ordinary count, category × saved-state counts, candidates, coverage and separate authoritative membership. Each candidate supplies source references, category confidence/basis, token/base identity, raw flags/mask, decoded offset/index/queue locations and compressed-stream spans. Compression permits stream provenance, not a linear physical record offset. Concrete output example: S1 ordinary=1, EXPLICITLY_CLEAR=1, membership=INDETERMINATE. [Validation and complete file inventory](ordinary-outpost-beacon-detection/validation.md) link the review diffs and actual checks.

Provenance: existing project readers at starting HEAD `4029c5242edc8dde2651260b896d22b31c401744`, paths above, are reused directly; the optional diagnostics addition is documented in the diff. Original project-authored presentation/runner/tests are source-informed by SOR-S-0127/0128 and prior SOR-S-0124 research. Installed Python/stdlib/zlib retains SOR-S-0113 credit; Bethesda supplies local research inputs; TheDailyXPerience donor data retains SOR-S-0125 / SOR-P-0003 local-only restrictions. No external implementation, new dependency, source contact, fork, PR or disclosure. No new static-tool execution was needed.
