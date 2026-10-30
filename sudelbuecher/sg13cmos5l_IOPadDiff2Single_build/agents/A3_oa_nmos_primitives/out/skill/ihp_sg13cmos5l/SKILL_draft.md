---
name: ihp-sg13cmos5l-rotated-mos-rows
description: IHP sg13cmos5l-specific companion to ../generic/ (rotated-row MOS arrays). Holds the process adapter (layers, json rule keys, SG13_dev device cells, LVS recognition), the deck files that implement each rule and the ones missing from this PDK copy, latch-up as the IHP deck computes it, ThickGateOx / NWell specifics, the library's pin / text conventions, and the IHP pitfalls with workarounds (Python DRC subset and LVS when the KLayout Ruby deck cannot run).
---

# Rotated-row MOS arrays in IHP sg13cmos5l [IHP]

Draft, 2026-10-28, Claude (Opus 5.5). The procedure is `../generic/SKILL_draft.md`; this part adds what is
specific to IHP sg13cmos5l and to the pad-buffer cell library of the Chipalooza project.

## Files

- `adapter.py`: the process adapter for `../generic/generator.py` (layer map from `sg13cmos5l.lyp`, rule keys of
  `sg13cmos5l_tech_default.json` with the deck rule each implements, device cells, LVS recognition notes).
- `rules.md`: every rule of `../generic/rules.md` with its IHP value and deck citation, plus the IHP pitfalls.
- `tools/oa_core_pd_drc.py`, `tools/oa_core_pd_lvs.py`: the Python DRC subset and LVS used here (copies of the
  project's tools; DECK path inside).
- `make_pictures.py`, `pictures/`: tile with letters / tracks / pins / scale bar, before / after, rule picture.
- Worked examples: `../../build_oa_n.py` -> `oa_n10`, `oa_mcs_c` in `../../oa_n_cells.gds`;
  `../../../out_bg/build_bg_n.py` -> `bg_n4` (NA / NB 2 x 10/4 each, MS2, MS3, SKS) in `../../../out_bg/bg_n_cells.gds`;
  picture `pictures/bg_n4.png`.

## Device cells (SG13_dev, exported PCell variants)

- HV NMOS `nmosHV`: frame with the gate vertical; Activ (0, 0; L + 0.68, W); poly (0.34, -0.18; 0.34 + L,
  W + 0.18); S/D stripes Metal1 0.16 wide at 0.07 ... 0.23 from each Activ end, full W, contacts at about 0.34 pitch
  (exact positions depend on W only); ThickGateOx 0.27 beyond the Activ along L, 0.52 along W; texts `nmosHV` on
  TEXT 63/0 and HeatTrans 51/0; Metal1.pin on the stripes, GatPoly.pin 5/2 on the gate.
- Library names: `nmosHV$N` variants of `pad_buffer_cells.gds` (10/1 = nmosHV$7, 10/4 = nmosHV$10, 2/4 = nmosHV$11,
  3.4/30 = $8, 0.5/2 = $9, 1/0.45 = $5). No 5/4 variant exists and none can be derived (no W = 5 reference). Copy them unchanged; R270 + shift (0, L + 0.68) puts W along x with upright texts.
- No PCell code in this PDK copy: a missing variant (here 2/1) comes from `derive_mos` (x from a same-L variant,
  y from a same-W variant, checked layer by layer). Give it a unique name (`nmosHV_w2_l1`) for reimport.
- `ptap1` PCell: 2 contact rows, Activ 0.78, Substrate 40/0 + Metal1.pin. The tie segments here are plain p+
  Activ with one contact row (rules.md 4) and no 40/0.

## Deck files

Present: `ihp-sg13cmos5l.drc`, `rule_decks/sg13cmos5l_maximal.drc`, the json, `feol/5_1_nwell, 5_2, 5_3, 5_6, 5_9,
5_14_cont, 5_15`, `beol/5_17_metaln, 5_18, 5_19_via1, 5_20, 5_21, 5_27, 6_9, 6_10, 7_3`, `geometry/3_1, 3_2`,
`pin/7_4`, `forbidden/*`, `antenna.drc`, `density.drc`. Missing (included by `ihp-sg13cmos5l.drc`):
`layers_def.drc`, `feol/5_5_activ, 5_7_thickgateox, 5_8_gatpoly, 5_10_psd, 7_2_latchup`,
`beol/5_16_metal1, 5_22, 5_23, 9_1`. No LVS deck, no PEX rules, no model cards in this copy.

## Latch-up as the deck computes it

- LU.a (PMOS): MAX, `all_ntie.ext_enlarge_inside(NWell, 20 um)`: distance measured inside the NWell.
- LU.b (NMOS, 20 um): json `LU_b` only; its file `7_2_latchup.drc` is missing. The Python subset reads it as LU.a
  for the substrate (grow the ties by 0.5 um steps inside the substrate). Report the measured distance per tie
  segment (oa_n10: 18.90 um, oa_mcs_c: 7.48 um).
- LU.d1: tie Activ at most 6 um beyond a contact (`generator.tie` checks it).
- Stack limit with one tie: ten rows of L = 1 um (oa_n10, 18.90 um) or four rows of L = 4 um (19.56 um); bg_n4
  (four L = 4 rows + an L = 1 row) needs a second segment on top (rules.md 19).

## HV and well specifics

- All devices here are HV (under ThickGateOx): Gat.b1 0.25 between gates, pSD.j1 0.40 from an NFET gate,
  TGO.a 0.27, TGO.e 0.86 merge distance; NW.*1 values (0.62) apply in TGO.
- Angles (3_2_angle.drc): NWell, pSD, ThickGateOx only "no acute angle < 87 deg"; polygons following the devices
  are legal and cheaper than rectangles.
- No NWell for NMOS arrays; a shared well, if ever needed, merges with the PMOS group's (NW.b 0.62 same net).

## Library conventions

- Pins: `Metal1.pin` 8/2 + `Metal1.text` 8/25, `Metal2.pin` 10/2 + `Metal2.text` 10/25, text at the box centre,
  one per net, on the cell edge. Device names on TEXT 63/0. Nothing on Via2 / Metal3 and above.
- Reference netlists `.cdl`: one line per finger, dummies included (`M<name> d g s b sg13_hv_nmos w= l= ng=1 m=1`).

## Run

```sh
python3 build_oa_n.py <pad_buffer_cells.gds> <out_dir>
python3 skill/ihp_sg13cmos5l/tools/oa_core_pd_drc.py oa_n_cells.gds oa_n10 logs/drc_oa_n10.txt
python3 skill/ihp_sg13cmos5l/tools/oa_core_pd_lvs.py oa_n_cells.gds oa_n10 oa_n_cells.cdl oa_n10
python3 skill/ihp_sg13cmos5l/make_pictures.py oa_n_cells.gds oa_n_cells.cdl <pad_buffer_cells.gds> .
```

In IIC-OSIC-TOOLS (KLayout >= 0.30.2) also run IHP's `run_drc.py` / `run_lvs.py` (`--disable_tap_extraction`
only matters for ptap1 PCells); this was not possible in the cloud container (KLayout 0.28.16, no Ruby).
