<!--
Saved verbatim by the main session on 2026-11-07 at the user's request: the assembler agent could not write .md files
in this session and returned this report in its hand-back. Text unchanged, except that a model name in the byline is replaced by `claude`.
-->
## bias_tree_noab_pd assembly (slot 7): done

The cell is finished and both checks pass. Both PDK DRC decks give 0 items, and LVS against the source netlist says "Circuits match uniquely" with no property errors. The cell is **32.21 x 18.68 = 601.7 um2**, against 1972 um2 for the naive cell (-69.5 %). The two halves' boxes take 490.3 um2 of that (81.5 %).

All files are in `/home/user/s2d2s_c5_tree/macros/slot7_testplatform/layout/tree/assembly/`. I changed nothing outside it, ran no git command that changes state, and deleted `scratch/`. The `tree_pmos` and `tree_nmos` sub-cells XOR to 0 against the two halves' GDS files.

### Floorplan (cell coordinates, origin at the lower-left corner)
```
y 18.68 +====================== vdd rail M1 0.00..32.21 x 17.32..18.68 (tree_pmos plate + N tie, extended) ======+
        | [ tree_pmos  R0 @ (0.405,10.25)  20.985 x 8.43 ]  | fan-out bay x 21.39..32.21: M1 risers  -> en_3v3_b |
        |                                                    | x 28.21/28.71/29.21/29.71/30.23/30.84  -> iref     |
        |                                                    | M2 pin stubs to the right edge         -> vbpc     |
        |                                                    |                                        -> vbp,vbn  |
        |   two M2 tracks inside tree_pmos's bottom margin   | vbnc = tree_pmos's own M2 lane, extended -> vbnc   |
y 10.25 +----- channel 0.52 (ThickGateOx filled; en_3v3_b track) ----------------------------------------> en_3v3  |
y  9.73 | three M2 tracks inside tree_nmos's free top margin (iref, vbn, vbp)                                    |
        | [ tree_nmos  R0 @ (2.31,0.78)  32.21 x 9.73 : s | d A B C B A B A B A C A B d | N N N N N | c ]          |
y  0    +====================== vss rail M1 0.00..32.21 x 0.00..1.01 (tree_nmos plate + p+ tie) =================+
```
- **Width:** set by `tree_nmos`. A bay of about 10.8 x 7.1 um beside `tree_pmos` is unavoidable; the pin risers and stubs use it, and Metal3+ stays free there.
- **Height:** 9.73 (NMOS) + 0.52 (channel) + 8.43 (PMOS).
- **PMOS x offset (0.405):** chosen so that its ni pin falls inside the NMOS ni stub, its iref pin over the NMOS iref riser, and its vbn pin exactly 0.18 (M1.b) from the NMOS ni stub.
- **PMOS y (10.25):** the highest track (en_3v3, 10.76..10.96) ends 0.21 below `tree_pmos`'s first Metal2 lane. The PMOS NWell is 2.79 um above the NMOS N+ (NW.d1 needs 0.62).
- **No mirroring:** with the PMOS half mirrored, vbn would have lined up, but iref, en_3v3_b and ni would each need a run of about 29 um.

### How each joining net is routed
Tracks are Metal2, 0.20 wide on a 0.41 pitch (horizontal); drops and risers are Metal1 (vertical).

| net | route | drawn M1 / M2 (um), vias |
|---|---|---|
| ni (internal, no pin) | one straight M1 bridge, 0.21 x 0.52 | 0.52 / 0, 0 |
| iref | PMOS pin drops to an M2 pad on the NMOS iref riser (1 via); track y 8.59 to riser x 28.21; pin | 8.10 / 32.06, 3 |
| vbn | PMOS pin drops to track y 9.00; via onto the NMOS vbn stub; that stub rises to the pin | 4.70 / 30.25, 3 |
| vbp | NMOS vbp stub and the PMOS second vbp gate column both drop to track y 9.41; riser x 28.71; pin | 5.55 / 21.04, 4 |
| en_3v3_b | NMOS M2 riser goes up into track y 9.94; PMOS pin drops onto it; riser x 29.21; pin | 7.20 / 32.87, 3 |
| vbpc | via inside the PMOS pin stub; NMOS stub raised; track y 10.35; riser x 29.71; pin | 5.50 / 31.91, 4 |
| en_3v3 | NMOS M1 stub rises past the en_3v3_b riser to track y 10.76, which runs straight to the edge | 1.28 / 33.16, 1 |
| vbnc | `tree_pmos`'s vbnc M2 lane (it reaches the PMOS right edge) extended to a riser on the NMOS vbnc bar; pin | 2.50 / 11.16, 1 |

### Pins
| name | layer | box (um) |
|---|---|---|
| vdd | Metal1 8/2 + 8/25 | (0, 17.32; 32.21, 18.68), full top edge |
| vss | Metal1 8/2 + 8/25 | (0, 0; 32.21, 1.01), full bottom edge |
| en_3v3_b | Metal2 10/2 + 10/25 | (31.78, 16.445; 32.21, 16.735) |
| iref | Metal2 | (31.78, 15.545; 32.21, 15.835) |
| vbpc | Metal2 | (31.78, 14.645; 32.21, 14.935) |
| vbp | Metal2 | (31.78, 13.745; 32.21, 14.035) |
| vbn | Metal2 | (31.78, 12.845; 32.21, 13.135) |
| vbnc | Metal2 | (31.78, 11.945; 32.21, 12.235) |
| en_3v3 | Metal2 | (31.78, 10.715; 32.21, 11.005) |

- The signal stubs are 0.29 wide with pin shapes 0.43 long, the same as `oa_core_pd` and `bg_core_pd`. The gap between neighbouring stubs is at least 0.61 um.
- Only Metal1 and Metal2 are used; Via2 and everything above are empty.

### Rails, ties and latch-up
- **Ties:** one N tie (Activ 1.025..20.77 x 17.76..18.06, inside the vdd rail) and one p+ tie (0.52..31.69 x 0.27..0.57, under the vss rail). No ties were added.
- **Latch-up (20 um limit, `check_tree.py`):** the farthest P+ in NWell is 6.89 um from the N tie (34 shapes). The farthest N+ is 8.89 um from the p+ tie (43 shapes). LU.a, LU.b, LU.c and LU.d are all 0 in the decks.

### DRC
Both decks give 0 items: the main deck runs 333 rules (feol, beol, deep mode) and the maximal deck reports 0 errors ("maximum rule set"). Logs in `checks/`:
- main deck: `drc_bias_tree_noab_pd.log` / `.lyrdb`
- maximal deck: `drc_bias_tree_noab_pd_max.log` / `_max.lyrdb` / `_max.out`

### LVS
Run with `sak-lvs.sh -d`, Magic + Netgen, against `checks/bias_tree_noab_pd_source_ref.spice`. `make_ref.py` builds that file by copying `bias_diodes` and `bias_tree_noab_pd` line for line from the source files.
- **Result:** "Circuits match uniquely". 14 devices after merging (NMOS 22→8, PMOS 17→6), 10 nets, and `bias_diodes` was flattened.
- **Property errors:** none; the only line containing "property" is "Resolving symmetries by property value".
- **Log:** `checks/lvs/bias_tree_noab_pd.magic.lvs/bias_tree_noab_pd.lvs.out` (stdout in `checks/lvs.stdout`).
- **Negative test:** with the ni bridge removed, LVS reports "Netlists do not match" (11 against 10 nets) and returns rc=1.

### Files and sha256
- `bias_tree_noab_pd.gds`: **704b21ce7540c9925b82d95a89f7a69957e1bd71b5bac60a1186930f786c4356**. Two builds give the same bytes; the second build is compared byte for byte in `run_checks.sh`.
- `build_tree.py` (generator; it reads `../pmos/tree_pmos.gds` and `../nmos/tree_nmos.gds` and instantiates them; top cell `bias_tree_noab_pd`, no new sub-cells, so no `tree_asm_` prefix was needed).
- `make_ref.py`, `check_tree.py` (layers, pins, latch-up, area), `render_tree.py`.
- `run_checks.sh`: build ×2, both DRC decks, LVS, checks, pictures; sha256 list in `checks/sha256.txt`.
- Pictures: `bias_tree_noab_pd.png` (top-level routing coloured per net) and `before_after.png` (naive and new at one scale).
- Inputs read: `tree_pmos.gds` 7176896d…d962, `tree_nmos.gds` 9a193aba…91f4.

### Decisions
- **Hand-placed tracks:** I placed the eight nets on fixed tracks rather than porting A2's grid router; with this few nets the coordinates fit in one table in `build_tree.py`, with assertions on the constraints.
- **vbp through the second gate column:** vbp joins at the PMOS's unlabelled second vbp gate column. The labelled vbp pin on the left of `tree_pmos` stays unused; it is connected inside the cell.
- **vbnc through the PMOS's own lane:** vbnc uses `tree_pmos`'s own Metal2 lane, extended outside the cell (no edit inside the cell). That saves a track.
- **ThickGateOx fill:** filled only across the 0.52 gap, over `tree_pmos`'s width, so the oxide merges (the minimum space would be 0.86).
- **Pin order** (bottom to top): en_3v3, vbnc, vbn, vbp, vbpc, iref, en_3v3_b.

### Problems and notes for the top level
- No DRC or LVS iteration was needed.
- **Inherited from `tree_nmos`:** its Metal2 en_3v3_b riser and the new en_3v3 track start 0.04–0.045 um from the left edge, and its vbnc Metal1 bar is 0.06 from the right edge. A neighbour needs the usual spacing beyond the edge.
- **NWell near the left edge:** the PMOS NWell starts 0.405 from the left edge, so a neighbour's N+ in thick oxide must stay at least 0.215 outside that edge (NW.d1 0.62).
- **Labels:** the half-cells keep their own internal labels, including ni; the extractor flattened everything and they caused no conflict.
- **Not part of the cell's verification:** a backannotated sheet and simulation. The devices are exactly those of the source netlist, merged in parallel.
