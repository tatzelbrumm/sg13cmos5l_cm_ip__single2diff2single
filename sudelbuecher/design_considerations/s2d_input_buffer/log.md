<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Running log — pad input buffer (single-ended pad → fully differential), sharing the driver's bias

Session 2026-10-20, Claude (configured model `claude-opus-5-5`; the serving model may differ).
Newest entries at the bottom. Times are Europe/Berlin, taken from the session transcript.

Task as given: propose an architecture for an analog input pad → on-chip fully differential signal,
matching (sharing bias infrastructure with) the differential → single-ended buffered output pad and
its refinements. Propose specifications and characterization / verification suites, including CACE.
Keep logs and chatlogs consistent with the `_sudelbuecher` precedent.

Everything new is in this folder. Nothing in `../class_ab_pad_driver/` was edited. Nothing was
written to the main repo, `~/DoNotLitter` or the harness.

## 15:17 — reading (sources indexed, not copied)

- `_sudelbuecher/CLAUDE.md`; main repo `CLAUDE.md` §6 (where the record lives, chat-log rule),
  `TOP_LEVEL_MODULE.md` §1–§4.
- `chatlog/README.md`, `chatlog/2026-10-06_opus_class_ab_pad_driver_cace_verification_setup.md`.
- `verbatim_chatlog_recovery/verbatim-chatlog-export.md` (how to export a chat log without the
  `[reasoning_extraction]` stop) and `chat-recovery-after-compaction.md`; `cloud_environment.md`.
- `description/s2d_d2s_pinbuffers.md` (the proposal and its nine tests).
- `design_considerations/s2d_input_buffer_topology_verbatim.md` (the topology sketch this work
  sizes), `pad_test_circuit_suggestions_verbatim.md` (test modes).
- `class_ab_pad_driver/`:
  - `class_ab_pad_driver.md`;
  - `improvements/{proposed_improvements.md, bias.md, log.md}`;
  - `power_down/{kickoff_power_down.md, log.md}`;
  - `build_verification_suite/kickoff_build_verification_suite.md`;
  - `verification/cace/{README.md, d2s_miller_biased.yaml, first_run_summary.md, templates/}`.
- Netlists `improvements/sim/{units, d2s_mpdda, d2s_bias_lp, d2s_bias_ref}.spice`,
  `power_down/sim/{d2s_mpdda_pd, d2s_bias_ref_pd}.spice`.
- Main repo `macros/`: `sg13cmos5l_IOPadSingle2Diff` is a stub (pins in, vcm, outp, outn, vdd,
  vss). `ls_up_1v2_3v3` has the newest CACE layout (`results/`, `scripts/cace/cace_to_csv.py`).
- Project doc `claude/sg13cmos5l_pad_cell_internals.md` (IOPadAnalog, padres, 586.9 Ω).
- `sg13cmos5l_ocd_chipalooza`: `config.txt` (11 allowed pad types, default `IOPadAnalog`),
  `scripts/parse_config.py` (the slot gets `padres` as `<name>_esd`), `verilog/gl/sg13cmos5l_padframe.v`.

What the reading showed:

- The input pad is a standard `IOPadAnalog`; the slot sees `padres`. No custom pad is needed for an
  input with gate-only inputs. The driver's case (a), with the clamp frames used as output devices,
  is a pad type outside the harness's list.
- The topology sketch (`s2d_mpdda`) fits the driver's units and bias lines directly.

A slip, recorded: before reading the CLAUDE.md rule "no git commands without asking", the first
listing commands ran `git log` in both worktrees and `git status` in the main one. Checked right after:
no `index.lock` or other lock file in either `.git`. The `_sudelbuecher` worktree's `.git` points to
a host path that the sandbox does not mount, so `git log` there did nothing. No git command since.

## 15:24 — cloud environment

Built as `../../cloud_environment.md` pins it: xschem `ddc7344`, ngspice-47, OpenVAF `5ed9e63`,
IHP-Open-PDK iic-jku `c271a7e9`, with OSDI compiled into `libs.tech/ngspice/osdi`, plus
`libs.ref/sg13cmos5l_io/cdl`. CACE 2.11.0 under Python 3.12. That is the version the IIC-OSIC-TOOLS
2026.09 image installs (`_build/images/iic-osic-tools/skel/headless/scripts/install_eda.sh`).

Tool check: `improvements/sim/tb/tb_mpdda_loop.spice` gives 78.9 dB / 1.366 MHz / 72.4°, and
`tb_mpdda_dc.spice` gives gain 0.49994, 0.055 mV, 1.24 mV and 295.8 µA. Those are the references in
`results_improvements.txt`.

CACE 2.11 needs an xschem `.sch` for the DUT and for every template; `.spice` templates are
unimplemented there ("TODO: Implement substitution for spice templates!").

## 15:29 — netlists (`sim/`)

- `s2d_mpdda.spice`: four signal units (A1 = A2, F1, F2), a folded cascode, a CMFB from two more units
  into a cascoded PMOS diode, mirrored 1 : 1 by the loads. `unit_r2` is included from the driver's
  `units.spice`, not copied.
- `s2d_bias.spice`: `s2d_bias_diodes` (four of the driver's six diodes), the fixture `s2d_bias_lp`, the
  trees `s2d_bias_in` / `s2d_bias_out`, and the fan-outs `bias_fanout_n` / `_p`.
- `s2d_pd.spice`: `en_3v3` wrappers around the unchanged cells.

## 15:34 — first results and two changes

- Operating point: every branch at least 80 mV clear of saturation, output common mode −22 mV off.
  The cause was the sink ratio: the driver's 36/6 µm in four 9 µm fingers against a 24/6 µm CMFB sink
  in four 6 µm fingers. Now SX/SY are six fingers of BN and SXC/SYC four. The output CM error is now
  +10.9 mV, from the units' current against the sinks.
- Loops: the CM loop had 40° at 0.2 pF per output. Two built-in hv NMOS capacitors (12 × 12 µm,
  about 0.55 pF) on the outputs give 70° with no external load.

## 15:36 — signal window

At vdd = 3.0 V and vref = vcm = 1.65 V the nonlinearity is 62 mV (tt) and 140 mV (ss −40 °C): the PMOS
unit tails leave saturation when a gate is above about vdd − 1.3 V. At 1.2 V it is ≤ 0.7 mV at every
corner tried. The driver's units obey the same window, and its vref must equal its input common
mode, so `s2d_input_buffer.md` proposes vcm = 1.2 V for both buffers.

## 15:44 — full characterization (`sim/results_s2d.txt`)

Sections 1–13, made by cloud-only scratch scripts (not shipped); the eight decks in `sim/tb/`
reproduce one case each, and name their reference values. Run times: about 6 min + 4 min on 2 cores.

- Two passes needed fixing. The first rejection pass used node name `gnd`, which ngspice treats as
  ground ("shorted VSRC"). Without mismatch the differential rejections come out as several hundred
  dB, so they were rerun with 20 mismatch seeds.
- The first enable pass used 2 pF loads in the scratch script while the decks had 0.5 pF; rerun at
  0.5 pF.
- Input capacitance: 17 fF.

## 15:47 — xschem sheets (`xschem/`)

`s2d_mpdda`, `s2d_bias_lp` and `s2d_mpdda_biased` (`.sch`, `.sym`), and an `xschemrc` that adds
`../../class_ab_pad_driver/improvements/xschem` for `unit_r2`. The sheets are placed by a cloud-only
generator (not shipped); they are a first pass, to be tidied by hand.

- Round trip (xschem netlist against the `.spice` source, device by device; cloud-only checker):
  MISMATCHES: 0 for `s2d_mpdda` (22 devices) and `s2d_bias_lp` (8). A planted fault (SX's gate moved
  to vbp) was caught.
- The checker caught a real fault first: the CMFB diode's gate trunk had no `vcmfb` label, so the
  loads' gates were a separate net. Fixed before anything else used the sheet.
- Bias pins of `s2d_mpdda.sch` were `ipin` while the symbol said `inout`. xschem reported it when CACE
  netlisted the DUT, and returned status 10. Now `iopin`; status 0.

## 15:55 — CACE (`verification/cace/`)

`s2d_mpdda_biased.yaml` with ten parameter groups (514 runs), five templates written for this
setup (no generator to edit), `README.md`. DUT `s2d_mpdda_biased` = `s2d_mpdda` + `s2d_bias_lp`, as
`d2s_miller_biased`. Runs went to a cloud scratch directory (`--run-path`), so no `_runs/` is shipped.
CACE's datasheet `_docs/s2d_mpdda_biased.md` is shipped without its plots: images pick up a
provenance stamp on the way to the computer.

## 16:00 — design note

`s2d_input_buffer.md`: architecture, shared bias, signal window, performance, enable, proposed
specification, verification suites (decks, CACE, bench), open points.

## 16:03 — CACE runs, and three limits that were wrong

- First full run: 37 of 40 pass. Three failures, all from the setup, not the circuit:
  - f3dB ≥ 1 MHz and 1 % settling ≤ 1 µs were also run at 2 pF of external load. The limits are for
    0.5 pF. Now ac_params runs at 0.5 pF only, and tran_params at 0 and 0.5 pF.
  - Process MC gain 1.83…2.36. The cause is in the PDK, not here: `res_stat` draws rhigh's "global"
    sheet-resistance deviation (`nsig_rsh = agauss(0,1,1)`, 5.1 % σ, `resistors_mod.lib`) in a
    `.model` inside the `rhigh` subcircuit, so ngspice draws it per instance. That acts as 5 % unit
    mismatch. `d2s_miller`'s first CACE run (2026-10-02) shows the same: gain 0.415…0.605 for 0.5.
    mc_params now keeps rhigh at `typ`; global rhigh spread stays covered by the bcs/wcs corners.
- Second and third runs: 40 of 40 pass. The third adds Idd ≤ 125 µA (cell + fixture), the limit that
  matches the specification (see below). 514 runs, 5 min 18 s. Summary: `verification/cace/first_run_summary.md`.
- Mismatch, 100 seeds at vcm = 1.2 V: input offset σ 6.7 mV, gain σ 0.90 %, output CM σ 11.0 mV.

## 16:05 — independent check of the note

A separate agent compared every number in `s2d_input_buffer.md` and this log against
`sim/results_s2d.txt`, the netlists and the yaml. It found seven discrepancies and four smaller items.
All are fixed:

- the run count (514);
- the Idd limit (yaml 150 → 125 µA, so that it matches the specification);
- vdd − 1.7 V → 1.3 V in the yaml;
- the loop row of the specification (0…10 pF in CACE; differential and CM values separated);
- the files that did not exist yet (`first_run_summary.md`, `_docs/`);
- "vd back at 0 within 1 µs" → measured 2 µs after the edge;
- which seeds and which vcm the mismatch rows come from;
- the gain citation (§6);
- the CM phase-margin difference (17° / 10° / 4° at 0 / 0.5 / 2 pF);
- the unit-count explanation of the gain. It now reads: both cells have two input and two feedback
  units; the gains differ by which side is differential.

The specification table now quotes CACE's worst cases next to the tt values.

