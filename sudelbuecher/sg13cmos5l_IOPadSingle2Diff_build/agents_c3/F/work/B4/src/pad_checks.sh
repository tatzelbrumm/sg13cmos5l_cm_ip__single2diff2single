#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F (C3) stage B: DRC (run_drc.py + maximal with latch-up) and deep LVS of the pad candidate.
#   sh pad_checks.sh <out dir> <run dir>
O=$(cd "$1" && pwd); mkdir -p "$2"; R=$(cd "$2" && pwd); S=$(cd "$(dirname "$0")" && pwd)
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDKPATH=/foss/pdks/ihp-sg13cmos5l
T=/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech; TOP=sg13cmos5l_IOPadSingle2Diff; L=$O/logs
python3 $T/lvs/run_lvs.py --layout="$O/pad_candidate.gds" --netlist="$O/pad_candidate.cdl" --topcell=$TOP \
    --run_dir="$R/lvs" --run_mode=deep --disable_tap_extraction > "$L/pad_lvs.log" 2>&1 &
LP=$!
python3 $T/drc/run_drc.py --path="$O/pad_candidate.gds" --topcell=$TOP --no_density --mp=4 --run_dir="$R/drc" \
    > "$L/pad_run_drc.log" 2>&1
klayout -b -r $T/drc/rule_decks/sg13cmos5l_maximal.drc -rd input="$O/pad_candidate.gds" -rd topcell=$TOP \
    -rd report="$R/maximal.lyrdb" -rd latchUpRules=true -rd thr=4 > "$L/pad_maximal_lu.log" 2>&1
wait $LP
cp "$R"/lvs/*.lvsdb "$L/pad_candidate.lvsdb" 2>/dev/null; cp "$R"/lvs/*_extracted.cir "$L/pad_candidate_extracted.cir" 2>/dev/null
python3 -B "$S/lvs_report.py" "$L/pad_candidate.lvsdb" > "$L/pad_lvs_report.txt" 2>&1
{ echo "run_drc.py: $(grep -oE 'No DRC violations detected|Violated rules are : .*' "$L/pad_run_drc.log"), tables $(grep -c 'tables selected' "$L/pad_run_drc.log"), 'exception' lines $(grep -c exception "$L/pad_run_drc.log")"
  echo "maximal + latch-up: $(grep -oE 'Number of DRC errors for maximum rule set: [0-9]+' "$L/pad_maximal_lu.log"), LU rules listed $(grep -c 'Rule LU' "$L/pad_maximal_lu.log")"
  echo "LVS (deep, --disable_tap_extraction): $(grep -oE 'Netlists match|Netlists don.t match' "$L/pad_lvs.log" | head -1)"; } > "$L/pad_checks.txt"
cat "$L/pad_checks.txt"
