<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Running log: alternatives to the source-degenerated pad buffers

Session 2026-10-26 (from 02:13), Claude (configured model `claude-fable-5-1`; the serving model may differ),
cloud container linked to Christoph's computer, attached to the claude.ai Project "Chipalooza sg13cmos5l".
Newest entries at the bottom. Times are Europe/Berlin (CET).

Task, from Christoph's message of 02:13: the source-degenerated `s2d_mpdda` / `d2s_mpdda` may take too
much space; search the literature for alternatives that use less area and, ideally, are faster than
about 1 MHz and have a wider voltage range. Second: look at the consolidation chat log and running log
and find a way of logging the work that does not get the logging stopped.

Result: `alternatives.md` (this folder). Chat log: `sudelbuecher/chatlog/2026-10-26_fable_pad_buffer_alternatives.md`.

## 02:13–02:17: context

- Read: memory (Project files); the `_sudelbuecher` `CLAUDE.md`; `chatlog/README.md`;
  `chatlog/2026-09-28_opus_safety_stops_and_chatlog_export.md`;
  `verbatim_chatlog_recovery/verbatim-chatlog-export.md`; `consolidation/log.md` (head and tail);
  `pad_buffer_layout/log.md` and `layout_primitives.md` §4–6; `class_ab_pad_driver.md` §I–VII;
  `s2d_input_buffer.md` (summary, §I–II); `improvements/proposed_improvements.md` §II, §VII;
  `units.spice`, `d2s_mpdda.spice`; the two Project images.
- No git command.
- Starting point taken from those files:
  - `d2s_mpdda`: 4 × `unit_r2` (20/1 PMOS pair, 2 × 5/6 tails, 150 kΩ rhigh), fold with 36/6 sinks and
    30/3 cascodes, 24/4 loads, Hogervorst class-AB, two MOS Miller capacitors 16 × 16; 2014 µm² drawn,
    296 µA, loop 1.5–2 MHz, offset σ 5.3 mV, gain over corners −0.16…0 %.
  - `s2d_mpdda`: 6 × `unit_r2` (4 signal + 2 CMFB), fold, MOS load capacitors; 2680 µm² drawn
    (≈ 5500 µm² with spacing against ≈ 6500 µm² available), 99 µA, 1.6 MHz, 67.6 dB.
  - Both: inputs are PMOS gates, usable only ≥ 1.3 V below vdd; vcm = 1.2 V.
  - The design rule of `proposed_improvements.md` §II: in the matched-pair DDA a unit qualifies only if its
    output depends on gp − gn alone. `unit_t` (triode), `unit_w` (bulk) and `unit_q` (square-law) failed
    that test (DDA error 29–200 mV at ±0.5 V against 1 mV for `unit_r`).

## 02:17: four literature searches started (parallel agents, web only)

1. compact rail-to-rail class-AB buffers (LCD column drivers, constant-gm inputs, FVF buffers,
   single-stage load-compensated);
2. single-to-differential converters (DDA-based, active balun, current-conveyor, pseudo-differential,
   complementary/bulk-driven inputs, the resistive FDA as the reference point);
3. linearized transconductors and DDA/CFIA gain-by-matching (resistor-free linearization, K–J-type
   triode degeneration, strong-inversion pairs, bulk-driven, Nauta; current-source area rules);
4. open-PDK precedents (Chipalooza, IHP SG13G2, sky130, gf180) with area and bandwidth numbers.

## 02:18: decisions (Christoph, verbatim)

> "it would be nice if poly resistors could be avoided altogether. they tend to be bulky and their
> parameter spread could be all over the place."

> "Make that a firm, not a hard constraint."

- The first three searches were cancelled by the interruptions and started again at 02:19 with the
  resistor preference in their briefs: MOS-only first, resistor-based candidates listed but ranked below.

## 02:20: logging method

- Precedent followed: `verbatim_chatlog_recovery/verbatim-chatlog-export.md`. This log is written by
  hand in the design folder (decisions verbatim, results, checksums). The chat log is built by script
  from the session transcript: user messages and visible replies verbatim, tool calls as `*[ ]*`
  summaries (tool name, first line of the main argument cut at 150 characters, errors), nothing else.
  The script checks that every user and assistant text is present and that no 40-character window of
  the excluded material occurs in the file, and prints counts only.
- Dry run at 02:20: 3 turns, 4 assistant texts, all present, overlap 0.

## 02:27–02:48: searches returned

- Four reports, saved verbatim as `research/1_rail_to_rail_buffers.md`, `2_s2d_converters.md`,
  `3_linearized_transconductors.md`, `4_open_pdk_precedents.md` (each with its source list).
- Checked on this computer: `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/ngspice/models/` carries the same
  `sg13g2_moshv_mismatch.lib` the third report quotes (hv NMOS factuo 0.005, hv PMOS 0.004 per √µm²).
- The reports' own derivations are marked as such inside them; the agents could not reach IEEE Xplore,
  so several numbers come from open copies or from comparison tables in other papers.

## 02:49: result saved

- `alternatives.md`: starting point from the project's own notes; the three governing relations
  (Gm × range ≈ I_tail for class A; only CM dependence and mismatch matter in the matched-pair DDA; the
  pad pole caps the d2s at ≈ 3 MHz at 100 pF); a table of resistor-free units (K–J triode degeneration,
  Nauta inverter pair, large-V_ov pair with cascoded tail, cross-coupled quad, class-AB pairs,
  complementary pairs; bulk-driven stays rejected); architecture levers (bias root per slot, current
  sources at V_ov 0.5–0.6 V sized from the PDK's A_VT, s2d as two unity-gain DDAs without CMFB, the
  Miller capacitors only go with a capacitive-only load spec); range; precedents; next steps.
- Area by group of `d2s_mpdda` from the netlist: tails 240, sinks 432, cascodes 360, loads 192, pairs
  160, Miller caps 512, rhigh 100 µm² — the resistors are 5 % of the drawn area.
- Transferred with `device_commit_files` from fresh file names; sha256 on both sides:
  `alternatives.md` 9455c3f5…, research 1–4: 6f865e8c…, 20698d12…, a05d5e93…, 05bc104d….
- No classifier stop so far in this session.

## 02:50: logs

- This log, then the chat log by the export script (counts printed by the script are in the chat log's
  header), then the `chatlog/README.md` entry with a `.bak` copy first.

## 02:50–02:51: new task (Christoph, verbatim)

> "pad load must tolerate resistive (and transmission line, if the buffer is not WAY too slow for these,
> anyhow) loading. Explore how much a minimal output resistance >50 Ω will buy us."

> "I can't cleanly tell apart series and load resistance, apparently."

- Read as: R_s = series resistance inside the pad cell (ours), R_L = the bench's load; study R_s with
  the feedback before and after it.

## 02:52–03:05: toolchain and decks

- Cloud toolchain built after `cloud_environment.md`: ngspice-47 (without X), OpenVAF `5ed9e63`,
  IHP `c271a7e9` sparse, OSDI compiled by the PDK script. The first build failed on apt (no `apt-get
  update`, X libraries); second build fine.
- Staged from the computer: `class_ab_pad_driver/improvements/sim/{units,ccomp,d2s_mpdda,d2s_bias_lp}.spice`,
  `tb/tb_mpdda_{loop,step,dc}.spice`, `results_improvements.txt`. Netlists unchanged.
- `tb_mpdda_loop` reproduces its reference: 78.9 dB, 1.37 MHz, 72.4°.
- Two deck templates derived from the loop and step decks: `Rs vout_a vout`, feedback node and load as
  placeholders filled by `sed` in a shell loop. Settling at the pad computed from `wrdata` output
  (last excursion outside ±1 % of the step within 1–4.9 µs), because `meas … cross=last` picked up the
  falling edge at 5 µs.

## 02:55: question (Christoph, verbatim)

> "In parallel, how completely off the beaten path can you think to come up with pad driver / pad input
> to internal differential signal buffers?"

- Answered in the chat (12 ideas: current-output pad driver; current-input / virtual-ground pad using
  `padres`; clamp frames as a complementary FVF; `padres` as feedback resistor; two-path fast/slow
  driver; trim via the harness IDAC instead of matching; chopper S2D with switches only; 1-bit ΣΔ over
  digital pads; LV units behind HV cascodes; MOS-cap attenuator with a pseudo-resistor DC path;
  differential I/O on two pins; CML-style current-steering driver). No file written for it; it is in
  the chat log.

## 03:06–03:12: results

- Loop sweep (feedback before / at the pad × R_s 0, 50, 200, 500 Ω × five loads), step sweep at the pad
  (feedback before R_s), and a 50 Ω line of 1 m / 2 m with an open and a terminated far end. R_s = 0 rows
  reproduce `results_improvements.txt` exactly (loop: 53.1/78.9/104.3 dB; step: 943/327/309/361/2687 ns).
- Feedback before R_s: 1 nF margin 24° → 37° (50 Ω) → 63° (200 Ω) → 80° (500 Ω); 50 Ω load loop
  0.23 → 0.42 → 0.78 → 1.15 MHz; pad amplitude into 50 Ω halves at R_s = 50 Ω; 1 kΩ gain error −4.8 %
  at 50 Ω. Feedback at the pad: worse in every cell. The lines are lumped at this speed (170 ns rise
  against 10–20 ns round trip): overshoot 6.3 → 6.1 % with R_s = 50 Ω.
- Written: `series_resistor.md`, `sim/tb_rs_loop.tpl`, `sim/tb_rs_step.tpl`, `sim/loop_results.txt`,
  `sim/step_results.txt`.
