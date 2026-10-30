| generic name | value | source |
|---|---:|---|
| `grid` | 0.005 | sg13cmos5l_tech_default.json grid = 0.005 (drawing grid (geometry/3_1_offgrid.drc)) |
| `diff_width` | 0.15 | sg13cmos5l_tech_default.json Act_a = 0.15 (Min. Activ width) |
| `diff_space` | 0.21 | sg13cmos5l_tech_default.json Act_b = 0.21 (Min. Activ space) |
| `finger_gap` | 0.25 | sg13cmos5l_tech_default.json Gat_b1 = 0.25 (Min. space between unrelated 3.3 V GatPoly over Activ; with end caps Gat_c the poly merges into one gate strip) |
| `gate_len_min` | 0.4 | sg13cmos5l_tech_default.json Gat_a4 = 0.4 (Min. GatPoly width = channel length, 3.3 V PFET) |
| `poly_endcap` | 0.18 | sg13cmos5l_tech_default.json Gat_c = 0.18 (Min. GatPoly extension over Activ (end cap)) |
| `poly_to_diff` | 0.07 | sg13cmos5l_tech_default.json Gat_d = 0.07 (Min. GatPoly (field) space to Activ) |
| `contact_size` | 0.16 | sg13cmos5l_tech_default.json Cnt_a = 0.16 (Cont size) |
| `contact_space` | 0.18 | sg13cmos5l_tech_default.json Cnt_b = 0.18 (Min. Cont space) |
| `diff_encl_contact` | 0.07 | sg13cmos5l_tech_default.json Cnt_c = 0.07 (Min. Activ enclosure of Cont) |
| `poly_encl_contact` | 0.07 | sg13cmos5l_tech_default.json Cnt_d = 0.07 (Min. GatPoly enclosure of Cont) |
| `poly_contact_to_diff` | 0.14 | sg13cmos5l_tech_default.json Cnt_e = 0.14 (Min. Cont on GatPoly space to Activ) |
| `diff_contact_to_gate` | 0.11 | sg13cmos5l_tech_default.json Cnt_f = 0.11 (Min. Cont on Activ space to GatPoly) |
| `m1_width` | 0.16 | sg13cmos5l_tech_default.json M1_a = 0.16 (Min. Metal1 width) |
| `m1_space` | 0.18 | sg13cmos5l_tech_default.json M1_b = 0.18 (Min. Metal1 space) |
| `m1_encl_contact` | 0 | sg13cmos5l_tech_default.json M1_c = 0 (Min. Metal1 enclosure of Cont) |
| `m1_endcap_contact` | 0.05 | sg13cmos5l_tech_default.json M1_c1 = 0.05 (Min. Metal1 endcap enclosure of Cont) |
| `m1_area` | 0.09 | sg13cmos5l_tech_default.json M1_d = 0.09 (Min. Metal1 area (um2)) |
| `m1_wide_space` | 0.22 | sg13cmos5l_tech_default.json M1_e = 0.22 (Min. Metal1 space next to Metal1 wider than M1_e_w, parallel run > M1_e_cr) |
| `via1_size` | 0.19 | sg13cmos5l_tech_default.json V1_a = 0.19 (Via1 size) |
| `via1_space` | 0.22 | sg13cmos5l_tech_default.json V1_b = 0.22 (Min. Via1 space) |
| `m1_encl_via1` | 0.01 | sg13cmos5l_tech_default.json V1_c = 0.01 (Min. Metal1 enclosure of Via1) |
| `m1_endcap_via1` | 0.05 | sg13cmos5l_tech_default.json V1_c1 = 0.05 (Min. Metal1 endcap enclosure of Via1) |
| `m2_width` | 0.2 | sg13cmos5l_tech_default.json Mn_a = 0.2 (Min. Metal2 width) |
| `m2_space` | 0.21 | sg13cmos5l_tech_default.json Mn_b = 0.21 (Min. Metal2 space) |
| `m2_encl_via1` | 0.005 | sg13cmos5l_tech_default.json Mn_c = 0.005 (Min. Metal2 enclosure of Via1) |
| `m2_endcap_via1` | 0.05 | ihp_sg13cmos5l literal 0.05: sg13cmos5l_maximal.drc rule text M2.c1 'Min. Metal2 endcap enclosure of Via1 = 0.05' (no json key) |
| `well_width` | 0.62 | sg13cmos5l_tech_default.json NW_a = 0.62 (Min. NWell width) |
| `well_space_same` | 0.62 | sg13cmos5l_tech_default.json NW_b = 0.62 (Min. NWell space or notch, same net (merged below this)) |
| `well_space_diff` | 1.8 | sg13cmos5l_tech_default.json NW_b1 = 1.8 (Min. PWell width between NWell regions, different nets) |
| `well_encl_pdiff` | 0.62 | sg13cmos5l_tech_default.json NW_c1 = 0.62 (Min. NWell enclosure of P+Activ inside ThickGateOx) |
| `well_encl_tap` | 0.62 | sg13cmos5l_tech_default.json NW_e1 = 0.62 (Min. NWell enclosure of an NWell tie in N+Activ inside ThickGateOx) |
| `well_to_ndiff` | 0.62 | sg13cmos5l_tech_default.json NW_d1 = 0.62 (Min. NWell space to external N+Activ inside ThickGateOx) |
| `pimp_encl_pdiff` | 0.18 | sg13cmos5l_tech_default.json pSD_c = 0.18 (Min. pSD enclosure of P+Activ in NWell) |
| `pimp_encl_gate` | 0.4 | sg13cmos5l_tech_default.json pSD_i1 = 0.4 (Min. pSD enclosure of PFET gate inside ThickGateOx) |
| `pimp_to_ntap` | 0.03 | sg13cmos5l_tech_default.json pSD_d1 = 0.03 (Min. pSD space to N+Activ in NWell) |
| `hvox_encl_diff` | 0.27 | sg13cmos5l_tech_default.json TGO_a = 0.27 (Min. ThickGateOx extension over Activ) |
| `hvox_encl_gate` | 0.34 | sg13cmos5l_tech_default.json TGO_c = 0.34 (Min. ThickGateOx extension over GatPoly over Activ) |
| `hvox_space` | 0.86 | sg13cmos5l_tech_default.json TGO_e = 0.86 (Min. ThickGateOx space (merged below this)) |
| `lu_tap_dist` | 20 | sg13cmos5l_tech_default.json LU_a = 20 (sg13cmos5l_maximal.drc LU.a: Max. space from any portion of P+Activ inside NWell to an nSD-NWell tie (grown inside NWell)) |
| `lu_tap_cont_ext` | 6 | sg13cmos5l_tech_default.json LU_d = 6 (sg13cmos5l_maximal.drc LU.d: Max. extension of NWell tie Activ beyond Cont) |

| layer | GDS | source |
|---|---|---|
| `diff` | 1/0 | sg13cmos5l_maximal.drc:1455 Activ |
| `poly` | 5/0 | sg13cmos5l_maximal.drc:1460 GatPoly |
| `poly_pin` | 5/2 | sg13cmos5l_maximal.drc:1461 GatPoly_pin (drawn by the PCell) |
| `contact` | 6/0 | sg13cmos5l_maximal.drc:1464 Cont |
| `m1` | 8/0 | sg13cmos5l_maximal.drc:1467 Metal1 |
| `m1_pin` | 8/2 | sg13cmos5l_maximal.drc:1468 Metal1_pin |
| `m1_text` | 8/25 | Metal1 text: the library's pin convention (pad_buffer_cells.gds); LVS labels |
| `m2` | 10/0 | sg13cmos5l_maximal.drc:1473 Metal2 |
| `m2_pin` | 10/2 | sg13cmos5l_maximal.drc:1474 Metal2_pin |
| `m2_text` | 10/25 | Metal2 text: as m1_text |
| `pimp` | 14/0 | sg13cmos5l_maximal.drc:1478 pSD |
| `via1` | 19/0 | sg13cmos5l_maximal.drc:1480 Via1 |
| `well` | 31/0 | sg13cmos5l_maximal.drc:1490 NWell |
| `hvox` | 44/0 | sg13cmos5l_maximal.drc:1498 ThickGateOx |
| `heat` | 51/0 | drawn by the pmosHV PCell (thermal marker); not read by the DRC deck |
| `text` | 63/0 | sg13cmos5l_maximal.drc:1508 TEXT (device tags) |
