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

## Files

```
schematic/xschem/bias_dist_pd.sch/.sym   sheet in label style (lab_pin on every device pin), generated; symbol
schematic/xschem/xschemrc                adds hv_logic
netlist/source/bias_dist_pd.spice        source netlist (with hv_logic.spice)
```

Checked 2026-10-27: xschem's netlist of the sheet against the source subckt, device by device (37 devices, equal),
symbol pin order = source port order. Not simulated: no CACE suite yet. To be decided: the number of inputs and
outputs (3 / 4 here), where `en_in<k>` / `en_out<j>` come from (static configuration bits through `ls_up_1v2_3v3`),
and the matching requirement, which sets NI / NM / PD / PO sizes.
