#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F (C3) stage A checks of a run_A.sh output dir.   sh checks_A.sh <inputs dir> <out dir> <scratch run dir>
S=$(cd "$(dirname "$0")" && pwd); I=$(cd "$1" && pwd); O=$(cd "$2" && pwd); mkdir -p "$3"; W=$(cd "$3" && pwd)
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDK=ihp-sg13cmos5l PDKPATH=/foss/pdks/ihp-sg13cmos5l
T=/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech; L=$O/logs; TOP=sg13cmos5l_IOPadSingle2Diff
mkdir -p "$O/cells/logs" "$L"
sh "$S/check_cells.sh" "$O/cells/s2d_tails_f.gds" "$O/cells/s2d_tails_f.cdl" "$W/cells" s2d_tails_hi_f:no-y \
    s2d_tails_lo_f:no-y > "$O/cells/logs/summary.txt"
for c in s2d_tails_hi_f s2d_tails_lo_f; do
  mkdir -p "$O/cells/logs/$c"
  cp "$W/cells/$c/drc.log" "$W/cells/$c/maximal.log" "$W/cells/$c/lvs.log" "$W/cells/$c/sym.txt" "$O/cells/logs/$c/"
done
python3 -B "$S/row_xor.py" "$I/P/s2d_p3_cells.gds" "$O/cells/s2d_tails_f.gds" > "$O/cells/logs/row_xor_vs_P.txt"
python3 -B "$S/tpl_xor.py" "$I/template/sg13cmos5l_IOPadSingle2Diff_template.gds" "$O/placement_A.gds" \
    > "$L/template_unchanged.txt"
python3 $T/drc/run_drc.py --path="$O/placement_A.gds" --topcell=$TOP --no_density --mp=4 --run_dir="$W/drc" \
    > "$L/placement_A_run_drc.log" 2>&1
klayout -b -r $T/drc/rule_decks/sg13cmos5l_maximal.drc -rd input="$O/placement_A.gds" -rd topcell=$TOP \
    -rd report="$W/maximal.lyrdb" -rd latchUpRules=true -rd thr=4 > "$L/placement_A_maximal_lu.log" 2>&1
mkdir -p "$W/row"; python3 -B "$I/row_check.py" "$O/placement_A.gds" $TOP "$W/row" > "$W/row/stdout.txt" 2>&1
cp "$W/row/edges.md" "$L/row_check_edges.md"; cp "$W/row/nets.md" "$L/row_check_nets.md"
{ echo "cells:"; cat "$O/cells/logs/summary.txt"; tail -2 "$O/cells/logs/row_xor_vs_P.txt"; cat "$L/template_unchanged.txt"
  echo "placement run_drc.py: $(grep -oE 'No DRC violations detected|Violated rules are : .*' "$L/placement_A_run_drc.log")," \
       "tables $(grep -c 'tables selected' "$L/placement_A_run_drc.log"), lines with 'exception': $(grep -c exception "$L/placement_A_run_drc.log")"
  echo "placement maximal (latchUpRules=true): $(grep -oE 'Number of DRC errors for maximum rule set: [0-9]+' "$L/placement_A_maximal_lu.log"), LU rules listed: $(grep -c 'Rule LU' "$L/placement_A_maximal_lu.log")"
  echo "row_check: bands / rails pass $(grep -c '| pass' "$L/row_check_nets.md") of $(($(grep -c '^| ' "$L/row_check_nets.md") - 1)), edge layers DIFFERENT $(grep -c DIFFERENT "$L/row_check_edges.md")"
} > "$L/summary.txt"
cat "$L/summary.txt"
