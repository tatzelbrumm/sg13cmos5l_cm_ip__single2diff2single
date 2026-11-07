<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# bias_dist_pd: switchable distribution mirror (3 inputs, 4 outputs)

New on 2026-10-27, for the floorplan with the generator in the slot's main area: one or more reference currents in,
one copy per pad tree out, each input and each output switchable.

```
iin0..2 --TG(en_in<k>)--+-- ni: NI (NMOS diode 6u/6u) --- NM (6u/6u) --- vpd: PD (PMOS diode 5u/6u)
                        |                                                  |
                       TDN (ni -> vss while disabled)            PO0..3 (5u/6u) --TG(en_out<j>)-- iout0..3
```

- Inputs: *sourced* currents (from `bias_gen_pd`'s `iref`, `oa_core_pd` / `bg_core_pd` directly, or the harness
  `ibias`). Every input with `en_in<k>` = 1 passes its transmission gate; enabled inputs add in NI.
- Outputs: *sourced* copies, 1 : 1, into the NMOS input diode of a `bias_tree_pd` (one per pad). A disabled output's
  TG is open and its PO carries no current. The trees keep their own TG and TDN.
- en_3v3 = 0: every TG open, TDN pulls ni to vss, SVPD pulls vpd to vdd. Enables: `en_in<k>` / `en_out<j>` are gated
  with en_3v3 by nand2_hv + inv_hv, as in the selector's decode.
- Devices: those of `bias_tree_pd` (NI 6u/6u like the tree's NI, PD / PO 5u/6u like BP, switches 1u/0.45u). The
  current passes two mirrors more than with the generator next to the tree: their mismatch adds to the tree's.

Ports (order): `vdd vss en_3v3 en_3v3_b iin0 iin1 iin2 en_in0 en_in1 en_in2 iout0 iout1 iout2 iout3 en_out0 en_out1
en_out2 en_out3`.

## Truth table

`ei<k>_b = NAND(en_3v3, en_in<k>)`, `ei<k> = NOT ei<k>_b`; input TG k (TIN<k> gate `ei<k>`, TIP<k> gate `ei<k>_b`)
conducts when **en_3v3 = 1 and en_in<k> = 1**. Likewise `eo<j>` for output TG j (TON<j> / TOP<j>): conducts when
**en_3v3 = 1 and en_out<j> = 1**. TDN (gate `en_3v3_b`) pulls `ni` to vss; SVPD (PMOS, gate `en_3v3`) pulls `vpd` to
vdd when en_3v3 = 0.

| en_3v3 | en_3v3_b | en_in<k> | en_out<j> | iout<j> | ni | vpd |
|:-:|:-:|---|---|---|---|---|
| 1 | 0 | one input on | on | 5.07 µA (1 : 1.014 of the 5 µA input) | 0.91 V | 1.97 V |
| 1 | 0 | two / three inputs on | on | 10.08 / 15.07 µA: enabled inputs add | 1.05 / 1.15 V | 1.69 / 1.47 V |
| 1 | 0 | any | off | 0 (0.2 pA) | as above | as above |
| 1 | 0 | none | on | 0 (1 pA) | 0.11 V (floats on NI) | 3.10 V |
| 0 | 1 | any | any | 0 (0.2 pA): disabled | 0 (TDN) | 3.3 V (SVPD) |
| 1 | 1 | input on | on | 0 (0.6 pA); the enabled input's 5 µA flows into TDN | 7 mV | 3.25 V |
| 0 | 0 | any | any | 0 (0.2 pA) | 0.11 V (floats) | 3.3 V (SVPD) |

The last two rows are invalid enable states (en_3v3 / en_3v3_b not complementary): nothing conducts to an output,
nothing is damaged; with both high an enabled input's current is wasted in TDN. Simulated: `testbenches/spice/tb_truth.spice`
(tt, 27 °C, 3.3 V; 5 µA PMOS-mirror sources into the inputs, 6u/6u NMOS diodes as loads), output in
`testbenches/spice/tb_truth.out`, 2026-11-07.

## Files

```
schematic/xschem/bias_dist_pd.sch/.sym   sheet drawn by hand in readable analog style (2026-11-07, xschem-analog-schematic
                                         skill): wires, devices upright, groups [D] enable decode, [S] switches,
                                         [M] mirror, [O] PMOS outputs; symbol unchanged
schematic/bias_dist_pd.png / .svg        render of the sheet
schematic/xschem/xschemrc                adds hv_logic
netlist/source/bias_dist_pd.spice        source netlist (with hv_logic.spice)
testbenches/spice/tb_truth.spice / .out  truth table, DC (ngspice -b in this folder, repo environment)
```

Checked 2026-10-27: xschem's netlist of the sheet against the source subckt, device by device (37 devices, equal),
symbol pin order = source port order. Simulated only for its truth table (2026-11-07, above); no CACE suite yet. To be decided: the number of inputs and
outputs (3 / 4 here), where `en_in<k>` / `en_out<j>` come from (static configuration bits through `ls_up_1v2_3v3`),
and the matching requirement, which sets NI / NM / PD / PO sizes.

Redrawn 2026-11-07 from the label-style sheet (Christoph: "a human readable schematic that contains everything is a
good start"): xschem's netlist against the source subckt 23 = 23 devices, 14 = 14 gate instances, ports equal;
topology-equivalent to the label-style sheet (`scripts/xschem/sheet_equiv.py`); no short (`sch_lint.py`); xschem exit 0,
no `Error:` in its log. The supply pins of the hv_logic gates join vdd / vss by label: wired, every `iin` / `po` line
would cross them (88 crossings against 45).

## Layout note: a later split into analog and digital cells (not done)

Christoph, 2026-11-07: "For layout purposes, maybe some split of bias_dist_pd into analog switches and digital control
might prove advantageous." Two clean cuts (from the redraw):

- **A, strict:** a digital cell of 7 `nand2_hv` + 7 `inv_hv` (in: `en_3v3`, `en_in0..2`, `en_out0..3`; out: 14 control
  nets `ei<k>` / `ei<k>_b` / `eo<j>` / `eo<j>_b`) and an analog cell (TGs, mirror, outputs) that takes the 14 control
  nets, `en_3v3` (SVPD) and `en_3v3_b` (TDN).
- **B, by row (probably better for layout):** one switch slice per input and output (nand + inverter + TG; ports in,
  out, `en_3v3`, `en_k`, vdd, vss; the logic-to-switch nets stay inside the slice), 7 slices around one analog core
  (NI, NM, TDN, PD, SVPD, PO0..3) whose boundary nets are `ni`, `po0..3`, `en_3v3`, `en_3v3_b`, vdd, vss. The matched
  devices (NI / NM 6u/6u, PD / PO 5u/6u) stay together in the core; the decode is static configuration and makes noise
  only when the configuration changes.

**The recurring transmission gate** (7 here: TIN / TIP, TON / TOP) is the project's standard 1u / 0.45u hv TG, NMOS
bulk on vss, PMOS bulk on vdd; the same pair is TGN / TGP in bias_tree_pd, bias_tree_noab_pd and bias_tree_rb, TEN / TEP
in bias_gen_pd, and the S2D pad's TPP / TNP. No cell of its own exists in the schematics (the devices sit flat in each
sheet). Layout cells exist: `d2s_tgsw_f2` in the d2s pad (TGN + TGP + the pull-down TDN, 7.0 × 3.65 µm) and the s2d
pad's split across its tree rows; the harness's `xgate` (`../ocd_analog_switches`: ports `ena_b vdd in out vss ena`)
is the same circuit with 2u / 0.5u devices, a KLayout layout and no level shifter. A slice cell of option B would make
the TG a cell.

Open questions from the redraw: `iin<k>` are `inout` on the symbol but `iout<j>` are `out`, although both are current
nodes; `en_3v3` and `en_3v3_b` are separate ports, so the caller must keep them complementary (both high would let TDN
pull `ni` to vss with input TGs on).
