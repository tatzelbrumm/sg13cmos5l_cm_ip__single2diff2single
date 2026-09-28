<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Parametrized sg13cmos5l ESD clamps: `Clamp_N` / `Clamp_P`

The IHP `sg13cmos5l_io` library ships its ESD clamps only as flat layouts:
`sg13cmos5l_Clamp_{N,P}{2,8,15}N{..}D` and `..._{N,P}20N0D`. Whatever PCells built
them were flattened away. This directory rebuilds them as KLayout PyCells in the
PDK's own style (`cni` / `DloGen`, `<name>_code.py` → `class <name>`, as in
`ihp-sg13cmos5l/libs.tech/klayout/python/sg13cmos5l_pycell_lib/ihp`). The only
parameter is `ng`: for the reference values of `ng` the cells come out identical
to IHP's, and other values are interpolated between them.

N43N43D4R is not covered. It is a different topology (4 rows of `ng=1`
devices in a taller frame).

## Parameters

| param | values | meaning |
|---|---|---|
| `ng`  | N·D 1–42, P·D 1–41, N/P·0D 1–27 | gate fingers (L = 0.6 µm hv device) |
| `tie` | `D` / `0D` | `D`: gate is a pin (`gate`) with an antenna diode. `0D`: gate tied off to the rail through an rppd (always-off clamp) |

Per finger: N = 4.4 µm × 1 row, P = 6.66 µm × 2 stacked rows (MP0 + MP1).
Cell names follow IHP's scheme: `sg13cmos5l_Clamp_<F><ng>N<ng|0>D`.
Pins: N·D `gate iovss pad`, N·0D `iovss pad`, P·D `gate iovdd iovss pad`,
P·0D `iovdd iovss pad`, all in the same order as `sg13cmos5l_io.cdl`.

## How the cells decompose

Every clamp sits in a fixed 80 µm frame (N 80 × 9.9, P 80 × 19.26) and is made of
three parts:

* **Frame.** Guard rings, wells and ring contacts are identical in every
  reference of a family and tie variant. They are stored as extracted
  geometry. The N·0D frame's inner ring sits 50 nm higher than the N·D one.
* **Array.** The fingers are purely rule based (`clamp_engine.py`). The active
  length is **0.30 + 1.51·ng µm** for both parities, centred on x = 40 µm. The
  finger sequence is end source 0.47 / gate 0.6 / drain 1.18 / gate 0.6 /
  source 0.64 …; odd `ng` ends in a 0.74 µm drain. End contact columns sit
  0.15 µm inside the active edge. Sources get 0.2 µm M2 + M3 straps tied to the
  inner ring. Drains get 0.61 µm M2 `pad` straps that exit at the top, where
  the bond pad joins them. The gates are contacted at both heads (P: also in
  the middle) and joined by an M1 bus.
* **Tie block.** This is hand-drawn. For `D` it is the antenna diode plus the
  M2 `gate` strap. Its x position is interpolated piecewise-linearly in `ng`
  through the references (2 → 20.24, 8 → 17.975, 15 → 15.33 µm, identical for
  N and P, snapped to the 5 nm grid). The block itself is taken from the
  nearest reference, which sets the diode size (P2/P8: 0.48 µm, P15 and all
  N: 0.78 µm). For `0D` it is the rppd at a fixed x (N: 3.54 µm / 1.959 kΩ,
  P: 12.9 µm / 6.768 kΩ).

`extract_clamp_refdata.py` subtracts the rule-generated array from each reference
and aborts if the rules produce anything the reference lacks, or leave anything
outside the tie window. `clamp_refdata.py` is its output; don't edit it by hand.

## Files

| file | role |
|---|---|
| `__init__.py`, `load_clamp_pcells.py` | register KLayout library **`SG13_cm_clamps`** (finds the PDK's `sg13cmos5l_pycell_lib` and `cni` via `$KLAYOUT_PATH`/`$PDKPATH` if they aren't on the path yet) |
| `use_clamp_pcells.py` | swap `sg13cmos5l_Clamp_*` cells (static copies or `.klib` references) in an existing layout for the PCells; writes only if the flattened geometry is unchanged |
| `clamp_base_code.py`, `Clamp_N_code.py`, `Clamp_P_code.py` | the PyCells (`DloGen`) |
| `clamp_engine.py` | geometry rules + interpolation, pure Python, integer nm |
| `clamp_refdata.py` | extracted frames / tie blocks (generated) |
| `extract_clamp_refdata.py` | regenerates `clamp_refdata.py` from `sg13cmos5l_io.{gds,cdl}` |
| `clamp_netlist.py` | CDL (as in `sg13cmos5l_io.cdl`) and ngspice (as the PDK xschem symbols) subcircuits |
| `clamp_klayout.py` | writes engine output into a `klayout.db` layout |
| `gen_clamp.py` | CLI: GDS + CDL + ngspice for any `ng`, no PDK needed |
| `verify_clamp.py` | XOR against the references (engine and PCell paths) + sweep |
| `lvs_clamp.py` | light device/connectivity check (not the PDK LVS) |

## Use

In the IIC-OSIC-TOOLS container, after `source .designinit` (so that
`KLAYOUT_PATH` points into the PDK):

```sh
# GUI: library SG13_cm_clamps appears in the library browser
klayout -e -rm scripts/pcells/load_clamp_pcells.py layout/<file>.gds

# batch files
python3 scripts/pcells/gen_clamp.py N 11 D -o /tmp/clamps      # .gds .cdl .spice
python3 scripts/pcells/gen_clamp.py --limits
```

The `.spice` output starts with `.global sub!`. `sg13cmos5l_io.cdl` leaves
`sub!` undeclared, and plain ngspice would otherwise make it a separate local
node in every instance.

## Putting the PCells into an existing layout

```sh
klayout -b -r scripts/pcells/use_clamp_pcells.py -rd input=<in.gds> -rd output=<out.gds>
```

If this fails with a `UnicodeDecodeError` inside IHP's `sg13cmos5l_pycell_lib/__init__.py`,
the locale isn't UTF-8: IHP's library reads its module files with the locale's encoding.
IIC-OSIC-TOOLS already sets `LC_ALL=en_US.UTF-8`; elsewhere, run with a UTF-8 locale.

It replaces each `sg13cmos5l_Clamp_<F><ng>N<..>D` cell with `Clamp_<F>(ng, tie)` in all its
placements, compares the flattened top cell layer by layer, and writes only if all drawing
and pin layers are identical. Label moves are listed but don't block: IHP's cells carry
extra hand-placed `pad` labels, while the PCells put one on each drain strap.

Things to know:

* The clamps become cells named `Clamp_N` / `Clamp_P` (`Clamp_N$1` … for further variants),
  no longer `sg13cmos5l_Clamp_N15N15D` etc.
* The saved GDS contains the full geometry plus a PCell reference. Opened with the library
  registered (`-rm load_clamp_pcells.py`), the cells are live PCells whose `ng`/`tie` can be
  edited. Without it they show as `<defunct>` but the geometry is intact, so DRC, LVS and
  stream-out read the same shapes.
* `SG13_cm_clamps` is registered without a technology restriction. GDS doesn't store a
  layout's technology, so a restricted library could not re-attach to its instances when a
  saved file is read back.

## Verification status (2026-09-28)

* **Reproduction.** All 8 reference cells come out **identical** to the
  originals on every drawing and pin layer (merged XOR is empty), through both
  the engine and the real IHP `cni` PCell path. Ring, diode and rppd labels are
  identical. `pad` labels are regenerated as one per drain strap (IHP has extra
  hand-placed ones), and their coverage is checked.
* **DRC.** The IHP `ihp-sg13cmos5l.drc` deck, flat mode, density and angle
  tables off, was run on the 8 references and on all 137 swept cells: **0
  violations**. Caveat: this ran on KLayout 0.28.16 with a one-line shim
  (`def absolute; nil; end`), because the deck wants ≥ 0.29.11. The shim is
  also why the angle table had to stay off. Re-run properly in the container
  with `run_drc.py`.
* **Connectivity.** `lvs_clamp.py` passes on all references and all 137 swept
  cells: one combined MOS per cell with W = 4.4·ng (N) or 13.32·ng (P) µm and
  L = 0.6 µm, D = pad, S = rail, G = `gate` or rppd→rail, and the diode is on
  the gate net. It catches injected opens and shorts. It is **not** sign-off;
  use `run_lvs.py` (KLayout ≥ 0.30.2) against the `.cdl` for that.
* **Not yet verified.** Simulating the ngspice netlists, PDK LVS, and
  electrical/ESD adequacy of interpolated sizes. The antenna diode's size
  follows the nearest reference and has not been re-derived from antenna
  rules. `ng` values outside 2–15 (D) or other than 20 (0D) are extrapolated.

```sh
python3 scripts/pcells/verify_clamp.py <pdk>/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds \
        --pdk-python <pdk>/libs.tech/klayout/python --sweep-gds /tmp/sweep.gds
python3 scripts/pcells/lvs_clamp.py /tmp/sweep.gds
```
