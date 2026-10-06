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
