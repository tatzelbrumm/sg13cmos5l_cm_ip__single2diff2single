<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Patterns: score form

2026-10-28, Claude (Opus 5.5). Three compact PMOS primitives written as scores [generic]. The instance built
from them (IHP sg13cmos5l) is `../ihp_sg13cmos5l/examples/oa_p_cells.gds`. `generator.py` reads the
```` ```score ```` blocks below (`parse_scores()`) and `example_build.py` builds the cells from them. The scores are
data, not illustrations.

## Vocabulary

| layout operation | musical term | in the score |
|---|---|---|
| translation, an array of one cell (AREF) | repetition | the same letter in consecutive columns |
| mirror about a vertical axis | retrogradation | a row read right to left |
| point symmetry (R180) | retrograde inversion | rows read bottom-up and right to left; `symmetry R180` |
| interdigitation of two devices | alternation (hocket) | letters alternating along a row (`o 8 o`), or links alternating bottom / top (`_ ^ _`) |
| end dummy | the rest that closes a phrase | `d` at both row ends, `drain=rest` |
| voice | one device / net and the layer that carries it | `voice <letter> ...` lines, track lists |

## Notation (what `parse_scores()` reads)

```
stack | chain | single <cell name>          one block per cell, closed by `end`
  key value ; key value                     header: nets, tracks, pins (key with several values = a list)
  voice <letter> <device name> <kind> <w> <l> [drain=<net>|rest]
                                            kind = adapter device kind; rest = dummy, D = S (strapped)
  | <letters> |                             one row of fingers, top row first; columns line up
  symmetry R180 swap <a> <b>                the R180 image of the matrix is the matrix, with a <-> b
  links _ ^ _ ...                           chain: series links at the bottom (_) or top (^) of each finger pair
end
```

Fingers are placed R270: the channel length runs vertically, texts upright. Every row is one or more AREFs of the
device cells (repetition). In a `stack`, rows pair up around a Metal2 track band: rows 1 and 3 have their drains at
the bottom, rows 2 and 4 at the top. Rows 2 and 3 share a source plate.

## oa_pmir_c: retrograde inversion, two bands

```score
stack oa_pmir_c
  src vdd ; gate vpg ; bulk nw ; pin_band -1
  tracks co c8 c2 vpg          # from the centre line outwards; gate outermost
  voice o PO     pmos_hv 2   8 drain=co      # output, weight 20
  voice 8 P8     pmos_hv 2   8 drain=c8      # weight 8
  voice 2 P2     pmos_hv 2   8 drain=c2      # weight 2
  voice 1 P0     pmos_hv 2   8 drain=vpg     # unit, diode: D = G
  voice x dummy  pmos_hv 2   8 drain=rest    # P0's point partner, full width
  voice d dummyn pmos_hv min 8 drain=rest    # end rest: one S/D contact wide (min)
  | d o o o 8 o o 8 o d |
  | d o 8 o 1 2 8 o o d |
  | d o o 8 2 x o 8 o d |
  | d o 8 o o 8 o o o d |
  symmetry R180 swap 1 x
end
```

- **Rows 4 and 3 are rows 1 and 2 played backwards and upside down** (retrograde inversion, R180 about the array
  centre). Only P0 (`1`) and its partner `x` trade places: 31 real fingers on 32 positions leave no centre cell.
- **Counts** (one finger = 2/8): `o` (PO) 20, `8` (P8) 8, `2` (P2) 2, `1` (P0) 1, `x` 1, `d` 8. The digits are the
  mirror weights.
- **Repetition:** every row is `d` + an AREF of 8 equal 2/8 fingers + `d`. The letters say only which drain track
  each finger joins.
- **Voices on lanes (Metal2 tracks):** each band carries all four nets, inner to outer: `co c8 c2 vpg`.
  - band A (between rows 1 and 2), bottom to top: `co c8 c2 vpg`;
  - band B (between rows 3 and 4), bottom to top: `vpg c2 c8 co`, the point image.
  - Lower row of a band: drain tab at the column's left edge. Upper row: at its right edge (2 Via1 each).
- **Staircase (left edge):** co, c8 and c2 join band A to band B on vertical Metal2 lines, the outermost net on the
  outermost line. vpg needs no line: the Metal1 gate columns along both row ends carry it, with one Via1 per band.
- **Supply (Metal1):** top and bottom plates run to the cell edge, rows 2 and 3 share a plate, and the end-column
  dummies' straps continue through the bands. That makes one vdd path with no tap and no side rail.
- **Pins:** co c8 c2 vpg on Metal2 at the right edge, band B. vdd on Metal1 at the bottom edge.

## oa_ms1: repetition with alternating links

```score
chain oa_ms1
  src vdd ; end ks ; gate en_3v3_b ; bulk nw ; inner ms%d
  voice S MS1 pmos_hv 0.5 12.5
  | S S S S S S S S |
  links _ ^ _ ^ _ ^ _          # ms1 bottom, ms2 top, ... ms7 bottom
end
```

- Eight equal fingers in one AREF, with one merged gate strip (en_3v3_b).
- The series path alternates bottom / top links (hocket): vdd enters at finger 0 top and ks leaves at finger 7 top.
- Gate contact column at the left end. Pins: vdd and ks on the top edge, en_3v3_b on the left edge.

## oa_svpg: a single note

```score
single oa_svpg
  s vdd ; d vpg ; g en_3v3 ; bulk nw
  voice W SVPG pmos_hv 1 0.45
  | W |
end
```

- One finger. S on the top edge, D on the bottom edge, gate contact and pin on the right.

## bg_pmir_pcas_c: mirror + cascode stack, retrograde inversion

```score
cstack bg_pmir_pcas_c
  src vdd ; gate vpg ; cgate vpc ; bulk nw
  mtracks co vpg ca            # over every mirror row, from its drain side; gate in the middle (on the pad)
  ctracks iout vpc g           # over every cascode row
  lines_left vpg co ca         # Metal1 side lines, inner to outer
  lines_right vpc g iout
  pins vpg:B vpc:B g:B iout:R vdd:T
  voice o PO     pmos_hv 10  1 drain=co  cdrain=iout cname=POC   # weight 2 (8 fingers)
  voice b PB     pmos_hv 10  1 drain=vpg cdrain=vpc  cname=PBC   # diode pair (4)
  voice a PA     pmos_hv 10  1 drain=ca  cdrain=g    cname=PAC   # (4)
  voice d dummyn pmos_hv min 1 drain=rest                        # end rest, one S/D contact wide
  | d o b a o d |              # mirror rows only, top first; each pair (Ma, Mb) becomes Ma Ca Cb Mb,
  | d a o o b d |              # Ca / Cb = the cascodes with the same letters (C = repetition of M)
  | d b o o a d |
  | d o a b o d |
  symmetry R180
end
```

- **Voices on two levels.** The mirror (o b a) and its cascodes (O B A, read from the same letters) stand in the
  same columns, one row apart. The mirror's drain and the cascode's source are one node, joined in Metal1 across
  the 0.21-class diffusion gap.
- **Rows:** `Ma Ca Cb Mb | Ma Ca Cb Mb`. Mirror rows face the cell edges and share the middle source plate; cascode
  rows face each other with their drains.
- **Retrograde inversion:** the 8-row stack is its own R180 image (rows 1 <-> 8, 2 <-> 7, ...), without a swap.
- **Latin square.** Every row and every column of the mirror holds one b, one a and two o (counts 4 : 4 : 8). A
  linear gradient in x or y cancels per row and per column, not only at the centroid.
- **Lanes:** three Metal2 tracks over every row's own channel (co vpg ca over the mirror, iout vpc g over the
  cascodes), with no band between rows. Every finger has the same tab (the same metal over every matched channel);
  only its via chooses the lane.
- **Side lines (Metal1):** vpg co ca on the left, vpc g iout on the right. Pins: vpg, vpc, g on the bottom edge;
  iout on the right edge; vdd on the top plate.

## bg_ms1, bg_svpg: the chain with its pins moved

```score
chain bg_ms1
  src vdd ; end ks ; gate en_3v3_b ; bulk nw ; inner ms%d ; gate_pin B ; end_pin B
  voice S MS1 pmos_hv 0.5 12.5
  | S S S S S S S S |
  links _ ^ _ ^ _ ^ _          # ks leaves finger 7's top along a line inside the right well margin
end
single bg_svpg
  s vdd ; d vpg ; g en_3v3 ; bulk nw
  voice W SVPG pmos_hv 1 0.45
  | W |
end
```

- Same devices as oa_ms1 / oa_svpg. bg_ms1 brings ks and en_3v3_b to the bottom edge inside the same 0.62 well
  margin, so the outline is unchanged.

## From the OA core to the bandgap core (what carried over)

- Unchanged:
  - one-contact rests;
  - no tap inside, the well to every edge, the parent's tap segment checked against the latch-up distance;
  - point symmetry checked by XOR (score and layout);
  - pins on the edges the assembler names.
- Changed for short L (1 instead of 8): no track bands. The lanes run over each row's own channel, the cascodes
  sit in their own rows with their mirror's letters (`cstack`), and the map is a Latin square as well as R180.
- The chain and the single are the same scores. Only the pins move (`gate_pin B`, `end_pin B`).
