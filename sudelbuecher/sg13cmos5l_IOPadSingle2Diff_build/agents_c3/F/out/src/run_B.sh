#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F (C3) stage B: build the changed cells, the routing context, the routed block and the pad candidate with its CDL.
#   sh run_B.sh <inputs dir> <stage-A out dir (s2d_tails_f)> <out dir>
set -e
S=$(cd "$(dirname "$0")" && pwd); I=$(cd "$1" && pwd); A=$(cd "$2" && pwd); mkdir -p "$3"; O=$(cd "$3" && pwd)
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDK=ihp-sg13cmos5l PDKPATH=/foss/pdks/ihp-sg13cmos5l FCELLS="$O/cells" FINPUTS="$I"
mkdir -p "$O/cells" "$O/logs"
python3 -B "$S/build_f_tails.py" "$O/cells/s2d_tails_f.gds" "$O/cells/s2d_tails_f.cdl" > "$O/logs/build_tails_f_B2.txt" 2>&1   # stage B2: rebuilt (right vbp stub only)
python3 -B "$S/build_f_casc_n.py" "$I/N/s2d_n3_cells.gds" "$I/N/s2d_n3_cells.cdl" "$O/cells/s2d_casc_n_f.gds" "$O/cells/s2d_casc_n_f.cdl" > "$O/logs/build_cells.txt"
python3 -B "$S/build_f_pins.py" "$I/P/s2d_p3_cells.gds" "$I/P/s2d_p3_cells.cdl" "$O/cells/s2d_pins_f.gds" "$O/cells/s2d_pins_f.cdl" >> "$O/logs/build_cells.txt"
python3 -B "$S/strip_tub_labels.py" "$I/P/s2d_p3_cells.gds" "$O/cells/p3_router.gds"
python3 -B "$S/make_ctx.py" "$I/template/sg13cmos5l_IOPadSingle2Diff_template.gds" "$O/cells/padctx_f.gds" >> "$O/logs/build_cells.txt"
python3 -B "$S/make_pwr.py" "$O/cells/pwr_f.gds" >> "$O/logs/build_cells.txt"
python3 -B "$S/route_block.py" "$S/block_cfg.py" "$O/cells/s2d_block.gds" > "$O/logs/route.txt" 2>&1
python3 -B "$S/fix_block.py" "$O/cells/s2d_block.gds" >> "$O/logs/route.txt"
python3 -B "$S/build_pad.py" "$I/template/sg13cmos5l_IOPadSingle2Diff_template.gds" "$O/cells/s2d_block.gds" "$O/pad_candidate.gds" > "$O/logs/build_pad.txt"
python3 -B "$S/compose_cdl.py" "$S/block_cfg.py" "$O/pad_candidate.cdl" "$I/P/s2d_p3_cells.cdl" "$I/N/s2d_n3_cells.cdl" \
    "$O/cells/s2d_tails_f.cdl" "$O/cells/s2d_casc_n_f.cdl" "$O/cells/s2d_pins_f.cdl" >> "$O/logs/build_pad.txt"
grep -E "failed:|fix_block" "$O/logs/route.txt"
