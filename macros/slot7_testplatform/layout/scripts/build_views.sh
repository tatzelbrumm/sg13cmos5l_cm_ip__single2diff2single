#!/bin/bash
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Build the slot_7 views of the test platform (design repo root, after `export PDK_ROOT=/foss/pdks; source .designinit`):
#   macros/slot7_testplatform/layout/scripts/build_views.sh <base slot_7.gds> [--pads foundry] [--stage-b]
#   1. make_slot_7.py: final/gds/slot_7.gds from <base> (the delivery slot_7.gds: frame + 13 custom-pad pins)
#   2. magic: final/lef/slot_7.lef (as the slot Makefile's lef target: -hide -pinonly 2um), duplicate PIN blocks merged
#   3. final/lib/slot_7.lib: the pin-less Liberty stub; final/vh/slot_7.vh: the port list (unchanged by the platform),
#      both copied by the caller from the delivery (the platform adds no port)
set -e
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDK=${PDK:-ihp-sg13cmos5l}
D=macros/slot7_testplatform
mkdir -p $D/final/gds $D/final/lef
python3 $D/layout/scripts/make_slot_7.py "$1" $D/final/gds/slot_7.gds "${@:2}"
cd $D
magic -dnull -noconsole -rcfile ${PDK_ROOT}/${PDK}/libs.tech/magic/${PDK}.magicrc << ENDMAGIC
drc off
crashbackups stop
gds read final/gds/slot_7.gds
load slot_7
lef write final/lef/slot_7.lef -hide -pinonly 2um
quit -noprompt
ENDMAGIC
rm -f *.mag *.mag.orig
python3 layout/scripts/lef_merge_pins.py final/lef/slot_7.lef
echo "Done!"
