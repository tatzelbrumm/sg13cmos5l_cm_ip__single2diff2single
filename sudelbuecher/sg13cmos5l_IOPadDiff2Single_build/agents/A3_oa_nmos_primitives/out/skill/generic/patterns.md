<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Patterns: score form (process-agnostic) [generic]

2026-10-28, Claude (Opus 5.5). Three forms say the same thing: this score, the pictures (`pictures/`, and with
process numbers `../ihp_sg13cmos5l/pictures/`), and `generator.py` (which parses the scores below with
`parse_score()` and checks every `sym` / `cc` claim with `check_score()`).

## Vocabulary

| layout | music | in a score |
|---|---|---|
| translation (repetition of a finger / row) | repetition | `A A A`; rows repeated: `translate_y=<k>` |
| mirror | retrogradation | row reads the same backwards: `sym mirror_x`; row sequence: `sym mirror_y` |
| point symmetry | retrograde inversion | `sym point` |
| interdigitation | alternation (hocket) | voices take turns, here by rows: `A B A A B A A B A` |
| end dummy | the rest that closes a phrase | `d ... d` at both row ends |
| devices appended in a short row's free end | coda | `extras:` (drawn by hand, listed after the row) |

A **voice** is a device: its letter, its S / D / G / B nets, and so the Metal2 tracks it sits on. A **line** is one
stripe row of a finger row: line B = the bottom stripes, line T = the top stripes. Convention used throughout:
S on line B, D on line T (all rows the same current direction).

## Score syntax (parsed by `generator.parse_score`)

```
row   <name> : <letter> <letter> ...            # rows bottom first, fingers left to right
voice <letter> = <device> D=<net> G=<net> S=<net> B=<net>
sym   mirror_y|mirror_x|point|translate_y=<k> rows=<first>-<last>
cc    <letter>,<letter> rows=<first>-<last>     # these voices share one centroid
```

## P1. Pure-row alternation (the 2:1 mirror array, e.g. block `oa_n10`)

```
row X0 : d A A A d
row X1 : d B B B d
row X2 : d A A A d
row X3 : d A A A d
row X4 : d B B B d
row X5 : d A A A d
row X6 : d A A A d
row X7 : d B B B d
row X8 : d A A A d
row Y  : e C S e          # extras: MS3 SKS (coda in the free end of row Y)
voice A = M10   D=d10 G=vnc S=vres B=vss
voice B = M11   D=vnc G=vnc S=vss  B=vss
voice C = MC10  D=vpc G=vbr S=d10  B=vss
voice S = MS2   D=ks  G=vbr S=vss  B=vss
voice d = dummy D=vss G=vnc S=vss  B=vss
voice e = dummy D=vss G=vbr S=vss  B=vss
sym mirror_y rows=X0-X8
sym mirror_x rows=X0-X8
sym point    rows=X0-X8
cc  A,B      rows=X0-X8
```

- Generators: repetition along x (`A A A`, one array instance per row), alternation along y with period
  `A B A`, and retrogradation of the whole row sequence (`mirror_y`). Every row is its own retrograde
  (`d ... d`), so the matrix is also point symmetric. Centroids (finger index, row index): A (2, 4), B (2, 4).
- Second moments about the centre row: A 7.0, B 6.0 (rows²). B at rows {1, 4, 7} balances them best among the
  symmetric choices ({0,4,8}: 4.7 / 10.7; {2,4,6}: 8.7 / 2.7).
- Voices on lines and Metal2 lanes (one track per line, drawn over the stripes):

  | row type | line B (S) | line T (D) | gate bar | track ends at |
  |---|---|---|---|---|
  | A rows | vres | d10 | vnc | vres: right joiner; d10: left joiner |
  | B rows | vss | vnc | vnc | vss: both dummy straps; vnc: both gate bars |
  | Y row | d10 (C) / vss (S) | vpc (C, lifted to an extra lane above) / ks (S) | vbr (left only) | d10: left joiner; vss: right strap |

- Why pure rows: a line that carries one net per run needs one track and no band, so rows stack at the
  minimum active space. A row mixing A and B would carry two nets per line and need a band of two tracks
  between rows (the older "band" style).

## P2. Stacked matched pair with a merged gate (e.g. block `oa_mcs_c`)

```
row r0 : S                # one long-L finger per row, gate along x (no rotation), rows at the finger gap
row r1 : L
voice S = MCS D=vbr  G=vbr S=vss B=vss
voice L = MCL D=vres G=vbr S=vss B=vss
```

- Symmetry: none in the voice matrix (one finger per voice); the repetition is of the device cell, not of the
  voice, so no `sym` claim is made.

- Generator: repetition in y at the finger gap (one 1 x 2 array instance); the gate polys merge into one plate.
- Lines are vertical here (S stripes left, D stripes right); the sources join in one Metal1 strap to the tie, the
  two drains leave on the right.

## P3. Coda: small devices in the free end of a short row

`row Y : e C S e` is two fingers shorter than the array rows. The free end takes the small switches (MS3, SKS),
which share the row's lines: their sources join the vss track of line B, the drain of SKS and the gate of MS3 join
the ks track of line T, MS3's drain joins the vpc lane above. No cell outline, no extra spacing.

## P4. Mirrored pair stack with inverted current direction (the matched pair NA / NB, block `bg_n4`)

```
row R0      : d A d
row R1      : d B d
row R2 flip : d B d
row R3 flip : d A d
row Y  flip : e S         # extras: MS3 SKS (coda in the free end of row Y)
voice A = NA    D=g   G=g S=ea  B=vss
voice B = NB    D=vpc G=g S=eb  B=vss
voice S = MS2   D=ks  G=g S=vss B=vss
voice d = dummy D=g   G=g S=g   B=vss     # Vgs = 0 (rules.md 28); version 1 had D = S = vss
voice e = dummy D=g   G=g S=g   B=vss
sym mirror_y_orient rows=R0-R3
sym mirror_x        rows=R0-R3
cc  A,B             rows=R0-R3
```

- Generators: `A B` followed by its retrograde `B A` (retrogradation in y), and the retrograde half plays with the
  current direction inverted (`flip`: S on the top line). Each voice has one finger of each direction, so a
  direction-dependent error cancels inside each device; linear gradients in x and y cancel (common centroid).
- Voices on lines (S / D by orientation):

  | row | line B | line T | leaves on |
  |---|---|---|---|
  | R0 (A) | ea | g | ea: left joiner; g: both gate bars |
  | R1 (B) | eb | vpc | eb: right joiner; vpc: left outer column |
  | R2 (B, flip) | vpc | eb | as R1 |
  | R3 (A, flip) | g | ea | as R0 |
  | Y (S, flip) | ks | vss (plate up to the far tie) | ks: right, to the coda and the ks riser |

- The two sources leave on opposite sides (ea left, eb right) and come back on one lane at the bottom edge, meeting
  at the array's centre line: the two source paths are mirror images (same lengths, same via counts), and the two
  pins sit next to each other on that centre line.
- Rows R1 and R2 face each other with the same net (vpc) on both facing lines.
- Every finger of the pair sees the minimum active space above and below (tie, neighbour row, row Y): the same
  active-edge environment for all four fingers.
- Why not a 2 x 2 cross-quad `A B / B A`: with one finger per voice per row the lines are pure only if each row
  holds one voice; a cross-quad needs two fingers per row and, with the finger widths available, a cell about
  25 % wider than requested (e.g., in IHP sg13cmos5l see ../ihp_sg13cmos5l/rules.md, item 22).

## Transfer: the next blocks

- `bg_nab`: drawn as P4 (block `bg_n4`, with `bg_misc_n` as its row Y + coda).
- Any 1:1 matched pair whose devices share the gate: P4. Any n:1 mirror: P1 with the row sequence chosen for equal
  second moments.
