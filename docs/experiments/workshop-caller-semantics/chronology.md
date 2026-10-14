# Cross-session chronology and frequency

[Report](report.md), [reproducible tool](../../../research/workshop-caller-semantics/README.md),
[pooled summary](frequency.csv), [five-second bins](bins.csv).
Full per-event CSV, per-thread distributions and action receipts remain local in
`.local-work/workshop-caller-semantics/chronology-02/`.

## Timebase and interpretation

Event QPC uses 10,000,000 ticks/second in both ready receipts. Relative seconds
are measured separately from each session's earliest captured event; they are
neither load-relative nor shared between sessions. Intervals sort QPC within
each group, never journal order. Percentiles use the lower empirical rank
floor((n-1)×p); median uses the conventional midpoint. Pooled intervals combine
threads and cannot estimate the duration of a single update loop. Per-thread
distributions are retained independently.

050 health has fresh `health_utc`/QPC pairs, but this artifact deliberately keeps
native relative timing and observed operator UTC separate. 060 health `utc` is
the session-start identity field repeated unchanged (plugin.cpp39); it cannot
calibrate wall-clock event times. ACK `ack_utc` is fresh but carries only captured
sequence counters. ACK prefixes therefore bound serialized emissions, with
non-atomic gameplay/worker and scheduling uncertainty. No invented UTC-QPC affine
mapping is used. There is no recorded input-idle interval or actual camera
activation timestamp. Settled testimony is not an inactivity detector.

| Caller / identity | Returns with coherent return identity | TIDs | Relative first–last seconds | Pooled median / maximum interval |
|---|---:|---:|---|---|
| 050 AD0C36 /002 | 20 | 1 | 92.3586714–92.3719496 | 0.6794 ms /0.7912 ms |
| 050 AD0C36 /003 | 20 | 1 | 92.3588635–92.3721342 | 0.6797 ms /0.7934 ms |
| 060 F4A1D4 /002 | 5,280 | 20 | 758.0716176–830.7078376 | 0.1950 ms /16.3236586s |
| 060 F4A1D4 /003 | 11,542 | 21 | 518.4989131–1175.4772609 | 0.1959 ms /99.3975681s |
| 060 F498F1 /002 | 1 | 1 | 829.6998038 | No within-identity interval |
| 060 F498F1 /003 | 1 | 1 | 743.9361280 | No within-identity interval |

Two further F4A1D4 returns have incoherent identity and are retained as a separate
group. Two other pairs have incoherent before records but coherent return records,
which this table counts for timing only. Four-pair arithmetic quarantine remains
unchanged. 050 all 40 calls occur across 13.4628 ms, with actual Q/E/callback
ancestry verified by fresh replay. 060 all center scopes have parent 0; unhooked
native ancestry and queued job identity are unavailable.

## Action and emission chronology

Observed UTC below is UTC+00, not Sydney wall time (add 11 hours on 2026-10-13).
Counts cover ACK emission-prefix differences, not precisely the named gameplay
action alone. 006 numbers in the original receipts refer to schema 6, not a new run.

| Boundary / fresh ACK UTC | Captured sequence | Centers since prior ACK |
|---|---:|---|
| Menu, 08:58:35.592 | 142748 | 0 |
| Initial Save25/003 settle, 09:05:31.281 | 264112 | F4A1D4:5632 coherent 003 +1 incoherent |
| After travel to 002,09:08:12.963 | 364874 | F4A1D4:5204 coherent 002,176 coherent 003 +1 incoherent; F498F1:one 003 |
| After return 003,09:11:03.474 | 476992 | F4A1D4:76 coherent 002,5590 coherent 003; F498F1:one 002 |
| Retirement tail | 562326 | F4A1D4:144 coherent 003 |

The last tail includes waiting, analysis/operator communication and STOP latency;
it is not proven idle/free-camera exposure. F498F1 appears once per departing
identity within travel-spanning windows; exact gameplay activation is unrecorded.
050 local 003→002→003 controls have zero captured events; one new landing has
sequences 1–52, return has 53–1194. Operator return markers 03:29:59.396410–
03:31:58.717733 bracket the burst. Retirement is separately recorded in both
original `retired.json` files; no new live session occurred.

## Bursts, gaps and observer duration

060 thread 40180 has 570002 before samples across 1.4151371 s (median1.4134 ms),
but 1050003 return samples span 327.9348087 s with a 325.317569 s gap. Thread 9956
has only 50003 before samples across 599.1078717 s (median8.2626224s). The mixed
population contradicts a uniform single-thread periodic loop explanation.
Descriptive one-second gap counts are 41 for coherent 002 pooled returns and 422
for 003. This threshold summarizes gaps; it is not a capture stop quota or an
engine-frame assumption. Five-second bins expose dense clusters without hiding
the sparse tail. Static ancestry must assign purpose; timing alone cannot.

060 before→return QPC brackets include snapshotting, spool-lock contention,
synchronous writes before native entry and scheduler delay. They are not pure
F4AB80 runtime. For example, thread 49532/003 has a maximum 1.0162258 s bracket
while its median is 0.312 ms. This establishes long instrumented elapsed brackets,
without identifying the cause or proving a reference-state mutation. 050 has no
equivalent before timestamp; comparing native helper costs across versions would
be invalid. Complete retired journals show no transport hole; zero events in a
period still does not imply no gameplay work or no uninstrumented native call.
