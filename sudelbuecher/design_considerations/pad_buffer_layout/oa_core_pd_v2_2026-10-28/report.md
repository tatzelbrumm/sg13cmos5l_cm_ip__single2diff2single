1. The compact oa_core_pd is done: 40.51 × 58.135 µm = 2355 µm², down from v1's 76.00 × 50.74 = 3856 µm² (−39 %), aspect 1.44, vdd rail top, vss rail bottom, Metal1/Metal2 only, all ports on the right edge.
2. It uses the NMOS specialist's two cells (oa_n10 with oa_mcs_c, sharing one p+ tie), the PMOS specialist's three cells (oa_pmir_c, oa_ms1, oa_svpg) and my oa_pcas_c (oa_pcas with its ring removed). All PMOS sit in one vdd NWell. No rings, no tie between array rows.
3. Checks: DRC 0 on the block (my Python subset, 72 rules, latch-up included). LVS matches against a netlist composed from the specialists' own CDLs, and also against the backannotated sheet. The build is byte-reproducible.
4. Backannotation package: the edited sheet netlists in xschem to the same 28 devices as the new subckt text. Only finger, series and dummy changes. Every ratio that sets the circuit is kept.
5. Skill export is in out/skill/, split into generic/ and ihp_sg13cmos5l/. Its example rebuilds the delivered GDS byte for byte from inside the skill folder. bg_core_pd stayed on hold; out_bg/ is empty and v1 in out/ is unchanged.

---

**Report: oa_core_pd v2, compact assembly (2026-10-28, 02:44–04:09 CET, cloud workspace only, no device tools, no git, inputs untouched)**
Tags: [generic] holds for any process, [IHP] is the sg13cmos5l instance. "Measured" means taken from the GDS or the check logs; reasoning is marked.

**What I did**
- **Assembly script:** `out/v2/generator.py` plus `configs/oa_core_pd_v2.py`. Process values come from `process/ihp_sg13cmos5l.py`, each with its json key or deck file. The steps are:
  - the floorplan is written as a short indented text (a "placement grammar");
  - gaps are found by DRC and a check for touching nets;
  - same-net wells and thick oxide are merged;
  - tie strips go under the rails where they fit, plus explicit tie segments;
  - a router on Metal1/Metal2 connects the pins, with a keep-out over the PMOS mirror;
  - the script reports area, latch-up and wire lengths, and can compose the LVS reference netlist.
- **Router test on v1:** the six unchanged v1 cells at their v1 positions, routed automatically, give DRC 0 and LVS match against v1's netlist.
- **oa_pcas_c** (`make_oa_pcas_c.py`): oa_pcas with its 4 ntap1 ring instances, its ring Metal1 and its vdd pin removed, and NWell drawn to the cell edge.
  - Measured: XOR against oa_pcas minus the ring shows nothing differing; LVS matches (bulk on an internal net nw); 183.3 → 130.7 µm². No device change.
- **Primitive edits:** none besides oa_pcas_c. The other five cells are used exactly as delivered; only orientations were chosen (oa_ms1 R90, oa_svpg M90, which made svpg's en_3v3 pin reachable).
- **Floorplan:** three stacked rows of nearly equal width (39.49 / 37.7 / 36.72 µm):
  - oa_pmir_c turned R270, its pins facing down;
  - oa_pcas_c, oa_ms1, oa_svpg;
  - the NMOS pair with its shared tie.
  - Two side-by-side alternatives measured 2519 and 2485 µm² before full routing, because they left an empty strip under the shorter column.
- **Ties:** a thick-oxide n tie under the vdd rail, only where the rail is free (NW.e1 0.62, TGO.a 0.27), plus the PMOS specialist's two 8.2 µm segments in oa_pmir_c's margins. Latch-up check: all device diffusion within 20 µm (LU.a, LU_b) [IHP].

**Area, measured (`logs/area_audit.txt`)**

| | v1 | v2 |
|---|---|---|
| Block | 3856 µm² | 2355 µm² |
| Bands inside cells (rings, enclosures, track bands) | 884 µm² (22.9 %) | 316 µm² |
| Free area | 710 µm² (18.4 %) | 232 µm² (9.9 %) |
| vdd NWells | 3 | 1 |
| Tie diffusion | 268 µm² | 36 µm² |
| Gate area / block | 31.8 % | 48.8 % |
| Device diffusion / block | 39.0 % | 61.0 % |

**Checks, measured (`run_checks.sh` runs everything from scratch in 75 s)**
- **DRC:** 0 on the block, on oa_n10 and oa_mcs_c, on the porting self-test and on both regression layouts.
  - The tap-less PMOS cells checked alone show only LU.a: oa_pmir_c 80, oa_pcas_c 18, oa_ms1 16, oa_svpg 2. That is intended; in the block, LU passes.
- **LVS:** five runs all match. They are oa_pcas_c, the two regressions, the block against the composed reference (111 devices, 28 after combining parallel fingers), and the block against the backannotated netlist.
- **Rebuild:** the GDS rebuilds to the same bytes (22ad9f9552e4), also from inside the skill folder.
- **Gap search:** shown to detect conflicts — oa_pcas_c next to oa_misc_n needs 0.350 µm, which is exactly NW.d1 0.62 minus misc_n's 0.27 edge band [IHP].

**Backannotation (`out/v2/backannotation/`)**
- **What it contains:** the sheet copy `oa_core_pd.sch`, the subckt text for bias_ref_pd.spice, `device_changes.txt`, the xschem netlist of the new sheet and the LVS form. Topology comes from the sheet and sizes from the layout; any topology difference stops the script.
- **Device changes:**
  - M10 ng 8 → 18 and M11 ng 4 → 9 (W and L unchanged).
  - MS1 becomes 8 × 0.5/12.5 in series (as in v1).
  - Dummies, with D = S = bulk:
    - PMOS 4.4/8 (8 × 0.3 + one 2/8) on vpg: 35.2 µm² of gate, was 144;
    - NMOS 36/1 on vnc: 36 µm², was 10;
    - NMOS 4/1 on vbr: new.
  - [reasoning] The dummies only change gate capacitance on vpg/vnc/vbr; not simulated.
- **Ratios:** M10:M11 = 2:1; PO:P8:P2:P0 and POC:P8C:P2C:P0C = 20:8:2:1; MCS:MCL = 1:1. All kept.
- **Ports:** unchanged, so no .sym change.

**Lessons for bg_core_pd**
- [generic] The area went, in order:
  - rings and the bands they enclose (884 µm²);
  - empty bays around islands (209 + 190 + 124 µm²);
  - three separate vdd wells (their PMOS ring bands were 572 µm², now 185 µm²);
  - a tie row between array rows (31.3 × 0.78 µm in oa_nmir);
  - full-size dummies.
- [generic] Floorplan rules that worked:
  - rows of equal width;
  - one well per supply;
  - each cell's pin edge facing its partner;
  - the matched array in its own row with a keep-out;
  - ports on one edge.
- [generic] Gap search by DRC alone misses shorts, because touching metal of two nets merges silently. My generator adds a label check per trial and one on the full placement.
- [IHP] For bg: bg_pmir_pcas without its ring, in the vdd well with bg_misc_p's cells. The NMOS specialist estimates bg_nab at about 16 × 20 µm with interdigitated rows. Ties go in the rails.
- Rules (I1–I13) and pitfalls (P1–P18, I20–I25) are in the two `rules.md` files.

**Deviations and decisions for you**
- **Ports moved:** iout and en_3v3 now sit on the right edge (v1 had them on top), so that nothing crosses the PMOS mirror. Say if the top edge is required.
- **Width cost of the pmir_c ties:** they push the well 0.51 µm past both sides, adding 1.02 µm of width (≈59 µm²).
- **Rail heights:** kept at 1.50 / 1.42 µm. A thinner vss rail would save about 33 µm² [reasoning], but it breaks the abutment convention.
- **DRC tool:** DRC is my Python subset, not IHP's own deck, which cannot run here.
- **Location:** the "updated sheet copy in out/" is in `out/v2/backannotation/`.

**Worth remembering**
- The assembly script is `out/v2/generator.py`; the IHP process values are in `out/v2/process/ihp_sg13cmos5l.py`.
- xschem netlisting uses the PDK copy at `scratchpad/ext/pdk_a49358c`, read only, through `work_v2/xs/xschemrc`.

**Files** (sha256, first 12 hex), all in /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent/out/:
```
22ad9f9552e4 v2/oa_core_pd.gds            85ab643d2bf6 v2/oa_core_pd_ref.cdl
02c18b6e7c8e v2/oa_pcas_c.gds             607b9345bd0c v2/oa_pcas_c.cdl
82b0bbf0f49d v2/make_oa_pcas_c.py         65d8c10da96e v2/configs/oa_core_pd_v2.py
cea21b865695 v2/generator.py              db37b9a7f3d1 v2/process/ihp_sg13cmos5l.py
f638e9434740 v2/backannotate.py           797fd925b983 v2/area_audit.py
16445525a27c v2/render_block.py           517c41d0ee74 v2/drc.py
a4694db5b833 v2/lvs.py                    df977416ff33 v2/run_checks.sh
820cf1df6af7 v2/configs/regress_merged_well.py   b88be8d7c6b4 v2/configs/regress_v1cells.py
05e30183e707 v2/backannotation/oa_core_pd.sch    dcf636300029 v2/backannotation/oa_core_pd_subckt.spice
0c0a4f134833 v2/backannotation/device_changes.txt 26a6e16b90dc v2/backannotation/oa_core_pd_xschem.spice
9725cbd0bf8a v2/backannotation/oa_core_pd_backannotated.cdl
ea3b06455f9a v2/oa_core_pd.png            b77e0c8219e6 v2/v1_vs_v2.png   c97ce84d9268 v2/rule_savings.png
c2936cfd9bfc v2/logs/drc_oa_core_pd.txt   fffbf2c75b77 v2/logs/lvs_vs_ref.txt   6d71fca49c75 v2/logs/lvs_vs_backannotated.txt
8c47023c566e v2/logs/area_audit.txt       b4980c93f7f2 v2/logs/build.txt (other logs in v2/logs/)
3fa4a4d5c163 skill/generic/SKILL_draft.md 99e7777b11d2 skill/generic/patterns.md  5c6d71a4d038 skill/generic/rules.md
cea21b865695 skill/generic/generator.py   f638e9434740 skill/generic/backannotate.py b61dfb85f455 skill/generic/adapter_template.py
797fd925b983 skill/generic/area_audit.py  16445525a27c skill/generic/render_block.py f89e09b20cea skill/generic/score_picture.py
ab4a96333664 skill/generic/pictures/score_compact.png   ab0e4b09593f skill/generic/pictures/score_v1.png
b38e03c69b72 skill/ihp_sg13cmos5l/SKILL_draft.md        98abfcdf7d57 skill/ihp_sg13cmos5l/rules.md
db37b9a7f3d1 skill/ihp_sg13cmos5l/adapter.py            517c41d0ee74 skill/ihp_sg13cmos5l/tools/drc.py
a4694db5b833 skill/ihp_sg13cmos5l/tools/lvs.py          1286d8a7be3b skill/ihp_sg13cmos5l/examples/oa_core_pd_v2.py
82b0bbf0f49d skill/ihp_sg13cmos5l/examples/make_oa_pcas_c.py  (+ copies of oa_p_cells / oa_n_cells / oa_pcas_c .gds/.cdl)
ea3b06455f9a skill/ihp_sg13cmos5l/pictures/oa_core_pd.png  b77e0c8219e6 .../v1_vs_v2.png  c97ce84d9268 .../rule_savings.png
```
