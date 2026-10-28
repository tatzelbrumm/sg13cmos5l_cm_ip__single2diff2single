# oa_core_pd layout from the OA primitives: report

2026-10-28, 01:34 to 02:23 CET (Europe/Berlin). Work was done in the cloud workspace only.

## Envelope and size
- **Envelope:** BRIEF.md asked for the pad-cell envelope. The library's fit cell `fit_bias_tree_oa_bg` packs tree, OA core and bandgap into 80 × 102.3 µm. During the task the coordinator changed this to slot 7, minimum area, aspect 1:1 to 2:1, and I followed that.
- **Block:** x 0–76.00, y 0–50.74 µm, 3856 µm².
- **Utilization:** the six primitive bounding boxes add up to 2915.7 µm², 76 % of the block.
- **What sets the size:**
  - Height is `oa_pmir` (42.77) plus `oa_mcs` (6.01) plus the rails.
  - Width is `oa_pmir` with its jumpers (29.8), plus `oa_nmir` (34.1), plus a routing channel, plus `oa_misc_n` (9.5).
  - My reasoning: `oa_mcs` alone is 62.5 µm long, so the block can't be narrower than that anyway.

## Floorplan
Coordinates in µm. All values are named parameters at the top of `oa_core_pd_build.py`.

| cell | placement | bounding box x | bounding box y |
|---|---|---|---|
| `oa_pmir` | mirrored (M0) at (3.755, 48.6) | 0–28.025 | 7.81–50.58 |
| `oa_pmir_image_jumpers` (new) | same transform as `oa_pmir` | 1.945–29.76 | 18.545–39.845 |
| `oa_pcas` | mirrored (M0) at (31.605, 38.08) | 29.625–51.085 | 32.47–41.01 |
| `oa_misc_p` | rotated 180° at (73.98, 48.19) | 63.96–76.0 | 33.03–50.17 |
| `oa_nmir` | R0 at (32.5, 20.69) | 29.97–64.09 | 7.09–31.47 |
| `oa_misc_n` | R0 at (65.4, 20.69) | 65.13–74.64 | 18.86–31.47 |
| `oa_mcs` | R0 at (0.27, 2.53) | 0–62.5 | 0.70–6.71 |

- **Grouping:** the PMOS cells sit at the top (`oa_pmir`, `oa_pcas`, `oa_misc_p`). The NMOS cells sit below (`oa_nmir`, `oa_misc_n`), with `oa_mcs` along the bottom.
- **pcas to pmir:** pcas's four source tracks are in line with pmir's band B, in the same order (vpg, c2, c8, co) and at the same 0.5 µm pitch. They connect with four straight M2 lines. pcas's drain tracks face down toward nmir.
- **misc_p over misc_n:** `oa_misc_p` is rotated so that ks sits at its bottom, directly above misc_n's ks pins.
- **Ties:** misc_n's vss tie is in line with nmir's tie, so one straight M1 piece joins them.

## Devices of the sheet and the primitives that hold them
The sheet (`oa_core_pd_xschem.spice`, 18 devices) and subcircuit `oa_core_pd` of `bias_ref_pd.spice` agree device by device: nets, model, w, l, ng. The port order differs:
- xschem netlist: `vdd vss en_3v3 en_3v3_b iout`;
- symbol and hand netlist: `vdd vss iout en_3v3 en_3v3_b`. `oa_core_pd.cdl` uses this order.

| sheet devices | W/L (ng) | primitive | as drawn (from extraction) |
|---|---|---|---|
| P0, P2, P8, PO | 2/8, 4/8 (2), 16/8 (8), 40/8 (20) | `oa_pmir` | 1, 2, 8, 20 fingers of 2/8, plus 9 dummies 2/8 (S=D=B=vdd, G=vpg) |
| P0C, P2C, P8C, POC | 0.5/2, 1/2, 4/2 (2), 10/2 (5) | `oa_pcas` | 1, 1, 2, 5 fingers, no dummies |
| M10, M11 | 180/1 (8), 90/1 (4) | `oa_nmir` | 18 and 9 fingers of 10/1, plus 1 dummy 10/1 (S=D=B=vss, G=vnc) |
| MCS, MCL | 3.4/30 | `oa_mcs` | as in the sheet |
| MC10, MS2, MS3, SKS | 10/1, 10/1, 0.5/2, 1/0.45 | `oa_misc_n` | as in the sheet |
| MS1, SVPG | 0.5/100, 1/0.45 | `oa_misc_p` | MS1 as 8 × 0.5/12.5 in series (nodes ms1–ms7); SVPG as in the sheet |

- No sheet device is missing from the primitives.
- Primitive devices that are not in the sheet: the 10 dummies, and MS1 split into 8 series devices.
- The finger counts and the MS1 split are the netlist changes listed in the library README; the sheet does not have them yet.

## Wiring
- **Layers used:** in the new cells, Metal1 (8/0), Via1 (19/0) and Metal2 (10/0), plus pins on 8/2 + 8/25 and 10/2 + 10/25. Nothing on Via2 or Metal3 and above anywhere in the hierarchy (checked).
- **Why only M1/M2:** the primitives use only Metal1 and Metal2. Top-level wiring therefore runs between the cells, and crosses a cell only on M2 where that cell has no M2.
- **Wire geometry:** wires are 0.29 µm on both metals. Via1 is 0.19 µm with 0.05 µm enclosure on all sides. Everything is on the 5 nm grid.
- **Rails and straps (all M1):**
  - vss rail: y 0–1.42, overlapping oa_mcs's substrate tie.
  - vdd rail: y 49.24–50.74, overlapping the top ring sides of oa_pmir and oa_misc_p.
  - Two 2 µm straps connect oa_pcas's ring to vdd.
  - One 4 µm strap connects oa_misc_n's tie to vss.
  - nmir's tie connects straight to misc_n's tie.
- **Point symmetry of `oa_pmir`:**
  - The new cell `oa_pmir_image_jumpers` holds the point image of pmir's own left-side M1 jumpers, their 8 vias and the 8 M2 band tracks. The image is taken about the array centre (11.125, 19.405 in cell coordinates).
  - Measured: pmir's M2 plus the image cell is exactly point-symmetric (XOR with its image is 0.000 µm²). The device layers were already symmetric.
  - The remaining M1/Via1 asymmetry (14.16 / 0.14 µm²) is inside oa_pmir as delivered: P0's drain tab against the inner dummy's drain-source strap.
  - The external connection is a single tap, from band B's right end straight into pcas. That spot is the point image of the cell's own pin position (band A, left end). Bands A and B are now joined on both sides.
- **High-impedance nets:**
  - iout leaves pcas's drain tracks immediately and runs up in M2 to the top edge. Outside pcas, it runs parallel to a high-impedance wire only for a 1.6 µm stub next to vnc, at 0.5 µm pitch.
  - vnc, vbr and vpc turn down at x 51.35–52.35, away from iout.
  - vpg crosses iout once, as a short M1 hop.
  - vbr (M2) and vres (M1) share the channel between nmir and misc_n for about 12 µm, at 0.55 µm pitch.
  - ks runs in M2 from misc_p to misc_n, about 7 µm, plus two short branches.
  - en_3v3 runs about 3 µm to the top edge. en_3v3_b runs about 5 µm down to SKS, plus 1.3 µm to the edge.
- **Added pads:** MC10's drain stripe (vpc) and MS2's drain stripe (ks) are only 0.16 µm wide. I added 0.29 × 0.29 µm M1 pads on them for via landings. The pads are top-cell shapes; the primitive is unchanged.

## Ports
Each port is a pin box plus a text, following the library's convention (`<metal>.pin` + `<metal>.text`).

| port | layers | box (µm) | edge |
|---|---|---|---|
| vdd | Metal1 8/2 + 8/25 | the whole top rail | top |
| vss | Metal1 8/2 + 8/25 | the whole bottom rail | bottom |
| iout | Metal2 10/2 + 10/25 | 52.805–53.095 × 50.24–50.74 | top |
| en_3v3 | Metal2 10/2 + 10/25 | 65.485–65.775 × 50.24–50.74 | top |
| en_3v3_b | Metal2 10/2 + 10/25 | 75.5–76.0 × 31.855–32.145 | right |

## DRC
- **Method:** my own checks in Python on `klayout.db` 0.30.12, in `oa_core_pd_drc.py`.
- **Why not IHP's deck:**
  - Only KLayout 0.28.16 is installed; the deck needs 0.29.11 or newer with Ruby.
  - Downloading the KLayout source was blocked: the GitHub repository isn't enabled for this session, klayout.org and klayout.de return 403 under the network policy, and the PyPI source package has no Ruby or DRC parts.
  - The uploaded `drc/` folder is missing files the main deck includes: `layers_def.drc`, `5_5_activ`, `5_7`, `5_8_gatpoly`, `5_10_psd`, `5_16_metal1`, `7_2_latchup` and others.
- **Rule values:**
  - All come from `sg13cmos5l_tech_default.json`; the log names the key for each rule.
  - One exception: M2.c1 = 0.05 µm, which has no json key. I took it from the rule text in `sg13cmos5l_maximal.drc`.
- **Rule semantics:**
  - They follow the deck file named for each rule in the log: `sg13cmos5l_maximal.drc`, `feol/5_1_nwell.drc`, `feol/5_14_cont.drc`, `beol/5_17_metaln.drc`, `beol/5_19_via1.drc`, `pin/7_4_pin.drc`, `geometry/*`, `forbidden/*` and `antenna.drc`.
  - For rules whose implementing file is missing (Act.a/b, Gat.a/b/d, M1.a/b/e/f, TGO.f, LU.b), the log marks them "json only". The check is my plain reading of the rule.
- **Rules checked:**
  - grid, angles, CMOS5L forbidden layers;
  - NW.a/b/b1/c/c1/d/d1/e/e1/f/f1, with NW.b and NW.b1 told apart by the NWell's net;
  - Act.a/b/d, TGO.a–f, Gat.a/a3/a4/b/b1/c/d/e, pSD.a/b/c/d/i1/j1;
  - Cnt.a–h and Cnt.j, M1.a/b/c1/d/e/f, V1.a/b/c/c1, M2.a–f, Pin.e and Pin.f_M2, and a check that nothing is on Metal3 or above;
  - latch-up LU.a/b (20 µm, measured inside the well);
  - antenna Ant.b and Ant.d for gate-only nets.
- **Not checked:** density, fillers, slits, contact and via arrays (Cnt.b1, V1.b1), and rules for devices that aren't in this block.
- **Result:**
  - 0 violations on `oa_core_pd` and on each of the six primitives.
  - Antenna ratios: en_3v3 2.30, en_3v3_b 0.17 (limit 200).
  - Logs: `logs/drc_oa_core_pd.txt`, `logs/drc_lib_cells.txt`.
- **Self-test:** I injected violations of 23 rule families plus an antenna ratio of 207 into a copy of the layout; all were found (`logs/selftest_drc.txt`).

## LVS
- **Method:** extraction with `klayout.db` (`oa_core_pd_lvs.py`). Devices are recognized using the derivations in the DRC decks:
  - sg13_hv_pmos: gate on P+ Activ in NWell under ThickGateOx, bulk = NWell;
  - sg13_hv_nmos: gate on N+ Activ outside NWell under ThickGateOx, bulk = substrate;
  - low-voltage gates outside ThickGateOx are counted as errors: 0 found.
- **Passes:**
  - Parallel fingers are combined on both the layout and the reference side.
  - A first pass uses all labels to find shorts and opens by net name.
  - A second pass compares against the reference using only the top cell's labels.
- **Reference netlist (`oa_core_pd.cdl`):** the sheet in symbol port order, with MS1 as 8 × 0.5/12.5 in series and the 9 + 1 dummies.
- **Result:**
  - MATCH, 27 devices after combining parallel fingers, no low-voltage gates, no shorts or opens by label.
  - Logs: `logs/lvs_oa_core_pd.txt` and `oa_core_pd.lvsdb`.
- **Primitives:**
  - All six match their subcircuits in `pad_buffer_cells.cdl` (`logs/lvs_lib_cells.txt`).
  - Only `oa_misc_n` needs same-name labels joined: ks (3 stripes) and vpc (2 stripes) are not connected inside the cell.
  - `oa_pcas` and `oa_misc_p` no longer need joining.
- **Self-test:** an injected M2 short between vbr and vpc, and a removed vnc connection, both give MISMATCH, and the label check names both (`logs/selftest_lvs.txt`).

## Other checks
- **Standalone exports:** `oa_pmir.gds`, `oa_pcas.gds` and `oa_misc_p.gds` XOR to 0 against the library cells on every layer, with equal texts. Only the leaf PCell variant names differ (for example `ntap1` versus `ntap1$35`). The build uses the library cells.
- **Output against library:** 0 differences across 28 cells (6 primitives and their sub-cells), comparing XOR per layer, texts and instances.
- **Reproducibility:** the build writes the GDS without timestamps; two runs gave the same sha256.

## Deviations from the brief
1. **Envelope:** slot 7 at minimum area, as you directed, not the pad pitch.
2. **DRC and LVS method:** my own Python checks instead of IHP's decks. They cover less than the full deck.
3. **Orientation:** three primitives are placed mirrored or rotated (pmir mirrored, pcas mirrored, misc_p rotated 180°). The cells' own geometry is unchanged.
4. **"json only" rules:** where the deck file is missing, the check is my reading of the rule, marked as such in the log.

## Observations on the primitives (left unchanged)
- **`oa_misc_p`:** it still carries the note "NEEDS TO BE BROKEN UP" on layer 63/0. It stays as delivered, per your decision of 2026-10-27 08:45. Its 12 × 17 µm slot in this floorplan is where a broken-up version would go.
- **`oa_misc_n`:**
  - ks and vpc are split inside the cell; the top level joins them.
  - Its 0.16 µm drain stripes are too narrow for a via, so the top cell adds M1 pads.
- **`oa_nmir`:** still in the old generator style: not rotated, a shared tie in the middle, a dummy in the centre, and M2 trunks running over the channels. The Q&A recommends rotating it and adding rings.
- **`oa_pmir` pins:**
  - Its M2 pin boxes (co, c8, c2, vpg) sit on the block's left edge at x = 0.
  - They are the cell's own pins, not block ports, but a slot-level router may show them.
- **`oa_pmir` symmetry:** the P0 / inner-dummy asymmetry described under Wiring is built into the cell.

## Open questions
1. Should the sheet adopt MS1 as 8 × 0.5/12.5 in series and M10 / M11 at 18 / 9 fingers, so that the sheet itself matches the layout in LVS?
2. pmir's connection is a single tap at band B's right end. Would you prefer taps at mid-height on both bands? By my estimate (not drawn) that costs about 9 µm of block height.
3. Are these port sides right for the slot: iout and en_3v3 on top, en_3v3_b on the right, vdd on top, vss at the bottom?
4. The rails are M1 at 1.42 µm and 1.5 µm. Do you want M2 straps on them, wider rails, or a prBoundary layer?
5. vbr and vres share a 12 µm channel at 0.55 µm pitch. Is that acceptable, or should vres move?
6. Should the image jumpers become part of `oa_pmir` in the library at the next reimport?

I have not started bg_core_pd.
