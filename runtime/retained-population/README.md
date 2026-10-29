# Retained-population observer 0.2.0 (R1 offline only)

The current [R1 design](../../docs/experiments/resource-retained-population/d5p-r1-design.md)
and [pre-repair diagnosis](../../docs/experiments/resource-retained-population/d5p-r1-diagnosis.md)
govern schema 2. Retail remains NO-GO. The historical v1 package and operation
helpers explicitly refuse schema-2 builds; they are not a migrated retail gate.

The original Phase A instrument followed the [D5P brief](../../docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5P_SFSE_retained_population_observer.md).
The [design](../../docs/experiments/resource-retained-population/d5p-design.md)
records eleven selected observation boundaries. No helper installs a plugin,
launches Starfield, attaches a debugger, changes gameplay, saves or configuration.
The proposed Phase B card requires separate explicit authorization.

Build and run the real disposable Windows fixtures using installed CPython,
MSVC, MASM and the Windows SDK:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B runtime/retained-population/build.py r1-reproduction
```

The build writes an exclusive directory below `.local-work/d5p/`. It reads the
pinned installed EXE, ESM and PlanetData, the existing SFSE runtime and the
approved unchanged SFSE interface header. Native source, generated site hashes,
compiler commands, logs, DLL, host, damaged-evidence copies and qualification
remain local. Fixtures may intentionally terminate their own disposable process;
they never launch or terminate the game. An isolated fixture's 60-second startup
and worker waits are engineering test bounds, not scientific capture deadlines.

`protect.py <fresh-name>` uses the retained D5L active archive-backed preservation
method. It hashes surviving inputs and protected saves/backups and makes one
Save52 restoration rehearsal copy in ignored scratch. Originals and the active
baseline remain unchanged. It does not rehash the retired loose evidence tree.
The historical four-ZIP failure stays historical. This helper grants no live GO.

`package.py <qualified-build-path>` prepares a single local review ZIP and an
exact compatibility/package manifest. It neither installs nor enables it.
Only `Data/SFSE/Plugins/SorRetainedPopulation.dll` is runtime-essential. Keep the
notices, source and build method with the review package; review Vortex's actual
file preview before any separately authorized installation.

The DLL uses a reusable 1,024-cell MPSC ring. Each schema-2 event owns 1,528 bytes; native
point words are copied immediately, never dereferenced later by the writer.
At most 64 ordered points and 256 slots, members or regions are inspected per
bounded traversal. Capacity or retry-exhaustion loss advances a conservative global epoch and
acquisition continues. Unsupported reads close the affected claim. The worker
writes bounded batches of 64 records and preserves explicit output/disk failures. There is no silent eviction, gameplay work
queue, forced generation or native-call replay. Hook timing is affected by
bounded copying and Win32 reads. The worker performs file I/O and checks both
40,000,000,000-byte free-space floors. STOP leaves resident wrappers that bypass
observation and call their originals; hot unpatching/unloading is unsupported.

Each raw frame has a 16-byte little-endian header: magic `0x31505253`, payload
length, sequence low word and payload CRC32. The payload begins with 16 u64
fields, six u64 operands, count/owner u32, source bytes, effective descriptor,
region header and up to 1,024 point bytes. See `Event` and the independent reader
for exact offsets. Only its counted point bytes are geometry. The writer appends
raw records, flushes them, then appends and flushes an acknowledgment binding
the cumulative byte count, sequence, prefix CRC32 and identity-file SHA-256.
Enqueued, written, flushed and independently verified counts are distinct.
Each drain uses an enqueue snapshot and returns after that batch, so continuous
production cannot starve flush, health or STOP. Disk checks reserve batch bytes.
Stream writes are buffered; the explicit raw flush and subsequent ACK flush
remain the durability barriers. Written bytes alone are never durable evidence.

`read_capture.py <session> --dll-sha256 <approved-hash>` reads evidence only;
`--out <new-file>` writes a separate result. It checks framing, sequence, CRC,
session/plugin identity and acknowledged prefixes before reducing chains. A
valid prefix after a crash can contain a complete witnessed region even when
session coverage is incomplete. Missing or damaged evidence is not absence.
The reader reports raw masks, contrary geometry, hit-only and bypass observations.
It separately counts construction-only and retention-only witnesses. Current
owner, raw mode and the converter's actual descriptor must agree with the
qualified construction context; original and copied geometry are both retained.
A witnessed good region may remain qualified when a different append fails;
the chain then explicitly reports `population_partial`.

Native integration is pinned to 1.16.244.0 and the exact installed hashes and
site guards in `build.json`. The synthetic host uses the same built DLL and
hook/transport code, with separate fixture entry points that refuse a retail
host name. SFSE retail loading, sole-thread availability, actual scheduling,
all-alias writer coverage and general asynchronous unwinding through the inline
branch or dynamically emitted prologue are not established by these fixtures.
The bridge performs only nonthrowing capture operations; no general exception
recovery, safe mod integration or intervention-free behavior is promised.

Startup waits for verified sole-thread admission using the earlier observer's
pattern, while enforcing disk protection and operator STOP. It never patches
around a peer thread. Waiting does not establish readiness or authorize a save
load; the main-menu READY gate remains mandatory.

R1 adds unpaced transport and actual-hook controls, exact single/multiple loss
recovery, in-flight/cross-loss contamination, retained-Grid and coverage-bound
reason tests, and early/late output failure controls. Test receipts remain
local under the exclusive build directory. Ticket-state fault injection forces
the bounded retry-exhaustion path; it is not reproduction of historical CAS
contention. Timing describes the actual tested native-shaped layouts, not a
retail latency guarantee. No test supplies missing original runtime operands.
