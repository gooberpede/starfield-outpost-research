# Operator save identification

Read [save-identities.csv](save-identities.csv) for full SHA-256, original source,
read copy and new protected copy. [cases.csv](cases.csv) joins **every case** to
one of those three identities. A filename is an offline locator, never a menu ID.
The decoded header location is the saved player location, not every outpost.

| Cases / research aliases | Full original .sfs filename | Character / decoded menu fields | Candidate current English menu time |
|---|---|---|---|
| P1/R1: Kreet25 / Save25; SOR-002 and SOR-003 | `Save25_D6036588M417474696C61204B6972616C79_000231_20261009102224_4_0_4.sfs` | **Attila Kiraly**; **Kreet - Outpost**; level **4**; **2h 31m** | **10/9/26, 9:22:22 PM**, UTC+11:00 |
| P2: Kreet39 / Save39 | `Save39_D6036588M417474696C61204B6972616C79_000209_20261020003045_3_0_4.sfs` | **Attila Kiraly**; **Kreet - Outpost**; level **3**; **2h 9m** | **10/20/26, 11:30:44 AM**, UTC+11:00 |
| P3/P4/R2: Save52 / HIST-0267 | `Save52_BA75E3CDM43616F205472616E_580743_20260818064541_319_15_4.sfs` | **Cao Tran**; **Jemison - The Lodge**; level **319**; **58d 7h 43m** | **8/18/26, 5:45:40 PM**, UTC+11:00 |

Character/location/level are first-stream header observations using the owned
[save-menu reader](../../../save-analysis/scripts/save_menu.py), version 1.0.0.
Playtime is its documented header-text projection. These are decoded fields,
not fresh menu screenshots. **Save kind is UNKNOWN** for the actual displayed
label in each case: the reader's `SAVE`/manual candidate comes only from the
filename prefix. Confirm SAVE versus AUTO/EXIT/QUICK during the bounded future
identification step. No name or kind was decoded from the filename's hex text.

Dates above use freshly checked current original file-last-write times and the
existing menu model, converted using
the **current requested menu offset +11:00**, including the August save. They
are not inferred from filename timestamps, not header FILETIME, and not a
reconstruction of the offset originally used in August. Save25's hash-bound
historical original mtime in `.local-work/two-outpost-anchor/extract-03/manifest.json`
would display **9:22:24 PM**, whereas its current hash-identical original has
mtime ending in **9:22:22 PM**. Both are preserved in the table/receipts;
the current value governs the instruction. Its extraction copy has another
retimed mtime and must not supply a menu label. No save timestamp was changed.
Menu locale, OS offset, restoration/retiming and actual rendered time remain
uncertain; Save39/52 filename seconds differ from the mtime display by one.
Retain exact identity and document any discrepancy rather than changing the file.
The bounded current-directory first-stream census parsed **271/271** save headers
and found one row matching each selected current character/location/level/playtime/
modeled timestamp tuple; those matches have the selected SHA-256 values. This
does not establish screenshot labels, current save kind or future absence of
collisions. The initial historical-time census's zero Save25 match is preserved
alongside `menu-current.json` and `menu-collisions-current.json` locally.

The source/protected ledger is exact, including unavailable original locators.
Fresh copies of the three read inputs are under
`.local-work/resource-geometry-live-prep/protected/`; source and copy hashes agree.
Earlier Save25 extraction and Save39 protection remain unchanged. Hashes identify
bytes; timestamps identify possible menu rows. **Save41 is HIST-0255 and is not
Save52/HIST-0267.** No new SaveNN alias is assigned to a named outpost.

## Bounded future identification gate

PROSPECTIVE — NOT AUTHORIZED. Before launch, under a separate RG2-B approval,
hash the exact original/protected file and inventory current Saves metadata.
In Load → character select, choose **Attila Kiraly** or **Cao Tran** and match
location, level, playtime, save kind and displayed date together. Photograph the
row and character header. Do not select by ordinal, `Save25` or `HIST-0267`.

If two rows are visually identical, the menu alone cannot maintain the hash join.
Do not guess. The smallest disambiguation is a separately approved isolated
loadable copy set with an explicit source/hash→installed-copy manifest and
preserved timestamp handling; this entails save-directory writes and requires
RG2-B to authorize them. No renaming, removal or installation occurred in RG2-A.
If actual metadata differs, retain the photograph and original pins and stop
that case for reconciliation. An unavailable original can be supplied only by
the hash-matched protected copy under that same approved handling protocol.

## Travel and exact outpost identity

| Case | Intended user-facing target / route from saved player location | Saved identity checks before sampling |
|---|---|---|
| P1 | Kreet, **SOR-002**. Save25 player is at SOR-003 parent `84b996`, near `(355.113800,2457.793457,-32.662582)`. Use the named SOR-002 map marker if present. Otherwise travel in the same qualified source plane toward ΔXY approximately `(-232.413345,-2184.747223)` from that player position; heading-to-compass conversion is UNKNOWN. Never walk by this vector without qualifying axes. | ordinary beacon saved token `822821`, parent `822834`, Workshop bytes `f1517de43e171745`, center `(122.700455,273.046234,18.352507)` |
| P2 | Kreet, **Kreet Outpost 1**, Lab vicinity. Save39 player `(1087.219849,1180.014771,-19.421165)` is ~1.57 XY units from the beacon: ΔXY `(+1.539917,-0.286255)`. Confirm the nearby beacon's displayed name; do not fast travel to another Kreet outpost. | beacon `841421`, parent `839160`, Workshop `41da48765780cc0c`, center `(1088.759766,1179.728516,-18.834455)` |
| P3 | From **Jemison - The Lodge**, starmap → **Feynman V** → named **Feynman V Cu Co Ni IL** outpost marker. Actual fast-travel availability and landing/arrival offset UNKNOWN; if unavailable, record the restriction and stop for route review. Do not substitute the other Feynman site. | beacon `83388f`, parent `84ec80`, Workshop `c3a5866f4cfcf585`, center `(83.460693,67.887711,-0.153640)` in saved 2b site plane |
| P4 | From the Lodge, starmap → **Carinae III-a** → **Carinae III-a Rc Fe**. Same conditional map/travel gate. It is not Carinae III-c or Carinae V-c. | beacon `82be17`, parent `84655c`, Workshop `91bac704da9b1e34`, center `(86.638062,70.479126,6.211388)` |
| R1 | Save25 player is already near **SOR-003**, Kreet. Confirm name before leaving. | beacon `84b985`, parent `84b996`, Workshop `0efca066ee4c7b9b`, center `(356.820404,2459.058594,-31.890842)` |
| R2 | From Lodge, starmap → Feynman V → **Feynman V Cu IL F**; distinct from P3. | beacon `84e101`, parent `859b49`, Workshop `b0e207c2dee2c1b6`, center `(81.190742,90.277481,5.303274)` |

Saved three-byte tokens, Workshop identifier bytes and live RefIDs are different
domains. They cannot be pasted as current console IDs. Reacquire the selected
beacon reference after load and establish name/body/center association before
using it as a frame anchor. Existing [ownership research](../workshop-membership/report.md)
supports ordinary construction/Workshop associations, not complete active-player
membership. User construction provenance, ordinary named Workshop and body/frame
joins support these candidates; current ownership/menu access remains a live gate.
