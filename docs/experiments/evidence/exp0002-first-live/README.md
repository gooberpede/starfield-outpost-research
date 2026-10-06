# SOR-EV-0003 — First primary EXP0002 live attempt

2026-10-06 Australia/Sydney. SOR-D-0012; [run record](../../EXP0002-gate-b-run.md). Authored index REVIEW-REQUIRED; all listed artifacts LOCAL-ONLY. No raw save, process/module data or proprietary content is promoted into Git. Evidence completeness: A0 anomaly complete, primary sequence incomplete. No membership/coordinate acquisition. Target exited normally; protected parent/backup unchanged. Observer retired through user-managed Vortex.

Paths below are relative to ignored `.local-work/exp0002-gate-b/`. Archives retain original bytes. post-exit.json correlates source/copy hashes and metadata, records the new incidental exit save and one missing older exit-save filename, and states limits. The exit save is not a primary checkpoint. session-start.json and package receipt preserve their creation-time pending states; the run record supplies subsequent outcomes. No debugger, manual checkpoint saves, or construction.

| Local artifact | Bytes | SHA-256 |
|---|---:|---|
| 20261006T060326Z-preflight.json | 48958 | `51ae5ba917b61ff6521bc9a6c85b22dac4e4ba6c10256c36e9e0975a33267636` |
| config-lf-package.json | 1271 | `18a4aa3a81fc6774c592a9314351f7cb27c5377f7c9d9450769a0a1bee033705` |
| session-start.json | 1207 | `92cc281830aeb82925213b5affcd34b26b07f73ab35861f79e6b0065f7ae1206` |
| post-exit.json | 84177 | `0189a343b77919608776a9132e2780c8099f080f9b7bf2a716f298e34e9396ba` |
| archive/observer/A0-anomaly.json | 612 | `ee099381fe821da7e42d9888463a10d97a2cd5e1637717c17c339173ea398fd5` |
| archive/observer/modules.json | 4129 | `e67cdb78faa98dce75b8e4a067ebce4e978108a872bbab7bbe91b1d76c5588d1` |
| archive/observer/ready.json | 219 | `e3e48e48ea5c73691ce662373749f91372724284ccf979885f63b498dc30d7c1` |
| archive/observer/request-A0.txt | 3 | `123d98c79967fdf88225a0650aa3212b3debc5c3240629d2cf4158c687a3267f` |
| archive/sfse-logs/sfse.txt | 1088 | `5352ce6a2f5c8bc43ec8a430188a26af8bcb1219585ff12f74c510438f791554` |
| archive/sfse-logs/sfse_loader.txt | 1293 | `0910ab461a844040920065dcb5d68f6e322d7542eb57c138ea6826a9d1c0d300` |

The incidental save's private filename/path appears only in post-exit.json. Neutral artifact identity: incidental exit sample, 2,077,984 bytes, SHA-256 `fe3d299110bbf588676fc570b01b27ea2df7a08a079ef525579e16207ba91b4d`. No semantic parsing. Source-reported SFSE notification diagnosis is credited separately as SOR-S-0118, not conflated with runtime proof. Initial final log showed startup messages; after exit it also showed data-load messages 2/3, with no recorded save-load 6/7. Log absence alone cannot establish all dispatch behavior.

Four packaging and thirteen timestamp tests passed. The earlier 125 native/26 output tests were not rerun: native sources and DLL are unchanged. They did not qualify notification delivery, actual ZIP newline bytes, or PowerShell locale conversion; the first live attempt exposed those gaps. Full local review diff, final validation and hashes are in this evidence root; no integration/publication approval is implied.
