# bg_core_pd compact: A2 report (2026-10-28, 06:25 CET)

1. **Block:** 47.55 × 50.05 µm. DRC 0 on 74 rules, latch-up check included. LVS matches both the netlist built from the primitives' own netlists and the backannotated sheet.
2. **Wells and ties:** one vdd NWell holds A4's `bg_pmir_pcas_c`, `bg_ms1` and `bg_svpg`. The n ties are one in the vdd rail and one 13.1 µm segment for `bg_ms1`, which hangs below the mirror. The NMOS ties are only inside A3's `bg_n4`, and the pnp collector rings are the substrate ties. vdd is on top, vss at the bottom, ports on the right edge, Metal1 and Metal2 only.
3. **My two primitives:**
   - `bg_res_c`: the resistor array, now wired, ring removed, 515.0 → 401.1 µm² (−22 %).
   - `bg_pnp_c`: the 3 × 3 pnp array, now wired, same size.
   - Both are DRC 0 and LVS MATCH, and their device layers XOR to 0 against the library cells.
4. **Backannotation:** the only real device change is the resistors. They become chains of 18, 11 and 10 segments of 0.5 × 9.94 µm.
   - Total length changes: R0 −0.32 %, R1A +0.04 %, R1B +0.04 %.
   - Resistance changes, from the xschem symbol's value expression (each segment has its own head): R0 +0.70 %, R1A +1.03 %, R1B +1.02 %. Not simulated.
   - The ratios R1A/R0 and R1B/R0 rise by 0.32 %.
   - The library `bg_res` already had these same segments, so the deviation is not new; the sheet now carries it.
5. **Skill export:** in `out_bg/skill/`, generic/IHP split kept. New generic rules G25–G34 and pitfalls P19–P25; IHP rules I32–I41. The two IHP examples rebuild `oa_core_pd` (22ad9f9552e4) and `bg_core_pd` (c799ffb54646) byte for byte.

**A3's dummies:** `bg_n4` is the option-1 version, with all dummies tied to g on every terminal (bulk vss). The backannotated sheet lists them that way.

[m] = checked by a tool; [r] = my reasoning, not simulated. Cloud workspace only, no git; `inputs*/`, `out/`, `primN/` and `primP/` were only read.

## What "placed only" meant [m]
- **`bg_pnp`:** a 3 × 3 array of the unmodified pnp cell with shared collector rings, but no emitter or base wiring and no pins.
- **`bg_res`:** `cell_tree.md` predates the 2026-10-27 22:23–22:51 wiring. The library cell is already wired and has a p-tap ring and 0.6 µm R0 reserves.
- **`bg_res_c`:** keeps the 41 segments, the 0.68 µm pitch and the interleave, and drops the ring and the reserves. The wiring is new: chain directions are chosen so ea and eb leave at one end, e2 and vss at the other.

## Floorplan
Picture: `bg_core_pd.png`; placement score: `skill/generic/pictures/score_bandgap.png`.
```
vdd rail 1.00 (thick n tie)                         gap 0.22 (pmir's side lines reach its top edge, M1.e)
[svpg][ bg_pmir_pcas_c 45.17 x 16.15            ]   one vdd NWell
[ bg_res_c (MX, pins down)  ][ bg_ms1 (R270)  ]     ms1 hangs from pmir's well; tie segment in pmir's margin
[ bg_pnp_c ][ strip 6.3 um ] [ bg_n4 (MY)     ]     channel 1.35 um between ms1 and n4
vss rail 0.80
```
- **Width** is set by the top row: svpg + pmir = 47.55 µm. The lower part (res 28.49 + n4 18.12 = 46.61) fits under it.
- **Height** is set by the tall column: res + pnp = 31.86 µm; the MOS column is 30.14 µm [m].
- **Area audit** [m] (`logs/area_audit.txt`):
  - Free area is 249.9 µm² (10.5 %), mostly the strip beside the pnp array, which is the routing channel for ea, eb and e2.
  - Bands inside the primitives (rings, enclosures) dropped from 880.3 to 314.8 µm².
  - Tie diffusion dropped from 303.8 to 8.0 µm², plus 17.8 µm² at top level.
- **Alternatives** [r]: rotating `bg_n4` beside the pnp array, or putting `bg_ms1` in the top row, came to 2420–2700 µm² on paper. Moving svpg elsewhere would save 0.94 µm of width but make vpg run about 40 µm along the mirror.

## Per changed cell [m]
| cell (owner) | library → revised | DRC | LVS | backannotation |
|---|---|---|---|---|
| bg_pmir_pcas_c (A4) | 1064.9 → 729.5 µm² | LU.a only (96, tap-less) | MATCH (A4) | real devices unchanged; dummies 8 × 0.3/1 on vpg and on vpc |
| bg_ms1 + bg_svpg (A4) | 206.4 → 100.8 + 5.3 | LU.a only (16 / 2) | MATCH (A4) | MS1 = 8 × 0.5/12.5 in series |
| bg_n4 (A3, option 1) | 401.2 + 91.2 → 413.1 | 0 | MATCH (A3) | NA / NB 2 × 10/4 each (ng 2); dummies 16/4 + 2/1 tied to g |
| bg_res_c (A2) | 515.0 → 401.1 | 0 | MATCH | resistor chains (summary point 4) |
| bg_pnp_c (A2) | 394.3 → 394.3 | 0 | MATCH | none (Q2 m = 8, Q1 m = 1) |

The latch-up hits in the tap-less PMOS cells are expected; the block's ties resolve them, and LU.a is 0 at block level.

## Block checks [m]
- **DRC** (`logs/drc_bg_core_pd.txt`): 0 of 74 rules, antenna 0. Each placed cell (`logs/drc_cell_*.txt`) is also 0 apart from the expected LU.a in the tap-less PMOS cells.
- **LVS:**
  - Against the composed reference (`bg_core_pd.cdl`, A4's internal bulk tied to vdd): MATCH.
  - Against the backannotated netlist: MATCH, 30 devices after combining; 12 labels, no shorts, no opens.
- **Latch-up:** all device diffusion is within reach.
- **Reproducibility:** `run_checks.sh` rebuilds everything from scratch in 29 s, with byte-identical GDS for the block and both of my cells.

## Core nets and enables [m]
- **e2:** 4.32 µm on Metal2, 1 via.
- **eb:** 4.59 µm on Metal2, no via.
- **ea:** 3.50 µm Metal1 + 14.55 µm Metal2, 1 via, including its branch to Q1.
- **ea and eb** both land on n4's own Metal2 inside the cell (eb on a riser, ea on the end of a lane); the keep-outs allow each cell's own nets. They are not mirror images. The few µm of length difference at µA currents should be negligible against kΩ–MΩ resistors [r], but the PDK copy has no metal sheet resistance to confirm it.
- **iout** leaves the mirror's right edge directly.
- **en_3v3** runs 52.6 µm on Metal2 over the vdd rail; it is a static enable.
- **en_3v3_b** reaches its port through the channel between ms1 and n4. It is routed before g and vpc, which hop under it on Metal1.
- No enable crosses the resistor, pnp or NMOS arrays.

## Backannotation package (`backannotation/`, `run_backannotation.sh`) [m]
- **`bg_core_pd.sch`** is the sheet copy edited from `inputs_bg/bg_core_pd.sch`:
  - R0, R1A and R1B are replaced by chains in a side box;
  - NA and NB get ng = 2;
  - MS1 becomes a series chain;
  - the dummies are added, including 2 dummy resistor segments on vss.
- **`bg_core_pd_subckt.spice`** is the hand-netlist text, with ports in the order vdd vss iout en_3v3 en_3v3_b.
- **`device_changes.txt`** lists every change. The current ratios PO : PA : PB = 2 : 1 : 1, the cascode ratios and NA : NB are all kept.
- **`bg_core_pd_xschem.spice`**, the xschem netlist of the new sheet, has 66 devices and matches the subckt text device by device.
- **xschem pnp problem:** the supplied `inputs_bg/bg_core_pd_xschem.spice` has "?" for both pnp lines because the pnp symbol calls two Tcl helpers the PDK's xschemrc lacks. `xs/xschemrc` defines them; `xs/bg_core_pd_sheet_xschem.spice` is the original sheet netlisted that way.

## Tool changes (copies in `out_bg/`; `out/v2` untouched)
- **generator.py:**
  - the reference netlist now takes resistor, bipolar, capacitor and diode lines;
  - a new repair step widens too-narrow metal joints (one 0.035 µm sliver appeared at a pnp pad corner);
  - the minimum-area fix can also grow a pin's short side.
- **backannotate.py:** handles resistor chains and their dummies, bipolar counts (m), and writes resistors and bipolars into the LVS netlist. Rerun on the delivered `oa_core_pd`, it reproduces that package byte for byte except one wording change.
- **area_audit.py and render_block.py:** resistors and pnps now count as devices through a new adapter hook; resistor bodies are drawn; pictures can have rows.
- **tools/drc.py:** rules for the resistor's bar-shaped contacts.
- **tools/lvs.py:** recognises the resistor and the pnp with the substrate as collector.

## Lessons (full text in `skill/`)
**Carried over from the OA core:**
- no rings;
- one well per supply;
- ties in the rail plus margin segments only where latch-up needs them;
- ports on one edge;
- keep-outs over whole arrays;
- automatic DRC gaps;
- the reference netlist built from the primitives;
- backannotation from the layout.

**New generic lessons:**
- G25: revise the primitives first; the first placement already reached 85 % primitive area.
- G27/G28: wire a pnp array as one supply plane, with a Metal2 emitter frame and a gap for the centre device.
- G29/G30: wire a resistor array as chains linked at alternating head rows; the parity and direction of each chain decide which edge its pins land on.
- G31/G32: the resistor array over the pnp array forms the tall column. A small PMOS cell hanging from the PMOS row's well gets its own tie segment in that row's margin.
- G33: the strip beside the narrower array and the slack between the two columns become routing channels.
- G34: backannotate resistor chains as chains.
- P19–P25: the pitfalls hit on the way.

**New IHP lessons:**
- I32–I37: pnp geometry, the resistor body layer, 29.708 kΩ per segment from the symbol, the bar contacts, the tie segment for `bg_ms1`, and the 0.22 µm gap under the vdd rail.
- I38–I41: extraction and xschem pitfalls.

## Open points [r]
- **Resistor change not simulated.** The change comes from the symbol's value expression only. I expect branch currents about 0.7–1 % lower and a 0.3 % shift in the R1/R0 ratios, which set the temperature-coefficient balance. A simulation of the backannotated sheet would settle it.
- **pnp emitter wiring is not mirror-symmetric** because Q1 needs an exit. I estimate the extra resistance below 1 Ω at about 0.3 µA per emitter.

## Files (sha256, first 12 hex; all 101 files in `out_bg/logs/sha256.txt`)
Everything is in `/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent/out_bg/`.
```
c799ffb54646 bg_core_pd.gds               e14c60e1457e bg_core_pd.cdl
a5b2f8be48f9 bg_res_c.gds                 b36373b29a44 bg_res_c.cdl            398255350c60 build_bg_res_c.py
1b8c367b6a44 bg_pnp_c.gds                 e70344ba3df9 bg_pnp_c.cdl            cffcf03d914b build_bg_pnp_c.py
38d41da509fc configs/bg_core_pd.py        66e59828186e generator.py            1dda6eeea62a process/ihp_sg13cmos5l.py
c34539d5de5d make_bg_core_pd_ref.py       d30313ceea9e make_bg_library_set.py  a73dfb1d8326 verify_bg_cells.py
00e78a2f2826 tools/drc.py                 bb96a967a294 tools/lvs.py            e6b03f3f0f06 backannotate.py
1b767eb6b65c area_audit.py                78d3aa79ba10 render_block.py         810a404dce57 run_checks.sh
fb710c737216 run_backannotation.sh        c68285e0f412 xs/xschemrc             1a4f59a0da27 xs/bg_core_pd_sheet_xschem.spice
b22996a3148e backannotation/bg_core_pd.sch                 49dcd45b61f4 backannotation/bg_core_pd_subckt.spice
11b99141a2c1 backannotation/device_changes.txt             81d482ad8649 backannotation/bg_core_pd_xschem.spice
8ed3dbb1e13c backannotation/bg_core_pd_backannotated.cdl
4596639f66da bg_core_pd.png               2796d6504653 primitives_before_after.png   eb3e7413705b rule_savings.png
c7324ff11896 logs/drc_bg_core_pd.txt      4c8f2fdfb7cc logs/lvs_vs_ref.txt     c820eab1eaa3 logs/lvs_vs_backannotated.txt
87549d0d3a35 logs/drc_bg_res_c.txt        faf5aeed6b9a logs/lvs_bg_res_c.txt   231a3ab99a5d logs/drc_bg_pnp_c.txt
a813b67d25f0 logs/lvs_bg_pnp_c.txt        d42cf94740da logs/verify_bg_cells.txt 52d62ea2affa logs/area_audit.txt
d835ffa556c1 logs/build.txt               a68ed778a1c4 logs/backannotation.txt bdd11548d1b3 requests_for_A3_A4.md
59c09ac8cc9c skill/generic/SKILL_draft.md cd464ee4ce43 skill/generic/rules.md  a99334a1f308 skill/generic/patterns.md
c1492ed65ac0 skill/ihp_sg13cmos5l/SKILL_draft.md          969ebec6cf75 skill/ihp_sg13cmos5l/rules.md
e830f4b4c40f skill/ihp_sg13cmos5l/examples/bg_core_pd.py
```
Inputs used, read only: A3's `primN/out_bg/bg_n_cells.gds` eca26681a054 (option 1) and A4's `primP/out_bg/bg_p_cells.gds` 9b747470b752.
