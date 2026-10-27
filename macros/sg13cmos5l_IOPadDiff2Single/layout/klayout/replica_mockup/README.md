<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# replica_mockup

A mock-up, not the pad cell (2026-10-27): `../sg13cmos5l_IOPadDiff2Single.klay.gds` with the class-AB replicas
RP1 / RN1 built into clamp frames grown by the replica fingers. Top cell `sg13cmos5l_IOPadDiff2Single_replica_mockup`.

- `Clamp_P_M1` ng 43, l 0.6 µm: OP 82 fingers, RP1 = the centre gate column (2 fingers), its drain partner a dummy
  with the gate on iovdd. I_Q ratio 82 / 2 as before.
- 2 × `Clamp_N_M1` ng 35, l 1 µm: the upper frame carries RN1 as an S-G-D-G-S pair at the centre drain;
  ON = 35 + 33 = 68 fingers as in the netlist.
- `DCNDiode` l 67.6 µm, `DCPDiode` l 65.8 µm, centred, so the stripes lie under all comb lines of the wider arrays;
  the top-level n+ band around DCNDiode clipped to the longer diode, its contacts with it.
- The clamps and diodes are static cells from the prototype engine
  (`sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/replica_prototype/clamp_engine.diff`), not PCells: the replica
  option is not in `scripts/pcells` yet.
- Metal2 as in the pad cell since 2026-10-27: N comb from the pad bar up into a junction bar at y 44–50, P comb from
  the bar up to the P frame. n1 (RP1 drain) and n2 (RN1 drain, through a gap in the bar) run up to y 88, where
  RP2 / RN2 would sit; labels `n1`, `n2` on Metal2.
- Checked (klayout.db): devices OP 546.12 / 0.6, RP1 and dummy 13.32 / 0.6, ON 154.0 + 145.2 / 1, RN1 8.8 / 1;
  pad, n1, n2, gates and rails distinct; own Metal1 / Metal2 width and space checks (incl. Mn.e), NWell spacing,
  contacts on Activ / under Metal1, vias landed: clean. Not run: the IHP DRC deck, LVS.
- `replica_mockup.png`: Metal2 by net over the device layers, y 0–92 µm.
