# D5AR source-recorder startup history

2026-11-05, Australia/Sydney. **STATIC / REVIEW-REQUIRED.** A retired-address
recorder must start before the first geographic-source lifetime. A null manager
after world teardown cannot establish that history. The supported method is
fresh-process SFSE Preload before ordinary engine initialization, together with
the producer's owner, sole-thread and complete ancestor guards.

## Source report and actual installed binary

Ian Patterson and SFSE contributors' pinned
[sfse.cpp](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/sfse/sfse.cpp#L30)
describes the pre-global-initializer hook; its lines 48–78 and 90–131 connect the
CRT import replacement to phase-zero plugin loading. Pinned
[PluginManager.cpp](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/sfse/PluginManager.cpp#L95)
lines 95–169 and 414–429 describe export resolution and invocation. These are
read-only research leads, not incorporated implementation. The MIT header
approval does not authorize other SFSE code reuse.

The independent installed-binary check reads SFSE SHA-256
`28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b`.
All addresses below are **SFSE preferred static VAs**, image base `0x180000000`,
not Starfield VAs or runtime addresses. The actual binary is 116,216 bytes.

| Actual installed instruction/data chain | Supported conclusion |
| --- | --- |
| Export `StartSFSE`, RVA `0xd6e0`; code `0x18000d766..0x18000d792` obtains the EXE module and passes string `0x180014ef0` to `0x18000e5e0`. That string is `_initterm_e`; the helper matches CRT library string `0x180014f00`. | This is the EXE CRT import, not the SFSE DLL's own import or a guessed plugin phase. |
| `0x18000d79f..0x18000d7d3` saves the original slot in `0x180019ed0`, obtains writable protection and installs `0x18000cf60`. | The original entry is retained; the replacement controls the call before forwarding. |
| `0x18000cf7c..0x18000cf94` checks/sets once flag `0x18001c128`; `0x18000d081` scans plugins; `0x18000d086..0x18000d088` passes phase zero to `0x180009850`. | Ordinary phase-zero invocation is once per process initialization. |
| `0x1800098c6` supplies the `SFSEPlugin_Preload` string; zero phase selects it at `0x1800099cd..0x1800099d4`, resolves through the actual `GetProcAddress` IAT and stores the returned function at record `+0x2a0`. | The phase names follow actual data and control flow, not a header-only assumption. |
| `0x1800099f1..0x1800099f4` passes that phase to `0x18000a8a0`; `0x18000a8a4..0x18000a8b6` loads the corresponding function and invokes it with the native SFSE interface. Only afterward does `0x18000d099..0x18000d0a6` call the retained CRT initializer. | The actual installed ordinary Preload path calls the plugin before forwarding EXE initialization. It does not defer Preload until a later world teardown. |

The complete disassembly has two direct calls to the phase installer: this
phase-zero call and the separate phase-one startup path. The reported upstream
source and installed native flow agree on the relevant ordering; no claim of
byte-identical upstream source compilation is needed or made.

## Experiment and limits

[The original read-only exporter](../../../research/resource-retained-population/d5ar_sfse_preload.py)
uses installed Microsoft dumpbin 14.51.36256.0. It reads the pinned DLL as data,
exports imports/exports/disassembly to a fresh ignored directory and hashes the
DLL, tool, method and outputs before/after. It neither loads nor executes SFSE,
opens an analysis database, changes an installation/configuration/save, nor uses
a network. Both caller-available drive floors apply; mismatches or tool failure
stop the experiment. Existing logs are retained without replacement or deletion.
The source-bounded receipt is
[sfse-preload-binary01](../../../.local-work/d5ar/sfse-preload-binary01/receipt.json).
Its export status deliberately requires semantic review; successful dumpbin
execution alone does not establish the table's conclusions.

This is a bounded ordinary-startup argument, not detection of arbitrary injected
code, direct manual export calls, prior engine initialization by another plugin,
or a deliberately fabricated acquisition. The separately approved effective load
set and fresh-process route must preserve that contract. The startup receipt is
not a signature or a retrospective lifetime log. Late/manual injection and an
unqualified earlier engine-initializing plugin cannot receive this source-history
certificate. No new live/deployment authority follows from the static proof.

The recorder must retain every admitted ending address until process exit,
refuse address reuse, and disable source diagnostics after any coverage loss.
Its source-group/free synchronization and native ending-call completeness need
their own independent proof. Safe protected holder geometry remains a separate
result if any source-history premise is unavailable.
