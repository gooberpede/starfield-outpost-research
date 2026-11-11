# Experiment A: x87 preservation through exception observation

2026-10-16, Australia/Sydney. SOR-EXP-0034 / SOR-EV-0042 continuation.
[Authorized brief](../../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_experiment_A_x87_state_preservation.md`).
Authored material REVIEW-REQUIRED; raw synthetic evidence/builds LOCAL-ONLY.

| Element | Result |
|---|---|
| Question | Can the existing disposable exception observation route preserve the required x87 environment through its tested adversarial conditions? |
| Answer | **PASS within the defined offline fixture conditions after exactly one correction.** The original route loses both full-width pointer high words; the corrected continuation restores captured entry state. |
| Confidence and coverage | Direct disposable execution with independently decoded field bytes; one Intel CPU and Windows installation, masked x87 state, two continuation instruction classes, nesting, interruption, concurrency and cooperative STOP. Independent review is recorded in [review.md](review.md). |
| Evidence | Local `diagnostic-04` versus `corrected-02`, `states.bin`, `comparison.json`, assembly listings, `build.json` and `run.log`; [contract/ledger](validation.md), [commands/source](../../../../research/x87-preservation/README.md). |
| Limits | Retail safety, native spatial equivalence, arbitrary exception chains, unmasked pending x87 exceptions and retail storage/lifetime are **NOT TESTED**. No observer implementation or live authority follows. |
| Next step | Maintainer critical review of this bounded qualification. No additional experiment is needed to close this assignment; further instrumentation needs a separate decision and brief. |

## Qualified observations and first divergence

The pre-trap boundary follows the complete seeded x87 sequence and precedes the
authored MOV/ADD terminal. Adjacent FXSAVE64 captures agree; a non-REX.W FXSAVE
captures the legacy representation separately. The first handler instruction
sequence allocates aligned stack storage and executes FXSAVE64 before calling
C++, saving LastError, copying evidence or invoking nested observations. It
captures actual handler-thread hardware state, not a reinterpretation of CONTEXT.
Windows dispatch has necessarily already occurred; this is first VEH entry,
not kernel trap entry. Its stack adjustment affects integer flags only.

The post boundary immediately follows the displaced MOV or ADD, before further
x87 work. The unpatched control executes those same instructions at the original
sites. Minimal and adversarial cases use the same seed, operands, assembly probe,
continuation and decoder. Minimal skips nested/geometry/lifecycle work inside the
handler; the adversarial case retains deliberately destructive callbacks, nested
and caught exceptions, thread stress and cooperative retirement. Handler-entry
measurement and evidence copying are unavoidable diagnostic work even in the
minimal condition. Every frame owns its before/entry/after association.

In both uncorrected exception conditions, **hardware at handler entry still has
the original full FIP and FDP**. The supplied Windows FltSave representation
already lacks their high words. After ordinary continuation, hardware FXSAVE64
also lacks them. Thus this is not merely a display problem: an architectural
post-state difference is observed. The context representation diverges before
this handler's manipulation; architectural loss is bounded between captured
handler entry and the controlled continuation boundary. The exact OS restore
instruction and kernel path were not observed. Minimal reproduction rules out
the adversarial callback as a necessary cause, without assigning an unobserved
instruction as the first cause.

The one [pre-implementation correction plan](correction-plan.md) uses captured
entry pointer bytes in an invocation-owned copy of FltSave, then executes
FXRSTOR64 in the leaf continuation before the displaced instruction. The supplied
CONTEXT still receives only the historical RIP change. Its raw image and the
entry image remain separate, unmodified evidence. The decoder verifies the
entire restore image against those two original sources. No pointer is inferred
from expected code addresses or borrowed after handler return.

## Three-way results and exact fields

Each final run has six unpatched controls per process: three modes before
installation and three after retirement. Minimal has 99 trapped probes.
Adversarial has 1,112 decoded trapped state probes including one nested child;
the older native comparison counts 1,111 because it does not compare that child.
There are 1,173 total trap hits, including 61 geometry-site hits outside the state
corpus. Native counters and decoder counts measure different populations.

| Condition | Uncorrected `diagnostic-04` | Corrected `corrected-02` |
|---|---|---|
| Unpatched | All 12 controls preserve every compared field | All 12 preserve every compared field |
| Minimal | 99/99 lose FIP/FDP high words after continuation | 99/99 preserve all required x87 fields |
| Adversarial | 1,112/1,112 lose FIP/FDP high words after continuation | 1,112/1,112 preserve all required x87 fields |
| Entry hardware | Every trapped frame matches its pre-state | Every trapped frame matches its pre-state |
| Raw Windows context | Every trapped frame lacks high FIP/FDP words | Same representation limit; retained explicitly |

The following table gives corrected adversarial sequence 4, binary frame offset
17,172, with snapshot offsets defined in the source README. Hex integers are
decoded little-endian; ST payloads retain byte order. These are disposable
process virtual addresses, not game RVAs or stable identities. Other frames
have different data pointers, thread/stack associations and sometimes FIP paths.

| Required field | Before | First VEH entry hardware | Raw FltSave | Corrected after |
|---|---|---|---|---|
| CW | `0x077f` | Same | Same | Same |
| SW, including conditions/TOP | `0x6501` | Same | Same | Same |
| Abridged physical tag | `0xb0` | Same | Same | Same |
| Opcode, meaningful 11 bits | `0x321` | Same | Same | Same |
| FIP, full 64 bits | `0x00007ff71d1057a9` | Same | Low offset `0x1d1057a9`; upper representation zero | `0x00007ff71d1057a9` |
| FDP, full 64 bits | `0x000000d5190ff810` | Same | Low offset `0x190ff810`; upper representation zero | `0x000000d5190ff810` |
| ST0, 80-bit payload | `00000000000000a00040` | Same | Same | Same |
| ST1, 80-bit payload | `34c26821a2da0fc900c0` | Same | Same | Same |
| ST2 payload, empty slot | `00000000000000000000` | Same | Same | Same |
| ST3, 80-bit payload | `0000000000000080ff3f` | Same | Same | Same |
| ST4–ST7 payloads, empty slots | Each ten zero bytes | Same | Same | Same |
| MXCSR | `0x1f80` | Same | Same | Same |

For the uncorrected counterpart, sequence 4 at frame offset 15,636 has FIP
`0x00007ff7b1c056f9` and FDP `0x0000004517d7f550` before and at entry. Context
and after contain `0x00000000b1c056f9` and `0x0000000017d7f550`. All other
table fields match. Every frame's exact values and differences, not merely
these examples, are retained in comparison.json and raw binary records.

TOP is 4. Tag bits identify physical registers 4, 5 and 7 as nonempty, mapping
to logical ST0, ST1 and ST3; logical ST2 is an intentionally freed hole. The
live values are 2.5, negative pi and 1. Empty-register payload equality is retained
as a byte diagnostic; their values are not claimed as architecturally usable.
CW masks exceptions and selects extended precision/downward rounding. SW seeds
masked invalid sticky status and C0/C2/C3, with C1 clear and no pending unmasked
exception. FOP and FDP are explicitly seeded through FXRSTOR64 because ordinary
arithmetic left FDP zero on this host. Their successful restoration is confirmed
by the independent pre-trap captures; authored expected bytes alone are not proof.

In the 64-bit save image, full pointers occupy the selector positions of the
legacy layout. FXSAVE64 has no separate meaningful selector fields to compare.
Legacy pre FXSAVE and Windows context retain low offsets with observed zero
selector/reserved words at field offsets 12/14 and 20/22. Those zero words
must not be substituted for the high bits of the separate 64-bit image.
The instruction-layout interpretation follows Intel's FXSAVE/FXRSTOR entries,
Tables 3-46/3-47, [SDM Volume 2A, September 2016, 253666-060US](https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-vol-2a-manual.pdf).
Microsoft's [x64 CONTEXT documentation](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-context)
identifies FltSave's XMM_SAVE_AREA32 representation. Neither source is used as
proof of this host's actual exception behavior; that comes from the captures.

## Scope, retained failures and decision

The corrected path preserves every required meaningful x87 field compared above,
including both full-width pointers, under the fixture's seeded state and tested
lifecycle. GP/RSP, arithmetic flags, all 16 distinct YMM patterns, XMM and three
MXCSR modes still pass. [The ledger](validation.md) records nesting, interrupted
observation, in-flight STOP, geometry/replay, malformed evidence and preservation.

Historical `native-11` remains unchanged with its 1,110 reported pointer losses.
New `diagnostic-01` exposed an undersized inherited geometry snapshot after the
diagnostic expanded the probe: the adversarial process failed after 1,009 complete
state frames. Its batch wrapper initially missed the negative process exit and
reported zero; that build receipt is **not a successful full run**. The checked
buffer/closure adaptations and signed exit detection were repaired before
`diagnostic-02`. That run still left FDP zero after arithmetic; `diagnostic-03`
qualified explicit high FDP/FOP seeding and supported correction eligibility.
`corrected-01` passed. Final paired runs add nonzero x87 condition/sticky status
and deterministic in-flight STOP. These are measurement/coverage refinements;
there was only one preservation correction. No failed artifacts were replaced.
Early log label `OSbuild` incorrectly described GetVersion's packed compatibility
return; final labels and Python version provenance correct that interpretation.

This is a scoped engineering PASS, not whole-machine or universal x87 proof.
Only one masked x87 configuration is qualified, with two observed status patterns
across retained runs; no unmasked pending exception, every NaN/denormal/tag pattern,
nonzero legacy selector, arbitrary-depth nesting, handler chain, asynchronous
retirement, unwind/stack walking through the correction, or XSTATE extension is
qualified. The early entry hardware being intact is host evidence, not a Windows
API guarantee. The fixture's R15-owned image is not evidence that a retail site
can reserve that register or acquire storage safely. No native spatial pair,
observer/DLL/package, deployed file, save, game process or Ghidra state was changed.
