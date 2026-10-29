# D5P frozen contract and architecture decision

2026-10-29, Australia/Sydney. [Governing brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5P_SFSE_retained_population_observer.md).
AC1–AC8 are frozen without amendment. This is Phase A only. Phase B, B6,
installation, game execution and publication remain unauthorized.

The selected design observes natural calls and completed owned state. It does
not use debugger exceptions. The decision follows the D5C source-pointer map,
distinct visited key and D5L copy-failure analysis in the [native ledger](native.md).
The D5L–D5O failed runs establish failures of those retail acquisition methods;
they do not establish that an in-process hook is reliable.

| Route | Evidence value | Decision and qualification burden |
|---|---|---|
| Existing SFSE task/message interfaces | Startup and scheduling; no selected-source decision or geometry callback was found in the inspected header. | Reuse the approved public load interface, not a task callback as a causal witness. |
| Function entry/exit only | A provider return can show retained state but cannot certify successful point copying or distinguish an earlier visited bypass. | Use entry wrappers for conservative lifetime invalidation, not as a substitute for decision/copy evidence. |
| Targeted natural CALL wrappers and one inline branch witness | Preserve original calls and capture actual lookup, query, mask, append and synchronous generation return. | Selected. Five CALL sites, one visited branch and five independent invalidation routes require native ABI, relay and transport qualification. |
| Fourteen external breakpoint sites | Existing controls and failed retail evidence. | Rejected as the implementation architecture. No INT3, DR register, single-step or debugger event pump is used. |

The five call sites are module RVAs `0x79fccb`, `0x79feaf`, `0x79ff18`,
`0x79b8e8` and `0x79aced`. The visited branch is `0x79fca3`. Generation return
is checked while the provider still holds ProcGen protection. Append return is
compared with its temporary geometry, then with the completed owner's region;
wrapper insertion alone supplies no successful construction evidence.

Each extra lifetime detour has a separate reason: reset `0x79ddf0`, destruction
`0x79d910`, map erase `0x975030`, Grid clear `0x9829b0`, and standalone source
retirement `0x982b70`. Entry and exit advance one conservative observer epoch;
an in-flight invalidation closes joins. This deliberately invalidates unrelated
sources too. A reset entry is not presented as the engine's post-clear epoch.
These tokens qualify a bounded observed native lifetime, not a universal census
of every alias or writer. First observed is never first-ever.

The implementation adapts the project's fixed-site relay, hash guard and
resident-hook approach, and the sibling observer's thread-local scope and
bounded producer/consumer patterns. It does not copy CommonLibSF, XMake package
sources or the sibling's dependencies. Exact source hashes and revisions belong
in the D5P source ledger and build manifest. The sibling's existing passive
travel success is evidence for its own observer, not this implementation.

The user explicitly approved extending the pinned SFSE `PluginAPI.h` MIT use to
D5P, retaining copyright, permission and disclaimer. This extends the EXP0002
scope only for that unchanged header; it does not approve SFSE runtime source or
CommonLibSF incorporation. The [permission record](../../PERMISSIONS.md) retains
the exact grant.
