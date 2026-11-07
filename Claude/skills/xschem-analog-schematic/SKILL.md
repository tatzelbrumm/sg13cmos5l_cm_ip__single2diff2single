---
name: "xschem-analog-schematic"
description: "Draw, tidy or check xschem .sch/.sym schematics and testbenches from a SPICE netlist, for any PDK (IHP, sky130, gf180, ...), in readable analog style, verified by netlisting back and comparing device by device or by topology."
---

# xschem-analog-schematic

Use this skill when the deliverable is an **xschem schematic** (`.sch` / `.sym`), not a figure.
For SVG/PNG figures in reports, use `analog-schematic` instead. Use it also to **check sheets the
user has edited by hand** (see "Hand edits and symbol changes").

The skill is **process-agnostic**. Everything that depends on a PDK (symbol names, pin positions,
parameter names, how a resistor's substrate is connected) is **read from that PDK's `.sym`
files**, never assumed. The IHP and sky130 tables at the end are worked examples, not defaults.

The netlist is the source of truth. The schematic is derived from it, and it is not done until
xschem's own netlist of it matches the source **device by device**. A schematic that looks right
proves nothing: in the first session that used this skill, two bulk stubs touched and xschem
silently merged `vss` into `vdd`, and a hand edit moved two gates from `vbn` to `vss`. Only the
round-trip comparison caught them.

## Workflow

1. **Identify the PDK and its xschem library.** Find the PDK's `xschemrc`, usually
   `$PDK_ROOT/$PDK/libs.tech/xschem/xschemrc`, and the symbol directory it adds to
   `XSCHEM_LIBRARY_PATH`. Look at an existing schematic in the user's project to see how it
   references symbols, for example `sg13g2_pr/sg13_hv_nmos.sym` or
   `sky130_fd_pr/nfet_01v8.sym`, and use the same form.
2. **Build the symbol table from the `.sym` files** (see "PDK adapter"). For every device model in
   the netlist you need: the symbol file, pin names with offsets and `@pinlist` order, the
   `template` (property names and defaults) and the `format` (how xschem writes the netlist line).
   For a PDK you haven't used before, also netlist a one-device test schematic per symbol, with a
   distinct label on every pin, and check that the terminal order is what you derived.
3. **Parse the source subcircuit.** Use the `.subckt` port order, and for each device: model,
   terminal nets in SPICE order, and its parameters. Map each terminal to a symbol pin through the
   `@pinlist` order. Replace `{param}` expressions by their defaults; the schematics carry plain
   values.
4. **Plan the placement** using the style rules below: rows, columns, mirror pairs, rails. Write
   it as a `name: (x, y, rot, flip)` table before writing any file. For a testbench, first look
   for a sibling testbench the user has already drawn and use it as the template (see
   "Testbench style").
5. **Write the `.sch`**, with real orthogonal wires for every net that has a short route, and a
   `lab_pin` only where a wire would cross more than half the sheet. A wire that crosses a few
   others without a dot is still better than a label (see "Hand-drawn refinements"). Use the
   property names from the PDK's own `template` (`w`/`l`/`ng`/`m` for IHP, `W`/`L`/`nf`/`mult`
   for sky130).
6. **Write the `.sym`.** Its pin order must equal the `.subckt` port order, and its pin names must
   equal the `ipin`/`opin`/`iopin` names in the `.sch` (see "Hand edits and symbol changes").
7. **Lint the geometry, netlist with xschem and compare** (see Verification). Fix every short and
   every mismatch before delivering, and do both again after every manual move or compaction.
8. **Render and look** (recipe under "Rendering"). Check that no labels overlap symbol text or
   each other, rails are continuous, stacks are straight and no wire stub is left dangling. Do not
   copy the images into the user's folders: files that pass through the app get a provenance
   stamp. Show them in the conversation only if asked.

A first pass that puts a net label on every terminal (stub plus `lab_pin`) is acceptable as a
quick, connectivity-exact draft. Say that it is a draft. The finished style below uses wires.

## Style (from Christoph Maier's hand-drawn d2s_miller / d2s_loadcomp, 2026-10-01)

These rules are about circuit structure, not about any one process.

**Sheet structure**
- Signal flows **left to right**: inputs on the left, output on the right edge.
- **All ports in one column at the far left** (x ≈ 60), ordered top to bottom by where they are
  used. The positive supply sits at the top, ground at the bottom, and each bias or input pin at
  the height of the row it feeds, so that its wire runs straight across. The output `iopin` sits
  on the **right edge**, at mid-height between the output devices.
- **Rails are wires, not labels.** The supply is one horizontal bus across the full width at the
  top, ground one bus across the bottom. Every source and bulk that goes to a rail is wired to it.

**Rows (y), all devices upright (rot 0)**
- PMOS current sources and mirror tops sit in one row just under the supply.
- PMOS cascodes go in the next row, then the signal row (input pairs, floating class-AB pairs).
- NMOS cascodes are in a row above the NMOS sinks; the sinks sit just above ground.
- Row pitch is 160–240 units. Leave horizontal routing channels between rows for long nets, such
  as the pair drains running to the folding nodes.

**Columns (x)**
- Each current branch forms **one vertical column**, rail to rail: for example, the mirror PMOS,
  its cascode, the floating pair, the NMOS cascode and the sink all share one x.
- **Differential pairs and mirrors are mirror images.** The left device is unflipped and the right
  one flipped (or the reverse), so that gates face outward for input pairs and inward for tails
  and mirrors that share a gate trunk. Pair spacing is about 220 units.
- Tail current sources sit directly above their input devices, about 40 units inside them.
- The output devices are in the rightmost column, PMOS at the top (on the supply) and NMOS at the
  bottom (on ground), with the output as a vertical trunk between them.

**Two-terminal devices**
- Degeneration resistors are horizontal, between the two sources of a pair.
- Compensation capacitors are horizontal, between the output trunk and the node they compensate.
- For a symbol whose pins sit at (0,−30) and (0,+30), "horizontal" means rot 1 or rot 3. Choose
  the one that puts the correct pin on the correct side (see Geometry).

**Wiring**
- Orthogonal only, every coordinate on the 10-unit grid, no diagonals.
- Crossings without a dot are not connections; xschem draws the dots at T-junctions.
- Bulks are wired to their source or rail, never left to a label alone. Even inside a branch, the
  PMOS bulk goes to the supply and the NMOS bulk to ground, unless the source netlist ties it
  elsewhere. How the bulk wire is drawn: see "Hand-drawn refinements".

**Labels** (from his hand-drawn tb_pd_enable and his label flips in the IOPadDiff2Single CACE
templates, 2026-10-25)
- `lab_pin` and `lab_wire` are always placed with rot 0. The text points **away from the wire it
  ends**: `flip=0` (text left) at the left end of a bus or on a stub that runs left, `flip=1`
  (text right) at the right end of a bus, on a stub that runs right, and on vertical stubs.
- A label stub is short (20–40 units), touches nothing but its own pin, never runs into a symbol
  body, and its text does not overlap symbol text, another label or a wire.
- When the same fix is needed in several sibling sheets ("flip them, mutatis mutandis"), find the
  labels by their role (same net, same position relative to the same instance pin), not by name,
  because label names (`lp5`, `l12`) differ between copies.

**What to avoid** (each of these was seen)
- Net-label soup: one label per terminal, with names colliding ("vbpvbp", "vddvss").
- Bulk or gate stubs from neighbouring devices that touch. xschem joins touching wire ends and
  labels, which merges nets **silently**.
- Leftover labels under a hand-drawn wire. They are harmless only while they agree with the wire;
  once someone edits the wire, they keep the old connection alive.
- A label stub that ends on another net's bus. That is the same silent merge; it happened when a
  stub from a new source's `+` pin ended on the `vss` bus just above the source row.
- **A wire along a row of pins that runs past the pin it serves.** xschem joins every pin and
  every wire end that lies anywhere on a wire. After a manual compaction (vcm_rb, b4cd2288,
  2026-11-07) the `m` wire along y = −690 into BA's gate ran on 60 units: through BA's bulk pin,
  which sits on the gate's height 40 units to the right, and onto the end of BA's bulk jog, so `m`
  merged with the OTA's tail node `bt`. The netlist only showed renamed nets. Rules: end every
  wire on its own pin; never draw a wire along a pin's height past pins of other nets (on a MOS the
  gate and the bulk share one height); after every manual move or compaction, run `sch_lint.py`
  and the netlist comparison again.
- A wire end that overshoots into a symbol body (a gate trunk ending 20 units inside the next
  device, a bulk stub starting inside its own device). Harmless while it carries the pin's own
  net, but it is how the next edit picks up a pin. `sch_lint.py -v` lists them as THROUGH.
- A device moved without its label: a `lab_pin` left on the old gate position names its net
  silently (joined by name) and its text lands on whatever is moved there next.
- Group titles and labels on top of wires (a title crossed by a drain wire, a title sitting on a
  bus). Move the title, or widen the box so the title fits inside it.

## Hand-drawn refinements (from his edits of vcm_rb / vref_s2d_rb, 2026-11-07)

He took two sheets drawn by these rules and edited them by hand (commits c84cc366 → b4cd2288 →
d0638017 in sg13cmos5l_cm_ip__single2diff2single). Each change below recurs across both sheets,
so take it as a rule.

**Leave every pin along its own lead.** Gates and bulks leave horizontally, drains and sources
vertically (for a rotated symbol, along the rotated lead), for at least one 20-unit step before
the wire turns. He re-routed every gate wire that turned straight up or down at the gate pin: the
gate now steps 20 sideways and then turns (TR: gate at x 1140, wire to 1120, then down to `vbp`).
A gate trunk between two facing gates connects to its bus from the trunk's middle, not from a pin.

**Bulks: a 20-unit stub, then a wire of its own.** Every bulk leaves its B pin by a 20-unit stub on
the bulk side and continues as a separate vertical to the rail, or to the node line of its source
when the bulk is tied to an internal source (MR's bulk to `ts`, SU's to `gh`, BA's and BB's to
`bt`). He replaced both of the other forms:
- a short wire from B to S along the symbol's own column: it hides the bulk inside the symbol;
- a 10-unit stub kept clear of the parameter text: the bulk vertical may run through the text.

Devices stacked in one column share one bulk vertical (CY over SY, TGN over TDN). The bulks of
two facing devices may be joined by one horizontal at the B height (F2 to F3 in vref_s2d_rb),
which then drops to the rail.

**All devices upright, also pass devices.** TGP of a transmission gate had been drawn upside down
(rot 2) because the netlist had D on iref. He drew it upright and swapped D and S in the source
netlist, with a comment ("a transmission gate is symmetric"). For a symmetric pass device, propose
that swap instead of rot 2.

**Placement**
- Put a device next to the line it is biased from, so the bias line is a short wire: he moved
  the fold-node replica CY / SY from the far side of the average to directly beside BNC, so `vbnc`
  became a 160-unit wire instead of a label. The signal net (`xp`) now crosses the detector column
  once; he preferred that.
- A series stack shares one column: `gh` → SU → `m` → SL1 → `xp` (SU and SL1 both flipped, same
  x); the parallel device SL2 is the mirror image beside SL1, gates facing.
- Flip a diode-connected device so that its gate faces the side where the diode node continues
  (MR and SU: gate on the right, the gate-to-drain link drops onto the node line on that side).
- A block that is "as <another cell>" is drawn as in that cell: the reference input went back to
  his bias_tree_pd drawing (TDN under TGN in one column, NI flipped under TGP, the `en_3v3_b`
  trunk dropping from the input pin to TDN's gate).
- MOS capacitors are drawn as capacitors: rot 1, gate up to the node, D / S / B down to the rail
  (CB, CB1, CB2), each under the node it holds.

**Compaction**
- Spacing is set by text, not by a pitch: he packed the groups until one device's parameter text
  ends 20–40 units before the next device's pins or wires (vcm_rb: 2840 → 2150 units wide).
- Rails hug the circuit. In vref_s2d_rb he moved the supply from −1240 to −1000 and the lines'
  PMOS row from −1140 to −900; the supply now sits 70–100 units above the topmost source pin.
- Take an output straight out of the node where it is made: `vref` runs along the source line of
  the F fingers to the pin, not down to a separate output bus.
- The title block (`title.sym`) sits right under the ground rail.

**Labels**
- Prefer a wire to a label, even across several crossings without a dot: he replaced the
  `en_3v3_b` labels at TDN and SPD by one wire that crosses nine other wires.
- Labels stay as annotation: a `lab_wire` at both ends of a long bus (`flip=0` at the left end,
  `flip=1` at the right end), a `lab_pin` at the far end of a long trunk, a `lab_wire` naming each
  internal node at a corner where it is drawn.

## Testbench style (from his hand-drawn tb_pd_enable, 2026-10-25)

- **Sources in one row at the bottom**, all upright and on one y, their `−` pins on a single GND
  bus wire across the full width, with one `gnd` symbol on it.
- **Each `+` runs straight up to its rail.** `vdd` and `vddo` are horizontal buses across the top,
  labelled at both ends. `vss` and `vsso` are short buses just above the source row, from their
  source to the instances that use them.
- **Stimulus sources** (for example `Vp`/`Vn` on the inputs) stand on the bus they are referenced
  to (`vref`), which runs horizontally under the device under test.
- **Enable** is one vertical trunk with a label at each instance pin it drives.
- **Bias lines** from a bias block to the device under test run as a staircase: from each output
  pin horizontally to its own column, then vertically to the input pin, with a `lab_wire` at each
  corner.
- **Loads** (`RL`, `CL`) sit right of the output; the output label is on the right edge.
- The **code block** is at the bottom left; the title and the explanatory notes are at the top
  left.

**Siblings are redrawn from the user's template, not drawn anew.** When the user has redrawn one
testbench of a family (enable, leak, startup, unpowered, …), carry his layout over to the others:
1. Start from his sheet. Remove the instances the sibling does not have.
2. For instances both have, take the sibling's symbol and properties but keep his position.
   Take the sibling's code block and texts, placed where his are.
3. Put each instance the sibling adds in the place of the one it replaces (state the rot/flip), or
   else in a free slot of the source row, at least 120 units from its neighbours.
4. Wherever one of his wires would now make a wrong connection, cut it at that pin.
5. **Wire the new sources in; don't leave them on labels.** Put a series source in the line it
   measures (a 0 V ammeter source between the rail and the supply pin it feeds, `+` towards the
   rail), a source that drives a node under that node with its `−` on the GND bus, and a
   source that ties two rails in the column between them. To make room, shorten buses that
   run past their last connection only to carry an end label (in tb_pd_leak/unpowered the `vref`
   bus ran on to the right edge after its load was gone). Labels are the fallback where no
   wire fits; name an unlabelled new net with a `lab_wire` on its wire.
6. Trim wire ends that your edit left dangling back to their last attachment. Leave his own
   overshoots alone: a wire end that already dangled in his sheet stays.
7. Verify by topology against the sibling as it was (see Verification), then render and look.
   Report any intended difference (for example a source return he moved from GND to `vss`) as
   carried over, not as fixed.

## Geometry (xschem 3.4; holds for every PDK)

- Instance placement is `C {sym} x y rot flip {props}`, and the pin position is
  `(x, y) + T(pin offset)`.
- **Flip negates x** of the pin offset in symbol coordinates (y points down). Then rotation,
  for an offset (x, y): rot 1 → (−y, x), rot 2 → (−x, −y), rot 3 → (y, −x).
  These rules were checked against hand-drawn files for rot 0/1/3 and for flip on MOS devices.
- Wires are `N x1 y1 x2 y2 {lab=net}`. The `lab` on a wire is only a hint; connectivity comes
  from geometry. Any wire end or pin that touches another joins the nets.
- **A pin connects anywhere along a wire**, not only at its ends. Hand-drawn wires often run
  past the pin they serve (a supply wire from the rail to y = −70 for a pin at y = −80). Never
  delete such a wire because one end dangles; count everything that lies on it.
- Generic symbols come from xschem's own `devices/` library and are the same for every PDK:
  `lab_pin`, `ipin`, `opin`, `iopin` (pin at (0,0); `lab_pin` text sits left of the pin,
  `flip=1` puts it right), `isource` (p (0,−30), m (0,30); current flows p → m inside the
  source, as in SPICE `I p m`), and `title`.

## PDK adapter: read the symbols, don't assume them

For each symbol you use, parse the `.sym` file:

```python
import re
def sym_info(path):
    s = open(path).read()
    k = re.search(r'^K \{(.*?)\n\}', s, re.M | re.S) or re.search(r'^K \{(.*?)\}', s, re.M | re.S)
    kb = k.group(1) if k else ''
    typ = re.search(r'type=(\S+)', kb)
    fmt = re.search(r'\bformat="([^"]*)"', kb)
    tpl = re.search(r'\btemplate="([^"]*)"', kb)
    pins = []
    for m in re.finditer(r'^B 5 ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) \{([^}]*)\}', s, re.M):
        x1, y1, x2, y2 = map(float, m.group(1, 2, 3, 4))
        a = dict(re.findall(r'(\w+)=(\S+)', m.group(5)))
        pins.append((a.get('name'), (x1 + x2) / 2, (y1 + y2) / 2, a.get('sim_pinnumber')))
    return dict(type=typ and typ.group(1), format=fmt and fmt.group(1),
                template=tpl and tpl.group(1), pins=pins)
```

- **Pins** are the `B 5` boxes (layer 5). The box centre is the connection point, and `name=` is
  the pin name.
- **`@pinlist` order**, which is the order of terminals on the netlist line, is the order of the
  `B 5` lines in the file, unless the pins carry `sim_pinnumber`, which then wins. Never assume
  D G S B; take it from the file. In sky130's `res_high_po` the box order is M, P, B.
- **`template`** gives the property names and their defaults; copy them and set the values from
  the netlist. **`format`** shows the netlist line. Check it for a model prefix that xschem adds
  (sky130 writes `sky130_fd_pr__@model`, so the schematic's `model=` holds the short name) and
  for terminals that are attributes rather than pins.
- **Substrate and bulk differ by PDK.** A three-terminal resistor may have a real bulk pin
  (sky130 `res_high_po`: pin B) or a `body=` attribute that is pasted into the pin list (IHP
  `rhigh`: `@pinlist @body`, default `sub!`). Wire a pin; set an attribute to the netlist's net
  name.
- **Device names.** Most PDK templates use `spiceprefix=X`, so xschem writes `X<name>`. Compare
  by instance name with the prefix stripped.
- **Look for standard cells before drawing logic from transistors.** In IHP sg13cmos5l the
  standard cells and the gates inside the IO cells are 1.2 V only; there is no 3.3 V logic
  library. `sg13cmos5l_LevelUp` / `LevelUpInv` (1.2 → 3.3 V) exist only as sub-cells inside
  `sg13cmos5l_IOPadInOut30mA.gds`. A 3.3 V inverter or level shifter has to be drawn.

### Worked examples (read from the symbols, 2026-10-01)

The IHP rows were confirmed by round-trip netlisting of full schematics. Of the sky130 rows,
`pfet_01v8` and `res_high_po` were confirmed by netlisting one-device schematics; `nfet_01v8` and
`cap_mim_m3_1` were only read from their symbols.

| PDK, symbol | type | pins (name: offset) in `@pinlist` order | parameter names |
|---|---|---|---|
| IHP `sg13cmos5l_pr/sg13_hv_nmos` (`_lv_`, `sg13g2_pr/` same) | nmos | D (20,−30), G (−20,0), S (20,30), B (20,0) | `w l ng m`, `model=sg13_hv_nmos` |
| IHP `sg13_hv_pmos` | pmos | S (20,−30), G (−20,0), D (20,30), B (20,0) — **source on top** | same |
| IHP `rhigh` / `rppd` / `rsil` | res | P (0,−30), M (0,30); substrate = `body=` attribute | `w l b m` |
| IHP `cap_cmomi` / `cap_cmomf` | capacitor | c0 (0,−30), c1 (0,30) | `w l mmin mmax feed` |
| sky130 `sky130_fd_pr/nfet_01v8` | nmos | D (20,−30), G (−20,0), S (20,30), B (20,0) | `W L nf mult`, prefix `sky130_fd_pr__` |
| sky130 `pfet_01v8` | pmos | D (20,30), G (−20,0), S (20,−30), B (20,0) — pin **order** D G S B, source on top | same |
| sky130 `res_high_po` | resistor | M (0,30), P (0,−30), B (−20,0) — **bulk is a pin**, order M P B | `W L mult` |
| sky130 `cap_mim_m3_1` | capacitor | c0 (0,−30), c1 (0,30) | `W L MF` |

The IHP pmos lists S before D, while the sky130 pfet lists D first, with the same geometry. That
is exactly the kind of difference that makes a hard-coded D G S B order wrong for one of them.

## Hand edits and symbol changes

The user redraws sheets and symbols by hand. His version is then the source of the drawing:
never regenerate over it, and check it by topology, not by names.

- **Moving, renaming or reordering pins in a `.sym` breaks every sheet that places it, silently.**
  xschem does not move the wires. The old wire ends either dangle (the instance is disconnected)
  or, worse, land on another pin, so that nets rotate. In this project, moving the pins of
  `d2s_mpdda_pd.sym` left `Xd` disconnected in all four power-down testbenches and put `vbpc` on
  `vbn`. After any `.sym` edit: list every `.sch` that places the symbol, **including the CACE
  templates** (`verification/cace/templates/*.sch`) and testbenches, then re-wire or regenerate
  them and check each by topology. Tell the user which sheets were affected before touching them.
- **The `.sym` pin names must equal the `ipin`/`opin`/`iopin` names in its `.sch`.** If one is
  renamed and not the other, xschem netlists without an error: the `.subckt` header takes the
  `.sym` names, and the sheet's nets of the old names float inside. Seen with `inv_3v3_pd`
  (sheet ports `a`/`y`, symbol pins `en_3v3`/`en_3v3_b`).
- **Duplicated cells.** Where the same cell exists in two places (a scratch repository and the
  delivered macros), list the duplicates and say which copy is ahead; don't replace duplicates by
  symlinks unless the user asks.
- **One cross-macro `xschemrc`.** Each macro's own `xschemrc` references only that macro. For
  interactive work across macros, one `macros/xschemrc` that adds every macro's schematic and
  testbench directory is enough; start xschem from `macros/`. Check for basename collisions
  first: with two `foo.sym` on the path, the first one wins without a warning.
- **Learn from his edits.** After he has edited a sheet you drew, compare the two versions by
  instance (position, rot, flip) and by how each pin is wired (direction of the first segment,
  stub lengths, shared verticals), render both side by side, and write the changes that recur
  into the style rules here. A one-off may be a slip: a label left behind, a title on a wire.
- **His drawing can change the netlist.** When he swaps the terminals of a symmetric device to draw
  it upright, the source netlist is changed with it; until it is, the device-by-device comparison
  fails on purpose. Report it; don't "fix" the drawing back.
- **Keep a reference snapshot** of what was delivered (sheets, symbols, CACE templates, in their
  directory layout, read-only), so hand edits can be checked against it later. If the user keeps
  the project in git but the tool container has no git, get an old commit on the host with
  `git archive <commit> <dirs> | tar -x -C <ref_dir>`, inside a directory the container can see.

## Splitting a sheet into a hierarchy (pad_ref_rb, 2026-11-07)

When a group moves out of a sheet into its own cell (the shared bias tree of vcm_rb and
vref_s2d_rb became bias_tree_rb):
1. Work on his sheet as committed (a `git archive` export), not on a regenerated one, so that the
   script can be rerun.
2. Delete the moved devices, their labels, their group boxes and titles, and every wire that lies
   entirely in the freed region. Cut a wire that spans the cut back to its new start.
3. Bring each net that came from the moved group in as an input pin in the port column, at the
   height where its bus started, so that the bus still runs straight (`vbp`, `vbnc`, `ni`).
4. Shift the rest by the freed width; move a rail when the moved group was the only thing that
   held it (vref_s2d_rb: the supply came down from −1000 to −720). Renumber the group titles in
   netlist order and replace the header text with the new netlist's header.
5. The new cell's sheet is cut from his drawing of the group, with its outputs as pins on the
   right edge at the bus heights. Fix what the cut exposes (NI's text ran into TDN's: NI moved
   next to NBP, the two gates now share a trunk).
6. The top sheet: the blocks in a row on common rails, every `vdd` up and every `vss` down by its
   own vertical. The shared lines run straight from the tree into the first block at the same
   pin heights, and over the top of that block to the next one. Of the lines that climb out of
   the bundle, the top one branches first and runs highest, so the branches don't cross each
   other (a lower line still crosses the lines above it, once each). The enable runs along the
   bottom with a riser to each block.
7. Symbols: inputs on the left in port order, outputs on the right, `vdd` on top, `vss` below,
   and `@symname` outside the box (inside, a long name ran into the `vss` pin label).
8. Check each leaf device by device, the top's instance lines (cell and nets) against the source
   subckt, and the whole hierarchy flattened against the flattened source netlists by topology.

## Verification

- Netlist each schematic with xschem in batch mode:
  `xschem --rcfile <dir>/xschemrc -n -s -q -x --no_x -o <dir>/net <dir>/<cell>.sch`
  - Use **absolute paths and set `PWD`** in the subprocess environment. xschem resolves relative
    names against `$PWD`, not against the working directory of the process. A wrong `PWD`
    silently netlists an empty schematic.
  - **Delete the old netlist first**, so that a failed run cannot be compared as if it were fresh.
  - **Don't treat the exit status as pass/fail, but read every `Error:` line.** Run with
    `--log FILE`; `-q` hides the messages. xschem 3.4.8 returns 10 both for harmless ERC notes
    (`undriven node` on testbench nets that sources in code blocks drive) and for real faults that
    no netlist comparison sees: `Unmatched subcircuit schematic pin direction: iin0 ipin <-->
    inout` (a sheet pin of another type than the symbol's pin) still writes a correct netlist.
    Check that every pin's type (ipin / opin / iopin) matches the symbol's `dir`.
  - **Missing symbols show up in the netlist, not on stderr:** search the netlist for
    `IS MISSING`. Test the search once on a sheet with a deliberately wrong library path.
  - To netlist a cell as a real `.subckt` (for comparison with a parent's view), add
    `--tcl 'set top_is_subckt 1'`.
- **Lint the geometry before netlisting:** `python3 -I sch_lint.py [-v] [--lib DIR] SHEET.sch …`
  (in this skill's folder, standard library only) rebuilds the connectivity the way xschem does
  and reports every connected group that carries two label or port names, with the join that
  separates them and every device pin lying inside one of its wires. It caught the `bt` / `m`
  short of b4cd2288 (join at (1750, −690), BA.G and BA.B inside the `m` wire) and is clean on
  d0638017. With `-v` it also lists pins inside wires elsewhere and the crossings.
- Parse xschem's netlist (`X…`/`M…`/`R…`/`C…`/`I…` lines; the `**.subckt` header gives the port
  order). xschem wraps long lines, the commented header too: join `\n+` and `\n*+` before parsing,
  or a cell with many ports (18 in bias_dist_pd) reads as having lost its last port. Compare per device: model (allowing for a prefix the `format` adds), terminal nets
  **in `@pinlist` order** mapped back to the source's terminal order, the sizing parameters, and
  the port order. Report every difference and exit non-zero if there is any.
- **Compare by topology when names may differ.** After a hand edit, internal net names and
  instance names change while the circuit does not. Flatten both netlists to primitives and test
  them for graph isomorphism with the ports anchored by name. MOS drain and source are
  interchangeable, so are the two ends of a resistor or capacitor, and the two terminal pairs of
  an E/G source swap only together (keep the polarity). Compare sizes too. A behavioural source
  (`E … value=…`) is not a linear E; don't parse it as one. Report the differences as
  "device, value, net before → net after", and list every symbol whose pins moved, were renamed
  or reordered, with the sheets that place it.
- **Build the reference netlists with the reference tree's own symbols and rc.** Netlisting an
  old sheet against the current symbols already contains the breakage you are looking for.
- **Include testbenches and CACE templates** in every check, not only the cell schematics.
- Sanity-check the checker once by changing one label in a copy and confirming that it fails.
- A source netlist may leave `m` at its default while xschem writes `m=1` on every device: add
  the default before comparing sizes, or every device differs.
- Port order: in hierarchical use, xschem takes the port order from the **`.sym`**, for both
  the instance line and the `.subckt` definition it writes. The order of pin instances in the
  `.sch` is ignored there. This was checked with xschem 3.4.4: a parent schematic was netlisted
  with the child's pins in two different `.sch` orders, and the result was identical. The `.sch`
  order matters only when the schematic is netlisted **stand-alone** as the top level; then
  xschem orders the `**.subckt` header by the order of the pin instances in the file. Deleting
  and re-placing a pin, or cut-and-paste, moves it to the end or the front. Keep the `.sym`
  equal to the source netlist (it is what parents use), and keep the `.sch` in the same order so
  that stand-alone netlists stay usable.

Reference implementations: `gen_xschem.py` (label-draft generator, IHP-specific symbol table;
replace it with a `sym_info` lookup when porting) and `check_xschem.py` (round-trip comparison by
name) in `sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/class_ab_pad_driver/`;
`scripts/xschem/sheet_equiv.py OLD_ROOT NEW_ROOT [SHEET ...]` (topology comparison of whole
trees, testbenches and CACE templates included; pure Python, no networkx) and
`macros/vcm_rb/schematic/gen_sheet.py --check SOURCE CELL NETLIST` (devices and subcircuit
instances by name) in `sg13cmos5l_cm_ip__single2diff2single`; `sch_lint.py` (geometric shorts) in
this skill's folder. The delivered reference snapshot of 2026-10-20 is in
`…_sudelbuecher/sudelbuecher/design_considerations/consolidation/reference_sheets_2026-10-20/`.

## Rendering

- Headless, with the window system faked:
  `xvfb-run -a xschem -q --rcfile <rc> --command "xschem zoom_full; xschem print svg <f>.svg; xschem exit closewindow force" <sheet>.sch`,
  then convert with cairosvg (`output_width` about 1800) and open the PNG. Without
  `zoom_full` the image can come out empty, and with xschem 3.4.8RC the shorter
  `-q -x --svg --plotfile` form gave blank images.
- Run it with `PWD` set to the sheet's directory and the same rc as for netlisting, so that the
  symbols resolve.
- At sheet scale the parameter text is unreadable; render at 6000–8000 px wide and crop regions to
  check overlaps. To study an old version, `git archive <commit> <dirs> | tar -x` into a scratch
  folder and render it from there with its own rc.

## Environment notes

- Set `PDK_ROOT` and `PDK` (for example `ihp-sg13cmos5l`, `sky130A`, `gf180mcuD`). A minimal
  project `xschemrc` that sources `$PDK_ROOT/$PDK/libs.tech/xschem/xschemrc` and appends its own
  directory is enough. Some PDKs (sky130 via open_pdks) also need their own library directory,
  such as `xschem_sky130`, on the path; check what the PDK's `xschemrc` appends.
- `devices/lab_pin.sym`-style references resolve only if `…/xschem_library` itself (not just
  `…/xschem_library/devices`) is on `XSCHEM_LIBRARY_PATH`. If labels don't name their nets,
  the netlist shows `net1, net2, …`; check the path before anything else.
- The IIC-OSIC-TOOLS container has no git and no networkx. Anything the user is to run there
  must be pure Python on the standard library. The host's `~/EDA` is `/foss/designs` inside it,
  and the container cannot see the host's `/tmp`.
- In a cloud container without the user's toolchain, `apt-get install xschem` works (3.4.4).
  PDK symbol libraries can be cloned from GitHub (IHP-Open-PDK, `dev` branch for sg13cmos5l;
  `StefanSchippers/xschem_sky130`). Rendering and netlisting work headless with `-q -x`.