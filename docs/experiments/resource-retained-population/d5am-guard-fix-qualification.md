# D5AM 0.9.1 guard composition repair

2026-11-04, Australia/Sydney. OFFLINE ONLY; independent scoped acceptance is recorded in
[the combined review](d5am-n0-repair-review.md).
Authority is the [repair amendment](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_AMENDMENT_SOR_D5AM_guard_repair_2026-11-04.md`).
The failed N0 episode, original 0.9.0 package, prediction and source locks remain
historical. This repair does not authorize another deployment or live run.

| Question | Current answer |
| --- | --- |
| REPAIR-Q1 | The original geometry target hash is preserved while only the exact documented installed causal patch is accepted. The frozen native positive and adverse controls PASS; REPAIR-Q1 is independently COMPLETE at the offline scope. |
| REPAIR-Q2 | Offline engineering checks PASS: full 157-case regression, exact-object ABI, reader replay and byte reproduction. REPAIR-Q2 is independently COMPLETE at the offline package qualification scope. |
| Coverage | Pinned Starfield 1.16.244.0 instruction/guard domains and explicitly owned native fixture pages. Retail startup of 0.9.1 is NOT TESTED. |

## Root cause and counterexample

Retail geometry CALL RVA `0x21e09ed` resolves to shared helper RVA `0x22cc350`.
Its independently pinned original first-32-byte hash is
`b63e0cf10f62d69305ffc0859b6ef445f43549fa2ae10224ab1634b16c2bbbd0`.
Causal site 3 at RVA `0x22cc366` replaces nine bytes beginning at helper offset `0x16`.
The original installer configures both against original bytes, installs causal
patches, then runs the geometry worker guard. That guard previously compared
modified RAM directly with the original target hash. N0's `geometry_guard`
failure before READY is a decisive coverage counterexample to the former
offline composition qualification. It is not evidence about construction
winner selection or the immutable prediction.

The old fixture guarded `d5ai_native_acquire`, whereas its new causal bridge
used a separate copied original helper. Both components could pass without
testing the retail alias. The repair fixture instead creates an actual native
CALL to the same private original helper patched by causal site 3. Its geometry
wrapper, original shared acquisition and causal bridge execute together.

## Implementation and guard boundaries

The new `d5am_guard_build.py` and `d5am_guard_package.py` adapt the retained owned
D5AM builder/package methods under SOR-P-0002. The new geometry header derives
from the owned `d5ai_geometry.h`; the original source files remain untouched.
The build authenticates and copies the same retained build16 sources, approved
support/notices and pinned executable, then derives a separate 0.9.1 tree.
It copies the new geometry header to that tree's expected include name.
These are source-informed owned adaptations, not independent clean-room work.

| Preserved owned method basis | SHA-256 |
| --- | --- |
| `research/resource-retained-population/d5am_candidate_build.py` | `055809a928fd4eef6129d913b4a211663639e6b42385f6414b6a79496498c7c2` |
| `research/resource-retained-population/d5am_candidate_package.py` | `020ba617ffbcb0470e6a5f546888fbcffdf3290991dd43579a69496169a19de2` |
| `runtime/construction-winner/d5ai_geometry.h`, identical to retained build16 header | `15ab107dc71beda6b35c7534618a4cf86b759d0db149de1decff066bc42c5349` |
| `runtime/construction-winner/d5am_fixture.inc`, copied then adapted only in the fresh derivative | `434e35adcddde0237356906e79d7e6b93807530bbdf1ba6c4a3017570fbc0fe3` |

The retained build16 manifest remains
`15d10475806aeb593ac7236a48ea1b71f8e3614bf8cdd7e1ded830b0fcdbf457`;
the installed executable remains
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
The primary independently preserves all 299 old operational source-lock inputs.


Initial `configure_acquire` still validates the exact original CALL window and
original 32-byte target hash before installation. The new runtime verifier permits
only causal site 3, at the recorded reader helper offset `0x16`, with length 9
bytes. It requires
the full exact installed patch and the existing causal guards, including the
relay-page hash, all site windows and all three original full helper bodies
reconstructed using only known edits. It then restores only those nine bytes
in a local copy and compares the original geometry 32-byte target hash. Unknown
changes in the overlap, outside it, or in the relay remain failures. No RAM
baseline is learned, no target guard is removed and no arbitrary modified hash
is accepted. Geometry's own exact CALL and relay checks remain active.

The builder enumerates all 55 installed patch spans against all 76 original
guard domains, including core targets, geometry target, scheduler targets,
callback, vtables and full causal helper bodies. Existing causal-window
overlays handle core/site and geometry/site intersections. The only raw target
guard overlap is the documented geometry target with causal site 3. The census
is static interval evidence, separate from the actual native controls. Its 76
domains include initial 32-byte site windows: core and geometry do not retain
all those tail bytes as persistent runtime guards. Their exact installed spans
and relays remain guarded. The 70 interval intersections include two extra
initial-only cross-family windows (core site 2 with causal site 9; geometry site
2 with causal site 8), the three persistent causal-window intersections below,
and seven full causal-helper intersections.

| Persistent guard | Intersecting installed edit | Existing handling |
| --- | --- | --- |
| Causal window 6, RVA `0x79fc85`, 32 bytes | Core site 2 at RVA `0x79fca3`; two bytes intersect. | Exact known overlay in causal guard. |
| Causal window 8, RVA `0x21e0a87`, 32 bytes | Geometry completion at RVA `0x21e0aa5`; two bytes intersect. | Exact known overlay in causal guard. |
| Causal window 9, RVA `0x79fcb3`, 32 bytes | Core site 3 at RVA `0x79fccb`; five bytes intersect. | Exact known overlay in causal guard. |
| Geometry target, RVA `0x22cc350`, 32 bytes | Causal site 3 at RVA `0x22cc366`; nine bytes intersect. | New exact composition verifier. |

No core target, scheduler target, vtable or command-callback guard overlaps an
installed patch. All original configuration guards execute before installation;
no initial-only intersection authorizes accepting changed original bytes.

The worker now repeats the existing causal verification while checking this
geometry alias: another relay-page hash, sixteen site-window checks and three
full-helper checks per valid guard pass. This is additional observer CPU/memory
work; no microsecond bound or uninstrumented scheduling equivalence is claimed.
No new native hook is added.

The native helper instructions, bridge ASM, admission/STOP protocol, causal
128-byte wire schema and scheduler 272-byte wire schema are unchanged. The new
geometry metadata states
`geometry_target_guard_basis=original32-exact-causal-overlap/1`.
The fixture's initial helper import displacements still use the declared owned
wait/wake substitutions; these are not retail scheduling measurements.

## Controls and preserved failures

Before installation, every new control rejects a wrong supplied target hash,
executes the uninstalled original shared CALL, and rejects a corrupted original
target before successful configuration. The positive installed case executes the actual
geometry CALL wrapper and shared helper, then the typed reader release. Adverse
cases corrupt the overlap, an untouched helper byte, the causal relay, restore
an original first patch byte, or corrupt the remembered `Patch.before` byte
while leaving native code intact. The actual ordinary worker must refuse
the changed producer and persist a protective terminal. Geometry capture is
unarmed in this alias control; full armed geometry/lifetime behavior belongs to
the unchanged complete legacy regression roster.

- `guard-dev01`: two fixture exits of 91. The test incorrectly called the new
  installed-only verifier before installation; preserved and corrected.
- `guard-dev02`: five new controls exit 0; the preimage control exits with code 91 because
  a deliberately failing late configure changed its target state before the
  restoration assertion. The production verifier was not the failed assertion.
  Its source-preservation gate also FAILS because fixture development continued
  during this development run.
- `guard-dev03`: all six controls exit 0; source-preservation FAIL because the
  builder census was completed during the development run. It is not promoted.
- `guard-final01`: all 157 expected exits PASS and `source_unchanged=true`, DLL
  `e20abfb622b2698ad35e64d79b0e0e9f85a38723088bba1ca87eb0af5a332ba6`.
  This milestone still duplicated the outside-byte corruption in its preimage
  case. It is retained rather than promoted after the distinct metadata
  adversary was requested. Its exact-object ABI passes 3,905 checks, 160 unwind
  contexts and ten bridges in `guard-abi01/qualification.json`.
- `guard-final02`: all 157 expected exits PASS, compilation succeeds and
  `source_unchanged=true`. It includes the distinct remembered-preimage control
  and explicit pre-install disabled/before checks. The six final repair source
  hashes are in `guard-final02-source.json`. No source edit followed that freeze.

## Applied reading, effects and safety

The current AGENTS, README, WORKFLOW, third-party policy, charter, evidence
standard and completion protocol were recovered for this repair, alongside the
original D5AM brief, N0 amendment, frozen run card and new repair amendment.
Previously completed relevant native/scheduler/owner-census reading remains
recorded in `native-specialist-handoff23b.json`; this repair changes guard
composition rather than causal semantics. The evidence standard requires
preserving N0's guard-composition counterexample and distinguishing checksums
from semantics.
The completion protocol requires correction and full retesting rather than a
diagnosis-only return. The repair amendment requires fresh named sources and a
new package: no existing operational lock input is edited while the primary
finishes protected N0 postflight/archive. SOR-P-0002 permits these owned method
adaptations; unchanged embedded SFSE notices remain mandatory.

Only fresh local derivative/build/session/receipt/ZIP outputs and new authored
repair files are written. Pinned MSVC/MASM and owned disposable hosts execute;
the existing 40,000,000,000-byte C:/D: floors remain. No game, debugger, Ghidra,
deployment, save/configuration write, network, Git staging, commit or push is
performed. Old authority/prediction/measurement manifests do not admit 0.9.1;
any future retail trial needs a new reviewed exact binding and separate GO.


## Frozen engineering handoff

| Artifact | Actual result |
| --- | --- |
| `.local-work/d5am/guard-final02/build.json` | All original 151 cases plus six new alias/guard controls meet their expected exits; frozen source unchanged. |
| `.local-work/d5am/guard-abi02/qualification.json` | PASS: 3,905 ABI checks, 160 unwind contexts, ten bridges; exact final object `5b90714d99bf0a1803b58926c0ed95a00a905d88e1ca087cd730adee878cdd91`; sources unchanged. |
| `.local-work/d5am/guard-replay02/qualification.json` | PASS: six actual new READY/guard/terminal/reader controls with exact producer binding and input preservation. |
| `.local-work/d5am/guard-replay02/native-replay/qualification.json` | PASS: 111 native/STOP/invalid-operand and adverse identity/join checks; complete owned geometry and one exact native task/core join retained. |
| `.local-work/d5am/guard-optimization02.json` | PASS: 32 entrypoints, 96 optimization refusals including inherited `PYTHONOPTIMIZE=1` with `-E -B`; sources unchanged. |
| `.local-work/d5am/package-guard-final02/package.json` | A fresh MSVC/MASM rebuild from frozen exact sources produces a byte-identical DLL; fresh ZIP round-trip and source checks PASS. |

The final DLL is `1596f2cffff18dd91bd18fb755076fb8740c757241cb7c81c33ffa3a3d672754`.
The separately named archive is
`.local-work/d5am/package-guard-final02/SorConstructionWinner-0.9.1-D5AM-guard-final02-NOT-AUTHORIZED.zip`,
SHA-256 `816274053c800cd3de724bebafe5df7acfa46b0b41e87d39021ff5fbc0290a07`.
It remains local and has no publication clearance.

| New native case | READY before fault | Actual terminal | Independent reader disposition |
| --- | --- | --- | --- |
| `d5am-guard-alias` | Yes. | Healthy, `output_fault=none`, resident inert. | Native accounting complete; seven authenticated causal events and one scheduler event. |
| `d5am-guard-overlap` | Yes. | Failed, `causal_or_scheduler_guard`, resident inert. | Seven causal frames authenticate; full/native completeness refused for `CORE_OUTPUT_FAILURE`. |
| `d5am-guard-outside` | Yes. | Failed, `causal_or_scheduler_guard`, resident inert. | Same explicit protective refusal. |
| `d5am-guard-relay` | Yes. | Failed, `causal_or_scheduler_guard`, resident inert. | Same explicit protective refusal. |
| `d5am-guard-preimage` | Yes. | Failed, `geometry_guard`, resident inert; original helper/code guards remain healthy. | Same explicit protective refusal; no corrupt frame is invented. |
| `d5am-guard-patch` | Yes. | Failed, `causal_or_scheduler_guard`, resident inert. | Same explicit protective refusal. |

Every new terminal has zero native bridge-active count. These negative tests
prove protective refusal, not successful scientific capture after corruption.
The alias snapshot is unarmed; the full original armed geometry/lifetime and
native construction/STOP checks are separate, retained positive controls. No
fixture proves ordinary retail scheduling or 0.9.1 retail startup. The failed
N0 startup remains unchanged; the prediction has no new sample and no new
binding to 0.9.1. The primary owns integration and verified complete/task-only
delivery exports; the non-implementing reviewer supplies independent acceptance.
