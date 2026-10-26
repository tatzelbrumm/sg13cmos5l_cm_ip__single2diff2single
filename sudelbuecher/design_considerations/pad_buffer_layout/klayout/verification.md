<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# DRC and LVS of `pad_buffer_cells`

2026-10-26, about 03:50 CET. Run by Claude (Opus 5.5) with IHP's own decks, the PDK's `run_drc.py` and
`run_lvs.py`, unchanged.

## Result

- **DRC: no violations.** This covers the whole library cell `pad_buffer_cells`: every cell, the fit
  checks included. Tables "main" (333 rules executed) and "sg13cmos5l_maximal" ran; density was left
  out (`--no_density`), because it only makes sense for a full chip.
- **LVS: 39 of 39 cells match** against `pad_buffer_cells.cdl`:

  bg_misc_n bg_misc_p bg_nab bg_pcas bg_pmir bias_tree_n bias_tree_p bias_tree_sw bias_tree_swp
  d2s_ab_n d2s_ab_p d2s_casc_n d2s_casc_p d2s_cma d2s_cmb d2s_loads d2s_pd_n d2s_pd_p d2s_rhigh
  d2s_tails oa_mcs oa_misc_n oa_misc_p oa_nmir oa_pcas oa_pmir_a oa_pmir_b s2d_casc_n s2d_casc_p
  s2d_cload s2d_loads s2d_pd_n s2d_pd_p s2d_rhigh s2d_sinks_cmfb s2d_tails sinks_6x6 tub_p20x1
  tub_p20x1_dummy

## Options and what they mean

- `--disable_tap_extraction` for every cell. Otherwise IHP's extraction makes a resistor device of
  each ntap1 / ptap1 (`R$13 vdd $3 ntap1 …`), and the bulks land on a net of their own. With the option
  the well or substrate is the tie's net, which is how the schematics write it.
- `--implicit_nets='*'` for seven cells: `bg_misc_n`, `bg_misc_p`, `d2s_ab_n`, `d2s_ab_p`, `oa_misc_n`,
  `oa_misc_p`, `oa_pcas`. In these, a net appears as two labelled pins of the same name that the cell
  does not join itself; the parent does:
  - n1 / n2: the RP1 / RN1 gate bars and the RP2 / RN2 source;
  - ms4: the link of the MS1 chain between its two rows;
  - c8, vnc, …: in `oa_pcas`, nets beyond the two M2 trunks that the 2 µm fingers have room for.
  The option treats same-named labels as connected and changes nothing else.
- Dummies are in the reference netlist: S = D (MOS) or shorted (rhigh). Parallel devices are combined
  by the LVS as usual: the dummies of a row form one W = n·w device on each side.
- Each `unit_r2` resistor is 4 series rhigh segments in layout and in the reference netlist. The LVS
  reduces both to one 0.5 × 50.6 µm device per unit.

## Not checked by LVS

- `d2s_inputs`, `s2d_inputs`: arrays of `tub_p20x1` / `tub_p20x1_dummy` (each of which matches).
  The tubs are not wired to each other; their nets are notes on 63/0.
- `bg_pnp`, `bg_res`: placed, not wired.
- `fit_*`, `zone_80x94` and the top cell: arrangements only.

## Fixes made before the clean run

| finding (IHP deck or own pre-check) | cause | fix in `pad_buffer_cells.py` |
|---|---|---|
| poly space (Gat.b) at many gates | a poly stub narrower than its gate left 0.12 µm shoulders under the gate bar | bar 0.42 µm above the Activ (shoulders 0.24 µm away) |
| contact space (Cnt.b) in the MS1 blocks | the two rows of a block had ties of different lengths, with offset contacts where they overlap | both rows get the longer tie (`row_len()`) |
| M1 width at row ends | the end stripe's drop met the tie's M1 a few tens of nm off its corner | tie M1 drawn out under all stripes that land on it |
| M1.d (area 0.09 µm²) | one-gate bars (0.26 × 0.26 µm); the PCell's stripes on 0.5 µm fingers (0.08 µm²) | bars at least 0.5 µm long; stripes under 0.6 µm lengthened downward |
| Pin.e (pin box outside M1) | pin box 0.3 µm wide on a 0.26 µm bar | follows from the bar fix |
| LVS `d2s_rhigh`, `s2d_rhigh` | the left dummy's strap missed the vss tie | tie extended 1.2 µm beyond both ends |

## How it was run, and how to repeat it

In IIC-OSIC-TOOLS (KLayout ≥ 0.30.2 needed), after `source .designinit`, in this folder:

```sh
python3 pad_buffer_cells.py
python3 $PDK_ROOT/$PDK/libs.tech/klayout/tech/drc/run_drc.py --path=pad_buffer_cells.gds \
    --topcell=pad_buffer_cells --run_dir=drc --no_density
for c in $(grep '^.SUBCKT' pad_buffer_cells.cdl | awk '{print $2}'); do
  python3 $PDK_ROOT/$PDK/libs.tech/klayout/tech/lvs/run_lvs.py --layout=pad_buffer_cells.gds \
      --netlist=pad_buffer_cells.cdl --topcell=$c --run_dir=lvs/$c --disable_tap_extraction --implicit_nets='*'
done
```

`--implicit_nets='*'` only matters for the seven cells above; for all others the result is the same
without it.

The cloud container had no KLayout ≥ 0.30.2: Ubuntu ships 0.28.16, and conda-forge's 0.30.12 has no Ruby.
So these runs used:
- KLayout 0.30.4 built from source, without Qt and with Ruby only;
- its `strmrun` behind a `klayout -b -r … -rd …` shim;
- a small Ruby runner that loads KLayout's DRC/LVS engine sources and evaluates the deck inside module
  `DRC` / `LVS`, as KLayout's own interpreter macros do;
- IHP-Open-PDK at iic-jku `c271a7e9`, the image's commit (`sudelbuecher/cloud_environment.md`).

The image's own `klayout` needs none of this.
