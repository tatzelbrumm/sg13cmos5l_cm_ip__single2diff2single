# F stage 2: own cells (2026-10-31, 17:50 CET)

- Scripts in `src/` (copies of `../work/src/`); cells in `cells/` (.gds + .cdl); checks in `logs/stage2_checks.txt`.
- Previews in `previews/`. Rule values come from `sg13cmos5l_tech_default.json`, keys cited in the scripts.
- [m] = measured / tool result, [r] = reasoning.

| cell | size (µm) | DRC (run_drc, main + maximal incl. LU) | LVS (run_lvs, no tap extraction) |
|---|---|---|---|
| d2s_rhigh | 13.92 × 15.41 | 0 | match (16 segments + 2 dummies) |
| bias_tree_pd | 52.36 × 11.82 | 0 | match against "sheet minus Xd" |
| d2s_cma / d2s_cmb | 35.40 × 11.52 / 35.40 × 9.36 | 0 / 0 | match / match |
| cma_ring | — | 0 | (no device) |
| guard_tie, nw_isolator, edge_stubs | — | only M3.c1 / V1.c1 standalone: their vias land on the pad's M1 / M3 | in context, see below |
| pad candidate `pad_stage2.gds` (all the above in the pad top) | 80 × 180 | **0** | probes: 8 / 8 nets as expected [m] |

**d2s_rhigh** (`build_d2s_rhigh.py`), after bg_res_c:
- The library rhigh segment, unchanged, at 0.68 pitch, with the map `d A B C1 C2 C2 C1 B A A B C1 C2 C2 C1 B A d`.
- All 8 terminals are on M2 at the top edge (x 0.93 … 11.13).
- Nested links alternate M1 / M2 on one level, so 2 levels per side instead of 3.
- p+ ties on both sides; the dummies are shorted to them.
- Smaller than the library (14.76 × 17.50).
- Magic PEX (EXT_MODE=2): **18 capacitor-only nodes**, one per segment (16 + 2 dummies) [m].

**bias_tree_pd** (`build_bias_tree_pd.py`):
- The library bias_tree_p | swp | sw | bias_tree_n are placed unchanged, with their rings, and wired at the top.
- The ring removal I considered saves under 2 µm of width [r], so I did not do it.
- The bottom-right L of the floorplan (≈ 535 µm²) cannot take 620 µm². So the tree moves to the top band
  (x 2.6–55.0, y 157.0–168.8). tree_p's well merges with the loads' well (one iovdd NWell).
- The CMB reserve moves to the bottom-right L, next to the b join (x 47–66, y 92–104 plus x 54–66, y 104–123), plus
  y 169.4–177.5 at the top. That is ≈ 1040 µm² in total, as before.
- iref / en_3v3 / en_3v3_b leave at its top edge: pins proposed at x ≈ 24.2 / 25.9 / 26.7. vinp / vref / vinn go
  to x 56–59 (right channel). Picture: `previews/floorplan_v1_stage2.png`.

**CMA / CMB** (`build_pad_stage2.py`):
- Kept as one unit each, as in the sheet, in their own regions (the cells d2s_cma / d2s_cmb).
- **CMA's guard ring: closed** [m]. A p+ ring (iovss), 0.30 wide, sits in the existing NW.b1 1.80 gaps: below to DCN's
  guard well, left to the band well, right to CMB's well. It joins DCPDiode's p+ guard ring above.
  - To make room under the junction, CMA's M1 U lost its bottom strip.
  - Its two columns are now fed from the junction by M2 tabs with 88 Via1. m2_junction's 332 Via1 onto the old strip
    are removed.
  - CMA is now ringed by p+ iovss on all sides, with n-wells on iovdd below (DCN guard), left (band) and above
    (DCPDiode).
- Series channel resistance: no split, so it is unchanged from A1's 7.96 × 32.16. L/W = 4.04 squares, against
  1.0 for the former 16 × 16 [r].

**guard tie** (open point of 10-28): closed [m].
- M2 at x 1.25–1.65, with 26 Via1 on the DCN guard M1 (y 26–38) and 2 Via2 into M3 iovdd (66–91.5).
- guard is now on the same net as iovdd (band 66–91.5).

**NWell isolator** above the P frame:
- n+ (iovdd) at y 84.79–85.09 in NWell 84.55–85.33, x 2.84–77.16.
- It is 0.29 above the frame's p+ ring (NW.f 0.24), not at the limit.
- 19 Via1 / Via2 taps into M3 iovdd, none at x 37–40.8 (dabn / dabp).

**edge stubs:**
- All IHP edge intervals above y 84 are drawn at both edges, each tied to its rail: p+ iovss via 126–134; iovdd n+
  via M2 to M3 iovdd 93.5–119; vss / vdd via stacks.
- `row_check.py`: every edge layer is the same as IOPadAnalog's, and every band and rail is one net through the row.
- Row DRC: 0.
- Note: the row check's label column ("dabn/vss") is cosmetic. It keys hierarchical net names across cells; the
  pass / fail logic is not affected [m, checked by probing].

**Changes to the pad top's static cells** (stage 2):
- cap_cma → d2s_cma (M1, M2 tabs, Via1, pins);
- cap_cmb → d2s_cmb (renamed, pins);
- m2_junction (−332 Via1);
- new cells: cma_ring, guard_tie, nw_isolator, edge_stubs.
- PCells, TopLayersTo4, Metal3ViasUp and contacts are untouched; the PCell context is kept.
