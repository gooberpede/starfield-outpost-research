# Independent hook and native-caller audit

2026-10-13, Australia/Sydney. Specialist contribution to the
[authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_cross_session_native_center_state_and_observer_interference.md).
Authored interpretation REVIEW-REQUIRED; native exports and binary receipts LOCAL-ONLY.

**The two historical center sets do not compare equivalent execution boundaries.
Observer 0.6.0 did instrument the older AD0C36 center CALL; observer 0.5.0 did
not instrument F4A1D4. Both call the same native center calculation, without a
caller-selected Z mode. Caller/state selection and timing remain material;
existing ABI tests do not prove behavioral noninterference.** No direct observer
write to reference XYZ or a demonstrated center corruption defect was found.

This audit reread source and archived native instructions, checked the two actual
build manifests, rehashed all 61 manifest source inputs, and inspected retained
fixture receipts. It did not launch a game, build or execute native fixtures,
access runtime memory, edit a native database, or alter original evidence.

## Address and version boundary

Native addresses in this report are RVAs for retail 1.16.244.0, image preferred
base `0x140000000`, executable SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Static exports use preferred-base VAs. Runtime pointers in original captures
remain session-specific addresses; pointer equality across sessions is invalid.
Source references below are repository-relative paths and one-based lines.

## Center and caller instruction provenance

The complete native F4AB80 export is
`.local-work/recon/workshop-origin-04.tsv:6–58`. It copies reference
`+8C/+90/+94` to the caller's twelve-byte output. Base type, global location and
47FCE0 predicate gate ExtraWorkshop lookup; when the native gate succeeds and
the vector is not all zero, it adds ExtraWorkshop `+60/+64/+68` separately to
output XYZ. Neither `+D3` nor caller address selects a Z calculation. Native
stores target the output, not reference XYZ. Consequently output is a consumer
result, not an observed write back to reference position. A zero compensation
vector makes either branch produce the same output, so those samples cannot
reconstruct the predicate's actual outcome.

`.local-work/recon/engine-oracle-01.tsv:6–104` gives AD0B90's preconditions and
AD0C36's actual operands: RCX=RBX reference, RDX=caller stack output. It validates
ordinary base and location before calling center, then consumes center X/Y plus
two source translation words to construct the grid floor. The immediate caller
does not choose a different height mode and does not write reference XYZ.
Its grid computation does not consume the center Z or a third translation word.

`.local-work/recon/workshop-origin-03.tsv:25–124` gives F4A140's different
preconditions and F4A1D4's actual operands: RCX=R15 reference, RDX=caller stack
output. Earlier 2116840 result RBX and own-cell interior flag gate reachability:
an interior own cell or nonzero helper result takes the early status=3 exit.
Null own cell by itself is allowed. After center returns, the routine copies
the resulting XYZ to its R14 output/context and derives more state. This gives
a concrete native selection distinction; it does not establish what 2116840
means or prove a loading/lifetime transition for the two sampled references.

The two caller sequences provide no direct explanation for the numerical Z
change: both invoke the same center with the selected reference and output.
An explanation must identify different reference/compensation operands, their
native producing history, a sampling defect, or interference elsewhere.

The second060 observed center site F498F1 is independently covered by
`.local-work/recon/workshop-origin-02.tsv:299–342`. RCX is R14 reference and
RDX is RSP+68 output; after return, the output pointer and R14 enter a local
descriptor passed to F48A60. It is a third immediate consumer path, with no
different F4AB80 Z mode. Its two observed invocations are not additional
F4A1D4 invocations and must retain their distinct site identities. The complete
function export was consulted locally; no proprietary instruction excerpt is
copied into this authored report.

## Patch, emission and consumer matrix

| Native patch / original target | 0.5.0 wrapper and emission | 0.6.0 wrapper and emission | Comparison limit |
|---|---|---|---|
| AD0C36 → F4AB80, complete five-byte CALL | `center_hook`, kind2 only after native return and only inside top stage2 callback | Generated `invoke<AD0C36,center>`, kind8 before/after/unwind | Patched in both; an absent 060 event is not an uninstrumented path. Before-output is not a native center result. |
| F498F1, F4A094, F4A1D4, 18843F2, 21B28FC, 21BB8F0 → F4AB80 | Not instrumented | Separate site-qualified kind8 scopes at all six | 050 absence conveys no reachability information. |
| 4B916F0/4B916F8 callback pointers → AD8EC0 | `callback_hook`, begin/end/unwind stage2, TLS ref/context | Not instrumented | 060 lacks equivalent Q/E/callback ancestry, despite retaining AD0C36 site identity. |
| AD93FA → AD08D0; AD0AB5 → B1E190 | Q/E before/end/unwind, actual arguments and TLS ancestry | Not instrumented | Source-frame/query evidence cannot be inferred from a 060 own-cell sample. |
| AD0D36 → 96F5C0 | `selector_hook`, kind6 input then kind3 output, linked prior native center | Not instrumented | No 060 equivalent ordinary Workshop grid output. |
| Retained travel/route nineteen-CALL set, excluding the four above | Route/request/identity/fallback/grid and command scopes | Not instrumented | Travel trigger and route are not captured equivalently. Exact nineteen pairs: `runtime/native-oracle-050/build.py:44`; wrapper mapping `plugin.cpp:11`. |
| 115 CALLs → B4E410, including 5A14DA | Not instrumented | Generic before/after/unwind; 5A14DA dedicated kind10 restoration | Setters are invocations, not guaranteed stores or allocation births. |
| B7351A, 18DC8D0 → B73310 | Not instrumented | Kind3 scalar application, sixteen-byte operand including mode | Partial writer coverage; outer D3 change follows ordinary inner CALL. |
| Ordinary virtual slot 4B967B0 → B734C0 | Not instrumented | Kind2 outer conversion before/after/unwind | Other subclass slots remain uncovered. |
| ACD2C0 → B4A0B0; ACD2D8 →18C28B0; 18C2982 →22CDF60; 18CE315 →B4A0B0 | Not instrumented | Producer, queued producer, allocation, application | TLS ancestry and command-generation relation are different joins. |

The complete [per-site ledger](coverage.csv) has 150 rows: all 21 patches in
050 and all 129 in 060, original targets, wrapper symbols, emitted event kinds,
phase, raw counts, downstream consumer and gaps. A read-only memory-mapped header
scan independently counted all 1,194 schema5 and 562,326 schema6 records. It
found zero AD0C36 events anywhere in060; F4A1D4 has33,648 records (16,824 pairs),
and F498F1 has four records (two pairs). This is **instrumented but not observed**,
not a missing patch or selected-identity filtering artifact. The two callback
slots share one wrapper and cannot be distinguished from their 120 aggregate
callback invocations. 050 shared helper kinds were joined to fixed sites where
unique; the two delta CALLs have no kind35/36 records at either site.

060 `build.py:42–64` derives complete CALLs from the pinned xref export and
checks their actual opcode/target. Selected qualification-11 manifest contains
exactly seven center sites including AD0C36. 050 `build.py:44` contains exactly
one center site. Overall 050 has nineteen CALL plus two pointer edits; 060 has
128 CALL plus one pointer edit. This matrix describes installed instrumentation;
whether a site fired must be determined from complete raw records, before any
identity/report filtering. Unknown or filtered records are not absent calls.

## Sampling counterexamples and field meaning

1. **D3 absence is designed coverage, not a zero flag.** 050 `core.h:87` copies
   only `0xD0` reference bytes; its extra read cannot recover reference `+D3`.
   060 `history.h:32` copies `0xD8`, which includes D3. Comparing a default-zero
   decoder value for missing 050 D3 with actual 060 D3 would be invalid.
2. **Status0 has different race coverage.** 050 `core.h:99–100` rechecks only
   `+24` twelve-byte identity, `+98` base pointer and `+C8` extra-list pointer.
   It does not recheck coordinate bytes. 060 `history.h:37` compares the full
   `0xD8` prefix. Thus status0 does not certify an atomic coordinate/extra/parent
   snapshot in either version, and specifically does not exclude a 050
   coordinate change during sampling. The060 comparison is at `history.h:38`.
3. **050 samples after native return.** `core.h:163–169` calls original center
   before collecting reference, extras, context and output. A concurrent writer
   can intervene between the native read and those later snapshots. 060
   `history.h:73–83,90` brackets the call, but its before/after snapshots are
   also non-atomic and do not expose the precise native read instant.
4. **Own frame is not query frame.** Both source snapshots read reference+B0,
   then cell+110 when exterior. 050 separately records query/source context;
   060 world snapshots stop at +180 and omit historical descriptor key+310.
   An available own-world pointer cannot substitute for the older query key.

## Observer interference audit

| Mechanism | Source/evidence checked | Defensible result |
|---|---|---|
| Patch bytes and relay stack | Both `patch.h:32–83`; both plugin installation paths; build guards | Complete CALLs use E8 rel32 to a fourteen-byte leaf indirect jump. Callback/virtual edits use eight-byte pointers. No stolen prologue. Preimages, sole-thread admission, page protection, cache flush and retained resident hooks are explicit. This does not prove absence of other unrecorded instrumentation. |
| Original call and argument order | 050 `core.h:155–187`; 060 `history.h:64–90`; generated wrapper definitions | Original pointers forwarded. 060 forwards R8/R9 on the audited four-register contracts; center output copied after return. No observer formula replaces native output. 050 center declaration has two operands, matching recovered center instructions. |
| FP/LastError and ABI | Both Environment implementations; 050 qualification520 receipt; 060 qualification receipt and MASM fixtures | FXSAVE64/FXRSTOR64 and LastError restoration surround observation; retained tests cover nonvolatile GPR/XMM, MXCSR and native return channels. They do not prove arbitrary flags/register preservation, AVX upper-state preservation, every implicit-input contract, or retail noninterference. Caller instructions around the two audited center sites do not establish an extra incoming flags/Z-mode contract. |
| Exceptions | `__try/__finally` wrapper scopes and retained C++/SEH tests | Native exceptions propagate; cleanup records unwind rather than swallowing game faults. Record-allocation/I/O failure remains intervention risk; fixture success is not retail fault absence. |
| Reentrancy and depth | 050 TLS depth32/suppression and overflow fixtures; 060 TLS Scope chain | 050 has a bounded TLS capture depth and explicitly fails capture on overflow; 060 has nested stack scopes without a matching explicit32 bound. Both separate threads' ancestry. No exercised retail overflow is established. |
| Concurrency and ordering | 050 `core.h:33–45,77`; 060 `history.h:48–59,67–83` | 050 assigns sequence before queue publication, so cross-thread raw file order need not be numeric sequence order. 060 assigns sequence under spool lock after snapshot reads. Neither sequence orders actual native stores. TLS does not fabricate cross-thread producer ancestry. |
| Engine-thread I/O and timing | 050 queue push versus worker flush; 060 `Spool::emit/flush` | 050 engine callbacks copy to a bounded nonblocking MPSC queue. 060 engine callbacks acquire a shared exclusive SRW lock, hash each event, query C:/D: free space and perform synchronous cached raw/journal WriteFile. Worker group-flush holds the same lock. No lock spans a native call, but contention and storage latency can delay it before/after. This is a concrete intervention difference. |
| Admission and STOP | Both await_admission/install and worker retirement paths | Source guards require a sole-thread startup observation; STOP makes wrappers inert while leaving patches resident. 060 waits for active calls before closing transport. These are bounded engineering controls, not proof that sampling leaves gameplay state unchanged. |

No source-backed direct reference XYZ write, deliberate compensation, fabricated
center call, swallowed native exception or demonstrated ABI defect explains the
observed Z values. Timing-sensitive interference is **possible and unexcluded**;
the different engine-thread I/O design supports the existence of a changed timing
mechanism, not causation of this discrepancy. Existing successful fixture ABI,
concurrency and transport tests contradict only the corresponding exercised
synthetic defects. A passing native field arithmetic check is not a general
noninterference test.

The direct-writer counterexample remains: B22BF0, B230A0 and 1A25420 contain XYZ
stores outside the 115 B4E410 CALLs. Existing
[writer audit](../position-write-history/static-audit.md) records exact native
sites and ordinary-converter mask ordering. Missing selected converter events
cannot establish no translation or no other writes.

## Reproducible checks and exact input pins

The specialist executed original CPython3.14 standard-library checks only:
recompute SHA256 for every `sources` entry of the two selected `build.json`
files; assert no mismatches; assert the exact seven 060 center `guards` sites;
assert 050's sole center `call_pairs` entry; assert the D0/D8 source-copy boundaries
and post-original 050 center call. All passed: **61 source pins, exact center-site
sets, sampling-boundary counterexamples**. These are source/manifest checks,
not new executable or game tests. An initial inline PowerShell quoting attempt
failed with Python SyntaxError before doing work; a single-quoted here-string
retry executed successfully. No scientific input changed.

Header-count reproduction uses Python `mmap.ACCESS_READ` over the original raw
files: schema6 stride3328, site uint64 at record+40; schema5 stride17768, kind
uint64 at record+56. Assert exact divisibility before traversal. Map050 kind tags
to its fixed `call_pairs`/relay_targets order; kinds35/36 additionally carry a
runtime return address in block blob data+8 (record+88+14×1040+24), normalized
by runtime module base `0x7ff7a4950000` and subtracting five. No such delta
records were present. Callback slots remain explicitly ambiguous. Hash validation
and semantic decoding remain separate checks in the primary independent verifier;
this header scan is an independent coverage count, not a substitute for them.
One first attempt looked for absent schema5 `session.json` after completing the
schema6 scan; retry used the independently recorded module base and succeeded.

| Input path | SHA256 |
|---|---|
| `runtime/native-oracle-050/core.h` | `44461be7cbd10676b52a1b0d6762ce4b753030f3cae6320a84e4f1c7df91b6dd` |
| `runtime/native-oracle-050/build.py` | `f3f8dcf340f5b15ce562bd02867be275417bcd17a065a775fa8404b0b5f6f1d2` |
| `runtime/native-oracle-050/plugin.cpp` | `5a7e22175b5e2807be7e1d569300e240674869f054fc3511087a49be30e9da74` |
| `runtime/native-oracle-050/patch.h` | `b3b924e4e141a785d33a7f8a2fc41736af6866268669ff3b585125509dd40677` |
| `runtime/native-oracle-060/history.h` | `b2d3ae4a0e9f0662e0bf82d7aacd02c264668963e67e3430ad44a4adee3d063c` |
| `runtime/native-oracle-060/build.py` | `7e1ac4dee118fc245208815f68e55c3e3150e29fbbcb698654b2c7e28578eacb` |
| `runtime/native-oracle-060/plugin.cpp` | `bfea396f921bd2e2b2b7cbd5b6bd05c0d6bf3dfaf2adf2a4dfc47750f8d27df1` |
| `.local-work/native-oracle-050/builds/qualification-03/build.json` | `d7b1bf845bbdd770f1088e8d59c51409d24312fe8fdadac4b7857b0d7eaca501` |
| `.local-work/position-write-history/builds/qualification-11/build.json` | `5aa022529772285369aca2a7cafa4be240368ed83e94f635fdfb463ea2c803a8` |
| `.local-work/position-write-history/builds/qualification-11/identity.generated.h` | `ccbc41ce7c8aa536f57f9aa3aef0a34bbbc0bf37c3ce3fdd4cb0920f637fbdc5` |
| `.local-work/recon/workshop-origin-02.tsv` | `bf5ad254692fd06fb74aca2d47885e880330efbe7eae719ddac091d4b9e63255` |
| `.local-work/recon/engine-oracle-01.tsv` | `33c4508537b7993cc6942a3ecc8bc8b8bd77812a5d3bb9c7b104efa5ac35cfad` |
| `.local-work/recon/workshop-origin-03.tsv` | `0b2b6adee14887253ad4443a5dd02c12c5f3f32d1fb283817576857097f3ccff` |
| `.local-work/recon/workshop-origin-04.tsv` | `c087406d27e0c8c04ba79e496b537ff415e264ac77f46584085fdc68b329e9a0` |
| `.local-work/position-write-history/writer-audit.tsv` | `006979e228a26ed171ee280d8ab8a974a6604e6aa5e0fa8b7f238bce073395d9` |
| `.local-work/native-oracle-050/builds/qualification-03/qualification.txt` | `e2708bf720741db5a215e413187c26a9b06a31398d9df57c4679b8866386b440` |
| `.local-work/position-write-history/builds/qualification-11/qualification.txt` | `ec67ffdf0d30262bdfe6024e7897c2af98b58247c9cdf2e041577a738fd05e22` |

## Distinct contribution and acquisition challenge

Novel audit contributions are the verified AD0C36 coverage correction; the D0
versus D8 flag-coverage counterexample; unequal race-check semantics; the actual
F4A140 own-cell/helper gates; and the precise engine-thread storage/lock difference.
These reduce uncertainty without claiming an identified historical cause.

The smallest useful comparison needs the **same AD0C36 natural operation** after
the older new-landing/return trigger, with paired reference XYZ/D3/own-frame,
compensation and returned native XYZ, plus Q/E source identity. Merely collecting
more F4A1D4 centers under the local-travel control cannot distinguish the old
case. Before proposing broad writer capture, exploit existing 060 AD0C36 event
coverage and reconstruct the original context difference; establish whether the
matching operation was reached at all.

To test interference itself requires a deliberately scoped contrasting observer
configuration or equivalent uninstrumented observation, with the same natural
trigger and comparable native boundary. A minimal callback/center channel reduces
intervention but does not prove the effect of removing broad writers. Such a
comparison costs additional live authority and remains vulnerable to unrelated
session differences. No new observer build or live experiment is authorized
here. Full XYZ equivalence and causal noninterference remain NOT ESTABLISHED.
