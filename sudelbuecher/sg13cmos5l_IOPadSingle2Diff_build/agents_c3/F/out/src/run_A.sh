#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F (C3) stage A: build F's changed cells, place, render.   sh run_A.sh <inputs dir> <out dir>   (PDK_ROOT=/foss/pdks)
set -e
S=$(cd "$(dirname "$0")" && pwd); I=$(cd "$1" && pwd); mkdir -p "$2"; O=$(cd "$2" && pwd)
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDK=ihp-sg13cmos5l PDKPATH=/foss/pdks/ihp-sg13cmos5l
mkdir -p "$O/cells" "$O/previews" "$O/logs"
python3 -B "$S/build_f_tails.py" "$O/cells/s2d_tails_f.gds" "$O/cells/s2d_tails_f.cdl" "$O/previews" \
    > "$O/logs/build_tails_f.txt" 2>&1
python3 -B "$S/place_A.py" "$I/template/sg13cmos5l_IOPadSingle2Diff_template.gds" "$O" "$I/P/s2d_p3_cells.gds" \
    "$I/N/s2d_n3_cells.gds" "$O/cells/s2d_tails_f.gds" > "$O/logs/place_A.txt"
R="python3 -B $S/render_A.py $O/placement_A.gds $O/placement_A.tsv"
$R "$O/previews/placement_A.png"
$R "$O/previews/placement_A_input_group.png" 0 104 80 162 "input group: tails_lo / tubs / tails_hi, R, junction channels"
$R "$O/previews/placement_A_pockets.png" 0 28 80 110 "pockets: NMOS fold left, PMOS output stage right"
$R "$O/previews/placement_A_top.png" 0 144 80 181 "top band: cload, pd_p, bias tree, core-side pin channel"
python3 -B "$S/stats_A.py" "$O/placement_A.tsv" "$I/P/s2d_p3_cells.gds" "$I/N/s2d_n3_cells.gds" > "$O/logs/stats_A.md"
