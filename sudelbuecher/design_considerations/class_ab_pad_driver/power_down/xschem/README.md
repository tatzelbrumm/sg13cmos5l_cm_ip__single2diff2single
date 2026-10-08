<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# xschem schematics of the power-down cells

The cells of `../sim/d2s_mpdda_pd.spice` and `../sim/d2s_bias_ref_pd.spice` and the four
testbenches in `../sim/tb/`. Each cell sheet is a copy of the hand-edited sheet of the
unmodified cell in `../../improvements/xschem/`, with the new devices added. Placement and
wiring of the existing devices are unchanged; where room was needed, whole parts of the sheet
were moved (listed under "Changes to the copied sheets").

`xschemrc` sources the PDK's xschemrc, then appends this directory and
`../../improvements/xschem`, so that `unit_r2.sym` resolves from there.

## Files

| sheet | contents | pins |
|---|---|---|
| `d2s_mpdda_pd` | `d2s_mpdda` with the four units as `unit_r2` boxes, plus [E] | as `d2s_mpdda`, then en_3v3 (16) |
| `d2s_bias_in_pd` | `d2s_bias_in`, flat, plus [E] | vdd vss vddo vsso iref, 6 bias outputs, en_3v3 |
| `d2s_bias_out_pd` | `d2s_bias_out`, flat, plus [E] | as `d2s_bias_in_pd` |
| `d2s_bias_oa_pd` | `d2s_bias_oa`, flat, plus [E] | vdd vss vddo vsso, 6 bias outputs, en_3v3 |
| `d2s_bias_bg_pd` | `d2s_bias_bg`, flat, plus [E] | as `d2s_bias_oa_pd` |
| `tb_pd_*` | testbenches, one per deck in `../sim/tb/` | none |

In every symbol, en_3v3 is a new pin and the last one in the pin order. All other pins keep
their positions. On the bias symbols, en_3v3 is on the left edge at (-140, 100), below iref.
On `d2s_mpdda_pd.sym`, it is on the left edge at (-180, -80), above vinp; the slot below vfb
collides with the pin texts at the bottom edge. The `@symname` text of `d2s_mpdda_pd.sym` moved
40 units to the right, so that the longer name clears the vdd pin.

## The new block [E] (enable / power-down)

Every new device sits in a dashed #d55e00 frame tagged [E], and the legend under each sheet has
an [E] entry. en_3v3 swings 0 ... 3.3 V on vdd / vss and is active high. Every cell has its own
inverter IP / IN (1u / 0.45u) for en_3v3_b. All switches are 1u / 0.45u hv devices.

| cell | switch | gate | pulls | purpose, when disabled |
|---|---|---|---|---|
| `d2s_mpdda_pd` | SA (PMOS, well on vddo) | en_3v3 | a to vddo | OP off, gate on its source (clamp) |
| | SB (NMOS, bulk vsso) | en_3v3_b | b to vsso | ON off, gate on its source (clamp) |
| | SABP (PMOS, well on vdd) | en_3v3 | vabp to vdd | ABP off, so it cannot conduct between the pulled a and b |
| | SABN (NMOS, bulk vss) | en_3v3_b | vabn to vss | ABN off, likewise |
| `d2s_bias_in_pd` | TGN / TGP | en_3v3 / en_3v3_b | iref to ni (NI's gate line) | transmission gate: cuts iref off |
| | TDN | en_3v3_b | ni to vss | NI and the whole mirror tree off |
| `d2s_bias_out_pd` | TGN / TGP | en_3v3 / en_3v3_b | iref to pi (PI's gate line) | cuts iref off |
| | TDP | en_3v3 | pi to vdd | PI and the tree off |
| `d2s_bias_oa_pd`, `d2s_bias_bg_pd` | MS1 (existing) | en_3v3_b (was vss) | ks up | the always-on start-up pull-up is off |
| | SKS | en_3v3_b | ks to vss | start-up held off |
| | SVPG | en_3v3 | vpg to vdd | PMOS mirror of the core off |
| | TGN / TGP | en_3v3 / en_3v3_b | core output iref to ni | cuts the core off the tree |
| | TDN | en_3v3_b | ni to vss | tree off |

Enabled, all switches are off (TGN / TGP on) and each cell is its `improvements` version.

## Changes to the copied sheets

- `d2s_bias_in_pd`, `d2s_bias_out_pd`: the port column moved from x = 60 to x = -340. The rails
  vddo, vdd, vss and vsso run on to it. The new [E] frame (x = -280 ... 140) holds the inverter,
  the transmission gate on the iref line and TDN / TDP. The old iref line from x = 60 on is now
  ni / pi. en_3v3 enters between vddo and vdd.
- `d2s_bias_oa_pd`, `d2s_bias_bg_pd`:
  - The port column moved to x = -180. The left [E] frame holds the inverter.
  - Everything right of [R] moved 240 to the right. The gap holds a second [E] frame with the
    transmission gate between POC's drain (iref) and NI, and TDN.
  - SKS (in [S], next to ks) and SVPG (oa: in [S], left of P0; bg: in [C], between PB and PA)
    each have a small [E] frame of their own.
  - MS1's gate wire to vss is gone, and the vss rail is merged at x = 140.
  - en_3v3 runs in the gap between vddo and vdd. en_3v3_b runs in the gap between vss and vsso,
    and up at x = 140 to MS1 and SKS.
- `d2s_mpdda_pd`: no existing device or wire moved. The port column has no free
  rail-to-rail column, so the new devices sit in free spots near their nodes, in five [E] frames:
  - IP / IN at the top middle, fed by a wire from en_3v3. The pin is between vdd and vbp. IN
    reaches vss through FNL's bulk tie at x = 1280.
  - SA beside OP, SB under ON's gate line, SABP above ABP's gate line, SABN under the vbnc line.
  - The four switch gates take en_3v3 / en_3v3_b from lab_pin labels. A wire would cross most
    of the sheet.

## Testbenches (`tb_pd_*.sch`)

Laid out like `../../improvements/xschem/tb_mpdda_step.sch`:

- supplies on the left
- bias block `Xb` and DUT `Xd` in the middle, from the symbols in this directory, wired bias
  line by bias line
- load or pad on the right

The code block holds the deck's `.lib`, `.temp`, `.option`, `.param` and `.save` lines and its
`.control` section, unchanged. The `.include` lines are not needed. The enable net is `en`, as in
the decks.

| sheet | deck reference | from the sheet's netlist (ngspice-47, tt 27 C) |
|---|---|---|
| `tb_pd_leak` | total 0.104 nA (bias 0.030, front end 0.054, vddo 0.020) | itot 1.0358e-10 A (ibias 3.02e-11, idrv 5.39e-11, iddo 1.96e-11) |
| `tb_pd_enable` | 1.542 ... 1.761 V, 1 mV after 0.87 us; disabled 1.646 ... 1.650 V | emin 1.54232, emax 1.76131 V, t_1mV 0.8710 us; dmin 1.64592, dmax 1.65006 V |
| `tb_pd_unpowered` | V_SG(OP) -0.558 ... +0.002 V, V_GS(ON) 0 ... 0.714 V, 2.36 / 0.23 mA, vddo 3.83 V | pmin -0.5583, pmax 0.0021, nmax 0.7137 V, ipm 2.356 mA, inm 0.227 mA, vddm 3.830 V |
| `tb_pd_startup_oa` | I_Q 212.0 uA, within 10 % from 10.9 us after the edge | iqf 212.02 uA, t1 11.92 us (edge at 1 us), t2 1.21 us; the deck itself gives the same |

In `tb_pd_startup_oa`, the deck's `.save` and its interactive `plot` name `xb.xc.vbr` and
`xb.xc.ks`, the core's nodes in the hierarchical netlist. In the flat sheet `d2s_bias_oa_pd`,
they are `xb.vbr` and `xb.ks`. The code block is unchanged as required, so ngspice skips those
two vectors. The measurements do not use them.

To simulate a sheet, put the PDK `.spiceinit` in the netlist directory, then run:

```
xschem --rcfile xschemrc -n -s -q -x -o net tb_pd_enable.sch
cd net && ngspice tb_pd_enable.spice
```

## How the sheets were checked

- **Cell sheets.** Each sheet was netlisted with xschem 3.4.8RC, with
  `xschem --rcfile xschemrc -n -s -q -x -o <dir> <sheet>.sch`. It was then compared device by
  device with its `.subckt` in `../sim/`, using the method of
  `../../improvements/xschem/check_xschem.py`. The comparison covers model, terminal nets in
  order, w / l / ng, the port order of the `.sch` and the `.sym`, and `unit_r2` against
  `../../improvements/sim/units.spice`. The four bias cells are compared against their
  `.subckt` flattened through `inv_3v3_pd`, `d2s_bias_in_tree_pd`, `oa_core_pd` / `bg_core_pd`
  and `d2s_bias_diodes`. Result: 0 mismatches for all five. The check was tested on a copy with
  two planted faults: SB's gate label changed to en_3v3, and two pins swapped in a `.sym`. It
  reported both.
- **Geometry.** A geometric pass found:
  - no dangling wire ends
  - no net crossing itself
  - no component joining two net names
  
  Wires that cross without a dot are not connected (xschem joins wires only at end points). The
  new devices add 6 to 11 such crossings per bias sheet and 9 on `d2s_mpdda_pd`.
- **Testbenches.** Every element (name, nets with GND = 0, value or model and sizes) and the
  code lines were compared with the deck. Result: 0 mismatches. Each sheet was then simulated
  from its netlist (table above).
