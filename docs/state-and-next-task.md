<!-- Moved verbatim from CLAUDE.md (blob 6201ab3, commit 1903407). Read only when the task needs it. -->

# Verified state and next task

## 7. State and next task

**Verified working, all on the current `main`:**

- rename complete and consistent
- tapeout GDS re-exported from `.klay.gds`, geometry verified unchanged
- Magic DRC clean, KLayout DRC clean, Magic+Netgen LVS "Circuits match uniquely"
- full-RC PEX, all ports connected
- top-level transient simulated
- inverter: three testbenches + CACE characterization
- counter: lint → Icarus → cocotb → LibreLane (all eight checkers clear) → PEX →
  gate-level cocotb → XSPICE co-simulation in Xschem

**Next: replace the template example modules with the real design.** The teardown
touches more than `macros/`:

- `macros/inverter/`, `macros/counter/`
- top `Makefile` — `build-inverter`, `build-counter`, `build-macros`, `clean-*`
- `schematic/xschem/xschemrc` — sources both macro `xschemrc` files
- `layout/<TOP>.klay.klib` — binds library `inverter` → `../macros/inverter/layout/inverter.gds`
- `schematic/xschem/<TOP>.sch` — 2 × `inverter.sym`
- `layout/<TOP>.klay.gds` — 2 × `inverter` placements, **needs KLayout**, then re-export
- `testbenches/xschem/<TOP>_tb_tran.sch` — DUT and stimulus
- `submission.yaml` (still has `TODO` fields, and `analog-pins: 3` is inherited)
- `README.md`

Re-run the full sign-off after any layout change; the committed outputs are the
reference to diff against.

**Also still open:** the mixed-signal path for the I/O-limited design will need digital
logic and level shifters. The mechanism is `generate-xspice` — LibreLane hardens the
block, `magic-pex` extracts it, and the XSPICE model drops into an Xschem testbench
beside the analog. Verified working with the counter.
