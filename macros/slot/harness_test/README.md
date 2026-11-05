# harness_test: slot_7 for the custom-pad integration test (plumbing demo, not a design)

`final/gds/slot_7.gds` (top cell `slot_7`) exists only to test how slot 7 and its two custom pads
go through the Chipalooza harness flow (harness fork `tatzelbrumm/sg13cmos5l_ocd_chipalooza`,
branch `custom-pad-test`, see `docs/harness_test.md`). It contains no circuit.

Generated, not drawn: `build_views.sh <harness>/magic/slot7_wrapper.mag` runs `make_slot7.py`, which
reads the pins of the regenerated harness wrapper and writes `slot7_pins.md` (the one pin table),
`final/gds/slot_7.gds` and `final/vh/slot_7.vh`; magic writes `final/lef/slot_7.lef` from the GDS;
`final/lib/slot_7.lib` is the usual pin-less stub.

| | real | stand-in |
|---|---|---|
| frame (537.15 x 273 um, harness pins on the left, supplies) | from `macros/slot/layout/klayout/slot.klay.gds`, unchanged | |
| 13 pad pins on the right edge (Metal3, positions and names of the wrapper) | yes | |
| S2D `outp` -> D2S `vinp`, S2D `outn` -> D2S `vinn` | | Metal3 stub + Via3 + vertical Metal4 line; replaces the real slot circuit's connection |
| `vref` (x2), `iref` (x2), `en_3v3` (x2), `en_3v3_b` (x2), `vcm` | | labelled stubs (Metal3 stub, Via3, Metal4 landing pad with pin and label); no bias source, level shifter or reference behind them |
| circuits (bias generator, enable logic, references) | | none |
