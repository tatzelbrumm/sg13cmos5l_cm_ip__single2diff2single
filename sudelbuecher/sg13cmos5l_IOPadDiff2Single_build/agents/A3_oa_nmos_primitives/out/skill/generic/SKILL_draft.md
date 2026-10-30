---
name: rotated-row-mos-arrays
description: Process-agnostic skill for compact analog MOS primitives (current mirrors, sink / cascode rows, start-up switches) as rotated-finger rows interdigitated by rows, with Metal2 tracks drawn over the stripes, narrow strapped end dummies and tie segments only where latch-up needs them. Generator and checks take every layer, rule and device from a process adapter. Use with a process part such as ../ihp_sg13cmos5l/.
---

# Rotated-row MOS arrays (process-agnostic) [generic]

Draft, 2026-10-28, Claude (Opus 5.5), from building two NMOS primitives (a 2:1 mirror array with cascode,
start-up and power-down switches; a matched long-L pair). The process part with numbers, quirks and tools for
the first process is `../ihp_sg13cmos5l/SKILL_draft.md`.

## When to use

- A block of same-L fingers (mirror, sink row, cascode row) that must be matched (common centroid /
  interdigitated) and compact, wired in Metal1 / Metal2 only.
- Small switches of the same block that can ride in a short row's free end.
- Not for: resistor arrays, BJTs, MOS capacitors, devices whose bulk is their source (they need one well each).

## Procedure

1. **Netlist to voices.** For each device: letter, D / G / S / B nets, total W, L, finger count. Split into fingers
   of one W per voice group (keep total W and L; report every ng / w change as backannotation).
2. **Choose the row length** (fingers per row) from the target outline: rows = fingers / row length. Prefer counts
   that let a pure-row sequence be mirror-symmetric (2:1 -> `A B A` per period, 9 rows; 1:1 -> `A B B A`).
3. **Write the score** (`patterns.md` syntax): rows bottom first, end rests `d ... d`, voices, and the `sym` / `cc`
   claims. Run `python3 generator.py patterns.md` or `check_score()`; fix the score until every claim holds.
4. **Pick the lines:** S on line B, D on line T for every row (one current direction). A line must carry one net
   per contiguous run; if a row mixes nets on a line, split the row or accept a two-track band (older style).
5. **Sides:** dummy strap (net of the dummies: the bulk, or the row's gate net for Vgs = 0, `rules.md` 28; then
   the supply needs its own path), gate bar per gate net, one joiner per net that has tracks in several
   rows; decide which side each net's tracks end on (`ext` in `Block.line_tracks`).
6. **Ties:** one contact row, on the side(s) that bring every N+ active within the latch-up distance; segments
   follow the outline; contacts on a grid anchored at an edge shared with the neighbour. Check the stack limit
   first (`rules.md` 19): a stack taller than the latch-up distance gets a second segment on the far side, never
   one between rows; join every segment to the supply in metal.
6a. **Matched pairs (pattern P4):** stack `A B B A` with the retrograde half flipped (S on top), sources out on
   opposite sides and back on one lane to two pins side by side on the array's centre line (`rules.md` 20-23).
7. **Extras / coda:** small devices in the free end of a short row; tabs to that row's lines.
8. **Outlines:** thick oxide / implant / well as grown-and-closed polygons (`outline()`).
9. **Pins:** one per net on an edge, pin box + label.
10. **Check:** DRC (0 or listed), LVS (match, devices as drawn incl. dummies), the latch-up distance per tie
    segment, the device cells identical to the library, byte-reproducible build. Inject a few faults (delete the
    tie, move a row by a few grid steps, remove a via) to prove the checks see them.
11. **Pictures** from the GDS (`render.py`): the tile with letters and track names, before / after at one scale,
    the rule picture.

## Using the generator

```python
import klayout.db as db, generator as g, adapter            # adapter = the process part's module
P = adapter.Process(); lib = db.Layout(); lib.read("<device library>.gds")
ly = db.Layout(); ly.dbu = lib.dbu; cx = g.Ctx(P, ly)
fing = g.Mos(cx, g.copy_cell(lib, adapter.DEVICES["<key>"][0], ly), "<model>")
top = ly.create_cell("<block>"); blk = g.Block(cx, top)
score = g.parse_score(open("<score>.txt").read()); assert all(c[1] for c in g.check_score(score))
for k, (name, letters) in enumerate(score["rows"]):
    blk.add_row(name, letters, {l: fing for l in set(letters)}, 0.0, k * (fing.lact + cx.r("active_space")))
# then: g.strap(), g.gate_contacts(), blk.vertical(...), blk.line_tracks(...), g.tie(), g.outline(), blk.wire()
```

Complete uses: `../../build_oa_n.py` (patterns P1, P2, P3) and `../../../out_bg/build_bg_n.py` (P4 + coda, two
tie segments); block-specific parts are the score, the voices, the coda and the side assignment of each net.

## Pattern notation

`patterns.md`: repetition (translation), retrogradation (mirror), retrograde inversion (point symmetry),
alternation / hocket (interdigitation), rests (end dummies), coda (extras). Roles in a picture:
`pictures/tile_roles.png`.

## Pitfalls

`rules.md`, items 15-18 and 25-26 (narrow via tabs, timestamps, L-shaped labels, small-device baselines, the M1
area of a single-via pad, a full-width top row without a free end), plus:
mixing nets on one line (forces a band); placing the gate bar inside the strap (the strap must be innermost,
it ties the dummies' stripes that end next to the bar); forgetting that a tie next to the W-end of an unrotated
device needs the implant-to-gate distance, not the active space.

## Porting to another process

Fill a copy of `adapter_template.py`. For each field, where to look and how to verify:

| adapter field | where in a new PDK | verify |
|---|---|---|
| `LAYERS` | layer map / layer properties file, DRC deck layer definitions | draw one of each, read it back by name |
| `ANGLES` | DRC angle / grid rules | a 45-degree test polygon per layer through DRC |
| rules `finger_gap`, `poly_*`, `active_space` | DRC deck: gate-to-gate over active for the device class, poly space, endcap, active space | self-test row: two fingers at `finger_gap` pass, at `finger_gap` - grid fail |
| `cont*`, `polycont_to_active` | contact rules | gate contact column of a row passes DRC |
| `m1_*`, `via1*`, `m2_*` (incl. endcap enclosures) | metal / via rules; endcap ("line-end") rules may live only in the deck text | 3-via pad and a via at a narrow tab end pass |
| `tie_impl_enc`, `impl_to_*` | implant rules; implant-to-gate for the device class | tie under a rotated row and beside an unrotated W-end |
| `thickox_*` | thick-oxide (HV device) rules, merge distance | outline of a 2-row array |
| `lu_ptie`, `lu_ntie`, `tie_cont_ext_max` | latch-up rules (often a separate deck file) | delete the tie of a self-test array: the check must fire |
| `well_*` | well rules (same / different net, enclosures, spacings in HV) | only if a well is drawn |
| `DEVICES` | the PDK's PCell library: export the variants you need; confirm the cell frame (gate vertical, two M1 stripes) | `Mos()` measures active, poly, stripes; XOR against the library |
| `LVS` | LVS deck: device recognition layers, terminal derivation, bulk; tie handling | self-test cell: LVS match with dummies in the reference |
| `PEX` | extraction rules: sheet R and C per layer; what is extracted | decide track width / sharing; nothing in the generator depends on it yet |
| `MODEL` | model cards: L / W / nf ranges, binning | finger width inside the characterized range |

Check tools: DRC and LVS of the target PDK, run on a self-test cell (two rows, a strap, a gate bar, a joiner, a
tie) before the real block; if the official decks cannot run, write a subset checker and prove it by injecting
faults (see the IHP part for one).
