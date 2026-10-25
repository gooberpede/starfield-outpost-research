# Demand timing and observation windows

[Native register](native.md), [acquisition matrix](acquisitions.md),
[D5B session account](../resource-combined-acquisition/phase-b.md). Times below
are UTC on 2026-10-25. Add 11 hours for Australia/Sydney. Journal SAMPLE times
are debugger-side FILETIME measurements, not instruction-execution timestamps;
PHASE records themselves have no timestamp. Operator reports are kept separate.

| Boundary | Evidence-supported time/order | Limit |
|---|---|---|
| Process/main menu | Process starts 01:48:31.4557036; wrapper dispatch 01:50:05.167215; operator confirmed main menu with no save loaded before attachment | Process and dispatch are operational receipts. Main menu is an operator report; no successful screenshot. |
| First recorded provider SAMPLE | Capture 1 at 01:52:10.519614, before both PHASE records | Evidence begins after launch/bootstrap. This is an ordinary provider request on an unqualified source, not the selected source's birth. |
| Save52 load / direct travel / landing | Operator was instructed to load once, travel directly to second Feynman V and enter Build Mode once | Separate start/completion times and load-completion witness are absent. The journal cannot assign generation to load versus travel from proximity alone. |
| Last producer sample before consumer phase | Capture 12204, selection stage, 02:54:00.528309 | Producer instrumentation remained active until the consumer entry trap. The following 13.289911-second sample interval is not proved to be wholly unarmed. |
| First phase boundary | Journal line 36808: `consumer_mode=true`, zero invalidated constructions, `LOSS_NO_NATIVE_LIFETIME_JOIN`; immediately before entry 12205 at 02:54:13.818220 | All threads switch to four consumer sites. Construction sites are unavailable during this phase. Zero cleared construction stacks is not zero past construction or an epoch witness. |
| Consumer evaluation | Entry 12205 → ACCEPTs 12901/12906/12907 → transfer 15119 at 03:05:16.875308 | Source/Workshop-bound geometry consumption. At least 11 minutes 3.057088 seconds between entry/transfer samples lie within the consumer phase; debugger pauses are included. No timing for actual uninterrupted engine work is inferred. |
| Second phase boundary | Journal line 45553, after transfer's positive ACK: `consumer_mode=false`, same explicit lifetime-coverage loss | Producer sites restored; pending tokens/stacks reset globally. No later SAMPLE occurs. This boundary cannot repair the first blind interval or prove no intervening replacement. |
| Operator completion / exit | Completion/STOP file 03:05:48.998957; wrapper exits 03:05:52.911425; process absence checked 03:08:37.128430 | Operator says “In Build Mode now.” Captured transfer precedes that receipt; exact UI entry/landing time remains unknown. Exit is declared controlled disposal. |

The **two recorded phase transitions** are two lifetime-coverage breaks, not
evidence of two measured periods when execution ran with no hardware sites
armed. The continuous consumer phase between them blinds construction. Producer
mode also rotates the selection probe, replaces provider-entry watching with
provider-return watching on a thread during generation, and swaps the updater
site for ordinary CALL watching. It never probes the source-map hit/miss decision.
Nested requests and unsampled stage ordering can therefore prevent a qualified
chain even outside the global consumer phase. Thirty-six generation entries on
other sources do not validate continuous selected-source construction coverage.

Construction could have occurred before the relevant thread/provider arming,
during load/travel/terrain preparation, in a producer scheduling gap, or during
the consumer phase before its source scan. D5B does not date the earliest
selected-source presence. Geometry must exist by its ACCEPT, but there is no
earlier measured birth bound. A missed construction and same-process reuse can
both be true; these are not mutually exclusive histories.

For source `0:37536:20928:0029d20e`, **the earliest supported ordinary demand
candidate is coordinate/cell preparation that enumerates its live descriptor,
potentially during arrival before Build Mode**. No static timestamp or generic
landing callback proves it is the first request. The earliest practical continuous
observation point already exercised operationally is main-menu attachment and
verified arming before the operator's Save52 load instruction. Retaining only
source-specific provider/decision probes through direct travel avoids D5B's
global consumer switch. Starting at Build Mode risks missing the highest-value
ordinary-demand window; starting after landing may also be too late.

Main-menu arming is deliberately earlier than the expected arrival demand, to
avoid assuming load timing. It is not a comprehensive load observer or proof of
source absence before attachment. If the first qualified event is a hit or
visited skip, construction history remains unknown and calls for a bounded
lifecycle/presence follow-up. The geographic label must be derived from copied
chart/descriptor/source fields and owner; pointer equality alone is insufficient.
Manager pointer, ProcGen owner, source pointer, visited key, process/thread and
sampled lifetime all need separate records. A source allocation can be reused
after reset/teardown; geometry equality supplies no lifetime fence.
