<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# IOPad: layouts, schematics, and what refers to them

Inventory of 2026-10-27, 11:45–11:55, by Claude (configured model `claude-opus-5-5`) for Christoph Maier, on his
request of 11:44: "First, handle the correspondence of the IOPad*.gds layouts and the schematic/xschem
construction site, where I started putting together schematics and symbols for IHP's standard cells. I probably did
similar work elsewhere in the sudelbuecher for the single2diff and diff2single schematics. IOPad as shared,
consolidated library might be a good attractor for these, if we're ABSOLUTELY METICULOUS about avoiding software
engineers' mindset and systematically ignoring side effects."

Read only: nothing in the repository or the sudelbuecher was moved or edited for this.

## 1. What `macros/IOPad` holds

- `layout/klayout/pad_buffer_cells.gds`, `pad_buffer_cells.cdl` (moved there by Christoph at 11:25); `backups/`: the
  six IHP IO-cell GDS copies.
- `schematic/xschem/`: two kinds of file, plus `xschemrc`.

### 1a. Christoph's construction site (xschem 3.4.8RC; identical to the 2026-10-20 snapshot)

| file | content | pins | IHP counterpart (CDL of the local PDK checkout) |
|---|---|---|---|
| `DCNdiode.sch` | `dantenna` l=1.26u w=27.78u m=2, anode to cathode | anode, cathode | `sg13cmos5l_DCNDiode anode cathode guard`: 2 × `dantenna` **w=1.26u l=27.78u** from sub! to cathode, `ptap1` anode–sub!, guard unused. Here w and l are swapped, no guard pin. |
| `DCNdiode.sym` | copy of the PDK's `dantenna.sym` (type=diode, calls `@model`) | d0, d1 | does not match `DCNdiode.sch` |
| `DCPdiode.sch` | `dpantenna` l=1.26u w=27.78u m=2 | anode, cathode | `sg13cmos5l_DCPDiode anode cathode guard`: 2 × `dpantenna` w=1.26u l=27.78u anode→cathode, `ptap1` guard–sub! |
| `DCPdiode.sym` | copy of `dpantenna.sym` | d0, d1 | does not match `DCPdiode.sch` |
| `sg13cmos5l_ClampN15N15.sch` | hv NMOS 4.4/0.6, ng=1, m=15; the drain wire carries a stale label `iovss`, its pin says `pad` | gate, iovss, pad | `sg13cmos5l_Clamp_N15N15D gate iovss pad`: NMOS 66/0.6 ng=15 plus `dantenna` 0.78 × 0.78 on the gate. Here: no gate diode, m=15 instead of ng=15. |
| `sg13cmos5l_ClampN15N15.sym` | copy of `sg13_hv_nmos.sym` | D, G, S, B | does not match the sheet |
| `sg13cmos5l_ClampP15N15.sch` | hv PMOS 13.32/0.6, ng=2, m=15 | gate, iovdd, pad | `sg13cmos5l_Clamp_P15N15D gate iovdd iovss pad`: 2 × PMOS 99.9/0.6 ng=15, `dpantenna` on the gate, `ptap1` iovss–sub!. Same total W; no gate diode, no iovss pin. |
| `sg13cmos5l_ClampP15N15.sym` | copy of `sg13_hv_pmos.sym` | D, G, S, B | does not match the sheet |

None of these eight files is placed anywhere in the repository.

### 1b. Black-box symbols of IHP sub-cells (consolidation session 2026-10-20; redrawn 2026-10-24, pins unchanged)

Each netlists as `X<name> <pins> sg13cmos5l_<cell>`; the subcircuit has to come from the IHP IO netlist.

| symbol | pins, in netlist order | placed in |
|---|---|---|
| `sg13cmos5l_Clamp_N20N0D.sym` | iovss pad | `sg13cmos5l_IOPadSingle2Diff.sch` (CN) |
| `sg13cmos5l_Clamp_P20N0D.sym` | iovdd iovss pad | `sg13cmos5l_IOPadSingle2Diff.sch` (CP) |
| `sg13cmos5l_DCNDiode.sym` | anode cathode guard | `sg13cmos5l_IOPadDiff2Single.sch` (DN), `sg13cmos5l_IOPadSingle2Diff.sch` (DN) |
| `sg13cmos5l_DCPDiode.sym` | anode cathode guard | `sg13cmos5l_IOPadDiff2Single.sch` (DP), `sg13cmos5l_IOPadSingle2Diff.sch` (DP) |
| `sg13cmos5l_SecondaryProtection.sym` | core minus pad plus | `sg13cmos5l_IOPadSingle2Diff.sch` (SP) |

PDK xschem symbols for the IO library (corrected 13:12): the local IHP-GmbH checkout has none. The PDK in use
(iic-jku dev `a49358c`) has `libs.tech/xschem/sg13cmos5l_io/`: the fifteen pad cells (`sg13cmos5l_IOPad*.sym`), no
sub-cells, each a link to the SG13G2 symbol. `sg13cmos5l_IOPadAnalog.sym` → `sg13g2_IOPadAnalog.sym` netlists
`@name @pinlist @symname` with the pins in the order vss vdd iovss iovdd pad padres pad (two `pad` pins), which is
not the order of the subcircuit in the same PDK (`pad padres vdd vss iovdd iovss`): placing it would cross-wire the
cell. The project places none of these symbols.

### 1c. Counterparts of Christoph's PCells (added 2026-10-27, 13:22)

Decided at 13:09 (log): sheets for both diodes and both clamps, named as the layout cells. Each symbol is a copy of the
black box of 1b with the same pin positions (a drop-in swap keeps the wires), `type=subcircuit`,
`format="@spiceprefix@name @pinlist @symname"`; the clamps get a `gate` pin, and the gate tie to the rail is removed.
Values as placed in `sg13cmos5l_IOPadDiff2Single.klay.gds`; no ptap1 / ntap1 (LVS runs with
`--disable_tap_extraction`).

| cell | pins | devices |
|---|---|---|
| `DCNDiode` | anode cathode guard | 2 × dantenna anode → cathode, w = 1.26u, l = 63.78u; guard: no device |
| `DCPDiode` | anode cathode guard | 2 × dpantenna anode → cathode, w = 1.26u, l = 63.78u; guard: no device |
| `Clamp_N_M1` | gate iovss pad | sg13_hv_nmos D pad, G gate, S / B iovss, w = 149.6u, l = 1u, ng = 34 |
| `Clamp_P_M1` | gate iovdd iovss pad | sg13_hv_pmos D pad, G gate, S / B iovdd, w = 546.12u, l = 0.6u, ng = 82; iovss: no device |

Verified with xschem 3.4.4 in the cloud workspace against the PDK's symbols at `a49358c`: each sheet netlisted as a
subcircuit, and a test parent with a distinct label on every pin, in the spice and in the LVS mode of
`make klayout-lvs-netlist`, compared device by device (model, nets in order, w / l / ng, ports): 0 mismatches; a
copy with the NMOS bulk moved onto the gate net was caught. Rendered and looked at. Nothing places them yet.

## 2. Layouts against these

### 2a. The six IHP IO cells (copies in `IOPad/layout/klayout/backups/`)

Compared by XOR with `sg13cmos5l_io.gds` of the local PDK checkout (IHP-GmbH/IHP-Open-PDK, branch dev, `0488153`,
files of 2026-09-30):

| cell | sub-cells | copy vs. local PDK | symbols in IOPad |
|---|---|---|---|
| `sg13cmos5l_IOPadAnalog` | Clamp_N20N0D, Clamp_P20N0D, DCNDiode, DCPDiode, SecondaryProtection | differs only on PolyRes 128/0, 2 µm² | all five sub-cells (1b) |
| `sg13cmos5l_IOPadIOVss` | DCNDiode, DCPDiode | identical | both (1b) |
| `sg13cmos5l_IOPadVss` | DCNDiode, DCPDiode | identical | both (1b) |
| `sg13cmos5l_IOPadIOVdd` | Clamp_N43N43D4R, RCClampInverter, RCClampResistor | the PDK has 520 µm² PolyRes 128/0 more | none |
| `sg13cmos5l_IOPadVdd` | the same | the same | none |
| `sg13cmos5l_IOPadInOut30mA` | Clamp_N15N15D, Clamp_P15N15D, DCNDiode, DCPDiode, GateDecode, LevelDown, LevelUp, SecondaryProtection, io_inv_x1, io_nand2_x1, io_nor2_x1, io_tie | geometry differs on 11 layers, and the PDK has three layers the copy lacks (PolyRes, GatPoly.pin, HeatTrans); the local PDK uses `sg13g2_SecondaryProtection` and two `M2_M1_OS_*` via cells where the copy has `sg13cmos5l_SecondaryProtection` | DCN, DCP, SecondaryProtection (1b); simplified sheets of Clamp_*15N15D (1a) |

The copies come from another PDK revision than the local checkout.

### 2b. The pad cell `sg13cmos5l_IOPadDiff2Single.klay.gds` uses Christoph's PCells, not IHP's cells

PCell parameters from the GDS context, devices counted in the geometry:

| PCell (library `SG13_cm_clamps`) | parameters | drawn | the pad's sheet / netlist has |
|---|---|---|---|
| `DCNDiode` | dantenna, l=63.78u | 2 diode stripes 63.78 × 1.26 µm | IHP `sg13cmos5l_DCNDiode` (2 × 27.78 µm) |
| `DCPDiode` | dpantenna, l=63.78u | the same | IHP `sg13cmos5l_DCPDiode` (2 × 27.78 µm) |
| `Clamp_P_M1` | ng=41, l=0.6u, frame 80u | 82 channels 6.66/0.6 | OP: w=546.12u l=0.6u ng=82 (matches) |
| `Clamp_N_M1`, two instances | ng=34, l=1u, frame 80u | 2 × 34 = 68 channels 4.4/1 | ON: w=290.4u l=1u ng=66 (68 drawn, 66 in the netlist) |

For LVS the pad's sheet needs counterparts of these PCells, which is presumably what the construction-site sheets
(1a) were started for; the IHP black boxes (1b) describe different devices.

## 3. The IHP IO netlist: one current version, two outdated sources

Settled 12:44–12:47. Christoph's container (DoctorEvil): `$PDK_ROOT/ihp-sg13cmos5l/COMMIT` = iic-jku/IHP-Open-PDK dev
`a49358c` (2026-10-15), `libs.ref/sg13cmos5l_io/spice/sg13cmos5l_io.spice`. The IO library's three files, fetched at
that commit from GitHub, are byte-identical (sha256) to the local checkout (IHP-GmbH dev `0488153`) and to the
revision of the cloud CACE runs (iic-jku dev `c271a7e`, 2026-09-21, `sudelbuecher/cloud_environment.md`):
`sg13cmos5l_io.spice` `1b07a9ee…`, `sg13cmos5l_io.cdl` `52279f2a…`, `sg13cmos5l_io.gds` `e6f0d64b…`.

| source | `Clamp_N20N0D` | `IOPadAnalog` | status |
|---|---|---|---|
| the PDK in use (container, cloud runs, local checkout) | iovss pad | pad padres vdd vss iovdd iovss | current |
| `sudelbuecher/sg13cmos5l_IOPadInOut30mA/sg13cmos5l_io.spi` (generated 2024-05-27), and the excerpt `sudelbuecher/sg13cmos5l_IOPadAnalog/sg13cmos5l_IOPadAnalog_real_hierarchy.spi` taken from it; the container's LibreLane runs of 31 Aug name a `.spi` of this kind | iovss iovdd pad | vss vdd iovss iovdd pad padres | outdated |
| project doc `claude/sg13cmos5l_pad_cell_internals.md` (from another checkout), which says the CMOS5L order differs from SG13G2's | not stated | iovdd iovss pad padres vdd vss | wrong for the PDK in use, where the order equals SG13G2's |

- The black-box symbols (1b) match the PDK in use; `tb_pad_dc.spice` (S2D) includes the right file name,
  `sg13cmos5l_io.spice`.
- The six IHP GDS copies in `IOPad/layout/klayout/backups/` (§2a) are therefore older than the PDK in use too.
- Two faults in the PDK's CDL (all three revisions): `sg13cmos5l_IOPadInOut30mA` calls `Clamp_N15N15D` with four nodes
  (`net2 iovss pad ptap1`) for three pins, and its `XR0 vss sub!` has no model name.

## 4. What refers to IOPad (the side effects of any move or rename)

- **Symbol lookup** is by bare file name through `XSCHEM_LIBRARY_PATH`, in two different orders:
  - `macros/xschemrc`: glob over `macros/*/schematic/xschem` and `macros/*/testbenches/xschem`, sorted; `IOPad` sorts
    before every lower-case macro name.
  - The xschemrc of `sg13cmos5l_IOPadDiff2Single` (schematic, testbenches), `sg13cmos5l_IOPadSingle2Diff` (schematic,
    testbenches) and `slot` (schematic): the own folder first, then `foreach dep {… IOPad …}` →
    `../../../IOPad/schematic/xschem`.
  - `schematic/xschem/xschemrc` (top) sources the two pads' xschemrc.
  - Today no symbol file name occurs twice in `macros/*/{schematic,testbenches}/xschem`, so both orders resolve the
    same. A symbol added to IOPad under a name that exists elsewhere would resolve differently depending on where
    xschem is started.
- **Sheets**: `sg13cmos5l_IOPadDiff2Single.sch` (DN, DP) and `sg13cmos5l_IOPadSingle2Diff.sch` (CP, CN, DN, DP, SP).
  Renaming a black-box symbol, or changing its pins or their order, changes both.
- **Comparison baseline**: `sudelbuecher/design_considerations/consolidation/reference_sheets_2026-10-20/` mirrors the
  repository's folders, IOPad included, and is the reference root of `scripts/xschem/sheet_equiv.py` ("Do not edit
  these files"). Moving files in `macros/IOPad` changes what that comparison reports.
- **Layout**: `macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.klib` →
  `../../../IOPad/layout/klayout/pad_buffer_cells.gds`.
- No Makefile, CACE yaml or testbench refers to an IOPad path. `macros/README.md` describes IOPad as "IHP IO GDS
  copies, Christoph's clamp / diode sheets, and symbols of IHP IO sub-cells" (now partly stale). IOPad has no Makefile
  and no README.

## 5. The sudelbuecher

- No xschem sheets or symbols of IHP IO cells apart from the 2026-10-20 snapshot of IOPad (1a identical, 1b redrawn
  since, same pins).
- Related material, not xschem: `sg13cmos5l_IOPadAnalog/` (Clamp_N20N0D unit-cell DRC study, the real-hierarchy
  `.spi` excerpt), `sg13cmos5l_IOPadInOut30mA/` (GateDecode DRC study, full-hierarchy `.spi`, the "verified schematic
  v3" figure, `sg13cmos5l_io.spi` of 2024-05-27, `sg13cmos5l_io.celllist`), `esd_protection/` (notes, `.tex` / `.pdf`).
- The d2s / s2d design-consideration sheets (`class_ab_pad_driver/{xschem,improvements/xschem,power_down/xschem}`,
  `s2d_input_buffer/xschem`) hold only circuit-block symbols; clamps appear in their text notes only.

## 5a. Byte-order marks in xschemrc files (found 13:18)

Eight xschemrc files start with a UTF-8 BOM: `macros/IOPad/schematic/xschem`, `macros/OgueyAebischerBias/{schematic,
testbenches}/xschem`, `macros/inverter/{schematic,testbenches}/xschem`, `macros/slot/testbenches/xschem`, and the top
`schematic/xschem`, `testbenches/xschem`. xschem 3.4.4 (cloud workspace) rejects such an rc as a whole (`invalid
command name "ï»¿#"`) and then finds no symbols; whether the container's xschem 3.4.8RC tolerates it was not checked.
Not changed.

## 6. Proposal and status

Status 13:24: item 1, the PCell counterparts, done (1c), named as the layout cells (item 2: the case-only difference
to Christoph's `DCNdiode` / `DCPdiode` stays). Item 4 done (project doc corrected 13:04). Item 5 decided "Netlist
follows layout": ON w = 299.2u, ng = 68 in `d2s_mpdda_pd.sch` and `netlist/source/d2s_mpdda_pd.spice` (13:21, only
the `XON` line of the netlist changes); `netlist/source/d2s_mpdda.spice` (the original without power-down, included by
`sg13cmos5l_IOPadSingle2Diff/testbenches/spice/tb_s2d_loopback.spice`) still has 66. The CACE results and the
macro README's numbers are from ON = 66.


1. `IOPad/schematic/xschem` as the one home of pad-level cells, with two kinds kept apart:
   - IHP's originals as black boxes (the five of 1b exist; more only when a sheet needs one);
   - counterparts of Christoph's PCells (`Clamp_N_M1`, `Clamp_P_M1`, `DCNDiode`, `DCPDiode` of `SG13_cm_clamps`):
     a sheet and a symbol with matching pins each, devices and parameters as the PCell draws them, so that the pad's
     sheet places what the layout has. The construction-site sheets (1a) are the starting point.
2. Names that cannot be confused: today `DCNdiode` (Christoph's) and `sg13cmos5l_DCNDiode` (IHP's) differ only by
   prefix and case, and Christoph's PCell is called `DCNDiode`, IHP's cell name without the prefix.
3. Before any rename or move: every sheet that places the symbol (§4), the `sheet_equiv.py` baseline, and the two
   lookup orders.
4. PDK revision: settled (§3), the black boxes match it. The project doc's pin-order section needs correcting.
5. ON: 68 fingers drawn against 66 in the netlist.
6. `pad_buffer_cells`: bound and usable as it is; its sheets in `IOPad/schematic/xschem` later, the hand-made CDL
   until then.
