# Position writer, ABI and lifetime audit

2026-10-13, Australia/Sydney. Specialist contribution under the
[authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_workshop_position_write_history_Z_oracle.md),
independently read against the prior [Z dependency ledger](../workshop-z-restoration/dependencies.md).
Authored interpretation REVIEW-REQUIRED; proprietary exports LOCAL-ONLY.

**A scoped ordinary writer acquisition is feasible, but setter plus converter
hooks cannot prove a complete reference history.** The existing native state has
concrete direct XYZ stores outside B4E410/B73310. Initial saved-record restoration,
later frame conversion and final center are distinguishable operations. A missing
writer, allocation/destruction interval, command producer or save-load epoch must
remain a named gap. This audit does not claim live reachability or qualified hooks.

## Provenance and method

All addresses below are static VAs for preferred image base `140000000`;
RVA = VA minus that base. Installed retail `Starfield.exe` was read and freshly
hashed: 102476200 bytes, SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
It matches the existing analyzed program's metadata. Existing Ghidra 12.1.2 state
was exported with `-readOnly -noanalysis`, using installed JDK 21.0.12.8 and an
original project-owned `WriterAuditRead.java`. No symbols/types/comments or
analysis state were edited; no game/process access occurred.

Local evidence under `.local-work/position-write-history/`:

| Artifact | SHA256 / purpose |
|---|---|
| `writer-audit.tsv` | `006979e228a26ed171ee280d8ab8a974a6604e6aa5e0fa8b7f238bce073395d9`; fresh complete existing xrefs to B4E410/B73310/B734C0/F4AB80 and complete 18CE300 instructions |
| `WriterAuditRead.java` | `ce030dd7e1794a1e22c385225d32ce621b972cf81484cc84f6b8a652a3b13c0b`; reads listing/xrefs, writes one CREATE_NEW UTF-8 export; requires existing program; no target/DB effects |
| `writer-audit-retry.log` | `adca3b261deb8c43d06fb0b5b9c4e9c50da0c7c6c24a1f8e8e6e4b115702327e`; successful read-only export receipt; initial launcher/settings failures retained separately |

Prior primary exports were reread, not inferred from an agent summary:
`.local-work/recon/workshop-z-01.tsv` (SHA256 `b046f98fbbe7a0e9476fa41b05f68ab983ce944e3fb2f92cb7c7a8b9d129b60a`),
`workshop-z-02-retry.tsv` (`19be5ad49fddb1808f7b68147cdfe9ccebae8edef06b1ae3d6f847d5a5496762`),
`static-exhaustion-68.tsv` (`8a23d28ee34f329aec82044d79282c4c0849e09bf33feef446adddb903298a0f`),
`workshop-origin-04.tsv` (`c087406d27e0c8c04ba79e496b537ff415e264ac77f46584085fdc68b329e9a0`).
Also reread `.local-work/workshop-z-restoration/native-instructions.tsv` and
`writer-instructions.tsv`, whose hashes/provenance are retained in the
[prior source ledger](../workshop-z-restoration/sources.csv).

The first standard Ghidra launcher could not write its settings outside the
workspace; a direct Java launch then failed script loading for the same reason.
Retry with `application.settingsdir` in existing local scratch succeeded.
An optional default file-cache maintenance write remained denied; this was not
used as scientific evidence. The unsuccessful Java process was retired. These
failures are tool-environment failures, not missing native paths.

## Writer coverage and ABI

Native x64 calling registers are recorded from instructions, not accepted from
decompiler type guesses. Candidate CALL replacement still needs byte/preimage,
stack, register, return and floating-point qualification. Passing the original
operand pointer preserves aliasing; replacing it with copied XYZ is unsafe.

| Operation / decisive sites | Established operands and effects | Coverage / exclusion |
|---|---|---|
| Created restoration `1833B20 →5A0520`, CALL `1405A14DA →B4E410` | RCX reference from stack+50; RDX creation input R15+10, 12 XYZ bytes. Setter writes current 8C/90/94. Saved 0B bypasses both saved 20 edge additions before construction. | Covers actual initial setter in this branch; creation routine can reuse/rework references, so CALL alone does not prove allocation birth. |
| Setter `B4E410`, stores `140B4E49D/4AB` | RCX reference, RDX XYZ; void. Equality test can skip stores. Before setter, conditional BBEC70 receives incoming R8; reference/physics side effects surround writes. | Fresh xrefs contain 115 direct CALLs, not merely loader calls. Hooking selected call sites is narrower than function-wide coverage. Unwind DATA xrefs are not call sites. |
| Ordinary frame transition `B734C0`, CALL `140B7351A →B73310` | RCX reference, RDX stack `{XYZ12,mode32}`; incoming R8B requested mask 02 state. If old state differs, adds already signed vector, then changes only mask 02 at 73531. | Inner CALL observes XYZ before/after, **not** post-transition d3: bit write occurs after its return. Outer observation required for d3 before/after. |
| Generic scalar application `B73310`, stores `140B7335A/366` | All XYZ binary32 VADDSS. Reads operand DWORD+C as integer mode; updates linked extra/ACCA40 paths. R9 propagates into 28CCC40. | Fresh xrefs: ordinary CALL 7351A and derived CALL 18DC8D0. A 12-byte operand replacement loses downstream semantics. Do not assume downstream implicit inputs unused without qualification. |
| Ordinary virtual transition CALL `140B4A294` | RCX reference; RDX signed vector; R8B flag selected from target parent key; indirect target `[R9+7F8]`. | Ordinary table 144B95FB8 slot 144B967B0 resolves B734C0. Preserve dispatch, do not force ordinary target for derived references. |
| Reset `B22BF0`, stores `140B22C2D/3B` | Direct XYZ initialization and clear d3 mask 02. | Actual setter bypass; cannot be covered by B4E410 CALL list. |
| Plugin DATA `B230A0`, stores `140B23671/67E` | Direct restored XYZ/rotation fields and frame-state clearing. | Different load family, not automatically the saved-created case. Execution exclusion needs actual branch/lifetime evidence. |
| Placement/context `141A25420`, stores `141A25B2A/38` | Inlined setter-like comparisons, pre/post side effects, copies stack 60/64/68 XYZ directly to reference R12. | Concrete actual XYZ writer bypassing B4E410. Existence disproves an exhaustive setter-hook claim; applicability to the two Workshops remains unobserved. |
| Replacement/move `B48CA0`, restored extra `AF6A60`, other placement callers | Relevant branches/qualified input contexts in prior complete instruction export; AF6A60 ultimately passes converted input to B4E410. | Plausible alternatives retained; names alone do not establish which path executed. No all-alias writer proof. |
| Registration `17E2180` | Reads position and can OR d3 mask 02 even on no-world/failed lookup paths. | Flag transition can occur without an XYZ write. Frame bit alone is not evidence of translation. |
| Preparation 1856D10, grid AD0C3B onward | Preparation subtracts into separate output structure; grid consumes XY. | Excluded as direct reference 94 writers; adjacent stack word is not grid translation Z. |
| Center F4AB80 | RCX reference, RDX caller output 12; void. Copies fresh 8C/90/94; conditional extraBC+60/64/68 additions. | Consumer, not reference writer. Zero decision uses all three compensation components. Capture raw full vector and gate validity; missing extras differ from zero vector. |

Fresh B734C0 references contain no direct CALL. DATA references include ordinary
slot 144B967B0 and candidate slots 144C2D1D0,144C2DEF8,144CB1CC8,144CC8970,
144CC97E0,144CCA5C0,144CCB270,144CCBEB0,144CCCF48,144CCDC58,144CCF1F8,
144CCFF90,144CD1590. These require independent table/RTTI qualification before
patching; 148612F5C is metadata. A value scan alone cannot establish vtable type.

## Producer, command and application identity

ACD180 constructs vector from edge 8×100,edgeC×100 and edge 30 at
140ACD1DB–202. Immediate CALL 140ACD2C0 passes RCX reference, RDX parent,
R8 vector. Queued CALL 140ACD2D8 passes RCX service, RDX reference, R8 parent,
R9 vector into 18C28B0. That routine may apply immediately depending on thread
and global state; a producer function name is not proof of deferral.

The genuine queued branch allocates a command via CALL 1418C2982→22CDF60.
Its returned pointer becomes RDX and receives callback 18CE300 at+8, XYZ at+10,
reference at+20 and parent at+28 before queue publication atomics. The reference
is retained by native reference counting; the observer must not add its own
reference mutation. Producer/application join requires this command identity
and invocation/epoch evidence, not equality of reference/vector alone.

Fresh callback 18CE300 instructions establish application CALL 1418CE315→B4A0B0:
RCX=command+20 reference, RDX=command+28 parent, R8=command+10 vector.
Thus at that exact CALL `R8-0x10` is a source-qualified command identity.
After return, native code clears command+20 and releases the reference.
Capturing allocator return within a queued-producer invocation can link producer
to command; it needs TLS/nesting and exact caller association. Command address
reuse must not merge separate invocations. Deferred applications may use another
thread and may occur after producer retirement; unfinished pairs remain visible.

## Earliest identity and lifetime limits

At the creation setter, the native pointer/current FormID/base may exist while
Workshop ExtraData and its stable 64-bit identity do not. Preserve the generic
event population and attach later identity observations retrospectively.
Save25 tokens 822821/84B985, runtime FormIDs, raw pointers and Workshop identities
`f1517de43e171745` / `0efca066ee4c7b9b` are distinct namespaces. Prior
[comparison ledger](../workshop-z-restoration/comparisons.csv) supplies the scoped
join, not a numeric token-to-FormID rule. Parent+B0 may be zero while resolver
fallback exists; the enclosing query key is a separate source frame.

Use a load/session epoch plus native invocation sequence and observed identity
changes; retain pointer-reuse uncertainty if allocation/destruction coverage is
absent. Repeated pointer/base/FormID samples do not prove continuous lifetime.
Unchanged d3 does not prove no writes, and unchanged position does not prove no
setter invocation. Center equality proves current arithmetic only. A closed
covered interval needs established writer coverage and a qualified lifetime,
neither supplied by an installed-hook count.

## Distinct specialist contribution and remaining qualification

The specialist independently rechecked installed executable identity, found the
inlined direct position-store counterexample in 141A25420, recovered complete
native xrefs, established the 16-byte scalar application operand and post-call
d3 ordering, and exported the previously missing queued callback to demonstrate
a legitimate command-pointer application join. These findings informed primary
design before freeze. No third-party implementation was incorporated.

No live observation or full native ABI preservation test was performed by this
audit. Primary implementation/fixtures must qualify selected hooks, return and
floating-point state, stack forwarding, lossless durable transport, retrospective
identity joins and retirement. Even successful fixtures prove those mechanisms
within their fixtures; they cannot certify a global native writer set.
