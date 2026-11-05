# Stage B4 note: P's input band with vfbp / vdd swapped (F, C3, 2026-11-04)

[M] = measured in this run; everything else is reasoning. Inputs: `inputs/` with `P` = `inputs_B4/P`.

**What went in.** `src/patch_b4.py` edits stage B3's routed `s2d_block`:
- It replaces the own shapes of `s2d_inputs_c3` with the new cell's. The new cell's own shapes differ from B3's only
  on Metal1 and Via1, and its instances are the same [M]. Every other P cell in the block is XOR-identical to the
  new library [M].
- It moves outp's landing. Then `fix_block`, `build_pad` and `compose_cdl` run as in B3 (`src/run_B4.sh`).

**Reconnection: a local patch, not a reroute.**
- **vfbp (outp).** The router lands outp on the band in one place: a Via1 plus an M2 pad at x 41.16–41.45, on its
  M1 riser (pad y 133.58–137.65). The Via1 and pad move from the old vfbp track (y 136.19–136.45) to the new one
  (y 135.71–135.97), which the riser already crosses.
- **vdd** needs nothing. No block wiring lands on its track: it is joined inside the cell to the tub-end M1, and
  the block reaches iovdd there [M].
- **Nothing else moved** [M]: XOR against B3 differs only on Metal1 and Via1, all inside the band, x 5.83–50.36,
  y 135.70–136.42. That is the cell's own gate-tab change plus the moved Via1. Placement, the pad line and shields,
  vbp, vbnc, B3's y detour, the reserve and the `pwr_f` rail tie are as in B3.

**Lengths** (net_metrics, routing metal) [M]. The routing metal is unchanged, so before = after:

| net | M1 | M2 | M3 |
|---|---:|---:|---:|
| outp (vfbp) | 86.2 µm | 75.4 µm | 0 µm |
| iovdd (the cell's vdd) | 51.2 µm | 108.0 µm | 4.0 µm |

**Coupling to the pad net (vin)**, in the PEX that `checks_B.sh` runs (magic, EXT mode 2), at pad level [M]:

| pair | B3 | B4 |
|---|---:|---:|
| pad – outp | 5.729 fF | 0.371 fF (≤ 1 fF) |
| pad – iovdd | 40.23 fF | 45.59 fF |

The +5.4 fF to iovdd is the vdd track now beside vin; the lead's cell PEX predicted this. Every other pad coupling in
the top 15 is the same value in B3 and B4, and no net is new in that list [M]. Tables: `logs/coupling_lengths_B4.md`.

**Checks** (`logs/summary_B.txt`, identical to B3 apart from the PEX path) [M]: cells DRC / maximal / LVS pass, XOR as
before; pad run_drc.py clean (0 exceptions), maximal + latch-up 0, deep LVS match, circuit check EQUAL, reserve 0 µm²,
row_check 25 / 25, PEX 28 capacitor-only nodes; row DRC: run_drc.py clean, maximal + latch-up 0.

**CDL unchanged.** `pad_candidate.cdl` is byte-identical, sha256 ec55fc18348d [M]; see `netlist_changes.md` §7.

B3 is kept as `out/stageB3_v1/`. `messages.md` points 15–16 cover vdd and the inputs dir.
