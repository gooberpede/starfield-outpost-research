# P3 candidate provenance and reproduction

2026-11-01, Australia/Sydney. Offline P3 only; D5AB INCOMPLETE / REWORK,
D5R OPEN and P4/B2 NOT AUTHORIZED. The [active ledger](d5ab-p3-investigation-ledger.md)
preserves the original contract, source freezes, failures and corrections.
Final qualification and independent review remain separate requirements.

## Input and rights boundaries

Admission HEAD is `1578d69baf7a1b2d047629b1fba162c8ae505b13`; index SHA-256 is
`a2cee965e6ec8e0bca03d46441438a1ec7016560ef0d70269697b6f794f44976`.
The only prior working-tree input was the supplied untracked P3 brief, SHA-256
`c339869fff9b32f0dccb34099821c2054d01675dad55f0a9e6c2504ef159faf9`.
The baseline receipt is `.local-work/d5ab/p3/baseline.json`. No staging, commit,
push, remote change, publication or live operation is authorized.

The pinned executable is Starfield 1.16.244.0, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Preferred static VAs use image base `0x140000000`; RVAs subtract that base.
Disposable relocated DLL/host addresses and runtime pointers are separate domains.
Installed EXE/ESM/PlanetData/SFSE/loader and fifteen existing analysis-database
pins are checked against the retained identity receipt. Original P1 exports and
the 826-entry historical preservation inventory remain immutable. These offline
checks are not a new retail protected-save preflight.

Builds use existing MSVC/MASM 14.51.36231, compiler 19.51.36256.0, Windows SDK and
explicit installed CPython 3.14. Exact commands, source snapshots, guards,
compiler diagnostics and output hashes are retained by each build. No dependency
is downloaded. Existing owned P1/P2/D5Q/S/V/Z/X, PE-reader, queue, protection,
consumer and review-export methods are reused under SOR-P-0002. The unchanged
approved SFSE PluginAPI header and MIT notices retain their D5X permission basis.
[Sources](../../SOURCES.md#d5ab-p3-native-integration-qualification) and
[credits](../../../CREDITS.md) record Microsoft's read-only ABI documentation
consultation; no external implementation or new licence acceptance is introduced.

Read-only post-test host provenance records Windows 10 Home 22H2, OS build
19045.6466, 64-bit process and loaded System32 `ntdll.dll` file version
10.0.19041.4842, SHA-256
`36b1a62e4bf6bf7d68458fff6e8a33b39f6527ec6a46e55ecdd12cde83894c8d`.
The two independent local receipts are `p3/platform.json` and
`p3/unwind-platform01.json`. This identifies the observed host implementation;
it is neither an admission-time OS pin nor universal Windows/memory-integrity
validation. No OS setting or binary is modified.

## Candidate and compatibility rules

The final candidate recipe uses `.local-work/d5x/p3-native-final04` and same-input
`.local-work/d5x/p3-repro02`. Provenance02 verifies DLL identity
`9d2f0bab159f3ec23186426fb4833eb645578d2a43612bb2e8def6b1af455dcc`.
The source remains schema `sor-d5x/4`, with eighteen sites, seventeen event kinds,
312-byte payloads and 16-byte frame headers. The visited site's guarded window
changes from nine to thirteen bytes. Five inline bridges now use CALL-entered
RBP frames; the erase trampoline has registered unwind information and a pinned
register tail transfer. The final source hashes, not schema number alone,
identify this revision. Existing guard/image pins are never transferred to a
different executable.

Schema 4 tightens empty-reset, publication, complete-selection and native-return
checks. It separates byte authentication from sampled loss metadata: a bad tuple
can deny session/scientific qualification while later authenticated durable
bytes remain recoverable. `candidate_chains` preserves conditional partial
evidence. `reset_scoped_chains` exposes a complete later reset-to-store witness
when loss bounds, fresh lifetime and intervening history suffice. Whole-session
losslessness and retail source/firstness qualification remain separate; the
retail flags stay false. Evidence-state contradictions concern a proposed join,
not an unobserved engine outcome. No old receipt is rewritten or retroactively
upgraded. Full schema-2 B1 and accepted schema-3 result equality is required.

## Reproduction commands and receipt inventory

Use `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe -B`, without
`-O`, followed by the script and arguments below. Every output label must be
fresh. The retained labels identify historical runs, not permission to overwrite.
The [verification driver](../../../research/resource-retained-population/d5ab_p3_provenance.py)
reads `.local-work/d5ab/p3/final-plan.json`; its selected metadata is delivered in
`d5ab-p3-test-results.json` after successful verification.

| Operation | Script / arguments | Expected retained receipt |
|---|---|---|
| Full compiled producer | `runtime/construction-winner/build.py p3-native-final04` | Final04 `build.json`; all 90 current cases. |
| Reproducible DLL | `runtime/construction-winner/build.py p3-repro02 normal p3-positive-bypass p3-unwind-probe p3-store-access-fault` | Repro02 `build.json`; four controls and identical DLL. |
| Independent native oracle | `research/resource-retained-population/d5ab_p3_native_qualify.py .local-work/d5x/p3-native-final04 .local-work/d5ab/p3-native-controls-final02` | 257 native checks, including 226 required unwind contexts. |
| Exact bridge-object ABI | `research/resource-retained-population/d5ab_p3_bridge_abi.py .local-work/d5x/p3-native-final04 .local-work/d5ab/p3-bridge-abi03` | Thirteen checks against exact final `bridges.obj`; separate clobber-stub caller. |
| P1 full compatibility | `research/resource-retained-population/d5ab_p1_qualify.py .local-work/d5x/p3-native-final04 .local-work/d5ab/p3-reader-legacy-final02 --original-case-regressions` | 316 checks; all original 66 native cases and historical schema-2/3 comparisons. |
| New consumer counterexamples | `research/resource-retained-population/d5ab_p3_reader.py .local-work/d5x/p3-native-final04 .local-work/d5ab/p3-reader-final02` | 133 checks with exact packaged consumers. |
| Actual worker/controller | `research/resource-retained-population/d5ab_p2_controller.py --parallel .local-work/d5x/p3-native-final04 p3-controller-final02` | 26 actual-worker cases and child receipts. |
| Windows file sharing | `research/resource-retained-population/d5ab_p2_file_sharing.py .local-work/d5x/p3-native-final04 p3-sharing-final02` | Held DELETE-access command publication; old error 32 and final interoperability. |
| Complete-producer capacities | `research/resource-retained-population/d5ab_p3_capacity.py .local-work/d5x/p3-native-final04 p3-capacity-final02` | Nine scenario/capacity combinations with independent offer totals. |
| Independent frame/ACK audit | `research/resource-retained-population/d5ab_p3_transport_audit.py .local-work/d5x/p3-native-final04 .local-work/d5ab/p3-transport-audit02` | All 88 recorded sessions, CRC/sequence/prefix/terminal/phase accounting. |
| Queue admission oracle | `research/resource-retained-population/d5ab_queue.py .local-work/d5ab/p3-queue01 8000` | Nine runs, three capacities/repeats; unchanged production queue source. |
| Original native instructions | `research/resource-retained-population/d5ab_p1_native_controls.py .local-work/d5ab/p3-original-instructions01` | Eleven constructor/cell-cleanup controls. |
| Legacy semantic oracles | `research/resource-retained-population/d5ab_p1_legacy_semantics.py .local-work/d5x/p2-native06 .local-work/d5ab/p3-legacy-semantics02` | 54 unchanged explicit schema-3 semantic oracles with final consumer pins. |
| Own-thread worker lease | `runtime/construction-winner/worker_health.py --qualify .local-work/d5ab/p3-worker-legacy01` | Nine legacy identity/death controls. |
| Disposable protection parity | `research/resource-retained-population/d5ab_p3_protection.py .local-work/d5ab/p3-protection03` | Sixteen tests using disposable bytes and existing policy/guard functions. |
| Native query join | `research/resource-retained-population/d5ab_p3_query_join.py .local-work/d5ab/p3-query-join02` | Twenty-three exact retained instruction facts and address-domain arithmetic. |
| Combined verification | `research/resource-retained-population/d5ab_p3_provenance.py .local-work/d5ab/p3/final-plan.json .local-work/d5ab/p3-provenance02` | All final components, receipts, six explicit unchanged production contracts, original exports and preservation pins. |

The private erase-tail proof at `.local-work/d5ab/p3/erase-tail-proof.json` binds
the exact eight original bytes at preferred VA `0x140975038`, their guard and
source method. Incoming RAX is defined before use, justifying the trampoline's
register tail. Raw instruction bytes and generated caller/native exports remain
local-only. Same-input reproducibility means identical DLL bytes and package
member content; ZIP metadata/timestamps are not claimed byte-identical.

## Preserved development and failures

Dev01–04 retain their exact sources/results, including Dev01 overlap, Dev03's
failed erase-tail unwind and the successful Dev04 correction. ABI01's linker
failure came from a fixture C++ object overwriting the same-named assembly object;
ABI02 uses distinct filenames and executes the intended code. Final01/02 have
90 expected exits but source/package overlap and are not final correspondence
proof. Final03 is valid for its own exact 90-case/257-check/132-consumer version;
the later cause-sum prefix counterexample requires Final04 consumer requalification.
Its original 88-session audit observes a real sampled-generation inconsistency
under overloaded STOP while all 65,553 admitted frames remain authenticated.
The synthetic cause-sum variant exposed early prefix truncation; Development12
fixes that limitation while retaining strict scientific refusals. None of these
histories is edited into a later PASS.

Provenance01's unchanged-component filter used slash-separated names against a
Windows-backslash baseline and returned an empty mapping. The independent
reviewer caught that vacuous supplemental check. Provenance02 normalizes names,
requires the exact six nonempty unchanged contracts and verifies every hash.
It also replaces misleading zero test counts with explicit count/unit metadata
for controls, audited sessions and static facts. The original receipt remains
unchanged; no native rebuild or experimental rerun is needed for this verifier fix.

Both-drive 40,000,000,000-byte guards remain in experiments. Binaries, objects,
packages, raw captures, native exports, protected inputs and bulk/private receipts
are LOCAL-ONLY. Authored code/synthesis/selected metadata are REVIEW-REQUIRED,
not publication-cleared. Final patches, inclusion/exclusion manifests and
independent disposition are recorded in the P3 review package.
