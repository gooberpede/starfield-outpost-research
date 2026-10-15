# Beacon resource observer 0.7.0

Offline candidate for [SOR-EXP-0035](../../docs/experiments/continuous-beacon-preview/contract.md).
No deployment or live execution authority. Previous release identities are preserved.

Build with installed CPython:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B runtime/beacon-resource-070/build.py --name qualification-final
```

Reads pinned installed PE/SFSE, its own source, unchanged approved interface header,
project support and protected baseline. Runs disposable MSVC/MASM/decoder/worker
fixtures; writes exclusive ignored build, receipts and Vortex ZIP. No target launch,
save/configuration/database change, downloads or Git mutation. Exact input/output
hashes and compiler receipt are in build.json and build logs. Required runtime
deployment is only Data/SFSE/Plugins/SorNativePositionOracle.dll. ResearchNotices
remain package notices and are not required beside the DLL.

capture.h observes ten natural CALL boundaries and uses unchanged 060 hash-bound
group-flushed spool. Event phase 1/2/3 = before/normal return/unwind. Event size is
3328 bytes, little-endian. Header has twelve u64 fields (sequence, invocation,
parent, thread, QPC, site RVA, kind, phase, reference, command, result, status),
four u64 args, then eight 400-byte blobs (ref/base/extra/cell/world/operand/aux/output).
Each blob is address u64, length u32, read-ok u32, up to 384 owned bytes.
Zero read-ok is missing data, never observed empty bytes.

| Kind | Blob/identity roles |
|---|---|
| 101 evaluation | args = state/indexed input/radius f32 bits/geometry f32 bits; ref=indexed24, base=query cache0x68, reference=indexed domain pointer, command=held preview ref if captured, extra=preview raw header, output=base form header, operand=domain form header, cell/world=non-atomic optional headers. |
| 102 UI | command=actual callback command; args1=model; output=guarded payload header, operand=selector pointer, cell=selector header. No rendering claim. |
| 103/104 actual common consumer | args1/2=actual begin/end, args3=local fold, aux/output=fold header snapshots. |
| 105 selected special append | operand=resource-pointer operand, base=resource header. |
| 106 row construction | reference=actual RDI resource; base=resource header; command=pre-construction ordinal; operand=constructed destination raw row after return; output=payload header. |
| 107 queue allocation | command=returned command pointer after normal return; no resource epoch inferred. |
| 108 population header | args0=source index, args1/2=begin/end. Empty is valid equal endpoints; invalid header status1. |
| 109 member | args3=index; operand=pointer slot, output=resource header; reference=pointer. Failed slot status2, failed pointed read status4. |
| 110 final row census | args3=ordinal, operand=actual final 0x170-byte row; linked to own UI invocation. |

Invocation status bits: 2 missing population header, 8 changed header reread,
0x100 unwind, 0x200 observed writer overlap/epoch change, 0x400 invalid final row
range, 0x800 completion after STOP, 0x1000 wrong model/getter contract.
Raw/member statuses are independent. Header equality cannot exclude member ABA.
Counters cover admitted, written and group-flushed records; producer overlap
tracking continues after admission closes. No lock spans a native invocation.
Backpressure, memory reads, assembly relays and file locks affect timing.

inspect_resources.py streams raw/WAL verification and retains invocation summaries.
Optional --out is exclusive JSON. It returns a verified prefix for unretired
evidence, explicit INCOMPLETE for partial/corrupt tails or unpaired calls, and
RETIRED_INTEGRITY_OK only with matching terminal counts. It does not repair raw
evidence. Failed tails can leave a useful verified prefix, not scientific absence.
Output distinguishes population-signature changes from actual reconciled UI rows.

operate.py reads file/process metadata and audits pins. Future explicitly approved
request/stop actions write only this observer's session control files; STOP uses
four preallocated bytes and remains available under low-disk/protection failure.
No helper launches, attaches, deploys or changes saves/configuration. The final
run-card governs all future use. Worker STOP drains admitted invocations, leaves
guarded resident inert wrappers until normal process exit and then closes handles.
No hot unpatch/unload or arbitrary acquisition deadline/quota is promised.

Lineage: [source register](../../docs/experiments/continuous-beacon-preview/sources.md).
All proprietary/raw/build/fixture outputs stay ignored/local. Publication remains
separate from engineering and scientific confidence.
