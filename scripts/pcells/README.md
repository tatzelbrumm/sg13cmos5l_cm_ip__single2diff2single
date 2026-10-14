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

## M1-only variants: `Clamp_N_M1` / `Clamp_P_M1`

These are derived from `Clamp_N` / `Clamp_P` for use inside the core, where the
clamp gets wired by hand from above. The code is `generate_m1()` at the end of
`clamp_engine.py` and `clamp_m1_base` in `clamp_base_code.py`.

| param | values | meaning |
|---|---|---|
| `ng` | ≥ 1 | gate fingers |
| `l`  | ≥ `Lmin` (N 0.45u, P 0.40u, from the PDK techparams), 5 nm grid | gate length, e.g. `0.6u` (default, as IHP) |
| `frame` | `fit` (default) / `80u` | `fit`: the rings wrap the array. `80u`: IHP's fixed 80 µm frame with the array centred, as in `Clamp_N` / `Clamp_P` |

What is the same as in the IHP cells:

* **Finger array.** It keeps the 1.18 µm drain (ESD ballast) / 0.64 µm source
  between gates, the 0.47 µm end source and, for odd `ng`, the 0.74 µm end drain.
  Contact columns, gate heads, M1 gate bus, ThickGateOx, and for P the NWell, pSD
  and the two device rows are all unchanged. Only the pitch grows with `l`: the
  active length is **0.30 + ng·(l + 0.91) µm**.
* **Guard rings.** Both rings have the same cross-section (0.34 µm Activ + Cont +
  M1, same well and implant layers) and the same y layout. N: inner p+ substrate
  tap `iovss`, outer n+ tap in an NWell ring (unlabelled, as in IHP's cell). P:
  inner n+ well tap `iovdd`, outer p+ substrate tap `iovss`.

What is different:

* **Nothing above Metal1.** There is no Via1, M2, Via2 or M3. The source columns
  run down in M1 into the inner ring. The drain columns are separate M1 pins
  `pad` and must be joined from above. In P the two device rows share one M1
  column.
* **No tie block.** There is no antenna diode and no rppd. The M1 gate bus is
  the pin `gate`.
* **With `frame = fit` the rings wrap the array** instead of forming the fixed
  80 µm frame. In x they keep the spacings the IHP cells have in y: device Activ
  to inner ring 0.61 µm, inner ring to outer ring 1.46 µm. The array starts at
  (2.75, 2.75) µm. The cell is **5.80 + ng·(l + 0.91) µm** wide (outer ring
  Activ) and 9.9 µm (N) or 19.26 µm (P) tall, as in IHP's cells. The NWell (N)
  and pSD (P) of the outer ring extend 0.62 or 0.18 µm beyond that.
* **With `frame = 80u`** the rings are IHP's 80 µm frame and the array is centred
  on x = 40 µm (snapped to the 5 nm grid when its length is an odd multiple of
  5 nm). The array must keep 0.61 µm to the inner ring, so `ng` ≤ 49 at
  `l` = 0.6 µm. At `l` = 0.6 µm the cell equals `Clamp_N` / `Clamp_P` (tie `D`,
  same `ng`) on Activ, pSD, GatPoly, ThickGateOx, NWell, Substrate and the array
  contacts, apart from the antenna diode it omits.
* Ring contacts are re-spaced on a 0.34 µm pitch, centred on each side.
* Pins: N `gate iovss pad`, P `gate iovdd iovss pad`. Each pin is an M1 pin
  shape plus a label: the bus, each drain column, and the bottom side of each
  named ring.

Things to watch when using them:

* The `gate` net has no antenna diode in the cell. Check antenna rules once it is
  wired.
* The N cell's NWell guard ring is a floating net in the cell, as in IHP's. Tie it
  to `iovdd` at the level above.

## Files

| file | role |
|---|---|
| `__init__.py`, `load_clamp_pcells.py` | register KLayout library **`SG13_cm_clamps`** (finds the PDK's `sg13cmos5l_pycell_lib` and `cni` via `$KLAYOUT_PATH`/`$PDKPATH` if they aren't on the path yet) |
| `use_clamp_pcells.py` | swap `sg13cmos5l_Clamp_*` cells (static copies or `.klib` references) in an existing layout for the PCells; writes only if the flattened geometry is unchanged |
| `clamp_base_code.py`, `Clamp_N_code.py`, `Clamp_P_code.py` | the PyCells (`DloGen`) |
| `Clamp_N_M1_code.py`, `Clamp_P_M1_code.py` | the M1-only PyCells (base class `clamp_m1_base` in `clamp_base_code.py`) |
| `clamp_engine.py` | geometry rules + interpolation, pure Python, integer nm; `generate_m1()` for the M1-only variants |
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

To try it interactively first, start KLayout with `-rm …/load_clamp_pcells.py`, open the
layout, and run in the Macro Development window (Python):

```python
import runpy
runpy.run_path('/foss/designs/sg13cmos5l_cm_ip__single2diff2single/scripts/pcells/use_clamp_pcells.py')['swap_in_view']()
```

This runs the same swap-and-compare on the layout in the window, writes nothing to disk, and
is a single undo step (Edit > Undo reverts it completely).

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

### `Clamp_N_M1` / `Clamp_P_M1` (2026-10-14)

Test set: N and P × `ng` 1, 2, 3, 8 × `l` = Lmin, Lmin + 5 nm, 0.6 µm, 1.0 µm
with `frame = fit` (32 cells), plus `ng` 1, 3, 49 × `l` = Lmin + 5 nm, 0.6 µm with
`frame = 80u` (12 cells), built through the `cni` PCell path.

* **`Clamp_N` / `Clamp_P` unchanged.** `verify_clamp.py` still passes after the
  `l`/`x0` generalisation of `array_extent`/`gate_lefts`/`columns`.
* **No layers above M1.** There are no Via1/M2/Via2/M3/Recog/PolyRes shapes.
* **Connectivity** (scratch `klayout.db` extraction, as in `lvs_clamp.py`): each
  cell gives one combined MOS with W = 4.4·ng (N) or 13.32·ng (P) µm and L = `l`.
  S is on the rail, D on `pad` (drain columns joined by name), G on `gate`. The
  `pad`, `gate`, `iovss` (and `iovdd`) nets are distinct. The engine output and
  the PCell output are XOR-identical.
* **80 µm frame.** The array is centred (ThickGateOx symmetric about x = 40 µm
  within the grid). At `l` = 0.6 µm the cells match `Clamp_N` / `Clamp_P` on the
  layers listed above, for `ng` = 1, 2, 8, 15 and 42 (N) / 41 (P).
* **DRC.** The unmodified IHP deck (`run_drc.py`, main + maximal tables, flat,
  density off, offgrid and angle on) ran on KLayout 0.30.0 over all 44 cells:
  547 rule categories, **0 violations**. The same set included `Clamp_N`/`Clamp_P` ng = 8 as a
  baseline. An injected 0.1 µm M1 gap was flagged (M1.b), and so was the ring
  pulled to 0.21 µm from the array (pSD.d), so the deck does see these cells.
* **Bad parameters** (`l` < Lmin, `l` off the 5 nm grid, `ng` < 1, an array too
  long for the 80 µm frame) raise an error and produce an empty cell.
* **Not yet verified.** PDK LVS (needs a schematic, KLayout ≥ 0.30.2) and ESD
  adequacy of the ring spacing and `l` choices.

The test scripts are in `test_m1/`. Run them from any working directory; they
write their GDS there:

```sh
python3 scripts/pcells/test_m1/test_m1.py m1_cells.gds     # PCell path + extraction (needs the PDK)
python3 scripts/pcells/test_m1/xor_engine.py m1_cells.gds  # PCell output == engine output; 80u == Clamp_N/P
python3 scripts/pcells/test_m1/drc_gds.py m1_drc.gds       # DRC input, + IHP baseline cells
python3 scripts/pcells/test_m1/drc_negative_gds.py m1_neg.gds   # DRC must flag these
python3 $PDKPATH/libs.tech/klayout/tech/drc/run_drc.py --path=m1_drc.gds --topcell=TOP --run_mode=flat --no_density
python3 $PDKPATH/libs.tech/klayout/tech/drc/run_drc.py --path=m1_neg.gds --topcell=TOP --run_mode=flat --no_density
```
