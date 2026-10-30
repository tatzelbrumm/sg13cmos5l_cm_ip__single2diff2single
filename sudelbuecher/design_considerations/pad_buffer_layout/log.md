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

## 15:33: questions (Christoph, verbatim)

> "Remind me why .cdl and not .spice ? Seems to be a useful convention I'm not quite familiar with. I went
> through your generated layouts and have a lot of questions ... they're not hand optimized quite yet:
> sudelbuecher/design_considerations/pad_buffer_layout/klayout/pad_buffer_cells_questions.txt  We might
> build some layout pattern skill from iterating this."

- `.cdl`: answered in the chat (LVS netlist with primitive devices vs. simulation netlist with subcircuit calls).
- `klayout/pad_buffer_cells_answers.md`: answers to every question, six generator shortcuts (A–F) behind
  most of them, eleven layout patterns as candidates for a skill. sha256 `af99218a…`, the same on both sides.
- Checked against the GDS while answering: `d2s_pd_n` / `s2d_pd_n` / `bias_tree_sw` are not identical
  (XOR differs in M1 / Via1 / M2, poly for `bias_tree_sw`); no M1 / M2 over any PolyRes body; pnpMPA
  instances 1.0 µm apart.

## 15:46: request (Christoph, verbatim)

> "first of all, take my pad_buffer_cells_questions.txt text, group them meaningfully, and make a markdown Q&A file
> with your answers. Also mention the gds of the subcells the question and answer is about."

- `klayout/pad_buffer_cells_qa.md`: the questions verbatim, in 11 topic groups (cell structure, dummies, gate
  orientation, shared diffusion, rings, metal, special devices, resistors, PNPs, MOS caps, fit / zone), each with
  the GDS cells, subcells, devices and sizes it concerns. Replaces `klayout/pad_buffer_cells_answers.md`.
  sha256 `eaadf085…`, the same on both sides.
- New in it, checked against the GDS: `d2s_cma` = `d2s_cmb` and `oa_misc_p` = `bg_misc_p` (identical geometry);
  rotated input tubs would make a d2s row 87 µm wide; pnpMPA collector rings (Activ) 1.4 µm apart, `bg_pnp` about
  22.9 × 18.5 µm with touching rings; the cascode question answered for the bias devices (NBPC, PBNC, BNC, BPC) too.

## 16:31: bg_pnp check (Christoph's abutted array)

> "Let's get to work. I exported the PNP array and abutment seems DRC legal. Verify, and place the labels in the gap
> between tie and pwell, upper left region, aligned with the array." / "Check LvS while you're at it."

- `klayout/bg_pnp.gds`: 3 × 3 AREF of pnpMPA, pitch 7.15 × 5.67 µm, collector rings fully shared (0.35 µm).
- DRC (IHP deck, main + maximal): clean hierarchically. Flattened: 12 × NW.b1 (NWell gap 1.75 < 1.80 µm, different
  nets), because the bases are not wired yet. Schematic has B = vss for Q1 and Q2: once wired, the NWells are one
  net and NW.b (0.62 µm) applies.
- LVS (reference: 9 unwired pnpMPA, shared collector): all 9 devices match, A = 4p, P = 8u, one collector net;
  the 9 floating base nets match only with ambiguity warnings, and the run reports FAIL.
- Labels: the 9 stale 63/0 labels replaced by "Q1 (ea)" / "Q2 (e2)", size 0.4 µm, left / centre aligned at
  (−3.30, +2.31) from each device centre (upper-left corner of the gap between TIE ring and NWell). Geometry XOR
  unchanged. sha256 `d2c0dc6a…`, the same on both sides.

## 16:45: bg_pnp back into the library (Christoph: "ok reimport the changed bg_pnp.gds into pad_buffer_cells.gds")

- `klayout/pad_buffer_cells.gds`: cell `bg_pnp` replaced by the one in `bg_pnp.gds` (3 × 3 AREF, shared collector
  rings, new labels), on the library's own `pnpMPA` cell (geometry identical, checked). Size 25.7 × 21.6 →
  22.2 × 17.8 µm. All other 130 cells unchanged (shapes and instances compared). Its instances in the top cell
  and in `fit_bias_tree_oa_bg` keep their positions; the fit packing was not redone. DRC of `bg_pnp` in the
  library: clean. sha256 `5fd32afb…`, the same on both sides.
- `klayout/cell_tree.md`: the `bg_pnp` line updated.
- `pad_buffer_cells.py` still generates the old 9-instance `bg_pnp`.

## 17:30: switch cells compacted (Christoph: bias_tree_sw compacted by him, the others "mutatis mutandis", no taps)

- `klayout/bias_tree_sw.gds`: only the TDN label moved to x = 0.83 (second device of the 1 × 2 array).
- `klayout/d2s_pd_n.gds`, `s2d_pd_n.gds`, `d2s_pd_p.gds`, `s2d_pd_p.gds`: rebuilt like his bias_tree_sw. 1 × 2
  array of the 1/0.45 device at 0.83 µm pitch, shared middle diffusion (vss, vcm, vdd, vcm), no tap, common gate
  as one poly pad and one M1 bar over both contacts. s2d: the vcm M2 trunk, Via1 and M2 pin are gone; vcm is an M1
  pin on the middle stripe. All S/D pins on M1, stripe width × 0.5 µm. 2.5 × 2.3 µm (n), 3.2 × 2.4 µm (p).
  d2s_pd_n / s2d_pd_n and d2s_pd_p / s2d_pd_p now differ only in labels.
- DRC (IHP deck): only LU.b (NMOS) / LU.a (PMOS), the missing taps, as intended. LVS: all five match (bulk as
  its own net; reference netlist in the container, not saved here).

## 17:43: gate contacts closer to the devices (Christoph; "A metal2 via should fit without DRC violations.")

- All five switch cells (bias_tree_sw after his removal of the ni M1 square): gate contact 0.18 µm above Activ
  instead of 0.52 µm (y 1.18–1.34 instead of 1.52–1.68). Limits: Cnt.e 0.14 (contact on poly to Activ) and,
  binding, M1.b 0.18 from the gate M1 to the S/D stripes ending at y = 1.0. Poly cap to 1.41 (Cnt.d 0.07).
  pd cells: one poly cap and one M1 bar (0.42–1.54 × 1.18–1.39) over both gates; bias_tree_sw: separate caps and
  0.53 × 0.21 µm M1 pads (M1.d area). Gate pins 0.29 × 0.21 µm on the contacts. Cells now end at the PCell
  outline (y 1.52 n, 1.62 p) instead of 1.78.
- Via1 fit: test copies with Via1 on each gate contact and a minimum M2 pad (0.29 × 0.5 µm) pass DRC; the
  delivered cells have no via.
- DRC: only LU.a / LU.b (no taps). LVS: all five match.

## 18:12: switch cells back into the library (Christoph: "Good job! Now reimport to pad_buffer_cells.gds")

- `klayout/pad_buffer_cells.gds`: `d2s_pd_n`, `s2d_pd_n`, `d2s_pd_p`, `s2d_pd_p`, `bias_tree_sw` replaced by the
  compact versions (1 × 2 arrays of the library's own `nmosHV$5` / `pmosHV$7`, geometry checked identical),
  identical to the separate GDS files. `ptap1$8` and `ntap1$9`, now unused, removed. All other cells unchanged
  (own shapes and instances); placements in the top cell and the fit cells kept, not repacked. DRC in the
  library: only LU.a / LU.b. sha256 `7100f3de…`, the same on both sides.
- `klayout/cell_tree.md`: the five lines updated.
- Not updated: `pad_buffer_cells.cdl` (still has the tap bulks for these cells) and `pad_buffer_cells.py`.

## 18:21: .cdl updated; bg_res repitched (Christoph: "update the .cdl for now ... push bg_res.gds horizontally to
## minimum distance of the poly resistors. Surrounding layers may overlap if consistent with DRC and LvS." /
## "I mean the exported .gds, not the one in your collection (quite yet).")

- `klayout/pad_buffer_cells.cdl`: the five switch subcircuits rewritten by hand for the tap-less cells (bulk on an
  internal net sub / nw; s2d_pd_n / s2d_pd_p lose the vss / vdd pin). LVS of the five against the library GDS:
  all match. sha256 `94346504…`.
- `klayout/bg_res.gds` (his export): resistor pitch 1.4 → 0.68 µm (rhigh 0.5 + Gat.b 0.18; M1 heads would allow
  0.64, contacts 0.54). pSD / nSD / SalBlock / EXTBlock now overlap and merge; PolyRes stays per segment. Labels
  moved with their resistors. 56.9 → 28.1 µm wide. DRC (main + maximal, incl. Rhi / Sal / EXTB): clean.
  LVS extraction: 41 × rhigh 0.5 / 9.94 µm, as before; the unwired nets match only with ambiguity warnings,
  so the verdict is FAIL, before and after alike. sha256 `0766d12e…`. Not yet in `pad_buffer_cells.gds`.

## 18:32: d2s_rhigh / s2d_rhigh compacted (Christoph: "compactify the exported d2s_high and s2d_high the same way")

- His exports were identical to the library cells. Regenerated with a container copy of `pad_buffer_cells.py`
  with RPITCH 1.4 → 0.68 µm (the file on the computer is unchanged), cells copied out into
  `klayout/d2s_rhigh.gds` (27.7 → 14.7 µm wide) and `klayout/s2d_rhigh.gds` (38.9 → 20.1 µm). Same structure:
  4 segments per unit, nested M2 jumpers, M1 between neighbours, dummies shorted to the ptap strip below.
- DRC (main + maximal): clean. LVS against `pad_buffer_cells.cdl`: both match. sha256 `1b0da5da…`, `77b837e3…`.
  Not yet in `pad_buffer_cells.gds`.

## 20:56: d2s_rhigh side tie (Christoph moved the ptap to the left; "Adjust its height. How close can it be moved to
## the resistor array? Adjust the metal1 vss wiring (and pin) accordingly." / "Eventually, I want a tie left and
## right, but figure out the existing one first.")

- `klayout/d2s_rhigh.gds`: ptap1 0.78 × 13.81 µm (Activ y −0.58 … 13.23, pSD aligned with the rhigh implants
  −0.61 … 13.26), Activ right edge at x = −0.54. Binding rule EXTB.c (pSD ≥ 0.31 from the rhigh EXTBlock at
  −0.2); next pSD.b (0.33 to the rhigh pSD); Sal.d 0.34. A probe 5 nm closer fails EXTB.c.
- vss: the left dummy's head straps run straight into the tie M1; the strap down to the old tie and the old pin
  are gone; vss pin 0.5 × 0.4 µm at the bottom of the tie M1. The right dummy keeps its head-to-head strap and
  floats until the right tie comes. Cell bottom −4.89 → −3.48 µm (old tie region freed).
- DRC clean. LVS: matches with the right dummy floating; against `pad_buffer_cells.cdl` (dummy on vss) the only
  difference is that dummy. sha256 `1aa3e280…`.

## 21:05: d2s_rhigh right tie (Christoph: "reproduce the substrate tap on the right side of the resistor array";
## he has git-staged the work so far)

- `klayout/d2s_rhigh.gds`: the left tie mirrored about the array centre (x = 6.03): Activ 12.60 … 13.38, i.e.
  0.54 µm from the right dummy's poly, same height; right dummy head straps mirrored into its M1, its vertical
  strap removed; second vss pin and label, mirrored. Cell 14.76 × 18.56 µm.
- DRC clean. LVS against `pad_buffer_cells.cdl` (both dummies on vss): match; the two ties are one vss net
  through the substrate. sha256 `0c7ddf10…`.

## 21:11: d2s_rhigh closed tap ring (Christoph: "extend the taps left and right to a closed substrate tap ring
## around the resistor array. Is there a reason not to put the top and bottom substrate taps farther away than
## minimum DRC rules?" / 21:12 question on W520 package temperature, answered in the chat)

- `klayout/d2s_rhigh.gds`: ring of four ptap1 (sides 0.78 × 16.11 µm, top / bottom 13.14 × 0.78 µm, Activ
  butting at the corners, M1 bridged at the four joints). Top / bottom strips at the same rule distance as the
  sides: pSD 0.31 from the array's EXTBlock (Activ y 13.60 … 14.38 and −1.73 … −0.95). They lie under the M2
  jumper tracks; cell outline unchanged (14.76 × 18.56 µm). vss pins unchanged on the side strips.
- DRC clean. LVS against `pad_buffer_cells.cdl`: match. sha256 `6d624b31…`.

## 21:22–21:28: d2s_rhigh interconnect (Christoph asked pros / cons of M2 for the three neighbour links, of the
## dummy-to-ring straps, of M2 paths instead of boxes; decided: "Keep the metal1 dummy straps, metal2 for adjacent
## resistors for symmetry, make paths for the M2 jumpers.")

- `klayout/d2s_rhigh.gds`: the three M1 links between neighbouring heads (C2 at both top junctions, A at the
  bottom) replaced by a Via1 on each head and a straight M2 path; now every junction is via – M2 – via (32 Via1,
  one per head). All M2 as paths, width 0.29 µm, square ends (0.145 µm extension = Via1 enclosure 0.05): 12
  jumpers (U-shaped, 4 points; the 3 neighbour links straight) and 8 end drops; M2 pins stay boxes. Merged M2
  identical to before plus the 3 new links. Dummy M1 straps unchanged.
- DRC clean. LVS against `pad_buffer_cells.cdl`: match. sha256 `2f32bfdb…`.

## 21:35: d2s_rhigh pins (Christoph shortened the M2 end drops; "Any reason against moving the metal2 pins so close
## to the resistor array, or does the guard ring enforce sufficient distance, anyhow?")

- His `klayout/d2s_rhigh.gds` (staged 21:33): end drops end at y −2.28, the level of the lowest bottom jumper
  track; M2 pins 0.29 × 0.4 µm at −2.425 … −2.025, the cell's bottom edge. Cell 14.76 × 17.50 µm.
  DRC clean, LVS against `pad_buffer_cells.cdl`: match (checked here, file unchanged). Answer in the chat: no
  rule links M2 to the ring or the resistors; M2 spacing to the lowest track 0.39 µm; no metal over bodies.

## 21:48: s2d_rhigh like d2s_rhigh (Christoph: "apply the changes mutatis mutandis to s2d_rhigh.gds"; question on
## guarding bg_res, answered in the chat)

- The d2s_rhigh edits written as one procedure (container only) and checked first: applied to the generator's
  0.68 µm d2s_rhigh it reproduces Christoph's current `d2s_rhigh.gds` exactly (geometry and labels).
- `klayout/s2d_rhigh.gds` (n = 6): ptap ring at the rule distance (Activ x −1.32 … −0.54 and 18.04 … 18.82,
  y −1.73 … −0.95 and 13.60 … 14.38), dummy M1 straps into the ring, vss pins on both side strips, the M1
  neighbour links replaced by Via1 + M2 (48 Via1, one per head), all M2 as paths (30), end drops to the lowest
  bottom track (y −3.48), M2 pins there. 20.2 × 19.9 µm (was 20.1 × 22.4).
- DRC clean. LVS against `pad_buffer_cells.cdl`: match. sha256 `c90abfb2…`.

## 21:56: rhigh blocks into the library; NWell under rhigh looked up (Christoph: "Look up the possibility of nwell
## under the array please. Also, reimport the d2s_rhigh.gds and s2d_rhigh.gds into pad_buffer_cells.gds.")

- `klayout/pad_buffer_cells.gds`: `d2s_rhigh` (his file, 45d3c6c6) and `s2d_rhigh` (c90abfb2) replaced; library
  `rhigh` reused (identical), the ring strips added as new ptap1 variants; old ties `ptap1`, `ptap1$1` removed
  (unused). All other cells unchanged (own shapes and instances). DRC of both cells clean, LVS both match.
  sha256 `737220b2…`.
- NWell under rhigh (container test on bg_res, not delivered): IHP's LVS deck connects the rhigh bulk marker to
  pwell, iso_pwell and nwell_drw (`res_connections.lvs`); no DRC rule forbids it. bg_res with one NWell under
  array + ntap1 ring at the ptap positions: DRC clean (main + maximal); LVS extracts all 41 rhigh with bulk on the
  NWell net, match. Model `rhigh` (`resistors_mod.lib`): r3_cmc, bulk node bn carries only the parasitic area /
  perimeter capacitance (dfinf 1e-4: no voltage dependence). Rule manual not in this PDK checkout; the online
  docs have only the general sections. Characterization over NWell not documented.

## 22:11: bg_res tap ring (Christoph: substrate guard ring appropriate; the bandgap resistors go onto core7, not the
## pads; "follow precedent from the other hi res poly arrays and put an nwell tap ring around bg_res.gds";
## connections to be thought about, drawn only after he has git-staged the ring)

- Read as the precedent: p-tap (substrate) ring as in d2s_rhigh / s2d_rhigh ("substrate guard ring"); said so in
  the chat, n-well variant on request.
- `klayout/bg_res.gds`: ring of four ptap1 at the rule distance (Activ x −1.32 … −0.54 and 28.24 … 29.02, y −1.73
  … −0.95 and 10.89 … 11.67), M1 bridged at the joints, both dummies' heads strapped into the side strips in M1,
  vss pins on both side strips. 30.4 × 13.5 µm. DRC clean; LVS (39 unwired segments, dummies on vss): match.
  sha256 `d4967381…`. Not yet in `pad_buffer_cells.gds`.

## 22:23–22:33: bg_res series wiring (Christoph: "vertical M2 paths and horizontal M1 paths"; interconnect inside
## the guard ring; "just the reserved room for now" for stretching R0; bg_res as a candidate for bottom-up
## parasitic extraction; "Don't let chatlog run into a compaction.")

- Git (read-only, optional locks off, via the main repository's worktree entry): `bg_res.gds` staged, index =
  working file; no lock files before or after. Chatlog exported at 22:33 before drawing.
- `klayout/bg_res.gds`: chains left to right, first arc on top. M2 vertical path from every head (Via1),
  M1 horizontal path per resistor and side (Via1), width 0.29 µm, square ends; tracks below the bottom heads at
  y −0.735 (R0), −1.205 (R1A), −1.675 (R1B), above the top heads at 11.275 / 11.745 / 12.215 after 0.6 µm
  reserved for a stretched R0 segment. Ring top / bottom strips moved out to keep the tracks inside (Activ
  −2.87 … −2.09 and 12.63 … 13.41). Terminals in M2 over the ring strips: e2 (R0 at 1), vss (R1A at 2 + R1B at 4,
  one Via1 to the ring = the only join), eb (R1B at 36 + R0 at 39), ea (R1A at 38, top). 30.4 × 16.3 µm.
- DRC clean. LVS: match; extracted R0 eb–e2 178.92 µm, R1A ea–vss 109.34 µm, R1B eb–vss 99.4 µm, dummies on vss.
  sha256 `0a7cd280…`. Not yet in `pad_buffer_cells.gds`; `.cdl` has no bg_res subcircuit yet.

## 22:42: bg_res nitpicks + .cdl (Christoph: ring M1 not flush, "Nudge the vertical guards out a little"; reserve
## symmetric top and bottom; "Also update pad_buffer_cells.cdl.")

- Cause of the M1 step: the ptap1 PCell's M1 end inset along a long strip depends on the strip length (contact
  array): 0.02 µm at 16.28 µm, 0.15 µm at 16.88 µm, while across a short strip it is always 0.09 µm. Moving the
  side strips can't make Activ and M1 flush together, so the M1 step at the top and bottom edges is filled
  (0.06 µm high, full ring width): the M1 ring is now one rectangular frame (outer −1.18 … 28.88 × −3.38 …
  13.32, hole −0.68 … 28.38 × −2.78 … 12.72), Activ frame unchanged.
- Reserve now 0.6 µm below the bottom heads too; bottom tracks at −1.335 / −1.805 / −2.275, ring bottom strip
  Activ −3.47 … −2.69. Cell 30.4 × 16.9 µm.
- `klayout/pad_buffer_cells.cdl`: subcircuit `bg_res` (e2 ea eb vss) added by hand, segment chains as drawn,
  header line added. `bg_res.gds` against it: DRC clean, LVS match. sha256 bg_res `c9d02408…`, .cdl `b09bda73…`.
  The library's `bg_res` is still the old unwired cell until reimported.

## 22:51: bg_res into the library (Christoph: "Yes, reimport bg_res into pad_buffer_cells.gds."; question on PEX
## options, IIC-OSIC-TOOLS 2026.09 vs 2026.10, answered in the chat)

- `klayout/pad_buffer_cells.gds`: `bg_res` replaced by the wired, ring-guarded cell (c9d02408), on the library's
  `rhigh$1`; ring strips as ptap1 variants. The library still had the 1.4 µm-pitch, unwired bg_res (56.9 ×
  11.2 µm), now 30.4 × 16.9 µm. All other cells unchanged. DRC clean, LVS against `pad_buffer_cells.cdl` match.
  sha256 `099b188f…`. Fit cells not repacked: in `fit_bias_tree_oa_bg` bg_res now overlaps bg_nab and
  bias_tree_p (bounding boxes); the top-cell placement has no overlap.

## 23:45–23:59: sinks_6x6 (Christoph exported `sinks_6x6_row.gds` = row r2 with the transistor array turned m45, pitch
## 8 µm; "push the nmos transistors as close together as design rules allow for separate drains"; "Can I get away
## with connecting the gates with poly only?")

- DRC probes of the turned 6/6 array alone (container): gap 0.21 fails Gat.b1 (0.25 between 3.3 V gates over
  Activ); 0.25 and 0.30 pass; 0.40 fails Gat.b (endcaps 0.18 + 0.18 leave a 0.04 poly gap); 0.54 passes again
  (separate gates). Window 0.36 < gap < 0.54 forbidden.
- `klayout/sinks_6x6_row.gds`: array pitch 8 → 6.25 µm (gap 0.25, the minimum; endcaps overlap, so the 8 gates
  form one poly strip); device labels moved with the devices. Everything else untouched: the old row's M1 / M2 /
  poly bar / pins (DRC M1.d and Pin.e, the same as in the export) and the 57.6 µm ptap strip. sha256 `a467d63f…`.

## 00:04–00:06: sinks_6x6_row tap, sources, vss pin, gate contacts, TGO (Christoph: "adjust the width of the
## substrate tap to the width of the transistor array and connect the bottom diffusion contacts (sources) to it. put
## the vss pin onto the metal1 net"; "add gate contacts left and right of the transistor array. minimum drc
## distance?"; "do i still need the thick gate ox rectangle?")

- `klayout/sinks_6x6_row.gds`: ptap1 49.75 × 0.78 µm (= array width), same y; one M1 rectangle from the tap M1 to
  the top of the bottom S/D stripes (y 0.23) over the full array width ties all 8 sources to it; vss pin = the
  tap M1 rectangle, label in its centre (old pin off). Gate contacts at both ends of the gate strip, 0.14 µm from
  the array Activ (Cnt.e; a probe at 0.135 fails Cnt.e), poly tab with 0.07 enclosure, M1 pad 0.29 × 0.32 µm
  (Via1-ready, M1.d) at the gate centre y = 3.34. The old row's TGO rectangle removed: it lay over nothing
  (y 21.2 … 28.2); the PCells' own TGO merge into one region at 6.25 µm pitch.
- DRC: only M1.d, all six from the old row's 0.29 × 0.29 via pads (y 12–13). sha256 `20c0f9cf…`.

## 00:12–00:14: sinks_6x6_row wiring (Christoph: gate contacts over the entire transistor length; drain M1 out over
## the full width, M2 lines to connect the drains; labels at the Activ centres; "connect the poly contacts with metal1
## over the gate area or ... above the array with metal2?"; "Would it be advantageous to make the drain contacts
## narrower than the full transistor width?" — both answered in the chat)

- `klayout/sinks_6x6_row.gds`: gate contact columns at both ends, 17 contacts each over the gate length (0.54 …
  6.30), 0.14 µm from the array Activ, poly tab over the full gate length, M1 column 0.26 × 5.86 µm (Via1-ready),
  vbn pin = each column. Drain M1 plates over the full 6 µm width of every transistor, y 6.45 … 7.90; three M2
  path tracks over the whole array: x (y 6.70), y (7.20), vss (7.70), one Via1 per plate at its centre onto its
  own net; the vss track serves the dummy drains and drops at both ends outside the gate columns to the tap
  (Via1). x / y M2 pins at the left end. Labels at the Activ centres. The old row's wiring above the array (no
  longer connected) removed. Cell 51.6 × 9.6 µm.
- DRC clean. LVS against a row reference (dummies S = D = vss, SX on x, SY on y, all gates vbn): match.
  sha256 `23b666f7…`.

## 00:23: sinks_6x6_row guard ring, BN variant (Christoph renamed the cell to sinks_6x6_row; "not so happy with
## vertical metal2. extend the substrate tap to a full guard ring. That takes care of vss to the dummies. two
## horizontal metal1 lines remain. prepare for a variant corresponding to _r1 where one of the dummies is the diode
## connected transistor")

- Read "two horizontal metal1 lines" as the x / y lines; they stay M2, because an M1 line over the drain plates
  would short them.
- `klayout/sinks_6x6_row.gds` (rebuilt around his transistor array, otherwise only the rename): ptap guard ring,
  sides 0.27 µm outside the array's ThickGateOx (TGO.b; Activ x −1.57 … −0.79 and 50.54 … 51.32), top strip
  0.22 µm above the drain plates (M1.e; Activ y 7.53 … 8.31), bottom strip where the tap was (−1.635 … −0.855),
  M1 bridged and flush. Sources: one M1 plate to the bottom strip. Dummy drain plates run into the top strip;
  the vss M2 track and its drops are gone. x / y M2 tracks at 6.70 / 7.20 µm over the whole array, plates up to
  7.40. vss pin = bottom strip M1; vbn = gate columns; x / y M2 pins at the left end. 52.9 × 10.0 µm.
- `klayout/sinks_6x6_row_bn.gds` (new, cell sinks_6x6_row_bn): the _r1 map dummy X Y Y X X Y BN; BN's drain plate
  joined in M1 to the right gate column (diode), not to the ring.
- DRC both clean; LVS both match their row references. sha256 `11edee22…`, `e83176e2…`.

## 00:27–00:42: sinks_6x6 from two rows (Christoph: another row upside down with shared M2; drain contacts not full
## width; M2 and the guard ring one level up in sinks_6x6, drain wiring maybe a layout-only cell; update
## sinks_6x6_row; d2s_casc_n in parallel, the 6x6 first)

- `klayout/sinks_6x6.gds`: cell sinks_6x6 = sinks_6x6_row (R0) + sinks_6x6_row_bn (R180, so it reads the old
  r1 map dummy X Y Y X X Y BN left to right, under the r2 row: every column has one X and one Y as before) +
  sinks_6x6_wiring (layout only). The rows' drains face each other, 0.21 µm apart (Act.b).
- Drain contacts: device cell `nmosHV_ds` = the 6/6 transistor with the drain contact row cut at one end (15 of
  17 contacts, stripe 5.285 µm of 6). With the upper row turned R180 the short end alternates, leaving 0.43 µm
  for the other row's tab.
- sinks_6x6_wiring: x track (M2 path) over the lower drain stripes (y 6.53), y track over the upper ones (7.04),
  columns 1–6; direct Via1 on the own row's stripe (M1 pad), otherwise a 0.29 µm M1 tab at the column edge to the
  other track (columns 1, 4, 5); dummy drains in M1 at stripe level out to the ring sides; poly links joining the
  two rows' gates at both ends (outside the Activ, 0.18 µm Gat.d); ptap ring around both rows over the source
  plates (sides 0.27 µm outside the TGO), flush M1. Top-level pins: x, y (M2), vss (ring), vbn (gate column).
- `klayout/sinks_6x6_row.gds`, `sinks_6x6_row_bn.gds`: rows without ring and M2: transistors (nmosHV_ds), source
  plate down to the ring strip position (vss label), gate columns (vbn); row_bn = r2 map with BN at position 0,
  BN drain to the left gate column.
- DRC: sinks_6x6 clean; the rows alone only LU.b (no tap). LVS sinks_6x6 against the library's sinks_6x6
  subcircuit: match (SX 36/6, SY 36/6, dummies, BN diode). 52.9 × 16.9 µm (was 60.4 × 16.4 incl. wiring outside).
  sha256 sinks_6x6 `2f5e6751…`, row `5beeb01a…`, row_bn `e1261184…`.
- d2s_casc_n handed to a parallel worker (rotated m45 arrays, 4+1), results to follow.

## 00:47–00:49: sinks_6x6 vbn track; one row cell (Christoph: "how do you propose to contact the shared vbn? Maybe a
## horizontal metal2 wire across the horizontal center line"; "why are two versions _row and _row_bn necessary? Try
## to use one version only and move the difference to the wiring or to the parent cell.")

- Three M2 tracks between the rows at 0.5 µm pitch: x 6.53 (over the lower drain stripes), vbn 7.03 (centre line),
  y 7.53 (over the upper stripes); the upper row moved up 0.49 µm. All three run over the full block width
  (−1.6 … 51.35), pins x / vbn / y at the left block edge. vbn: at both ends the poly link is widened to 0.30 µm
  for a contact, M1 pad 0.30 × 0.32 µm (M1.d), Via1 to the track. One TGO rectangle bridges the 0.16 µm gap the
  move left between the two rows' ThickGateOx (TGO.e 0.86).
- One row cell: both instances are `sinks_6x6_row` (R0 and R180). The BN diode link (BN drain stripe to the upper
  right gate column) and the end-device labels (3 × dummy, BN) are in `sinks_6x6_wiring`; the row keeps the labels
  of its six matched transistors. `sinks_6x6_row_bn.gds` is obsolete (not deleted).
- sinks_6x6: DRC clean, LVS match (library subcircuit); 52.9 × 17.4 µm. Row alone: LU.b only.
  sha256 sinks_6x6 `6e696017…`, sinks_6x6_row `db806381…`.

## 00:57: sinks_6x6 gate connection (Christoph: "isn't the gate contact through narrow poly VERY flimsy?")

- Agreed: 0.19 µm poly links and one contact per end. Now: the two rows' gate contact columns (17 contacts each)
  are joined in M1 through the band between the rows (jogged to x −0.55 … −0.18 so it stays 0.18 µm clear of
  the drain stripes), two Via1 per end onto the vbn track. Poly links and the single contacts removed.
- To free the band at the row ends, the dummy drains no longer run out to the ring sides: each dummy's drain is
  tied to its own source by a 0.29 µm M1 strap over the dummy's channel (lower row both ends, upper row its left
  end; the upper right end is BN).
- DRC clean, LVS match. sha256 `7a423929…`.

## 01:03–01:14: sinks_6x6 back to the original transistor cell (Christoph: "Don't mess with the drain contacts of the
## transistors. DON'T BREAK UP THE TRANSISTOR ARRAY!!! Rather, leave some room to the left and right between the
## transistor arrays and the guard ring."; "PURGE nmosHV_ds.")

- Undone: nmosHV_ds (shortened drain contacts) and the dummy straps over the channels. nmosHV is the unmodified
  PCell copy (XOR 0 against the exported sinks_6x6_row), one m45 AREF, 8 × 6.25 µm, per row.
- Room at both row ends, between array and ring, 1.0 µm: 0.18 gap, 0.29 µm M1 channel (dummy drain to the ring
  strip), 0.18, gate contact column (0.26 µm M1, 17 contacts on a poly tab), 0.07 to the ring. Ring sides moved
  out by 0.21 µm.
- Drains: full-width stripes unchanged. One 0.29 µm M1 tab per transistor, lower row at the column's left edge going
  up, upper row at its right edge going down, Via1 onto the x / vbn / y M2 tracks at y = 6.90 / 7.40 / 7.90 between
  the rows. Upper row from y = 8.115 (was 7.38); block 53.4 × 18.1 µm.
- vbn: gate columns of both rows joined in M1 at each end, one Via1 each onto the vbn track; BN drain (upper row,
  right end) to its column in M1.
- sinks_6x6_row_bn.gds deleted; no file contains nmosHV_ds any more. Old build scripts removed (container).
- sinks_6x6: DRC clean, LVS match. sinks_6x6_row alone: LU.b only (the ring is in the parent). sha256 `8e2caf7f…`
  (block), `e0e4d2c0…` (row).

## 01:20–01:30: sinks_6x6 reimported into pad_buffer_cells.gds (Christoph: "your solution is good and needs only
## minimally more space. Keep it! Good to reimport to pad_buffer_cells.gds. Update the .cdl if necessary.")

- sinks_6x6 now holds sinks_6x6_row (twice) and sinks_6x6_wiring; nmosHV reuses the library's identical cell, the
  two ring ptap1 variants are new (ptap1$17, ptap1$18). sinks_6x6_r1, sinks_6x6_r2 and their tap ptap1$2 are
  gone. No other cell changed; instance positions unchanged.
- The block is now 53.4 × 18.1 µm (was 60.4 × 16.4) with its origin at the lower row's Activ, so in the parents it
  sits about 8 µm higher. Top cell: no overlap. Fit cells (not repacked): overlaps casc_n / casc_p / tails.
- pad_buffer_cells.cdl unchanged: its sinks_6x6 subcircuit is the one LVS matched.
- sinks_6x6 in the library: DRC clean, LVS match. sha256 `434de2e1…`.

## 01:22–01:29: d2s_casc_n rotated, by a background worker (Christoph, 00:38: "start in parallel with d2s_casc_n.gds:
## transistors rotated by 90 deg (and mirrored? as in sinks_6x6_row)"; "use transistor arrays where you can.")

- First worker (00:42) was cancelled by an interrupt after reading its inputs; restarted 01:22.
- The four 15/3 cascodes are one 2 × 2 AREF of the exported nmosHV$1, m45 like the sinks; pitch 15.25 (x) × 4.42 (y).
  Lower row CX CX (bottom stripes x, top l1), upper row CY CY (bottom b, top y). BNC (nmosHV$2, same rotation) stands
  right of the array: drain to the gate column (diode), source to the ring. Both device cells XOR 0 vs the export.
- Gate: M1 contact columns on poly tabs, left (21 contacts, vbnc pin) and right (23, also BNC's gate). No thin poly.
- M2 path tracks (0.29) over the full width: x at y = −0.40, l1 / b at 3.80 / 4.30, y at 8.50; one M1 tab + Via1 per
  stripe. Pins x / l1 / b / y on M2 at the left edge, vbnc and vss on M1. No dummies (no matching needed).
- ptap1 ring, flush M1 frame; block 35.3 × 11.5 µm (was 26.3 × 17.6 without a ring).
- DRC clean, LVS match. sha256 `5cb3fe59…`. Not reimported into pad_buffer_cells.gds.

## 01:29–01:36: d2s_tails, s2d_tails like sinks_6x6, by a background worker (Christoph: "apply the transformations for
## sinks_6x6, mutatis mutandis, to d2s_tails and s2d_tails.")

- pmosHV$1 (5/6) unmodified (XOR 0 vs the exports), m45, one AREF per row at 5.25 µm pitch (Gat.b1; poly endcaps
  merge). One row cell per block, R0 lower (.cdl _r2 map, dummies at both ends), R180 upper (_r1 map, dummy + BP).
- Sources: M1 plate to the ring strip. Drains: one 0.29 µm M1 tab + Via1 each onto its own full-width M2 path track
  in the band, 0.5 µm pitch from y = 6.90; each row's nets on its own side of the vbp centre track.
  d2s: sb_B sa_C1 sa_C2 sb_A | vbp | sa_B sb_C1 sb_C2 sa_A. s2d: sb_A2 sa_F1 sa_F2 sb_A1 sb_M1 sa_M2 | vbp |
  sb_M2 sa_M1 sa_A2 sb_F1 sb_F2 sa_A1.
- Row ends as in sinks_6x6 (dummy-drain lane, gate columns joined, Via1 to vbp, BP drain to its column). ntap1 ring
  (vdd), flush M1 frame, one NWell and one ThickGateOx over everything. Pins on M2 left edge, vdd on M1.
- d2s_tails 35.3 × 21.8 µm (was 45.0 × 14.0), s2d_tails 45.8 × 23.8 µm (was 59.6 × 14.0).
- DRC clean, LVS match (.cdl unchanged); row cells alone LU.a only. sha256 d2s_tails `a32204a2…`, d2s_tails_row
  `1a40db34…`, s2d_tails `10256f95…`, s2d_tails_row `3630bea7…`. Not reimported.
- Open: neighbouring output tracks couple slightly over the full width (shorter tracks would trade off symmetry).

## 01:37: d2s_casc_n common centroid requested (Christoph: "please common centroid: CX CY / CY CX. This will require a
## little more area and maybe vertical metal1 lines within the guard ring to the left of the 4 big transistors.")

- Given to the background worker: l1 / b stay shared in the band; x / y tracks below and above, joined by two vertical
  M1 lines inside the ring, left of the array.
- Done 01:41: lower row CX CY, upper row CY CX, still one 2 × 2 AREF of the unmodified nmosHV$1; row pitch 4.42 → 4.74.
  Tracks bottom to top: y, x | lower row | l1, b | upper row | y, x. Source tracks in the same order below and above
  (not mirrored), so x and y each get one short and one long tab. Lower-row tabs 0.5 µm left of the device centre,
  upper-row tabs 0.5 µm right. x / y joined by two vertical 0.29 µm M1 lines left of the gate column (left ring side
  out by 0.81). Block 36.1 × 11.9 µm. x / y pins only on the lower tracks.
- DRC clean, LVS match. sha256 `6c82a781…`. Not reimported.

## 01:48–01:58: d2s_casc_n, d2s_tails, s2d_tails reimported; library re-placed (Christoph: "reintegrate to
## pad_buffer_cells.gds, and rearrange the cells in pad_buffer_cells.gds so that they don't overlap after their
## layout changes.")

- Reimported the versions on disk (d2s_casc_n `6c82a781…`, d2s_tails `a32204a2…`, s2d_tails `10256f95…`). Device
  cells reuse the library's identical nmosHV$1 / $2 and pmosHV$1; the rings' tap variants are new (ptap1$19/$20,
  ntap1$16 … $19). Old row cells _r1 / _r2 of the tails and their taps are gone. No other primitive changed.
- Top cell and fit cells re-placed with the generator's own rules (columns with 8 µm gaps, first-fit-decreasing shelf
  packing in 80 µm, 2 µm gaps); the code reproduces the original generator output exactly. No overlaps left.
- Fit heights in 80 µm (zone 94 µm), at generation → now: d2s front 94.2 → 79.4, d2s front + caps 98.8 → 94.9,
  s2d front 136.5 → 123.7 (also with cload), bias / oa / bg 131.1 → 132.8.
- The three cells in the library: DRC clean, LVS match; pad_buffer_cells.cdl unchanged. sha256 `82309bf8…`.

## 01:53–02:00: d2s_casc_p like d2s_casc_n, by the background worker (Christoph: "apply the transformations, mutatis
## mutandis, of d2s_casc_n to d2s_casc_p.")

- One 2 × 2 AREF of the unmodified pmosHV$3, pitch 15.25 × 4.74, common centroid PCL PCR / PCR PCL. BPC (pmosHV$4)
  right of the array as the diode, source to the right ring side.
- Tracks bottom to top: pr, pl | lower row | l2, a | upper row | pr, pl; pl / pr joined by two vertical M1 lines left
  of the gate column. Gate columns 22 contacts each. Pins a / l2 / pl / pr on M2 left edge, vbpc and vdd on M1.
- ntap1 ring (vdd), flush M1 frame; one NWell (0.24 beyond the ring), one ThickGateOx, one pSD. 36.6 × 12.4 µm
  (was 23.0 × 18.0).
- DRC clean, LVS match. sha256 `5b05fffb…`. Not reimported.
- Next for the worker (Christoph, 01:55): s2d_casc_p, then s2d_casc_n, same kind of transformations.

## 02:00–02:05: s2d_casc_p like d2s_casc_p, by the background worker

- One 2 × 3 AREF of the unmodified pmosHV$3, pitch 15.25 × 5.24, point-reflected common centroid LPC LNC DC /
  DC LNC LPC. BPC right of the array as the diode. Gate columns 24 contacts each.
- Tracks bottom to top: ln, dd, lp | lower row | voutp, vcmfb, voutn | upper row | ln, dd, lp; vcmfb between the two
  outputs. Sources joined by three vertical M1 lines (equal length) left of the gate column.
- ntap1 ring, one NWell / ThickGateOx / pSD. 52.4 × 13.9 µm (was 31.6 × 18.0). Row pitch set by the 0.205 M1 gap of
  the far tabs to the other row's drain stripe.
- DRC clean, LVS match. sha256 `3a1b1bdf…`. Not reimported.

## 01:58: s2d_sinks_cmfb requested (Christoph: "s2d_sinks_cmfb needs the attention of an agent that handled
## sinks_6x6 and similar cells.")

- Given to the tails worker: as sinks_6x6, xc / vbn / yc tracks, dummies at all four row ends, no diode.
- Done 02:07: unmodified nmosHV, m45, one AREF of 6 per row at 6.25; row cell s2d_sinks_cmfb_row twice (R0 lower =
  _r2 map dummy SYC SXC SXC SYC dummy, R180 upper = _r1 map dummy SXC SYC SYC SXC dummy). Tracks xc / vbn / yc at
  6.90 / 7.40 / 7.90, shared by both rows; dummy lanes at all four ends; gate columns joined, Via1 to vbn. Device
  labels in the wiring cell (the two row maps are not 180° images of each other). 40.9 × 18.1 µm (was 45.9 × 16.4).
- DRC clean, LVS match; row alone LU.b only. sha256 s2d_sinks_cmfb `c98cc576…`, s2d_sinks_cmfb_row `cf7805ed…`.
  Not reimported.

## 02:05–02:12: s2d_casc_n like d2s_casc_n, by the background worker

- One 2 × 4 AREF of the unmodified nmosHV$1, pitch 15.25 × 5.74, point-reflected common centroid with the main pair
  inside: CXC CX CY CYC / CYC CY CX CXC. BNC right of the array as the diode. Gate columns 25 contacts each.
- Tracks bottom to top: y, yc, xc, x | lower row | vdd, vcmfb, voutp, voutn | upper row | y, yc, xc, x; neither
  output next to vdd (vcmfb then neighbours only voutp). Sources joined by four equal vertical M1 lines.
- ptap1 ring, one ThickGateOx. 67.7 × 14.9 µm (was 43.5 × 17.6).
- DRC clean, LVS match. sha256 `9c0c841f…`. Not reimported.

## 02:02–02:10: d2s_casc_p upright PCells, BPC in line, dummy (Christoph: "the pcell transistors are all upside down.
## ... the small transistor to the right sits in the vertical center, so its gate is crossed by metal2. Maybe better
## to move it in line with one row of the large transistors. For symmetry, one could add a dummy transistor to the
## other row.")

- Devices R270 shifted by W in y instead of m45: same polygons on every layer, PCell texts upright.
- BPC on the lower row's centre line (diode, source to the right ring side); dummy pmosHV$4 on the upper row's
  centre line, gate vbpc, D / S to vdd (ring). Row pitch 4.74 → 4.94 (BPC-dummy gap 0.26); 36.6 × 13.6 µm.
- All M2 tracks end flush with the right gate column, so no metal over BPC or dummy.
- DRC clean, LVS match against the .cdl plus "Md2s_casc_p_dummy_5 vdd vbpc vdd vdd sg13_hv_pmos w=1u l=4u"
  (library .cdl to be updated at reimport). sha256 `d17e459d…`.
- Aligning BPC / dummy with the rows' outer edges instead of the centre lines would save about 1 µm of height.

## 02:05–02:14: d2s_loads as one sinks-style row, by the background worker (Christoph: "d2s_loads needs attention of
## the agent that has handled or is handling similar layouts ... single row sinks.")

- Unmodified pmosHV$2 (6/4), R270 (upright texts), one AREF of 10 at 6.25 (Gat.b1). Sources to an M1 plate on the
  ntap1 ring's bottom strip. Drains: one centred 0.29 µm M1 tab each up to full-width M2 tracks pl / l2 / pr at
  4.90 / 5.40 / 5.90; all tabs equally long; l2 between the outputs, gate columns (11 contacts) via1 to it at both ends.
- Dummy-drain lanes at both ends; ntap1 ring, one NWell / ThickGateOx. 66.3 × 9.1 µm (was 53.4 × 9.0).
- DRC clean, LVS match. The worker could not reach the computer (02:13); committed afterwards. sha256 `a5c70237…`.

## 02:20: drain tabs to 3 Via1 (Christoph: "unnecessarily narrow drain connections with only one via from metal1 to
## metal2 ... wide enough drain metal1 connections to allow for 3 vias in a row, where the drains are wide enough.")

- Tabs about 1.11 µm wide (3 × 0.19 Via1 + 2 × 0.22 + 2 × 0.05 enclosure), 3 Via1 onto the track.
- Sinks-style worker: sinks_6x6, d2s_tails, s2d_tails, s2d_sinks_cmfb, d2s_loads. Cascode worker (source tabs too):
  d2s_casc_n, d2s_casc_p, s2d_casc_p, s2d_casc_n.
- Cascodes done 02:26: every drain and source tab 1.11 µm with 3 Via1 at 0.41 pitch; band offsets ∓0.5 → ∓0.75 from
  the device centre (crossing tabs 0.39 apart). Tab ends 0.105 past the track centre (was 0.145) so the wide tabs keep
  0.245 to the other row's stripe (M1.e 0.22 for width > 0.3). Sizes unchanged; XOR only M1 / Via1 inside the tabs.
  DRC clean, LVS match. sha256 d2s_casc_n `63111115…`, d2s_casc_p `50fdc580…`, s2d_casc_p `16fb4e74…`,
  s2d_casc_n `56e4ff96…`.
- Sinks-style blocks done 02:33: d2s_tails, s2d_tails all drains 1.11 µm / 3 Via1. sinks_6x6, s2d_sinks_cmfb half the
  drains and d2s_loads all drains got only 2 Via1 on 0.70 µm tabs (M1.e 0.22 against 0.18 / 0.185 clearances).
  Sizes unchanged, XOR only in the tabs. DRC clean, LVS match. sha256 sinks_6x6 `240efbbd…`, d2s_tails `94944177…`,
  s2d_tails `f85133ba…`, s2d_sinks_cmfb `7fc02aa1…`, d2s_loads `37626712…`.
- Follow-up given (02:34): the cascode worker's shorter tab ends (0.105 past the track centre, V1.c 0.01) gain the
  missing 0.04, so 3 Via1 everywhere in sinks_6x6, s2d_sinks_cmfb, d2s_loads.
- Done 02:43: all drains in sinks_6x6, s2d_sinks_cmfb, d2s_loads now 1.11 µm / 3 Via1. The tab ends already were
  0.01 past the vias, so the margin came from M2: on the former 2-via tabs the via row moves 0.035 / 0.04 into the
  track (M2.c 0.005 on the track's long side) and the tab end with it, leaving exactly M1.e 0.22. Tracks, rows, ring
  unchanged; XOR only M1 / Via1 in the tab zone. DRC clean, LVS match. sha256 sinks_6x6 `96d36a44…`,
  s2d_sinks_cmfb `a88a25fd…`, d2s_loads `e9506e3d…`.

## 02:30–02:40: bg_misc_p transistors turned, first stab by the sinks-style worker (Christoph: "the transistors of
## bg_misc_p need to be turned by ±90 degrees ... at least for a preliminary stab.")

- Unmodified device cells, R270 (upright texts). MS1 chain: one AREF of 8 at 0.75 pitch (Gat.b1), 12.5 µm gates
  vertical, one merged en_3v3_b poly strip with contact columns (36 contacts) at both ends. Series meander in M1:
  vdd at device 0 top, ms1 … ms7 alternately linking bottom / top stripes of neighbours, ks at device 7 top.
- SVPG at the bottom right, own en_3v3 gate contact. ntap1 ring, one NWell / ThickGateOx. All pins on M1.
- 12.0 × 17.1 µm (was 58.2 × 5.5). DRC clean, LVS match. sha256 `52f37173…`. Not reimported.
- Open: SVPG below the chain would give about 9.5 × 19; the right side has about 12 µm unused next to SVPG.

## 02:34: bg_nab rotated? (question only)

- Estimated: full 10 µm dummies → about 65 × 10 µm; dummies W ≈ 2 µm (same L, Activ height and gap, so the outer
  devices see the same near environment at their W ends) → about 49 × 10 µm (now 31.6 × 12.6). Not started.

## 02:35–02:45: bg_nab rotated, 2 µm dummies, by the sinks-style worker (Christoph: "Yes, queue it.")

- One row dummy NA NB NB NA dummy, R270 (upright texts). NA / NB the unmodified nmosHV$10 (10/4) at 10.25 pitch;
  dummies a fresh SG13_dev nmosHV w=2u l=4u (same Activ height and L), all gaps 0.25, one merged g poly strip.
- Tracks: above g (4.90), vpc (5.40); below eb (−0.22), ea (−0.72): alternating order, so NA and NB each get one short
  and one long tab. 1.11 µm tabs with 3 Via1, centred. Gate columns (11 contacts) via1 to the g track. Dummy stripes
  straight in M1 to the ring strips. ptap1 ring, one ThickGateOx.
- 48.9 × 8.2 µm (was 31.6 × 12.6). DRC clean, LVS match against the .cdl with w=2u dummies. New file bg_nab.gds,
  sha256 `a41113ca…`. At reimport: dummy cell needs a unique name; library .cdl dummies → w=2u.

## 02:36: bg_pcas, bg_pmir (question only)

- Rotated rows of 9 × 10/1 would be ~96 µm wide (zone 80). Options given: (1) keep orientation, gate-head contacts,
  M1 gate bus, M2 tracks over the rows, end dummies, ring; (2) rotate and fold into 4 rows (~49 × 18); (3) merge
  bg_pmir + bg_pcas as in-line cascodes sharing the co / ca / vpg stripe (~33 × 30 for both). Waiting for a choice.

## 02:41: bg_pmir_pcas (Christoph: "Go with option 3. create bg_pmir_pcas.")

- Given to the cascode worker: R0 kept; each column = mirror and cascode pmosHV$14 (10/1) placed so they share the
  ca / co / vpg stripe (unmodified PCells, overlapping placement); 2 × 10 columns, dummy stacks at both ends of both
  rows (one more per row than today); gate contacts on the 1 µm gate heads, no poly stubs or bars. ca / co are only
  wires between PA / PAC and PO / POC in bg_core_pd.sch, so they become internal; ports g iout vdd vpc vpg.
  Reference subckt in the container (/opt/eda/bgpp/ref.cdl); the library .cdl gets it at reimport.

## 02:44: bias_tree_n, bias_tree_p rotated (Christoph: "It is probably sufficient to use copies of the narrow transistor
## as dummies, or the narrow transistor on one side and a narrow dummy on the other. Extract them from pad_buffer_cells
## if they aren't already to work on them.")

- Extracted from pad_buffer_cells.gds (`82309bf8…`); no exports existed. Chosen: narrow device at one end, narrow
  dummy at the other: n = NBPC(2.4/6) NBP NI NABP dummy(2.4/6), p = PBNC(2/6) PBN PABN dummy(2/6), replacing the two
  wide dummies each. Given to the sinks-style worker (R270, one row, abutted gates, 3-via tabs, rings); new files
  bias_tree_n.gds, bias_tree_p.gds. Library .cdl to change at reimport.
- Done 02:50: one row each, R270, unmodified cells (dummy = the narrow device's cell), gaps 0.25, one merged gate
  strip, gate columns (17 contacts) via1 to the gate track (n: ni, so NI closes through its drain; p: extra vbp track).
  Drains 1.11 µm / 3 Via1 (narrow devices too), all tabs to the top track (matched devices equal). Tracks bottom to top
  n: ni vbp vabp vbpc; p: vbp vbn vabn vbnc. bias_tree_n 27.4 × 11.1 (was 43.6 × 8.6), bias_tree_p 18.8 × 11.6
  (was 37.0 × 8.0). DRC clean, LVS match. sha256 `d8ca188a…`, `c64471ee…`. Not reimported.
- Done 02:52: 2 × 10 stacks at 3.40 pitch, R0 (r2 R0 too, upright texts), cascode 1.38 right of the mirror so its
  source stripe lands on the mirror's drain stripe (contacts coincide). Gate heads 1 µm wide, 2 contacts, 2 Via1:
  vpg heads at the outer row ends, vpc heads in the band. M2 tracks bottom to top: ca co vpg | r2 | g vpc iout | r1 |
  vpg co ca, outer pairs joined by three vertical M1 lines left of the array. No metal over channels.
- co / ca kept as single nets (as in bg_core_pd.sch), each shared stripe up to its track: costs about 2 µm height vs.
  per-stack internal nodes (a netlist change). Out stripes 1 Via1 each (0.16 stripes between head pads).
- 38.6 × 27.6 µm (bg_pmir + bg_pcas today 1152 µm² without full rings). DRC clean, LVS match (40 devices). New file
  bg_pmir_pcas.gds, sha256 `c462bf92…`. Library .cdl needs the combined subckt at reimport.

## 03:03–03:25: all reworked cells reimported; library re-placed (Christoph: "reimport all the gds files you and your
## agents have worked on back into pad_buffer_cells. as you put them back, rearrange them to avoid overlaps and try
## to improve the fit into the pad area. Make me a table ...")

- Compared every block gds in klayout/ with the library: 13 changed + bg_pmir_pcas new were reimported (sinks_6x6,
  d2s_tails, s2d_tails, d2s_casc_n, d2s_casc_p, s2d_casc_p, s2d_casc_n, s2d_sinks_cmfb, d2s_loads, bg_misc_p, bg_nab,
  bias_tree_n, bias_tree_p); the rest already matched. bg_pmir and bg_pcas removed from the library (replaced by
  bg_pmir_pcas; their gds files in klayout/ are untouched). Identical leaf cells keep their names; only the reworked
  blocks' own row / wiring / ring cells changed.
- pad_buffer_cells.cdl by hand: d2s_casc_p (+ dummy), bg_nab (2/4 dummies), bias_tree_n / _p (narrow dummies),
  bg_pmir + bg_pcas → bg_pmir_pcas (39 subckts).
- Top cell: generator columns (no overlaps by construction). Fit cells: the lower of the generator's shelf packing
  and a skyline bottom-left packing over 4000 orders, no rotation. Heights in 80 µm (zone 94): d2s front 75.6 (shelf
  85.2), d2s front + caps 87.9 (96.6), s2d front 138.6 (also with cload), bias / oa / bg 106.3 (114.6). No overlaps.
- s2d cannot fit as is: its bounding boxes alone need 87.2 µm of height in 80 µm, and seven of its primitives are
  41 … 75 µm wide; with 90° rotation allowed it would be 107.5.
- All 14 reimported cells in the library: DRC clean, LVS match. sha256 gds `da6ac38a…`, cdl `b470a10b…`.

## 03:32–03:36: s2d_loads in two rows; narrow dummies (Christoph: "s2d_loads, rotate, 2 rows, narrower dummies";
## "which cells have unnecessarily wide dummy transistors?"; "yes, go.")

- Candidates for narrow (W = 2 µm, same L) end dummies are the rotated rows only: s2d_sinks_cmfb (4, ≈ 8 µm),
  d2s_loads (2, ≈ 8 µm), sinks_6x6 / d2s_tails / s2d_tails (3 each, but the BN / BP diode at the upper row's end stays
  full width and breaks the shared row cell; ≈ 3 … 4 µm). Unrotated cells keep full-width dummies.
- Given to the sinks-style worker: s2d_loads as two rows "dummy LP LN D D LN LP dummy" (R0 / R180) with 2/4 dummies;
  s2d_sinks_cmfb with 2/6 dummies; d2s_loads with 2/4 dummies.

## 03:38: split diode as end dummies (Christoph: "what about the idea of splitting the diode into narrower transistors
## that second as dummies? that could deteriorate the input to output ratio, but the output currents would still
## match.") — question only

- ngspice, IHP HV models (psp103), op, output Vds = diode Vgs, total diode W kept: 4 × 1.5/6 instead of 1 × 6/6 (NMOS)
  raises Iout/Iref by +7.0 … 8.2 % over 1 … 30 µA; 4 × 1.25/6 instead of 5/6 (PMOS) lowers it by 4.8 … 5.2 %.
  Nearly constant over current and corner, so it sizes out: 4 × 1.605/6 (n) within ±0.3 % over tt/ss/ff/sf/fs,
  +0.6 / −0.3 % at 1 / 30 µA; 4 × 1.185/6 (p) within ±0.11 % over the corners, −0.37 / +0.04 % at 1 / 30 µA.
- Not modelled: edge-position layout effects on the four fingers. The diode centroid moves from one corner to the
  array centre (linear gradients between diode and outputs cancel). Same gate area, same random mismatch.
- Would apply to sinks_6x6 (≈ 9 µm narrower), d2s_tails, s2d_tails (≈ 7.6 µm each); schematic and .cdl diode change.
- Done 03:45 (s2d_loads two rows, narrow dummies), by the sinks-style worker; fresh SG13_dev 2/4 and 2/6 dummies,
  unmodified, R270, 0.25 gap. s2d_loads: one row cell twice (R0 / R180), "dummy LP LN D D LN LP dummy", tracks
  vcmfb, lp, dd, ln, vcmfb (lp and ln each between vcmfb and dd; point-symmetric about dd), 45.8 × 15.8 µm (was
  74.6 × 9.0). s2d_sinks_cmfb 32.9 × 18.1 (was 40.9; now also R270, upright texts). d2s_loads 58.3 × 9.1 (was 66.3).
  DRC clean, LVS match. sha256 s2d_loads `0d01697b…`, s2d_loads_row `96331eef…` (new), s2d_sinks_cmfb `068f9715…`,
  s2d_sinks_cmfb_row `0588e54b…`, d2s_loads `2e3a023d…`. Not reimported.

## 03:55–04:05: s2d_loads, s2d_sinks_cmfb, d2s_loads reimported; library re-placed (Christoph: "ok reimport
## s2d_loads, s2d_sinks_cmfb, d2s_loads to pad_buffer_cells, rearrange cells to avoid overlaps.")

- Versions on disk (`0d01697b…`, `068f9715…`, `2e3a023d…`). The new 2/4 dummy cell (pmosHV$15) is shared by both
  loads; s2d_loads_row / _wiring new; only s2d_sinks_cmfb's own row / wiring changed otherwise.
- .cdl: s2d_loads (two rows, 4 × 2/4 dummies), s2d_sinks_cmfb (2/6 dummies), d2s_loads (2/4 dummies); 39 subckts.
- Re-placed as before, no overlaps. Fit heights (zone 94): d2s front 74.0, d2s front + caps 82.5, s2d front 145.4
  (six s2d primitives wider than 39 µm cannot pair in 80 µm), bias / oa / bg 106.3.
- The three cells in the library: DRC clean, LVS match. sha256 gds `434b8233…`, cdl `598edcc6…`.

## 04:01: oa_pmir (Christoph: "why are oa_pmir_a and oa_pmir_b necessary? anyhow, looks like the transistors should be
## rotated and there's an expert agent that can do it.")

- Not necessary: they are rows 1–2 and 3–4 of one 4 × 8 point-symmetric 2/8 PMOS mirror (PO ×20, P8 ×8, P2 ×2,
  P0 diode, one dummy as P0's partner); the generator's block() only builds two rows.
- Given to the sinks-style worker as one cell oa_pmir: R270, rows 1 / 2 and 3 / 4 as R0 / R180 pairs with shared
  drain bands, 2/8 end dummies at both ends of every row (+8 devices), new file oa_pmir.gds. Library / .cdl at reimport.

## 04:03: oa_pcas (Christoph: "also queue oa_pcas. the transistors should be rotated.")

- Given to the cascode worker (parallel to oa_pmir): one rotated row POC POC P8C POC P0C P2C POC P8C POC (L = 2 for
  all, W 2 / 0.5 / 1), one merged vpc poly strip, source tracks (co, c8, vpg, c2) on one side, drain tracks (iout,
  vnc, vpc, vbr) on the other, no dummies; new file oa_pcas.gds.

## 04:07–04:12: oa_misc_p rotated (Christoph: "oa_misc_p needs rotating. which agent?")

- No agent needed: oa_misc_p is identical to bg_misc_p (same netlist apart from the name, original layouts XOR 0).
  oa_misc_p.gds = the rotated bg_misc_p (`52f37173…`) with the top cell renamed; replaced his export (= library
  cell). DRC clean, LVS match against the oa_misc_p subckt. sha256 `ec81c155…`. Not reimported.
- 04:06 (question only): the inner dummy in oa_pmir is P0's point partner (31 units on 32 positions, no centre cell
  in 4 × 8); keeping it, the alternatives cost more (P0 doubled → ratio 20:2; odd × odd grids; split P0).
- oa_pcas done 04:10 (cascode worker): one rotated row POC POC P8C POC P0C P2C POC P8C POC, R270 (upright texts),
  gaps 0.25, one merged vpc poly strip incl. the 0.5 µm P0C, gate columns to the vpc track. Tracks bottom to top
  vpg, c2, c8, co | row | iout, vnc, vbr, vpc (co / iout innermost). Tabs: 3 Via1 on 2 µm, 2 on P2C and P0C. No dummies.
  ntap1 ring. 21.5 × 8.5 µm (was 30.2 × 5.0 without ring). DRC clean, LVS match. His export (= library cell, XOR 0)
  replaced after the worker stopped at the existing file. sha256 `5a38cb70…`. Not reimported.
- oa_pmir done 04:14 (sinks-style worker): one row cell oa_pmir_row (10 × pmosHV$9 2/8, 2.25 pitch, R270), all four
  rows R0 (upright texts; the wiring chooses the drain stripe: rows 1, 3 drain at the bottom, 2, 4 at the top).
  Bottom to top: ring, row 4, band B, row 3, shared vdd plate, row 2, band A, row 1, ring; point-symmetric. Tracks
  band A co, c8, c2, vpg, band B the 180° image. Drain tabs 0.70 µm / 2 Via1 (two rows' tabs share a 2 µm column).
  Bands joined per net by four vertical M1 jumpers just outside the left ring side. Inner dummy D–S strapped.
  28.0 × 42.8 µm (was 2 × 76.8 × 8.0). DRC clean (incl. LU), LVS match. New file oa_pmir.gds, sha256 `6dd9d4f9…`.

## 08:35–08:45: oa_misc_p split (Christoph: "what is oa_misc_p doing?"; "ok good job with oa_misc_p, but this block
## needs to be broken up.")

- oa_misc_p = PMOS half of oa_core_pd's start-up and power-down: MS1 (0.5/100 as 8 × 0.5/12.5, gate en_3v3_b) trickles
  current into ks, which opens MS3 to pull vpc down and start the core; MS2 (gate vbr) pulls ks down once running.
  SVPG (gate en_3v3) pulls vpg to vdd when disabled (PMOS mirror off, iout high-Z). bg_misc_p is the same block.
- Given to the sinks-style worker: split into <pre>_ms1 (start-up chain, own ntap ring) and <pre>_svpg (switch, own
  small ntap ring) for oa and bg; new files; library / .cdl swap at reimport.
- 08:45 correction (Christoph: "NO. NO ntap rings."): the four split cells get no ring or tap, like the tap-less
  switch cells; bulk on an internal net nw tied by the parent, as in the .cdl for d2s_pd_p; missing-tap DRC accepted.
- 08:45 cancelled (Christoph: "Or for now, leave the blocks as they are. I'll deal with hand layout later, in
  context."): oa_misc_p / bg_misc_p stay as delivered; the worker told to stop and deliver nothing.

## 09:03–09:15: staged cells pulled back into pad_buffer_cells.gds (Christoph deleted the oa_pmir_a / _b exports;
## "pull these back in in their preliminary state": bg_misc_p, d2s_loads, oa_misc_p, oa_pcas, oa_pmir, s2d_loads,
## s2d_loads_row, s2d_sinks_cmfb, s2d_sinks_cmfb_row)

- d2s_loads, s2d_loads, s2d_sinks_cmfb (with rows) were already in the library at these versions. Reimported:
  oa_misc_p and bg_misc_p as on disk (`c4b6d572…`, `0f51faf6…`: his note "NEEDS TO BE BROKEN UP" on 63/0 added,
  geometry unchanged), oa_pcas (`5a38cb70…`), oa_pmir (`6dd9d4f9…`). oa_pmir_a / oa_pmir_b removed from the library.
- .cdl: oa_pmir replaces oa_pmir_a / oa_pmir_b (38 subckts). Re-placed, no overlaps; bias / oa / bg fit 102.3 µm.
- The four cells in the library: DRC clean, LVS match. sha256 gds `fe2c540f…`, cdl `52fb7fad…`.

## 2026-10-28 04:09–05:08 oa_core_pd v2 (compact) into the macro (Christoph, 04:22: "There's a spectacularly compact Oguey-Aebischer layout from Agent 2. Is that already on my file system?"; 04:25: "okay, as long as you don't wait with it until Agent 2 has finished bg_core_pd, which is next in line.")

- Layout: A2 assembled it from A3's / A4's primitives at 04:09.
  - 40.51 × 58.135 µm = 2355 µm², against 3856 µm² for v1 (−39 %).
  - One vdd NWell, no rings, no tie between rows; Metal1 / Metal2 only; ports on the right edge.
  - A2's checks: DRC 0 (Python subset, LU included); LVS match against the composed reference and against the
    backannotated sheet; byte-reproducible build.
  - My check, an independent flat extraction (padswitch/verify.py): every sheet device on its nets; MS1 is
    8 × 0.5/12.5 from vdd to ks; the dummies are PMOS 4.4/8 (gate vpg) and NMOS 36/1 (vnc) + 4/1 (vbr), with
    D = S = bulk; one label per net.
- In the notes (04:27): A2's whole output is in `design_considerations/pad_buffer_layout/oa_core_pd_v2_2026-10-28/`
  (`v2/`, `skill/`, `report.md`).
- In the macro (05:05):
  - `macros/oa_core_pd/layout/gds/oa_core_pd.gds` is v2 (sha 22ad9f95…).
  - `oa_core_pd.sch` is backannotated in the sheet's own style: M10 ng 8 → 18, M11 ng 4 → 9 (W, L unchanged); MS1 as
    the drawn 8-device chain in a new box [S1]; the three dummies in box [D]. A2's own backannotated sheet copy,
    with its label-style box, was not used.
  - Subckt `oa_core_pd` in `bias_ref_pd.spice`: the same devices, in place.
  - README updated.
- Checks of the backannotation:
  - the sheet against the new subckt: equal, 28 devices;
  - all 94 sheets of the repo (outside OgueyAebischerBias), with their own xschemrc, flattened: after swapping in
    the new oa_core_pd subckt, the 93 others are identical to before; only oa_core_pd itself changed;
  - source against sheet: bias_sel_pd, bias_sel_noab_pd and both pads equal.
  - Open: `bias_oa_pd`'s flat sheet still has the pre-layout core, while its source (which instantiates oa_core_pd)
    has the new one: 34 against 44 devices.
- Backup of the four replaced files and the check outputs: `oa_core_pd_v2_2026-10-28/macro_before/` and
  `macro_install/`.

## 2026-10-28 05:20–06:32 bg_core_pd compact: A2's assembly checked, into the notes and the macro (Christoph, 04:25: "There should be lessons learned from Oguey Aebischer for first modifying layout primitives for the bandgap reference, then compacting the overall bandgap core."; 04:28: "It might make sense for Agent 2 to recruit help from Agents 3 and 4.")

- Layout: A2 assembled it by 06:19 from A3's bg_n4 (option 1), A4's bg_pmir_pcas_c / bg_ms1 / bg_svpg and its own
  bg_res_c / bg_pnp_c.
  - 47.55 × 50.05 µm = 2380 µm². The library primitives take 2673 µm² in their bounding boxes (−11 %), and 3424 µm²
    placed as a block (−31 %).
  - One vdd NWell, no rings, no tie between rows; Metal1 / Metal2 only; vdd on top, vss at the bottom, ports on the
    right edge, as in oa_core_pd v2.
  - bg_res_c: the library's segments, now wired, ring removed, 515.0 → 401.1 µm². bg_pnp_c: the 3 × 3 array, now
    with emitter / base wiring, same size.
  - A2's checks: DRC 0 of 74 rules (latch-up and antenna included); LVS match against the composed reference and
    against its backannotated netlist (30 devices); byte-reproducible build.
- My check, an independent flat extraction (MOS; rhigh in squares on PolyRes; pnp emitters with their nets):
  - every MOS on its sheet nets, the dummies as listed;
  - R0 357.84 squares eb–e2, R1A 218.68 ea–vss, R1B 198.80 eb–vss, the dummy segments vss–vss;
  - Q1's emitter on ea, 8 × Q2 on e2, base vss;
  - one label per net.
- In the notes (06:23): A2's whole `out_bg/` (105 files, my check files in `logs/session_check_*`) in
  `design_considerations/pad_buffer_layout/bg_core_pd_2026-10-28/`.
- In the macro (06:26):
  - `macros/bg_core_pd/layout/gds/bg_core_pd.gds` (sha c799ffb5…), new;
  - README: the layout section, and what the sheet does not have yet.
- Not done yet: the sheet and the subckt `bg_core_pd` in `bias_ref_pd.spice`. A2's backannotated sheet copy puts the
  41 resistor segments in a grid of labels and is not used. What the backannotation has to bring in:
  - R0 / R1A / R1B as chains of 18 / 11 / 10 segments 0.5/9.94: R +0.70 / +1.03 / +1.02 %, R1 / R0 +0.32 %, not
    simulated (the library bg_res already had these segments);
  - NA / NB ng 2;
  - MS1 as an 8-device chain;
  - the dummies: PMOS 2.4/1 on vpg and on vpc, NMOS 16/4 + 2/1 with D = S = G = g, 2 rhigh segments on vss.
- A2's open point: ea and eb are not mirror images (18 µm against 4.6 µm of Metal1 / Metal2, at µA currents into
  kΩ–MΩ; the PDK copy has no metal sheet resistance to confirm that it doesn't matter).
- Backup: the README and the sheet as they were, in `bg_core_pd_2026-10-28/macro_before/`.
- Agents folder: A2's report as `agents/A2_oa_core_pd_layout/report_bg.md`, with three pictures. The messages to
  A2, A3 and A4 from 05:20 on are added to their `messages.md`, taken from the agents' own transcripts.

## 2026-10-28 10:39–11:00 bg_core_pd sheet backannotated, resistor chains as vector instances (Christoph, 10:39: "try the vector instances.")

- Sheet `macros/bg_core_pd/schematic/xschem/bg_core_pd.sch` (sha bd3e1864…), in its own style, as for oa_core_pd:
  - R0 / R1A / R1B as xschem vector instances `R0[17:0]`, `R1A[10:0]`, `R1B[9:0]` (0.5u / 9.94u each), connected
    by bus labels: `eb,n0[16:0]` / `n0[16:0],e2`, `ea,n1a[9:0]` / `n1a[9:0],vss`, `eb,n1b[8:0]` / `n1b[8:0],vss`.
    xschem netlists them as the chains eb – n0[16] … n0[0] – e2 etc.;
  - box [C] widened (+210 / +230 from x 520 / 670, +470 from x 820), so the labels clear the bulk wires and the
    neighbouring resistor texts;
  - NA / NB ng 2; MS1 as the drawn chain in [S1]; dummies MDUM0–3 and `RDUM[1:0]` in [D].
- Subckt `bg_core_pd` in `bias_ref_pd.spice` (sha 709f30ac…) edited in place, block-scoped, with the sheet's names;
  README (sha 1323e721…) says the sheet follows the layout.
- Checks (`bg_core_pd_2026-10-28/macro_install/`):
  - LVS of the GDS against the sheet's netlist: MATCH, 30 devices after combining, no shorts or opens;
  - sheet against subckt: equal, 67 devices;
  - all 94 sheets with their own xschemrc, before / after, with the new subckt swapped in before: 93 identical,
    only bg_core_pd.sch differs (6 devices out, 55 in);
  - pads, source against sheet: as before (IOPadDiff2Single equal; IOPadSingle2Diff's only difference is the
    expression {wcl} against its value 12u, unchanged).
- Open, as for oa: `bias_bg_pd`'s flat sheet still has the pre-layout core; its source instantiates bg_core_pd.
- Backups in `bg_core_pd_2026-10-28/macro_before/` (bias_ref_pd.spice, the README with the layout section).
- The batch svg renders misplace right-aligned labels by an amount that depends on xschem's window zoom; the label
  clearances were checked by geometry (worst case: xschem's text width estimate).

## 2026-10-29 (night) and 14:04–14:25, 2026-10-30 15:01–16:10: Claude Code cloud sessions, IIC-OSIC-TOOLS 2026.10, bg_core_pd PEX here, oa_core_pd brief for the cloud (Christoph: "Task at hand: set up Chipalooza sg13cmos5l tasks so that they ARE covered."; 14:04: "okay as proof of concept, set up a cloud PEX task for bg_core_pd."; 14:12: "... then the sponsored cloud PEX should be the Oguey Aebischer variant. Test only ONE of these on my current setup, the other one as Anthropic sponsored cloud process.")

- `sudelbuecher/cloud_environment.md` (sha f95e6bfd…, pushed in cd46d8a): reference IIC-OSIC-TOOLS 2026.10 (tag
  2026-10-14), the 2026.09 pins beside it. The image repo doesn't pin the IHP PDK; provisional df4c5054 (dev head on
  the tag day), the true value is `$PDK_ROOT/ihp-sg13cmos5l/COMMIT` in the 2026.10 image. New section "Claude Code
  cloud sessions": environment `sg13cmos5l` (Custom network + defaults + `www.klayout.org`; `PDK_ROOT`, `PDK`,
  `BASH_DEFAULT_TIMEOUT_MS`), the setup script (lines 152–199), sessions start from `toplevel`.
- The $250 cloud credit covers only Claude Code cloud sessions (claude.ai/code), until 5 Nov 08:59 CET; this
  Cowork chat is not covered.
- bg_core_pd, here (Cowork, Christoph's quota), `toplevel` 1903407, the 2026.10 tools built in the container, PDK
  df4c5054, the macro's own Makefile targets:
  - `magic-drc`: no errors; `magic-lvs`: match;
  - `magic-pex` EXT_MODE 1/2/3 and `klayout-pex` 2: all ports connected, about 1 s each; 123 devices; C elements
    50 / 313 / 347 (magic) and 317 (kpex), R 359 in mode 3;
  - port C in fF, magic 1 / 2 / 3 / kpex: iout 44.2 / 41.9 / 39.4 / 40.5, vdd 48.5 / 76.1 / 63.7 / 73.4,
    en_3v3_b 0 / 12.0 / 11.7 / 13.6 (mode 1 lumps everything to substrate; in mode 3 the sum covers only the port
    node itself);
  - warnings, not errors: xschem's res_drc on the bus instance names (`invalid command name "9:0"` etc.), and
    `MS1_x` sg13_hv_pmos l = 12.5 µm above the model's 10 µm limit.
- Template findings, worked around without touching design files:
  - the PEX targets call `$(SCRIPTS_DIR)/check_pex_ports.py` with `SCRIPTS_DIR := scripts`, relative to the
    macro, but the script is in the repository root: `make ... SCRIPTS_DIR=../../scripts`;
  - kpex 0.6.8 takes `--pdk ihp-sg13cmos5l`, the template passes `ihp_sg13cmos5l`: the setup script wraps `kpex`;
  - the `sak-*` scripts come without exec bits: `chmod +x` in the setup script.
- Brief `sudelbuecher/cloud_sessions/C0_oa_core_pd_pex.md` (sha aa2c6f07…, pushed in cd46d8a): oa_core_pd from
  `toplevel`, results on `claude/c0-oa-core-pd-pex` and `claude/c0-oa-core-pd-pex-sudel`, bg_core_pd numbers for
  comparison. `C0_pilot.md` deleted (3acf926).
- Chatlog: the transcript records from 2026-10-27 03:12 to 2026-10-29 14:15 are lost (session restore and
  compaction); turns 97–121 of the chatlog have only Christoph's messages.
- Next: Christoph starts the cloud session (steps 2–7: environment `sg13cmos5l`, repository branch `toplevel`).

## 2026-10-30 16:30–17:55: GitLab backup, Claude cloud environment `sg13cmos5l`, Claude GitHub App (Christoph, 17:43: "Step by step ... and we'll log everything of this, with screenshots, as per standard procedure.")

- Screenshots: `chatlog/pix/2026-10-30_opus_cloud_setup_01…21_*.png`, shown in the chatlog at the turns where
  they were sent; the credit screenshot of 29 Oct as `chatlog/pix/2026-10-29_opus_usage_cloud_session_credit.png`
  (cropped to the Settings dialog).
- GitLab backup: remote `gitlab` = `git@gitlab.com:tatzelbrumm/sg13cmos5l_cm_ip_single2diff2single.git` (GitLab
  path with one underscore), kept separate from `origin`; `git push gitlab --all` and `--tags`; GitLab's starter
  commit on `main` replaced with `git push --force gitlab origin/main:refs/heads/main` (force push allowed on
  the protected `main` for that). GitLab's GitHub importer was not used: its OAuth asks for read and write on all
  repositories and fablab-neckar-alb.
- claude.ai: "Connect GitHub" (identity only), monthly API credits not claimed (they don't cover cloud
  sessions).
- Environment `sg13cmos5l` (claude.ai/code → environment menu → New environment; edit via the gear wheel on its
  row): Network access "Limited", allowed `www.klayout.org` and `github.com`, "Allow package managers" on;
  network secrets none; setup script 48 lines (`cloud_environment.md` lines 152–199); 3 variables (`PDK_ROOT`,
  `PDK`, `BASH_DEFAULT_TIMEOUT_MS`). `cloud_environment.md` corrected to these option names.
- Claude GitHub App (github.com/apps/claude → Install → tatzelbrumm → Only select repositories): installed on
  `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single` only; read on administration, commit statuses, merge
  queues, metadata; read and write on actions, checks, code, discussions, issues, pull requests, repository
  hooks, workflows. Confirmed with the authenticator code; claude.ai Connectors shows "GitHub Integration" ✓.
- Branch protection on GitHub for `main`, `toplevel`, `sudel_buecher`: not set; the brief's rule is the only guard.
- Next: start the cloud session (repository, branch `toplevel`, environment `sg13cmos5l`, the brief's first message).
