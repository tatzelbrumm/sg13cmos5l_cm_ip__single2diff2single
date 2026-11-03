<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Cleaned-out pad template for `sg13cmos5l_IOPadSingle2Diff` (draft for review, 2026-11-03)

IHP's `sg13cmos5l_IOPadAnalog` with its core-side plates cleared for the s2d buffer. The clean-out follows C2's
`sg13cmos5l_IOPadDiff2Single`. Top cell `sg13cmos5l_IOPadSingle2Diff`, so that phase 4 can build on it. This file is
not yet the macro's layout (`../sg13cmos5l_IOPadSingle2Diff.klay.gds`); no make target reads this folder.

| file | |
|---|---|
| `sg13cmos5l_IOPadSingle2Diff_template.gds` | the template (sha256 4b034c3ff186…) |
| `sg13cmos5l_IOPadSingle2Diff_template.png`, `IOPadAnalog.png` | renders, M3 / M4 / TM1 and their vias hidden: after and before |
| `build_template.py` | the generator: `python3 build_template.py <notes>/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/F2/out/padctx` |

## What changed against IOPadAnalog

Kept, unchanged:
- the five protection instances: `Clamp_N20N0D`, `DCNDiode`, `DCPDiode`, `Clamp_P20N0D`, `SecondaryProtection`, at
  IHP's positions;
- IOPadAnalog's own shapes in the ESD zone y ≤ 84.44: the iovdd n+ plate, the iovss p+ plate, and the pad M2;
- the ring rails on M3 / M4 / TM1 with Via3 / TopVia1;
- prBoundary 0,0 – 80,180.

Cleared, above the Clamp_P frame (y > 84.44):
- the iovss p+ plate (y 84.51–139.92);
- the three bands across the cell: n+ iovdd 148.35, p+ vss 156.85, n+ vdd 166.85, with their M2 / via ties;
- the ten pad M2 fingers to the core side, which now end at y 84.2;
- the core-side `pad` and `padres` pins at y 180.

Added:
- **C2's `nw_isolator`:** n+ in NWell on iovdd above the frame's outer p+ ring, x 2.84–77.16, y 84.79–85.09, with
  Via1 / Via2 into M3 iovdd. Its M2 stack at x 54.345 is left out, because it would touch SP's pad finger. The stacks
  at x 39.245 and 57.365 are back: C2 had left them out for its own lines.
- **C2's `edge_stubs`:** IOPadAnalog's edge intervals at both edges, each tied to its rail. The left iovdd n+ stub
  (y 148.5) is now tied like the right one, by M2 x 1.30–1.60 down to M3 iovdd. In C2 the d2s block tied it.
- **`sp_ties`,** the ties SecondaryProtection lost with the plate and the band:
  - pad: IHP's own M2 finger x 53.17–54.01, kept from the frame up to SP's pad pin (y 140.17);
  - iovss: M1 under both p+ rings, then a Via1 / M2 / Via2 stack x 55.2–58.6 into M3 iovss (y 126.4–133.7);
  - iovdd: Via1 on the n+ ring's right leg, then M2 x 59.6–60.2 down to Via2 into M3 iovdd at y 118.55;
  - `padres`: IHP's M2 line as a stub x 57.355–57.855, y 147.18–151, with a pin and text in the top cell.

## Free region for the buffer

- y 86.15–180 (above the isolator's M2), x ≈ 1.8–78.2 (inside the edge stubs).
- In it: SP (x 51.53–59.39, y 139.99–149.27) and its ties.
- Routing obstacles: the M2 pad finger (x 53.17–54.01, y 84.2–140.17), the M1 / M2 iovss stack (x 55.2–58.6,
  y 126.4–140.17), the M2 iovdd line (x 59.6–60.2, y 118.3–148) and the two left / right iovdd M2 lines in the stubs.

## Checks (notes branch, `sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_s2d/template/`)

- **IHP DRC on the template alone:**
  - `sg13cmos5l_maximal.drc` with latch-up on: 0 errors;
  - `run_drc.py --no_density`: 32 tables, no exception, "No DRC violations".
- **Row `Filler1000 | IOPadAnalog | template | Filler200 | IOPadIOVdd | template | Filler1000` (C2's `row_check.py`):**
  - the template's edge intervals are IOPadAnalog's on every layer;
  - every rail and every band is one net through the row;
  - maximal deck with latch-up and `run_drc.py` (LU.b): 0 violations.
- **Connectivity:** IHP's KLayout LVS extraction (`--disable_tap_extraction`, deep) of the template is identical to
  IOPadAnalog's, device for device and net for net, after renumbering the instances. The ports are the same as
  IOPadAnalog's.
- **Found on the way:** IHP's own IOPadAnalog does not pass IHP's KLayout LVS against IHP's
  `libs.ref/sg13cmos5l_io/spice/sg13cmos5l_io.spice`. The extraction gives `iovdd` as two nets (reasoning: the M3 / M4 / TM1
  rails 66–91.5 and 93.5–119 join only through the ring); `vss` merges with `iovss`; `vdd` has no device. The CDL
  (`cdl/sg13cmos5l_io.cdl`) doesn't even load: pin count mismatch at line 560. The template inherits the same two-net
  `iovdd`. Phase 4 has to deal with it, as C2 did with the vss / iovss merge.
