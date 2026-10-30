---
name: compact-mos-primitives-ihp-sg13cmos5l
description: IHP sg13cmos5l-specific companion to ../generic/ (compact MOS primitives; OA and bandgap cores). Holds the process adapter (every DRC value with its json key, the layer map, a pmosHV PCell reproduction verified XOR 0), plus what goes beyond numbers. That covers HV PMOS / ThickGateOx / NWell behaviour, LU.a as the deck computes it, the deck files missing from the uploaded copy and the Python DRC / LVS workaround, the library's pin and text conventions, and the pitfalls hit on oa_pmir_c, oa_ms1 and oa_svpg.
---

# Compact MOS primitives in IHP sg13cmos5l [IHP]

2026-10-28, Claude (Opus 5.5). The procedure is in `../generic/SKILL_draft.md`; this folder makes it concrete for
sg13cmos5l. Everything here is **[IHP]**.

## Files

| file | what |
|---|---|
| `adapter.py` | the process adapter. 16 layers (deck lines), 41 rule values (json keys or deck text), the `pmos_hv` device (PCell construction), LVS recognition, model / PEX facts, `table()` |
| `rules.md` | I1 ... I16 = the IHP values of G1 ... G16; I17 ... I26 = IHP-only lessons and pitfalls; I27 ... I31 = the bandgap stack (G17 ... G24) |
| `lu_context.py` | `<gds> <cell> T,B,L,R`: latch-up with the parent's tap segments for any tap-less cell; minimum segment lengths, context cell, DRC rules |
| `make_pictures.py` | renders `pictures/` and `../generic/pictures/` from `examples/` |
| `pictures/before_after.png` | old library cells vs new, same scale |
| `pictures/rule_savings.png` | top-left corner old vs new, each saving with its json key and value |
| `pictures/before_after_bg.png` | bandgap PMOS cells old vs new, same scale |
| `examples/` | `oa_p_cells.gds` / `.cdl`, `bg_p_cells.gds` / `.cdl` (the delivered cells), `before_cells.gds` and `before_bg_cells.gds` (library cells), `lu_context.gds` |
| `tools/` | the Python DRC subset and extraction LVS, unchanged from the v1 assembly (IHP-only) |

## Use

```
python3 ../generic/example_build.py adapter.py /tmp/oa          # cells from the scores, devices from the adapter
python3 tools/oa_core_pd_drc.py /tmp/oa.gds oa_pmir_c           # Python DRC subset (LU.a only, as intended)
python3 tools/oa_core_pd_lvs.py /tmp/oa.gds oa_pmir_c /tmp/oa.cdl oa_pmir_c
python3 ../generic/check.py sym /tmp/oa.gds oa_pmir_c adapter.py
python3 lu_context.py examples/oa_p_cells.gds oa_pmir_c T,B     # parent tap segments, LU numbers
```

With KLayout >= 0.30.2 and Ruby (IIC-OSIC-TOOLS), run IHP's own `run_drc.py` / `run_lvs.py --disable_tap_extraction`
instead of `tools/`.

## IHP know-how

- **Devices.**
  - pmosHV is a single-finger PCell: S/D contact columns at Cnt_c from the ends, the gate Cnt_f from them; pSD
    pSD_c around Activ and pSD_i1 (0.40) around the gate in W; NWell and ThickGateOx both 0.62 around Activ.
  - The library's cells are copies of it, and the adapter redraws it exactly. Contact positions are floored to
    5 nm (I23).
  - The narrowest finger with an S/D contact is 0.30: that is the rest's width (I1).
- **HV specifics.**
  - ThickGateOx must cover every 3.3 V gate (TGO_c 0.34) and Activ (TGO_a 0.27), and two TGO regions merge below
    0.86 (TGO_e).
  - Because the PCell already draws TGO 0.62 out, a tap inside TGO costs nothing extra (I17).
  - NW_c1 = 0.62 sets every cell edge.
- **Latch-up.**
  - Only LU.a matters for PMOS: 20 um inside the NWell to an ntap.
  - The tap-less cells show LU.a in their own DRC; the parent's segments clear it (I5, I6).
  - LU.b (NMOS) is json-only in the upload.
- **Wells.**
  - One NWell per vdd cluster (I4).
  - The well outline may have 45° edges (I7), but square PCell corners keep full arrays rectangular.
- **Pins.** `<metal>.pin` (8/2, 10/2) + `<metal>.text` (8/25, 10/25), one per net, on the edge, Metal1 / Metal2 only
  (M3+ belong to the pad ring).
- **Deck gaps and workaround.**
  - The upload lacks several include files and the LVS deck, and the container's KLayout is too old (I21).
  - `tools/` implements 72 rules from the json plus LU.a and antenna.
  - It is not the full deck: density, fill and rules for devices not in these cells are not checked.

- **Bandgap stack.**
  - With L = 1 a 10/1 row is 1.68 high, less than a 4-track band (1.66), so lanes go over the channels (I27).
  - The library's 10/1 PCell is itself not point-symmetric in its contacts: 5 nm flooring (I28).

## Pitfalls hit here

See `rules.md`:
- I20 ... I25: the bulk net of tap-less cells in LVS, the contact rounding, the 45° sizing of straight edges, the
  parser's `drain=`, the antenna crash on a context cell;
- I29: V1.b between a pad and a line on one lane, M2.c1 at the cell edge.
