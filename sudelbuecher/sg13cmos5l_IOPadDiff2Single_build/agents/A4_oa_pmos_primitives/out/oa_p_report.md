# Brief P report: compact PMOS primitives for oa_core_pd (IHP sg13cmos5l)

2026-10-28, 02:39–03:26 CET. Worked in the cloud workspace only; no git, `inputs/` untouched. Tags: **[generic]**
holds for any process, **[IHP]** is sg13cmos5l-specific. [m] = measured on the GDS / by a tool, [r] = my reasoning.

## Cells and sizes [m]

All three cells are tap-less, each with one NWell (= ThickGateOx) rectangle to the cell edge. Bulk is the internal
net `nw`, tied to vdd by the parent's tap of the merged vdd well. This follows the user's notices of 02:58 and 03:01.

| cell | before | after | change |
|---|---|---|---|
| `oa_pmir_c` | oa_pmir 28.03 x 42.77 = 1198.6 um² | 20.09 x 39.49 = 793.4 um² | −34 % |
| `oa_ms1` + `oa_svpg` | oa_misc_p 12.04 x 17.14 = 206.4 um² (library unrotated: 58.2 x 5.5) | 6.99 x 14.42 = 100.8, plus 2.24 x 2.37 = 5.3 um² | −49 % |

oa_pmir_c, where the 7.94 um of width and 3.28 um of height went:
- end dummies 2.00 → 0.30 [IHP I1: 2 Cnt_c + Cnt_a]: −3.40 width;
- ring and Metal1 jumpers removed: left side 3.755 → 0.62, right side 2.02 → 0.62 [IHP I4, I11: NW_c1];
- top / bottom margin 1.98 → 0.62 each;
- each band 1.94 → 1.66 [IHP I10: Metal2 0.20 at 0.41].

## Device map [m]

- `oa_pmir_c`: one R270 AREF of pmosHV 2/8 per row plus 0.3/8 rests (score `generic/patterns.md`):

  ```
  r1 drain↓  | d o o o 8 o o 8 o d |     o = PO (co) 20, 8 = P8 (c8) 8, 2 = P2 (c2) 2, 1 = P0 (vpg, diode) 1,
  r2 drain↑  | d o 8 o 1 2 8 o o d |     x = P0's point partner (2/8, D = S = vdd), d = rest 0.3/8 (D = S = vdd);
  r3 drain↓  | d o o 8 2 x o 8 o d |     all gates vpg. Band A (r1/r2) tracks bottom to top co c8 c2 vpg;
  r4 drain↑  | d o 8 o o 8 o o o d |     band B (r3/r4) the point image.
  ```

  - c2, c8 and co bands are joined by a Metal2 staircase over the left row ends. vpg runs through the Metal1 gate
    columns on both sides.
  - vdd runs: top / bottom plates to the edge → rest straps → Metal1 through the bands → the shared r2/r3 plate.
- `oa_ms1`: 8 x 0.5/12.5 (library pmosHV$13), one AREF at 0.75 pitch with a merged en_3v3_b gate strip. Series
  meander vdd → ms1 … ms7 → ks; gate contact column on the left.
- `oa_svpg`: 1/0.45 (pmosHV$7), R270. S = vdd on top, D = vpg at the bottom, gate contact on the right.
- Device cells:
  - 2/8, 0.5/12.5 and 1/0.45 are unmodified copies of the library's PCell cells.
  - 0.3/8 is drawn by the adapter's `pmos_hv()`, which reproduces all 15 single-finger pmosHV cells of the library
    with XOR 0 [m].
  - An adapter-only build (`generic/example_build.py`) XORs 0 against the delivered GDS [m].

## Taps and latch-up (LU_a = 20 um, `sg13cmos5l_maximal.drc` LU.a)

- **Own DRC [m]:** the cells have no tap, so their own DRC shows only LU.a: 80 / 16 / 2 errors, i.e. every S/D. This
  is intended. [generic G3–G6]
- **Assumed parent taps:** one-contact tap segments, which `generic/generator.py tap_path` draws. Farthest P+ Activ
  for each tap set [m, `check.py lu`]:
  - **(a) recommended:** top + bottom segments inside oa_pmir_c's 0.62 margins, Activ y 38.46–38.76 and −0.51–−0.21
    under the existing vdd plates.
    - Full width gives 19.23 um.
    - The minimum centred length is 7.86 um each. Context `ctx_tb` with 8.2 um segments: 0 DRC violations including
      LU.a.
    - The parent's well must reach 0.51 um past the top / bottom edges (NW_e1 0.62). [IHP I5]
  - **(b)** left edge only: 19.47 um at full height, minimum 29.10 um; `ctx_left` (29.4 um) passes the rule checks
    with 0 violations.
  - **(c)** left + right edges: 9.92 um.
  - **(d)** top only: 38.87 um, fails.
  - **oa_ms1** with a segment along any full edge: ≤ 13.80 um. **oa_svpg:** ≤ 1.75 um. Both are fine within 20 um of
    any tap of the merged well, minus their own extent.
- **Where the well must continue:** every edge of all three cells is an NWell / TGO edge, at NW_c1 0.62 from the outer
  P+ Activ. Abut or overlap them with any vdd-well neighbour (oa_pcas too); never leave a second vdd well. [generic G4]
  - Merged and abutted: 1.24 um P+ to P+.
  - Separate vdd wells would need 1.86 (NW_c1 + NW_b + NW_c1).
  - Old ringed cells: 4.66.
  - Different nets: 3.04 (NW_b1 1.80). [IHP I4]

## Symmetry of oa_pmir_c [m, `check.py sym`, R180 about (9.425, 19.125)]

- XOR with the point image is 0.000 um² on Activ, GatPoly, Cont, pSD, NWell and ThickGateOx.
- Metal differs by: Metal1 13.78 um², Via1 0.14 um², Metal2 27.46 um².
  - These come from P0's drain tab against the inner dummy's strap, the staircase on the left only, and the pins on
    the right only.
  - No Metal2 runs over a real channel. [r] The metal asymmetry does not touch the devices.
- Letter map: 40 fingers, 0 mismatches under R180, with P0 ↔ x. The real fingers alone XOR to P0 + x (34.72 um²), as
  expected.

## Verification [m]

- **DRC:** `inputs/tools/oa_core_pd_drc.py`, the Python subset (72 rules from the json; not IHP's full deck).
  - oa_pmir_c, oa_ms1 and oa_svpg show LU.a only (no tap, see above); antenna 0.
  - Context cells with the parent's taps: 0.
  - The tool's antenna step crashes on `ctx_left` (circuit lookup); its rule part was run directly. [IHP I24]
- **LVS:** `inputs/tools/oa_core_pd_lvs.py` against `oa_p_cells.cdl`: 3 of 3 MATCH (40 / 8 / 1 devices).
  - First run: oa_pmir_c mismatched on the bulk (vdd in the reference, a floating NWell in the layout). Fixed with the
    bulk on the internal net `nw`. [generic pitfall, IHP I20]
- **Build:** byte-reproducible (no GDS timestamps); two builds gave the same sha256.

## Backannotation (layout-driven changes vs. the sheet / v1 `oa_core_pd.cdl`)

1. oa_pmir end dummies 8 x 2/8 → 8 x 0.3/8. Total dummy W 18 → 4.4 um (L = 8), so v1's `MDUMP W=18u` becomes
   `W=4.4u`.
   - [r] DC: none (S = D = vdd).
   - [r] vpg's total gate area 640 → 531 um² (−17 %): vpg settles slightly faster at start-up / enable.
   - Not simulated.
2. Bulk of the three cells: `nw` inside the cells, vdd through the merged well in oa_core_pd. The sheet has vdd, so
   there is no change at block level.
3. No W / L / ng change of a real device.
   - MS1 stays 8 x 0.5/12.5 in series, the library's existing backannotation.
   - An area sweep found 8 fingers to be the minimum: 7–10 lie within 0.4 %; two rows of 4 cost +10 %. [generic G16]

## Pins (`<metal>.pin` + `<metal>.text`, one per net, on the edge) [m]

| cell | Metal1 | Metal2 |
|---|---|---|
| oa_pmir_c | vdd: bottom edge (the top edge also carries the vdd plate) | right edge, band B, 0.41 pitch, bottom to top: vpg 8.895, c2 9.305, c8 9.715, co 10.125. This is pcas's source order. |
| oa_ms1 | vdd and ks: top edge; en_3v3_b: left edge | — |
| oa_svpg | vdd: top; vpg: bottom; en_3v3: right | — |

Note: oa_pmir_c's left edge carries the c2 staircase line in Metal2. Keep Mn_b 0.21 to a neighbour's Metal2.

## Lessons for the bandgap PMOS cells (bg_pmir_pcas, bg_misc_p)

- **[generic]** bg_misc_p is oa_misc_p with other names. Build `bg_ms1` / `bg_svpg` from the same chain and single
  scores.
- **[generic]** Remove bg_pmir_pcas's ntap ring and merge its NWell with its vdd neighbours. Use one-contact rests
  instead of full dummy stacks. Join its outer track pairs with a Metal2 staircase over the row ends instead of
  vertical Metal1 lines.
- **[IHP]** bg_pmir_pcas is 38.6 um wide.
  - [r] Side taps alone would leave about 19.3 um to the centre, which is marginal.
  - Prefer top / bottom tap segments in the margins (as in (a)), then check with `ihp_sg13cmos5l/lu_context.py`.
- **[generic]** Write the map as a score first. `point_image()` and `check.py sym` catch symmetry errors before DRC.

## Skill export

`out/skill/`:
- `generic/` [generic]: score notation, generator, checks, renderer, rules G1–G16, SKILL_draft with a porting section.
- `ihp_sg13cmos5l/` [IHP]: adapter with 41 json-cited rules and 16 layers, rules I1–I26 (deck gaps, ThickGateOx and
  pSD specifics, tool pitfalls), pictures with values, examples, tools.
