# Witnessed D4D component and map sequence

Scope: PID 19676, pinned executable 1.16.244.0 and [native contract](native.md).
Preferred static VAs remain based at `0x140000000`; measured runtime image base
is `0x7ff7d35b0000`. Node/payload offsets below are byte offsets. Component and
slot ordinals are zero-based. FormID-sized words are numeric observations; BIOM
labels are compared with the pinned installed projection. [Sources](phase-b-sources.csv).

The common observed first key word is `0x0005de4c000100d2`, matching owner
`0x0005de4c`, the copied runtime type word `0x00d2` and flag `0x10000` under
the native range constructor. Each second key equals the row's observed BIOM
word in this instance. The upper range bound and unsigned increasing order pass.
D4C predicted BIOM order conditionally; it did not predict these runtime type/key words.

| Ordinal / capture | BIOM word / second key | Root word | Slots 0, 1, 2, 3, 4, 5 |
|---|---|---|---|
| 0 / 359 | `0x0007d721` | `0x00000000` | `0, 0, 0, 0, 0, 0x000083ec` |
| 1 / 360 | `0x000fd00b` | `0x000057cf` | `0, 0, 0, 0, 0, 0x000083ec` |
| 2 / 361 | `0x000fd00f` | `0x000057c1` | `0x000057c4, 0, 0, 0, 0, 0x000083ec` |
| 3 / 362 | `0x001297f1` | `0x000057cf` | `0, 0, 0, 0, 0, 0x000083ec` |
| 4 / 363 | `0x0017b85d` | `0x000057d5` | `0, 0, 0, 0, 0, 0x000083ec` |
| 5 / 364 | `0x0018a8a0` | `0x000057d6` | `0x000057d8, 0x000057db, 0, 0, 0, 0x000083ec` |
| 6 / 365 | `0x002636ba` | `0x000057c1` | `0x000057c4, 0, 0, 0, 0, 0` |
| 7 / 366 | `0x0028acd1` | `0x000057d5` | `0, 0, 0, 0, 0, 0x000083ec` |

Here `0` denotes the observed null word `0x00000000`; it is not a missing field.
All six words are copied from node `+0x74..+0x88`, corresponding to payload
`+0x54..+0x68`. Slot 5 is the sixth word at node `+0x88` / payload `+0x68`.
That word lay beyond the earlier D4A diagnostic's `0x68`-byte component copy.
The new capture supplies it directly rather than treating that earlier omission
as evidence of zero. Upstream initialization of the word remains unestablished.

## Array transitions and origin reconstruction

Use `Wa` for component 2 slot 5 and `Wb` for component 7 slot 5; both words are
Water `0x000083ec`. Tungsten is `0x000057c4`, and selected Chlorine root is
`0x000057d5`. These explanatory occurrence labels are not native identifiers.

| Decisive transition | Observed values and supported interpretation |
|---|---|
| Component 2 → next boundary 362 | Under root `0x000057c1` (installed Lead label), array `[Tungsten, Wa]` is installed; staging becomes empty. |
| Component 6 → next boundary 366 | Its own Tungsten replaces the Lead-keyed entry. The earlier `[Tungsten, Wa]` is displaced into staging; it is not the new component 6 Tungsten that reaches the final Chlorine entry. |
| Component 7 → cleanup 367 | Wb appends to staging, then root `0x000057d5` exchanges arrays. Chlorine receives `[Tungsten, Wa, Wb]`; its prior three-Water array is displaced into final staging. |
| Return 368 | Completed map retains that exact Chlorine array. Cleanup does not merge the discarded prior array back. |
| Ready 369 / calls 370–373 | Root insertion produces a root-plus-supplement list. The copied sorted pointer array and every ordinary CALL agree as Water, Water, Tungsten, Chlorine. |

The offline method propagates distinct component/slot tokens through these static
append/exchange rules and checks the resulting word arrays against every observed
map and staging boundary. Independent reviewer replay repeats the token propagation
separately. Individual append allocator outcomes and invisible all-writer/ABA
exclusion are not claimed. No operation mismatch was detected in this trace.
The pair of identical Water pointers cannot identify which post-sort Water CALL
corresponds to Wa versus Wb; their multiplicity and final map order are preserved.

| Ordinary capture | Main-file IRES | Rarity byte | Effective weight bits |
|---|---|---|---|
| 370 | Water `0x000083ec` | 6 | `0x00000000` |
| 371 | Water `0x000083ec` | 6 | `0x00000000` |
| 372 | Tungsten `0x000057c4` | 1 | `0x3e4ccccd` |
| 373 | Chlorine `0x000057d5` | 0 | `0x3f800000` |

Every copied IRES has the expected type and Starfield.esm file provenance. Both
Water calls are ordinary zero-weight generation operands; they establish neither
two Water veins nor one atmospheric plus one terrestrial source. No density,
occurrence-quota or fallback explanation is needed for this sequence. Absence of
such an explanation here does not establish whole-engine impossibility.

The source and Workshop joins are described in [the result](phase-b.md). Generation
thread/lifetime/invocation and consumer thread/lifetime/updater are distinct.
Equal retained source bytes, candidate correspondence or matching names do not
establish a historical generation epoch or persistence authority. This result is
OBSERVED-INTERNAL, not a validated mod integration point.
