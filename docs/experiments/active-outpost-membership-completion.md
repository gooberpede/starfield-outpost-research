# SOR-EXP-0010 — Alternate beacon identity and conservative membership prototype

2026-10-09. SOR-EV-0016 / SOR-F-0015 / SOR-ST-0018 / SOR-H-0007.
Scope: the [invoked brief](../implementation-briefs/CODEX_RESEARCH_BRIEF_active_outpost_membership_completion.md), with the maintainer's subsequent faction-quest explanation and request to defer the quest-status edge case. Offline work only; critical review pending. This is material progress and a bounded partial implementation. It does **not** establish complete active-player classification or claim that further offline analysis is impossible.

## Result and decisive distinctions

The new [prototype](../../save-analysis/scripts/outpost_membership.py) separates base identity, initial-data restoration, saved disabled state, extra-data interpretation and active-player membership. It supports conditional REFR initial cases 4, 5, 6 and 7, reports omitted form flags as unknown, and returns `INDETERMINATE` when enumeration/ownership is incomplete. Its three-result interface includes `OUTPOSTS_PRESENT` and `NO_ACTIVE_OUTPOSTS`, but neither is emitted by this partial implementation. Candidate counts are diagnostic evidence, not active counts. No filename, outpost name, expected count, JSON network or quest-completion label is an input to classification.

The existing controls reproduce the important distinction: Save3/S0/S0C have no inline beacon candidates; S1/S1C have one, with saved IsDisabled clear. Save52/HIST-0267 has 19 inline candidates: 17 disabled-clear and two disabled-set. Its independent operator/JSON count of 17 is comparison evidence only. That agreement is preserved; it does not establish player ownership for arbitrary beacons. [Fresh measurements and exact input hashes](active-outpost-membership-completion/manifest.csv) include every challenge label; [selected record ledger](active-outpost-membership-completion/records.csv) supplies decoded offsets, cases and flags.

Milestone A remains **partial**: zero/one diagnostic separation succeeds, but the active-player semantics are not independently proven. B is **unachieved**: an empty candidate set cannot establish absence. C supplies a fresh bounded corpus challenge, with unsupported files and unknown ground truth visible. Previously known aggregate results and HIST-0016 were already familiar; this is not a fully blinded experiment. New features are frozen before the old per-file comparison, and old heuristic labels are never treated as independent ground truth.

The full challenge has 412 labels / 389 distinct physical hashes, 409 exact R3 closures / 48,863,625 records, and three resource exclusions (HIST-0252/0256/0257). It reports 1,825 candidates/leads: 1,804 inline case5 (1,717 disabled-clear / 87 disabled-set) and 21 case6 leads with omitted flags. The latter occur three each in HIST-0016/0058/0100/0143/0189/0250/0251. These are correlated record occurrences, not 1,825 independent outposts. The old inline counts agree on all 409 comparable labels; the 21 additional leads expose the old representation gap rather than prove 21 active false negatives. Three operator-zero labels, 20 operator-one labels and one mature network label are available; the other 388 labels lack independent active-player ground truth. All 412 semantic predictions abstain as INDETERMINATE, so there is no measured semantic true/false-positive rate. Detection-only controls have zero spurious inline candidates on the three known negatives and reproduce one on all 20 known one-outpost controls.

## HIST-0016: a specific alternate path, rather than a missing inline record

All native addresses here are preferred static VAs in pinned Starfield 1.16.244.0, image base `0x140000000`, executable SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. They are not runtime pointers. All save offsets are offsets in the fully decoded logical byte stream, not physical `.sfs` offsets.

The selector `0x141832f00`, paired readers `0x141835610` / `0x141835c20`, and form loader `0x1405dfa40` establish this conditional REFR interpretation:

| Initial case | Queue consumption before general self reference | Body fields | Observed/tested scope |
|---|---|---|---|
| 5 | cell, inline base | transform shape/XYZ, conditional angles/packed byte | Existing controls and mature vanilla beacons |
| 6 | cell, placement parent | same transform, then two signed 16-bit placement indices | Three HIST-0016 alternate candidates |
| 4 | cell | transform | Synthetic regression; no claimed beacon example |
| 7 | initial reference | no transform in this initial reader | Synthetic regression; no claimed beacon example |

For dynamic tag-10 references the selector chooses 5 when change bit `0x8000` is clear; otherwise `flags & 0x02000008` chooses 6, then `flags & 6` chooses 4, otherwise 7. This decision presumes a REFR-family form type; it does not resolve an inherited type by itself. Earlier speculation that HIST-0016 uses case 7 is rejected: its `0x92018200` selects **case 6**. General self-reference consumption is separate from the base position.

| Saved token | R3 record start/end | Body start | Conditional R1 association offset | Template token → array value | Installed template/base lead |
|---|---|---|---|---|---|
| `82c210` | 3875017 / 3875436 | 3875107 | 744978 | `10f467` → `0302B256` | UC REFR `0202B256` → ACTI `02038ACA` |
| `8163c8` | 3294780 / 3295199 | 3294870 | 620088 | `10f45c` → `0302B254` | FC REFR `0202B254` → ACTI `02038AC8` |
| `81be60` | 3448919 / 3449359 | 3449018 | 465210 | `10f46e` → `0302B255` | RI REFR `0202B255` → ACTI `02038AC9` |

Each adjacent pair is found in R1, independently of names. The template-token form-array mappings and installed ESM NAME relationships are observed bytes; interpreting adjacency as a complete created-reference/template map remains **INFERRED**, because the enclosing R1 grammar has not been reconstructed. Conditional full-plugin slot 3 accounts for the difference between installed ESM self-slot 2 and saved slot 3. The prototype records the regex-observed plugin sequence explicitly as a conditional hypothesis, not a full plugin-table/load-remapping implementation. Dynamic save token `82c210` is also not interchangeable with an engine-assigned loaded FormID.

The three saved names corroborate the faction identities, but are not classifier inputs or ownership evidence. Their record change flags omit bit 0, so **saved IsDisabled and IsDeleted are both UNKNOWN**, not clear. The initial reader's placement-parent queue does not contain an inline base. These facts explain why the old type-5 detector missed these records without establishing that they are active player outposts.

## Installed definitions and ownership challenge

The original [ESM reader](../../save-analysis/scripts/inspect_outpost_definitions.py) performs two complete header/group walks of each selected file and bounded subrecord decoding. It independently observes:

| File | ACTI / EDID | ACTI file offset | Template REFR / file offset |
|---|---|---|---|
| Starfield.esm | `002C60E9` / OutpostBeaconActivator | 3761304 | `0029A8C8` / 139749949 |
| SFBGS050.esm | `02038AC8` / OutpostBeaconActivatorFC | 283947 | `0202B254` / 89302225 |
| SFBGS050.esm | `02038AC9` / OutpostBeaconActivatorRI | 285202 | `0202B255` / 89334099 |
| SFBGS050.esm | `02038ACA` / OutpostBeaconActivatorUC | 286457 | `0202B256` / 89361083 |

All four have the same 19 observed KWDA entries, including prior WorkshopKeyword `00054BA7`; all four selected templates lack an explicit XOWN subrecord. The missing XOWN is **not** proof of player ownership or no inherited ownership. An EDID-prefix selection is a discovery scope, not an exhaustive scan of every keyword-bearing ACTI, every plugin override or every historical content version. Two current installed ESMs cannot certify save-era content equivalence. Definition hashes and offsets are in [the definition ledger](active-outpost-membership-completion/definitions.csv).

**SOURCE-REPORTED, maintainer, this conversation:** each faction outpost belongs to a short Terran Armada quest, and handing it in removes player control. The maintainer cannot independently label HIST-0016's hand-in status and subsequently asks to defer resolving quest state within saves as disproportionate edge-case work. This correction is retained under SOR-D-0026. It supplies a concrete ownership discriminator and rejects assuming that a faction beacon's presence means continued player control. It does not independently prove a particular HIST-0016 quest stage, disable bit, deletion bit or registry state.

Focused installed QUST inspection identifies self-domain `02028235` / SFTER_MQOutpostUC, `02028236` / SFTER_MQOutpostFC, and `02028237` / SFTER_MQOutpostRI at ESM offsets 101949805, 101958322 and 101966785. With HIST-0016's conditional full-plugin mapping, these would be `03028235`–`03028237`; loaded runtime identities remain separate. Their VMAD bytes associate SFTER_MQOutpostScript, beacon aliases, faction properties and the fragment property BlockPlayerActivation. A bounded local BA2 directory walk locates the matching PEX files. PEX string tables contain AddKeyword, GetRef, beacon alias and BlockPlayerActivation-variable identifiers; byte sequences are consistent with GetRef followed by AddKeyword on the alias using that variable. This is a **source-informed lead**, not a validated full bytecode/control-flow decoder or stage-to-player-control proof. The attempted general VMAD property walk stopped on unsupported property type 17; that failure is retained and is not a negative result. Quest-stage save decoding was not started after the maintainer's deferral.

## Saved flags, extra data and runtime predicates

Saved form flags are read only when change bit 0 is present, after the case-dependent transform and general self queue pop. Named IsDisabled uses `0x800`; named IsDeleted uses `0x20`. Restoration masks and auxiliary semantics remain scoped to the pinned loader. When a flag is omitted, existing/default/template/load state must be reconstructed before assigning its final value. A clear saved disabled flag is an observed state input, not complete proof of continued player control after quests or load.

**IsDeleted is shelved for active classification.** It is reported incidentally where decoded; the suggestive name and gameplay removal are insufficient evidence. No discovered candidate with an actually decoded set IsDeleted bit was observed in this challenge. Omitted fields and unsupported representations remain unknown, so this does not assert that no outpost anywhere has the bit set. No beacon deletion experiment or outpost-specific deleted-bit search was performed. The earlier proposal in SOR-EXP-0009 is historical, not the current recommendation.

Further read-only native inspection distinguishes:

- ExtraOwnership is type `0x1f`, reader `0x14053a2d0`; `0x21` is ExtraRank. The S1 record body contains no byte `0x1f`, which excludes an explicit type-1f dispatch in that body, **not** inherited/template/faction ownership.
- ExtraPromotedRef is type `0x84`, reader `0x14054c2f0`, confirmed against its vtable. Its counted reference/byte pairs can contain player reference `00000014`. That occurrence is **promotion-related**, not an ownership field. Treating the player reference as owner is rejected.
- ExtraFlags `0x9c`, reader `0x140545e40`, has a buffer-version gate. The prototype refuses its payload when buffer version is unknown or in `0x42`–`0x59`; it does not silently apply the modern uint32 layout across all saves.
- Readers `0x140547c90` / `0x14054b4b0` support only the empty-array cases for extras `0x4c` / `0x80` in this prototype. Nonempty cases stop with reason codes. Extra `0xda`, reader `0x140a23de0`, includes queued identities and version-dependent fields; it is not skipped by guessing a fixed size.
- ExtraWorkshop `0xbc` is recognized only at a correctly reached dispatch boundary. Its versioned contents are not fully decoded. A byte search for `bc` cannot supply that boundary. Thus leading unsupported extras can prevent even a workshop-presence observation.

The prior [Almanac/registration trace](active-outpost-identification.md#independent-native-membership-route-and-exact-obstruction) is preserved. Fresh inspection of `0x140f3bfc0` confirms that its exclusion query uses a property/keyword interface at reference `+0x68` with global `0x145f0c6d0`. Neither that global's resolved FormID nor equivalence to BlockPlayerActivation is established. This should not be silently rewritten as the ordinary base keyword test. The registry's auxiliary-bit/parent/base/keyword predicates and ExtraWorkshop restoration are stronger leads than beacon presence, but are not a complete offline player-membership predicate.

The corpus extra walk stops at unknown ExtraFlags buffer version on all 1,804 inline candidates, and at a nonempty extra0x80 payload on all 21 alternate leads. This is measured unsupported coverage, not an assertion that ExtraWorkshop is absent. In HIST-0016, the promoted-reference tokens `10f47e/10f47f/10f47d` map conditionally to faction actor quests `0309E247/0309E246/0309E248`, providing another association lead without player ownership proof.

## Completeness obligation and precise remaining dependency

A justified negative needs enumeration of all load-reconstructed qualifying placed references, with inherited form types, created/static template identities, content overrides, current disabled/auxiliary state, extra-data/keyword/property restoration and registration filters resolved. R3 byte closure alone does not supply that set. The two inspected ESMs and a partially reconstructed R1 association cannot exclude omitted default/static references or other beacon definitions.

HIST-0016 makes two gaps concrete: case-6 omits both inline base and saved flags, and the faction quest can change player control while beacon identity remains meaningful. The prototype exposes both gaps instead of erasing candidates or assigning false flags. Existing labelled zero/one controls do not discriminate promotion, enabled state, auxiliary registration suppression and player control; Save52 corroborates the disabled split but does not label faction quest hand-in states.

This is **not an information-theoretic impossibility result**. Further authorized offline analysis could reconstruct R1, extra-data and the quest/property path; it has not been exhausted. The user has deferred the quest-status edge case, so it would be inaccurate to claim the original brief's strict outcome (i), or an unconditional proof that every offline method fails under outcome (ii). The result is an explicitly scoped partial handoff with new alternate-identity evidence, tested failure behavior and an identified causal lead. No scientific confidence promotion to complete membership or absence is proposed.

The single smallest additional **data** item to revisit that semantic gap would be an already existing, protected, independently labelled pre-hand-in/post-hand-in save pair for one of `SFTER_MQOutpostUC/FC/RI`, confirming player control at each checkpoint. Prefer existing archives; no new live work is requested or authorized here. That pair would distinguish continued beacon presence from control loss and focus decoding on the exact restored property/quest change. It would not alone prove universal absence. Until the maintainer elects to revisit the deferred edge case, retain `INDETERMINATE` and continue no automatic live experiment.

## Reproduction and review

Run the installed Python from the repository; use fresh output names:

```powershell
python -B save-analysis/scripts/test_outpost_membership.py
python -B save-analysis/scripts/test_outpost_record_framing.py
python -B save-analysis/scripts/inspect_outpost_definitions.py --run definitions-new --data 'C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data'
python -B save-analysis/scripts/challenge_outpost_membership.py --run challenge-new --definitions .local-work/membership-completion/definitions-new/definitions.json
```

The runner locates existing identity manifests and verified ignored copies by SHA-256. Missing historical copies are archived once by hash; originals are read only for copying/integrity. Physical ≤128 MiB, decoded ≤64 MiB, and ≥40,000,000,000-byte C/D free-space guards apply; the final runner has a cooperative 1800-second bound. Decoded bytes stay in memory. Full private receipts, script/definition/tool identities, input before/after checks and native exports remain ignored/local.

[Actual validation, failures, changed-file inventory and complete review diff](active-outpost-membership-completion/validation.md) are part of this handoff. Sources SOR-S-0127/0128, previous project methods SOR-S-0124, Python/stdlib SOR-S-0113, installed Ghidra/JDK and donor SOR-S-0125 / SOR-P-0003 are credited. No third-party implementation/dependency, outside consultation/contact, fork, PR or disclosure. Raw proprietary material and donor saves remain LOCAL-ONLY; authored ledgers and source-informed implementation remain REVIEW-REQUIRED. No staging, commit, push or publication; await critical review.
