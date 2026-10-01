---
name: "xschem-analog-schematic"
description: "Draw or tidy xschem .sch schematics from a SPICE netlist (IHP sg13g2/sg13cmos5l symbols) in readable analog style, verified by netlisting back and comparing device by device."
---

# xschem-analog-schematic

Use this skill when the deliverable is an **xschem schematic** (`.sch` / `.sym`), not a figure.
For SVG/PNG figures in reports, use `analog-schematic` instead.

The netlist is the source of truth. The schematic is derived from it, and it is not done until
xschem's own netlist of it matches the source **device by device**. A schematic that looks right
proves nothing: in the first session that used this skill, two bulk stubs touched and xschem
silently merged `vss` into `vdd`, and a hand edit moved two gates from `vbn` to `vss`. Only the
round-trip comparison caught them.

## Workflow

1. **Parse the source subcircuit.** Use the `.subckt` port order, and for each device: model,
   terminal nets in SPICE order, and w / l / ng / m / value. Replace `{param}` expressions by
   their defaults; xschem schematics here carry plain values.
2. **Plan the placement** using the style rules below: rows, columns, mirror pairs, rails. Write
   it as a `name: (x, y, rot, flip)` table before writing any file.
3. **Write the `.sch`**, with real orthogonal wires for every net that has a short route, and a
   `lab_pin` only where a wire would cross more than half the sheet.
4. **Write the `.sym`.** Its pin order must equal the `.subckt` port order.
5. **Netlist with xschem and compare** (see Verification). Fix every mismatch before delivering.
6. **Render and look.** Use `xschem -q -x --svg --plotfile f.svg f.sch`, convert it to PNG
   (cairosvg), and open the PNG. Check that no labels overlap, rails are continuous and stacks are
   straight. Do not copy the images into the user's folders: files that pass through the app get a
   provenance stamp. Show them in the conversation only if asked.

A first pass that puts a net label on every terminal (stub plus `lab_pin`) is acceptable as a
quick, connectivity-exact draft. Say that it is a draft. The finished style below uses wires.

## Style (from Christoph Maier's hand-drawn d2s_miller / d2s_loadcomp, 2026-10-01)

**Sheet structure**
- Signal flows **left to right**: inputs on the left, output on the right edge.
- **All ports in one column at the far left** (x ≈ 60), ordered top to bottom by where they are
  used. `vdd` sits at the top, `vss` at the bottom, and each bias or input pin at the height of the
  row it feeds, so that its wire runs straight across. The output `iopin` sits on the **right
  edge**, at mid-height between the output devices.
- **Rails are wires, not labels.** `vdd` is one horizontal bus across the full width at the top,
  `vss` one bus across the bottom. Every source and bulk that goes to a rail is wired to it.

**Rows (y), all devices upright (rot 0)**
- PMOS current sources and mirror tops sit in one row just under `vdd`.
- PMOS cascodes go in the next row, then the signal row (input pairs, floating class-AB pair).
- NMOS cascodes are in a row above the NMOS sinks; the sinks sit just above `vss`.
- Row pitch is 160–240 units. Leave horizontal routing channels between rows for long nets, such
  as the pair drains running to the folding nodes.

**Columns (x)**
- Each current branch forms **one vertical column**, rail to rail: for example, the mirror PMOS,
  its cascode, the floating pair, the NMOS cascode and the sink all share one x.
- **Differential pairs and mirrors are mirror images.** The left device is unflipped and the right
  one flipped (or the reverse), so that gates face outward for input pairs and inward for tails
  and mirrors that share a gate trunk. Pair spacing is about 220 units.
- Tail current sources sit directly above their input devices, about 40 units inside them.
- The output devices are in the rightmost column, PMOS at the top (on `vdd`) and NMOS at the
  bottom (on `vss`), with `vout` as a vertical trunk between them.

**Two-terminal devices**
- Degeneration resistors are horizontal (`rhigh` rot 3), between the two sources of a pair.
- Compensation capacitors are horizontal (`cap_cmomi` rot 1), between the `vout` trunk and the
  node they compensate.

**Wiring**
- Orthogonal only, every coordinate on the 10-unit grid, no diagonals.
- Crossings without a dot are not connections; xschem draws the dots at T-junctions.
- Bulks are wired to their source or rail, never left to a label alone. Even inside a branch, the
  PMOS bulk goes to `vdd` and the NMOS bulk to `vss`, unless the source netlist ties it elsewhere.

**What to avoid** (each of these was seen)
- Net-label soup: one label per terminal, with names colliding ("vbpvbp", "vddvss").
- Bulk or gate stubs from neighbouring devices that touch. xschem joins touching wire ends and
  labels, which merges nets **silently**.
- Leftover labels under a hand-drawn wire. They are harmless only while they agree with the wire;
  once someone edits the wire, they keep the old connection alive.

## Geometry facts (xschem 3.4, IHP symbols)

Library references: `sg13cmos5l_pr/<sym>.sym` (also resolves via `sg13g2_pr/`), and
`devices/{lab_pin,ipin,opin,iopin,isource,title}.sym`.

Pin offsets in symbol coordinates (y points down):

| symbol | pins |
|---|---|
| `sg13_hv_nmos` / `sg13_lv_nmos` | D (20,−30), G (−20,0), S (20,30), B (20,0) |
| `sg13_hv_pmos` / `sg13_lv_pmos` | S (20,−30), G (−20,0), D (20,30), B (20,0) |
| `rhigh`, `rppd`, `rsil` | P (0,−30), M (0,30); the substrate is the **`body=` attribute** (PDK default `sub!`), not a pin |
| `cap_cmomi`, `cap_cmomf` | c0 (0,−30), c1 (0,30) |
| `isource` | p (0,−30), m (0,30); current flows p → m inside the source, as in SPICE `I p m` |
| `lab_pin`, `ipin`, `opin`, `iopin` | (0,0); `lab_pin` text sits left of the pin, `flip=1` puts it right |

Instance placement is `C {sym} x y rot flip {props}`. **Flip negates x** in symbol coordinates.
Rotation, for a pin offset (x, y): rot 1 → (−y, x), rot 2 → (−x, −y), rot 3 → (y, −x).
These rules were checked against hand-drawn files for rot 0/1/3 and for flip on MOS devices.

MOS instance properties follow the PDK template:
`name= l= w= ng= m= mm_ok=1 model=sg13_hv_nmos spiceprefix=X`.

Wires are `N x1 y1 x2 y2 {lab=net}`; the `lab` on a wire is only a hint, and connectivity comes
from geometry.

## Verification

- Netlist each schematic with xschem in batch mode:
  `xschem --rcfile <dir>/xschemrc -n -s -q -x -o <dir>/net <dir>/<cell>.sch`
  - Use **absolute paths and set `PWD`** in the subprocess environment. xschem resolves relative
    names against `$PWD`, not against the working directory of the process. A wrong `PWD`
    silently netlists an empty schematic.
  - **Delete the old netlist first**, so that a failed run cannot be compared as if it were fresh.
  - **Don't treat the exit status as pass/fail.** xschem 3.4.8 has returned 10 while writing a
    complete netlist. Print the status and xschem's messages, then compare whatever was written.
- Parse xschem's netlist (`X…`/`I…` lines; the `**.subckt` header gives the port order). Compare
  per device: model, terminal nets **in order**, w/l/ng/value, and the port order. Report every
  difference and exit non-zero if there is any.
- Sanity-check the checker once by changing one label in a copy and confirming that it fails.
- Port order: in hierarchical use, xschem takes the port order from the **`.sym`**, for both
  the instance line and the `.subckt` definition it writes. The order of pin instances in the
  `.sch` is ignored there. This was checked with xschem 3.4.4: a parent schematic was netlisted
  with the child's pins in two different `.sch` orders, and the result was identical. The `.sch`
  order matters only when the schematic is netlisted **stand-alone** as the top level; then
  xschem orders the `**.subckt` header by the order of the pin instances in the file. Deleting
  and re-placing a pin, or cut-and-paste, moves it to the end or the front. Keep the `.sym`
  equal to the source netlist (it is what parents use), and keep the `.sch` in the same order so
  that stand-alone netlists stay usable.

Reference implementations: `gen_xschem.py` (label-draft generator) and `check_xschem.py`
(round-trip comparison) in
`sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/class_ab_pad_driver/`.

## Environment notes

- `PDK_ROOT` and `PDK=ihp-sg13cmos5l` must be set. A minimal `xschemrc` that sources
  `$PDK_ROOT/$PDK/libs.tech/xschem/xschemrc` and appends its own directory is enough.
- In a cloud container without the user's toolchain: `apt-get install xschem` works (3.4.4),
  and the PDK's `libs.tech/xschem` can be sparse-cloned from IHP-Open-PDK (`dev` branch for
  sg13cmos5l). Rendering and netlisting work headless with `-q -x`.