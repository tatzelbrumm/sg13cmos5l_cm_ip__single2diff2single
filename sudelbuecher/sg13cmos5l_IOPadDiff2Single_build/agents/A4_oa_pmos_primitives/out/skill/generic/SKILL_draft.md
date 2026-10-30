---
name: compact-mos-primitives
description: Process-agnostic skill for compact analog MOS layout primitives (current-mirror stacks, mirror + cascode stacks, series chains, single switches). Turns a pattern score into a cell through a process adapter. Covers tap-less cells in one merged well, minimum-width end dummies, point-symmetric drain-band stacks, a latch-up check against the parent's tap segments, and porting to another PDK. Use with an adapter such as ../ihp_sg13cmos5l/.
---

# Compact MOS primitives (process-agnostic) [generic]

2026-10-28, Claude (Opus 5.5). This skill is drawn from `oa_pmir_c`, `oa_ms1`, `oa_svpg` (OA core) and from
`bg_pmir_pcas_c`, `bg_ms1`, `bg_svpg` (bandgap core). Their numbers are IHP
sg13cmos5l values and live in `../ihp_sg13cmos5l/`. Nothing in this folder depends on a process: rule values, layers
and devices come from the adapter.

## When to use

- A block of equal fingers must match: a mirror with ratio weights, sinks, loads. Use the **stack**.
- A mirror with its cascodes, short L (row height close to a band height). Use the **cstack** (G17–G19).
- A long-L device must be split into series fingers. Use the **chain**.
- A single switch. Use the **single**.
- The block should be minimum area. Its well merges with its neighbours, and the parent places the taps.
- Not covered: in-line stacks (mirror + cascode sharing one diffusion), resistor arrays, bipolars. The rules
  G1 ... G24 still apply.

## Procedure

1. **Adapter.** Pick or write `<pdk>/adapter.py` (see "Porting" below). Run its device self-test: the drawn device
   must XOR 0 against the PDK's PCell for several W / L values.
2. **Score.** Write the block as a score (`patterns.md`, notation section):
   - voices = devices / drain nets;
   - rows = letters, with a rest `d` (W `min`) at each row end;
   - tracks from the centre line outwards, the gate net last;
   - `symmetry R180 swap a b` if one matched device has no partner.
   `parse_scores()` + `point_image()` check the symmetry before drawing.
3. **Build.** `G.build(ly, P, score, cells)` returns the cell, the device list and info. Pass library PCell copies
   as `cells` where they exist; the adapter draws the rest. `G.cdl()` writes the reference netlist with the same
   device list. The well is a floating internal net (`bulk nw`) in a tap-less cell.
4. **Verify in the PDK.**
   - DRC: the target deck. Remaining errors must be latch-up only (no tap in the cell).
   - LVS: against the `.cdl`.
   - `check.py sym`: device layers XOR 0 with the R180 image; report the metal XOR as information.
   - `check.py pins`: every pin on an edge.
5. **Latch-up with the parent's taps.** Choose the tap segments the parent will draw (`tap_path`, one contact column,
   following the outline). Compute the farthest P diffusion (`check.py lu`), find the minimum segment length,
   build a context cell (cell + segments) and run the PDK's DRC on it. Report the numbers per segment.
6. **Pictures** (`render.py`): a tile with letters, tracks, taps, pins and scale bar; before / after at the same
   scale; the rule behind each saving.
7. **Backannotation.** List every W / L / finger / series change against the schematic and its electrical effect.

## Pattern notation

See `patterns.md`:
- translation = repetition (an AREF);
- mirror = retrogradation;
- point symmetry = retrograde inversion (`symmetry R180`);
- interdigitation = alternation (hocket);
- the end dummy = the rest that closes a phrase (`d`, `drain=rest`).

Voices are the devices, and their lanes are the Metal2 tracks of a band.

## Pictures

- `pictures/tile_stack.png`: the stack pattern with letters, bands, staircase, gate columns, the supply spine and
  the parent's tap segments. Instance: IHP sg13cmos5l.
- `pictures/tile_chain.png`: chain and single.
- `pictures/tile_cstack.png`: the mirror + cascode stack (lanes over the channels, joints, side lines).
- Before / after and the rule-driven savings with values: `../ihp_sg13cmos5l/pictures/`.

## Generators and tools (all adapter-driven)

- `generator.py`:
  - `parse_scores`, `point_image`, `build`;
  - `mirror_stack`, `cascode_stack`, `series_row` (pin options `gate_pin` / `end_pin`), `switch_cell`;
  - `tap_path` (for the parent), `well_polygon`, `cdl`, `load_adapter`, `min_contact_width`.
- `check.py`: `sym`, `lu`, `pins`. These are geometric checks; they do not replace the PDK's DRC / LVS.
- `render.py`: draws cells from GDS.
- `example_build.py <adapter.py> <out>`: builds every score of `patterns.md`. For IHP sg13cmos5l the result XORs 0
  against the delivered cells.

## Rules and pitfalls

See `rules.md` (G1 ... G24, all [generic]). The most important:
- no tap between rows (G3);
- one merged well per net (G4);
- tap segments only where latch-up needs them, following the outline (G5, G6);
- unmodified device cells (G8);
- one-contact rests (G1);
- full-size symmetry partners (G2);
- for short L: no bands, lanes over the channels, Latin-square maps (G17–G19).

## Porting to another process

Write one adapter file with the same names as `../ihp_sg13cmos5l/adapter.py`. For each field:

| adapter field | where to find it in a new PDK | how to verify |
|---|---|---|
| `LAYERS` (generic name -> GDS layer / datatype) | the DRC deck's layer definitions (`source.polygons("L/D")` or equivalent), the layer map of the tech file | draw one cell, run the PDK's DRC: no "unknown layer"; LVS extracts the devices |
| `RULES` (generic name -> value + source) | the DRC deck / rule json / design-rule manual: contact size / space / enclosures, poly end cap, poly-to-diffusion, metal widths / spaces / via enclosures, well enclosure / space (same and different net), implant enclosures, thick-oxide extensions, latch-up distance | the generator asserts the derived spacings. The PDK's DRC on the built cells must show nothing but latch-up |
| `WELL_45`, angle facts | the deck's angle / off-grid checks for the well layer | DRC on a cell with a chamfered well |
| `HVOX_LIKE_WELL` and similar | how the PCell draws thick oxide / implants | XOR the adapter's device against the PCell |
| `device(ly, kind, w, l)` + `DEVICES[kind]` (model name, LVS recognition, min W / L, finger limit) | the PCell source or GDS of the PDK's devices; the LVS deck's device extraction; the model card's W / L range | XOR 0 against PCell instances over a W / L sweep; LVS of a single finger |
| `TAP_COUNTS`, `lu_tap_dist` | the latch-up section of the DRC deck (which ties count, how the distance is grown) | a context cell (block + parent taps) passes the deck's latch-up rules |
| `PEX` | the PEX rule files (sheet R, capacitance per layer) | not used by these generators. Before routing long tracks, check the extracted R / C of one band |

- What does not port automatically: the pin / text layer convention of the target library, and the LVS tool's
  bulk-net handling for tap-less cells (a floating well net, or an implicit tie).
- Check both on one switch cell first.
