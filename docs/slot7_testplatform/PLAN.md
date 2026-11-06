<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# PLAN: slot 7 as a stand-alone test platform for the two bias references

Written 2026-11-06 by Claude in a cloud session, after `docs/launch/slot7_testplatform_TASK.md` (branch
`harness-test`). Branch `claude/c5-slot7-testplatform`. Steps and numbers: `RUNLOG.md`.

Goal: a real `slot_7.gds` that is useful on silicon without the custom pads. The Oguey–Aebischer and the Banba
bandgap reference can be enabled, selected and measured only through what every slot has: the shared analog bus,
`dig_in` / `enable`, `dig_out`, the gated supplies. The 13 custom-pad pins stay where they are, so the pads can be
added later without moving anything.

## 1. Facts checked (task file "Facts to start from")

| fact | checked how | result |
|---|---|---|
| slot frame 537.15 x 273 um, harness pins on the left | `macros/slot/layout/klayout/slot.klay.gds` (from `harness-test`), KLayout dump | yes. All signal pins are 2 um Metal3 stubs at x 0..2. Supplies are **TopMetal1** (GDS 126; this stack is Metal1..4 + TopMetal1, so magic's "metal5" in the wrapper is TopMetal1), also at x 0..2: `vdd_1v2` y 2.0..56.8, `vss_1v2` 66.4..96.4, `vss_3v3` 113.5..143.5, `vdd_3v3` 151.1..256.1 |
| ungated supply areas become obstruction | harness `scripts/run_gen_user_wrappers.sh`, `magic/slot7_wrapper.mag` | for slot 7: obstruction `obsm1` / `obsm2` on the right strip x 535.15..537.15 (GDS 8/23, 10/23 in the frame); the frame ground strip at x 533.15..535.15, y 11.6..71.1 (Metal2) is relabelled `vss_1v2`. No other obstruction inside slot 7. The platform stays out of x >= 520 |
| current delivery `slot_7.gds` | `sg13cmos5l_cm_slot7` `main` 40ba9b0 = `harness-test` 4611357 (same sha256) | 13 Metal3 pins at x 535.05..536.45, labelled stubs; `outp`->`vinp`, `outn`->`vinn` joined by Metal4 lines at x 530 / 528 |
| how `analog_bus0..3` reach `analog[0..3]` | harness `verilog/rtl/chipalooza_frame.v` | chip pad `analog[k]` = shared net `user_analog_shared[k]` (one net in `LVS_STRUCTURAL`). Per slot one `analog_switch_med` (hv NMOS + PMOS 10u x 40, gate drive `gate_drive_med`) from that net to the slot's `analog_bus<k>`, enable `select & analog_bus_ena[k]`. The diagnostic switches of project 0 sit on the same net and are off unless `proj_sel` = 0 |
| what drives `enable`, `dig_in`, the gated supplies | `user_project_control{,_base}.v`, `housekeeping.v`, `router.v` | `proj_sel` (SPI reg 0x50) selects one slot; slot 7 = 7. Reg 0x51 = {`analog_bus_ena[3:0]`, `dig_ena`, `1v2_ena`, `3v3_ena`, `proj_ena`} (bit 7..0); `enable` = `select & proj_ena`; gated supplies by `power_stage2` (3.3 V) / `power_stage1v2` (1.2 V), enable `select & ...`. `dig_in[i]` = router output (reg 0x20+i: 0x0..0xB = digital pad `io_in[n]`, **0xD = 0, 0xE = 1**, 0xF = sequencer; **the reset value 0x0 routes every bit to pad io[0]**), through a latch (`dig_ena` = gate, reset while the slot is not selected), buffered by `buf_8` on the harness's **always-on** 1.2 V rail. So `dig_in` / `enable` are valid 1.2 V levels even when the slot's own `vdd_1v2` is gated off, and 0 whenever slot 7 is not selected. `dig_out` of the selected slot is readable in SPI reg 0x38 / 0x39 (`dbus_in`) without a pad |
| reusable layouts | READMEs + the delivery repo's run log of 2026-11-06 | `oa_core_pd`, `bg_core_pd`: PDK KLayout DRC 0, magic+netgen "match uniquely" (property errors only on the simulation-only `mm_ok`). `analog_switch_small.klay.gds` (from the harness's magic layout, in `macros/ocd_analog_switches`): **KLayout DRC 0 (checked today, RUNLOG)**. The harness submodule `sg13cmos5l_ocd_ip__analog_switches` is pinned at `d210467` (same commit the copies were made from) |
| schematics without layout | `en_ctrl_3v3`, `ls_up_1v2_3v3`, `hv_logic`, bias trees | no layout. Substitute: one new cell `tp_en_ctrl` (section 3) |

## 2. What goes on the slot

**Stage A (this session):** the two **cores**, not the full `bias_oa_pd` / `bias_bg_pd`. The cores are what has a
checked layout, and the core output `iout` (~5 uA, sourced) is itself the quantity to measure. The trees of the full
references are stage B.

```
                   vdd_3v3
                     |
 dig_in[0] --+   +---------+   en_oa, en_oa_b   +-----------+  i_oa   +---------------------+
 dig_in[1] --+-->| tp_en_  |------------------->| oa_core_pd|-------->| TG0 analog_switch_  |--> analog_bus0
 enable    --+   | ctrl    |   en_bg, en_bg_b   +-----------+         | small, en dig_in[2] |
 vdd_1v2 (sense)-|         |------------------->| bg_core_pd|-------->| TG1 ..., en dig_in[3]|--> analog_bus1
                 +---------+                    +-----------+  i_bg   +---------------------+
                  |  |
     dig_out[0] <-+  +-> dig_out[1]     (read-back of en_oa / en_bg on 1.2 V)
     dig_out[11:2] tied to vss_1v2
```

**Stage B (only if A is finished):** the bias trees behind the cores, a multiplexer of their bias voltages onto
`analog_bus2`, and the harness `ibias0` / `ibias1` as a third reference (onto `analog_bus3` or into the tree).

## 3. The enable cell `tp_en_ctrl` (replaces `en_ctrl_3v3` + `ls_up_1v2_3v3`)

`en_ctrl_3v3` exists only as a sheet, and it is built for a pad cell whose 1.2 V and 3.3 V rails are not the slot's.
In the slot the 3.3 V logic runs on the gated `vdd_3v3` itself (so a "vdd_3v3 present" detector is moot), and the
inputs `dig_in` / `enable` come from always-on harness logic (section 1). That allows a simpler fail-safe circuit,
the same ratioed principle as `pg_det` in `en_ctrl_3v3`:

```
xb_c = NOT( dig_in[c] AND enable AND vdd_1v2 )      weak hv PMOS 0.3/20 pull-up to vdd_3v3 against a series stack of
                                                    hv NMOS 2/0.45: one per channel (gate dig_in[c]) on a shared pair
                                                    (gate enable, gate vdd_1v2) to vss_3v3
en_c   = NOT xb_c,  en_c_b = NOT en_c               hv inverters 1/0.45 (the hv_logic size) on vdd_3v3
dig_out[c] = NOT xb_c on vdd_1v2                    hv inverter on the 1.2 V rail (read-back)
RD: hv NMOS 0.3/20, gate vdd_3v3, vdd_1v2 -> vss    pulls a gated-off, floating vdd_1v2 low
```

- A core is on only if `dig_in[c]` = 1, `enable` = 1 **and** the slot's `vdd_1v2` is up; every other state, including
  `vdd_1v2` gated off while `vdd_3v3` stays on, gives `en_c` = 0. No latch, so no undefined state. Prototype
  (RUNLOG): low level <= 18 mV at 1.08 V gate drive, 3.6 V, all corners, -40..125 C.
- Cost: ~1.3..2.4 uA from `vdd_3v3` per enabled channel; the cell has no state, so it is slow (tens of ns), which is
  irrelevant for static enables.
- No standard cells, no 1.2 V supply needed for the enables themselves.
- TG enables (`dig_in[2]`, `dig_in[3]`) go straight into `analog_switch_small`, whose own `inv_4` input stage and
  `sw_lvl_shift` run on the slot's `vdd_1v2` / `vdd_3v3`. With `vdd_1v2` gated off a TG's state is undefined, but the
  cores are then off by construction, so no reference current reaches the bus (to be shown in phase 2).

## 4. Pin map

| slot pin | use |
|---|---|
| `dig_in[0]` | OA core enable (AND `enable`, AND `vdd_1v2` present) |
| `dig_in[1]` | BG core enable (same) |
| `dig_in[2]` | TG0: OA `iout` -> `analog_bus0` |
| `dig_in[3]` | TG1: BG `iout` -> `analog_bus1` |
| `dig_in[23:4]` | unused, reserved (stage B, pad enables/selects) |
| `enable` | global enable of both cores |
| `clk`, `reset` | unused |
| `dig_out[0]`, `dig_out[1]` | read-back: `en_oa`, `en_bg` (1.2 V); SPI reg 0x38 bits 0 / 1 |
| `dig_out[11:2]` | tied to `vss_1v2` (defined level for the harness mux inputs) |
| `analog_bus0` | OA output current |
| `analog_bus1` | BG output current |
| `analog_bus2`, `analog_bus3` | unused, reserved for stage B |
| `ibias0`, `ibias1`, `vbias` | unused in stage A (stage B) |
| `vdd_3v3`, `vss_3v3` | cores, `tp_en_ctrl`, TG signal path |
| `vdd_1v2`, `vss_1v2` | TG input stages, read-back inverters, sensed by `tp_en_ctrl` |
| `s7_an_*` (13) | custom-pad pins, labelled stubs exactly as in the current delivery (unconnected, `outp`/`vinp` and `outn`/`vinn` joined) |

## 5. Measurement procedure (SPI writes are register address = value)

Observables: I_OA (OA output current), I_BG (BG output current), read-back bits, fail-safe behaviour, bus leakage.

Path for I_OA: SMU on chip pin `analog[0]` -> shared net -> slot 7's harness `analog_switch_med` (bus 0) ->
`analog_bus0` -> TG0 -> `oa_core_pd` `iout`. I_BG: the same with `analog[1]`, bus 1, TG1, `bg_core_pd`.

Power-up and enable sequence:
1. `0x50 = 0x07` (select slot 7). With `0x51` still 0 everything in the slot is off.
2. `0x20..0x37 = 0x0D` (all 24 `dig_in` routes to constant 0; **the reset value 0x0 would follow pad io[0]**).
3. `0x51 = 0x06` (3.3 V and 1.2 V power gates on; `proj_ena` = 0, `dig_ena` = 0).
4. `0x51 = 0x0E` (`dig_ena` = 1: latches transparent, all `dig_in` = 0).
5. `0x51 = 0x0F` (`enable` = 1). Cores still off (`dig_in[1:0]` = 0).

Measuring I_OA:
6. `0x22 = 0x0E` (`dig_in[2]` = 1, TG0 closed); `0x51 = 0x1F` (harness bus-0 switch closed).
7. SMU on `analog[0]`: force V_F (default 0.7 V, about the gate voltage of the NMOS input diode the core normally
   drives; sweep 0..2 V for the compliance curve), measure I_leak (core still off).
8. `0x20 = 0x0E` (`dig_in[0]` = 1, OA on). Read `0x38`: bit 0 = 1. Measure I_on. **I_OA = I_on - I_leak** (current
   flows out of the pin into the SMU; sign by the SMU's convention).
9. Fail-safe checks, each followed by restoring the state: `0x51 = 0x1B` (1.2 V gated off) -> I back to I_leak;
   `0x51 = 0x1E` (`enable` = 0) -> I back to I_leak, read-back bit 0 = 0.
10. `0x20 = 0x0D`, `0x22 = 0x0D`, `0x51 = 0x0F` (OA off, TG0 open, bus switch open).

Measuring I_BG: steps 6..10 with `0x23` (`dig_in[3]`), `0x21` (`dig_in[1]`), `0x51` bit 5 (`0x2F` / `0x2B` / `0x2E`),
`analog[1]`, read-back bit 1. Both at once: bits 4 and 5, two SMUs.

Over temperature (-40 / 27 / 125 C): repeat 6..10 at each point; I_leak grows with temperature (17 other slots'
open `analog_switch_med`, the pad's ESD diodes, TG0 / TG1), hence the subtraction at every point.

Power-down: open the bus switches (`0x51` bits 7..4 = 0) and set the SMU to 0 V **before** gating off `vdd_3v3`. With
`vdd_3v3` off and a voltage on the bus, the TG PMOS and the core's output PMOS drain conduct into the floating
`vdd_3v3` (junction to the n-well); phase 2 quantifies this.

## 6. Floorplan (slot-local um; final numbers in the layout script)

```
 y 273 +-------------------------------------------------------------------------------------------+
       |TM1 vdd_3v3 (from the left stub y 151..256)              | free: stage B (trees, mux),  |pads|
       | +-----------+  +-----------+                             | bias/enable for the custom  |x>=520
       | | oa_core_pd|  | bg_core_pd|  (M1/M2 only: M3/M4 may     | pads later                   |13 stubs
   ~150| +-----------+  +-----------+   cross them)               |                              |
       |TM1 vss_3v3 (113..143)                                    |                              |
   ~110| [TG0] [TG1]  analog_switch_small x 2  <- analog_bus0/1  |                              |
   ~ 90| [ tp_en_ctrl ]  <- dig_in[3:0], enable (y 78..90)        |                              |
   ~ 70|  dig_out[11:0] (y 72..77) tie / read-back; TM1 vss_1v2   |                              |
       |TM1 vdd_1v2 (2..57)                                       |                              |
   y 0 +-------------------------------------------------------------------------------------------+
       x 0 (harness pins)                                    x ~140                              x 520
```

Routing: signals on Metal2/Metal3 from the left-edge pins; Metal4 vertical; TopMetal1 for the supplies (straps no
wider than 20 um, slit rules), via stacks down to the cells' Metal1/Metal2 rails. Everything at x < 140 except the
pad stubs, so x 140..520 stays free.

## 7. Pads: keep them, and the fallback swap

- Custom pads (current plan): the 13 `s7_an_*` Metal3 pins and their stubs at x >= 527 are copied unchanged from the
  current delivery `slot_7.gds`, so the GDS fits the custom-pad wrapper of `custom-pad-test` as before. Later the
  pads' `iref` (a sourced reference current into the pad's own NMOS diode) can be fed from the cores through
  `bias_dist_pd`, their `en_3v3` / `en_3v3_b` from a third channel of `tp_en_ctrl`, `vref` / `vcm` from `vbias`.
- Fallback with foundry `sg13cmos5l_IOPadAnalog` pads: `config.txt` `s7_an[0]:  sg13cmos5l_IOPadAnalog  s7_an_0` and
  `s7_an[1]:  sg13cmos5l_IOPadAnalog  s7_an_1`, `make config ... wrappers`; in `slot_7.gds` remove the 13 stubs and put
  back the frame's own right-edge pins `s7_an[0]` (Metal3 x 535.05..536.44, y 132.16..156.93), `s7_an[1]` (y
  242.16..266.93) and `s7_an_0_esd` (x 535.15..537.15, y 163.415..163.905). The layout script gets an option for
  this (`--pads foundry`). Both variants live only in x >= 527, the platform in x < 140: no collision (checked by
  the script).

## 8. Checks planned

- Phase 2: ngspice (xschem netlist) of the stage-A cell: enable / disable of each core, read-back, `iout` into a
  voltage-held bus (SMU model at 0.7 V, sweep 0..2.5 V) over `tt ss ff sf fs` x -40 / 27 / 125 C (plus the resistor
  corners for BG), leakage of open TGs, gated supplies off (no current, no back-feeding).
- Phase 3: PDK KLayout DRC (feol + beol) of `tp_en_ctrl` and `slot_7`; magic + netgen LVS against the sheet.
- Phase 4: harness flow on `claude/c5-testplatform-test`, net-by-net extraction check of the pre-fill top.
