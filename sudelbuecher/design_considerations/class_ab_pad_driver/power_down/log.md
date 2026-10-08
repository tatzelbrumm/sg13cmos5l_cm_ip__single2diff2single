<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Running log — power-down (digital enable) for the class-AB pad driver and its bias

Session 2026-10-06, Claude (configured model `claude-opus-5-5`; the serving model may differ).
Newest entries at the bottom. Times are Europe/Berlin.

Task: `kickoff_power_down.md` in this folder. IHP sg13cmos5l only. `../improvements/` is read-only
for this task; Christoph decides when to merge back.

## 16:44 — kickoff, and where things go

- Files: `sim/` (netlists with `_pd` suffix, `results_power_down.txt`), `xschem/`, `figures/` if
  needed, and this log. Nothing in `../improvements/`, `chatlog/` or `~/DoNotLitter`.
- Transfers: a new staging folder per delivery, `device_commit_files` with mtime guards, sha256
  check afterwards (pixel compare for PNG/SVG).
- Cloud setup (PDK checkout, scratch `xschemrc`, ngspice runs): on hold. Christoph flagged it as
  needing a fix and is asking the improvements session how.

## 16:52 — reading (sources indexed, not copied)

- `../improvements/log.md`, `../improvements/bias.md`, `../improvements/xschem/README.md`
- `../improvements/sim/d2s_mpdda.spice`, `d2s_bias_lp.spice`, `d2s_bias_ref.spice`, `d2s_lc2.spice`
- `../class_ab_pad_driver.md` (its "Not yet included" list names this task)
- main repo: `CLAUDE.md`, `TOP_LEVEL_MODULE.md` §2–§4,
  `macros/OgueyAebischerBias/verification/cace/{_docs/reference.md,netlist/schematic/reference.spice}`
  (`ToBiasStartup`)
- project doc `claude/sg13cmos5l_pad_cell_internals.md`
- Not yet read: IHP `libs.ref/sg13cmos5l_io/cdl/sg13cmos5l_io.cdl` (IHP-Open-PDK dev). No copy
  exists in the two connected folders; waits for the PDK checkout.

What the reading showed:

- `ToBiasStartup`'s `disable` pulls only vbr and vbn low (two NMOS). It leaves the PMOS lines to
  float.
- In `oa_core` and `bg_core`, MS1 is always on (gate at vss), about 0.46 µA.
- With the bias off, ABP and ABN let go of a and b, so the output gates float unless pulled.

## 17:08 — decisions (Christoph, verbatim)

> 1. Signal enabling the block: Assume a 0…1.2V digital signal. I think there's a cowork session
>    looking into level shifters. append the port to the end of the list for now. in a
>    consolidation step we may reorder the port positions later.
> 2. thinking about 1. again ... maybe for now, using en_3v3 as input port may be a good
>    preliminary choice, so the question about the enable logic from available digital ports in
>    the slot would be deferred.
> 3. Plan for case (a), OP and ON are the pad's clamps.
> 4. Investigate and let me know your findings.
> 5. Don't rely on the harness for now. Insert a transmission gate.
> 6. Accept a glitch for now and investigate how bad it gets.
> 7. I also have to guess. Let's assume that `power_3v3_ena` is a static signal, and a dedicated
>    control signal powers our circuit off — maybe bias, buffered output pad, and (eventually)
>    input pad and internal circuitry separately. Key point of this exercise is to figure out
>    where switch transistors to pull bias lines, inputs and outputs etc. need to be included.

So: port `en_3v3`, 0…3.3 V, active high, last in each port list. Its complement `en_3v3_b` is
made locally by one hv inverter on vdd/vss in each cell.

## 17:10 — switch plan, first draft (not simulated)

Principle: pull each current *root* off, plus every node where two pulls would otherwise fight.
Pull everything else only if simulation shows a line drifting into conduction.

| cell | node | switch | on when | why |
|---|---|---|---|---|
| bias tree (`_in`; reused by `_oa`, `_bg`) | iref port → NI | transmission gate | enabled | decision 5: the external source is cut off |
| | NI side of the TG (gates of NBP, NBPC, NABP) | NMOS to vss | disabled | every tree current starts here |
| `_out` | iref port → PI | transmission gate | enabled | as above |
| | PI side of the TG | PMOS to vdd | disabled | as above |
| `oa_core`, `bg_core` | MS1 gate | rewired from vss to `en_3v3_b` | — | the always-on 0.46 µA |
| | vpg (mirror gates) | PMOS to vdd | disabled | holds the core in its zero-current state, so iout = 0 |
| | ks | NMOS to vss | disabled | otherwise ks floats with MS1 off and MS3 could pull vpc |
| `d2s_mpdda` | a (OP gate) | PMOS to vddo, n-well vddo | disabled | OP off; gate tied to its source as in a clamp |
| | b (ON gate) | NMOS to vsso, ON's tap ring | disabled | ON off, likewise |
| | vabp (ABP, FPL gates) | PMOS to vdd | disabled | otherwise vabp floats two leakage-level diode drops (RP1 + RP2) below vddo; ABP, from a at vddo to b at vsso, then sees both as V_SG and conducts |
| | vabn (ABN, FNL gates) | NMOS to vss | disabled | as above |

Expected to need no switch: vbp, vbpc, vbn, vbnc (they carry only leakage once the roots are
off); the DDA inputs (gates only); l1, l2, x, y (no current path once tails and sinks are off);
vout (high-Z with OP and ON off). Simulation decides.

Placement choice: the vabp/vabn pulls go in the driver, not the bias, because the hazard (a
pulled up while b is pulled down) is local to the driver.

Unpowered (vdd = vddo = 0, en_3v3 = 0): neither pull has gate drive. During an ESD event on the
pad, vddo and vdd rise. If en_3v3 stays near 0, the a pull-up gets V_SG = vddo and turns on, and
the local inverter drives `en_3v3_b` high, which turns on the b pull-down. So the same switches
may hold the gates during the event. That is the hypothesis to check against IHP's clamp gate
ties and GateDecode once the `.cdl` is readable. A floating `en_3v3` would defeat it.

Device count added: driver 4 + inverter 2; bias tree 3 + inverter 2; cores 2 more each.

## 19:16 — cloud environment switched to `sudelbuecher/cloud_environment.md`

Built in the container as pinned there: xschem 3.4.8RC `ddc7344`, ngspice-47, OpenVAF `5ed9e63`, IHP-Open-PDK
iic-jku fork `c271a7e9`, OSDI compiled into `libs.tech/ngspice/osdi`. No ev7 stand-in, no OSDI patch, no apt
xschem/ngspice. The sparse checkout adds `libs.ref/sg13cmos5l_io/cdl` (now also in the kickoff). Every number in
this log and in `sim/results_power_down.txt` comes from these tools; none were produced before.

Tool check with the unchanged netlists: `run_bias.py` driver and corners and `run_improvements.py` table, cload,
corners and noise reproduce `results_bias.txt` / `results_improvements.txt` exactly. `run_bias.py startup`
differs in 5 bandgap lines at t_r = 1 µs only: t90 0.1–0.3 µs longer (results file, section 0).

## 19:20 — IHP's clamp practice (`sg13cmos5l_io.cdl` at `c271a7e9`, indexed, not copied)

- Static clamps of `IOPadAnalog` (`Clamp_P20N0D`, `Clamp_N20N0D`): gate tied to its own source through an rppd
  resistor, 6.77 kΩ to iovdd (P) and 1.96 kΩ to iovss (N). Passive, so it also holds unpowered. A resistor of
  that size on a and b is impossible here (µA bias), so this is not an option for case (a).
- Driven clamps of the digital pads (`Clamp_P15N15D`, `Clamp_N15N15D` in `IOPadOut30mA`, `IOPadInOut30mA`): gate
  driven directly by `GateDecode` / `GateLevelUpInv`, whose `LevelUp` output stages run on iovdd and vss. With
  en = 0, `GateDecode` gives pgate = iovdd and ngate = vss. Only an antenna diode sits on the gate; nothing holds
  it unpowered. The rail ESD clamps (`IOPadVdd`, `IOPadIOVdd`: RC-triggered `Clamp_N43N43D4R`) carry the event.
- So the switch plan of 17:10 is the analog counterpart of `GateDecode`, with active ties to the own rail.
- Aside: at this commit `sg13cmos5l_IOPadAnalog`'s port order is `pad padres vdd vss iovdd iovss`. The project doc
  `claude/sg13cmos5l_pad_cell_internals.md` gives `iovdd iovss pad padres vdd vss` for cmos5l. Its source may
  be an older or different repository; worth checking before any positional instance.

## 20:45 — netlists, decks, sheets and results

Files (all in this folder):

- `sim/d2s_mpdda_pd.spice`, `sim/d2s_bias_ref_pd.spice`: the switch plan of 17:10, unchanged. All switches
  and the inverters are 1u / 0.45u hv devices.
- `sim/tb/`: four standalone decks, each naming its reference from the results file: `tb_pd_leak`,
  `tb_pd_enable`, `tb_pd_startup_oa`, `tb_pd_unpowered`. They include `../../../improvements/sim/units.spice`
  and `ccomp.spice`. All four reproduce their reference.
- `sim/results_power_down.txt`: all numbers, sections 0–7. Made by cloud-only scratch scripts (not shipped);
  the decks reproduce one case of each test.
- `xschem/`: cell sheets and symbols of the five `_pd` cells and sheets of the four decks, drawn by a parallel
  agent from copies of the hand-edited `../improvements/xschem` sheets, with the new devices in [E] frames.
  `xschem/README.md` lists the placement. Round trip: MISMATCHES: 0 on all nine (rerun in this session);
  the testbench sheets' netlists reproduce the deck references.

Results:

- **Enabled:** identical to the originals in DC, loop, step, THD, noise and over PVT (I_Q ≤ 0.15 %, offset
  ≤ 0.02 mV). Supply-to-output gain moves by ≤ 2.2 dB, only at 1 MHz and above.
- **Disabled, supply current** (vdd + vddo, vout held at 1.65 V): 0.08–0.35 nA at −40 and 27 °C; 7–34 nA at
  125 °C; up to 47 nA at ff/3.6 V/125 °C with the pad at 0 V. At 125 °C 73–95 % of it is the output stage on
  vddo (OP at V_SG = 0 and its well junctions); the bias cell is ≤ 4.3 nA (bandgap, ff/3.6 V/125 °C), the
  driver front end ≤ 2.4 nA. The output devices are the clamp frames, so this floor belongs to case (a).
- **Disabled, nodes:** a = vddo and b = vsso within 2 µV. The unswitched lines vbp, vbpc, vbn and vbnc sit
  0.06–0.31 V from their rails and carry leakage only, so they need no switch.
- **Start-up after enable:** every variant at every corner reaches its enabled DC operating point, with none
  stuck. I_Q within 10 % after 0.5–0.9 µs (in, out, bg) and 8–15 µs (oa). Supply ramps of 1 and 100 µs
  start correctly with en_3v3 tied to vdd, and with en_3v3 low through the ramp and raised at 1 ms.
- **vout at enable (glitch accepted for now):**
  - Variant in, vd = 0: vout goes 69–123 mV below and 106–142 mV above vref. It is within 1 mV after 0.7–1.1 µs.
  - Variant oa: 92–230 mV below and 190–300 mV above; within 1 mV after 1.2–1.9 µs at vd = 0, but 7–29 µs
    at vd = 1 V.
  - Cause: a and b are released at once, while the bias (slowest in oa) is still coming up.
  - At disable, vout moves ≤ 6 mV before the load takes over; there is no glitch.
- **Unpowered** (not an ESD simulation; no pad diodes or rail clamps):
  - Rails held at 0 V: neither pull has drive, and the Miller capacitors and Cgd lift a and b 0.4–0.56 V above
    their rails.
  - vdd and vddo as one floating rail, as in the slot: the pad charges the rail through OP. The a pull-up then
    turns on by itself, and OP's gate stays within 3 mV of vddo. ON's gate is kicked to 0.68–0.75 V by CMB
    before the rail is high enough for the inverter to turn on SB. ON then conducts briefly into vsso
    (0.13–0.36 mA), like a gate-coupled NMOS.
  - A floating `en_3v3` behaves almost the same as one held at 0 V.
- **Side observation:** at ss/3.0 V/−40 °C with vd = 1 V the enabled output reaches only 2.08 V (in) / 2.13 V
  (oa) instead of 2.15 V. The original `d2s_mpdda` gives the same numbers: the input pairs run out of headroom.
  The enable has nothing to do with it.
