# Block-assembly patterns (process-agnostic score form)

Every pattern in three forms that say the same thing: the **score** (placement grammar, parsed by
`generator.parse_floorplan`), the **picture** (`pictures/score_*.png`, and the layer pictures of the IHP example in
`../ihp_sg13cmos5l/pictures/`), the **generator** (`generator.py`, with the score as its `FLOORPLAN`).

## 1. Vocabulary
| music term | layout operation | grammar |
|---|---|---|
| repetition (translation) | the same cell again, next in time (H) or voice (V) | sibling `cell` lines |
| retrogradation (mirror) | x reversed: right edge becomes left edge | `o=R` (= `M90`) |
| inversion | y reversed: top edge becomes bottom edge | `o=I` (= `M0`) |
| retrograde inversion (point symmetry) | both: the 180 degree point image | `o=RI` (= `R180`) |
| a voice | a row of cells between two rails or channels | a child of `V` |
| time | left to right inside a row | the children of `H` |
| a rest | reserved empty space (a routing channel) | `space w= h=` |
| the rest that closes a phrase | a tie / dummy at the end of a row | `rail ... tap=` or a tie segment |
| hocket (alternation) | two cells sharing one edge (tie, well) by exact overlap | `FREE` with the measured offset |

Edges carry meaning: a cell's pin edge must face the cell it talks to; a supply edge (tie, well, rail) faces the
same supply. The transform is chosen for the edges, not for the looks.

## 2. Grammar (exact; one node per line, indentation = nesting)
```
V  [gap=G[,G...]] [align=left|right|center]        voices, top to bottom
H  [gap=G[,G...]] [align=bottom|top|center]        time, left to right
cell <instance> [o=R0|R90|R180|R270|M0|M45|M90|M135|P|R|I|RI]
rail <net> h=<um> [tap=n|p] [thick=1] [tap_x=x0,x1[;x0,x1]]
space [w=<um>] [h=<um>]
FREE                                                children: cell <inst> o=<T> at=<x>,<y> (cell origin)
G = number (um, negative = overlap) | auto (smallest DRC-clean, short-free gap)
```

## 3. The patterns used (example: an OA reference core; measured results e.g. in IHP sg13cmos5l, see ../ihp_sg13cmos5l/)

### 3.1 v1: "islands" (what not to do)
Six primitives each with its own ring and well, placed as islands around a tall mirror; rails bridged by straps.
```
FREE
  cell mirror   o=I   at=...      # tall: sets the block height
  cell cascode  o=I   at=...      # short: leaves an empty bay above it
  cell switch_p o=RI  at=...      # own well, own ring: third well of the same supply
  cell nmir     o=P   at=...      # two rows with a tie row between them
  cell misc_n   o=P   at=...
  cell long_l   o=P   at=...      # the longest row: sets the block width
```
Picture: `pictures/score_v1.png`. Result, e.g. in IHP sg13cmos5l (see ../ihp_sg13cmos5l/rules.md): free area 18 %,
ring / enclosure bands 23 % of the block, three wells of one supply.

### 3.2 compact: "stacked voices of equal length"
```
V gap=auto,auto,auto,auto
  rail vdd h=<rail> tap=n thick=1        # the supply tie lives under the rail (free parts only)
  cell mirror o=R270                     # the matched array, its pin edge turned DOWN to its partner
  H align=top gap=auto                   # the small PMOS cells: one voice, same well as the mirror
    cell cascode
    cell ms_chain o=R90
    cell switch   o=R                    # turned so its narrow pin is reachable
  FREE                                   # hocket: two NMOS cells overlap their single tie exactly
    cell n_array at=0,0
    cell long_l  at=<dx>,<dy>
  rail vss h=<rail>
```
Rules of the pattern:
- voices of nearly equal width (here within 7 % of each other): the block is the widest voice; little is left over;
- one well for all cells of one supply: the PMOS voices abut and their wells merge (`MERGE_WELLS`);
- the matched array is a voice of its own, at the edge, so that no foreign net crosses it (`keepout`);
- pins: each voice's pin edge faces the next voice (mirror pins down to the cascodes, cascode drains down to the
  NMOS array), ports on one block edge (the right one here), next to the cells that drive them.
Picture: `pictures/score_compact.png`. Result, e.g. in IHP sg13cmos5l (see ../ihp_sg13cmos5l/rules.md): 39 % smaller
than v1, aspect 1.44, free area 10 %.

### 3.3 candidates tried (score only; the generator places each in seconds)
```
# side by side: tall mirror column | [small PMOS] / cascodes / NMOS pair     -> 7 % larger than the stacked score
V gap=auto,auto
  rail vdd h=<rail> tap=n thick=1
  H align=top gap=auto
    cell mirror o=I
    V align=left gap=auto
      H align=top gap=auto
        cell ms_chain o=R270
        cell switch
      cell cascode o=I
      FREE ...
  rail vss h=<rail>
```
The side-by-side scores lost against the stacked one because the mirror column and the right column differ in
height by 12 %: an empty strip under the shorter column. Lesson: compare the voices' lengths before routing.

## 4. Wiring patterns
- **Straight continuation** (repetition across a seam): when two cells' tracks face each other at the same pitch,
  the router's grid includes their centre lines and the connection is a straight jump with no via.
- **Point image of the wiring** (retrograde inversion): a point-symmetric array gets point-symmetric wiring by
  copying its own one-sided wiring with `Block.point_image(inst, layers, select, name)` (R180 about the well centre).
- **Landing**: on a pin narrower than the wire, land with a via from the other metal (`via_access_nodes`); on a pin
  that is a minimum-pitch track, continue it on its own centre line.
- **Keep-out with allowance**: a matched array closes its area to every net except its own.

## 5. Tie / well patterns
- One well per supply, outline = union of the cells' wells with gaps below the well space rule closed (rectilinear
  polygon, no bounding rectangle); taps: a stripe under the rail where the rail band is free, and segments in the
  array's margins where its designer computed them; latch-up checked on the whole block.
- Substrate ties: one strip shared by two abutting NMOS cells (exact overlap of their tie strips), no ring.

## 6. Bipolar core block (bg_core_pd, 2026-10-28)
Score (`pictures/score_bandgap.png`; letters: M PMOS mirror + cascodes, s switch, k startup chain, N NMOS pair +
switches, R resistor array, Q bipolar array):
```
V gap=auto
  rail vdd h=<rail> tap=n thick=1
  H align=top gap=auto
    cell s                      # next to the mirror's gate line (shortest gate net)
    cell M                      # sets the width
  H align=top gap=auto          # top-aligned: k must touch M's well
    V align=left gap=auto       # the tall column: R over Q
      cell R o=I                # inversion: its pins face Q and the strip
      cell Q
    V align=left gap=<slack>    # the MOS column; its slack against the R+Q column becomes a channel
      cell k o=R270             # hangs from M's well; tie segment in M's bottom margin
      cell N o=R                # retrograde: its gate pins under M's gate pins
  rail vss h=<rail>
```
- **Two voices of unequal length** (R+Q 31.86 um, k+N 30.14 um): the difference is a channel between k and N for the
  crossing enable, not empty space.
- **Strip beside the narrower array** (R is 6.3 um wider than Q): the core nets' channel.

Array patterns, as process-free scores:
```
bipolar 3 x 3 (unit Q1 in the centre, 8 x Q2):     resistor array, 41 segments (d dummy):
  Q2 Q2 Q2    frame (upper metal) over the top        d 0 a 0 b 0 a 0 b 0 a b 0 a 0 b 0 a 0 b a b 0 a 0 b 0 a 0 b a 0 b 0 a 0 b 0 a 0 d
  Q2 Q1 Q2 -> row, bottom row, left column, right     chains left to right, links alternately at the bottom and top
  Q2 Q2 Q2    column below the middle row; Q1 exits   head rows; 0 = 18 segments (even: both ends on top), a = 11
              right through the gap                   (odd: vss at the bottom left, its net at the top right),
                                                      b = 10 (even); levels by interval colouring (optimal for intervals): 3 per side
```
