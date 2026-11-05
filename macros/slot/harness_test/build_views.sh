#!/bin/bash
# Build the harness-test views of slot_7 from the harness slot7_wrapper.mag.
# Usage (slot repository root):  macros/slot/harness_test/build_views.sh <harness>/magic/slot7_wrapper.mag
#   1. make_slot7.py:  slot7_pins.md (pin table), final/gds/slot_7.gds, final/vh/slot_7.vh
#   2. magic:          final/lef/slot_7.lef from the GDS (as the Makefile's lef target:  -hide -pinonly 2um)
#   3. final/lib/slot_7.lib:  the same pin-less Liberty stub as the Makefile's lib target
set -e
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDK=${PDK:-ihp-sg13cmos5l}
python3 macros/slot/harness_test/make_slot7.py "$1"
mkdir -p final/lef final/lib
magic -dnull -noconsole -rcfile ${PDK_ROOT}/${PDK}/libs.tech/magic/${PDK}.magicrc << ENDMAGIC
drc off
crashbackups stop
gds read final/gds/slot_7.gds
load slot_7
lef write final/lef/slot_7.lef -hide -pinonly 2um
quit -noprompt
ENDMAGIC
rm -f slot_7.mag *.mag.orig
printf 'library (slot_7) {\n  input_threshold_pct_fall: 50.0;\n  input_threshold_pct_rise: 50.0;\n  output_threshold_pct_fall: 50.0;\n  output_threshold_pct_rise: 50.0;\n  slew_lower_threshold_pct_fall: 20.0;\n  slew_lower_threshold_pct_rise: 20.0;\n  slew_upper_threshold_pct_fall: 80.0;\n  slew_upper_threshold_pct_rise: 80.0;\n  \n  cell (slot_7) {\n  }\n}\n' > final/lib/slot_7.lib
echo "Done!"
