# Brief P2 report: compact PMOS primitives for bg_core_pd (IHP sg13cmos5l)

2026-10-28, 04:30–05:30 CET (a rate-limit pause until 05:20). Cloud workspace only; no git; `inputs*/` untouched.
[m] = measured, [r] = reasoning. **[generic]** / **[IHP]** as in `out/skill/`.

## Sizes [m]

| cell | before (library) | after | change |
|---|---|---|---|
| `bg_pmir_pcas_c` | bg_pmir_pcas 38.59 x 27.60 = 1065.0 um² (ntap ring) | 45.17 x 16.15 = 729.5 um² | −31.5 % |
| `bg_ms1` + `bg_svpg` | bg_misc_p 12.04 x 17.14 = 206.4 um² | 6.99 x 14.42 = 100.8, plus 2.24 x 2.37 = 5.3 um² | −49 % |

- The cells are tap-less, with one NWell = ThickGateOx rectangle to every edge and bulk = internal net `nw`.
- `bg_pmir_pcas_c`'s width (45.2) is inside A2's 40–50 um.
- Height = 8 rows x 1.68 + 7 gaps x 0.21 (Act_b) + 2 x 0.62 (NW_c1). There are no track bands [IHP I27].

## Device map [m]: score `cstack bg_pmir_pcas_c` in `out/skill/generic/patterns.md`

```
Ma | d o b a o d |   mirror (drain down)        o = PO (co -> POC: iout)   8 fingers 10/1
Ca | d O B A O d |   cascodes, same letters     b = PB (vpg -> PBC: vpc)   4  (diode pair)
Cb | d A O O B d |   cascodes (drain up)        a = PA (ca -> PAC: g)      4
Mb | d a o o b d |   mirror (drain up)          d = rest 0.3/1, D = S = vdd, G = row gate (16)
Ma | d b o o a d |   ... second group, = R180 image of the first; every row and column holds b, a, o, o
Ca | d B O O A d |
Cb | d O A B O d |
Mb | d o a b o d |
```

- **Mirror drain = cascode source** in every column: one Metal1 joint across the 0.21 gap [generic G18].
- **Lanes over each row's channel** (Metal2): co vpg ca over the mirror rows, iout vpc g over the cascodes. Every
  finger has the same centred 3-Via1 tab; only the via picks the lane [G17, G20].
- **Gate pads** at both ends of every row, with a Via1 onto the middle lane (vpg / vpc).
- **Side lines (Metal1, full height):** vpg co ca on the left, vpc g iout on the right.
- **vdd:** top and bottom plates plus the middle plate. The rest columns form the vdd spine.
- **Device cells:** the library's unmodified pmosHV$14 (10/1), $13 and $7. The 0.3/1 rest comes from the
  adapter's `pmos_hv`. An adapter-only build XORs 0 against `bg_p_cells.gds`.

## Symmetry of bg_pmir_pcas_c (R180 about (20.925, 7.455), `check.py sym`) [m]

- XOR 0.000 um² on Activ, GatPoly, pSD, NWell, ThickGateOx, Metal1 and Metal2. The metal over all 32 matched
  channels is identical.
- Cont: 2.458 um² = 32 x 0.0768 um². That is the self-XOR of the library's 10/1 PCell, which floors its contact
  spread over W = 10 to 5 nm [IHP I28]. The array itself adds nothing.
- Via1: 1.733 um² = 48 vias on the side lines: mirror rows' vias on the left, cascode rows' on the right.

## LU (LU_a 20 um) against A2's ties [m]

- **Assumed:** A2's tie in the top vdd rail.
  - A full-width tie abutting the top edge gives a farthest P+ of 15.53 um.
  - A segment inside my top margin (Activ y 15.12–15.42 under the vdd plate, centred at x 20.93) needs a length of
    at least 15.67 um. The 16.0 um context: 0 DRC violations. The parent's NWell then reaches 0.51 above the edge
    (NW_e1).
- Top + bottom ties: 7.97 um. Left + right alone: 22.46 um, fails.
- **bg_ms1 / bg_svpg:** any top segment (13.6 / 1.4 um).
- Own DRC shows LU.a only (96 / 16 / 2 S/D), as intended for tap-less cells. [IHP I30]

## Verification [m]

- **DRC:** Python subset `inputs/tools/oa_core_pd_drc.py` (72 rules): LU.a only; antenna 0.
  - First run: 8 x V1.b (a gate-pad via and a line via on one lane, 0.20 apart) and 8 x M2.c1 (outer-line vias at
    the cell edge).
  - Fixed with line gap 0.20 = V1_b − 2 V1_c and an edge 0.04 beyond the line [G21, G22].
- **LVS** (`oa_core_pd_lvs.py` vs `bg_p_cells.cdl`): 3 of 3 MATCH at the first run (48 / 8 / 1 devices).
  - bg_pmir_pcas_c combines to PB 40/1, PA 40/1, PO 80/1, PBC, PAC and POC as the sheet, plus rests 2.4/1 on vpg
    and on vpc.
- **Build:** byte-reproducible; the OA cells are unchanged (`out/oa_p_cells.gds` 0429f81fb8dd).

## Backannotation

1. No W / L / ng change of a real device: 4 / 4 / 8 fingers of 10/1 = the sheet's ng 4 / 4 / 8; cascodes the same;
   ca / co stay single nets.
2. Dummies:
   - the library had 4 x 10/1 per gate net; now 8 x 0.3/1 per gate net, so dummy W 40 → 2.4 um each on vpg and on
     vpc;
   - [r] gate area on vpg and on vpc 200 → 162 um² (−19 %); no DC effect.
3. [r] Mirror and cascode no longer share one diffusion, as the library's in-line stacks did. ca / co get a second
   S/D stripe and a Metal1 joint per finger: a little more junction capacitance, negligible. Not simulated.
4. MS1 stays 8 x 0.5/12.5 (the area minimum, G16); SVPG unchanged.

## Pins (cell coordinates, um; Metal1 `.pin` + `.text`; bbox x −1.66 … 43.51, y −0.62 … 15.53) [m]

The sides follow A2's requests: NMOS / bipolar below (bottom edge), port edge right, vdd rail on top.
- The brief's "vpg / vpc / ca / co face the NMOS side": ca / co stay internal, as A2 allows. g takes the bottom
  edge instead.
- All side lines run the full height, so every one of them is also reachable at the top edge.

| cell | net | box | edge |
|---|---|---|---|
| bg_pmir_pcas_c | vpg | (−0.80, −0.62; −0.59, −0.30), left line | bottom |
| | vpc | (42.44, −0.62; 42.65, −0.30) | bottom |
| | g | (42.85, −0.62; 43.06, −0.30) | bottom |
| | iout | (43.26, 7.135; 43.51, 7.775), outermost right line | right |
| | vdd | (20.605, 15.21; 21.245, 15.53); top plate x 0 … 41.85. A bottom vdd plate also spans x 0 … 41.85, y −0.62 … 0.23. | top |
| bg_ms1 | vdd | (0, 13.48; 0.5, 13.8) | top |
| | ks | (5.93, −0.62; 6.14, −0.30); line inside the right well margin | bottom |
| | en_3v3_b | (−0.39, −0.62; −0.18, −0.30); gate column | bottom |
| bg_svpg | vdd / vpg / en_3v3 | (0, 1.43; 1, 1.75) / (0, −0.62; 1, −0.30) / (1.30, 0.435; 1.62, 0.695) | top / bottom / right |

## Lessons added to the skill (`out/skill/`, extended, not replaced)

- **[generic] G17–G24:**
  - short-L stacks without bands, lanes over the channels;
  - cascode rows carry their mirror's letters (joints, no join track);
  - Latin-square maps;
  - wide-tab spacing;
  - line gap for vias sharing a lane;
  - edge endcap;
  - check a PCell's own symmetry first;
  - side lines as pins.
- **[generic] Generator:** `cascode_stack`, `series_row(gate_pin, end_pin)`, `lu_context.py` for any cell and side
  set.
- **[IHP] I27–I31:** the geometry numbers, the asymmetric 10/1 PCell, the first DRC fixes, the LU numbers and
  bg_ms1's bottom pins.
