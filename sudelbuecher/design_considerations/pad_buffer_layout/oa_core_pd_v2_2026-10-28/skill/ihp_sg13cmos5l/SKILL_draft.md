---
name: analog-block-assembly-ihp-sg13cmos5l
description: IHP sg13cmos5l-specific companion of the process-agnostic analog-block-assembly skill - the process adapter (layers, rule values with json keys, tie / thick-oxide / well construction, latch-up as the IHP deck measures it), the Python DRC subset and LVS extractor that replace the IHP KLayout decks in this environment, the library's pin conventions, and the IHP pitfalls hit while assembling oa_core_pd (OA reference core, slot 7) from compact primitives.
---

# Analog block assembly in IHP sg13cmos5l (IHP-specific part)

The procedure, notation and generators are in `../generic/` (start with `../generic/SKILL_draft.md`). This folder
holds what only holds for IHP sg13cmos5l (HV devices under ThickGateOx, Metal1 / Metal2 routing).

## Files
- `adapter.py`: the process adapter (every value with its json key / deck file).
- `tools/drc.py`: Python DRC subset on klayout.db (72 rules, values from `sg13cmos5l_tech_default.json`, semantics
  from `sg13cmos5l_maximal.drc` and the feol / beol files); `run(gds_or_layout, cell)`, antenna Ant.b / Ant.d.
  IHP-only: layer numbers and derivations are written in.
- `tools/lvs.py`: extraction + compare (sg13_hv_pmos / sg13_hv_nmos only; `--flat-ref` for a hierarchical
  reference; `extract(..., combine=False)` for the backannotation). IHP-only.
- `examples/oa_core_pd_v2.py`: the delivered block's config; `python3 ../../generic/generator.py oa_core_pd_v2.py
  out.gds` reproduces the delivered GDS byte for byte (sha256 22ad9f9552e4); primitives copied next to it.
- `examples/make_oa_pcas_c.py`: a well-merging copy of a ringed library cell (ring instances and ring Metal1
  removed, NWell to the cell edge, XOR self-check of everything else).
- `pictures/`: `oa_core_pd.png` (the block, cell names, ties, ports, scale bar), `v1_vs_v2.png` (same scale),
  `rule_savings.png` (the rule behind each saving, annotated).

## IHP know-how
- **Decks:** IHP's KLayout DRC needs KLayout >= 0.29.11 with Ruby; this container has klayout.db 0.30.12 (Python,
  no Ruby). The uploaded PDK copy has `libs.tech/klayout/tech/drc/rule_decks/` with `sg13cmos5l_tech_default.json`,
  `sg13cmos5l_maximal.drc`, feol / beol / geometry / pin / forbidden files, but not `layers_def.drc`, `5_5_activ`,
  `5_8_gatpoly`, `5_16_metal1`, `7_2_latchup` and no LVS deck: hence the Python subset. Rules only in the json
  (no implementing file here) are checked by their plain reading and marked "json only" (e.g. LU_b, M1_a).
- **Devices:** HV MOS = gate (Activ & GatPoly) under ThickGateOx (44/0); PMOS on Activ & pSD in NWell, bulk NWell;
  NMOS outside NWell, bulk substrate. N+ = Activ not under pSD (nSD 7/0 not needed: maximal.drc derives nSD).
  Device cells: SG13_dev PCells pmosHV / nmosHV / ntap1 / ptap1 as placed in `pad_buffer_cells.gds`.
- **Ties:** n tie = Activ in NWell without pSD; inside ThickGateOx the NWell must enclose it by NW.e1 0.62 (outside
  it NW.e 0.24, and then TGO.b 0.27 to the oxide edge); one contact row needs Activ 0.30 = Cnt.a 0.16 + 2 x Cnt.c
  0.07, contacts at 0.34 pitch (Cnt.b 0.18); LU.d: tie Activ <= 6 um beyond a contact.
- **Latch-up:** LU.a (maximal.drc): P+Activ in NWell <= 20 um from an NWell tie, measured inside the well, grown in
  0.5 um steps; LU_b 20 um for N+ (json only, read the same way).
- **Wells:** NW.b 0.62 (same net) / NW.b1 1.80 (different nets); NWell outline: `geometry/3_2_angle.drc` checks only
  acute corners for nwell_drw (ACUTE_LIMIT_DEG = 87.0): rectilinear or 45 degree outlines that follow the cells are
  legal; Activ / GatPoly / Metal1-4 are 0/45/90, Cont / Via1 0/90.
- **Pins:** `<metal>.pin` box (8/2, 10/2) + `<metal>.text` (8/25, 10/25), one per net, on the cell edge.
- **Tap-less cells:** their device bulk goes on an internal net (`nw`) in the cell's CDL; with `vdd` standalone LVS
  fails (floating NWell). The block's LVS reference ties `nw` to vdd (`compose_reference(..., ties={"nw": "vdd"})`).

## Pitfalls specific to IHP (details in `rules.md`, I-numbers)
- Wide-metal spacing (M1.e 0.22 next to M1 wider than 0.30, M2.e 0.24 next to M2 wider than 0.39, run > 1 um)
  applied unconditionally by the router next to wide cell metal can make a small pin unreachable (oa_svpg's
  en_3v3 at a block corner): turn the cell.
- oa_pmir_c's band pins are Metal2 0.20 at 0.41 pitch: no 0.29 pad, and no Via1 inside (V1.c 0.01 needs 0.21):
  reachable only on their centre line or through the cell's own net metal.
- `Region.sized(dx, dy)` in klayout.db needs the mode (3 arguments); `sized(a, b)` is (d, mode).
- xschem netlisting needs the PDK's xschem symbols; the uploaded copy has only `libs.tech/klayout`: a fuller PDK
  copy elsewhere in the workspace was used read-only (`PDK_ROOT` in an xschemrc).
