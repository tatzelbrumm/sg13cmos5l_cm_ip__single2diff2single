#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F2 stage A: rebuild the reworked cells, the pad context (rejected F's stage-2 pad-top cells) and the placement.
#   sh run_A.sh <out_dir>        (src/ next to this script; needs PDK_ROOT=/foss/pdks)
set -e
S=$(cd "$(dirname "$0")" && pwd); O=$1
P2=/home/user/sudel/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/P2/out/d2s_p2_cells.gds
mkdir -p "$O/cells" "$O/padctx" "$O/previews"
python3 -B "$S/build_f2_n.py" "$O/cells/d2s_f2_n_cells.gds" "$O/cells/d2s_f2_n_cells.cdl"
python3 -B "$S/build_f2_p.py" "$O/cells/d2s_f2_p_cells.gds" "$O/cells/d2s_f2_p_cells.cdl"
python3 -B "$S/build_f2_sp.py" "$O/cells/d2s_f2_sp_cells.gds" "$O/cells/d2s_f2_sp_cells.cdl"
python3 -B "$S/src_F/build_pad.py" "$O/padctx/pad_ctx.gds" "$O/padctx"
python3 -B "$S/place_A.py" "$O/padctx/pad_ctx.gds" "$P2" "$O/cells/d2s_f2_p_cells.gds" "$O/cells/d2s_f2_n_cells.gds" \
    "$O/cells/d2s_f2_sp_cells.gds" "$O"
python3 -B "$S/render_A.py" "$O/placement_A.gds" "$O/placement_A.tsv" "$O/previews/placement_A.png"
