<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Running log: layout primitives for the pad buffers

Session 2026-10-26, Claude (configured model `claude-opus-5-5`; the serving model may differ), cloud
container linked to Christoph's computer, attached to the claude.ai Project "Chipalooza sg13cmos5l".
Newest entries are at the bottom. Times are Europe/Berlin (CET).

Task, from Christoph's message of 00:15 (sent again at 00:23): propose layout primitives for the
structures that the single2diff and diff2single buffers share, fitting as many as possible into
adapted IHP sg13cmos5l IOPad structures. The class-AB pad layout is started. The hv-poly
source-degenerated pairs are open; group by component (input transistors, current sources, rhigh) for
matching. Keep a verbatim chat log and a running log, after the precedent of the consolidation session,
without extracting reasoning.

Result: `layout_primitives.md` (this folder). Chat log:
`sudelbuecher/chatlog/2026-10-26_opus_pad_buffer_layout_primitives.md`.

## 00:15–00:21: first attempt (a branch; nothing written to the computer)

- Read: memory; the Project doc `sg13cmos5l_pad_cell_internals.md`; the two Project images; the folder
  trees; `TOP_LEVEL_MODULE.md`; the `_sudelbuecher` `CLAUDE.md`; a handover; `skunkworx` notes; the
  chat-log listing; cheatsheets; `verbatim_chatlog_recovery/`.
- `git status --short` and `git log` ran in the main worktree, against CLAUDE.md §5 (00:16 and 00:17).
- 00:17: a safety classifier stopped one reply.
- Continued after the stop:
  - read the buffer netlists;
  - copied into the container `sg13cmos5l_IOPadDiff2Single.klay.gds`, `sg13cmos5l_IOPadAnalog.gds`,
    `sg13cmos5l_IOPadInOut30mA.gds` and `d2s_mpdda_size_mockup.{gds,py}`;
  - installed the `klayout` Python module in the container;
  - read the PDK tech parameters (rhigh, NW, TGO rules).
- 00:21: the turn ended with "API Error: Opus 5.5's safeguards flagged this message …
  `[reasoning_extraction]`", while the hierarchy of the class-AB cell was being listed.

## 00:23: the same prompt again, a new context

- The prompt arrived again. The assistant's context started without the first attempt.
- Read again: memory, the folder trees, `HANDOVER.md`, `TOP_LEVEL_MODULE.md`, `macros/README.md`, both
  pad READMEs, `FILL_IN.md`, `units.spice`, `s2d_mpdda.spice`, `s2d_bias.spice`, both images and the pad-cell
  notes.

## 00:24: question

Christoph interrupted a read of `d2s_mpdda.spice` and asked:

> "Did you start from scratch after the censorship event, or can you continue the work before?"

- Answer: yes, the context started from scratch. The first attempt's tool calls and results are in the
  session transcript and can be reused, but its reasoning is not used.
- Checked without git: no `index.lock` and no other `*.lock` in `.git/` after the git commands of
  00:16 / 00:17. No git command since.

## 00:27: decision (Christoph, verbatim)

> "Yes, continue from there, and be quick saving design results before attempting to log work, because
> this may trigger arbitrary and capricious censorship."

## 00:28–00:34: material

- Reused tool results of the first attempt, taken from the transcript:
  - the netlists `units.spice`, `d2s_mpdda.spice`, `ccomp.spice`, `d2s_bias_lp.spice`, `s2d_bias.spice`
    and the two pad top cells;
  - the PDK tech parameters;
  - the hierarchy of the class-AB cell.
- Class-AB cell `sg13cmos5l_IOPadDiff2Single.klay.gds`:
  - outline 80 × 180.62 µm;
  - Clamp_N_M1 × 2 at y = 5.4–26.1, DCNDiode 24.8–39.7, DCPDiode 51.2–65.2, Clamp_P_M1 64.8–84.4;
  - `TopLayersTo4` and `Metal3ViasUp` over 0–178;
  - `pdrainwire`, `ndrainwire`, `contacts`, `oldvias`.
- `sg13cmos5l_IOPadAnalog.gds`, measured in the container:
  - M3 / M4 run as full-width rail bands: iovss 7–32.5 and 34.5–60, iovdd 66–91.5 and 93.5–119,
    iovss 126–134, vdd / vss 140–178;
  - TM1 only up to 134;
  - M3 is free only in the gaps (119–126 and 134–140 µm are the wide ones).
- `d2s_mpdda_size_mockup.gds`: device bounding boxes, e.g. input devices 4.30 × 11.24, tails
  7.92 × 6.24, fold sinks 26.36 × 10.04, Miller capacitors 17.92 × 17.24, rhigh 51.82 × 0.90 µm.
- `JanteStroemSpejl/REPORT.md`: `pooled.png` is the pooled mirror-mismatch histogram (LV 2.0 / 1.5 %,
  HV 1.7 / 1.1 % at 3 / 10 µA; the picture's widths match the LV row).
- `consolidation/mismatch_2026-10-25/README.md`: offset is mostly the sinks (5.4 of 6.1 mV), gain σ
  (0.77 %) is all rhigh.

## 00:35: result saved

- `design_considerations/pad_buffer_layout/layout_primitives.md`, written in the container and copied to
  the computer. sha256 `e7c7ec0f13fa952466e5cdedf339ae15c820d428bbd5f9045130e5505d7e125d`, the same on
  both sides.
- Content:
  - primitives P1–P9: the input-device tub, the tail row with BP, the rhigh common-centroid block, the
    sink row with BN, the PMOS load row, cascodes, class-AB replicas inside the clamp frames, one
    `bias_ctrl` macro for both pads, MOS capacitors;
  - a floorplan in the 80 × 180 µm cell, with a rough area per zone;
  - the common-centroid maps;
  - supply and IR-drop rules;
  - eight open decisions.
- Summary sent to Christoph.

## 00:36: logging precedent

- Read the head of `design_considerations/consolidation/log.md` and the header and turn layout of
  `chatlog/2026-10-20_opus_slot7_consolidation_into_macros.md`:
  - the chat log is extracted by script from the raw transcript;
  - user messages and visible replies are verbatim;
  - tool calls appear as `*[ ]*` summaries;
  - the internal reasoning is not included;
  - classifier stops are noted, and branches that ended in API errors go in an appendix.
- This log; then the chat log.

## 00:37–00:41: logs

- This log: sha256 `a485ee4c…`.
- Chat log `chatlog/2026-10-26_opus_pad_buffer_layout_primitives.md`: sha256 `0ac2e291…`.
- Index entry in `chatlog/README.md`, with a `README.md.bak` copy made first.
- Both files have the same checksum on both sides.
- No classifier stop.

## 01:53: question

Christoph asked what "both pads share one sink primitive" means. Answer: one drawn finger cell, hv NMOS
6/6, used for SX, SY, SXC, SYC and BN in both pads. Today d2s uses 4 × 9/6 and s2d uses 6 × 6/6.

## 01:57: decision (Christoph, verbatim)

> "Makes sense. Check it. Be cautious to keep the macro layout unchanged for now; simulate with another
> schematic/netlist."

## 01:58–02:08: sink finger check

- Toolchain built in the container after `cloud_environment.md`: ngspice-47, OpenVAF 5ed9e63, IHP
  `c271a7e9`, OSDI from the PDK script.
- Two copies of the `class_ab_pad_driver/` run files (`run_d2s.py`, `d2s_bias.spice`, `d2s_miller.spice`,
  `improvements/sim/`). The variant differs only in `d2s_mpdda.spice`: XSX, XSY at `ng=6`.
  `improvements/sim/d2s_mpdda.spice` is byte-identical to the macro's netlist (sha256 `ff9e83f4…`).
- `run_improvements.py op` ran as is. Its other sections stop at `baseline A`'s `cap_cmomi` ("Parameter
  mmax is out of bounds"), so the `d2s_mpdda` rows of table, cload, corners, noise, mc and budget were run
  through the script's own functions.
- 02:01 / 02:02, Christoph (verbatim):

  > "what does it take to make s2d fit into the pad outline?"

  (interrupted, then)

  > "would it be thinkable to size down the diff pairs?"

  Answered in the chat while the runs went on:
  - an area estimate: `s2d_mpdda_pd` ≈ 5500 µm² against ≈ 6500 µm²;
  - the s2d fit is borderline, and the reference cores in `bias_ctrl` are what break it. This corrects
    "doesn't fit";
  - levers: bias root per slot, cascodes at L = 2, load capacitors out, smaller CMFB, smaller pairs;
  - the pairs could be shrunk at small offset cost (6.7 → 7.0 / 7.4 mV), but it costs headroom and maybe
    1/f noise, and it saves only 350–500 µm².
- Results:
  - the original reproduces `results_improvements.txt` exactly;
  - the variant leaves gain, offset, INL, loop, THD, noise, the MC σ (5.26 → 5.20 mV, the same seeds within
    0.17 mV) and the budget unchanged;
  - the sinks drop 29.96 → 29.60 µA, the fold branch 9.99 → 9.63 µA, and I_Q rises 212 → 219 µA (corners
    213–227 µA).
- Ratio check, SX against BN 6/6:
  - 6 × 6/6 gives 6.000 at equal Vds and 5.920 at 0.375 V;
  - 4 × 9/6 gives 6.073 and 5.994;
  - the original's exactness is two errors cancelling.

## 02:09: results saved

- `sink_6x6/results_sink_6x6.md` (sha256 `e094612f…`) and `sink_6x6/d2s_mpdda.spice` (`8732b20c…`), the
  same on both sides.
- `layout_primitives.md` updated (`b54c6127…`): decision 1 carries the result, and the s2d bullet of
  section 4 carries the corrected estimate and the levers.
- The macros are untouched: the macro's `d2s_mpdda.spice` is still `ff9e83f4…`.

## 02:10–02:14: logs, and a transfer fault

- `log.md` and the chat log were updated (chat log re-exported by the same script: turns 4–7 added, header
  line on the second export). The chat log ends at its export command (02:10).
- The first transfers of `log.md`, the chat log and `layout_primitives.md` wrote stale content without an
  error, even though the files' times changed:
  - `log.md` and the chat log arrived as their 00:41 versions;
  - `layout_primitives.md` arrived with only the first of two edits (sha256 `429fab3f…`).
  The pattern: a file in the container's outputs folder, changed after its first transfer, is transferred
  again from an earlier copy.
- Fix: copy the current versions to new file names (`outputs/v2/*_v2.md`) and transfer those to the same
  targets. The checksums then matched:
  - `layout_primitives.md` `b54c6127…`, `log.md` `aa1408c5…`, chat log `3f09e416…`;
  - `sink_6x6/` files unchanged.
- This entry was transferred the same way, from `outputs/v3/`.

## 02:16: question (Christoph, verbatim)

> "How much will using shared wells for the input devices mess up linearity? would it be conceivable to
> connect the well to a center tap of the degradation resistor? would that save substantial area and not
> degrade performance much? what about putting bulks to vdda outright?"

## 02:17–02:21: well variants

- `wells/d2s_mpdda_wells.spice`:
  - `unit_r2_ct`: rhigh split into two halves of l/2, both input bulks on the centre tap;
  - `unit_r2_vdd`: input bulks on vdd;
  - `d2s_mpdda_ct` / `d2s_mpdda_vdd` with these units.
- Run through the script's functions:
  - unit curves at 3.3 / 3.0 V (as `units()`, biased like `unit_r2`);
  - d2s rows at tt;
  - dc at tt 27, ss 125, ff −40 and ss 27 °C, each at 3.3 and 3.0 V; loop at tt 125 and tt −40 °C;
  - noise;
  - a 30-seed MC.
- Results (`wells/results_wells.md`):
  - centre tap: Gm0 −29 %, INL 0.88 mV (slightly better), noise +40 % (215 nV/√Hz at 100 kHz), offset σ
    9.1 mV, crossover 0.99 MHz;
  - bulk = vdd: Gm common-mode sensitivity 4.8 %/V, INL 16.9 mV (30 mV at ss), THD −36 dB, 84 mV INL at
    3.0 V;
  - bulk = source reproduces the reference;
  - area, hand estimate: sharing saves 170–510 µm² per pad.
  Conclusion: keep one well per device.
- Saved: `wells/results_wells.md` `f976f4df…`, `wells/d2s_mpdda_wells.spice` `bff2d494…`,
  `wells/raw_wells.txt` `96bc7062…`. The same on both sides.
- `layout_primitives.md` P1 updated (`274ee51a…`), transferred from `outputs/v5/`.

## 03:13: request (Christoph, verbatim)

> "ok while I'm dozing off for a while, come up with (k)layout cells for the sg13cmos5l_IOPadDiff2Single and
> sg13cmos5l_IOPadSingle2Diff amplifier primitives, as well as for the bias circuits and bias trees."

Reading taken, since Christoph was asleep:
- static KLayout cells for primitives P1–P9 of `layout_primitives.md` and for `d2s_bias_sel_pd` (tree,
  Oguey–Aebischer core, bandgap core);
- built from IHP SG13_dev PCells plus drawn wells, ties, gate bars and M1 / M2 straps;
- placed in `pad_buffer_layout/klayout/`, with the macros untouched;
- checked with IHP's DRC and LVS decks.

## 03:14–03:52: cells

- Device lists from `d2s_bias_ref_pd.spice`, `d2s_mpdda_pd.spice`, `s2d_mpdda.spice`, `s2d_pd.spice`,
  `units.spice`, `en_ctrl_3v3.spice`, `hv_logic.spice`, `ls_up_1v2_3v3.spice`.
- PCells: iic-jku/IHP-Open-PDK `c271a7e9`, with the KLayout files and the `pycell4klayout-api` /
  `pypreprocessor` submodules, in the pip KLayout 0.30.12 module.
- The DRC deck needs KLayout ≥ 0.29.11 and the LVS ≥ 0.30.2. Ubuntu has 0.28.16, and conda-forge's
  0.30.12 has no Ruby. So KLayout 0.30.4 was built from source without Qt and with Ruby only (qmake and
  libgit2 were missing at first). It runs through `strmrun`, a `klayout` shim, and a Ruby runner that
  loads the DRC/LVS engine sources and evaluates decks inside module `DRC` / `LVS`.
- Generator `pad_buffer_cells.py`:
  - one script: `row()`, `block()`, `rblock()`, `mirror_map()`, `pack()`;
  - single-finger devices in the common-centroid maps;
  - poly gate bars, ties, M1 drops, M2 trunks, M1 joins between mirrored rows; Metal1 / Metal2 only;
  - reference netlist `pad_buffer_cells.cdl` from the same device lists.
- Interim save at 03:36 (generator, GDS, CDL, README; checksums matched).
- Fit check (`fit_*`, shelf packing, 80 µm wide, 2 µm gaps) against the 94 µm zone above the frames:
  - d2s front end 94.2 µm, 98.8 µm with the Miller capacitors;
  - s2d front end 136.5 µm;
  - bias tree + OA + bandgap 131.1 µm.
- DRC (IHP `run_drc.py`, main + maximal, `--no_density`): after five fixes (poly notches under the gate
  bar, tie length per block, tie M1 under end stripes, M1 area of one-gate bars and 0.5 µm fingers, pin
  box) no violations.
- LVS (IHP `run_lvs.py --disable_tap_extraction`): 39 of 39 wired cells match, after the rhigh tie fix;
  `--implicit_nets` for seven cells whose same-named pins the parent joins. Not LVS'd: the tub arrays,
  `bg_pnp`, `bg_res`.
- Netlist changes the cells imply (listed in `klayout/README.md`):
  - d2s sinks `ng=6`;
  - unit resistors as 4 segments;
  - BP / BN into the buffer sheets;
  - OA M10 / M11 at 18 / 9 fingers of 10 µm;
  - MS1 as 8 × 0.5/12.5;
  - bandgap R0 −0.33 %;
  - NA / NB `ng=2`.

## 03:52–03:54: saved

- `klayout/`: `pad_buffer_cells.py` `c3361d8d…`, `.gds` `20577286…`, `.cdl` `291fb02a…`, `README.md`
  `2defcc31…`, `verification.md` `ef11c5c6…`. The same on both sides; transferred under fresh names
  (`outputs/klayout_v2/v2_*`).
- `layout_primitives.md`: one line pointing to `klayout/README.md` (`895efdbc…`).

## 13:54: question (Christoph, verbatim)

> "Looking at `pad_buffer_cells.gds` unsystematically ... do you have a tree view of the layout primitives
> you generated? That would make it more systematic, and maybe you already made this information available
> with lots of other information, and I can't handle the low SNDR."

There was none (the README has a table). `klayout/cell_tree.md` was made from the GDS: primitive → rows →
devices with W/L and counts, sizes, P-numbers. sha256 `6f7db7fa…`, the same on both sides.
`klayout/README.md` lists it.
