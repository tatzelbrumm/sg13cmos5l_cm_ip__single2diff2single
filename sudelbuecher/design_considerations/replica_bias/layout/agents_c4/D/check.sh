#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Claude, agent D (C4): DRC (run_drc.py --no_density; maximal deck with latch-up) and LVS of one cell.
#   sh check.sh <gds> <cdl> <cell> <run dir> <log dir>
G=$(realpath "$1"); C=$(realpath "$2"); CELL=$3; mkdir -p "$4" "$5"; R=$(realpath "$4"); L=$(realpath "$5")
T=/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDK=ihp-sg13cmos5l

python3 $T/drc/run_drc.py --path="$G" --topcell="$CELL" --no_density --mp=4 --run_dir="$R/drc_$CELL" > "$L/${CELL}_run_drc.log" 2>&1 &
P1=$!
klayout -b -r $T/drc/rule_decks/sg13cmos5l_maximal.drc -rd input="$G" -rd topcell="$CELL" \
    -rd report="$R/${CELL}_maximal.lyrdb" -rd latchUpRules=true -rd thr=4 > "$L/${CELL}_maximal_lu.log" 2>&1 &
P2=$!
python3 $T/lvs/run_lvs.py --layout="$G" --netlist="$C" --topcell="$CELL" --run_dir="$R/lvs_$CELL" \
    --disable_tap_extraction > "$L/${CELL}_lvs.log" 2>&1
wait $P1 $P2
echo "$CELL run_drc.py: $(grep -oE 'No DRC violations detected|Total DRC violations.*|Violated rules.*' "$L/${CELL}_run_drc.log" | tail -1)" \
     "| exception: $(grep -ci exception "$L/${CELL}_run_drc.log")" \
     "| maximal+LU: $(grep -oE 'Number of DRC errors for maximum rule set: [0-9]+' "$L/${CELL}_maximal_lu.log" | grep -oE '[0-9]+$')" \
     "| LVS: $(grep -oE 'Netlists match|Netlists don.t match' "$L/${CELL}_lvs.log" | head -1)"
