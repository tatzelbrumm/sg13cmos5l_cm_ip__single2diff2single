<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Layout cells for the pad buffers and their bias (`pad_buffer_cells`)

2026-10-26. Drawn by Claude (Opus 5.5) for Christoph Maier, after `../layout_primitives.md`, while
Christoph slept. These are proposals. The macros are untouched; nothing here is instantiated by any
macro yet.

| file | what |
|---|---|
| `pad_buffer_cells.py` | the generator: one script, IHP SG13_dev PCells plus drawn geometry, comments say why |
| `pad_buffer_cells.gds` | all cells; top cell `pad_buffer_cells` shows them in three columns plus the fit checks |
| `pad_buffer_cells.cdl` | reference netlist per wired cell, written by the same script from the same device lists |
| `verification.md` | DRC and LVS with IHP's decks: DRC clean, LVS 39 of 39 wired cells match; options, fixes, how to repeat |

Regenerate inside IIC-OSIC-TOOLS, after `source .designinit`: `python3 pad_buffer_cells.py` (or
`klayout -b -r pad_buffer_cells.py`). The `.gds` and `.cdl` land in the current directory.

## How the cells are built

Every matched device is a single IHP PCell finger (`ng=1`), so the common-centroid maps of
`layout_primitives.md` can be followed finger by finger. All fingers face the same way: left stripe =
source, current flowing in x.

A row (`row()` in the script) has:
- devices hanging from a common top edge, 0.6 µm apart;
- a poly bar 0.42 µm above the tallest Activ, joining the gates of neighbouring devices on the same gate
  net, with one contact per gate and an M1 bar;
- an ntap (PMOS) or ptap (NMOS) strip underneath. Stripes on its net drop to it in M1; drain stripes on
  the device's own gate net (diodes) rise to the gate bar in M1;
- M2 trunks for nets that occur on two or more stripes, everything else as an M1 pin;
- one NWell + ThickGateOx + pSD rectangle over a PMOS row, one ThickGateOx rectangle over an NMOS row.

A block (`block()`) is two rows sharing their tie. The second row is mirrored about the tie, and trunks
and gate bars of the same net are joined by M1 tracks left of the rows. Only Metal1 and Metal2 are
used, because M3, M4 and TM1 are the IO ring's rails in the pad cell.

## Cells

Amplifier primitives. Nets follow `d2s_mpdda.spice` / `s2d_mpdda.spice` / `units.spice`; `sa_U` / `sb_U`
are the source nodes of unit U.

| cell | contents | wired |
|---|---|---|
| `tub_p20x1`, `tub_p20x1_dummy` | P1: one input device (hv PMOS 2 × 10/1) in its own n-well, well = source; dummy with g = d = s | yes |
| `d2s_inputs` | 2 × 4 tubs `Aa C2b C1b Ba / Bb C1a C2a Ab`, dummy tubs at the ends; nets of every tub as notes (63/0) | tubs only |
| `s2d_inputs` | signal units in the same map (A1 A2 F1 F2), CMFB cross-quad `M1a M2b / M1b M2a`, dummies | tubs only |
| `d2s_tails`, `s2d_tails` | P2: hv PMOS 5/6 tails in one well on vdd, same map as the tubs, BP at an end, dummies; gate vbp | yes |
| `d2s_rhigh`, `s2d_rhigh` | P3: each 150 kΩ as 4 series segments 0.5 × 12.65 µm, sequence U… U…, nested M2 jumpers, ends as M2 pins, dummies shorted to a vss ptap | yes |
| `sinks_6x6` | P4, shared by both pads: SX / SY 6 + 6 fingers 6/6 `X Y Y X X Y / Y X X Y Y X`, BN at an end, dummies; gate vbn | yes |
| `s2d_sinks_cmfb` | SXC / SYC 4 + 4 fingers 6/6, cross-coupled | yes |
| `d2s_loads`, `s2d_loads` | P5: hv PMOS 6/4, `L R R L L R R L` (d2s), `P N D D N P P N D D N P` (s2d) | yes |
| `d2s_casc_n`, `d2s_casc_p`, `s2d_casc_n`, `s2d_casc_p` | P6: 15/3 cascodes; BNC (1/8) and BPC (1/4) on the same gate line | yes |
| `d2s_ab_p`, `d2s_ab_n` | P7: class-AB groups RP2 FPL ABP / RN2 FNL ABN; RP1 / RN1 here as the fall-back (the proposal puts them into the clamp frames) | yes |
| `d2s_cma`, `d2s_cmb`, `s2d_cload` | MOS capacitors (CMA's well is the pad net: ESD zone, latch-up rules) | yes |
| `d2s_pd_p`, `d2s_pd_n`, `s2d_pd_p`, `s2d_pd_n` | power-down switches and output ties | yes |

Bias (`d2s_bias_sel_pd`, the same in both pads):

| cell | contents | wired |
|---|---|---|
| `bias_tree_n`, `bias_tree_p`, `bias_tree_sw`, `bias_tree_swp` | `d2s_bias_in_tree_pd` without BP / BN (in the tail and sink rows) | yes |
| `oa_pmir_a`, `oa_pmir_b` | OA core PMOS mirror as 31 fingers 2/8 + 1 dummy in a 4 × 8 point-symmetric map; the two blocks stack, a over b | yes |
| `oa_pcas`, `oa_nmir`, `oa_mcs`, `oa_misc_n` | cascodes; M10 / M11 as 18 + 9 fingers 10/1, point-symmetric; MCS / MCL; MC10, MS2, MS3, SKS | yes |
| `oa_misc_p` | MS1 as 8 × 0.5/12.5 in series, SVPG | rows only; the chain link between the two rows (ms4) is a pin pair |
| `bg_pmir`, `bg_pcas`, `bg_nab` | bandgap PMOS mirror and cascodes as 10/1 fingers, point-symmetric; NA / NB `NA NB NB NA` | yes |
| `bg_misc_n`, `bg_misc_p` | MS2, MS3, SKS; MS1 chain as in the OA core, SVPG | as `oa_misc_p` |
| `bg_pnp` | Q1 in the middle of 8 Q2 (pnpMPA 2 × 2 µm) | placed, not wired |
| `bg_res` | R1A 11, R1B 10, R0 18 segments of 9.94 µm, mirror-symmetric sequence, dummies | placed, not wired |

Not drawn: `en_ctrl_3v3` and the level shifters, the logic gates of `d2s_bias_sel_pd`, and the
connections between blocks.

## Verification (details in `verification.md`)

- IHP's DRC (main + maximal tables, no density) finds no violations in any cell.
- IHP's LVS matches all 39 wired cells against `pad_buffer_cells.cdl` (`--disable_tap_extraction`;
  `--implicit_nets` for seven cells whose same-named pins the parent joins).
- Not LVS'd: the tub arrays (the tub itself matches), `bg_pnp`, `bg_res`.

## Netlist changes the cells imply

These are layout-driven. The schematics do not have them yet, and LVS against the macros needs them:

1. d2s fold sinks SX / SY: `ng=4` → `ng=6` (the shared 6/6 finger; simulated in `../sink_6x6/`).
2. Each `unit_r2` resistor as 4 series segments of 12.65 µm. Each extra head adds contact resistance, a
   few hundred Ω in 150 kΩ. It is the same in every unit, so the gain is unaffected; re-simulate Gm.
3. BP into the tail rows and BN into the sink rows: move them from `d2s_bias_sel_pd` into the buffer
   sheets (`layout_primitives.md`, decision 4).
4. OA core: M10 `ng=8` → 18 and M11 `ng=4` → 9. The SG13_dev PCell finger limit is 10 µm; the netlist
   now has 22.5 µm fingers.
5. MS1 (0.5/100) as 8 × 0.5/12.5 in series, in both cores, because it does not fit an 80 µm cell as one
   device.
6. Bandgap R0 is 178.9 µm instead of 179.5 µm (−0.33 %), because all segments are 9.94 µm long; R1A
   and R1B come out at 109.34 / 99.4 µm. Trim in simulation.
7. NA / NB as 2 × 10/4 each (`ng=2`).

## Fit in the pad cell (from the drawn cells)

First-fit shelf packing, 2 µm between bounding boxes, 80 µm wide (cells `fit_*` in the GDS). The zone
above the clamp frames is y = 84 … 178 µm, i.e. 94 µm:

| set | packed height |
|---|---:|
| d2s front end (inputs, tails, rhigh, sinks, loads, cascodes, class AB, power-down) | 94.2 µm |
| the same with the Miller capacitors CMA / CMB | 98.8 µm |
| s2d front end | 136.5 µm |
| bias tree + OA core + bandgap core | 131.1 µm |

- The d2s front end alone just fills the zone.
- The Miller capacitors, and above all the two reference cores, belong in the slot: one bias root per
  slot, with a current leg per pad.
- s2d needs about 42 µm more than the zone even without its bias.
- Interconnect between the blocks is not in these numbers.
